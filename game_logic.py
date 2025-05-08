from typing import List

class TicTacToeGame:
    def __init__(self):
        self.board: List[List[str]] = []
        self.current_player: str = 'X'
        self.reset_game()

    def reset_game(self):
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
    
    def reset_player(self, player='X'):
        if player in ['X', 'O']:
            self.current_player = player
        else:
            raise ValueError("Player must be 'X' or 'O'")

    def make_move(self, row, col):
        if not (0 <= row < 3 and 0 <= col < 3):
            return "Invalid: Out of bounds"
        if self.board[row][col] != '':
            return "Invalid: Cell already occupied"

        self.board[row][col] = self.current_player

        if self.check_winner():
            return f"{self.current_player} wins"
        elif self.check_draw():
            return "Draw"
        else:
            self.toggle_player()
            return "Continue"

    def toggle_player(self):
        self.current_player = 'O' if self.current_player == 'X' else 'X'

    def check_winner(self):
        b = self.board

        for i in range(3):
            if all(b[i][j] == self.current_player for j in range(3)):  
                return True
            if all(b[j][i] == self.current_player for j in range(3)):  
                return True
 
        if all(b[i][i] == self.current_player for i in range(3)):  
            return True
        if all(b[i][2 - i] == self.current_player for i in range(3)):  
            return True
        return False

    def check_draw(self):
        return all(cell != '' for row in self.board for cell in row)

    def serialize_board(self) -> str:
        return ''.join(cell if cell else ' ' for row in self.board for cell in row)

    def deserialize_board(self, state_str: str):
        if len(state_str) != 9:
            raise ValueError("State string must be exactly 9 characters long")
        self.board = [[state_str[3 * i + j] if state_str[3 * i + j] != ' ' else '' 
                   for j in range(3)] for i in range(3)]

    def get_current_player(self):
        return self.current_player
    
    def get_game_status(self):
        if self.check_winner():
            return f"{self.current_player} wins"
        elif self.check_draw():
            return "Draw"
        else:
            return "Ongoing"

    def print_board(self):
        for row in self.board:
            print(' | '.join(cell if cell else ' ' for cell in row))
            print('-' * 5)