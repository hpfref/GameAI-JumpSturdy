import unittest
import timeit
from zuggenerator import legal_moves


if __name__ == '__main__':
    
    fen_early = "b0b0b0b0b0b0/1b0b0b0b0b0b01/8/8/8/8/1r0r0r0r0r0r01/r0r0r0r0r0r0 b"
    fen_mid = "b0b0b01bb1/2b0b0bbb02/5r02/3b04/4r0b02/8/2rrr01r02/r0r0r0r01r0 r"
    fen_late = "3b02/5r02/3r04/8/8/2b02b02/2r05/6 b"
    
    # Number of Executions
    num_repeats = 1000
        
    # Measurement of Execution Time and Calculation of Average
    time_early = timeit.repeat("legal_moves(fen_early)", globals=locals(), number=1, repeat=num_repeats)
    avg_early = sum(time_early) / num_repeats

    time_mid = timeit.repeat("legal_moves(fen_mid)", globals=locals(), number=1, repeat=num_repeats)
    avg_mid = sum(time_mid) / num_repeats

    time_late = timeit.repeat("legal_moves(fen_late)", globals=locals(), number=1, repeat=num_repeats)
    avg_late = sum(time_late) / num_repeats
        
    print("Average time early game:", avg_early)
    print("Average time mid game:", avg_mid)
    print("Average time late game:", avg_late)
