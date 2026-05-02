
import os
from colorama import Fore, Style

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
    print(f"{Fore.BLUE}Created by Aadharsh{Style.RESET_ALL}")
