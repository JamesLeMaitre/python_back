from datetime import datetime
from typing import List, Optional, Dict, Union
from fastapi import FastAPI, Response
from pydantic import BaseModel
import mysql.connector


class UserModel(BaseModel):
    firstname: str
    lastname: str
    address: str
    date_create: Optional[datetime] = None
    date_update: Optional[datetime] = None


class User:
    def __init__(self, db):
        self.db = db

    def get_user_by_id(self, id: int) -> Optional[Dict]:
        cursor = self.db.cursor()
        cursor.execute(f"SELECT * FROM users WHERE id = {id}")
        result = cursor.fetchone()
        if result is None:
            return None
        user = {"id": result[0], "firstname": result[1], "lastname": result[2], "address": result[3], "date_create": result[4], "date_update": result[5]}
        return user

    def get_all_users(self) -> List[Dict]:
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        users = []
        for result in results:
            user = {"id": result[0], "firstname": result[1], "lastname": result[2], "address": result[3], "date_create": result[4], "date_update": result[5]}
            users.append(user)
        return users

    def add_user(self, user: UserModel) -> int:
        cursor = self.db.cursor()
        insert_query = "INSERT INTO users (firstname, lastname, address, date_create) VALUES (%s, %s, %s, %s)"
        date_create = datetime.now()
        insert_data = (user.firstname, user.lastname, user.address, date_create)
        cursor.execute(insert_query, insert_data)
        self.db.commit()
        return cursor.lastrowid

    def update_user(self, id: int, user: UserModel) -> Optional[Dict]:
        cursor = self.db.cursor()
        update_query = "UPDATE users SET firstname = %s, lastname = %s, address = %s, date_update = %s WHERE id = %s"
        date_update = datetime.now()
        update_data = (user.firstname, user.lastname, user.address, date_update, id)
        cursor.execute(update_query, update_data)
        self.db.commit()

        updated_user = self.get_user_by_id(id)
        if not updated_user:
            return None
        return updated_user

    def delete_user(self, id: int) -> None:
        cursor = self.db.cursor()
        delete_query = "DELETE FROM users WHERE id = %s"
        delete_data = (id,)
        cursor.execute(delete_query, delete_data)
        self.db.commit()


app = FastAPI()
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="python_db"
)
user = User(db)


def formatter(status: bool, message: str, data: Optional[Union[Dict, List]]) -> Dict:
    return {"status": status, "message": message, "data": data}


@app.get("/api/v1/users")
async def get_all_users(response: Response):
    try:
        users = user.get_all_users()
        if not users:
            response.status_code = 404
            return formatter(False, "No users found", None)
        response.status_code = 200
        return formatter(True, "Users retrieved successfully", users)
    except:
        response.status_code = 500
        return formatter(False, "Internal Server Error", None)


@app.get("/api/v1/users/{id}")
async def get_user_by_id(id: int, response: Response):
    try:
        user_by_id = user.get_user_by_id(id)
        if not user_by_id:
            response.status_code = 404
            return formatter(False, "User not found", None)
        response.status_code = 200
        return formatter(True, "User retrieved successfully", user_by_id)
    except:
        response.status_code = 500
        return formatter(False, "Internal Server Error", None)


@app.delete("/api/v1/users/{id}")
async def delete_user_by_id(id: int, response: Response):
    try:
        user.delete_user(id)
        response.status_code = 200
        return formatter(True, "User deleted successfully", None)
    except:
        response.status_code = 500
        return formatter(False, "Internal Server Error", None)


@app.put("/api/v1/users/{id}")
async def update_user_by_id(id: int, user: UserModel, response: Response):
    try:
        updated_user = user.update_user(id, user)
        if not updated_user:
            response.status_code = 404
            return formatter(False, "User not found", None)
        response.status_code = 200
        return formatter(True, "User updated successfully", updated_user)
    except:
        response.status_code = 500
        return formatter(False, "Internal Server Error", None)


@app.post("/api/v1/users")
async def add_user(user: UserModel, response: Response):
    try:
        User(db).add_user(user)
        new_user = User(db).get_user_by_id(User(db).add_user(user))
        response.status_code = 201
        return formatter(True, "User added successfully", new_user)
    except:
        response.status_code = 500
        return formatter(False, "Internal Server Error", None)

