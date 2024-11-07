from fastapi import FastAPI, HTTPException
from models import Student
from typing import List
import httpx
import logging
import json
from fastapi.middleware.cors import CORSMiddleware


logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

app = FastAPI()

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

students = {}


@app.post("/students", response_model=Student)
def create_student(student: Student):
    if student.id in students:
        logger.warning(f"Attempt to create student with duplicate ID: {student.id}")
        raise HTTPException(status_code=400, detail="Student with this ID already exists.")
    students[student.id] = student
    logger.info(f"Created student: {student}")
    return student


@app.get("/students", response_model=List[Student])
def get_all_students():
    logger.info("Fetching all students.")
    return list(students.values())


@app.get("/students/{id}", response_model=Student)
def get_student(id: int):
    if id not in students:
        logger.warning(f"Student with ID {id} not found.")
        raise HTTPException(status_code=404, detail="Student not found.")
    logger.info(f"Fetched student with ID {id}: {students[id]}")
    return students[id]


@app.delete("/students/{id}", status_code=204)
def delete_student(id: int):
    if id not in students:
        logger.warning(f"Attempt to delete student with ID {id} not found.")
        raise HTTPException(status_code=404, detail="Student not found.")
    del students[id]
    logger.info(f"Deleted student with ID {id}")
    return {"detail": "Student deleted successfully"}


@app.put("/students/{id}", response_model=Student)
def update_student(id: int, student: Student):
    if id not in students:
        logger.warning(f"Attempt to update student with ID {id} not found.")
        raise HTTPException(status_code=404, detail="Student not found.")
    students[id].name = student.name
    students[id].age = student.age
    students[id].email = student.email
    logger.info(f"Updated student with ID {id}: {students[id]}")
    return students[id]



@app.get("/students/{id}/summary")
async def generate_summary(id: int):
    if id not in students:
        logger.warning(f"Student with ID {id} not found for summary generation.")
        raise HTTPException(status_code=404, detail="Student not found.")

    student = students[id]
    prompt_content = (
        f"Generate a detailed summary based on the following details for the student:\n"
        f"Name: {student.name}\n"
        f"Age: {student.age}\n"
        f"Email: {student.email}\n"
        f"Do not mention any generic or missing information, just create a professional summary based on the provided data."
    )

    try:
        logger.info(f"Sending request to Ollama API with prompt: {prompt_content}")

        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://localhost:11434/api/chat",
                json={
                    "model": "llama3.2",
                    "messages": [{"role": "user", "content": prompt_content}]
                },
                timeout=60.0,
            )
            response.raise_for_status()
            logger.info(f"Ollama API response status: {response.status_code}")

            summary_content = ""
            for line in response.iter_lines():
                if line:
                    try:
                        message_data = json.loads(line)
                        summary_content += message_data.get("message", {}).get("content", "")
                        if message_data.get("done"):
                            logger.info("Summary generation completed successfully.")
                            break
                    except json.JSONDecodeError as e:
                        logger.error(f"JSON parsing error for line: {line} - {e}")
                        continue

            return {"summary": summary_content.strip()}
    except httpx.RequestError as e:
        logger.error(f"Error connecting to Ollama API: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error connecting to Ollama API: {str(e)}")
    except ValueError as json_error:
        logger.error(f"JSON parsing error: {str(json_error)}")
        raise HTTPException(status_code=500, detail="Error parsing response from Ollama API.")
