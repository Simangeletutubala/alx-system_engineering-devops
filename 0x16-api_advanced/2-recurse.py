#!/usr/bin/python3
"""Contains recurse function"""
import requests

def recurse(subreddit, hot_list=[], after=None):
    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {'User-agent': 'Mozilla/5.0'}
    params = {'limit': 100, 'after': after} if after else {'limit': 100}

    response = requests.get(url, headers=headers, params=params)

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
        return None
