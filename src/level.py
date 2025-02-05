from src.board import boards


class Level:
    def __init__(self, level_index):
        self.boards_count = len(boards)
        if self.boards_count > level_index:    
            self.current_level_index = level_index
        else: #TODO throw
            pass

        self.board = boards[self.current_level_index]

        self.rows_count = len(self.board)
        self.cols_count = len(self.board[0])

        self.square_size = 50