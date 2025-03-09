#!/usr/bin/python3
"""
Script to query a list of all hot posts on a given Reddit subreddit.
"""

import requests

def recurse(subreddit, hot_list=[]):
    """
    Recursively retrieves a list of titles of all hot posts
    on a given subreddit.

    Args:
        subreddit (str): The name of the subreddit.
        hot_list (list, optional): List to store the post titles.
                                    Default is an empty list.

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

    # Define parameters for the request, including pagination
    params = {
        "after": None,  # Initialize as None, will change after first request
        "limit": 100
    }

    try:
        # Send a GET request to the subreddit's hot posts page
        response = requests.get(url, headers=headers, params=params, allow_redirects=False)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

    # If the status code is 404 (subreddit not found), return None
    if response.status_code == 404:
        print("Invalid subreddit.")
        return None
    
    # Check for redirects (e.g., if the subreddit is invalid, Reddit might redirect to search results)
    if response.status_code == 301 or response.status_code == 302:
        print("Invalid subreddit, redirecting to search.")
        return None

    # Parse the JSON response and extract relevant data
    try:
        results = response.json().get("data", {})
    except ValueError:
        print("Error: Could not parse the response as JSON.")
        return None

    # If no posts are found, return None
    if not results:
        return None

    after = results.get("after")
    
    # Append post titles to the hot_list
    for post in results.get("children", []):
        hot_list.append(post.get("data", {}).get("title"))

    # If there are more posts to retrieve, recursively call the function
    if after:
        params["after"] = after
        return recurse(subreddit, hot_list)

    # Return the final list of hot post titles
    return hot_list


# Example usage:
if __name__ == "__main__":
    subreddit = "python"  # Replace with the desired subreddit
    hot_posts = recurse(subreddit)

    if hot_posts:
        print("Hot posts:")
        for post in hot_posts:
            print(post)
    else:
        print("No posts found or an error occurred.")
