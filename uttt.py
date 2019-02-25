from time import sleep
from math import inf
from random import randint

class ultimateTicTacToe:
    def __init__(self):
        """
        Initialization of the game.
        """
        self.board=[['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_']]
        self.maxPlayer='X'
        self.minPlayer='O'
        self.maxDepth=3
        self.bestMove = (-1, -1)
        #The start indexes of each local board
        self.globalIdx=[(0,0),(3,0),(6,0),(0,3),(3,3),(6,3),(0,6),(3,6),(6,6)]

        #Start local board index for reflex agent playing
        self.startBoardIdx=4
        #self.startBoardIdx=randint(0,8)

        #utility value for reflex offensive and reflex defensive agents
        self.winnerMaxUtility=10000
        self.twoInARowMaxUtility=500
        self.preventThreeInARowMaxUtility=100
        self.cornerMaxUtility=30

        self.winnerMinUtility=-10000
        self.twoInARowMinUtility=-100
        self.preventThreeInARowMinUtility=-500
        self.cornerMinUtility=-30

        self.expandedNodes=[]
        self.currExpandedNodes=0
        self.currPlayer=True
        self.twos = False

    def printGameBoard(self):
        """
        This function prints the current game board.
        """
        print('\n'.join([' '.join([str(cell) for cell in row]) for row in self.board[:3]])+'\n')
        print('\n'.join([' '.join([str(cell) for cell in row]) for row in self.board[3:6]])+'\n')
        print('\n'.join([' '.join([str(cell) for cell in row]) for row in self.board[6:9]])+'\n')


    def evaluatePredifined(self, isMax):
        """
        This function implements the evaluation function for ultimate tic tac toe for predifined agent.
        input args:
        isMax(bool): boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        score(float): estimated utility score for maxPlayer or minPlayer
        """
        #YOUR CODE HERE
        """
        3 types of victory: row, column, diagonal
        1. check for 3 in a row victory (|10000|)
        2. check for 2 in a row w/out 3rd spot taken (|500| for each, |100| if spot taken)
        3. check for corner squares taken (|30| for each)
        """
        score=0
        # cover max player first
        if isMax:
            if self.evaluateLocalBoardPredefined(0, 0, 'X') == 10000 or self.evaluateLocalBoardPredefined(3, 0, 'X') == 10000 or self.evaluateLocalBoardPredefined(6, 0, 'X') == 10000 or self.evaluateLocalBoardPredefined(0, 3, 'X') == 10000 or self.evaluateLocalBoardPredefined(3, 3, 'X') == 10000 or self.evaluateLocalBoardPredefined(6, 3, 'X') == 10000 or self.evaluateLocalBoardPredefined(0, 6, 'X') == 10000 or self.evaluateLocalBoardPredefined(3, 6, 'X') == 10000 or self.evaluateLocalBoardPredefined(6, 6, 'X') == 10000:
               self.twos = False
               return 10000
            else:
                if self.twos:
                    if self.evaluateLocalBoardPredefined(0, 0, 'X') % 100 == 0:
                        score += self.evaluateLocalBoardPredefined(0, 0, 'X')
                    if self.evaluateLocalBoardPredefined(3, 0, 'X') % 100 == 0:
                        score += self.evaluateLocalBoardPredefined(3, 0, 'X')
                    if self.evaluateLocalBoardPredefined(6, 0, 'X') % 100 == 0:
                        score += self.evaluateLocalBoardPredefined(6, 0, 'X')
                    if self.evaluateLocalBoardPredefined(0, 3, 'X') % 100 == 0:
                        score += self.evaluateLocalBoardPredefined(0, 3, 'X')
                    if self.evaluateLocalBoardPredefined(3, 3, 'X') % 100 == 0:
                        score += self.evaluateLocalBoardPredefined(3, 3, 'X')
                    if self.evaluateLocalBoardPredefined(6, 3, 'X') % 100 == 0:
                        score += self.evaluateLocalBoardPredefined(6, 3, 'X')
                    if self.evaluateLocalBoardPredefined(0, 6, 'X') % 100 == 0:
                        score += self.evaluateLocalBoardPredefined(0, 6, 'X')
                    if self.evaluateLocalBoardPredefined(3, 6, 'X') % 100 == 0:
                        score += self.evaluateLocalBoardPredefined(3, 6, 'X')
                    if self.evaluateLocalBoardPredefined(6, 6, 'X') % 100 == 0:
                        score += self.evaluateLocalBoardPredefined(6, 6, 'X')
                else:
                    score += self.evaluateLocalBoardPredefined(0, 0, 'X') + self.evaluateLocalBoardPredefined(3, 0, 'X') + self.evaluateLocalBoardPredefined(6, 0, 'X') + self.evaluateLocalBoardPredefined(0, 3, 'X') + self.evaluateLocalBoardPredefined(3, 3, 'X') + self.evaluateLocalBoardPredefined(6, 3, 'X') + self.evaluateLocalBoardPredefined(0, 6, 'X') + self.evaluateLocalBoardPredefined(3, 6, 'X') + self.evaluateLocalBoardPredefined(6, 6, 'X')
        # min player
        else:
            if self.evaluateLocalBoardPredefined(0, 0, 'O') == 10000 or self.evaluateLocalBoardPredefined(3, 0, 'O') ==10000 or self.evaluateLocalBoardPredefined(6, 0, 'O') == 10000 or self.evaluateLocalBoardPredefined(0, 3, 'O') == 10000 or self.evaluateLocalBoardPredefined(3, 3, 'O') == 10000 or self.evaluateLocalBoardPredefined(6, 3, 'O') == 10000 or self.evaluateLocalBoardPredefined(0, 6, 'O') == 10000 or self.evaluateLocalBoardPredefined(3, 6, 'O') == 10000 or self.evaluateLocalBoardPredefined(6, 6, 'O') == 10000:
               self.twos = False
               return -10000
            else:
                if self.twos:
                    if self.evaluateLocalBoardPredefined(0, 0, 'O') % 100 == 0:
                        score += self.evaluateLocalBoardPredefined(0, 0, 'O')
                    if self.evaluateLocalBoardPredefined(3, 0, 'O') % 100 == 0:
                        score += self.evaluateLocalBoardPredefined(3, 0, 'O')
                    if self.evaluateLocalBoardPredefined(6, 0, 'O') % 100 == 0:
                        score += self.evaluateLocalBoardPredefined(6, 0, 'O')
                    if self.evaluateLocalBoardPredefined(0, 3, 'O') % 100 == 0:
                        score += self.evaluateLocalBoardPredefined(0, 3, 'O')
                    if self.evaluateLocalBoardPredefined(3, 3, 'O') % 100 == 0:
                        score += self.evaluateLocalBoardPredefined(3, 3, 'O')
                    if self.evaluateLocalBoardPredefined(6, 3, 'O') % 100 == 0:
                        score += self.evaluateLocalBoardPredefined(6, 3, 'O')
                    if self.evaluateLocalBoardPredefined(0, 6, 'O') % 100 == 0:
                        score += self.evaluateLocalBoardPredefined(0, 6, 'O')
                    if self.evaluateLocalBoardPredefined(3, 6, 'O') % 100 == 0:
                        score += self.evaluateLocalBoardPredefined(3, 6, 'X')
                    if self.evaluateLocalBoardPredefined(6, 6, 'O') % 100 == 0:
                        score += self.evaluateLocalBoardPredefined(6, 6, 'O')
                else:
                    score += self.evaluateLocalBoardPredefined(0, 0, 'O') + self.evaluateLocalBoardPredefined(3, 0, 'O') + self.evaluateLocalBoardPredefined(6, 0, 'O') + self.evaluateLocalBoardPredefined(0, 3, 'O') + self.evaluateLocalBoardPredefined(3, 3, 'O') + self.evaluateLocalBoardPredefined(6, 3, 'O') + self.evaluateLocalBoardPredefined(0, 6, 'O') + self.evaluateLocalBoardPredefined(3, 6, 'O') + self.evaluateLocalBoardPredefined(6, 6, 'O')
                score *= -1
        self.twos = False
        return score

    def evaluateLocalBoardPredefined(self, row_start, col_start, player):
        # check row winner
        if (self.board[row_start][col_start] == self.board[row_start][col_start+1] == self.board[row_start][col_start+2] == player) or (self.board[row_start+1][col_start] == self.board[row_start+1][col_start+1] == self.board[row_start+1][col_start+2] == player) or (self.board[row_start+2][col_start] == self.board[row_start+2][col_start+1] == self.board[row_start+2][col_start+2] == player):
           return 10000
        # check column winner
        if (self.board[row_start][col_start] == self.board[row_start+1][col_start] == self.board[row_start+2][col_start] == player) or (self.board[row_start][col_start+1] == self.board[row_start+1][col_start+1] == self.board[row_start+2][col_start+1] == player) or (self.board[row_start][col_start+2] == self.board[row_start+1][col_start+2] == self.board[row_start+2][col_start+2] == player):
            return 10000
        # check diagonal winner
        if (self.board[row_start][col_start] == self.board[row_start+1][col_start+1] == self.board[row_start+2][col_start+2] == player) or (self.board[row_start][col_start+2] == self.board[row_start+1][col_start+1] == self.board[row_start+2][col_start] == player):
            return 10000

        # now we know there is no winner, so go to rule 2
        fives = 0
        ones = 0
        # check 2/3 rows
        if (self.board[row_start][col_start] == self.board[row_start][col_start+1] == player) and self.board[row_start][col_start+2] == '_':
            fives += 1
        elif (self.board[row_start][col_start] == self.board[row_start][col_start+1] == player) and self.board[row_start][col_start+2] != '_':
            ones += 1
        if (self.board[row_start+1][col_start] == self.board[row_start+1][col_start+1] == player) and self.board[row_start+1][col_start+2] == '_':
            fives += 1
        elif (self.board[row_start+1][col_start] == self.board[row_start+1][col_start+1] == player) and self.board[row_start+1][col_start+2] != '_':
            ones += 1
        if (self.board[row_start+2][col_start] == self.board[row_start+2][col_start+1] == player) and self.board[row_start+2][col_start+2] == '_':
            fives += 1
        elif (self.board[row_start+2][col_start] == self.board[row_start+2][col_start+1] == player) and self.board[row_start+2][col_start+2] != '_':
            ones += 1

        if (self.board[row_start][col_start+1] == self.board[row_start][col_start+2] == player) and self.board[row_start][col_start] == '_':
            fives += 1
        elif (self.board[row_start][col_start+1] == self.board[row_start][col_start+2] == player) and self.board[row_start][col_start] != '_':
            ones += 1
        if (self.board[row_start+1][col_start+1] == self.board[row_start+1][col_start+2] == player) and self.board[row_start+1][col_start] == '_':
            fives += 1
        elif (self.board[row_start+1][col_start+1] == self.board[row_start+1][col_start+2] == player) and self.board[row_start+1][col_start] != '_':
            ones += 1
        if (self.board[row_start+2][col_start+1] == self.board[row_start+2][col_start+2] == player) and self.board[row_start+2][col_start] == '_':
            fives += 1
        elif (self.board[row_start+2][col_start+1] == self.board[row_start+2][col_start+2] == player) and self.board[row_start+2][col_start] != '_':
            ones += 1

        if (self.board[row_start][col_start] == self.board[row_start][col_start+2] == player) and self.board[row_start][col_start+1] == '_':
            fives += 1
        elif (self.board[row_start][col_start] == self.board[row_start][col_start+2] == player) and self.board[row_start][col_start+1] != '_':
            ones += 1
        if (self.board[row_start+1][col_start] == self.board[row_start+1][col_start+2] == player) and self.board[row_start+1][col_start+1] == '_':
            fives += 1
        elif (self.board[row_start+1][col_start] == self.board[row_start+1][col_start+2] == player) and self.board[row_start+1][col_start+1] != '_':
            ones += 1
        if (self.board[row_start+2][col_start] == self.board[row_start+2][col_start+2] == player) and self.board[row_start+2][col_start+1] == '_':
            fives += 1
        elif (self.board[row_start+2][col_start] == self.board[row_start+2][col_start+2] == player) and self.board[row_start+2][col_start+1] != '_':
            ones += 1

        # check 2/3 columns
        if (self.board[row_start][col_start] == self.board[row_start+1][col_start] == player) and self.board[row_start+2][col_start] == '_':
            fives += 1
        elif (self.board[row_start][col_start] == self.board[row_start+1][col_start] == player) and self.board[row_start+2][col_start] != '_':
            ones += 1
        if (self.board[row_start][col_start+1] == self.board[row_start+1][col_start+1] == player) and self.board[row_start+2][col_start+1] == '_':
            fives += 1
        elif (self.board[row_start][col_start+1] == self.board[row_start+1][col_start+1] == player) and self.board[row_start+2][col_start+1] != '_':
            ones += 1
        if (self.board[row_start][col_start+2] == self.board[row_start+1][col_start+2] == player) and self.board[row_start+2][col_start+2] == '_':
            fives += 1
        elif (self.board[row_start][col_start+2] == self.board[row_start+1][col_start+2] == player) and self.board[row_start+2][col_start+2] != '_':
            ones += 1

        if (self.board[row_start+1][col_start] == self.board[row_start+2][col_start] == player) and self.board[row_start][col_start] == '_':
            fives += 1
        elif (self.board[row_start+1][col_start] == self.board[row_start+2][col_start] == player) and self.board[row_start][col_start] != '_':
            ones += 1
        if (self.board[row_start+1][col_start+1] == self.board[row_start+2][col_start+1] == player) and self.board[row_start][col_start+1] == '_':
            fives += 1
        elif (self.board[row_start+1][col_start+1] == self.board[row_start+2][col_start+1] == player) and self.board[row_start][col_start+1] != '_':
            ones += 1
        if (self.board[row_start+1][col_start+2] == self.board[row_start+2][col_start+2] == player) and self.board[row_start][col_start+2] == '_':
            fives += 1
        elif (self.board[row_start+1][col_start+2] == self.board[row_start+2][col_start+2] == player) and self.board[row_start][col_start+2] != '_':
            ones += 1

        if (self.board[row_start][col_start] == self.board[row_start+2][col_start] == player) and self.board[row_start+1][col_start] == '_':
            fives += 1
        elif (self.board[row_start][col_start] == self.board[row_start+2][col_start] == player) and self.board[row_start+1][col_start] != '_':
            ones += 1
        if (self.board[row_start][col_start+1] == self.board[row_start+2][col_start+1] == player) and self.board[row_start+1][col_start+1] == '_':
            fives += 1
        elif (self.board[row_start][col_start+1] == self.board[row_start+2][col_start+1] == player) and self.board[row_start+1][col_start+1] != '_':
            ones += 1
        if (self.board[row_start][col_start+2] == self.board[row_start+2][col_start+2] == player) and self.board[row_start+1][col_start+2] == '_':
            fives += 1
        elif (self.board[row_start][col_start+2] == self.board[row_start+2][col_start+2] == player) and self.board[row_start+1][col_start+2] != '_':
            ones += 1

        # check 2/3 diagonals
        if (self.board[row_start][col_start] == self.board[row_start+1][col_start+1] == player) and self.board[row_start+2][col_start+2] == '_':
            fives += 1
        elif (self.board[row_start][col_start] == self.board[row_start+1][col_start+1] == player) and self.board[row_start+2][col_start+2] != '_':
            ones += 1
        if (self.board[row_start+1][col_start+1] == self.board[row_start+2][col_start+2] == player) and self.board[row_start][col_start] == '_':
            fives += 1
        elif (self.board[row_start+1][col_start+1] == self.board[row_start+2][col_start+2] == player) and self.board[row_start][col_start] != '_':
            ones += 1
        if (self.board[row_start][col_start] == self.board[row_start+2][col_start+2] == player) and self.board[row_start+1][col_start+1] == '_':
            fives += 1
        elif (self.board[row_start][col_start] == self.board[row_start+2][col_start+2] == player) and self.board[row_start+1][col_start+1] != '_':
            ones += 1

        if (self.board[row_start+2][col_start] == self.board[row_start+1][col_start+1] == player) and self.board[row_start][col_start+2] == '_':
            fives += 1
        elif (self.board[row_start+2][col_start] == self.board[row_start+1][col_start+1] == player) and self.board[row_start][col_start+2] != '_':
            ones += 1
        if (self.board[row_start+1][col_start+1] == self.board[row_start][col_start+2] == player) and self.board[row_start+2][col_start] == '_':
            fives += 1
        elif (self.board[row_start+1][col_start+1] == self.board[row_start][col_start+2] == player) and self.board[row_start+2][col_start] != '_':
            ones += 1
        if (self.board[row_start+2][col_start] == self.board[row_start][col_start+2] == player) and self.board[row_start+1][col_start+1] == '_':
            fives += 1
        elif (self.board[row_start+2][col_start] == self.board[row_start][col_start+2] == player) and self.board[row_start+1][col_start+1] != '_':
            ones += 1

        ret = (500 * fives) + (100 * ones)
        if ret != 0:
            self.twos = True
            return ret

        corners = 0
        if self.board[row_start][col_start] == player:
            corners += 1
        if self.board[row_start+2][col_start] == player:
            corners += 1
        if self.board[row_start][col_start+2] == player:
            corners += 1
        if self.board[row_start+2][col_start+2] == player:
            corners += 1
        
        # print("corners: ", corners*30)
        return (corners * 30)

    def evaluateDesigned(self, isMax):
        """
        This function implements the evaluation function for ultimate tic tac toe for your own agent.
        input args:
        isMax(bool): boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        score(float): estimated utility score for maxPlayer or minPlayer
        """
        #YOUR CODE HERE
        score=0
        max_score = 0
        min_score = 0
        # cover max player first
        if self.evaluateLocalBoardDesigned(0, 0, 'X') == 10000 or self.evaluateLocalBoardDesigned(3, 0, 'X') == 10000 or self.evaluateLocalBoardDesigned(6, 0, 'X') == 10000 or self.evaluateLocalBoardDesigned(0, 3, 'X') == 10000 or self.evaluateLocalBoardDesigned(3, 3, 'X') == 10000 or self.evaluateLocalBoardDesigned(6, 3, 'X') == 10000 or self.evaluateLocalBoardDesigned(0, 6, 'X') == 10000 or self.evaluateLocalBoardDesigned(3, 6, 'X') == 10000 or self.evaluateLocalBoardDesigned(6, 6, 'X') == 10000:
           self.twos = False
           max_score = 10000
        else:
            if self.twos:
                if self.evaluateLocalBoardDesigned(0, 0, 'X') % 100 == 0:
                    max_score += self.evaluateLocalBoardDesigned(0, 0, 'X')
                if self.evaluateLocalBoardDesigned(3, 0, 'X') % 100 == 0:
                    max_score += self.evaluateLocalBoardDesigned(3, 0, 'X')
                if self.evaluateLocalBoardDesigned(6, 0, 'X') % 100 == 0:
                    max_score += self.evaluateLocalBoardDesigned(6, 0, 'X')
                if self.evaluateLocalBoardDesigned(0, 3, 'X') % 100 == 0:
                    max_score += self.evaluateLocalBoardDesigned(0, 3, 'X')
                if self.evaluateLocalBoardDesigned(3, 3, 'X') % 100 == 0:
                    max_score += self.evaluateLocalBoardDesigned(3, 3, 'X')
                if self.evaluateLocalBoardDesigned(6, 3, 'X') % 100 == 0:
                    max_score += self.evaluateLocalBoardDesigned(6, 3, 'X')
                if self.evaluateLocalBoardDesigned(0, 6, 'X') % 100 == 0:
                    max_score += self.evaluateLocalBoardDesigned(0, 6, 'X')
                if self.evaluateLocalBoardDesigned(3, 6, 'X') % 100 == 0:
                    max_score += self.evaluateLocalBoardDesigned(3, 6, 'X')
                if self.evaluateLocalBoardDesigned(6, 6, 'X') % 100 == 0:
                    max_score += self.evaluateLocalBoardDesigned(6, 6, 'X')
            else:
                max_score += self.evaluateLocalBoardDesigned(0, 0, 'X') + self.evaluateLocalBoardDesigned(3, 0, 'X') + self.evaluateLocalBoardDesigned(6, 0, 'X') + self.evaluateLocalBoardDesigned(0, 3, 'X') + self.evaluateLocalBoardDesigned(3, 3, 'X') + self.evaluateLocalBoardDesigned(6, 3, 'X') + self.evaluateLocalBoardDesigned(0, 6, 'X') + self.evaluateLocalBoardDesigned(3, 6, 'X') + self.evaluateLocalBoardDesigned(6, 6, 'X')
    # min player

        if self.evaluateLocalBoardDesigned(0, 0, 'O') == 10000 or self.evaluateLocalBoardDesigned(3, 0, 'O') ==10000 or self.evaluateLocalBoardDesigned(6, 0, 'O') == 10000 or self.evaluateLocalBoardDesigned(0, 3, 'O') == 10000 or self.evaluateLocalBoardDesigned(3, 3, 'O') == 10000 or self.evaluateLocalBoardDesigned(6, 3, 'O') == 10000 or self.evaluateLocalBoardDesigned(0, 6, 'O') == 10000 or self.evaluateLocalBoardDesigned(3, 6, 'O') == 10000 or self.evaluateLocalBoardDesigned(6, 6, 'O') == 10000:
           self.twos = False
           min_score = -10000
        else:
            if self.twos:
                if self.evaluateLocalBoardDesigned(0, 0, 'O') % 100 == 0:
                    min_score += self.evaluateLocalBoardDesigned(0, 0, 'O')
                if self.evaluateLocalBoardDesigned(3, 0, 'O') % 100 == 0:
                    min_score += self.evaluateLocalBoardDesigned(3, 0, 'O')
                if self.evaluateLocalBoardDesigned(6, 0, 'O') % 100 == 0:
                    min_score += self.evaluateLocalBoardDesigned(6, 0, 'O')
                if self.evaluateLocalBoardDesigned(0, 3, 'O') % 100 == 0:
                    min_score += self.evaluateLocalBoardDesigned(0, 3, 'O')
                if self.evaluateLocalBoardDesigned(3, 3, 'O') % 100 == 0:
                    min_score += self.evaluateLocalBoardDesigned(3, 3, 'O')
                if self.evaluateLocalBoardDesigned(6, 3, 'O') % 100 == 0:
                    min_score += self.evaluateLocalBoardDesigned(6, 3, 'O')
                if self.evaluateLocalBoardDesigned(0, 6, 'O') % 100 == 0:
                    min_score += self.evaluateLocalBoardDesigned(0, 6, 'O')
                if self.evaluateLocalBoardDesigned(3, 6, 'O') % 100 == 0:
                    min_score += self.evaluateLocalBoardDesigned(3, 6, 'X')
                if self.evaluateLocalBoardDesigned(6, 6, 'O') % 100 == 0:
                    min_score += self.evaluateLocalBoardDesigned(6, 6, 'O')
            else:
                min_score += self.evaluateLocalBoardDesigned(0, 0, 'O') + self.evaluateLocalBoardDesigned(3, 0, 'O') + self.evaluateLocalBoardDesigned(6, 0, 'O') + self.evaluateLocalBoardDesigned(0, 3, 'O') + self.evaluateLocalBoardDesigned(3, 3, 'O') + self.evaluateLocalBoardDesigned(6, 3, 'O') + self.evaluateLocalBoardDesigned(0, 6, 'O') + self.evaluateLocalBoardDesigned(3, 6, 'O') + self.evaluateLocalBoardDesigned(6, 6, 'O')
            min_score *= -1
        self.twos = False
        score = max_score + min_score
        return score


    def evaluateLocalBoardDesigned(self, row_start, col_start, player):
        # check row winner
        if (self.board[row_start][col_start] == self.board[row_start][col_start+1] == self.board[row_start][col_start+2] == player) or (self.board[row_start+1][col_start] == self.board[row_start+1][col_start+1] == self.board[row_start+1][col_start+2] == player) or (self.board[row_start+2][col_start] == self.board[row_start+2][col_start+1] == self.board[row_start+2][col_start+2] == player):
           return 10000
        # check column winner
        if (self.board[row_start][col_start] == self.board[row_start+1][col_start] == self.board[row_start+2][col_start] == player) or (self.board[row_start][col_start+1] == self.board[row_start+1][col_start+1] == self.board[row_start+2][col_start+1] == player) or (self.board[row_start][col_start+2] == self.board[row_start+1][col_start+2] == self.board[row_start+2][col_start+2] == player):
            return 10000
        # check diagonal winner
        if (self.board[row_start][col_start] == self.board[row_start+1][col_start+1] == self.board[row_start+2][col_start+2] == player) or (self.board[row_start][col_start+2] == self.board[row_start+1][col_start+1] == self.board[row_start+2][col_start] == player):
            return 10000

        # checking V pattern
        num_vs = 0
        if (self.board[row_start][col_start] == self.board[row_start][col_start+2] == self.board[row_start+1][col_start+1] == player and self.board[row_start][col_start+1] == self.board[row_start+2][col_start] == self.board[row_start+2][col_start+2] == '_'):
            return 2000
        if (self.board[row_start][col_start] == self.board[row_start+1][col_start+1] == self.board[row_start+2][col_start] == player and self.board[row_start+1][col_start] == self.board[row_start][col_start+2] == self.board[row_start+2][col_start+2] == '_'):
            return 2000
        if (self.board[row_start][col_start+2] == self.board[row_start+1][col_start+1] == self.board[row_start+2][col_start+2] == player and self.board[row_start+1][col_start+2] == self.board[row_start][col_start] == self.board[row_start+2][col_start] == '_'):
            return 2000
        if (self.board[row_start+1][col_start+1] == self.board[row_start+2][col_start] == self.board[row_start+2][col_start+2] == player and self.board[row_start][col_start] == self.board[row_start][col_start+2] == self.board[row_start+2][col_start+1] == '_'):
            return 2000

        if (self.board[row_start][col_start] == self.board[row_start][col_start+2] == self.board[row_start+1][col_start+1] == player and self.board[row_start][col_start+1] != '_' and self.board[row_start+2][col_start] == self.board[row_start+2][col_start+2] == '_'):
            return 1000 
        if (self.board[row_start][col_start] == self.board[row_start][col_start+2] == self.board[row_start+1][col_start+1] == player and self.board[row_start][col_start+1] == '_' and self.board[row_start+2][col_start] != '_' and self.board[row_start+2][col_start+2] == '_'):
            return 1000
        if (self.board[row_start][col_start] == self.board[row_start][col_start+2] == self.board[row_start+1][col_start+1] == player and self.board[row_start][col_start+1] == self.board[row_start+2][col_start] == '_' and self.board[row_start+2][col_start+2] != '_'):
            return 1000

        if (self.board[row_start][col_start] == self.board[row_start+1][col_start+1] == self.board[row_start+2][col_start] == player and self.board[row_start+1][col_start] != '_' and self.board[row_start][col_start+2] == self.board[row_start+2][col_start+2] == '_'):
            return 1000
        if (self.board[row_start][col_start] == self.board[row_start+1][col_start+1] == self.board[row_start+2][col_start] == player and self.board[row_start+1][col_start] == '_' and self.board[row_start][col_start+2] != '_' and self.board[row_start+2][col_start+2] == '_'):
            return 1000
        if (self.board[row_start][col_start] == self.board[row_start+1][col_start+1] == self.board[row_start+2][col_start] == player and self.board[row_start+1][col_start] == self.board[row_start][col_start+2] == '_' and self.board[row_start+2][col_start+2] != '_'):
            return 1000

        if (self.board[row_start][col_start+2] == self.board[row_start+1][col_start+1] == self.board[row_start+2][col_start+2] == player and self.board[row_start+1][col_start+2] != '_' and self.board[row_start][col_start] == self.board[row_start+2][col_start] == '_'):
            return 1000
        if (self.board[row_start][col_start+2] == self.board[row_start+1][col_start+1] == self.board[row_start+2][col_start+2] == player and self.board[row_start+1][col_start+2] == '_' and self.board[row_start][col_start] != '_' and self.board[row_start+2][col_start] == '_'):
            return 1000
        if (self.board[row_start][col_start+2] == self.board[row_start+1][col_start+1] == self.board[row_start+2][col_start+2] == player and self.board[row_start+1][col_start+2] == self.board[row_start][col_start] == '_' and self.board[row_start+2][col_start] != '_'):
            return 1000

        if (self.board[row_start+1][col_start+1] == self.board[row_start+2][col_start] == self.board[row_start+2][col_start+2] == player and self.board[row_start][col_start] != '_' and self.board[row_start][col_start+2] == self.board[row_start+2][col_start+1] == '_'):
            return 10000
        if (self.board[row_start+1][col_start+1] == self.board[row_start+2][col_start] == self.board[row_start+2][col_start+2] == player and self.board[row_start][col_start] == '_' and self.board[row_start][col_start+2] != '_' and self.board[row_start+2][col_start+1] == '_'):
            return 10000
        if (self.board[row_start+1][col_start+1] == self.board[row_start+2][col_start] == self.board[row_start+2][col_start+2] == player and self.board[row_start][col_start] == self.board[row_start][col_start+2] == '_' and self.board[row_start+2][col_start+1] != '_'):
            return 10000

        # now we know there is no winner, so go to rule 2
        fives = 0
        ones = 0
        # check 2/3 rows
        if (self.board[row_start][col_start] == self.board[row_start][col_start+1] == player) and self.board[row_start][col_start+2] == '_':
            fives += 1
        elif (self.board[row_start][col_start] == self.board[row_start][col_start+1] == player) and self.board[row_start][col_start+2] != '_':
            ones += 1
        if (self.board[row_start+1][col_start] == self.board[row_start+1][col_start+1] == player) and self.board[row_start+1][col_start+2] == '_':
            fives += 1
        elif (self.board[row_start+1][col_start] == self.board[row_start+1][col_start+1] == player) and self.board[row_start+1][col_start+2] != '_':
            ones += 1
        if (self.board[row_start+2][col_start] == self.board[row_start+2][col_start+1] == player) and self.board[row_start+2][col_start+2] == '_':
            fives += 1
        elif (self.board[row_start+2][col_start] == self.board[row_start+2][col_start+1] == player) and self.board[row_start+2][col_start+2] != '_':
            ones += 1

        if (self.board[row_start][col_start+1] == self.board[row_start][col_start+2] == player) and self.board[row_start][col_start] == '_':
            fives += 1
        elif (self.board[row_start][col_start+1] == self.board[row_start][col_start+2] == player) and self.board[row_start][col_start] != '_':
            ones += 1
        if (self.board[row_start+1][col_start+1] == self.board[row_start+1][col_start+2] == player) and self.board[row_start+1][col_start] == '_':
            fives += 1
        elif (self.board[row_start+1][col_start+1] == self.board[row_start+1][col_start+2] == player) and self.board[row_start+1][col_start] != '_':
            ones += 1
        if (self.board[row_start+2][col_start+1] == self.board[row_start+2][col_start+2] == player) and self.board[row_start+2][col_start] == '_':
            fives += 1
        elif (self.board[row_start+2][col_start+1] == self.board[row_start+2][col_start+2] == player) and self.board[row_start+2][col_start] != '_':
            ones += 1

        if (self.board[row_start][col_start] == self.board[row_start][col_start+2] == player) and self.board[row_start][col_start+1] == '_':
            fives += 1
        elif (self.board[row_start][col_start] == self.board[row_start][col_start+2] == player) and self.board[row_start][col_start+1] != '_':
            ones += 1
        if (self.board[row_start+1][col_start] == self.board[row_start+1][col_start+2] == player) and self.board[row_start+1][col_start+1] == '_':
            fives += 1
        elif (self.board[row_start+1][col_start] == self.board[row_start+1][col_start+2] == player) and self.board[row_start+1][col_start+1] != '_':
            ones += 1
        if (self.board[row_start+2][col_start] == self.board[row_start+2][col_start+2] == player) and self.board[row_start+2][col_start+1] == '_':
            fives += 1
        elif (self.board[row_start+2][col_start] == self.board[row_start+2][col_start+2] == player) and self.board[row_start+2][col_start+1] != '_':
            ones += 1

        # check 2/3 columns
        if (self.board[row_start][col_start] == self.board[row_start+1][col_start] == player) and self.board[row_start+2][col_start] == '_':
            fives += 1
        elif (self.board[row_start][col_start] == self.board[row_start+1][col_start] == player) and self.board[row_start+2][col_start] != '_':
            ones += 1
        if (self.board[row_start][col_start+1] == self.board[row_start+1][col_start+1] == player) and self.board[row_start+2][col_start+1] == '_':
            fives += 1
        elif (self.board[row_start][col_start+1] == self.board[row_start+1][col_start+1] == player) and self.board[row_start+2][col_start+1] != '_':
            ones += 1
        if (self.board[row_start][col_start+2] == self.board[row_start+1][col_start+2] == player) and self.board[row_start+2][col_start+2] == '_':
            fives += 1
        elif (self.board[row_start][col_start+2] == self.board[row_start+1][col_start+2] == player) and self.board[row_start+2][col_start+2] != '_':
            ones += 1

        if (self.board[row_start+1][col_start] == self.board[row_start+2][col_start] == player) and self.board[row_start][col_start] == '_':
            fives += 1
        elif (self.board[row_start+1][col_start] == self.board[row_start+2][col_start] == player) and self.board[row_start][col_start] != '_':
            ones += 1
        if (self.board[row_start+1][col_start+1] == self.board[row_start+2][col_start+1] == player) and self.board[row_start][col_start+1] == '_':
            fives += 1
        elif (self.board[row_start+1][col_start+1] == self.board[row_start+2][col_start+1] == player) and self.board[row_start][col_start+1] != '_':
            ones += 1
        if (self.board[row_start+1][col_start+2] == self.board[row_start+2][col_start+2] == player) and self.board[row_start][col_start+2] == '_':
            fives += 1
        elif (self.board[row_start+1][col_start+2] == self.board[row_start+2][col_start+2] == player) and self.board[row_start][col_start+2] != '_':
            ones += 1

        if (self.board[row_start][col_start] == self.board[row_start+2][col_start] == player) and self.board[row_start+1][col_start] == '_':
            fives += 1
        elif (self.board[row_start][col_start] == self.board[row_start+2][col_start] == player) and self.board[row_start+1][col_start] != '_':
            ones += 1
        if (self.board[row_start][col_start+1] == self.board[row_start+2][col_start+1] == player) and self.board[row_start+1][col_start+1] == '_':
            fives += 1
        elif (self.board[row_start][col_start+1] == self.board[row_start+2][col_start+1] == player) and self.board[row_start+1][col_start+1] != '_':
            ones += 1
        if (self.board[row_start][col_start+2] == self.board[row_start+2][col_start+2] == player) and self.board[row_start+1][col_start+2] == '_':
            fives += 1
        elif (self.board[row_start][col_start+2] == self.board[row_start+2][col_start+2] == player) and self.board[row_start+1][col_start+2] != '_':
            ones += 1

        # check 2/3 diagonals
        if (self.board[row_start][col_start] == self.board[row_start+1][col_start+1] == player) and self.board[row_start+2][col_start+2] == '_':
            fives += 1
        elif (self.board[row_start][col_start] == self.board[row_start+1][col_start+1] == player) and self.board[row_start+2][col_start+2] != '_':
            ones += 1
        if (self.board[row_start+1][col_start+1] == self.board[row_start+2][col_start+2] == player) and self.board[row_start][col_start] == '_':
            fives += 1
        elif (self.board[row_start+1][col_start+1] == self.board[row_start+2][col_start+2] == player) and self.board[row_start][col_start] != '_':
            ones += 1
        if (self.board[row_start][col_start] == self.board[row_start+2][col_start+2] == player) and self.board[row_start+1][col_start+1] == '_':
            fives += 1
        elif (self.board[row_start][col_start] == self.board[row_start+2][col_start+2] == player) and self.board[row_start+1][col_start+1] != '_':
            ones += 1

        if (self.board[row_start+2][col_start] == self.board[row_start+1][col_start+1] == player) and self.board[row_start][col_start+2] == '_':
            fives += 1
        elif (self.board[row_start+2][col_start] == self.board[row_start+1][col_start+1] == player) and self.board[row_start][col_start+2] != '_':
            ones += 1
        if (self.board[row_start+1][col_start+1] == self.board[row_start][col_start+2] == player) and self.board[row_start+2][col_start] == '_':
            fives += 1
        elif (self.board[row_start+1][col_start+1] == self.board[row_start][col_start+2] == player) and self.board[row_start+2][col_start] != '_':
            ones += 1
        if (self.board[row_start+2][col_start] == self.board[row_start][col_start+2] == player) and self.board[row_start+1][col_start+1] == '_':
            fives += 1
        elif (self.board[row_start+2][col_start] == self.board[row_start][col_start+2] == player) and self.board[row_start+1][col_start+1] != '_':
            ones += 1

        ret = (500 * fives) + (100 * ones)
        if ret != 0:
            self.twos = True
            return ret

        corners = 0
        if self.board[row_start][col_start] == player:
            corners += 1
        if self.board[row_start+2][col_start] == player:
            corners += 1
        if self.board[row_start][col_start+2] == player:
            corners += 1
        if self.board[row_start+2][col_start+2] == player:
            corners += 1
        
        # print("corners: ", corners*30)
        return (corners * 30)

    def checkMovesLeft(self):
        """
        This function checks whether any legal move remains on the board.
        output:
        movesLeft(bool): boolean variable indicates whether any legal move remains
                        on the board.
        """
        #YOUR CODE HERE
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j] == '_':
                    return True
        return False

    def checkWinner(self):
        #Return termimnal node status for maximizer player 1-win,0-tie,-1-lose
        """
        This function checks whether there is a winner on the board.
        output:
        winner(int): Return 0 if there is no winner.
                     Return 1 if maxPlayer is the winner.
                     Return -1 if miniPlayer is the winner.
        """
        #YOUR CODE HERE
        out1 = 0
        out2 = 0
        if self.currPlayer:
            out1 = 1
            out2 = -1
        else:
            out1 = -1
            out2 = 1
        if self.evaluatePredifined(self.currPlayer) == 10000:
            return out1
        elif self.evaluatePredifined(self.currPlayer) == -10000:
            return out1
        elif self.evaluatePredifined(not self.currPlayer) == 10000:
            return out2
        elif self.evaluatePredifined(not self.currPlayer) == -10000:
            return out2
        else:
            a = abs(self.evaluatePredifined(self.currPlayer))
            b = abs(self.evaluatePredifined(not self.currPlayer))
            if a > b:
                return out1
            elif b > a:
                return out2
            else:
                return 0

    def alphabeta(self,depth,currBoardIdx,alpha,beta,isMax):
        """
        This function implements alpha-beta algorithm for ultimate tic-tac-toe game.
        input args:
        depth(int): current depth level
        currBoardIdx(int): current local board index
        alpha(float): alpha value
        beta(float): beta value
        isMax(bool):boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        bestValue(float):the bestValue that current player may have
        """
        #YOUR CODE HERE
        if depth == 3:
            return self.evaluatePredifined(not isMax)
        
        if isMax:
            bestValue = float('-inf')
            startIndex = self.globalIdx[currBoardIdx]
            for i in range(0, 3):
                for j in range(0, 3):
                    if self.board[i + startIndex[0]][j + startIndex[1]] == '_':
                        self.board[i + startIndex[0]][j + startIndex[1]] = self.maxPlayer
                        self.currExpandedNodes += 1
                        currValue = self.alphabeta(depth + 1, (3*j) + i, alpha, beta, not isMax)
                        if (currValue > bestValue) and depth == 0:
                            self.bestMove = (startIndex[0] + i, startIndex[1] + j)
                        bestValue = max(bestValue, currValue)
                        self.board[i + startIndex[0]][j + startIndex[1]] = '_'
                        alpha = max(alpha, bestValue)
                        if beta <= alpha:
                            break
            return bestValue
        else:
            bestValue = float('inf')
            startIndex = self.globalIdx[currBoardIdx]
            for i in range(0, 3):
                for j in range(0, 3):
                    if self.board[i + startIndex[0]][j + startIndex[1]] == '_':
                        self.board[i + startIndex[0]][j + startIndex[1]] = self.minPlayer
                        self.currExpandedNodes += 1
                        currValue = self.alphabeta(depth + 1, (3*j) + i, alpha, beta, not isMax)
                        if currValue < bestValue and depth == 0:
                            self.bestMove = (startIndex[0] + i, startIndex[1] + j)
                        bestValue = min(bestValue, currValue)
                        self.board[i + startIndex[0]][j + startIndex[1]] = '_'
                        alpha = min(alpha, bestValue)
                        if beta <= alpha:
                            break
            return bestValue
    def ownalphabeta(self,depth,currBoardIdx,alpha,beta,isMax):
        """
        This function implements alpha-beta algorithm for ultimate tic-tac-toe game.
        input args:
        depth(int): current depth level
        currBoardIdx(int): current local board index
        alpha(float): alpha value
        beta(float): beta value
        isMax(bool):boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        bestValue(float):the bestValue that current player may have
        """
        #YOUR CODE HERE
        if depth == 3:
            return self.evaluateDesigned(not isMax)
        
        if isMax:
            bestValue = float('-inf')
            startIndex = self.globalIdx[currBoardIdx]
            for i in range(0, 3):
                for j in range(0, 3):
                    if self.board[i + startIndex[0]][j + startIndex[1]] == '_':
                        self.board[i + startIndex[0]][j + startIndex[1]] = self.maxPlayer
                        currValue = self.alphabeta(depth + 1, (3*j) + i, alpha, beta, not isMax)
                        if (currValue > bestValue) and depth == 0:
                            self.bestMove = (startIndex[0] + i, startIndex[1] + j)
                        bestValue = max(bestValue, currValue)
                        self.board[i + startIndex[0]][j + startIndex[1]] = '_'
                        alpha = max(alpha, bestValue)
                        if beta <= alpha:
                            break
            return bestValue
        else:
            bestValue = float('inf')
            startIndex = self.globalIdx[currBoardIdx]
            for i in range(0, 3):
                for j in range(0, 3):
                    if self.board[i + startIndex[0]][j + startIndex[1]] == '_':
                        self.board[i + startIndex[0]][j + startIndex[1]] = self.minPlayer
                        currValue = self.alphabeta(depth + 1, (3*j) + i, alpha, beta, not isMax)
                        if currValue < bestValue and depth == 0:
                            self.bestMove = (startIndex[0] + i, startIndex[1] + j)
                        bestValue = min(bestValue, currValue)
                        self.board[i + startIndex[0]][j + startIndex[1]] = '_'
                        alpha = min(alpha, bestValue)
                        if beta <= alpha:
                            break
            return bestValue

    def minimax(self, depth, currBoardIdx, isMax):
        """
        This function implements minimax algorithm for ultimate tic-tac-toe game.
        input args:
        depth(int): current depth level
        currBoardIdx(int): current local board index
        isMax(bool):boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        bestValue(float):the bestValue that current player may have
        """
        #YOUR CODE HERE

        if depth == 3:
            # print("depth is 3: ",self.evaluatePredifined(not isMax))
            return self.evaluatePredifined(not isMax)

        if isMax:
            bestValue = float('-inf')
            startIndex = self.globalIdx[currBoardIdx]
            for i in range(0, 3):
                for j in range(0, 3):
                    if self.board[i + startIndex[0]][j + startIndex[1]] == '_':
                        self.board[i + startIndex[0]][j + startIndex[1]] = self.maxPlayer
                        self.currExpandedNodes += 1
                        currValue = self.minimax(depth + 1, (3*j) + i, not isMax)
                        if currValue > bestValue and depth == 0:
                            self.bestMove = (startIndex[0] + i, startIndex[1] + j)
                        bestValue = max(bestValue, currValue)
                        self.board[i + startIndex[0]][j + startIndex[1]] = '_'
            return bestValue

        else:
            bestValue = float('inf')
            startIndex = self.globalIdx[currBoardIdx]
            for i in range(0, 3):
                for j in range(0, 3):
                    if self.board[i + startIndex[0]][j + startIndex[1]] == '_':
                        self.board[i + startIndex[0]][j + startIndex[1]] = self.minPlayer
                        self.currExpandedNodes += 1
                        currValue = self.minimax(depth + 1, (3*j) + i, not isMax)
                        if currValue < bestValue and depth == 0:
                            self.bestMove = (startIndex[0] + i, startIndex[1] + j)
                        bestValue = min(bestValue, currValue)
                        self.board[i + startIndex[0]][j + startIndex[1]] = '_'
            return bestValue

    def findBestMove(self, currBoardIdx, player, alg_flag):
        # alg_flag: 0 for minimax and 1 for alphabeta
        startIndex = self.globalIdx[currBoardIdx]
        bestValue = 0
        if player:
            bestValue = float('-inf')
            for i in range(3):
                for j in range(3):
                    if self.board[i + startIndex[0]][j + startIndex[1]] == '_':
                        self.board[i + startIndex[0]][j + startIndex[1]] = self.maxPlayer
                        currValue = float('-inf')
                        if (alg_flag):
                            currValue = self.alphabeta(0, currBoardIdx, float('-inf'), float('inf'), not player)
                        else:
                            currValue = self.minimax(0, (3*j) + i, not player)
                        self.board[i + startIndex[0]][j + startIndex[1]] = '_'
                        if currValue > bestValue:
                            self.bestMove = (i + startIndex[0], j + startIndex[1])
                            bestValue = currValue
        else:
            bestValue = float('inf')
            for i in range(3):
                for j in range(3):
                    if self.board[i + startIndex[0]][j + startIndex[1]] == '_':
                        self.board[i + startIndex[0]][j + startIndex[1]] = self.minPlayer
                        currValue = float('inf')
                        if (alg_flag):
                            currValue = self.alphabeta(0, currBoardIdx, float('-inf'), float('inf'), not player)
                        else:
                            currValue = self.minimax(0, (3*j) + i, not player)
                        self.board[i + startIndex[0]][j + startIndex[1]] = '_'
                        if currValue < bestValue:
                            self.bestMove = (i + startIndex[0], j + startIndex[1])
                            bestValue = currValue
        return bestValue

    def getBoardIdx(self, top_left, potential_move):
        """
        This function returns the index of the large board after a potential move
        input args:
        top_left(tuple): tuple containing x and y coord of top left cell of current board
        potential_move(tuple): tuple containing x and y coord of potential move

        Calculate with formula that depends on indices being ordered from left to right and then top to bottom
        """
        return (potential_move[0] - top_left[0]) + 3*(potential_move[1] - top_left[1])

    def getTopLeft(self, currIdx):
        # This should return a tuple with the top left of a given local board
        return self.globalIdx[currIdx]


    def playGamePredifinedAgent(self,maxFirst,isMinimaxOffensive,isMinimaxDefensive):
        """
        This function implements the processes of the game of predifined offensive agent vs defensive agent.
        input args:
        maxFirst(bool): boolean variable indicates whether maxPlayer or minPlayer plays first.
                        True for maxPlayer plays first, and False for minPlayer plays first.
        isMinimaxOffensive(bool):boolean variable indicates whether it's using minimax or alpha-beta pruning algorithm for offensive agent.
                        True is minimax and False is alpha-beta.
        isMinimaxOffensive(bool):boolean variable indicates whether it's using minimax or alpha-beta pruning algorithm for defensive agent.
                        True is minimax and False is alpha-beta.
        output:
        bestMove(list of tuple): list of bestMove coordinates at each step
        bestValue(list of float): list of bestValue at each move
        expandedNodes(list of int): list of expanded nodes at each move
        gameBoards(list of 2d lists): list of game board positions at each move
        winner(int): 1 for maxPlayer is the winner, -1 for minPlayer is the winner, and 0 for tie.
        """
        #YOUR CODE HERE
        bestValue=[]
        gameBoards=[]
        bestMoveArr=[]
        expNodesList = []
        currIdx = self.startBoardIdx
        winner = 0

        if maxFirst:
            self.currPlayer = True
        else:
            self.currPlayer = False
        while True:
            if self.evaluatePredifined(not self.currPlayer) == 10000:
                return gameBoards, bestMoveArr, expNodesList, bestValue, self.checkWinner()
            if self.evaluatePredifined(not self.currPlayer) == -10000:
                return gameBoards, bestMoveArr, expNodesList, bestValue, self.checkWinner()
            if self.checkMovesLeft() == False:
                return gameBoards, bestMoveArr, expNodesList, bestValue, self.checkWinner()
            if self.currPlayer:
                if isMinimaxOffensive:
                    bestMoveVal = self.minimax(0, currIdx, self.currPlayer)
                else:
                    bestMoveVal = self.alphabeta(0, currIdx, float('-inf'), float('inf'), self.currPlayer)

                top_left = self.getTopLeft(currIdx)
                currIdx = self.getBoardIdx(top_left, self.bestMove)
                bestMoveArr.append(self.bestMove)
                """
                print("Max player score: ")   
                print(self.evaluatePredifined(self.currPlayer))   
                print("Min Player score: ")
                print(self.evaluatePredifined(not self.currPlayer)) 
                """
                self.expandedNodes.append(self.currExpandedNodes)
                self.currExpandedNodes = 0 
                bestValue.append(bestMoveVal)
                self.board[self.bestMove[0]][self.bestMove[1]] = self.maxPlayer
                gameBoards.append(self.board)
                self.printGameBoard()
                self.currPlayer = not self.currPlayer
            else:
                if isMinimaxDefensive:
                    bestMoveVal = self.minimax(0, currIdx, self.currPlayer)
                else:
                    bestMoveVal = self.alphabeta(0, currIdx, float('-inf'), float('inf'), self.currPlayer)

                top_left = self.getTopLeft(currIdx)
                currIdx = self.getBoardIdx(top_left, self.bestMove)
                bestMoveArr.append(self.bestMove)
                """
                print("Max player score: ")   
                print(self.evaluatePredifined(not self.currPlayer))   
                print("Min Player score: ")
                print(self.evaluatePredifined(self.currPlayer)) 
                """
                self.expandedNodes.append(self.currExpandedNodes)
                self.currExpandedNodes = 0  
                bestValue.append(bestMoveVal)
                self.board[self.bestMove[0]][self.bestMove[1]] = self.minPlayer
                gameBoards.append(self.board)
                self.printGameBoard()
                self.currPlayer = not self.currPlayer

        
        return gameBoards, bestMoveArr, expNodesList, bestValue, winner

    def playGameYourAgent(self):
        """
        This function implements the processes of the game of your own agent vs predifined offensive agent.
        input args:
        output:
        bestMove(list of tuple): list of bestMove coordinates at each step
        gameBoards(list of 2d lists): list of game board positions at each move
        winner(int): 1 for maxPlayer is the winner, -1 for minPlayer is the winner, and 0 for tie.
        """
        #YOUR CODE HERE
        bestValue=[]
        gameBoards=[]
        bestMoveArr=[]
        expNodesList = []
        currIdx = randint(0, 8)
        firstPlayer = randint(0, 1)      # 0 is own agent, 1 is predefined offensive agent
        winner = 0

        if firstPlayer:
            self.currPlayer = True
        else:
            self.currPlayer = False
        while True:
            if self.evaluatePredifined(not self.currPlayer) == 10000:
                return gameBoards, bestMoveArr, expNodesList, bestValue, self.checkWinner()
            if self.evaluatePredifined(not self.currPlayer) == -10000:
                return gameBoards, bestMoveArr, expNodesList, bestValue, self.checkWinner()
            if self.checkMovesLeft() == False:
                return gameBoards, bestMoveArr, expNodesList, bestValue, self.checkWinner()
            if self.currPlayer:
                bestMoveVal = self.alphabeta(0, currIdx, float('-inf'), float('inf'), self.currPlayer)
                top_left = self.getTopLeft(currIdx)
                currIdx = self.getBoardIdx(top_left, self.bestMove)
                bestMoveArr.append(self.bestMove)
                """
                print("Max player score: ")   
                print(self.evaluatePredifined(self.currPlayer))   
                print("Min Player score: ")
                print(self.evaluatePredifined(not self.currPlayer)) 
                """
                self.expandedNodes.append(self.currExpandedNodes)
                bestValue.append(bestMoveVal)
                self.board[self.bestMove[0]][self.bestMove[1]] = self.maxPlayer
                gameBoards.append(self.board)
                self.printGameBoard()
                self.currPlayer = not self.currPlayer
            else:
                bestMoveVal = self.ownalphabeta(0, currIdx, float('-inf'), float('inf'), self.currPlayer)
                top_left = self.getTopLeft(currIdx)
                currIdx = self.getBoardIdx(top_left, self.bestMove)
                bestMoveArr.append(self.bestMove)
                """
                print("Max player score: ")   
                print(self.evaluatePredifined(not self.currPlayer))   
                print("Min Player score: ")
                print(self.evaluatePredifined(self.currPlayer)) 
                """
                self.expandedNodes.append(self.currExpandedNodes)  
                self.currExpandedNodes = 0
                bestValue.append(bestMoveVal)
                self.board[self.bestMove[0]][self.bestMove[1]] = self.minPlayer
                gameBoards.append(self.board)
                self.printGameBoard()
                self.currPlayer = not self.currPlayer

        
        return gameBoards, bestMoveArr, expNodesList, bestValue, winner


    def playGameHuman(self):
        """
        This function implements the processes of the game of your own agent vs a human.
        output:
        bestMove(list of tuple): list of bestMove coordinates at each step
        gameBoards(list of 2d lists): list of game board positions at each move
        winner(int): 1 for maxPlayer is the winner, -1 for minPlayer is the winner, and 0 for tie.
        """
        #YOUR CODE HERE
        bestMove=[]
        gameBoards=[]
        winner=0
        return gameBoards, bestMove, winner

if __name__=="__main__":
    uttt=ultimateTicTacToe()
    # gameBoards, bestMove, expNodesList, bestValue, winner=uttt.playGamePredifinedAgent(True,True,True)
    gameBoard, bestMove, expNodesList, bestValue, winner = uttt.playGameYourAgent()
    print("The number of expanded nodes: ")
    print(uttt.expandedNodes)
    if winner == 1:
        uttt.printGameBoard()
        print("The winner is maxPlayer!!!")
    elif winner == -1:
        uttt.printGameBoard()
        print("The winner is minPlayer!!!")
    else:
        print("Tie. No winner:(")
