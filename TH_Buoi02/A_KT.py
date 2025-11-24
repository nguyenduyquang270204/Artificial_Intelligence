import copy
from heapq import heappush, heappop

# Kích thước puzzle (3x3)
n = 3

# Các hướng di chuyển: xuống, trái, lên, phải
rows = [1, 0, -1, 0]
cols = [0, -1, 0, 1]


# --------------------------
# Hàng đợi ưu tiên (min-heap)
# --------------------------
class PriorityQueue:
    def __init__(self):
        self.heap = []

    def push(self, key):
        heappush(self.heap, key)

    def pop(self):
        return heappop(self.heap)

    def empty(self):
        return len(self.heap) == 0


# --------------------------
# Cấu trúc một node trong cây tìm kiếm
# --------------------------
class Node:
    def __init__(self, parent, mats, empty_tile_posi, costs, levels):
        self.parent = parent
        self.mats = mats
        self.empty_tile_posi = empty_tile_posi
        self.costs = costs  # số ô sai
        self.levels = levels  # số bước đã đi

    # Ưu tiên theo f(n) = g(n) + h(n)
    def __lt__(self, nxt):
        return (self.costs + self.levels) < (nxt.costs + nxt.levels)


# --------------------------
# Hàm tính số ô sai
# --------------------------
def calculateCosts(mats, final) -> int:
    count = 0
    for i in range(n):
        for j in range(n):
            if mats[i][j] != 0 and mats[i][j] != final[i][j]: # So điều kiện nếu khác ô trống và khác vị trí đúng
                count += 1 # Cập nhật số ô sai
    return count


# --------------------------
# Sinh node mới
# --------------------------
def newNodes(parent, mats, empty_tile_posi, new_empty_tile_posi, levels, final) -> Node:
    new_mats = copy.deepcopy(mats)

    # Đổi chỗ ô trống với ô kế bên
    x1, y1 = empty_tile_posi
    x2, y2 = new_empty_tile_posi
    new_mats[x1][y1], new_mats[x2][y2] = new_mats[x2][y2], new_mats[x1][y1]

    # Tính số ô sai sau khi di chuyển
    costs = calculateCosts(new_mats, final)

    return Node(parent, new_mats, new_empty_tile_posi, costs, levels)


# --------------------------
# In ma trận
# --------------------------
def printMatrix(mats):
    for row in mats:
        print(" ".join(str(x) for x in row))
    print()


# --------------------------
# Kiểm tra tọa độ hợp lệ
# --------------------------
def isSafe(x, y):
    return 0 <= x < n and 0 <= y < n


# --------------------------
# In đường đi từ gốc đến node đích
# --------------------------
def printPath(root):
    if root is None:
        return
    printPath(root.parent)
    printMatrix(root.mats)


# --------------------------
# Giải thuật chính
# --------------------------
def solve(initial, empty_tile_posi, final):
    pq = PriorityQueue()

    # Node gốc
    costs = calculateCosts(initial, final)
    root = Node(None, initial, empty_tile_posi, costs, 0)
    pq.push(root)

    while not pq.empty():
        minimum = pq.pop()

        # Nếu đã đến đích
        if minimum.costs == 0:
            print("Đã tìm thấy lời giải!\nĐường đi từ đầu đến cuối:")
            printPath(minimum)
            return

        # Sinh các node con
        for i in range(4):
            new_tile_posi = [
                minimum.empty_tile_posi[0] + rows[i],
                minimum.empty_tile_posi[1] + cols[i],
            ]

            if isSafe(new_tile_posi[0], new_tile_posi[1]):
                child = newNodes(
                    minimum,
                    minimum.mats,
                    minimum.empty_tile_posi,
                    new_tile_posi,
                    minimum.levels + 1,
                    final,
                )
                pq.push(child)


# --------------------------
# CHẠY CHƯƠNG TRÌNH
# --------------------------
initial = [
    [1, 2, 3],
    [5, 6, 0],
    [7, 8, 4],
]

final = [
    [1, 2, 3],
    [5, 8, 6],
    [0, 7, 4],
]

empty_tile_posi = [1, 2]

solve(initial, empty_tile_posi, final)
