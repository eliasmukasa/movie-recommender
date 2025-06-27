# app.py

import pandas as pd
from flask import Flask, request, jsonify
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# --- Data Loading and Preparation (No Changes Here) ---

try:
    movies = pd.read_csv("movies.csv")
except FileNotFoundError:
    movies = pd.DataFrame(columns=['movieId', 'title', 'genres'])
    print("WARNING: movies.csv not found. Recommender will not work.")

tfidf = TfidfVectorizer(stop_words='english')
movies['genres'] = movies['genres'].fillna('')
tfidf_matrix = tfidf.fit_transform(movies['genres'])
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
indices = pd.Series(movies.index, index=movies['title']).drop_duplicates()


# --- Step 2: Define the Recommendation Function (THIS IS WHERE THE FIX IS) ---

def get_recommendations(title, cosine_sim=cosine_sim):
    """
    This function takes in a movie title and the cosine similarity matrix,
    and returns a list of the 10 most similar movies.
    """
    title_lower = title.lower()
    matching_titles = movies[movies['title'].str.lower().str.contains(title_lower)]

    if matching_titles.empty:
        return []

    matched_title = matching_titles['title'].iloc[0]

    if matched_title not in indices:
        return []

    idx = indices[matched_title]
    
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    movie_indices = [i[0] for i in sim_scores]
    
    return movies['title'].iloc[movie_indices].tolist()



# --- Step 3: API Endpoints (No Changes Here) ---

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/recommend')
def recommend():
    movie_title = request.args.get('title')
    if not movie_title:
        return jsonify({"error": "A 'title' parameter is required."}), 400

    recommendations = get_recommendations(movie_title)
    if not recommendations:
        return jsonify({"error": f"Movie titled '{movie_title}' not found in the dataset."}), 404
    
    return jsonify({"recommendations": recommendations})


if __name__ == '__main__':
    # Running on port 8080 to avoid potential conflicts
    app.run(debug=True, port=8080)
