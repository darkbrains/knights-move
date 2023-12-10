N = 8


def print_board(board, horse_x, horse_y):
    print("  -------------------------")
    for i in range(N):
        print(str(8-i) + "|", end=' ')
        for j in range(N):
            if i == horse_x and j == horse_y:
                print("🐴", end=' ')
            else:
                print("⬜" if (i + j) % 2 == 0 else "⬛", end=' ')
        print("|")
    print("  -------------------------")
    print("   A  B  C  D  E  F  G  H")


def is_valid(x, y, board):
    return (x >= 0 and y >= 0) and (x < N and y < N) and (board[x][y] == -1)


def convert_position_to_coordinates(position):
    column = ord(position[0].upper()) - ord('A')
    row = N - int(position[1])
    return row, column


def convert_coordinates_to_position(x, y):
    column = chr(y + ord('A'))
    row = str(N - x)
    return column + row


def solve_kt_util(n, board, curr_x, curr_y, move_x, move_y, pos, path):
    if pos == n**2:
        return True
    next_moves = sorted([(curr_x + move_x[i], curr_y + move_y[i]) for i in range(8)
                         if is_valid(curr_x + move_x[i], curr_y + move_y[i], board)],
                        key=lambda move: count_next_moves(move[0], move[1], move_x, move_y, board))
    for new_x, new_y in next_moves:
        board[new_x][new_y] = pos
        path.append((new_x, new_y))
        if solve_kt_util(n, board, new_x, new_y, move_x, move_y, pos+1, path):
            return True
        path.pop()
        board[new_x][new_y] = -1
    return False


def count_next_moves(x, y, move_x, move_y, board):
    count = 0
    for i in range(8):
        if is_valid(x + move_x[i], y + move_y[i], board):
            count += 1
    return count


def validate_input(user_input):
    if len(user_input) != 2:
        raise ValueError("Input must be exactly two characters (e.g., B5).")
    column, row = user_input[0].upper(), user_input[1]
    if not (column.isalpha() and 'A' <= column <= 'H'):
        raise ValueError("The first character must be a letter from A to H.")
    if not (row.isdigit() and 1 <= int(row) <= 8):
        raise ValueError("The second character must be a single digit from 1 to 8.")
    return convert_position_to_coordinates(user_input)


def solve_kt(n, start_x, start_y):
    board = [[-1 for _ in range(n)] for _ in range(n)]
    path = []
    move_x = [2, 1, -1, -2, -2, -1, 1, 2]
    move_y = [1, 2, 2, 1, -1, -2, -2, -1]
    board[start_x][start_y] = 0
    path.append((start_x, start_y))
    pos = 1
    if not solve_kt_util(n, board, start_x, start_y, move_x, move_y, pos, path):
        print("There is no solution")
    else:
        print_board(board, start_x, start_y)
        print("Sequence of moves:")
        print(" -> ".join([convert_coordinates_to_position(x, y) for x, y in path]))


try:
    user_input = input("Enter starting position (eg B5): ")
    start_x, start_y = validate_input(user_input)
    solve_kt(N, start_x, start_y)
except ValueError as e:
    print(e)
