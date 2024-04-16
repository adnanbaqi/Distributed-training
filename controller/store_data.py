from fastapi import APIRouter, HTTPException, status, File, UploadFile, Query
from fastapi.responses import JSONResponse
from immudb.client import ImmudbClient
import re
import os
<<<<<<< HEAD
import uuid  
import json  # Import for JSON handling

from dotenv import load_dotenv
load_dotenv()

router = APIRouter()

# Initialize Immudb client and fetch credentials from environment variables
immudb_user = os.getenv('IMMUDB_USERNAME')
immudb_password = os.getenv('IMMUDB_PASSWORD')
immudb_database = os.getenv('IMMUDB_DS1')

if immudb_user is None or immudb_password is None or immudb_database is None:
    raise ValueError("Environment variables IMMUDB_USERNAME, IMMUDB_PASSWORD, and IMMUDB_DS1 must be set.")

client = ImmudbClient()
client.login(immudb_user, immudb_password)

try:
    client.useDatabase(immudb_database)
    print(f'Using existing database "{immudb_database}".')
except Exception:
    try:
        client.createDatabase(immudb_database)
        client.useDatabase(immudb_database)
        print(f'Created and switched to database "{immudb_database}".')
    except Exception as e:
        print(f'Error creating or switching to database "{immudb_database}": {e}')
        raise
    
=======

router = APIRouter()

# Fetch credentials and database name from environment variables
immudb_user = os.getenv('IMMUDB_USERNAME')
immudb_password = os.getenv('IMMUDB_PASSWORD')
immudb_database = os.getenv('IMMUDB_DS1')

if immudb_user is None or immudb_password is None or immudb_database is None:
    raise ValueError("Environment variables IMMUDB_USERNAME, IMMUDB_PASSWORD, and IMMUDB_DS1 must be set.")

# Initialize Immudb client and login
client = ImmudbClient()
client.login(immudb_user, immudb_password)

# Try to use the specified database, assuming it exists
try:
    client.useDatabase(immudb_database)
    print(f'Using existing database "{immudb_database}".')
except Exception:
    # Assuming createDatabase does not throw an error if the database already exists,
    # or catching the specific exception if it does
    try:
        client.createDatabase(immudb_database)
        client.useDatabase(immudb_database)
        print(f'Created and switched to database "{immudb_database}".')
    except Exception as e:
        print(f'Error creating or switching to database "{immudb_database}": {e}')
        raise

>>>>>>> 7aa2d69bbe4397e655a20c8a90b2d3c45df56c0e
LANGUAGE_MAP = {
    ".py": "Python",
    ".js": "JavaScript",
    ".java": "Java",
    ".cpp": "C++",
    ".cs": "C#",
    ".rb": "Ruby",
    ".go": "Go",
    ".php": "PHP",
    ".ts": "TypeScript",
    ".html": "HTML",
    ".css": "CSS",
    ".sql": "SQL",
<<<<<<< HEAD
    ".txt": "Text",
    ".md": "Markdown",  # Example of an added type
=======
    ".txt": "TextExtension-Based_Unknown",
>>>>>>> 7aa2d69bbe4397e655a20c8a90b2d3c45df56c0e
    # Add more mappings as needed
}

def count_tokens(text):
    token_pattern = r'\b\w+\b|\d+|[+\-*/=<>!&|%^~]+'
    tokens = re.findall(token_pattern, text)
    return len(tokens)

def detect_language(filename):
    extension = filename.split('.')[-1].lower()
    return LANGUAGE_MAP.get(f".{extension}", "Unknown")
@router.post("/api/v1/store")
async def store(file: UploadFile = File(...), provider_id: str = Query(...), validator_id: str = Query(...)):
    try:
        session_id = uuid.uuid4().hex  # Generate a unique session ID
        content = await file.read()
        text = content.decode("utf-8")

        language = detect_language(file.filename)
        num_tokens = count_tokens(text)

        # Prepare data as JSON
        data_to_store = json.dumps({
            "text": text,
            "language": language,
            "num_tokens": num_tokens,
            "provider_id": provider_id,
            "validator_id": validator_id
        }).encode('utf-8')  # Encode the JSON as bytes

        # Store data in Immudb using session_id as the key
        client.set(session_id.encode(), data_to_store)  

        return JSONResponse(content={
            "message": "Code snippet stored successfully",
            "session_id": session_id,
            "language": language,
            "num_tokens": num_tokens,
            "provider_id": provider_id,
            "validator_id": validator_id
        }, status_code=status.HTTP_201_CREATED)
    except Exception as e:
        return JSONResponse(content={"detail": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
