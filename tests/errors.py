import sys
import traceback


# This file contains a list of possible errors
class UnexpectedCaseError(Exception):
    """Exception raised for impossible cases."""

    def __init__(self, message="Unexpected Case "):
        self.message = message
        _, _, tb = sys.exc_info()
        if tb:
            self.traceback = traceback.extract_tb(tb)
        else:
            self.traceback = traceback.extract_stack()[:-1]
        super().__init__(self.message)

    def __str__(self):
        if self.traceback:
            last_call = self.traceback[-1]
            return f"{self.message}at line {last_call.lineno} in {last_call.filename}"
        else:
            return self.message


class AssertionError(Exception):
    """Exception raised for impossible cases."""

    def __init__(self, expected, actual, message="Assertion error"):
        self.expected = expected
        self.actual = actual
        self.message = message

        # Get the traceback information
        _, _, tb = sys.exc_info()
        if tb:
            self.traceback = traceback.extract_tb(tb)
        else:
            self.traceback = traceback.extract_stack()[:-1]

        super().__init__(self.message)

    def __str__(self):
        if self.traceback:
            last_call = self.traceback[-1]
            return (
                f"{self.message}: {self.expected} != {self.actual} "
                f"at line {last_call.lineno} in {last_call.filename}"
            )
        else:
            return f"{self.message}: {self.expected} != {self.actual}"


class DirectionError(Exception):
    """Exception raised when the building direction of a boundary is incorrect (top left to bottom right)"""

    def __init__(self, boundary, relative_location, message="DirectionError"):
        self.boundary = boundary
        self.relative_location = relative_location
        self.message = message

        # Get the traceback information
        _, _, tb = sys.exc_info()
        if tb:
            self.traceback = traceback.extract_tb(tb)
        else:
            self.traceback = traceback.extract_stack()[:-1]

        super().__init__(self.message)

    def __str__(self):
        if self.traceback:
            last_call = self.traceback[-1]
            return (
                f'{self.message}: At boundary "{self.relative_location}", particularly {self.boundary} '
                f"at line {last_call.lineno} in {last_call.filename}"
            )
        else:
            return f"{self.message}: At boundary {self.relative_location}, particularly {self.boundary}"
