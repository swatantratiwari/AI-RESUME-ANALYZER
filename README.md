ai-resume-analyzer/README.md
# 🧠 AI Resume Analyzer  
### Full-Stack Resume Scoring, JD Matching & AI-Powered Improvement Suggestions  
Built using **Python (Flask) + React + Tailwind + Machine Learning**

---

## 🚀 Overview  
AI Resume Analyzer is a full-stack application that analyzes resumes and generates detailed insights.  
It extracts text from **PDF, DOCX, or TXT** files, detects structure, computes resume quality scores, matches content with a Job Description, and also provides **AI-generated bullet point improvements**.

This project is ideal for **students, job seekers, and developers** who want to evaluate resumes or build a portfolio-worthy AI project.

---

## ✨ Features  

### 🧩 Resume Parsing  
- Extracts text from **PDF / DOCX / TXT**  
- Uses `pdfminer.six`, `python-docx`, and pure text processing  

### 📚 Section Detection  
Automatically detects:  
- Education  
- Experience  
- Skills  
- Projects  
- Achievements  
- Certifications  

### 🎯 Scoring Engine  
Generates a detailed score based on:  
- Resume structure  
- Keyword coverage  
- Job Description match  
- Readability & grammar signals  
- Section quality  

### 💬 AI Suggestions  
- Improvement suggestions  
- Better bullet points  
- JD-optimized keywords  

### 💻 Modern React Frontend  
- File Upload UI (Drag & Drop or Button)  
- JD text area  
- Clean Tailwind-based dashboard  
- Score visualizations  

### 🔥 Flask API Backend  
API endpoint:  
POST /api/analyze

Response includes:  
```json
{
  "overall_score_pct": 78.5,
  "scores": {
    "structure_pct": 80.0,
    "jd_match_pct": 70.0
  },
  "sections_found": [...],
  "generated_bullets": [...],
  "suggestions": [...]
}ai-resume-analyzer/
│
├── backend/
│   ├── app.py
│   ├── analyzer/
│   │   ├── text_extractor.py
│   │   ├── section_detector.py
│   │   └── resume_scorer.py
│   ├── uploads/
│   ├── test_post.py
│   └── test_resume.txt
│
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
│
└── README.md

🛠️ Installation & Setup
🔹 1. Clone Repo
git clone https://github.com/<your-username>/AI-RESUME-ANALYZER.git
cd AI-RESUME-ANALYZER

🐍 Backend Setup (Flask)
🔹 2. Create virtual environment
python -m venv venv

🔹 3. Activate venv

Windows

venv\Scripts\activate


Mac/Linux

source venv/bin/activate

🔹 4. Install backend dependencies
pip install flask flask-cors pdfminer.six python-docx nltk scikit-learn

🔹 5. Run backend server
cd backend
python app.py


Backend runs at:

http://127.0.0.1:5000

⚛️ Frontend Setup (React + Vite)
🔹 6. Install frontend dependencies
cd frontend
npm install

🔹 7. Start frontend
npm run dev


Frontend runs at:

http://localhost:5173

🔗 Connecting Frontend to Backend

Make sure the frontend sends requests to:

http://127.0.0.1:5000/api/analyze


Usually done using axios or fetch.

🧪 Testing API with cURL
curl -i -X POST \
  -F "resume=@test_resume.txt" \
  -F "job_description=python developer backend" \
  http://127.0.0.1:5000/api/analyze

☁️ Deployment
🔹 Backend: Render

Create Web Service

Python 3.10+

Start Command:

gunicorn app:app

🔹 Frontend: Vercel

Import frontend folder

Build Command:

npm run build


Output Directory:

dist

📌 To Add in Your Resume
• Built an AI-driven Resume Analyzer using Python (Flask) and React that extracts text from resumes, detects sections, evaluates resume structure, provides JD match scoring, and generates actionable improvement suggestions using AI.

⭐ Future Improvements

OCR support for scanned PDFs

Multi-language resume support

AI-based grammar correction

Export report as PDF

Resume builder module

🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first.

📜 License

MIT License.

💛 Support

If you like this project, consider giving it a ⭐ on GitHub!


---

# 🚀 Want badges for your GitHub repo?

I can generate these:

✔ Flask  
✔ React  
✔ Tailwind  
✔ Python  
✔ Vite  
✔ MIT License  
✔ Pull Requests welcome  

Just say:

👉 **“Add GitHub badges”**
