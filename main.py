import logging

from src.core import User, XOGame
from src.algorithm.bot_algorithm import (
    EasyBotAlgorithm,
    MedBotAlgorithm,
    HardBotAlgorithm,
)
from src.utils.errors import XOError, XOUserSymbolError
from src.utils.helper_functions_main import clear_screen, prompt_symbol, show_header
from src.utils.helper_prompt_functions import (
    get_user_id,
    get_game_mode,
    play_bot_game,
    play_user_game,
)

from colorama import init, Fore, Style

init(autoreset=True)

GAME_MODES = {
    1: (EasyBotAlgorithm, 'Easy Bot Mode'),
    2: (MedBotAlgorithm, 'Medium Bot Mode'),
    3: (HardBotAlgorithm, 'Hard Bot Mode'),
    4: (XOGame, 'Player vs Player Mode'),
}

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s"
)
logger = logging.getLogger(__name__)

show_header()

# Get User Symbols
user_1 = User(prompt_symbol(1))
while True:
    try:
        user_2 = User(prompt_symbol(2))
        break
    except XOUserSymbolError as e:
        logger.info(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")


game_mode = get_game_mode()

if game_mode == 4:
    g = XOGame(
        user_1.user_symbol,
        user_2.user_symbol,
        logger,
    )
else:
    n = get_user_id()

    cls, msg = GAME_MODES[game_mode]
    logger.info(f"{Fore.GREEN}Selected Game Mode: {msg}{Style.RESET_ALL}")
    g = cls(
        1 if n == 0 else 2,
        user_1.user_symbol,
        user_2.user_symbol,
        logger,
    )

clear_screen()
g.display_xo_board()

try:
    if game_mode == 4:
        play_user_game(g, logger)
    else:
        play_bot_game(g, logger)
except KeyboardInterrupt:
    msg = "Game Interrupted by User. Exiting..."
    logger.info(f"{Fore.BLUE}{msg}{Style.RESET_ALL}")


# Game Over : Display Result
msg = f"{g.current_user.user_symbol}'s Win! 🥶" if g.winner else "It's a Draw!"
logger.info(f"\033[5m{Fore.BLUE}{msg}{Style.RESET_ALL}\033[0m")

logger.info(
    "Thanks for Playing! \n"
)
