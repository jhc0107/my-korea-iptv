import requests
import json

url = (
    "https://apis.sbs.co.kr/play-api/1.0/onair/channel/S01"
    "?v_type=2&platform=pcweb&protocol=hls&ssl=N"
    "&rscuse=&jwt-token=&sbsmain="
)

headers = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://www.sbs.co.kr/",
}

r = requests.get(url, headers=headers, timeout=20)

print("HTTP:", r.status_code)

data = r.json()

source = data.get("onair", {}).get("source", {})

print("channel:", source.get("channel"))
print("stream:", source.get("stream"))

print("")
print("mediasource:")
print(json.dumps(
    source.get("mediasource"),
    ensure_ascii=False,
    indent=2
))

print("")
print("mediasourcelist:")
print(json.dumps(
    source.get("mediasourcelist"),
    ensure_ascii=False,
    indent=2
))
