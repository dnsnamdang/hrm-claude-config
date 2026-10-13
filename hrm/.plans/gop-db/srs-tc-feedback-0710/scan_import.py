import json,os,docx,re
from docx.oxml.ns import qn
L=json.load(open('srs_list.json'))
def txt(e): return ''.join(x.text or '' for x in e.iter(qn('w:t')))
def sty(p):
    pp=p.find(qn('w:pPr'))
    if pp is None or pp.find(qn('w:pStyle')) is None: return ''
    return pp.find(qn('w:pStyle')).get(qn('w:val'))
for x in L:
    f=f"drive/{x['id']}.docx"
    if not os.path.exists(f): continue
    d=docx.Document(f); body=list(d.element.body.iterchildren())
    heads=[(i,txt(e)) for i,e in enumerate(body) if e.tag.endswith('}p') and sty(e).startswith('Heading') and re.search(r'import|nhập .*excel|nhập từ file',txt(e),re.I)]
    upd=sum(1 for e in body if e.tag.endswith('}tbl') for tr in e.iter(qn('w:tr')) if re.search(r'^(Người|Ngày) (cập nhật|tạo)',txt(tr.findall(qn('w:tc'))[1]) if len(tr.findall(qn('w:tc')))>1 else ''))
    print(x['part'],x['name'][:38],'| import heads:',[(i,h[:45]) for i,h in heads],'| rows Người/Ngày:',upd)
