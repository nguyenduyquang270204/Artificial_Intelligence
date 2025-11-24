# ===============================
# IMPORTS
# ===============================
import cv2
import numpy as np
from random import randint

# ===============================
# CLASS: Block
# ===============================
class Block:
    def __init__(self, i, j):
        self.value = None
        self.pos = (i, j)

    def setValue(self, value):
        self.value = value


# ===============================
# CLASS: GUI (Game)
# ===============================
class GUI:
    def __init__(self, windowName):
        self.windowName = windowName
        self.width, self.height = 400, 400
        self.menuHeight = 100
        self.image = np.zeros((self.height + self.menuHeight, self.width, 3), np.uint8)
        self.turn = 1
        self.vsCom = 0
        self.reset()

    # ---------------------------
    # Reset Game
    # ---------------------------
    def reset(self):
        self.blocks = []
        self.win = False
        self.change = True
        self.selected = False

        for i in range(3):
            row = []
            for j in range(3):
                block = Block(i, j)
                start = (j * (self.width // 3) + 3, i * (self.height // 3) + 3)
                end = ((j + 1) * (self.width // 3) - 3, (i + 1) * (self.height // 3) - 3)
                row.append([block, start, end])
            self.blocks.append(row)

    # ---------------------------
    # Draw GUI and Game Screen
    # ---------------------------
    def draw(self):
        self.image = np.zeros((self.height + self.menuHeight, self.width, 3), np.uint8)

        # Draw 3x3 grid
        for i in range(3):
            for j in range(3):
                start_point = self.blocks[i][j][1]
                end_point = self.blocks[i][j][2]
                cv2.rectangle(self.image, start_point, end_point, (255, 255, 255), -1)

                value = " " if self.blocks[i][j][0].value is None else self.blocks[i][j][0].value
                cv2.putText(
                    self.image, value,
                    (j * (self.width // 3) + 25, (i * self.height // 3) + 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 5, (0, 0, 0), 5
                )

        # Status text
        if self.checkWin():
            if self.turn == 1:
                string = "Player 1 Wins" if self.turn != self.vsCom else "Computer Wins"
            else:
                string = "Player 2 Wins" if self.turn != self.vsCom else "Computer Wins"
        else:
            if not self.checkDraw():
                if self.turn == 1:
                    string = "Player 1's Turn" if self.turn != self.vsCom else "Computer's Turn"
                else:
                    string = "Player 2's Turn" if self.turn != self.vsCom else "Computer's Turn"
            else:
                string = "Match Draw!!"

        # Draw status and menu
        cv2.putText(self.image, string, (self.width // 2 - 70, self.height + 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(self.image, "R - Reset", (10, self.height + 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(self.image, "Esc - Exit", (10, self.height + 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        mode_text = "vs Computer" if self.vsCom == 0 else "vs Human"
        cv2.putText(self.image, f"Space - {mode_text}",
                    (self.width // 2 + 10, self.height + 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        if self.selected and not (self.checkWin() or self.checkDraw()):
            self.change = True
            self.selected = False
            self.turn *= -1

    # ---------------------------
    # Main Game Loop
    # ---------------------------
    def mainLoop(self):
        cv2.namedWindow(self.windowName)
        cv2.setMouseCallback(self.windowName, self.mouseCall)

        try:
            while True and cv2.getWindowProperty(self.windowName, 1) != -1:
                if self.change:
                    self.change = False
                    self.draw()

                # Computer move
                if self.vsCom == self.turn and not (self.checkWin() or self.checkDraw()):
                    block = self.nextMove()
                    block.setValue("x" if self.turn == 1 else "o")
                    self.selected = True
                    self.change = True

                cv2.imshow(self.windowName, self.image)
                key = cv2.waitKey(1)

                # Key events
                if key == 27:
                    break
                elif key in [ord("r"), ord("R")]:
                    self.reset()
                elif key == ord(" ") and not (self.checkWin() or self.checkDraw()):
                    self.vsCom = 0 if self.vsCom else self.turn
                    self.change = True

            cv2.destroyAllWindows()

        except:
            print("Window is successfully closed")

    # ---------------------------
    # Win & Draw Check
    # ---------------------------
    def checkWin(self):
        b = self.blocks
        self.win = (
            # Rows
            (b[0][0][0].value and b[0][0][0].value == b[0][1][0].value == b[0][2][0].value) or
            (b[1][0][0].value and b[1][0][0].value == b[1][1][0].value == b[1][2][0].value) or
            (b[2][0][0].value and b[2][0][0].value == b[2][1][0].value == b[2][2][0].value) or
            # Columns
            (b[0][0][0].value and b[0][0][0].value == b[1][0][0].value == b[2][0][0].value) or
            (b[0][1][0].value and b[0][1][0].value == b[1][1][0].value == b[2][1][0].value) or
            (b[0][2][0].value and b[0][2][0].value == b[1][2][0].value == b[2][2][0].value) or
            # Diagonals
            (b[0][0][0].value and b[0][0][0].value == b[1][1][0].value == b[2][2][0].value) or
            (b[2][0][0].value and b[2][0][0].value == b[1][1][0].value == b[0][2][0].value)
        )
        return self.win

    def checkDraw(self):
        for i in range(3):
            for j in range(3):
                if self.blocks[i][j][0].value is None:
                    return False
        return True

    # ---------------------------
    # Minimax AI
    # ---------------------------
    def nextMove(self):
        blocks = [self.blocks[i][j][0] for i in range(3) for j in range(3) if self.blocks[i][j][0].value is None]

        if len(blocks) == 0:
            return None

        scoresList = {}
        for block in blocks:
            if block.value is None:
                if self.computerWins(block):
                    scoresList[block] = 50
                elif self.playerWins(block):
                    scoresList[block] = -50
                elif not self.checkDraw():
                    block.value = "x" if self.turn == 1 else "o"
                    scoresList[block] = self.min_max(1, self.vsCom)
                    block.value = None
                else:
                    scoresList[block] = 0

        if not scoresList:
            return blocks[randint(0, len(blocks) - 1)]

        bestScore = max(scoresList.values(), key=abs)
        bestBlocks = [block for block, score in scoresList.items() if score == bestScore]
        return bestBlocks[randint(0, len(bestBlocks) - 1)]

    def min_max(self, depth, player):
        scoresList = []
        for row in self.blocks:
            for block in row:
                if block[0].value is None:
                    if self.computerWins(block[0]):
                        return 50 - depth
                    elif self.playerWins(block[0]):
                        return -50 + depth
                    else:
                        block[0].value = "x" if self.turn == 1 else "o"
                        scoresList.append(self.min_max(depth + 1, player * -1))
                        block[0].value = None

        if scoresList:
            return max(scoresList, key=abs)
        return 0

    def computerWins(self, block):
        block.value = "x" if self.vsCom == 1 else "o"
        flag = self.checkWin()
        self.win = False
        block.value = None
        return flag

    def playerWins(self, block):
        block.value = "x" if self.vsCom != 1 else "o"
        flag = self.checkWin()
        self.win = False
        block.value = None
        return flag

    # ---------------------------
    # Mouse Event Handler
    # ---------------------------
    def mouseCall(self, event, posx, posy, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN and not self.win and self.turn != self.vsCom:
            self.setBlockInPos(posx, posy)

    def setBlockInPos(self, x, y):
        for i in range(3):
            for j in range(3):
                if (self.blocks[i][j][0].value is None and
                        self.blocks[i][j][1][0] <= x <= self.blocks[i][j][2][0] and
                        self.blocks[i][j][1][1] <= y <= self.blocks[i][j][2][1]):
                    self.blocks[i][j][0].setValue("x" if self.turn == 1 else "o")
                    self.change = True
                    self.selected = True
                    return


# ===============================
# MAIN PROGRAM
# ===============================
if __name__ == "__main__":
    game = GUI("TicTacToe")
    game.mainLoop()
