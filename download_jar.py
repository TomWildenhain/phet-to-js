import urllib.request 
import hashlib
import sys
import os
import shutil
import requests
import re
from conversion_engine import make_temp_dirs

def get_jar_url_from_phet_url(url):
    resp = requests.get(url)
    if resp.status_code == 200:
        match = re.search(r"<a href=\"([^\"]*)\" id=\"simulation-main-link-run-main\"", resp.text)
        if match:
            return "https://phet.colorado.edu" + match.group(1)
        else:
            raise Exception("Failed to find jar file on page %s" % url)
    else:
        raise Exception("Failed to download page %s. Received status code %d." % (url, resp.status_code))


def sha256(filename):
    h  = hashlib.sha256()
    b  = bytearray(128*1024)
    mv = memoryview(b)
    with open(filename, 'rb', buffering=0) as f:
        for n in iter(lambda : f.readinto(mv), 0):
            h.update(mv[:n])
    return h.hexdigest()

jar_or_phet_url = sys.argv[1]
download_path = sys.argv[2]

try:
    if jar_or_phet_url.endswith(".jar"):
        jar_url = jar_or_phet_url
    else:
        jar_url = get_jar_url_from_phet_url(jar_or_phet_url)
    make_temp_dirs()
    temp_name = ""
    jar_path = download_path + "/sim.jar"
    urllib.request.urlretrieve(jar_url, jar_path)
    jar_hash = sha256(jar_path)
    conversion_path = "./temp/conversions/" + jar_hash
    if not os.path.exists(conversion_path):
        os.mkdir(conversion_path)
    new_jar_path = conversion_path + "/sim.jar"
    if os.path.exists(new_jar_path):
        os.remove(jar_path)
    else:
        shutil.move(jar_path, new_jar_path)
    print(jar_hash)
    exit(0)
except Exception as e:
    print(e, file=sys.stderr)
    exit(1)