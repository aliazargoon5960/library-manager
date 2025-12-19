from pydantic import BaseModel, Field, validator

class BookSchema(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    author: str = Field(..., min_length=1, max_length=100)
    isbn: str = Field(...)

    @validator('isbn')
    def isbn_must_be_numeric_and_length(cls, v):
        if not v.isdigit():
            raise ValueError('ISBN باید فقط عدد باشد')
        if len(v) not in (10, 13):
            raise ValueError('ISBN باید ۱۰ یا ۱۳ رقم باشد')
        return v
