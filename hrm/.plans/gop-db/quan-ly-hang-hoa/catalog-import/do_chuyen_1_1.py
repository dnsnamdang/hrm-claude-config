import openpyxl,sys,collections,re
f17,d=sys.argv[1],sys.argv[2]
norm=lambda s: re.sub(r'\s+',' ',str(s).strip()).casefold() if s not in (None,'') and str(s).strip() else None
rd=lambda f:[l.rstrip('\n').split('\t') for l in open(d+f,encoding='utf-8')]
T={norm(n):int(i) for i,n in rd('types.tsv')}
g2t=collections.defaultdict(set)
for r in list(openpyxl.load_workbook(f17,read_only=True,data_only=True)['NewERP Green Power'].iter_rows(values_only=True))[1:]:
    if not any(r[1:6]): continue
    try: g=int(float(r[8]))
    except: continue
    l=norm(r[4])
    if l in T: g2t[g].add(T[l])
t2g=collections.defaultdict(set)
for g,v in g2t.items():
    for t in v: t2g[t].add(g)
one=lambda g: len(g2t.get(g,()))==1
both=lambda g: one(g) and len(t2g[next(iter(g2t[g]))])==1
AG=[(int(g),int(a)) for g,a in rd('attr_groups.tsv')]
MG=[(int(p),int(g)) for p,g,s in rd('machine_groups.tsv') if s not in ('0','NULL')]
for name,f in (('nhóm→1 Loại',one),('1–1 hai chiều',both)):
    ag=[x for x in AG if f(x[0])]; pr={(next(iter(g2t[g])),a) for g,a in ag}
    # Loại nhận từ >1 nhóm 1-chiều: hợp hay không?
    mg=[x for x in MG if f(x[1])]
    print(f'{name}: nhóm {sum(1 for g in g2t if f(g))} | THUỘC TÍNH {len(ag)}/{len(AG)} liên kết, {len({g for g,_ in ag})} nhóm ⇒ {len(pr)} cặp / {len({t for t,_ in pr})} Loại | NHÓM MÁY {len(mg)}/{len(MG)} liên kết, {len({g for _,g in mg})} nhóm, {len({p for p,_ in mg})} hàng')
# với "nhóm→1 Loại": Loại nhận thuộc tính từ >1 nhóm 1-chiều với bộ khác nhau
ga=collections.defaultdict(set)
for g,a in AG: ga[g].add(a)
src=collections.defaultdict(set)
for g,a in AG:
    if one(g): src[next(iter(g2t[g]))].add(g)
print('nhóm→1 Loại: Loại nhận từ >1 nhóm', sum(1 for v in src.values() if len(v)>1), '— bộ khác nhau', sum(1 for v in src.values() if len(v)>1 and len({frozenset(ga[g]) for g in v})>1))
