import os
import subprocess
from subprocess import PIPE

def convert_jar(path):
    print("Convert", path)
    subprocess.call(["python", r"C:\Users\Tom\Dropbox\Random\CheerpJ\cheerpj_win_1.4\cheerpj_1.4\cheerpjfy.py", path])

if __name__ == "__main__":
    names = [path for path in os.listdir("./jars") if path.endswith(".jar")]
    failures = []
    for name in sorted(names):
        if not os.path.exists("./jars/" + name + ".js"):
            try:
                convert_jar("./jars/" + name)
            except Exception as e:
                print("Fail:", name)
                print(e)
                failures.append(name)
        else:
            print("Skip", name)
    print("DONE")
    print("failures: ", failures)