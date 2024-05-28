### To import from src:
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), 'src')))
###
import time
import unittest
import timeit
from board import fen_to_board
from gamestate import select_move, select_min_max_move, evaluate


def test_function_runtime(func, *args, **kwargs):
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    runtime = end_time - start_time
    return result, runtime

def test_search_algorithms(fen):
    # Test Alpha-Beta Search
    print("Testing Alpha-Beta Search")
    best_move_ab, runtime_ab = test_function_runtime(select_move, fen)
    print(f"Alpha-Beta Best Move: {best_move_ab}, Runtime: {runtime_ab:.4f} seconds")

    # Test Min-Max Search
    print("Testing Min-Max Search")
    best_move_mm, runtime_mm = test_function_runtime(select_min_max_move, fen)
    print(f"Min-Max Best Move: {best_move_mm}, Runtime: {runtime_mm:.4f} seconds")

    return best_move_ab, runtime_ab, best_move_mm, runtime_mm

# Benchmark time of Zuggenerator execution
def test_evaluate(fen, reps, evaluate):
    # Measurement of Execution Time and Calculation of Average
    board, _ = fen_to_board(fen)
    time_total = timeit.repeat("evaluate(board)", globals=locals(), number=1, repeat=reps)
    time_avg = sum(time_total) / reps
    return time_avg



if __name__ == "__main__":
    # FENs to test
    fen_early = "b0b0b0b0b0b0/1b0b0b0b0b0b01/8/8/8/8/1r0r0r0r0r0r01/r0r0r0r0r0r0 b"
    fen_mid = "b0b0b01bb1/2b0b0bbb02/5r02/3b04/4r0b02/8/2rrr01r02/r0r0r0r01r0 r"
    fen_late = "3b02/5r02/3r04/8/8/2b02b02/2r05/6 b"

    # alpha beta / minmax
    test_search_algorithms(fen_late) #depends on max depth set in alphabeta / minmax func


    #reps = 1000
    #print("Average time early game (in ms):", test_evaluate(fen_early,reps,evaluate)*1000)
    #print("Average time mid game (in ms):", test_evaluate(fen_mid,reps,evaluate)*1000)
    #print("Average time late game (in ms):", test_evaluate(fen_late,reps,evaluate)*1000)