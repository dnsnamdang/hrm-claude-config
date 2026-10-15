import re
KEYS=[('nguoi_cn',r'^(Người cập nhật|Người sửa)'),('ngay_cn',r'^(Ngày cập nhật|Ngày giờ cập nhật|Thời gian cập nhật|Ngày sửa)'),
      ('nguoi_tao',r'^Người tạo'),('ngay_tao',r'^(Ngày tạo|Ngày giờ tạo|Thời gian tạo)')]
DISP={'nguoi_cn':'Người cập nhật bản ghi gần nhất','ngay_cn':'Ngày giờ cập nhật bản ghi gần nhất',
      'nguoi_tao':'Người tạo bản ghi','ngay_tao':'Ngày giờ tạo bản ghi'}
FILT={'nguoi_cn':'Lọc theo người cập nhật bản ghi gần nhất','ngay_cn':'Lọc theo ngày cập nhật bản ghi gần nhất',
      'nguoi_tao':'Lọc theo người tạo bản ghi','ngay_tao':'Lọc theo ngày tạo bản ghi'}
OK={'nguoi_cn':r'(cập nhật|sửa) bản ghi gần nhất','ngay_cn':r'(cập nhật|sửa) bản ghi gần nhất',
    'nguoi_tao':r'(tạo|thêm) bản ghi','ngay_tao':r'(tạo|thêm) bản ghi'}
def keys_of(name):
    ks=[]
    for part in re.split(r'\s*[/,]\s*',re.sub(r'^(Cột|Ô|Lọc)\s+','',name.strip())):
        for k,p in KEYS:
            if re.match(p,part,re.I) and k not in ks: ks.append(k)
    return ks
def is_filter(name,desc,typ):
    s=(desc+' '+typ).lower()
    return bool(re.search(r'lọc|nhãn nổi|khoảng|từ ngày|chọn nhân|chọn nhân sự|từ\s*(→|–|-)\s*đến',s)) or bool(re.search(r'\btừ\b|\bđến\b',name))
DEF_WORDS=r'(gần nhất|đã thêm bản ghi|đã tạo bản ghi|tạo bản ghi|thêm bản ghi|ngày tạo mới bản ghi|người (đã )?(tạo|thêm|sửa|cập nhật)|(ngày|thời điểm|thời gian) (thêm|tạo|sửa|cập nhật))'
KEEP_WORDS=r'(hoặc|dd/|định dạng|cấu trúc|sắp xếp|mặc định|lọc|chọn|mã phòng|trống|không đổi|sửa được|ⓘ)'
import unicodedata
def transform(name,desc,typ=''):
    name=unicodedata.normalize('NFC',name); desc=unicodedata.normalize('NFC',desc)
    ks=keys_of(name)
    if not ks: return None
    d=desc.strip()
    if all(re.search(OK[k],d,re.I) for k in ks): return None
    filt=is_filter(name,d,typ)
    lead=' / '.join((FILT if filt else DISP)[k] for k in ks)
    if filt and len(ks)>1: lead='Lọc theo '+' / '.join(FILT[k][9:] for k in ks)
    sents=[s for s in re.split(r'(?<=[.;])\s+',d) if s.strip() and s.strip() not in ('–','-')]
    out=[]
    PURE=r'^(hiển thị\s+)?(tên\s+)?(người|ngày|thời gian|thời điểm|ngày và thời gian)(\s+(đã|thực hiện))?\s+(tạo|thêm|sửa|cập nhật)[^.;,]{0,25}?(gần nhất|bản ghi|mới bản ghi|tài khoản)?\.?$'
    for s in sents:
        low=s.lower().strip()
        if re.match(PURE,low) and not re.search(r'(dd/|định dạng|cấu trúc|sắp xếp|mặc định|→|hoặc|chính|lọc|hiển thị tên|họ tên|nhân viên)',low): continue
        if low in ('người đã thêm bản ghi.','người tạo gói.','người đã tạo bản ghi.'): continue
        if filt and low.startswith('lọc theo') and re.search(r'(gần nhất|bản ghi)',low) and not re.search(r'(dd/|định dạng|cấu trúc|khoảng|trọn|hoặc)',low): continue
        s2=re.sub(r'^Hiển thị\s+[^,]*?(gần nhất|bản ghi)[^,]*,\s*','',s,flags=re.I)
        s2=re.sub(r'^Hiển thị\s+[^,]*?gần nhất\s+(?=theo\b)','',s2,flags=re.I)
        if s2!=s: s=s2[0].upper()+s2[1:]; low=s.lower()
        if re.search(DEF_WORDS,low) and re.search(r'(dd/|định dạng)',low):
            s2=re.sub(r'^(Hiển thị\s+)?(ngày và thời gian|thời điểm|thời gian|ngày giờ)\s+[^,]*?(gần nhất|bản ghi|tạo|thêm|sửa)[^,]*,\s*(theo\s+)?','',s,flags=re.I)
            if s2!=s: s=s2[0].upper()+s2[1:]
        if s.lower().rstrip('.')==name.lower(): continue
        out.append(s.strip())
    if out and re.match(r'^theo (cấu trúc|định dạng)',out[0],re.I):
        first=out.pop(0); first=first[0].lower()+first[1:]
        return lead+', '+first+((' '+' '.join(out)) if out else '')
    if out and re.match(r'^(dạng\s+)?dd/',out[0],re.I):
        first=re.sub(r'^dạng\s+','',out.pop(0),flags=re.I)
        return lead+', dạng '+first+((' '+' '.join(out)) if out else '')
    new=lead+'.'+((' '+' '.join(out)) if out else '')
    return new
