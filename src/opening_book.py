import json
import os
from board import fen_to_board, board_to_fen

class OpeningBook:
    def __init__(self, book_file):
        self.book_file = book_file
        try:
            with open(book_file, 'r') as f:
                self.book = json.load(f)
        except json.JSONDecodeError:
            self.book = {}  

    def get_move(self, board_position):
        """Returns the best move for a given board position, if available in the opening book."""
        if board_position in self.book:
            moves = self.book[board_position]
            best_move = max(moves, key=lambda move: move['win_rate'])
            return best_move['move']
        return None
    
    def add_move(self, board_position, move, win_rate):
        if board_position not in self.book:
            self.book[board_position] = []
        self.book[board_position].append({'move': move, 'win_rate': win_rate})

    def save_book(self):
        with open(self.book_file, 'w') as f:
            json.dump(self.book, f, indent=4)
            

book_file_path = os.path.join(os.path.dirname(__file__), 'book.json')
book = OpeningBook(book_file_path)
board_position = "b0b0b0b0b0b0/1b0b0b0b0b0b01/8/8/8/8/1r0r0r0r0r0r01/r0r0r0r0r0r0 b" 
book.add_move(board_position, "(2,2)", 0.6)
board_position1 = "1b01b0b0b0/r02b02b0b0/2r02b02/1r0r01b02b0/4r01b01/3r04/6r01/1r01r0r0r0 r" 
book.add_move(board_position1, "(4,5)", 0.6)
book.save_book()  