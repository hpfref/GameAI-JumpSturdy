# transposition_table.py
import hashlib
import random

class TranspositionTable:
    def __init__(self):
        self.table = {}
        self.zobrist_table = self._initialize_zobrist_table()

    def _initialize_zobrist_table(self):
        return [[[random.getrandbits(64) for _ in range(6)] for _ in range(64)] for _ in range(2)]

    def compute_zobrist_hash(self, board, player):
        h = 0
        for y in range(8):
            for x in range(8):
                piece = board[y, x]
                if piece and piece != 'X':  # Skip 'X' fields
                    piece_index = self._get_piece_index(piece)
                    h ^= self.zobrist_table[self._player_index(player)][8 * y + x][piece_index]
        return h

    def update_zobrist_hash(self, h, move, board, player):
        from_pos, to_pos = move
        piece = board[from_pos]
        target_piece = board[to_pos] if board[to_pos] else ''

        if piece and piece != 'X':
            piece_index = self._get_piece_index(piece)
            h ^= self.zobrist_table[self._player_index(player)][8 * from_pos[1] + from_pos[0]][piece_index]

        if target_piece and target_piece != 'X':
            target_index = self._get_piece_index(target_piece)
            h ^= self.zobrist_table[self._player_index(player)][8 * to_pos[1] + to_pos[0]][target_index]

        if piece and piece != 'X':
            h ^= self.zobrist_table[self._player_index(player)][8 * to_pos[1] + to_pos[0]][piece_index]

        return h

    def _get_piece_index(self, piece):
        piece_dict = {'r': 0, 'rr': 1, 'br': 2, 'b': 3, 'bb': 4, 'rb': 5}
        return piece_dict[piece]

    def _player_index(self, player):
        return 0 if player == 'b' else 1

    def store(self, zobrist_hash, depth, value, flag, best_move):
        if zobrist_hash not in self.table:
            self.table[zobrist_hash] = []
        self.table[zobrist_hash].append((depth, value, flag, best_move))

    def lookup(self, zobrist_hash):
        if zobrist_hash in self.table:
            return self.table[zobrist_hash]
        return None



EXACT, LOWERBOUND, UPPERBOUND = 0, 1, 2