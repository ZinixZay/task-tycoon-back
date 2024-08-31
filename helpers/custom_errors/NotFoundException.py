from fastapi import HTTPException

class NotFoundException(HTTPException):
    def __init__(self, message:str = 'blank'):
        super().__init__(status_code=404, detail=message)