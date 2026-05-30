"""
Reports Route
-------------
POST /api/reports/analyze
Accepts uploaded documents, runs all four agents in parallel,
and returns the unified risk report.
"""

from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
import asyncio

from agents.health_agent    import analyze_health_documents
from agents.finance_agent   import analyze_finance_documents
from agents.insurance_agent import analyze_insurance_documents
from agents.fraud_agent     import analyze_transactions
from risk_engine.scorer     import AgentScores, calculate_cpi

router = APIRouter()


@router.post("/analyze")
async def analyze_documents(files: List[UploadFile] = File(...)):
    """
    Upload one or more documents (PDF, image, CSV).
    Returns the full Crisis Prevention Report.
    """
    if not files:
        raise HTTPException(status_code=400, detail="No files uploaded.")

    # Extract text from all uploaded files (simplified — use a real parser in prod)
    combined_text = ""
    for f in files:
        content = await f.read()
        combined_text += content.decode("utf-8", errors="ignore") + "\n"

    # Run all four agents concurrently
    loop = asyncio.get_event_loop()
    health_result, finance_result, insurance_result, fraud_result = await asyncio.gather(
        loop.run_in_executor(None, analyze_health_documents,    combined_text),
        loop.run_in_executor(None, analyze_finance_documents,   combined_text),
        loop.run_in_executor(None, analyze_insurance_documents, combined_text),
        loop.run_in_executor(None, analyze_transactions,        combined_text),
    )

    # Build scores (placeholder extraction — parse agent JSON in production)
    scores = AgentScores(
        health_score=50.0,         # replace with parsed health_result["risk_score"]
        finance_score=60.0,        # replace with parsed finance_result["risk_score"]
        insurance_gap_score=40.0,  # replace with parsed insurance_result["gap_score"]
        fraud_score=20.0,          # replace with parsed fraud_result["fraud_score"]
    )

    report = calculate_cpi(scores)

    return {
        "report": {
            "crisis_probability_index": report.crisis_probability_index,
            "risk_category":            report.risk_category,
            "primary_risk":             report.primary_risk,
            "summary":                  report.summary,
            "scores": {
                "health":    report.health_score,
                "finance":   report.finance_score,
                "insurance": report.insurance_gap_score,
                "fraud":     report.fraud_score,
            },
        },
        "agent_outputs": {
            "health":    health_result,
            "finance":   finance_result,
            "insurance": insurance_result,
            "fraud":     fraud_result,
        },
    }
