from collections import deque
goal=(1,2,3,4,5,6,7,8,0)
offset=[(-3,"up"), (3,"down"), (-1, "left"), (1, "right")]
def solve_8_puzzle(start):
    q=deque([(start, [])])
    visited={start}
    while q:
        board, path = q.popleft()
        if board == goal:
            return path
        zero = board.index(0)
        r, c= zero//3, zero%3

        for shift, action in offset:
            newzero=zero+shift
            if 0<=newzero<9:
                if action == "left" and c == 0:
                    continue
                if action == "right" and c == 2:
                    continue
                b=list(board)
                b[zero], b[newzero] = b[newzero], b[zero]
                nxt = tuple(b)

                if nxt not in visited:
                    visited.add(nxt)
                    q.append((nxt, path + [action]))
    return None

if __name__ == "__main__":
    # Test board configuration
    start_board = (1, 2, 3, 0, 4, 6, 7, 5, 8)

    moves = solve_8_puzzle(start_board)
    print("Solved in", len(moves), "moves!")
    print("Path:", " -> ".join(moves))               

