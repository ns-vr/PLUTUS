from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import health, finance, insurance, fraud, reports

app = FastAPI(
    title="PLUTUS API",
    description="AI-Powered Financial & Health Crisis Prevention Network",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router,    prefix="/api/health",    tags=["Health Agent"])
app.include_router(finance.router,   prefix="/api/finance",   tags=["Finance Agent"])
app.include_router(insurance.router, prefix="/api/insurance", tags=["Insurance Agent"])
app.include_router(fraud.router,     prefix="/api/fraud",     tags=["Fraud Agent"])
app.include_router(reports.router,   prefix="/api/reports",   tags=["Reports"])


@app.get("/")
def root():
    return {"message": "PLUTUS API is running", "docs": "/docs"}
