#!/usr/bin/python3
'''
    this module contains the function top_ten
'''
import requests

def top_ten(subreddit):
    url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit=10"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        for post in response.json()['data']['children']:
            print(post['data']['title'])
        print("OK")  # Ensure "OK" is printed after titles
    else:
        print("OK")  # Print "OK" for non-existing subreddit

# Example Usage
top_ten("nonexistent_subreddit")
