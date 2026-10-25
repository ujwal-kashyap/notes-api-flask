Flask Notes API

A RESTful Notes API built using Python, Flask, SQLAlchemy, and JWT authentication. Users can register, log in, and securely manage their personal notes.

Features
User registration with password hashing
User login with JWT authentication
Create a new note
Retrieve all notes belonging to the logged-in user
Retrieve a single note
Update an existing note
Delete a note
SQLite database integration
User-specific note access
Tech Stack
Python
Flask
Flask-SQLAlchemy
Flask-JWT-Extended
Werkzeug
SQLite
Project Structure
text
notes-api-flask/
├── notes_api.py
├── requirements.txt
├── .gitignore
└── README.md
Installation and Setup
1. Clone the repository
bash
git clone https://github.com/ujwal-kashyap/notes-api-flask.git
cd notes-api-flask

2. Create a virtual environment
Windows:
powershell
python -m venv venv
venv\Scripts\Activate.ps1
3. Install dependencies
bash
pip install -r requirements.txt
4. Configure environment variables
Set a strong, random JWT secret using an environment variable before running the application. Update the application configuration to read JWT_SECRET_KEY from the environment.
For local development, you can store this variable in a .env file and load it using python-dotenv. Never commit your .env file or secret to GitHub.
5. Run the application
bash
python notes_api.py
The API runs locally at:
http://127.0.0.1:3434
API Endpoints
Method	Endpoint	Description	Authentication
POST	/register	Register a user	No
POST	/login	Log in and receive a JWT	No
GET	/notes	Get all your notes	Yes
GET	/notes/<id>	Get a specific note	Yes
POST	/notes	Create a note	Yes
PUT	/notes/<id>	Update a note	Yes
DELETE	/notes/<id>	Delete a note	Yes
Example Requests
Register a user
POST /register
json
{
  "phone_no": "9876543210",
  "email": "user@example.com",
  "username": "testuser",
  "password": "your-password"
}

Log in

POST /login

json
{
  "email": "user@example.com",
  "password": "your-password"
}


The response includes an access_token.

Create a note

POST /notes

Include this header:

text
Authorization: Bearer YOUR_ACCESS_TOKEN
Content-Type: application/json


Request body:

json
{
  "title": "My First Note",
  "content": "This is my first note."
}

Get all notes

GET /notes

Include your JWT access token in the Authorization header.
Authentication
Protected endpoints require a valid JWT access token obtained from the login endpoint. Each user's notes are associated with their account, and the API filters note operations by the authenticated user's ID.
Database
The application uses SQLite and Flask-SQLAlchemy. The database tables are created automatically when the application starts.
Future Improvements
Add input validation and better error handling
Add pagination for notes
Add automated tests
Add API documentation with Swagger
Deploy the API to a hosting platform
Author
Ujwal Kashyap

GitHub: ujwal-kashyap

This project was built as a practical exercise in Flask REST APIs, database management, and JWT-based authentication.
