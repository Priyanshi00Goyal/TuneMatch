
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
# DATA / FILE CONFIGURATION
# ==================================================

from pathlib import Path

# ==================================================
# DATA / FILE CONFIGURATION
# ==================================================

BASE_DIR = Path(__file__).resolve().parent

PLAYLIST_PATH = str(BASE_DIR / "playlist.json")

# Automatically find CSV file in the TuneMatch folder
csv_files = list(BASE_DIR.glob("*.csv"))

if not csv_files:
    st.error(
        "❌ No CSV dataset found!\n\n"
        f"Please put your dataset CSV file inside:\n"
        f"{BASE_DIR}"
    )
    st.stop()

DATA_PATH = str(csv_files[0])

# Load dataset
df = load_data(DATA_PATH)


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

    .stApp {
        background:
            radial-gradient(circle at 0% 0%,
                rgba(124, 58, 237, 0.22), transparent 25%),
            radial-gradient(circle at 100% 10%,
                rgba(59, 130, 246, 0.18), transparent 25%),
            linear-gradient(135deg, #070b16 0%, #0d1324 50%, #080d19 100%);
        color: #f8fafc;
    }

    .main .block-container {
        max-width: 1450px;
        padding-top: 2.5rem;
        padding-bottom: 5rem;
        padding-left: 3rem;
        padding-right: 3rem;
    }

    .main-title {
        font-size: 68px;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(
            90deg, #c084fc, #818cf8, #60a5fa, #c084fc
        );
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -3px;
        line-height: 1.1;
        margin-top: 10px;
        margin-bottom: 5px;
        filter: drop-shadow(0 0 25px rgba(139,92,246,0.25));
    }

    .subtitle {
        text-align: center;
        font-size: 18px;
        color: #94a3b8;
        letter-spacing: 1px;
        margin-bottom: 45px;
    }

    h1, h2, h3, h4 {
        color: #f8fafc !important;
    }

    h1 { font-weight: 850 !important; }
    h2 { font-weight: 800 !important; }
    h3 { font-weight: 750 !important; }

    div[data-baseweb="tab-list"] {
        gap: 8px;
        padding: 8px;
        background: rgba(15, 23, 42, 0.72);
        border: 1px solid rgba(148, 163, 184, 0.12);
        border-radius: 18px;
        margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.18);
    }

    button[data-baseweb="tab"] {
        color: #94a3b8 !important;
        font-size: 15px;
        font-weight: 700;
        border-radius: 12px;
        padding: 11px 18px;
        transition: all 0.25s ease;
    }

    button[data-baseweb="tab"]:hover {
        color: #ffffff !important;
        background: rgba(124,58,237,0.15);
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        color: #ffffff !important;
        background: linear-gradient(
            135deg,
            rgba(124,58,237,0.55),
            rgba(79,70,229,0.45)
        );
        box-shadow: 0 5px 20px rgba(124,58,237,0.25);
    }

    .feature-card {
        position: relative;
        padding: 30px;
        min-height: 210px;
        border-radius: 24px;
        background: linear-gradient(
            145deg,
            rgba(30,41,59,0.95),
            rgba(15,23,42,0.88)
        );
        border: 1px solid rgba(148,163,184,0.13);
        box-shadow: 0 15px 40px rgba(0,0,0,0.22);
        overflow: hidden;
        transition: all 0.3s ease;
    }

    .feature-card::before {
        content: "";
        position: absolute;
        top: -70px;
        right: -70px;
        width: 150px;
        height: 150px;
        background: radial-gradient(
            circle,
            rgba(139,92,246,0.25),
            transparent 70%
        );
    }

    .feature-card:hover {
        transform: translateY(-7px);
        border-color: rgba(167,139,250,0.45);
        box-shadow: 0 20px 50px rgba(124,58,237,0.20);
    }

    .feature-icon {
        width: 58px;
        height: 58px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 17px;
        font-size: 28px;
        background: linear-gradient(
            135deg,
            rgba(124,58,237,0.3),
            rgba(59,130,246,0.25)
        );
        border: 1px solid rgba(167,139,250,0.25);
        margin-bottom: 18px;
    }

    .feature-title {
        font-size: 21px;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 10px;
    }

    .feature-description {
        font-size: 14px;
        line-height: 1.7;
        color: #94a3b8;
    }

    .song-card {
        position: relative;
        padding: 25px 28px;
        margin-bottom: 18px;
        border-radius: 22px;
        background: linear-gradient(
            145deg,
            rgba(30,41,59,0.94),
            rgba(15,23,42,0.92)
        );
        border: 1px solid rgba(148,163,184,0.13);
        box-shadow: 0 12px 35px rgba(0,0,0,0.25);
        transition: all 0.25s ease;
    }

    .song-card::before {
        content: "";
        position: absolute;
        left: 0;
        top: 18px;
        bottom: 18px;
        width: 4px;
        border-radius: 10px;
        background: linear-gradient(180deg, #8b5cf6, #3b82f6);
    }

    .song-card:hover {
        transform: translateY(-4px);
        border-color: rgba(167,139,250,0.4);
        box-shadow: 0 18px 45px rgba(124,58,237,0.18);
    }

    .song-card h3 {
        margin-top: 0;
        color: #ffffff !important;
    }

    .song-card p {
        color: #cbd5e1;
        font-size: 14px;
        line-height: 1.7;
    }

    .song-card b {
        color: #a78bfa;
    }

    [data-testid="stMetric"] {
        background: linear-gradient(
            145deg,
            rgba(30,41,59,0.9),
            rgba(15,23,42,0.88)
        );
        border: 1px solid rgba(148,163,184,0.13);
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        transition: all 0.25s ease;
    }

    [data-testid="stMetric"]:hover {
        transform: translateY(-3px);
        border-color: rgba(167,139,250,0.4);
        box-shadow: 0 12px 35px rgba(124,58,237,0.15);
    }

    [data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
        font-weight: 600;
    }

    [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-weight: 850;
    }

    .stButton > button {
        min-height: 42px;
        border: none !important;
        border-radius: 13px !important;
        color: #ffffff !important;
        font-weight: 750 !important;
        background: linear-gradient(
            135deg,
            #7c3aed,
            #4f46e5
        ) !important;
        box-shadow: 0 6px 20px rgba(124,58,237,0.25);
        transition: all 0.25s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        background: linear-gradient(
            135deg,
            #8b5cf6,
            #6366f1
        ) !important;
        box-shadow: 0 10px 28px rgba(124,58,237,0.4);
    }

    div[data-baseweb="input"],
    div[data-baseweb="select"] > div {
        background: rgba(15,23,42,0.85) !important;
        border: 1px solid rgba(148,163,184,0.2) !important;
        border-radius: 13px !important;
    }

    input {
        color: #ffffff !important;
    }

    input::placeholder {
        color: #64748b !important;
    }

    div[data-baseweb="select"] span {
        color: #f8fafc !important;
    }

    div[data-testid="stSlider"] {
        padding-top: 10px;
        padding-bottom: 10px;
    }

    div[data-testid="stCheckbox"] label {
        color: #cbd5e1 !important;
        font-weight: 600;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            #070b16 0%,
            #0d1324 55%,
            #080d19 100%
        );
        border-right: 1px solid rgba(148,163,184,0.12);
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #ffffff !important;
    }

    [data-testid="stSidebar"] p {
        color: #94a3b8;
    }

    [data-testid="stSidebar"] [data-testid="stMetric"] {
        background: rgba(30,41,59,0.55);
        box-shadow: none;
    }

    [data-testid="stAlert"] {
        border-radius: 16px !important;
        border: 1px solid rgba(148,163,184,0.15);
        background: rgba(30,41,59,0.7);
    }

    [data-testid="stDataFrame"] {
        border-radius: 18px;
        overflow: hidden;
        border: 1px solid rgba(148,163,184,0.15);
        box-shadow: 0 10px 30px rgba(0,0,0,0.18);
    }

    .stDownloadButton > button {
        width: 100%;
        border-radius: 13px !important;
        border: 1px solid rgba(167,139,250,0.35) !important;
        background: rgba(124,58,237,0.15) !important;
        color: #ddd6fe !important;
        font-weight: 750 !important;
    }

    .stDownloadButton > button:hover {
        background: rgba(124,58,237,0.3) !important;
        border-color: #a78bfa !important;
    }

    hr {
        border: none;
        height: 1px;
        background: linear-gradient(
            90deg,
            transparent,
            rgba(148,163,184,0.25),
            transparent
        );
        margin: 32px 0;
    }

    [data-testid="stImage"] {
        border-radius: 18px;
    }

    ::-webkit-scrollbar {
        width: 8px;
    }

    ::-webkit-scrollbar-track {
        background: #070b16;
    }

    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #6d28d9, #3730a3);
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: #8b5cf6;
    }

    .footer {
        text-align: center;
        color: #64748b;
        font-size: 13px;
        margin-top: 60px;
        padding: 25px;
        border-top: 1px solid rgba(148,163,184,0.08);
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ==================================================
# FAVORITES / PLAYLIST
# ==================================================

if "favorites" not in st.session_state:
    st.session_state.favorites = load_playlist(PLAYLIST_PATH)


# ==================================================
# HEADER
# ==================================================

st.markdown(
    '<div class="main-title">🎵 TuneMatch</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Your personal music discovery engine.</div>',
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

st.sidebar.metric("🎵 Songs", len(df))
st.sidebar.metric("🎤 Artists", df["artist"].nunique())
st.sidebar.metric("🎼 Genres", df["genre"].nunique())

st.sidebar.divider()

st.sidebar.success("🟢 TuneMatch Engine Online")

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

    st.subheader("✨ What can TuneMatch do?")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">🎧</div>
                <div class="feature-title">Song Recommendations</div>
                <div class="feature-description">
                    Select a song and discover tracks with similar
                    musical characteristics.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">🎭</div>
                <div class="feature-title">Mood Discovery</div>
                <div class="feature-description">
                    Choose a mood and discover songs that match
                    your selected feeling.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">📊</div>
                <div class="feature-title">Music Analytics</div>
                <div class="feature-description">
                    Explore genres, energy, danceability and other
                    characteristics of your music dataset.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.divider()

    st.subheader("📚 Dataset Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Songs", len(df))

    with col2:
        st.metric("Artists", df["artist"].nunique())

    with col3:
        st.metric("Genres", df["genre"].nunique())

    with col4:
        st.metric(
            "Average Energy",
            round(df["energy"].mean(), 2)
        )

    st.divider()

    st.info(
        "💡 Go to the Recommendations tab to start discovering music."
    )


# ==================================================
# RECOMMENDATION TAB
# ==================================================

with recommendation_tab:

    st.header("🎧 Song Recommendations")

    genres = ["All"] + sorted(df["genre"].dropna().unique().tolist())

    selected_genre = st.selectbox(
        "🎼 Select Genre",
        genres
    )

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

    if selected_genre == "All":
        filtered_df = df.copy()
    else:
        filtered_df = df[
            df["genre"] == selected_genre
        ].copy()

    search_query = st.text_input(
        "🔎 Search Song or Artist",
        placeholder="Type a song title or artist name..."
    )

    if search_query:
        search_mask = (
            filtered_df["title"].astype(str).str.contains(
                search_query,
                case=False,
                na=False
            )
            |
            filtered_df["artist"].astype(str).str.contains(
                search_query,
                case=False,
                na=False
            )
        )

        search_results = filtered_df[search_mask]
    else:
        search_results = filtered_df

    if search_results.empty:

        st.warning("🔍 No songs or artists found.")

    else:

        selected_song = st.selectbox(
            "🎶 Choose a Song",
            search_results["title"].tolist()
        )

        selected_rows = df[df["title"] == selected_song]

        if selected_rows.empty:
            st.error("Selected song could not be found in the dataset.")
        else:

            selected_data = selected_rows.iloc[0]

            st.subheader("🎵 Selected Song")

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("Artist", selected_data["artist"])

            with col2:
                st.metric("Genre", selected_data["genre"])

            with col3:
                st.metric("Year", int(selected_data["year"]))

            with col4:
                st.metric(
                    "Energy",
                    round(selected_data["energy"], 2)
                )

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

            fig, ax = plt.subplots(figsize=(8, 4))

            ax.bar(features, values)
            ax.set_ylim(0, 1)
            ax.set_ylabel("Value")
            ax.set_title(selected_song)

            plt.xticks(rotation=30)
            plt.tight_layout()

            st.pyplot(fig)
            plt.close(fig)

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
                    50,
                    same_genre_only
                )

                if recommendations.empty:

                    st.warning("No similar songs found.")

                else:

                    sort_columns = {
                        "Similarity": "similarity",
                        "Energy": "energy",
                        "Danceability": "danceability",
                        "Valence": "valence",
                        "Year": "year"
                    }

                    sort_column = sort_columns[sort_option]

                    if sort_column in recommendations.columns:
                        recommendations = (
                            recommendations
                            .sort_values(
                                by=sort_column,
                                ascending=False
                            )
                            .head(number_of_recommendations)
                        )
                    else:
                        recommendations = recommendations.head(
                            number_of_recommendations
                        )

                    st.success(
                        f"🎧 Songs similar to **{selected_song}**"
                    )

                    for _, song in recommendations.iterrows():

                        explanation = explain_recommendation(
                            selected_data,
                            song
                        )

                        col1, col2 = st.columns([5, 1])

                        with col1:

                            similarity = song.get(
                                "similarity",
                                0
                            )

                            st.markdown(
                                f"""
                                <div class="song-card">

                                <h3>🎵 {song['title']}</h3>

                                <p>
                                <b>Artist:</b> {song['artist']}
                                </p>

                                <p>
                                <b>Genre:</b> {song['genre']}
                                </p>

                                <p>
                                <b>Year:</b> {int(song['year'])}
                                </p>

                                <p>
                                <b>Similarity:</b> {similarity}%
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

    mood_number_of_recommendations = st.slider(
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

        mood_recommendations = get_mood_recommendations(
            df,
            selected_mood,
            mood_number_of_recommendations
        )

        if mood_recommendations.empty:

            st.warning(
                "No songs found for this mood."
            )

        else:

            st.success(
                f"Songs matching {selected_mood}"
            )

            for _, song in mood_recommendations.iterrows():

                mood_match = song.get(
                    "mood_match",
                    0
                )

                st.markdown(
                    f"""
                    <div class="song-card">

                    <h3>🎵 {song['title']}</h3>

                    <p>
                    <b>Artist:</b> {song['artist']}
                    </p>

                    <p>
                    <b>Genre:</b> {song['genre']}
                    </p>

                    <p>
                    <b>Mood Match:</b> {mood_match}%
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
            f"You have {len(st.session_state.favorites)} "
            f"song(s) in your playlist."
        )

        for index, song in enumerate(
            st.session_state.favorites
        ):

            col1, col2 = st.columns([5, 1])

            with col1:

                st.markdown(
                    f"""
                    <div class="song-card">

                    <h3>🎵 {song['title']}</h3>

                    <p>
                    <b>Artist:</b> {song['artist']}
                    </p>

                    <p>
                    <b>Genre:</b> {song['genre']}
                    </p>

                    <p>
                    <b>Year:</b> {int(song['year'])}
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

                    st.session_state.favorites.pop(index)

                    save_playlist(
                        PLAYLIST_PATH,
                        st.session_state.favorites
                    )

                    st.rerun()

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

    if not st.session_state.favorites:

        st.info("❤️ Your playlist is empty.")

        st.write(
            "Add some songs from the Recommendations tab "
            "to generate your music profile."
        )

    else:

        playlist_df = pd.DataFrame(
            st.session_state.favorites
        )

        profile_df = df[
            df["title"].isin(
                playlist_df["title"]
            )
        ].copy()

        if profile_df.empty:

            st.warning(
                "Could not find playlist songs in the dataset."
            )

        else:

            favorite_genre = (
                profile_df["genre"]
                .value_counts()
                .idxmax()
            )

            average_energy = profile_df["energy"].mean()
            average_danceability = profile_df["danceability"].mean()
            average_acousticness = profile_df["acousticness"].mean()
            average_valence = profile_df["valence"].mean()

            st.subheader("🎵 Your Music Statistics")

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

            st.subheader("🧠 Your Music Personality")

            if (
                average_energy >= 0.7
                and average_danceability >= 0.7
            ):

                personality = (
                    "⚡ You enjoy energetic and danceable music."
                )

            elif average_energy >= 0.7:

                personality = (
                    "🔥 Your playlist has a high-energy vibe."
                )

            elif average_acousticness >= 0.6:

                personality = (
                    "🎹 You seem to enjoy acoustic and mellow sounds."
                )

            elif average_valence >= 0.7:

                personality = (
                    "😊 Your playlist has a positive and uplifting vibe."
                )

            elif average_valence <= 0.35:

                personality = (
                    "🌙 Your playlist leans toward calm and emotional music."
                )

            else:

                personality = (
                    "🎧 Your music taste is nicely balanced."
                )

            st.success(personality)

            st.subheader("📊 Your Audio Profile")

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

            fig, ax = plt.subplots(figsize=(8, 4))

            ax.bar(
                profile_features,
                profile_values
            )

            ax.set_ylim(0, 1)
            ax.set_ylabel("Average Value")
            ax.set_title("Your Music Characteristics")

            plt.xticks(rotation=20)
            plt.tight_layout()

            st.pyplot(fig)
            plt.close(fig)


# ==================================================
# ANALYTICS TAB
# ==================================================

with analytics_tab:

    st.header("📊 Music Analytics")

    st.write(
        "Explore the characteristics of the TuneMatch dataset."
    )

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("🎵 Songs", len(df))

    with col2:
        st.metric("🎤 Artists", df["artist"].nunique())

    with col3:
        st.metric("🎼 Genres", df["genre"].nunique())

    with col4:
        st.metric(
            "⚡ Avg Energy",
            round(df["energy"].mean(), 2)
        )

    with col5:
        st.metric(
            "💃 Avg Danceability",
            round(df["danceability"].mean(), 2)
        )

    st.divider()

    st.subheader("🎼 Genre Distribution")

    genre_counts = df["genre"].value_counts()

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.pie(
        genre_counts.values,
        labels=genre_counts.index,
        autopct="%1.1f%%"
    )

    ax.set_title("Songs by Genre")

    st.pyplot(fig)
    plt.close(fig)

    st.subheader("⚡ Average Energy by Genre")

    energy_by_genre = (
        df.groupby("genre")["energy"]
        .mean()
        .sort_values(ascending=False)
    )

    fig, ax = plt.subplots(figsize=(9, 5))

    ax.bar(
        energy_by_genre.index,
        energy_by_genre.values
    )

    ax.set_ylim(0, 1)
    ax.set_ylabel("Energy")

    plt.xticks(rotation=30)
    plt.tight_layout()

    st.pyplot(fig)
    plt.close(fig)

    st.subheader("💃 Average Danceability by Genre")

    danceability_by_genre = (
        df.groupby("genre")["danceability"]
        .mean()
        .sort_values(ascending=False)
    )

    fig, ax = plt.subplots(figsize=(9, 5))

    ax.bar(
        danceability_by_genre.index,
        danceability_by_genre.values
    )

    ax.set_ylim(0, 1)
    ax.set_ylabel("Danceability")

    plt.xticks(rotation=30)
    plt.tight_layout()

    st.pyplot(fig)
    plt.close(fig)

    st.subheader("😊 Average Valence by Genre")

    valence_by_genre = (
        df.groupby("genre")["valence"]
        .mean()
        .sort_values(ascending=False)
    )

    fig, ax = plt.subplots(figsize=(9, 5))

    ax.bar(
        valence_by_genre.index,
        valence_by_genre.values
    )

    ax.set_ylim(0, 1)
    ax.set_ylabel("Valence")

    plt.xticks(rotation=30)
    plt.tight_layout()

    st.pyplot(fig)
    plt.close(fig)

    st.subheader("📅 Songs by Release Year")

    year_counts = (
        df["year"]
        .value_counts()
        .sort_index()
    )

    fig, ax = plt.subplots(figsize=(9, 5))

    ax.plot(
        year_counts.index,
        year_counts.values,
        marker="o"
    )

    ax.set_xlabel("Year")
    ax.set_ylabel("Number of Songs")

    plt.tight_layout()

    st.pyplot(fig)
    plt.close(fig)

    st.subheader("⚡ Most Energetic Songs")

    top_energy = (
        df[["title", "artist", "energy"]]
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

    st.subheader("💃 Most Danceable Songs")

    top_danceable = (
        df[["title", "artist", "danceability"]]
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


# ==================================================
# FOOTER
# ==================================================

st.markdown(
    """
    <div class="footer">
        🎵 TuneMatch · Content-Based Music Recommendation System
    </div>
    """,
    unsafe_allow_html=True
)
