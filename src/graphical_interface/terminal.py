
import logging
import os

from ..core.user import User
from ..utils.errors import XOError
from ..core.game import XOGame

from colorama import Fore, Style, init
init(autoreset=True)

class TerminalGame(XOGame):
    def __init__(
            self,
            user_symbol_1: str,
            user_symbol_2: str,
            logger: None | logging.Logger
        ) -> None:
        super().__init__(user_symbol_1, user_symbol_2, logger)

    def display_xo_board(self):
        """Display the board in a readable and aligned format."""
        state = self.xo_board.state

        top_border = "┌───┬───┬───┐"
        mid_border = "├───┼───┼───┤"
        dwn_border = "└───┴───┴───┘"

        print(top_border)
        for i in range(0, len(state), 3):
            row = [
                self._render_value(state[j], j)
                for j in range(i, i + 3)
            ]
            print(f"│ {row[0]} │ {row[1]} │ {row[2]} │")
            if i < len(state) - 3:
                print(mid_border)
        print(dwn_border)

    def play_turn(self, cell: int) -> None | bool:
        """Start the game loop."""
        if self.get_move(cell) is True:
            result: User | None = self.return_winner()
            if result is None:
                self.logger.debug("It's a Draw!")
                return False
            else:
                self.logger.debug(
                    f"Congratulations **{result.user_symbol}**!"
                )
            return True
        return None

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
