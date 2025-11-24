class Graph:
    def __init__(self, adjac_lis):
        # Lưu danh sách kề của đồ thị (dạng dict)
        self.adjac_lis = adjac_lis   

    def get_neighbors(self, v):
        # Trả về danh sách các đỉnh kề của v
        return self.adjac_lis[v]     

    # Hàm heuristic (ước lượng chi phí còn lại) – ở đây đơn giản: mọi đỉnh đều = 1
    def h(self, n):
        H = {
            'A': 1,
            'B': 1,
            'C': 1,
            'D': 1
        }
        return H[n]

    def a_star_algorithm(self, start, stop):
        # open_lst: tập các đỉnh đã được phát hiện nhưng chưa duyệt hết
        open_lst = set([start])

        # closed_lst: tập các đỉnh đã duyệt xong
        closed_lst = set([])

        # poo: lưu chi phí thực tế (g(n)) từ start đến mỗi node
        poo = {}
        # Chi phí đi từ start đến start là 0
        poo[start] = 0               

        # par: lưu node cha (để truy vết đường đi ngược lại)
        par = {}
        # Node bắt đầu có cha là chính nó
        par[start] = start           

        # Lặp cho đến khi không còn node nào trong open_lst
        while len(open_lst) > 0:
            # n là node có giá trị f(n) = g(n) + h(n) nhỏ nhất
            n = None  

            # Tìm node có f nhỏ nhất trong open_lst
            for v in open_lst:
                # Nếu n chưa có hoặc v có f nhỏ hơn → chọn v làm n mới
                if n == None or poo[v] + self.h(v) < poo[n] + self.h(n):
                    n = v

            # Nếu không tìm được node nào hợp lệ
            if n == None:
                print('Path does not exist!')
                return None

            # Nếu node hiện tại là đích → truy vết ngược đường đi
            if n == stop:
                # Danh sách đường đi (sẽ đảo ngược sau)
                reconst_path = []
                # Dừng khi quay về start      
                while par[n] != n:        
                    reconst_path.append(n)
                    # Quay ngược về node cha
                    n = par[n]            
                reconst_path.append(start)
                # Đảo ngược để có thứ tự từ start → stop
                reconst_path.reverse()   

                print('Path found: {}'.format(reconst_path))
                return reconst_path

            # Duyệt các láng giềng (neighbors) của node n
            for (m, weight) in self.get_neighbors(n):
                # Nếu m chưa nằm trong open_lst hoặc closed_lst → thêm vào open_lst
                if m not in open_lst and m not in closed_lst:
                    open_lst.add(m)             # Thêm vào tập mở
                    par[m] = n                  # Ghi nhận cha của m là n
                    poo[m] = poo[n] + weight    # Cập nhật chi phí thực tế g(m)

                # Nếu m đã được xét nhưng tìm được đường đi ngắn hơn
                else:
                    if poo[m] > poo[n] + weight:    # Nếu g(m) mới < g(m) cũ
                        poo[m] = poo[n] + weight    # Cập nhật chi phí g(m)
                        par[m] = n                  # Cập nhật cha mới của m

                        # Nếu m nằm trong closed_lst → di chuyển lại vào open_lst
                        if m in closed_lst:
                            closed_lst.remove(m)
                            open_lst.add(m)

            # Sau khi duyệt xong các láng giềng của n:
            open_lst.remove(n)     # Xóa n khỏi open_lst
            closed_lst.add(n)      # Đưa n vào closed_lst (đã hoàn thành)

        # Nếu vòng lặp kết thúc mà không tìm thấy đường đi
        print('Path does not exist!')
        return None


# -----------------------------
# Đồ thị ví dụ (graph adjacency list)
# -----------------------------
adjac_lis = {
    'A': [('B', 1), ('C', 3)],            # A kề B (1), C (3)
    'B': [('A', 1), ('D', 1), ('C', 1)],  # B kề A, D, C
    'C': [('A', 3), ('B', 1), ('D', 5)],  # C kề A, B, D
    'D': [('B', 1), ('C', 5)]             # D kề B, C
}

# Khởi tạo đồ thị và chạy thuật toán A*
graph1 = Graph(adjac_lis)
graph1.a_star_algorithm('A', 'D')
