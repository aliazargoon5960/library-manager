from pydantic import BaseModel, Field, field_validator
import re

class BookSchema(BaseModel):
    title: str = Field(
        ..., 
        min_length=2, 
        max_length=100,
        description="عنوان کتاب"
    )

    author: str = Field(
        ..., 
        min_length=3,
        description="نام نویسنده"
    )
    
    isbn: str = Field(
        ...,
        description="شابک کتاب"
    )

    @field_validator('isbn')
    @classmethod
    def validate_isbn(cls, v):
        isbn_clean = v.strip()
        if not re.match(r"^\d{10}(\d{3})?$", isbn_clean):
            raise ValueError("شابک باید ۱۰ یا ۱۳ رقم عدد باشد")
        return isbn_clean

    class Config:
        str_strip_whitespace = True