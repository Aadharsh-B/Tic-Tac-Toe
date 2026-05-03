import logging
import time

from .errors import XOError
from colorama import init, Fore, Style

init(autoreset=True)
logger = logging.getLogger(__name__)


def get_user_id() -> int:
    while True:
        try:
            n = int(
                input(
                    "Do You Want To Play First? "
                    "(1 for Yes, 0 for No): ",
                )
            )
            if n not in {0, 1}:
                _msg = (
                    "Invalid Input. "
                    "`n` must be 1 or 0."
                )
                logger.info(_msg)
                raise ValueError(_msg)
            return n

        except ValueError:
            logger.info(
                f"{Fore.RED}Invalid Input."
                "Please enter 1 for Yes or 0 for No. "
                f"{Style.RESET_ALL}"
            )


def get_game_mode():
    """
    Recieves a Integer Input from the User to Select the Game Mode.
    
    1. Easy Bot
    2. Medium Bot
    3. Hard Bot
    4. Player vs Player

    Returns:
        1 (EasyBotAlgorithm) | 2 (MedBotAlgorithm) | 3 (HardBotAlgorithm) | 4 (XOGame):
            An Instance of the Selected Game Mode.
    """
    while True:
        try:
            n = int(
                input(
                    "Select Game Mode: "
                    "(\n"
                    "\t1 for Easy Bot,\n"
                    "\t2 for Medium Bot,\n"
                    "\t3 for Hard Bot,\n"
                    "\t4 for Player vs Player,\n"
                    "): ",
                )
            )
            if n not in {1, 2, 3, 4}:
                _msg = (
                    "Invalid Input. "
                    "`n` must be 1, 2, 3 or 4."
                )
                logger.debug(_msg)
                raise ValueError(_msg)
            return n

        except ValueError:
            _msg = (
                f"{Fore.RED}Invalid Input. \n"
                "Please Re-Enter a number between 1 and 4. "
                f"{Style.RESET_ALL}"
            )
            logger.info(_msg)


def play_user_game(g, logger: logging.Logger):
    while True:
        cell = g.get_and_validate_cell_id()
        g.clear_screen()
        try:
            result = g.play_turn(cell)
        except ValueError:
            msg = "Invalid input. Please enter a number between 1 and 9."
            logger.info(f"{Fore.RED}{msg}{Style.RESET_ALL}")
        except TypeError:
            msg = "Invalid Input. Please enter a Number between 1 and 9."
            logger.info(f"{Fore.RED}{msg}{Style.RESET_ALL}")
        except XOError as e:
            msg = "Error: Invalid Move! "
            logger.info(f"{Fore.RED}{msg}{Style.RESET_ALL}")
        else:
            if result is not None:
                break
        finally:
            g.display_xo_board()


def play_bot_game(g, logger: logging.Logger):
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
            logger.info(f"{Fore.RED}{msg}{Style.RESET_ALL}")
        except TypeError:
            msg = "Invalid Input. Please enter a Number between 1 and 9."
            logger.info(f"{Fore.RED}{msg}{Style.RESET_ALL}")
        except XOError as e:
            msg = "Error: Invalid Move! "
            logger.info(f"{Fore.RED}{msg}{Style.RESET_ALL}")
        else:
            if result is not None:
                break
        finally:
            g.display_xo_board()
