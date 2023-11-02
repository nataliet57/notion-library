import pandas as pd
import os
from notion_client import Client
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

# Notion API credentials and endpoint
NOTION_KEY = os.getenv('NOTION_KEY')
NOTION_PAGE_ID = os.getenv('NOTION_PAGE_ID')
NOTION_API_ENDPOINT = f'https://api.notion.com/v1/pages'
client = Client(auth=NOTION_KEY)

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

def write_row(client, database_id, book_name, avg, num_perfect_ratings):
    client.pages.create(
        **{
          'parent': {
            'database_id': database_id,
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
                  'number': float(avg),
              },
              'Number of Ratings': {
                  'number': num_perfect_ratings,
              },
          },
        }
    )

for book_name in book_ratings_map:
   value = book_ratings_map[book_name]
   write_row(client, NOTION_PAGE_ID, book_name, value[0], value[2])
