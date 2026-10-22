import openpyxl,sys,collections,re
f17,d=sys.argv[1],sys.argv[2]
norm=lambda s: re.sub(r'\s+',' ',str(s).strip()).casefold() if s not in (None,'') and str(s).strip() else None
rd=lambda f:[l.rstrip('\n').split('\t') for l in open(d+f,encoding='utf-8')]
T={norm(n):int(i) for i,n in rd('types.tsv')}
G={int(i):(n,int(s)) for i,n,s in rd('groups.tsv')}
g2t=collections.defaultdict(set); miss=set()
for r in list(openpyxl.load_workbook(f17,read_only=True,data_only=True)['NewERP Green Power'].iter_rows(values_only=True))[1:]:
    if not any(r[1:6]): continue
    g=r[8]
    try: g=int(float(g))
    except: continue
    l=norm(r[4])
    if not l: continue
    if l in T: g2t[g].add(T[l])
    else: miss.add(l)
print('Loại tên không khớp DB:',len(miss))
print('Bảng ghép: nhóm',len(g2t),'| cặp',sum(len(v) for v in g2t.values()),'| nhóm 1–1',sum(1 for v in g2t.values() if len(v)==1))
# Thuộc tính
AG=[(int(g),int(a)) for g,a in rd('attr_groups.tsv')]
cov=[x for x in AG if x[0] in g2t]; unc=[x for x in AG if x[0] not in g2t]
pairs={(t,a) for g,a in cov for t in g2t[g]}
print('\nTHUỘC TÍNH: liên kết',len(AG),'| nhóm có liên kết',len({g for g,_ in AG}),'| thuộc tính',len({a for _,a in AG}))
print(' có trong bảng ghép:',len(cov),'liên kết /',len({g for g,_ in cov}),'nhóm ⇒',len(pairs),'cặp Loại–thuộc tính trên',len({t for t,_ in pairs}),'Loại')
print(' KHÔNG có trong bảng ghép:',len(unc),'liên kết /',len({g for g,_ in unc}),'nhóm (mất)')
# Loại nhận thuộc tính từ >1 nhóm (bị gộp)
src=collections.defaultdict(set)
for g,a in cov:
    for t in g2t[g]: src[t].add(g)
merged=[t for t,v in src.items() if len(v)>1]
print(' Loại gộp thuộc tính từ >1 nhóm:',len(merged))
ga=collections.defaultdict(set)
for g,a in AG: ga[g].add(a)
diff=[t for t in merged if len({frozenset(ga[g]) for g in src[t]})>1]
print('  trong đó các nhóm nguồn có BỘ thuộc tính khác nhau:',len(diff))
# Nhóm máy
MG=[(int(p),int(g),(int(s) if s!='NULL' else None)) for p,g,s in rd('machine_groups.tsv')]
live=[x for x in MG if x[2] not in (0,None)]
print('\nNHÓM MÁY: liên kết',len(MG),'| hàng phụ tùng còn dùng',len(live),'liên kết /',len({p for p,_,_ in live}),'hàng | nhóm máy',len({g for _,g,_ in live}))
c=[x for x in live if x[1] in g2t]; u=[x for x in live if x[1] not in g2t]
mp={(p,t) for p,g,_ in c for t in g2t[g]}
print(' có trong bảng ghép:',len(c),'liên kết /',len({g for _,g,_ in c}),'nhóm ⇒',len(mp),'cặp hàng–Loại (mở rộng x',round(len(mp)/max(len(c),1),1),')')
print(' KHÔNG có trong bảng ghép:',len(u),'liên kết /',len({g for _,g,_ in u}),'nhóm /',len({p for p,_,_ in u}),'hàng')
fan=collections.Counter(len(g2t[g]) for _,g,_ in c)
print(' số Loại mỗi nhóm máy (theo liên kết):',sorted(fan.items())[:12])
top=sorted({g for _,g,_ in c},key=lambda g:-len(g2t[g]))[:5]
print(' nhóm máy nhiều Loại nhất:',[(g,G.get(g,('?',))[0],len(g2t[g])) for g in top])
