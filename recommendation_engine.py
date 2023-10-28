import pickle
from get_top_rated_movies import get_top_rated_movies
from poster_utils import fetch_poster

# Load the SVD model
with open('artifacts/svd_model.pkl', 'rb') as file:
    svd = pickle.load(file)

# Load the get_top_rated_movies function
with open('artifacts/recommendation_function.pkl', 'rb') as file:
    get_top_rated_movies = pickle.load(file)

# Load data and model
movies = pickle.load(open('artifacts\movie_list.pkl', 'rb'))
similarity = pickle.load(open('artifacts\similarity.pkl', 'rb'))


# Define a function to get movie recommendations for a user
def get_movie_recommendations(user_id, threshold=3.5, num_recommendations=10):
    recommended_movies = get_top_rated_movies(user_id, threshold, num_recommendations)
    reco_movie_data = []
    
    for i in range(5):  # Iterate through the top 5 recommendations
        movie_id = recommended_movies[i][0]  # Extract movie ID from recommended_movies
        predicted_rating = recommended_movies[i][1]  # Extract predicted rating
        poster_url = fetch_poster(movie_id)  # Fetch the poster URL
        
        reco_movie_data.append((movie_id, predicted_rating, poster_url))
    
    return reco_movie_data



# def recommend(movie):
#     index = movies[movies['title'] == movie].index[0]
#     distances = sorted(enumerate(similarity[index]), reverse=True, key=lambda x: x[1])
#     recommended_movie_names = []
#     recommended_movie_posters = []
#     for i in distances[1:6]:
#         # fetch the movie poster
#         movie_id = movies.iloc[i[0]].movie_id
#         recommended_movie_posters.append(fetch_poster(movie_id))
#         recommended_movie_names.append(movies.iloc[i[0]].title)

#     return recommended_movie_names, recommended_movie_posters


# # Define a function to get movie recommendations for a user
# def get_movie_recommendations(user_id, threshold=3.5, num_recommendations=10):
#     recommended_movies = get_top_rated_movies(user_id, threshold, num_recommendations)
#     return recommended_movies

# # Example usage:
# user_id = 1  # Replace with the user's ID
# recommended_movies = get_movie_recommendations(user_id, threshold=3.5, num_recommendations=10)

# # Print or return the recommended movies
# for movie in recommended_movies:
#     print(f"Movie ID: {movie[0]}, Predicted Rating: {movie[1]}")
