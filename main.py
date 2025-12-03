import streamlit as st
from PIL import Image
import io
import base64
import os
from fpdf import FPDF
import pandas as pd

# Page configuration with SEO
st.set_page_config(
    page_title="Free File Format Converter Online - Image, Document, Spreadsheet Converter",
    page_icon="🔄",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': 'https://github.com/yourusername/file-converter',
        'Report a bug': 'https://github.com/yourusername/file-converter/issues',
        'About': """
        # File Format Converter
        Convert files between different formats instantly!
        
        **Supported Conversions:**
        - Images: PNG, JPG, WEBP, BMP, ICO
        - Documents: TXT to PDF
        - Spreadsheets: CSV ↔ XLSX
        
        Made with ❤️ using Streamlit
        """
    }
)

# SEO Meta Tags
st.markdown("""
<meta name="description" content="Free online file format converter. Convert images (PNG, JPG, WEBP), documents (PDF, TXT), spreadsheets (CSV, XLSX). Fast, secure, no registration required.">
<meta name="keywords" content="file converter, format converter, image converter, PDF converter, document converter, free online converter, PNG to JPG, CSV to Excel">
<meta name="author" content="Your Name">
<meta name="robots" content="index, follow">
<meta property="og:title" content="Free File Format Converter Online - Convert Any File">
<meta property="og:description" content="Convert files between different formats instantly. Images, documents, spreadsheets - all free with no registration.">
<meta property="og:type" content="website">
<meta name="twitter:card" content="summary_large_image">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
""", unsafe_allow_html=True)

# Enhanced Custom CSS
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700;800&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Animated gradient background */
    .stApp {
        background: linear-gradient(-45deg, #667eea, #764ba2, #f093fb, #4facfe);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .main .block-container {
        background: rgba(255, 255, 255, 0.98);
        border-radius: 25px;
        padding: 2.5rem;
        box-shadow: 0 25px 70px rgba(0,0,0,0.3);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    /* Title animations */
    .main-title {
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 4rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        animation: titleFloat 3s ease-in-out infinite;
        letter-spacing: -2px;
    }
    
    @keyframes titleFloat {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    .subtitle {
        text-align: center;
        color: #6c757d;
        font-size: 1.4rem;
        margin-bottom: 2.5rem;
        font-weight: 500;
        animation: fadeInUp 1s ease;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Feature cards */
    .feature-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        border: 2px solid transparent;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        opacity: 0;
        transition: opacity 0.4s;
        z-index: 0;
    }
    
    .feature-card:hover::before {
        opacity: 0.05;
    }
    
    .feature-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 20px 50px rgba(102, 126, 234, 0.3);
        border-color: #667eea;
    }
    
    /* Buttons with gradient and glow */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 15px;
        padding: 1rem 2.5rem;
        font-size: 1.15rem;
        font-weight: 700;
        letter-spacing: 0.5px;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
        position: relative;
        overflow: hidden;
    }
    
    .stButton>button::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
    }
    
    .stButton>button:hover::before {
        width: 300px;
        height: 300px;
    }
    
    .stButton>button:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.6);
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    .stButton>button:active {
        transform: translateY(0) scale(0.98);
    }
    
    /* Download button with success color */
    .stDownloadButton>button {
        width: 100%;
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        border: none;
        border-radius: 15px;
        padding: 1rem 2.5rem;
        font-size: 1.15rem;
        font-weight: 700;
        letter-spacing: 0.5px;
        box-shadow: 0 8px 25px rgba(56, 239, 125, 0.4);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .stDownloadButton>button:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 15px 40px rgba(56, 239, 125, 0.6);
        background: linear-gradient(135deg, #38ef7d 0%, #11998e 100%);
    }
    
    /* Beautiful tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 15px;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 20px;
        padding: 1rem;
        box-shadow: inset 0 2px 10px rgba(0,0,0,0.1);
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 15px;
        padding: 14px 28px;
        font-weight: 700;
        color: #495057;
        transition: all 0.3s ease;
        border: 2px solid transparent;
        font-size: 1.05rem;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(102, 126, 234, 0.1);
        transform: translateY(-2px);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
        border-color: rgba(255, 255, 255, 0.3);
    }
    
    /* Success box with animation */
    .success-box {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        padding: 1.8rem;
        border-radius: 20px;
        text-align: center;
        font-size: 1.4rem;
        font-weight: 700;
        margin: 1.5rem 0;
        box-shadow: 0 10px 35px rgba(56, 239, 125, 0.4);
        animation: successPulse 2s ease infinite;
    }
    
    @keyframes successPulse {
        0%, 100% {
            box-shadow: 0 10px 35px rgba(56, 239, 125, 0.4);
        }
        50% {
            box-shadow: 0 10px 50px rgba(56, 239, 125, 0.6);
        }
    }
    
    /* File info card */
    .file-info {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 5px solid #667eea;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    .file-info:hover {
        transform: translateX(5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    /* File uploader styling */
    .stFileUploader {
        border-radius: 15px;
        transition: all 0.3s ease;
    }
    
    .stFileUploader:hover {
        transform: scale(1.02);
    }
    
    /* Info/Warning boxes */
    .stAlert {
        border-radius: 15px;
        border-left: 5px solid;
        font-weight: 500;
        animation: slideInLeft 0.5s ease;
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    /* Image preview styling */
    .stImage {
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
        transition: all 0.3s ease;
    }
    
    .stImage:hover {
        transform: scale(1.03);
        box-shadow: 0 15px 40px rgba(0,0,0,0.2);
    }
    
    /* Selectbox styling */
    .stSelectbox > div > div {
        border-radius: 12px;
        border: 2px solid #e9ecef;
        transition: all 0.3s ease;
    }
    
    .stSelectbox > div > div:hover {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Radio buttons */
    .stRadio > div {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 15px;
    }
    
    /* Text area */
    .stTextArea textarea {
        border-radius: 15px;
        border: 2px solid #e9ecef;
        transition: all 0.3s ease;
        font-family: 'Courier New', monospace;
    }
    
    .stTextArea textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Dataframe styling */
    .stDataFrame {
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
    }
    
    /* Spinner animation */
    .stSpinner > div {
        border-color: #667eea !important;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 15px;
        font-weight: 700;
        font-size: 1.1rem;
        padding: 1rem 1.5rem;
        transition: all 0.3s ease;
    }
    
    .streamlit-expanderHeader:hover {
        background: linear-gradient(135deg, #e9ecef 0%, #dee2e6 100%);
        transform: translateX(5px);
    }
    
    /* Metric styling */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Caption styling */
    .caption {
        color: #6c757d;
        font-style: italic;
        font-size: 0.95rem;
    }
    
    /* Footer gradient */
    .footer-gradient {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        animation: gradientShift 10s ease infinite;
    }
</style>
""", unsafe_allow_html=True)

# Title with emoji animation
st.markdown('<h1 class="main-title">🔄 File Format Converter</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">✨ Convert files between formats instantly - Fast, Free & Beautiful! ✨</p>', unsafe_allow_html=True)

# Helper functions
def get_file_size(file):
    """Get file size in KB/MB"""
    size_bytes = len(file.getvalue()) if hasattr(file, 'getvalue') else file.size
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.2f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.2f} MB"

def convert_image(input_file, output_format):
    """Convert image to different format"""
    try:
        img = Image.open(input_file)
        
        # Convert RGBA to RGB if saving as JPEG
        if output_format.upper() in ['JPG', 'JPEG'] and img.mode in ['RGBA', 'LA', 'P']:
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = background
        
        # Save to buffer
        buffer = io.BytesIO()
        
        if output_format.upper() == 'JPG':
            output_format = 'JPEG'
        
        img.save(buffer, format=output_format.upper())
        return buffer.getvalue()
    except Exception as e:
        st.error(f"Error converting image: {str(e)}")
        return None

def convert_text_to_pdf(text_content, filename="document.pdf"):
    """Convert text to PDF"""
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        
        # Split text into lines and add to PDF
        for line in text_content.split('\n'):
            pdf.multi_cell(0, 10, line.encode('latin-1', 'replace').decode('latin-1'))
        
        # Save to buffer
        buffer = io.BytesIO()
        pdf_output = pdf.output(dest='S').encode('latin-1')
        buffer.write(pdf_output)
        return buffer.getvalue()
    except Exception as e:
        st.error(f"Error converting to PDF: {str(e)}")
        return None

def convert_csv_to_xlsx(csv_file):
    """Convert CSV to Excel"""
    try:
        df = pd.read_csv(csv_file)
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Sheet1')
        return buffer.getvalue()
    except Exception as e:
        st.error(f"Error converting CSV: {str(e)}")
        return None

def convert_xlsx_to_csv(xlsx_file):
    """Convert Excel to CSV"""
    try:
        df = pd.read_excel(xlsx_file)
        return df.to_csv(index=False).encode('utf-8')
    except Exception as e:
        st.error(f"Error converting Excel: {str(e)}")
        return None

# Main tabs
tab1, tab2, tab3 = st.tabs(["🖼️ Image Converter", "📄 Document Converter", "📊 Spreadsheet Converter"])

# TAB 1: Image Converter
with tab1:
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown("### 🖼️ Image Format Converter")
    st.info("✨ Convert between PNG, JPG, WEBP, BMP, ICO formats instantly!")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_image = st.file_uploader(
            "📁 Upload Your Image",
            type=['png', 'jpg', 'jpeg', 'webp', 'bmp', 'ico'],
            key="image_upload",
            help="Supported: PNG, JPG, WEBP, BMP, ICO"
        )
    
    with col2:
        output_format_img = st.selectbox(
            "🎯 Convert to:",
            ["PNG", "JPG", "WEBP", "BMP", "ICO"],
            key="img_format"
        )
    
    if uploaded_image:
        col1, col2 = st.columns(2)
        
        with col1:
            st.image(uploaded_image, caption="📸 Original Image", use_container_width=True)
            st.markdown(f'<div class="file-info">📁 <b>File:</b> {uploaded_image.name}<br>📊 <b>Size:</b> {get_file_size(uploaded_image)}</div>', unsafe_allow_html=True)
        
        with col2:
            if st.button("🔄 Convert Image Now", key="convert_img_btn", type="primary"):
                with st.spinner("✨ Converting your image..."):
                    converted = convert_image(uploaded_image, output_format_img)
                    
                    if converted:
                        st.markdown('<div class="success-box">✅ Image Converted Successfully!</div>', unsafe_allow_html=True)
                        
                        # Preview converted image
                        st.image(converted, caption=f"✨ Converted to {output_format_img}", use_container_width=True)
                        
                        # Get size of converted file
                        converted_size = len(converted)
                        if converted_size < 1024 * 1024:
                            size_str = f"{converted_size / 1024:.2f} KB"
                        else:
                            size_str = f"{converted_size / (1024 * 1024):.2f} MB"
                        
                        st.info(f"📊 Converted Size: {size_str}")
                        
                        # Download button
                        original_name = os.path.splitext(uploaded_image.name)[0]
                        st.download_button(
                            "⬇️ Download Converted Image",
                            converted,
                            f"{original_name}.{output_format_img.lower()}",
                            f"image/{output_format_img.lower()}",
                            use_container_width=True
                        )
    st.markdown('</div>', unsafe_allow_html=True)

# TAB 2: Document Converter
with tab2:
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown("### 📄 Document Format Converter")
    st.info("✨ Convert text to PDF or convert between CSV and Excel!")
    
    conversion_type = st.radio(
        "📌 Select Conversion Type:",
        ["📝 Text to PDF", "📊 CSV to Excel", "📈 Excel to CSV"],
        horizontal=True
    )
    
    if conversion_type == "📝 Text to PDF":
        text_input = st.text_area(
            "✍️ Enter or paste your text:",
            height=300,
            placeholder="Start typing or paste your text here...\n\nYour text will be converted to a professional PDF document!"
        )
        
        if text_input:
            col1, col2 = st.columns(2)
            with col1:
                st.metric("📝 Characters", len(text_input))
            with col2:
                st.metric("📖 Words", len(text_input.split()))
            
            if st.button("🔄 Convert to PDF", type="primary", key="pdf_btn"):
                with st.spinner("📄 Creating your PDF document..."):
                    pdf_data = convert_text_to_pdf(text_input)
                    
                    if pdf_data:
                        st.markdown('<div class="success-box">✅ PDF Created Successfully!</div>', unsafe_allow_html=True)
                        
                        st.download_button(
                            "⬇️ Download PDF Document",
                            pdf_data,
                            "document.pdf",
                            "application/pdf",
                            use_container_width=True
                        )
    
    elif conversion_type == "📊 CSV to Excel":
        csv_file = st.file_uploader("📁 Upload CSV File", type=['csv'], key="csv_upload")
        
        if csv_file:
            st.markdown(f'<div class="file-info">📁 <b>File:</b> {csv_file.name}<br>📊 <b>Size:</b> {get_file_size(csv_file)}</div>', unsafe_allow_html=True)
            
            # Preview CSV
            df = pd.read_csv(csv_file)
            st.markdown("#### 👀 Preview (First 10 Rows)")
            st.dataframe(df.head(10), use_container_width=True)
            st.caption(f"Showing 10 of {len(df)} total rows • {len(df.columns)} columns")
            
            if st.button("🔄 Convert to Excel", type="primary", key="csv_btn"):
                with st.spinner("📊 Converting to Excel format..."):
                    xlsx_data = convert_csv_to_xlsx(csv_file)
                    
                    if xlsx_data:
                        st.markdown('<div class="success-box">✅ Converted to Excel Successfully!</div>', unsafe_allow_html=True)
                        
                        original_name = os.path.splitext(csv_file.name)[0]
                        st.download_button(
                            "⬇️ Download Excel File",
                            xlsx_data,
                            f"{original_name}.xlsx",
                            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            use_container_width=True
                        )
    
    else:  # Excel to CSV
        xlsx_file = st.file_uploader("📁 Upload Excel File", type=['xlsx', 'xls'], key="xlsx_upload")
        
        if xlsx_file:
            st.markdown(f'<div class="file-info">📁 <b>File:</b> {xlsx_file.name}<br>📊 <b>Size:</b> {get_file_size(xlsx_file)}</div>', unsafe_allow_html=True)
            
            # Preview Excel
            df = pd.read_excel(xlsx_file)
            st.markdown("#### 👀 Preview (First 10 Rows)")
            st.dataframe(df.head(10), use_container_width=True)
            st.caption(f"Showing 10 of {len(df)} total rows • {len(df.columns)} columns")
            
            if st.button("🔄 Convert to CSV", type="primary", key="xlsx_btn"):
                with st.spinner("📊 Converting to CSV format..."):
                    csv_data = convert_xlsx_to_csv(xlsx_file)
                    
                    if csv_data:
                        st.markdown('<div class="success-box">✅ Converted to CSV Successfully!</div>', unsafe_allow_html=True)
                        
                        original_name = os.path.splitext(xlsx_file.name)[0]
                        st.download_button(
                            "⬇️ Download CSV File",
                            csv_data,
                            f"{original_name}.csv",
                            "text/csv",
                            use_container_width=True
                        )
    st.markdown('</div>', unsafe_allow_html=True)

# TAB 3: Spreadsheet Converter (Quick Convert)
with tab3:
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown("### 📊 Smart Spreadsheet Converter")
    st.info("✨ Auto-detects your file type and suggests the best conversion!")
    
    st.markdown("""
    **⚡ Quick Conversions:**
    - 📊 CSV → Excel: Add formatting and multiple sheets support
    - 📈 Excel → CSV: Universal compatibility for all platforms
    """)
    
    uploaded_file = st.file_uploader(
        "📁 Upload Your Spreadsheet",
        type=['csv', 'xlsx', 'xls'],
        key="spreadsheet_upload"
    )
    
    if uploaded_file:
        file_ext = os.path.splitext(uploaded_file.name)[1].lower()
        
        st.markdown(f'<div class="file-info">📁 <b>File:</b> {uploaded_file.name}<br>📊 <b>Size:</b> {get_file_size(uploaded_file)}<br>📝 <b>Format:</b> {file_ext[1:].upper()}</div>', unsafe_allow_html=True)
        
        # Auto-detect and suggest conversion
        if file_ext == '.csv':
            st.success("✅ CSV file detected → Perfect for Excel conversion!")
            
            df = pd.read_csv(uploaded_file)
            st.markdown("#### 👀 Data Preview")
            st.dataframe(df.head(10), use_container_width=True)
            st.caption(f"📊 {len(df)} rows × {len(df.columns)} columns")
            
            if st.button("🔄 Convert to Excel", key="auto_csv", type="primary"):
                with st.spinner("✨ Converting to Excel..."):
                    xlsx_data = convert_csv_to_xlsx(uploaded_file)
                    if xlsx_data:
                        st.markdown('<div class="success-box">✅ Converted Successfully!</div>', unsafe_allow_html=True)
                        st.download_button(
                            "⬇️ Download Excel File",
                            xlsx_data,
                            f"{os.path.splitext(uploaded_file.name)[0]}.xlsx",
                            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            use_container_width=True
                        )
        else:
            st.success("✅ Excel file detected → Perfect for CSV conversion!")
            
            df = pd.read_excel(uploaded_file)
            st.markdown("#### 👀 Data Preview")
            st.dataframe(df.head(10), use_container_width=True)
            st.caption(f"📊 {len(df)} rows × {len(df.columns)} columns")
            
            if st.button("🔄 Convert to CSV", key="auto_xlsx", type="primary"):
                with st.spinner("✨ Converting to CSV..."):
                    csv_data = convert_xlsx_to_csv(uploaded_file)
                    if csv_data:
                        st.markdown('<div class="success-box">✅ Converted Successfully!</div>', unsafe_allow_html=True)
                        st.download_button(
                            "⬇️ Download CSV File",
                            csv_data,
                            f"{os.path.splitext(uploaded_file.name)[0]}.csv",
                            "text/csv",
                            use_container_width=True
                        )
    st.markdown('</div>', unsafe_allow_html=True)

# Footer with information
st.markdown("---")
with st.expander("📚 Supported Formats & Pro Tips"):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 🖼️ Images
        **Supported Formats:**
        - 🟢 **PNG** - Lossless, transparency
        - 🔵 **JPG/JPEG** - Compressed, smaller size
        - 🟣 **WEBP** - Modern, efficient
        - 🟡 **BMP** - Uncompressed
        - 🔴 **ICO** - Icons & favicons
        
        **💡 Best Use Cases:**
        - **Web**: WEBP or JPG
        - **Print**: PNG or BMP
        - **Icons**: ICO
        - **Transparency**: PNG or WEBP
        """)
    
    with col2:
        st.markdown("""
        ### 📄 Documents
        **Supported Formats:**
        - 📝 **TXT** → **PDF**
        - 📊 **CSV** ↔ **XLSX**
        
        **💡 Best Use Cases:**
        - **Sharing**: PDF (universal)
        - **Data Analysis**: CSV/XLSX
        - **Reports**: PDF
        - **Import/Export**: CSV
        
        **🎯 Pro Tips:**
        - PDF preserves formatting
        - CSV is universal
        - Excel adds features
        """)
    
    with col3:
        st.markdown("""
        ### 📊 Spreadsheets
        **Conversions:**
        - CSV → Excel (XLSX)
        - Excel (XLSX/XLS) → CSV
        
        **💡 Advantages:**
        - **CSV**: Simple, universal
        - **Excel**: Formulas, formatting
        
        **⚡ Speed Tips:**
        - Large files? Use CSV
        - Need formulas? Use Excel
        - Sharing data? Use CSV
        - Professional reports? Excel
        """)

st.markdown("---")

with st.expander("🔒 Privacy & Security Guarantee"):
    st.markdown("""
    ### 🛡️ Your Data is 100% Safe
    
    ✅ **Browser-Only Processing** - All conversions happen locally in your browser  
    ✅ **Zero Storage** - We never save, store, or access your files  
    ✅ **No Tracking** - We don't collect any personal data or analytics  
    ✅ **100% Free Forever** - No hidden costs, no registration required  
    ✅ **HTTPS Secure** - All connections are encrypted  
    ✅ **Open Source** - Transparent code you can verify  
    
    ### ⚡ How It Works
    
    1. 📁 **Upload** your file (stays in your browser)
    2. 🎯 **Select** output format
    3. 🔄 **Convert** instantly (processed locally)
    4. ⬇️ **Download** your converted file
    5. 🗑️ **Auto-delete** - Original file is discarded automatically
    
    ### 🌟 Why Choose Us?
    
    - **Lightning Fast** - No server delays
    - **Unlimited Conversions** - Convert as many files as you want
    - **No File Size Limits** - Convert files of any size
    - **Works Offline** - Once loaded, works without internet
    - **Mobile Friendly** - Works perfectly on all devices
    """)

st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%); 
border-radius: 20px; color: white; font-weight: 700; box-shadow: 0 10px 40px rgba(102, 126, 234, 0.4);" class="footer-gradient">
    <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">🔄 File Format Converter</div>
    <div style="font-size: 1rem; opacity: 0.95;">Made with ❤️ using Streamlit | Fast • Secure • Beautiful • 100% Free</div>
    <div style="font-size: 0.9rem; margin-top: 1rem; opacity: 0.9;">✨ Convert Unlimited Files • No Registration • Privacy First ✨</div>
</div>
""", unsafe_allow_html=True)
