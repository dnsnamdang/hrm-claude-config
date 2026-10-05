"""python3 upload.py <slug> — ghi đè HDSD + SRS của danh mục lên Drive, GIỮ NGUYÊN ID (kiểm lại sau khi đẩy)."""
import json, sys, os, subprocess
H = os.path.dirname(os.path.abspath(__file__))
ROOT = '1f6lwBkUC0cm_9VGxYdaoBDrJP5RS26q6'
slug = sys.argv[1]
x = next(i for i in json.load(open(os.path.join(H, 'index.json'))) if i['slug'] == slug)
I = {f['ID']: f['Path'] for f in json.load(open(os.path.join(H, 'drive_ls.json')))}
sys.path.insert(0, os.path.join(H, '..', '_catalog_docs_lib'))
from catalog_v2 import load_cfg
cfg = load_cfg(slug)
only = sys.argv[2] if len(sys.argv) > 2 else None
for k, loc in (('hdsd', cfg['file_hdsd']), ('srs', cfg['file_srs'])):
    if only and k != only:
        continue
    src = os.path.join(H, slug, 'out', loc)
    dst = I[x[k + '_id']]
    cmd = ['rclone', 'copyto', src, 'gdrive:' + dst, '--drive-root-folder-id=' + ROOT]
    if len(x[k + '_id']) > 40:  # file đã bị chuyển thành Google Docs → ghi nội dung docx vào đúng file đó
        cmd.append('--drive-import-formats=docx')
    subprocess.run(cmd, check=True)
    out = subprocess.run(['rclone', 'lsjson', 'gdrive:' + dst, '--drive-root-folder-id=' + ROOT], capture_output=True, text=True).stdout
    j = json.loads(out)
    ok = j and j[0]['ID'] == x[k + '_id']
    print(k, dst, 'OK giữ ID' if ok else 'SAI ID!!', j[0]['ModTime'] if j else '')
