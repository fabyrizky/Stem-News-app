import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import requests
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter
import json

# Konfigurasi halaman
st.set_page_config(
    page_title="Future STEM News Intelligence",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS untuk styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #424242;
        text-align: center;
        margin-bottom: 3rem;
    }
    .stButton>button {
        background-color: #1E88E5;
        color: white;
        border-radius: 20px;
        padding: 0.5rem 2rem;
        font-weight: bold;
        border: none;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #1565C0;
        transform: translateY(-2px);
    }
    .info-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .personality-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Inisialisasi session state
if 'search_history' not in st.session_state:
    st.session_state.search_history = []
if 'personality_type' not in st.session_state:
    st.session_state.personality_type = None
if 'api_key' not in st.session_state:
    st.session_state.api_key = ""

# Header aplikasi
st.markdown('<h1 class="main-header">🔬 Future STEM News Intelligence</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Temukan berita STEM terkini dan dapatkan rekomendasi personal!</p>', unsafe_allow_html=True)

# Sidebar untuk konfigurasi
with st.sidebar:
    st.header("⚙️ Konfigurasi")
    
    # Input API Key
    api_key = st.text_input(
        "NewsAPI Key",
        type="password",
        value=st.session_state.api_key,
        help="Dapatkan gratis di https://newsapi.org"
    )
    if api_key:
        st.session_state.api_key = api_key
    
    st.markdown("---")
    
    # Test Kepribadian
    st.header("🧠 Test Kepribadian")
    
    if st.session_state.personality_type:
        st.success(f"Tipe: {st.session_state.personality_type}")
        if st.button("Ulangi Test"):
            st.session_state.personality_type = None
            st.rerun()
    else:
        with st.expander("Mulai Test Kepribadian"):
            st.write("Jawab pertanyaan berikut:")
            
            q1 = st.radio(
                "1. Saat weekend, saya lebih suka:",
                ["Menghabiskan waktu sendiri", "Bertemu beberapa teman dekat", "Pergi ke acara sosial"]
            )
            
            q2 = st.radio(
                "2. Dalam diskusi, saya:",
                ["Lebih suka mendengarkan", "Seimbang berbicara & mendengar", "Suka memimpin pembicaraan"]
            )
            
            q3 = st.radio(
                "3. Energi saya terisi saat:",
                ["Sendiri dengan hobi", "Bersama 1-2 orang terdekat", "Di tengah keramaian"]
            )
            
            if st.button("Lihat Hasil"):
                scores = {"introvert": 0, "ambivert": 0, "ekstrovert": 0}
                
                # Scoring
                answers = [q1, q2, q3]
                for answer in answers:
                    if "sendiri" in answer.lower() or "mendengarkan" in answer.lower():
                        scores["introvert"] += 1
                    elif "beberapa" in answer.lower() or "seimbang" in answer.lower() or "1-2" in answer:
                        scores["ambivert"] += 1
                    else:
                        scores["ekstrovert"] += 1
                
                # Determine type
                max_score = max(scores.values())
                for ptype, score in scores.items():
                    if score == max_score:
                        st.session_state.personality_type = ptype.capitalize()
                        break
                
                st.rerun()
    
    st.markdown("---")
    
    # Riwayat Pencarian
    st.header("📚 Riwayat Pencarian")
    if st.session_state.search_history:
        for i, query in enumerate(reversed(st.session_state.search_history[-5:])):
            st.text(f"{i+1}. {query}")
    else:
        st.info("Belum ada riwayat")

# Main content area
if not st.session_state.api_key:
    st.warning("⚠️ Masukkan NewsAPI Key di sidebar untuk mulai!")
    st.info("""
    ### Cara mendapatkan API Key GRATIS:
    1. Kunjungi https://newsapi.org/register
    2. Daftar dengan email
    3. Copy API Key dari dashboard
    4. Paste di sidebar
    """)
else:
    # Search section
    col1, col2, col3 = st.columns([3, 1, 1])
    
    with col1:
        search_query = st.text_input(
            "🔍 Cari berita STEM:",
            placeholder="Contoh: artificial intelligence, quantum computing, biotechnology..."
        )
    
    with col2:
        search_button = st.button("Cari", type="primary", use_container_width=True)
    
    with col3:
        clear_button = st.button("Clear", use_container_width=True)
    
    if clear_button:
        st.session_state.search_history = []
        st.rerun()
    
    # Function to fetch news
    def fetch_news(query, api_key):
        url = "https://newsapi.org/v2/everything"
        params = {
            'q': f'{query} AND (science OR technology OR engineering OR mathematics)',
            'apiKey': api_key,
            'language': 'en',
            'sortBy': 'relevancy',
            'pageSize': 20,
            'from': (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        }
        
        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                return response.json()
            else:
                st.error(f"Error: {response.status_code}")
                return None
        except Exception as e:
            st.error(f"Error: {str(e)}")
            return None
    
    # Process search
    if search_button and search_query:
        # Add to history
        if search_query not in st.session_state.search_history:
            st.session_state.search_history.append(search_query)
        
        # Fetch news
        with st.spinner("🔄 Mencari berita..."):
            news_data = fetch_news(search_query, st.session_state.api_key)
        
        if news_data and news_data.get('articles'):
            articles = news_data['articles']
            
            # Create tabs for different views
            tab1, tab2, tab3, tab4 = st.tabs(["📰 Berita", "📊 Visualisasi", "💡 Rekomendasi", "📈 Analisis"])
            
            with tab1:
                st.subheader(f"Ditemukan {len(articles)} artikel")
                
                # Display articles in cards
                for i, article in enumerate(articles[:10]):
                    with st.container():
                        st.markdown(f"""
                        <div class="info-card">
                            <h4>{article.get('title', 'No Title')}</h4>
                            <p><strong>Sumber:</strong> {article.get('source', {}).get('name', 'Unknown')}</p>
                            <p><strong>Tanggal:</strong> {article.get('publishedAt', '')[:10]}</p>
                            <p>{article.get('description', 'No description available.')}</p>
                            <a href="{article.get('url', '#')}" target="_blank">Baca selengkapnya →</a>
                        </div>
                        """, unsafe_allow_html=True)
            
            with tab2:
                st.subheader("📊 Visualisasi Data")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Word Cloud
                    st.markdown("### ☁️ Word Cloud")
                    
                    # Collect all text
                    all_text = " ".join([
                        article.get('title', '') + " " + article.get('description', '')
                        for article in articles
                    ])
                    
                    # Generate word cloud
                    if all_text.strip():
                        wordcloud = WordCloud(
                            width=400,
                            height=300,
                            background_color='white',
                            colormap='viridis'
                        ).generate(all_text)
                        
                        fig, ax = plt.subplots(figsize=(8, 6))
                        ax.imshow(wordcloud, interpolation='bilinear')
                        ax.axis('off')
                        st.pyplot(fig)
                
                with col2:
                    # Source distribution
                    st.markdown("### 📊 Distribusi Sumber")
                    
                    sources = [article.get('source', {}).get('name', 'Unknown') for article in articles]
                    source_counts = Counter(sources)
                    
                    fig = px.pie(
                        values=list(source_counts.values()),
                        names=list(source_counts.keys()),
                        title="Sumber Berita"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                # Timeline
                st.markdown("### 📅 Timeline Publikasi")
                
                # Extract dates
                dates = []
                for article in articles:
                    if article.get('publishedAt'):
                        date = article['publishedAt'][:10]
                        dates.append(date)
                
                if dates:
                    date_counts = Counter(dates)
                    df_timeline = pd.DataFrame(
                        list(date_counts.items()),
                        columns=['Date', 'Count']
                    ).sort_values('Date')
                    
                    fig = px.line(
                        df_timeline,
                        x='Date',
                        y='Count',
                        title='Jumlah Artikel per Hari',
                        markers=True
                    )
                    st.plotly_chart(fig, use_container_width=True)
            
            with tab3:
                st.subheader("💡 Rekomendasi Personal")
                
                if st.session_state.personality_type:
                    personality = st.session_state.personality_type
                    
                    st.markdown(f"""
                    <div class="personality-card">
                        <h3>Rekomendasi untuk {personality}</h3>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Recommendations based on personality and search
                    recommendations = {
                        "Introvert": {
                            "careers": [
                                "🔬 Research Scientist - Fokus pada penelitian mendalam",
                                "💻 Software Developer - Coding dan problem solving",
                                "📊 Data Analyst - Analisis data secara independen",
                                "🔧 Technical Writer - Dokumentasi teknis"
                            ],
                            "projects": [
                                "📱 Buat aplikasi personal untuk tracking habits",
                                "🤖 Develop chatbot dengan Natural Language Processing",
                                "📈 Analisis dataset publik tentang " + search_query,
                                "📝 Tulis blog teknis tentang temuan Anda"
                            ],
                            "tips": "Manfaatkan kekuatan Anda dalam fokus mendalam. Cari proyek yang memungkinkan eksplorasi detail."
                        },
                        "Ambivert": {
                            "careers": [
                                "👥 Tech Lead - Balance coding & team coordination",
                                "🎯 Product Manager - Bridge tech & business",
                                "🔍 UX Researcher - User interviews & data analysis",
                                "📢 Developer Advocate - Tech evangelism"
                            ],
                            "projects": [
                                "🌐 Buat platform kolaborasi untuk " + search_query,
                                "📊 Dashboard interaktif untuk visualisasi data",
                                "🎮 Game edukasi tentang konsep STEM",
                                "🤝 Organize hackathon atau study group"
                            ],
                            "tips": "Fleksibilitas Anda adalah aset. Pilih proyek yang menggabungkan kerja solo dan kolaborasi."
                        },
                        "Ekstrovert": {
                            "careers": [
                                "🎤 Tech Evangelist - Public speaking & demos",
                                "👔 Sales Engineer - Technical sales",
                                "🏫 STEM Educator - Teaching & mentoring",
                                "🚀 Startup Founder - Leadership & networking"
                            ],
                            "projects": [
                                "📹 YouTube channel tentang " + search_query,
                                "🎪 Organize STEM workshop untuk komunitas",
                                "🌍 Build open-source project dengan contributors",
                                "📱 Social learning app untuk STEM"
                            ],
                            "tips": "Energi sosial Anda dapat menginspirasi orang lain. Fokus pada proyek yang melibatkan komunitas."
                        }
                    }
                    
                    recs = recommendations.get(personality, recommendations["Ambivert"])
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("### 💼 Karier Potensial")
                        for career in recs["careers"]:
                            st.markdown(f"• {career}")
                    
                    with col2:
                        st.markdown("### 🚀 Ide Proyek")
                        for project in recs["projects"]:
                            st.markdown(f"• {project}")
                    
                    st.info(f"💡 **Tips:** {recs['tips']}")
                    
                else:
                    st.warning("🧠 Selesaikan test kepribadian di sidebar untuk rekomendasi personal!")
            
            with tab4:
                st.subheader("📈 Analisis Mendalam")
                
                # Sentiment/Topic Analysis (Simplified)
                st.markdown("### 🎯 Topik Utama")
                
                # Extract key topics
                topics = []
                keywords = ['AI', 'Machine Learning', 'Quantum', 'Biotech', 'Robotics', 
                           'Climate', 'Space', 'Medicine', 'Energy', 'Data']
                
                for keyword in keywords:
                    count = sum(1 for article in articles 
                              if keyword.lower() in (article.get('title', '') + 
                                                   article.get('description', '')).lower())
                    if count > 0:
                        topics.append({'Topic': keyword, 'Count': count})
                
                if topics:
                    df_topics = pd.DataFrame(topics).sort_values('Count', ascending=False)
                    
                    fig = px.bar(
                        df_topics,
                        x='Topic',
                        y='Count',
                        title='Distribusi Topik STEM',
                        color='Count',
                        color_continuous_scale='viridis'
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                # Summary
                st.markdown("### 📝 Ringkasan Analisis")
                
                total_articles = len(articles)
                unique_sources = len(set(sources))
                date_range = f"{min(dates) if dates else 'N/A'} hingga {max(dates) if dates else 'N/A'}"
                
                st.markdown(f"""
                <div class="info-card">
                    <h4>Statistik Pencarian: {search_query}</h4>
                    <ul>
                        <li><strong>Total artikel:</strong> {total_articles}</li>
                        <li><strong>Sumber unik:</strong> {unique_sources}</li>
                        <li><strong>Rentang tanggal:</strong> {date_range}</li>
                        <li><strong>Topik dominan:</strong> {df_topics.iloc[0]['Topic'] if not df_topics.empty else 'N/A'}</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
                
                # AI-like insights
                st.markdown("### 🤖 Wawasan AI")
                
                insights = [
                    f"Topik '{search_query}' menunjukkan aktivitas tinggi dalam {len(articles)} artikel terbaru.",
                    f"Sumber paling aktif adalah {source_counts.most_common(1)[0][0] if source_counts else 'Unknown'}.",
                    f"Tren menunjukkan peningkatan minat pada {df_topics.iloc[0]['Topic'] if not df_topics.empty else 'teknologi'} dalam konteks {search_query}.",
                    "Pertimbangkan untuk mengeksplorasi intersection antara topik ini dengan bidang lain untuk inovasi."
                ]
                
                for insight in insights:
                    st.markdown(f"• {insight}")
        
        else:
            st.error("Tidak ada hasil ditemukan. Coba kata kunci lain!")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem;'>
    <p>🚀 Future STEM News Intelligence v1.0</p>
    <p>Built with ❤️ using Streamlit | Powered by NewsAPI</p>
</div>
""", unsafe_allow_html=True)