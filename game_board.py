import pygame
import pygame.display as display
import pygame.time as time
import re

class Controller(object):
    def __init__(self, game_board, w=700):
        '''
            Constructor for Controller
            game_board: 2D list of -1,0,1 representing the Connect4 board
            w: The width of the window
        '''
        self.w = w
        self.h = w - w/7
        self.radius = w/14

        self.game_display = pygame.display.set_mode((self.w, self.h))
        self.game_board = game_board
        self.colors = {'red':(255,0,0),\
                       'yellow':(255,255,0),\
                       'black':(0,0,0),\
                       'light gray':(200,200,200),\
                       'white':(255,255,255)}

    def setup(self):
        pygame.font.init()
        pygame.display.set_caption('Connect 4')
        pygame.display.update()

    def text_to_screen(self, screen, text, x, y, shade):
        try:
            text = str(text)
            font = pygame.font.SysFont('arial', 40)
            text = font.render(text, True, shade)
            screen.blit(text, (x, y))
        except:
            pass

    # draw columns and the corresponding numbers
    def draw_columns(self):
        for column in range(0,7):
            if column % 2 == 0:
                pygame.draw.rect(self.game_display, self.colors['light gray'], [self.w / 7 * column, 0,
                                self.radius * 2 + self.w / 7 * column, self.h])
            else:
                pygame.draw.rect(self.game_display, self.colors['white'], [self.w / 7 * column, 0,
                                self.radius * 2 + self.w / 7 * column, self.h])
            self.text_to_screen(self.game_display, column + 1, self.radius * .8 + self.w / 7 * column,
                        35, self.colors['black']) 
        pygame.display.update()
    
    def draw_tokens(self):
        for y in range(self.game_board.shape(0)):
            for x in range(self.game_board.shape(1)):
                # not an empty slot
                if not self.game_board[x][y] == -1:
                    token_color = self.colors['yellow'] if self.game_board[x][y] == 0 else self.colors['red']
                    pygame.draw.circle(self.game_display, token_color,\
                        [int(x*(self.radius*2) + self.radius),\
                        int(y * self.h/6 + self.radius)], self.radius)
    
    def get_inputs(self, event):
        '''
        event: A pygame.event that occurred in the game loop
        return: The index selected by the user
        '''
        # keyboard press 1-7 or numpad 1-7
        if event.type == pygame.KEYDOWN:
            if re.search(r"^\[?[1-7]\]?", pygame.key.name(event.key)):
                try:
                    return int(pygame.key.name(event.key)) - 1
                except:
                    return int(pygame.key.name(event.key)[1]) - 1
        # mouse click
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x = pygame.mouse.get_pos().shape(0)
            # which column the cursor clicked in
            if x <= self.w / 7: return 0
            elif self.w / 7 < x <= 2*self.w / 7: return 1
            elif 2 * self.w / 7 < x <= 3 * self.w / 7: return 2
            elif 3 * self.w / 7 < x <= 4 * self.w / 7: return 3
            elif 4 * self.w / 7 < x <= 5 * self.w / 7: return 4
            elif 5 * self.w / 7 < x <= 6 * self.w / 7: return 5
            elif 6 * self.w / 7 < x <= self.w : return 6
