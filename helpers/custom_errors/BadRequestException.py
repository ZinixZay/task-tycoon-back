from fastapi import HTTPException

class BadRequestException(HTTPException):
    def __init__(self, message:str = 'blank'):
        super().__init__(status_code=400, detail=message)