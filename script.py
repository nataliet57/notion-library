import pandas as pd
from notion_client import Client
from pprint import pprint
from csv import writer

# Notion integration token and database URL

notion_token = 'secret_EZ6qGNjHN3YE6opz5y7ke3ABQlTHWnf2dYuYz2ZTehr'
notion_page_id = 'c585bf17deac4715adb7d80b37445aa5'
notion_database_id = '7de8c091807a4800925f944b5d171d2f'
client = Client(auth=notion_token)
database = client.databases.retrieve(database_id=notion_database_id)

filename = input("Enter the filename with .csv appended: ")
data = []

# Create new row in Notion table for each mapping of a book
def write_row(client, database_id, book_name, avg, num_perfect_ratings, count):
    client.pages.create(
        **{
          'parent': {
            'database_id': database_id,
          },
          'properties': {
              'Name': {
                  'title': [
                      {
                          'text': {
                              'content': book_name,
                          },
                      },
                  ],
              },
              'Average': {
                  'number': float(avg),
              },
              'Perfect_Ratings': {
                  'number': num_perfect_ratings,
              },
              'Count': {
                  'number': count,
              },
          },
        }
    )

# Function to get notion db row 
def safe_get(data, dot_chained_keys):
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

# Data structure to hold list of books that already exist
rows = []

# For every book in the notion db, create an object and append it to rows
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

# Write every row into the csv the user passed in
with open(filename, 'a') as f_object:
    # Pass this file object to csv.writer()
    writer_object = writer(f_object)
    for row in rows:
      writer_object.writerow(row)
 
    # Close the file object
    f_object.close()

data = pd.read_csv(filename, encoding='utf-8', header = None)

book_ratings_map = {}

# Iterate over the rows including the new books and existing books and populate the hashmap
for index, row in data.iterrows():
    book_name = row.iloc[0].casefold().strip()    
    # if row was imported from existing notion table
    if len(row) == 5:
        rating = row.iloc[1] 
        if book_name in book_ratings_map:
            currSumRating = book_ratings_map[book_name][0] * book_ratings_map[book_name][1]
            newSumRating = row.iloc[1] * row.iloc[3]
            book_ratings_map[book_name][1] += row.iloc[3]
            currRating = (currSumRating + newSumRating) / book_ratings_map[book_name][1]
            book_ratings_map[book_name][0] = currRating
        else:
            book_ratings_map[book_name] = [rating, row.iloc[2], row.iloc[2]]

    # Check if the book name is already in the hashmap
    if len(row) == 3:
        rating = row.iloc[2]  # Third column (index 1) is the rating
        if book_name in book_ratings_map:
            book_ratings_map[book_name][1] += 1
            currRating = book_ratings_map[book_name][0]
            countRatings = book_ratings_map[book_name][1]
            currRating = (currRating + rating) / countRatings
            book_ratings_map[book_name][0] = currRating
        else:
            book_ratings_map[book_name] = [rating, 1, 0]
    
        if rating == 5:
            book_ratings_map[book_name][-1] += 1

for book_name in book_ratings_map:
   value = book_ratings_map[book_name]
   write_row(client, notion_database_id, book_name, value[0], value[2], value[1])

