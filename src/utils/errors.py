class XOError(Exception):
    def __init__(self, msg):
        self.msg = msg
        super().__init__(msg)

    def __str__(self):
        return f"XOError: ({self.msg})"

class XOUserSymbolError(XOError):
    def __init__(self, msg):
        self.msg = msg
        super().__init__(msg)

    def __str__(self):
        return f"XOUserSymbolError: ({self.msg})"
