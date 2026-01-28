import pygame
import random
from .constants import RED, WHITE, BLUE, SQUARE_SIZE, SCOREBOARD_HEIGHT
from checkers.board import Board

class Game:
    def __init__(self, win):
        self._init()
        self.win = win
        self.board_offset = SCOREBOARD_HEIGHT  # Offset for scoreboard
    
    def update(self):
        self.board.draw(self.win, self.board_offset)
        self.draw_valid_moves(self.valid_moves)

    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = RED
        self.valid_moves = {}

    def winner(self):
        return self.board.winner()

    def reset(self):
        self._init()

    def select(self, row, col):
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)
        
        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True
            
        return False

    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)
            self.change_turn()
        else:
            return False

        return True

    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE//2 + self.board_offset), 15)

    def ai_move(self, color):
        
        all_moves = []
        capture_moves = []

        # Iterate over all pieces on the board
        for row in self.board.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    moves = self.board.get_valid_moves(piece)
                    for (r, c), skipped in moves.items():
                        move_info = (piece, (r, c), skipped)
                        all_moves.append(move_info)
                        if skipped:
                            capture_moves.append(move_info)

        if not all_moves:
            return  # No moves available; game logic will eventually detect winner

        # Prefer capture moves if any exist
        if capture_moves:
            piece, (row, col), skipped = random.choice(capture_moves)
        else:
            piece, (row, col), skipped = random.choice(all_moves)

        # Perform the chosen move on the board
        self.board.move(piece, row, col)
        if skipped:
            self.board.remove(skipped)

        # Switch turn back to the human
        self.change_turn()

    def change_turn(self):
        self.valid_moves = {}
        if self.turn == RED:
            self.turn = WHITE
        else:
            self.turn = RED