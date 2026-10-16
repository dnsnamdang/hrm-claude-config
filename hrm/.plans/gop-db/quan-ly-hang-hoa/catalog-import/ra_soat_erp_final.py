import openpyxl,sys,collections,re
from openpyxl.styles import Font,PatternFill,Alignment
src,gtsv,out=sys.argv[1:4]
wb=openpyxl.load_workbook(src,read_only=True,data_only=True)
norm=lambda s: re.sub(r'\s+',' ',str(s).strip()).casefold() if s is not None and str(s).strip()!='' else None
clean=lambda s: re.sub(r'\s+',' ',str(s).strip()) if s is not None else ''
G={}
for l in open(gtsv,encoding='utf-8'):
    i,st,nm,used,tot=l.rstrip('\n').split('\t'); G[int(i)]=(int(st),nm,int(used),int(tot))
# ---------- Sheet NewERP
ng=list(wb['NewERP Green Power'].iter_rows(values_only=True))
LV=['Tính chất','Nhóm chức năng','Nhóm sản phẩm','Loại sản phẩm']
rows=[]
for ex,r in enumerate(ng[1:],start=2):
    if not any(r[1:8]): continue
    rows.append((ex,r))
viol=[];summary=[];missing=[]
for k in (2,3,4):  # con ở cột k, cha cột k-1
    par=collections.defaultdict(collections.Counter); disp={}
    for ex,r in rows:
        c,p=norm(r[k]),norm(r[k-1])
        if c and p: par[c][p]+=1; disp.setdefault(c,clean(r[k])); disp.setdefault(p,clean(r[k-1]))
    bad={c for c,v in par.items() if len(v)>1}
    for c in sorted(bad,key=lambda x:disp[x]):
        summary.append((LV[k-1],disp[c],len(par[c]),'\n'.join(f'{disp[p]} ({n} dòng)' for p,n in par[c].most_common())))
    for ex,r in rows:
        c=norm(r[k])
        if c in bad:
            p=norm(r[k-1]); mc=par[c].most_common(); top=mc[0][0] if mc[0][1]>mc[1][1] else None
            if top==p: continue
            others=[disp[x] for x in par[c] if x!=p]
            viol.append((r[0],ex,LV[k-1],clean(r[k]),LV[k-2],clean(r[k-1]),par[c][p],disp[top] if top else '(ngang nhau — cần chọn)','; '.join(others),clean(r[1]),clean(r[2]),clean(r[3]),clean(r[4]),clean(r[5]),clean(r[7])))
for ex,r in rows:
    miss=[LV[i-1] for i in (1,2,3,4) if not norm(r[i])]
    if miss: missing.append((r[0],ex,', '.join(miss),clean(r[1]),clean(r[2]),clean(r[3]),clean(r[4]),clean(r[5]),clean(r[7])))
# ---------- Sheet Hang_hoa_ma_nhom_cu
hm=list(wb['Hang_hoa_ma_nhom_cu'].iter_rows(values_only=True))
g2l=collections.defaultdict(collections.Counter); l2g=collections.defaultdict(collections.Counter); ld={}
blank=[];nonint=[]
for ex,r in enumerate(hm[1:],start=2):
    if r[1] is None and r[2] is None: continue
    l=norm(r[1]); g=r[2]
    try: g=int(float(g)) if g not in (None,'') else None
    except: nonint.append((r[0],ex,clean(r[1]),clean(r[2]))); continue
    if not l or g is None: blank.append((r[0],ex,clean(r[1]),'' if g is None else g)); continue
    ld.setdefault(l,clean(r[1])); g2l[g][l]+=1; l2g[l][g]+=1
gname=lambda g: G[g][1] if g in G else '(không có trong DB)'
s2=[(g,gname(g),G[g][2] if g in G else '',len(v),'\n'.join(f'{ld[l]} ({n} dòng)' for l,n in v.most_common())) for g,v in sorted(g2l.items()) if len(v)>1]
s3=[(ld[l],len(v),'\n'.join(f'{g} - {gname(g)} ({n} dòng)' for g,n in v.most_common())) for l,v in sorted(l2g.items(),key=lambda x:ld[x[0]]) if len(v)>1]
s4=[(g,G[g][1],'Hoạt động' if G[g][0]==1 else 'Khoá/khác ('+str(G[g][0])+')',G[g][2],G[g][3]) for g in sorted(G) if g not in g2l]
s5=[]
for g,v in sorted(g2l.items()):
    if g not in G:
        for l,n in v.most_common(): s5.append((g,ld[l],n))
# ---------- Write
o=openpyxl.Workbook(); o.remove(o.active)
H=Font(bold=True,color='FFFFFF'); F=PatternFill('solid',fgColor='1ABC9C')
def sheet(name,note,head,data,widths):
    ws=o.create_sheet(name); ws.append([note]); ws['A1'].font=Font(italic=True)
    ws.append(list(head))
    for c in ws[2]: c.font=H; c.fill=F; c.alignment=Alignment(wrap_text=True,vertical='center')
    for d in data: ws.append(list(d))
    for i,w in enumerate(widths): ws.column_dimensions[openpyxl.utils.get_column_letter(i+1)].width=w
    for row in ws.iter_rows(min_row=3):
        for c in row: c.alignment=Alignment(wrap_text=True,vertical='top')
    ws.freeze_panes='A3'; ws.auto_filter.ref=f'A2:{openpyxl.utils.get_column_letter(len(head))}{ws.max_row}'
sheet('1a. Cấp con nhiều cha - tóm tắt',f'Sheet NewERP Green Power — nguyên tắc 1 cấp con chỉ thuộc 1 cấp cha. {len(summary)} tên vi phạm (so tên đã bỏ khoảng trắng thừa, không phân biệt hoa thường).',
      ['Cấp con','Tên','Số cha','Các cha (số dòng hàng)'],summary,[16,45,8,70])
sheet('1b. Cấp con nhiều cha - dòng',f'{len(viol)} dòng hàng KHÔNG nằm dưới cha chiếm đa số của tên đó (tên mà các cha ngang số dòng thì liệt kê mọi dòng). Cột "Dòng Excel" = số dòng trong sheet NewERP Green Power. Lọc theo cột Tên để xem từng tên.',
      ['STT (Cột1)','Dòng Excel','Cấp vi phạm','Tên','Cấp cha','Cha ở dòng này','Số dòng cùng cha này','Cha đa số','Cha khác','Tính chất','Nhóm CN','Nhóm SP','Loại SP','Tên hàng','Mã hàng'],viol,[8,8,14,35,14,35,10,30,40,22,25,30,35,50,22])
sheet('1c. Dòng thiếu cấp',f'{len(missing)} dòng hàng để trống ít nhất 1 trong 4 cấp (không xét được nguyên tắc 1 cha ở cấp trống).',
      ['STT (Cột1)','Dòng Excel','Cấp để trống','Tính chất','Nhóm CN','Nhóm SP','Loại SP','Tên hàng','Mã hàng'],missing,[8,8,25,22,25,30,35,50,22])
sheet('2. Nhóm cũ → nhiều Loại',f'Sheet Hang_hoa_ma_nhom_cu — {len(s2)} nhóm hàng cũ (groups.id) ứng với >1 Loại SP.',
      ['ID nhóm cũ','Tên nhóm trên DB','Hàng đang dùng trên DB','Số Loại','Các Loại (số dòng)'],s2,[10,40,12,8,70])
sheet('3. Loại → nhiều Nhóm cũ',f'Sheet Hang_hoa_ma_nhom_cu — {len(s3)} Loại SP ứng với >1 nhóm hàng cũ.',
      ['Loại SP','Số nhóm','Các nhóm cũ (số dòng)'],s3,[45,8,80])
sheet('4. Nhóm DB chưa có Loại',f'{len(s4)} nhóm trong bảng groups (DB hrm_erp_giacty, {len(G)} nhóm) không xuất hiện ở sheet Hang_hoa_ma_nhom_cu. "Hàng đang dùng" = products.status<>0.',
      ['ID nhóm','Tên nhóm','Trạng thái nhóm','Hàng đang dùng','Tổng hàng (kể cả đã xoá)'],s4,[10,50,16,12,14])
sheet('5. Loại gắn nhóm không có DB',f'{len(s5)} cặp ở sheet Hang_hoa_ma_nhom_cu trỏ tới ID nhóm không có trong bảng groups của DB.',
      ['ID nhóm (file)','Loại SP','Số dòng'],s5,[14,50,10])
if blank or nonint:
    sheet('6. Dòng chưa có ID nhóm cũ',f'{len(blank)+len(nonint)} dòng ở Hang_hoa_ma_nhom_cu có Loại nhưng để trống ID nhóm cũ (dòng 7990–9401). Đối chiếu Mã hàng: chỉ 6/1.227 mã có trên DB ⇒ phần lớn là hàng mới, chưa có nhóm cũ. Không tính vào các sheet 2–5.',
          ['STT (Cột1)','Dòng Excel','Loại SP','ID nhóm'],blank+nonint,[8,8,50,14])
o.save(out)
print('1a',len(summary),'1b',len(viol),'1c',len(missing),'2',len(s2),'3',len(s3),'4',len(s4),'used4',sum(1 for x in s4 if x[3]>0),'5',len(s5),'6',len(blank)+len(nonint))
from collections import Counter; print(Counter(x[0] for x in summary))
print('nhóm có trong file',len(g2l),'loại',len(l2g))
