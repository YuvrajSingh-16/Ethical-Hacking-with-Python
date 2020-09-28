#!/usr/bin/env python

import requests


def download(url):
    get_response = requests.get(url)
    print(get_response.content)
    file_name = url.split("/")[-1]
    with open(file_name, "wb") as out_file:
        out_file.write(get_response.content)


download("https://lh3.googleusercontent.com/0NcqVhsILMwH082enTDfSjEFddKcXqxJrd_4dMiJGIVuh1PIfyozlwc7HGe25F5kg3nl1cSB0KaIQ1DRkSsAwZ8Bw4VBsrLU=s688")