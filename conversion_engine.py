import requests
import re
import urllib.request 
import os
import hashlib
import shutil
import subprocess

CHEERPJ_PATH = "./cheerpj/cheerpj_win_1.4/cheerpjfy.py"

class ConversionEngineException(Exception):
    pass

def download_jar(jar_or_phet_url) -> None:
    make_temp_dirs()
    status = get_download_status(jar_or_phet_url)
    if status and not status.error:
        return
    dowload_path = _get_download_path(jar_or_phet_url)
    if not os.path.exists(dowload_path):
        os.mkdir(dowload_path)
    _clear_directory(dowload_path)
    out_file = open(dowload_path + "/out.txt", "w")
    err_file = open(dowload_path + "/err.txt", "w")
    subprocess.Popen(["python", "download_jar.py", jar_or_phet_url, dowload_path], stdout=out_file, stderr=err_file)

def _clear_directory(path):
    for file in os.listdir(path):
        os.remove(path + "/" + file)

class DownloadStatus:
    def __init__(self):
        self.finished = False
        self.hash = None
        self.error = None

class ConversionStatus:
    def __init__(self):
        self.console_text = ""
        self.finished = False

def get_download_status(jar_or_phet_url) -> DownloadStatus:
    download_path = _get_download_path(jar_or_phet_url)
    out_path = download_path + "/out.txt"
    err_path = download_path + "/err.txt"
    if not os.path.exists(download_path):
        return None
    status = DownloadStatus()
    if os.path.exists(out_path):
        out = _read_file(out_path).strip()
        err = _read_file(err_path).strip()
        if err:
            status.error = err
        elif out:
            status.hash = out
            status.finished = True
    return status

def _get_download_path(jar_or_phet_url):
    url_hash = _sha256str(jar_or_phet_url)
    return "./temp/downloads/%s" % url_hash

def _sha256str(string):
    import hashlib
    h = hashlib.sha256()
    h.update(string.encode())
    return str(h.hexdigest())

def convert_jar(jar_hash) -> None:
    make_temp_dirs()
    conversion_path = "./temp/conversions/" + jar_hash
    jar_path = conversion_path + "/sim.jar"
    if not os.path.exists(jar_path):
        return None

    out_file = open(conversion_path + "/out.txt", "w")
    err_file = open(conversion_path + "/err.txt", "w")
    subprocess.Popen(["python", CHEERPJ_PATH, jar_path], stdout=out_file, stderr=err_file)
    

def get_conversion_status(jar_hash) -> ConversionStatus:
    pass

def _read_file(path):
    with open(path, 'r') as file:
        return file.read()

def make_temp_dirs():
    paths = ["./temp", "./temp/jars", "./temp/conversions", "./temp/downloads"]
    for path in paths:
        if not os.path.exists(path):
            os.mkdir(path)


if __name__ == "__main__":
    url = "https://phet.colorado.edu/en/simulation/legacy/beta-decay"
    download_jar(url)
    status = get_download_status(url)
    import time
    while not status.finished:
        status = get_download_status(url)
        print(status)
        time.sleep(1)
    convert_jar(status.hash)
    print(status.hash)

