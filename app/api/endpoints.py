from fastapi import APIRouter, UploadFile, File, HTTPException
from app.core.rag_engine import create_vector_db_from_upload, get_rag_chain
from app.core.prompts import ANALYSIS_QUESTIONS

router = APIRouter()

@router.post("/analyze/pdf")
async def analyze_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="File must be a PDF")

    try:
        # 1. Ingestion
        content = await file.read()
        
        # CORRECTED FUNCTION CALL BELOW:
        vector_store = create_vector_db_from_upload(content)
        
        # 2. Get the Pure LCEL Chain
        rag_chain = get_rag_chain(vector_store)
        
        results = {}

        # 3. Execution
        for key, question in ANALYSIS_QUESTIONS.items():
            # Invoke the chain. 
            response = rag_chain.invoke(question)
            results[key] = response

        return {
            "filename": file.filename,
            "analysis": results
        }

    except Exception as e:
        print(f"Error: {e}") 
        raise HTTPException(status_code=500, detail="An error occurred during analysis.")