#!/usr/bin/python3
""" Module for a function that queries the Reddit API recursively."""

import requests

def count_words(subreddit, word_list, after=None, counts={}):
    """
    Recursively counts occurrences of specified words in titles of hot posts from a subreddit.

    Args:
    - subreddit (str): The name of the subreddit to fetch posts from.
    - word_list (list): A list of words to count occurrences in post titles.
    - after (str): The 'after' token used for pagination (default=None).
    - counts (dict): Dictionary to store word counts (default={}). Used internally for recursion.

    Returns:
    - None: Prints word counts in descending order of occurrence.
    """
    if after is None:
        url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    else:
        url = f"https://www.reddit.com/r/{subreddit}/hot.json?after={after}"

    headers = {'User-agent': 'Word Counter Bot'}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)

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

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

# Example Usage
if __name__ == "__main__":
    count_words("python", ["python", "java", "javascript"])
