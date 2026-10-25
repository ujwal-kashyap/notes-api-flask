import os
from dotenv import load_dotenv
load_dotenv()
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity
)

app = Flask(__name__)
app.config["JWT_SECRET_KEY"]=os.getenv("JWT_SECRET_KEY")
jwt = JWTManager(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///notes.db"
db = SQLAlchemy(app)
class Notes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40), nullable=False)
    content = db.Column(db.String(80), nullable=False)
    user_id=db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False)
    def __repr__(self):
        return f"({self.id}-{self.title})"
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone_no=db.Column(db.String(20),nullable=False,unique=True)
    email=db.Column(db.String(50),nullable=False,unique=True)
    username=db.Column(db.String(30),nullable=False,unique=True)
    password=db.Column(db.String(50),nullable=False)
    notes=db.relationship("Notes",backref="user",lazy=True)
with app.app_context():
    db.create_all()
@app.post("/register")
def register():
    data=request.get_json()
    hashed_password =generate_password_hash(data["password"])
    user=User(phone_no=data['phone_no'],
    email=data['email'],
    username=data['username'],
    password=hashed_password)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message":"registered successfully"}), 201
@app.post("/login")
def login():
    data=request.get_json()
    user=User.query.filter_by(email=data["email"]).first()
    if not user:
        return jsonify ({'error':'user not found'}),401
    if not check_password_hash(user.password, data["password"]):
        return jsonify ({'error':'password is wrong'}),404
    access_token = create_access_token(identity=str(user.id))
    return jsonify ({'message':"login succesful",
         "access_token":access_token})
# GET Get all notes
@app.get("/notes")
@jwt_required()
def home():
    user_id=get_jwt_identity()
    notes = Notes.query.filter_by(user_id=int(user_id)).all()
    if not notes:
        return jsonify({"error": "notes not found"}), 404
    return jsonify([
        {
            "id": note.id,
            "title": note.title,
            "content": note.content
        }
        for note in notes
    ])
#GET  Get one note
@app.get("/notes/<int:n>")
@jwt_required()
def get_notes(n):
    note = Notes.query.get(n)
    user_id =get_jwt_identity()
    note = Notes.query.filter_by( id=n, user_id=int(user_id)).first()
    if not note:
        return jsonify({"error": "note not found"}), 404
    return jsonify({
        "id": note.id,
        "title": note.title,
        "content": note.content
    })
# POST  Create a new note
@app.post("/notes")
@jwt_required()
def add_note():
    data = request.get_json()

    if "title" not in data:
        return jsonify({"error": "title is required"}), 400
    if "content" not in data:
        return jsonify({"error": "content is required"}), 400
    user_id = get_jwt_identity()
    new_note = Notes(
        title=data["title"],
        content=data["content"],
        user_id=int(user_id)
    )
    db.session.add(new_note)
    db.session.commit()

    return jsonify({
        "id": new_note.id,
        "title": new_note.title,
        "content": new_note.content
    }), 201 
# PUT - Update a note
@app.put("/notes/<int:id>")
@jwt_required()
def update_note(id):
    data = request.get_json()
    user_id = get_jwt_identity()
    note = Notes.query.filter_by( id=id, user_id=int(user_id) ).first()
    if not note:
        return jsonify({"error": "note not found"}), 404
    if "title" in data:
        note.title = data["title"]
    if "content" in data:
        note.content = data["content"]
    db.session.commit()
    return jsonify({
        "id": note.id,
        "title": note.title,
        "content": note.content
    })
# DELETE  Delete a note
@app.delete("/notes/<int:id>")
@jwt_required()
def delete_note(id):
   
    user_id = get_jwt_identity()
    note = Notes.query.filter_by( id=id, user_id=int(user_id) ).first()
    if not note:
        return jsonify({"message": "note not found"}), 404
    db.session.delete(note)
    db.session.commit()
    return jsonify({
        "message": "note deleted successfully"
    })
if __name__ == "__main__":
    app.run(debug=True, port=3434)