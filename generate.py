import requests
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


# ==========================================
# 고정 채널
# ==========================================

KBS1_URL = "http://koreatv.dothome.co.kr/kbs1.php"
KBS2_URL = "http://koreatv.dothome.co.kr/kbs2.php"
KBS24_URL = "https://news24.gscdn.kbs.co.kr/news24-02/news24-02_hd.m3u8"
MBC_URL = "http://vod.mpmbc.co.kr:1935/live/encoder-tv/playlist.m3u8"
SBS_BACKUP_URL = "http://110.42.54.62:8080/live/sbs.m3u8"
EBS1_URL = "http://ebsonairios.ebs.co.kr/groundwavetablet500k/tablet500k/playlist.m3u8"


# ==========================================
# SBS API에서 현재 주소 가져오기
# ==========================================

sbs_url = None

print("========================================")
print("SBS 방송 정보 확인")
print("========================================")

try:

    response = requests.get(
        API_URL,
        headers=HEADERS,
        timeout=20
    )

    print("HTTP Status:", response.status_code)

    response.raise_for_status()

    data = response.json()

    onair = data.get("onair", {})
    info = onair.get("info", {})
    source = onair.get("source", {})

    print("채널 :", info.get("channelname", "SBS"))
    print("프로그램 :", info.get("title", ""))
    print("저작권 제한 :", info.get("copyright_yn", ""))
    print("ON AIR 재생 :", info.get("playon_yn", ""))
    print("안내 :", info.get("onair_text", ""))

    # mediasource
    media_source = source.get("mediasource", {})

    if isinstance(media_source, dict):
        sbs_url = media_source.get("mediaurl")

    # mediasourcelist
    if not sbs_url:

        media_list = source.get("mediasourcelist", [])

        if isinstance(media_list, list):

            for media in media_list:

                if not isinstance(media, dict):
                    continue

                media_url = media.get("mediaurl")

                if media_url:
                    sbs_url = media_url
                    break

except Exception as e:

    print("")
    print("⚠️ SBS API 호출 실패")
    print("오류:", e)


# ==========================================
# SBS 주소가 없으면 백업 주소 사용
# ==========================================

if sbs_url:

    print("")
    print("✅ SBS 실시간 주소 확인")
    print(sbs_url)

else:

    print("")
    print("⚠️ SBS 실시간 주소를 가져오지 못했습니다.")
    print("→ SBS 기본 주소 대신 백업 주소를 사용합니다.")

    sbs_url = SBS_BACKUP_URL


# ==========================================
# M3U 생성
# ==========================================

try:

    with open(
        M3U_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        f.write("#EXTM3U\n\n")

        # KBS1
        f.write(
            '#EXTINF:-1 tvg-id="KBS1.kr" '
            'tvg-name="KBS 1TV" '
            'group-title="지상파",KBS 1TV\n'
        )
        f.write(KBS1_URL + "\n\n")

        # KBS2
        f.write(
            '#EXTINF:-1 tvg-id="KBS2.kr" '
            'tvg-name="KBS 2TV" '
            'group-title="지상파",KBS 2TV\n'
        )
        f.write(KBS2_URL + "\n\n")

        # KBS NEWS 24
        f.write(
            '#EXTINF:-1 tvg-id="KBS24.kr" '
            'tvg-name="KBS NEWS 24" '
            'group-title="지상파",KBS NEWS 24\n'
        )
        f.write(KBS24_URL + "\n\n")

        # MBC
        f.write(
            '#EXTINF:-1 tvg-id="MBC.kr" '
            'tvg-name="MBC" '
            'group-title="지상파",MBC\n'
        )
        f.write(MBC_URL + "\n\n")

        # SBS
        f.write(
            '#EXTINF:-1 tvg-id="SBS.kr" '
            'tvg-name="SBS" '
            'group-title="지상파",SBS\n'
        )
        f.write(sbs_url + "\n\n")

        # EBS1
        f.write(
            '#EXTINF:-1 tvg-id="EBS1.kr" '
            'tvg-name="EBS 1TV" '
            'group-title="지상파",EBS 1TV\n'
        )
        f.write(EBS1_URL + "\n")

    print("")
    print("========================================")
    print("✅ korea.m3u 생성 완료")
    print("========================================")

except Exception as e:

    print("")
    print("❌ korea.m3u 생성 실패")
    print("오류:", e)

    sys.exit(1)