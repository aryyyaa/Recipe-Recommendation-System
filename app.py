# app.py

import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import re
from selenium.common.exceptions import WebDriverException
import time
url = "https://ranveerbrar.com/recipes/"
def scrape_recipe_urls(url):
    # URL of the website to scrape

    chrome_options = Options()
    chrome_options.add_argument("--ignore-certificate-errors")

    # Initialize a Chrome webdriver with configured options
    driver = webdriver.Chrome(options=chrome_options)

    # Open the URL
    driver.get(url)

    # Get the page source after the JavaScript has loaded
    page_source = driver.page_source

    # Close the webdriver
    driver.quit()

    # Parse the HTML content
    soup = BeautifulSoup(page_source, "html.parser")

    # Find all anchor tags (a) with href attribute and extract the links
    recipe_urls = [link.get("href") for link in soup.find_all("a", href=True)
                if "/recipes/" in link.get("href")]

    # Filter out unwanted links
    recipe_urls = [link for link in recipe_urls if "course" not in link and "books" not in link and not link.endswith("recipes/")]

    # Prepend base URL to relative links
    recipe_urls = [ link for link in recipe_urls]
    recipe_urls = recipe_urls[-5:]
    
    # Create a DataFrame
    recipe_url_df = pd.DataFrame({"recipe_urls": recipe_urls})

    # Save to CSV file
    recipe_url_df.to_csv("C:/Users/Kushal/OneDrive/Documents/sem-6_Miniprj/Gpt-rec/recipe_recommendation_env/data/recipe.csv", index=False)
    return recipe_urls


def clean_ingredients(ingredients):
    # common_words = ['oil', 'salt', 'sugar', 'flour', 'water', 'pepper', 'butter']
    measures = ['teaspoon', 't', 'tsp.', 'tablespoon', 'T', 'tbl.', 'tb', 'tbsp.', 'fluid ounce', 'fl oz', 'gill', 'cup', 'c', 'pint', 'p', 'pt', 'fl pt', 'quart', 'q', 'qt', 'fl qt', 'gallon', 'g', 'gal', 'ml', 'milliliter', 'millilitre', 'cc', 'mL', 'l', 'liter', 'litre', 'L', 'dl', 'deciliter', 'decilitre', 'dL', 'bulb', 'level', 'heaped', 'rounded', 'whole', 'pinch', 'medium', 'slice', 'pound', 'lb', '#', 'ounce', 'oz', 'mg', 'milligram', 'milligramme', 'g', 'gram', 'gramme', 'kg', 'kilogram', 'kilogramme', 'x', 'of', 'mm', 'millimetre', 'millimeter', 'cm', 'centimeter', 'centimetre', 'm', 'meter', 'metre', 'inch', 'in', 'milli', 'centi', 'deci', 'hecto', 'kilo']
    words_to_remove = ['fresh', 'oil', 'a', 'red', 'bunch', 'and', 'clove', 'or', 'leaf', 'chilli', 'large', 'extra', 'sprig', 'ground', 'handful', 'free', 'small', 'pepper', 'virgin', 'range', 'from', 'dried', 'sustainable', 'black', 'peeled', 'higher', 'welfare', 'seed', 'for', 'finely', 'freshly', 'sea', 'quality', 'white', 'ripe', 'few', 'piece', 'source', 'to', 'organic', 'flat', 'smoked', 'ginger', 'sliced', 'green', 'picked', 'the', 'stick', 'plain', 'plus', 'mixed', 'mint', 'bay', 'basil', 'your', 'cumin', 'optional', 'fennel', 'serve', 'mustard', 'unsalted', 'baby', 'paprika', 'fat', 'ask', 'natural', 'skin', 'roughly', 'into', 'such', 'cut', 'good', 'brown', 'grated', 'trimmed', 'oregano', 'powder', 'yellow', 'dusting', 'knob', 'frozen', 'on', 'deseeded', 'low', 'runny', 'balsamic', 'cooked', 'streaky', 'nutmeg', 'sage', 'rasher', 'zest', 'pin', 'groundnut', 'breadcrumb', 'turmeric', 'halved', 'grating', 'stalk', 'light', 'tinned', 'dry', 'soft', 'rocket', 'bone', 'colour', 'washed', 'skinless', 'leftover', 'splash', 'removed', 'dijon', 'thick', 'big', 'hot', 'drained', 'sized', 'chestnut', 'watercress', 'fishmonger', 'english', 'dill', 'caper', 'raw', 'worcestershire', 'flake', 'cider', 'cayenne', 'tbsp', 'leg', 'pine', 'wild', 'if', 'fine', 'herb', 'almond', 'shoulder', 'cube', 'dressing', 'with', 'chunk', 'spice', 'thumb', 'garam', 'new', 'little', 'punnet', 'peppercorn', 'shelled', 'saffron', 'other''chopped', 'salt', 'olive', 'taste', 'can', 'sauce', 'water', 'diced', 'package', 'italian', 'shredded', 'divided', 'parsley', 'vinegar', 'all', 'purpose', 'crushed', 'juice', 'more', 'coriander', 'bell', 'needed', 'thinly', 'boneless', 'half', 'thyme', 'cubed', 'cinnamon', 'cilantro', 'jar', 'seasoning', 'rosemary', 'extract', 'sweet', 'baking', 'beaten', 'heavy', 'seeded', 'tin', 'vanilla', 'uncooked', 'crumb', 'style', 'thin', 'nut', 'coarsely', 'spring', 'chili', 'cornstarch', 'strip', 'cardamom', 'rinsed', 'honey', 'cherry', 'root', 'quartered', 'head', 'softened', 'container', 'crumbled', 'frying', 'lean', 'cooking', 'roasted', 'warm', 'whipping', 'thawed', 'corn', 'pitted', 'sun', 'kosher', 'bite', 'toasted', 'lasagna', 'split', 'melted', 'degree', 'lengthwise', 'romano', 'packed', 'pod', 'anchovy', 'rom', 'prepared', 'juiced', 'fluid', 'floret', 'room', 'active', 'seasoned', 'mix', 'deveined', 'lightly', 'anise', 'thai', 'size', 'unsweetened', 'torn', 'wedge', 'sour', 'basmati', 'marinara', 'dark', 'temperature', 'garnish', 'bouillon', 'loaf', 'shell', 'reggiano', 'canola', 'parmigiano', 'round', 'canned', 'ghee', 'crust', 'long', 'broken', 'ketchup', 'bulk', 'cleaned', 'condensed', 'sherry', 'provolone', 'cold', 'soda', 'cottage', 'spray', 'tamarind', 'pecorino', 'shortening', 'part', 'bottle', 'sodium', 'cocoa', 'grain', 'french', 'roast', 'stem', 'link', 'firm', 'asafoetida', 'mild', 'dash', 'boiling']
    
    cleaned_ingredients = []

    for ingredient in ingredients:
        
        # Remove punctuation and convert to lowercase
        ingredient = re.sub(r'[^\w\s]', '', ingredient.lower())
        # Remove common words
        ingredient = ' '.join([word for word in ingredient.split() if word.isalpha()])
        ingredient = ' '.join([word for word in ingredient.split() if word not in words_to_remove])
        ingredient = ' '.join([word for word in ingredient.split() if word not in measures])
        
        cleaned_ingredients.append(ingredient.strip())

    return cleaned_ingredients

def scrape_recipe_data(recipe_urls):
    recipe_data = []

    for url in recipe_urls:
        chrome_options = Options()
        chrome_options.add_argument("--ignore-certificate-errors")
        
        try:
            # Initialize a Chrome webdriver with configured options
            driver = webdriver.Chrome(options=chrome_options)

            # Open the URL
            driver.get(url)

            # Get the page source after the JavaScript has loaded
            page_source = driver.page_source

            # Close the webdriver
            driver.quit()

            # Parse the HTML content
            soup = BeautifulSoup(page_source, "html.parser")
            
            # Find the ingredient section on the page
            ingredients_section = soup.find(class_='ingredients_cont_wrap')
            if ingredients_section:
                # Extract all list items (ingredients)
                ingredients = ingredients_section.find_all('p')
                # Extract the text from each ingredient and clean it
                cleaned_ingredients = clean_ingredients([ingredient.get_text() for ingredient in ingredients])
                # Append the cleaned ingredients to the recipe data
                recipe_data.append(cleaned_ingredients)
            else:
                recipe_data.append([])  # If no ingredients section found, append an empty list
        
        except WebDriverException:
            # If the webpage is not active or encountered any WebDriverException, skip this URL
            print(f"Skipping URL: {url}")
            continue
    print(recipe_data, "data")
    return recipe_data

def save_to_csv(data, filename):
    # Read the existing CSV file
    df = pd.read_csv(filename)

    # Add a new column for cleaned ingredients
    df['cleaned_ingredients'] = pd.Series(data)
    
    df = df[df['cleaned_ingredients'].apply(lambda x: isinstance(x, list) and len(x) > 0)]
    
    # Save the DataFrame back to the CSV file
    df.to_csv(filename, index=False)

if __name__ == "__main__":
    recipe_urls = scrape_recipe_urls(url)
    # # Create a DataFrame
    # recipe_url_df = pd.DataFrame({"recipe_urls": recipe_urls})

    # # Save to CSV file
    # recipe_url_df.to_csv("recipe_urls.csv", index=False)

    
    # recipe_urls = pd.read_csv('C:/Users/Kushal/OneDrive/Documents/sem-6_Miniprj/Gpt-rec/recipe_recommendation_env/data/recipe.csv')['recipe_urls'].tolist()
    recipe_data = scrape_recipe_data(recipe_urls)
    save_to_csv(recipe_data, 'C:/Users/Kushal/OneDrive/Documents/sem-6_Miniprj/Gpt-rec/recipe_recommendation_env/data/recipe.csv')
 
#  now fetch urls naturally update the name and main code uncomment the scrape function 