### To import from src:
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), 'src')))
###
import numpy as np
import pygame as pg
from board import  fen_to_board
from visuals import load_pieces, draw_board, draw_pieces


def simulate_game(fen_list, window, pieces, clock, fps):
    for fen in fen_list:
        board, _ = fen_to_board(fen)
        
        # Draw the current board state
        window.fill((0, 0, 0))
        draw_board(board, window)
        draw_pieces(board, window, pieces)
        pg.display.flip()

        # Wait for a bit to visually see the move
        clock.tick(fps)
        
        print(fen)  # Print or log the FEN to see it


def extract_fens(filepath):
    """
    Reads the log from a file and extracts all FEN strings into a list.

    Parameters:
    filepath (str): The path to the file containing the log.

    Returns:
    List[str]: A list of FEN strings.
    """
    fens = []
    
    with open(filepath, 'r') as file:
        lines = file.readlines()
    
    for line in lines:
        if '/' in line and '0' in line:
            fens.append(line.strip())
    
    return fens


if __name__ == "__main__":
    pg.init()
    window = pg.display.set_mode((800, 800))
    pg.display.set_caption("Game Simulation")
    clock = pg.time.Clock()
    
    # Load pieces (assuming a function or method to do so)
    pieces = load_pieces()  # Define this function as per your requirements

    # Extract FENs from the file
    fens = extract_fens("scripts/contest_logs/C2-AD-AI.txt")

    fps=0.4

    # Simulate the game using the extracted FENs
    simulate_game(fens, window, pieces, clock, fps)
    
    # Quit pygame
    pg.quit()
