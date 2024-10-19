from fastapi import Request, status, HTTPException


# Custom handler for ValueError
async def value_error_handler(request: Request, exc: ValueError):
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=str(exc),
    )


# Custom handler for generic server-side errors (500)
async def generic_exception_handler(request: Request, exc: Exception):
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=str(exc),
    )


class NotFoundError(Exception):
    def __init__(self, message):
        super().__init__(message)


# Custom handler for NotFoundError
async def not_found_error_handler(request: Request, exc: NotFoundError):
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=str(exc),
    )


class ForbiddenError(Exception):
    def __init__(self, message):
        super().__init__(message)


# Custom handler for ForbiddenError
async def forbidden_error_handler(request: Request, exc: ForbiddenError):
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=str(exc),
    )
