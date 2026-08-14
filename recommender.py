import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity


FEATURES = [
    "danceability",
    "energy",
    "acousticness",
    "instrumentalness",
    "valence"
]


def load_data(file_path):
    """Load song data from CSV."""
    return pd.read_csv(file_path)


def prepare_features(df):
    """Prepare numerical song features for similarity calculation."""

    scaler = StandardScaler()

    feature_matrix = scaler.fit_transform(df[FEATURES])

    return feature_matrix


def get_recommendations(df, song_title, number_of_recommendations=5):
    """Return songs that are musically similar to the selected song."""

    feature_matrix = prepare_features(df)

    similarity_matrix = cosine_similarity(feature_matrix)

    # Find selected song
    matches = df.index[
        df["title"].str.lower() == song_title.lower()
    ].tolist()

    if not matches:
        return pd.DataFrame()

    song_index = matches[0]

    similarity_scores = list(
        enumerate(similarity_matrix[song_index])
    )

    # Sort by similarity score
    similarity_scores = sorted(
        similarity_scores,
        key=lambda x: x[1],
        reverse=True
    )

    # Remove the selected song itself
    similarity_scores = [
        item for item in similarity_scores
        if item[0] != song_index
    ]

    top_songs = similarity_scores[:number_of_recommendations]

    recommended_indices = [item[0] for item in top_songs]
    recommended_scores = [item[1] for item in top_songs]

    recommendations = df.iloc[recommended_indices].copy()

    recommendations["similarity"] = recommended_scores

    recommendations["similarity"] = (
        recommendations["similarity"] * 100
    ).round(2)

    return recommendations
