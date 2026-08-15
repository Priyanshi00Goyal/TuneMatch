import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from recommender import (
    load_data,
    get_recommendations
)


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="TuneMatch",
    page_icon="🎵",
    layout="wide"
)


# ==================================================
# CUSTOM CSS
# ==================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 50px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        font-size: 20px;
        margin-bottom: 35px;
    }

    .song-card {
        padding: 18px;
        border-radius: 12px;
        border: 1px solid #ddd;
        margin-bottom: 12px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ==================================================
# LOAD DATA
# ==================================================

DATA_PATH = "data/songs.csv"

df = load_data(DATA_PATH)


# ==================================================
# HEADER
# ==================================================

st.markdown(
    '<div class="main-title">🎵 TuneMatch</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Discover music that matches your taste.'
    '</div>',
    unsafe_allow_html=True
)


# ==================================================
# SIDEBAR
# ==================================================

st.sidebar.title("🎧 TuneMatch")

st.sidebar.write(
    "Your personal music recommendation engine."
)


# --------------------------------------------------
# GENRE FILTER
# --------------------------------------------------

genres = ["All"] + sorted(df["genre"].unique().tolist())

selected_genre = st.sidebar.selectbox(
    "🎼 Select Genre",
    genres
)


# --------------------------------------------------
# NUMBER OF RECOMMENDATIONS
# --------------------------------------------------

number_of_recommendations = st.sidebar.slider(
    "🎵 Number of Recommendations",
    min_value=1,
    max_value=10,
    value=5
)


# ==================================================
# FILTER DATA
# ==================================================

if selected_genre == "All":

    filtered_df = df.copy()

else:

    filtered_df = df[
        df["genre"] == selected_genre
    ].copy()


# ==================================================
# SONG SELECTION
# ==================================================

st.subheader("🎶 Choose a song")

if filtered_df.empty:

    st.warning("No songs available for this genre.")

else:

    selected_song = st.selectbox(
        "Select a song:",
        filtered_df["title"].tolist()
    )


    # ==================================================
    # SELECTED SONG INFORMATION
    # ==================================================

    selected_data = df[
        df["title"] == selected_song
    ].iloc[0]


    st.subheader("🎵 Now Selected")

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
            "Release Year",
            int(selected_data["year"])
        )

    with col4:

        st.metric(
            "Energy",
            round(
                selected_data["energy"],
                2
            )
        )


    # ==================================================
    # FEATURE VISUALIZATION
    # ==================================================

    st.subheader("📊 Audio Features")

    features = [
        "danceability",
        "energy",
        "acousticness",
        "instrumentalness",
        "valence"
    ]

    values = [
        selected_data[feature]
        for feature in features
    ]


    fig, ax = plt.subplots()

    ax.bar(
        features,
        values
    )

    ax.set_ylim(0, 1)

    ax.set_ylabel("Value")

    ax.set_title(
        f"Audio Features — {selected_song}"
    )

    plt.xticks(
        rotation=30
    )

    st.pyplot(fig)


    # ==================================================
    # RECOMMEND BUTTON
    # ==================================================

    same_genre_only = st.checkbox(
        "🎼 Recommend only from the same genre"
    )

    if st.button(
        "🎵 Find Similar Songs",
        use_container_width=True
    ):

        recommendations = get_recommendations(
            df,
            selected_song,
            number_of_recommendations
            same_genre_only
        )

        
        # --------------------------------------------------
        # DISPLAY RESULTS
        # --------------------------------------------------

        if recommendations.empty:

            st.warning(
                "No similar songs found."
            )

        else:

            st.success(
                f"🎧 Recommendations for **{selected_song}**"
            )


            for _, song in recommendations.iterrows():

                st.markdown(
                    f"""
                    <div class="song-card">

                    <h3>
                    🎵 {song['title']}
                    </h3>

                    <p>
                    <b>Artist:</b>
                    {song['artist']}
                    </p>

                    <p>
                    <b>Genre:</b>
                    {song['genre']}
                    </p>

                    <p>
                    <b>Year:</b>
                    {int(song['year'])}
                    </p>

                    <p>
                    <b>Similarity:</b>
                    {song['similarity']}%
                    </p>

                    </div>
                    """,
                    unsafe_allow_html=True
                )


            # --------------------------------------------------
            # RECOMMENDATION TABLE
            # --------------------------------------------------

            st.subheader(
                "📋 Recommendation Summary"
            )

            display_df = recommendations[
                [
                    "title",
                    "artist",
                    "genre",
                    "year",
                    "similarity"
                ]
            ].copy()


            display_df.columns = [
                "Song",
                "Artist",
                "Genre",
                "Year",
                "Similarity %"
            ]


            st.dataframe(
                display_df,
                use_container_width=True,
                hide_index=True
            )


# ==================================================
# DATASET SECTION
# ==================================================

st.divider()

st.subheader("📚 Explore Dataset")

st.write(
    f"Total songs in dataset: **{len(df)}**"
)

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)


# ==================================================
# PROJECT INFORMATION
# ==================================================

st.divider()

st.subheader("🧠 How TuneMatch Works")

st.write(
    """
    TuneMatch uses a content-based recommendation system.

    Each song is represented using five audio characteristics:

    • Danceability
    • Energy
    • Acousticness
    • Instrumentalness
    • Valence

    These features are standardized using Scikit-learn's
    StandardScaler and compared using cosine similarity.

    Songs with more similar feature patterns receive
    higher similarity scores.
    """
)
