import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from recommender import (
    load_data,
    get_recommendations,
    get_mood_recommendations
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

genres = [
    "All"
] + sorted(
    df["genre"].unique().tolist()
)

selected_genre = st.sidebar.selectbox(
    "🎼 Select Genre",
    genres
)


# --------------------------------------------------
# MOOD SELECTOR
# --------------------------------------------------

moods = [
    "None",
    "😌 Chill",
    "⚡ Energetic",
    "💃 Dance",
    "😊 Happy",
    "💔 Melancholy"
]

selected_mood = st.sidebar.selectbox(
    "🎭 Choose a Mood",
    moods
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
# FILTER DATA BY GENRE
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

st.subheader("🎶 Choose a Song")

if filtered_df.empty:

    st.warning(
        "No songs available for this genre."
    )

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
    # AUDIO FEATURES
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


    ax.set_ylim(
        0,
        1
    )


    ax.set_ylabel(
        "Value"
    )


    ax.set_title(
        f"Audio Features — {selected_song}"
    )


    plt.xticks(
        rotation=30
    )


    st.pyplot(fig)


    # ==================================================
    # SIMILAR SONG RECOMMENDATIONS
    # ==================================================

    st.divider()

    st.subheader(
        "🎧 Similar Songs"
    )


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
            number_of_recommendations,
            same_genre_only
        )


        if recommendations.empty:

            st.warning(
                "No similar songs found."
            )

        else:

            st.success(
                f"🎧 Recommendations for "
                f"**{selected_song}**"
            )


            # ------------------------------------------
            # SONG CARDS
            # ------------------------------------------

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


            # ------------------------------------------
            # RECOMMENDATION TABLE
            # ------------------------------------------

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
# MOOD-BASED RECOMMENDATIONS
# ==================================================

st.divider()

st.subheader(
    "🎭 Mood-Based Recommendations"
)


if selected_mood == "None":

    st.info(
        "Choose a mood from the sidebar "
        "to get mood-based recommendations."
    )


else:

    if st.button(
        f"🎵 Find {selected_mood} Songs",
        use_container_width=True
    ):

        mood_recommendations = (
            get_mood_recommendations(
                df,
                selected_mood,
                number_of_recommendations
            )
        )


        if mood_recommendations.empty:

            st.warning(
                "No mood recommendations found."
            )


        else:

            st.success(
                f"Songs matching the "
                f"{selected_mood} mood"
            )


            # ------------------------------------------
            # MOOD SONG CARDS
            # ------------------------------------------

            for _, song in (
                mood_recommendations.iterrows()
            ):

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
                    <b>Mood Match:</b>
                    {song['mood_match']}%
                    </p>

                    </div>
                    """,
                    unsafe_allow_html=True
                )


# ==================================================
# DATASET
# ==================================================

st.divider()

st.subheader(
    "📚 Explore Dataset"
)


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

st.subheader(
    "🧠 How TuneMatch Works"
)


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

    TuneMatch also considers genre and artist similarity
    when calculating recommendation scores.

    Mood recommendations are generated by analyzing
    characteristics such as energy, danceability,
    acousticness, and valence.
    """
)

# ==================================================
# MUSIC ANALYTICS DASHBOARD
# ==================================================

st.divider()

st.header("📊 Music Analytics Dashboard")

st.write(
    "Explore patterns and trends across the TuneMatch dataset."
)


# ==================================================
# DATASET STATISTICS
# ==================================================

st.subheader("📌 Dataset Overview")

total_songs = len(df)

total_artists = df["artist"].nunique()

total_genres = df["genre"].nunique()

average_energy = df["energy"].mean()

average_danceability = df["danceability"].mean()


col1, col2, col3, col4, col5 = st.columns(5)


with col1:

    st.metric(
        "🎵 Songs",
        total_songs
    )


with col2:

    st.metric(
        "🎤 Artists",
        total_artists
    )


with col3:

    st.metric(
        "🎼 Genres",
        total_genres
    )


with col4:

    st.metric(
        "⚡ Avg Energy",
        round(
            average_energy,
            2
        )
    )


with col5:

    st.metric(
        "💃 Avg Danceability",
        round(
            average_danceability,
            2
        )
    )


# ==================================================
# GENRE DISTRIBUTION
# ==================================================

st.subheader("🎼 Genre Distribution")


genre_counts = (
    df["genre"]
    .value_counts()
)


fig1, ax1 = plt.subplots()


ax1.pie(
    genre_counts.values,
    labels=genre_counts.index,
    autopct="%1.1f%%"
)


ax1.set_title(
    "Songs by Genre"
)


st.pyplot(fig1)


# ==================================================
# ENERGY BY GENRE
# ==================================================

st.subheader(
    "⚡ Average Energy by Genre"
)


energy_by_genre = (
    df.groupby("genre")["energy"]
    .mean()
    .sort_values(
        ascending=False
    )
)


fig2, ax2 = plt.subplots()


ax2.bar(
    energy_by_genre.index,
    energy_by_genre.values
)


ax2.set_ylabel(
    "Average Energy"
)


ax2.set_ylim(
    0,
    1
)


ax2.set_title(
    "Average Energy by Genre"
)


plt.xticks(
    rotation=30
)


st.pyplot(fig2)


# ==================================================
# DANCEABILITY BY GENRE
# ==================================================

st.subheader(
    "💃 Average Danceability by Genre"
)


danceability_by_genre = (
    df.groupby("genre")["danceability"]
    .mean()
    .sort_values(
        ascending=False
    )
)


fig3, ax3 = plt.subplots()


ax3.bar(
    danceability_by_genre.index,
    danceability_by_genre.values
)


ax3.set_ylabel(
    "Average Danceability"
)


ax3.set_ylim(
    0,
    1
)


ax3.set_title(
    "Average Danceability by Genre"
)


plt.xticks(
    rotation=30
)


st.pyplot(fig3)


# ==================================================
# VALENCE BY GENRE
# ==================================================

st.subheader(
    "😊 Average Valence by Genre"
)


valence_by_genre = (
    df.groupby("genre")["valence"]
    .mean()
    .sort_values(
        ascending=False
    )
)


fig4, ax4 = plt.subplots()


ax4.bar(
    valence_by_genre.index,
    valence_by_genre.values
)


ax4.set_ylabel(
    "Average Valence"
)


ax4.set_ylim(
    0,
    1
)


ax4.set_title(
    "Average Valence by Genre"
)


plt.xticks(
    rotation=30
)


st.pyplot(fig4)


# ==================================================
# RELEASE YEAR DISTRIBUTION
# ==================================================

st.subheader(
    "📅 Songs by Release Year"
)


year_counts = (
    df["year"]
    .value_counts()
    .sort_index()
)


fig5, ax5 = plt.subplots()


ax5.plot(
    year_counts.index,
    year_counts.values,
    marker="o"
)


ax5.set_xlabel(
    "Release Year"
)


ax5.set_ylabel(
    "Number of Songs"
)


ax5.set_title(
    "Songs in Dataset by Release Year"
)


st.pyplot(fig5)


# ==================================================
# TOP ENERGETIC SONGS
# ==================================================

st.subheader(
    "⚡ Most Energetic Songs"
)


top_energy = (
    df[
        [
            "title",
            "artist",
            "energy"
        ]
    ]
    .sort_values(
        by="energy",
        ascending=False
    )
    .head(5)
    .copy()
)


top_energy.columns = [
    "Song",
    "Artist",
    "Energy"
]


st.dataframe(
    top_energy,
    use_container_width=True,
    hide_index=True
)


# ==================================================
# TOP DANCEABLE SONGS
# ==================================================

st.subheader(
    "💃 Most Danceable Songs"
)


top_danceable = (
    df[
        [
            "title",
            "artist",
            "danceability"
        ]
    ]
    .sort_values(
        by="danceability",
        ascending=False
    )
    .head(5)
    .copy()
)


top_danceable.columns = [
    "Song",
    "Artist",
    "Danceability"
]


st.dataframe(
    top_danceable,
    use_container_width=True,
    hide_index=True
)
