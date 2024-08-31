from fastapi import HTTPException

class ForbiddenException(HTTPException):
    def __init__(self, message:str = 'blank'):
        super().__init__(status_code=403, detail=message)