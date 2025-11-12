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
    with open(input_path, "r") as f:
        text = [line.strip().split() for line in f]

    N = len(text)

    clauses = []
    num_vars = N*N*N
    
    

    def var(r, c, v):
        return r * N * N + c * N + v
        
    # each cell has one value
    for r in range(N):
        for c in range(N):
            # each cell has at least one value
            clauses.append([var(r, c, v) for v in range(1, 10)])
            
            # Each cell has at most one value
            for v1 in range(1, N+1):
                for v2 in range(v1 + 1, N+1):
                    clauses.append([-var(r, c, v1), -var(r, c, v2)])

    # each row one v
    for r in range(N):
        for v in range(1,N+1):
            # for every col at least one V
            clauses.append([var(r, c, v) for c in range(N)])
            
            # each v is at most in one column
            for c1 in range(N):
                for c2 in range(c1 + 1, N):
                    clauses.append([-var(r, c1, v), -var(r, c2, v)])
            
    # each cell has one value
    for c in range(N):
        for v in range(1,N+1):
            # for every v at least one column
            clauses.append([var(r, c, v) for r in range(N)])
            
            # each v is at most in one column
            for r1 in range(N):
                for r2 in range(r1 + 1, N):
                    clauses.append([-var(r1, c, v), -var(r2, c, v)])
           
         
         
    print(len(clauses))
    boxdim = int(N**0.5)
             
    # boxes
    for row_offset in range(0, N, boxdim):
        for col_offset in range(0, N, boxdim):
            print("new box")

            for v in range(1, N+1):
                box = []

                for i in range(boxdim):
                    for j in range (boxdim):
                        r = i+row_offset
                        c = j+col_offset
                        box.append(var(r,c,v))   
                # at least one
                clauses.append(box)
                
                # at most one
                for loop1 in range(len(box)):
                    for loop2 in range(loop1+1, len(box)):
                        
                        clauses.append([-box[loop1], -box[loop2]])


    #  Non-consecutive rule:
    # For every cell (r, c) and each orthogonal neighbor (r′, c′):
    # value(r, c) − value(r′, c′) ̸ = 1.

    for i in range(N):
        for j in range(N):
            for v in range(1, N+1):
                
                # check for right border
                if i+1 < N:
                    # for 0 and value N of v checks
                    if v+1 <= N:
                        clauses.append([-var(i, j, v), -var(i+1, j, v+1)])
                    if v-1 >= 1:
                        clauses.append([-var(i, j, v), -var(i+1, j, v-1)])
                        
                # check for down border
                if j+1 < N:
                    if v+1 <= N:
                        clauses.append([-var(i, j, v), -var(i, j+1, v+1)])
                    if v-1 >= 1:
                        clauses.append([-var(i, j, v), -var(i, j+1, v-1)])
                        
    for i in range (N):
        for j in range(N):
            text_int = text[i][j]            
            text_int = int(text_int)
            if text_int > 0:
                clauses.append([var(i, j, text_int)])
    return clauses, num_vars


