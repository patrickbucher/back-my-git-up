#!/usr/bin/env python3

from datetime import datetime
import json
import os
import sys

import requests
from suitable import Api


def main():
    if len(sys.argv) < 2:
        raise ValueError(f'usage: {sys.argv[0]} [token] [target]')
    token, target = sys.argv[1], sys.argv[2]

    if os.path.exists(target):
        if not os.path.isdir(target):
            raise ValueError(f'{target} is not a directory')
    else:
        os.mkdir(target)

    repos = fetch_repos(sys.argv[1])
    repos = to_url_name_tuples(repos)

    ansible = Api(['localhost'])
    for (name, url) in repos:
        dest = os.path.join(target, name)
        print(f'cloning {url} to {dest}... ', end='')
        start = datetime.now()
        ansible.git(repo=url, dest=dest, accept_hostkey=True)
        stop = datetime.now()
        seconds = (stop - start).total_seconds()
        print(f'done in {seconds:.2f} seconds')


def to_url_name_tuples(repos):
    tuples = []
    names = [r.split('/')[-1] for r in repos]
    urls = [f'git@github.com:{r}.git' for r in repos]
    for name, url in zip(names, urls):
        tuples.append((name, url))
    return tuples


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
