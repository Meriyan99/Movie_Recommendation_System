# import pickle
import pandas as pd
# from surprise import Reader, Dataset, SVD, Trainset
# from surprise.model_selection import cross_validate, train_test_split

# # Load the SVD model
# with open('artifacts/svd_model.pkl', 'rb') as file:
#     svd = pickle.load(file)

# # Load the get_top_rated_movies function
# with open('artifacts/recommendation_function.pkl', 'rb') as file:
#     get_top_rated_movies = pickle.load(file)

# Function to append user ratings to an existing CSV file
def add_user_ratings_to_csv(user_id, movie_id, rating, csv_file):
    new_data = {'userId': [user_id], 'movieId': [movie_id], 'rating': [rating]}
    new_ratings = pd.DataFrame(new_data)
    
    # Append the new ratings to the existing CSV file
    existing_ratings = pd.read_csv(csv_file)
    updated_ratings = pd.concat([existing_ratings, new_ratings], ignore_index=True)
    
    # Save the updated ratings to the CSV file
    updated_ratings.to_csv(csv_file, index=False)

# Input user ratings for 5 movies and append to the existing CSV file
for i in range(5):
    user_id = int(input(f"Enter User ID for Movie {i+1}: "))
    movie_id = int(input(f"Enter Movie ID for Movie {i+1}: "))
    rating = float(input(f"Enter Rating for Movie {i+1}: "))
    
    # Append the user rating to the existing CSV file 'ratings_small.csv'
    add_user_ratings_to_csv(user_id, movie_id, rating, 'ratings_small.csv')
    
# # Reload the dataset and update the trainset
# reader = Reader()
# ratings = pd.read_csv('ratings_small.csv')
# data = Dataset.load_from_df(ratings[['userId', 'movieId', 'rating']], reader)
# trainset = data.build_full_trainset()

# # Fit the SVD model with the updated trainset
# svd.fit(trainset)

# # Example: Get recommendations for a user (e.g., user 1) after updating the model
# user_id = 1
# recommended_movies = get_top_rated_movies(user_id, threshold=3.5, num_recommendations=5)

# print(f"Top 5 movies recommended for User {user_id} with ratings > 3.5:")
# for movie in recommended_movies:
#     print(f"Movie ID: {movie[0]}, Predicted Rating: {movie[1]}")
