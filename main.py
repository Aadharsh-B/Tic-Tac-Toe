import logging
import os

from src import TerminalGame
from src.core import User
from src.utils.errors import XOError, XOUserSymbolError

from colorama import init, Fore, Style


init(autoreset=True)


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def prompt_symbol(
        player_number,
        is_retry = False,
    ) -> str:
    msg = (
        f"{Fore.CYAN}"
        "Enter symbol for User"
        f"{player_number}{Style.RESET_ALL}: "
    )
    if is_retry:
        msg = (
            f"{Fore.YELLOW}"
            "Symbol already Taken. "
            "Please Choose a Different Symbol for User "
            f"{player_number}{Style.RESET_ALL}: "
        )

    while True:
        symbol = input(msg).strip()
        if symbol:
            return symbol[0]

        print(
            f"{Fore.YELLOW}"
            "Please Enter at Least 1 Character."
            "{Style.RESET_ALL}"
        )


def show_header():
    clear_screen()
    print(f"Tic-Tac-Toe")


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
        g = TerminalGame(
            user_1.user_symbol,
            user_2.user_symbol,
            logger,
        )
        break
    except XOUserSymbolError as e:
        logger.info(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")

clear_screen()
g.display_xo_board()

try:
    while True:
        cell = int(
            input(
                f"{g.current_user.user_symbol}'s Turn. "
                "Enter a Cell ID in between (1-9): "
            )
        )
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


msg = f"{g.current_user.user_symbol}'s Win! 🥶" if g.winner else "It's a Draw!"
print(f"\033[5m{Fore.BLUE}{msg}{Style.RESET_ALL}\033[0m")

print(
    "Thanks for Playing! \n"
    "Goodbye!"
)
