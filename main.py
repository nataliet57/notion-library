import pandas as pd
import requests
import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

# Read data from CSV
data = pd.read_csv('ratings.csv')
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
        book_ratings_map[book_name].append(rating)
    else:
        # If not, create a new list with the current rating
        book_ratings_map[book_name] = [rating]
print(book_ratings_map)

# # Notion API credentials and endpoint
# NOTION_KEY = os.getenv('NOTION_KEY')
# NOTION_PAGE_ID = os.getenv('NOTION_PAGE_ID')
# NOTION_API_ENDPOINT = f'https://api.notion.com/v1/pages'

# headers = {
#     'Authorization': f'Bearer {NOTION_KEY}',
#     'Content-Type': 'application/json',
# }

# # Iterate over rated books and update Notion database
# for index, row in rated_books.iterrows():
#     book_name = row['book_name']
#     rating = row['rating']

#     payload = {
#         'parent': {
#             'database_id': NOTION_PAGE_ID,
#         },
#         'properties': {
#             'Book Name': {
#                 'title': [
#                     {
#                         'text': {
#                             'content': book_name,
#                         },
#                     },
#                 ],
#             },
#             'Rating': {
#                 'number': float(rating),
#             },
#         },
#     }

#     response = requests.post(NOTION_API_ENDPOINT, headers=headers, json=payload)

#     if response.status_code == 200:
#         print(f'Successfully added {book_name} with rating {rating} to Notion database.')
#     else:
#         print(f'Failed to add {book_name} to Notion database. Status code: {response.status_code}')
