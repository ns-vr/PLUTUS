from fastapi import APIRouter
router = APIRouter()

@router.get("/status")
def health_status():
    return {"agent": "health", "status": "ready"}
