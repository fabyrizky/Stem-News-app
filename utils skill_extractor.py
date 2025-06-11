ddef extract_skills(user_skills, industry_skill_df):
    """
    Menyesuaikan skill pengguna dengan daftar skill industri.
    Mengembalikan skill yang cocok dan relevan.
    """
    industry_skills_set = set(industry_skill_df['skill'].str.lower())
    matched_skills = [skill for skill in user_skills if skill in industry_skills_set]
    return matched_skills