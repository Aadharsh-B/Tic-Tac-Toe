import logging
from src.utils.errors import XOError

class Board:
    WIN_COMBINATIONS = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6),
    ]

    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.state: list[None | str] = [None] * 9
        self._accepted_cell_ids: set[int] = set(range(1, 10))

    def register_action(self, cell_id: int, user_symbol: str) -> None:
        """Register a User Action in XOBoard.

        Args:
            cell_id (int): ID of Cell for Registering an Action (1-9).
            user_symbol (str): User Symbol that is to be Registered ('X' or 'O').

        Raises:
            XOError: If cell is occupied, invalid cell_id, or invalid user_symbol.
        """
        self.validate_cell_id(cell_id)

        self.state[cell_id - 1] = user_symbol
        self.logger.info(f"Registered '{user_symbol}' at cell {cell_id}.")
        
    def game_complete(self, user_symbol: str) -> bool:
        """Check if the given user has won the game.

        Args:
            user_symbol (str): User symbol to check for win.

        Returns:
            bool: True if the user has a winning combination.
        """
        return any(
            all(self.state[i] == user_symbol for i in combo)
            for combo in self.WIN_COMBINATIONS
        )

    def reset_board(self) -> None:
        """Reset the Board to Its Initial Empty State."""
        self.state = [None] * 9
        self.logger.info("Board has been Reset.")

    def is_full(self) -> bool:
        """Check if the board is full.

        Returns:
            bool: True if all cells are occupied.
        """
        return all(cell is not None for cell in self.state)

    def validate_cell_id(self, cell_id: int) -> None:
        """Validate that the selected cell is within the board range."""
        if cell_id not in self._accepted_cell_ids:
            _msg = f"Input ({cell_id}) is an Invalid cell ID (1-9)."
            self.logger.error(_msg)
            raise XOError(_msg)

        if self.state[cell_id - 1] is not None:
            _msg = f"Cell {cell_id} has Already been Played."
            self.logger.error(_msg)
            raise XOError(_msg)
