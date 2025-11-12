"""
SAT Assignment Part 2 - Non-consecutive Sudoku Solver (Puzzle -> SAT/UNSAT)

THIS is the file to edit.

Implement: solve_cnf(clauses) -> (status, model_or_None)"""


from typing import Iterable, List, Tuple

def solve_cnf(clauses: Iterable[Iterable[int]], num_vars: int) -> Tuple[str, List[int] | None]:
    """
    Implement your SAT solver here.
    Must return:
      ("SAT", model)  where model is a list of ints (DIMACS-style), or
      ("UNSAT", None)
      
    """
    
    # create dict
    
    
    truth_values = {}
    for i in range(1, num_vars+1):
      truth_values[i] = None
      
      
    for clause in clauses:
      if len(clause) == 1:
        if clause[0] < 0:
          truth_values[abs(clause[0])] = False
        else:
          truth_values[abs(clause[0])] = True
          
    print(truth_values)
      
      
    # print(clauses)
    
    return None
