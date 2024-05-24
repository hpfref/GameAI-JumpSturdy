### To import from src:
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), 'src')))
###
import unittest
import timeit
from move_gen import legal_moves, translate_moves
from board import fen_to_board


# Unit-Test for correct output of Zuggenerator
class LegalMovesTest(unittest.TestCase):
    
    ### Groups with erroneaus wiki entries: O, I, X, E, U, AC mid game, Z, T endgame 2, AG endgame, AA, Q, W, V, Sturdy jumper midgame

    def test_n_moves_startFEN(self):
        fen = "b0b0b0b0b0b0/1b0b0b0b0b0b01/8/8/8/8/1r0r0r0r0r0r01/r0r0r0r0r0r0 b"
        expected_moves = ['B2-A2', 'B2-C2', 'B2-B3', 'C2-B2', 'C2-D2', 'C2-C3', 'D2-C2', 'D2-E2', 'D2-D3', 'E2-D2', 'E2-F2', 'E2-E3', 'F2-E2', 'F2-G2', 'F2-F3', 'G2-F2', 'G2-H2', 'G2-G3', 'B1-C1', 'B1-B2', 'C1-B1', 'C1-D1', 'C1-C2', 'D1-C1', 'D1-E1', 'D1-D2', 'E1-D1', 'E1-F1', 'E1-E2', 'F1-E1', 'F1-G1', 'F1-F2', 'G1-F1', 'G1-G2']
        board, player  = fen_to_board(fen)
        moves = translate_moves(legal_moves(board, player))
        self.assertEqual(len(moves), 34, "Incorrect number of moves for startFEN")
        self.assertEqual(sorted(moves), sorted(expected_moves), "Incorrect moves for startFEN")

    def test_group_A_late_game(self):
        fen = "6/1b06/1r03bb2/2r02b02/8/5r0r0/2r0r04/6 r"
        expected_moves = ["B3-A3", "B3-C3", "C4-B4", "C4-D4", "C4-C3", "F6-E6", "F6-G6", "F6-F5", "G6-F6", "G6-H6", "G6-G5", "C7-B7", "C7-D7", "C7-C6", "D7-C7", "D7-E7", "D7-D6"]
        board, player = fen_to_board(fen)
        moves = translate_moves(legal_moves(board, player))
        self.assertEqual(len(moves), 17, "Incorrect number of moves for group A late game")
        self.assertEqual(sorted(moves), sorted(expected_moves), "Incorrect moves for group A late game")
    
    def test_group_A_mid_game(self):
        fen = "6/1b0b0b0b0b0b01/1b0b0b0b0b0b01/8/8/1r0r0r0r0r0r01/1r0r0r0r0r0r01/6 b"
        expected_moves = ["B2-C2", "B2-A2", "B2-B3", "C2-D2", "C2-B2", "C2-C3", "D2-E2", "D2-C2", "D2-D3","E2-F2", "E2-D2", "E2-E3", "F2-G2", "F2-E2", "F2-F3", "G2-H2", "G2-F2", "G2-G3","B3-C3", "B3-A3", "B3-B4", "C3-D3", "C3-B3", "C3-C4", "D3-E3", "D3-C3", "D3-D4","E3-F3", "E3-D3", "E3-E4", "F3-G3", "F3-E3", "F3-F4", "G3-H3", "G3-F3", "G3-G4"]
        board, player = fen_to_board(fen)
        moves = translate_moves(legal_moves(board, player))
        self.assertEqual(len(moves), 36, "Incorrect number of moves for group A mid game")
        self.assertEqual(sorted(moves), sorted(expected_moves), "Incorrect moves for group A mid game")
    
    def test_group_AL_opening_strategy(self):
        fen = "6/1bbbbbbbbbbbb1/8/8/8/1r0r0r0r0r0r01/8/r0r0r0r0r0r0 b"
        expected_moves = ["B2-A4", "B2-C4", "B2-D3", "C2-B4", "C2-D4", "C2-A3", "C2-E3", "D2-C4", "D2-E4", "D2-B3", "D2-F3", "E2-D4", "E2-F4", "E2-C3", "E2-G3", "F2-E4", "F2-G4", "F2-D3", "F2-H3", "G2-F4", "G2-H4", "G2-E3"]
        board, player = fen_to_board(fen)
        moves = translate_moves(legal_moves(board, player))
        self.assertEqual(len(moves), 22, "Incorrect number of moves for group AL opening strategy")
        self.assertEqual(sorted(moves), sorted(expected_moves), "Incorrect moves for group AL opening strategy")

    def test_group_AL_end_game(self):
        fen = "8/2b02b02/2r02r02/8/8/2b02b02/2r02r02/8 b"
        expected_moves = ["C6-B6", "C6-D6", "F6-E6", "F6-G6", "C2-B2", "C2-D2", "F2-E2", "F2-G2"]
        board, player = fen_to_board(fen)
        moves = translate_moves(legal_moves(board, player))
        self.assertEqual(len(moves), 8, "Incorrect number of moves for group AL end game")
        self.assertEqual(sorted(moves), sorted(expected_moves), "Incorrect moves for group AL end game")
    
    def test_group_M_endgame_with_edge_cases(self):
        fen = "6/1b06/8/2b01bbb0rb1/1rbr0rr1r0r01/8/b07/6 b"
        expected_moves = ["B2-A2", "B2-B3", "B2-C2", "C4-B4", "C4-D4", "C4-D5", "E4-C5", "E4-D6", "E4-F6", "E4-G5", "F4-G5", "G4-E5", "G4-F6", "G4-H6", "B5-A7", "B5-C7", "B5-D6", "A7-B7"]
        board, player = fen_to_board(fen)
        moves = translate_moves(legal_moves(board, player))
        self.assertEqual(len(moves), 18, "Incorrect number of moves for Jump Mccurdy endgame with edge cases")
        self.assertEqual(sorted(moves), sorted(expected_moves), "Incorrect moves for Jump Mccurdy endgame with edge cases")

    def test_group_M_endgame_with_knight(self):
        fen = "6/8/6rr1/8/8/8/b0b0b05/6 r"
        expected_moves = ["G3-F1", "G3-E2"]
        board, player = fen_to_board(fen)
        moves = translate_moves(legal_moves(board, player))
        self.assertEqual(len(moves), 2, "Incorrect number of moves for Jump Mccurdy endgame with knight")
        self.assertEqual(sorted(moves), sorted(expected_moves), "Incorrect moves for Jump Mccurdy endgame with knight")
     
    def test_group_L_example_position(self):
        fen = "3b02/2bb2b02/5b0bb1/2r0b04/2rb3b01/1rr1rr2r0r0/5r02/2rr3 b"
        expected_moves = ["C2-A3", "C2-B4", "C2-D4", "C2-E3", "C5-A6", "C5-B7", "C5-D7", "C5-E6", "D4-D5", "D4-E4", "E1-D1", "E1-E2", "E1-F1", "F2-E2", "F2-F3", "F2-G2", "F3-E3", "F3-F4", "G3-E4", "G3-F5", "G3-H5", "G5-F5", "G5-H5", "G5-H6"]
        board, player = fen_to_board(fen)
        moves = translate_moves(legal_moves(board, player))
        self.assertEqual(len(moves), 24, "Incorrect number of moves for gang³ example position")
        self.assertEqual(sorted(moves), sorted(expected_moves), "Incorrect moves for gang³ example position")

    def test_group_L_early_to_mid_game(self):
        fen = "1b01b0b01/b01bb0b01bb0b01/1b06/8/7b0/1r02r01rr1/2rr2rr2/r0r01r0r01 b"
        expected_moves = ["A2-A3", "A2-B2", "B3-A3", "B3-B4", "B3-C3", "C1-B1", "C1-D1", "C2-A3", "C2-B4", "C2-D4", "C2-E3", "D2-D3", "D2-E2", "E1-D1", "E1-E2", "E1-F1", "F1-E1", "F1-G1", "F2-D3", "F2-E4", "F2-G4", "F2-H3", "G2-G3", "G2-H2", "H5-G5", "H5-G6", "H5-H6"]
        board, player = fen_to_board(fen)
        moves = translate_moves(legal_moves(board, player))
        self.assertEqual(len(moves), 27, "Incorrect number of moves for gang³ early- to mid-game position")
        self.assertEqual(sorted(moves), sorted(expected_moves), "Incorrect moves for gang³ early- to mid-game position")

    
    def test_group_AF_mid_game_with_rook(self):
        fen = "b02b01b0/3b01b02/b02b02b01/b01b05/5r02/1r02r02r0/2rrr02r01/r03r01 b"
        expected_moves = ["B1-B2", "B1-C1", "E1-E2", "E1-D1", "E1-F1", "G1-G2", "G1-F1", "D2-D3", "D2-C2", "D2-E2", "F2-F3", "F2-E2", "F2-G2", "A3-A4", "A3-B3", "D3-D4", "D3-C3", "D3-E3", "G3-G4", "G3-F3", "G3-H3", "A4-A5", "A4-B4", "C4-C5", "C4-B4", "C4-D4"]
        board, player = fen_to_board(fen)
        moves = translate_moves(legal_moves(board, player))
        self.assertEqual(len(moves), 26, "Incorrect number of moves for mid-game with rook")
        self.assertEqual(sorted(moves), sorted(expected_moves), "Incorrect moves for mid-game with rook")

    def test_group_AF_end_game_with_rook(self):
        fen = "6/1b03b02/3b01r0b01/bb2b04/1b01r02r0r0/1r0r02rbr01/1r06/6 r"
        expected_moves = ["F3-E3", "D5-C5", "D5-E5", "G5-G4", "G5-F5", "G5-H5", "H5-H4", "H5-G5", "B6-A6", "B6-C6", "C6-C5", "C6-B6", "C6-B5", "C6-D6", "G6-G5", "G6-H6", "B7-B6", "B7-A7", "B7-C7"]
        board, player = fen_to_board(fen)
        moves = translate_moves(legal_moves(board, player))
        self.assertEqual(len(moves), 19, "Incorrect number of moves for end-game with rook")
        self.assertEqual(sorted(moves), sorted(expected_moves), "Incorrect moves for end-game with rook")

    def test_group_AI_end_game(self):
        fen = "2b03/8/8/3b0b03/2b03b01/2r03r01/2r05/6 r"
        expected_moves = ["C6-B6", "C6-D6", "C7-B7", "C7-C6", "C7-D7", "G6-F6", "G6-H6"]
        board, player = fen_to_board(fen)
        moves = translate_moves(legal_moves(board, player))
        self.assertEqual(len(moves), 7, "Incorrect number of moves for AI end-game")
        self.assertEqual(sorted(moves), sorted(expected_moves), "Incorrect moves for AI end-game")

    def test_group_AI_mid_game(self):
        fen = "2bbbb1b0/1b06/1b01b04/4b03/4r03/3r02b01/1r0r02rr2/2rr2r0 b"
        expected_moves = ["B2-A2", "B2-B3", "B2-C2", "B3-A3", "B3-B4", "B3-C3", "D1-B2", "D1-C3", "D1-E3", "D1-F2", "D3-C3", "D3-D4", "D3-E3", "E1-C2", "E1-D3", "E1-F3", "E1-G2", "E4-D4", "E4-F4", "G1-F1", "G1-G2", "G6-F6", "G6-F7", "G6-G7", "G6-H6"]
        board, player = fen_to_board(fen)
        moves = translate_moves(legal_moves(board, player))
        self.assertEqual(len(moves), 25, "Incorrect number of moves for AI mid-game")
        self.assertEqual(sorted(moves), sorted(expected_moves), "Incorrect moves for AI mid-game")

    def test_group_AJ_early_game(self):
        fen = "b0b01b02/3bbb0bb2/2b03bb1/8/2b01r03/5r02/1rr1r0rr1rr1/1rr4 b"
        expected_moves = ["B1-B2", "B1-C1", "C1-B1", "C1-C2", "C1-D1", "E1-D1", "E1-E2", "E1-F1", "D2-B3", "D2-C4", "D2-E4", "D2-F3", "E2-E3", "F2-D3", "F2-E4", "F2-G4", "F2-H3", "C3-B3", "C3-C4", "C3-D3", "G3-E4", "G3-F5", "G3-H5", "C5-B5", "C5-C6", "C5-D5"]
        board, player = fen_to_board(fen)
        moves = translate_moves(legal_moves(board, player))
        self.assertEqual(len(moves), 26, "Incorrect number of moves for early game")
        self.assertEqual(sorted(moves), sorted(expected_moves), "Incorrect moves for early game")

    def test_group_AJ_end_game(self):
        fen = "6/1b02br3/6bb1/2b0b04/2r04r0/8/1rr1r0rr1r01/6 b"
        expected_moves = ["B2-A2", "B2-B3", "B2-C2", "G3-E4", "G3-F5", "G3-H5", "C4-B4", "C4-D4", "D4-C4", "D4-C5", "D4-D5", "D4-E4"]
        board, player = fen_to_board(fen)
        moves = translate_moves(legal_moves(board, player))
        self.assertEqual(len(moves), 12, "Incorrect number of moves for end game")
        self.assertEqual(sorted(moves), sorted(expected_moves), "Incorrect moves for end game")

    
    def test_group_AC_5th_move(self):
        fen = "2bbb0b0b0/1bbb0b0b0b0b01/8/8/8/1r01r04/2r01r0r0r01/r0r0r0r0r0r0 b"
        expected_moves = ["C2-C3", "D2-D3", "E2-E3", "F2-F3", "G2-G3", "G2-H2", "F1-E1", "G1-F1", "D2-C2", "E2-D2", "F2-E2", "G2-F2", "E1-E2", "F1-F2", "G1-G2", "E1-F1", "F1-G1", "C2-D2", "D2-E2", "E2-F2", "F2-G2", "D1-C3", "B2-A4", "D1-E3", "B2-C4", "B2-D3", "D1-F2"]
        
        board, player = fen_to_board(fen)
        moves = translate_moves(legal_moves(board, player))
        self.assertEqual(len(moves), 27, "Incorrect number of moves for group AC/DC! 5th move")
        self.assertEqual(sorted(moves), sorted(expected_moves), "Incorrect moves for group AC/DC! 5th move")
    
    def test_group_AB_before_endgame(self):
        fen = "1b0b0b0b0b0/1b01bb2b01/8/3bb1b02/5rr2/2r01r03/2rr5/r0r0r0r0r0r0 b"
        expected_moves = ["C1-B1", "C1-C2", "C1-D1", "D1-C1", "D1-E1", "E1-D1", "E1-E2", "E1-F1", "F1-E1", "F1-F2", "F1-G1", "G1-F1", "G1-G2", "B2-A2", "B2-B3", "B2-C2", "D2-B3", "D2-C4", "D2-E4", "D2-F3", "G2-F2", "G2-G3", "G2-H2", "D4-B5", "D4-C6", "D4-E6", "D4-F5", "F4-E4", "F4-G4"]
        
        board, player = fen_to_board(fen)
        moves = translate_moves(legal_moves(board, player))
        self.assertEqual(len(moves), 29, "Incorrect number of moves for group (Blut)Gruppe AB before endgame")
        self.assertEqual(sorted(moves), sorted(expected_moves), "Incorrect moves for group (Blut)Gruppe AB before endgame")

    def test_group_AB_before_last_move(self):
        fen = "b0b0b01b01/2b03b01/8/3b01b02/1b01r01r02/2br1r03/b01r02r02/2r0r0r01 r"
        expected_moves = ["F8-G8", "F8-F7", "F8-E8", "E8-F8", "E8-E7", "E8-D8", "D8-E8", "D8-D7", "D8-C8", "F7-G7", "F7-F6", "F7-E7", "C7-D7", "C7-B7", "E6-F6", "E6-E5", "E6-D6", "C6-E5", "C6-D4", "C6-B4", "C6-A5", "F5-G5", "F5-E5", "D5-E5", "D5-C5"]
        
        board, player = fen_to_board(fen)
        moves = translate_moves(legal_moves(board, player))
        self.assertEqual(len(moves), 25, "Incorrect number of moves for group (Blut)Gruppe AB before last move")
        self.assertEqual(sorted(moves), sorted(expected_moves), "Incorrect moves for group (Blut)Gruppe AB before last move")

    def test_group_G_early_game(self):
        fen = "b01b0b0b0b0/1b0b01b01b01/3b01b02/2b05/8/2r0r01rr2/1r04r01/r0r0r0r0r0r0 r"
        expected_moves = ["B8-B7", "B8-C8", "C8-B8", "C8-C7", "C8-D8", "D8-C8", "D8-D7", "D8-E8", "E8-D8", "E8-E7", "E8-F8", "F8-E8", "F8-F7", "F8-G8", "G8-F8", "G8-G7", "B7-A7", "B7-B6", "B7-C7", "C6-B6", "C6-C5", "C6-D6", "D6-C6", "D6-D5", "D6-E6", "G7-F7", "G7-G6", "G7-H7", "F6-D5", "F6-E4", "F6-G4", "F6-H5"]
        
        board, player = fen_to_board(fen)
        moves = translate_moves(legal_moves(board, player))
        self.assertEqual(len(moves), 32, "Incorrect number of moves for group G early game")
        self.assertEqual(sorted(moves), sorted(expected_moves), "Incorrect moves for group G early game")

    def test_group_G_late_game(self):
        fen = "b01b01b01/8/2b03b01/1b06/1r01b01b02/3r04/2r03r01/4r01 r"
        expected_moves = ["F8-E8", "F8-F7", "F8-G8", "C7-B7", "C7-C6", "C7-D7", "G7-F7", "G7-G6", "G7-H7", "D6-C6", "D6-E6", "B5-A5", "B5-C5"]
        
        board, player = fen_to_board(fen)
        moves = translate_moves(legal_moves(board, player))
        self.assertEqual(len(moves), 13, "Incorrect number of moves for group G late game")
        self.assertEqual(sorted(moves), sorted(expected_moves), "Incorrect moves for group G late game")

    def test_group_AD_middlegame(self):
        fen = "b0b0b01bb1/2b0b0bbb02/5r02/3b04/4r0b02/8/2rrr01r02/r0r0r0r01r0 r"
        expected_moves = ["B8-B7", "B8-C8", "C8-B8", "C8-D8", "D8-C8", "D8-E8", "D8-D7", "E8-D8", "E8-F8", "E8-E7", "G8-F8", "G8-G7", "C7-A6", "C7-B5", "C7-D5", "C7-E6", "D7-D6", "D7-E7", "F7-E7", "F7-G7", "F7-F6", "E5-D5", "E5-D4", "E5-E4", "F3-E3", "F3-E2", "F3-G3"]
        
        board, player = fen_to_board(fen)
        moves = translate_moves(legal_moves(board, player))
        self.assertEqual(len(moves), 27, "Incorrect number of moves for group AD middlegame")
        self.assertEqual(sorted(moves), sorted(expected_moves), "Incorrect moves for group AD middlegame")

    def test_group_AD_endgame(self):
        fen = "3b02/5r02/3r04/8/8/2b02b02/2r05/6 b"
        expected_moves = ["C6-B6", "C6-D6", "F6-E6", "F6-G6", "F6-F7", "E1-D1", "E1-F1", "E1-E2", "E1-F2"]
        
        board, player = fen_to_board(fen)
        moves = translate_moves(legal_moves(board, player))
        self.assertEqual(len(moves), 9, "Incorrect number of moves for group AD endgame")
        self.assertEqual(sorted(moves), sorted(expected_moves), "Incorrect moves for group AD endgame")

    def test_group_Pepe_endgame(self):
        fen = '2b02bb/1bb2b03/5bb2/8/1r03r02/6r01/8/r01r01rrr0 b'
        expected_moves = ['D1-C1', 'D1-D2', 'D1-E1', 'G1-E2', 'G1-H3', 'B2-A4', 'B2-C4', 'B2-D3', 'E2-D2', 'E2-E3', 'E2-F2', 'F3-D4', 'F3-E5', 'F3-G5', 'F3-H4']
        
        board, player = fen_to_board(fen)
        moves = translate_moves(legal_moves(board, player))
        self.assertEqual(len(moves), 15, "Incorrect number of moves for group Pepe endgame")
        self.assertEqual(sorted(moves), sorted(expected_moves), "Incorrect moves for group Pepe endgame")

    def test_group_Pepe_midgame(self):
        fen = 'b01bbb01b0/1b02b03/3bbr01b01/8/3rr1b0b01/8/2r01r01rr1/r0r0r01r01 r'
        expected_moves = ['B8-B7', 'B8-C8', 'C8-C7', 'C8-B8', 'C8-D8', 'D8-D7', 'D8-C8', 'D8-E8', 'F8-F7', 'F8-E8', 'F8-G8', 'C7-C6', 'C7-B7', 'C7-D7', 'E7-E6', 'E7-D7', 'E7-F7', 'G7-E6', 'G7-F5', 'G7-H5', 'D5-B4', 'D5-C3', 'D5-E3', 'D5-F4', 'E3-F3']
        
        board, player = fen_to_board(fen)
        moves = translate_moves(legal_moves(board, player))
        self.assertEqual(len(moves), 25, "Incorrect number of moves for group Pepe midgame")
        self.assertEqual(sorted(moves), sorted(expected_moves), "Incorrect moves for group Pepe midgame")

    def test_group_K_early_game(self):
        fen = 'b0b0b0b0b0b0/1bb3b0b01/3b04/4b03/5r02/1r02r03/2r0r02r01/r0r0r0r0r0r0 b'
        expected_moves = ['B1-C1', 'C1-B1', 'C1-C2', 'C1-D1', 'D1-C1', 'D1-D2', 'D1-E1', 'E1-D1', 'E1-E2', 'E1-F1', 'F1-E1', 'F1-F2', 'F1-G1', 'G1-F1', 'G1-G2', 'B2-A4', 'B2-C4', 'B2-D3', 'F2-E2', 'F2-F3', 'F2-G2', 'G2-F2', 'G2-G3', 'G2-H2', 'D3-C3', 'D3-D4', 'D3-E3', 'E4-D4', 'E4-E5', 'E4-F5', 'E4-F4']
        
        board, player = fen_to_board(fen)
        moves = translate_moves(legal_moves(board, player))
        self.assertEqual(len(moves), 31, "Incorrect number of moves for group K early game")
        self.assertEqual(sorted(moves), sorted(expected_moves), "Incorrect moves for group K early game")

    def test_group_K_endgame(self):
        fen = '1bbb01b0b0/4b03/4rr1b01/2b02b02/5r02/1r06/3r02r01/1rrr01r01 r'
        expected_moves = ['C8-A7', 'C8-B6', 'C8-D6', 'C8-E7', 'D8-D7', 'D8-E8', 'F8-E8', 'F8-F7', 'F8-G8', 'D7-C7', 'D7-D6', 'D7-E7', 'G7-F7', 'G7-G6', 'G7-H7', 'B6-A6', 'B6-B5', 'B6-C6', 'F5-E5', 'F5-G5', 'E3-C2', 'E3-D1', 'E3-F1', 'E3-G2']
        
        board, player = fen_to_board(fen)
        moves = translate_moves(legal_moves(board, player))
        self.assertEqual(len(moves), 24, "Incorrect number of moves for group K endgame")
        self.assertEqual(sorted(moves), sorted(expected_moves), "Incorrect moves for group K endgame")

    def test_group_N_mid_end_game(self):
        fen = 'b0b01b0b0b0/8/4b0b02/3br4/6b01/2rr3rb1/4rr3/r0r02r0r0 r'
        expected_moves = ['C6-E5', 'C8-B8', 'C6-B4', 'C8-C7', 'C8-D8', 'C6-A5', 'E7-D5', 'E7-G6', 'E7-F5', 'G8-F8', 'G8-G7', 'B8-B7', 'B8-C8', 'D4-B3', 'F8-F7', 'F8-G8', 'D4-C2', 'F8-E8', 'D4-F3', 'D4-E2']
        
        board, player = fen_to_board(fen)
        moves = translate_moves(legal_moves(board, player))
        self.assertEqual(len(moves), 20, "Incorrect number of moves for group N mid/end game")
        self.assertEqual(sorted(moves), sorted(expected_moves), "Incorrect moves for group N mid/end game")

    def test_group_N_end_game(self):
        fen = 'b0b0b0b0b0b0/8/5b01b0/5r0b01/3b04/4r0rr1rb/3r04/r0r0r0r01r0 b'
        expected_moves = ['H3-H4', 'C1-B1', 'C1-D1', 'E1-E2', 'G4-G5', 'G1-G2', 'B1-C1', 'D5-D6', 'D1-D2', 'F3-E3', 'F1-G1', 'F3-G3', 'F1-E1', 'H6-G8', 'H3-G3', 'C1-C2', 'G4-H4', 'E1-D1', 'E1-F1', 'G1-F1', 'B1-B2', 'D1-E1', 'D5-C5', 'D5-E6', 'D1-C1', 'D5-E5', 'F1-F2', 'H6-F7']
        
        board, player = fen_to_board(fen)
        moves = translate_moves(legal_moves(board, player))
        self.assertEqual(len(moves), 28, "Incorrect number of moves for group N end game")
        self.assertEqual(sorted(moves), sorted(expected_moves), "Incorrect moves for group N end game")

    def test_group_T_endgame_1(self):
        fen = '6/1b06/2bb1b0b02/6bb1/1r0br5/3r0rr3/8/4r0r0 b'
        expected_moves = ['B2-A2', 'B2-C2', 'B2-B3', 'C3-A4', 'C3-E4', 'C3-B5', 'C3-D5', 'E3-D3', 'E3-F3', 'E3-E4', 'F3-E3', 'F3-G3', 'F3-F4', 'G4-E5', 'G4-F6', 'G4-H6']
        
        board, player = fen_to_board(fen)
        moves = translate_moves(legal_moves(board, player))
        self.assertEqual(len(moves), 16, "Incorrect number of moves for group T endgame 1")
        self.assertEqual(sorted(moves), sorted(expected_moves), "Incorrect moves for group T endgame 1")

    def test_group_J_endgame(self):
        fen = '6/1b06/1r0b02bb2/2r02b02/8/5rr2/2r03r01/6 b'
        expected_moves = ['B2-A2', 'B2-C2', 'C3-D3', 'F4-E4', 'F4-G4', 'F4-F5', 'F3-D4', 'F3-E5', 'F3-G5', 'F3-H4']
        
        board, player = fen_to_board(fen)
        moves = translate_moves(legal_moves(board, player))
        self.assertEqual(len(moves), 10, "Incorrect number of moves for group J endgame")
        self.assertEqual(sorted(moves), sorted(expected_moves), "Incorrect moves for group J endgame")

    def test_group_J_midgame(self):
        fen = 'b0b04/b02bb2b01/2b05/4rb3/6b01/2r04r0/1r01r0r01r01/r0r04 r'
        expected_moves = ['B8-B7', 'B8-C8', 'C8-B8', 'C8-C7', 'C8-D8', 'B7-A7', 'B7-B6', 'B7-C7', 'D7-C7', 'D7-D6', 'D7-E7', 'E7-D7', 'E7-E6', 'E7-F7', 'G7-F7', 'G7-G6', 'G7-H7', 'C6-B6', 'C6-C5', 'C6-D6', 'H6-G6', 'H6-H5', 'H6-G5']
        
        board, player = fen_to_board(fen)
        moves = translate_moves(legal_moves(board, player))
        self.assertEqual(len(moves), 23, "Incorrect number of moves for group J midgame")
        self.assertEqual(sorted(moves), sorted(expected_moves), "Incorrect moves for group J midgame")

    def test_group_F_advanced_game(self):
        fen = 'b0b04/r0r0b02b0b0b0/2r02r0r0r0/8/8/b0b0b02b02/r0r0r02r0b0b0/4r0r0 b'
        expected_moves = ['B1-A2', 'B1-C1', 'C1-B1', 'C1-B2', 'C1-D1', 'C1-C2', 'C2-D2', 'F2-E2', 'F2-G2', 'F2-G3', 'G2-F2', 'G2-F3', 'G2-H2', 'G2-H3', 'H2-G2', 'H2-G3', 'A6-B6', 'A6-B7', 'B6-A6', 'B6-A7', 'B6-C6', 'B6-C7', 'C6-B6', 'C6-B7', 'C6-D6', 'F6-E6', 'F6-G6', 'G7-F8', 'G7-H7', 'H7-G7', 'H7-G8']
        
        board, player = fen_to_board(fen)
        moves = translate_moves(legal_moves(board, player))
        self.assertEqual(len(moves), 31, "Incorrect number of moves for group F advanced game")
        self.assertEqual(sorted(moves), sorted(expected_moves), "Incorrect moves for group F advanced game")

    def test_group_F_endgame(self):
        fen = '6/3bb4/1br6/r01b0b02bb1/1rr2r0r01b0/6rb1/4rr3/6 b'
        expected_moves = ['D2-C4', 'D2-B3', 'D2-E4', 'D2-F3', 'C4-B4', 'C4-B5', 'C4-D4', 'C4-C5', 'D4-C4', 'D4-E4', 'D4-E5', 'D4-D5', 'G4-F6', 'G4-E5', 'G4-H6', 'H5-G5', 'H5-H6', 'G6-F8', 'G6-E7']
        
        board, player = fen_to_board(fen)
        moves = translate_moves(legal_moves(board, player))
        self.assertEqual(len(moves), 19, "Incorrect number of moves for group F endgame")
        self.assertEqual(sorted(moves), sorted(expected_moves), "Incorrect moves for group F endgame")

    def test_group_R_midgame(self):
        fen = '1b0b01b0b0/3bb4/8/1r03b02/3b0rrr0b01/6r01/1r0r0r04/2r01r01 r'
        expected_moves = ['D8-C8', 'D8-E8', 'D8-D7', 'F8-E8', 'F8-G8', 'F8-F7', 'B7-A7', 'B7-C7', 'B7-B6', 'C7-B7', 'C7-D7', 'C7-C6', 'D7-C7', 'D7-E7', 'D7-D6', 'G6-F6', 'G6-H6', 'E5-C4', 'E5-G4', 'E5-D3', 'E5-F3', 'B4-A4', 'B4-C4', 'B4-B3']
        
        board, player = fen_to_board(fen)
        moves = translate_moves(legal_moves(board, player))
        self.assertEqual(len(moves), 24, "Incorrect number of moves for group R midgame")
        self.assertEqual(sorted(moves), sorted(expected_moves), "Incorrect moves for group R midgame")

    def test_group_R_endgame(self):
        fen = '6/7rr/4bb1r01/8/8/b02bb3b0/8/6 r'
        expected_moves = ['G3-F3', 'G3-H3', 'G3-G2', 'H2-F1']
        
        board, player = fen_to_board(fen)
        moves = translate_moves(legal_moves(board, player))
        self.assertEqual(len(moves), 4, "Incorrect number of moves for group R endgame")
        self.assertEqual(sorted(moves), sorted(expected_moves), "Incorrect moves for group R endgame")

    def test_group_AG_midgame(self):
        fen = 'b03b01/3bb2bb1/2bb1br3/1b06/5r02/2rr5/1r02rr3/r0r02rr1 b'
        expected_moves = ['B1-C1', 'B1-B2', 'F1-E1', 'F1-G1', 'F1-F2', 'D2-B3', 'D2-F3', 'D2-C4', 'D2-E4', 'G2-E3', 'G2-F4', 'G2-H4', 'C3-A4', 'C3-E4', 'C3-B5', 'C3-D5', 'B4-A4', 'B4-C4', 'B4-B5']
        
        board, player = fen_to_board(fen)
        moves = translate_moves(legal_moves(board, player))
        self.assertEqual(len(moves), 19, "Incorrect number of moves for group AG midgame")
        self.assertEqual(sorted(moves), sorted(expected_moves), "Incorrect moves for group AG midgame")

    def test_group_S_early_game(self):
        fen = 'b0b0b0b0b0b0/2bbb02bb1/4b03/8/3r04/8/1r0r01r0r0r01/r0r0r0r0r0r0 r'
        expected_moves = ['B8-C8', 'B8-B7', 'C8-B8', 'C8-C7', 'C8-D8', 'D8-C8', 'D8-D7', 'D8-E8', 'E8-D8', 'E8-E7', 'E8-F8', 'F8-E8', 'F8-F7', 'F8-G8', 'G8-F8', 'G8-G7', 'B7-A7', 'B7-B6', 'B7-C7', 'C7-B7', 'C7-C6', 'C7-D7', 'E7-D7', 'E7-E6', 'E7-F7', 'F7-E7', 'F7-F6', 'F7-G7', 'G7-F7', 'G7-G6', 'G7-H7', 'D5-C5', 'D5-D4', 'D5-E5']
        
        board, player = fen_to_board(fen)
        moves = translate_moves(legal_moves(board, player))
        self.assertEqual(len(moves), 34, "Incorrect number of moves for group S early game")
        self.assertEqual(sorted(moves), sorted(expected_moves), "Incorrect moves for group S early game")

    def test_group_S_end_game(self):
        fen = '2b03/1b0b05/6b01/3bb2r01/3r02r01/2b05/2r03r01/3r02 b'
        expected_moves = ['D1-C1', 'D1-D2', 'D1-E1', 'B2-A2', 'B2-B3', 'B2-C2', 'C2-B2', 'C2-C3', 'C2-D2', 'G3-F3', 'G3-H3', 'D4-B5', 'D4-C6', 'D4-E6', 'D4-F5', 'C6-B6', 'C6-D6']
        
        board, player = fen_to_board(fen)
        moves = translate_moves(legal_moves(board, player))
        self.assertEqual(len(moves), 17, "Incorrect number of moves for group S end game")
        self.assertEqual(sorted(moves), sorted(expected_moves), "Incorrect moves for group S end game")

    def test_group_AlphaJump_position_1(self):
        fen = '5b0/1bbb0b0brb0b01/8/3b0r03/8/4b03/1rr1b0r0rrrr1/1r04 r'
        expected_moves = ['C8-B8', 'C8-C7', 'C8-D7', 'C8-D8', 'B7-A5', 'B7-C5', 'B7-D6', 'E4-E3', 'E4-F4', 'F7-H6', 'F7-G5', 'F7-E5', 'F7-D6', 'G7-H5', 'G7-F5', 'G7-E6', 'E2-G1', 'E2-C1']
        
        board, player = fen_to_board(fen)
        moves = translate_moves(legal_moves(board, player))
        self.assertEqual(len(moves), 18, "Incorrect number of moves for Group AlphaJump position 1")
        self.assertEqual(sorted(moves), sorted(expected_moves), "Incorrect moves for Group AlphaJump position 1")

    def test_group_AlphaJump_position_2(self):
        fen = '6/1bbbbbbbbbbbb1/8/8/8/1rrrrrrrrrrrr1/6 b'
        expected_moves = ['B2-A4', 'B2-C4', 'B2-D3', 'C2-A3', 'C2-B4', 'C2-D4', 'C2-E3', 'D2-B3', 'D2-C4', 'D2-E4', 'D2-F3', 'E2-C3', 'E2-D4', 'E2-F4', 'E2-G3', 'F2-D3', 'F2-E4', 'F2-G4', 'F2-H3', 'G2-E3', 'G2-F4', 'G2-H4']
        
        board, player = fen_to_board(fen)
        moves = translate_moves(legal_moves(board, player))
        self.assertEqual(len(moves), 22, "Incorrect number of moves for Group AlphaJump position 2")
        self.assertEqual(sorted(moves), sorted(expected_moves), "Incorrect moves for Group AlphaJump position 2")


    def test_group_Sturdy_Jumpers_endgame(self):
        fen = '1b03b0/r02bb1b02/3b04/1r06/4r0r0b01/2b03r01/2r05/2r01r01 r'
        expected_moves = ['A2-B2', 'B4-A4', 'B4-C4', 'B4-B3', 'E5-F5', 'E5-D5', 'E5-E4', 'F5-E5', 'F5-F4', 'G6-F6', 'G6-H6', 'C7-B7', 'C7-D7', 'D8-D7', 'D8-E8', 'D8-C8', 'F8-E8', 'F8-G8', 'F8-F7']
        
        board, player = fen_to_board(fen)
        moves = translate_moves(legal_moves(board, player))
        self.assertEqual(len(moves), 19, "Incorrect number of moves for Group Sturdy Jumpers endgame")
        self.assertEqual(sorted(moves), sorted(expected_moves), "Incorrect moves for Group Sturdy Jumpers endgame")
        




# Benchmark time of Zuggenerator execution
def benchmark_zuggenerator(fen, reps, legal_moves):
    # Measurement of Execution Time and Calculation of Average
    board, player = fen_to_board(fen)
    time_total = timeit.repeat("legal_moves(board, player)", globals=locals(), number=1, repeat=reps)
    time_avg = sum(time_total) / reps
    return time_avg


if __name__ == '__main__':
    
    benchmark = True
    unit_test = True

    if benchmark:
        # FENs to test
        fen_early = "b0b0b0b0b0b0/1b0b0b0b0b0b01/8/8/8/8/1r0r0r0r0r0r01/r0r0r0r0r0r0 b"
        fen_mid = "b0b0b01bb1/2b0b0bbb02/5r02/3b04/4r0b02/8/2rrr01r02/r0r0r0r01r0 r"
        fen_late = "3b02/5r02/3r04/8/8/2b02b02/2r05/6 b"
        
        # Number of Executions
        reps = 1000
        #legal_moves(fen_early)
        print("Average time early game (in ms):", benchmark_zuggenerator(fen_early,reps,legal_moves)*1000)
        print("Average time mid game (in ms):", benchmark_zuggenerator(fen_mid,reps,legal_moves)*1000)
        print("Average time late game (in ms):", benchmark_zuggenerator(fen_late,reps,legal_moves)*1000)

    if unit_test:
        unittest.main()
