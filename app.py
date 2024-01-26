import streamlit as st
import difflib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Function to set the background image using CSS
def set_background_image(image_url):
    # Apply custom CSS to set the background image
    page_bg_img = '''
    <style>
    .stApp {
        background-position: top;
        background-image: url(%s);
        background-size: cover;
    }

    @media (max-width: 768px) {
        /* Adjust background size for mobile devices */
        .stApp {
            background-position: top;
            background-size: contain;
            background-repeat: no-repeat;
        }
    }
    </style>
    ''' % image_url
    st.markdown(page_bg_img, unsafe_allow_html=True)

# Function to get movie recommendations
def get_recommendations(movie_name):
    # Load the movies data
    movies_data = pd.read_csv('movies.csv')

    # Preprocess the data
    selected_features = ['genres', 'keywords', 'tagline', 'cast', 'director']
    for feature in selected_features:
        movies_data[feature] = movies_data[feature].fillna('')
    combined_features = movies_data['genres'] + ' ' + movies_data['keywords'] + ' ' + movies_data['tagline'] + ' ' + movies_data['cast'] + ' ' + movies_data['director']

    # Convert text data to feature vectors
    vectorizer = TfidfVectorizer()
    feature_vectors = vectorizer.fit_transform(combined_features)

    # Calculate cosine similarity
    similarity = cosine_similarity(feature_vectors)

    # Find close matches
    find_close_match = difflib.get_close_matches(movie_name, movies_data['title'].tolist())
    if find_close_match:
        close_match = find_close_match[0]
        index_of_the_movie = movies_data[movies_data.title == close_match]['index'].values[0]
        similarity_score = list(enumerate(similarity[index_of_the_movie]))
        sorted_similar_movies = sorted(similarity_score, key=lambda x: x[1], reverse=True)[:10]

        # Return movie recommendations
        recommendations = [movies_data.iloc[movie[0]]['title'] for movie in sorted_similar_movies]
        return recommendations
    else:
        return None

# Set the background image URL
background_image_url = "https://wallpapercave.com/wp/wp2714503.jpg"

# Set the background image
set_background_image(background_image_url)

custom_css = """
   <style>
   body {
       background-color: #4699d4;
       color: #ffffff;
       font-family: Arial, sans-serif;
   }
   select {
       background-color: #000000 !important; /* Black background for select box */
       color: #ffffff !important; /* White text within select box */
   }
   label {
       color: #000000 !important; /* White color for select box label */
   }
   div[data-baseweb="input"] input {
       width: 200px;  /* Adjust the width as needed */
   }
   </style>
   """
st.markdown(custom_css, unsafe_allow_html=True)

# Streamlit app content
st.markdown("<h1 style='color:white;'>🎬 Movie Recommendation App</h1>", unsafe_allow_html=True)
st.markdown("""
<span style='color:#F0F8FF;'>
Welcome to the Movie Recommendation App! Enter the name of your favorite movie, and we'll suggest some similar movies for you.
</span>
""", unsafe_allow_html=True)

# User input for movie name
# Provide a non-empty label for the input
movie_name_label = "<span style='color: white;'>Enter your favorite movie name above</span>"

# Custom CSS to style the input box and label
custom_input_css = """
<style>
    div[data-baseweb="input"] input {
        width: 200px;
        /* Add any additional styles you want for the input box */
    }
</style>
"""
st.markdown(custom_input_css, unsafe_allow_html=True)

# Create the text input with a white-colored label
movie_name = st.text_input('', '', key='movie_name_input')
st.markdown(movie_name_label, unsafe_allow_html=True)

# Button to trigger movie recommendations
if st.button('Get Recommendations'):
    if movie_name:
        # Get recommendations
        recommendations = get_recommendations(movie_name)
        if recommendations:
            # Display recommendations
            st.markdown("<h3 style='color:white;'>Movies suggested for you:</h3>", unsafe_allow_html=True)
            for i, movie in enumerate(recommendations, start=1):
                st.markdown(f"<span style='color:white; font-weight:bold;'>{i}. {movie}</span>", unsafe_allow_html=True)
        else:
            st.warning('Movie not found. Please enter a valid movie name.')
    else:
        st.warning('Please enter a movie name.')
