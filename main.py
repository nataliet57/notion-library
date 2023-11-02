import pandas as pd
import requests
import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

# Read data from CSV
data = pd.read_csv('test.csv')
data.iloc[:, 0] = data.iloc[:, 0].str.upper()

book_ratings_map = {}

# Iterate over the rows and populate the hashmap
for index, row in data.iterrows():
    book_name = row.iloc[0]  # First column (index 0) is the book name
    reader = row.iloc[1]
    rating = row.iloc[2]  # Third column (index 1) is the rating

    # Check if the book name is already in the hashmap
    if book_name in book_ratings_map:
        # If yes, append the rating to the existing list of ratings
        book_ratings_map[book_name][1] += 1
        currRating = book_ratings_map[book_name][0]
        countRatings = book_ratings_map[book_name][1]
        currRating = (currRating + rating) / countRatings
        book_ratings_map[book_name][0] = currRating
    else:
        book_ratings_map[book_name] = [rating, 1]
    
    if rating == 5:
      if len(book_ratings_map[book_name]) == 2:
         book_ratings_map[book_name].append(1)
      else:
         book_ratings_map[book_name][-1] += 1

# Notion API credentials and endpoint
NOTION_KEY = os.getenv('NOTION_KEY')
NOTION_PAGE_ID = os.getenv('NOTION_PAGE_ID')
NOTION_API_ENDPOINT = f'https://api.notion.com/v1/pages'

headers = {
    'Authorization': f'Bearer {NOTION_KEY}',
    'Content-Type': 'application/json',
}

for book_name in book_ratings_map.items():
    value = book_ratings_map[book_name]
    payload = {
        'parent': {
            'database_id': NOTION_DATABASE_ID,
        },
        'properties': {
            'Book Name': {
                'title': [
                    {
                        'text': {
                            'content': book_name,
                        },
                    },
                ],
            },
            'Average Rating': {
                'number': float(value[0]),
            },
            'Number of Ratings': {
                'number': value[2],
            },
        },
    }
    response = requests.post(NOTION_API_ENDPOINT, headers=headers, json=payload)

    if response.status_code == 200:
        print(f'Successfully added {book_name} with rating {rating} to Notion database.')
    else:
        print(f'Failed to add {book_name} to Notion database. Status code: {response.status_code}')
