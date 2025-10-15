from fastapi import FastAPI, UploadFile, File, Form
import pdfplumber
from sentence_transformers import SentenceTransformer, util
import spacy
import os

app = FastAPI(title="Smart Resume Screener")

# Load models once at startup
nlp = spacy.load("en_core_web_sm")
model = SentenceTransformer("all-MiniLM-L6-v2")

# Utility functions
def extract_text(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text() or ""
            text += page_text + "\n"
    return text

def extract_skills(text):
    skills_list = []
    skills_file = os.path.join(os.path.dirname(__file__), "../skills_ontology/base_skills.txt")
    with open(skills_file, "r", encoding="utf-8") as f:
        for line in f:
            skill = line.strip()
            if skill and skill.lower() in text.lower():
                skills_list.append(skill)
    return list(set(skills_list))

@app.post("/screen")
async def screen(resume: UploadFile = File(...), jd: str = Form(...)):
    # Save uploaded resume temporarily
    file_path = f"temp_{resume.filename}"
    with open(file_path, "wb") as f:
        f.write(await resume.read())

    # Extract text and skills
    text = extract_text(file_path)
    skills_found = extract_skills(text)

    # Compute semantic similarity between resume & JD
    emb_resume = model.encode([text], normalize_embeddings=True)
    emb_jd = model.encode([jd], normalize_embeddings=True)
    similarity = float(util.cos_sim(emb_resume, emb_jd)[0][0])

    # Convert similarity (0–1) to a 1–10 score
    score = round(1 + 9 * ((similarity + 1) / 2), 1)

    # Cleanup
    os.remove(file_path)

    return {"skills_found": skills_found, "score": score}
# FastAPI app entry point
