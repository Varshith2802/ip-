<<<<<<< HEAD
import os
import bcrypt
import requests
from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from pydantic import BaseModel, Field

# Determine the MongoDB connection details from environment variables
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("MONGO_DB_NAME", "ip_reputation_db")

# Pydantic models for request body validation
class UserIn(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)

class UserOut(BaseModel):
    username: str

# Connect to MongoDB
try:
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    users_collection = db["users"]
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    raise HTTPException(status_code=500, detail="Database connection failed.")

# Initialize FastAPI app
app = FastAPI(title="Auth Service")

# Add CORS middleware to allow requests from the frontend origin
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

@app.post("/register")
async def register_user(user: UserIn):
    """Register a new user with a hashed password."""
    # Check if the username already exists
    if users_collection.find_one({"username": user.username}):
        raise HTTPException(status_code=400, detail="Username already registered.")

    # Hash the password before storing
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    
    user_doc = {
        "username": user.username,
        "hashed_password": hashed_password.decode('utf-8')
    }
    
    users_collection.insert_one(user_doc)
    return {"message": "User registered successfully"}

@app.post("/login")
async def login_user(user: UserIn = Body(...)):
    """Authenticate a user and return a message on success."""
    db_user = users_collection.find_one({"username": user.username})

    # Check if the user exists and the password is correct
    if not db_user or not bcrypt.checkpw(user.password.encode('utf-8'), db_user["hashed_password"].encode('utf-8')):
        raise HTTPException(status_code=401, detail="Invalid username or password.")
    
    return {"message": "Login successful"}

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Authentication Service"}

@app.get("/check-reputation/{ip_address}")
async def check_ip_reputation(ip_address: str):
    """
    Checks the reputation of a given IP address using a third-party service and adds a custom reputation status.
    """
    try:
        response = requests.get(f"http://ip-api.com/json/{ip_address}")
        response.raise_for_status()
        data = response.json()

        # Simple, hardcoded reputation check for demonstration
        reputation = "Unknown"
        if data.get('query') in ['8.8.8.8', '1.1.1.1']:
            reputation = "Clean"
        elif data.get('query') in ['185.220.101.5', '192.99.1.11']:
            reputation = "Known Threat"
        
        data['reputation'] = reputation
        return data

    except requests.exceptions.RequestException as e:
        print(f"Error checking IP: {e}")
        raise HTTPException(status_code=500, detail="Could not check IP reputation.")
=======
import os
import bcrypt
import requests
from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from pydantic import BaseModel, Field

# Determine the MongoDB connection details from environment variables
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("MONGO_DB_NAME", "ip_reputation_db")

# Pydantic models for request body validation
class UserIn(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)

class UserOut(BaseModel):
    username: str

# Connect to MongoDB
try:
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    users_collection = db["users"]
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    raise HTTPException(status_code=500, detail="Database connection failed.")

# Initialize FastAPI app
app = FastAPI(title="Auth Service")

# Add CORS middleware to allow requests from the frontend origin
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

@app.post("/register")
async def register_user(user: UserIn):
    """Register a new user with a hashed password."""
    # Check if the username already exists
    if users_collection.find_one({"username": user.username}):
        raise HTTPException(status_code=400, detail="Username already registered.")

    # Hash the password before storing
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    
    user_doc = {
        "username": user.username,
        "hashed_password": hashed_password.decode('utf-8')
    }
    
    users_collection.insert_one(user_doc)
    return {"message": "User registered successfully"}

@app.post("/login")
async def login_user(user: UserIn = Body(...)):
    """Authenticate a user and return a message on success."""
    db_user = users_collection.find_one({"username": user.username})

    # Check if the user exists and the password is correct
    if not db_user or not bcrypt.checkpw(user.password.encode('utf-8'), db_user["hashed_password"].encode('utf-8')):
        raise HTTPException(status_code=401, detail="Invalid username or password.")
    
    return {"message": "Login successful"}

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Authentication Service"}

@app.get("/check-reputation/{ip_address}")
async def check_ip_reputation(ip_address: str):
    """
    Checks the reputation of a given IP address using a third-party service and adds a custom reputation status.
    """
    try:
        response = requests.get(f"http://ip-api.com/json/{ip_address}")
        response.raise_for_status()
        data = response.json()

        # Simple, hardcoded reputation check for demonstration
        reputation = "Unknown"
        if data.get('query') in ['8.8.8.8', '1.1.1.1']:
            reputation = "Clean"
        elif data.get('query') in ['185.220.101.5', '192.99.1.11']:
            reputation = "Known Threat"
        
        data['reputation'] = reputation
        return data

    except requests.exceptions.RequestException as e:
        print(f"Error checking IP: {e}")
        raise HTTPException(status_code=500, detail="Could not check IP reputation.")
>>>>>>> 4aac0aa (Initial commit: IP Reputation Checker microservices + Kubernetes manifests)
