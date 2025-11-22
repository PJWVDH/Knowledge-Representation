#!/usr/bin/env python3
"""
Sudoku Solver Comparison - DPLL vs Backtracking

Compares two algorithms for solving Sudoku puzzles:
1. CNF encoding + DPLL solver
2. Direct backtracking solver

Usage:
  python main.py --in <puzzle.txt>
  python main.py --batch <directory>
  python main.py --run-all

Output:
  - Individual puzzle results with timing and solvability
  - Comparison statistics between both algorithms
  - CSV file with detailed results
"""

import argparse
import time
import os
import csv
from typing import Tuple, Iterable, List
from encoder import to_cnf
from DPLL_solver import solve_cnf
from backtracking_solver import solveSudoku, isSafe


def parse_args():
    p = argparse.ArgumentParser(description="Compare DPLL and Backtracking Sudoku solvers")
    p.add_argument("--in", dest="inp", help="Single puzzle file to solve")
    p.add_argument("--batch", dest="batch", help="Directory containing multiple puzzles")
    p.add_argument("--run-all", dest="run_all", action="store_true", help="Run on all Simple and Trivial Sudoku puzzles")
    p.add_argument("--output", dest="output", default="results.csv", help="CSV output file (default: results.csv)")
    return p.parse_args()


def read_puzzle(input_path: str) -> List[List[int]]:
    """Read a Sudoku puzzle from a text file."""
    with open(input_path) as f:
        puzzle = [[int(x) for x in line.strip().split()] for line in f if line.strip()]
    return puzzle


def solve_with_dpll(input_path: str) -> Tuple[str, float, List[List[int]]]:
    """Solve using CNF encoding + DPLL solver."""
    start_time = time.time()
    clauses, num_vars = to_cnf(input_path)
    status, solution = solve_cnf(clauses, num_vars)
    elapsed_time = time.time() - start_time
    return status, elapsed_time, solution


def solve_with_backtracking(input_path: str) -> Tuple[str, float, List[List[int]]]:
    """Solve using direct backtracking."""
    puzzle = read_puzzle(input_path)
    start_time = time.time()
    solved = solveSudoku(puzzle)
    elapsed_time = time.time() - start_time
    status = "SAT" if solved else "UNSAT"
    return status, elapsed_time, puzzle if solved else None


def compare_single_puzzle(input_path: str, verbose: bool = True):
    """Compare both algorithms on a single puzzle."""
    if verbose:
        print(f"\n{'='*80}")
        print(f"Solving: {input_path}")
        print(f"{'='*80}\n")
    
    # Method 1: CNF + DPLL
    if verbose:
        print("Method 1: CNF Encoding + DPLL Solver")
        print("-" * 40)
    try:
        dpll_status, dpll_time, dpll_solution = solve_with_dpll(input_path)
        if verbose:
            print(f"Result: {dpll_status}")
            print(f"Time: {dpll_time:.6f} seconds")
            if dpll_solution and dpll_status == "SAT":
                print("Solution:")
                for row in dpll_solution:
                    print(" ".join(map(str, row)))
    except Exception as e:
        if verbose:
            print(f"Error: {e}")
        dpll_status, dpll_time, dpll_solution = "ERROR", None, None
    
    if verbose:
        print()
    
    # Method 2: Backtracking
    if verbose:
        print("Method 2: Direct Backtracking")
        print("-" * 40)
    try:
        bt_status, bt_time, bt_solution = solve_with_backtracking(input_path)
        if verbose:
            print(f"Result: {bt_status}")
            print(f"Time: {bt_time:.6f} seconds")
            if bt_solution and bt_status == "SAT":
                print("Solution:")
                for row in bt_solution:
                    print(" ".join(map(str, row)))
    except Exception as e:
        if verbose:
            print(f"Error: {e}")
        bt_status, bt_time, bt_solution = "ERROR", None, None
    
    if verbose:
        print()
    
    # Comparison
    if verbose:
        print("Comparison")
        print("-" * 40)
        if dpll_status == bt_status:
            print(f"✓ Both methods agree: {dpll_status}")
        else:
            print(f"✗ Methods disagree! DPLL: {dpll_status}, Backtracking: {bt_status}")
        
        if dpll_time is not None and bt_time is not None:
            if dpll_time < bt_time:
                speedup = bt_time / dpll_time
                print(f"✓ DPLL is faster by {speedup:.2f}x ({dpll_time:.6f}s vs {bt_time:.6f}s)")
            else:
                speedup = dpll_time / bt_time
                print(f"✓ Backtracking is faster by {speedup:.2f}x ({bt_time:.6f}s vs {dpll_time:.6f}s)")
    
    return {
        "file": input_path,
        "dpll_status": dpll_status,
        "dpll_time": dpll_time,
        "bt_status": bt_status,
        "bt_time": bt_time
    }


def compare_batch(directory: str, verbose: bool = True):
    """Compare both algorithms on multiple puzzles in a directory."""
    if verbose:
        print(f"\n{'='*80}")
        print(f"Batch Comparison: {directory}")
        print(f"{'='*80}\n")
    
    results = []
    puzzle_files = sorted([f for f in os.listdir(directory) if f.endswith('.txt')])
    
    for puzzle_file in puzzle_files:
        puzzle_path = os.path.join(directory, puzzle_file)
        result = compare_single_puzzle(puzzle_path, verbose=verbose)
        results.append(result)
    
    # Summary statistics
    if verbose:
        print(f"\n{'='*80}")
        print("Summary Statistics")
        print(f"{'='*80}\n")
        
        total_puzzles = len(results)
        dpll_solved = sum(1 for r in results if r["dpll_status"] == "SAT")
        bt_solved = sum(1 for r in results if r["bt_status"] == "SAT")
        agreement = sum(1 for r in results if r["dpll_status"] == r["bt_status"])
        
        print(f"Total puzzles: {total_puzzles}")
        print(f"DPLL solved: {dpll_solved}/{total_puzzles} ({dpll_solved/total_puzzles*100:.1f}%)")
        print(f"Backtracking solved: {bt_solved}/{total_puzzles} ({bt_solved/total_puzzles*100:.1f}%)")
        print(f"Agreement: {agreement}/{total_puzzles} ({agreement/total_puzzles*100:.1f}%)")
        print()
        
        # Timing statistics (only for successfully solved puzzles)
        dpll_times = [r["dpll_time"] for r in results if r["dpll_time"] is not None and r["dpll_status"] == "SAT"]
        bt_times = [r["bt_time"] for r in results if r["bt_time"] is not None and r["bt_status"] == "SAT"]
        
        if dpll_times:
            print(f"DPLL average time: {sum(dpll_times)/len(dpll_times):.6f} seconds")
            print(f"DPLL min time: {min(dpll_times):.6f} seconds")
            print(f"DPLL max time: {max(dpll_times):.6f} seconds")
        
        if bt_times:
            print(f"Backtracking average time: {sum(bt_times)/len(bt_times):.6f} seconds")
            print(f"Backtracking min time: {min(bt_times):.6f} seconds")
            print(f"Backtracking max time: {max(bt_times):.6f} seconds")
        
        # Head-to-head comparison
        if dpll_times and bt_times:
            dpll_faster = sum(1 for r in results if r["dpll_time"] and r["bt_time"] and r["dpll_time"] < r["bt_time"])
            print(f"\nDPLL faster on: {dpll_faster}/{len(results)} puzzles")
            print(f"Backtracking faster on: {len(results) - dpll_faster}/{len(results)} puzzles")
    
    return results


def save_results_to_csv(results: List[dict], output_file: str):
    """Save results to a CSV file."""
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['category', 'type', 'puzzle_file', 'dpll_status', 'dpll_time', 'bt_status', 'bt_time', 'agreement', 'faster_method', 'speedup']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for result in results:
            # Extract category and type from file path
            file_path = result['file']
            path_parts = file_path.split(os.sep)
            
            category = "Unknown"
            puzzle_type = "Unknown"
            puzzle_file = os.path.basename(file_path)
            
            if "Trivial_Sudokus" in path_parts:
                category = "Trivial"
                if "SAT" in path_parts:
                    puzzle_type = "SAT"
                elif "UNSAT" in path_parts:
                    puzzle_type = "UNSAT"
            elif "Simple_Sudokus" in path_parts:
                category = "Simple"
                if "SAT" in path_parts:
                    puzzle_type = "SAT"
                elif "UNSAT" in path_parts:
                    puzzle_type = "UNSAT"
            
            agreement = result['dpll_status'] == result['bt_status']
            
            faster_method = "N/A"
            speedup = None
            if result['dpll_time'] is not None and result['bt_time'] is not None:
                if result['dpll_time'] < result['bt_time']:
                    faster_method = "DPLL"
                    speedup = result['bt_time'] / result['dpll_time']
                else:
                    faster_method = "Backtracking"
                    speedup = result['dpll_time'] / result['bt_time']
            
            writer.writerow({
                'category': category,
                'type': puzzle_type,
                'puzzle_file': puzzle_file,
                'dpll_status': result['dpll_status'],
                'dpll_time': f"{result['dpll_time']:.6f}" if result['dpll_time'] is not None else "N/A",
                'bt_status': result['bt_status'],
                'bt_time': f"{result['bt_time']:.6f}" if result['bt_time'] is not None else "N/A",
                'agreement': agreement,
                'faster_method': faster_method,
                'speedup': f"{speedup:.2f}x" if speedup is not None else "N/A"
            })
    
    print(f"\nResults saved to {output_file}")


def run_all_puzzles(output_file: str):
    """Run comparison on all Simple and Trivial Sudoku puzzles."""
    print(f"\n{'='*80}")
    print("Running All Simple and Trivial Sudoku Puzzles")
    print(f"{'='*80}\n")
    
    all_results = []
    
    # Directories to process
    directories = [
        "Trivial_Sudokus/SAT",
        "Trivial_Sudokus/UNSAT",
        "Simple_Sudokus/SAT",
        "Simple_Sudokus/UNSAT"
    ]
    
    for directory in directories:
        if os.path.exists(directory):
            print(f"\nProcessing {directory}...")
            results = compare_batch(directory, verbose=False)
            all_results.extend(results)
            print(f"Completed {directory}: {len(results)} puzzles")
        else:
            print(f"Warning: Directory {directory} not found")
    
    # Save to CSV
    save_results_to_csv(all_results, output_file)
    
    # Overall summary
    print(f"\n{'='*80}")
    print("Overall Summary")
    print(f"{'='*80}\n")
    
    total_puzzles = len(all_results)
    dpll_solved = sum(1 for r in all_results if r["dpll_status"] == "SAT")
    bt_solved = sum(1 for r in all_results if r["bt_status"] == "SAT")
    agreement = sum(1 for r in all_results if r["dpll_status"] == r["bt_status"])
    
    print(f"Total puzzles: {total_puzzles}")
    print(f"DPLL solved: {dpll_solved}/{total_puzzles} ({dpll_solved/total_puzzles*100:.1f}%)")
    print(f"Backtracking solved: {bt_solved}/{total_puzzles} ({bt_solved/total_puzzles*100:.1f}%)")
    print(f"Agreement: {agreement}/{total_puzzles} ({agreement/total_puzzles*100:.1f}%)")
    print()
    
    # Timing statistics
    dpll_times = [r["dpll_time"] for r in all_results if r["dpll_time"] is not None]
    bt_times = [r["bt_time"] for r in all_results if r["bt_time"] is not None]
    
    if dpll_times:
        print(f"DPLL average time: {sum(dpll_times)/len(dpll_times):.6f} seconds")
        print(f"DPLL min time: {min(dpll_times):.6f} seconds")
        print(f"DPLL max time: {max(dpll_times):.6f} seconds")
    
    if bt_times:
        print(f"Backtracking average time: {sum(bt_times)/len(bt_times):.6f} seconds")
        print(f"Backtracking min time: {min(bt_times):.6f} seconds")
        print(f"Backtracking max time: {max(bt_times):.6f} seconds")
    
    if dpll_times and bt_times:
        dpll_faster = sum(1 for r in all_results if r["dpll_time"] and r["bt_time"] and r["dpll_time"] < r["bt_time"])
        print(f"\nDPLL faster on: {dpll_faster}/{total_puzzles} puzzles")
        print(f"Backtracking faster on: {total_puzzles - dpll_faster}/{total_puzzles} puzzles")


def main():
    args = parse_args()
    
    if args.run_all:
        # Run all puzzles and save to CSV
        run_all_puzzles(args.output)
    elif args.inp:
        # Single puzzle comparison
        compare_single_puzzle(args.inp)
    elif args.batch:
        # Batch comparison
        results = compare_batch(args.batch)
        save_results_to_csv(results, args.output)
    else:
        print("Error: Please specify either --in <puzzle.txt>, --batch <directory>, or --run-all")
        exit(1)


if __name__ == "__main__":
    main()
