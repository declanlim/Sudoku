def get_grid(grid_string: str) -> list[list[int]]:
    """
    Takes in a a string of numbers representing a sudoku grid and returns a list representing the
    grid
    """
    # declares 2d list to store grid
    grid = [[0 for _ in range(9)] for _ in range(9)]

    # stores the grid in the list
    for i, line in enumerate(grid_string.splitlines()):
        for j in range(9):
            grid[i][j] = int(line[j])
    return grid


def print_grid(grid: list[list[int]]):
    """
    Takes in a list representing the sudoku grid and prints the grid with formatting
    """
    print("+-----------+-----------+-----------+")
    for line_count, line in enumerate(grid):
        newline = "| "
        for counter, num in enumerate(line):
            if num == 0:
                num = "-"

            if (counter + 1) % 3 == 0:
                newline += str(num) + " | "
            else:
                newline += str(num) + "   "
        print(newline)
        if (line_count + 1) % 3 == 0:
            print("+-----------+-----------+-----------+")

    print("\n")


def is_valid(grid: list[list[int]], value: int, column_num: int, row_num: int) -> bool:
    """
    Checks if a specified value is allowed in the specified row and column for the given grid
    """
    row = []
    column = []
    subgrid = []
    # checks if the indexes are too big
    if (row_num > 9 or row_num < 1) or (column_num > 9 or column_num < 1):
        print("The indexes supplied were invalid")
        return False
    else:
        # gets the factor of 3 in the grid
        factor_x = round((row_num / 3) + 1 / 5)
        factor_y = round((column_num / 3) + 1 / 5)
        # adjusts the row and column number
        row_num -= 1
        column_num -= 1

        # stores numbers in columns and rows
        for i in range(0, 9):
            column.append(grid[i][column_num])
            row.append(grid[row_num][i])

        for i in range((3 * factor_x) - 3, 3 * factor_x):
            subgrid.append(grid[i][(3 * factor_y) - 3:3 * factor_y])

        if value in column:
            return False
        if value in row:
            return False

    return True


def get_bit_boards(grid: list[list[int]], number: int) -> list[list[int]]:
    """
    Generates a bit board for a specified number given a grid
    """
    new_board = [[1 for i in range(9)] for i in range(9)]

    for i in range(0, 9):
        line = grid[i][:]

        if number in line:
            index = line.index(number)
            # Makes the row of the index of  0
            new_board[i][:] = [0 for count in range(9)]

            # Makes the column of the index of number 0
            for count in range(9):
                new_board[count][index] = 0

            # Gets the indexes of the subgrid where the value is found
            factor_x = round(((i + 1) / 3) + 0.2)
            factor_y = round(((index + 1) / 3) + 0.2)

            # # Makes the values of the subgrid 0
            for l in range((3 * factor_x) - 3, 3 * factor_x):
                new_board[l][(3 * factor_y) - 3:3 * factor_y] = [0 for count in range(3)]

    # makes all existing squares with numbers 0
    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0:
                new_board[i][j] = 0
    return new_board


def update_bit_boards():
    """
    Updates all bit boards
    """
    for i in range(1, 10):
        bit_boards[i - 1] = get_bit_boards(solved, i)


def finished(grid: list[list[int]]) -> bool:
    """
    Checks if a given grid is a finished sudoku puzzle
    """
    for line in grid:
        if 0 in line:
            return False
    return True


def check_line():
    """
    Checks all lines for the sudoku grid
    """
    # iterates through each line of the bit board and checks for possible spaces
    for line_num, line in enumerate(board):
        # If the number appears once in the line, it is added to the solved puzzle
        if line.count(1) == 1:
            index = line.index(1)

            solved[line_num][index] = board_num + 1

            # for board in bit_boards:
            # makes the line 0
            board[line_num][:] = [0 for count in range(9)]
            # makes the column 0
            for counter in range(9):
                board[counter][index] = 0


def check_col():
    """
    Checks all columns for the sudoku grid
    """
    for col_num in range(9):
        col = []

        # gets the column
        for col_count in range(9):
            col.append(board[col_count][col_num])

        # if the number appears once in the column, it as added to the solved puzzle
        if col.count(1) == 1:
            index = col.index(1)
            solved[index][col_num] = board_num + 1

            # for board in bit_boards:
            # makes the column 0
            for counter in range(9):
                board[counter][col_num] = 0
            # makes the line 0
            board[index][:] = [0 for count in range(9)]


gridString = """600302500
050000012
020500000
742605000
000000054
305000027
280150000
000040200
000000700"""

iterations = 1

# gets the square as an array of numbers
grid = get_grid(gridString)

# creates another grid to store the solved array
solved = get_grid(gridString)

bit_boards = []

# gets the bit_board for each number
for i in range(1, 10):
    bit_boards.append(get_bit_boards(grid, i))

while not finished(solved):
    # Stops the program running after 75 iterations
    print("iteration " + str(iterations))
    if iterations == 75:
        print("too many iterations")
        break
    iterations += 1

    # iterates through each bit board
    for board_num, board in enumerate(bit_boards):
        check_line()
        update_bit_boards()
        check_col()
        update_bit_boards()

        # print_grid(board)

        # # gets each subgrid from the square
        # for count in range(1, 4):
        #     for col in range(1, 4):
        #         subgrid = [](board[i][(3 * col) - 3:3 * col])
        #         print(subgrid)
        #         for i in range((3 * count) - 3, 3 * count):
        #             subgrid.append

print_grid(solved)
