import streamlit as st
import pandas as pd
import joblib
import requests
import os
import gdown
from dotenv import load_dotenv
import time


load_dotenv()
API_KEY = os.getenv('TMDB_API_KEY')

st.set_page_config(
    page_title="Movie Recommender System",
    page_icon="🎬",
    layout="wide"
)


def download_if_missing(url, filename):
    
    if not os.path.exists(filename):
        st.warning(f"Downloading {filename} (first run only)...")
        gdown.download(url, filename, quiet=False)

# G- Drive file links 
download_if_missing("https://drive.google.com/uc?id=1m6fCzyvM3IcD-ieFYBZoND6UBnZKHmJL", "cleaned_movie_df.pkl")

download_if_missing("https://drive.google.com/uc?id=1Faq17OXipnG1rEVJcOlvG7j_-WEn9Yns", "siml_matrix.pkl")


with open('style.css','r',encoding='utf-8') as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

@st.cache_resource
def load_data():
    df = pd.read_pickle('cleaned_movie_df.pkl')
    siml = joblib.load('siml_matrix.pkl')
    return df, siml

df, siml = load_data()


@st.cache_data(ttl=100)
def get_movie_details(movie_id, movie_title=None, release_date=None):
    base_url = "https://image.tmdb.org/t/p/w500"
    no_poster = "https://placehold.co/300x450/1a1a1a/e50914?text=Poster%0ANot%0AAvailable"
    poster, trailer = None, None
    
    year = None
    if release_date:
        try:
            year = str(release_date)[:4]
        except:
            pass

    try:
        # 1️⃣ Try fetching by movie_id
        resp = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}',
                            params={'api_key': API_KEY})
        if resp.status_code == 200:
            data = resp.json()
            if data.get('poster_path'):
                poster = f"{base_url}{data['poster_path']}"

            vids = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}/videos',
                                params={'api_key': API_KEY})
            if vids.status_code == 200:
                for v in vids.json().get('results', []):
                    if v.get('type') == 'Trailer' and v.get('site') == 'YouTube':
                        trailer = f"https://www.youtube.com/watch?v={v['key']}"
                        break

        # 2️⃣ Fallback to soarch by title
        if movie_title and not poster:
            search_params = {"api_key": API_KEY, "query": movie_title}
            if year:
                search_params["year"] = year

            search = requests.get("https://api.themoviedb.org/3/search/movie", params=search_params)
            results = search.json().get("results", []) if search.status_code == 200 else []

            if not results:
                search = requests.get("https://api.themoviedb.org/3/search/movie",
                                      params={"api_key": API_KEY, "query": movie_title})
                results = search.json().get("results", []) if search.status_code == 200 else []

            if results:
                match = results[0]
                if not poster and match.get("poster_path"):
                    poster = f"{base_url}{match['poster_path']}"
                if not trailer and match.get("id"):
                    tid = match["id"]
                    vids = requests.get(f'https://api.themoviedb.org/3/movie/{tid}/videos',
                                        params={'api_key': API_KEY})
                    if vids.status_code == 200:
                        for v in vids.json().get('results', []):
                            if v.get('type') == 'Trailer' and v.get('site') == 'YouTube':
                                trailer = f"https://www.youtube.com/watch?v={v['key']}"
                                break

        if not poster:
            poster = no_poster
        if not trailer and movie_title:
            trailer = f"https://www.youtube.com/results?search_query={movie_title}+trailer"

        return {"poster_url": poster, "trailer_url": trailer}

    except:
        return {"poster_url": no_poster, "trailer_url": None}


def recommend(movie_title, num_rcm=5):
    try:
        idx = df[df['title'] == movie_title].index[0]
    except:
        return None
    
    dist = siml[idx]
    similar = sorted(list(enumerate(dist)), reverse=True, key=lambda x: x[1])[1:num_rcm+1]
    
    results = []
    for i in similar:
        results.append({
            'title': df.iloc[i[0]]['title'],
            'movie_id': df.iloc[i[0]]['id'],
            'similarity_score': i[1],
            'genres': df.iloc[i[0]]['genres'],
            'release_date': df.iloc[i[0]]['release_date'],
            'vote_average': df.iloc[i[0]]['vote_average'],
            'overview': df.iloc[i[0]]['overview'],
            'cast': df.iloc[i[0]]['cast_clean'],
            'director': df.iloc[i[0]]['crew_lean']
        })
    
    return results


def create_movie_card(movie, idx):
    media = get_movie_details(movie['movie_id'], movie['title'], movie['release_date'])
    
    poster = media['poster_url'] or "https://placehold.co/300x450/1a1a1a/e50914?text=Poster%0ANot%0AAvailable"
    trailer = media['trailer_url'] or f"https://www.youtube.com/results?search_query={movie['title']}+trailer"
    
    with st.container():
        card_html = f"""
        <div class="movie-card">
            <div class="rating-badge">⭐ {movie['vote_average']}/10</div>
            <img src="{poster}" class="movie-poster" alt="{movie['title']}"
                 onerror="this.src='https://placehold.co/300x450/1a1a1a/e50914?text=No+Poster';">
            <div class="movie-title">{movie['title']}</div>
            <a href="{trailer}" target="_blank" class="trailer-btn">▶ Watch Trailer</a>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)
        
        with st.expander("📖 View Full Details", expanded=False):
            col1, col2 = st.columns([1, 2])
            with col1:
                st.image(poster, width=200)
            with col2:
                st.markdown(f"### {movie['title']}")
                st.markdown(f"**⭐ Rating:** {movie['vote_average']}/10")
                st.markdown(f"**📅 Release Date:** {movie['release_date']}")
                st.markdown(f"**🎭 Genres:** {movie['genres']}")
                st.markdown(f"**🎬 Director:** {movie['director']}")
                st.markdown(f"**👥 Cast:** {movie['cast']}")
                st.markdown("**📖 Overview:**")
                st.write(movie['overview'])
                


col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.title("Cinepolis - Find Your Next Movie")
    st.markdown("## 🎬 Movie Recommendation System")
    st.markdown("**Note:** Dataset contains movies till 2017")

    movie_list = df['title'].values
    selected_movie = st.selectbox("Type or select a movie:", movie_list)
    show_recs = st.button("🔍 Get Recommendations", type="primary")

if show_recs:
    sp_col1, sp_col2, sp_col3 = st.columns([1, 2, 1])
    with sp_col2:
        with st.spinner("Finding similar movies..."):
            recs = recommend(selected_movie, 5)
    
    if recs:
        st.markdown(f"<h2 style='text-align: center;'>🎯 Movies Similar to: <strong>{selected_movie}</strong></h2>", unsafe_allow_html=True)
        st.markdown("---")
        
        sp2_col1, sp2_col2, sp2_col3 = st.columns([1, 2, 1])
        with sp2_col2:
            with st.spinner("Loading movie details..."):
                time.sleep(1.5)
        
        col_left, col_center, col_right = st.columns([0.3, 3, 0.3])
        with col_center:
            cols_per_row = 3
            for i in range(0, len(recs), cols_per_row):
                cols = st.columns(cols_per_row)
                for j in range(cols_per_row):
                    if i + j < len(recs):
                        with cols[j]:
                            create_movie_card(recs[i + j], i + j)
    else:
        st.error("Movie not found!")
