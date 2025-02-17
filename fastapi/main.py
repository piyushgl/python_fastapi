from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# Pydantic Model
class Student(BaseModel):
    fname: str
    lname: str
    roll_nbr: int

# Response Model
class StudentResponse(BaseModel):
    fname: str
    lname: str
    roll_nbr: int
    message: str = "Success"

# In-memory storage (replace with database in production)
students_db = []

@app.post("/students/", response_model=StudentResponse)
async def add_student(student: Student):
    # Check if student already exists
    if any(s.roll_nbr == student.roll_nbr for s in students_db):
        raise HTTPException(
            status_code=400,
            detail=f"Student with roll number {student.roll_nbr} already exists"
        )
    
    students_db.append(student)
    return StudentResponse(
        fname=student.fname,
        lname=student.lname,
        roll_nbr=student.roll_nbr,
        message="Student added successfully"
    )

@app.delete("/students/{roll_nbr}", response_model=StudentResponse)
async def remove_student(roll_nbr: int):
    for student in students_db:
        if student.roll_nbr == roll_nbr:
            students_db.remove(student)
            return StudentResponse(
                fname=student.fname,
                lname=student.lname,
                roll_nbr=student.roll_nbr,
                message="Student removed successfully"
            )
    
    raise HTTPException(
        status_code=404,
        detail=f"Student with roll number {roll_nbr} not found"
    )

@app.get("/students/{roll_nbr}", response_model=StudentResponse)
async def search_student(roll_nbr: int):
    for student in students_db:
        if student.roll_nbr == roll_nbr:
            return StudentResponse(
                fname=student.fname,
                lname=student.lname,
                roll_nbr=student.roll_nbr,
                message="Student found"
            )
    
    raise HTTPException(
        status_code=404,
        detail=f"Student with roll number {roll_nbr} not found"
    )

@app.get("/students/", response_model=List[StudentResponse])
async def get_all_students():
    if not students_db:
        raise HTTPException(
            status_code=404,
            detail="No students found"
        )
    return [StudentResponse(**student.dict()) for student in students_db] 