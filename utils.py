import PyPDF2
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load spaCy model once (outside functions)
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Error: spaCy model 'en_core_web_sm' not found.")
    print("Please run: python -m spacy download en_core_web_sm")
    nlp = None  # will be checked later

def extract_text_from_pdf(file):
    """
    Extract text from PDF file object (Streamlit uploaded file).
    """
    if file is None:
        return ""

    try:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            page_text = page.extract_text() or ""  # handle None
            text += page_text + "\n"
        return text.strip()
    except Exception as e:
        print(f"PDF extraction failed: {e}")
        return ""

def preprocess_text(text):
    """
    Clean and lemmatize text. Keep it reasonably readable.
    """
    if not text or nlp is None:
        # fallback if spaCy not available
        return text.lower().strip()

    doc = nlp(text.lower())
    tokens = [
        token.lemma_
        for token in doc
        if not token.is_stop and not token.is_punct and token.lemma_.strip() != ""
    ]
    return " ".join(tokens)

def calculate_similarity(resume_text, job_text):
    """
    Calculate cosine similarity between two texts using TF-IDF.
    Returns value between 0–100.
    """
    if not resume_text.strip() or not job_text.strip():
        return 0.0

    vectorizer = TfidfVectorizer(
        stop_words='english',
        max_features=5000,          # prevent memory explosion on long docs
        ngram_range=(1, 2)         # capture some phrases
    )

    # Fit on both documents together → correct way
    vectors = vectorizer.fit_transform([resume_text, job_text])

    # cosine_similarity returns [[1.0, sim], [sim, 1.0]]
    similarity_matrix = cosine_similarity(vectors[0:1], vectors[1:2])

    similarity = similarity_matrix[0][0]  # scalar value 0.0–1.0
    return round(similarity * 100, 2)     # return as percentage