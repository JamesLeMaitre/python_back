import mysql.connector
from fastapi import FastAPI, Response, Depends

from model import UserModel

app = FastAPI()

# Database configuration
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "python_db"
}


# Function to create database connection
def get_db():
    db = mysql.connector.connect(**db_config)
    try:
        yield db
    finally:
        db.close()


# Dependency for database cursor
def get_cursor(db: mysql.connector.connection = Depends(get_db)):
    return db.cursor()


# Function to format response
def formatter(status: int, message: str, data=None) -> dict:
    response = {"status": True if status in [200, 201] else False, "message": message}
    if data is not None:
        response["data"] = data
    return response


# GET endpoint to retrieve all data from a table
@app.get("/api/v1/users")
async def get_table_data(response: Response, cursor: mysql.connector.cursor = Depends(get_cursor)):
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]
    data = [dict(zip(column_names, row)) for row in results]
    response.status_code = 201
    return formatter(200, "Data retrieved successfully", data)


# POST endpoint to add data to a table
def insert_data(db, data):
    cursor = db.cursor()
    try:
        insert_query = "INSERT INTO users (firstname, lastname, address) VALUES (%s, %s, %s)"
        datas = (data.firstname, data.lastname, data.address)
        cursor.execute(insert_query, datas)
        db.commit()
        lastrowid = cursor.lastrowid
        cursor.execute(f"SELECT * FROM users WHERE id = {lastrowid}")
        result = cursor.fetchone()
        if result:
            result_dict = {
                "id": result[0],
                "firstname": result[1],
                "lastname": result[2],
                "address": result[3]
            }
            return True, result_dict
        else:
            return False, None
    except:
        return False, None


@app.post("/api/v1/users")
async def add_data(data: UserModel, response: Response, db: mysql.connector.connect = Depends(get_db)):
    success, result = insert_data(db, data)
    if success:
        response.status_code = 201
        return formatter(201, "Data added successfully", result)
    else:
        response.status_code = 400
        return formatter(400, "Failed to add data", {})


# GET endpoint to retrieve data by ID
@app.get("/api/v1/users/{id}")
async def get_table_data_by_id(id: int, response: Response, db: mysql.connector.connect = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM users WHERE id = {id}")
    result = cursor.fetchone()
    if result is None:
        return formatter(404, "Data not found")
    user = UserModel(id=result[0], firstname=result[1], lastname=result[2], address=result[3])
    response.status_code = 200
    return formatter(200, "Data retrieved successfully", user.dict())


@app.delete("/api/v1/users/{id}")
async def delete_table_data_by_id(id: int, response: Response, db: mysql.connector.connect = Depends(get_db)):
    cursor = db.cursor()
    try:
        cursor.execute(f"SELECT * FROM users WHERE id = {id}")
        result = cursor.fetchone()
        if result is None:
            response.status_code = 404
            return formatter(404, "Data not found")
        cursor.execute(f"DELETE FROM users WHERE id = {id}")
        db.commit()
        response.status_code = 200
        return formatter(200, "User delete successfully")

    except:
        response.status_code = 400
        return formatter(400, "Failed to delete data")


@app.put("/api/v1/users/{id}")
async def update_data_by_id(id: int, data: UserModel, response: Response,
                            db: mysql.connector.connect = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM users WHERE id = {id}")
    result = cursor.fetchone()
    if result is None:
        response.status_code = 404
        return formatter(404, "Data not found")
    update_query = "UPDATE users SET firstname=%s, lastname=%s, address=%s WHERE id=%s"
    update_data = (data.firstname, data.lastname, data.address, id)
    cursor.execute(update_query, update_data)
    if cursor.rowcount == 0:
        response.status_code = 404
        return formatter(404, "Data not found")
    db.commit()
    response.status_code = 200
    updated_data = {"id": id, "firstname": data.firstname, "lastname": data.lastname, "address": data.address}
    return formatter(200, "Data updated successfully", updated_data)
