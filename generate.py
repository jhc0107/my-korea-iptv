import requests
import json

# SBS 실시간 방송 API
api_url = (
    "https://apis.sbs.co.kr/play-api/1.0/onair/channel/S01"
    "?v_type=2&platform=pcweb&protocol=hls&ssl=N"
    "&rscuse=&jwt-token=&sbsmain="
)

headers = {
    "User-Agent": (
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
        "AppleWebKit/605.1.15 (KHTML, like Gecko) "
        "Version/17.0 Mobile/15E148 Safari/604.1"
    ),
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://www.sbs.co.kr/",
}

# SBS API 요청
response = requests.get(
    api_url,
    headers=headers,
    timeout=20
)

print("HTTP Status:", response.status_code)

response.raise_for_status()

data = response.json()

# API 응답 구조 확인
print("===== SBS API RESPONSE =====")
print(json.dumps(data, ensure_ascii=False, indent=2))
print("============================")

# mediasourcelist에서 HLS 주소 찾기
media_list = (
    data
    .get("onair", {})
    .get("source", {})
    .get("mediasourcelist", [])
)

sbs_url = None

for media in media_list:
    media_url = media.get("mediaurl")

    if media_url:
        sbs_url = media_url

        print("화질:", media.get("quality"))
        print("SBS URL:", sbs_url)

        break

# 기존 mediasource 구조도 확인
if not sbs_url:
    media_source = (
        data
        .get("onair", {})
        .get("source", {})
        .get("mediasource", {})
    )

    sbs_url = media_source.get("mediaurl")

# URL을 찾지 못한 경우
if not sbs_url:
    print("SBS HLS 주소를 찾지 못했습니다.")
    raise RuntimeError(
        "SBS API 응답에 mediaurl이 없습니다."
    )

# M3U 파일 생성
with open("korea.m3u", "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n")
    f.write('#EXTINF:-1 tvg-id="SBS" tvg-name="SBS",SBS\n')
    f.write(sbs_url + "\n")

print("korea.m3u 생성 완료")