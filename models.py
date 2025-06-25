from sqlalchemy import Column, Integer, String, Date
from database import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True) 
    first_name = Column(String)
    middle_name = Column(String)
    last_name = Column(String)
    age = Column(Integer)
    city = Column(String)

class ClassInfo(Base):
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True, index=True)  
    class_name = Column(String)
    description = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)
    number_of_hours = Column(Integer)

class StudentClass(Base):
    __tablename__ = "student_classes"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    class_id = Column(Integer, ForeignKey("classes.id"))

    


