#!/usr/bin/env python

import requests


def request(url):
    try:
        return requests.get(url)
    except requests.exceptions.ConnectionError:
        return "[-] Check the link again."


target_url = "http://10.0.2.24/mutillidae/index.php?page=dns-lookup.php"
response = request(target_url)
print(response.content)