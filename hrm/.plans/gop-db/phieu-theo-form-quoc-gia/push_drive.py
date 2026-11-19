# -*- coding: utf-8 -*-
"""Đẩy SRS/HDSD đã sửa lên Drive THEO ID (ghi đè nội dung, giữ nguyên link + tên file).

Chạy:  python push_drive.py              -> chạy thử, chỉ in việc sẽ làm
       python push_drive.py --go [STT…]  -> đẩy thật (mặc định cả 16 màn)

- File nguồn: giao/<STT>/<tên file>. Token lấy từ remote rclone `gdrive`.
- Chốt an toàn: modifiedTime trên Drive phải <= MOC (lúc tải bản gốc 28/10). Lớn hơn = có người sửa sau
  lúc mình tải -> BỎ QUA, báo lại để đối chiếu. Đã đẩy thành công thì mốc của file = giờ mình đẩy
  (lưu push_log.json) nên chạy lại không bị chặn nhầm.
- ⚠️ Ghi đè .docx = Google XOÁ HẾT nhận xét trên file -> in số nhận xét đang có, >0 thì bỏ qua.
- Đẩy xong so md5 với file local.
"""
import hashlib
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request

H = os.path.dirname(os.path.abspath(__file__))
GIAO = os.path.join(H, 'giao')
LOG = os.path.join(H, 'push_log.json')
RCLONE = os.path.expandvars(r'%LOCALAPPDATA%\Microsoft\WinGet\Packages\Rclone.Rclone_Microsoft.Winget.Source_8wekyb3d8bbwe'
                            r'\rclone-v1.75.1-windows-amd64\rclone.exe')
MOC = '2026-10-28T07:00:00Z'
MIME = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'

# STT: [(Drive id, tên file trong giao/<STT>/), ...]
FILES = {
    '26': [('1soFAY5i5Qi8RjLrVzYuszINiZ17C1xkY', 'SRS - Phiếu yêu cầu chuyển hàng.docx'),
           ('1CEQLFcg_nDHgKKpIoBLmdXmKQomubsvX', 'HDSD_Phiếu yêu cầu chuyển hàng.docx')],
    '27': [('19eShyMadGRY9ouqQK3jbRwodxwYq6uOx', 'SRS - Phiếu chuyển hàng nhập thẳng.docx'),
           ('1xhCH_9O0YTVPr_W4raOZ9WhD03GMoah_', 'HDSD_Phiếu chuyển hàng nhập thẳng.docx')],
    '31': [('1RUz7RSF84gQ9JKs9jJosa-P8uZH6qMsS', 'SRS - Phiếu yêu cầu gia hạn giữ hàng.docx'),
           ('1IuiZGnXWi7n774Dr5ZCVu1TbTm-pnyid', 'HDSD_Phiếu yêu cầu gia hạn hàng giữ.docx')],
    '32': [('1H7VbMHjv3TPM3HgeMoGm3NFiWHBmC4Ie', 'SRS - Yêu cầu hủy hàng giữ.docx'),
           ('1uAoS0gaZxZJkl8SX7OnVccXJIkyX1W2M', 'HDSD_Yêu cầu hủy hàng giữ.docx')],
    '33': [('1eeTtxWEgmCVCIVmaj6e-moVGcVVbqFKv', 'SRS - Yêu cầu điều chuyển hàng giữ.docx'),
           ('143-PY4K8iYkphynm3LRmaAIi9ZEXeSTD', 'HDSD_Yêu cầu điều chuyển hàng giữ.docx')],
    '48': [('1n6Ly2PSR4Ya3EmQuKVRgczXZhSD8mMqZ', 'SRS - Phiếu đề nghị thu tiền.docx'),
           ('1tqJ-jOgYIQEJYcTMgWTlCT2OoZzwRx-y', 'HDSD_Phiếu đề nghị thu tiền.docx')],
    '49': [('1Im8PbBFeRRZga3Flv51aJH3v53eIQY5S', 'SRS - Phiếu đề nghị thanh toán.docx'),
           ('1B779TXlrCreSS967QUGcn02eD_v5JWvU', 'HDSD_Phiếu đề nghị thanh toán.docx')],
    '160': [('1iFzcLaSIEM5QMQ6r60XiRdlnz63k2k9z', 'SRS - Phiếu thu tiền.docx'),
            ('12PNbY1lkPezuMewdOBSCeQRW2fXNX3BN', 'HDSD_Phiếu thu tiền.docx')],
    '161': [('1Jr4bjQzZDGMDcVu2DhRZLHIOcCsjTGc8', 'SRS - Phiếu chi tiền.docx'),
            ('1je_yqHUJnltM0YPyQMIBfesvsWNo1xHF', 'HDSD_Phiếu chi tiền.docx')],
    '162': [('1nVpE2oZXT4Jmg8d4teoDjiGxSWA4Fb1J', 'SRS - Phiếu_báo_có.docx'),
            ('1jvfpFNF2asVrmoBa-O1lWfCMWi9uP2p9', 'HDSD_Phiếu_báo_có.docx')],
    '163': [('1pLJ5lA8TYBZnk2JmsfjHKzz2Vo3yv7f_', 'SRS - Phiếu ủy nhiệm chi.docx'),
            ('13q6gYKDkF04lsYlL3RKyFZYAq0i-WZ0q', 'HDSD_Phiếu ủy nhiệm chi.docx')],
    '187': [('1VCXvT4i6Qsf2r7Og88CFemLQv0tmdkUq', 'SRS - Yêu cầu xuất giữ.docx'),
            ('1Lw2ve2rmzXWTozg8UHxBotzmVSCR_vrr', 'HDSD_Yêu cầu xuất giữ.docx')],
    '188': [('1ZB-qQNgm7dpPMQosvxlo5oPDdRXP5vDy', 'SRS - Phiếu xuất giữ.docx'),
            ('1cc6nooILubhFr_ILc7dVna_H_srjKiEP', 'HDSD_Phiếu xuất giữ.docx')],
    '191': [('1829fy4miIS41QpOo4KNHBAX_FsvvVc4-', 'SRS - Phieu huy hang giu.docx'),
            ('1YZNmlq6NeeAn7SaiLeyEM29eaSU6-lJT', 'HDSD_Phieu huy hang giu.docx')],
    '232': [('1xdJN54n1dfcWDWYfjS0KWvd1nYT6eGAL', 'SRS - Yêu cầu kiểm tra sửa chữa - bảo hành.docx'),
            ('1IxMflEGt5ugMp5CEiHFKqvRJd6d-aYzD', 'HDSD_Yeu cau kiem tra sua chua - bao hanh.docx')],
    '233': [('1PkDaG9HxWtI-OFid0akYkIzPbesByB7o', 'SRS - Phiếu xử lý yêu cầu.docx'),
            ('1D7BcxgDhChHYG9zBS_cv-rlQObzA1ZA9', 'HDSD_Phieu xu ly yeu cau.docx')],
}


def token():
    subprocess.run([RCLONE, 'about', 'gdrive:'], capture_output=True)  # làm mới token nếu hết hạn
    dump = json.loads(subprocess.run([RCLONE, 'config', 'dump'], capture_output=True, text=True).stdout)
    return json.loads(dump['gdrive']['token'])['access_token']


def call(req):
    for k in range(6):
        try:
            return json.load(urllib.request.urlopen(req))
        except urllib.error.HTTPError as e:
            if e.code in (403, 429, 500, 503) and k < 5:
                print('   thử lại sau', 10 * (k + 1), 's:', e.code)
                time.sleep(10 * (k + 1))
                continue
            raise


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    go = '--go' in sys.argv
    only = [a for a in sys.argv[1:] if not a.startswith('--')] or list(FILES)
    log = json.load(open(LOG, encoding='utf-8')) if os.path.exists(LOG) else {}
    hdr = {'Authorization': 'Bearer ' + token()}
    for stt in only:
        for fid, name in FILES[stt]:
            path = os.path.join(GIAO, stt, name)
            data = open(path, 'rb').read()
            meta = call(urllib.request.Request(
                f'https://www.googleapis.com/drive/v3/files/{fid}?fields=name,modifiedTime&supportsAllDrives=true',
                headers=hdr))
            cm = call(urllib.request.Request(
                f'https://www.googleapis.com/drive/v3/files/{fid}/comments?fields=comments(id)&pageSize=100',
                headers=hdr))
            n_cm = len(cm.get('comments', []))
            moc = log.get(fid, MOC)
            tag = f'[{stt}] {meta["name"]}'
            if meta['modifiedTime'] > moc:
                print('BỎ QUA (Drive sửa sau mốc)', tag, meta['modifiedTime'], '>', moc)
                continue
            if n_cm:
                print('BỎ QUA (đang có', n_cm, 'nhận xét — đẩy sẽ mất)', tag)
                continue
            if not go:
                print('SẼ ĐẨY', tag, f'{len(data) / 1e6:.1f} MB', '| Drive', meta['modifiedTime'])
                continue
            res = call(urllib.request.Request(
                f'https://www.googleapis.com/upload/drive/v3/files/{fid}?uploadType=media&supportsAllDrives=true'
                '&fields=md5Checksum,modifiedTime',
                data=data, method='PATCH', headers={**hdr, 'Content-Type': MIME}))
            ok = res['md5Checksum'] == hashlib.md5(data).hexdigest()
            print('OK' if ok else 'LỆCH MD5', tag, res['modifiedTime'], flush=True)
            if ok:
                log[fid] = res['modifiedTime']
                json.dump(log, open(LOG, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
            time.sleep(2)


if __name__ == '__main__':
    main()
