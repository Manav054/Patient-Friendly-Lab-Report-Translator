from fastapi import APIRouter, File, Form, HTTPException, Query, UploadFile

from app.services.gemini_service import analyze_lab_report_images
from app.services.pdf_service import process_file_to_images
from app.services.storage_service import get_report, save_report

router = APIRouter()


@router.post("/analyze-report")
async def analyze_report(
    file: UploadFile = File(...),
    target_language: str = Query(
        "English", description="Target language for translation"
    ),
    patient_id: str = Form(None),
):
    """
    Endpoint to upload a lab report (PDF/Image) and get plain-English, structured results.
    """
    try:
        # 1. Convert file to images and check size
        images_bytes = process_file_to_images(file, max_size_mb=5)

        # 2. Send to Gemini for analysis
        extraction = analyze_lab_report_images(
            images_bytes, target_language=target_language
        )

        # 3. Return structured JSON as dict to avoid FastAPI response validation 500s
        extraction_dict = (
            extraction.model_dump()
            if hasattr(extraction, "model_dump")
            else dict(extraction)
        )

        # 4. Save to storage and inject report_id
        report_id = save_report(extraction_dict, patient_id=patient_id)
        extraction_dict["report_id"] = report_id

        return extraction_dict
    except HTTPException as he:
        raise he
    except ValueError as ve:
        raise HTTPException(status_code=500, detail=str(ve))
    except Exception as e:
        import traceback

        traceback.print_exc()
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {e!s}"
        )


@router.get("/report/{report_id}")
async def get_shared_report(report_id: str):
    """
    Endpoint to fetch a previously analyzed report by its UUID.
    """
    report = get_report(report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    report["report_id"] = report_id
    return report
