# -*- coding: utf-8 -*-
"""Đẩy HDSD bản gọn lên Drive THEO ID (folder HDSD có file trùng tên → không đẩy theo tên được).

python3 push_hdsd_by_id.py <slug> [<slug> ...]

- Đích: hdsd_gon_targets.json (drive_id + dup_ids), cộng EXTRA bên dưới cho màn làm trước khi có file đó.
- Chỉ ghi đè khi modifiedTime trên Drive == mốc đã biết (lần đọc ban đầu, hoặc lần mình đẩy gần nhất,
  lưu ở push_log.json). Lệch = có người sửa tay sau mình → BỎ QUA, in cảnh báo để hỏi user.
- Sau khi đẩy: tải lại theo ID, so từng byte với file local.
- Tự thử lại khi Google trả 403 rateLimitExceeded (rclone dùng client_id chung, hay bị).
"""
import json
import os
import subprocess
import sys
import tempfile
import time
import urllib.request
import urllib.error
import filecmp

H = os.path.dirname(os.path.abspath(__file__))
LOG = os.path.join(H, 'push_log.json')
EXTRA = {
    'provinces': {'drive_name': 'HDSD_Danh mục Tỉnh-TP.docx', 'ids': ['14ZdBWrNqj7RqRj0QNnj6dweqYLS8o8SZ']},
    'type-accounts': {'drive_name': 'HDSD_Danh mục loại tài khoản.docx',
                      'ids': ['14Yjg2IgGHZPNeDv1t1OrqDx-ebYD9_BC']},   # bản trùng 1-Yoc… (21/08) đã bỏ 29/09
}
MIME = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'


def token():
    subprocess.run(['rclone', 'about', 'gdrive:'], capture_output=True)
    dump = json.loads(subprocess.run(['rclone', 'config', 'dump'], capture_output=True, text=True).stdout)
    return json.loads(dump['gdrive']['token'])['access_token']


TOK = {}


def api(req, tries=8):
    for i in range(tries):
        req.headers['Authorization'] = 'Bearer ' + TOK['v']
        try:
            with urllib.request.urlopen(req) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            body = e.read().decode('utf-8', 'ignore')
            if e.code == 401:                     # token 1 giờ hết hạn giữa chừng → lấy lại
                TOK['v'] = token()
                continue
            if e.code in (403, 429) and 'ateLimit' in body:
                time.sleep(15 * (i + 1))
                continue
            raise RuntimeError('%s %s' % (e.code, body[:200]))
    raise RuntimeError('vẫn bị giới hạn sau %d lần thử' % tries)


def main(slugs):
    targets = {t['slug']: t for t in json.load(open(os.path.join(H, 'hdsd_gon_targets.json')))}
    log = json.load(open(LOG)) if os.path.exists(LOG) else {}
    TOK['v'] = token()
    tok = TOK['v']
    for slug in slugs:
        if slug in targets:
            t = targets[slug]
            name = t['drive_name']
            ids = [(t['drive_id'], t['drive_modtime'])] + list(zip(t['dup_ids'], t['dup_modtime']))
        else:
            t = EXTRA[slug]
            name = t['drive_name']
            ids = [(i, None) for i in t['ids']]
        src = os.path.join(H, slug, 'out', name)
        assert os.path.exists(src), 'Thiếu file ' + src
        data = open(src, 'rb').read()
        for fid, first in ids:
            known = log.get(fid, first)
            meta = api(urllib.request.Request(
                'https://www.googleapis.com/drive/v3/files/%s?fields=modifiedTime&supportsAllDrives=true' % fid,
                headers={'Authorization': 'Bearer ' + tok}))
            cur = meta['modifiedTime']
            if known and cur[:19] != known[:19]:
                print('BỎ QUA %s %s — Drive sửa lúc %s, mốc đã biết %s (có người sửa tay?)' % (slug, fid, cur, known))
                continue
            res = api(urllib.request.Request(
                'https://www.googleapis.com/upload/drive/v3/files/%s?uploadType=media&supportsAllDrives=true'
                '&fields=id,modifiedTime' % fid, data=data, method='PATCH',
                headers={'Authorization': 'Bearer ' + tok, 'Content-Type': MIME}))
            log[fid] = res['modifiedTime']
            json.dump(log, open(LOG, 'w'), indent=1)
            tmp = os.path.join(tempfile.mkdtemp(), 'chk.docx')
            subprocess.run(['rclone', 'backend', 'copyid', 'gdrive:', fid, tmp], capture_output=True)
            ok = os.path.exists(tmp) and filecmp.cmp(tmp, src, shallow=False)
            print('%s %s %s %s' % ('OK  ' if ok else 'LỆCH', slug, fid, res['modifiedTime']))


if __name__ == '__main__':
    main(sys.argv[1:])
