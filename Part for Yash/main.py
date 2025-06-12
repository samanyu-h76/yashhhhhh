import os
from user_setup import register_user
from image_search.image_handler import process_image_and_scrape_dishes
from image_search.dish_recommender import recommend_dishes_gemini_with_firebase

def main():
    print("=== Welcome to Smart Restaurant Personalization ===\n")

    # 1. Setup user - enter name & dietary prefs, saved in Firebase, returns user_id
    user_id = register_user()

    print(f"\nHello, {user_id}! Let's personalize your menu.\n")

    # 2. Ask user to upload/scan image - here simplified as file path input
    image_path = input("Upload or scan an image of a dish (enter image file path): ").strip()

    # 3. Process image, scrape dishes visually matched
    print("\nProcessing your image and searching for dish matches...\n")
    dishes = process_image_and_scrape_dishes(image_path)

    if not dishes:
        print("Sorry, no dishes found from your image. Please try another image.")
        return

    print(f"Dishes found: {dishes}")

    # 4. Get personalized recommendations based on user prefs from Firebase + Gemini AI
    recommendations = recommend_dishes_gemini_with_firebase(user_id, dishes)

    if not recommendations:
        print("Sorry, couldn't generate personalized dish recommendations.")
        return

    print("\nHere are your personalized menu recommendations:\n")

    for item in recommendations:
        print(f"🍽️ {item['original']}")
        for variant in item['variants']:
            print(f"  ➜ {variant}")
        print()

if __name__ == "__main__":
    main()
