#!/usr/bin/python3
"""
Script that queries the number of subscribers on a given Reddit subreddit.
"""

import requests

def number_of_subscribers(subreddit):
    """
    Return the total number of subscribers on a given subreddit.

    Args:
    - subreddit (str): The name of the subreddit (e.g., 'learnpython').

    Returns:
    - int: The total number of subscribers on the subreddit.
           Returns 0 if the subreddit does not exist or an error occurs.
    """
    url = f"https://www.reddit.com/r/{subreddit}/about.json"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(url, headers=headers, allow_redirects=False)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
        
        data = response.json()
        subscribers = data['data']['subscribers']
        return subscribers
    
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
        return 0
    
    except KeyError:
        print(f"Subreddit '{subreddit}' does not exist or has no subscriber data.")
        return 0

# Example usage:
if __name__ == "__main__":
    subreddit = "learnpython"
    num_subscribers = number_of_subscribers(subreddit)
    print(f"Number of subscribers on r/{subreddit}: {num_subscribers}")
