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

        self.expandedNodes=0
        self.currPlayer=True

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
            if self.evaluateLocalBoard(0, 0, 'X') == 10000 or self.evaluateLocalBoard(3, 0, 'X') == 10000 or self.evaluateLocalBoard(6, 0, 'X') == 10000 or self.evaluateLocalBoard(0, 3, 'X') == 10000 or self.evaluateLocalBoard(3, 3, 'X') == 10000 or self.evaluateLocalBoard(6, 3, 'X') == 10000 or self.evaluateLocalBoard(0, 6, 'X') == 10000 or self.evaluateLocalBoard(3, 6, 'X') == 10000 or self.evaluateLocalBoard(6, 6, 'X') == 10000:
               return 10000
            else:
                score += self.evaluateLocalBoard(0, 0, 'X') + self.evaluateLocalBoard(3, 0, 'X') + self.evaluateLocalBoard(6, 0, 'X') + self.evaluateLocalBoard(0, 3, 'X') + self.evaluateLocalBoard(3, 3, 'X') + self.evaluateLocalBoard(6, 3, 'X') + self.evaluateLocalBoard(0, 6, 'X') + self.evaluateLocalBoard(3, 6, 'X') + self.evaluateLocalBoard(6, 6, 'X')
        # min player
        else:
            if self.evaluateLocalBoard(0, 0, 'O') == 10000 or self.evaluateLocalBoard(3, 0, 'O') == 10000 or self.evaluateLocalBoard(6, 0, 'O') == 10000 or self.evaluateLocalBoard(0, 3, 'O') == 10000 or self.evaluateLocalBoard(3, 3, 'O') == 10000 or self.evaluateLocalBoard(6, 3, 'O') == 10000 or self.evaluateLocalBoard(0, 6, 'O') == 10000 or self.evaluateLocalBoard(3, 6, 'O') == 10000 or self.evaluateLocalBoard(6, 6, 'O') == 10000:
               return -10000
            else:
                score += self.evaluateLocalBoard(0, 0, 'O') + self.evaluateLocalBoard(3, 0, 'O') + self.evaluateLocalBoard(6, 0, 'O') + self.evaluateLocalBoard(0, 3, 'O') + self.evaluateLocalBoard(3, 3, 'O') + self.evaluateLocalBoard(6, 3, 'O') + self.evaluateLocalBoard(0, 6, 'O') + self.evaluateLocalBoard(3, 6, 'O') + self.evaluateLocalBoard(6, 6, 'O')
                score *= -1
        return score

    def evaluateLocalBoard(self, row_start, col_start, player):
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
        if (self.board[row_start+1][col_start+1] == self.board[row_start][col_start+1] == player) and self.board[row_start+2][col_start] == '_':
            fives += 1
        elif (self.board[row_start+1][col_start+1] == self.board[row_start][col_start+1] == player) and self.board[row_start+2][col_start] != '_':
            ones += 1
        if (self.board[row_start+2][col_start] == self.board[row_start][col_start+2] == player) and self.board[row_start+1][col_start+1] == '_':
            fives += 1
        elif (self.board[row_start+2][col_start] == self.board[row_start][col_start+2] == player) and self.board[row_start+1][col_start+1] != '_':
            ones += 1

        if fives != 0 and ones != 0:
            return (500 * fives) + (100 * ones)

        corners = 0
        if self.board[row_start][col_start] == player:
            corners += 1
        if self.board[row_start+2][col_start] == player:
            corners += 1
        if self.board[row_start][col_start+2] == player:
            corners += 1
        if self.board[row_start+2][col_start+2] == player:
            corners += 1

        return corners * 30

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
        return score

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
        score = self.evaluatePredifined(isMax)
        if score == 10000:
            return score
        if score == -10000:
            return score
        if self.checkMovesLeft() == False:
            return score
        
        if isMax:
            if depth == 3:
                return float('-inf')
            bestValue = float('-inf')
            startIndex = self.globalIdx[currBoardIdx]
            for i in range(0, 3):
                for j in range(0, 3):
                    if self.board[i + startIndex[0]][j + startIndex[1]] == '_':
                        self.board[i + startIndex[0]][j + startIndex[1]] = self.maxPlayer
                        currValue = max(score, self.alphabeta(depth + 1, (3*j) + i, alpha, beta, not isMax))
                        if (currValue > bestValue):
                            bestValue = currValue
                        self.board[i + startIndex[0]][j + startIndex[1]] = '_'
                        alpha = max(alpha, bestValue)
                        if beta <= alpha:
                            break
            return bestValue
        else:
            if depth == 3:
                return float('inf')
            bestValue = float('inf')
            startIndex = self.globalIdx[currBoardIdx]
            for i in range(0, 3):
                for j in range(0, 3):
                    if self.board[i + startIndex[0]][j + startIndex[1]] == '_':
                        self.board[i + startIndex[0]][j + startIndex[1]] = self.minPlayer
                        currValue = min(score, self.alphabeta(depth + 1, (3*j) + i, alpha, beta, not isMax))
                        if currValue < bestValue:
                            bestValue = currValue
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

        score = self.evaluatePredifined(isMax)
        if score == 10000:
            return score
        if score == -10000:
            return score
        if self.checkMovesLeft() == False:
            return score

        if isMax:
            if depth == 3:
                return float('-inf')
            bestValue = float('-inf')
            startIndex = self.globalIdx[currBoardIdx]
            for i in range(0, 3):
                for j in range(0, 3):
                    if self.board[i + startIndex[0]][j + startIndex[1]] == '_':
                        self.board[i + startIndex[0]][j + startIndex[1]] = self.maxPlayer
                        currValue = max(score, self.minimax(depth + 1, (3*j) + i, not isMax))
                        if (currValue > bestValue):
                            bestValue = currValue
                        self.board[i + startIndex[0]][j + startIndex[1]] = '_'
            return bestValue

        else:
            if depth == 3:
                return float('inf')
            bestValue = float('inf')
            startIndex = self.globalIdx[currBoardIdx]
            for i in range(0, 3):
                for j in range(0, 3):
                    if self.board[i + startIndex[0]][j + startIndex[1]] == '_':
                        self.board[i + startIndex[0]][j + startIndex[1]] = self.minPlayer
                        currValue = min(score, self.minimax(depth + 1, (3*j) + i, not isMax))
                        if (currValue < bestValue):
                            bestValue = currValue
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
        expandedNodes = []
        currIdx = self.startBoardIdx
        winner = 0

        if maxFirst:
            self.currPlayer = True
        else:
            self.currPlayer = False
        while True:
            if self.evaluatePredifined(not self.currPlayer) == 10000:
                return gameBoards, bestMoveArr, expandedNodes, bestValue, self.checkWinner()
            if self.evaluatePredifined(not self.currPlayer) == -10000:
                return gameBoards, bestMoveArr, expandedNodes, bestValue, self.checkWinner()
            if self.checkMovesLeft() == False:
                return gameBoards, bestMoveArr, expandedNodes, bestValue, self.checkWinner()
            if self.currPlayer:
                if isMinimaxOffensive:
                    # # # bestMoveVal = self.minimax(0, 4, True)
                    bestMoveVal = self.findBestMove(currIdx, self.currPlayer, 0)     # 0 is for minimax
                    # SHOULD PROBABLY APPEND BESTMOVEVAL TO THE ARRAY BEFORE RETURNING
                    if bestMoveVal == 10000:
                        return gameBoards, bestMoveArr, expandedNodes, bestValue, 1
                else:
                    # NOT SURE WHAT TO DO FOR THE ALPHABETA THING YET (MAYBE PASS AN ALPHA/MINIMAX PARAM TO FINDBESTMOVE)
                    bestMoveVal = self.findBestMove(currIdx, self.currPlayer, 1)     # 1 is for alphabeta
                    # SHOULD PROBABLY APPEND BESTMOVEVAL TO ARRAY BEFORE RETURNING
                    if bestMoveVal == 10000:
                        return gameBoards, bestMoveArr, expandedNodes, bestValue, 1
                top_left = self.getTopLeft(currIdx)
                """
                print("Top Left: ")
                print(top_left)
                print("Potential move")
                print(self.bestMove)
                """
                currIdx = self.getBoardIdx(top_left, self.bestMove)
                # print("Curr Idx")
                # print(currIdx)
                bestMoveArr.append(self.bestMove)
                bestValue.append(bestMoveVal)
                self.board[self.bestMove[0]][self.bestMove[1]] = self.maxPlayer
                gameBoards.append(self.board)
                self.printGameBoard()
                self.currPlayer = not self.currPlayer
            else:
                if isMinimaxDefensive:
                    # # # bestMoveVal = self.minimax(0, 4, False)
                    bestMoveVal = self.findBestMove(currIdx, self.currPlayer, 0)     # 0 is for minimax
                    # SHOULD PROBABLY APPEND TO VAL LIST
                    if bestMoveVal == -10000:
                        return gameBoards, bestMoveArr, expandedNodes, bestValue, -1
                else:
                    # SEE ABOVE COMMENT FOR ALPHABETA
                    bestMoveVal = self.findBestMove(currIdx, self.currPlayer, 1)     # 1 is for alphabeta
                    if bestMoveVal == -10000:
                        return gameBoards, bestMoveArr, expandedNodes, bestValue, -1
                top_left = self.getTopLeft(currIdx)
                currIdx = self.getBoardIdx(top_left, self.bestMove)
                # print(currIdx)
                bestMoveArr.append(self.bestMove)        
                bestValue.append(bestMoveVal)
                self.board[self.bestMove[0]][self.bestMove[1]] = self.minPlayer
                gameBoards.append(self.board)
                self.printGameBoard()
                self.currPlayer = not self.currPlayer

        
        return gameBoards, bestMoveArr, expandedNodes, bestValue, winner

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
        bestMove=[]
        gameBoards=[]
        winner=0
        return gameBoards, bestMove, winner


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
    gameBoards, bestMove, expandedNodes, bestValue, winner=uttt.playGamePredifinedAgent(True,False,True)
    print("The number of expanded nodes: ")
    print(len(expandedNodes))
    if winner == 1:
        uttt.printGameBoard()
        print("The winner is maxPlayer!!!")
    elif winner == -1:
        uttt.printGameBoard()
        print("The winner is minPlayer!!!")
    else:
        print("Tie. No winner:(")
