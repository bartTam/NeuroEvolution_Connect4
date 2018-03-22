# -*- coding: utf-8 -*-
'''
NOTE:
    Player 1 is Yellow and is a 1 on the gameBoard
    Player 2 is Red and is a 2 on the gameBoard
    
    Player 1 (Yellow) always goes first
'''

import pygame
import re

# prepare pygame
pygame.init()
pygame.font.init()

# window size
gameDisplay = pygame.display.set_mode((1000, 600))

# name on top left of window
pygame.display.set_caption('Connect 4')

# start the game clock
clock = pygame.time.Clock()

# total_w the pixel width of the screen
# h the pixel height of the screen
total_w, h = pygame.display.get_surface().get_size()

# a game board 7 wide by 6 tall filled with zeros
gameBoard = [[0 for a in range(7)] for b in range(6)]

# the list of player moves to be used for undoing moves
move_tracker = [0 for c in range(42)]
move_pos = 0         # the index for the list of player moves, useful for undo

# sizes
w = 7 * total_w / 10 # width of the game board in integer units
radius = w / 14      # radius of a player token
font_size = 35       # size of the font
x_index = 0          # the x index of where the next token will be placed


done = False         # user presses X on top right of window
playerOneTurn = True # player one (yellow) and player two (red)

# background is true when there is a new game to reset the board background
background = False
undo = False         # the program will enter the undo section of the game loop

# RGB colors
WHITE = (255, 255, 255)
HOVER = (200, 200, 200)
DARK = (10, 10, 10)
LIGHT = (30, 30, 30)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
color = YELLOW

# prepare the screen for drawing images
pygame.display.update()

'''
Graphics Functions
'''

# print given text at an x,y position on the screen
def text_to_screen(screen, text, x, y, shade):
    try:
        text = str(text)
        font = pygame.font.SysFont('arial', 40)
        text = font.render(text, True, shade)
        screen.blit(text, (x, y))

    except:
        print('this error shouldn\'t happen')

# the gray and dark gray columns to see where tokens can be placed
def draw_columns():
    column = 0
            
    # redraw background columns
    while column < 7:
        if column % 2 == 0:
            pygame.draw.rect(gameDisplay, DARK,
                             [w / 7 * column,
                              0,
                              radius * 2 + w / 7 * column,
                              h])
        else:
            pygame.draw.rect(gameDisplay, LIGHT,
                             [w / 7 * column, 0,
                              radius * 2 + w / 7 * column,
                              h])
        text_to_screen(gameDisplay,
                       column + 1,
                       radius * .8 + w / 7 * column,
                       35,
                       WHITE)
        column = column + 1

# display the new game button with the ability to change color based on state
def draw_new_game_button(state):
    
    ng_button_coords = [w + radius / 2, h - 100, 5 * radius, 70]
    
    # default state unfocused
    if state == 'default':
        pygame.draw.rect(gameDisplay, WHITE, ng_button_coords)
    
    elif state == 'hover':
        pygame.draw.rect(gameDisplay, HOVER, ng_button_coords)
        
    text_to_screen(gameDisplay,
                   'New Game',
                   ng_button_coords[0] + radius / 2,
                   ng_button_coords[1] + 12,
                   LIGHT)

# display the undo button with the ability to change color based on state
def draw_undo_button(state):
    u_button_coords = [w + radius / 2, h - 190, 5 * radius, 70]
    
    # default state unfocused
    if state == 'default':
        pygame.draw.rect(gameDisplay, WHITE, u_button_coords)
    
    elif state == 'hover':
        pygame.draw.rect(gameDisplay, HOVER, u_button_coords)
        
    text_to_screen(gameDisplay,
                   'Undo',
                   u_button_coords[0] + 47 + radius / 2,
                   u_button_coords[1] + 12,
                   LIGHT)

# display which player's turn it is on the right with text and a color
def draw_player_turn():
    
    if playerOneTurn:
        turn = 'Yellow Turn'
        turn_display_w = w + radius
    else:
        turn = 'Red Turn'
        turn_display_w = w + 67
    
    # display player turn bar on the right
    pygame.draw.rect(gameDisplay, color, [w + radius / 2, 110, 5 * radius, 70])
    text_to_screen(gameDisplay, turn, turn_display_w,  122, LIGHT)

# erase the token from the screen and undo the move on the gameBoard
def draw_undo():
    global move_pos
    global playerOneTurn
    y_index = 0
    
    if move_pos == 0:
        return None
    
    # player move tracker index goes back by 1
    move_pos = move_pos - 1
    
    # get the column color
    if move_tracker[move_pos] % 2 == 1:
        replace_color = LIGHT
    else:
        replace_color = DARK
    
    # find the previously picked spot
    while y_index < len(gameBoard) - 1 and gameBoard[y_index + 1][move_tracker[move_pos]] == 0:
        y_index = y_index + 1
    
    # correct for a possible off by 1 issue
    if gameBoard[0][move_tracker[move_pos]] == 0 and y_index < len(gameBoard) - 1:
        y_index = y_index + 1
    
    # reset gameboard position with the found y_index and remove token from screen
    gameBoard[y_index][move_tracker[move_pos]] = 0
    pygame.draw.circle(gameDisplay, replace_color,
                       [int(move_tracker[move_pos] * 100 + radius),
                        int(y_index * h / 6 + radius)],
                        int(radius))
    
    # redraw number if a circle was overlapping a number
    if y_index == 0:
        text_to_screen(gameDisplay,
                       move_tracker[move_pos] + 1,
                       radius * .8 + w / 7 * move_tracker[move_pos],
                       35,
                       WHITE)
    
    # reset the player's previous move in the move tracker and switch turn back to other player
    move_tracker[move_pos] = 0
    switch()

# draw the panel on the right with the title
def draw_ui():
    
    # ui panel background
    pygame.draw.rect(gameDisplay, LIGHT, [w, 0, total_w, h])
    text_to_screen(gameDisplay, 'Connect 4', w + 1.2 * radius, 35, WHITE)
    
    #ui panel button drawing
    draw_new_game_button('default')
    draw_undo_button('default')

# call all relevant functions to show a blank board on the surface
def draw_surface():
    draw_columns()
    draw_ui()
    pygame.display.update()

# draw the token on the surface if possible and update the gameBoard
def draw_token(x_index):
    y_index = 0
    
    #print(x_index)
    
    # the player chose an invalid location
    if gameBoard[0][x_index] != 0:
        return False
    
    # find the next open spot on the y axis to place the token
    while y_index < len(gameBoard) - 1 and gameBoard[y_index + 1][x_index] == 0:
        y_index = y_index + 1
    
    # draw token in player's desired column
    pygame.draw.circle(gameDisplay, color,
                       [int(x_index * 100 + radius),
                        int(y_index * h / 6 + radius)],
                        int(radius))
    
    # put a user piece on the gameBoard
    if playerOneTurn:
        piece = 1
    else:
        piece = 2
    
    # set the piece in the gameBoard
    gameBoard[y_index][x_index] = piece
    return True

'''
Game Functions
'''

# switches the turn from player one turn to player two turn and vice versa
def switch():
    global color
    global playerOneTurn
    
    if playerOneTurn:
        color = RED
        #print('Player Red turn')
    else:
        color = YELLOW
        #print('Player Yellow turn')
    playerOneTurn = not playerOneTurn

'''
determines if the game has ended and which player has won

returns
    0 if no player has won
    1 if player yellow (player 1) has won
    2 if player red (player 2) has won

'''
def hasWon():
    
    # cycle between player 1 and player 2
    for p in range(1,3):
        
        # horizontal cases ----
        for y in range(4):
            for x in range(6):
                for i in range(4):
                    if gameBoard[x][y+i] == p:
                        if i == 3:
                            return p
                    else:
                        break
       
        # vertical cases ||||
        for x in range(3):
            for y in range(7):    
                for i in range(4):
                    if gameBoard[x+i][y] == p:
                        if i == 3:
                            return p
                    else:
                        break
                        
        # ascending diagonal ////
        for x in range(3,6):
            for y in range(4):    
                for i in range(4):
                    if gameBoard[x-i][y+i] == p:
                        if i == 3:
                            return p
                    else:
                        break
                        
        # descending diagonal \\\\
        for x in range(3,6):
            for y in range(3,7): 
                for i in range(4):
                    if gameBoard[x-i][y-i] == p:
                        if i == 3:
                            return p
                    else:
                        break
    return 0

'''
Call Functions
'''

# print the default screen when the program is first run
draw_surface()

# game loop
while not done:
    
    # gets any event that happens in the window every frame
    for event in pygame.event.get():
        
        x, y = pygame.mouse.get_pos()
        
        # new game button is clicked with mouse
        if w + 5 * radius >= x >= w + radius and h - 30 >= y >= h - 100:
            draw_new_game_button('hover')
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                background = True
        else:
            draw_new_game_button('default')
            
        # undo button is clicked with mouse
        if w + 5 * radius >= x >= w + radius and h - 120 >= y >= h - 190:
            draw_undo_button('hover')
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                undo = True
        else:
            draw_undo_button('default')
            
        # undo button u pressed
        if pygame.key.get_pressed()[pygame.K_u] != 0:
            undo = True
        
        # user presses top right X
        if event.type == pygame.QUIT:
            done = True
            
        # new game button n pressed
        if pygame.key.get_pressed()[pygame.K_n] != 0:
            background = True
        
        # keyboard press 1-7 or numpad 1-7 to drop a token
        if event.type == pygame.KEYDOWN:
            
            if re.search(r"^\[?[1-7]\]?", pygame.key.name(event.key)):
                
                try:
                    x_index = int(pygame.key.name(event.key)) - 1
                except:
                    x_index = int(pygame.key.name(event.key)[1]) - 1
            
                # switch turns and colors
                if draw_token(x_index):
                    switch()
                    move_tracker[move_pos] = x_index
                    move_pos = move_pos + 1
                
                # check for game end
                if hasWon() == 1:
                    print('Player Yellow wins')
                    background = True
                elif hasWon() == 2:
                    print('Player Red wins')
                    background = True
        
        # mouse click to drop a token
        if event.type == pygame.MOUSEBUTTONDOWN:
            
            # player must have clicked in the game area of the screen
            if 0 <= x <= w:
                
                # find which of the 7 slots the player has clicked on
                if x <= w / 7:
                    x_index = 0
                    
                elif 1 * w / 7 < x <= 2 * w / 7:
                    x_index = 1
                    
                elif 2 * w / 7 < x <= 3 * w / 7:
                    x_index = 2
                    
                elif 3 * w / 7 < x <= 4 * w / 7:
                    x_index = 3
                    
                elif 4 * w / 7 < x <= 5 * w / 7:
                    x_index = 4
                    
                elif 5 * w / 7 < x <= 6 * w / 7:
                    x_index = 5
                    
                elif 6 * w / 7 < x <= w :
                    x_index = 6
                
                # switch turns and colors
                if draw_token(x_index):
                    switch()
                    move_tracker[move_pos] = x_index
                    move_pos = move_pos + 1
                    
                # check for game end
                if hasWon() == 1:
                    print('Player Yellow wins')
                    background = True
                elif hasWon() == 2:
                    print('Player Red wins')
                    background = True
                
        # undo button was pressed
        if undo:
            draw_undo()
            undo = False
            
        # reset game and redraw background
        if background:
            gameBoard = [[0 for a in range(7)] for b in range(6)]
            moveTracker = [0 for c in range(42)]
            move_pos = 0
            draw_surface()
            color = YELLOW
            playerOneTurn = True
            background = False
            draw_player_turn()
        
        # display the player's turn on the right
        draw_player_turn()
                        
    # tell the window to update with new info
    pygame.display.update()
    clock.tick(60)

# stop the loop    
pygame.quit()
quit()

