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
import hashlib
import re
from typing import List, Dict
import base64
from io import BytesIO
import time

# Konfigurasi halaman dengan tema modern
st.set_page_config(
    page_title="Future STEM News Intelligence",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/yourusername/future-stem-news',
        'Report a bug': 'https://github.com/yourusername/future-stem-news/issues',
        'About': 'Future STEM News Intelligence - AI-Powered STEM News Analysis'
    }
)

# Enhanced CSS dengan Dark Mode Support
def load_css(dark_mode=False):
    if dark_mode:
        return """
        <style>
            /* Dark Mode Theme */
            .stApp {
                background-color: #1a1a1a;
                color: #ffffff;
            }
            .main-header {
                font-size: 3.5rem;
                background: linear-gradient(45deg, #667eea, #764ba2);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                text-align: center;
                margin-bottom: 1rem;
                font-weight: 800;
                animation: fadeIn 1s ease-in;
            }
            .sub-header {
                font-size: 1.5rem;
                color: #a0a0a0;
                text-align: center;
                margin-bottom: 3rem;
                animation: fadeIn 1.5s ease-in;
            }
            .feature-card {
                background: linear-gradient(135deg, #1e1e1e 0%, #2d2d2d 100%);
                border: 1px solid #333;
                padding: 2rem;
                border-radius: 20px;
                margin: 1rem 0;
                box-shadow: 0 8px 32px rgba(0,0,0,0.3);
                transition: all 0.3s ease;
            }
            .feature-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 12px 40px rgba(0,0,0,0.4);
            }
            .stButton>button {
                background: linear-gradient(45deg, #667eea, #764ba2);
                color: white;
                border: none;
                padding: 0.75rem 2rem;
                font-weight: 600;
                border-radius: 30px;
                transition: all 0.3s ease;
                box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
            }
            .stButton>button:hover {
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
            }
            .personality-result {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 2rem;
                border-radius: 20px;
                margin: 2rem 0;
                box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
                animation: slideIn 0.5s ease-out;
            }
            .news-card {
                background: #2d2d2d;
                border: 1px solid #333;
                padding: 1.5rem;
                border-radius: 15px;
                margin: 1rem 0;
                transition: all 0.3s ease;
                border-left: 4px solid #667eea;
            }
            .news-card:hover {
                background: #333;
                transform: translateX(5px);
            }
            .metric-card {
                background: linear-gradient(135deg, #1e1e1e, #2d2d2d);
                border: 1px solid #333;
                padding: 1.5rem;
                border-radius: 15px;
                text-align: center;
                box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            }
            .metric-number {
                font-size: 2.5rem;
                font-weight: 700;
                color: #667eea;
            }
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(20px); }
                to { opacity: 1; transform: translateY(0); }
            }
            @keyframes slideIn {
                from { opacity: 0; transform: translateX(-20px); }
                to { opacity: 1; transform: translateX(0); }
            }
            /* Custom Scrollbar */
            ::-webkit-scrollbar {
                width: 10px;
                height: 10px;
            }
            ::-webkit-scrollbar-track {
                background: #1e1e1e;
            }
            ::-webkit-scrollbar-thumb {
                background: #667eea;
                border-radius: 5px;
            }
            ::-webkit-scrollbar-thumb:hover {
                background: #764ba2;
            }
        </style>
        """
    else:
        return """
        <style>
            /* Light Mode Theme */
            .main-header {
                font-size: 3.5rem;
                background: linear-gradient(45deg, #1E88E5, #1565C0);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                text-align: center;
                margin-bottom: 1rem;
                font-weight: 800;
                animation: fadeIn 1s ease-in;
            }
            .sub-header {
                font-size: 1.5rem;
                color: #5e5e5e;
                text-align: center;
                margin-bottom: 3rem;
                animation: fadeIn 1.5s ease-in;
            }
            .feature-card {
                background: white;
                padding: 2rem;
                border-radius: 20px;
                margin: 1rem 0;
                box-shadow: 0 8px 32px rgba(0,0,0,0.1);
                border: 1px solid #e0e0e0;
                transition: all 0.3s ease;
            }
            .feature-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 12px 40px rgba(0,0,0,0.15);
            }
            .stButton>button {
                background: linear-gradient(45deg, #1E88E5, #1565C0);
                color: white;
                border: none;
                padding: 0.75rem 2rem;
                font-weight: 600;
                border-radius: 30px;
                transition: all 0.3s ease;
                box-shadow: 0 4px 15px rgba(30, 136, 229, 0.3);
            }
            .stButton>button:hover {
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(30, 136, 229, 0.4);
            }
            .personality-result {
                background: linear-gradient(135deg, #1E88E5 0%, #1565C0 100%);
                color: white;
                padding: 2rem;
                border-radius: 20px;
                margin: 2rem 0;
                box-shadow: 0 8px 32px rgba(30, 136, 229, 0.3);
                animation: slideIn 0.5s ease-out;
            }
            .news-card {
                background: #f8f9fa;
                padding: 1.5rem;
                border-radius: 15px;
                margin: 1rem 0;
                transition: all 0.3s ease;
                border-left: 4px solid #1E88E5;
                box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            }
            .news-card:hover {
                background: #ffffff;
                transform: translateX(5px);
                box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            }
            .metric-card {
                background: white;
                padding: 1.5rem;
                border-radius: 15px;
                text-align: center;
                box-shadow: 0 4px 15px rgba(0,0,0,0.08);
                border: 1px solid #e0e0e0;
            }
            .metric-number {
                font-size: 2.5rem;
                font-weight: 700;
                color: #1E88E5;
            }
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(20px); }
                to { opacity: 1; transform: translateY(0); }
            }
            @keyframes slideIn {
                from { opacity: 0; transform: translateX(-20px); }
                to { opacity: 1; transform: translateX(0); }
            }
        </style>
        """

# Initialize session state dengan fitur baru
if 'search_history' not in st.session_state:
    st.session_state.search_history = []
if 'personality_type' not in st.session_state:
    st.session_state.personality_type = None
if 'api_key' not in st.session_state:
    st.session_state.api_key = ""
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False
if 'bookmarks' not in st.session_state:
    st.session_state.bookmarks = []
if 'user_preferences' not in st.session_state:
    st.session_state.user_preferences = {
        'language': 'en',
        'notifications': False,
        'auto_refresh': False
    }
if 'search_results_cache' not in st.session_state:
    st.session_state.search_results_cache = {}

# Helper Functions
def get_cache_key(query: str) -> str:
    """Generate cache key for search query"""
    return hashlib.md5(query.encode()).hexdigest()

def analyze_sentiment(text: str) -> str:
    """Simple sentiment analysis"""
    positive_words = ['breakthrough', 'success', 'innovative', 'revolutionary', 'promising', 'excellent']
    negative_words = ['failure', 'concern', 'risk', 'threat', 'problem', 'issue']
    
    text_lower = text.lower()
    pos_count = sum(word in text_lower for word in positive_words)
    neg_count = sum(word in text_lower for word in negative_words)
    
    if pos_count > neg_count:
        return "Positive 😊"
    elif neg_count > pos_count:
        return "Negative 😟"
    else:
        return "Neutral 😐"

def extract_key_topics(articles: List[Dict]) -> Dict[str, int]:
    """Extract and count key STEM topics"""
    topics = {
        'AI & Machine Learning': ['ai', 'artificial intelligence', 'machine learning', 'deep learning', 'neural'],
        'Quantum Computing': ['quantum', 'qubit', 'superposition', 'entanglement'],
        'Biotechnology': ['biotech', 'gene', 'crispr', 'dna', 'vaccine', 'medicine'],
        'Climate Tech': ['climate', 'renewable', 'sustainable', 'carbon', 'energy'],
        'Space Technology': ['space', 'rocket', 'satellite', 'mars', 'nasa', 'spacex'],
        'Robotics': ['robot', 'automation', 'autonomous', 'drone'],
        'Cybersecurity': ['cyber', 'security', 'encryption', 'privacy', 'hack'],
        'Blockchain': ['blockchain', 'crypto', 'defi', 'nft', 'web3']
    }
    
    topic_counts = {topic: 0 for topic in topics}
    
    for article in articles:
        text = (article.get('title', '') + ' ' + article.get('description', '')).lower()
        for topic, keywords in topics.items():
            if any(keyword in text for keyword in keywords):
                topic_counts[topic] += 1
    
    return {k: v for k, v in topic_counts.items() if v > 0}

def generate_ai_insights(articles: List[Dict], query: str) -> List[str]:
    """Generate AI-powered insights from articles"""
    insights = []
    
    # Topic analysis
    topics = extract_key_topics(articles)
    if topics:
        top_topic = max(topics, key=topics.get)
        insights.append(f"🎯 {top_topic} dominates the conversation with {topics[top_topic]} mentions")
    
    # Time analysis
    dates = [a.get('publishedAt', '')[:10] for a in articles if a.get('publishedAt')]
    if dates:
        recent_date = max(dates)
        insights.append(f"📅 Most recent coverage: {recent_date}")
    
    # Source diversity
    sources = list(set([a.get('source', {}).get('name', 'Unknown') for a in articles]))
    insights.append(f"📰 Coverage from {len(sources)} different sources shows {('broad' if len(sources) > 5 else 'focused')} interest")
    
    # Sentiment trend
    sentiments = [analyze_sentiment(a.get('title', '') + a.get('description', '')) for a in articles[:5]]
    positive_ratio = sentiments.count("Positive 😊") / len(sentiments) if sentiments else 0
    if positive_ratio > 0.6:
        insights.append("🌟 Overall positive sentiment suggests optimistic developments")
    elif positive_ratio < 0.4:
        insights.append("⚠️ Mixed sentiment indicates challenges or controversies")
    
    # Personalized insight based on search
    if 'quantum' in query.lower():
        insights.append("💡 Quantum computing news often precedes major tech shifts by 3-5 years")
    elif 'ai' in query.lower() or 'artificial' in query.lower():
        insights.append("🤖 AI developments are accelerating - consider upskilling in this area")
    
    return insights

def create_pdf_report(articles: List[Dict], query: str, insights: List[str]) -> bytes:
    """Generate PDF report of search results"""
    # Simplified PDF generation (you'd use reportlab in production)
    report = f"""
FUTURE STEM NEWS INTELLIGENCE REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
Search Query: {query}

EXECUTIVE SUMMARY
================
Total Articles: {len(articles)}
Date Range: {min([a.get('publishedAt', '')[:10] for a in articles if a.get('publishedAt')])} to {max([a.get('publishedAt', '')[:10] for a in articles if a.get('publishedAt')])}

KEY INSIGHTS
============
"""
    for insight in insights:
        report += f"• {insight}\n"
    
    report += "\n\nTOP ARTICLES\n============\n"
    for i, article in enumerate(articles[:10], 1):
        report += f"""
{i}. {article.get('title', 'No Title')}
   Source: {article.get('source', {}).get('name', 'Unknown')}
   Date: {article.get('publishedAt', '')[:10]}
   URL: {article.get('url', 'N/A')}
   
"""
    
    # Convert to bytes
    return report.encode('utf-8')

# Load CSS based on theme
st.markdown(load_css(st.session_state.dark_mode), unsafe_allow_html=True)

# Enhanced Header with animation
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown('<h1 class="main-header">🔬 Future STEM News Intelligence</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">AI-Powered STEM News Analysis & Personal Insights</p>', unsafe_allow_html=True)

# Top bar with theme toggle and share button
col1, col2, col3, col4 = st.columns([1, 1, 1, 3])
with col1:
    if st.button("🌓 Theme", help="Toggle dark/light mode"):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

with col2:
    # Share button with custom URL
    share_url = "https://future-stem-news-intelligence.streamlit.app"
    if st.button("📤 Share", help="Share this app"):
        st.info(f"Share this app: {share_url}")
        st.code(share_url)

with col3:
    if st.button("📊 Stats", help="View app statistics"):
        with st.expander("📊 App Statistics", expanded=True):
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.markdown("""
                <div class="metric-card">
                    <div class="metric-number">""" + str(len(st.session_state.search_history)) + """</div>
                    <div>Total Searches</div>
                </div>
                """, unsafe_allow_html=True)
            with col_b:
                st.markdown("""
                <div class="metric-card">
                    <div class="metric-number">""" + str(len(st.session_state.bookmarks)) + """</div>
                    <div>Bookmarks</div>
                </div>
                """, unsafe_allow_html=True)
            with col_c:
                st.markdown("""
                <div class="metric-card">
                    <div class="metric-number">""" + ("✓" if st.session_state.personality_type else "?") + """</div>
                    <div>Profile Set</div>
                </div>
                """, unsafe_allow_html=True)

# Developer Information
with st.expander("ℹ️ About Developer & Project", expanded=False):
    st.markdown("""
    <div class="developer-info">
        <h3>👨‍💻 Developed by: M Faby Rizky K</h3>
        <p><strong>Future STEM News Intelligence</strong> is an advanced AI-powered platform designed to revolutionize 
        how we consume and analyze Science, Technology, Engineering, and Mathematics news content.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **🎯 Project Vision:**
        - Democratize access to STEM knowledge
        - Provide intelligent news curation
        - Enable data-driven insights
        - Foster scientific literacy
        """)
        
        st.markdown("""
        **🛠️ Technology Stack:**
        - **Frontend:** Streamlit
        - **Data Processing:** Pandas, NumPy
        - **Visualization:** Matplotlib, Seaborn, Plotly
        - **NLP:** WordCloud, NLTK
        - **AI/ML:** Scikit-learn
        """)
    
    with col2:
        st.markdown("""
        **🌟 Key Features:**
        - 🔍 Real-time STEM news analysis
        - 📊 Interactive data visualizations
        - ☁️ Intelligent word cloud generation
        - 📈 Trend analysis and predictions
        - 🎯 Personalized content recommendations
        - 📱 Responsive and user-friendly interface
        """)
        
        st.markdown("""
        - 💼 LinkedIn: [https://www.linkedin.com/in/m-faby-rizky-k/](#)
        - 🐙 GitHub: [https://github.com/fabyrizky](#)
        - 📧 Email: fabyrizky@gmail.com
        """)

# Enhanced Sidebar
with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    
    # API Key input with validation
    api_key = st.text_input(
        "NewsAPI Key",
        type="password",
        value=st.session_state.api_key,
        help="Get your free API key at https://newsapi.org"
    )
    if api_key:
        st.session_state.api_key = api_key
        if len(api_key) == 32:  # Basic validation
            st.success("✅ API Key set")
        else:
            st.error("❌ Invalid API Key format")
    
    st.markdown("---")
    
    # Enhanced Personality Test
    st.markdown("### 🧠 Personality Profile")
    
    if st.session_state.personality_type:
        st.markdown(f"""
        <div class="personality-result">
            <h4>Your Type: {st.session_state.personality_type}</h4>
            <p>Personalized recommendations active</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 Retake Test", use_container_width=True):
            st.session_state.personality_type = None
            st.rerun()
    else:
        with st.expander("🎯 Take Personality Test", expanded=True):
            st.write("Discover your STEM personality type!")
            
            q1 = st.radio(
                "1. Your ideal work environment:",
                ["🏠 Home office with minimal distractions", 
                 "☕ Co-working space with some interaction", 
                 "🏢 Busy office with team collaboration"],
                key="q1"
            )
            
            q2 = st.radio(
                "2. When learning new tech:",
                ["📚 Read documentation thoroughly first", 
                 "🎯 Mix of reading and hands-on practice", 
                 "👥 Learn by teaching others"],
                key="q2"
            )
            
            q3 = st.radio(
                "3. Your innovation style:",
                ["🔬 Deep research on one problem", 
                 "🔄 Balance multiple projects", 
                 "🚀 Quick prototypes with feedback"],
                key="q3"
            )
            
            q4 = st.radio(
                "4. Preferred communication:",
                ["✉️ Async (email, messages)", 
                 "📞 Mix of async and meetings", 
                 "🎥 Video calls and presentations"],
                key="q4"
            )
            
            if st.button("🎯 Get Results", type="primary", use_container_width=True):
                # Enhanced scoring system
                scores = {"introvert": 0, "ambivert": 0, "ekstrovert": 0}
                
                answers = [q1, q2, q3, q4]
                for answer in answers:
                    if any(word in answer.lower() for word in ["home", "documentation", "deep", "async"]):
                        scores["introvert"] += 1
                    elif any(word in answer.lower() for word in ["mix", "balance", "some"]):
                        scores["ambivert"] += 1
                    else:
                        scores["ekstrovert"] += 1
                
                # Determine personality with descriptions
                personality_types = {
                    "introvert": ("Introvert", "🧘 The Deep Thinker - You excel at focused, analytical work"),
                    "ambivert": ("Ambivert", "⚖️ The Balancer - You adapt well to various situations"),
                    "ekstrovert": ("Ekstrovert", "🌟 The Collaborator - You thrive in social, dynamic environments")
                }
                
                max_score = max(scores.values())
                for ptype, score in scores.items():
                    if score == max_score:
                        st.session_state.personality_type, description = personality_types[ptype]
                        st.balloons()
                        break
                
                st.rerun()
    
    st.markdown("---")
    
    # Preferences Section
    st.markdown("### 🎨 Preferences")
    
    with st.expander("⚙️ App Settings"):
        # Language selection
        lang = st.selectbox(
            "Language",
            ["English", "Bahasa Indonesia"],
            index=0 if st.session_state.user_preferences['language'] == 'en' else 1
        )
        st.session_state.user_preferences['language'] = 'en' if lang == "English" else 'id'
        
        # Notification toggle
        notif = st.checkbox(
            "Enable notifications",
            value=st.session_state.user_preferences['notifications']
        )
        st.session_state.user_preferences['notifications'] = notif
        
        # Auto-refresh toggle
        auto_refresh = st.checkbox(
            "Auto-refresh results",
            value=st.session_state.user_preferences['auto_refresh']
        )
        st.session_state.user_preferences['auto_refresh'] = auto_refresh
    
    st.markdown("---")
    
    # Enhanced Search History
    st.markdown("### 📚 Recent Searches")
    if st.session_state.search_history:
        for i, query in enumerate(reversed(st.session_state.search_history[-5:]), 1):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.text(f"{i}. {query[:20]}...")
            with col2:
                if st.button("🔍", key=f"history_{i}", help=f"Search again: {query}"):
                    st.session_state.search_again = query
    else:
        st.info("No search history yet")
    
    # Bookmarks Section
    st.markdown("### 📌 Bookmarks")
    if st.session_state.bookmarks:
        st.info(f"{len(st.session_state.bookmarks)} articles saved")
        if st.button("📋 View All", use_container_width=True):
            st.session_state.show_bookmarks = True
    else:
        st.info("No bookmarks yet")

# Main Content Area
if not st.session_state.api_key:
    # Welcome screen for new users
    st.markdown("""
    <div class="feature-card">
        <h2>🎉 Welcome to Future STEM News Intelligence!</h2>
        <p>Your AI-powered companion for staying ahead in Science, Technology, Engineering, and Mathematics.</p>
        
        <h3>✨ What you can do:</h3>
        <ul>
            <li>🔍 Search and analyze STEM news in real-time</li>
            <li>📊 Visualize trends with interactive charts</li>
            <li>🧠 Get personalized career and project recommendations</li>
            <li>🤖 Receive AI-generated insights and predictions</li>
            <li>📄 Export reports and save bookmarks</li>
        </ul>
        
        <h3>🚀 Getting Started:</h3>
        <ol>
            <li>Get your free API key from <a href="https://newsapi.org/register" target="_blank">NewsAPI</a></li>
            <li>Enter the API key in the sidebar</li>
            <li>Take the personality test for personalized recommendations</li>
            <li>Start searching for STEM topics that interest you!</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature showcase
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>🎯 Smart Analysis</h3>
            <p>AI-powered insights that help you understand trends and patterns in STEM news</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>📈 Visual Intelligence</h3>
            <p>Interactive charts and visualizations that make complex data easy to understand</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h3>🚀 Personal Growth</h3>
            <p>Tailored recommendations for projects and careers based on your personality type</p>
        </div>
        """, unsafe_allow_html=True)

else:
    # Search Interface
    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
    
    with col1:
        # Check if we need to search again from history
        search_value = ""
        if hasattr(st.session_state, 'search_again'):
            search_value = st.session_state.search_again
            del st.session_state.search_again
        
        search_query = st.text_input(
            "🔍 Search STEM News:",
            placeholder="Try: quantum computing, CRISPR, Mars mission, neural networks...",
            value=search_value,
            key="search_input"
        )
    
    with col2:
        search_button = st.button("🔍 Search", type="primary", use_container_width=True)
    
    with col3:
        export_button = st.button("📄 Export", use_container_width=True, 
                                 disabled=not bool(st.session_state.get('last_search_results')))
    
    with col4:
        clear_button = st.button("🗑️ Clear", use_container_width=True)
    
    if clear_button:
        st.session_state.search_history = []
        st.session_state.search_results_cache = {}
        st.session_state.bookmarks = []
        st.rerun()
    
    # Enhanced search function with caching
    def fetch_news_cached(query, api_key):
        cache_key = get_cache_key(query)
        
        # Check cache first (valid for 1 hour)
        if cache_key in st.session_state.search_results_cache:
            cached_time, cached_data = st.session_state.search_results_cache[cache_key]
            if (datetime.now() - cached_time).seconds < 3600:  # 1 hour cache
                return cached_data
        
        # Fetch fresh data
        url = "https://newsapi.org/v2/everything"
        params = {
            'q': f'{query} AND (science OR technology OR engineering OR mathematics OR research)',
            'apiKey': api_key,
            'language': 'en',
            'sortBy': 'relevancy',
            'pageSize': 50,  # Get more results for better analysis
            'from': (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                # Cache the results
                st.session_state.search_results_cache[cache_key] = (datetime.now(), data)
                return data
            else:
                st.error(f"API Error: {response.status_code}")
                return None
        except requests.exceptions.Timeout:
            st.error("Request timed out. Please try again.")
            return None
        except Exception as e:
            st.error(f"Error: {str(e)}")
            return None
    
    # Handle search
    if (search_button or search_value) and search_query:
        # Add to history
        if search_query not in st.session_state.search_history:
            st.session_state.search_history.append(search_query)
        
        # Show loading animation
        with st.spinner('🔄 Analyzing STEM news...'):
            news_data = fetch_news_cached(search_query, st.session_state.api_key)
        
        if news_data and news_data.get('articles'):
            articles = news_data['articles']
            st.session_state.last_search_results = articles
            
            # Generate AI insights
            insights = generate_ai_insights(articles, search_query)
            
            # Display results count with animation
            st.success(f"✨ Found {len(articles)} articles about '{search_query}'")
            
            # Quick stats bar
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Articles", len(articles))
            with col2:
                sources = len(set([a.get('source', {}).get('name', 'Unknown') for a in articles]))
                st.metric("Sources", sources)
            with col3:
                topics = extract_key_topics(articles)
                st.metric("Topics", len(topics))
            with col4:
                recent = sum(1 for a in articles if a.get('publishedAt', '')[:10] == datetime.now().strftime('%Y-%m-%d'))
                st.metric("Today", recent)
            
            # Enhanced tabs with icons
            tab1, tab2, tab3, tab4, tab5 = st.tabs([
                "📰 News Feed", 
                "📊 Analytics", 
                "💡 AI Insights", 
                "🎯 Personalized", 
                "📌 Bookmarks"
            ])
            
            with tab1:
                st.markdown("### 📰 Latest Articles")
                
                # Filter and sort options
                col1, col2, col3 = st.columns([2, 2, 1])
                with col1:
                    sort_by = st.selectbox("Sort by", ["Relevance", "Date", "Source"])
                with col2:
                    filter_source = st.selectbox(
                        "Filter source",
                        ["All"] + list(set([a.get('source', {}).get('name', 'Unknown') for a in articles]))
                    )
                with col3:
                    view_mode = st.radio("View", ["Cards", "List"], horizontal=True)
                
                # Apply filters
                filtered_articles = articles
                if filter_source != "All":
                    filtered_articles = [a for a in articles if a.get('source', {}).get('name') == filter_source]
                
                # Sort articles
                if sort_by == "Date":
                    filtered_articles.sort(key=lambda x: x.get('publishedAt', ''), reverse=True)
                
                # Display articles
                for i, article in enumerate(filtered_articles[:20]):
                    if view_mode == "Cards":
                        st.markdown(f"""
                        <div class="news-card">
                            <h4>{article.get('title', 'No Title')}</h4>
                            <p><strong>Source:</strong> {article.get('source', {}).get('name', 'Unknown')} | 
                               <strong>Date:</strong> {article.get('publishedAt', '')[:10]} |
                               <strong>Sentiment:</strong> {analyze_sentiment(article.get('title', '') + article.get('description', ''))}
                            </p>
                            <p>{article.get('description', 'No description available.')[:200]}...</p>
                            <a href="{article.get('url', '#')}" target="_blank">Read more →</a>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Bookmark button
                        col1, col2, col3 = st.columns([1, 1, 4])
                        with col1:
                            if st.button("📌 Bookmark", key=f"bookmark_{i}"):
                                if article not in st.session_state.bookmarks:
                                    st.session_state.bookmarks.append(article)
                                    st.success("Bookmarked!")
                    else:
                        # List view
                        with st.expander(f"{i+1}. {article.get('title', 'No Title')[:80]}..."):
                            st.write(f"**Source:** {article.get('source', {}).get('name', 'Unknown')}")
                            st.write(f"**Date:** {article.get('publishedAt', '')[:10]}")
                            st.write(f"**Description:** {article.get('description', 'No description')}")
                            st.write(f"**URL:** {article.get('url', 'N/A')}")
                            if st.button("📌 Bookmark", key=f"bookmark_list_{i}"):
                                if article not in st.session_state.bookmarks:
                                    st.session_state.bookmarks.append(article)
                                    st.success("Bookmarked!")
            
            with tab2:
                st.markdown("### 📊 Data Analytics Dashboard")
                
                # Analytics layout
                col1, col2 = st.columns(2)
                
                with col1:
                    # Enhanced Word Cloud
                    st.markdown("#### ☁️ Topic Cloud")
                    all_text = " ".join([
                        article.get('title', '') + " " + article.get('description', '')
                        for article in articles
                    ])
                    
                    if all_text.strip():
                        # Remove common words
                        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'from', 'that', 'this', 'is', 'was', 'are', 'were'}
                        words = all_text.lower().split()
                        filtered_words = [word for word in words if word not in stop_words and len(word) > 3]
                        filtered_text = " ".join(filtered_words)
                        
                        wordcloud = WordCloud(
                            width=600,
                            height=400,
                            background_color='white' if not st.session_state.dark_mode else 'black',
                            colormap='viridis',
                            max_words=50
                        ).generate(filtered_text)
                        
                        fig, ax = plt.subplots(figsize=(10, 6))
                        ax.imshow(wordcloud, interpolation='bilinear')
                        ax.axis('off')
                        st.pyplot(fig)
                
                with col2:
                    # Topic Distribution
                    st.markdown("#### 🎯 Topic Distribution")
                    topics = extract_key_topics(articles)
                    if topics:
                        df_topics = pd.DataFrame(list(topics.items()), columns=['Topic', 'Count'])
                        fig = px.pie(
                            df_topics,
                            values='Count',
                            names='Topic',
                            title="STEM Topics Distribution",
                            color_discrete_sequence=px.colors.qualitative.Set3
                        )
                        fig.update_traces(textposition='inside', textinfo='percent+label')
                        st.plotly_chart(fig, use_container_width=True)
                
                # Timeline Analysis
                st.markdown("#### 📅 Publication Timeline")
                dates = []
                for article in articles:
                    if article.get('publishedAt'):
                        dates.append(article['publishedAt'][:10])
                
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
                        line=dict(color='#667eea', width=3),
                        marker=dict(size=10)
                    ))
                    fig.update_layout(
                        title="Articles Published Over Time",
                        xaxis_title="Date",
                        yaxis_title="Number of Articles",
                        hovermode='x unified'
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                # Source Analysis
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### 📰 Top Sources")
                    sources = [article.get('source', {}).get('name', 'Unknown') for article in articles]
                    source_counts = Counter(sources).most_common(10)
                    df_sources = pd.DataFrame(source_counts, columns=['Source', 'Articles'])
                    
                    fig = px.bar(
                        df_sources,
                        x='Articles',
                        y='Source',
                        orientation='h',
                        title="Top 10 News Sources",
                        color='Articles',
                        color_continuous_scale='Blues'
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    st.markdown("#### 😊 Sentiment Analysis")
                    sentiments = [analyze_sentiment(a.get('title', '') + a.get('description', '')) for a in articles[:20]]
                    sentiment_counts = Counter(sentiments)
                    
                    fig = px.pie(
                        values=list(sentiment_counts.values()),
                        names=list(sentiment_counts.keys()),
                        title="Article Sentiment Distribution",
                        color_discrete_map={
                            'Positive 😊': '#4CAF50',
                            'Neutral 😐': '#FFC107',
                            'Negative 😟': '#F44336'
                        }
                    )
                    st.plotly_chart(fig, use_container_width=True)
            
            with tab3:
                st.markdown("### 🤖 AI-Powered Insights")
                
                # Display AI insights with icons
                st.markdown("#### 🔮 Key Insights")
                for insight in insights:
                    st.info(insight)
                
                # Trend Prediction
                st.markdown("#### 📈 Trend Analysis")
                topics = extract_key_topics(articles)
                if topics:
                    # Create trend visualization
                    df_trends = pd.DataFrame(list(topics.items()), columns=['Topic', 'Mentions'])
                    df_trends['Trend'] = df_trends['Mentions'].apply(lambda x: '🔥 Hot' if x > 5 else '📈 Rising' if x > 2 else '🌱 Emerging')
                    
                    fig = px.bar(
                        df_trends,
                        x='Topic',
                        y='Mentions',
                        color='Trend',
                        title="STEM Topic Trends",
                        color_discrete_map={
                            '🔥 Hot': '#FF6B6B',
                            '📈 Rising': '#4ECDC4',
                            '🌱 Emerging': '#95E1D3'
                        }
                    )
                    fig.update_layout(xaxis_tickangle=-45)
                    st.plotly_chart(fig, use_container_width=True)
                
                # Research Suggestions
                st.markdown("#### 🔬 Research Opportunities")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("""
                    <div class="feature-card">
                        <h4>📚 Literature Gaps</h4>
                        <ul>
                            <li>Cross-disciplinary applications</li>
                            <li>Long-term impact studies</li>
                            <li>Ethical implications research</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown("""
                    <div class="feature-card">
                        <h4>🚀 Innovation Areas</h4>
                        <ul>
                            <li>Practical applications</li>
                            <li>Scalability solutions</li>
                            <li>User experience design</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
            
            with tab4:
                st.markdown("### 🎯 Personalized Recommendations")
                
                if st.session_state.personality_type:
                    personality = st.session_state.personality_type
                    
                    # Enhanced recommendations based on personality and search
                    recommendations = {
                        "Introvert": {
                            "careers": {
                                "AI": ["ML Research Scientist", "Data Scientist", "AI Ethics Researcher"],
                                "Quantum": ["Quantum Algorithm Developer", "Theoretical Physicist", "Quantum Software Engineer"],
                                "Biotech": ["Bioinformatics Specialist", "Computational Biologist", "Genomics Researcher"],
                                "General": ["Research Scientist", "Technical Writer", "Software Architect"]
                            },
                            "projects": {
                                "AI": ["Build a personal AI assistant", "Create ML model for research papers", "Develop ethical AI framework"],
                                "Quantum": ["Quantum circuit simulator", "Cryptography research", "Quantum algorithm visualization"],
                                "Biotech": ["Gene sequence analyzer", "Protein folding predictor", "Bioinformatics pipeline"],
                                "General": ["Open-source contribution", "Technical blog series", "Research paper"]
                            },
                            "learning": {
                                "style": "Self-paced online courses, books, documentation",
                                "platforms": ["Coursera", "edX", "ArXiv papers", "Technical books"],
                                "approach": "Deep dive into fundamentals before practice"
                            }
                        },
                        "Ambivert": {
                            "careers": {
                                "AI": ["AI Product Manager", "ML Engineer", "AI Consultant"],
                                "Quantum": ["Quantum Computing Consultant", "Quantum Software Lead", "Research Coordinator"],
                                "Biotech": ["Biotech Project Manager", "Clinical Data Analyst", "Bioinformatics Team Lead"],
                                "General": ["Tech Lead", "Solutions Architect", "Innovation Manager"]
                            },
                            "projects": {
                                "AI": ["AI-powered web app", "Collaborative ML platform", "AI workshop series"],
                                "Quantum": ["Quantum computing tutorial", "Hybrid classical-quantum app", "Quantum hackathon"],
                                "Biotech": ["Health tracking platform", "Biotech startup MVP", "Research collaboration tool"],
                                "General": ["Full-stack application", "Tech meetup organization", "Cross-functional project"]
                            },
                            "learning": {
                                "style": "Mix of self-study and group learning",
                                "platforms": ["Udacity", "Pluralsight", "Local meetups", "Online communities"],
                                "approach": "Balance theory with hands-on projects"
                            }
                        },
                        "Ekstrovert": {
                            "careers": {
                                "AI": ["AI Evangelist", "Developer Relations", "AI Sales Engineer"],
                                "Quantum": ["Quantum Computing Educator", "Business Development", "Community Manager"],
                                "Biotech": ["Biotech Entrepreneur", "Clinical Trial Manager", "Science Communicator"],
                                "General": ["Tech Evangelist", "Startup Founder", "Conference Speaker"]
                            },
                            "projects": {
                                "AI": ["AI education YouTube channel", "Community AI project", "AI conference organization"],
                                "Quantum": ["Quantum computing podcast", "Public quantum demos", "Educational workshop series"],
                                "Biotech": ["Public health campaign", "Biotech startup", "Science communication blog"],
                                "General": ["Tech conference", "Community platform", "Educational content creation"]
                            },
                            "learning": {
                                "style": "Interactive workshops, bootcamps, conferences",
                                "platforms": ["General Assembly", "Tech conferences", "Hackathons", "Bootcamps"],
                                "approach": "Learn by teaching and networking"
                            }
                        }
                    }
                    
                    # Get relevant category based on search
                    category = "General"
                    if "ai" in search_query.lower() or "artificial" in search_query.lower():
                        category = "AI"
                    elif "quantum" in search_query.lower():
                        category = "Quantum"
                    elif any(word in search_query.lower() for word in ["bio", "gene", "medicine", "health"]):
                        category = "Biotech"
                    
                    recs = recommendations.get(personality, recommendations["Ambivert"])
                    
                    # Display recommendations in beautiful cards
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown(f"""
                        <div class="personality-result">
                            <h3>💼 Career Paths for {personality}s in {category}</h3>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        for career in recs["careers"].get(category, recs["careers"]["General"]):
                            st.markdown(f"""
                            <div class="feature-card">
                                <h4>👔 {career}</h4>
                                <p>Perfect for {personality.lower()}s interested in {search_query}</p>
                            </div>
                            """, unsafe_allow_html=True)
                    
                    with col2:
                        st.markdown(f"""
                        <div class="personality-result">
                            <h3>🚀 Project Ideas for {personality}s</h3>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        for project in recs["projects"].get(category, recs["projects"]["General"]):
                            st.markdown(f"""
                            <div class="feature-card">
                                <h4>💡 {project}</h4>
                                <p>Leverage your {personality.lower()} strengths</p>
                            </div>
                            """, unsafe_allow_html=True)
                    
                    # Learning recommendations
                    st.markdown("#### 📚 Personalized Learning Path")
                    learning = recs["learning"]
                    
                    st.markdown(f"""
                    <div class="feature-card">
                        <h4>🎓 Recommended Learning Style</h4>
                        <p><strong>Style:</strong> {learning['style']}</p>
                        <p><strong>Platforms:</strong> {', '.join(learning['platforms'])}</p>
                        <p><strong>Approach:</strong> {learning['approach']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Action steps
                    st.markdown("#### 🎯 Next Steps")
                    action_steps = [
                        f"1. Explore {category} courses on recommended platforms",
                        f"2. Start with a small {personality.lower()}-friendly project",
                        f"3. Connect with {category} communities that match your style",
                        f"4. Set up personalized news alerts for {search_query}",
                        f"5. Create a learning schedule that fits your {personality.lower()} energy patterns"
                    ]
                    
                    for step in action_steps:
                        st.success(step)
                
                else:
                    st.warning("🧠 Complete the personality test in the sidebar for personalized recommendations!")
            
            with tab5:
                st.markdown("### 📌 Your Bookmarks")
                
                if st.session_state.bookmarks:
                    # Bookmark management
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.info(f"You have {len(st.session_state.bookmarks)} bookmarked articles")
                    with col2:
                        if st.button("🗑️ Clear All", key="clear_bookmarks"):
                            st.session_state.bookmarks = []
                            st.rerun()
                    
                    # Display bookmarks
                    for i, article in enumerate(st.session_state.bookmarks):
                        col1, col2 = st.columns([4, 1])
                        with col1:
                            st.markdown(f"""
                            <div class="news-card">
                                <h4>{i+1}. {article.get('title', 'No Title')}</h4>
                                <p><strong>Source:</strong> {article.get('source', {}).get('name', 'Unknown')} | 
                                   <strong>Date:</strong> {article.get('publishedAt', '')[:10]}</p>
                                <p>{article.get('description', 'No description available.')[:150]}...</p>
                                <a href="{article.get('url', '#')}" target="_blank">Read full article →</a>
                            </div>
                            """, unsafe_allow_html=True)
                        with col2:
                            if st.button("❌", key=f"remove_bookmark_{i}", help="Remove bookmark"):
                                st.session_state.bookmarks.pop(i)
                                st.rerun()
                else:
                    st.info("No bookmarks yet. Click the 📌 button on any article to save it here!")
        
        else:
            st.error("No results found. Try different keywords or check your API key.")
    
    # Export functionality
    if export_button and 'last_search_results' in st.session_state:
        with st.spinner("Generating report..."):
            articles = st.session_state.last_search_results
            insights = generate_ai_insights(articles, st.session_state.search_history[-1])
            report = create_pdf_report(articles, st.session_state.search_history[-1], insights)
            
            # Create download button
            st.download_button(
                label="📥 Download Report",
                data=report,
                file_name=f"stem_news_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )

# Footer
st.markdown("---")
st.markdown(f"""
<div style='text-align: center; color: #666; padding: 2rem;'>
    <p>🚀 Future STEM News Intelligence v2.0 | Built with ❤️ using Streamlit</p>
    <p>Share this app: <code>https://future-stem-news-intelligence.streamlit.app</code></p>
    <p>© 2024 | Powered by NewsAPI | <a href="https://github.com/yourusername/future-stem-news" target="_blank">GitHub</a></p>
</div>
""", unsafe_allow_html=True)
# Auto-refresh functionality
if st.session_state.user_preferences['auto_refresh']:
    time.sleep(300)  # Refresh every 5 minutes
    st.rerun()