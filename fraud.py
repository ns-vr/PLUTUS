from fastapi import APIRouter
router = APIRouter()

@router.get("/status")
def fraud_status():
    return {"agent": "fraud", "status": "ready"}
