import openpyxl,sys,re,collections
wb=openpyxl.load_workbook(sys.argv[1],data_only=True,read_only=True)
ws=wb.worksheets[0]
def c(v): return re.sub(r'\s+',' ',str(v)).strip() if v is not None else ''
rows=[]
for i,r in enumerate(ws.iter_rows(values_only=True)):
    if i==0: continue
    r=list(r)+[None]*7
    stt,ten,model,n,g,f,t=[c(x) for x in r[:7]]
    if not any([ten,model,n,g,f,t]): continue
    rows.append((i+1,ten,model,n,g,f,t))
print('so dong',len(rows))
miss=[r for r in rows if not all(r[2:])]
print('dong thieu o (model/4 cap):',len(miss)); [print('  ',m) for m in miss[:15]]
bym=collections.defaultdict(set)
for r in rows:
    if r[2]: bym[r[2].upper()].add(r[3:])
conf={m:v for m,v in bym.items() if len(v)>1}
print('model trung khac danh muc:',len(conf)); [print('  ',m,v) for m,v in list(conf.items())[:10]]
print('model lap lai (cung danh muc):',sum(1 for m in bym if sum(1 for r in rows if r[2].upper()==m)>1 and m not in conf))
# cung ten cap duoi nhung khac cha trong file
for lv,name in [(4,'Nhom chuc nang'),(5,'Nhom SP'),(6,'Loai SP')]:
    par=collections.defaultdict(set)
    for r in rows:
        if r[lv]: par[r[lv].lower()].add(r[lv-1].lower())
    bad={k:v for k,v in par.items() if len(v)>1}
    print(f'{name}: cung ten khac cha trong file = {len(bad)}'); [print('  ',k,v) for k,v in list(bad.items())[:8]]
with open(sys.argv[2],'w') as fo:
    for r in rows: fo.write('\t'.join(map(str,r))+'\n')
