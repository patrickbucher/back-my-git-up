#!/usr/bin/env python3

import json
import sys

import requests


def main():
    if len(sys.argv) < 2:
        raise ValueError(f'usage: {sys.argv[0]} [token]')

    print(fetch_repos(sys.argv[1]))


def fetch_repos(token):
    repo_endpoint = 'https://api.github.com/user/repos'
    headers = {'Authorization': 'token ' + sys.argv[1]}

    page = 1
    repo_names = set([])
    while True:
        query_params = {'affiliation': 'owner', 'per_page': '20', 'page': page}
        query_params = [f'{k}={v}' for k, v in query_params.items()]
        query_string = '&'.join(query_params)
        query_url = f'{repo_endpoint}?{query_string}'

        r = requests.get(query_url, headers=headers)
        payload = json.loads(r.text)
        new_repo_names = extract_names(payload)
        if not new_repo_names:
            break
        repo_names.update(new_repo_names)
        page += 1

    return sorted(list(repo_names))


def extract_names(payload):
    repo_names = []
    for repo in payload:
        repo_names.append(repo['full_name'])
    return repo_names

if __name__ == '__main__':
    main()
