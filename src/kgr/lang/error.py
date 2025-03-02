class Error:
    def __init__(self, message: str, file_location: str):
        self.message = message
        self.file_location = file_location
        self.children = []

    def add_child(self, error: 'Error'):
        self.children.append(error)

    def __str__(self):
        child_str = "\n".join("  " + str(child) for child in self.children)
        return f"{self.message} ({self.file_location})" + (f"\n{child_str}" if self.children else "")
