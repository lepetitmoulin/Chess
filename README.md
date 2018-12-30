# Chess
This program implements a very simple chess program, designed as a base to develop further tools for chess study. I have made
every effort to optimize the visual representation of the board as moves are made, and while the representations of the pieces
and the empty squares remains stubbornly suboptimal, it does (or will) provide the necessary functionality required to play
through a game.

For the time being, the program asks for user inputs that are constrained in a variety of ways. The program insists on algebraic
notation for moves, so a familiarity with algebraic chess notation is a prerequisite for playing the game with any enjoyment.
Otherwise, errors will abound.

Algebraic notation primer:

'Files' are denoted by lowercase letters [a-h] (e.g. 'the a-file' or 'the d-file') and 'ranks' are denotes by numeric characters
[1-8] (e.g. 'the 8th rank' or 'the 3rd rank').

Piece abbreviations are as follows:
Rook = 'R'
Knight = 'N'
Bishop = 'B'
Queen = 'Q'
King = 'K'

Pawns (and pawn moves) are denoted by a lowercase letter [a-h] as the first character of a move. If no capture is intended,
one simply uses the notation '[lowercase letter[a-h]][numeric 1-8]', the first indicating both the origin and destination file,
and the second indicating the destination rank. For example, 'e4' would indicate moving the pawn that is already in the e-file
to the fourth rank of the e-file.

All non-capture moves are performed in the same fashion, with the destination square indicated by the last two characters of 
the move, and the first character of the move indicating the piece. For example, 'Rh3' would move the rook to the 3rd rank
of the f-file (square h3).

Difficulties do arise, however, with rooks and knights, as each side is given two of these pieces, and it can arrive that both
of these pieces of each side can occupy the same square. In the case of KNIGHTS, one most commonly uses the following structure:
    
    'N[origin file][destination file][destination rank]' (e.g. 'Nbd7')

In the rare event that both of one's knights occupy the same file, the rather logical alternative is used:

    'N[origin rank][destination file][destination rank]' (e.g. 'N3e4')
  
A parallel structure is used to resolve collisions between rooks. If two rooks occupying the same RANK, who could both legally
go to a given destination square, follows the convention:

    'R[origin file][destination file][destination rank]' (e.g. 'Rad3')

And if occupying the same file:

    'R[origin rank][destination file][destination rank]' (e.g. 'R1d3')
    
Captures are effected by adding an 'x' before the destination square. (e.g. 'Nxd4' (knight takes on d4), 'gxf3' (pawn takes on
g3), etc.)

Castling is performed kingside by entering 'O-O', and queenside by entering 'O-O-O'. If the King has already moved, castling is
not available either side. If the kingside rook has moved, kingside castling is not legal; if the queenside rook has moved,
queenside castling is not legal.

En passant functionality is enabled, though perhaps shakily. The basic idea is that, if your opponent has advanced a pawn into 
the first rank of your camp (the fourth rank, if you are white; the fifth rank, if you are black) and you advance a pawn to
a horizontally adjacent square to that enemy pawn, that enemy pawn has the option of capturing the pawn that you just advanced, 
occupying then the square behind that pawn you just advanced. This option expires if not used after the initial pawn move. For 
example, say that I am black and I have advanced a pawn to the d4 square, and your e-pawn remains on its starting position. You 
boldly strike out with the move e4, putting your pawn horizontally adjacent to my pawn. My pawn would then have the right to 
capture the pawn you just advanced to e4, planting itself then on e3. This move would be effected by entering 'dxe3'. If I 
decide that it is not in my best interest to take your measly pawn, I forfeit the right to capture with en passant.

As of 29 December 2018, there is no functionality for offering draws, nor for pawn promotion. Theses function will be implemented soon.

Theoretical draws will also need to be accounted for (e.g. instances of king+knight vs. king, king+bishop vs. king, king vs. king), as well as draws by repetition (if players repeat the same moves three times each, a draw is claimed).
