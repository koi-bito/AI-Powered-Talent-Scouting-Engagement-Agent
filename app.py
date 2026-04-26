from flask import Flask, render_template, request, jsonify
import os
import pandas as pd
from matcher import match_with_jd_gemini
from chatbot import engage

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/rank', methods=['POST'])
def rank():
    jd = request.form['jd']
    file = request.files.get('candidates_file')

    if file and file.filename != '':
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        df = pd.read_csv(filepath)
    else:
        df = pd.read_csv('data/sample_candidates.csv')

    candidates = []
    for _, row in df.iterrows():
        candidates.append({
            "name": row["name"],
            "skills": row["skills"].split(", "),
            "experience_years": row["experience_years"],
            "interest_level": row["interest_level"]
        })

    # Use Gemini-based matching
    match_scores = match_with_jd_gemini(jd, candidates)

    ranked = []
    for i, cand in enumerate(candidates):
        # Use Gemini-based engagement
        interest_text = engage(cand, jd)
        interest_map = {"high": 90, "medium": 60, "low": 30}
        interest_score = interest_map.get(cand["interest_level"], 60)
        final_score = 0.7 * match_scores[i] * 100 + 0.3 * interest_score
        ranked.append({
            "name": cand["name"],
            "match_score": round(match_scores[i] * 100, 2),
            "interest_score": interest_score,
            "final_score": round(final_score, 2),
            "engagement": interest_text
        })

    ranked.sort(key=lambda x: x["final_score"], reverse=True)
    return jsonify(ranked)

if __name__ == '__main__':
    app.run(debug=True)
