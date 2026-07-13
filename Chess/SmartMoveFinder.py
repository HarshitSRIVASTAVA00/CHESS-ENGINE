import random

OPENING_BOOK = {

    # QUEEN'S PAWN OPENINGS (1. d4)
    "d2d4": ["d7d5", "g8f6", "f7f5"], # Queen's Pawn, Indian Defenses, Dutch Defense

    # --- THE DUTCH DEFENSE (1. d4 f5) ---
    "d2d4 f7f5": ["g2g3", "c2c4"], 
    "d2d4 f7f5 g2g3": ["g8f6"],
    "d2d4 f7f5 g2g3 g8f6": ["f1g2"], # Classic kingside fianchetto response

    # --- CLOSED GAMES (1. d4 d5) ---
    "d2d4 d7d5": ["c2c4", "g1f3", "c1f4"], # Queen's Gambit, Standard, London System
    "d2d4 d7d5 c2c4": ["e7e6", "c7c6", "d5c4"], # Declined (QGD), Slav, Accepted (QGA)
    
    # Queen's Gambit Declined (QGD)
    "d2d4 d7d5 c2c4 e7e6": ["b1c3", "g1f3"],
    "d2d4 d7d5 c2c4 e7e6 b1c3": ["g8f6", "f8e7"],
    
    # Slav Defense
    "d2d4 d7d5 c2c4 c7c6": ["g1f3", "b1c3"],
    "d2d4 d7d5 c2c4 c7c6 g1f3": ["g8f6"],
    "d2d4 d7d5 c2c4 c7c6 g1f3 g8f6": ["b1c3"],
    
    # Queen's Gambit Accepted (QGA)
    "d2d4 d7d5 c2c4 d5c4": ["g1f3", "e2e3", "e2e4"],
    "d2d4 d7d5 c2c4 d5c4 g1f3": ["g8f6"],

    # --- INDIAN DEFENSES (1. d4 Nf6) ---
    "d2d4 g8f6": ["c2c4", "g1f3"],
    "d2d4 g8f6 c2c4": ["e7e6", "g7g6", "c7c5", "e7e5"], # Nimzo/QID, KID/Grunfeld, Benoni, Budapest

    # Nimzo-Indian & Queen's Indian (QID)
    "d2d4 g8f6 c2c4 e7e6": ["b1c3", "g1f3"],
    "d2d4 g8f6 c2c4 e7e6 b1c3": ["f8b4"], # Nimzo-Indian Defense
    "d2d4 g8f6 c2c4 e7e6 b1c3 f8b4": ["e2e3", "d1c2"],
    "d2d4 g8f6 c2c4 e7e6 g1f3": ["b7b6", "f8b4"], # Queen's Indian / Bogo-Indian
    "d2d4 g8f6 c2c4 e7e6 g1f3 b7b6": ["g2g3", "a2a3"], # Queen's Indian main lines
    
    # King's Indian (KID) & Grunfeld Defense
    "d2d4 g8f6 c2c4 g7g6": ["b1c3", "g2g3"],
    "d2d4 g8f6 c2c4 g7g6 b1c3": ["f8g7", "d7d5"], # KID or Grunfeld
    "d2d4 g8f6 c2c4 g7g6 b1c3 f8g7": ["e2e4"], # King's Indian Mainline
    "d2d4 g8f6 c2c4 g7g6 b1c3 f8g7 e2e4": ["d7d6"], 
    "d2d4 g8f6 c2c4 g7g6 b1c3 d7d5": ["c4d5", "g1f3", "c1f4"], # Grunfeld Mainlines
    
    # Benoni Defense
    "d2d4 g8f6 c2c4 c7c5": ["d4d5"],
    "d2d4 g8f6 c2c4 c7c5 d4d5": ["e7e6", "d7d6"],
    "d2d4 g8f6 c2c4 c7c5 d4d5 e7e6": ["b1c3"],
    
    # Budapest Gambit
    "d2d4 g8f6 c2c4 e7e5": ["d4e5"],
    "d2d4 g8f6 c2c4 e7e5 d4e5": ["f6g4"],
    "d2d4 g8f6 c2c4 e7e5 d4e5 f6g4": ["g1f3", "c1f4"],


    # QUEEN'S PAWN OPENINGS (1. d4)
    
    "d2d4": ["d7d5", "g8f6", "f7f5"], # Queen's Pawn, Indian Defenses, Dutch Defense

    # --- THE DUTCH DEFENSE (1. d4 f5) ---
    "d2d4 f7f5": ["g2g3", "c2c4"], 
    "d2d4 f7f5 g2g3": ["g8f6"],
    "d2d4 f7f5 g2g3 g8f6": ["f1g2"], # Classic kingside fianchetto response

    # --- CLOSED GAMES (1. d4 d5) ---
    "d2d4 d7d5": ["c2c4", "g1f3", "c1f4"], # Queen's Gambit, Standard, London System
    "d2d4 d7d5 c2c4": ["e7e6", "c7c6", "d5c4"], # Declined (QGD), Slav, Accepted (QGA)
    
    # Queen's Gambit Declined (QGD)
    "d2d4 d7d5 c2c4 e7e6": ["b1c3", "g1f3"],
    "d2d4 d7d5 c2c4 e7e6 b1c3": ["g8f6", "f8e7"],
    
    # Slav Defense
    "d2d4 d7d5 c2c4 c7c6": ["g1f3", "b1c3"],
    "d2d4 d7d5 c2c4 c7c6 g1f3": ["g8f6"],
    "d2d4 d7d5 c2c4 c7c6 g1f3 g8f6": ["b1c3"],
    
    # Queen's Gambit Accepted (QGA)
    "d2d4 d7d5 c2c4 d5c4": ["g1f3", "e2e3", "e2e4"],
    "d2d4 d7d5 c2c4 d5c4 g1f3": ["g8f6"],

    # --- INDIAN DEFENSES (1. d4 Nf6) ---
    "d2d4 g8f6": ["c2c4", "g1f3"],
    "d2d4 g8f6 c2c4": ["e7e6", "g7g6", "c7c5", "e7e5"], # Nimzo/QID, KID/Grunfeld, Benoni, Budapest

    # Nimzo-Indian & Queen's Indian (QID)
    "d2d4 g8f6 c2c4 e7e6": ["b1c3", "g1f3"],
    "d2d4 g8f6 c2c4 e7e6 b1c3": ["f8b4"], # Nimzo-Indian Defense
    "d2d4 g8f6 c2c4 e7e6 b1c3 f8b4": ["e2e3", "d1c2"],
    "d2d4 g8f6 c2c4 e7e6 g1f3": ["b7b6", "f8b4"], # Queen's Indian / Bogo-Indian
    "d2d4 g8f6 c2c4 e7e6 g1f3 b7b6": ["g2g3", "a2a3"], # Queen's Indian main lines
    
    # King's Indian (KID) & Grunfeld Defense
    "d2d4 g8f6 c2c4 g7g6": ["b1c3", "g2g3"],
    "d2d4 g8f6 c2c4 g7g6 b1c3": ["f8g7", "d7d5"], # KID or Grunfeld
    "d2d4 g8f6 c2c4 g7g6 b1c3 f8g7": ["e2e4"], # King's Indian Mainline
    "d2d4 g8f6 c2c4 g7g6 b1c3 f8g7 e2e4": ["d7d6"], 
    "d2d4 g8f6 c2c4 g7g6 b1c3 d7d5": ["c4d5", "g1f3", "c1f4"], # Grunfeld Mainlines
    
    # Benoni Defense
    "d2d4 g8f6 c2c4 c7c5": ["d4d5"],
    "d2d4 g8f6 c2c4 c7c5 d4d5": ["e7e6", "d7d6"],
    "d2d4 g8f6 c2c4 c7c5 d4d5 e7e6": ["b1c3"],
    
    # Budapest Gambit
    "d2d4 g8f6 c2c4 e7e5": ["d4e5"],
    "d2d4 g8f6 c2c4 e7e5 d4e5": ["f6g4"],
    "d2d4 g8f6 c2c4 e7e5 d4e5 f6g4": ["g1f3", "c1f4"],
}
transpositionTable = {}

pieceScore = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "p": 1}
# Knight positional scores: encourage center control, punish edges
knightScores = [
    [-0.5, -0.4, -0.3, -0.3, -0.3, -0.3, -0.4, -0.5],
    [-0.4, -0.2,  0.0,  0.0,  0.0,  0.0, -0.2, -0.4],
    [-0.3,  0.0,  0.1,  0.1,  0.1,  0.1,  0.0, -0.3],
    [-0.3,  0.0,  0.1,  0.2,  0.2,  0.1,  0.0, -0.3],
    [-0.3,  0.0,  0.1,  0.2,  0.2,  0.1,  0.0, -0.3],
    [-0.3,  0.0,  0.1,  0.1,  0.1,  0.1,  0.0, -0.3],
    [-0.4, -0.2,  0.0,  0.0,  0.0,  0.0, -0.2, -0.4],
    [-0.5, -0.4, -0.3, -0.3, -0.3, -0.3, -0.4, -0.5]
]

# Bishop positional scores: encourage diagonals and active development
bishopScores = [
    [-0.2, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.2],
    [-0.1,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.1],
    [-0.1,  0.0,  0.1,  0.1,  0.1,  0.1,  0.0, -0.1],
    [-0.1,  0.0,  0.1,  0.2,  0.2,  0.1,  0.0, -0.1],
    [-0.1,  0.0,  0.1,  0.2,  0.2,  0.1,  0.0, -0.1],
    [-0.1,  0.0,  0.1,  0.1,  0.1,  0.1,  0.0, -0.1],
    [-0.1,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.1],
    [-0.2, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.2]
]

# Pawn positional scores: reward pushing forward toward promotion
pawnScores = [
    [ 0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
    [ 0.8,  0.8,  0.8,  0.8,  0.8,  0.8,  0.8,  0.8],
    [ 0.5,  0.5,  0.5,  0.5,  0.5,  0.5,  0.5,  0.5],
    [ 0.3,  0.3,  0.3,  0.4,  0.4,  0.3,  0.3,  0.3],
    [ 0.2,  0.2,  0.2,  0.3,  0.3,  0.2,  0.2,  0.2],
    [ 0.1,  0.1,  0.1,  0.0,  0.0,  0.1,  0.1,  0.1],
    [ 0.1,  0.1,  0.1, -0.2, -0.2,  0.1,  0.1,  0.1],
    [ 0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0]
]

# King Middlegame: Hide in the corners (castling squares like g1 and c1 get bonuses)
kingScores = [
    [-0.3, -0.4, -0.4, -0.5, -0.5, -0.4, -0.4, -0.3],
    [-0.3, -0.4, -0.4, -0.5, -0.5, -0.4, -0.4, -0.3],
    [-0.3, -0.4, -0.4, -0.5, -0.5, -0.4, -0.4, -0.3],
    [-0.3, -0.4, -0.4, -0.5, -0.5, -0.4, -0.4, -0.3],
    [-0.2, -0.3, -0.3, -0.4, -0.4, -0.3, -0.3, -0.2],
    [-0.1, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.1],
    [ 0.2,  0.2,  0.0,  0.0,  0.0,  0.0,  0.2,  0.2],
    [ 0.2,  0.3,  0.1,  0.0,  0.0,  0.1,  0.3,  0.2]
]

# King Endgame: March to the center (e4, d4, e5, d5 get massive bonuses)
kingEndgameScores = [
    [-0.5, -0.4, -0.3, -0.2, -0.2, -0.3, -0.4, -0.5],
    [-0.3, -0.2, -0.1,  0.0,  0.0, -0.1, -0.2, -0.3],
    [-0.3, -0.1,  0.2,  0.3,  0.3,  0.2, -0.1, -0.3],
    [-0.3, -0.1,  0.3,  0.4,  0.4,  0.3, -0.1, -0.3],
    [-0.3, -0.1,  0.3,  0.4,  0.4,  0.3, -0.1, -0.3],
    [-0.3, -0.1,  0.2,  0.3,  0.3,  0.2, -0.1, -0.3],
    [-0.3, -0.3,  0.0,  0.0,  0.0,  0.0, -0.3, -0.3],
    [-0.5, -0.3, -0.3, -0.3, -0.3, -0.3, -0.3, -0.5]
]

piecePositionScores = {"N": knightScores, "B": bishopScores, "p": pawnScores, "K": kingScores, "k": kingEndgameScores}
CHECKMATE = 1000
STALEMATE = 0
DEPTH = 4


def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves) - 1)]

def findBestMove(gs, validMoves):
    global nextMove
    nextMove = None
    transpositionTable.clear()
    historyString = getGameHistoryString(gs)
    if historyString in OPENING_BOOK:
        bookMoves = OPENING_BOOK[historyString]
        chosenBookMoveStr = random.choice(bookMoves)
        for move in validMoves:
            moveStr = move.getRankFile(move.startRow, move.startCol) + move.getRankFile(move.endRow, move.endCol)
            if moveStr == chosenBookMoveStr:
                print(f"Book move played: {chosenBookMoveStr}") # For your terminal testing
                return move # Return instantly! No math required!
    random.shuffle(validMoves)
    turnMultiplier = 1 if gs.whiteToMoves else -1
    findMoveNegaMaxAlphaBeta(gs, validMoves, DEPTH, -CHECKMATE, CHECKMATE, turnMultiplier)
    return nextMove  


def findMoveNegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, turnMultiplier):
    global nextMove
    
    # Create a unique string for this exact board state
    boardHash = str(gs.board) + str(gs.whiteToMoves)
    
    if boardHash in transpositionTable:
        entry = transpositionTable[boardHash]
        # Only use the memory if it looked as deep or deeper than we currently need
        if entry['depth'] >= depth:
            score = entry['score']
            if entry['flag'] == 'exact':
                return score
            elif entry['flag'] == 'lowerbound' and score > alpha:
                alpha = score
            elif entry['flag'] == 'upperbound' and score < beta:
                beta = score
            if alpha >= beta:
                return score

    if depth == 0:
        return quiescenceSearch(gs, alpha, beta, turnMultiplier)

    maxScore = -CHECKMATE   
    validMoves.sort(key=scoreMove, reverse=True) 
    
    alphaOrig = alpha # Save the original alpha to figure out what kind of score we got

    for playerMove in validMoves:
        gs.makeMove(playerMove)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMaxAlphaBeta(gs, nextMoves, depth - 1, -beta, -alpha, -turnMultiplier)
        gs.undoMove()  
        
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = playerMove
                
        if maxScore > alpha:
            alpha = maxScore
        if alpha >= beta:
            break
    # Figure out what kind of score we ended up with
    flag = 'exact'
    if maxScore <= alphaOrig:
        flag = 'upperbound'
    elif maxScore >= beta:
        flag = 'lowerbound'
        
    # Save it to the memory bank
    transpositionTable[boardHash] = {
        'score': maxScore,
        'depth': depth,
        'flag': flag
    }      
    return maxScore

def quiescenceSearch(gs, alpha, beta, turnMultiplier):

    stand_pat = turnMultiplier * scoreBoard(gs)

    if stand_pat >= beta:
        return beta
    if alpha < stand_pat:
        alpha = stand_pat
        
    validMoves = gs.getValidMoves()
    validMoves.sort(key=scoreMove, reverse=True)
    
    for move in validMoves:
        if move.pieceCaptured == "--":
            continue # Skip non-captures to prevent infinite search loops
            
        gs.makeMove(move)
        # Recursively call Quiescence Search
        score = -quiescenceSearch(gs, -beta, -alpha, -turnMultiplier)
        gs.undoMove()
        
        if score >= beta:
            return beta
        if score > alpha:
            alpha = score
            
    return alpha

def scoreBoard(gs):
    if gs.checkmate:
        if gs.whiteToMoves:
            return -CHECKMATE # Black wins
        else:
            return CHECKMATE # White wins
    elif gs.stalemate:
        return STALEMATE
        
    score = 0
    white_pawn_files = [0] * 8
    black_pawn_files = [0] * 8
    isEndgame = False
    whiteQueenCount = sum([row.count("wQ") for row in gs.board])
    blackQueenCount = sum([row.count("bQ") for row in gs.board])
    if whiteQueenCount == 0 and blackQueenCount == 0:
        isEndgame = True
    
    # Make sure we use the right King table
    piecePositionScores["K"] = kingEndgameScores if isEndgame else kingScores

    for row in range(len(gs.board)):
        for col in range(len(gs.board[row])):
            square = gs.board[row][col]
            if square != "--":
                piece_color = square[0]
                piece_type = square[1]
                if piece_type == "p":
                    if piece_color == "w":
                        white_pawn_files[col] += 1
                    elif piece_color == "b":
                        black_pawn_files[col] += 1
                
                # 1. Base Material Score
                material_val = pieceScore[piece_type]
                
                # 2. Positional Score (if table exists for this piece)
                position_val = 0
                if piece_type in piecePositionScores:
                    if piece_color == 'w':
                        position_val = piecePositionScores[piece_type][row][col]
                    elif piece_color == 'b':
                        # Flip the row index so Black values moving downward!
                        position_val = piecePositionScores[piece_type][7 - row][col]
                
                # 3. Combine scores
                if piece_color == 'w':
                    score += (material_val + position_val)
                elif piece_color == 'b':
                    score -= (material_val + position_val)
            
    pawn_score = 0
    for col in range(8):
        # Doubled Pawns Penalty (-0.1 per extra pawn)
        if white_pawn_files[col] > 1:
            pawn_score -= 0.1 * (white_pawn_files[col] - 1)
        if black_pawn_files[col] > 1:
            pawn_score += 0.1 * (black_pawn_files[col] - 1) # + means good for White, bad for Black
            
        # Isolated Pawns Penalty (-0.1)
        if white_pawn_files[col] > 0:
            left_w = white_pawn_files[col - 1] if col > 0 else 0
            right_w = white_pawn_files[col + 1] if col < 7 else 0
            if left_w == 0 and right_w == 0:
                pawn_score -= 0.1
                
        if black_pawn_files[col] > 0:
            left_b = black_pawn_files[col - 1] if col > 0 else 0
            right_b = black_pawn_files[col + 1] if col < 7 else 0
            if left_b == 0 and right_b == 0:
                pawn_score += 0.1
        if white_pawn_files[col] > 0:
            left_b = black_pawn_files[col - 1] if col > 0 else 0
            right_b = black_pawn_files[col + 1] if col < 7 else 0
            center_b = black_pawn_files[col]
            if left_b == 0 and right_b == 0 and center_b == 0:
                pawn_score += 0.3 # Huge bonus for White
                
        if black_pawn_files[col] > 0:
            left_w = white_pawn_files[col - 1] if col > 0 else 0
            right_w = white_pawn_files[col + 1] if col < 7 else 0
            center_w = white_pawn_files[col]
            if left_w == 0 and right_w == 0 and center_w == 0:
                pawn_score -= 0.3 # Huge bonus for Black
                
    # Add the pawn structure score to the main score
    score += pawn_score
        
                    
    return score

def scoreMove(move):
    moveScore = 0
    
    if move.pieceCaptured != "--":
        moveScore = 10 * pieceScore[move.pieceCaptured[1]] - pieceScore[move.pieceMoved[1]]
        
    if move.isPawnPromotion:
        moveScore += 90 # Treat it like capturing a Queen
        
    # Note: You can add checks here later if you add an 'isCheck' flag to your Move class!
    
    return moveScore

def getGameHistoryString(gs):
    history = []
    for move in gs.moveLog:
        # Get standard coordinate notation (e.g., 'e2' + 'e4')
        start_sq = move.getRankFile(move.startRow, move.startCol)
        end_sq = move.getRankFile(move.endRow, move.endCol)
        history.append(start_sq + end_sq)
        
    return " ".join(history)