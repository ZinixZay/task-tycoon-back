from pydantic import BaseModel


class CustomBaseModel(BaseModel):
    class Config:
        use_enum_values = True
