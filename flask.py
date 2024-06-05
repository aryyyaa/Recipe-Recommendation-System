from flask import Flask, request, jsonify
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Load the scraped recipe data from CSV
recipe_data = pd.read_csv('path_to_your_recipe_csv')

# Drop rows with missing ingredient data
recipe_data.dropna(subset=['cleaned_ingredients'], inplace=True)

# Initialize TF-IDF Vectorizer
tfidf_vectorizer = TfidfVectorizer()

# Fit and transform the cleaned ingredients into TF-IDF vectors
tfidf_matrix = tfidf_vectorizer.fit_transform(recipe_data['cleaned_ingredients'].apply(lambda x: ' '.join(x)))

# Compute cosine similarity between recipe vectors
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Function to get recommendations based on recipe title
def get_recommendations(title, cosine_sim=cosine_sim):
    # Get the index of the recipe that matches the title
    idx = recipe_data[recipe_data['recipe_urls'] == title].index[0]

    # Get pairwise similarity scores with all recipes
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the recipes based on similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the top 5 most similar recipes (excluding the queried recipe itself)
    sim_scores = sim_scores[1:6]

    # Get the indices of recommended recipes
    recipe_indices = [score[0] for score in sim_scores]

    # Return the titles of recommended recipes
    return recipe_data['recipe_urls'].iloc[recipe_indices]

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    recipe_url = data['recipe_url']
    recommendations = get_recommendations(recipe_url)
    return jsonify({'recommendations': recommendations.tolist()})

if __name__ == '__main__':
    app.run(debug=True)
