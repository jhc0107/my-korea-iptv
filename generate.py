import requests
import json
import os
import sys

# ==========================================
# SBS 실시간 방송 API
# ==========================================

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

M3U_FILE = "korea.m3u"


# ==========================================
# SBS API 호출
# ==========================================

try:
    response = requests.get(
        api_url,
        headers=headers,
        timeout=20
    )

    print("HTTP Status:", response.status_code)

    response.raise_for_status()

    data = response.json()

except Exception as e:
    print("SBS API 호출 실패")
    print(e)

    # 기존 M3U 유지
    if os.path.exists(M3U_FILE):
        print("기존 korea.m3u를 그대로 유지합니다.")
        sys.exit(0)
    else:
        sys.exit(1)


# ==========================================
# 기본 정보 확인
# ==========================================

onair = data.get("onair", {})
info = onair.get("info", {})
source = onair.get("source", {})

channel_name = info.get("channelname", "SBS")
program_title = info.get("title", "")
onair_text = onair.get("onair_text", "")

print("")
print("===== SBS 방송 정보 =====")
print("채널 :", channel_name)
print("프로그램 :", program_title)
print("안내 :", onair_text)
print("========================")
print("")


# ==========================================
# HLS 주소 찾기
# ==========================================

sbs_url = None

# 1. mediasource 확인
media_source = source.get("mediasource", {})

if isinstance(media_source, dict):
    sbs_url = media_source.get("mediaurl")


# 2. mediasourcelist 확인
if not sbs_url:
    media_list = source.get("mediasourcelist", [])

    if isinstance(media_list, list):
        for media in media_list:

            if not isinstance(media, dict):
                continue

            media_url = media.get("mediaurl")

            if media_url:
                sbs_url = media_url

                print("화질 :", media.get("quality"))
                break


# ==========================================
# 스트림이 없는 경우
# ==========================================

if not sbs_url:

    print("⚠️ 현재 SBS HLS 스트림 주소가 없습니다.")

    if onair_text:
        print("SBS 안내 :", onair_text)

    print("")
    print("기존 korea.m3u를 변경하지 않습니다.")

    # 중요:
    # GitHub Actions가 실패하지 않도록 정상 종료
    sys.exit(0)


# ==========================================
# HLS 주소 확인
# ==========================================

print("================================")
print("SBS HLS 주소:")
print(sbs_url)
print("================================")


# ==========================================
# M3U 생성
# ==========================================

try:

    with open(M3U_FILE, "w", encoding="utf-8") as f:

        f.write("#EXTM3U\n")

        f.write(
            '#EXTINF:-1 tvg-id="SBS" '
            'tvg-name="SBS",SBS\n'
        )

        f.write(sbs_url + "\n")

    print("")
    print("✅ korea.m3u 생성 완료")

except Exception as e:

    print("M3U 파일 생성 실패")
    print(e)

    sys.exit(1)