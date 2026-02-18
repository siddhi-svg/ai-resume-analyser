# AI Resume Analyzer

An intelligent tool that analyzes your resume against a job description using NLP techniques — gives you a match score, skill gap insights, recommended job roles, and actionable career advice.

![AI Resume Analyzer Demo](https://via.placeholder.com/800x450.png?text=AI+Resume+Analyzer+Screenshot)  
*(Add your real screenshot here later)*

## ✨ Features

- 📄 PDF resume upload & text extraction
- 📝 Job description pasting & analysis
- 🔢 Match percentage (TF-IDF + Cosine Similarity)
- 🎯 Top 3 recommended job roles based on your skills
- 🕵️‍♀️ Professional skill gap detection
- 📊 Clean, modern UI with visual feedback
- 📥 Downloadable analysis report (.txt)

## 🛠️ Tech Stack

- **Frontend / App**: [Streamlit](https://streamlit.io/)
- **PDF Parsing**: PyPDF2
- **NLP & Similarity**: scikit-learn (TF-IDF + Cosine), spaCy (lemmatization)
- **Deployment**: Streamlit Community Cloud

## 🚀 Quick Start (Local Development)

### Prerequisites

- Python 3.8+
- Git

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/siddhi-svg/ai-resume-analyser.git
cd ai-resume-analyser

# 2. Create & activate virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Download spaCy English model (very important!)
python -m spacy download en_core_web_sm

# 5. Run the app
streamlit run app.py
