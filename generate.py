import requests

# SBS 실시간 방송 API (S01 채널 ID)
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
    )
}

sbs_url = None

try:
    response = requests.get(api_url, headers=headers, timeout=20)
    response.raise_for_status()  # 404, 500 등 에러 시 예외 발생
    data = response.json()
    
    # HLS 주소 추출
    sbs_url = data.get("onair", {}).get("source", {}).get("mediasource", {}).get("mediaurl")

except requests.exceptions.HTTPError as e:
    print(f"[경고] SBS API HTTP 에러 발생: {e}")
except Exception as e:
    print(f"[경고] SBS 주소를 가져오는 데 실패했습니다: {e}")

# M3U 파일 생성
with open("korea.m3u", "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n")
    if sbs_url:
        f.write("#EXTINF:-1 tvg-id=\"SBS\" tvg-name=\"SBS\",SBS\n")
        f.write(sbs_url + "\n")
        print("korea.m3u 생성 완료 (SBS 포함)")
    else:
        print("korea.m3u 생성 완료 (SBS 주소 수집 실패로 제외됨)")
