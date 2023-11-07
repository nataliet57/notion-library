## Book Ratings Notion Database Populator
## Overview
This script is designed to populate a Notion database with book ratings data from a CSV file. It uses your Notion API key and a pre-existing table in Notion to update the database with entries for each book that received at least one rating. The script normalizes book names for extra whitespace and capitalization, calculates the average rating from all members, and counts the number of "Favorites" (books rated 5 stars).

Prerequisites
Python 3.x
Notion API Key
Existing Notion Database/Table
Installation
Clone the repository to your local machine:

bash
Copy code
git clone https://github.com/nataliet57/notion-library.git
Install required Python packages:

### Copy code
pip install requests pandas notion_client os unicodedata

### Usage
Run the script:
python script.py
Enter the path to the CSV file containing book ratings data when prompted.

The script will update your Notion database with the book ratings data. Duplicate entries are automatically handled.

CSV File Format
The CSV file should have the following columns:

Book Name
Member Name
Rating: Rating given by a member (between 1 and 5)
Each row in the Notion database will include the following information:

https://github.com/nataliet57/notion-library/assets/30819550/ab5e2864-34de-40b9-ba82-8f793e124e6f


Note
Consecutive runs of the script with the same CSV file and an existing database will not create duplicate rows. The script merges the existing database with the new data and removes entries that are already in the Notion database.

# Challenges & API
The biggest challenge I had was navigating how to update an existing table without entering duplicate books for another CSV file. I had 2 approaches of doing this, using the UPDATE API action or deleting the table and inserting a new one. To elaborate, in my first implementation, I would search if the book exists in the database by querying using the filter function. If it exists, then increment the count column by 1, and recalculate the average. If the rating is 5, then update the perfect rating column. If it doesn't exist, create a new row in the table. It was straight forward querying the book name column on the  existing Notion database to check if the book name existed. However, I ran into a problem where if I queried a book name that contained words of a longer book name, it would return multiple books. For example, if I had a book called Harry Potter, and another book calld Harry Potter and the Sorcerer's Stone, the script would return two book names, and there would be no way to identify which book to update. In addition, I had trouble trying to navigate my way around the PATCH operation in the documentation. I felt like it was catered towards using Javascript as the programming language. One suggestion would be to include different languages such as Python, Javascript, or Golang in the API documentation. 

After sinking a bit too much time into finding a way to fix it, I opted for the second option. Although it had a larger time and space complexity O(N), this straight forward solution was easier to implement. I used the python writer package to get every row in the Notion db to write it to the csv with the new books that will be populated into the database. 

# Resources
I familiarized myself with the Notion API by watching a 5 minute video on how to use the Notion API here: https://danisler.com/dev/notion-in-5-minutes. I found it to be extremely helpful and made the entire process a lot more seamless. Here is the list of packages I worked with upon development

1. Pandas: A powerful data analysis and manipulation library for Python. It provides data structures like DataFrame for efficient data handling.
2. PPrint (Pretty Print): A module for pretty-printing data structures and objects in Python. It enhances the readability of printed output.
3. OS: The os module provides a way of interacting with the operating system. It is used for file operations, such as checking file existence and manipulation of file paths.
4. Notion Client: The notion_client library provides a Python client for the Notion API. It is used to interact with Notion databases, allowing you to create, retrieve, and update Notion objects.
5. CSV: A module in Python's standard library for reading and writing CSV files. It provides functionality to read data from and write data to CSV files.
6. Requests: A popular HTTP library for making requests in Python. It simplifies making HTTP requests and handles the complexities of various protocols.
