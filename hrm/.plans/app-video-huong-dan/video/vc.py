#!/usr/bin/env python3
"""Bộ máy quay video HDSD app — 1 máy ảo iOS (skill video-creator-docs, bản cho app).

- Động cơ theo BƯỚC: `act` chạy lúc bắt đầu bước; bước sau chỉ bắt đầu khi lời bước trước đọc xong (+0,35s).
- Bấm theo CHỮ trên màn (OCR Vision, `ocr` dựng từ ocr.swift) — không phụ thuộc toạ độ cứng; có toạ độ dự phòng.
- `wait_text()` chờ màn tải xong; đoạn chờ ghi vào `cuts` để build cắt khỏi video (lời dời theo mốc mới).
- Bước `clip=` chèn video ngoài (vd đoạn gọi điện quay trên iPhone thật) thay cho hình máy ảo.
Dùng: from vc import *  (xem record_mytodo.py)
"""
import hashlib, json, os, re, signal, subprocess, sys, time, unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
M = '/Users/dnsnamdang/.npm/_npx/e41f45e886283da6/node_modules/@mobilenext/mobilecli-darwin-arm64/mobilecli-darwin-arm64'
DEV = os.environ.get('DEV', 'D0C0E274-8590-4D39-9196-CD5D535338DD')
TOOLS = os.environ.get('VTOOLS', os.path.expanduser('~/.cache/tpe-video-tools'))  # `ocr` + `ttsenv/` (cách dựng: plan.md)
OCR = os.path.join(TOOLS, 'ocr')
TTS = os.path.join(TOOLS, 'ttsenv', 'bin', 'edge-tts')
WORK = os.environ.get('VWORK', os.path.expanduser('~/.cache/tpe-video-work'))  # bản quay thô, lời đọc cache
CACHE = os.path.join(WORK, 'tts-cache')
os.makedirs(CACHE, exist_ok=True)

T0 = None
taps, cuts = [], []
MARKS = []         # khung vàng của bước đang chạy (hl() thêm vào)
STEP_T = 0.0
DRY = False          # True = chạy thử thao tác, không quay, không chờ lời


def now():
    return time.time() - T0 if T0 else 0.0


def w(s):
    time.sleep(s)


def mcli(*a):
    return subprocess.run([M, *a], capture_output=True, text=True).stdout


def nz(t):
    t = unicodedata.normalize('NFD', t.lower()).replace('đ', 'd')
    return re.sub(r'\s+', ' ', ''.join(c for c in t if unicodedata.category(c) != 'Mn')).strip()


def tap(x, y):
    taps.append({'x': x, 'y': y, 't': round(now(), 3)})
    mcli('io', 'tap', f'{int(x)},{int(y)}', '--device', DEV)


def text(s):
    mcli('io', 'text', s, '--device', DEV)


def swipe(x1, y1, x2, y2, dur=None):
    mcli('io', 'swipe', f'{x1},{y1},{x2},{y2}', '--device', DEV, *(['--duration', str(dur)] if dur else []))


def home():
    mcli('io', 'button', 'HOME', '--device', DEV)


def ocr():
    """[(x, y, w, h, text)] theo điểm 402×874."""
    f = os.path.join(WORK, '_ocr.png')
    subprocess.run(['xcrun', 'simctl', 'io', DEV, 'screenshot', f], capture_output=True)
    out = subprocess.run([OCR, f], capture_output=True, text=True).stdout
    rows = []
    for line in out.splitlines():
        try:
            box, t = line.split('\t', 1)
            x, y, bw, bh = map(float, box.split())
            rows.append((x * 402, y * 874, bw * 402, bh * 874, t))
        except ValueError:
            pass
    return rows


def find(label, exact=False, area=None, nth=0):
    """Toạ độ tâm dòng chữ khớp `label` (không dấu, không hoa thường). area=(x0,y0,x1,y1) giới hạn vùng."""
    key = nz(label)
    hits = []
    for x, y, bw, bh, t in ocr():
        n = nz(t)
        if (n == key) if exact else (key in n):
            cx, cy = x + bw / 2, y + bh / 2
            if area and not (area[0] <= cx <= area[2] and area[1] <= cy <= area[3]):
                continue
            hits.append((round(cx), round(cy)))
    hits.sort(key=lambda p: (p[1], p[0]))
    return hits[nth] if len(hits) > nth else None


def tap_text(label, exact=False, area=None, nth=0, fallback=None, tries=10, dx=0, dy=0):
    for _ in range(tries):
        p = find(label, exact, area, nth)
        if p:
            return tap(p[0] + dx, p[1] + dy)
        w(0.6)
    print(f'   ! không thấy "{label}"' + (f', bấm dự phòng {fallback}' if fallback else ''), flush=True)
    if fallback:
        tap(*fallback)


def wait_text(label, timeout=15, cut=True, exact=False, area=None):
    """Chờ chữ xuất hiện (màn tải xong). cut=True: đoạn chờ bị cắt khỏi video."""
    t = now()
    end = time.time() + timeout
    while time.time() < end:
        if find(label, exact, area):
            break
        w(0.4)
    else:
        print(f'   ! hết giờ chờ "{label}"', flush=True)
    if cut and now() - t > 0.5 and not DRY:
        cuts.append([round(t + 0.2, 3), round(now(), 3)])


def hl(label=None, rect=None, off=0.3, padx=10, pady=8, area=None, full_row=False, h=None):
    """Tô khung vàng: theo chữ (tìm vị trí lúc quay) hoặc rect=(x, y, w, h) điểm 402×874."""
    if rect is None:
        for x, y, bw, bh, t in ocr():
            if nz(label) in nz(t) and (not area or (area[0] <= x + bw / 2 <= area[2] and area[1] <= y + bh / 2 <= area[3])):
                rect = (8, y - pady, 386, (h or bh + 2 * pady)) if full_row else (x - padx, y - pady, bw + 2 * padx, h or bh + 2 * pady)
                break
    if rect:
        MARKS.append([round(v) for v in rect] + [round(now() - STEP_T + off, 2)])
    else:
        print(f'   ! hl không thấy "{label}"', flush=True)


def gone(label, timeout=10):
    end = time.time() + timeout
    while time.time() < end and find(label):
        w(0.4)


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
    parts = [p.strip() for p in re.split(r'(?<=[.!?])\s+', say) if p.strip()]
    files = [tts(p) for p in parts]
    out = os.path.join(CACHE, 'step-' + hashlib.md5(say.encode()).hexdigest() + '.m4a')
    if os.path.exists(out):
        return out
    sil = os.path.join(CACHE, 'sil.mp3')
    if not os.path.exists(sil):
        subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'lavfi', '-i', 'anullsrc=r=24000:cl=mono', '-t', '0.25', sil])
    seq = []
    for k, f in enumerate(files):
        seq += ([sil] if k else []) + [f]
    lst = out + '.txt'
    open(lst, 'w').write(''.join(f"file '{p}'\n" for p in seq))
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-c:a', 'aac', '-ar', '48000', out], check=True)
    return out


def run(S, name, only=None):
    """S: [dict(ch, say, act?, mark?, clip?)]. only=(a, b): chạy thử bước a..b (không quay, không chờ lời)."""
    global T0, DRY
    print('Tạo lời đọc…', flush=True)
    for i, s in enumerate(S):
        s['audio'] = voice(i, s['say'])
        s['dur'] = dur(s['audio'])
    print('Tổng lời:', round(sum(s['dur'] + 0.35 for s in S) / 60, 1), 'phút', flush=True)
    if '--tts-only' in sys.argv:
        return
    if only:
        DRY = True
        T0 = time.time()
        for i in range(only[0], only[1] + 1):
            s = S[i]
            print(f'[thử] Bước {i} [{s["ch"]}] {s["say"][:70]}', flush=True)
            if s.get('act'):
                s['act']()
            w(float(os.environ.get('PAUSE', '0.8')))
        return

    rec = os.path.join(WORK, f'rec_{name}.mov')
    p = subprocess.Popen(['xcrun', 'simctl', 'io', DEV, 'recordVideo', '--codec=h264', '--force', rec],
                         stderr=subprocess.PIPE, text=True)
    while True:
        line = p.stderr.readline()
        if not line or 'Recording started' in line:
            break
    T0 = time.time()
    w(1.0)
    timeline = []
    for i, s in enumerate(S):
        t = now()
        print(f'Bước {i:03d} [{s["ch"]}] {round(t, 1)}s — {s["say"][:60]}', flush=True)
        c0 = len(cuts)
        global STEP_T
        STEP_T = t
        MARKS.clear()
        try:
            if s.get('act'):
                s['act']()
        except Exception as e:
            print(f'Bước {i} lỗi: {e}', flush=True)
        # thời gian bị cắt trong bước này không tính vào thời gian đọc lời
        cut_in = sum(b - a for a, b in cuts[c0:])
        rest = s['dur'] + 0.35 - (now() - t - cut_in)
        if rest > 0:
            time.sleep(rest)
        timeline.append({'i': i, 'ch': s['ch'], 'say': s['say'], 'start': round(t, 3), 'end': round(now(), 3),
                         'audio': s['audio'], 'mark': s.get('mark', []) + [m[:4] + [m[4]] for m in MARKS], 'clip': s.get('clip')})
    w(1.0)
    end = now()
    p.send_signal(signal.SIGINT)
    p.wait()
    json.dump({'rec': rec, 'end': round(end, 3), 'steps': timeline, 'taps': taps, 'cuts': cuts},
              open(os.path.join(WORK, f'timeline_{name}.json'), 'w'), ensure_ascii=False, indent=1)
    print('Xong, dài', round(end / 60, 1), 'phút', flush=True)


def wheel_value(x, y=683):
    for cx, cy in [(r[0] + r[2] / 2, r[1] + r[3] / 2) for r in []]:
        pass
    best = None
    for rx, ry, bw, bh, t in ocr():
        cx, cy = rx + bw / 2, ry + bh / 2
        if abs(cx - x) < 22 and abs(cy - y) < 12 and t.strip().isdigit():
            best = int(t.strip())
    return best


def set_wheel(x, target, y=683, modulo=24):
    """Đặt bánh xe giờ/phút (CupertinoPicker) về `target`. Đo 09/11: kéo 35–50px = đúng 1 hàng, 70px trôi ~3 hàng
    (quán tính) ⇒ còn xa thì kéo 100px, gần thì kéo từng hàng 42px; mỗi lần đọc lại bằng OCR."""
    for _ in range(14):
        cur = wheel_value(x, y)
        if cur is None:
            w(0.5)
            continue
        diff = (target - cur) % modulo
        if diff > modulo // 2:
            diff -= modulo
        if diff == 0:
            return True
        step = 100 if abs(diff) >= 5 else 42
        sign = 1 if diff > 0 else -1          # tăng giá trị = kéo lên
        swipe(x, y + 60, x, y + 60 - sign * step, 1500)
        w(1.0)
    print(f'   ! không đặt được bánh xe x={x} về {target}', flush=True)
    return False


def keys(*combo):
    mcli('io', 'keys', *combo, '--device', DEV)


def clear_field():
    """Xoá hết chữ trong ô đang focus (Cmd+A rồi Backspace)."""
    keys('cmd+a', 'backspace')


DATE_COLS = [42, 95, 147, 200, 253, 306, 358]   # T2..CN trên sheet chọn ngày
DATE_ROW0, DATE_ROW_H = 458, 49                  # hàng đầu của lưới tháng


def pick_date(d, confirm=True):
    """Chọn ngày `d` (datetime.date) trên sheet chọn ngày đang mở (tháng đang hiển thị = tháng của d)."""
    import datetime
    first = d.replace(day=1)
    idx = first.weekday() + d.day - 1
    tap(DATE_COLS[idx % 7], DATE_ROW0 + DATE_ROW_H * (idx // 7))
    w(0.6)
    if confirm:
        tap_text('Chọn', area=(200, 780, 402, 840), fallback=(297, 808))
        w(0.6)


M_COLS = [66, 110, 155, 200, 245, 289, 334]     # ô chọn ngày kiểu Material (khối Báo lịch lãnh đạo)
M_ROW0, M_ROW_H = 427, 42


def pick_date_m(d):
    first = d.replace(day=1)
    idx = first.weekday() + d.day - 1
    tap(M_COLS[idx % 7], M_ROW0 + M_ROW_H * (idx // 7))
    w(0.6)
    tap_text('OK', exact=True, area=(250, 650, 402, 720), fallback=(325, 685))
    w(0.8)


def tap_row(label, x, area=None, tries=8):
    """Bấm ở cột x, cùng hàng với dòng chữ `label` (ô tick / vòng tròn bên trái chữ)."""
    for _ in range(tries):
        p = find(label, area=area)
        if p:
            return tap(x, p[1])
        w(0.6)
    print(f'   ! tap_row không thấy "{label}"', flush=True)


def tap_btn(label, area=None, tries=10, fallback=None):
    """Bấm NÚT: dòng chữ ngắn kết thúc bằng `label` (cho phép 1 ký tự icon phía trước, vd "v Hoàn thành", "/ Sửa")."""
    key = nz(label)
    for _ in range(tries):
        hits = []
        for x, y, bw, bh, t in ocr():
            n = nz(t)
            if n.endswith(key) and len(n) <= len(key) + 3:
                cx, cy = x + bw / 2, y + bh / 2
                if not area or (area[0] <= cx <= area[2] and area[1] <= cy <= area[3]):
                    hits.append((round(cx), round(cy)))
        if hits:
            hits.sort(key=lambda p: (p[1], p[0]))
            return tap(*hits[0])
        w(0.6)
    print(f'   ! không thấy nút "{label}"', flush=True)
    if fallback:
        tap(*fallback)


def type_in(label, value, area=None, tries=3):
    """Bấm ô (theo chữ gợi ý `label`), chờ bàn phím, gõ `value`, ĐỌC LẠI màn xem chữ đã vào chưa; chưa thì xoá gõ lại."""
    for _ in range(tries):
        if label:
            tap_text(label, area=area, tries=4)
        w(0.9)
        text(value)
        w(0.7)
        if find(value[:10]):
            return True
        clear_field()
        w(0.4)
    print(f'   ! gõ không vào: "{value}"', flush=True)
    return False
