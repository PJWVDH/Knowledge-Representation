"""
SAT Assignment Part 1 - Non-consecutive Sudoku Encoder (Puzzle -> CNF)

THIS is the file to edit.

Implement: to_cnf(input_path) -> (clauses, num_vars)

You're required to use a variable mapping as follows:
    var(r,c,v) = r*N*N + c*N + v
where r,c are in range (0...N-1) and v in (1...N).

You must encode:
  (1) Exactly one value per cell
  (2) For each value v and each row r: exactly one column c has v
  (3) For each value v and each column c: exactly one row r has v
  (4) For each value v and each sqrt(N)×sqrt(N) box: exactly one cell has v
  (5) Non-consecutive: orthogonal neighbors cannot differ by 1
  (6) Clues: unit clauses for the given puzzle
"""


from typing import Tuple, Iterable



def to_cnf(input_path: str) -> Tuple[Iterable[Iterable[int]], int]:
    """
    Read puzzle from input_path and return (clauses, num_vars).

    - clauses: iterable of iterables of ints (each clause), no trailing 0s
    - num_vars: must be N^3 with N = grid size
    """

    with open(input_path) as f:
        text = [line.strip().split() for line in f]

    N = len(text)
    B = int(N**0.5)

    clauses = []

    def var(r, c, v):
        return r * N * N + c * N + v
    
    num_vars = N * N * N

    # (1) Exactly one value per cell
    for r in range(N):
        for c in range(N):
            # At least one value in cell
            clauses.append([var(r, c, v) for v in range(1, N + 1)])
            # At most one value in cell
            for v1 in range(1, N + 1):
                for v2 in range(v1 + 1, N + 1):
                    clauses.append([-var(r, c, v1), -var(r, c, v2)])
            
    # (2) Exactly one row per value in each row
    for r in range(N):
        for v in range(1, N + 1):
            # At least one column for value v in row r
            clauses.append([var(r, c, v) for c in range(N)])
            # At most one column for value v in row r
            for c1 in range(N):
                for c2 in range(c1 + 1, N):
                    clauses.append([-var(r, c1, v), -var(r, c2, v)])

     # (3) Exactly one column per value in each column
    for c in range(N):
        for v in range(1, N + 1):
            # At least one column for value v in row r
            clauses.append([var(r, c, v) for r in range(N)])
            # At most one column for value v in row r
            for r1 in range(N):
                for r2 in range(r1 + 1, N):
                    clauses.append([-var(r1, c, v), -var(r2, c, v)])

     # (4) Exactly one v in a sqrt(N) by sqrt(N) box
    for r_box in range(0, N, B):
        for c_box in range(0, N, B):
            for v in range(1, N + 1):
                vars_list = [
                    var(r_box + i, c_box + j, v)
                    for i in range(B)
                    for j in range(B)
                    
                ]
                # At least one v in the box
                clauses.append(vars_list)
                # At most one v in the box
                for i1 in range(len(vars_list)):
                    for i2 in range(i1 + 1, len(vars_list)):
                        clauses.append([-vars_list[i1], -vars_list[i2]])
    
    # (5) orthogonal cant be more exactly be abs|value(r,c) - value(r', c')| == 1
    for r in range(0, N):
        for c in range(0, N):
            for v in range(1, N+1):
                if c + 1 < N:
                    if v < N:
                        # Right and left
                        clauses.append([-var(r, c, v), -var(r, c + 1, v + 1)])
                    if v > 1:
                        clauses.append([-var(r, c, v), -var(r, c + 1, v - 1)])

                if r + 1 < N:
                    if v < N:
                        # Up and down
                        clauses.append([-var(r, c, v), -var(r + 1, c, v + 1)])
                    if v > 1:
                        clauses.append([-var(r, c, v), -var(r + 1, c, v - 1)])

    # (6) Unit clauses of a certain puzzle, so the values that are already filled in.

    for r in range(N):
        for c in range(N):
            v = text[r][c]
            v = int(v)
            if v > 0:
                clauses.append([var(r, c, v)])

    return clauses, num_vars

