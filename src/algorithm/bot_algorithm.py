import logging
import random
from typing import Literal

from ..core.game import XOGame

class EasyBotAlgorithm(XOGame):
    def __init__(
            self,
            bot_symbol_number: Literal[1, 2],
            user_symbol_1: str,
            user_symbol_2: str,
            logger: None | logging.Logger = None,
        ) -> None:
        """Initialize a Bot Algorithm."""
        super().__init__(user_symbol_1, user_symbol_2, logger)
        if bot_symbol_number == 1:
            self.bot_symbol = user_symbol_1
        else:
            self.bot_symbol = user_symbol_2

    def get_move(self, cell_id: None | int = None) -> None | bool:
        if self.current_user.user_symbol == self.bot_symbol:
            
            # Bot's Move
            cell_id = self.bot_move
            if cell_id is not None:
                return super().get_move(cell_id)
            
            else:
            # `bot_move` is None,
            # Meaning the Board is Filled and the Bot Cannot make a Move
                self.is_over = True
                if self.xo_board.game_complete(self.bot_symbol):
                    self.winner = self.current_user
                if self.xo_board.is_full():
                    self.is_draw = True
                return True
        
        # User's Move
        if cell_id is None:
            msg = "Cell ID must be Provided for User's Move."
            self.logger.exception(msg)
            raise ValueError(msg)

        return super().get_move(cell_id)

    @property
    def bot_move(self) -> None | int:
        """Make a Random Move as a Easy Bot.

        Algorithm:
            1. Read through `self.xo_board.state` to find all Empty Cells.
            2. Randomly Select one of the Empty Cells and Register the Bot's Move.
        Returns:
            None | int: Cell ID of the Move if Successful,
            None if the Bot cannot make a move (Filled).
        """
        empty_cells = [
            idx + 1 for idx, cell in enumerate(self.xo_board.state)
            if cell is None
        ]

        if not empty_cells:
            return None

        return random.choice(empty_cells)


class HardBotAlgorithm(XOGame):

    MIN = -10
    MAX = 10

    def __init__(
            self,
            bot_symbol_number: Literal[1, 2],
            user_symbol_1: str,
            user_symbol_2: str,
            logger: None | logging.Logger = None,
        ) -> None:
        """Initialize a Bot Algorithm."""
        super().__init__(user_symbol_1, user_symbol_2, logger)
        # Assign a Symbol to the Bot `User_1` or `User_2`
        if bot_symbol_number == 1:
            self.bot_symbol = user_symbol_1
        else:
            self.bot_symbol = user_symbol_2

    def get_move(self, cell_id: None | int = None) -> None | bool:
        if self.current_user.user_symbol == self.bot_symbol:
            
            # Bot's Move
            cell_id = self.bot_move
            if cell_id is not None:
                return super().get_move(cell_id)
            
            else:
            # `bot_move` is None,
            # Meaning the Board is Filled and the Bot Cannot make a Move
                self.is_over = True
                if self.xo_board.game_complete(self.bot_symbol):
                    self.winner = self.current_user
                if self.xo_board.is_full():
                    self.is_draw = True
                return True
        
        # User's Move
        if cell_id is None:
            msg = "Cell ID must be Provided for User's Move."
            self.logger.exception(msg)
            raise ValueError(msg)

        return super().get_move(cell_id)

    def minimax(self, board, is_maximizing):

        bot_symbol = self.bot_symbol
        human_symbol = self._get_other_user_symbol(bot_symbol)

        if self.check_winner(board, bot_symbol):
            return 1
        elif self.check_winner(board, human_symbol):
            return -1
        elif self.check_draw(board):
            return 0

        if is_maximizing:
            best_score = self.MIN

            for i in range(9):
                if board[i] is None:
                    # try and move and reset the index
                    board[i] = bot_symbol
                    score = self.minimax(board, False)
                    board[i] = None
                    best_score = max(best_score, score)

            return best_score

        else:
            best_score = self.MAX

            for i in range(9):
                if board[i] is None:
                    # try and move and reset the index
                    board[i] = human_symbol
                    score = self.minimax(board, True)
                    board[i] = None
                    best_score = min(best_score, score)

            return best_score

    def check_full(self, board: list[str | None]):
        return None not in board

    def check_winner(self, board, user_symbol):
        WIN_COMBINATIONS = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 4, 8), (2, 4, 6),
        ]
        return any(
            all(board[i] == user_symbol for i in combo)
            for combo in WIN_COMBINATIONS
        )

    def check_draw(self, board):
        return all(cell is not None for cell in board)

    @property
    def bot_move(self) -> None | int:
        board = self.xo_board.state.copy()

        bot_symbol = self.bot_symbol

        best_score = self.MIN
        best_move = None

        for i in range(9):
            if board[i] is None:
                board[i] = bot_symbol
                score = self.minimax(board, False)
                board[i] = None

                if score > best_score:
                    best_score = score
                    best_move = i

        return None if best_move is None else best_move + 1




class MedBotAlgorithm(XOGame):

    MIN = -10
    MAX = 10

    def __init__(
            self,
            bot_symbol_number: Literal[1, 2],
            user_symbol_1: str,
            user_symbol_2: str,
            logger: None | logging.Logger = None,
        ) -> None:
        """Initialize a Bot Algorithm."""
        super().__init__(user_symbol_1, user_symbol_2, logger)
        # Assign a Symbol to the Bot `User_1` or `User_2`
        if bot_symbol_number == 1:
            self.bot_symbol = user_symbol_1
        else:
            self.bot_symbol = user_symbol_2
        
        # Flag to Alternate Random and UnBeatable Choices. (defaults `True`)
        self.flag = False

    def get_move(self, cell_id: None | int = None) -> None | bool:
        if self.current_user.user_symbol == self.bot_symbol:
            
            # Bot's Move
            cell_id = self.bot_move
            if cell_id is not None:
                return super().get_move(cell_id)
            
            # `bot_move` is None,
            # Meaning the Board is Filled and the Bot Cannot make a Move
            self.is_over = True
            if self.xo_board.game_complete(self.bot_symbol):
                self.winner = self.current_user
            if self.xo_board.is_full():
                self.is_draw = True
            return True
        
        # User's Move
        if cell_id is None:
            msg = "Cell ID must be Provided for User's Move."
            self.logger.exception(msg)
            raise ValueError(msg)

        return super().get_move(cell_id)

    def minimax(
            self,
            board: list[None | str],
            is_maximizing: bool,
            alpha: int,
            beta: int,
        ):
        bot_symbol = self.bot_symbol
        human_symbol = self._get_other_user_symbol(bot_symbol)

        if self.check_winner(board, bot_symbol):
            return 1
        elif self.check_winner(board, human_symbol):
            return -1
        elif self.check_draw(board):
            return 0

        if is_maximizing:
            best_score = self.MIN

            for i in range(9):
                if board[i] is None:
                    # try and move and reset the index
                    board[i] = bot_symbol
                    score = self.minimax(board, False, alpha, beta)
                    board[i] = None
                    best_score = max(best_score, score)

                    alpha = max(alpha, score)
                    if beta <= alpha:
                        break

            return best_score

        else:
            best_score = self.MAX

            for i in range(9):
                if board[i] is None:
                    # try and move and reset the index
                    board[i] = human_symbol
                    score = self.minimax(board, True, alpha, beta)
                    board[i] = None
                    best_score = min(best_score, score)

                    beta = min(beta, score)
                    if beta <= alpha:
                        break

            return best_score

    def check_full(self, board: list[str | None]):
        return None not in board

    def check_winner(self, board, user_symbol):
        WIN_COMBINATIONS = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 4, 8), (2, 4, 6),
        ]
        return any(
            all(board[i] == user_symbol for i in combo)
            for combo in WIN_COMBINATIONS
        )

    def check_draw(self, board):
        return all(cell is not None for cell in board)

    @property
    def bot_move(self) -> None | int:
        self.flag = not self.flag
        if self.flag:
            return self.random_move
        return self.best_move

    @property
    def random_move(self) -> None | int:
        empty_cells = [
            idx + 1 for idx, cell in enumerate(self.xo_board.state)
            if cell is None
        ]

        if not empty_cells:
            return None

        self.logger.debug("Tic-Tac-Toe (Medium AI) : Random Choice")
        return random.choice(empty_cells)

    @property
    def best_move(self) -> None | int:
        board = self.xo_board.state.copy()

        bot_symbol = self.bot_symbol

        best_score = self.MIN
        best_move = None

        for i in range(9):
            if board[i] is None:
                board[i] = bot_symbol
                score = self.minimax(board, False, self.MIN, self.MAX)
                board[i] = None

                if score > best_score:
                    best_score = score
                    best_move = i

        self.logger.debug("Tic-Tac-Toe (Medium AI) : minMax Optimal Choice")
        return None if best_move is None else best_move + 1
