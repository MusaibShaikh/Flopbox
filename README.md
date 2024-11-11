# Flopbox

Flopbox is a file upload and download application with separate backend and frontend services. The backend is built with FastAPI, and the frontend is developed using React and Material UI. The application allows users to upload, view, and download files, with authentication and authorization mechanisms.

## Table of Contents

- [Getting Started](#getting-started)
- [Backend Setup](#backend-setup)
- [Frontend Setup](#frontend-setup)
- [Database](#database)
- [Project Structure](#project-structure)
- [Notes](#notes)

## Getting Started

1. **Clone the repository**:

   ```bash
   git clone <repo-url>
   cd Flopbox

## Backend Setup

The backend is located in the Flopbox/app directory and is built with FastAPI.

### Features
The backend supports the following functionalities:

-User Registration: Create new users.
-User Login: Authenticate users.
-File Upload: Upload files associated with a user.
-List Files: Retrieve a list of files uploaded by the user.
-View File: View file details.
-Download File: Download a file uploaded by the user.

### Requirements
Python 3.8+
Docker (optional for using Docker Compose)

### Running the Backend
Navigate to the backend directory:

```bash
cd Flopbox/app
```
#### Install dependencies:
Install the dependencies using pip:

```bash
pip install -r requirements.txt
```
#### Run the backend
Run the backend using the following command
```bash
uvicorn main:app --reload
```
The backend server should be accessible at http://127.0.0.1:8000. API documentation is available at http://127.0.0.1:8000/docs.
You can test backend at http://127.0.0.1:8000/docs

## Frontend Setup
The frontend is located in the flopbox-frontend directory and is built with React.

### Running the Frontend
1. Navigate to frontend directory
```bash
cd flopbox-frontend
```

2. Install Dependencies
```bash
npm install
```

3. Start the frontend:
```bash
npm start
```

The frontend should be accessible at http://localhost:3000.

Note : For now frontend is not fully developed, but you are welcome to test the backend completely


## Functionalities:

1. The backend has register user and login user functionalities, it uses salted hash algorithm for authenticating the password
2. You can upload files and download files
3. You can view files for a particular user 
4. You can delete a uploaded file
5. You can view a particular file
