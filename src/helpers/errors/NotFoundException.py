from fastapi import HTTPException

class NotFoundException(HTTPException):
    def __init__(self, message:str = 'NotFoundException'):
        super().__init__(status_code=403, detail=message)