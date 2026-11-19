#!/usr/bin/env python3
"""Quay video HDSD app Meeting — 2 máy ảo (L = chủ trì namdangit, R = người tham gia thuydt), push THẬT từ cổng dev.

Động cơ theo BƯỚC (skill video-creator-docs): act chạy lúc bắt đầu bước, bước sau chỉ bắt đầu khi lời bước trước đọc
xong (+0,35s). Ghi timeline.json (mốc bước, lời, chạm, khung vàng) cho build.py dựng.
Chạy: python3 record.py   (2 máy đã mở app, L ở Meeting › Tổng quan, R ở màn hình chính)
"""
import hashlib, json, os, signal, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
M = '/Users/dnsnamdang/.npm/_npx/e41f45e886283da6/node_modules/@mobilenext/mobilecli-darwin-arm64/mobilecli-darwin-arm64'
DEV = {'L': 'D0C0E274-8590-4D39-9196-CD5D535338DD', 'R': 'FE6D3E86-49A0-4D92-AFDD-58C5DAF761BB'}
TTS = os.path.join(HERE, 'ttsenv', 'bin', 'edge-tts')
CACHE = os.path.join(HERE, 'tts-cache')
os.makedirs(CACHE, exist_ok=True)

NAME = 'Họp triển khai kế hoạch tháng 11'
GOAL = 'Phân công đầu việc và mốc hoàn thành trong tháng'

# ── thao tác ───────────────────────────────────────────────────────────────
T0 = None
taps = []


def now():
    return time.time() - T0 if T0 else 0.0


def mcli(*a):
    return subprocess.run([M, *a], capture_output=True, text=True).stdout


def tap(d, x, y):
    taps.append({'dev': d, 'x': x, 'y': y, 't': round(now(), 3)})
    mcli('io', 'tap', f'{x},{y}', '--device', DEV[d])


def text(d, s):
    mcli('io', 'text', s, '--device', DEV[d])


def swipe(d, x1, y1, x2, y2, dur=None):
    mcli('io', 'swipe', f'{x1},{y1},{x2},{y2}', '--device', DEV[d], *(['--duration', str(dur)] if dur else []))


def home(d):
    mcli('io', 'button', 'HOME', '--device', DEV[d])


def labels(d):
    out = []

    def walk(o):
        if isinstance(o, dict):
            l = (o.get('label') or o.get('text') or o.get('name') or '').strip()
            r = o.get('rect') or {}
            if l and r:
                out.append((l, r))
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    try:
        walk(json.loads(mcli('dump', 'ui', '--device', DEV[d])))
    except Exception:
        pass
    return out


def ocr(d):
    f = os.path.join(HERE, f'_ocr_{d}.png')
    subprocess.run(['xcrun', 'simctl', 'io', DEV[d], 'screenshot', f], capture_output=True)
    out = subprocess.run([os.path.join(HERE, 'ocr'), f], capture_output=True, text=True).stdout
    rows = []
    for line in out.splitlines():
        try:
            box, t = line.split('\t', 1)
            x, y, bw, bh = map(float, box.split())
            rows.append((x * 402, y * 874, bw * 402, bh * 874, t))
        except ValueError:
            pass
    return rows


def tap_where(d, pick, fallback, tries=8):
    """pick(rows) -> (x, y) | None ; thử lại vì danh sách còn đang tải."""
    for _ in range(tries):
        hit = pick(ocr(d))
        if hit:
            print(f'   OCR {d} → {hit}', flush=True)
            return tap(d, *hit)
        w(0.7)
    print(f'   OCR {d} không thấy, bấm mặc định {fallback}', flush=True)
    tap(d, *fallback)


KEY = 'trien khai'


def nz(t):
    import unicodedata
    t = unicodedata.normalize('NFD', t.lower()).replace('đ', 'd')
    return ''.join(c for c in t if unicodedata.category(c) != 'Mn')


def pick_noti(rows):
    """Dòng 'Tạo mới' mà ngay dưới là tên cuộc họp mới → bấm vào tên."""
    for x, y, bw, bh, t in sorted(rows, key=lambda r: r[1]):
        if 'tao moi' in nz(t):
            for x2, y2, bw2, bh2, t2 in rows:
                if KEY in nz(t2) and 0 < y2 - y < 40:
                    return (round(x2 + bw2 / 2), round(y2 + bh2 / 2))
    return None


def pick_card(rows):
    """Thẻ có tên cuộc họp mới và nhãn 'Lên lịch' cùng hàng."""
    for x, y, bw, bh, t in sorted(rows, key=lambda r: r[1]):
        if KEY in nz(t) and any('len lich' in nz(t2) and abs(y2 - y) < 16 for _, y2, _, _, t2 in rows):
            return (round(x + bw / 2), round(y + bh / 2))
    return None


def ensure_bell():
    """Chắc chắn danh sách chuông đang mở ở máy R."""
    for _ in range(3):
        if any('chua doc' in nz(t) or 'doc tat ca' in nz(t) for *_, t in ocr('R')):
            return
        tap('R', 365, 86); w(2.2)

def w(s):
    time.sleep(s)


# ── kịch bản ───────────────────────────────────────────────────────────────
# mark: [(máy, x, y, w, h)] toạ độ điểm (402×874) — khung vàng suốt bước
S = [
    dict(ch='Mở đầu', say='Xin chào. Các bạn đang xem video hướng dẫn sử dụng Phần mềm quản trị ERP TPE.'),
    dict(ch='Mở đầu', say='Video này hướng dẫn tạo cuộc họp trên ứng dụng di động, và cách người tham gia nhận thông báo, xác nhận tham dự.'),
    dict(ch='Mở đầu', say='Bên trái là điện thoại của người chủ trì. Bên phải là điện thoại của người tham gia.',
         mark=[('L', 0, 0, 402, 874), ('R', 0, 0, 402, 874)]),
    # ── Tạo cuộc họp
    dict(ch='Tạo cuộc họp', say='Ở phân hệ Meeting, người chủ trì bấm nút Tạo meeting ở giữa thanh dưới.',
         mark=[('L', 160, 752, 84, 100)]),
    dict(ch='Tạo cuộc họp', say='Màn Tạo meeting mở ra. Đầu tiên chọn Phân loại họp, ở đây là họp Nội bộ.',
         act=lambda: (tap('L', 201, 787), w(2.2), tap('L', 296, 214))),
    dict(ch='Tạo cuộc họp', say='Chọn Loại meeting trong danh sách, ví dụ Họp giao ban.',
         act=lambda: (tap('L', 306, 255), w(2.0), tap('L', 120, 678))),
    dict(ch='Tạo cuộc họp', say='Nhập tên cuộc họp.',
         act=lambda: (tap('L', 200, 343), w(0.8), text('L', NAME))),
    dict(ch='Tạo cuộc họp', say='Nhập mục tiêu, hoặc nội dung chính cần trao đổi.',
         act=lambda: (tap('L', 200, 465), w(0.8), text('L', GOAL))),
    dict(ch='Tạo cuộc họp', say='Tiếp theo là mục Thời gian, địa điểm và chủ trì. Người tạo mặc định là người chủ trì.',
         act=lambda: (tap('L', 200, 628), w(1.2), swipe('L', 200, 650, 200, 250, 800))),
    dict(ch='Tạo cuộc họp', say='Chọn ngày giờ bắt đầu. Giờ kết thúc tự lấy sau một tiếng.',
         act=lambda: (tap('L', 306, 373), w(1.6), swipe('L', 130, 735, 130, 690, 1200), w(1.3), swipe('L', 130, 735, 130, 690, 1200), w(1.4), tap('L', 375, 608))),
    dict(ch='Tạo cuộc họp', say='Nhập địa điểm họp.',
         act=lambda: (tap('L', 200, 710), w(0.8), text('L', 'Phòng họp tầng 3'))),
    dict(ch='Tạo cuộc họp', say='Bấm Tạo meeting. Cuộc họp được lưu ở trạng thái Đang tạo, và mở ra màn chi tiết.',
         act=lambda: tap('L', 295, 805)),
    # ── Mời người tham gia
    dict(ch='Mời người tham gia', say='Bấm vào Nhân sự tham gia để mời người họp.',
         act=lambda: (w(0.8), tap('L', 200, 482))),
    dict(ch='Mời người tham gia', say='Bấm Thêm nhanh, rồi tìm theo tên nhân viên.',
         act=lambda: (w(0.6), tap('L', 321, 143), w(2.4), tap('L', 200, 139), w(0.8), text('L', 'Đào Thị Thúy'))),
    dict(ch='Mời người tham gia', say='Tick chọn Đào Thị Thúy, rồi bấm Thêm.',
         act=lambda: (w(1.2), tap('L', 200, 210), w(1.2), tap('L', 295, 805))),
    dict(ch='Mời người tham gia', say='Bấm Lưu để quay lại màn chi tiết.',
         act=lambda: (w(0.8), tap('L', 295, 805))),
    dict(ch='Mời người tham gia', say='Bấm Lên lịch. Hệ thống hỏi lại trước khi gửi lịch họp tới các thành viên.',
         act=lambda: (w(1.0), tap('L', 196, 805))),
    dict(ch='Mời người tham gia', say='Bấm Lên lịch để xác nhận.',
         act=lambda: (w(0.6), tap('L', 121, 542))),
    # ── Nhận thông báo
    dict(ch='Nhận thông báo', say='Ngay lúc đó, điện thoại người tham gia nhận được thông báo Cuộc họp mới, kèm thời gian, địa điểm và người chủ trì.',
         mark=[('R', 8, 50, 386, 110)]),
    dict(ch='Nhận thông báo', say='Người tham gia mở ứng dụng, rồi bấm vào biểu tượng chuông.',
         act=lambda: (w(0.4), tap('R', 339, 233), w(2.4), tap('R', 365, 86))),
    dict(ch='Nhận thông báo', say='Thông báo mới nằm trên cùng. Bấm vào thông báo, ứng dụng mở thẳng tới cuộc họp.',
         act=lambda: (w(1.0), ensure_bell(), tap_where('R', pick_noti, (220, 345)))),
    # ── Xác nhận tham dự
    dict(ch='Xác nhận tham dự', say='Ở mục Xác nhận tham dự có hai nút: Có mặt, và Vắng có lý do.',
         mark=[('R', 12, 262, 380, 84)]),
    dict(ch='Xác nhận tham dự', say='Bấm Có mặt. Trạng thái chuyển thành Đã xác nhận Có mặt.',
         act=lambda: tap('R', 106, 320)),
    dict(ch='Xác nhận tham dự', say='Phía chủ trì, mở Danh sách meeting rồi kéo xuống để tải lại. Thẻ cuộc họp hiện số người đã xác nhận.',
         act=lambda: (tap('L', 270, 815), w(2.4), swipe('L', 200, 250, 200, 620, 700), w(2.0)), mark=[('L', 14, 182, 374, 124)]),
    dict(ch='Xác nhận tham dự', say='Mở cuộc họp, rồi bấm Nhân sự tham gia để xem từng người. Đào Thị Thúy đã xác nhận Có mặt.',
         act=lambda: (tap_where('L', pick_card, (200, 240)), w(3.2), tap('L', 200, 495))),
    dict(ch='Xác nhận tham dự', say='Bấm Quay lại để về màn chi tiết.',
         act=lambda: (w(0.6), tap('L', 105, 805))),
    # ── Đổi lịch họp
    dict(ch='Đổi lịch họp', say='Cần đổi giờ họp, chủ trì vào Thông tin chung, mở mục Thời gian, địa điểm và chủ trì.',
         act=lambda: (w(0.8), tap('L', 200, 420), w(2.4), tap('L', 200, 238))),
    dict(ch='Đổi lịch họp', say='Chọn lại giờ bắt đầu. Giờ kết thúc tự lùi theo.',
         act=lambda: (tap('L', 306, 274), w(1.6), swipe('L', 297, 750, 297, 700, 1200), w(1.2),
                      swipe('L', 297, 750, 297, 700, 1200), w(1.2), tap('L', 375, 608))),
    dict(ch='Đổi lịch họp', say='Bấm Lưu. Màn hình của người tham gia tự cập nhật giờ mới, và hiện thông báo Cuộc họp đổi lịch, ghi rõ lịch cũ và lịch mới.',
         act=lambda: (tap('L', 295, 805), w(9.5), swipe('R', 100, 8, 100, 520, 400)), mark=[('R', 8, 50, 386, 110)]),
    # ── Chốt lịch
    dict(ch='Chốt lịch', say='Bây giờ người tham gia đang ở màn hình khoá.', mark=[('R', 0, 60, 402, 200)]),
    dict(ch='Chốt lịch', say='Chủ trì bấm Chốt lịch. Hệ thống hỏi lại.',
         act=lambda: (w(0.6), tap('L', 300, 805))),
    dict(ch='Chốt lịch', say='Bấm Chốt lịch để xác nhận. Thông báo Đã chốt lịch hiện ngay trên màn hình khoá của người tham gia.',
         act=lambda: (w(0.6), tap('L', 109, 542)), mark=[('R', 14, 600, 374, 170)]),
    dict(ch='Chốt lịch', say='Cuộc họp chuyển sang trạng thái Chốt lịch, sẵn sàng cho buổi họp.'),
    # ── Kết
    dict(ch='Kết', say='Đó là các chức năng chính khi tạo cuộc họp, và xác nhận tham dự trên ứng dụng di động.'),
    dict(ch='Kết', say='Cảm ơn các bạn đã xem video!'),
]


# ── lời đọc ────────────────────────────────────────────────────────────────
def dur(f):
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f],
                                capture_output=True, text=True).stdout.strip())


def tts(sentence):
    f = os.path.join(CACHE, hashlib.md5(sentence.encode()).hexdigest() + '.mp3')
    if os.path.exists(f) and os.path.getsize(f) > 1000:
        return f
    for i in range(16):
        try:
            r = subprocess.run([TTS, '--voice', 'vi-VN-HoaiMyNeural', '--rate=+4%', '--text', sentence, '--write-media', f],
                               capture_output=True, timeout=40)
        except subprocess.TimeoutExpired:
            continue
        if r.returncode == 0 and os.path.exists(f) and os.path.getsize(f) > 1000:
            return f
        time.sleep(1.5 * (i + 1))
    sys.exit(f'TTS lỗi: {sentence}')


def voice(i, say):
    import re
    parts = [p.strip() for p in re.split(r'(?<=[.!?])\s+', say) if p.strip()]
    files = [tts(p) for p in parts]
    out = os.path.join(CACHE, f'step{i:02d}.m4a')
    sil = os.path.join(CACHE, 'sil.mp3')
    if not os.path.exists(sil):
        subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'lavfi', '-i', 'anullsrc=r=24000:cl=mono', '-t', '0.25', sil])
    seq = []
    for k, f in enumerate(files):
        seq += ([sil] if k else []) + [f]
    lst = os.path.join(CACHE, f'step{i:02d}.txt')
    open(lst, 'w').write(''.join(f"file '{p}'\n" for p in seq))
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-c:a', 'aac', '-ar', '48000', out], check=True)
    return out


def main():
    global T0
    print('Tạo lời đọc…', flush=True)
    for i, s in enumerate(S):
        s['audio'] = voice(i, s['say'])
        s['dur'] = dur(s['audio'])
    print('Tổng lời:', round(sum(s['dur'] + 0.35 for s in S), 1), 's', flush=True)
    if '--tts-only' in sys.argv:
        return

    # máy R: về màn hình chính, đúng trang có icon app
    home('R'); w(1.8)
    for _ in range(6):
        ls = labels('R')
        if any(l == 'Tân Phát ERP-HRM' and 0 <= r.get('x', -1) < 402 for l, r in ls):
            break
        lib = any('Thư viện ứng dụng' in l and 0 <= r.get('x', -1) < 402 for l, r in ls)
        swipe('R', 50, 500, 350, 500, 300) if lib else swipe('R', 350, 500, 50, 500, 300)
        w(1.8)
    else:
        sys.exit('Máy R: không thấy icon app trên màn hình chính')

    recs, starts = {}, {}
    for d in ('L', 'R'):
        p = subprocess.Popen(['xcrun', 'simctl', 'io', DEV[d], 'recordVideo', '--codec=h264', '--force',
                              os.path.join(HERE, f'rec_{d}.mov')], stderr=subprocess.PIPE, text=True)
        recs[d] = p
    for d, p in recs.items():
        while True:
            line = p.stderr.readline()
            if not line or 'Recording started' in line:
                starts[d] = time.time()
                break
    T0 = max(starts.values())
    offs = {d: round(T0 - t, 3) for d, t in starts.items()}  # giây cần cắt đầu mỗi file để khớp T0
    w(1.0)

    timeline = []
    for i, s in enumerate(S):
        t = now()
        print(f'Bước {i:02d} [{s["ch"]}] {round(t, 1)}s — {s["say"][:60]}', flush=True)
        try:
            if s.get('act'):
                s['act']()
        except Exception as e:
            print(f'Bước {i} lỗi: {e}', flush=True)
        rest = s['dur'] + 0.35 - (now() - t)
        if rest > 0:
            time.sleep(rest)
        timeline.append({'i': i, 'ch': s['ch'], 'say': s['say'], 'start': round(t, 3), 'end': round(now(), 3),
                         'audio': s['audio'], 'mark': s.get('mark', [])})
    w(1.2)
    end = now()
    for p in recs.values():
        p.send_signal(signal.SIGINT)
    for p in recs.values():
        p.wait()
    json.dump({'offs': offs, 'end': round(end, 3), 'steps': timeline, 'taps': taps},
              open(os.path.join(HERE, 'timeline.json'), 'w'), ensure_ascii=False, indent=1)
    print('Xong, dài', round(end, 1), 's', flush=True)


if __name__ == '__main__':
    main()
