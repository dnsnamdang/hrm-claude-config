import sys,json,unicodedata,collections,re
D=sys.argv[1]
def rd(f): return [l.rstrip('\n').split('\t') for l in open(f'{D}/{f}',encoding='utf-8') if l.strip()]
def dash(s): return re.sub(r'\s+',' ',re.sub(r'\s*,\s*',' - ',s)).strip()
def key(s):
    s=unicodedata.normalize('NFD',dash(s).replace('đ','d').replace('Đ','D'))
    return ' '.join(''.join(c for c in s if unicodedata.category(c)!='Mn').lower().split())
T={r[0]:r for r in rd('tpath.tsv')}; F={r[0]:r for r in rd('fpath.tsv')}; G={r[0]:r for r in rd('gpath.tsv')}; N={r[0]:r for r in rd('npath.tsv')}
LV={1:'Tính chất',2:'Nhóm chức năng',3:'Nhóm sản phẩm',4:'Loại sản phẩm'}
PX={1:'TCHH',2:'NCN',3:'NSP',4:'LSP'}; NXT={1:7,2:49,3:283,4:969}
rows=[];skip=[]
for x in rd('xres.tsv'):
    r,ten,model,n,g,f,t,nt,nf,ng,nn,mid,tid,fid,gid,nid=x
    o={'r':int(r),'ten':ten,'model':model,'file':[n,g,f,t],'mid':mid}
    if not mid: o['ly_do']='Model chưa có trên DB'; skip.append(o); continue
    if t.strip()=='0': o['ly_do']='Loại SP trong file = "0" (chưa điền)'; skip.append(o); continue
    if tid: o['db']=(4,tid); o['new']=[]
    else:
        chain=[(4,t)]  # node moi tu duoi len
        if fid: o['db']=(3,fid)
        else:
            chain.append((3,f))
            if gid: o['db']=(2,gid)
            else:
                chain.append((2,g))
                if nid: o['db']=(1,nid)
                else: chain.append((1,n)); o['db']=None
        o['new']=chain
    rows.append(o)
def parent_id(o,i):
    ch=o['new']
    if i+1<len(ch): return ('new',ch[i+1][0],key(ch[i+1][1]))
    return ('db',)+tuple(o['db']) if o['db'] else None
while True:
    par=collections.defaultdict(set); who=collections.defaultdict(list)
    for o in rows:
        for i,(lv,nm) in enumerate(o['new']):
            par[(lv,key(nm))].add(parent_id(o,i)); who[(lv,key(nm))].append(o)
    bad=[k for k,v in par.items() if len(v)>1]
    if not bad: break
    drop=set()
    for k in bad:
        for o in who[k]:
            if id(o) not in drop:
                drop.add(id(o)); o['ly_do']=f'{LV[k[0]]} mới "{o["new"][[key(nm) for lv,nm in o["new"]].index(k[1])][1]}" nằm dưới nhiều cha khác nhau trong file'
                skip.append(o)
    rows=[o for o in rows if id(o) not in drop]
# tao node moi
nodes={}  # (lv,key)->info
for o in rows:
    for i,(lv,nm) in enumerate(o['new']):
        k=(lv,key(nm)); nd=nodes.setdefault(k,{'lv':lv,'names':collections.Counter(),'rows':[],'first':o['r'],'parent':parent_id(o,i)})
        nd['names'][dash(nm)]+=1; nd['rows'].append(o['r'])
for lv in (1,2,3,4):
    for k,nd in sorted([(k,v) for k,v in nodes.items() if k[0]==lv], key=lambda kv: kv[1]['first']):
        best=max(nd['names'].items(), key=lambda kv:(kv[1], -list(nd['names']).index(kv[0])))[0]
        nd['name']=best; nd['code']=f'{PX[lv]}.{NXT[lv]:04d}'; NXT[lv]+=1
def dbpath(lv,id):
    if lv==4: r=T[id]; return [(r[10],r[11]),(r[7],r[8]),(r[4],r[5]),(r[1],r[2])]
    if lv==3: r=F[id]; return [(r[7],r[8]),(r[4],r[5]),(r[1],r[2])]
    if lv==2: r=G[id]; return [(r[4],r[5]),(r[1],r[2])]
    r=N[id]; return [(r[1],r[2])]
for o in rows:
    p=[(c,nm,'có sẵn') for c,nm in (dbpath(*o['db']) if o['db'] else [])]
    for lv,nm in reversed(o['new']):
        nd=nodes[(lv,key(nm))]; p.append((nd['code'],nd['name'],'MỚI'))
    o['path']=p; assert len(p)==4
    o['lech']=[LV[i+1] for i in range(4) if key(p[i][1])!=key(o['file'][i])]
    o['how']='Loại có sẵn trên DB' if not o['new'] else 'Loại mới tạo'
newlist=[]
for k,nd in nodes.items():
    pr=nd['parent']
    if pr is None: pc,pn,ps='','',''
    elif pr[0]=='db':
        pth=dbpath(pr[1],pr[2]); pc,pn=pth[-1]; ps='có sẵn'
    else: pp=nodes[(pr[1],pr[2])]; pc,pn,ps=pp['code'],pp['name'],'MỚI'
    newlist.append({'cap':nd['lv'],'cap_ten':LV[nd['lv']],'code':nd['code'],'name':nd['name'],'pcode':pc,'pname':pn,'psrc':ps,'so_dong':len(nd['rows']),'dong':nd['rows'],'bien_the':[n for n in nd['names'] if n!=nd['name']]})
newlist.sort(key=lambda d:(d['cap'],d['code']))
# hang hoa
P=collections.defaultdict(list)
for p in rd('prods.tsv'): P[p[0]].append(p)
CTY={'1':'Tân Phát','2':'Hải Phòng','3':'Vinh','4':'Sài Gòn','5':'TĐH Tân Phát','6':'Upservice','7':'ETEK Green (cũ)','8':'Tập đoàn ETEK','9':'ETEK Green'}
upd={};keep={}
for o in rows:
    for p in P[o['mid']]:
        mid,pid,code,name,cty,st,ptid,ptname=p
        rec={'pid':int(pid),'code':code,'name':name,'cty':CTY.get(cty,cty),'status':'Đang dùng' if st!='0' else 'Đã xoá (status 0)','model':o['model'],'r':o['r']}
        if ptid: rec['loai_hien_tai']=ptname; keep.setdefault(pid,rec)
        elif pid not in upd: rec.update({'path':o['path'],'how':o['how'],'lech':o['lech'],'file':o['file']}); upd[pid]=rec
for o in rows:
    if not P[o['mid']]: o['khong_hang']=True
json.dump({'rows':rows,'skip':sorted(skip,key=lambda s:s['r']),'new':newlist,'upd':sorted(upd.values(),key=lambda u:u['r']),'keep':list(keep.values())},open(f'{D}/resolved2.json','w'),ensure_ascii=False,indent=0)
c=collections.Counter
print('dong hop le',len(rows),'bo qua',len(skip),c(s['ly_do'][:40] for s in skip))
print('moi',c(n['cap'] for n in newlist))
print('hang gan',len(upd),c(u['how'] for u in upd.values()),c(u['status'] for u in upd.values()),'giu nguyen',len(keep))
print('dong lech cay',sum(1 for o in rows if o['lech']),'model khong co hang',sum(1 for o in rows if o.get('khong_hang')))
print('bien the ten',[ (n['name'],n['bien_the']) for n in newlist if n['bien_the']])
