# -*- coding: utf-8 -*-
"""Bộ kiểm thử seeder MasterDataPl8Seeder — Redmine #11303.
DB đích: hrm_prod_6_6 (SAU khi chạy) · DB đối chứng: hrm_pl8_before (TRƯỚC khi chạy)."""
import json, subprocess, collections, sys

AFTER='hrm_prod_6_6'; BEFORE='hrm_pl8_before'
def q(sql):
    r=subprocess.run(['mysql','-uroot','-N','-e',sql],capture_output=True,text=True)
    if r.returncode: raise RuntimeError(r.stderr)
    return [l.split('\t') for l in r.stdout.splitlines()]
def one(sql): return q(sql)[0][0]

sheet=json.load(open('sheets.json'))
def parse(x): return [p.strip() for p in x.split(',') if p.strip()]

results=[]
def tc(id,name,cond,detail=''):
    results.append((id,name,'PASS' if cond else 'FAIL',detail if not cond else ''))

# ---------- nạp trạng thái DB SAU ----------
FROWS={}; SROWS={}; IROWS={}; AROWS={}
for i,c,n,st in q("select id,code,name,status from %s.internal_business_scopes"%AFTER): FROWS[int(i)]=(c,n,int(st))
for i,c,n,st,f in q("select id,code,name,status,ifnull(internal_business_scope_id,0) from %s.scopes"%AFTER): SROWS[int(i)]=(c,n,int(st),int(f))
for i,c,n,st in q("select id,code,name,status from %s.industries"%AFTER): IROWS[int(i)]=(c,n,int(st))
for i,c,n,st in q("select id,code,name,status from %s.applications"%AFTER): AROWS[int(i)]=(c,n,int(st))

def uniq(rows, code, name):
    hit=[i for i,v in rows.items() if v[0]==code and v[1]==name]
    return hit[0] if len(hit)==1 else None

ISC=collections.defaultdict(set)
for a,b in q("select industry_id,scope_id from %s.industry_scopes"%AFTER): ISC[int(a)].add(int(b))
APAIR=collections.defaultdict(set); ASCO=collections.defaultdict(set)
for a,s,i in q("select application_id,ifnull(scope_id,0),industry_id from %s.application_industries"%AFTER): APAIR[int(a)].add((int(s),int(i)))
for a,s in q("select application_id,scope_id from %s.application_scopes"%AFTER): ASCO[int(a)].add(int(s))
ACODE={v[0]:i for i,v in AROWS.items()}

# ================= AC1 — mã lĩnh vực =================
bad=[]
for r in sheet['linh_vuc_cty_kinh_doanh']['rows']:
    if uniq(FROWS, r['Mã(cập nhật)'].strip(), r['Lĩnh vực công ty kinh doanh'].strip()) is None:
        bad.append(r['Mã(cập nhật)'])
tc('AC1','7 Lĩnh vực Công ty kinh doanh có mã LVCTKD mới, tên đúng, duy nhất', not bad, str(bad))
tc('AC1-b','Không còn mã LVKDNB.0001..0007 trong DB',
   int(one("select count(*) from %s.internal_business_scopes where code regexp '^LVKDNB\\\\.[0-9]'"%AFTER))==0)
tc('AC1-c','Bản ghi LVKDNB.KHAC giữ nguyên mã theo quyết định đã chốt',
   int(one("select count(*) from %s.internal_business_scopes where code='LVKDNB.KHAC'"%AFTER))==1)

# ================= AC2/AC3 — nhóm ngành =================
lvcode={r['Lĩnh vực công ty kinh doanh'].strip(): r['Mã(cập nhật)'].strip() for r in sheet['linh_vuc_cty_kinh_doanh']['rows']}
b_new=[]; b_field=[]; b_lock=[]; b_active=[]
for r in sheet['nhom_nganh']['rows']:
    code=r['Mã'].strip(); nm=r['Tên nhóm ngành'].strip(); note=r['Ghi chú'].strip()
    sid=uniq(SROWS,code,nm)
    if sid is None:
        (b_new if note=='Thêm mới nhóm ngành' else b_field).append(code); continue
    c,n,st,fid=SROWS[sid]
    if note=='Khóa nhóm ngành':
        if st!=2: b_lock.append(code)
        continue
    if st!=1: b_active.append(code)
    want=lvcode[r['Lĩnh vực công ty kinh doanh'].strip()]
    if not fid or FROWS[fid][0]!=want: b_field.append('%s->%s'%(code,want))
tc('AC2','13 nhóm ngành mới (NN.0023–NN.0035) tồn tại', not b_new, str(b_new))
tc('AC2-b','34 nhóm ngành (trừ nhóm bị khoá) đang Hoạt động', not b_active, str(b_active))
tc('AC2-c','Mọi nhóm ngành gắn đúng Lĩnh vực Công ty kinh doanh theo file', not b_field, str(b_field))
tc('AC3','Nhóm ngành NN.0012 chuyển trạng thái Khoá', not b_lock, str(b_lock))
tc('AC3-b','NN.0012 không còn nhóm giải pháp ĐANG HOẠT ĐỘNG nào trỏ vào',
   int(one("""select count(*) from %s.industry_scopes x join %s.scopes s on s.id=x.scope_id
             join %s.industries i on i.id=x.industry_id
             where s.code='NN.0012' and s.internal_business_scope_id is not null and i.status=1"""%(AFTER,AFTER,AFTER)))==0)

# ================= AC4 — nhóm giải pháp =================
b_map=[]; b_lk=[]
for r in sheet['nhom_giai_phap']['rows']:
    code=r['Mã nhóm giải pháp'].strip(); nm=r['Tên nhóm giải pháp'].strip()
    iid=uniq(IROWS,code,nm)
    if iid is None:
        b_map.append(code+' (không tra được)'); continue
    want=set(parse(r['Mã nhóm ngành mới']) or parse(r['Mã nhóm ngành']))
    got={SROWS[s][0] for s in ISC.get(iid,set())}
    if want!=got: b_map.append('%s: có %s, cần %s'%(code,sorted(got),sorted(want)))
    if r['Ghi chú'].strip()=='Khóa nhóm giải pháp' and IROWS[iid][2]!=2: b_lk.append(code)
tc('AC4','401 nhóm giải pháp gắn đúng tập Nhóm ngành theo file', not b_map, '; '.join(b_map[:5]))
tc('AC4-b','Nhóm giải pháp NGP.0167 chuyển trạng thái Khoá', not b_lk, str(b_lk))

# ================= AC5/AC6 — ứng dụng =================
b_pair=[]; b_sc=[]; b_nm=[]
for r in sheet['ung_dung']['rows']:
    code=r['Mã ứng dụng'].strip(); aid=ACODE.get(code)
    if not aid: b_pair.append(code+' (thiếu ứng dụng)'); continue
    use=parse(r['Map Nhóm ngành - Nhóm giải pháp Mã (Cập nhật)']) or parse(r['Map Nhóm ngành - Nhóm giải pháp Mã'])
    want={tuple(p.split(':')) for p in use}
    got={(SROWS[s][0], IROWS[i][0]) for s,i in APAIR.get(aid,set())}
    if want!=got: b_pair.append('%s: thừa %s thiếu %s'%(code,sorted(got-want)[:3],sorted(want-got)[:3]))
    wants={w[0] for w in want}; gots={SROWS[s][0] for s in ASCO.get(aid,set())}
    if wants!=gots: b_sc.append('%s: thừa %s thiếu %s'%(code,sorted(gots-wants)[:3],sorted(wants-gots)[:3]))
    nn=r['Tên ứng dụng (cập nhật)'].strip()
    if nn and AROWS[aid][1]!=nn: b_nm.append(code)
tc('AC5','145 ứng dụng có đúng cặp (Nhóm ngành : Nhóm giải pháp) theo file', not b_pair, '; '.join(b_pair[:5]))
tc('AC5-b','2 ứng dụng UD.0141 / UD.0142 đã đổi tên', not b_nm, str(b_nm))
tc('AC6','Tập Nhóm ngành của ứng dụng (application_scopes) suy đúng từ cặp', not b_sc, '; '.join(b_sc[:5]))
tc('AC6-b','Mọi ứng dụng đều còn >= 1 nhóm ngành (không bị xoá trắng)',
   int(one("select count(*) from %s.applications a where not exists (select 1 from %s.application_scopes x where x.application_id=a.id)"%(AFTER,AFTER)))==0)
tc('AC6-c','Cây 3 tầng khép kín: mọi cặp của ứng dụng đều tồn tại trong industry_scopes',
   int(one("""select count(*) from %s.application_industries ai
              left join %s.industry_scopes isc on isc.industry_id=ai.industry_id and isc.scope_id=ai.scope_id
              where isc.id is null"""%(AFTER,AFTER)))==0)

# ================= AC7 — dữ liệu lịch sử =================
for lbl,sql in [
 ('scopes -> lĩnh vực',      "select count(*) from {A}.scopes s left join {A}.internal_business_scopes f on f.id=s.internal_business_scope_id where s.internal_business_scope_id is not null and f.id is null"),
 ('industry_scopes',         "select count(*) from {A}.industry_scopes x left join {A}.scopes s on s.id=x.scope_id left join {A}.industries i on i.id=x.industry_id where s.id is null or i.id is null"),
 ('application_scopes',      "select count(*) from {A}.application_scopes x left join {A}.scopes s on s.id=x.scope_id left join {A}.applications a on a.id=x.application_id where s.id is null or a.id is null"),
 ('application_industries',  "select count(*) from {A}.application_industries x left join {A}.scopes s on s.id=x.scope_id left join {A}.industries i on i.id=x.industry_id where x.scope_id is null or s.id is null or i.id is null"),
 ('prospective_projects',    "select count(*) from {A}.prospective_projects p left join {A}.scopes s on s.id=p.scope_id left join {A}.industries i on i.id=p.industry_id left join {A}.applications a on a.id=p.application_id where (p.scope_id is not null and s.id is null) or (p.industry_id is not null and i.id is null) or (p.application_id is not null and a.id is null)"),
 ('request_solutions',       "select count(*) from {A}.request_solutions r left join {A}.scopes s on s.id=r.scope_id left join {A}.industries i on i.id=r.industry_id where (r.scope_id is not null and s.id is null) or (r.industry_id is not null and i.id is null)"),
 ('solutions',               "select count(*) from {A}.solutions x left join {A}.scopes s on s.id=x.scope_id left join {A}.industries i on i.id=x.industry_id left join {A}.applications a on a.id=x.application_id where (x.scope_id is not null and s.id is null) or (x.industry_id is not null and i.id is null) or (x.application_id is not null and a.id is null)"),
 ('meeting_investment_demands',"select count(*) from {A}.meeting_investment_demands m left join {A}.internal_business_scopes f on f.id=m.internal_business_scope_id left join {A}.scopes s on s.id=m.scope_id where (m.internal_business_scope_id is not null and f.id is null) or (m.scope_id is not null and s.id is null)"),
 ('form_template_snapshots', "select count(*) from {A}.form_template_snapshots t left join {A}.scopes s on s.id=t.scope_id left join {A}.industries i on i.id=t.industry_id left join {A}.applications a on a.id=t.application_id where (t.scope_id is not null and s.id is null) or (t.industry_id is not null and i.id is null) or (t.application_id is not null and a.id is null)"),
]:
    n_before=int(one(sql.format(A=BEFORE))); n_after=int(one(sql.format(A=AFTER)))
    note='' if n_after==0 else '(%d dòng mồ côi ĐÃ CÓ TỪ TRƯỚC, seeder không sinh thêm)'%n_after
    tc('AC7','Seeder không sinh thêm tham chiếu mồ côi: '+lbl+(' '+note if note else ''),
       n_after<=n_before, 'trước %d -> sau %d'%(n_before,n_after))

# ================= So sánh TRƯỚC / SAU =================
def cnt(db,t): return int(one("select count(*) from %s.%s"%(db,t)))
for t,expect in [('internal_business_scopes','same'),('applications','same'),('industries','same')]:
    tc('TC-01','Số bản ghi %s không đổi (không xoá, không tạo thừa)'%t, cnt(BEFORE,t)==cnt(AFTER,t),
       '%d -> %d'%(cnt(BEFORE,t),cnt(AFTER,t)))
tc('TC-01-b','scopes tăng đúng 13 bản ghi', cnt(AFTER,'scopes')-cnt(BEFORE,'scopes')==13,
   '%d -> %d'%(cnt(BEFORE,'scopes'),cnt(AFTER,'scopes')))
for t in ['internal_business_scopes','scopes','industries','applications']:
    tc('TC-02','Không bản ghi %s nào bị xoá (id cũ còn nguyên)'%t,
       int(one("select count(*) from {B}.{t} b left join {A}.{t} a on a.id=b.id where a.id is null".format(B=BEFORE,A=AFTER,t=t)))==0)

tc('TC-03','Bộ danh mục CŨ trùng mã (scopes id>22) không bị sửa',
   int(one("""select count(*) from {B}.scopes b join {A}.scopes a on a.id=b.id where b.id>22 and
        ((a.code<=>b.code)=0 or (a.name<=>b.name)=0 or (a.status<=>b.status)=0 or (a.internal_business_scope_id<=>b.internal_business_scope_id)=0)""".format(B=BEFORE,A=AFTER)))==0)
tc('TC-03-b','Bộ danh mục CŨ (industries id>401) không bị sửa',
   int(one("""select count(*) from {B}.industries b join {A}.industries a on a.id=b.id where b.id>401 and
        ((a.code<=>b.code)=0 or (a.name<=>b.name)=0 or (a.status<=>b.status)=0)""".format(B=BEFORE,A=AFTER)))==0)
tc('TC-03-c','industry_scopes của bộ CŨ không đổi số dòng',
   int(one("select count(*) from %s.industry_scopes where industry_id>401"%BEFORE))==int(one("select count(*) from %s.industry_scopes where industry_id>401"%AFTER)))

tc('TC-04','applications: không đổi mã, không đổi trạng thái',
   int(one("select count(*) from {B}.applications b join {A}.applications a on a.id=b.id where (a.code<=>b.code)=0 or (a.status<=>b.status)=0".format(B=BEFORE,A=AFTER)))==0)
tc('TC-04-b','applications: đúng 2 bản ghi đổi tên',
   int(one("select count(*) from {B}.applications b join {A}.applications a on a.id=b.id where (a.name<=>b.name)=0".format(B=BEFORE,A=AFTER)))==2)
# 126 ứng dụng không có cột "(Cập nhật)" phải giữ nguyên cặp y hệt trước khi chạy
unchanged={r['Mã ứng dụng'].strip() for r in sheet['ung_dung']['rows']
           if not r['Map Nhóm ngành - Nhóm giải pháp Mã (Cập nhật)'].strip()}
def pairs_by_code(db):
    m=collections.defaultdict(set)
    for a,s_,i in q("""select a.code, ifnull(sc.code,'-'), i.code from %s.application_industries x
                       join %s.applications a on a.id=x.application_id
                       left join %s.scopes sc on sc.id=x.scope_id
                       join %s.industries i on i.id=x.industry_id"""%(db,db,db,db)):
        m[a].add((s_,i))
    return m
PB=pairs_by_code(BEFORE); PA=pairs_by_code(AFTER)
moved=[c for c in unchanged if PB.get(c,set())!=PA.get(c,set())]
tc('TC-04-c','126 ứng dụng KHÔNG có cột cập nhật giữ nguyên cặp y hệt trước khi chạy',
   not moved, str(moved[:5]))
tc('TC-04-d','Đúng 19 ứng dụng có cột cập nhật là số ứng dụng bị đổi cặp',
   len([c for c in PA if PB.get(c,set())!=PA.get(c,set())])==19,
   'thực tế đổi: %d' % len([c for c in PA if PB.get(c,set())!=PA.get(c,set())]))

tc('TC-05','internal_business_scopes: không đổi trạng thái bản ghi nào',
   int(one("select count(*) from {B}.internal_business_scopes b join {A}.internal_business_scopes a on a.id=b.id where (a.status<=>b.status)=0".format(B=BEFORE,A=AFTER)))==0)

tc('TC-06','Không sinh mã trùng: internal_business_scopes',
   int(one("select count(*) from (select code from %s.internal_business_scopes group by code having count(*)>1) x"%AFTER))==0)
tc('TC-06-b','Không sinh mã trùng: applications',
   int(one("select count(*) from (select code from %s.applications group by code having count(*)>1) x"%AFTER))==0)
tc('TC-06-c','Không sinh mã trùng trong bộ danh mục đang dùng: scopes',
   int(one("select count(*) from (select code from %s.scopes where internal_business_scope_id is not null group by code having count(*)>1) x"%AFTER))==0)

# ================= Nghiệp vụ liên đới =================
tc('TC-12','Không dự án/báo giá/giải pháp nào đang trỏ vào nhóm ngành vừa bị khoá mà bị mất dữ liệu',
   int(one("""select count(*) from {A}.prospective_projects p join {A}.scopes s on s.id=p.scope_id
              where s.code='NN.0012' and s.internal_business_scope_id is not null and p.scope_id is null""".format(A=AFTER)))==0)
tc('TC-13','Danh mục bị khoá vẫn còn trong DB để bản ghi lịch sử hiển thị được (không bị xoá)',
   int(one("select count(*) from %s.scopes where code='NN.0012' and status=2"%AFTER))==1
   and int(one("select count(*) from %s.industries where code='NGP.0167' and name='Gara 2s-3s' and status=2"%AFTER))==1)

# ================= Audit =================
tc('TC-14','7 lĩnh vực đổi mã đều có updated_by',
   int(one("select count(*) from %s.internal_business_scopes where code like 'LVCTKD.%%' and updated_by is not null"%AFTER))==7)
tc('TC-14-b','13 nhóm ngành tạo mới có cả created_by và updated_by',
   int(one("""select count(*) from %s.scopes where code between 'NN.0023' and 'NN.0035'
              and internal_business_scope_id is not null and created_by is not null and updated_by is not null"""%AFTER))==13)
tc('TC-14-c','Bản ghi bị khoá có updated_by',
   int(one("select count(*) from %s.scopes where code='NN.0012' and internal_business_scope_id is not null and updated_by is not null"%AFTER))==1)


# ================= Bước 6: đồng bộ scope_id bảng nghiệp vụ =================
def lech(db,t):
    return int(one("""select count(*) from {d}.{t} x
        left join {d}.industry_scopes ok on ok.industry_id=x.industry_id and ok.scope_id=x.scope_id
        where x.scope_id is not null and x.industry_id is not null and ok.scope_id is null""".format(d=db,t=t)))
tot_b=sum(lech(BEFORE,t) for t in ['prospective_projects','request_solutions','solutions'])
tot_a=sum(lech(AFTER,t)  for t in ['prospective_projects','request_solutions','solutions'])
tc('TC-21','Seeder KHÔNG làm tăng số dòng nghiệp vụ có scope_id lệch với nhóm giải pháp',
   tot_a<=tot_b, 'trước %d -> sau %d'%(tot_b,tot_a))
tc('TC-21-b','13 dòng lệch SẴN từ trước được giữ nguyên, không bị seeder sửa', tot_a==tot_b,
   'trước %d -> sau %d'%(tot_b,tot_a))
# các dòng được sửa phải khớp đúng ánh xạ cũ->mới trong file
remap={}
for r in sheet['nhom_giai_phap']['rows']:
    new=parse(r['Mã nhóm ngành mới']); cur=parse(r['Mã nhóm ngành'])
    if new and len(new)==len(cur):
        m={o:n for o,n in zip(cur,new) if o!=n}
        if m: remap[r['Mã nhóm giải pháp'].strip()]=m
wrong=[]
for t in ['prospective_projects','request_solutions','solutions']:
    for i,ob,oa,ic in q("""select x.id, b.scope_id, x.scope_id, i.code from {A}.{t} x
            join {B}.{t} b on b.id=x.id
            join {A}.industries i on i.id=x.industry_id
            where (x.scope_id<=>b.scope_id)=0""".format(A=AFTER,B=BEFORE,t=t)):
        oldc = SROWS[int(ob)][0] if int(ob) in SROWS else '?'
        newc = SROWS[int(oa)][0] if int(oa) in SROWS else '?'
        if remap.get(ic,{}).get(oldc) != newc:
            wrong.append('%s#%s %s: %s->%s (file nói %s)'%(t,i,ic,oldc,newc,remap.get(ic,{}).get(oldc)))
tc('TC-22','Mọi dòng nghiệp vụ bị sửa scope_id đều khớp ĐÚNG ánh xạ cũ->mới trong file',
   not wrong, '; '.join(wrong[:5]))
tc('TC-22-b','Số dòng nghiệp vụ bị sửa đúng bằng 245',
   sum(int(one("select count(*) from {A}.{t} x join {B}.{t} b on b.id=x.id where (x.scope_id<=>b.scope_id)=0".format(A=AFTER,B=BEFORE,t=t)))
       for t in ['prospective_projects','request_solutions','solutions'])==245)
tc('TC-23','Seeder không sửa cột nào khác ngoài scope_id ở bảng nghiệp vụ',
   int(one("""select count(*) from {A}.prospective_projects a join {B}.prospective_projects b on b.id=a.id
              where (a.industry_id<=>b.industry_id)=0 or (a.application_id<=>b.application_id)=0
                 or (a.name<=>b.name)=0 or (a.code<=>b.code)=0 or (a.status<=>b.status)=0""".format(A=AFTER,B=BEFORE)))==0)

# ---------- in kết quả ----------
w=max(len(r[1]) for r in results)
npass=sum(1 for r in results if r[2]=='PASS')
for id,name,st,detail in results:
    mark='  PASS' if st=='PASS' else '✗ FAIL'
    print('%s  %-9s %-*s %s' % (mark,id,w,name,detail))
print('\n%d/%d PASS' % (npass,len(results)))
sys.exit(0 if npass==len(results) else 1)
