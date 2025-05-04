import pandas as pd
import streamlit as st
import requests
import os
from dotenv import load_dotenv
import ast

# Load API key from .env
load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

# Handle missing API key
if not TMDB_API_KEY:
    st.error("TMDB API Key is missing. Please create a .env file with TMDB_API_KEY=your_key_here")
    st.stop()

st.set_page_config(layout="wide")
st.title("🎬 SDG-Aware Movie Recommendation System")

# Fetch movie poster from TMDB
def fetch_poster(title):
    search_url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={title}"
    response = requests.get(search_url)
    data = response.json()
    
    if data['results']:
        poster_path = data['results'][0].get('poster_path')
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"
    return None

# Load movie dataset
df = pd.read_csv('tmdb_5000_movies.csv')

# Extract genre names from stringified lists
def extract_genre_names(genre_str):
    try:
        genre_list = ast.literal_eval(genre_str)
        return [genre['name'] for genre in genre_list if 'name' in genre]
    except:
        return []

df['genre_names'] = df['genres'].apply(extract_genre_names)

# SDG keyword mapping
sdg_keywords = {
    'SDG 4: Quality Education': ['education', 'learning', 'school', 'teaching', 'student', 'knowledge'],
    'SDG 5: Gender Equality': ['gender', 'women', 'equality', 'feminism', 'empowerment'],
    'SDG 10: Reduced Inequalities': ['racism', 'poverty', 'discrimination', 'inequality', 'marginalized', 'migration'],
    'SDG 13: Climate Action': ['climate', 'environment', 'pollution', 'sustainability', 'nature'],
    'SDG 16: Peace & Justice': ['justice', 'peace', 'crime', 'corruption', 'law', 'human rights']
}

# Tag movies with SDGs based on overview keywords
def map_sdgs(overview):
    matched_sdgs = []
    if isinstance(overview, str):
        overview = overview.lower()
        for sdg, keywords in sdg_keywords.items():
            if any(keyword in overview for keyword in keywords):
                matched_sdgs.append(sdg)
    return matched_sdgs

df['sdg_tags'] = df['overview'].apply(map_sdgs)

# Search bar
search_query = st.text_input("🔍 Search for a movie by title")

# Handle search results
if search_query:
    searched = df[df['title'].str.contains(search_query, case=False, na=False)]
    st.subheader("🔎 Search Results")
    if not searched.empty:
        for _, row in searched.iterrows():
            with st.container():
                col1, col2 = st.columns([1, 2])
                with col1:
                    poster_url = fetch_poster(row['title'])
                    if poster_url:
                        st.image(poster_url, width=150)
                with col2:
                    st.markdown(f"### 🎬 {row['title']}")
                    st.write("**SDG Tags:**", ", ".join(row['sdg_tags']) if row['sdg_tags'] else "None")
                    st.write("**Genres:**", ", ".join(row['genre_names']) if row['genre_names'] else "Unknown")
                    st.write("**Rating:**", row.get('vote_average', 'N/A'))
                st.markdown("---")
    else:
        st.warning("No movies found for your search.")

# SDG dropdown
sdg_options = list(sdg_keywords.keys())
selected_sdg = st.selectbox("🎯 Select SDG", options=[""] + sdg_options, format_func=lambda x: "" if x == "" else x)

# Genre multiselect
all_genres = sorted(set(genre for sublist in df['genre_names'] for genre in sublist))
selected_genres = st.multiselect("🎭 Filter by Genre:", all_genres)

# Slider for number of movies
num_recs = st.slider("Number of recommendations:", min_value=1, max_value=20, value=10)

# SDG-based filtering and recommendation display
if selected_sdg:
    filtered = df[df['sdg_tags'].apply(lambda tags: selected_sdg in tags)]
    if selected_genres:
        filtered = filtered[filtered['genre_names'].apply(lambda g_list: any(g in g_list for g in selected_genres))]
    st.subheader(f"🎯 Top {num_recs} Recommendations for {selected_sdg}")

    # Show in groups of 5
    movie_chunks = [filtered.head(num_recs).iloc[i:i+5] for i in range(0, num_recs, 5)]

    for chunk in movie_chunks:
        cols = st.columns(5)
        for col, (_, row) in zip(cols, chunk.iterrows()):
            with col:
                with st.container():
                    poster_url = fetch_poster(row['title'])
                    if poster_url:
                        st.image(poster_url, use_container_width=True)
                    else:
                        st.markdown("🎞️ *No poster available*")

                    st.markdown(f"**🎬 {row['title']}**", help=row['overview'])
                    st.markdown(f"**🎯 SDGs:** {', '.join(row['sdg_tags']) if row['sdg_tags'] else 'None'}")
                    st.markdown(f"**🎭 Genres:** {', '.join(row['genre_names']) if row['genre_names'] else 'Unknown'}")
                    st.markdown(f"**⭐ Rating:** {row.get('vote_average', 'N/A')}")

                    # Like/Dislike buttons
                    unique_key = f"{row.name}_{row.get('title', 'movie')}"
                    col_like, col_dislike = st.columns([1, 1])
                    with col_like:
                        if st.button("👍 Like", key=f"like_{unique_key}"):
                            st.success("You liked this movie!")
                    with col_dislike:
                        if st.button("👎 Dislike", key=f"dislike_{unique_key}"):
                            st.warning("You disliked this movie!")
