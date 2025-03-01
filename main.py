from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from dotenv import load_dotenv
import jwt
import bcrypt
import os
import uuid
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
CORS(app, origins = ["*"])

client = MongoClient(os.getenv("uri"))
db = client['CoriderAssessment-users']

secret = os.getenv("secret")

@app.post("/users")
def createUser():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name and not email and not password:
        return {"status":"details"}, 400
    checker = db.User.find_one({"email":email})
    if checker:
        return {"status":"email"}, 409
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    id = str(uuid.uuid4())[:40]
    creation = db.User.insert_one({"name":name, "email":email, "password":hashed.decode("utf-8"), "id":id})
    if not creation:
        return {"status":"server"}, 500
    return {"status":"success"}, 200

@app.get("/users/<id>")
def getOneUsers(id):
    return {"users" :db.User.find_one({"id":id}, {"_id":0})}, 200

@app.get("/users")
def getAllUsers():
    return {"users":list(db.User.find({}, {"_id":0}))}, 200

@app.put("/users/<id>")
def updateUser(id):
    # try:
    data = request.get_json()
    checker = db.User.find({"id":id})
    content = data.get("content")
    if not checker:
        return {"status":"id"}, 404
    content['password'] = bcrypt.hashpw(content['password'].encode("utf-8"), salt=bcrypt.gensalt()).decode("utf-8")
    db.User.update_one({"id":id}, {"$set":content})
    return {"user":"success"}, 200
    # except:
    #     return {"status":"fail"}, 500

@app.delete("/users/<id>")
def deleteUser(id):
    try:
        checker = db.User.find({"id":id})
        if not checker:
            return {"status":"id"}, 404
        db.User.delete_one({"id":id})
        return {"status":"success"}, 200
    except:
        return {"status":"fail"}, 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)