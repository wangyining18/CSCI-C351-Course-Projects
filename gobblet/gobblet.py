import sys
import copy

POSITIVE_INFINITY = sys.maxsize
NEGATIVE_INFINITY = -sys.maxsize
N = 4
# different type of pieces
EMPTY = 0
BLACK = 1
WHITE = 2
# The piece:
# None, or small, medium, medium_large, large piece
# Do not change the value. It's related to the index of array
NONE = -1
SMALL = 0
MEDIUM = 1
MEDIUM_LARGE = 2
LARGE = 3
##Players
BLACK_PLAYER = 1
WHITE_PLAYER = -BLACK_PLAYER
#pieces
TOTAL_PIECES=12
#result
WIN=100

class Pos:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def key(self):
        return self.x + self.y * 4

class Piece:
    def __init__(self, color, size):
        self.color = color
        self.size = size
        # (-1,-1) means the piece is out of the board
        self.pos = Pos(-1,-1)
    def __str__(self):
        return "color: {0}, size: {1}, pos( {2}, {3})".format(self.color, self.size, self.pos.x, self.pos.y)

class Board:
    def __init__(self):
        self.black_on_board=[]
        self.black_out_board =[[Piece(BLACK, LARGE), Piece(BLACK,MEDIUM_LARGE),
                             Piece(BLACK,MEDIUM), Piece(BLACK, SMALL)]]
        for i in range(0, 2):
            self.black_out_board.append(copy.deepcopy(self.black_out_board[0]))

        self.white_on_board=[]
        self.white_out_board =[[Piece(WHITE, LARGE), Piece(WHITE,MEDIUM_LARGE),
                            Piece(WHITE,MEDIUM), Piece(WHITE, SMALL)]]
        for i in range(0, 2):
            self.white_out_board.append(copy.deepcopy(self.white_out_board[0]))
        # store the piece on the front on the board
        self.board=dict()

    def place_a_piece(self, piece, x, y, color, on_board):
        if x <0 or x >= N or y <0 or y >= N:
            return False
        key = Pos(x,y).key()
        piece_on_board = self.board.get(key)

        if piece_on_board == None or piece_on_board.size < piece.size:
            if color == BLACK and not on_board:
                self.black_on_board.append(piece)
            elif color == WHITE and not on_board:
                self.white_on_board.append(piece)
            else:
                return False
            piece.pos = Pos(x,y)
            self.board[key]=piece
            return True
        else:
            return False
    def __str__(self):
        res = ""
        for (key, tire) in self.board.items():
            res = res + str(tire) + "\n"
        return res

LEFT_DIAGONAL = 8
RIGHT_DIAGONAL = 9

def terminal(state):
    board = state.board
    count = [ 0 for i in range(0, 10)]
    for (key, piece) in board.items():
        (x,y) = (piece.pos.x, piece.pos.y)
        if x == y:
            if piece.color == BLACK:
                count[LEFT_DIAGONAL] = count[LEFT_DIAGONAL] + 1
            elif piece.color == WHITE:
                count[LEFT_DIAGONAL] = count[LEFT_DIAGONAL] - 1
        if x + y == N-1:
            if piece.color == BLACK:
                count[RIGHT_DIAGONAL] = count[RIGHT_DIAGONAL] + 1
            elif piece.color==WHITE:
                count[RIGHT_DIAGONAL] = count[RIGHT_DIAGONAL] - 1

        if piece.color == BLACK:
            count[x] = count[x] + 1
            count[y+N] = count[y+N] + 1
        elif piece.color == WHITE:
            count[x] = count[x] - 1
            count[y+N] = count[y+N] - 1

    for c in count:
        if c == N:
            return [True, BLACK_PLAYER, WIN]
        elif c == -N:
            return [True, WHITE_PLAYER, WIN]
    return [False, None, 0]



def successors(state, cur_player):
    results=[]
    if cur_player == BLACK_PLAYER:
        for i in range(0, len(state.black_on_board)):
            # move one piece on board
            suc = copy.deepcopy(state)
            piece = suc.black_on_board[i]
            (x,y) = (piece.pos.x, piece.pos.y)
            if suc.place_a_piece(piece, x-1, y, BLACK, True):
                results.append(suc)

            suc = copy.deepcopy(state)
            piece = suc.black_on_board[i]
            (x,y) = (piece.pos.x, piece.pos.y)
            if suc.place_a_piece(piece, x+1, y, BLACK, True):
                results.append(suc)

            suc = copy.deepcopy(state)
            piece = suc.black_on_board[i]
            (x,y) = (piece.pos.x, piece.pos.y)
            if suc.place_a_piece(piece, x, y-1, BLACK, True):
                results.append(suc)

            suc = copy.deepcopy(state)
            piece = suc.black_on_board[i]
            (x,y) = (piece.pos.x, piece.pos.y)
            if suc.place_a_piece(piece, x, y+1, BLACK, True):
                results.append(suc)

        for i in range(0, 3):
            for x in range(0, N):
                for y in range(0, N):
                    # place one piece on board
                    suc = copy.deepcopy(state)
                    if len( suc.black_out_board[i] ) > 0:
                        piece = suc.black_out_board[i].pop(0)
                        if suc.place_a_piece(piece, x, y, BLACK, False):
                            results.append(suc)

    elif cur_player == WHITE_PLAYER:
        for i in range(0, len(state.white_on_board)):
            # move one piece on board
            suc = copy.deepcopy(state)
            piece = suc.white_on_board[i]
            (x,y) = (piece.pos.x, piece.pos.y)
            if suc.place_a_piece(piece, x-1, y, WHITE, True):
                results.append(suc)

            suc = copy.deepcopy(state)
            piece = suc.white_on_board[i]
            (x,y) = (piece.pos.x, piece.pos.y)
            if suc.place_a_piece(piece, x+1, y, WHITE, True):
                results.append(suc)

            suc = copy.deepcopy(state)
            piece = suc.white_on_board[i]
            (x,y) = (piece.pos.x, piece.pos.y)
            if suc.place_a_piece(piece, x, y-1, WHITE, True):
                results.append(suc)

            suc = copy.deepcopy(state)
            piece = suc.white_on_board[i]
            (x,y) = (piece.pos.x, piece.pos.y)
            if suc.place_a_piece(piece, x, y+1, WHITE, True):
                results.append(suc)

        for i in range(0, 3):
            for x in range(0, N):
                for y in range(0, N):
                    # place one piece on board
                    suc = copy.deepcopy(state)
                    if len(suc.white_out_board[i]) > 0:
                        piece = suc.white_out_board[i].pop(0)
                        if suc.place_a_piece(piece, x, y, WHITE, False):
                            results.append(suc)

    return results

# The number of current player's pieces on board minus the number of adversary's pieces on board
def heuristic(state, player):
    res = len(state.black_on_board) - len( state.white_on_board )

    if player == BLACK_PLAYER:
        return res
    elif player == WHITE_PLAYER:
        return -res
    else:
        return 0

def max_value(state, alpha, beta, depth, player):
    (res, won_player, WON) = terminal(state)
    if res:
        if won_player == player:
            return WON
        else:
            return -WON

    if depth <= 0:
        return heuristic(state, player)
    visited=[]
    for succ in successors(state, player):
        if succ in visited:
            continue
        visited.append(succ)
        alpha = max(alpha, min_value(succ, alpha, beta, depth-1, player))
        if alpha >= beta:
            return alpha
    return alpha


def min_value(state, alpha, beta, depth, player):
    (res, won_player, WON) = terminal(state)
    if res:
        if player == won_player:
            return WON
        else:
            return -WON

    if depth <= 0:
        return heuristic(state, player)
    visited=[]
    for succ in successors(state, -player):
        if succ in visited:
            continue
        visited.append(succ)
        beta = min(beta, max_value(succ, alpha, beta, depth-1, player))
        if alpha >= beta:
            return beta
    return beta

# player is the player making the move in this round
def alpha_beta_decision(state, depth, player):
    alpha = NEGATIVE_INFINITY
    beta = POSITIVE_INFINITY
    next_move = None
    next_value = 0
    visited=[]
    for succ in successors(state, player):
        if succ in visited:
            continue
        visited.append(succ)
        val = min_value(succ, alpha, beta, depth, player)
        if alpha < val:
            next_move = succ
            next_value = val

    return next_move


def gobby(players, level, time):
    depth = level*3*time
    depth=1

    state = Board()

    if players == 'h2':
        return
    elif players == 'hr':
        return
    elif players == 'rh':
        return
    elif players == 'rr':
        while True:
            # robot 1: BLACK PLAYER
            print("state for robot1")
            print(state)
            state = alpha_beta_decision(state, depth, BLACK_PLAYER)
            (res, player, WON) = terminal(state)
            if res:
                return player
            print("state for robot2")
            print(state)
            # robot 2: WHITE PLAYER
            state = alpha_beta_decision(state, depth, WHITE_PLAYER)
            (res, player, WON) = terminal(state)
            if res:
                return player
    else:
        print("invalid parameters")
        return False

gobby('rr',1,1)
