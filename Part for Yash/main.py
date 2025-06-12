import streamlit as st
from user_setup import register_user
from image_search.image_handler import process_image_and_scrape_dishes
from image_search.dish_recommender import recommend_dishes_gemini_with_firebase

# Initialize session state
if 'user_id' not in st.session_state:
    st.session_state.user_id = None

# Title of the app
st.title("Smart Restaurant Personalization")

# Step 1: User Registration
if st.session_state.user_id is None:
    st.header("Step 1: Register User")
    user_name = st.text_input("Enter your name")
    dietary_prefs = st.text_input("Enter your dietary preferences")
    if st.button
