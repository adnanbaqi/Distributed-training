from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from finetuning.finetuning import Training  # Ensure this import works based on your project setup

router = APIRouter()

class FinetuneRequest(BaseModel):
    session_id: str
    gpu_id: str

@router.post("/api/v1/finetune/")
async def finetune(request: FinetuneRequest):
    success, message = await Training(request.session_id, request.gpu_id)
    if success:
        return {"message": message}
    else:
        raise HTTPException(status_code=500, detail=message)

