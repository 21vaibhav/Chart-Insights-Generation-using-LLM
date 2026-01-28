# input/image_loader.py

from PIL import Image
import io
import streamlit as st
import fitz

def load_image(uploaded_file):
    """
    Load an image file (PNG, JPG, etc.)
    """
    if uploaded_file is None:
        return None
    
    try:
        image = Image.open(uploaded_file)
        return image
    except Exception as e:
        st.error(f"Error loading image: {str(e)}")
        return None


def load_pdf_as_images(uploaded_file):
    """
    Load PDF file and convert all pages to images
    """
    if uploaded_file is None:
        return None
    
    try:
        pdf_bytes = uploaded_file.read()
        pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
        
        images = []
        for page_num in range(len(pdf_document)):
            page = pdf_document[page_num]
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
            img_data = pix.tobytes("ppm")
            img = Image.open(io.BytesIO(img_data))
            images.append(img)
        
        return images
    except Exception as e:
        st.error(f"Error loading PDF: {str(e)}")
        return None 
