import os
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.core.rag_engine import create_vector_db_from_upload, get_rag_chain
from app.core.prompts import ANALYSIS_QUESTIONS

router = APIRouter()

@router.post("/analyze/pdf")
async def analyze_pdf(file: UploadFile = File(...)):
    # 1. Debugging: Check if API Key exists in Render Environment
    api_key = os.getenv("HUGGINGFACEHUB_API_TOKEN")
    if not api_key:
        print("CRITICAL ERROR: HUGGINGFACEHUB_API_TOKEN is missing in environment variables!")
        raise HTTPException(status_code=500, detail="Server Configuration Error: API Key missing.")
    else:
        print(f"API Key found: {api_key[:4]}...{api_key[-4:]}") # Print partial key to logs

    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="File must be a PDF")

    try:
        print(f"Starting analysis for: {file.filename}")
        
        # 2. Safer File Reading
        # Read all bytes into memory immediately to avoid stream issues
        content = await file.read()
        print(f"File read successfully. Size: {len(content)} bytes")
        
        # 3. Create Vector DB
        print("Creating Vector DB (calling HuggingFace API)...")
        vector_store = create_vector_db_from_upload(content)
        print("Vector DB created successfully.")
        
        # 4. Get Chain
        rag_chain = get_rag_chain(vector_store)
        
        results = {}

        # 5. Execution Loop
        for key, question in ANALYSIS_QUESTIONS.items():
            print(f"Generating section: {key}...")
            # Invoke the chain
            response = rag_chain.invoke(question)
            results[key] = response

        print("Analysis complete.")
        return {
            "filename": file.filename,
            "analysis": results
        }

    except Exception as e:
        # Print the FULL error to the Render logs
        print(f"FULL ERROR TRACEBACK: {e}")
        # Return the specific error to the frontend so we can see it
        raise HTTPException(status_code=500, detail=f"Backend Error: {str(e)}")