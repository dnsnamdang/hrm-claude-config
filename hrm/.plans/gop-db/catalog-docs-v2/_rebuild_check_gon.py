# Dựng lại + kiểm toàn bộ HDSD gọn: trang trắng, chú thích tách ảnh, mũi tên, mục đích.
import json, os, subprocess, sys, fitz
from docx import Document
H = os.path.dirname(os.path.abspath(__file__))
S = sys.argv[1]
T = {t['slug']: t['drive_name'] for t in json.load(open(os.path.join(H, 'hdsd_gon_targets.json')))}
T['provinces'] = 'HDSD_Danh mục Tỉnh-TP.docx'; T['type-accounts'] = 'HDSD_Danh mục loại tài khoản.docx'
slugs = sys.argv[2:] or list(T)
for s in slugs:
    r = subprocess.run(['python3', 'gen_hdsd_gon.py'], cwd=os.path.join(H, s), capture_output=True, text=True, timeout=600)
    if r.returncode:
        print(s, 'LỖI DỰNG', r.stderr[-300:]); continue
    f = os.path.join(H, s, 'out', T[s]); dst = os.path.join(S, 'r_' + s + '.docx')
    subprocess.run(['cp', f, dst]); pdf = dst[:-5] + '.pdf'
    if os.path.exists(pdf): os.remove(pdf)
    subprocess.run(['soffice', '-env:UserInstallation=file://' + S + '/lo_profile', '--headless', '--convert-to', 'pdf', '--outdir', S, dst], capture_output=True, timeout=300)
    d = fitz.open(pdf); t = [p.text for p in Document(dst).paragraphs]
    blank = [i + 1 for i in range(len(d)) if not d[i].get_text().strip() and not d[i].get_images()]
    tach = []   # chú thích nằm cao hơn mọi ảnh lớn của trang = bị tách khỏi ảnh
    for i in range(1, len(d)):
        imgs = [b for b in d[i].get_image_info() if b['bbox'][3] - b['bbox'][1] > 40]
        top = min((b['bbox'][1] for b in imgs), default=1e9)
        tach += [i + 1 for bl in d[i].get_text('blocks') if bl[4].strip().startswith('Hình ') and bl[1] < top]
    print('%-22s trang %2d | trắng %s | chú thích tách %s | → %d | Mục đích %s' % (
        s, len(d), blank, tach, sum('→' in x for x in t), any('Mục đích' in x for x in t)), flush=True)
