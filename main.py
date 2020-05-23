from time import sleep

import pygame
import random
import enum
import copy
import ujson  # to speed up the deep copying process

pygame.init()

display_width = 800
display_height = 800
black = (0, 0, 0)
white = (255, 255, 255)
GREEN = (0, 220, 0)
BRIGHT_GREEN = (0, 255, 0)
RED = (220, 0, 0)
BRIGHT_RED = (255, 0, 0)
BLUE = (0, 0, 220)
BRIGHT_BLUE = (0, 0, 255)
length = 3
topleftx, toplefty = 250, 250
BUTTON_W = 100
BUTTON_H = 50

box_dimen = 100
marking_arr = [[0, 0, 0],
               [0, 0, 0],
               [0, 0, 0]]


class Player(enum.Enum):
    player = 1
    computer = 2
    blank = 0


gameDisplay = pygame.display.set_mode((display_width, display_height))
# function returns the Surface object
clock = pygame.time.Clock()


def boxcoordinate(boxx, boxy):
    x = topleftx + boxx * box_dimen
    y = toplefty + boxy * box_dimen

    return x, y


def draw_grid():
    for boxy in range(length):
        for boxx in range(length):
            x, y = boxcoordinate(boxx, boxy)
            pygame.draw.rect(gameDisplay, black, (x, y, box_dimen, box_dimen), 1)
            if marking_arr[boxy][boxx] == 1:
                # x = x + box_dimen/2
                # y = y + box_dimen/2
                pygame.draw.ellipse(gameDisplay, black, [x, y, box_dimen, box_dimen], 1)
            elif marking_arr[boxy][boxx] == 2:
                pygame.draw.line(gameDisplay, black, (x, y + box_dimen), (x + box_dimen, y))
                pygame.draw.line(gameDisplay, black, (x, y), (x + box_dimen, y + box_dimen))


def getBoxAtCursor(x, y):
    new_x = x - topleftx
    new_y = y - toplefty
    total_length = box_dimen * length
    if topleftx < x < topleftx + total_length and toplefty < y < toplefty + total_length:
        col = int(new_x / box_dimen)
        row = int(new_y / box_dimen)

        return col, row

    else:
        return None, None


def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()


def message_display(text, size, x, y, color):
    """Displays text on surface gameDisplay"""

    fontText = pygame.font.Font('freesansbold.ttf', size)
    textSurf, textRect = text_objects(text, fontText, color)
    textRect.center = (x, y)
    gameDisplay.blit(textSurf, textRect)


def button(msg, x, y, w, h, ic, ac, action=None):
    """Creates interactive button with text on surface gameDisplay

    Parameters
    ic: color when cursor not on button
    ac: color when cursor on button
    action: function that is called when button is clicked
    w: width of button
    h: height of button
    """
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac, (x, y, w, h))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(gameDisplay, ic, (x, y, w, h))

    smallText = pygame.font.Font("freesansbold.ttf", 20)  # add customization later
    textSurf, textRect = text_objects(msg, smallText, black)
    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    gameDisplay.blit(textSurf, textRect)


def gameover(board):
    """Checks if game is over, possible outputs are either players or a draw."""

    draw = 3
    winner = 0
    for row in board:
        track = 1
        for ele in row:
            track = track * ele
            draw = draw * ele
        if track == 1:
            winner = 1
            return winner
        elif track == 8:
            winner = 2
            return winner

    for j in range(length):
        track = 1
        for i in range(length):
            track = track * board[i][j]
        if track == 1:
            winner = 1
            return winner
        elif track == 8:
            winner = 2
            return winner
    track = 1
    for i in range(length):
        track = track * board[i][i]
    if track == 1:
        winner = 1
        return winner
    elif track == 8:
        winner = 2
        return winner
    track = 1
    for i in range(length):
        track = track * board[length - i - 1][i]
    if track == 1:
        winner = 1
        return winner
    elif track == 8:
        winner = 2
        return winner
    if draw != 0:
        return 3
    return winner


def endgame(x, mode):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.fill(white)
        if x != 3:
            message_display("GAME OVER", 50, display_width / 2, display_height / 2, black)
            message_display("Winner is Player %d" % x, 50, display_width / 2, display_height / 2 + 50, black)

        else:
            message_display("DRAW", 50, display_width / 2, display_height / 2, black)
        if mode == 1:
            button("Retry", 0.15 * display_width, 0.85 * display_height, BUTTON_W, BUTTON_H, GREEN, BRIGHT_GREEN,
                   gameloop)
        else:
            button("Retry", 0.15 * display_width, 0.85 * display_height, BUTTON_W, BUTTON_H, GREEN, BRIGHT_GREEN,
                   gameloop_ai)
        button("Main Menu", 0.35 * display_width, 0.85 * display_height, BUTTON_W, BUTTON_H, BLUE, BRIGHT_BLUE,
               game_intro)
        button("QUIT", 0.75 * display_width, 0.85 * display_height, BUTTON_W, BUTTON_H, RED, BRIGHT_RED, quitgame)
        pygame.display.update()
        clock.tick(15)


def game_intro():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.fill(white)
        message_display("TIC TAC TOE", 70, 0.4 * display_width, 0.5 * display_height, black)
        button("VS HUMAN", 0.5 * display_width, 0.55 * display_height, 30, 30, white, white, gameloop)
        button("VS AI", 0.5 * display_width, 0.6 * display_height, 30, 30, white, white, gameloop_ai)

        pygame.display.update()
        clock.tick(15)


def get_oppo(player):
    if player == 1:
        return 2
    else:
        return 1


def minimax(board, player):
    """minimax algorithm to minimize the maximum loss given that enemy plays optimally.

    :param board: list array of state of board
    :param player: player that is currently playing
    :return:
    """
    if gameover(board) != 0 and gameover(board) != 3:
        if player != gameover(board):
            return -1, [-1, -1]
        else:
            return 1, [-1, -1]

    score = -2
    move = [-1, -1]
    for i in range(length):
        for j in range(length):
            if board[i][j] == 0:
                new_board = ujson.loads(ujson.dumps(board))
                new_board[i][j] = player
                new_score = -1 * minimax(new_board, get_oppo(player))[0]
                if new_score > score:
                    score = new_score
                    move = [i, j]

    if move == [-1, -1]:
        return 0, [-1, -1]

    return score, move


def gameloop_ai():
    global marking_arr
    turn = random.randrange(2)  # determines who starts first, 0 is player, 1 is CPU
    marking_arr = [[0] * len(inner) for inner in marking_arr]
    mousex = 0
    mousey = 0
    flag = False

    while True:
        mouseClicked = False
        if turn == 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mousex, mousey = event.pos
                    mouseClicked = True

            boxx, boxy = getBoxAtCursor(mousex, mousey)
            if boxx is not None and boxy is not None:
                if mouseClicked == True and marking_arr[boxy][boxx] == 0:
                    flag = False
                    marking_arr[boxy][boxx] = turn + 1
                    turn = (turn + 1) % 2
                elif mouseClicked == True and marking_arr[boxy][boxx] != 0:
                    flag = True
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            sum = 0
            for row in marking_arr:
                for ele in row:
                    sum = sum + ele
            if sum == 0:
                randomx = random.randrange(2) * 2
                randomy = random.randrange(2) * 2
                marking_arr[randomx][randomy] = Player.computer.value
                turn = (turn + 1) % 2
            if sum != 0:
                board = ujson.loads(ujson.dumps(marking_arr))
                current_score, move = minimax(board, Player.computer.value)
                if move != [-1, -1]:
                    i, j = move
                    marking_arr[i][j] = Player.computer.value
                    turn = (turn + 1) % 2

        gameDisplay.fill(white)
        draw_grid()
        if flag:
            message_display("Please select an empty box.", 30, 0.75 * display_width, 50, black)
        if gameover(marking_arr) == 0:
            turn_string = str(turn + 1)
            message_display("It is now Player %s's turn" % turn_string, 30, 200, 50, black)
        else:
            endgame(gameover(marking_arr), 2)

        pygame.display.update()
        clock.tick(15)


def gameloop():
    global marking_arr
    marking_arr = [[0] * len(inner) for inner in marking_arr]
    turn = random.randrange(2)
    mousex = 0
    mousey = 0  # storing positions of cursor
    flag = False  # True when an occupied box is clicked

    while True:
        mouseClicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mousex, mousey = event.pos
                mouseClicked = True

        boxx, boxy = getBoxAtCursor(mousex, mousey)
        if boxx is not None and boxy is not None:
            if mouseClicked == True and marking_arr[boxy][boxx] == 0:
                flag = False
                marking_arr[boxy][boxx] = turn + 1
                turn = (turn + 1) % 2
            elif mouseClicked == True and marking_arr[boxy][boxx] != 0:
                flag = True

        gameDisplay.fill(white)
        draw_grid()
        if flag:
            message_display("Please select an empty box.", 30, 0.75 * display_width, 50, black)
        if gameover(marking_arr) == 0:
            turn_string = str(turn + 1)
            message_display("It is now Player %s's turn" % turn_string, 30, 200, 50, black)
        else:
            endgame(gameover(marking_arr), 1)

        pygame.display.update()
        clock.tick(15)


def quitgame():
    pygame.quit()
    quit()


game_intro()
pygame.quit()
quit()
