import pandas as pd
import unicodedata
import os
from notion_client import Client
from pprint import pprint
import csv
import requests

import sys
from csv import writer
import os
import requests
 

# Notion integration token and database URL

notion_token = 'secret_EZ6qGNjHN3YE6opz5y7ke3ABQlTHWnf2dYuYz2ZTehr'
notion_page_id = 'c585bf17deac4715adb7d80b37445aa5'
notion_database_id = '7de8c091807a4800925f944b5d171d2f'
client = Client(auth=notion_token)
database = client.databases.retrieve(database_id=notion_database_id)
notion = Client(auth=notion_token)

url = f"https://api.notion.com/v1/databases/{notion_database_id}/query"
headers = {
    "Authorization": f"Bearer {notion_token}",
    "Content-Type": "application/json",
    "Notion-Version": "2021-08-16",  # Specify the desired API version here
}

data = []
next_cursor = None

def safe_get(data, dot_chained_keys):
    '''
        {'a': {'b': [{'c': 1}]}}
        safe_get(data, 'a.b.0.c') -> 1
    '''
    keys = dot_chained_keys.split('.')
    for key in keys:
        try:
            if isinstance(data, list):
                data = data[int(key)]
            else:
                data = data[key]
        except (KeyError, TypeError, IndexError):
            return None
    return data

db_rows = client.databases.query(database_id=notion_database_id)

rows = []

for row in db_rows['results']:
    book_name = safe_get(row, 'properties.Name.title.0.plain_text')
    perfect_ratings = safe_get(row, 'properties.Perfect_Ratings.number')
    average = safe_get(row, 'properties.Average.number')
    count = safe_get(row, 'properties.Count.number')
    
    rows.append([
        book_name,
        perfect_ratings,
        average,
        count
    ])

filename = 'test.csv'

with open(filename, 'a') as f_object:
    # Pass this file object to csv.writer()
    # and get a writer object
    writer_object = writer(f_object)
    for row in rows:
      writer_object.writerow(row)
 
    # Close the file object
    f_object.close()

data = pd.read_csv(filename, encoding='utf-8', header = None)

book_ratings_map = {}

# Iterate over the rows and populate the hashmap
for index, row in data.iterrows():
    # uunicode = unicodedata.normalize('NFKD', row.iloc[0]).casefold()
    book_name = row.iloc[0].casefold().strip()
    reader = row.iloc[1]
    rating = row.iloc[2]  # Third column (index 1) is the rating

    # Check if the book name is already in the hashmap
    print(book_name)
    if book_name in book_ratings_map:
        # If yes, append the rating to the existing list of ratings
        book_ratings_map[book_name][1] += 1
        currRating = book_ratings_map[book_name][0]
        countRatings = book_ratings_map[book_name][1]
        currRating = (currRating + rating) / countRatings
        book_ratings_map[book_name][0] = currRating
    else:
        book_ratings_map[book_name] = [rating, 1, 0]
    
    if rating == 5:
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
   write_row(client, notion_page_id, book_name, value[0], value[2])

