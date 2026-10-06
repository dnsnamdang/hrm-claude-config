import subprocess, json
def q(sql):
    return subprocess.run(['mysql','-uroot','local_hrm_erp','-N','-e',sql],capture_output=True,text=True,check=True).stdout
cols=[c.split('\t')[0] for c in q("show columns from prospective_projects").strip().split('\n')]
override={
 'code':None,'name':None,'status':'2','created_by':'13','updated_by':'13','created_at':'NOW()','updated_at':'NOW()',
 'form_template_snapshot_id':'NULL','form_template_id':'NULL','implementation_type':'3','is_parent_project':'0','parent_id':'NULL',
 'customer_need_solution_date':"'2026-11-25'",'internal_solution_close_date':"'2026-11-18'",
}
for code,name in [('HN_KD3.UD.0100.2026.DA094','Cung cấp thiết bị chẩn đoán và cân chỉnh góc lái cho xưởng dịch vụ Toyota Hải Dương'),
                  ('HN_KD3.UD.0100.2026.DA095','Cung cấp cầu nâng và thiết bị bảo dưỡng nhanh cho xưởng dịch vụ Mazda Thái Bình')]:
    sel=[]
    for c in cols:
        if c=='id': continue
        if c=='code': sel.append("'%s'"%code)
        elif c=='name': sel.append("'%s'"%name)
        elif c in override: sel.append(override[c])
        else: sel.append('`%s`'%c)
    clist=','.join('`%s`'%c for c in cols if c!='id')
    q("insert into prospective_projects (%s) select %s from prospective_projects where id=152"%(clist,','.join(sel)))
print(q("select id,code,name,status,created_by from prospective_projects where code in ('HN_KD3.UD.0100.2026.DA094','HN_KD3.UD.0100.2026.DA095')"))
