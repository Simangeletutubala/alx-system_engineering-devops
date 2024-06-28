#!/usr/bin/python3
"""
Module for a recursive function that queries the Reddit API and returns a list
containing the titles of all hot articles for a given subreddit.
"""

import requests
import time

def recurse(subreddit, hot_list=[], after=None):
    """
    Recursively fetches all hot article titles from a subreddit using the Reddit API.

    Args:
        subreddit (str): The name of the subreddit.
        hot_list (list): List to store the titles of hot articles.
        after (str): Token indicating the starting point for the next page of results.

    Returns:
        list or None: List of article titles if successful, None if subreddit is invalid or no articles found.
    """
    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {'User-agent': 'Mozilla/5.0'}
    params = {'limit': 100, 'after': after} if after else {'limit': 100}

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Raise an exception for 4xx/5xx errors

        data = response.json()
        posts = data['data']['children']

        for post in posts:
            hot_list.append(post['data']['title'])

        after = data['data']['after']
        if after:
            time.sleep(1)  # Add a small delay between requests to comply with rate limits
            return recurse(subreddit, hot_list, after)
        else:
            return hot_list if hot_list else None

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

    except KeyError:
        print(f"Error: Unexpected JSON format from Reddit API.")
        return None

# Example usage:
if __name__ == "__main__":
    subreddit = "python"  # Example subreddit
    titles = recurse(subreddit)
    
    if titles:
        print(f"List of titles in r/{subreddit}:\n")
        for index, title in enumerate(titles, 1):
            print(f"{index}. {title}")
    else:
        print(f"No hot articles found in r/{subreddit}.")
