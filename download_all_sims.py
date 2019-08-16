import urllib.request 
import hashlib
import sys
import os
import shutil
import requests
import re

def get_simulation_urls():
    resp = requests.get("https://phet.colorado.edu/en/simulations")
    matches = re.findall(r"<a href=\"([^\"]*)\" class=\"simulation-link\">", resp.text)
    return {"https://phet.colorado.edu" + match for match in matches}

def get_jar_url_from_phet_url(url):
    resp = requests.get(url)
    match = re.search(r"<a href=\"([^\"]*)\" id=\"simulation-main-link-run-main\"", resp.text)
    if match:
        return "https://phet.colorado.edu" + match.group(1)
    return None

def download_jar(url):
    name = url[url.rfind("/")+1:]
    print("Downloading", name)
    urllib.request.urlretrieve(jar_url, "./jars/" + name)

if __name__ == "__main__":
    jar_urls = set()
    for url in get_simulation_urls():
        jar_url = get_jar_url_from_phet_url(url)
        if jar_url and jar_url.endswith(".jar"):
            print(jar_url)
            download_jar(jar_url)
            jar_urls.add(jar_url)