import tensorflow as tf
import re
import numpy as np
from sklearn.model_selection import train_test_split
import keras
from keras import layers
from board import fen_to_board
from gamestate import evaluateFREF
import keras
from tensorflow import keras


# This was a brief attempt at implementing a neural network to approximate the evaluation function
# Not suitable and functional for us, as usually, chess engines trained by NN use an approximating evaluation function as the output - typically Stockfish
# Not applicable for us, as we do not have a "correct" evaluation function for guidance
# Reinforcement Learning could be an option here, but the reward would have to be "game won", hence an incredible amount of games would be required for training
# - not feasible for us within the time frame


def parse_game_logs(game_logs):
    lines = game_logs.strip().split("\n")
    parsed_entries = []
    
    i = 0  
    while i < len(lines) - 1:  
        move_line = lines[i]
        board_state_line = lines[i + 1]  
    
        match = re.match(r"(Red|Blue) move: (.+?)\s*---\s*time left: (\d+)", move_line)
        if match:
            move = match.group(2)
            time_left = int(match.group(3))
            
            parsed_entries.append((board_state_line, move, time_left))
            
            i += 2  
        else:
            i += 1  
    print(parsed_entries)
    return parsed_entries

game_logs = """
Red move: B8-B7   ---  time left: 118506
b0b0b0b0b0b0/1b0b0b0b0b0b01/8/8/8/8/1rrr0r0r0r0r01/1r0r0r0r0r0 b
Blue move: E2-D2   ---  time left: 118529
b0b0b0b0b0b0/1b0b0bb1b0b01/8/8/8/8/1rrr0r0r0r0r01/1r0r0r0r0r0 r
Red move: B7-A5   ---  time left: 117359
b0b0b0b0b0b0/1b0b0bb1b0b01/8/8/r07/8/1r0r0r0r0r0r01/1r0r0r0r0r0 b
Blue move: G2-H2   ---  time left: 117067
b0b0b0b0b0b0/1b0b0bb1b01b0/8/8/r07/8/1r0r0r0r0r0r01/1r0r0r0r0r0 r
Red move: D8-D7   ---  time left: 116037
b0b0b0b0b0b0/1b0b0bb1b01b0/8/8/r07/8/1r0r0rrr0r0r01/1r01r0r0r0 b
Blue move: D2-C4   ---  time left: 115617
b0b0b0b0b0b0/1b0b0b01b01b0/8/2b05/r07/8/1r0r0rrr0r0r01/1r01r0r0r0 r
Red move: A5-A4   ---  time left: 114264
b0b0b0b0b0b0/1b0b0b01b01b0/8/r01b05/8/8/1r0r0rrr0r0r01/1r01r0r0r0 b
Blue move: B2-B3   ---  time left: 114153
b0b0b0b0b0b0/2b0b01b01b0/1b06/r01b05/8/8/1r0r0rrr0r0r01/1r01r0r0r0 r
Red move: A4-B3   ---  time left: 110513
b0b0b0b0b0b0/2b0b01b01b0/1r06/2b05/8/8/1r0r0rrr0r0r01/1r01r0r0r0 b
Blue move: C2-B3   ---  time left: 112695
b0b0b0b0b0b0/3b01b01b0/1b06/2b05/8/8/1r0r0rrr0r0r01/1r01r0r0r0 r
Red move: D7-C5   ---  time left: 105515
b0b0b0b0b0b0/3b01b01b0/1b06/2b05/2r05/8/1r0r0r0r0r0r01/1r01r0r0r0 b
Blue move: C1-B1   ---  time left: 111244
bb1b0b0b0b0/3b01b01b0/1b06/2b05/2r05/8/1r0r0r0r0r0r01/1r01r0r0r0 r
Red move: E8-E7   ---  time left: 99116
bb1b0b0b0b0/3b01b01b0/1b06/2b05/2r05/8/1r0r0r0rrr0r01/1r02r0r0 b
Blue move: F1-E1   ---  time left: 109771
bb1b0bb1b0/3b01b01b0/1b06/2b05/2r05/8/1r0r0r0rrr0r01/1r02r0r0 r
"""
def encode_board_state(board_state_str):
    piece_to_int = {'b': 1, 'bb': 2, 'rb': 3, 'r': 4, 'rr': 5, 'br': 6}
    board_encoded = []
    board_state_str = board_state_str[:-2].replace('/', '')
    i = 0
    while i < len(board_state_str):
        if i < len(board_state_str) - 1 and board_state_str[i:i+2] in piece_to_int:
            board_encoded.append(piece_to_int[board_state_str[i:i+2]])
            i += 2  
        elif board_state_str[i] in piece_to_int:
            board_encoded.append(piece_to_int[board_state_str[i]])
            i += 1
        else:
            board_encoded.extend([0] * int(board_state_str[i]))
            i += 1
    return board_encoded

    
def encode_move(move_str):
    col_to_index = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7}
    from_pos, to_pos = move_str.split('-')
    from_col, from_row = col_to_index[from_pos[0]], int(from_pos[1]) - 1
    to_col, to_row = col_to_index[to_pos[0]], int(to_pos[1]) - 1
    from_index = from_row * 8 + from_col
    to_index = to_row * 8 + to_col
    return from_index, to_index

def normalize_time_left(time_left, max_time=120000):
    time_left = max(0, min(time_left, max_time))
    normalized_time = time_left / max_time
    return normalized_time

def preprocess_data(parsed_entries):
    X, y = [], []
    for entry in parsed_entries:
        board_state_str, move_str, time_left = entry
        board, player = fen_to_board(board_state_str)
        board_state_encoded = encode_board_state(board_state_str)
        move_encoded = encode_move(move_str)
        time_left_normalized = normalize_time_left(time_left)
        input_vector = board_state_encoded + list(move_encoded) + [time_left_normalized]
        X.append(input_vector)
        move_eval = evaluateFREF(board, player)
        y.append(move_eval)  
        
    return np.array(X), np.array(y)



parsed_entries = parse_game_logs(game_logs)
X, y = preprocess_data(parsed_entries)
#print(X, y)
model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(128, activation='relu', input_shape=(len(X[0]),)),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(1, activation='linear')
])
model.compile(optimizer=tf.keras.optimizers.Adam(), loss='mean_squared_error')

model.fit(X, y, epochs=10, batch_size=32, validation_split=0.1)

import os

script_dir = os.path.dirname(__file__)

output_file_name = "model_plot.png"

dot_img_file = os.path.join(script_dir, output_file_name)
keras.utils.plot_model(model, to_file=dot_img_file, show_shapes=True)