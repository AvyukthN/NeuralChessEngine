# driver file

import pygame
from engine import BoardState

pygame.init()

WIDTH = 512
DIMENSION = 8
SQUARE_SIZE = WIDTH // DIMENSION

MAX_FPS = 15
IMAGES = {}

def loadImages():
    pieces = ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR", "bP", "wR", "wN", "wB", "wK", "wQ", "wB", "wN", "wR", "wP"]
    
    for i in range(len(pieces)):
        IMAGES.update({pieces[i]: pygame.transform.scale(pygame.image.load("assets\{}.png".format(pieces[i])), (SQUARE_SIZE, SQUARE_SIZE))})

def boardPrinter(boardArr):
    print("\n")
    for i in range(len(boardArr)):
        lineStr = ""
        for j in range(len(boardArr[i])):
            lineStr += boardArr[i][j] + " "
        print(lineStr)
    print("\n")

def drawBoardState(screen, boardStateObject):
    drawBoard(screen) # draws squares
    drawPieces(screen, boardStateObject.board) # draw pieces on board squares

def drawBoard(screen):
    colors = [pygame.Color("white"), pygame.Color("light blue")]
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            color = colors[((i + j) % 2)]
            pygame.draw.rect(screen, color, pygame.Rect(j * SQUARE_SIZE, i * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def drawPieces(screen, bs):
    boardState = bs.board

    for i in range(len(boardState)):
        for j in range(len(boardState[i])):
            if boardState[i][j] != "--":
                screen.blit(IMAGES[boardState[i][j]], (j * SQUARE_SIZE, i * SQUARE_SIZE))

def vaidMove(moveArr):
    pass

def main():
    screen = pygame.display.set_mode((WIDTH, WIDTH))
    clock = pygame.time.Clock()

    screen.fill(pygame.Color("white"))    
    bs = BoardState()

    boardPrinter(bs.board)

    loadImages() # should only do once before while loop cuz it takes a lot of time to load the images

    SquareSelected = ()
    playerClicks = []

    running = True

    bs.whiteToMove = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running == False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                location = pygame.mouse.get_pos()
                col = location[0] // SQUARE_SIZE
                row = location[1] // SQUARE_SIZE
                
                SquareSelected = (row, col)
                playerClicks.append(SquareSelected)

                if len(playerClicks) == 2 and (playerClicks[1] == playerClicks[0]):
                    SquareSelected = ()
                    playerClicks[1] = []
        
                if (len(playerClicks) == 2 and (playerClicks[0] != playerClicks[1])): 
                    # move
                    if bs.whiteToMove == True:
                        toMove = "w"
                    if bs.whiteToMove == False:
                        toMove = "b"

                    if (bs.board[playerClicks[0][0]][playerClicks[0][1]][0] == toMove):
                        bs.board[playerClicks[1][0]][playerClicks[1][1]] = bs.board[playerClicks[0][0]][playerClicks[0][1]]
                        bs.board[playerClicks[0][0]][playerClicks[0][1]] = "--"

                        bs.moveLog.update({bs.moveCount: [[playerClicks[0][0], playerClicks[0][1]], [playerClicks[1][0], playerClicks[1][1]]]})
                        bs.moveCount += 1

                        temp = bs.whiteToMove
                        bs.whiteToMove = not(temp)

                        print(bs.moveLog)
                        boardPrinter(bs.board)

                    playerClicks = []
                    SquareSelected = ()

        clock.tick(MAX_FPS)
        pygame.display.flip() # this makes the display in pygame only update the portion of the window that it needs to

        drawBoard(screen)
        drawPieces(screen, bs)

if __name__ == '__main__':
    main()
