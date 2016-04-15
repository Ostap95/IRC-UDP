class GameLogic:

    def __init__(self, player=1):
        self.board = [[' ',  ' ',  ' '],
                    [' ',  ' ',  ' '],
                    [' ',  ' ',  ' ']]
        self.numPlays = 0
        self.mainPlayer = False
        self.permission = True
        self.winner = False

    """ Prints the current board"""
    def currentBoard(self):
        print "\n\n " + self.board[0][0] + " | " + self.board[0][1] + " | " + self.board[0][2] + " " + "\n---+---+---\n " + \
        self.board[1][0] + " | " + self.board[1][1] + " | " + self.board[1][2] + " " + "\n---+---+---\n " + self.board[2][0] + \
        " | " + self.board[2][1] + " | " + self.board[2][2] + " \n"
        return

    """ Changes between main and second player """
    def changePlayer(self, value):
        self.mainPlayer = value

    def changePermission(self, value):
        self.permission = value

    def getPermission(self):
        return self.permission
    # play( --play / 3, play % 3)
    """ Function used to make a play on the board """
    def play(self, row, column):
        if not (row >= 0 and row < 3 and column >= 0 and column < 3):
            return False

        if self.board[row][column] != ' ':
            print "Invalid play"
            return

        if self.numPlays == 9:
            return False

        # Insert player Symbol

        if not self.mainPlayer:
            self.board[row][column] = 'X'
        else:
            self.board[row][column] = 'O'
        self.numPlays += 1
        return True


    """ Updates the board based on the play made by the other player """
    def receivePlay(self, row, column):
        if not (row >= 0 and row < 3 and column >= 0 and column < 3):
            return False

        if self.numPlays == 9:
            return False

        # Insert player Symbol

        if  self.mainPlayer:
            self.board[row][column] = 'X'
        else:
            self.board[row][column] = 'O'
        self.numPlays += 1
        return True

    def checkWinner(self):
        i = 0
        if (self.board[0][0] == self.board[1][1] and self.board[0][0] == self.board[2][2] and self.board[0][0] != ' ') or  +\
        (self.board[0][2] == self.board[1][1] and self.board[0][2] == self.board[2][0] and self.board[0][2] != ' '):
            if self.board[1][1] == 'X':
                return 1 # Player 1 wins
            else:
                return 0 # Player 2 wins
        else:
            for i in range(0, 2):
                if (self.board[i][0] == self.board[i][1] and self.board[i][0] == self.board[i][2] and self.board[i][0] != ' '):
                    if self.board[i][0] == 'X':
                        return 1
                    else:
                        return 0

                if (self.board[0][i] == self.board[1][i] and self.board[0][i] == self.board[2][i] and self.board[0][i] != ' '):
                    if self.board[0][i] == 'X':
                        return 1
                    else:
                        return 0

        if self.numPlays == 9:
            return 2 # Empate
        else:
            return -1



    def resetGame(self):
         self.board = [[' ',  ' ',  ' '],
                     [' ',  ' ',  ' '],
                     [' ',  ' ',  ' ']]
         self.numPlays = 0
         self.mainPlayer = False
         self.permission = True
         self.winner = False
