import requests
from datetime import datetime
import hmac
import hashlib
import base64
import xml.etree.ElementTree as ET
import os

storageAccount = os.getenv("AZR_STORAGE_ACCOUNT")
resource = os.getenv("AZR_STORAGE_RESOURCE")
API_SECRET = os.getenv("AZR_STORAGE_API_KEY")


VERB = "GET"

params = {}#{"restype": "container", "comp": "list"}



headers = {}
headers["x-ms-version"] = "2014-02-14"
headers["x-ms-date"] = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
hdrs = [f"{k}:{v}" for k, v in headers.items() if k.startswith("x-ms")]
hdrs.sort()
canonicalizedHeaders = "\n".join(hdrs)
prms = [f"{k}:{v}" for k, v in params.items()]
prms.sort()
canonicalizedResource = f"/{storageAccount}/{resource}" 
if prms:
    canonicalizedResource +=  "\n" +  "\n".join(prms)

contentLength = ""
contentMD5 = ""

stringToSign = VERB + "\n\n\n" + contentLength + "\n" + contentMD5 + "\n" + "\n\n\n\n\n\n\n" + canonicalizedHeaders + "\n" + canonicalizedResource
signature = hmac.new(base64.b64decode(API_SECRET), msg=bytes(stringToSign , 'utf-8'), digestmod=hashlib.sha256).digest()
key = base64.b64encode(signature).decode("utf-8")
headers["Authorization"] = f"SharedKey {storageAccount}:{key}"


dat = requests.get(f"https://{storageAccount}.blob.core.windows.net/{resource}", params=params, headers=headers)
print(dat.headers)

# File I/O (e.g. download) like this:
with open("dl.dat", "wb") as out:
    for chunk in dat.iter_content(chunk_size=1024):
        if chunk:
            out.write(chunk)


# list queries etc return XML:
# response = ET.fromstring(dat.text)

