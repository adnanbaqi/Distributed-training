from fastapi import APIRouter, HTTPException, Header, Depends
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from finetuning.finetuning import Training

import logging

# Load environment variables from .env file
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load the authentication token from environment variables
AUTH_TOKEN = os.getenv('AUTH_TOKEN')

if not AUTH_TOKEN:
    raise ValueError("No AUTH_TOKEN found in environment. Check your .env file.")

router = APIRouter()

class FinetuneRequest(BaseModel):
    session_id: str
    gpu_id: str

def valid_token(x_token: str = Header(...)):
    if x_token != AUTH_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid or missing token")

@router.post("/api/v1/finetune/", dependencies=[Depends(valid_token)])
async def finetune(request: FinetuneRequest):
    logging.info(f"Received finetuning request for session_id: {request.session_id} on gpu_id: {request.gpu_id}")
    try:
        success, message = await Training(request.session_id, request.gpu_id)
        if success:
            logging.info(f"Finetuning successful for session_id: {request.session_id}")
            return {"message": message}
        else:
            logging.error(f"Finetuning failed for session_id: {request.session_id}, error: {message}")
            raise HTTPException(status_code=500, detail=message)
    except Exception as e:
        logging.error(f"Unexpected error during finetuning for session_id: {request.session_id}, error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
