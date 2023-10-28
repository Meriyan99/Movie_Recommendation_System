import pickle
from surprise import Reader, Dataset, SVD
from surprise.model_selection import cross_validate, train_test_split
import pandas as pd
from authenticate import Authenticate

reader = Reader()
ratings = pd.read_csv('ratings_small.csv')
ratings.head()

data = Dataset.load_from_df(ratings[['userId', 'movieId', 'rating']], reader)

trainset, testset = train_test_split(data, test_size=0.2)  # 80% training, 20% testing

svd = SVD()

cross_validate(svd, data, measures=['RMSE', 'MAE'], cv=5, verbose=True)

trainset = data.build_full_trainset()

svd.fit(trainset)

# user_id = 1
# movie_id = 302
# predicted_rating = svd.predict(user_id, movie_id, 3).est
# print(f"Predicted rating for User {user_id} and Movie {movie_id}: {predicted_rating}")


# Define a function to get recommended movies for a user with a rating threshold
def get_top_rated_movies(user_id, threshold=3.5, num_recommendations=5):
    # Filter movies that the user has not rated
    movies_not_rated_by_user = [i for i in range(1, 193609) if not trainset.ur[trainset.to_inner_uid(user_id)]
                               or i not in [j[0] for j in trainset.ur[trainset.to_inner_uid(user_id)]]]

    # Predict ratings for all unrated movies for the user
    predicted_ratings = [(movie_id, svd.predict(user_id, movie_id).est) for movie_id in movies_not_rated_by_user]

    # Sort the predictions in descending order of estimated ratings
    predicted_ratings.sort(key=lambda x: x[1], reverse=True)

    # Get the top-rated movies above the threshold
    top_rated_movies = [movie for movie in predicted_ratings if movie[1] > threshold]

    return top_rated_movies[:num_recommendations]


# import yaml
# from yaml.loader import SafeLoader
# with open('config.yaml') as file:
#     config = yaml.load(file, Loader=SafeLoader)

# # Initialize authentication
# authenticator = Authenticate(
#     config['credentials'],
#     config['cookie']['name'],
#     config['cookie']['key'],
#     config['cookie']['expiry_days'],
#     config['preauthorized']
# )

# # Use the login method to retrieve the 'username' value
# name, auth_status, username = authenticator.login('Login Form', location='main')

# # Now you can access the 'username' value
# if auth_status:
#     print(f"Authenticated user: {name} ({username})")
# else:
#     print("Authentication failed.")

# Example usage:
# user_id = {username}

# print(f"Authenticated user: {name} ({username})")
def your_function(user):
    user_id = user
    recommended_movies = get_top_rated_movies(user_id, threshold=3.5, num_recommendations=5)

    print(f"Top 5 movies recommended for User {user_id} with ratings > 3.5:")
    for movie in recommended_movies:
        print(f"Movie ID: {movie[0]}, Predicted Rating: {movie[1]}")


# Save the SVD model
with open('artifacts/svd_model.pkl', 'wb') as file:
    pickle.dump(svd, file)

# Save the get_top_rated_movies function
with open('artifacts/recommendation_function.pkl', 'wb') as file:
    pickle.dump(get_top_rated_movies, file)


