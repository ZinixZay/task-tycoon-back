from fastapi import HTTPException

class UnauthorizedException(HTTPException):
    def __init__(self, message:str = 'UnauthorizedException'):
        super().__init__(status_code=401, detail=message)
