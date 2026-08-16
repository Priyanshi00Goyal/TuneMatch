# 🎵 TuneMatch

<p align="center">

### 🎧 Your Personal Music Discovery Engine

A content-based music recommendation system that helps you discover songs based on **sound, mood, and musical characteristics.**

<br>

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Scikit Learn](https://img.shields.io/badge/Scikit--learn-ML-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualization-11557C?style=for-the-badge)

</p>

---

## 🌟 Overview

**TuneMatch** is a Python-based music recommendation application designed to make music discovery more personalized.

Instead of recommending songs randomly, TuneMatch analyzes the **musical characteristics** of songs and finds tracks with similar audio profiles.

The application combines:

- 🎧 Content-based recommendation
- 🎭 Mood-based discovery
- 🔎 Song & artist search
- 🎼 Genre filtering
- ❤️ Personal playlists
- 👤 Music personality analysis
- 📊 Music analytics
- 🧠 Explainable recommendations

All inside an interactive **Streamlit web application**.

---

# 🎬 What Can TuneMatch Do?

| Feature | Description |
|---|---|
| 🎧 Recommendations | Find songs similar to your selected track |
| 🎭 Mood Discovery | Discover songs according to your mood |
| 🔎 Search | Search songs and artists instantly |
| 🎼 Genre Filter | Explore music by genre |
| 📊 Sorting | Sort recommendations by similarity, energy, danceability, valence or year |
| ❤️ Playlist | Create and manage your personal playlist |
| 💾 Persistence | Save playlists locally |
| 👤 Music Profile | Analyze your personal music taste |
| 🧠 Explainability | Understand why a song was recommended |
| 📈 Analytics | Explore patterns in the music dataset |

---

# 🧠 How TuneMatch Works

TuneMatch follows a **content-based recommendation approach**.

Each song is represented using numerical audio characteristics.

### 🎵 Audio Features

```text
┌───────────────────────────────┐
│        Song Features          │
├───────────────────────────────┤
│ 💃 Danceability               │
│ ⚡ Energy                     │
│ 🎹 Acousticness               │
│ 🎼 Instrumentalness            │
│ 😊 Valence                    │
└───────────────────────────────┘
