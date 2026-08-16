import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from recommender import (
    load_data,
    get_recommendations,
    get_mood_recommendations,
    load_playlist,
    save_playlist,
    explain_recommendation
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

    /* Main background */
    .stApp {
        background: linear-gradient(
            135deg,
            #f8f9ff 0%,
            #eef1ff 100%
        );
    }

    /* Main title */
    .main-title {
        font-size: 58px;
        font-weight: 800;
        text-align: center;
        margin-top: 10px;
        margin-bottom: 5px;
    }

    /* Subtitle */
    .subtitle {
        text-align: center;
        font-size: 20px;
        margin-bottom: 35px;
        opacity: 0.75;
    }

    /* Song cards */
    .song-card {
        padding: 22px;
        border-radius: 18px;
        border: 1px solid #dddddd;
        margin-bottom: 15px;
        background: rgba(255, 255, 255, 0.85);
        box-shadow: 0px 5px 15px rgba(0,0,0,0.06);
        transition: 0.2s;
    }

    .song-card:hover {
        transform: translateY(-2px);
        box-shadow: 0px 8px 20px rgba(0,0,0,0.10);
    }

    /* Section titles */
    .section-title {
        font-size: 28px;
        font-weight: 700;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 12px;
        font-weight: 600;
        padding: 8px 18px;
    }

    /* Metrics */
    [data-testid="stMetric"] {
        background: rgba(255,255,255,0.75);
        padding: 15px;
        border-radius: 15px;
        border: 1px solid #dddddd;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: rgba(255,255,255,0.9);
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ==================================================
# LOAD DATA
# ==================================================

DATA_PATH = "data/songs.csv"
PLAYLIST_PATH = "data/playlist.csv"

df = load_data(DATA_PATH)


# ==================================================
# FAVORITES / PLAYLIST
# ==================================================

if "favorites" not in st.session_state:

    st.session_state.favorites = load_playlist(
        PLAYLIST_PATH
    )


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

st.sidebar.divider()

st.sidebar.success(
    "🟢 TuneMatch Engine Online"
)

st.sidebar.caption(
    "Content-based recommendation system"
)


# ==================================================
# NAVIGATION
# ==================================================

home_tab, recommendation_tab, mood_tab, playlist_tab, profile_tab, analytics_tab = st.tabs(
    [
        "🏠 Home",
        "🎧 Recommendations",
        "🎭 Mood",
        "❤️ My Playlist",
        "👤 My Profile",
        "📊 Analytics"
    ]
)


# ==================================================
# HOME TAB
# ==================================================

with home_tab:

    st.header("🏠 Welcome to TuneMatch")

    st.info(
        "🎵 Discover music based on sound, mood and your personal taste."
    )

    st.write(
        """
        TuneMatch is an intelligent content-based music discovery
        system that analyzes audio characteristics such as energy,
        danceability, acousticness and valence to recommend songs
        you'll love.
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
    sort_option = st.selectbox(
        "📊 Sort Recommendations By",
        [
            "Similarity",
            "Energy",
            "Danceability",
            "Valence",
            "Year"
        ]
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
    # SEARCH SONGS / ARTISTS
    # ----------------------------------------------

    search_query = st.text_input(
        "🔎 Search Song or Artist",
        placeholder="Type a song title or artist name..."
    )


    if search_query:

        search_mask = (
            filtered_df["title"]
            .str.contains(
                search_query,
                case=False,
                na=False
            )
            |
            filtered_df["artist"]
            .str.contains(
                search_query,
                case=False,
                na=False
            )
        )

        search_results = filtered_df[
            search_mask
        ]

    else:

        search_results = filtered_df


    # ----------------------------------------------
    # CHECK SEARCH RESULTS
    # ----------------------------------------------

    if search_results.empty:

        st.warning(
            "🔍 No songs or artists found."
        )

        st.stop()


    # ----------------------------------------------
    # SONG SELECTOR
    # ----------------------------------------------

    selected_song = st.selectbox(
        "🎶 Choose a Song",
        search_results["title"].tolist()
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
    weights = {
        "danceability": 1.2,
        "energy": 1.2,
        "acousticness": 1.0,
        "instrumentalness": 0.8,
        "valence": 1.1
    }

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
    # RECOMMEND BUTTON
    # ----------------------------------------------

    if st.button(
        "🎵 Find Similar Songs",
        use_container_width=True
    ):

        # ------------------------------------------
        # GET RECOMMENDATIONS
        # ------------------------------------------

        recommendations = get_recommendations(
            df,
            selected_song,
            50,
            same_genre_only
        )

        # ------------------------------------------
        # CHECK RESULTS
        # ------------------------------------------

        if recommendations.empty:

            st.warning(
                "No similar songs found."
            )

        else:

            # --------------------------------------
            # SORT RECOMMENDATIONS
            # --------------------------------------

            sort_columns = {
                "Similarity": "similarity",
                "Energy": "energy",
                "Danceability": "danceability",
                "Valence": "valence",
                "Year": "year"
            }

            sort_column = sort_columns[sort_option]

            recommendations = (
                recommendations
                .sort_values(
                    by=sort_column,
                    ascending=False
                )
                .head(
                    number_of_recommendations
                )
            )

            # --------------------------------------
            # DISPLAY RESULTS
            # --------------------------------------

            st.success(
                f"🎧 Songs similar to **{selected_song}**"
            )

            for _, song in recommendations.iterrows():
                explanation = explain_recommendation(
                selected_data,
                song
            )

                col1, col2 = st.columns([5, 1])

                # ----------------------------------
                # SONG CARD
                # ----------------------------------

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

                        <p>
                        <b>Similarity:</b>
                        {song['similarity']}%
                        </p>

                        <p>
                        <b>Energy:</b>
                        {round(song['energy'], 2)}
                        </p>

                        <p>
                        <b>Danceability:</b>
                        {round(song['danceability'], 2)}
                        </p>

                        <p>
                        <b>🧠 Why this song?</b>
                        {explanation}
                        </p>

                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                # ----------------------------------
                # ADD TO PLAYLIST
                # ----------------------------------

                with col2:

                    if st.button(
                        "❤️ Add",
                        key=f"favorite_{song['title']}"
                    ):

                        song_data = {
                            "title": song["title"],
                            "artist": song["artist"],
                            "genre": song["genre"],
                            "year": song["year"]
                        }

                        existing_titles = [
                            item["title"]
                            for item in st.session_state.favorites
                        ]

                        if song["title"] not in existing_titles:

                            st.session_state.favorites.append(
                                song_data
                            )

                            save_playlist(
                                PLAYLIST_PATH,
                                st.session_state.favorites
                            )

                            st.success(
                                f"❤️ {song['title']} added!"
                            )

                        else:

                            st.info(
                                "This song is already "
                                "in your playlist."
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
            explanation = explain_recommendation(
                selected_data,
                song
            )

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

                    save_playlist(  
                        PLAYLIST_PATH,
                        st.session_state.favorites
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
# PROFILE TAB
# ==================================================

with profile_tab:

    st.header("👤 My Music Profile")

    st.write(
        "Discover what your playlist says about your music taste."
    )

    # ----------------------------------------------
    # CHECK PLAYLIST
    # ----------------------------------------------

    if not st.session_state.favorites:

        st.info(
            "❤️ Your playlist is empty."
        )

        st.write(
            "Add some songs from the Recommendations tab "
            "to generate your music profile."
        )

    else:

        # ------------------------------------------
        # CONVERT PLAYLIST TO DATAFRAME
        # ------------------------------------------

        playlist_df = pd.DataFrame(
            st.session_state.favorites
        )

        # ------------------------------------------
        # MATCH PLAYLIST WITH DATASET
        # ------------------------------------------

        profile_df = df[
            df["title"].isin(
                playlist_df["title"]
            )
        ].copy()

        if profile_df.empty:

            st.warning(
                "Could not find playlist songs "
                "in the dataset."
            )

        else:

            # --------------------------------------
            # PROFILE METRICS
            # --------------------------------------

            favorite_genre = (
                profile_df["genre"]
                .value_counts()
                .idxmax()
            )

            average_energy = (
                profile_df["energy"].mean()
            )

            average_danceability = (
                profile_df["danceability"].mean()
            )

            average_acousticness = (
                profile_df["acousticness"].mean()
            )

            average_valence = (
                profile_df["valence"].mean()
            )

            # --------------------------------------
            # DISPLAY METRICS
            # --------------------------------------

            st.subheader(
                "🎵 Your Music Statistics"
            )

            col1, col2, col3, col4, col5 = st.columns(5)

            with col1:

                st.metric(
                    "🎼 Favorite Genre",
                    favorite_genre
                )

            with col2:

                st.metric(
                    "⚡ Avg Energy",
                    f"{average_energy:.2f}"
                )

            with col3:

                st.metric(
                    "💃 Danceability",
                    f"{average_danceability:.2f}"
                )

            with col4:

                st.metric(
                    "🎹 Acousticness",
                    f"{average_acousticness:.2f}"
                )

            with col5:

                st.metric(
                    "😊 Valence",
                    f"{average_valence:.2f}"
                )

            st.divider()

            # --------------------------------------
            # MUSIC PERSONALITY
            # --------------------------------------

            st.subheader(
                "🧠 Your Music Personality"
            )

            if (
                average_energy >= 0.7
                and average_danceability >= 0.7
            ):

                personality = (
                    "⚡ You enjoy energetic and "
                    "danceable music."
                )

            elif average_energy >= 0.7:

                personality = (
                    "🔥 Your playlist has a "
                    "high-energy vibe."
                )

            elif average_acousticness >= 0.6:

                personality = (
                    "🎹 You seem to enjoy "
                    "acoustic and mellow sounds."
                )

            elif average_valence >= 0.7:

                personality = (
                    "😊 Your playlist has a "
                    "positive and uplifting vibe."
                )

            elif average_valence <= 0.35:

                personality = (
                    "🌙 Your playlist leans toward "
                    "calm and emotional music."
                )

            else:

                personality = (
                    "🎧 Your music taste is "
                    "nicely balanced."
                )

            st.success(
                personality
            )

            # --------------------------------------
            # AUDIO PROFILE CHART
            # --------------------------------------

            st.subheader(
                "📊 Your Audio Profile"
            )

            profile_features = [
                "Energy",
                "Danceability",
                "Acousticness",
                "Valence"
            ]

            profile_values = [
                average_energy,
                average_danceability,
                average_acousticness,
                average_valence
            ]

            fig, ax = plt.subplots()

            ax.bar(
                profile_features,
                profile_values
            )

            ax.set_ylim(
                0,
                1
            )

            ax.set_ylabel(
                "Average Value"
            )

            ax.set_title(
                "Your Music Characteristics"
            )

            plt.xticks(
                rotation=20
            )

            st.pyplot(fig)

        
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
