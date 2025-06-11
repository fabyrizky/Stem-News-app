def recommend_courses(user_skills, target_industry, industry_skill_df, course_catalog_df):
    """
    Rekomendasi kursus berdasarkan skill gap pengguna untuk industri tertentu.
    """
    # Ambil skill yang dibutuhkan untuk industri yang dipilih
    required_skills = industry_skill_df[industry_skill_df['industry'].str.lower() == target_industry.lower()]
    required_skills_set = set(required_skills['skill'].str.lower())

    # Hitung gap skill
    user_skills_set = set([s.lower() for s in user_skills])
    skill_gap = required_skills_set - user_skills_set

    if not skill_gap:
        return [], []  # Tidak ada gap

    # Cari kursus yang mengajarkan skill-skill tersebut
    recommended_courses = course_catalog_df[course_catalog_df['skill'].str.lower().isin(skill_gap)]

    # Buat list readable
    course_list = recommended_courses[['course_title', 'provider', 'skill']].to_dict(orient='records')
    return list(skill_gap), course_list