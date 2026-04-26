import google.generativeai as genai

# Configure API key
genai.configure(api_key="YOUR_GEMINI_API_KEY")
model = genai.GenerativeModel("gemini-pro")

def engage(candidate, job_desc):
    prompt = f"""
    Based on the following candidate profile and job description, rate the candidate's interest level as "high", "medium", or "low".

    Candidate: {candidate['name']} with skills {', '.join(candidate['skills'])}.
    Job Description: {job_desc}
    """
    try:
        response = model.generate_content(prompt)
        level = response.text.strip().lower()
        if "high" in level:
            return "Very interested!"
        elif "medium" in level:
            return "Somewhat interested."
        else:
            return "Not very interested."
    except Exception as e:
        print("Error in engagement:", e)
        return "Unable to determine interest."
