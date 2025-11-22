"""
backtrracking algorithm from https://www.geeksforgeeks.org/sudoku-backtracking-7//
with added non-consecutive constraint

"""


# Function to check if it is safe to place num at mat[row][col]
def isSafe(mat, row, col, num):
    N = len(mat)
    B = int(N ** 0.5)
    
    # Check if num exists in the row
    for x in range(N):
        if mat[row][x] == num:
            return False

    # Check if num exists in the col
    for x in range(N):
        if mat[x][col] == num:
            return False

    # Check if num exists in the BxB sub-matrix
    startRow = row - (row % B)
    startCol = col - (col % B)

    for i in range(B):
        for j in range(B):
            if mat[i + startRow][j + startCol] == num:
                return False
    
    # Check non-consecutive constraint (orthogonal neighbors cannot differ by 1)
    # Check left
    if col > 0 and mat[row][col - 1] != 0 and abs(mat[row][col - 1] - num) == 1:
        return False
    # Check right
    if col < N - 1 and mat[row][col + 1] != 0 and abs(mat[row][col + 1] - num) == 1:
        return False
    # Check up
    if row > 0 and mat[row - 1][col] != 0 and abs(mat[row - 1][col] - num) == 1:
        return False
    # Check down
    if row < N - 1 and mat[row + 1][col] != 0 and abs(mat[row + 1][col] - num) == 1:
        return False

    return True

# Function to solve the Sudoku problem
def solveSudokuRec(mat, row, col):
    N = len(mat)
    
    # base case: Reached Nth column of the last row
    if row == N - 1 and col == N:
        return True

    # If last column of the row go to the next row
    if col == N:
        row += 1
        col = 0

    # If cell is already occupied then move forward
    if mat[row][col] != 0:
        return solveSudokuRec(mat, row, col + 1)

    for num in range(1, N + 1):
        
        # If it is safe to place num at current position
        if isSafe(mat, row, col, num):
            mat[row][col] = num
            if solveSudokuRec(mat, row, col + 1):
                return True
            mat[row][col] = 0

    return False

def solveSudoku(mat):
    """Solve Sudoku puzzle using backtracking. Returns True if solvable, False otherwise."""
    return solveSudokuRec(mat, 0, 0)

if __name__ == "__main__":
    mat = [
        [3, 0, 6, 5, 0, 8, 4, 0, 0],
        [5, 2, 0, 0, 0, 0, 0, 0, 0],
        [0, 8, 7, 0, 0, 0, 0, 3, 1],
        [0, 0, 3, 0, 1, 0, 0, 8, 0],
        [9, 0, 0, 8, 6, 3, 0, 0, 5],
        [0, 5, 0, 0, 9, 0, 6, 0, 0],
        [1, 3, 0, 0, 0, 0, 2, 5, 0],
        [0, 0, 0, 0, 0, 0, 0, 7, 4],
        [0, 0, 5, 2, 0, 6, 3, 0, 0]
    ]

    solveSudoku(mat)

    for row in mat:
        print(" ".join(map(str, row)))