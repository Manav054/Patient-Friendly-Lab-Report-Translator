from fastapi import APIRouter
from app.api.endpoints import report, patient, health

api_router = APIRouter()
api_router.include_router(report.router, tags=["report"])
api_router.include_router(patient.router, tags=["patient"])
api_router.include_router(health.router, tags=["health"])
