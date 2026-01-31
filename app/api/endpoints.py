from fastapi import APIRouter, UploadFile,File, HTTPException
from app.core.rag_engine import create_vector_db,get_rag_chain
from app.core.prompts import ANALYSIS_QUESTIONS

router= APIRouter()

@router.post("/analyze/pdf")
async def analyze_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="File must be a PDF")
    
    try:
        content = await file.read()
        vector_store = create_vector_db(content)

        rag_chain = get_rag_chain(vector_store)

        results = {}

        for key, question in ANALYSIS_QUESTIONS.items():
            # Invoke the chain with the specific question
            answer = rag_chain.invoke(question)
            results[key] = answer
        
        return {
            "filename": file.filename,
            "analysis": results
        }

    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error during analysis")