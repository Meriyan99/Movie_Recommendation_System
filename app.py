import pickle
import streamlit as st
# import requests
from authenticate import Authenticate
from get_top_rated_movies import get_top_rated_movies
from poster_utils import fetch_poster
from get_top_rated_movies import your_function


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(enumerate(similarity[index]), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
        # sample = movies.iloc[i[0]].title

    return recommended_movie_names, recommended_movie_posters

def get_movie_recommendations(user_id=1, threshold=3.5, num_recommendations=5):
    # Call the existing get_top_rated_movies function
    reco_movies = get_top_rated_movies(user_id, threshold=threshold, num_recommendations=num_recommendations)
    movies = pickle.load(open('artifacts\movie_list.pkl', 'rb'))
    
    reco_movie_id = [f"{movie[0]}" for movie in reco_movies]
    # reco_movie_names = [1, 2, 3, 4, 5]
    reco_movie_names = []
    for i in range(0, 5):
        print(reco_movie_id)
        reco_movie = reco_movie_id[i]
        # print(type(reco_movie))
        re_movie = int(reco_movie)
        # re_movie = 296
        # print(type(re_movie))
    # reco_movie_names = 'none'
        # reco_movie_names = [(movies.iloc[re_movie[0]].title)]
        if re_movie in movies['movie_id'].values:
            index = movies[movies['movie_id'] == re_movie].index[0]
            print(index)
            print(type(index))
            indeX = int(index)
            print(type(indeX))
            reco_movie_names.append(movies.iloc[indeX].title)
            print(reco_movie_names)
        else:
            print(f"Movie ID {re_movie} not found in the DataFrame.")
            reco_movie_names.append("Movie N/A")
            # reco_movie_names.append(f"Movie ID: {movie[0]}" for movie in reco_movies)
            # reco_movie_names = [f"Movie ID: {movie[0]}" for movie in reco_movies]
    # reco_movie_names = reco_movie
    reco_movie_posters = [fetch_poster(movie[0]) for movie in reco_movies]
    
    return reco_movie_names, reco_movie_posters

# def get_movie_recommendations(user_id=1, threshold=3.5, num_recommendations=5):
#     # Call the existing get_top_rated_movies function
#     reco_movies = get_top_rated_movies(user_id, threshold=threshold, num_recommendations=num_recommendations)
    
#     reco_movie_names = [f"Movie ID: {movie[0]}" for movie in reco_movies]
#     reco_movie_posters = [fetch_poster(movie[0]) for movie in reco_movies]
    
#     return reco_movie_names, reco_movie_posters



# Set page configuration
st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")

import yaml
from yaml.loader import SafeLoader
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Initialize authentication
authenticator = Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

# Main content area
st.title('Movie Recommender System Using ML')

name, authentication_status, username = authenticator.login('Login', 'main')

if st.session_state["authentication_status"]:
    
    st.write(f'Welcome *{st.session_state["name"]}!*')
    st.write(f'Here are some movie suggestions based on your rating')

    user = int(username)
    # Call the function and pass 'user' as an argument
    result = your_function(user)
    # result1 = type(user)

    reco_movie_names, reco_movie_posters = get_movie_recommendations(user_id=user, threshold=3.5, num_recommendations=5)
    # st.success("Here are your movie recommendations:")

    # Display recommendations in a carousel
    col1, col2, col3, col4, col5 = st.columns(5)
    cols = [col1, col2, col3, col4, col5]

    for i in range(5):
        with cols[i]:
            st.image(reco_movie_posters[i], width=200)
            st.write(reco_movie_names[i])


    # Load data and model
    movies = pickle.load(open('artifacts\movie_list.pkl', 'rb'))
    similarity = pickle.load(open('artifacts\similarity.pkl', 'rb'))

    # if st.session_state["authentication_status"]:

    # Sidebar with a title and background image
    st.sidebar.image("images.jpg")
    # Add CSS to make the image fill the sidebar width
    st.sidebar.markdown(
        f'<style>div[data-testid="stSidebar"] div[data-testid="stBlock"] img {{width: 100%;}}</style>',
        unsafe_allow_html=True,
    )
    st.sidebar.title("🎬 How to use?")
    # Add simplified instructions
    # st.sidebar.markdown(result1)
    st.sidebar.markdown("1. **Sugested Movies:** We have suggested few movies based on your rating")
    st.sidebar.markdown("2. **Search for a Movie:** Start by typing the name of a movie you like in the search bar.")
    st.sidebar.markdown("3. **Get Recommendations:** Click the 'Get Similar Movies' button.")
    st.sidebar.markdown("4. **Enjoy Your Movie Journey:** Search for more and enjoy your movie journey.")

    # # Main content area
    # st.title('Movie Recommender System Using ML')

    # User input and recommendation
    movie_list = movies['title'].values
    selected_movie = st.selectbox("Find similar movies:", movie_list)

    if st.button('Get Similar Movies', key="recommend_button"):
        st.spinner("Finding similar movies...")
        recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
        st.success("Here are some similar movies:")

        # Display recommendations in a carousel
        col1, col2, col3, col4, col5 = st.columns(5)
        cols = [col1, col2, col3, col4, col5]

        for i in range(5):
            with cols[i]:
                st.image(recommended_movie_posters[i], width=200)
                st.write(recommended_movie_names[i])

    authenticator.logout('Logout', 'main')

elif st.session_state["authentication_status"] == False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] == None:
    st.warning('Please enter your username and password')

# # Logout button
# authenticator.logout('Logout', location='main')

# Add a custom footer
st.markdown("---")
st.write("Built with ❤️ by BrainLeftException")
