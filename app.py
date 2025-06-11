import streamlit as st
import pandas as pd
from utils.skill_extractor import extract_skills
from utils.career_mapper import map_career_path
from utils.readiness_score import calculate_score
from utils.course_recommender import recommend_courses

# Load data
industry_skills = pd.read_csv("data/industry_skills.csv")
course_catalog = pd.read_csv("data/course_catalog.csv")

st.set_page_config(page_title="Career Shift Analyzer", page_icon="🚀")

st.title("🚀 Career Shift to Future Industry")
st.markdown("Analisis dan simulasi transisi karier Anda ke industri masa depan!")

# Input user
user_skills = st.text_area("Masukkan skill Anda (pisahkan dengan koma):")

if st.button("🔍 Analisis"):
    if user_skills:
        skill_list = [s.strip().lower() for s in user_skills.split(",")]
        extracted = extract_skills(skill_list, industry_skills)
        mapping = map_career_path(skill_list, industry_skills)
        score = calculate_score(skill_list, industry_skills)

        st.subheader("🧠 Skill yang dikenali:")
        st.write(extracted)

        st.subheader("🔀 Rekomendasi Karier:")
        st.write(mapping)

        st.subheader("📊 Skor Kesiapan Industri Masa Depan:")
        st.metric("Readiness Score", f"{score}/100")

            
        if isinstance(mapping, list) and mapping:
            best_industry = mapping[0]['industry']
            skill_gap, course_recos = recommend_courses(
                skill_list, best_industry, industry_skills, course_catalog
            )

            st.subheader("📚 Rekomendasi Kursus untuk Mengisi Skill Gap:")
            if course_recos:
                for course in course_recos:
                    st.markdown(f"- **{course['course_title']}** ({course['provider']}) – Skill: *{course['skill']}*")
            else:
                st.write("✅ Tidak ada gap skill besar – Anda sudah siap!")
        else:
            st.info("Tidak ada industri dominan terdeteksi.")

    else:
        st.warning("Silakan masukkan skill terlebih dahulu.")
