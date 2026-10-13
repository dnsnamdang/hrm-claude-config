# plans/NN.json + workbook đã tải -> danh sách op (chạy từ dưới lên trong từng tab)
import json,sys,openpyxl,re,os
sys.path.insert(0, os.path.dirname(__file__))
from gen_js import tsv
S=os.path.dirname(os.path.abspath(__file__))
wb=openpyxl.load_workbook(os.path.join(S,'tc/tc.xlsx'))
def cval(ws,r,c):
    v=ws.cell(r,c).value
    return '' if v is None else str(v)
def merge_of(ws,col,r):
    for m in ws.merged_cells.ranges:
        if m.min_col<=col<=m.max_col and m.min_row<=r<=m.max_row: return m
    return None
def group_start(ws,r):
    # hàng case đầu nhóm = hàng ngay dưới hàng tiêu đề nhóm (cột C là tiêu đề La Mã)
    x=r
    while x>18 and re.match(r'^TC', cval(ws,x-1,3)): x-=1
    return x
def build(nn):
    p=json.load(open(os.path.join(S,'plans',f'{nn}.json')))
    ws=wb.worksheets[int(nn)]
    assert ws.title.strip()==p['tab'].strip(), (ws.title,p['tab'])
    ops=[]; nextval={}
    for ins in [x for _,x in sorted(enumerate(p['inserts']), key=lambda t:(-t[1]['after_row'], 0 if t[1].get('new_group') else 1, -t[0]))]:
        r=ins['after_row']; cases=ins['cases']; n=len(cases)
        if not n: continue
        expect=cval(ws,r,3); assert expect.startswith('TC'), (nn,r,expect)
        rows=[[c['id'],c['func'],c['priority'],c['pre'],c['steps'],c['data'],c['expected']] for c in cases]
        op={'tab':ws.title.strip()[:20],'after_row':r,'expect_c':expect,'expect_next':cval(ws,r+1,3),
            'tsv':tsv(rows),'last_id':cases[-1]['id'],'first_id':cases[0]['id'],'merges':[],'header_from':None,'ab_tsv':None}
        if not ins.get('new_group'):
            op['n_rows']=n; op['paste_at']=f'C{r+1}'; op['last_case_row']=r+n
            gs=group_start(ws,r)
            for col,L in ((1,'A'),(2,'B')):
                m=merge_of(ws,col,r); s=m.min_row if m else gs
                op['merges'].append(f'{L}{s}:{L}{r+n}')
        else:
            # hàng tiêu đề của nhóm cuối cùng làm khuôn
            h=group_start(ws,r)-1
            op['n_rows']=n+1; op['header_from']=h; op['header_title']=ins['group_title']
            op['paste_at']=f'C{r+2}'; op['first_case_row']=r+2; op['last_case_row']=r+1+n
            op['ab_tsv']=tsv([[p.get('module',''), ins['group_name']]])
            op['merges']=[f'A{r+2}:A{r+1+n}', f'B{r+2}:B{r+1+n}'] if n>1 else []
        if r in nextval: op['expect_next']=nextval[r]
        nextval[r]=op['header_title'] if op['header_from'] else cases[0]['id']
        ops.append(op)
    return ops
if __name__=='__main__':
    nn=sys.argv[1]
    ops=build(nn)
    out=os.path.join(S,'ops',nn); os.makedirs(out,exist_ok=True)
    json.dump({'tab':wb.worksheets[int(nn)].title.strip()[:20],'count':len(ops)},open(os.path.join(out,'index.json'),'w'),ensure_ascii=False)
    tpl=open(os.path.join(S,'runner_tpl.js')).read()
    J='/Users/manhcuong/Desktop/dns/HRM/.playwright-mcp/tcw'
    open(os.path.join(J,f'run_{nn}.js'),'w').write(tpl.replace('__NN__',nn).replace('__FROM__','0').replace('__ONLY__','null'))
    for i,o in enumerate(ops):
        json.dump(o,open(os.path.join(out,f'{i:02d}.json'),'w'),ensure_ascii=False)
        print(i,o['after_row'],o['n_rows'],o['expect_c'],'->',o['last_id'],o['merges'],'NEW' if o['header_from'] else '')
