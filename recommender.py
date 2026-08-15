import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity


# Audio features used by the recommendation engine
AUDIO_FEATURES = [
    "danceability",
    "energy",
    "acousticness",
    "instrumentalness",
    "valence"
]


def load_data(file_path):
    """Load songs from CSV."""

    return pd.read_csv(file_path)


def prepare_audio_features(df):
    """Standardize audio features."""

    scaler = StandardScaler()

    features = scaler.fit_transform(
        df[AUDIO_FEATURES]
    )

    return features


def get_recommendations(
    df,
    song_title,
    number_of_recommendations=5,
    same_genre_only=False
):
    """
    Recommend songs based on audio similarity,
    genre and artist.
    """

    # ------------------------------------------
    # Find selected song
    # ------------------------------------------

    matches = df.index[
        df["title"].str.lower()
        == song_title.lower()
    ].tolist()

    if not matches:
        return pd.DataFrame()

    song_index = matches[0]


    # ------------------------------------------
    # Calculate audio similarity
    # ------------------------------------------

    feature_matrix = prepare_audio_features(df)

    similarity_matrix = cosine_similarity(
        feature_matrix
    )

    audio_scores = similarity_matrix[
        song_index
    ]


    # ------------------------------------------
    # Create recommendation dataframe
    # ------------------------------------------

    recommendations = df.copy()

    recommendations["audio_similarity"] = (
        audio_scores
    )


    # ------------------------------------------
    # Genre similarity
    # ------------------------------------------

    selected_genre = df.loc[
        song_index,
        "genre"
    ]

    recommendations["genre_score"] = (
        recommendations["genre"]
        == selected_genre
    ).astype(float)


    # ------------------------------------------
    # Artist similarity
    # ------------------------------------------

    selected_artist = df.loc[
        song_index,
        "artist"
    ]

    recommendations["artist_score"] = (
        recommendations["artist"]
        == selected_artist
    ).astype(float)


    # ------------------------------------------
    # Combined recommendation score
    # ------------------------------------------

    recommendations["score"] = (

        recommendations["audio_similarity"] * 0.70

        + recommendations["genre_score"] * 0.20

        + recommendations["artist_score"] * 0.10

    )


    # ------------------------------------------
    # Remove selected song
    # ------------------------------------------

    recommendations = recommendations[
        recommendations.index != song_index
    ]


    # ------------------------------------------
    # Same genre filter
    # ------------------------------------------

    if same_genre_only:

        recommendations = recommendations[
            recommendations["genre"]
            == selected_genre
        ]


    # ------------------------------------------
    # Sort recommendations
    # ------------------------------------------

    recommendations = recommendations.sort_values(
        by="score",
        ascending=False
    )


    # ------------------------------------------
    # Get top recommendations
    # ------------------------------------------

    recommendations = recommendations.head(
        number_of_recommendations
    )


    # ------------------------------------------
    # Convert score to percentage
    # ------------------------------------------

    recommendations["similarity"] = (
        recommendations["score"] * 100
    ).clip(0, 100).round(2)


    return recommendations
