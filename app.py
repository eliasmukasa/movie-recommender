# app.py

import pandas as pd
from flask import Flask, request, jsonify, render_template
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# --- Step 1: Load and Prepare Data (Optimized for Memory) ---
# We will still load the movie data and create the TF-IDF matrix at startup.
# This part is memory-efficient.

try:
    movies = pd.read_csv("movies.csv")
    # We create the TF-IDF matrix, which is relatively small.
    tfidf = TfidfVectorizer(stop_words='english')
    movies['genres'] = movies['genres'].fillna('')
    tfidf_matrix = tfidf.fit_transform(movies['genres'])
    # Create the title-to-index mapping
    indices = pd.Series(movies.index, index=movies['title']).drop_duplicates()
except FileNotFoundError:
    movies = pd.DataFrame(columns=['movieId', 'title', 'genres'])
    tfidf_matrix = None
    indices = None
    print("WARNING: movies.csv not found. Recommender will not work.")

# --- NOTICE: We have REMOVED the giant cosine_sim matrix from here ---


# --- Step 2: Define the Recommendation Function (Now More Efficient) ---

def get_recommendations(title):
    """
    This function now calculates similarity on-the-fly for just the one movie,
    saving a huge amount of memory.
    """
    if indices is None or title not in indices:
        # Fallback if data didn't load or title doesn't exist
        # Also handles the case-sensitive formatting issue from before
        title_lower = title.lower()
        matching_titles = movies[movies['title'].str.lower().str.contains(title_lower)]
        if matching_titles.empty:
            return [] # Movie not found
        # Use the full, correct title of the first match
        matched_title = matching_titles['title'].iloc[0]
        if matched_title not in indices:
            return []
        idx = indices[matched_title]
    else:
        # If the title matches exactly, get its index
        idx = indices[title]

    # --- THE CORE OPTIMIZATION ---
    # Calculate cosine similarity for only the selected movie against all others
    # This avoids storing the giant matrix in memory.
    sim_scores = cosine_similarity(tfidf_matrix[idx], tfidf_matrix)

    # Flatten the array and enumerate to keep track of indices
    sim_scores = list(enumerate(sim_scores[0]))
    
    # Sort and get top 10 like before
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

    if tfidf_matrix is None:
        return jsonify({"error": "Dataset not loaded on the server."}), 500

    recommendations = get_recommendations(movie_title)
    if not recommendations:
        return jsonify({"error": f"Movie titled '{movie_title}' not found or no recommendations available."}), 404
    
    return jsonify({"recommendations": recommendations})



# Health check endpoint for uptime monitoring
@app.route('/ping')
def ping():
    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=8080)
