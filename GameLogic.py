class GameLogic:

    def __init__(self, player=2):
        self.board = [['1',  '2',  '3'],
                    ['4',  '5',  '6'],
                    ['7',  '8',  '9']]
        self.numPlays = 0
        self.player = player
        self.winner = False

    def currentBoard(self):
        print "\n\n " + self.board[0][0] + " | " + self.board[0][1] + " | " + self.board[0][2] + " " + "\n---+---+---\n " + \
        self.board[1][0] + " | " + self.board[1][1] + " | " + self.board[1][2] + " " + "\n---+---+---\n " + self.board[2][0] + \
        " | " + self.board[2][1] + " | " + self.board[2][2] + " \n"
        return

    def changePlayer(self, player):
        self.player = player
        
    # play( --play / 3, play % 3, player)
    def play(self, row, column, player):
        if not (row >= 0 and row < 3 and column >= 0 and column < 3):
            print "here"
            return False
        if self.board[row][column] > '9':
            return False

        if self.numPlays == 9:
            return False

        # Insert player Symbol
        if player == 1:
            self.board[row][column] = 'X'
        else:
            self.board[row][column] = 'O'

        self.numPlays += 1
        return True

    def checkWinner(self):
        i = 0
        if (self.board[0][0] == self.board[1][1] & self.board[0][0] == self.board[2][2]) | (self.board[0][2] == self.board[1][1] & self.board[0][2] == self.board[2][0]):
            if self.board[1][1] == 'X':
                return 1 # Player 1 wins
            else:
                return 0 # Player 2 wins
        else:
            for i in range(0, 2):
                if (self.board[i][0] == self.board[i][1] & self.board[i][0] == self.board[i][2]):
                    if self.board[i][0] == 'X':
                        return 1
                    else:
                        return 0

                if (self.board[0][i] == self.board[1][i] & self.board[0][i] == self.board[2][i]):
                    if self.board[0][i] == 'X':
                        return 1
                    else:
                        return 0

        if self.numPlays == 9:
            return 2 # Empate
        else:
            return -1

    """def readPlay():
        play = 0
        position = 'X'
        if self.player == 1:
            position = 'X'
        else:
            position = 'O'
        while True:
            print "\n Player " + str(self.player) + ", please enter the number of the square " +\
            "where you want to place your " + position
            play = sys.stdin.readline()
            if play > 9 or play < 0:
                break
            return play
"""
