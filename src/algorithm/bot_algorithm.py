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
