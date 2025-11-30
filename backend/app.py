from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
from utils.text_extractor import extract_text
from utils.section_detector import detect_sections
from utils.resume_scorer import score_resume

app = Flask(__name__)
CORS(app)  # Allow React frontend to communicate

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    """Health check endpoint"""
    return jsonify({
        "message": "AI Resume Analyzer API is running!",
        "version": "1.0",
        "endpoints": ["/analyze"]
    })


@app.route('/analyze', methods=['POST'])
def analyze_resume():
    """Main endpoint to analyze resume"""
    try:
        # Check if file is present
        if 'resume' not in request.files:
            return jsonify({"error": "No resume file provided"}), 400
        
        file = request.files['resume']
        
        # Check if file has a name
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        # Check if file type is allowed
        if not allowed_file(file.filename):
            return jsonify({"error": "Invalid file type. Only PDF, DOCX, TXT allowed"}), 400
        
        # Get job description from form data (optional)
        job_description = request.form.get('job_description', '')
        
        # Save file securely
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Step 1: Extract text from resume
        resume_text = extract_text(filepath)
        
        if not resume_text:
            os.remove(filepath)  # Clean up
            return jsonify({"error": "Could not extract text from resume"}), 400
        
        # Step 2: Detect sections
        sections = detect_sections(resume_text)
        
        # Step 3: Score resume
        score_data = score_resume(resume_text, sections, job_description)
        
        # Clean up uploaded file
        os.remove(filepath)
        
        # Return analysis results
        return jsonify({
            "success": True,
            "filename": filename,
            "resume_text": resume_text[:500] + "..." if len(resume_text) > 500 else resume_text,  # First 500 chars
            "sections": sections,
            "score": score_data,
            "word_count": len(resume_text.split()),
            "character_count": len(resume_text)
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500


if __name__ == '__main__':
    print("🚀 Starting AI Resume Analyzer Backend...")
    print("📍 Server running at: http://localhost:5000")
    print("📋 Endpoints: / and /analyze")
    app.run(debug=True, port=5000)