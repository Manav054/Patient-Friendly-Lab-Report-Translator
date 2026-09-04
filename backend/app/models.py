from pydantic import BaseModel, Field
from typing import List

class TestResult(BaseModel):
    marker_name: str = Field(..., description="The name of the test or biomarker (e.g., Hemoglobin, LDL Cholesterol).")
    value: float = Field(..., description="The numerical result of the test.")
    unit: str = Field(..., description="The unit of measurement (e.g., mg/dL, g/L).")
    reference_range_low: float | None = Field(None, description="The lower bound of the standard reference range, if available.")
    reference_range_high: float | None = Field(None, description="The upper bound of the standard reference range, if available.")
    is_abnormal: bool = Field(..., description="True if the value is outside the reference range, False otherwise.")
    layman_explanation: str = Field(..., description="A 1-2 sentence plain-English, jargon-free explanation of what this marker means, especially if out of range.")

class LabReportExtraction(BaseModel):
    patient_identifiers_found: bool = Field(..., description="True if any Personally Identifiable Information (PII) was detected and omitted.")
    tests: List[TestResult] = Field(..., description="List of extracted test results.")
    suggested_physician_questions: List[str] = Field(..., description="2-3 specific questions the patient should ask their doctor based on the results, particularly focusing on any abnormal values.")
