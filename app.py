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
        font-size: 52px;
        font-weight: 800;
        text-align: center;
        margin-bottom: 0px;
    }

    .subtitle {
        text-align: center;
        font-size: 20px;
        margin-bottom: 30px;
    }

    .song-card {
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #dddddd;
        margin-bottom: 15px;
    }

    .section-title {
        font-size: 28px;
        font-weight: 700;
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
# FAVORITES / PLAYLIST
# ==================================================

if "favorites" not in st.session_state:
    st.session_state.favorites = []


# ==================================================
# HEADER
# ==================================================

st.markdown(
    '<div class="main-title">🎵 TuneMatch</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Your personal music discovery engine.'
    '</div>',
    unsafe_allow_html=True
)


# ==================================================
# SIDEBAR
# ==================================================

st.sidebar.title("🎧 TuneMatch")

st.sidebar.write(
    "Discover songs based on your musical taste."
)

st.sidebar.divider()

st.sidebar.metric(
    "🎵 Songs",
    len(df)
)

st.sidebar.metric(
    "🎤 Artists",
    df["artist"].nunique()
)

st.sidebar.metric(
    "🎼 Genres",
    df["genre"].nunique()
)


# ==================================================
# NAVIGATION
# ==================================================

home_tab, recommendation_tab, mood_tab, playlist_tab, analytics_tab = st.tabs(
    [
        "🏠 Home",
        "🎧 Recommendations",
        "🎭 Mood",
        "❤️ My Playlist",
        "📊 Analytics"
    ]
)


# ==================================================
# HOME TAB
# ==================================================

with home_tab:

    st.header("🏠 Welcome to TuneMatch")

    st.write(
        """
        TuneMatch is a content-based music recommendation
        system that analyzes musical characteristics to
        discover songs that sound similar.
        """
    )

    st.divider()

    # ----------------------------------------------
    # PROJECT FEATURES
    # ----------------------------------------------

    st.subheader("✨ What can TuneMatch do?")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            """
            ### 🎧 Song Recommendations

            Select a song and discover
            tracks with similar musical
            characteristics.
            """
        )

    with col2:

        st.markdown(
            """
            ### 🎭 Mood Discovery

            Choose a mood and discover
            songs that match your
            selected feeling.
            """
        )

    with col3:

        st.markdown(
            """
            ### 📊 Music Analytics

            Explore genres, energy,
            danceability and other
            characteristics.
            """
        )

    st.divider()

    # ----------------------------------------------
    # DATASET OVERVIEW
    # ----------------------------------------------

    st.subheader("📚 Dataset Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Songs",
            len(df)
        )

    with col2:

        st.metric(
            "Artists",
            df["artist"].nunique()
        )

    with col3:

        st.metric(
            "Genres",
            df["genre"].nunique()
        )

    with col4:

        st.metric(
            "Average Energy",
            round(
                df["energy"].mean(),
                2
            )
        )

    st.divider()

    st.info(
        "💡 Go to the Recommendations tab "
        "to start discovering music."
    )


# ==================================================
# RECOMMENDATION TAB
# ==================================================

with recommendation_tab:

    st.header("🎧 Song Recommendations")

    # ----------------------------------------------
    # GENRE
    # ----------------------------------------------

    genres = [
        "All"
    ] + sorted(
        df["genre"].unique().tolist()
    )

    selected_genre = st.selectbox(
        "🎼 Select Genre",
        genres
    )


    # ----------------------------------------------
    # NUMBER OF RECOMMENDATIONS
    # ----------------------------------------------

    number_of_recommendations = st.slider(
        "🎵 Number of Recommendations",
        min_value=1,
        max_value=10,
        value=5
    )


    # ----------------------------------------------
    # FILTER DATA
    # ----------------------------------------------

    if selected_genre == "All":

        filtered_df = df.copy()

    else:

        filtered_df = df[
            df["genre"] == selected_genre
        ].copy()


    # ----------------------------------------------
    # SONG SELECTOR
    # ----------------------------------------------

    selected_song = st.selectbox(
        "🎶 Choose a Song",
        filtered_df["title"].tolist()
    )


    selected_data = df[
        df["title"] == selected_song
    ].iloc[0]


    # ----------------------------------------------
    # SONG INFORMATION
    # ----------------------------------------------

    st.subheader("🎵 Selected Song")

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
            round(
                selected_data["energy"],
                2
            )
        )


    # ----------------------------------------------
    # AUDIO FEATURES
    # ----------------------------------------------

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
        selected_song
    )

    plt.xticks(
        rotation=30
    )

    st.pyplot(fig)


    # ----------------------------------------------
    # SAME GENRE
    # ----------------------------------------------

    same_genre_only = st.checkbox(
        "🎼 Recommend only from the same genre"
    )


    # ----------------------------------------------
    # RECOMMEND
    # ----------------------------------------------

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
                "No recommendations found."
            )

        else:

            st.success(
                f"🎧 Songs similar to "
                f"**{selected_song}**"
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
                    <b>Similarity:</b>
                    {song['similarity']}%
                    </p>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

    if st.button(
        f"❤️ Add {song['title']}",
        key=f"favorite_{song['title']}"
    ):

        song_data = {
            "title": song["title"],
            "artist": song["artist"],
            "genre": song["genre"],
            "year": song["year"]
        }

        # Avoid duplicates
        if song["title"] not in [
            item["title"]
            for item in st.session_state.favorites
        ]:

            st.session_state.favorites.append(
                song_data
            )

            st.success(
                f"❤️ {song['title']} added to your playlist!"
            )

        else:

            st.info(
                "This song is already in your playlist."
            )

# ==================================================
# MOOD TAB
# ==================================================

with mood_tab:

    st.header("🎭 Mood-Based Discovery")

    st.write(
        "What kind of music are you in the mood for?"
    )


    moods = [
        "😌 Chill",
        "⚡ Energetic",
        "💃 Dance",
        "😊 Happy",
        "💔 Melancholy"
    ]


    selected_mood = st.selectbox(
        "Choose your mood",
        moods
    )


    number_of_recommendations = st.slider(
        "Number of songs",
        min_value=1,
        max_value=10,
        value=5,
        key="mood_slider"
    )


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


        st.success(
            f"Songs matching "
            f"{selected_mood}"
        )


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
# PLAYLIST TAB
# ==================================================

with playlist_tab:

    st.header("❤️ My Playlist")

    if not st.session_state.favorites:

        st.info(
            "Your playlist is empty. "
            "Go to Recommendations and add some songs! 🎵"
        )

    else:

        st.success(
            f"You have "
            f"{len(st.session_state.favorites)} "
            f"song(s) in your playlist."
        )

        # ------------------------------------------
        # DISPLAY PLAYLIST
        # ------------------------------------------

        for index, song in enumerate(
            st.session_state.favorites
        ):

            col1, col2 = st.columns(
                [5, 1]
            )

            with col1:

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

                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with col2:

                if st.button(
                    "🗑️ Remove",
                    key=f"remove_{index}"
                ):

                    st.session_state.favorites.pop(
                        index
                    )

                    st.rerun()

        # ------------------------------------------
        # EXPORT PLAYLIST
        # ------------------------------------------

        st.divider()

        playlist_df = pd.DataFrame(
            st.session_state.favorites
        )

        csv_data = playlist_df.to_csv(
            index=False
        )

        st.download_button(
            label="💾 Download Playlist as CSV",
            data=csv_data,
            file_name="tunematch_playlist.csv",
            mime="text/csv",
            use_container_width=True
        )

        
# ==================================================
# ANALYTICS TAB
# ==================================================

with analytics_tab:

    st.header("📊 Music Analytics")

    st.write(
        "Explore the characteristics of the TuneMatch dataset."
    )


    # ----------------------------------------------
    # OVERVIEW
    # ----------------------------------------------

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:

        st.metric(
            "🎵 Songs",
            len(df)
        )

    with col2:

        st.metric(
            "🎤 Artists",
            df["artist"].nunique()
        )

    with col3:

        st.metric(
            "🎼 Genres",
            df["genre"].nunique()
        )

    with col4:

        st.metric(
            "⚡ Avg Energy",
            round(
                df["energy"].mean(),
                2
            )
        )

    with col5:

        st.metric(
            "💃 Avg Danceability",
            round(
                df["danceability"].mean(),
                2
            )
        )


    st.divider()


    # ----------------------------------------------
    # GENRE DISTRIBUTION
    # ----------------------------------------------

    st.subheader(
        "🎼 Genre Distribution"
    )


    genre_counts = (
        df["genre"]
        .value_counts()
    )


    fig, ax = plt.subplots()

    ax.pie(
        genre_counts.values,
        labels=genre_counts.index,
        autopct="%1.1f%%"
    )

    ax.set_title(
        "Songs by Genre"
    )

    st.pyplot(fig)


    # ----------------------------------------------
    # ENERGY BY GENRE
    # ----------------------------------------------

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


    fig, ax = plt.subplots()

    ax.bar(
        energy_by_genre.index,
        energy_by_genre.values
    )

    ax.set_ylim(
        0,
        1
    )

    ax.set_ylabel(
        "Energy"
    )

    plt.xticks(
        rotation=30
    )

    st.pyplot(fig)


    # ----------------------------------------------
    # DANCEABILITY BY GENRE
    # ----------------------------------------------

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


    fig, ax = plt.subplots()

    ax.bar(
        danceability_by_genre.index,
        danceability_by_genre.values
    )

    ax.set_ylim(
        0,
        1
    )

    ax.set_ylabel(
        "Danceability"
    )

    plt.xticks(
        rotation=30
    )

    st.pyplot(fig)


    # ----------------------------------------------
    # VALENCE BY GENRE
    # ----------------------------------------------

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


    fig, ax = plt.subplots()

    ax.bar(
        valence_by_genre.index,
        valence_by_genre.values
    )

    ax.set_ylim(
        0,
        1
    )

    ax.set_ylabel(
        "Valence"

    )

    plt.xticks(
        rotation=30
    )

    st.pyplot(fig)


    # ----------------------------------------------
    # RELEASE YEARS
    # ----------------------------------------------

    st.subheader(
        "📅 Songs by Release Year"
    )


    year_counts = (
        df["year"]
        .value_counts()
        .sort_index()
    )


    fig, ax = plt.subplots()

    ax.plot(
        year_counts.index,
        year_counts.values,
        marker="o"
    )

    ax.set_xlabel(
        "Year"
    )

    ax.set_ylabel(
        "Number of Songs"
    )

    st.pyplot(fig)


    # ----------------------------------------------
    # TOP ENERGY SONGS
    # ----------------------------------------------

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


    # ----------------------------------------------
    # TOP DANCEABLE SONGS
    # ----------------------------------------------

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
