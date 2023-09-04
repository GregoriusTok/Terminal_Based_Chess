from time import sleep
from stockfish import Stockfish
stockfish = Stockfish(path = r"C:\Users\aakas\Downloads\stockfish-windows-x86-64-modern\stockfish\stockfish-windows-x86-64-modern.exe", depth = 10, parameters={"Threads":2, "UCI_LimitStrength":True, "UCI_Elo":10})

#Chess 

def translator(move):
    move = list(move)
    # print(move)
    n = 0
    for i in move:
        if i.isnumeric():
            move[n] = 8 - int(i)
        else:
            if i == "a":
                move[n] = 0
            elif i == "b":
                move[n] = 1
            elif i == "c":
                move[n] = 2
            elif i == "d":
                move[n] = 3
            elif i == "e":
                move[n] = 4
            elif i == "f":
                move[n] = 5
            elif i == "g":
                move[n] = 6
            elif i == "h":
                move[n] = 7
        n += 1
    return move

Board = [
    ["BR", "BN", "BB", "BQ", "BK", "BB", "BN", "BR"], 
    ["BP", "BP", "BP", "BP", "BP", "BP", "BP", "BP"], 
    ["--", "--", "--", "--", "--", "--", "--", "--"], 
    ["--", "--", "--", "--", "--", "--", "--", "--"], 
    ["--", "--", "--", "--", "--", "--", "--", "--"], 
    ["--", "--", "--", "--", "--", "--", "--", "--"], 
    ["WP", "WP", "WP", "WP", "WP", "WP", "WP", "WP"], 
    ["WR", "WN", "WB","WQ", "WK", "WB", "WN", "WR"]]

# BoardCopy = Board

MoveList = []
PieceList = []

#If returns false then it breaks a rule
def PawnRules(move, WTurn, origin, destination, board = Board):
    '''
    Can't go back
    - if num2 is less than num1 then its going back
    Promotion (Has to be outside of func)
    - if num2 == 8 or 1 then turn P -> Q
    Can only move one forward
    - if |num2-num1| > 1 then its bad
    Can't go horizontal
    - if letter is diff but num is same then bad
    Can only go diagonal if enemy is there
    - if letter differs by 1 and number differs by 1 then check if enemy is destination
    '''
    if move[3] > move[1] and WTurn:
        print("Pawns can't go backwards")
        return False
    elif move[1] > move[3] and not WTurn:
        print("Pawns can't go backwards")
        return False

    if move[0] != move[2] and move[1] == move[3]:
        print("Pawns can't move horizontal")
        return False

    if move[1] == 6 and WTurn or move[1] == 1 and not WTurn:
        if abs(move[3] - move[1]) > 2:
            print("Pawns can only move one or two squares")
            return False
    else:
        if abs(move[3] - move[1]) != 1:
            print("Pawns can only move one square")
            return False
    
    if abs(move[0] - move[2]) == 1 and abs(move[3] - move[1]) == 1:
        # print(abs(move[0] - move[2]))
        if destination[0] == "B" and WTurn:
            pass
        elif destination[0] == "W" and not WTurn:
            pass
        elif destination[0] != "B" and WTurn:
            print("The pawn can't take that spot")
            return False
        elif destination[0] != "W" and not WTurn:
            print("The pawn can't take that spot")
            return False
    elif abs(move[0] - move[2]) != 0:
        print("Pawns can't move like that")
        return False
    
    if destination[0] != "-" and move[0] == move[2]:
        print("Can't go to that square")
        return False

    return True

def RookRules(move, WTurn, origin, destination, board = Board):
    '''
    Only in straight lines
    - Check if let same and num diff or vice versa
    Can only take enemy
    - Check if destination is enemy
    '''
    if move[0] != move[2] and move[1] == move[3]:
        pass
    elif move[0] == move[2] and move[1] != move[3]:
        pass
    elif move[0] != move[2] and move[1] != move[3]:
        print("Rooks can only move in straight lines")
        return False

    if move[1] == move[3]:
        # print("Hori")
        if move[0] < move[2]:
            i = move[0] + 1
            o = move[2]
        else:
            i = move[2] + 1
            o = move[0]
        while i < o:
            d = Board[move[1]][i]
            # print(d)
            if d != "--":
                print("Rooks can't jump over other pieces")
                return False
            i += 1
    elif move[0] == move[2]:
        # print("Vert")
        if move[1] < move[3]:
            i = move[1] + 1
            o = move[3]
        else:
            i = move[3] + 1
            o = move[1]
        while i < o:
            d = Board[i][move[0]]
            # print(d)
            if d != "--":
                print("Rooks can't jump over other pieces")
                return False
            i += 1

    if destination[0] != origin[0]:
        pass
    else:
        print("You can't take that piece")
        return False

    return True

def BishopRules(move, WTurn, origin, destination, board = Board):
    '''
    Only in diagonal lines
    - if let1 - let2 == num1 num2
    Can only take enemy
    - Check if destination is enemy
    '''
    if abs(move[0] - move[2]) == abs(move[1] - move[3]):
        pass
    elif abs(move[0] - move[2]) != abs(move[1] - move[3]):
        print("Bishops can only move in diagonals")
        return False

    if move[0] > move[2] and move[1] > move[3]:
        i = move[0] - 1
        o = move[1] - 1
        while i > move[2]:
            d = board[o][i]
            if d != "--":
                print("Bishops can't jump over other pieces")
                return False
            i-=1
            o-=1
    elif move[0] < move[2] and move[1] < move[3]:
        i = move[0] + 1
        o = move[1] + 1
        while i < move[2]:
            d = board[o][i]
            if d != "--":
                print("Bishops can't jump over other pieces")
                return False
            i+=1
            o+=1
    elif move[0] < move[2] and move[1] > move[3]:
        i = move[0] + 1
        o = move[1] - 1
        while i < move[2]:
            d = board[o][i]
            if d != "--":
                print("Bishops can't jump over other pieces")
                return False
            i+=1
            o-=1
    elif move[0] > move[2] and move[1] < move[3]:
        i = move[0] - 1
        o = move[1] + 1
        while i > move[2]:
            d = board[o][i]
            if d != "--":
                print("Bishops can't jump over other pieces")
                return False
            i-=1
            o+=1

    if destination[0] != origin[0]:
        pass
    else:
        print("You can't take that piece")
        return False

    return True

def QueenRules(move, WTurn, origin, destination, board = Board):
    '''
    Can only move in straights or diagonal
    - Combine Bishop and Rook
    Can only take enemy
    - Check if origin colour is diff from destination
    '''
    if abs(move[0] - move[2]) == abs(move[1] - move[3]):
        pass
    elif move[0] == move[2] and move[1] != move[3]:
        pass
    elif move[0] != move[2] and move[1] == move[3]:
        pass
    else:
        print("The Queen can only move diagonally or in straight lines")

    if move[1] == move[3]:
        # print("Hori")
        if move[0] < move[2]:
            i = move[0] + 1
            o = move[2]
        else:
            i = move[2] + 1
            o = move[0]
        while i < o:
            d = Board[move[1]][i]
            # print(d)
            if d != "--":
                print("The Queen can't jump over other pieces")
                return False
            i += 1
    elif move[0] == move[2]:
        # print("Vert")
        if move[1] < move[3]:
            i = move[1] + 1
            o = move[3]
        else:
            i = move[3] + 1
            o = move[1]
        while i < o:
            d = Board[i][move[0]]
            # print(d)
            if d != "--":
                print("The Queen can't jump over other pieces")
                return False
            i += 1
    elif move[0] > move[2] and move[1] > move[3]:
        i = move[0] - 1
        o = move[1] - 1
        while i > move[2]:
            d = board[o][i]
            if d != "--":
                print("The Queen can't jump over other pieces")
                return False
            i-=1
            o-=1
    elif move[0] < move[2] and move[1] < move[3]:
        i = move[0] + 1
        o = move[1] + 1
        while i < move[2]:
            d = board[o][i]
            if d != "--":
                print("The Queen can't jump over other pieces")
                return False
            i+=1
            o+=1
    elif move[0] < move[2] and move[1] > move[3]:
        i = move[0] + 1
        o = move[1] - 1
        while i < move[2]:
            d = board[o][i]
            if d != "--":
                print("The Queen can't jump over other pieces")
                return False
            i+=1
            o-=1
    elif move[0] > move[2] and move[1] < move[3]:
        i = move[0] - 1
        o = move[1] + 1
        while i > move[2]:
            d = board[o][i]
            if d != "--":
                print("The Queen can't jump over other pieces")
                return False
            i-=1
            o+=1

    if destination[0] != origin[0]:
        pass
    else:
        print("You can't take that piece")
        return False

    return True

def KnightRules(move, WTurn, origin, destination, board = Board):
    '''
    Moves in L
    - Check if diff in 1 dir is 1 and diff in other is 2
    Can only take enemy
    - Check if origin is diff from destination
    '''
    if abs(move[0] - move[2]) == 1 and abs(move[1] - move[3]) == 2:
        pass
    elif abs(move[0] - move[2]) == 2 and abs(move[1] - move[3]) == 1:
        pass
    else:
        print("Knights can't move like that")
        return False

    if origin[0] != destination[0]:
        pass
    else:
        print("You can't take that")
        return False

    return True

def KingRules(move, WTurn, origin, destination, board = Board):
    '''
    Can only move one square
    - Check if both abs diffs are less than 2
    Can only take enemy
    - Origin diff from dest
    Castle
    - Check if things were empty
    - Has to happen outside of func
    '''
    if abs(move[0] - move[2]) < 2 and abs(move[1] - move[3]) < 2:
        pass
    else:
        print("The King can't move like that")
        return False
    
    if origin[0] != destination[0]:
        pass
    else:
        print("You can not take that")
        return False

    return True

#Check Test
def CheckTest(WTurn, board = Board):
    #Find Kings
    kingnum = 0
    kinglet = 0
    for i in board:    
        try:
            if WTurn:
                kinglet = i.index("WK")
                break
            else:
                kinglet = i.index("BK")
                break
        except:
            kingnum += 1
            continue
    
    #Check straights
    #Down
    i = kingnum + 1
    while i < 8:
        p = board[i][kingnum]
        if p != "--":
            if WTurn:
                if p == "BR" or p == "BQ":
                    # print("1HI")
                    return True
                else:
                    break
            else:
                if p == "WR" or p == "WQ":
                    # print("2HI")
                    return True
                else:
                    break
        i += 1
    #Up
    i = kingnum - 1
    while i >= 0:
        p = board[i][kinglet]
        if p != "--":
            if WTurn:
                if p == "BR" or p == "BQ":
                    # print("3HI")
                    return True
                else:
                    break
            else:
                if p == "WR" or  p == "WQ":
                    # print("4HI")
                    return True
                else:
                    break                
        i -= 1
    #Right
    i = kinglet + 1
    while i < 8:
        p = board[kingnum][i]
        if p != "--":
            if WTurn:
                if p == "BR" or p == "BQ":
                    # print("5HI")
                    return True
                else:
                    break
            else:
                if p == "WR" or p == "WQ":
                    # print("6HI")
                    return True
                else:
                    break
        i += 1
    #Left
    i = kinglet - 1
    while i >= 0:
        p = board[i][kingnum]
        if p != "--":
            if WTurn:
                if p == "BR" or p == "BQ":
                    # print("7HI")
                    return True
                else:
                    break
            else:
                if p == "WR" or p == "WQ":
                    # print("8HI")
                    return True
                else:
                    break
        i -= 1

    #Check diagonals
    #Bottom Right
    i = kingnum + 1
    o = kinglet + 1
    while i < 8 and o < 8:
        p = board[i][o]
        if p != "--":
            if WTurn:
                if p == "BB" or p == "BQ":
                    return True
                else:
                    break
            else:
                if p == "WB" or p == "WQ":
                    return True
                else:
                    break
        i += 1
        o += 1
    #Top Left
    i = kingnum - 1
    o = kinglet - 1
    while i >= 0 and o >= 0:
        p = board[i][o]
        if p != "--":
            if WTurn:
                if p == "BB" or p == "BQ":
                    return True
                else:
                    break
            else:
                if p == "WB" or p == "WQ":
                    return True
                else:
                    break
        i -= 1
        o -= 1
    #Bottom Left
    i = kingnum + 1
    o = kinglet - 1
    while i > 8 and o >= 0:
        p = board[i][o]
        if p != "--":
            if WTurn:
                if p == "BB" or p == "BQ":
                    return True
                else:
                    break
            else:
                if p == "WB" or p == "WQ":
                    return True
                else:
                    break
        i += 1
        o -= 1
    #Top Right
    i = kingnum - 1
    o = kinglet + 1
    while i >= 0 and o > 8:
        p = board[i][o]
        if p != "--":
            if WTurn:
                if p == "BB" or p == "BQ":
                    return True
                else:
                    break
            else:
                if p == "WB" or p == "WQ":
                    return True
                else:
                    break
        i -= 1
        o += 1

    #Knights?
    if kingnum >= 2 and kinglet >= 1: #1
        if WTurn and board[kingnum - 2][kinglet - 1] == "BN":
            return True
        elif not WTurn and board[kingnum - 2][kinglet - 1] == "WN":
            return True
    if kingnum >= 2 and kinglet <= 6: #2
        if WTurn and board[kingnum - 2][kinglet + 1] == "BN":
            return True
        elif not WTurn and board[kingnum - 2][kinglet + 1] == "WN":
            return True
    if kingnum >= 1 and kinglet <=5: #3
        if WTurn and board[kingnum - 1][kinglet + 2] == "BN":
            return True
        elif not WTurn and board[kingnum - 1][kinglet + 2] == "WN":
            return True
    if kingnum <= 6 and kinglet <=5: #4
        if WTurn and board[kingnum + 1][kinglet + 2] == "BN":
            return True
        elif not WTurn and board[kingnum + 1][kinglet + 2] == "WN":
            return True
    if kingnum <= 5 and kinglet <= 6: #5
        if WTurn and board[kingnum + 2][kinglet + 1] == "BN":
            return True
        elif not WTurn and board[kingnum + 2][kinglet + 1] == "WN":
            return True
    if kingnum <= 5 and kinglet >= 1: #6
        if WTurn and board[kingnum + 2][kinglet - 1] == "BN":
            return True
        elif not WTurn and board[kingnum + 2][kinglet - 1] == "WN":
            return True
    if kingnum <= 6 and kinglet >= 2: #7
        if WTurn and board[kingnum + 1][kinglet - 2] == "BN":
            return True
        elif not WTurn and board[kingnum + 1][kinglet - 2] == "WN":
            return True
    if kingnum >= 1 and kinglet >= 2: #8
        if WTurn and board[kingnum - 1][kinglet - 2] == "BN":
            return True
        elif not WTurn and board[kingnum - 1][kinglet - 2] == "WN":
            return True

    return False
    
#Engine
def EngineCheck(movelist):
    # print(MoveList)
    stockfish.set_position(movelist)
    move = stockfish.get_best_move()

    return move

def Game(oneplayer):

    WTurn = True
    running = True
    IsCheck = False
    MoveList = []

    while running:
        emove = EngineCheck(MoveList)
        print()
        if not WTurn and oneplayer:
            print(emove)
        else:
            for i in Board:
                print(*i)

        while True:
            if CheckTest(WTurn):
                print("CHECK")
                IsCheck = True

            if WTurn == True:
                move = input("White move: ")
            else:
                if oneplayer:
                    move = emove
                else:
                    move = input("Black move: ")
                

            if move != "o-o" and move != "o-o-o":
                MoveList.append(move)
            elif move == "o-o":
                if WTurn:
                    MoveList.append("e1g1")
                else:
                    MoveList.append("e8g8")
            elif move == "o-o-o":
                if WTurn:
                    MoveList.append("e1c1")
                else:
                    MoveList.append("e8c8")

            if move == "STOP":
                running = False
                break
            elif move == "o-o":
                if WTurn:
                    Board[7][4] = "--"
                    Board[7][5] = "WR"
                    Board[7][6] = "WK"
                    Board[7][7] = "--"
                    break
                else:
                    Board[0][4] = "--"
                    Board[0][5] = "BR"
                    Board[0][6] = "BK"
                    Board[0][7] = "--"
                    break
            elif move == "o-o-o":
                if WTurn:
                    Board[7][0] = "--"
                    Board[7][1] = "--"
                    Board[7][2] = "WK"
                    Board[7][3] = "WR"
                    Board[7][4] = "--"
                    break
                else:
                    Board[0][0] = "--"
                    Board[0][1] = "--"
                    Board[0][2] = "BK"
                    Board[0][3] = "BR"
                    Board[0][4] = "--"
                    break
            else:
                move = translator(move)
                # print(move)
                origin = list(Board[move[1]][move[0]])
                destination = list(Board[move[3]][move[2]])

            if move[0] == move[2] and move[1] == move[3]:
                print("Same position")
                MoveList.pop()
                continue

            if Board[move[1]][move[0]] == '--':
                print("No piece selected")
                MoveList.pop()
                continue

            if WTurn and origin[0] != "W":
                print("Not you're piece.")
                MoveList.pop()
                continue
            elif not WTurn and origin[0] == "W":
                print("Not you're piece.")
                MoveList.pop()
                continue

            if origin[1] == "P":
                if not PawnRules(move, WTurn, origin, destination):
                    if destination[0] != "-":
                        MoveList.pop()
                        continue
                    else:
                        MoveList.pop()
                        continue
                elif move[3] == 0 or move[3] == 7: #Promotion
                    while True:
                        PromotionPiece = input("What piece would you like to promote to? ").upper()
                        if PromotionPiece == "KNIGHT" or PromotionPiece == "HORSE":
                            origin[1] =  "K"
                        elif PromotionPiece == "ROOK":
                            origin[1] =  "R"
                        elif PromotionPiece == "BISHOP":
                            origin[1] =  "B"
                        elif PromotionPiece == "QUEEN":
                            origin[1] =  "Q"
                        else:
                            print("Not a valid piece name")
                            continue
                        break
            elif origin[1] == "R":
                if not RookRules(move, WTurn, origin, destination):
                    MoveList.pop()
                    continue
            elif origin[1] == "B":
                if not BishopRules(move, WTurn, origin, destination):
                    MoveList.pop()
                    continue
            elif origin[1] == "Q":
                if not QueenRules(move, WTurn, origin, destination):
                    MoveList.pop()
                    continue
            elif origin[1] == "N":
                if not KnightRules(move, WTurn, origin, destination):
                    MoveList.pop()
                    continue
            elif origin[1] == "K":
                if not KingRules(move, WTurn, origin, destination):
                    MoveList.pop()
                    continue

            Board[move[1]][move[0]] = "".join(origin)

            break

        if not running:
            break
        
        # if WTurn:
        #     bestmove = EngineCheck(MoveList)
        #     print(bestmove)

        if WTurn:
            if CheckTest(WTurn):
                print("White has lost")
                running = False
            WTurn = False
        else:
            if CheckTest(WTurn):
                print("Black has lost")
                running = False
            WTurn = True
        if move != "o-o" and move != "o-o-o":
            Board[move[3]][move[2]] = Board[move[1]][move[0]]
            Board[move[1]][move[0]] = "--"

oneplayer = True
while True:
    a = input("One Player Mode? Y/N: ").upper()
    if a == "Y":
        oneplayer = True
    else:
        oneplayer = False

    Game(oneplayer)

    a = input("Again? Y/N: ").upper()
    if a == "Y":
        continue
    else:
        break
