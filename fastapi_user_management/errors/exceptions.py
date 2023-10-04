"""Define Custom errors here."""


class PasswordMatchError(Exception):
    """PasswordMatchError Custom error.

    Custom error that occur when new_password and its confirmation doesn't match.
    """

    def __init__(self, message: str = "Password doesn't match!") -> None:
        """Initiate custom error.

        Args:
            message (str): error message to display, \
                default is set to 'Password doesn't match!'.
        """
        self.message = message
        super().__init__(message)
