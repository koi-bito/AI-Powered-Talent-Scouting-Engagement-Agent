import google.generativeai as genai
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Configure API key (replace with yours)
genai.configure(api_key="YOUR_GEMINI_API_KEY")

def get_embedding(text):
    result = genai.embed_content(
        model="models/embedding-001",
        content=text,
        task_type="retrieval_document"
    )
    return result['embedding']

def match_with_jd_gemini(job_desc, candidates):
    try:
        job_emb = get_embedding(job_desc)
        cand_embs = [get_embedding(' '.join(c['skills'])) for c in candidates]
        scores = [cosine_similarity([job_emb], [emb])[0][0] for emb in cand_embs]
        return np.array(scores)
    except Exception as e:
        print("Error in matching:", e)
        return np.zeros(len(candidates))
