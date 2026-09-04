from fastapi import APIRouter

from app.services.storage_service import get_patient_reports

router = APIRouter()


@router.get("/patient/{patient_id}/reports")
async def get_patient_historical_reports(patient_id: str):
    """
    Endpoint to fetch all historical reports for a given patient.
    """
    reports = get_patient_reports(patient_id)
    return {"reports": reports}
