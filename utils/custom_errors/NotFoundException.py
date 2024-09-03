from fastapi import HTTPException

class NotFoundException(HTTPException):
    def __init__(self, message: dict = {}):
        message["message"] = message.get("message", "not found")
        super().__init__(status_code=404, detail=message)