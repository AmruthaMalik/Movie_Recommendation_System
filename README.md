# 🎬 SDG-Aware Movie Recommendation System

This project is an intelligent movie recommendation system built using *Streamlit* that maps movies to relevant *Sustainable Development Goals (SDGs)* based on their descriptions. The application helps promote *socially conscious viewing* by suggesting films aligned with global goals such as *Quality Education, Gender Equality, Climate Action*, and more.

## 🌐 Live Demo

To run this project locally, launch:
http://localhost:8501/


This will open the Streamlit app in your browser.

---

## 🖼 Screenshot

![Image](https://github.com/user-attachments/assets/fd7e3c22-fd6e-4bd9-bf07-50e5c15544c4)


---

## 📽 Demo Video

If your .mov video is too large to upload to GitHub directly, you can upload it to *YouTube as Unlisted* and embed it here like this:

---

## 📁 Project Structure

<pre>├── recc_app.py # Main Streamlit application 
├── sdg_mapping.py # SDG keyword mapping script 
├── tmdb_5000_movies.csv # Movie metadata dataset 
├── requirements.txt # Python dependencies 
└── README.md # Project documentation (this file) </pre>


---

## 🚀 Features

- 🔍 Search for movies by name
- 🎯 Filter movies based on SDG goals
- 🎭 Filter by genres (Drama, Comedy, Action, etc.)
- ⭐ View ratings, genres, and SDG matches
- 🖼 Display movie posters from TMDB
- 👍👎 Like or Dislike interaction buttons

---

## 📦 Installation Instructions

### 1. Clone the repository

bash
git clone https://github.com/AmruthaMalik/sdg-movie-recommender.git
cd sdg-movie-recommender



### 2. Install dependencies

pip install -r requirements.txt

### 3. Run the Streamlit app

streamlit run recc_app.py


Then open [http://localhost:8501](http://localhost:8501) in your browser.

## 🍿 How It Works

Loads data from tmdb_5000_movies.csv (includes overview, genre, vote info)

Analyzes the movie description and matches keywords to predefined SDGs

Assigns SDG tags to movies (e.g., SDG 4: Quality Education)

Filters and displays movies based on user preferences


## 🎯 SDG Keyword Mapping Logic

sdg_keywords = {
    'SDG 4: Quality Education': ['education', 'learning', 'school', 'teaching'],
    'SDG 5: Gender Equality': ['gender', 'women', 'equality'],
    'SDG 10: Reduced Inequalities': ['poverty', 'racism', 'inequality'],
    'SDG 13: Climate Action': ['climate', 'pollution', 'sustainability'],
    'SDG 16: Peace & Justice': ['justice', 'peace', 'corruption']
}

Each movie's overview is scanned for these keywords to assign appropriate SDG goals.

## 📊 Sample Output
Here's what a movie card may include:

🎬 Movie Title: Dead Poets Society

🎯 SDG Match: SDG 4: Quality Education

🎭 Genres: Drama

⭐ Rating: 8.2

👍 Like | 👎 Dislike

## 🛠 Built With
Streamlit

Pandas

The Movie Database (TMDB)

Python

### 🤝 Contributing
Contributions are welcome! If you have ideas for improving SDG detection or UI, feel free to fork the repo and submit a pull request.