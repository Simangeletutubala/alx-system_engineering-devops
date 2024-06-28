#!/usr/bin/python3
'''
    this module contains the function top_ten
'''
import requests

def top_ten(subreddit):
    """
    Fetches and prints the titles of the top 10 hot posts from a subreddit.

    Args:
    - subreddit (str): The name of the subreddit to fetch posts from.

    Prints:
    - Prints the titles of the top 10 hot posts from the specified subreddit.
      If there's an error or the subreddit is invalid, prints 'None'.
    """
    url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit=10"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)

        if response.status_code == 200:
            for post in response.json()['data']['children']:
                print(post['data']['title'])
        else:
            print(None)
    
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        print(None)

# Example Usage
if __name__ == "__main__":
    top_ten("python")
