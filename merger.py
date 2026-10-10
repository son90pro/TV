import urllib.request
import re

# Danh sách 10 nguồn M3U của anh Sơn (Tivi Vip 1 đã đưa lên đầu)
SOURCES = [
    {
        "name": "Tivi Vip 1",
        "url": "https://raw.githubusercontent.com/son90pro/TV/refs/heads/main/Tivi.m3u"
    },
    {
        "name": "Bia Ôm TV",
        "url": "https://raw.githubusercontent.com/son90pro/Bia-Om-TV/refs/heads/main/biaom_live.m3u"
    },
    {
        "name": "Khán Đài TV",
        "url": "https://raw.githubusercontent.com/son90pro/KhanDai-TV/refs/heads/main/playlist.m3u"
    },
    {
        "name": "Gà Vàng 33",
        "url": "https://raw.githubusercontent.com/son90pro/GaVang-TV/refs/heads/main/gavang33.m3u"
    },
    {
        "name": "Phá Làng TV",
        "url": "https://raw.githubusercontent.com/son90pro/Pha-Lang---TV/refs/heads/main/phalang.m3u"
    },
    {
        "name": "Chuối Chiên TV",
        "url": "https://raw.githubusercontent.com/son90pro/TheThaoVip/refs/heads/main/playlist.m3u"
    },
    {
        "name": "S8TV",
        "url": "https://raw.githubusercontent.com/son90pro/S8TV/refs/heads/main/s8tv.m3u"
    },
    {
        "name": "Xôi chè TV",
        "url": "https://raw.githubusercontent.com/son90pro/Xoi-Che-TV/refs/heads/main/xoiche.m3u"
    },
    {
        "name": "Bông lau TV",
        "url": "https://raw.githubusercontent.com/son90pro/Bong-Lau-TV/refs/heads/main/playlist.m3u"
    },
    {
        "name": "Sao Kê TV",
        "url": "https://raw.githubusercontent.com/son90pro/Sao-Ke--TV/refs/heads/main/saoketv.m3u"
    }
]

OUTPUT_FILE = "TheThao_Full.m3u"

def combine_m3u():
    output_lines = ["#EXTM3U\n"]
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

    for src in SOURCES:
        group_name = src["name"]
        url = src["url"]
        print(f"Đang tải và xử lý: {group_name}...")
        
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=15) as response:
                content = response.read().decode('utf-8', errors='ignore')
                lines = content.splitlines()

            for line in lines:
                line = line.strip()
                # Bỏ qua dòng trống hoặc thẻ #EXTM3U thừa
                if not line or line.startswith("#EXTM3U"):
                    continue
                
                if line.startswith("#EXTINF:"):
                    # Nếu kênh đã có group-title thì thay thế bằng tên nhóm mới
                    if 'group-title="' in line:
                        line = re.sub(r'group-title="[^"]*"', f'group-title="{group_name}"', line)
                    else:
                        # Nếu chưa có group-title thì chèn vào ngay trước dấu phẩy tên kênh
                        line = re.sub(r'(#EXTINF:[^,]*)(,)', rf'\1 group-title="{group_name}"\2', line, count=1)
                        if 'group-title="' not in line:
                            line = line.replace("#EXTINF:", f'#EXTINF: group-title="{group_name}"', 1)
                
                output_lines.append(line + "\n")
                
        except Exception as e:
            print(f"Lỗi khi lấy dữ liệu từ {group_name}: {e}")

    # Xuất ra file M3U tổng hợp
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.writelines(output_lines)
    print(f"\n=> Hoàn tất! File tổng hợp được lưu tại: {OUTPUT_FILE}")

if __name__ == "__main__":
    combine_m3u()
    
