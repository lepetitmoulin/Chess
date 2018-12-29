import copy #needed to make a 'dummy' board to determine if a move is legal

ranks = '12345678'
files = 'abcdefgh'
wQR, wKR, wKing, bQR, bKR, bKing = 0,0,0,0,0,0 #weird looking -- but this is for castling purposes !
en_passant = False
colors = {'w': 'White', 'b':'Black'}
enemies = {'w': 'b', 'b': 'w'}

'''
notation for the board is reversed, and negative for the ranks
e.g. the square e7, occupied at the outset by 'bP' is denoted by (-7, 4). e -> 4, 7 -> -7, then reverse
Thus, while typical moves are denoted, in algebraic notation, by 'f''r', here they are (-r, f)
'''
board = [['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
['e ', 'e ', 'e ', 'e ', 'e ', 'e ', 'e ', 'e '],
['e ', 'e ', 'e ', 'e ', 'e ', 'e ', 'e ', 'e '],
['e ', 'e ', 'e ', 'e ', 'e ', 'e ', 'e ', 'e '],
['e ', 'e ', 'e ', 'e ', 'e ', 'e ', 'e ', 'e '],
['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']
]
board_dict = {(i,j):board[i][j] for i in range(-8,0) for j in range(0,8)}

def pieces(color, board):
  if color == 'w':
    return {(i,j):board[i][j] for i in range(-8,0) for j in range(0,8) if 'w' in board[i][j]}
  else:
    return {(i,j):board[i][j] for i in range(-8,0) for j in range(0,8) if 'b' in board[i][j]}
    
def print_board(color):
#prints the board based on perspective of current player (black or white)
  if color=='w':
    for r in range(8):
        for f in range(8):
            print(board[r][f], end=" ")
        print("")
  else:
    for r in range(-1,-9,-1):
      for f in range(7, -1, -1):
        print(board[r][f], end = ' ')
      print('')

def ConvertAlgtoTuple(move):
    r=-int(move[-1])
    f=files.index(move[-2])
    return (r,f)

def getposition(move,piece,color, board):
    '''
    move: str, the move made by the user (e.g. 'e4' or 'Bb5' or 'Nxc3')
    piece: str of len(1), indicating the piece moved
    color: 'b' or 'w'
    returns: tuple, position of the piece within board variable, calculated based on the move given
    '''
    square = ConvertAlgtoTuple(move)
    mover = color + piece
    if piece == 'N':
          pos_knight = []
          squares = [(r,f) for r in range(-8,0) for f in range(len(board)) if abs(r - square[0])==2 and abs(f - square[1])==1 or abs(r - square[0])==1 and abs(f - square[1])==2]
          for i in squares:
              if board[i[0]][i[1]] == mover:
                  pos_knight.append(i[0])
                  pos_knight.append(i[1])
                  break
          return pos_knight
    elif piece == 'P':
        pos_pawn = []
        if color == 'w':
          if 'x' in move:
            orig_rank = files.index(move[0])
            return [square[0] + 1, orig_rank]
          else:
            if square[0] == -4:
                for i in range(-3,-1):
                    if board[i][square[1]] == mover:
                        pos_pawn.append(i)
                        pos_pawn.append(square[1])
                        break
            else:
                for i in range(square[0],square[0]+2):
                    if board[i][square[1]]==mover:
                      pos_pawn.append(square[0] + 1)
                      pos_pawn.append(square[1])
        else:
            if 'x' in move:
              orig_rank = files.index(move[0])
              return [square[0]-1, orig_rank]
            else:
              if square[0] == -5:
                  for i in range(-7, -5):
                      if board[i][square[1]] == mover:
                          pos_pawn.append(i)
                          pos_pawn.append(square[1])
                          break
              else:
                  for i in range(square[0], square[0]-2, -1):
                    if board[i][square[1]]==mover:
                      pos_pawn.append(square[0] - 1)
                      pos_pawn.append(square[1])
        return pos_pawn
    elif piece == 'B':
          pos_bishop=[]
          s,d = square[0] + square[1], square[0] - square[1]
          squares = [(r,f) for r in range(-8,0) for f in range(len(board)) if r-f == d or r+f==s]
          for i in squares:
              if  board[i[0]][i[1]] == mover:
                  pos_bishop.append(i[0])
                  pos_bishop.append(i[1])
                  break
          return pos_bishop
    elif piece == 'R':
        squares = [(r,square[1]) for r in range(-8,0)] + [(square[0], f) for f in range(8)]
        pos_rook = []
        for i in squares:
          #same vertical line
          if board[i[0]][i[1]] == mover and board[i[0] + 1][i[1]]== mover:
              if abs(i[0]) < abs(square[0]):
                  pos_rook.append(i[0])
                  pos_rook.append(i[1])
              else:
                  pos_rook.append(i[0] + 1)
                  pos_rook.append(i[1])
              break
          #same horizontal
          elif i[1] < 7 and board[i[0]][i[1]] == mover and board[i[0]][i[1]+1]== mover:
              if i[1] < square[1]:
                  pos_rook.append(i[0])
                  pos_rook.append(i[1]+1)
              else:
                  pos_rook.append(i[0])
                  pos_rook.append(i[1])
              break
          elif board[i[0]][i[1]] == mover and isClearPath(square, (i[0],i[1])):
              pos_rook.append(i[0])
              pos_rook.append(i[1])
              break
        return pos_rook
    elif piece == 'Q':
        #should be reworked using pieces() function
        pos_queen = [[r,f] for r in range(-8,0) for f in range(0,8) if board[r][f]==mover][0]
        return pos_queen
    elif piece == 'K':
        #should be reworked using pieces() function
        pos_king = [(r,f) for r in range (-8,0) for f in range(0,8) if board[r][f] == mover][0]
        return pos_king

def getsquares(pos,piece,color, board, en_passant=False):
      '''
      pos : tuple, position of the moving piece
      piece : str of length 1, the piece being moved
      color : 'b' or 'w'
      board : current board configuration, list of lists
      en_passant : bool, whether an en passant capture is legal
      returns: list of tuples indicating all possible squares to which the piece can legally move
      '''
      if color == 'w':
          enem_color = 'b'
      else:
          enem_color = 'w'
      mover = color + piece
      squares2=[]
      if piece == 'N':
          squares = [(r,f) for r in range(-8,0) for f in range(len(board)) if abs(r - pos[0])==2 and abs(f - pos[1])==1 or abs(r - pos[0])==1 and abs(f - pos[1])==2]
          for i in squares:
              p = board[i[0]][i[1]]
              if p == 'e ' or enem_color in p:
                  squares2.append((i[0], i[1]))
          return squares2
      elif piece == 'P':
          if color == 'w':
              if pos[0] == -2 and board[-3][pos[1]] == 'e ':
                  squares2.append((-3, pos[1]))
                  if board[-4][pos[1]] == 'e ':
                    squares2.append((-4, pos[1]))
              elif pos[0] != -2 and board[pos[0] - 1][pos[1]] == 'e ':
                  squares2.append((pos[0] - 1, pos[1]))
              if pos[1] <7 and enem_color in board[pos[0] - 1][pos[1] + 1]:
                  squares2.append((pos[0] - 1, pos[1] +1))
              if pos[1]>0 and enem_color in board[pos[0] - 1][pos[1] - 1]:
                  squares2.append((pos[0]-1, pos[1] - 1))
              if en_passant:
                  if pos[1] > 0 and enem_color in board[pos[0]][pos[1] -1]:
                    squares2.append((pos[0]-1, pos[1] - 1))
                  if pos[1] < 7 and enem_color in board[pos[0]][pos[1] +1]:
                    squares2.append((pos[0]-1, pos[1]+1))
          if color == 'b':
              if pos[0] == -7 and board[-6][pos[1]] == 'e ':
                  squares2.append((-6, pos[1]))
                  if board[-5][pos[1]] == 'e ':
                    squares2.append((-5, pos[1]))
              elif pos[0] != -7 and board[pos[0] + 1][pos[1]] == 'e ':
                  squares2.append((pos[0] + 1, pos[1]))
              if pos[1] < 7 and enem_color in board[pos[0] + 1][pos[1] + 1]:
                  squares2.append((pos[0] + 1, pos[1] +1))
              if pos[1] > 0 and enem_color in board[pos[0] + 1][pos[1] - 1]:
                  squares2.append((pos[0] + 1, pos[1] - 1))
              if en_passant:
                  if enem_color in board[pos[0]][pos[1] -1]:
                    squares2.append((pos[0]+1, pos[1] - 1))
                  if enem_color in board[pos[0]][pos[1] +1]:
                    squares2.append((pos[0]+1, pos[1]+1))
          return squares2
      elif piece == 'B':
          squares2 = []
          j,k = pos[0], pos[1]
          #NW diagonal
          while j>-8 and k>0 and (board[j-1][k-1] == 'e ' or enem_color in board[j-1][k-1]):
              squares2.append((j-1,k-1))
              if enem_color in board[j-1][k-1]:
                  break
              j-=1
              k-=1
          j,k = pos[0], pos[1]
          #NE diagonal
          while j>-8 and k<7 and (board[j-1][k+1] == 'e ' or enem_color in board[j-1][k+1]):
              squares2.append((j-1,k+1))
              if enem_color in board[j-1][k+1]:
                  break
              j-=1
              k+=1
          j,k = pos[0], pos[1]
          #SW diagonal
          while j<-1 and k>0 and (board[j+1][k-1] == 'e ' or enem_color in board[j+1][k-1]):
              squares2.append((j+1,k-1))
              if enem_color in board[j+1][k-1]:
                  break
              j+=1
              k-=1
          j,k = pos[0], pos[1]
          #SE diagonal
          while j<-1 and k<7 and (board[j+1][k+1] == 'e ' or enem_color in board[j+1][k+1]):
              squares2.append((j+1,k+1))
              if enem_color in board[j+1][k+1]:
                  break
              j+=1
              k+=1
          return squares2
      elif piece == 'R':
          #squares2 will include all possible squares to which the found rook can go
          squares2 = []
          j,k = pos[0], pos[1]
          #horizontal - right
          while k<7 and (board[j][k+1]=='e ' or enem_color in board[j][k+1]):
              squares2.append((j,k+1))
              if enem_color in board[j][k+1]:
                  break
              k+=1
          #horizontal - left
          j,k = pos[0], pos[1]
          while k>0 and (board[j][k-1]=='e ' or enem_color in board[j][k-1]):
              squares2.append((j,k-1))
              if enem_color in board[j][k-1]:
                  break
              k-=1
          #vertical - up
          j,k = pos[0], pos[1]
          while j>-8 and (board[j-1][k]=='e ' or enem_color in board[j-1][k]):
              squares2.append((j-1,k))
              if enem_color in board[j-1][k]:
                  break
              j-=1
          #horizontal - down
          j,k = pos[0], pos[1]
          while j<-1 and (board[j+1][k]=='e ' or enem_color in board[j+1][k]):
              squares2.append((j+1,k))
              if enem_color in board[j+1][k]:
                 break 
              j+=1
          return squares2
      elif piece == 'Q':
          squares2 = []
          j,k = pos[0], pos[1]
          #horizontal - right
          while k<7 and (board[j][k+1]=='e ' or enem_color in board[j][k+1]):
              squares2.append((j,k+1))
              if enem_color in board[j][k+1]:
                  break
              k+=1
          #horizontal - left
          j,k = pos[0], pos[1]
          while k>0 and (board[j][k-1]=='e ' or enem_color in board[j][k-1]):
              squares2.append((j,k-1))
              if enem_color in board[j][k-1]:
                  break
              k-=1
          #vertical - up
          j,k = pos[0], pos[1]
          while j>-8 and (board[j-1][k]=='e ' or enem_color in board[j-1][k]):
              squares2.append((j-1,k))
              if enem_color in board[j-1][k]:
                  break
              j-=1
          #horizontal - down
          j,k = pos[0], pos[1]
          while j<-1 and (board[j+1][k]=='e ' or enem_color in board[j+1][k]):
              squares2.append((j+1,k))
              if enem_color in board[j+1][k]:
                 break 
              j+=1
          j,k = pos[0], pos[1]
          #NW diagonal
          while j>-8 and k>0 and (board[j-1][k-1] == 'e ' or enem_color in board[j-1][k-1]):
              squares2.append((j-1,k-1))
              if enem_color in board[j-1][k-1]:
                  break
              j-=1
              k-=1
          j,k = pos[0], pos[1]
          #NE diagonal
          while j>-8 and k<7 and (board[j-1][k+1] == 'e ' or enem_color in board[j-1][k+1]):
              squares2.append((j-1,k+1))
              if enem_color in board[j-1][k+1]:
                  break
              j-=1
              k+=1
          j,k = pos[0], pos[1]
          #SW diagonal
          while j<-1 and k>0 and (board[j+1][k-1] == 'e ' or enem_color in board[j+1][k-1]):
              squares2.append((j+1,k-1))
              if enem_color in board[j+1][k-1]:
                  break
              j+=1
              k-=1
          j,k = pos[0], pos[1]
          #SE diagonal
          while j<-1 and k<7 and (board[j+1][k+1] == 'e ' or enem_color in board[j+1][k+1]):
              squares2.append((j+1,k+1))
              if enem_color in board[j+1][k+1]:
                  break
              j+=1
              k+=1
      elif piece == 'K': 
          j,k = pos[0], pos[1]
          squares = [(r,f) for r in range (j-1, j+2) for f in range(k-1, k+2) if r in range(-8,0) if f in range(0,8)]
          for i in squares:
              if board[i[0]][i[1]] == 'e ' or enem_color in board[i[0]][i[1]]:
                  squares2.append((i[0], i[1]))
      return squares2

def isLegalMove(move, piece, color, board, en_passant):
    current = getposition(move,piece,color, board)
    if current==[]:
      return False
    squares = getsquares(current,piece,color, board, en_passant)
    move_tuple = ConvertAlgtoTuple(move)
    if move_tuple in squares:
        dummy = copy.deepcopy(board)
        dummy[move_tuple[0]][move_tuple[1]] =color+piece
        dummy[current[0]][current[1]]='e '
        if inCheck(color, dummy):
          print('King is in check!')
          return False
        return True
    else:
        return False

def inCheck(color, board, square=None):
    if color == 'w':
        #checking to see if white king is in check
        if square==None:
            for k,v in pieces('w', board).items():
                if v == 'wK':
                    pos_king = k
        else:
            pos_king = square
        for k,v in pieces('b', board).items():
            squares = getsquares(k, v[-1], 'b', board)
            if pos_king in squares:
                return True
    else:
        if square==None:
            for k,v in pieces('b', board).items():
                if v == 'bK':
                    pos_king = k
        else:
            pos_king = square
        for k,v in pieces('w', board).items():
            squares = getsquares(k, v[-1], 'w', board)
            if pos_king in squares:
                return True
        
    return False

def canCastle(color, move):
    if inCheck(color, board):
        return False
    
    if color == 'w' and wKing==0:
        if move == 'O-O' and wKR!=0:
            return False
        elif move == 'O-O-O' and wQR!=0:
            return False
        r = -1
        if 'K' in board[r][4]:
            if move == 'O-O':
                if isClearPath((r,4), (r,7)) and 'R' in board[r][7] and inCheck(color, board, (r,5))==False and inCheck(color, board, (r,6))==False:
                    return True
            elif move == 'O-O-O':
                if isClearPath((r,4), (r,0)) and 'R' in board[r][0] and inCheck(color, board, (r,3))==False and inCheck(color, board, (r,2))==False:
                    return True
    elif color == 'b' and bKing==0:
        if move == 'O-O' and bKR!=0:
            return False
        elif move == 'O-O-O' and bQR!=0:
            return False
        r = -8
        if 'K' in board[r][4]:
            if move == 'O-O':
                if isClearPath((r,4), (r,7)) and 'R' in board[r][7] and inCheck(color, board, (r,5))==False and inCheck(color, board, (r,6))==False:
                    return True
            elif move == 'O-O-O':
                if isClearPath((r,4), (r,0)) and 'R' in board[r][0] and inCheck(color, board, (r,3))==False and inCheck(color, board, (r,2))==False:
                    return True
    return False
        
def isClearPath(square1, square2):
    '''
    square1, square2 : tuples (rank, file)
    returns: bool, True if all squares between two pieces are empty, False otherwise
    preconditions: squares must be referentiable in the above board scheme
    '''
    r1,f1 = square1[0], square1[1]
    r2,f2 = square2[0], square2[1]
    #same horizontal line
    if r1 == r2:
        if f1 > f2:
            maxim, minim = f1, f2
        else:
            maxim, minim = f2, f1
        for i in range(minim+1, maxim):
            if board[r1][i] != 'e ':
                return False
        return True
    #same vertical line
    elif f1==f2:
        if r1 > r2:
            maxim, minim = r1, r2
        else:
            maxim, minim = r2, r1
        for i in range(minim+1, maxim):
            if board[i][f1] != 'e ':
                return False
        return True
    #same diagonal-NW/SE
    elif abs(r1-f1) == abs(r2-f2):
        if r1 > r2:
            minim_r = r1,r2
            maxim_f, minim_f = f1,f2
        else:
            minim_r = r2,r1
            maxim_f, minim_f = f2,f1
        for i in range(0, maxim_f - minim_f + 1):
            if board[minim_r + i + 1][minim_f + i + 1] != 'e ':
                return False
    #same diagonal-NE/SW
    elif abs(r1+f1) == abs(r2+f2):
        if r1 > r2:
            minim_r = r1,r2
            maxim_f, minim_f = f1,f2
        else:
            minim_r = r2,r1
            maxim_f, minim_f = f2,f1
        for i in range(0, maxim_f - minim_f + 1):
            if board[minim_r + i + 1][minim_f - i - 1] != 'e ':
                return False
        return True

def castle_kingside(color, board):
  '''
  color : str, 'w' or 'b'
  board : list of lists, board config
  returns : nothing, only alters board to effectuate castling action
  '''
  if color == 'w':
    r=-1
  else:
    r = -8
  board[r][6] = color + 'K'
  board[r][5] = color + 'R'
  board[r][4] = 'e '
  board[r][7] = 'e '

def castle_queenside(color, board):
  '''
  color : str, 'w' or 'b'
  board : list of lists, board config
  returns : nothing, only alters board to effectuate castling action
  '''
  if color == 'w':
    r = -1
  else:
    r = -8
  board[r][2] = color + 'K'
  board[r][3] = color + 'R'
  board[r][0] = 'e '
  board[r][4] = 'e '

def en_passant_possible(color, orig, moveTuple):
  if color == 'w':
    if moveTuple[0]==-4 and orig[0]==-2: 
      if moveTuple[1]!=7 and moveTuple[1]!=0 and (board[-4][moveTuple[1]+1]=='bP' or board[-4][moveTuple[1]-1]=='bP'):
        return True
      elif moveTuple[1]==7 and board[-4][moveTuple[1]-1]=='bP':
        return True
      elif moveTuple[1]==0 and board[-4][moveTuple[1]+1]=='bP':
        return True
      else:
        return False
    else:
      return False
  elif color == 'b':
    if moveTuple[0]==-5 and orig[0]==-7:
      if moveTuple[1]!=7 and moveTuple[1]!=0  and (board[-5][moveTuple[1]+1]=='wP' or board[-5][moveTuple[1]-1]=='wP'):
        return True
      elif moveTuple[1]==7 and board[-5][moveTuple[1]-1]=='wP':
        return True
      elif moveTuple[1]==0 and board[-5][moveTuple[1]+1]=='wP':
        return True
      else:
        return False
    else:
      return False

def checkmate():
  return False

def chess_game():
    count = 0
    en_passant=False
    prev_move, prev_piece=None,None
    global wQR
    global wKR
    global wKing
    global bQR
    global bKR
    global bKing
    while checkmate()==False:
        if count%2 ==0:
            color = 'w'
            enem_color = 'b'
        else:
            color = 'b'
            enem_color = 'w'
        print_board(color)
        move = str(input(colors[color] + ' to move: '))
        if move == 'O-O':
          if canCastle(color, 'O-O'):
            castle_kingside(color, board)
            if color == 'w':
              wKing=1
            elif color=='b':
              bKing=1
            count+=1
          else:
            print('Illegal move. Try again.')
            print('------------------------')
        elif move == 'O-O-O':
          if canCastle(color, 'O-O-O'):
            castle_queenside(color, board)
            if color == 'w':
              wKing=1
            elif color=='b':
              bKing=1
            count+=1
          else:
            print('Illegal move. Try again.')
            print('------------------------')
        else:
            moveTuple = ConvertAlgtoTuple(move)

            if move[0] in files:
                piece = 'P'
            else:
                piece = move[0]
            
            if isLegalMove(move, piece, color, board, en_passant):

                if piece == 'R':
                  if getposition(move, piece, color, board)[1]==7:
                    if color == 'w':
                      wKR = 1
                    elif color == 'b':
                      bKR = 1
                  elif getposition(move, piece, color, board)[1]==0:
                    if color == 'w':
                      wQR = 1
                    elif color == 'b':
                      bQR = 1
                elif piece=='K':
                  if color=='w':
                    wKing=1
                  else:
                    bKing=1

                if len(move)>3 and move[1]!='x':
                    if move[1] in files:
                      pos = files.index(move[1])
                    elif move[1] in ranks:
                      pos = -int(move[1])
                    for k,v in pieces(color, board).items():
                      if k[1]==pos and piece in v:
                        orig = k
                        break
                      elif k[0]==pos and piece in v:
                        orig = k
                        break
                else:
                  orig = getposition(move, piece, color, board)

                board[orig[0]][orig[1]] = 'e '
                board[moveTuple[0]][moveTuple[1]] = color+piece
                
                if en_passant and prev_piece == 'P':
                    if color=='w':
                      if 'x' in move and moveTuple[0]==-6:
                          if prev_move==(-5, moveTuple[1]):
                            board[-5][moveTuple[1]]='e '
                          elif prev_move==(-5, moveTuple[1]-1):
                            board[-5][moveTuple[1]]='e '
                    else:
                      if 'x' in move and moveTuple[0]==-3:
                          if prev_move==(-4, moveTuple[1]):
                            board[-4][moveTuple[1]]='e '
                          elif prev_move==(-4, moveTuple[1]):
                            board[-4][moveTuple[1]]='e '

                if piece=='P':
                  en_passant = en_passant_possible(color, orig, moveTuple)

                count+=1
                prev_move, prev_piece = moveTuple, piece
                if inCheck(enem_color, board):
                  print(colors[enem_color] + ' King is in check!')
            
            else:
              print('Illegal move. Try again.')
              print('------------------------')

chess_game()



