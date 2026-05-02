import logging

from src import XOGame
from src.core import User
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

g = XOGame(
            user_1.user_symbol,
            user_2.user_symbol,
            logger,
        )

clear_screen()
g.display_xo_board()

try:
    while True:
        cell = g.get_and_validate_cell_id()
        g.clear_screen()
        try:
            result = g.play_turn(cell)
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
