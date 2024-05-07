# from fastapi import APIRouter, HTTPException, status, File, UploadFile, Query
# from fastapi.responses import JSONResponse
# from immudb.client import ImmudbClient
# import re
# import os
# import uuid
# import json
# import logging
# from dotenv import load_dotenv

# load_dotenv()

# logging.basicConfig(level=logging.INFO, filename='LOGS/endpoint.log', filemode='a',
#                     format='%(asctime)s - %(levelname)s - %(message)s')

# router = APIRouter()

# immudb_user = os.getenv('IMMUDB_USERNAME')
# immudb_password = os.getenv('IMMUDB_PASSWORD')
# immudb_database = os.getenv('IMMUDB_DS1')

# if immudb_user is None or immudb_password is None or immudb_database is None:
#     logging.error("Missing environment variables for Immudb credentials.")
#     raise ValueError("Environment variables IMMUDB_USERNAME, IMMUDB_PASSWORD, and IMMUDB_DS1 must be set.")

# client = ImmudbClient()
# client.login(immudb_user, immudb_password)

# try:
#     client.useDatabase(immudb_database)
#     logging.info(f'Using existing database "{immudb_database}".')
# except Exception as e:
#     try:
#         client.createDatabase(immudb_database)
#         client.useDatabase(immudb_database)
#         logging.info(f'Created and switched to database "{immudb_database}".')
#     except Exception as e:
#         error_message = f'Error creating or switching to database "{immudb_database}": {str(e)}'
#         logging.error(error_message, exc_info=True)
#         raise HTTPException(status_code=500, detail=error_message)

# LANGUAGE_MAP = {
#     ".py": "Python",
#     ".js": "JavaScript",
#     ".java": "Java",
#     ".cpp": "C++",
#     ".cs": "C#",
#     ".rb": "Ruby",
#     ".go": "Go",
#     ".php": "PHP",
#     ".ts": "TypeScript",
#     ".html": "HTML",
#     ".css": "CSS",
#     ".sql": "SQL",
#     ".txt": "Text",
#     ".md": "Markdown",
# }

# def count_tokens(text):
#     token_pattern = r'\b\w+\b|\d+|[+\-*/=<>!&|%^~]+'
#     tokens = re.findall(token_pattern, text)
#     return len(tokens)

# def detect_language(filename):
#     extension = filename.split('.')[-1].lower()
#     return LANGUAGE_MAP.get(f".{extension}", "Unknown")

# @router.post("/api/v1/store")
# async def store(file: UploadFile = File(...), provider_id: str = Query(...), validator_id: str = Query(...)):
#     try:
#         session_id = uuid.uuid4().hex
#         content = await file.read()
#         text = content.decode("utf-8")

#         language = detect_language(file.filename)
#         num_tokens = count_tokens(text)

#         data_to_store = json.dumps({
#             "text": text,
#             "language": language,
#             "num_tokens": num_tokens,
#             "provider_id": provider_id,
#             "validator_id": validator_id
#         }).encode('utf-8')

#         client.set(session_id.encode(), data_to_store)
#         logging.info(f"Stored data for session ID {session_id}")
#         return JSONResponse(content={
#             "message": "Code snippet stored successfully",
#             "session_id": session_id,
#             "language": language,
#             "num_tokens": num_tokens,
#             "provider_id": provider_id,
#             "validator_id": validator_id
#         }, status_code=status.HTTP_201_CREATED)
#     except Exception as e:
#         error_detail = {
#             "error": "Failed to store code snippet",
#             "exception": str(e),
#             "provider_id": provider_id,
#             "validator_id": validator_id
#         }
#         logging.error(f"Failed to store code snippet: {str(e)}", exc_info=True)
#         return JSONResponse(content=error_detail, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

from fastapi import APIRouter, HTTPException, status, File, UploadFile, Depends
from fastapi.responses import JSONResponse
from immudb.client import ImmudbClient
import re
import uuid
import json
import logging
import os
from dotenv import load_dotenv
from typing import Optional
from schemas.immudb_schema import StoreData  # Importing the schema

load_dotenv()

logging.basicConfig(
    level=logging.DEBUG,  # Change to logging.INFO or logging.WARNING for less verbosity
    filename='LOGS/endpoint.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

router = APIRouter()

immudb_user = os.getenv('IMMUDB_USERNAME')
immudb_password = os.getenv('IMMUDB_PASSWORD')
immudb_database = os.getenv('IMMUDB_DS1')

if immudb_user is None or immudb_password is None or immudb_database is None:
    logging.error("Missing environment variables for Immudb credentials.")
    raise ValueError("Environment variables IMMUDB_USERNAME, IMMUDB_PASSWORD, and IMMUDB_DS1 must be set.")

client = ImmudbClient()
client.login(immudb_user, immudb_password)

try:
    client.useDatabase(immudb_database)
    logging.info(f'Using existing database "{immudb_database}".')
except Exception as e:
    try:
        client.createDatabase(immudb_database)
        client.useDatabase(immudb_database)
        logging.info(f'Created and switched to database "{immudb_database}".')
    except Exception as e:
        error_message = f'Error creating or switching to database "{immudb_database}": {str(e)}'
        logging.error(error_message, exc_info=True)
        raise HTTPException(status_code=500, detail=error_message)

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
    ".txt": "Text",
    ".md": "Markdown",
}

def count_tokens(text):
    token_pattern = r'\b\w+\b|\d+|[+\-*/=<>!&|%^~]+'
    tokens = re.findall(token_pattern, text)
    return len(tokens)

def detect_language(filename):
    extension = filename.split('.')[-1].lower()
    return LANGUAGE_MAP.get(f".{extension}", "Unknown")

@router.post("/api/v1/store")
async def store(file: UploadFile = File(...), store_data: StoreData = Depends()):
    try:
        session_id = uuid.uuid4().hex
        content = await file.read()
        text = content.decode("utf-8")

        language = detect_language(file.filename)
        num_tokens = count_tokens(text)

        data_to_store = {
            "text": text,
            "language": language,
            "num_tokens": num_tokens,
            "provider_id": str(store_data.provider_id),
            "validator_id": str(store_data.validator_id),
            "wallet_id": str(store_data.wallet_id) if store_data.wallet_id else None
        }

        client.set(session_id.encode(), json.dumps(data_to_store).encode('utf-8'))
        logging.info(f"Stored data for session ID {session_id}")
        return JSONResponse(content={
            "message": "Code snippet stored successfully",
            "session_id": session_id,
            "language": language,
            "num_tokens": num_tokens,
            "provider_id": str(store_data.provider_id),
            "validator_id": str(store_data.validator_id),
            "wallet_id": str(store_data.wallet_id) if store_data.wallet_id else None
        }, status_code=status.HTTP_201_CREATED)
    
    except Exception as e:
        error_detail = {
            "error": "Failed to store code snippet",
            "exception": str(e),
            "provider_id": str(store_data.provider_id),
            "validator_id": str(store_data.validator_id),
            "wallet_id": str(store_data.wallet_id) if store_data.wallet_id else None
        }
        logging.error(f"Failed to store code snippet: {str(e)}", exc_info=True)
        return JSONResponse(content=error_detail, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
