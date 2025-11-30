import re


def detect_sections(text):
    """
    Detect different sections in resume text
    
    Args:
        text (str): Resume text content
    
    Returns:
        dict: Dictionary with detected sections and their status
    """
    text_lower = text.lower()
    
    sections = {
        "contact_info": False,
        "summary": False,
        "experience": False,
        "education": False,
        "skills": False,
        "projects": False,
        "certifications": False,
        "languages": False
    }
    
    # Contact Info Detection (email, phone, LinkedIn, etc.)
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
    
    if re.search(email_pattern, text) or re.search(phone_pattern, text):
        sections["contact_info"] = True
    
    # Summary/Objective Detection
    summary_keywords = ['summary', 'objective', 'profile', 'about me', 'professional summary']
    if any(keyword in text_lower for keyword in summary_keywords):
        sections["summary"] = True
    
    # Experience Detection
    experience_keywords = ['experience', 'work history', 'employment', 'professional experience', 'work experience']
    if any(keyword in text_lower for keyword in experience_keywords):
        sections["experience"] = True
    
    # Education Detection
    education_keywords = ['education', 'academic', 'degree', 'university', 'college', 'bachelor', 'master', 'phd']
    if any(keyword in text_lower for keyword in education_keywords):
        sections["education"] = True
    
    # Skills Detection
    skills_keywords = ['skills', 'technical skills', 'core competencies', 'technologies', 'expertise']
    if any(keyword in text_lower for keyword in skills_keywords):
        sections["skills"] = True
    
    # Projects Detection
    projects_keywords = ['projects', 'portfolio', 'work samples']
    if any(keyword in text_lower for keyword in projects_keywords):
        sections["projects"] = True
    
    # Certifications Detection
    cert_keywords = ['certification', 'certificate', 'licensed', 'credentials']
    if any(keyword in text_lower for keyword in cert_keywords):
        sections["certifications"] = True
    
    # Languages Detection
    language_keywords = ['languages', 'language proficiency', 'linguistic skills']
    if any(keyword in text_lower for keyword in language_keywords):
        sections["languages"] = True
    
    return sections


def extract_contact_details(text):
    """
    Extract specific contact details from resume
    
    Returns:
        dict: Extracted contact information
    """
    contact = {
        "email": None,
        "phone": None,
        "linkedin": None,
        "github": None
    }
    
    # Email extraction
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    email_match = re.search(email_pattern, text)
    if email_match:
        contact["email"] = email_match.group(0)
    
    # Phone extraction
    phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
    phone_match = re.search(phone_pattern, text)
    if phone_match:
        contact["phone"] = phone_match.group(0)
    
    # LinkedIn extraction
    linkedin_pattern = r'linkedin\.com/in/[\w-]+'
    linkedin_match = re.search(linkedin_pattern, text.lower())
    if linkedin_match:
        contact["linkedin"] = linkedin_match.group(0)
    
    # GitHub extraction
    github_pattern = r'github\.com/[\w-]+'
    github_match = re.search(github_pattern, text.lower())
    if github_match:
        contact["github"] = github_match.group(0)
    
    return contact