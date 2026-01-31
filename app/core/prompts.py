# We define specific questions to extract the exact details you want.
ANALYSIS_QUESTIONS = {
    
    "comprehensive_summary": """
    Write a comprehensive summary of this research paper. 
    It should be detailed (approx 800-1000 words logic) and cover the problem statement, 
    core approach, and final conclusion. 
    Do not be brief; explain the 'story' of the paper.
    """,

    "methodology": """
    Analyze the methodology proposed in this paper. 
    1. What specific algorithms, models, or theoretical frameworks did they use?
    2. How was the data collected or the experiment set up?
    Provide technical details.
    """,

    "key_findings": """
    What are the concrete findings and results? 
    Include quantitative metrics (accuracy, F1-score, speedup, p-values) if mentioned in the text.
    """,

    "limitations_and_strengths": """
    Critically analyze the paper:
    1. Strengths: What did this paper do remarkably well?
    2. Limitations: What are the specific weaknesses, constraints, or 'threats to validity' mentioned by the authors?
    """,

    "research_gaps": """
    Identify the research gaps. 
    What specific problems did this paper fail to address? 
    What questions remain unanswered?
    """,

    "future_suggestions": """
    Based on the identified research gaps and limitations, suggest 3 specific, novel project ideas 
    that a student or researcher could develop to fill these gaps. 
    Be creative but technically feasible.
    """
}