#!/usr/bin/env python3
"""Dọn trước khi quay lại: huỷ cuộc họp tên NAME đang mở trên dev; L về Meeting › Tổng quan; R đọc hết chuông,
về màn hình chính, xoá thông báo iOS."""
import json, os, subprocess, sys, time, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from record import tap, swipe, home, labels, w, DEV  # noqa
NAMES = os.environ.get('NAMES', 'Họp triển khai kế hoạch tháng 11').split('|')

SP = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API = 'http://dev-hrm.eteksofts.com/api/'


def call(method, path, tok, body=None):
    req = urllib.request.Request(API + path, method=method, data=json.dumps(body).encode() if body else None,
                                 headers={'Authorization': 'Bearer ' + tok, 'Accept': 'application/json',
                                          'Content-Type': 'application/json'})
    return json.load(urllib.request.urlopen(req, timeout=30))


tok = open(os.path.join(SP, 'tok_nam')).read().strip()
for m in call('GET', 'v1/assign/meeting/mine?per_page=20', tok).get('data') or []:
    if m.get('name') in NAMES and int(m.get('status') or 0) in (0, 1, 2, 5):
        call('POST', f"v1/assign/meeting/{m['id']}/change-status", tok,
             {'status': 4, 'cancel_reason_id': 1, 'cancel_reason': 'Dữ liệu thử quay video'})
        print('Huỷ', m['id'], m.get('code'))


def has(d, text):
    return any(text in l for l, r in labels(d) if 0 <= r.get('x', -1) < 402)


# L: về Tổng quan
for _ in range(4):
    if has('L', 'Cần xử lý gấp') and has('L', 'Tổng quan'):
        break
    if has('L', 'Tổng quan'):
        tap('L', 33, 815)
    else:
        tap('L', 36, 86)
    w(2)
# L: xoá chữ còn sót ở ô tìm của Danh sách meeting
from record import ocr, nz
tap('L', 270, 815); w(2.5)
if any(120 < y + bh / 2 < 160 and x > 40 and 'tim theo' not in nz(t) and t.strip() for x, y, bw, bh, t in ocr('L')):
    tap('L', 321, 139); w(2)
tap('L', 33, 815); w(2)
# R: chuông → Đọc tất cả → về Tổng quan → HOME
tap('R', 365, 86); w(4)
tap('R', 322, 92); w(2.5)
for _ in range(4):
    if has('R', 'Chào buổi') or has('R', 'Cần xử lý gấp'):
        break
    tap('R', 36, 86); w(2)
home('R'); w(1.2)
# xoá thông báo iOS
swipe('R', 100, 8, 100, 520, 400); w(1.5)
for _ in range(3):
    if not has('R', 'ShortLook') and not any('ERP-HRM,' in l for l, r in labels('R')):
        break
    swipe('R', 330, 690, 120, 690, 300); w(1.0)
    hit = [r for l, r in labels('R') if l in ('Xóa tất cả', 'Xóa')]
    if hit:
        r = hit[0]; tap('R', r['x'] + r['width'] // 2, r['y'] + r['height'] // 2); w(1.2)
swipe('R', 200, 860, 200, 300, 300); w(1.2)
home('R'); w(1)
print('L sẵn sàng:', has('L', 'Cần xử lý gấp'), '| R thông báo còn:', any('ERP-HRM,' in l for l, r in labels('R')))
