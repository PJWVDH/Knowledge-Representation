import time
import sys
from collections import Counter
from typing import Iterable, List, Optional, Tuple


def solve_cnf(clauses: Iterable[Iterable[int]], num_vars: int) -> Tuple[str, Optional[List[List[int]]]]:
    clauses = [set(cl) for cl in clauses]
    literal_counts = Counter(l for cl in clauses for l in cl)
    stats = {"calls": 0}
    start_time = time.time()

    sat, model_assignment = dpll(clauses, [0] * (num_vars + 1), literal_counts, stats, start_time, num_vars)

    print()

    if sat:
        # convert model to Sudoku grid
        grid = [[0]*9 for _ in range(9)]
        for var_index in range(1, num_vars + 1):
            val = model_assignment[var_index]
            if val == 1:  
                # Decode variable back to row, col, digit
                var = var_index - 1
                row = var // 81
                col = (var % 81) // 9
                digit = (var % 9) + 1
                grid[row][col] = digit
        return "SAT", grid
    else:
        return "UNSAT", None



def dpll(clauses: List[set],
         assignment: List[int],
         literal_counts: Counter,
         stats: dict,
         start_time: float,
         num_vars: int) -> Tuple[bool, Optional[List[int]]]:

    # Unit propagation
    clauses = [set(cl) for cl in clauses]
    assignment = assignment[:]
    unit_queue = [next(iter(cl)) for cl in clauses if len(cl) == 1]

    while unit_queue:
        lit = unit_queue.pop()
        var, val = abs(lit), 1 if lit > 0 else -1

        if assignment[var] == -val:
            return False, None
        if assignment[var] == val:
            continue

        assignment[var] = val
        new_clauses = []

        for cl in clauses:
            if lit in cl:
                continue 
            if -lit in cl:
                cl = cl - {-lit}
                if not cl:
                    return False, None
                if len(cl) == 1:
                    unit_queue.append(next(iter(cl)))
            new_clauses.append(cl)
        clauses = new_clauses

    if not clauses:
        model = assignment[:]
        for i in range(1, num_vars + 1):
            if model[i] == 0:
                model[i] = -1
        return True, model

    # Choose branching variable using simple heuristic
    unassigned_vars = [i for i in range(1, num_vars + 1) if assignment[i] == 0]
    if not unassigned_vars:
        return False, None

    var = max(unassigned_vars, key=lambda v: literal_counts.get(v, 0) + literal_counts.get(-v, 0))

    for val in (1, -1):
        target_lit, opp_lit = var if val > 0 else -var, -var if val > 0 else var
        new_clauses = []
        conflict = False
        for cl in clauses:
            if target_lit in cl:
                continue
            if opp_lit in cl:
                cl = cl - {opp_lit}
                if not cl:
                    conflict = True
                    break
            new_clauses.append(cl)
        if conflict:
            continue

        new_assignment = assignment[:]
        new_assignment[var] = val

        sat, model = dpll(new_clauses, new_assignment, literal_counts, stats, start_time, num_vars)
        if sat:
            return True, model

    return False, None
