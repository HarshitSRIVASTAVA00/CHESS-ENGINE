"""
this class is responsible for storing all the info about the current state of chess game . it wii also be
responsible for determining the valid moves at the current state . it will also keep a move log .
"""

class GameState():
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.moveFunctions = {"p": self.getPawnMoves, "R": self.getRookMoves, 
                              "N": self.getKnightMoves, "B": self.getBishopMoves,
                              "Q": self.getQueenMoves, "K": self.getKingMoves}
        self.whiteToMoves = True
        self.moveLog = []
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.inCheck = False
        self.pins = []
        self.checks = []
        self.enpassantPossible = () #coordinates for the square where en passant capture is possible
        self.enpassantPossibleLog = [self.enpassantPossible]
        self.currentCastlingRights = CastleRights(True, True, True, True)
        self.castleRightsLog = [CastleRights(self.currentCastlingRights.wks, self.currentCastlingRights.bks, self.currentCastlingRights.wqs, self.currentCastlingRights.bqs)]
        self.checkmate = False
        self.stalemate = False


    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) #log the move so we can undo it later
        self.whiteToMoves = not self.whiteToMoves #swap players
        #update the king's location if moved
        if move.pieceMoved == "wK":
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == "bK":
            self.blackKingLocation = (move.endRow, move.endCol)

        #pawn promotion
        if move.isPawnPromotion:
            promotedPiece = "Q" 
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + promotedPiece  

        #en passant move
        if move.isEnpassantMove:
            self.board[move.startRow][move.endCol] = "--" #capturing the pawn

        #update enpassantPossible variable
        if move.pieceMoved[1] == "p" and abs(move.startRow - move.endRow) == 2: #only on 2 square pawn advances
            self.enpassantPossible = ((move.startRow + move.endRow)//2, move.startCol) 
        else:
            self.enpassantPossible = ()

        self.enpassantPossibleLog.append(self.enpassantPossible)   

        #castle move
        if move.isCastleMove:
            if move.endCol - move.startCol == 2: #kingside castle move
                self.board[move.endRow][move.endCol-1] = self.board[move.endRow][move.endCol+1] #moves the rook
                self.board[move.endRow][move.endCol+1] = "--" #erase old rook
            else: #queenside castle move
                self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-2] #moves the rook
                self.board[move.endRow][move.endCol-2] = "--" #erase old rook

        #update castle rights
        self.updateCastleRights(move)
        self.castleRightsLog.append(CastleRights(self.currentCastlingRights.wks, self.currentCastlingRights.bks, 
                                                 self.currentCastlingRights.wqs, self.currentCastlingRights.bqs))
      
            


    def undoMove(self):
        if len(self.moveLog) != 0: #make sure that there is a move to undo
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMoves = not self.whiteToMoves #switch turns back   
            #update king's location if needed
            if move.pieceMoved == "wK":
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == "bK":
                self.blackKingLocation = (move.startRow, move.startCol)

            #undo en passant
            if move.isEnpassantMove:
                self.board[move.endRow][move.endCol] = "--" # Leave the ghost square empty
                self.board[move.startRow][move.endCol] = move.pieceCaptured # Put the pawn back on the correct square

            #undo a 2 square pawn advance
            self.enpassantPossibleLog.pop()
            self.enpassantPossible = self.enpassantPossibleLog[-1] # Set it back to the exact previous state   

            #undo castle move
            if move.isCastleMove:
                if move.endCol - move.startCol == 2: #kingside
                    self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-1]
                    self.board[move.endRow][move.endCol-1] = "--"
                else: #queenside
                    self.board[move.endRow][move.endCol-2] = self.board[move.endRow][move.endCol+1]
                    self.board[move.endRow][move.endCol+1] = "--"

            #undo castling rights
            self.castleRightsLog.pop() #get rid of the new castle rights from the move
            newRights = self.castleRightsLog[-1] # look at the previous rights
            self.currentCastlingRights = CastleRights(newRights.wks, newRights.bks, newRights.wqs, newRights.bqs)        
        

    def updateCastleRights(self, move):
        if move.pieceMoved == "wK":
            self.currentCastlingRights.wks = False
            self.currentCastlingRights.wqs = False
        elif move.pieceMoved == "bK":
            self.currentCastlingRights.bks = False
            self.currentCastlingRights.bqs = False
        elif move.pieceMoved == "wR":
            if move.startRow == 7:
                if move.startCol == 0: #left rook
                    self.currentCastlingRights.wqs = False
                elif move.startCol == 7: #right rook
                    self.currentCastlingRights.wks = False
        elif move.pieceMoved == "bR":
            if move.startRow == 0:
                if move.startCol == 0: #left rook
                    self.currentCastlingRights.bqs = False
                elif move.startCol == 7: #right rook
                    self.currentCastlingRights.bks = False        

    #valid moves
    def getValidMoves(self):
        moves = []
        self.inCheck, self.pins, self.checks = self.checkForPinsAndChecks()
        if self.whiteToMoves:
            kingRow = self.whiteKingLocation[0]
            kingCol = self.whiteKingLocation[1]
        else:
            kingRow = self.blackKingLocation[0]
            kingCol = self.blackKingLocation[1]
        if self.inCheck:
            if len(self.checks) == 1: #only 1 check, block or move king
                moves = self.getAllPossibleMoves()
                #to block check you must move a piece into one of the squares between the enemy piece and king
                check = self.checks[0] #check information
                checkRow = check[0]
                checkCol = check[1]
                pieceChecking = self.board[checkRow][checkCol] #enemy piece causing the check
                validSquares = [] #squares that pieces can move to
                #if knight, must capture knight or move king, other pieces can be blocked
                if pieceChecking[1] == "N":
                    validSquares = [(checkRow, checkCol)] #knights can only be blocked by capturing knight
                else:
                    for i in range(1, 8):
                        validSquare = (kingRow + check[2] * i, kingCol + check[3] * i) #check[2] and check[3] are the check directions
                        validSquares.append(validSquare)
                        if validSquare[0] == checkRow and validSquare[1] == checkCol: #once you get to piece end checking
                            break
                #get rid of any moves that don't block check or move king
                for i in range(len(moves)-1, -1, -1): #go through backwards when removing from a list as iterating
                    if moves[i].pieceMoved[1] != "K": #move doesn't move king so it must block or capture
                        if not (moves[i].endRow, moves[i].endCol) in validSquares: #move doesn't block or capture so remove it
                            moves.remove(moves[i])
            else: #double check, king has to move
                self.getKingMoves(kingRow, kingCol, moves)    
        else: #not in check so all moves are fine
            moves = self.getAllPossibleMoves() 
        if self.whiteToMoves:
            self.getCastleMoves(self.whiteKingLocation[0], self.whiteKingLocation[1], moves, "w")
        else:
            self.getCastleMoves(self.blackKingLocation[0], self.blackKingLocation[1], moves, "b")       
        if len(moves) == 0:
            if self.inCheck:
                self.checkmate = True
            else:
                self.stalemate = True
        else:
            self.checkmate = False
            self.stalemate = False    

        return moves


    def inCheck(self):
        if self.whiteToMoves:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])

    def squareUnderAttack(self, r, c):
        self.whiteToMoves = not self.whiteToMoves #switch to opponent's turn
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMoves = not self.whiteToMoves #switch turns back
        for move in oppMoves:
            if move.endRow == r and move.endCol == c: #square is under attack
                return True
        return False        

    def getAllPossibleMoves(self):           
        moves = [] #list of moves
        for r in range(len(self.board)): #number of rows  
            for c in range(len(self.board[r])): #number of columns in given row
                turn = self.board[r][c][0]
                if (turn == "w" and self.whiteToMoves) or (turn == "b" and not self.whiteToMoves):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves) #calls the appropriate move function based on piece type
        return moves                

    def getPawnMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
                
        if self.whiteToMoves: #white pawn moves
            if self.board[r-1][c] == "--": #1 square pawn advance
                # ONLY move forward if not pinned, or if pinned vertically
                if not piecePinned or pinDirection == (-1, 0) or pinDirection == (1, 0):
                    moves.append(Move((r, c), (r-1, c), self.board))
                    if r == 6 and self.board[r-2][c] == "--": #2 square pawn advance
                        moves.append(Move((r, c), (r-2, c), self.board))
                        
            if c-1 >= 0: #capture to the left
                if self.board[r-1][c-1][0] == "b": #enemy piece to capture
                    # ONLY capture if not pinned, or if pinned in this exact diagonal
                    if not piecePinned or pinDirection == (-1, -1):
                        moves.append(Move((r, c), (r-1, c-1), self.board))   
                elif (r-1, c-1) == self.enpassantPossible:
                    if not piecePinned or pinDirection == (-1, -1):
                        moves.append(Move((r, c), (r-1, c-1), self.board, isEnpassantMove=True))
                        
            if c+1 <= 7: #capture to the right
                if self.board[r-1][c+1][0] == "b": #enemy piece to capture
                    if not piecePinned or pinDirection == (-1, 1):
                        moves.append(Move((r, c), (r-1, c+1), self.board))
                elif (r-1, c+1) == self.enpassantPossible:
                    if not piecePinned or pinDirection == (-1, 1):
                        moves.append(Move((r, c), (r-1, c+1), self.board, isEnpassantMove=True))
                            

        else: #black pawn moves
            if self.board[r+1][c] == "--": #1 square pawn advance
                if not piecePinned or pinDirection == (-1, 0) or pinDirection == (1, 0):
                    moves.append(Move((r, c), (r+1, c), self.board))
                    if r == 1 and self.board[r+2][c] == "--": #2 square pawn advance
                        moves.append(Move((r, c), (r+2, c), self.board))
                        
            if c-1 >= 0: #capture to the left
                if self.board[r+1][c-1][0] == "w": #enemy piece to capture
                    if not piecePinned or pinDirection == (1, -1):
                        moves.append(Move((r, c), (r+1, c-1), self.board))  
                elif (r+1, c-1) == self.enpassantPossible:
                    if not piecePinned or pinDirection == (1, -1):
                        moves.append(Move((r, c), (r+1, c-1), self.board, isEnpassantMove=True))          
                        
            if c+1 <= 7: #capture to the right
                if self.board[r+1][c+1][0] == "w": #enemy piece to capture
                    if not piecePinned or pinDirection == (1, 1):
                        moves.append(Move((r, c), (r+1, c+1), self.board))
                elif (r+1, c+1) == self.enpassantPossible:
                    if not piecePinned or pinDirection == (1, 1):
                        moves.append(Move((r, c), (r+1, c+1), self.board, isEnpassantMove=True))    
                    
    def getRookMoves(self, r, c, moves):
            piecePinned = False
            pinDirection = ()
            for i in range(len(self.pins)-1, -1, -1):
                if self.pins[i][0] == r and self.pins[i][1] == c:
                    piecePinned = True
                    pinDirection = (self.pins[i][2], self.pins[i][3])
                    if self.board[r][c][1] != "Q": #can't remove queen from pin on rook moves, only remove it on bishop moves
                        self.pins.remove(self.pins[i])
                    break
            directions = ((-1, 0), (0, -1), (1, 0), (0, 1)) #up, left, down, right
            enemyColor = "b"  if self.whiteToMoves else "w"
            for d in directions:
                for i in range(1, 8):
                   endRow = r + d[0] * i
                   endCol = c + d[1] * i

                   if 0 <= endRow < 8 and 0 <= endCol < 8: # on board
                       # 1. Check if pinned in this direction
                       if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
                           endPiece = self.board[endRow][endCol]
                           # 2. Check the piece
                           if endPiece == "--": # empty space valid
                               moves.append(Move((r, c), (endRow, endCol), self.board))
                           elif endPiece[0] == enemyColor: # enemy piece valid
                               moves.append(Move((r, c), (endRow, endCol), self.board))
                               break
                           else: # friendly piece invalid
                               break
                       else: # if pinned in a different direction, it can't move this way at all
                           break
                   else: # off board
                       break        

    def getKnightMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        allyColor = "w" if self.whiteToMoves else "b"
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                if not piecePinned:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] != allyColor: #not an ally piece (empty or enemy piece)
                        moves.append(Move((r, c), (endRow, endCol), self.board))

    def getBishopMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1)) #4 diagonals
        enemyColor = "b"  if self.whiteToMoves else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8: #on board
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
                     endPiece = self.board[endRow][endCol]
                     if endPiece == "--": #empty space valid
                         moves.append(Move((r, c), (endRow, endCol), self.board))
                     elif endPiece[0] == enemyColor: #enemy piece valid
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                     else: #friendly piece invalid
                        break
                else: #off board
                    break

    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)
     
    def getKingMoves(self, r, c, moves):
        rowMoves = (-1, -1, -1, 0, 0, 1, 1, 1)
        colMoves = (-1, 0, 1, -1, 1, -1, 0, 1)
        allyColor = "w" if self.whiteToMoves else "b"
        for i in range(8):
            endRow = r + rowMoves[i]
            endCol = c + colMoves[i]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor: #not an ally piece (empty or enemy piece)
                    #place king on end square and check for checks
                    if allyColor == "w":
                        self.whiteKingLocation = (endRow, endCol)
                    else:
                        self.blackKingLocation = (endRow, endCol)
                    inCheck, pins, checks = self.checkForPinsAndChecks()
                    if not inCheck:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    #place king back on original location
                    if allyColor == "w":
                        self.whiteKingLocation = (r, c)
                    else:
                        self.blackKingLocation = (r, c)

    def checkForPinsAndChecks(self):
        pins = [] #squares allied pinned piece and direction pinned from
        checks = [] #squares where enemy is applying a check
        inCheck = False
        if self.whiteToMoves:
            enemyColor = "b"
            allyColor = "w"
            startRow = self.whiteKingLocation[0]
            startCol = self.whiteKingLocation[1]
        else:
            enemyColor = "w"
            allyColor = "b"
            startRow = self.blackKingLocation[0]
            startCol = self.blackKingLocation[1]
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for j in range(len(directions)):
            d = directions[j]
            possiblePin = () #reset possible pins
            for i in range(1, 8):
                endRow = startRow + d[0] * i
                endCol = startCol + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] == allyColor and endPiece[1] != "K":
                        if possiblePin == (): #first allied piece could be pinned
                            possiblePin = (endRow, endCol, d[0], d[1])
                        else: #2nd allied piece so no pin or check possible in this direction
                            break
                    elif endPiece[0] == enemyColor:
                        type = endPiece[1]
                        
                        if (0 <= j <= 3 and type == "R") or (4 <= j <= 7 and type == "B") or (i == 1 and type == "p" and ((enemyColor == "w" and 6 <= j <= 7) or (enemyColor == "b" and 4 <= j <= 5))) or (type == "Q") or (i == 1 and type == "K"):
                            if possiblePin == (): #no piece blocking so check
                                inCheck = True
                                checks.append((endRow, endCol, d[0], d[1]))
                                break
                            else: #piece blocking so pin
                                pins.append(possiblePin)
                                break
                        else: #enemy piece not applying check
                            break
                else: #off board
                    break #break out of loop for this direction 
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for m in knightMoves:
            endRow = startRow + m[0]
            endCol = startCol + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] == enemyColor and endPiece[1] == 'N': # enemy knight attacking king
                    inCheck = True
                    checks.append((endRow, endCol, m[0], m[1]))
                    
        return inCheck, pins, checks


    def getCastleMoves(self, r, c, moves, allyColor):
        if self.squareUnderAttack(r, c):
            return # can't castle while we are in check
        if (self.whiteToMoves and self.currentCastlingRights.wks) or (not self.whiteToMoves and self.currentCastlingRights.bks):
            self.getKingsideCastleMoves(r, c, moves, allyColor)
        if (self.whiteToMoves and self.currentCastlingRights.wqs) or (not self.whiteToMoves and self.currentCastlingRights.bqs):
            self.getQueensideCastleMoves(r, c, moves, allyColor)

    def getKingsideCastleMoves(self, r, c, moves, allyColor):
        if c != 4:
            return
        # Check if the two squares to the right are empty
        if self.board[r][c+1] == '--' and self.board[r][c+2] == '--':
            # Check if those two squares are under attack
            if not self.squareUnderAttack(r, c+1) and not self.squareUnderAttack(r, c+2):
                moves.append(Move((r, c), (r, c+2), self.board, isCastleMove=True))

    def getQueensideCastleMoves(self, r, c, moves, allyColor):
        if c != 4:
            return
        # Check if the three squares to the left are empty
        if self.board[r][c-1] == '--' and self.board[r][c-2] == '--' and self.board[r][c-3] == '--':
            # Check if the two squares the King moves through are under attack
            if not self.squareUnderAttack(r, c-1) and not self.squareUnderAttack(r, c-2):
                moves.append(Move((r, c), (r, c-2), self.board, isCastleMove=True))    
  


class CastleRights():
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs                               

                  

class Move():
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board, isEnpassantMove=False, isCastleMove=False):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]        
        self.isPawnPromotion = False
        if (self.pieceMoved == "wp" and self.endRow == 0) or (self.pieceMoved == "bp" and self.endRow == 7):
            self.isPawnPromotion = True
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol 

        self.isEnpassantMove = isEnpassantMove
        if self.isEnpassantMove:
            self.pieceCaptured = "wp" if self.pieceMoved == "bp" else "bp"

        self.isCastleMove = isCastleMove    
          

    def  __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]        