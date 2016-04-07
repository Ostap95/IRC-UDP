class GameLogic:

    def __init__(self):
        self.board = [(  '1',  '2',  '3'),
                    (  '4',  '4',  '5'),
                    (  '7',  '8',  '9')]
        self.nextPlayer = 0
        self.numPlays = 0

    def currentBoard(self):
        print "\n\n " + self.board[0][0] + " | " + self.board[0][1] + " | " + self.board[0][2] + " " + "\n---+---+---\n " + \
        self.board[1][0] + " | " + self.board[1][1] + " | " + self.board[1][2] + " " + "\n---+---+---\n " + self.board[2][0] + \
        " | " + self.board[2][1] + " | " + self.board[2][2] + " \n"

        return

    def play(self, row, column, player):
        if not (row >= 0 & row < 3 & column >= 0 & column < 3):
            return False
        if self.board[row][column] > '9':
            return False
        if player != nextPlayer:
            return False

        if self.numPlays == 9:
            return False

        # Insert player Symbol
        if player == 0:
            self.board[row][column] = 'X'
        else:
            self.board[row][column] = 'O'

        nextPlayer = (nextPlayer + 1)%2
        self.numPlays += 1
        return True

    def checkWinner(self):
        i = 0
        if (self.board[0][0] == self.board[1][1] & self.board[0][0] == self.board[2][2]) | (self.board[0][2] == self.board[1][1] & self.board[0][2] == self.board[2][0]):
            if self.board[1][1] == 'X':
                return 1
            else:
                return 0
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
            return 2
        else:
            return -1
