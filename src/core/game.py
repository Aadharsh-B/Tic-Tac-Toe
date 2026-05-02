import logging
import os

from colorama import Fore, Style, init
init(autoreset=True)

from src.core.board import Board
from src.core.user import User
from src.utils.errors import XOError, XOUserSymbolError

class XOGame:
    def __init__(
            self,
            user_symbol_1: str,
            user_symbol_2: str,
            logger: None | logging.Logger = None
        ) -> None:
        """Initialize an XO game."""
        self.logger = (
            logger
            if logger is not None
            else logging.getLogger(__name__)
        )

        self.xo_board = Board(self.logger)

        if user_symbol_1 == user_symbol_2:
            _msg = "Both Users cannot Play Using the Same Symbol."
            raise XOUserSymbolError(_msg)

        self.user_1: User = User(user_symbol_1)
        self.user_2: User = User(user_symbol_2)

        self.current_user: User = self.user_1

        # no initial victor
        self.winner = None

        self.is_draw = False
        self.is_over = False

    def game_reset(self):
        """Reset the game to a Starting State."""
        self.xo_board.reset_board()
        self.current_user = self.user_1

        self.winner = None

        self.is_draw = False
        self.is_over = False

    def get_move(self, cell_id: int) -> None | bool:
        """Handle the Current User's Move.

        Returns:
            True if the game is Finished.
            None if the game is Still Ongoing.
        Raises XOError if the Move is Invalid or the Game has Ended.
        """
        if self.is_over:
            raise XOError("Game is Already Complete.")

        symbol = self.current_user.user_symbol
        self.xo_board.register_action(cell_id, symbol)

        if self.xo_board.game_complete(symbol):
            self.winner = self.current_user
            self.is_over = True
            return True

        if self.xo_board.is_full():
            self.is_draw = True
            self.is_over = True
            return True

        self._switch_user()
        return None

    def _render_value(self, value: None | str, index: int) -> str:
        if value == self.user_1.user_symbol:
            return f"\033[32m{value}\033[0m"
        if value == self.user_2.user_symbol:
            return f"\033[31m{value}\033[0m"
        return f"\033[90m{index + 1}\033[0m"

    def _switch_user(self):
        """Switch the current player."""
        self.current_user = (
            self.user_2 if self.current_user == self.user_1 else self.user_1
        )

    def return_winner(self) -> None | User:
        """Return the winner of the game, if there is one."""
        if not self.is_over:
            raise XOError("Game is Not Yet Complete...")
        if self.is_draw:
            return None
        return self.winner
