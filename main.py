import random
import os
import curses


BOARD_SIZE = 4


def calculateBranch(score):
    return score


def moveAllTiles(board, vector):
    somethingChanged = False
    currentTile = [0, 0]
    #screen.addstr(str(vector))
    #getUserInput(screen)
    while currentTile[1] < BOARD_SIZE:
        # if tile was moved, then start over again
        moved = moveTile(board, currentTile, vector)
        #screen.addstr(str(currentTile))
        #screen.addstr(str(moved))
        #getUserInput(screen)
        if moved:
            somethingChanged = True
            currentTile = [-1, 0]

        # if tile was not moved, keep going down the board
        if currentTile[0] < BOARD_SIZE - 1:
            currentTile[0] += 1
        else:
            currentTile[0] = 0
            currentTile[1] += 1
    return somethingChanged


def moveTile(board, currentTile, vector):
    # get the location we want to move to
    moveIntoTile = (currentTile[0] + vector[0], currentTile[1] + vector[1])

    # if currentTile is zero, don't worry moving it
    if board[currentTile[1]][currentTile[0]] == 0:
        return False

    # if attempted move is outside of board, can't move there
    if moveIntoTile[0] < 0 or moveIntoTile[0] >= BOARD_SIZE or moveIntoTile[1] < 0 or moveIntoTile[1] >= BOARD_SIZE:
        return False

    # if the move tile is empty, move there
    if board[moveIntoTile[1]][moveIntoTile[0]] == 0:
        board[moveIntoTile[1]][moveIntoTile[0]] = board[currentTile[1]][currentTile[0]]
        board[currentTile[1]][currentTile[0]] = 0
        return True

    # if the move tile has the same value as the current tile, combine them and move
    if board[moveIntoTile[1]][moveIntoTile[0]] == board[currentTile[1]][currentTile[0]]:
        board[moveIntoTile[1]][moveIntoTile[0]] = board[moveIntoTile[1]][moveIntoTile[0]] * 2
        board[currentTile[1]][currentTile[0]] = 0
        return True

    # if we still haven't moved, then we can't move
    return False


def addNewValue(board):
    location = getTuple()
    while board[location[1]][location[0]] != 0:
        location = getTuple()
    board[location[1]][location[0]] = 2


def updateBoard(board, move):
    # get movement vector
    if move == "up":
        vector = (0, -1)
    elif move == "down":
        vector = (0, 1)
    elif move == "left":
        vector = (-1, 0)
    else:
        vector = (1, 0)

    # move all current pieces
    # make sure something has actually moved!
    somethingChanged = moveAllTiles(board, vector)
    if not somethingChanged:
        nextMove = getUserInput(screen)
        updateBoard(board, nextMove)
    else:
        # add a new 2 value to board if something has changed
        addNewValue(board)


def printBoard(board, screen):
    screen.clear()

    line = ""
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            line += str(board[y][x]) + "\t"
        line += "\n"
    screen.addstr(line)


def initializeBoard(board):
    firstLocation = getTuple()
    secondLocation = getTuple()
    while(secondLocation == firstLocation):
        secondLocation = getTuple()
    board[firstLocation[0]][firstLocation[1]] = 2
    board[secondLocation[0]][secondLocation[1]] = 2


def getTuple():
    first = random.randint(0, BOARD_SIZE - 1)
    second = random.randint(0, BOARD_SIZE - 1)
    return first, second


def gameOver(board):
    # check for win
    for y in range(BOARD_SIZE - 1):
        for x in range(BOARD_SIZE):
            if board[y][x] == 2048:
                return True
    # check for loss, if any two adjacent slots have the same number, not game over
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            if sameAdjacent(board, (x, y)):
                return False
    return True


def sameAdjacent(board, location):
    # We don't need to check left and up, because we are working our way down and to the right
    # so they have already been checked
    # check right
    if location[0] + 1 <= BOARD_SIZE - 1:
        if board[location[0]][location[1]] == board[location[0] + 1][location[1]]:
            return True
    # check down
    if location[1] + 1 <= BOARD_SIZE - 1:
        if board[location[0]][location[1]] == board[location[0]][location[1] + 1]:
            return True


def getUserInput(screen):
    event = screen.getch()
    if event == curses.KEY_LEFT:
        return "left"
    elif event == curses.KEY_RIGHT:
        return "right"
    elif event == curses.KEY_UP:
        return "up"
    elif event == curses.KEY_DOWN:
        return "down"
    elif event == 113:
        curses.endwin()
        exit()
    else:
        getUserInput(screen)


# main function

# set up
screen = curses.initscr()
random.seed()
board = [[0 for x in range(BOARD_SIZE)] for x in range(BOARD_SIZE)]
initializeBoard(board)
curses.noecho()
curses.curs_set(0)
screen.keypad(1)

# intro screen
screen.addstr("Welcome to 2048! The objective of the game is to get a node to 2048. Use the arrow keys to move nodes and press 'q' to quit\n\nPress any key to continue...")
screen.getch()

# main game loop
try:
    while(not gameOver(board)):
        screen.clear()
        printBoard(board, screen)
        move = getUserInput(screen)
        updateBoard(board, move)
    screen.clear()
    screen.addstr("Game over!")
    getUserInput(screen)
finally:
    curses.endwin()
