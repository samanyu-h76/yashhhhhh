# image_search/image_handler.py

import io
from google.cloud import vision
from tkinter import Tk, filedialog

def select_image():
    """Open file dialog to select image."""
    Tk().withdraw()  # Hide root window
    file_path = filedialog.askopenfilename(
        title="Select a food image",
        filetypes=[("Image Files", "*.jpg *.png *.jpeg *.webp")]
    )
    if file_path:
        print(f"✅ Image selected: {file_path}")
        return file_path
    else:
        print("❌ No image selected.")
        return None

def recognize_food_labels(image_path):
    """Use Google Vision API to detect labels in the food image."""
    client = vision.ImageAnnotatorClient()

    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.label_detection(image=image)

    if response.error.message:
        print(f"Google Vision API error: {response.error.message}")
        return []

    labels = response.label_annotations
    # Filter labels related to food or dishes
    food_labels = [label.description for label in labels if 'food' in label.description.lower() or 'dish' in label.description.lower()]

    if not food_labels:
        # fallback to top 5 labels if no explicit 'food' or 'dish'
        food_labels = [label.description for label in labels[:5]]

    print(f"🔍 Detected labels: {food_labels}")
    return food_labels

def scrape_dish_ideas(keywords):
    """Scrape dish ideas from AllRecipes based on keywords."""
    import requests
    from bs4 import BeautifulSoup

    query = "+".join(keywords)
    url = f"https://www.allrecipes.com/search/results/?search={query}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        results = []
        articles = soup.select("div.card__detailsContainer-left h3.card__title")
        for article in articles[:5]:
            title = article.get_text(strip=True)
            results.append(title)

        return results if results else ["No dishes found."]
    except Exception as e:
        print("❌ Error during web scraping:", e)
        return ["Error fetching dishes."]

def process_image_and_scrape_dishes(image_path=None):
    if not image_path:
        image_path = select_image()
        if not image_path:
            return None, []

    keywords = recognize_food_labels(image_path)
    dishes = scrape_dish_ideas(keywords)
    print(f"🍽️ Suggested Dishes: {dishes}")

    return image_path, dishes
