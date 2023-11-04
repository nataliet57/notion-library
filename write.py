from notion_client import Client
from pprint import pprint

notion_token = 'secret_EZ6qGNjHN3YE6opz5y7ke3ABQlTHWnf2dYuYz2ZTehr'
notion_page_id = '?v=940aceb5f587401ab90ce0ba1de53a9a'

def write_text(client, page_id, text, type):
    client.blocks.children.append(
        block_id=page_id,
        children=[
            {
                "object": "block",
                "type": type,
                type: {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": text
                            }
                        }
                    ]
                }
            }
        ]
    )

def main():
    client = Client(auth=notion_token)

    write_text(client, notion_page_id, 'Hello World!', 'to_do')

if __name__ == '__main__':
    main()
  