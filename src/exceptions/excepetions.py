from fastapi import HTTPException, status


class UnauthorizedException(HTTPException):

    def __init__(self, detail: str) -> None:
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED,
                         detail={'message': detail})


class BadRequestException(HTTPException):

    def __init__(self, detail: str) -> None:
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST,
                         detail={'message': detail})


class NotFoundException(HTTPException):

    def __init__(self, detail: str) -> None:
        super().__init__(status_code=status.HTTP_404_NOT_FOUND,
                         detail={'message': detail})