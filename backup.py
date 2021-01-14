#!/usr/bin/env python3

import json
import sys

import requests


def main():
    repo_endpoint = 'https://api.github.com/user/repos'
    r = requests.get(
        repo_endpoint+'?affiliation=owner&per_page=100',
        headers={'Authorization': 'token ' + sys.argv[1]}
    )
    payload = json.loads(r.text)
    extract_names(payload)


def extract_names(payload):
    for repo in payload:
        print(repo['full_name'])

if __name__ == '__main__':
    main()
