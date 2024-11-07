from pydantic import BaseModel, EmailStr, Field

class Student(BaseModel):
    id: int = Field(..., gt=0, description="Student ID must be a positive integer.")
    name: str = Field(..., min_length=1, max_length=100, description="Name must be between 1 and 100 characters.")
    age: int = Field(..., gt=0, le=120, description="Age must be between 1 and 120.")
    email: EmailStr
