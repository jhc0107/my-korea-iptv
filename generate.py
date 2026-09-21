import requests
import os
import sys


M3U_FILE = "korea.m3u"

API_URL = (
    "https://apis.sbs.co.kr/play-api/1.0/onair/channel/S01"
    "?v_type=2&platform=pcweb&protocol=hls&ssl=N"
    "&rscuse=&jwt-token=&sbsmain="
)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
        "AppleWebKit/605.1.15 (KHTML, like Gecko) "
        "Version/17.0 Mobile/15E148 Safari/604.1"
    ),
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://www.sbs.co.kr/",
}


print("========================================")
print("SBS 방송 정보 확인")
print("========================================")


# ==========================================
# 기본 M3U 내용
# ==========================================

m3u_header = """#EXTM3U
#EXTINF:-1 tvg-id="SBS" tvg-name="SBS",SBS
"""


# ==========================================
# SBS API 호출
# ==========================================

try:

    response = requests.get(
        API_URL,
        headers=HEADERS,
        timeout=20
    )

    print("HTTP Status:", response.status_code)

    response.raise_for_status()

    data = response.json()

except Exception as e:

    print("")
    print("❌ SBS API 호출 실패")
    print("오류:", e)

    # API 실패해도 빈 M3U 생성
    with open(M3U_FILE, "w", encoding="utf-8") as f:
        f.write(m3u_header)

    print("")
    print("✅ 빈 korea.m3u 생성 완료")
    print("SBS 주소는 다음 실행에서 다시 확인합니다.")

    sys.exit(0)


# ==========================================
# 방송 정보
# ==========================================

onair = data.get("onair", {})
info = onair.get("info", {})
source = onair.get("source", {})

channel_name = info.get("channelname", "SBS")
program_title = info.get("title", "")
onair_text = info.get("onair_text", "")
copyright_yn = info.get("copyright_yn", "")
playon_yn = info.get("playon_yn", "")

print("")
print("채널 :", channel_name)
print("프로그램 :", program_title)
print("저작권 제한 :", copyright_yn)
print("ON AIR 재생 :", playon_yn)
print("안내 :", onair_text)


# ==========================================
# HLS 주소 찾기
# ==========================================

sbs_url = None


# 1. mediasource
media_source = source.get("mediasource", {})

if isinstance(media_source, dict):
    sbs_url = media_source.get("mediaurl")


# 2. mediasourcelist
if not sbs_url:

    media_list = source.get("mediasourcelist", [])

    if isinstance(media_list, list):

        for media in media_list:

            if not isinstance(media, dict):
                continue

            media_url = media.get("mediaurl")

            if media_url:

                sbs_url = media_url

                print(
                    "화질 :",
                    media.get("quality", "")
                )

                break


# ==========================================
# M3U 생성
# ==========================================

try:

    with open(
        M3U_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(m3u_header)

        if sbs_url:

            f.write(sbs_url + "\n")

            print("")
            print("========================================")
            print("✅ SBS HLS 주소 확인")
            print("========================================")
            print(sbs_url)

        else:

            print("")
            print("⚠️ 현재 SBS HLS 주소가 없습니다.")
            print("빈 SBS 항목으로 korea.m3u를 생성합니다.")

            if onair_text:
                print("SBS 안내 :", onair_text)


    print("")
    print("========================================")
    print("✅ korea.m3u 생성 완료")
    print("========================================")

except Exception as e:

    print("")
    print("❌ korea.m3u 생성 실패")
    print("오류:", e)

    sys.exit(1)


print("")
print("작업 완료")