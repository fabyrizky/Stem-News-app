import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import requests
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter
import time

# Konfigurasi halaman
st.set_page_config(
    page_title="Future STEM News Intelligence",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS Modern Sci-Fi Theme
def load_modern_css():
    return """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Exo+2:wght@300;400;600&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 50%, #16213e 100%);
        color: #e0e6ed;
        font-family: 'Exo 2', sans-serif;
    }
    
    .main-title {
        font-family: 'Orbitron', monospace;
        font-size: 3.2rem;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(45deg, #00f5ff, #0083ff, #7c4dff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 2rem 0;
        text-shadow: 0 0 30px rgba(0, 245, 255, 0.3);
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    .sub-title {
        font-size: 1.2rem;
        text-align: center;
        color: #a0aec0;
        margin-bottom: 2rem;
        font-weight: 300;
    }
    
    .feature-box {
        background: rgba(0, 245, 255, 0.1);
        border: 1px solid rgba(0, 245, 255, 0.3);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .feature-box:hover {
        border-color: rgba(0, 245, 255, 0.6);
        background: rgba(0, 245, 255, 0.15);
        transform: translateY(-2px);
    }
    
    .news-item {
        background: rgba(255, 255, 255, 0.08);
        border-left: 3px solid #00f5ff;
        border-radius: 8px;
        padding: 1.2rem;
        margin: 0.8rem 0;
        transition: all 0.3s ease;
    }
    
    .news-item:hover {
        background: rgba(255, 255, 255, 0.12);
        border-left-color: #7c4dff;
    }
    
    .stButton > button {
        background: linear-gradient(45deg, #00f5ff, #0083ff);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
        font-family: 'Exo 2', sans-serif;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 245, 255, 0.3);
    }
    
    .stButton > button:hover {
        background: linear-gradient(45deg, #7c4dff, #00f5ff);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(124, 77, 255, 0.4);
    }
    
    .metric-card {
        background: rgba(0, 245, 255, 0.1);
        border: 1px solid rgba(0, 245, 255, 0.3);
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #00f5ff;
        font-family: 'Orbitron', monospace;
    }
    
    .sidebar-card {
        background: rgba(0, 245, 255, 0.05);
        border: 1px solid rgba(0, 245, 255, 0.2);
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    @keyframes glow {
        from { text-shadow: 0 0 20px rgba(0, 245, 255, 0.3); }
        to { text-shadow: 0 0 30px rgba(0, 245, 255, 0.6), 0 0 40px rgba(124, 77, 255, 0.3); }
    }
    
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(0, 245, 255, 0.3);
        border-radius: 10px;
        color: #e0e6ed;
    }
    </style>
    """

# Initialize session state
if 'search_history' not in st.session_state:
    st.session_state.search_history = []
if 'personality_type' not in st.session_state:
    st.session_state.personality_type = None
if 'api_key' not in st.session_state:
    st.session_state.api_key = ""
if 'bookmarks' not in st.session_state:
    st.session_state.bookmarks = []

# Load CSS
st.markdown(load_modern_css(), unsafe_allow_html=True)

# Helper Functions
def analyze_sentiment(text):
    positive_words = ['breakthrough', 'success', 'innovative', 'revolutionary', 'promising']
    negative_words = ['failure', 'concern', 'risk', 'threat', 'problem']
    
    text_lower = text.lower()
    pos_count = sum(word in text_lower for word in positive_words)
    neg_count = sum(word in text_lower for word in negative_words)
    
    if pos_count > neg_count:
        return "Positive 😊"
    elif neg_count > pos_count:
        return "Negative 😟"
    else:
        return "Neutral 😐"

def extract_key_topics(articles):
    topics = {
        'AI & ML': ['ai', 'artificial intelligence', 'machine learning', 'deep learning'],
        'Quantum': ['quantum', 'qubit', 'superposition'],
        'Biotech': ['biotech', 'gene', 'crispr', 'dna', 'vaccine'],
        'Climate': ['climate', 'renewable', 'sustainable', 'carbon'],
        'Space': ['space', 'rocket', 'satellite', 'mars', 'nasa'],
        'Robotics': ['robot', 'automation', 'autonomous'],
        'Cyber': ['cyber', 'security', 'encryption', 'privacy'],
        'Blockchain': ['blockchain', 'crypto', 'web3']
    }
    
    topic_counts = {topic: 0 for topic in topics}
    
    for article in articles:
        text = (article.get('title', '') + ' ' + article.get('description', '')).lower()
        for topic, keywords in topics.items():
            if any(keyword in text for keyword in keywords):
                topic_counts[topic] += 1
    
    return {k: v for k, v in topic_counts.items() if v > 0}

def generate_insights(articles, query):
    insights = []
    
    topics = extract_key_topics(articles)
    if topics:
        top_topic = max(topics, key=topics.get)
        insights.append(f"🎯 {top_topic} dominates with {topics[top_topic]} mentions")
    
    dates = [a.get('publishedAt', '')[:10] for a in articles if a.get('publishedAt')]
    if dates:
        recent_date = max(dates)
        insights.append(f"📅 Latest coverage: {recent_date}")
    
    sources = list(set([a.get('source', {}).get('name', 'Unknown') for a in articles]))
    insights.append(f"📰 {len(sources)} sources covering this topic")
    
    return insights

def fetch_news(query, api_key):
    url = "https://newsapi.org/v2/everything"
    params = {
        'q': f'{query} AND (science OR technology OR engineering OR mathematics)',
        'apiKey': api_key,
        'language': 'en',
        'sortBy': 'relevancy',
        'pageSize': 30,
        'from': (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Error: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

# Header
st.markdown('<div class="main-title">🔬 Future STEM News Intelligence</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">AI-Powered STEM News Analysis & Personal Insights</div>', unsafe_allow_html=True)

# Developer Info
with st.expander("ℹ️ About Developer & Project"):
    st.markdown("**👨‍💻 Developed by: M Faby Rizky K**")
    st.markdown("**Future STEM News Intelligence** is an advanced AI-powered platform for STEM news analysis.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**🎯 Vision:**")
        st.write("• Democratize STEM knowledge")
        st.write("• Intelligent news curation")
        st.write("• Data-driven insights")
        
    with col2:
        st.markdown("**🛠️ Tech Stack:**")
        st.write("• Frontend: Streamlit")
        st.write("• Data: Pandas, NumPy")
        st.write("• Viz: Matplotlib, Plotly")

# Sidebar
with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    
    api_key = st.text_input(
        "NewsAPI Key",
        type="password",
        value=st.session_state.api_key,
        help="Get free key at https://newsapi.org"
    )
    if api_key:
        st.session_state.api_key = api_key
        if len(api_key) == 32:
            st.success("✅ API Key valid")
        else:
            st.error("❌ Invalid API Key")
    
    st.markdown("---")
    
    st.markdown("### 🧠 Personality Profile")
    
    if st.session_state.personality_type:
        st.markdown(f"""
        <div class="sidebar-card">
            <strong>Your Type: {st.session_state.personality_type}</strong><br>
            Personalized recommendations active ✨
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 Retake Test"):
            st.session_state.personality_type = None
            st.rerun()
    else:
        with st.expander("🎯 Take Personality Test"):
            st.write("Discover your STEM personality!")
            
            q1 = st.radio(
                "Work environment:",
                ["🏠 Home office", "☕ Co-working space", "🏢 Busy office"],
                key="q1"
            )
            
            q2 = st.radio(
                "Learning style:",
                ["📚 Documentation first", "🎯 Mix theory & practice", "👥 Learn by teaching"],
                key="q2"
            )
            
            q3 = st.radio(
                "Innovation approach:",
                ["🔬 Deep research", "🔄 Multiple projects", "🚀 Quick prototypes"],
                key="q3"
            )
            
            if st.button("Get Results", type="primary"):
                scores = {"Introvert": 0, "Ambivert": 0, "Extrovert": 0}
                
                answers = [q1, q2, q3]
                for answer in answers:
                    if any(word in answer.lower() for word in ["home", "documentation", "deep"]):
                        scores["Introvert"] += 1
                    elif any(word in answer.lower() for word in ["mix", "multiple"]):
                        scores["Ambivert"] += 1
                    else:
                        scores["Extrovert"] += 1
                
                st.session_state.personality_type = max(scores, key=scores.get)
                st.balloons()
                st.rerun()
    
    st.markdown("---")
    
    st.markdown("### 📚 Recent Searches")
    if st.session_state.search_history:
        for i, query in enumerate(reversed(st.session_state.search_history[-5:]), 1):
            if st.button(f"{i}. {query[:15]}...", key=f"hist_{i}"):
                st.session_state.search_again = query
    else:
        st.info("No searches yet")

# Main Content
if not st.session_state.api_key:
    # Welcome Screen - using native Streamlit components
    st.markdown("## 🎉 Welcome to Future STEM News Intelligence!")
    st.markdown("Your AI-powered companion for STEM news analysis.")
    
    st.markdown("### ✨ Features:")
    col1, col2 = st.columns(2)
    with col1:
        st.write("🔍 Real-time STEM news search")
        st.write("📊 Interactive data visualizations")
        st.write("🧠 Personalized recommendations")
    with col2:
        st.write("🤖 AI-generated insights")
        st.write("📄 Export capabilities")
        st.write("🎯 Career guidance")
    
    st.markdown("### 🚀 Getting Started:")
    st.write("1. Get API key from [NewsAPI](https://newsapi.org/register)")
    st.write("2. Enter key in sidebar")
    st.write("3. Take personality test")
    st.write("4. Start searching!")
    
    # Feature Cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-box">
            <h3>🎯 Smart Analysis</h3>
            <p>AI-powered insights for STEM trends and patterns in news data.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-box">
            <h3>📈 Visual Intelligence</h3>
            <p>Interactive charts and visualizations that make data easy to understand.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-box">
            <h3>🚀 Personal Growth</h3>
            <p>Tailored career recommendations based on your personality type.</p>
        </div>
        """, unsafe_allow_html=True)

else:
    # Search Interface
    col1, col2, col3 = st.columns([3, 1, 1])
    
    with col1:
        search_value = getattr(st.session_state, 'search_again', "")
        if search_value:
            delattr(st.session_state, 'search_again')
        
        search_query = st.text_input(
            "🔍 Search STEM News:",
            placeholder="Try: quantum computing, CRISPR, neural networks...",
            value=search_value
        )
    
    with col2:
        search_button = st.button("🔍 Search", type="primary")
    
    with col3:
        clear_button = st.button("🗑️ Clear")
    
    if clear_button:
        st.session_state.search_history = []
        st.session_state.bookmarks = []
        st.rerun()
    
    # Handle Search
    if search_button and search_query:
        if search_query not in st.session_state.search_history:
            st.session_state.search_history.append(search_query)
        
        with st.spinner('🔄 Analyzing STEM news...'):
            news_data = fetch_news(search_query, st.session_state.api_key)
        
        if news_data and news_data.get('articles'):
            articles = news_data['articles']
            insights = generate_insights(articles, search_query)
            
            st.success(f"✨ Found {len(articles)} articles about '{search_query}'")
            
            # Quick Stats
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{len(articles)}</div>
                    <div>Articles</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                sources = len(set([a.get('source', {}).get('name', 'Unknown') for a in articles]))
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{sources}</div>
                    <div>Sources</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                topics = extract_key_topics(articles)
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{len(topics)}</div>
                    <div>Topics</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                recent = sum(1 for a in articles if a.get('publishedAt', '')[:10] == datetime.now().strftime('%Y-%m-%d'))
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{recent}</div>
                    <div>Today</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Tabs
            tab1, tab2, tab3, tab4 = st.tabs(["📰 News Feed", "📊 Analytics", "💡 Insights", "🎯 Personal"])
            
            with tab1:
                st.markdown("### 📰 Latest Articles")
                
                col1, col2 = st.columns([2, 2])
                with col1:
                    sort_by = st.selectbox("Sort by", ["Relevance", "Date", "Source"])
                with col2:
                    filter_source = st.selectbox(
                        "Filter source",
                        ["All"] + list(set([a.get('source', {}).get('name', 'Unknown') for a in articles]))
                    )
                
                filtered_articles = articles
                if filter_source != "All":
                    filtered_articles = [a for a in articles if a.get('source', {}).get('name') == filter_source]
                
                if sort_by == "Date":
                    filtered_articles.sort(key=lambda x: x.get('publishedAt', ''), reverse=True)
                
                for i, article in enumerate(filtered_articles[:15]):
                    with st.container():
                        st.markdown(f"**{article.get('title', 'No Title')}**")
                        st.caption(f"Source: {article.get('source', {}).get('name', 'Unknown')} | Date: {article.get('publishedAt', '')[:10]} | Sentiment: {analyze_sentiment(article.get('title', '') + article.get('description', ''))}")
                        st.write(f"{article.get('description', 'No description available.')[:150]}...")
                        
                        col_a, col_b = st.columns([1, 4])
                        with col_a:
                            if st.button("📌", key=f"bookmark_{i}", help="Bookmark"):
                                if article not in st.session_state.bookmarks:
                                    st.session_state.bookmarks.append(article)
                                    st.success("Bookmarked!")
                        with col_b:
                            st.markdown(f"[Read more →]({article.get('url', '#')})")
                        
                        st.divider()
            
            with tab2:
                st.markdown("### 📊 Analytics Dashboard")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### ☁️ Topic Cloud")
                    all_text = " ".join([
                        article.get('title', '') + " " + article.get('description', '')
                        for article in articles
                    ])
                    
                    if all_text.strip():
                        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
                        words = all_text.lower().split()
                        filtered_words = [word for word in words if word not in stop_words and len(word) > 3]
                        filtered_text = " ".join(filtered_words)
                        
                        wordcloud = WordCloud(
                            width=500,
                            height=300,
                            background_color='black',
                            colormap='plasma',
                            max_words=40
                        ).generate(filtered_text)
                        
                        fig, ax = plt.subplots(figsize=(8, 5))
                        ax.imshow(wordcloud, interpolation='bilinear')
                        ax.axis('off')
                        st.pyplot(fig)
                
                with col2:
                    st.markdown("#### 🎯 Topic Distribution")
                    if topics:
                        df_topics = pd.DataFrame(list(topics.items()), columns=['Topic', 'Count'])
                        fig = px.pie(
                            df_topics,
                            values='Count',
                            names='Topic',
                            title="STEM Topics",
                            color_discrete_sequence=px.colors.qualitative.Neon
                        )
                        fig.update_layout(
                            paper_bgcolor='rgba(0,0,0,0)',
                            plot_bgcolor='rgba(0,0,0,0)',
                            font_color='white'
                        )
                        st.plotly_chart(fig, use_container_width=True)
                
                st.markdown("#### 📅 Publication Timeline")
                dates = [a.get('publishedAt', '')[:10] for a in articles if a.get('publishedAt')]
                
                if dates:
                    date_counts = Counter(dates)
                    df_timeline = pd.DataFrame(
                        list(date_counts.items()),
                        columns=['Date', 'Articles']
                    ).sort_values('Date')
                    
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=df_timeline['Date'],
                        y=df_timeline['Articles'],
                        mode='lines+markers',
                        name='Articles',
                        line=dict(color='#00f5ff', width=3),
                        marker=dict(size=8, color='#7c4dff')
                    ))
                    fig.update_layout(
                        title="Articles Over Time",
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        font_color='white'
                    )
                    st.plotly_chart(fig, use_container_width=True)
            
            with tab3:
                st.markdown("### 🤖 AI Insights")
                
                st.markdown("#### 🔮 Key Findings")
                for insight in insights:
                    st.info(insight)
                
                if topics:
                    st.markdown("#### 📈 Trend Analysis")
                    df_trends = pd.DataFrame(list(topics.items()), columns=['Topic', 'Mentions'])
                    df_trends['Status'] = df_trends['Mentions'].apply(
                        lambda x: '🔥 Hot' if x > 5 else '📈 Rising' if x > 2 else '🌱 Emerging'
                    )
                    
                    fig = px.bar(
                        df_trends,
                        x='Topic',
                        y='Mentions',
                        color='Status',
                        title="STEM Trends",
                        color_discrete_map={
                            '🔥 Hot': '#ff4757',
                            '📈 Rising': '#00f5ff',
                            '🌱 Emerging': '#7c4dff'
                        }
                    )
                    fig.update_layout(
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        font_color='white'
                    )
                    st.plotly_chart(fig, use_container_width=True)
            
            with tab4:
                st.markdown("### 🎯 Personalized Recommendations")
                
                if st.session_state.personality_type:
                    personality = st.session_state.personality_type
                    
                    recommendations = {
                        "Introvert": {
                            "careers": ["Research Scientist", "Data Scientist", "Technical Writer"],
                            "projects": ["Personal AI assistant", "Research analysis", "Open-source contribution"],
                            "tips": "Focus on deep, analytical work. Perfect for research and development."
                        },
                        "Ambivert": {
                            "careers": ["Product Manager", "Tech Lead", "UX Researcher"],
                            "projects": ["Collaborative platform", "Interactive dashboard", "Study group"],
                            "tips": "Balance solo work with collaboration. Bridge technical and business needs."
                        },
                        "Extrovert": {
                            "careers": ["Tech Evangelist", "Sales Engineer", "STEM Educator"],
                            "projects": ["YouTube channel", "Workshop organization", "Community platform"],
                            "tips": "Use social energy to inspire others. Perfect for leadership roles."
                        }
                    }
                    
                    recs = recommendations.get(personality, recommendations["Ambivert"])
                    
                    st.markdown(f"#### 💼 Career Paths for {personality}s")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("**🎯 Recommended Careers:**")
                        for career in recs["careers"]:
                            st.write(f"• {career}")
                    
                    with col2:
                        st.markdown("**🚀 Project Ideas:**")
                        for project in recs["projects"]:
                            st.write(f"• {project}")
                    
                    st.info(f"💡 **Tips:** {recs['tips']}")
                
                else:
                    st.warning("🧠 Complete the personality test for personalized recommendations!")
        
        else:
            st.error("No results found. Try different keywords or check your API key.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    <p>🚀 Future STEM News Intelligence v2.0 | Built with ❤️ by M Faby Rizky K</p>
    <p>Powered by NewsAPI | Made with Streamlit</p>
</div>
""", unsafe_allow_html=True)
