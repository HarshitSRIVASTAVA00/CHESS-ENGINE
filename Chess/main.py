#main driver file .it will be responsible for handling user input and displaying the current GameState object

import pygame as p
import ChessEngine, SmartMoveFinder
import asyncio


BOARD_WIDTH = 512
BOARD_HEIGHT = 512
MOVE_LOG_PANEL_WIDTH = 250
MOVE_LOG_PANEL_HEIGHT = BOARD_HEIGHT
WIDTH = BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH
HEIGHT = BOARD_HEIGHT
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGE = {}

def loadImages():
    pieces = ["bp", "bR", "bN", "bB", "bQ", "bK","wp", "wQ", "wK", "wB", "wN", "wR"]
    for piece in pieces:
        IMAGE[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))



async def main():
    p.init()
    font = p.font.SysFont("Courier New", 16, False, False)
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False #flag variable for when a move is made
    gameOver = False
    loadImages()
    running = True
    sqSelected = () # no square is selected initially
    playerClicks = [] # keep track of player clicks
    playerOne = True # if a human is playing white, then this will be True. If an AI is playing, then it will be False.
    playerTwo = False # same as above but for black


    
    while running:
        humanTurn = (gs.whiteToMoves and playerOne) or (not gs.whiteToMoves and playerTwo)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver and humanTurn:
                    location = p.mouse.get_pos()
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE    
                
                    if col >=8: # the user clicked the same square twice
                        sqSelected = () # deselect
                        playerClicks = [] # clear player clicks
                    else:
                      sqSelected = (row, col)
                      playerClicks.append(sqSelected) # append for both 1st and 2nd clicks
                    
                    if len(playerClicks) == 2: # after 2nd click
                        move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                        print(move.getChessNotation())
                        for i in range(len(validMoves)): 
                            if move == validMoves[i]:
                                gs.makeMove(validMoves[i])
                                moveMade = True
                                animate = True
                                sqSelected = () # reset user clicks
                                playerClicks = [] 
                        if not moveMade:
                            playerClicks = [sqSelected] # keep the 2nd click if it was invalid

            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: # undo when 'z' is pressed
                    gs.undoMove()
                    humanTurn = (gs.whiteToMoves and playerOne) or (not gs.whiteToMoves and playerTwo)
                    if not humanTurn:
                        gs.undoMove()
                    moveMade = True
                    animate = False
                    gameOver = False
                    humanTurn = (gs.whiteToMoves and playerOne) or (not gs.whiteToMoves and playerTwo)
                if e.key == p.K_r: # reset the game when 'r' is pressed
                    gs = ChessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False
                    gameOver = False
                    humanTurn = (gs.whiteToMoves and playerOne) or (not gs.whiteToMoves and playerTwo)

        if not gameOver and not humanTurn and not moveMade:
            AIMove = SmartMoveFinder.findBestMove(gs, validMoves)
            if AIMove is None:
                AIMove = SmartMoveFinder.findRandomMove(validMoves)
            gs.makeMove(AIMove)
            moveMade = True
            animate = True
            sqSelected = () # reset user clicks
            playerClicks = []            

        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1], screen, gs.board, clock)    
            validMoves = gs.getValidMoves()
            moveMade = False 
            animate = False       
                        
        drawGameState(screen, gs, validMoves, sqSelected, font)

        if gs.checkmate:
            gameOver = True
            if gs.whiteToMoves:
                drawText(screen, "Black wins by checkmate")
            else:
                drawText(screen, "White wins by checkmate")
        elif gs.stalemate:
            gameOver = True
            drawText(screen, "Stalemate")   

        clock.tick(MAX_FPS)
        p.display.flip()
        await asyncio.sleep(0)

def highlightSquares(screen, gs, validMoves, sqSelected):
    global colors
    if gs.inCheck:
        # Get the current King's location
        r, c = gs.whiteKingLocation if gs.whiteToMoves else gs.blackKingLocation
        s = p.Surface((SQ_SIZE, SQ_SIZE))
        s.set_alpha(120) 
        s.fill(p.Color('red'))
        screen.blit(s, (c * SQ_SIZE, r * SQ_SIZE))
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMoves else 'b'):
            s = p.surface.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100) # transparency value
            s.fill(p.Color('cyan'))
            screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
            #highlight moves from that square
            s.fill(p.Color('yellow'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (move.endCol*SQ_SIZE, move.endRow*SQ_SIZE))
            



def drawGameState(screen, gs, validMoves, sqSelected, font):
    drawBoard(screen)
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board)
    drawMoveLog(screen, gs, font)


def drawBoard(screen):
    colors = [p.Color("white"), p.Color ("darkgreen")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawPieces(screen, board):
    for r in range(DIMENSION):
         for c in range(DIMENSION):
                piece = board[r][c]
                if piece != "--":
                   screen.blit(IMAGE[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def animateMove(move, screen, board, clock):
    global colors
    colors = [p.Color("white"), p.Color("darkgreen")]
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 5 # frames to move one square
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare
    for frame in range(frameCount + 1):
        r, c = (move.startRow + dR * frame / frameCount, move.startCol + dC * frame / frameCount)
        drawBoard(screen)
        drawPieces(screen, board)
        # erase the piece moved from its ending square
        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = p.Rect(move.endCol * SQ_SIZE, move.endRow * SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, endSquare)
        #draw captured piece onto rectangle
        if move.pieceCaptured != "--":
            screen.blit(IMAGE[move.pieceCaptured], endSquare)
        #draw moving piece
        screen.blit(IMAGE[move.pieceMoved], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(60)

def drawText(screen, text):
    font = p.font.SysFont("Helvetica", 32, True, False) # Font name, size, bold, italic
    textObject = font.render(text, 0, p.Color('Gray'))
    textLocation = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH/2 - textObject.get_width()/2, HEIGHT/2 - textObject.get_height()/2)
    screen.blit(textObject, textLocation)

    textObject = font.render(text, 0, p.Color('Black'))
    screen.blit(textObject, textLocation.move(2, 2))

def drawMoveLog(screen, gs, font):
    #  Draw the background panel
    moveLogRect = p.Rect(BOARD_WIDTH, 0, MOVE_LOG_PANEL_WIDTH, MOVE_LOG_PANEL_HEIGHT)
    p.draw.rect(screen, p.Color("black"), moveLogRect)
    
    #  Build the list of text strings FIRST
    moveLog = gs.moveLog
    moveTexts = []
    for i in range(0, len(moveLog), 2):
        moveString = str(i//2 + 1) + ". " + str(moveLog[i]) + " "
        if i + 1 < len(moveLog):
            moveString += str(moveLog[i+1])
        moveTexts.append(moveString)
        
    #  Define your spacing rules
    padding = 5
    line_spacing = 2
    
    #  Calculate heights NOW that moveTexts actually has items in it
    total_height = len(moveTexts) * (font.get_height() + line_spacing)
    
    # Determine where the text should start (the scrolling logic)
    start_y = padding
    if total_height > moveLogRect.height:
        start_y = moveLogRect.height - total_height - padding
        
    #  Render the text using start_y
    textY = start_y
    for line in moveTexts:
        # Only draw if the line is visible within our panel boundaries
        if textY >= 0 and textY < moveLogRect.height - font.get_height():
            textObject = font.render(line, True, p.Color("white"))
            textLocation = moveLogRect.move(padding, textY)
            screen.blit(textObject, textLocation)
            
        # Increase textY for the next line (whether it was drawn or not)
        textY += font.get_height() + line_spacing


if __name__ == "__main__":
   asyncio.run(main())