from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from immudb.client import ImmudbClient
<<<<<<< HEAD
import os
import json  # Ensure json is imported for handling JSON data
from dotenv import load_dotenv

load_dotenv()

=======
import re
import os
>>>>>>> 7aa2d69bbe4397e655a20c8a90b2d3c45df56c0e
router = APIRouter()

# Initialize immudb client
immudb_user = os.getenv('IMMUDB_USERNAME')
immudb_password = os.getenv('IMMUDB_PASSWORD')
immudb_database = os.getenv('IMMUDB_DS1')
<<<<<<< HEAD
=======

client = ImmudbClient()
client.login(immudb_user, immudb_password)
client.useDatabase(immudb_database)
>>>>>>> 7aa2d69bbe4397e655a20c8a90b2d3c45df56c0e

client = ImmudbClient()
client.login(immudb_user, immudb_password)
client.useDatabase(immudb_database)

@router.get("/api/v1/load/{session_id}")
async def load(session_id: str):
    try:
        response = client.get(session_id.encode())
        
        if response is None:
            raise HTTPException(status_code=404, detail="Session ID not found")

        # Decode the stored JSON data
        data = json.loads(response.value.decode("utf-8"))  # Make sure to parse the JSON data correctly
        return JSONResponse(content={"data": data}, status_code=status.HTTP_200_OK)
    except Exception as e:
<<<<<<< HEAD
        return JSONResponse(content={"detail": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
=======
        # Handle exceptions
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/api/v1/load/{key}")
async def load(key: str):
    try:
        # Assuming `key` is already url-safe and correctly formatted
        response = client.get(key.encode())
        
        if response is None:
            raise HTTPException(status_code=404, detail="Key not found")
        
        # Access the correct attribute of the response object to get the byte string
        # This example assumes the attribute is named 'value', adjust as necessary
        byte_value = response.value  # Adjust this line based on the actual attribute name
        
        text = byte_value.decode("utf-8")
        return {"text": text}
    except Exception as e:
        return JSONResponse(content={"detail": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

>>>>>>> 7aa2d69bbe4397e655a20c8a90b2d3c45df56c0e
