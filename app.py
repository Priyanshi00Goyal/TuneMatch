import streamlit as st
import pandas as pd

from recommender import (
    load_data,
    get_recommendations
)


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="TuneMatch",
    page_icon="🎵",
    layout="wide"
)


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown(
    """
    <style>

    .main-title {
        font-size: 48px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 10px;
    }

    .subtitle {
        text-align: center;
        font-size: 20px;
        margin-bottom: 40px;
    }

    .song-card {
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #ddd;
        margin-bottom: 15px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

DATA_PATH = "data/songs.csv"

df = load_data(DATA_PATH)


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown(
    '<div class="main-title">🎵 TuneMatch</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Discover songs that match your musical taste.'
    '</div>',
    unsafe_allow_html=True
)


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.title("🎧 TuneMatch")

st.sidebar.write(
    "Choose a song and let the recommendation engine "
    "find similar tracks."
)

number_of_recommendations = st.sidebar.slider(
    "Number of recommendations",
    min_value=1,
    max_value=10,
    value=5
)


# --------------------------------------------------
# SONG SELECTION
# --------------------------------------------------

st.subheader("🎶 Choose a song")

selected_song = st.selectbox(
    "Select a song:",
    df["title"].tolist()
)


# --------------------------------------------------
# SELECTED SONG INFORMATION
# --------------------------------------------------

selected_data = df[
    df["title"] == selected_song
].iloc[0]

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Artist",
        selected_data["artist"]
    )

with col2:
    st.metric(
        "Genre",
        selected_data["genre"]
    )

with col3:
    st.metric(
        "Year",
        int(selected_data["year"])
    )

with col4:
    st.metric(
        "Energy",
        round(selected_data["energy"], 2)
    )


# --------------------------------------------------
# RECOMMEND BUTTON
# --------------------------------------------------

if st.button(
    "🎵 Find Similar Songs",
    use_container_width=True
):

    recommendations = get_recommendations(
        df,
        selected_song,
        number_of_recommendations
    )

    if recommendations.empty:

        st.error(
            "Sorry, we couldn't find recommendations."
        )

    else:

        st.success(
            f"Songs similar to **{selected_song}**"
        )

        for _, song in recommendations.iterrows():

            st.markdown(
                f"""
                <div class="song-card">

                <h3>🎵 {song['title']}</h3>

                <p>
                <b>Artist:</b> {song['artist']} |
                <b>Genre:</b> {song['genre']} |
                <b>Year:</b> {int(song['year'])}
                </p>

                <p>
                Similarity:
                <b>{song['similarity']}%</b>
                </p>

                </div>
                """,
                unsafe_allow_html=True
            )


# --------------------------------------------------
# DATASET
# --------------------------------------------------

st.divider()

st.subheader("📚 Song Dataset")

st.dataframe(
    df,
    use_container_width=True
)


# --------------------------------------------------
# ABOUT
# --------------------------------------------------

st.divider()

st.subheader("ℹ️ How does TuneMatch work?")

st.write(
    """
    TuneMatch compares songs using numerical audio features:

    • Danceability  
    • Energy  
    • Acousticness  
    • Instrumentalness  
    • Valence  

    The features are standardized and compared using
    cosine similarity. Songs with more similar feature
    patterns receive higher similarity scores.
    """
)
