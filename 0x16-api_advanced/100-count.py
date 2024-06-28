#!/usr/bin/python3
""" Module for a function that queries the Reddit API recursively."""

import requests

def count_words(subreddit, word_list, after=None, counts={}):
    if after == None:
        url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    else:
        url = f"https://www.reddit.com/r/{subreddit}/hot.json?after={after}"

    headers = {'User-agent': 'Word Counter Bot'}
    response = requests.get(url, headers=headers)
    data = response.json()

    for post in data['data']['children']:
        title = post['data']['title'].lower()
        for word in word_list:
            if word.lower() in title.split():
                counts[word.lower()] = counts.get(word.lower(), 0) + 1

    next_page = data['data']['after']
    if next_page:
        count_words(subreddit, word_list, next_page, counts)
    else:
        sorted_counts = sorted(counts.items(), key=lambda x: (-x[1], x[0]))
        for word, count in sorted_counts:
            print(f"{word}: {count}")

# Example Usage
count_words("python", ["python", "java", "javascript"])

