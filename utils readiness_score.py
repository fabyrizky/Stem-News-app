def calculate_score(user_skills, industry_skill_df):
    """
    Menghitung skor kesiapan user berdasarkan jumlah skill yang cocok.
    Skor dalam skala 0–100.
    """
    total_industry_skills = len(industry_skill_df['skill'].unique())
    matched_skills = set(user_skills) & set(industry_skill_df['skill'].str.lower())
    score = int((len(matched_skills) / total_industry_skills) * 100)
    return min(score, 100)