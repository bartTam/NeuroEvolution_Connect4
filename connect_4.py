import pygame
import pygame.display as display
import pygame.time as time
import numpy as np
import threading

class Connect_4(object):

    def __init__(self, inputCallback=[None, None], headless=False, printing=True, **args):
        '''
            Constructor for Connect4
            inputCallback: The callback to run which will play a turn. If None, 
                then wait for player input
            headless: Whether or not to use pygame as a gui
        '''
        if headless:
            self.interface = _Interface(inputCallback, printing=printing, **args)
        else:
            self.interface = _Pygame_GUI(inputCallback, printing=printing, **args)

        self.gamestate = _Connect_4_Gamestate(self.interface, printing=printing, **args)
    
    def run_game(self):
        return self.gamestate.run_game()
        

class _Interface():
    def __init__(self, inputCallback, printing=True):
        self.inputCallback = inputCallback
        self.printing = printing
        self._init_callback()

    def _init_callback(self):
        # Replace any "None" callbacks with human input
        for callback in self.inputCallback:
            if callback is None:
                callback = lambda x: int(input()) - 1

    def __iter__(self):
        '''
        Determine the player and callback for each turn
        '''
        player = 0

        while True:
            yield player, self.inputCallback[player]
            player = (player + 1) % 2

    def print(self, *args, **kargs):
        '''
        Disable printing if printing is turned off
        '''
        if self.printing:
            print(*args, **kargs)

    def update_board(self, board):
        '''
        Update the visual of the board
        '''
        print_output = {-1:'_', 0:'X', 1:'O'}

        # Print each row
        self.print()
        for row in board:
            for value in row:
                self.print(print_output[value], end='')
            self.print()
        for i in range(board.shape[1]):
            self.print(i + 1, end='')
        self.print()

class _Pygame_GUI(_Interface):
    default_window_size = (1000, 600)
    def __init__(self, inputCallback, window_size=default_window_size, printing=True):
        super().__init__(inputCallback)

        self.printing = printing

        self.clock = time.Clock()

        # Make sure display is initialized
        if not display.get_init():
            display.init()
        self.window = display.set_mode(window_size)
        display.set_caption('Connect 4')
        self.window_size = display.get_surface().get_size()

    def _init_callback(self):
        '''
        Replace any "None" callbacks with human input
        '''
        pass

    def update_board(self, board):
        '''
        Update the visual of the board
        '''
        pass


class _Connect_4_Gamestate(object):
    default_game_board_size = (6,7)

    def __init__(self, interface, game_board_size=default_game_board_size, printing=True):
        self.num_rows, self.num_cols = game_board_size # numpy is row major
        # Initialize board to -1
        self.game_board = np.zeros(game_board_size) - 1
        self.game_moves = []
        self.current_player = 0
        # The winner -1 until one player wins, 0 for first player, 1 for second player
        self.winner = -1

        self.interface = interface
        self.interface.update_board(self.game_board)
        self.printing = printing
        self.turn_num = 0

    def run_game(self):
        '''
        Play the entire game
        '''
        for player, get_turn in self.interface:
            # Ensure there is never a stalemate
            if len(self.game_moves) == 41:
                self.print("Cat's game")
                return -1

            self.current_player = player
            # Ensure there is not too many in a column
            turn = get_turn(self.game_board)
            if not self.play_turn(turn):
                self.print("Invalid play")
                return -1

            # Successful so update the board
            self.interface.update_board(self.game_board)
            self.game_moves.append(turn)

            if self.winner != -1:
                break
        self.print(f'Player {self.winner + 1} Won!')
        return self.winner

    def print(self, *args, **kargs):
        if self.printing:
            print(*args, **kargs)

    def play_turn(self, column_num):
        # Pass turn
        if column_num is None:
            return True
        
        # Validate
        if (not isinstance(column_num, int)) or \
                column_num >= self.num_cols or \
                column_num < 0:
            return False

        # Play the piece
        for row in reversed(range(self.num_rows)):
            if self.game_board[row, column_num] == -1:
                self.game_board[row, column_num] = self.current_player
                if self._check_win(row, column_num):
                    self.winner = self.current_player
                return True
        return False
            
    def _check_win(self, x, y):
        # Check around the placed piece
        for curr_y in range(-1, 1):
            for curr_x in range(-1, 1):
                # Don't check current place
                if curr_y == 0 and curr_x == 0:
                    pass
                else:
                    i = 1
                    check_out = check_in = True
                    # Check up to 4 pieces away
                    for offset in range(1, 4):
                        if check_in:
                            to_check = x + offset * curr_x, y + offset * curr_y
                            if to_check[0] < 0 or  to_check[1] < 0:
                                check_in = False
                            elif self.game_board[to_check] == self.current_player:
                                i += 1
                            else:
                                check_in = False
                        if check_out:
                            to_check = x - offset * curr_x, y - offset * curr_y
                            if to_check[0] >= self.num_rows or to_check[1] >= self.num_cols:
                                check_out = False
                            elif self.game_board[to_check] == self.current_player:
                                i += 1
                            else:
                                check_out = False
                    if i >= 4:
                        return True
        return False
                                    
if __name__ == '__main__':
    def create_callback(start):
        def func(arg):
            func.val = (func.val + 1) % 7
            return func.val 
        func.val = start  - 1
        return func
    import random
    def rand_callback(arg):
        return random.randint(0, 6)
    Connect_4(inputCallback=[None, create_callback(1)], headless=True, printing=True).run_game()