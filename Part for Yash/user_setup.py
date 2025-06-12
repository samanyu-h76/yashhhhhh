from firebase_setup import initialize_firebase
from utils.dietary_constants import DIETARY_OPTIONS

def get_user_input():
    name = input("Enter your name: ").strip()

    print("\nSelect your dietary preferences (comma-separated numbers):")
    for idx, option in enumerate(DIETARY_OPTIONS, 1):
        print(f"{idx}. {option}")

    selected = input("\nYour choices (e.g., 1,4,6): ").strip()
    selected_indexes = [int(i) - 1 for i in selected.split(",") if i.strip().isdigit()]
    preferences = [DIETARY_OPTIONS[i] for i in selected_indexes if 0 <= i < len(DIETARY_OPTIONS)]

    return name, preferences

def register_user():
    db = initialize_firebase()
    users_ref = db.collection("users")

    name, preferences = get_user_input()

    user_doc = users_ref.document(name)
    if user_doc.get().exists:
        print(f"\n👤 User '{name}' already exists. Skipping to next step...")
        return name  # Proceed with this user
    else:
        user_doc.set({
            "name": name,
            "preferences": preferences
        })
        print(f"\n✅ New user '{name}' created with preferences: {preferences}")
        return name  # Proceed with this new user
