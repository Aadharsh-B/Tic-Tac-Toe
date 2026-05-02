class User:
    def __init__(self, user_symbol: str, name: None | str = None):
        if not self.is_valid_symbol(user_symbol):
            raise ValueError('user_symbol must be a single non-whitespace character')

        self.user_symbol = user_symbol
        self.name = name or 'Player'

    @staticmethod
    def is_valid_symbol(symbol: str) -> bool:
        return isinstance(symbol, str) and len(symbol) == 1 and not symbol.isspace()

    def set_symbol(self, symbol: str):
        if not self.is_valid_symbol(symbol):
            raise ValueError('user_symbol must be a single non-whitespace character')
        self.user_symbol = symbol

    def set_name(self, name: str):
        self.name = name or self.name

    def to_dict(self) -> dict:
        return {'name': self.name, 'user_symbol': self.user_symbol}

    def __repr__(self):
        return f"User(name={self.name!r}, user_symbol={self.user_symbol!r})"
