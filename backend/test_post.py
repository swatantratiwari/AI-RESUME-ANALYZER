import requests
import json

# API endpoint
url = "http://localhost:5000/analyze"

# Path to test resume
resume_file_path = "test_resume.txt"

# Optional: Job description for matching
job_description = """
We are looking for a Senior Software Engineer with experience in:
- Python and JavaScript development
- React and Flask frameworks
- RESTful API design
- Cloud technologies (AWS preferred)
- Team leadership and mentoring
- Agile development methodologies
"""

try:
    # Open and send the resume file
    with open(resume_file_path, 'rb') as resume_file:
        files = {'resume': resume_file}
        data = {'job_description': job_description}
        
        print("🚀 Sending request to API...")
        print(f"📄 File: {resume_file_path}")
        print(f"🎯 Endpoint: {url}\n")
        
        # Make POST request
        response = requests.post(url, files=files, data=data)
        
        # Check response
        if response.status_code == 200:
            print("✅ SUCCESS! API Response:\n")
            result = response.json()
            print(json.dumps(result, indent=2))
            
            # Display key metrics
            print("\n" + "="*60)
            print("📊 KEY METRICS:")
            print("="*60)
            print(f"Overall Score: {result['score']['overall_score']}/100")
            print(f"Section Score: {result['score']['section_score']}/30")
            print(f"Length Score: {result['score']['length_score']}/20")
            print(f"Keyword Score: {result['score']['keyword_score']}/20")
            print(f"Formatting Score: {result['score']['formatting_score']}/15")
            print(f"JD Match Score: {result['score']['jd_match_score']}/15")
            print(f"\nWord Count: {result['word_count']}")
            print(f"Character Count: {result['character_count']}")
            
            print("\n📋 Detected Sections:")
            for section, found in result['sections'].items():
                status = "✅" if found else "❌"
                print(f"{status} {section.replace('_', ' ').title()}")
            
            if result['score']['suggestions']:
                print("\n💡 Suggestions for Improvement:")
                for i, suggestion in enumerate(result['score']['suggestions'], 1):
                    print(f"{i}. {suggestion}")
            
        else:
            print(f"❌ ERROR {response.status_code}:")
            print(response.json())
            
except FileNotFoundError:
    print(f"❌ Error: Could not find file '{resume_file_path}'")
    print("Make sure test_resume.txt exists in the backend folder")
except requests.exceptions.ConnectionError:
    print("❌ Error: Could not connect to the API")
    print("Make sure Flask server is running on http://localhost:5000")
except Exception as e:
    print(f"❌ Unexpected error: {str(e)}")