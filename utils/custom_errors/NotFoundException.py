from fastapi import HTTPException

class NotFoundException(HTTPException):
    def __init__(self, message=None):
        detail = f'not found {message}'
        super().__init__(status_code=404, detail=detail)