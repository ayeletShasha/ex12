import numpy

class Game:
    PLAYER1 = 1
    PLAYER2 = 2
    BOARD_ROWS = 6
    BOARD_COLUMNS = 7
    LOCATION_ERROR = "Illegal Location"
    ROW = "row"
    COL = "col"
    DIAGONAL = "diagonal"
    WIN_SEQ_LEN = 4
    TIE = 0
    ILLEGAL_MOVE = "illegal move"

    def __init__(self):
        self.__cur_player = self.PLAYER1
        self.__board = self.__init_board([])
        # self.__board = [[1, 2, 1, 2, 1, 2, 1],
        #                 [1, 2, 1, 2, 1, 2, 1],
        #                 [2, 1, 2, 1, 2, 1, 2],
        #                 [1, 2, 1, 2, 1, 2, 1],
        #                 [1, 2, 1, 2, 1, 2, 1],
        #                 [2, 1, 2, 1, 2, 1, 2]]
        self.__direction_instructions = {self.ROW: (0, 1), self.COL: (1, 0),
                                         self.DIAGONAL: (1, 1)}

    def __init_board(self, board):
        for row in range(self.BOARD_ROWS):
            board.append(([0] * self.BOARD_COLUMNS)[::1])
        return board

    def make_move(self, column):
        """
        a method that conducts a single move in the game
        :param column: a column in which the player wants to insert a disc
        :return:
        """
        trans_board = numpy.transpose(self.__board[::1]) # transpose the
        # board so that columns are now arrays
        if 0 not in trans_board[column] or self.get_winner() or column >= \
                self.BOARD_COLUMNS or column < 0:
            # column is full, illegal or the game is already finished
            return self.ILLEGAL_MOVE  # exception?
        else:
            reversed_col = list(reversed(trans_board[column]))
            for hole in reversed_col:
                if hole == 0:
                    row_i = self.BOARD_ROWS - 1 - reversed_col.index(hole)
                    self.__board[row_i][column] = self.__cur_player
        winner = self.get_winner()
        if winner:  # is not none
            return winner
        self.__switch_player()

    def __switch_player(self):
        if self.__cur_player == self.PLAYER1:
            self.__cur_player = self.PLAYER2
        else:
            self.__cur_player = self.PLAYER1


    def get_winner(self):
        winner = self.__find_sequence()
        if winner:
            # is not none?
            return winner
        if self.__is_board_full():
            return self.TIE
        return None

    def __is_board_full(self):
        """
        a method that checks if the board is full
        :return: True if it is, False otherwise
        """
        for row in self.__board:
            if {self.PLAYER1, self.PLAYER2} & set(row) != 0:
                return False
        return True

    def __find_sequence(self):
        for row in range(self.BOARD_ROWS):
            if {self.PLAYER1, self.PLAYER2} & set(self.__board[row]) != 0:
                # check if there are any discs in this row. if there are,
                # check if there is a winning sequence
                for col in range(self.BOARD_COLUMNS):
                    cur_player = self.get_player_at(row, col)
                    if cur_player is not None:
                        for direc in self.__direction_instructions:
                            row_dir, col_dir = self.__direction_instructions[
                                direc]
                            if self.__find_sequence_helper(cur_player, row,
                                                        col, 0, row_dir,
                                                        col_dir):
                                return cur_player
        return None

    def __find_sequence_helper(self, player, row, col, seq, row_dir, col_dir):
        if seq == 4:
            # base case - we found a winning sequence
            return True
        if self.get_player_at(row, col) == 0:
            # base case - if the current location is empty, the sequence
            # has been broken
            return False
        if self.get_player_at(row, col) == player:
            # recursively check the next item in the sequence
            return self.__find_sequence_helper(player, row + row_dir,
                                        col + col_dir, seq + 1, row_dir,
                                        col_dir)

    def get_player_at(self, row, col):
        if 0 > row or row >= self.BOARD_ROWS or 0 > col or col >= \
                self.BOARD_COLUMNS:
            # if location isn't in the board
            return self.LOCATION_ERROR
        if self.__board[row][col] == 0:
            # if location is empty
            return None
        else:
            return self.__board[row][col]

    def get_current_player(self):
        return self.__cur_player


game = Game()
game.make_move(0)
game.make_move(1)
game.make_move(0)
game.make_move(1)
game.make_move(0)
game.make_move(1)
game.make_move(0)
a = game.get_winner()
print("")