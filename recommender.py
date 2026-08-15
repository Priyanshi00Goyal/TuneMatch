import pandas as pd

from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity


# ==================================================
# LOAD DATA
# ==================================================

def load_data(path):
    """
    Load the songs dataset from a CSV file.
    """

    df = pd.read_csv(path)

    return df


# ==================================================
# SIMILAR SONG RECOMMENDATIONS
# ==================================================

def get_recommendations(
    df,
    selected_song,
    number_of_recommendations=5,
    same_genre_only=False
):
    """
    Recommend songs similar to the selected song
    using audio features and cosine similarity.
    """

    data = df.copy()

    # ----------------------------------------------
    # Audio features
    # ----------------------------------------------

    features = [
        "danceability",
        "energy",
        "acousticness",
        "instrumentalness",
        "valence"
    ]

    # ----------------------------------------------
    # Check selected song
    # ----------------------------------------------

    if selected_song not in data["title"].values:
        return pd.DataFrame()

    # ----------------------------------------------
    # Standardize features
    # ----------------------------------------------

    scaler = StandardScaler()

    feature_matrix = scaler.fit_transform(
        data[features]
    )

    # ----------------------------------------------
    # Calculate cosine similarity
    # ----------------------------------------------

    similarity_matrix = cosine_similarity(
        feature_matrix
    )

    # ----------------------------------------------
    # Find selected song index
    # ----------------------------------------------

    selected_index = data[
        data["title"] == selected_song
    ].index[0]

    # Because DataFrame indexes may not start from 0,
    # convert the actual index to positional index.

    selected_position = data.index.get_loc(
        selected_index
    )

    similarity_scores = similarity_matrix[
        selected_position
    ]

    # ----------------------------------------------
    # Add similarity scores
    # ----------------------------------------------

    data["similarity"] = (
        similarity_scores * 100
    )

    # ----------------------------------------------
    # Remove selected song
    # ----------------------------------------------

    recommendations = data[
        data["title"] != selected_song
    ].copy()

    # ----------------------------------------------
    # Same genre filter
    # ----------------------------------------------

    if same_genre_only:

        selected_genre = data.loc[
            selected_index,
            "genre"
        ]

        recommendations = recommendations[
            recommendations["genre"] == selected_genre
        ]

    # ----------------------------------------------
    # Sort by similarity
    # ----------------------------------------------

    recommendations = recommendations.sort_values(
        by="similarity",
        ascending=False
    )

    # ----------------------------------------------
    # Number of recommendations
    # ----------------------------------------------

    recommendations = recommendations.head(
        number_of_recommendations
    )

    # ----------------------------------------------
    # Round similarity
    # ----------------------------------------------

    recommendations["similarity"] = (
        recommendations["similarity"]
        .round(2)
    )

    return recommendations


# ==================================================
# MOOD SCORE
# ==================================================

def calculate_mood_score(row, mood):
    """
    Calculate how well a song matches a selected mood.
    """

    danceability = row["danceability"]
    energy = row["energy"]
    acousticness = row["acousticness"]
    valence = row["valence"]

    if mood == "😌 Chill":

        return (
            acousticness * 0.5
            + (1 - energy) * 0.3
            + (1 - danceability) * 0.2
        )

    elif mood == "⚡ Energetic":

        return (
            energy * 0.6
            + danceability * 0.3
            + valence * 0.1
        )

    elif mood == "💃 Dance":

        return (
            danceability * 0.6
            + energy * 0.3
            + valence * 0.1
        )

    elif mood == "😊 Happy":

        return (
            valence * 0.6
            + energy * 0.2
            + danceability * 0.2
        )

    elif mood == "💔 Melancholy":

        return (
            (1 - valence) * 0.5
            + (1 - energy) * 0.3
            + acousticness * 0.2
        )

    return 0


# ==================================================
# MOOD RECOMMENDATIONS
# ==================================================

def get_mood_recommendations(
    df,
    mood,
    number_of_recommendations=5
):
    """
    Recommend songs based on mood.
    """

    recommendations = df.copy()

    recommendations["mood_score"] = (
        recommendations.apply(
            lambda row:
            calculate_mood_score(
                row,
                mood
            ),
            axis=1
        )
    )

    recommendations = recommendations.sort_values(
        by="mood_score",
        ascending=False
    )

    recommendations = recommendations.head(
        number_of_recommendations
    )

    recommendations["mood_match"] = (
        recommendations["mood_score"] * 100
    ).round(2)

    return recommendations
