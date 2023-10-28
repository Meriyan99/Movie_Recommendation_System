import requests

def fetch_poster(movie_id):
    try:
        url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
        data = requests.get(url)
        data = data.json()
        poster_path = data.get('poster_path')

        if poster_path:
            full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
            return full_path
        else:
            # Return the local file path to the placeholder image
            return "Printable-Blank-Movie-Poster.jpg"  # Replace with the actual file path

    except Exception as e:
        # Handle any exceptions that might occur during the image retrieval process
        print("Error fetching poster:", str(e))
        # Return the local file path to the placeholder image or handle the error appropriately
        return "Printable-Blank-Movie-Poster.jpg"  # Replace with the actual file path



