from pydantic import BaseModel
from typing import Optional
from datetime import date

# Schema for creating a student
class StudentCreate(BaseModel):
    first_name: str
    middle_name: Optional[str] = None
    last_name: str
    age: int
    city: str

# Schema for returning a student
class StudentOut(StudentCreate):
    id: int

    class Config:
        orm_mode = True


# Schema for creating a class
class ClassCreate(BaseModel):
    class_name: str
    description: Optional[str] = None
    start_date: date
    end_date: date
    number_of_hours: int

# Schema for returning a class
class ClassOut(ClassCreate):
    id: int

    class Config:
        orm_mode = True

# Schema for registration
class StudentClassCreate(BaseModel):
    student_id: int
    class_name: str

class StudentClassOut(BaseModel): 
    id: int
    student_id: int
    class_name: str

    class Config:
        orm_mode = True


