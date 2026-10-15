import sys,docx
from docx.oxml.ns import qn
d=docx.Document(sys.argv[1]); body=list(d.element.body.iterchildren())
want=[int(x) for x in sys.argv[2:]]
def txt(e): return ''.join(x.text or '' for x in e.iter(qn('w:t')))
for i in want:
    el=body[i]
    for r,tr in enumerate(el.findall(qn('w:tr'))):
        print(i,r,' || '.join(txt(tc).replace('\n',' ')[:200] for tc in tr.findall(qn('w:tc'))))
    print()
