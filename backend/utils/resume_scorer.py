import re


def score_resume(text, sections, job_description=""):
    """
    Score resume based on multiple criteria
    
    Args:
        text (str): Resume text
        sections (dict): Detected sections
        job_description (str): Optional job description for matching
    
    Returns:
        dict: Score breakdown and overall score
    """
    scores = {
        "overall_score": 0,
        "section_score": 0,
        "length_score": 0,
        "keyword_score": 0,
        "formatting_score": 0,
        "jd_match_score": 0,
        "suggestions": []
    }
    
    # 1. Section Completeness Score (30 points)
    section_score = calculate_section_score(sections, scores["suggestions"])
    scores["section_score"] = section_score
    
    # 2. Length Score (20 points)
    length_score = calculate_length_score(text, scores["suggestions"])
    scores["length_score"] = length_score
    
    # 3. Keyword Density Score (20 points)
    keyword_score = calculate_keyword_score(text, scores["suggestions"])
    scores["keyword_score"] = keyword_score
    
    # 4. Formatting Score (15 points)
    formatting_score = calculate_formatting_score(text, scores["suggestions"])
    scores["formatting_score"] = formatting_score
    
    # 5. Job Description Match Score (15 points)
    jd_match_score = calculate_jd_match(text, job_description, scores["suggestions"])
    scores["jd_match_score"] = jd_match_score
    
    # Calculate overall score (out of 100)
    scores["overall_score"] = round(
        section_score + length_score + keyword_score + formatting_score + jd_match_score
    )
    
    return scores


def calculate_section_score(sections, suggestions):
    """Score based on presence of key sections"""
    required_sections = ["contact_info", "experience", "education", "skills"]
    optional_sections = ["summary", "projects", "certifications"]
    
    score = 0
    
    # Required sections (20 points - 5 each)
    for section in required_sections:
        if sections.get(section):
            score += 5
        else:
            suggestions.append(f"Missing required section: {section.replace('_', ' ').title()}")
    
    # Optional sections (10 points - 3.33 each)
    for section in optional_sections:
        if sections.get(section):
            score += 3.33
    
    return round(score)


def calculate_length_score(text, suggestions):
    """Score based on resume length"""
    word_count = len(text.split())
    
    if 300 <= word_count <= 800:
        score = 20
    elif 200 <= word_count < 300 or 800 < word_count <= 1000:
        score = 15
        suggestions.append("Resume length could be optimized (aim for 300-800 words)")
    elif 100 <= word_count < 200 or 1000 < word_count <= 1500:
        score = 10
        suggestions.append("Resume is too short/long. Optimal range: 300-800 words")
    else:
        score = 5
        suggestions.append("Resume length is significantly outside optimal range")
    
    return score


def calculate_keyword_score(text, suggestions):
    """Score based on presence of strong action verbs and keywords"""
    text_lower = text.lower()
    
    # Strong action verbs
    action_verbs = [
        'achieved', 'improved', 'developed', 'managed', 'led', 'created',
        'implemented', 'designed', 'built', 'launched', 'optimized', 'increased',
        'reduced', 'streamlined', 'coordinated', 'executed', 'delivered'
    ]
    
    # Technical/professional keywords
    professional_keywords = [
        'project', 'team', 'analysis', 'strategy', 'solution', 'system',
        'process', 'data', 'customer', 'business', 'technical', 'development'
    ]
    
    action_verb_count = sum(1 for verb in action_verbs if verb in text_lower)
    keyword_count = sum(1 for keyword in professional_keywords if keyword in text_lower)
    
    score = 0
    
    # Action verbs (10 points)
    if action_verb_count >= 8:
        score += 10
    elif action_verb_count >= 5:
        score += 7
    elif action_verb_count >= 3:
        score += 4
    else:
        suggestions.append("Use more action verbs (achieved, developed, managed, etc.)")
    
    # Professional keywords (10 points)
    if keyword_count >= 8:
        score += 10
    elif keyword_count >= 5:
        score += 7
    elif keyword_count >= 3:
        score += 4
    else:
        suggestions.append("Include more professional keywords relevant to your field")
    
    return score


def calculate_formatting_score(text, suggestions):
    """Score based on formatting quality indicators"""
    score = 15  # Start with full score and deduct
    
    # Check for bullet points or list indicators
    bullet_indicators = ['•', '-', '*', '→', '▪']
    has_bullets = any(indicator in text for indicator in bullet_indicators)
    
    if not has_bullets:
        score -= 5
        suggestions.append("Use bullet points to improve readability")
    
    # Check for dates (experience/education timeline)
    date_patterns = [
        r'\d{4}',  # Year (2020)
        r'\d{1,2}/\d{4}',  # Month/Year (01/2020)
        r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4}'  # Month Year
    ]
    
    has_dates = any(re.search(pattern, text) for pattern in date_patterns)
    
    if not has_dates:
        score -= 5
        suggestions.append("Include dates for experience and education")
    
    # Check for excessive whitespace or poor structure
    lines = text.split('\n')
    empty_line_ratio = sum(1 for line in lines if line.strip() == '') / max(len(lines), 1)
    
    if empty_line_ratio > 0.5:
        score -= 5
        suggestions.append("Reduce excessive whitespace for better formatting")
    
    return max(score, 0)


def calculate_jd_match(text, job_description, suggestions):
    """Score based on matching with job description"""
    if not job_description or len(job_description.strip()) < 50:
        return 0  # No JD provided or too short
    
    text_lower = text.lower()
    jd_lower = job_description.lower()
    
    # Extract important words from JD (excluding common words)
    common_words = {'the', 'and', 'or', 'in', 'at', 'to', 'for', 'of', 'with', 'a', 'an', 'is', 'are', 'be', 'will'}
    jd_words = [word for word in re.findall(r'\b\w+\b', jd_lower) if word not in common_words and len(word) > 3]
    
    # Count matches
    if not jd_words:
        return 0
    
    match_count = sum(1 for word in jd_words if word in text_lower)
    match_percentage = (match_count / len(jd_words)) * 100
    
    score = 0
    if match_percentage >= 40:
        score = 15
    elif match_percentage >= 30:
        score = 12
    elif match_percentage >= 20:
        score = 9
    elif match_percentage >= 10:
        score = 6
    else:
        suggestions.append("Resume has low keyword match with job description. Tailor it more closely.")
    
    return score