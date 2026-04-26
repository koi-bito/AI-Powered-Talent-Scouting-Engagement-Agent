from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def match_with_jd(job_desc, candidates):
    skills_list = [' '.join(c['skills']) for c in candidates]
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([job_desc] + skills_list)
    similarities = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1:])
    return similarities.flatten()
