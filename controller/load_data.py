import os
import json
import logging
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, status, Depends, Security
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from immudb.client import ImmudbClient

load_dotenv()

logging.basicConfig(
    level=logging.DEBUG,  # Change to logging.INFO or logging.WARNING for less verbosity
    filename='LOGS/endpoint.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Security
security = HTTPBearer()

def validate_token(auth: HTTPAuthorizationCredentials = Security(security)):
    token = auth.credentials
    if token != os.getenv("GLOBAL_AUTH_TOKEN"):
        logging.error("Invalid token")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid or expired token")
    logging.info("Token validated successfully")

router = APIRouter(dependencies=[Depends(validate_token)])

# Initialize immudb client
immudb_user = os.getenv('IMMUDB_USERNAME')
immudb_password = os.getenv('IMMUDB_PASSWORD')
immudb_database = os.getenv('IMMUDB_DS1')

client = ImmudbClient()
try:
    client.login(immudb_user, immudb_password)
    logging.info("Logged into Immudb successfully.")
except Exception as e:
    logging.error("Failed to log into Immudb: %s", e)
    raise e

try:
    client.useDatabase(immudb_database)
    logging.info("Database selected successfully.")
except Exception as e:
    logging.error("Failed to select database: %s", e)
    raise e

@router.get("/api/v1/load/{session_id}")
async def load(session_id: str):
    try:
        logging.info(f"Attempting to retrieve session ID: {session_id}")
        response = client.get(session_id.encode())
        
        if response is None:
            logging.warning("Session ID not found: %s", session_id)
            raise HTTPException(status_code=404, detail="Session ID not found")

        data = json.loads(response.value.decode("utf-8"))
        logging.info(f"Session data retrieved and decoded successfully for session ID: {session_id}")
        return JSONResponse(content={"data": data}, status_code=status.HTTP_200_OK)
    except HTTPException as e:
        logging.error("HTTP exception occurred: %s", str(e))
        raise
    except Exception as e:
        logging.error("An error occurred: %s", str(e))
        return JSONResponse(content={"detail": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
