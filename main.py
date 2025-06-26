from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas
from database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 1. Create student
@app.post("/students/", response_model=schemas.StudentOut)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    db_student = models.Student(**student.dict())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


# 2. Get all students
@app.get("/students/", response_model=list[schemas.StudentOut])
def get_students(db: Session = Depends(get_db)):
    return db.query(models.Student).all()

# 3. Update student
@app.put("/students/{student_id}", response_model=schemas.StudentOut)
def update_student(student_id: int, updated_student: schemas.StudentCreate, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    for key, value in updated_student.dict().items():
        setattr(student, key, value)
    db.commit()
    db.refresh(student)
    return student

# 4. Delete student
@app.delete("/students/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    db.delete(student)
    db.commit()
    return {"message": "Student deleted successfully"}

# 5. Create class information
@app.post("/classes/", response_model=schemas.ClassOut)
def create_class(classinfo: schemas.ClassCreate, db: Session = Depends(get_db)):
    db_class = models.ClassInfo(**classinfo.dict())
    db.add(db_class)
    db.commit()
    db.refresh(db_class)
    return db_class

# 6. Update class information
@app.put("/classes/{class_id}", response_model=schemas.ClassOut)
def update_class(class_id: int, updated_class: schemas.ClassCreate, db: Session = Depends(get_db)):
    db_class = db.query(models.ClassInfo).filter(models.ClassInfo.id == class_id).first()
    if not db_class:
        raise HTTPException(status_code=404, detail="Class not found")
    for key, value in updated_class.dict().items():
        setattr(db_class, key, value)
    db.commit()
    db.refresh(db_class)
    return db_class

# 7. Delete class information
@app.delete("/classes/{class_id}")
def delete_class(class_id: int, db: Session = Depends(get_db)):
    db_class = db.query(models.ClassInfo).filter(models.ClassInfo.id == class_id).first()
    if not db_class:
        raise HTTPException(status_code=404, detail="Class not found")
    db.delete(db_class)
    db.commit()
    return {"message": "Class deleted successfully"}

# 8. Registering student into class
@app.post("/register/", response_model=schemas.StudentClassOut)
def register_student_to_class(data: schemas.StudentClassCreate, db: Session = Depends(get_db)):
    
    student = db.query(models.Student).filter(models.Student.id == data.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    
    class_ = db.query(models.ClassInfo).filter(models.ClassInfo.class_name == data.class_name).first()
    if not class_:
        raise HTTPException(status_code=404, detail="Class not found")
    
    
    registration = models.StudentClass(student_id=student.id, class_id=class_.id)
    db.add(registration)
    db.commit()
    db.refresh(registration)


    return {
        "id": registration.id,
        "student_id": student.id,
        "class_name": class_.class_name
    }


#9. Get students in a class
@app.get("/classes/{class_id}/students/")
def get_students_in_class(class_id: int, db: Session = Depends(get_db)):
    registrations = db.query(models.StudentClass).filter(models.StudentClass.class_id == class_id).all()
    student_list = []
    for reg in registrations:
        student = db.query(models.Student).filter(models.Student.id == reg.student_id).first()
        if student:
            student_list.append({
                "id": student.id,
                "first_name": student.first_name,
                "middle_name": student.middle_name,
                "last_name": student.last_name,
                "age": student.age,
                "city": student.city
            })
    return student_list

@app.get("/")
def read_root():
    return {"message": "Hello"}




