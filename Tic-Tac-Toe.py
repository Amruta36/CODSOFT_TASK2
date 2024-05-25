import math, random

class TicTacToe:
    def __init__(self):
        self.board = [' ']*9
        self.current_winner = None

    def print_board(self):
        for row in [self.board[i*3:(i+1)*3] for i in range(3)]:
            print('| ' + ' | '.join(row) + ' |')

    @staticmethod
    def print_board_nums():
        for row in [[str(i) for i in range(j*3, (j+1)*3)] for j in range(3)]:
            print('| ' + ' | '.join(row) + ' |')

    def available_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def empty_squares(self):
        return ' ' in self.board

    def num_empty_squares(self):
        return self.board.count(' ')

    def make_move(self, square, letter):
        if self.board[square] == ' ':
            self.board[square] = letter
            if self.winner(square, letter):
                self.current_winner = letter
            return True
        return False

    def winner(self, square, letter):
        row_ind = square // 3
        row = self.board[row_ind*3:(row_ind+1)*3]
        col_ind = square % 3
        column = [self.board[col_ind+i*3] for i in range(3)]
        if all([spot == letter for spot in row]) or all([spot == letter for spot in column]):
            return True
        if square % 2 == 0:
            diagonal1 = [self.board[i] for i in [0, 4, 8]]
            diagonal2 = [self.board[i] for i in [2, 4, 6]]
            if all([spot == letter for spot in diagonal1]) or all([spot == letter for spot in diagonal2]):
                return True
        return False

def play():
    game = TicTacToe()
    x_player = HumanPlayer('X')
    o_player = SmartComputerPlayer('O')
    game.print_board_nums()
    letter = 'X'
    while game.empty_squares():
        if letter == 'O': square = o_player.get_move(game)
        else: square = x_player.get_move(game)
        if game.make_move(square, letter):
            print(letter + f' makes a move to square {square}')
            game.print_board()
            if game.current_winner:
                print(letter + ' wins!')
                return letter
            letter = 'O' if letter == 'X' else 'X'
    print('It\'s a tie!')

class HumanPlayer:
    def __init__(self, letter):
        self.letter = letter
    def get_move(self, game):
        while True:
            try: return int(input(self.letter + '\'s turn. Input move (0-8): '))
            except ValueError: print('Invalid square. Try again.')

class SmartComputerPlayer:
    def __init__(self, letter):
        self.letter = letter
    def get_move(self, game):
        if len(game.available_moves()) == 9: return random.choice(game.available_moves())
        else: return self.minimax(game, self.letter)['position']
    def minimax(self, state, player):
        max_player, other_player = self.letter, 'O' if player == 'X' else 'X'
        if state.current_winner == other_player: return {'position': None, 'score': 1 * (state.num_empty_squares() + 1) if other_player == max_player else -1 * (state.num_empty_squares() + 1)}
        elif not state.empty_squares(): return {'position': None, 'score': 0}
        if player == max_player: best = {'position': None, 'score': -math.inf}
        else: best = {'position': None, 'score': math.inf}
        for possible_move in state.available_moves():
            state.make_move(possible_move, player)
            sim_score = self.minimax(state, other_player)
            state.board[possible_move] = ' '
            state.current_winner = None
            sim_score['position'] = possible_move
            if player == max_player:
                if sim_score['score'] > best['score']: best = sim_score
            else:
                if sim_score['score'] < best['score']: best = sim_score
        return best

play()
