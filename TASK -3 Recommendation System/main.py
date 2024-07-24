import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# Load the dataset
ratings = pd.read_csv('ratings.csv')
movies = pd.read_csv('movies.csv')

# Preprocess the data
# Create a user-item matrix
user_movie_matrix = ratings.pivot_table(index='userId', columns='movieId', values='rating')

# Fill missing values with 0
user_movie_matrix.fillna(0, inplace=True)

# Calculate user similarity matrix
user_similarity = cosine_similarity(user_movie_matrix)
user_similarity_df = pd.DataFrame(user_similarity, index=user_movie_matrix.index, columns=user_movie_matrix.index)

# Function to get movie recommendations for a specific user
def get_recommendations(user_id, num_recommendations=5):
    # Get the user's ratings
    user_ratings = user_movie_matrix.loc[user_id]
    
    # Get the similarity scores for the user
    similar_users = user_similarity_df[user_id]
    
    # Calculate weighted ratings for each movie
    weighted_ratings = user_movie_matrix.T.dot(similar_users)
    
    # Normalize the weighted ratings
    normalized_ratings = weighted_ratings / similar_users.sum()
    
    # Get the list of movies the user has not rated
    unrated_movies = user_ratings[user_ratings == 0].index
    
    # Get the predicted ratings for the unrated movies
    predicted_ratings = normalized_ratings.loc[unrated_movies]
    
    # Get the top N recommendations
    recommendations = predicted_ratings.nlargest(num_recommendations)
    
    # Get the movie titles
    recommended_movies = movies[movies['movieId'].isin(recommendations.index)]['title']
    
    return recommended_movies

# Get recommendations for a specific user
user_id = 1  # Example user ID
recommendations = get_recommendations(user_id, num_recommendations=5)
print("Recommendations for user", user_id)
print(recommendations)