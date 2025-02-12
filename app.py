import streamlit as st
import google.generativeai as genai
from agents import initialize_agents
import os
from dotenv import load_dotenv
from PIL import Image
import io
from fpdf import FPDF
from fpdf.enums import XPos, YPos

# Load environment variables
load_dotenv()

# Must be the first Streamlit command
st.set_page_config(
    page_title="Multi-Agent Design Analysis Platform",
    page_icon="👁️",
    layout="wide"
)

# Initialize agents silently
try:
    agents = initialize_agents()
except Exception as e:
    st.error(f"Error loading agents: {str(e)}")
    st.stop()

# Load environment variables and configure Gemini
api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
else:
    st.error("No API key found in .env file. Please add your Gemini API key to the .env file.")
    st.stop()

# Custom CSS for modern blue and purple theme
st.markdown("""
<style>
    /* Modern Blue and Purple Theme */
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    }
    
    /* Custom container styling */
    .agent-container {
        background-color: rgba(255, 255, 255, 0.1);
        border: 2px solid #4a90e2;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        transition: all 0.3s ease;
        color: #e0e0ff;
    }
    .agent-container:hover {
        box-shadow: 0 4px 15px rgba(74, 144, 226, 0.3);
        transform: translateY(-2px);
        border-color: #6c63ff;
    }
    
    /* Custom button styling */
    .stButton>button {
        background: linear-gradient(135deg, #4a90e2 0%, #6c63ff 100%);
        color: #ffffff;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        transition: all 0.3s ease;
        font-weight: 600;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #6c63ff 0%, #4a90e2 100%);
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(74, 144, 226, 0.3);
    }
    
    /* Custom header styling */
    h1, h2, h3 {
        color: #e0e0ff;
        font-family: 'SF Pro Display', sans-serif;
        text-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    
    /* Custom tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background-color: rgba(255, 255, 255, 0.05);
        padding: 8px;
        border-radius: 10px;
        flex-wrap: nowrap;
        overflow-x: auto;
        white-space: nowrap;
        scrollbar-width: none;  /* Firefox */
    }
    .stTabs [data-baseweb="tab-list"]::-webkit-scrollbar {
        display: none;  /* Chrome, Safari, Edge */
    }
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(74, 144, 226, 0.1);
        border: 1px solid #4a90e2;
        border-radius: 5px;
        color: #e0e0ff;
        padding: 8px 16px;
        font-size: 0.9em;
        min-width: auto;
        flex: 0 0 auto;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 6px;
    }
    .stTabs [data-baseweb="tab"] svg {
        width: 20px;
        height: 20px;
        min-width: 20px;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background-color: rgba(108, 99, 255, 0.2);
        transform: translateY(-1px);
        transition: all 0.2s ease;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #4a90e2 0%, #6c63ff 100%) !important;
        color: #ffffff !important;
        font-weight: 600;
    }
    
    /* Progress bar styling */
    .stProgress > div > div {
        background: linear-gradient(135deg, #4a90e2 0%, #6c63ff 100%);
    }

    /* File uploader styling */
    .uploadedFile {
        border: 2px dashed #4a90e2;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        margin: 20px 0;
        background-color: rgba(255, 255, 255, 0.05);
        color: #e0e0ff;
    }

    /* Warning message styling */
    .stAlert {
        background-color: rgba(255, 255, 255, 0.1);
        border: 2px solid #4a90e2;
        color: #e0e0ff;
    }

    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid #4a90e2;
        border-radius: 5px;
        color: #e0e0ff;
    }
    .streamlit-expanderHeader:hover {
        background-color: rgba(108, 99, 255, 0.2);
    }

    /* Text styling */
    p {
        color: #e0e0ff !important;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: rgba(26, 26, 46, 0.9);
    }
    
    /* Input fields */
    .stTextInput input {
        background-color: rgba(255, 255, 255, 0.1);
        border: 1px solid #4a90e2;
        color: #e0e0ff;
    }
    
    /* File uploader text */
    .stFileUploader label {
        color: #e0e0ff !important;
    }
    
    /* Success messages */
    .success {
        color: #00ff9d !important;
    }
    
    /* Error messages */
    .error {
        color: #ff6b6b !important;
    }

    /* Custom upload button styling */
    .upload-button button {
        background-color: #ab1a32 !important;
        color: white !important;
        border: none !important;
        padding: 12px 24px !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    .upload-button button:hover {
        background-color: #8a1528 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(171, 26, 50, 0.3) !important;
    }
    
    /* Upload section styling */
    .upload-section {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        padding: 20px;
        margin: 20px 0;
        display: flex;
        align-items: center;
        gap: 20px;
    }

    /* File uploader styling */
    .stFileUploader {
        width: 100%;
    }

    .stFileUploader > div {
        background-color: rgba(255, 255, 255, 0.1);
        border: 2px dashed #4a90e2;
        border-radius: 10px;
        padding: 20px;
    }

    .stFileUploader > div:hover {
        border-color: #6c63ff;
        background-color: rgba(255, 255, 255, 0.15);
    }

    .stFileUploader p {
        color: #e0e0ff !important;
    }

    /* Thumbnail container styling */
    .thumbnail-container {
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid #4a90e2;
        border-radius: 8px;
        padding: 15px;
        margin: 20px auto;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }

    .thumbnail-container:hover {
        border-color: #6c63ff;
        box-shadow: 0 4px 12px rgba(74, 144, 226, 0.2);
    }

    .thumbnail-container img {
        border-radius: 4px;
        max-width: 100%;
        height: auto;
        object-fit: contain;
        display: block;
    }
</style>
""", unsafe_allow_html=True)

# Material Icons SVG definitions
st.markdown("""
<style>
    /* Add Material Icons */
    @import url('https://fonts.googleapis.com/icon?family=Material+Icons');
</style>

<div style="display: none">
    <!-- Vision Analysis Icon -->
    <svg id="vision_icon" xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24" fill="#e0e0ff">
        <path d="M480-320q75 0 127.5-52.5T660-500q0-75-52.5-127.5T480-680q-75 0-127.5 52.5T300-500q0 75 52.5 127.5T480-320Zm0-72q-45 0-76.5-31.5T372-500q0-45 31.5-76.5T480-608q45 0 76.5 31.5T588-500q0 45-31.5 76.5T480-392Zm0 192q-146 0-266-81.5T40-500q54-137 174-218.5T480-800q146 0 266 81.5T920-500q-54 137-174 218.5T480-200Zm0-300Zm0 220q113 0 207.5-59.5T832-500q-50-101-144.5-160.5T480-720q-113 0-207.5 59.5T128-500q50 101 144.5 160.5T480-280Z"/>
    </svg>
    <!-- UX Analysis Icon -->
    <svg id="ux_icon" xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24" fill="#e0e0ff">
        <path d="M280-280h400v-400H280v400Zm0 80q-33 0-56.5-23.5T200-280v-400q0-33 23.5-56.5T280-760h400q33 0 56.5 23.5T760-680v400q0 33-23.5 56.5T680-200H280Zm200-280Zm-40 120h80v-80h80v-80h-80v-80h-80v80h-80v80h80v80Z"/>
    </svg>
    <!-- Market Research Icon -->
    <svg id="market_icon" xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24" fill="#e0e0ff">
        <path d="M160-160v-440h140v440H160Zm250 0v-640h140v640H410Zm250 0v-280h140v280H660Z"/>
    </svg>
    <!-- Upload Icon -->
    <svg id="upload_icon" xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24" fill="#e0e0ff">
        <path d="M440-320v-326L336-542l-56-58 200-200 200 200-56 58-104-104v326h-80ZM240-160q-33 0-56.5-23.5T160-240v-120h80v120h480v-120h80v120q0 33-23.5 56.5T720-160H240Z"/>
    </svg>
    <!-- Settings Icon -->
    <svg id="settings_icon" xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24" fill="#e0e0ff">
        <path d="m388-80-20-126q-19-7-40-19t-37-25l-118 54-93-164 108-79q-2-9-2.5-20.5T185-480q0-9 .5-20.5T188-521L80-600l93-164 118 54q16-13 37-25t40-18l20-127h184l20 126q19 7 40.5 18.5T669-710l118-54 93 164-108 77q2 10 2.5 21.5t.5 21.5q0 10-.5 21t-2.5 21l108 78-93 164-118-54q-16 13-36.5 25.5T592-206L572-80H388Zm92-270q54 0 92-38t38-92q0-54-38-92t-92-38q-54 0-92 38t-38 92q0 54 38 92t92 38Z"/>
    </svg>
    <!-- Report Icon -->
    <svg id="report_icon" xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24" fill="#e0e0ff">
        <path d="M320-240h320v-80H320v80Zm0-160h320v-80H320v80ZM240-80q-33 0-56.5-23.5T160-160v-640q0-33 23.5-56.5T240-880h320l240 240v480q0 33-23.5 56.5T720-80H240Zm280-520v-200H240v640h480v-440H520ZM240-800v200-200 640-640Z"/>
    </svg>
</div>
""", unsafe_allow_html=True)

# Title and description with modern styling
st.markdown("<h1 style='text-align: center; margin-bottom: 2rem;'><img src='data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIGhlaWdodD0iMjQiIHZpZXdCb3g9IjAgLTk2MCA5NjAgOTYwIiB3aWR0aD0iMjQiIGZpbGw9IiNlMGUwZmYiPjxwYXRoIGQ9Ik00ODAtMzIwcTc1IDAgMTI3LjUtNTIuNVQ2NjAtNTAwcTAtNzUtNTIuNS0xMjcuNVQ0ODAtNjgwcS03NSAwLTEyNy41IDUyLjVUMzAwLTUwMHEwIDc1IDUyLjUgMTI3LjVUNDgwLTMyMFptMC03MnEtNDUgMC03Ni41LTMxLjVUMzcyLTUwMHEwLTQ1IDMxLjUtNzYuNVQ0ODAtNjA4cTQ1IDAgNzYuNSAzMS41VDU4OC01MDBxMCA0NS0zMS41IDc2LjVUNDgwLTM5MlptMCAxOTJxLTE0NiAwLTI2Ni04MS41VDQwLTUwMHE1NC0xMzcgMTc0LTIxOC41VDQ4MC04MDBxMTQ2IDAgMjY2IDgxLjVUOTIwLTUwMHEtNTQgMTM3LTE3NCAyMTguNVQ0ODAtMjAwWm0wLTMwMFptMCAyMjBxMTEzIDAgMjA3LjUtNTkuNVQ4MzItNTAwcS01MC0xMDEtMTQ0LjUtMTYwLjVUNDgwLTcyMHEtMTEzIDAtMjA3LjUgNTkuNVQxMjgtNTAwcTUwIDEwMSAxNDQuNSAxNjAuNVQ0ODAtMjgwWiIvPjwvc3ZnPg==' style='vertical-align: middle; margin-right: 10px;'> Multi-Agent Design Analysis Platform</h1>", unsafe_allow_html=True)

# Main content with modern tabs
tabs = st.tabs([
    "Vision",
    "UX",
    "Market",
    "Report"
])

# Update the tab headers with custom styling
st.markdown("""
<style>
    /* Make tabs more compact and modern */
    .stTabs [data-baseweb="tab"] {
        font-size: 1rem;
        font-weight: 500;
        padding: 8px 24px;
        border-radius: 5px;
        margin-right: 4px;
        color: #ffffff;
        border: none;
    }
    
    /* Custom colors for each tab */
    .stTabs [data-baseweb="tab"]:nth-of-type(1) {
        background-color: #006381;
    }
    
    .stTabs [data-baseweb="tab"]:nth-of-type(2) {
        background-color: #bf5b17;
    }
    
    .stTabs [data-baseweb="tab"]:nth-of-type(3) {
        background-color: #2a7339;
    }
    
    .stTabs [data-baseweb="tab"]:nth-of-type(4) {
        background-color: #ab1a32;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        opacity: 0.8;
        transform: translateY(-1px);
        transition: all 0.2s ease;
    }
    
    .stTabs [aria-selected="true"] {
        opacity: 1 !important;
        font-weight: 600;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    
    /* Tab list container */
    .stTabs [data-baseweb="tab-list"] {
        background-color: rgba(255, 255, 255, 0.05);
        padding: 8px;
        border-radius: 10px;
        gap: 4px;
    }
    
    /* Tab panel content */
    .stTabs [data-baseweb="tab-panel"] {
        padding: 16px 0;
    }
</style>
""", unsafe_allow_html=True)

# Add upload section with button and file uploader
st.markdown("""
<div style="margin: 20px 0;">
""", unsafe_allow_html=True)

# File uploader
uploaded_file = st.file_uploader("Upload your design", type=["png", "jpg", "jpeg"])

# Analysis button - always visible but conditionally disabled
if uploaded_file is not None:
    analyze_button = st.button("Start Analysis", type="primary", key="analyze_enabled")
else:
    st.button("Start Analysis", type="primary", disabled=True, key="analyze_disabled")

st.markdown("</div>", unsafe_allow_html=True)

# Display uploaded image preview
if uploaded_file is not None:
    try:
        # Display the uploaded image as a small preview
        image = Image.open(uploaded_file)
        
        # Calculate dimensions while maintaining aspect ratio
        max_width = 300
        aspect_ratio = image.size[1] / image.size[0]
        new_width = min(max_width, image.size[0])
        new_height = int(new_width * aspect_ratio)
        
        # Create a high-quality resized image
        resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Create a container with specific width for the preview
        st.markdown("""
        <div class="thumbnail-container" style="max-width: 300px; margin: 10px auto;">
            <div style="display: flex; justify-content: center;">
        """, unsafe_allow_html=True)
        st.image(resized_image, use_column_width=False)
        st.markdown("</div></div>", unsafe_allow_html=True)
        
        # Store the original image in session state
        st.session_state["uploaded_image"] = image
        
        # Initialize agents
        if "agents" not in st.session_state:
            with st.spinner("Initializing AI agents..."):
                try:
                    st.session_state["agents"] = initialize_agents()
                except Exception as e:
                    st.error(f"Error initializing agents: {str(e)}")
                    st.stop()

        # Analysis process
        if 'analyze_button' in locals() and analyze_button:
            progress_container = st.container()
            with progress_container:
                progress_bar = st.progress(0)
                status_text = st.empty()
            
            try:
                # Vision Analysis
                status_text.markdown("Running Vision Analysis...")
                vision_agent = st.session_state["agents"]["vision"]
                vision_response = vision_agent.run(
                    "Analyze this design image in detail",
                    files=[uploaded_file]
                )
                st.session_state["vision_analysis"] = vision_response
                progress_bar.progress(33)

                # UX Analysis
                status_text.markdown("Running UX Analysis...")
                ux_agent = st.session_state["agents"]["ux"]
                ux_response = ux_agent.run(
                    f"Based on the vision analysis: {vision_response}, provide UX recommendations"
                )
                st.session_state["ux_analysis"] = ux_response
                progress_bar.progress(66)

                # Market Analysis
                status_text.markdown("Running Market Research...")
                market_agent = st.session_state["agents"]["market"]
                market_response = market_agent.run(
                    f"Based on the design analysis, research current market trends and competitor approaches"
                )
                st.session_state["market_analysis"] = market_response
                progress_bar.progress(100)
                status_text.markdown("Analysis Complete!")

                st.success("Analysis complete! View results in respective tabs.")
            except Exception as e:
                st.error(f"Error during analysis: {str(e)}")
                if "404" in str(e):
                    st.info("If you're seeing a model not found error, please check if you have access to the latest Gemini models in your region.")
    except Exception as e:
        st.error(f"Error processing image: {str(e)}")

# Content for tabs
with tabs[0]:
    st.markdown("<h2 style='margin-bottom: 1rem;'>Vision Analysis</h2>", unsafe_allow_html=True)
    if "vision_analysis" in st.session_state:
        st.markdown("""
        <div class="agent-container">
        """, unsafe_allow_html=True)
        st.markdown(st.session_state["vision_analysis"])
        st.markdown("</div>", unsafe_allow_html=True)

# Results tabs with modern styling
for tab_idx, (tab, title) in enumerate(zip(
    tabs[1:], 
    ["UX Analysis", "Market Research", "Comprehensive Report"]
)):
    with tab:
        st.markdown(f"<h2 style='margin-bottom: 1rem;'>{title}</h2>", unsafe_allow_html=True)
        
        if tab_idx < 2:  # For individual analysis tabs
            result_key = f"{title.lower().split()[0]}_analysis"
            if result_key in st.session_state:
                st.markdown("""
                <div class="agent-container">
                """, unsafe_allow_html=True)
                st.markdown(st.session_state[result_key])
                st.markdown("</div>", unsafe_allow_html=True)
        else:  # For the Report tab
            if all(key in st.session_state for key in ["vision_analysis", "ux_analysis", "market_analysis"]):
                st.markdown("<h3>Design Analysis Summary</h3>", unsafe_allow_html=True)
                
                for section in ["Vision Analysis", "UX Analysis", "Market Research"]:
                    with st.expander(f"{section}", expanded=True):
                        st.markdown("""
                        <div class="agent-container">
                        """, unsafe_allow_html=True)
                        st.markdown(st.session_state[f"{section.lower().split()[0]}_analysis"])
                        st.markdown("</div>", unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    if st.button("Export Report", use_container_width=True):
                        # Create PDF with adjusted margins for more horizontal space
                        pdf = FPDF(format='A4')
                        # Set smaller margins to have more space for text
                        pdf.set_margins(15, 15, 15)  # left, top, right margins
                        pdf.add_page()
                        
                        # Set default font first with a reasonable size
                        pdf.set_font('Helvetica', '', size=11)
                        
                        # Title
                        pdf.set_font('Helvetica', 'B', size=16)
                        pdf.cell(0, 10, 'Design Analysis Report', align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
                        pdf.ln(5)
                        
                        # Add timestamp
                        pdf.set_font('Helvetica', '', size=8)
                        from datetime import datetime
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        pdf.cell(0, 5, f'Generated on: {timestamp}', align='R', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
                        pdf.ln(10)
                        
                        # Sections
                        sections = {
                            'Vision Analysis': st.session_state["vision_analysis"],
                            'UX Analysis': st.session_state["ux_analysis"],
                            'Market Research': st.session_state["market_analysis"]
                        }
                        
                        def write_text_with_spacing(pdf, text, line_height=5):
                            # Split text into paragraphs
                            paragraphs = text.split('\n')
                            for paragraph in paragraphs:
                                # Clean the paragraph text
                                paragraph = paragraph.strip()
                                if not paragraph:
                                    continue
                                    
                                # Remove any non-ASCII characters
                                paragraph = ''.join(c if ord(c) < 128 else ' ' for c in paragraph)
                                
                                # Calculate available width
                                available_width = pdf.w - pdf.l_margin - pdf.r_margin
                                
                                # Write the paragraph
                                pdf.multi_cell(available_width, line_height, paragraph)
                                pdf.ln(2)  # Add small space between paragraphs
                        
                        for title, content in sections.items():
                            # Check if we need a page break
                            if pdf.get_y() > pdf.h - 40:  # If less than 40mm from bottom
                                pdf.add_page()
                            
                            # Section title
                            pdf.set_font('Helvetica', 'B', size=12)
                            pdf.set_fill_color(240, 240, 240)  # Light gray background
                            pdf.cell(0, 8, title, fill=True, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
                            pdf.ln(4)
                            
                            # Section content
                            pdf.set_font('Helvetica', '', size=10)
                            
                            # Write content with proper spacing
                            write_text_with_spacing(pdf, content)
                            pdf.ln(8)  # Add space between sections
                        
                        # Add footer
                        pdf.set_y(-20)
                        pdf.set_font('Helvetica', 'I', size=8)
                        pdf.cell(0, 10, 'Generated by Multi-Agent Design Analysis Platform', align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
                        
                        try:
                            # Save PDF to bytes
                            pdf_bytes = io.BytesIO()
                            pdf.output(pdf_bytes)
                            
                            # Download button
                            st.download_button(
                                "Download PDF Report",
                                pdf_bytes.getvalue(),
                                file_name="design_analysis_report.pdf",
                                mime="application/pdf",
                                use_container_width=True
                            )
                        except Exception as e:
                            st.error(f"Error generating PDF: {str(e)}")
                            st.info("If you're seeing font-related errors, try updating your system fonts or contact support.") 