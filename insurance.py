from fastapi import APIRouter
router = APIRouter()

@router.get("/status")
def insurance_status():
    return {"agent": "insurance", "status": "ready"}
