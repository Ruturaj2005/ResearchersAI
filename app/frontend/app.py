import streamlit as st
import requests
import json

# --- Page Configuration ---
st.set_page_config(
    page_title="ResearchersAI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Reduce default padding and margins
st.markdown("""
    <style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 0rem;
        padding-left: 3rem;
        padding-right: 3rem;
    }
    </style>
""", unsafe_allow_html=True)

# --- Custom CSS for Dark Classy Theme ---
st.markdown("""
    <style>
    /* Main Background */
    .main {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    }
    
    /* Streamlit Default Elements */
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: #e8e8e8 !important;
        font-weight: 600 !important;
        margin-top: 0.5rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    h1 {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.5rem !important;
    }
    
    h2 {
        font-size: 1.5rem !important;
    }
    
    h3 {
        font-size: 1.2rem !important;
    }
    
    /* Paragraphs and Text */
    p, .stMarkdown {
        color: #c5c5c5 !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background-color: transparent;
        margin-bottom: 0 !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 48px;
        white-space: pre-wrap;
        background: linear-gradient(145deg, #2a2d3a, #1f2229);
        border-radius: 8px 8px 0px 0px;
        color: #a0a0a0;
        font-weight: 500;
        padding: 10px 20px;
        border: 1px solid #3a3d4a;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: linear-gradient(145deg, #35384a, #2a2d3a);
        color: #e0e0e0;
        transform: translateY(-2px);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: #ffffff !important;
        border-bottom: 3px solid #667eea;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    /* Divider */
    hr {
        border-color: #3a3d4a !important;
        margin: 1rem 0 !important;
    }
    
    /* File Uploader */
    .stFileUploader {
        background: linear-gradient(145deg, #2a2d3a, #1f2229);
        border-radius: 10px;
        padding: 15px;
        border: 2px dashed #4a4d5a;
        margin-bottom: 1rem;
    }
    
    .stFileUploader label {
        color: #e0e0e0 !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 28px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5);
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1f2229 0%, #2a2d3a 100%);
        border-right: 1px solid #3a3d4a;
    }
    
    [data-testid="stSidebar"] h2 {
        color: #e8e8e8 !important;
        margin-bottom: 0.8rem !important;
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        margin-bottom: 0.3rem !important;
    }
    
    /* Info Box */
    .stAlert {
        background: linear-gradient(145deg, #2a2d3a, #1f2229);
        color: #c5c5c5;
        border-left: 4px solid #667eea;
        border-radius: 8px;
        padding: 0.8rem 1rem !important;
        margin: 0.5rem 0 !important;
    }
    
    /* Success Box */
    .stSuccess {
        background: linear-gradient(145deg, #1e3a2f, #1a2e26);
        color: #6ee7b7;
        border-left: 4px solid #10b981;
        border-radius: 8px;
        padding: 0.8rem 1rem !important;
        margin: 0.5rem 0 !important;
    }
    
    /* Warning Box */
    .stWarning {
        background: linear-gradient(145deg, #3a2e1e, #2e261a);
        color: #fbbf24;
        border-left: 4px solid #f59e0b;
        border-radius: 8px;
        padding: 0.8rem 1rem !important;
        margin: 0.5rem 0 !important;
    }
    
    /* Error Box */
    .stError {
        background: linear-gradient(145deg, #3a1e1e, #2e1a1a);
        color: #f87171;
        border-left: 4px solid #ef4444;
        border-radius: 8px;
        padding: 0.8rem 1rem !important;
        margin: 0.5rem 0 !important;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-top-color: #667eea !important;
    }
    
    /* Content Cards */
    [data-testid="stMarkdownContainer"] {
        background: transparent;
        padding: 0;
        margin: 0.3rem 0;
    }
    
    /* Input Fields */
    .stTextInput input, .stTextArea textarea {
        background-color: #2a2d3a;
        color: #e0e0e0;
        border: 1px solid #4a4d5a;
        border-radius: 8px;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1a1a2e;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    /* Tab Content Area */
    .stTabs [data-baseweb="tab-panel"] {
        background: linear-gradient(145deg, #2a2d3a, #1f2229);
        border-radius: 0px 8px 8px 8px;
        padding: 1.5rem;
        border: 1px solid #3a3d4a;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        margin-top: 0 !important;
    }
    
    /* Custom Header Badge */
    .header-badge {
        display: inline-block;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 0.75em;
        font-weight: 600;
        margin-left: 8px;
    }
    
    /* Stats Card */
    .stats-card {
        background: linear-gradient(145deg, #2a2d3a, #1f2229);
        border: 1px solid #3a3d4a;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        transition: transform 0.3s ease;
    }
    
    .stats-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.3);
    }
    
    /* Remove extra spacing */
    .element-container {
        margin-bottom: 0.5rem !important;
    }
    
    /* Compact sidebar items */
    [data-testid="stSidebar"] .element-container {
        margin-bottom: 0.3rem !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("# 🧠 ResearchersAI")
st.markdown("### Your Automated Academic Research Assistant <span class='header-badge'>AI-Powered</span>", unsafe_allow_html=True)
st.markdown("Upload a research paper (PDF) to extract summaries, methodologies, research gaps, and future project ideas automatically.")
st.divider()

# --- Sidebar ---
with st.sidebar:
    st.header("📄 Upload Document")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    
    process_btn = st.button("🚀 Analyze Paper", type="primary", use_container_width=True)
    
    st.info("ℹ️ System uses RAG (Retrieval Augmented Generation) to analyze long documents without hallucination.")
    
    st.markdown("---")
    st.markdown("**💡 Features:**")
    st.markdown("""
    • Deep paper analysis  
    • Gap identification  
    • Future research ideas  
    • Methodology extraction
    """)

# --- Main Logic ---
if uploaded_file is not None and process_btn:
    
    # 1. Show a loading spinner while backend works
    with st.spinner("🔄 Processing PDF... Reading text... Identifying Gaps... Generating Ideas..."):
        try:
            # 2. Prepare the file for API request
            files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
            
            # 3. Call the FastAPI Backend
            # Ensure your backend is running on port 8000
            response = requests.post("http://localhost:8000/api/v1/analyze/pdf", files=files)
            
            if response.status_code == 200:
                data = response.json()
                analysis = data["analysis"]
                
                # --- Success Message ---
                st.success(f"✅ Analysis Complete for: **{data['filename']}**")
                
                # --- Display Results in Tabs ---
                tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
                    "📝 Summary", 
                    "🧪 Methodology", 
                    "📊 Key Findings", 
                    "⚖️ Limitations", 
                    "🔍 Research Gaps", 
                    "🚀 Future Ideas"
                ])
                
                with tab1:
                    st.header("📝 Comprehensive Summary")
                    st.markdown(analysis["comprehensive_summary"])
                    
                with tab2:
                    st.header("🧪 Methodology & Approach")
                    st.markdown(analysis["methodology"])
                    
                with tab3:
                    st.header("📊 Key Findings & Results")
                    st.markdown(analysis["key_findings"])
                    
                with tab4:
                    st.header("⚖️ Strengths & Limitations")
                    st.markdown(analysis["limitations_and_strengths"])
                    
                with tab5:
                    st.header("🔍 Identified Research Gaps")
                    st.info("💡 These are areas where the current research fell short or suggested future work.")
                    st.markdown(analysis["research_gaps"])
                    
                with tab6:
                    st.header("🚀 Suggested Future Projects")
                    st.success("✨ Use these ideas for your next thesis or research project!")
                    st.markdown(analysis["future_suggestions"])
                    
            else:
                st.error(f"❌ Error {response.status_code}: {response.text}")
                
        except Exception as e:
            st.error(f"⚠️ Connection Error: Is the backend running? \n\n**Details:** {e}")

elif process_btn and not uploaded_file:
    st.warning("⚠️ Please upload a PDF file first.")
    
elif not uploaded_file:
    # --- Welcome Message ---
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style='text-align: center; padding: 2rem; background: linear-gradient(145deg, #2a2d3a, #1f2229); border-radius: 12px; border: 1px solid #3a3d4a; margin-top: 2rem;'>
            <h2 style='color: #e8e8e8; margin-bottom: 0.8rem !important;'>👋 Welcome to ResearcherAI</h2>
            <p style='color: #c5c5c5; font-size: 1.05em; margin-bottom: 1.2rem;'>Get started by uploading a research paper PDF in the sidebar</p>
            <div style='display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; margin-top: 1.5rem;'>
                <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 12px 20px; border-radius: 8px;'>
                    <strong>📝 Summaries</strong>
                </div>
                <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 12px 20px; border-radius: 8px;'>
                    <strong>🧪 Methodologies</strong>
                </div>
                <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 12px 20px; border-radius: 8px;'>
                    <strong>🔍 Research Gaps</strong>
                </div>
                <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 12px 20px; border-radius: 8px;'>
                    <strong>🚀 Future Ideas</strong>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # --- Quick Stats ---
        st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
        
        stats_col1, stats_col2, stats_col3, stats_col4 = st.columns(4)
        
        with stats_col1:
            st.markdown("""
            <div class='stats-card'>
                <div style='font-size: 1.8rem; color: #667eea;'>⚡</div>
                <div style='font-size: 0.9rem; color: #a0a0a0; margin-top: 0.3rem;'>Fast Analysis</div>
            </div>
            """, unsafe_allow_html=True)
        
        with stats_col2:
            st.markdown("""
            <div class='stats-card'>
                <div style='font-size: 1.8rem; color: #10b981;'>🎯</div>
                <div style='font-size: 0.9rem; color: #a0a0a0; margin-top: 0.3rem;'>Accurate Results</div>
            </div>
            """, unsafe_allow_html=True)
        
        with stats_col3:
            st.markdown("""
            <div class='stats-card'>
                <div style='font-size: 1.8rem; color: #f59e0b;'>🔒</div>
                <div style='font-size: 0.9rem; color: #a0a0a0; margin-top: 0.3rem;'>Secure & Private</div>
            </div>
            """, unsafe_allow_html=True)
        
        with stats_col4:
            st.markdown("""
            <div class='stats-card'>
                <div style='font-size: 1.8rem; color: #ef4444;'>💡</div>
                <div style='font-size: 0.9rem; color: #a0a0a0; margin-top: 0.3rem;'>Smart Insights</div>
            </div>
            """, unsafe_allow_html=True)
