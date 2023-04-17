class ResponseException(Exception):
    def __init__(self, status_code, error_message=""):
        self.error_message = error_message
        self.status_code = status_code

    def __str__(self) -> str:
        return self.error_message + ", " + f"HTTP response returned status code {self.status_code}"
