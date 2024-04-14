class ApiNotEnabledException(Exception):
    def __init__(self, code: str, error: str):
        super().__init__(f"Error ({code}): {error}")
