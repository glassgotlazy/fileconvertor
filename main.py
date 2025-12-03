import streamlit as st
from PIL import Image
import io
import base64
from pydub import AudioSegment
import tempfile
import os
from docx import Document
from fpdf import FPDF
import pandas as pd

# Page configuration with SEO
st.set_page_config(
    page_title="Free File Format Converter Online - Audio, Video, Image, Document Converter",
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
        - Audio: MP3, WAV, OGG
        - Documents: TXT, PDF, DOCX
        - Spreadsheets: CSV, XLSX
        
        Made with ❤️ using Streamlit
        """
    }
)

# SEO Meta Tags
st.markdown("""
<meta name="description" content="Free online file format converter. Convert images (PNG, JPG, WEBP), audio (MP3, WAV), documents (PDF, DOCX, TXT), and more. Fast, secure, no registration required.">
<meta name="keywords" content="file converter, format converter, image converter, audio converter, PDF converter, document converter, free online converter, PNG to JPG, MP3 to WAV">
<meta name="author" content="Your Name">
<meta name="robots" content="index, follow">
<meta property="og:title" content="Free File Format Converter Online - Convert Any File">
<meta property="og:description" content="Convert files between different formats instantly. Images, audio, documents - all free with no registration.">
<meta property="og:type" content="website">
<meta name="twitter:card" content="summary_large_image">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
""", unsafe_allow_html=True)

# Custom CSS
st.markdown("""
<style>
    /* Main styling */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .main .block-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        backdrop-filter: blur(10px);
    }
    
    .main-title {
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
    }
    
    .subtitle {
        text-align: center;
        color: #6c757d;
        font-size: 1.3rem;
        margin-bottom: 2rem;
    }
    
    /* Conversion cards */
    .conversion-card {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border-left: 5px solid #667eea;
        transition: transform 0.3s ease;
    }
    
    .conversion-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    /* Buttons */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    .stDownloadButton>button {
        width: 100%;
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(56, 239, 125, 0.4);
    }
    
    .stDownloadButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(56, 239, 125, 0.6);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 15px;
        padding: 0.7rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        padding: 12px 24px;
        font-weight: 600;
        color: #495057;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    
    /* Success box */
    .success-box {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        font-size: 1.3rem;
        font-weight: 600;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(56, 239, 125, 0.4);
    }
    
    /* File info */
    .file-info {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        border-left: 4px solid #667eea;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<h1 class="main-title">🔄 File Format Converter</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Convert files between formats instantly - Free & Secure!</p>', unsafe_allow_html=True)

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

def convert_audio(input_file, output_format):
    """Convert audio to different format"""
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(input_file.name)[1]) as tmp_input:
            tmp_input.write(input_file.getvalue())
            tmp_input_path = tmp_input.name
        
        # Load audio
        audio = AudioSegment.from_file(tmp_input_path)
        
        # Export to new format
        output_buffer = io.BytesIO()
        audio.export(output_buffer, format=output_format.lower())
        
        # Cleanup
        os.unlink(tmp_input_path)
        
        return output_buffer.getvalue()
    except Exception as e:
        st.error(f"Error converting audio: {str(e)}")
        return None

def convert_text_to_pdf(text_content, filename="document.pdf"):
    """Convert text to PDF"""
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        
        # Split text into lines and add to PDF
        for line in text_content.split('\n'):
            pdf.multi_cell(0, 10, line)
        
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
tab1, tab2, tab3, tab4 = st.tabs(["🖼️ Image Converter", "🎵 Audio Converter", "📄 Document Converter", "📊 Spreadsheet Converter"])

# TAB 1: Image Converter
with tab1:
    st.markdown("### 🖼️ Image Format Converter")
    st.info("Convert between PNG, JPG, WEBP, BMP, ICO formats")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_image = st.file_uploader(
            "Upload Image",
            type=['png', 'jpg', 'jpeg', 'webp', 'bmp', 'ico'],
            key="image_upload",
            help="Supported: PNG, JPG, WEBP, BMP, ICO"
        )
    
    with col2:
        output_format_img = st.selectbox(
            "Convert to:",
            ["PNG", "JPG", "WEBP", "BMP", "ICO"],
            key="img_format"
        )
    
    if uploaded_image:
        col1, col2 = st.columns(2)
        
        with col1:
            st.image(uploaded_image, caption="Original Image", use_container_width=True)
            st.markdown(f'<div class="file-info">📁 <b>File:</b> {uploaded_image.name}<br>📊 <b>Size:</b> {get_file_size(uploaded_image)}</div>', unsafe_allow_html=True)
        
        with col2:
            if st.button("🔄 Convert Image", key="convert_img_btn", type="primary"):
                with st.spinner("Converting image..."):
                    converted = convert_image(uploaded_image, output_format_img)
                    
                    if converted:
                        st.markdown('<div class="success-box">✅ Image Converted Successfully!</div>', unsafe_allow_html=True)
                        
                        # Preview converted image
                        st.image(converted, caption=f"Converted to {output_format_img}", use_container_width=True)
                        
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

# TAB 2: Audio Converter
with tab2:
    st.markdown("### 🎵 Audio Format Converter")
    st.info("Convert between MP3, WAV, OGG formats")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_audio = st.file_uploader(
            "Upload Audio File",
            type=['mp3', 'wav', 'ogg', 'm4a', 'flac'],
            key="audio_upload",
            help="Supported: MP3, WAV, OGG, M4A, FLAC"
        )
    
    with col2:
        output_format_audio = st.selectbox(
            "Convert to:",
            ["MP3", "WAV", "OGG"],
            key="audio_format"
        )
    
    if uploaded_audio:
        st.markdown(f'<div class="file-info">📁 <b>File:</b> {uploaded_audio.name}<br>📊 <b>Size:</b> {get_file_size(uploaded_audio)}</div>', unsafe_allow_html=True)
        
        st.audio(uploaded_audio, format=f'audio/{os.path.splitext(uploaded_audio.name)[1][1:]}')
        
        if st.button("🔄 Convert Audio", key="convert_audio_btn", type="primary"):
            with st.spinner("Converting audio... This may take a moment"):
                converted = convert_audio(uploaded_audio, output_format_audio)
                
                if converted:
                    st.markdown('<div class="success-box">✅ Audio Converted Successfully!</div>', unsafe_allow_html=True)
                    
                    # Preview
                    st.audio(converted, format=f'audio/{output_format_audio.lower()}')
                    
                    # Get size
                    converted_size = len(converted)
                    if converted_size < 1024 * 1024:
                        size_str = f"{converted_size / 1024:.2f} KB"
                    else:
                        size_str = f"{converted_size / (1024 * 1024):.2f} MB"
                    
                    st.info(f"📊 Converted Size: {size_str}")
                    
                    # Download
                    original_name = os.path.splitext(uploaded_audio.name)[0]
                    st.download_button(
                        "⬇️ Download Converted Audio",
                        converted,
                        f"{original_name}.{output_format_audio.lower()}",
                        f"audio/{output_format_audio.lower()}",
                        use_container_width=True
                    )

# TAB 3: Document Converter
with tab3:
    st.markdown("### 📄 Document Format Converter")
    st.info("Convert between TXT, PDF, DOCX formats")
    
    conversion_type = st.radio(
        "Select Conversion:",
        ["Text to PDF", "CSV to Excel", "Excel to CSV"],
        horizontal=True
    )
    
    if conversion_type == "Text to PDF":
        text_input = st.text_area(
            "Enter or paste your text:",
            height=300,
            placeholder="Type or paste your text here..."
        )
        
        if text_input:
            st.info(f"📝 Characters: {len(text_input)} | Words: {len(text_input.split())}")
            
            if st.button("🔄 Convert to PDF", type="primary"):
                with st.spinner("Creating PDF..."):
                    pdf_data = convert_text_to_pdf(text_input)
                    
                    if pdf_data:
                        st.markdown('<div class="success-box">✅ PDF Created Successfully!</div>', unsafe_allow_html=True)
                        
                        st.download_button(
                            "⬇️ Download PDF",
                            pdf_data,
                            "document.pdf",
                            "application/pdf",
                            use_container_width=True
                        )
    
    elif conversion_type == "CSV to Excel":
        csv_file = st.file_uploader("Upload CSV File", type=['csv'], key="csv_upload")
        
        if csv_file:
            st.markdown(f'<div class="file-info">📁 <b>File:</b> {csv_file.name}<br>📊 <b>Size:</b> {get_file_size(csv_file)}</div>', unsafe_allow_html=True)
            
            # Preview CSV
            df = pd.read_csv(csv_file)
            st.dataframe(df.head(10), use_container_width=True)
            st.caption(f"Showing first 10 rows of {len(df)} total rows")
            
            if st.button("🔄 Convert to Excel", type="primary"):
                with st.spinner("Converting to Excel..."):
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
        xlsx_file = st.file_uploader("Upload Excel File", type=['xlsx', 'xls'], key="xlsx_upload")
        
        if xlsx_file:
            st.markdown(f'<div class="file-info">📁 <b>File:</b> {xlsx_file.name}<br>📊 <b>Size:</b> {get_file_size(xlsx_file)}</div>', unsafe_allow_html=True)
            
            # Preview Excel
            df = pd.read_excel(xlsx_file)
            st.dataframe(df.head(10), use_container_width=True)
            st.caption(f"Showing first 10 rows of {len(df)} total rows")
            
            if st.button("🔄 Convert to CSV", type="primary"):
                with st.spinner("Converting to CSV..."):
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

# TAB 4: Spreadsheet Converter (Alternative view)
with tab4:
    st.markdown("### 📊 Spreadsheet Converter")
    st.info("Batch convert CSV ↔ Excel files")
    
    st.markdown("""
    **Quick Conversions:**
    - CSV → Excel: Add formatting, multiple sheets
    - Excel → CSV: Simple text format, universal compatibility
    """)
    
    uploaded_file = st.file_uploader(
        "Upload Spreadsheet",
        type=['csv', 'xlsx', 'xls'],
        key="spreadsheet_upload"
    )
    
    if uploaded_file:
        file_ext = os.path.splitext(uploaded_file.name)[1].lower()
        
        st.markdown(f'<div class="file-info">📁 <b>File:</b> {uploaded_file.name}<br>📊 <b>Size:</b> {get_file_size(uploaded_file)}<br>📝 <b>Type:</b> {file_ext[1:].upper()}</div>', unsafe_allow_html=True)
        
        # Auto-detect and suggest conversion
        if file_ext == '.csv':
            st.success("CSV file detected → Convert to Excel")
            
            df = pd.read_csv(uploaded_file)
            st.dataframe(df.head(10), use_container_width=True)
            
            if st.button("🔄 Convert to Excel", key="auto_csv", type="primary"):
                xlsx_data = convert_csv_to_xlsx(uploaded_file)
                if xlsx_data:
                    st.markdown('<div class="success-box">✅ Converted Successfully!</div>', unsafe_allow_html=True)
                    st.download_button(
                        "⬇️ Download Excel",
                        xlsx_data,
                        f"{os.path.splitext(uploaded_file.name)[0]}.xlsx",
                        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )
        else:
            st.success("Excel file detected → Convert to CSV")
            
            df = pd.read_excel(uploaded_file)
            st.dataframe(df.head(10), use_container_width=True)
            
            if st.button("🔄 Convert to CSV", key="auto_xlsx", type="primary"):
                csv_data = convert_xlsx_to_csv(uploaded_file)
                if csv_data:
                    st.markdown('<div class="success-box">✅ Converted Successfully!</div>', unsafe_allow_html=True)
                    st.download_button(
                        "⬇️ Download CSV",
                        csv_data,
                        f"{os.path.splitext(uploaded_file.name)[0]}.csv",
                        "text/csv",
                        use_container_width=True
                    )

# Footer with information
st.markdown("---")
with st.expander("ℹ️ Supported Formats & Tips"):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 🖼️ Images
        **Supported:**
        - PNG (Lossless, transparency)
        - JPG/JPEG (Compressed, smaller)
        - WEBP (Modern, efficient)
        - BMP (Uncompressed)
        - ICO (Icons)
        
        **Best Use:**
        - Web: WEBP or JPG
        - Print: PNG or BMP
        - Icons: ICO
        """)
    
    with col2:
        st.markdown("""
        ### 🎵 Audio
        **Supported:**
        - MP3 (Universal, compressed)
        - WAV (Uncompressed, quality)
        - OGG (Open format, good compression)
        
        **Best Use:**
        - Music: MP3
        - Editing: WAV
        - Streaming: OGG
        """)
    
    with col3:
        st.markdown("""
        ### 📄 Documents
        **Supported:**
        - PDF (Universal, print-ready)
        - CSV (Data, universal)
        - XLSX (Excel, formatted)
        - TXT (Plain text)
        
        **Best Use:**
        - Sharing: PDF
        - Data analysis: CSV/XLSX
        - Simple text: TXT
        """)

st.markdown("---")

with st.expander("🔒 Privacy & Security"):
    st.markdown("""
    ### Your Privacy Matters
    
    ✅ **All conversions happen in your browser** - Files never leave your device  
    ✅ **No storage** - Files are not saved on any server  
    ✅ **No tracking** - We don't collect or store your data  
    ✅ **100% Free** - No registration, no hidden fees  
    ✅ **Secure** - HTTPS encryption for all transfers  
    
    ### How It Works
    1. Upload your file
    2. Choose output format
    3. File is processed locally in your browser
    4. Download converted file
    5. Original file is automatically discarded
    
    **Note:** For large audio files (>50MB), conversion may take a few minutes.
    """)

st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 1rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
border-radius: 10px; color: white; font-weight: 600;">
    🔄 Made with ❤️ using Streamlit | Fast, Secure, & 100% Free File Converter
</div>
""", unsafe_allow_html=True)
