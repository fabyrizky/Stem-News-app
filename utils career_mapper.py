def map_career_path(user_skills, industry_skill_df):
    """
    Mencocokkan skill pengguna dengan industri yang paling sesuai.
    Mengembalikan daftar industri yang cocok beserta persentase kecocokan.
    """
    industry_matches = {}

    for _, row in industry_skill_df.iterrows():
        industry = row['industry']
        skill = row['skill'].lower()
        if skill in user_skills:
            industry_matches.setdefault(industry, 0)
            industry_matches[industry] += 1

    total_skills = len(user_skills) if user_skills else 1
    result = [
        {"industry": k, "match_percent": round(v / total_skills * 100, 1)}
        for k, v in sorted(industry_matches.items(), key=lambda item: item[1], reverse=True)
    ]

    return result if result else "Belum ada kecocokan ditemukan."