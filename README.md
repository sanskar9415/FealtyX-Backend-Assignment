# FealtyX - Python Assignment

## Overview

This project is a REST API implemented in Python using FastAPI. The API performs basic **CRUD** (Create, Read, Update, Delete) operations on a list of students. It also integrates with the **Ollama** API to generate AI-based summaries for each student's profile. 

### Features
- Create a new student.
- Get all students.
- Get a student by ID.
- Update a student by ID.
- Delete a student by ID.
- Generate a detailed summary for a student using Ollama's Llama3 model.

### Technologies Used
- **FastAPI**: A modern, fast web framework for building APIs with Python.
- **Pydantic**: Data validation and settings management using Python type annotations.
- **Ollama**: Integrated for generating AI-based summaries for student profiles.
- **httpx**: HTTP client for making asynchronous requests to Ollama API.
- **Uvicorn**: ASGI server for serving the FastAPI application.

---

## Table of Contents
1. [Installation](#installation)
2. [Setup & Usage](#setup--usage)
3. [API Endpoints](#api-endpoints)
4. [Ollama Integration](#ollama-integration)
5. [Development Notes](#development-notes)

---

## Installation

### Prerequisites
Before getting started, you need to have the following installed on your machine:

- Python 3.7+ (Python 3.8+ is recommended)
- `pip` (Python package installer)

### Steps to Set Up the Project Locally

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/your-username/fealtyx-assignment.git
   cd fealtyx-assignment
Create and activate a virtual environment:

For Windows:

```bash
python -m venv venv
```
.\venv\Scripts\activate

Install the required dependencies using pip:

```bash
pip install fastapi pydantic httpx uvicorn
```


Run the FastAPI server:

```bash
uvicorn main:app --reload
```
The server will now be running at http://127.0.0.1:8000.

## API Endpoints

### Create a Student
```bash
curl.exe -X POST "http://127.0.0.1:8000/students" -H "Content-Type: application/json" -d "{\"id\": 1, \"name\": \"Sanskar\", \"age\": 22, \"email\": \"sanskargupta9415@gmail.com\"}"
```

### Get all studenta
```bash
curl.exe -X GET "http://127.0.0.1:8000/students"
```
### Get a Student by ID
```bash
curl.exe -X GET "http://127.0.0.1:8000/students/1"
```
### Update a Student
```bash
curl.exe -X PUT "http://127.0.0.1:8000/students/1" -H "Content-Type: application/json" -d "{\"id\": 1, \"name\": \"HEYYBRO\", \"age\": 56, \"email\": \"sanskargupta@gmail.com\"}"
```

### Delete a Student
```bash
curl.exe -X DELETE "http://127.0.0.1:8000/students/1"
```
### Get a Summary by ID
```bash
curl.exe -X GET "http://127.0.0.1:8000/students/1/summary"
```

Ollama Integration
This project integrates with Ollama, a powerful AI tool for generating summaries. To use the Ollama API, follow these steps:

Install Ollama on your machine by following the installation guide.
Install the Llama3 model using the following command:
bash
Copy code
ollama install llama3.2
The API will automatically send a request to the local Ollama server (http://localhost:11434) to generate a detailed summary for a student when the /students/{id}/summary endpoint is hit.
Development Notes
Concurrency: The FastAPI app uses asynchronous calls to interact with the Ollama API, allowing for efficient handling of concurrent requests.
Error Handling: The application provides appropriate error messages for invalid operations, such as trying to access a non-existent student or failing to connect to the Ollama API.
Data Storage: The student data is stored in memory using a Python dictionary. There is no need for a database for this project.
