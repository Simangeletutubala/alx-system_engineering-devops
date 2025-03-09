#!/usr/bin/python3
"""
Script to query a list of all hot posts on a given Reddit subreddit.
"""

import requests


def recurse(subreddit, hot_list=[], after="", count=0):
    """
    Recursively retrieves a list of titles of all hot posts
    on a given subreddit.

    Args:
        subreddit (str): The name of the subreddit.
        hot_list (list, optional): List to store the post titles.
                                    Default is an empty list.
        after (str, optional): Token used for pagination.
                                Default is an empty string.
        count (int, optional): Current count of retrieved posts. Default is 0.

    Returns:
        list: A list of post titles from the hot section of the subreddit, 
              or None if subreddit is invalid or an error occurs.
    """
    # Construct the URL for the subreddit's hot posts in JSON format
    url = f"https://www.reddit.com/r/{subreddit}/hot/.json"

    # Define headers for the HTTP request, including User-Agent
    headers = {
        "User-Agent": "python:reddit-hot-posts:v1.0 (by /u/bdov_)"
    }

    # Define parameters for the request, including pagination and limit
    params = {
        "after": after,
        "count": count,
        "limit": 100
    }

    try:
        # Send a GET request to the subreddit's hot posts page
        response = requests.get(url, headers=headers, params=params, allow_redirects=False)

        # If the status code is 404 (subreddit not found), return None
        if response.status_code == 404:
            return None

        # Check for rate-limiting (status code 429) or other errors
        if response.status_code == 429:
            print("Rate limit exceeded, please try again later.")
            return None

        # Parse the JSON response and extract relevant data
        results = response.json().get("data", {})

        # If there's no data, return None
        if not results:
            return None

        after = results.get("after")
        count += results.get("dist")

        # Append post titles to the hot_list
        for c in results.get("children", []):
            hot_list.append(c.get("data", {}).get("title"))

        # If there are more posts to retrieve, recursively call the function
        if after:
            return recurse(subreddit, hot_list, after, count)

        # Return the final list of hot post titles
        return hot_list

    except requests.exceptions.RequestException as e:
        # Catch any request exceptions (e.g., network issues)
        print(f"An error occurred: {e}")
        return None


if __name__ == "__main__":
    # Example usage: Replace 'python' with the desired subreddit
    subreddit = "python"
    hot_posts = recurse(subreddit)

    if hot_posts is not None:
        for post in hot_posts:
            print(post)
    else:
        print("No posts found or there was an error.")
