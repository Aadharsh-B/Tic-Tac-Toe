import logging
import time

from src.core import User
from src.algorithm.bot_algorithm import EasyBotAlgorithm
from src.utils.errors import XOError, XOUserSymbolError
from src.utils.helper_functions_main import clear_screen, prompt_symbol, show_header

from colorama import init, Fore, Style

init(autoreset=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s"
)
logger = logging.getLogger(__name__)

show_header()

user_1 = User(prompt_symbol(1))
while True:
    try:
        user_2 = User(prompt_symbol(2))
        break
    except XOUserSymbolError as e:
        logger.info(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")

while True:
    try:
        n = int(
            input(
                "Do You Want To Play First? "
                "(1 for Yes, 0 for No): ",
            )
        )
        break
    except ValueError:
        logger.info(
            f"{Fore.RED}Invalid input."
            "Please enter 1 for Yes or 0 for No. "
            f"{Style.RESET_ALL}"
        )

g = EasyBotAlgorithm(
    1 if n == 0 else 2,
    user_1.user_symbol,
    user_2.user_symbol,
    logger,
)

clear_screen()
g.display_xo_board()

try:
    while True:
        if g.current_user.user_symbol == g.bot_symbol:
            logger.info(f"{Fore.RED}Bot's Turn... [Thinking]{Style.RESET_ALL}")
            time.sleep(2)
            cell = None  # Default ID for the Cell in Bot's Turn
        else:
            logger.info(f"{Fore.BLUE}Player's Turn...{Style.RESET_ALL}")
            cell = g.get_and_validate_cell_id()
        g.clear_screen()
        try:
            result = g.play_turn(cell) # pyright: ignore[reportArgumentType]
        except ValueError:
            msg = "Invalid input. Please enter a number between 1 and 9."
            print(f"{Fore.RED}{msg}{Style.RESET_ALL}")
        except TypeError:
            msg = "Invalid Input. Please enter a Number between 1 and 9."
            print(f"{Fore.RED}{msg}{Style.RESET_ALL}")
        except XOError as e:
            msg = "Error: Invalid Move! "
            print(f"{Fore.RED}{msg}{Style.RESET_ALL}")
        else:
            if result is not None:
                break
        finally:
            g.display_xo_board()

except KeyboardInterrupt:
    msg = "Game Interrupted by User. Exiting..."
    print(f"{Fore.BLUE}{msg}{Style.RESET_ALL}")


# Game Over : Display Result
msg = f"{g.current_user.user_symbol}'s Win! 🥶" if g.winner else "It's a Draw!"
print(f"\033[5m{Fore.BLUE}{msg}{Style.RESET_ALL}\033[0m")

print(
    "Thanks for Playing! \n"
    "Goodbye!"
)
