# 🎵 TuneMatch — Personal Music Discovery Engine

<p align="center">

  <img src="https://img.shields.io/badge/Python-3.13-blue?style=for-the-badge&logo=python" alt="Python">

  <img src="https://img.shields.io/badge/Streamlit-App-red?style=for-the-badge&logo=streamlit" alt="Streamlit">

  <img src="https://img.shields.io/badge/Pandas-Data%20Analysis-150458?style=for-the-badge&logo=pandas" alt="Pandas">

  <img src="https://img.shields.io/badge/Matplotlib-Visualization-11557c?style=for-the-badge&logo=matplotlib" alt="Matplotlib">

</p>

<p align="center">

  <strong>🎧 Discover music that matches your taste, mood, and listening personality.</strong>

</p>

<p align="center">

  <a href="https://tunematch-8y24ejjnpcfqykac8diw79.streamlit.app/">
    🚀 Live Demo
  </a>

</p>

---

## 📌 About The Project

**TuneMatch** is a content-based music recommendation system built with Python and Streamlit.

The application analyzes musical characteristics such as:

- 🎵 Energy
- 💃 Danceability
- 🎹 Acousticness
- 🎼 Instrumentalness
- 😊 Valence
- 🎤 Artist
- 🎼 Genre
- 📅 Release Year

Using these characteristics, TuneMatch recommends songs with similar musical profiles and also provides mood-based music discovery.

The project combines **data analysis, recommendation algorithms, visualization, and an interactive web interface** into one application.

---

# ✨ Features

## 🎧 Song Recommendations

Select a song and discover tracks with similar musical characteristics.

TuneMatch considers audio features such as:

- Energy
- Danceability
- Acousticness
- Instrumentalness
- Valence

You can also:

- Filter recommendations by genre
- Search songs by title or artist
- Choose the number of recommendations
- Sort recommendations by similarity
- Sort by energy
- Sort by danceability
- Sort by valence
- Sort by release year

---

## 🎭 Mood-Based Discovery

Choose your current mood and discover suitable songs.

Available moods include:

| Mood | Description |
|---|---|
| 😌 Chill | Calm and relaxing music |
| ⚡ Energetic | High-energy tracks |
| 💃 Dance | Dance-oriented songs |
| 😊 Happy | Positive and uplifting music |
| 💔 Melancholy | Emotional and mellow tracks |

---

## ❤️ Personal Playlist

Users can create their own playlist directly inside the application.

Features include:

- ❤️ Add songs
- 🗑️ Remove songs
- 💾 Save playlist
- 📥 Export playlist as CSV
- 🔄 Persistent playlist storage

---

## 👤 Music Profile

TuneMatch analyzes the user's saved playlist and generates a personalized music profile.

The profile includes:

- 🎼 Favorite Genre
- ⚡ Average Energy
- 💃 Average Danceability
- 🎹 Average Acousticness
- 😊 Average Valence

The application also generates a simple **Music Personality** based on the user's listening characteristics.

---

## 📊 Music Analytics

The Analytics dashboard provides insights into the dataset.

It includes:

- 🎼 Genre Distribution
- ⚡ Average Energy by Genre
- 💃 Average Danceability by Genre
- 😊 Average Valence by Genre
- 📅 Songs by Release Year
- ⚡ Most Energetic Songs
- 💃 Most Danceable Songs

---

# 🧠 Recommendation System

TuneMatch uses a **content-based recommendation approach**.

Instead of relying on other users' listening history, the system compares the characteristics of songs.

The recommendation process can be summarized as:

```text
User selects a song
        ↓
Extract audio features
        ↓
Compare with other songs
        ↓
Calculate similarity
        ↓
Apply optional genre filtering
        ↓
Rank recommendations
        ↓
Display similar songs
