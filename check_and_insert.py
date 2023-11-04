from notion_client import Client
from notion_client import AsyncClient
from pprint import pprint

import sys


import os

# Notion integration token and database URL

notion_token = 'secret_EZ6qGNjHN3YE6opz5y7ke3ABQlTHWnf2dYuYz2ZTehr'
notion_page_id = 'c585bf17deac4715adb7d80b37445aa5'
notion_database_id = '7de8c091807a4800925f944b5d171d2f'
client = Client(auth=notion_token)
database = client.databases.retrieve(database_id=notion_database_id)
notion = Client(auth=notion_token)

# Function to check if book_name exists in Notion database and update/insert accordingly
def check_and_update_notion(book_name):

    # Query the database to find the book by name
    # results = database.default_query(filter={"property": "Book Name", "text": {"equals": book_name}})
    results = database.query(filter={"property": "Book Name", "text": {"equals": book_name}})

    # If the book_name exists, update the count
    if results:
        page = results[0]
        current_count = page.get_property("Count")
        page.set_property("Count", current_count + 1)
        print(f'Updated count for {book_name}.')
    else:
        # If the book_name doesn't exist, insert a new row with count 1
        new_row = database.collection.add_row()
        new_row.set_property("Book Name", book_name)
        new_row.set_property("Count", 1)
        print(f'Inserted new row for {book_name}.')


results = notion.search(query='computer systems: a programm').get("results")
print(len(results))
result = results[0]
print("The result is a", result["object"])
pprint(result["id"])
database_id = result["id"]  # store the database id in a variable for future use

      

# Example usage
book_name = 'conscious business: how to build value through values'
