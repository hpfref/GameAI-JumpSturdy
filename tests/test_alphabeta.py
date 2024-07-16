### To import from src:
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), 'src')))
###
import time
import unittest
import timeit
from board import fen_to_board
from move_selection import select_move, select_min_max_move
from evaluate import evaluate
import cProfile
import pstats


def test_function_runtime(func, *args, **kwargs):
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    runtime = end_time - start_time
    return result, runtime

def test_minimax(fen, select_min_max_move):
    # Test Min-Max Search
    print("Testing Min-Max Search")
    best_move_mm, runtime_mm = test_function_runtime(select_min_max_move, fen)
    
    time_total_mm = timeit.repeat("select_min_max_move(fen)", globals=locals(), number=1, repeat=10)
    time_avg_mm = sum(time_total_mm) / 10
    print(f"Min-Max Best Move: {best_move_mm}, Average MinMax Runtime: {time_avg_mm} seconds")
    #print(f"Min-Max Best Move: {best_move_mm}, Runtime: {runtime_mm:.4f} seconds")

    return best_move_mm, runtime_mm

def test_alphabeta(fen, select_move):
    # Test Alpha-Beta Search6
    print("Testing Alpha-Beta Search")
    best_move_ab, runtime_ab = test_function_runtime(select_move, fen, 100000)
    #
    time_total_ab = timeit.repeat("select_move(fen, 100000)", globals=locals(), number=1, repeat=10)
    time_avg_ab = sum(time_total_ab) / 10
    print(f"Alpha-Beta Best Move: {best_move_ab}, Average Alpha-Beta Runtime: {time_avg_ab} seconds")
    #print(f"Alpha-Beta Best Move: {best_move_ab}, Runtime: {runtime_ab:.4f} seconds")
    return best_move_ab, runtime_ab

# Benchmark time of Zuggenerator execution
def test_evaluate(fen, reps, evaluate):
    # Measurement of Execution Time and Calculation of Average
    board, _ = fen_to_board(fen)
    time_total = timeit.repeat("evaluate(board)", globals=locals(), number=1, repeat=reps)
    time_avg = sum(time_total) / reps
    return time_avg



if __name__ == "__main__":
    # FENs to test
    fen_start = 'b0b0b0b0b0b0/1b0b0b0b0b0b01/8/8/8/8/1r0r0r0r0r0r01/r0r0r0r0r0r0 b'
    fen_early = "b0b0b0b0b0b0/1b0b0b0b0b0b01/8/8/8/8/1r0r0r0r0r0r01/r0r0r0r0r0r0 b"
    fen_mid = "b0b0b01bb1/2b0b0bbb02/5r02/3b04/4r0b02/8/2rrr01r02/r0r0r0r01r0 r"
    fen_late = "3b02/5r02/3r04/8/8/2b02b02/2r05/6 b"
    fen_o_late = "6/1bb1b02b01/8/2r05/3r01b02/5r0r02/2rr1r03/6 b"
    #cProfile.run('test_search_algorithms(fen_mid, select_move, select_min_max_move)', 'time')
    
    # alphabeta test
    profiler = cProfile.Profile()
    profiler.enable()
    test_alphabeta(fen_mid, select_move)
    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats('tottime')
    stats.print_stats()
    
    # minimax test
    #test_minimax(fen_start, select_min_max_move)
    # NOTE: Benchmarking those results with the wiki doesn't work because groups don't have the exact same 
    # amount of examined nodes and often don't even use the same boards.
    # When comparing the numbers for the start_fen with other teams, the node counts are pretty close to each other.
    # We believe that the differences might be due to erroneous node counting or move generators.

    # evaluate test
    #reps = 1000
    #print("Average time early game (in ms):", test_evaluate(fen_early,reps,evaluate)*1000)
    #print("Average time mid game (in ms):", test_evaluate(fen_mid,reps,evaluate)*1000)
    #print("Average time late game (in ms):", test_evaluate(fen_late,reps,evaluate)*1000)