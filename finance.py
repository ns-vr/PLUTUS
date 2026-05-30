from fastapi import APIRouter
router = APIRouter()

@router.get("/status")
def finance_status():
    return {"agent": "finance", "status": "ready"}
