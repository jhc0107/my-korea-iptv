import requests

# SBS 실시간 방송 API
api_url = (
    "https://apis.sbs.co.kr/play-api/1.0/onair/channel/SBS"
    "?v_type=2&platform=pcweb&protocol=hls&ssl=N"
    "&rscuse=&jwt-token=&sbsmain="
)

headers = {
    "User-Agent": (
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
        "AppleWebKit/605.1.15 (KHTML, like Gecko) "
        "Version/17.0 Mobile/15E148 Safari/604.1"
    )
}

response = requests.get(api_url, headers=headers, timeout=20)
response.raise_for_status()

data = response.json()

# 현재 SBS 실시간 HLS 주소
sbs_url = data["onair"]["source"]["mediasource"]["mediaurl"]

print("SBS URL:")
print(sbs_url)

# M3U 파일 생성
with open("korea.m3u", "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n")
    f.write("#EXTINF:-1 tvg-id=\"SBS\" tvg-name=\"SBS\",SBS\n")
    f.write(sbs_url + "\n")

print("korea.m3u 생성 완료")
