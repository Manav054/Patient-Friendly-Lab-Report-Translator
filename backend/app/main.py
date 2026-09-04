from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from app.services.pdf_service import process_file_to_images
from app.services.gemini_service import analyze_lab_report_images
from app.models import LabReportExtraction

# Load environment variables
load_dotenv()

app = FastAPI(title="Patient-Friendly Lab Report Translator")

# Configure CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/analyze-report", response_model=LabReportExtraction)
async def analyze_report(file: UploadFile = File(...)):
    """
    Endpoint to upload a lab report (PDF/Image) and get plain-English, structured results.
    """
    try:
        # 1. Convert file to images and check size
        images_bytes = process_file_to_images(file, max_size_mb=5)
        
        # 2. Send to Gemini for analysis
        extraction = analyze_lab_report_images(images_bytes)
        
        # 3. Return structured JSON
        return extraction
    except HTTPException as he:
        raise he
    except ValueError as ve:
        raise HTTPException(status_code=500, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

@app.get("/api/health")
async def health_check():
    return {"status": "ok"}
