class OrchestratorException(Exception):
    pass

class ExternalAPIError(OrchestratorException):
    def __init__(self, message: str, status_code: int = 502):
        self.message = message
        self.status_code = status_code
        super().__init__(message)

class ExternalAPITimeoutError(OrchestratorException):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)

class PartialFailureError(OrchestratorException):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)

class RuleNotFoundError(OrchestratorException):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)