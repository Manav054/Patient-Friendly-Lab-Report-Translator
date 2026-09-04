import os
from google import genai
from google.genai import types
from app.models import LabReportExtraction

def analyze_lab_report_images(images_bytes: list[bytes]) -> LabReportExtraction:
    """
    Sends the images of the lab report to Gemini and extracts structured JSON.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is not set.")

    client = genai.Client(api_key=api_key)
    
    prompt = """
    You are an expert clinical data extractor. Your task is to extract biomarker values from laboratory reports.
    Ignore and omit any Personally Identifiable Information (PII) such as names, addresses, or patient IDs.
    Extract the tests, their values, units, and reference ranges.
    Determine if the test is abnormal based on the reference range.
    Provide a 1-2 sentence layman explanation for each marker.
    Provide 2-3 suggested questions for the patient to ask their doctor.
    """

    contents = [prompt]
    
    # Add all images to the contents
    for img_bytes in images_bytes:
        contents.append(
            types.Part.from_bytes(
                data=img_bytes,
                mime_type="image/png"
            )
        )

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=contents,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=LabReportExtraction,
            temperature=0.1,
        ),
    )

    # The SDK parses it into the Pydantic model directly if response_schema is used,
    # wait, actually response.parsed contains the Pydantic object if response_schema is passed.
    if hasattr(response, 'parsed') and response.parsed:
        return response.parsed
    
    # Fallback to json parsing if response.parsed isn't set (depends on SDK version)
    import json
    return LabReportExtraction.model_validate_json(response.text)
