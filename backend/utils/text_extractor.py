import os
from docx import Document
import PyPDF2


def extract_text(filepath):
    """
    Extract text from PDF, DOCX, or TXT files
    
    Args:
        filepath (str): Path to the resume file
    
    Returns:
        str: Extracted text from the resume
    """
    file_extension = filepath.lower().split('.')[-1]
    
    try:
        if file_extension == 'pdf':
            return extract_from_pdf(filepath)
        elif file_extension == 'docx':
            return extract_from_docx(filepath)
        elif file_extension == 'txt':
            return extract_from_txt(filepath)
        else:
            return None
    except Exception as e:
        print(f"Error extracting text: {str(e)}")
        return None


def extract_from_pdf(filepath):
    """Extract text from PDF file"""
    text = ""
    try:
        with open(filepath, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        print(f"PDF extraction error: {str(e)}")
        return None


def extract_from_docx(filepath):
    """Extract text from DOCX file"""
    try:
        doc = Document(filepath)
        text = []
        for paragraph in doc.paragraphs:
            text.append(paragraph.text)
        return "\n".join(text).strip()
    except Exception as e:
        print(f"DOCX extraction error: {str(e)}")
        return None


def extract_from_txt(filepath):
    """Extract text from TXT file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return file.read().strip()
    except Exception as e:
        print(f"TXT extraction error: {str(e)}")
        return None