from .error import Error

class Result:
    def __init__(self, value=None, error: Error = None):
        self.value = value
        self.error = error

    @property
    def ok(self) -> bool:
        return self.error is None
    
    @property
    def failed(self) -> bool:
        return not self.ok

class Ok(Result):
    def __init__(self, value=None):
        super().__init__(value=value)

class Failure(Result):
    def __init__(self, error: Error):
        super().__init__(error=error)
