import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore

# Load env vars for Gemini
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# Initialize Firebase Admin only once
if not firebase_admin._apps:
    cred = credentials.Certificate('restaurant-data-backend-firebase-adminsdk-fbsvc-bdeb44e4a8.json')  # Path to your Firebase service account
    firebase_admin.initialize_app(cred)

db = firestore.client()
model = genai.GenerativeModel('gemini-1.5-flash')

def get_user_dietary_preferences(user_id):
    """Fetch user's dietary preferences list from Firestore."""
    try:
        doc_ref = db.collection('users').document(user_id)
        doc = doc_ref.get()
        if doc.exists:
            data = doc.to_dict()
            return data.get('dietary_preferences', [])
        else:
            print(f"User {user_id} not found in Firestore.")
            return []
    except Exception as e:
        print("Error fetching user dietary preferences:", e)
        return []

def recommend_dishes_gemini_with_firebase(user_id, dish_list):
    """
    Fetch dietary prefs from Firebase for given user_id,
    then generate dish recommendations from Gemini.
    """
    if not dish_list:
        return []

    dietary_prefs = get_user_dietary_preferences(user_id)
    print(f"Fetched dietary preferences for user {user_id}: {dietary_prefs}")

    prompt = (
        "You are a culinary AI assistant. Given a list of dishes and a customer's dietary preferences, "
        "suggest 2-3 personalized variants or ingredient swaps per dish. "
        "Consider dietary restrictions seriously.\n\n"
        f"Dietary Preferences: {', '.join(dietary_prefs) if dietary_prefs else 'None'}\n"
        f"Dishes: {', '.join(dish_list)}\n\n"
        "Output JSON array with entries like: "
        "[{\"original\": \"Dish Name\", \"variants\": [\"variant1\", \"variant2\"]}, ...]"
    )

    try:
        response = model.generate_content(prompt)
        response_text = response.text

        recommendations = json.loads(response_text)
        return recommendations

    except Exception as e:
        print("Gemini AI or JSON parsing error:", e)
        return []
