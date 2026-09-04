# Project Specification: Patient-Friendly Lab Report Translator

## 1. Project Overview
The **Patient-Friendly Lab Report Translator** is an AI-powered web application designed to demystify complex medical laboratory results. Users upload standard blood test PDFs (e.g., Complete Blood Count, Lipid Panels). The app uses multimodal AI to extract raw biomarker data, normalizes it, and presents a plain-English, visual dashboard. It highlights out-of-range metrics and generates suggested questions for the user to ask their physician.

## 2. Zero-Cost Technology Stack
*   **Frontend Framework:** Vue.js 3 (Composition API) — hosted on Vercel.
*   **Styling & UI:** Tailwind CSS + a charting library (like Chart.js or Recharts).
*   **Backend API:** Python with FastAPI — lightweight and excellent for data validation; hosted on Render (Free Tier). (Use uv package manager)
*   **AI / Vision Model:** Google Gemini 1.5 Flash (via Google AI Studio free tier) for multimodal document processing and structured JSON output.
*   **Deployment:** Vercel (Frontend) + Render (Backend).

---

## 3. Core Requirements

### 3.1. Frontend Development (Vue 3 on Vercel)
*   **Secure Upload Interface:** A drag-and-drop zone that accepts `.pdf`, `.jpg`, and `.png` files containing lab results. 
*   **Client-Side Validation:** Ensure file sizes do not exceed 5MB before sending payloads to the backend.
*   **Dashboard View:** A clean, non-alarming UI that displays:
    *   **The Biomarker Grid:** A clear table showing the Test Name, Result, Standard Range, and Unit.
    *   **Visual Indicators:** Color-coded status bars (e.g., Green for Normal, Yellow/Red for Out of Range).
    *   **Plain English Summaries:** A brief, jargon-free explanation of what each out-of-range marker means.
    *   **Actionable Questions:** A section generating 2-3 specific questions the patient should ask their doctor.
*   **Disclaimer:** A prominent, non-dismissible medical disclaimer stating the app provides information, not medical advice or diagnoses.

### 3.2. Backend Development (FastAPI on Render)
*   **File Handling Endpoint:** An endpoint (e.g., `/api/analyze-report`) that receives the uploaded file. If it's a PDF, convert it to images (using a library like `pdf2image`) before sending it to the vision model.
*   **Data Validation:** Use Pydantic models to define the exact JSON structure expected from the LLM, ensuring the frontend receives predictable data.
*   **Stateless Processing:** The backend should process the file in memory and return the structured JSON without saving sensitive medical documents to disk.

### 3.3. Prompt Engineering (Structured Extraction)
The system prompt must enforce strict adherence to a predefined JSON schema to ensure the data is machine-readable.
*   **Role Setup:** "You are an expert clinical data extractor. Your task is to extract biomarker values from laboratory reports."
*   **Strict JSON Output Constraint:** "Output ONLY valid JSON adhering strictly to the provided schema. Do not include markdown formatting or explanations outside the JSON."
*   **Schema Definition:** The prompt must include a schema resembling:
    {
      "patient_identifiers_found": boolean, 
      "tests": [
        {
          "marker_name": "string",
          "value": "float",
          "unit": "string",
          "reference_range_low": "float",
          "reference_range_high": "float",
          "is_abnormal": "boolean",
          "layman_explanation": "string (1-2 sentences)"
        }
      ],
      "suggested_physician_questions": ["string", "string"]
    }
*   **Anonymization Directive:** "Ignore and omit any Personally Identifiable Information (PII) such as names, addresses, or patient IDs."

### 3.4. Execution Flow
1.  **Upload:** User uploads a lab report via the Vue.js frontend.
2.  **Transmission:** The frontend sends the file to the FastAPI backend.
3.  **Preprocessing:** FastAPI converts the file to the required image format if necessary.
4.  **AI Extraction:** The backend sends the image and the strict JSON prompt to the Gemini 3.1 Flash Lite API.
5.  **Validation:** FastAPI receives the JSON, validates it against the Pydantic model, and returns it to the client.
6.  **Rendering:** The Vue app renders the color-coded dashboard and layman explanations based on the structured data.

---

## 4. Minimum Viable Product (MVP) Milestones
*   **Phase 1:** Set up the Vite + Vue 3 frontend (Vercel) and the FastAPI backend (Render). Establish a basic health-check connection between them.
*   **Phase 2:** Implement the file upload component and backend PDF/Image handling.
*   **Phase 3:** Integrate the Gemini API, refine the strict JSON prompt, and build the Pydantic validation models.
*   **Phase 4:** Build the frontend dashboard to dynamically render the extracted JSON data with color-coded status bars.

## 5. Security & Privacy Considerations
*   **Zero Retention:** Ensure the backend immediately discards files from memory after processing.
*   **HTTPS Only:** Enforce secure connections for all API requests.
*   **Anonymization:** Instruct the LLM to actively filter out patient names or IDs from the returned data.