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
