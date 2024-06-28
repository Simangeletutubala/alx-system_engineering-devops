#!/usr/bin/python3
"""Contains recurse function"""
import requests

def recurse(subreddit, hot_list=[], after=None):
    """
    Recursively fetches titles of hot posts from a subreddit.

    Args:
    - subreddit (str): The name of the subreddit to fetch posts from.
    - hot_list (list): A list to accumulate titles of hot posts (default=[]).
    - after (str): The 'after' token used for pagination (default=None).

    Returns:
    - list or None: A list of titles of hot posts from the subreddit.
                    Returns None if the subreddit is invalid or an error occurs.
    """
    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {'User-agent': 'Mozilla/5.0'}
    params = {'limit': 100, 'after': after} if after else {'limit': 100}

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)

        if response.status_code == 200:
            data = response.json()
            posts = data['data']['children']

            for post in posts:
                hot_list.append(post['data']['title'])

            after = data['data']['after']

            if after:
                return recurse(subreddit, hot_list, after)
            else:
                return hot_list
        else:
            print(f"Request failed with status code: {response.status_code}")
            return None
    
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

# Example usage:
if __name__ == "__main__":
    subreddit = "python"
    posts = recurse(subreddit)
    if posts:
        for idx, title in enumerate(posts, start=1):
            print(f"{idx}. {title}")
    else:
        print(f"Failed to fetch posts from r/{subreddit}")
