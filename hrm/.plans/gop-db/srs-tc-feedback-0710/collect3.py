import json,os,docx,re
from docx.oxml.ns import qn
L=json.load(open('srs_list.json'))
def txt(e): return ''.join(x.text or '' for x in e.iter(qn('w:t')))
PAT=re.compile(r'^\s*(Người cập nhật|Ngày cập nhật|Người tạo|Ngày tạo|Thời gian cập nhật|Thời gian tạo|Ngày giờ tạo|Ngày giờ cập nhật|Người sửa|Ngày sửa)\b',re.I)
out=[]
for x in L:
    f=f"drive/{x['id']}.docx"
    if not os.path.exists(f): continue
    d=docx.Document(f)
    for ti,t in enumerate(d.element.body.iter(qn('w:tbl'))):
        rows=t.findall(qn('w:tr'))
        if not rows: continue
        hdr=[txt(c).strip() for c in rows[0].findall(qn('w:tc'))]
        try: dc=max(i for i,h in enumerate(hdr) if re.search(r'mô tả|ghi chú|xử lý|nội dung',h,re.I))
        except ValueError: dc=len(hdr)-1
        for ri,tr in enumerate(rows[1:],1):
            cells=[txt(c).strip() for c in tr.findall(qn('w:tc'))]
            for ci,c in enumerate(cells[:3]):
                m=PAT.match(c)
                if m and len(c)<40:
                    out.append(dict(id=x['id'],doc=x['name'],t=ti,r=ri,nc=ci,dc=dc,name=c,desc=cells[dc] if dc<len(cells) else '',hdr=hdr)); break
json.dump(out,open('item3_rows.json','w'),ensure_ascii=False,indent=1)
print(len(out))
from collections import Counter
for (n,dsc),k in Counter((o['name'],o['desc']) for o in out).most_common(): print(k,'|',n,'|',dsc[:160])
