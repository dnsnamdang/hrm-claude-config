import json,re,os,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from locate import units, occ, N
H=os.path.dirname(os.path.abspath(__file__))
P=json.load(open(os.path.join(H,'post_plan.json')))
def tkey(t):
    m=re.match(r'(\d+):(\d+), (\d+) thg (\d+)',t); return (int(m.group(4)),int(m.group(3)),int(m.group(1)),int(m.group(2)))
cache={}
for f in sorted(set(x['file'] for x in P)):
    rows=[x for x in P if x['file']==f]
    cur=cache.setdefault(rows[0]['id'],units(os.path.join(H,'cur',rows[0]['id']+'.docx')))
    rows.sort(key=lambda x:tkey(x['posts'][0][1]))
    lastpos={}; lastany=None
    for x in rows:
        au=x['posts'][0][0]
        if x['target']:
            o=occ(cur,x['target'])
            if x['how'].startswith('gần đúng'):
                lp=lastpos.get(au,-1)
                after=[(n,u) for n,u in enumerate(o) if u>=lp]
                n,u=(after[0] if after else (0,o[0]))
                x['occ_index']=n+1; x['how']='gần đúng (chọn theo thứ tự nhận xét)'
            pos=o[x['occ_index']-1] if o and x['occ_index']<=len(o) else None
            if pos is not None: lastpos[au]=pos; lastany=(x['target'],x['occ_index'])
        elif lastany:
            x['target'],x['occ_index']=lastany; x['how']='không còn đoạn gốc — gắn cạnh nhận xét liền trước'
        x['occ_total']=len(occ(cur,x['target'])) if x['target'] else 0
json.dump(P,open(os.path.join(H,'post_plan.json'),'w'),ensure_ascii=False,indent=1)
from collections import Counter
print(Counter(x['how'] for x in P)); print('chưa có chỗ:',sum(1 for x in P if not x['target']))
