# Tách nhóm hàng DB chưa có trong file 17/10 (chưa mapping Loại): khoá / không có hàng / chỉ hàng đã xoá / còn hàng đang dùng
# python3 -I tach_nhom_chua_co_loai.py <file17> <groups_full.tsv> <out.xlsx>
import openpyxl,sys
from openpyxl.styles import Font,PatternFill,Alignment
f17,gt,out=sys.argv[1:4]
rs=list(openpyxl.load_workbook(f17,read_only=True,data_only=True)['NewERP Green Power'].iter_rows(values_only=True))[1:]
mapped={int(float(r[8])) for r in rs if r[8] not in (None,'') and r[4]}
G=[]
for l in open(gt,encoding='utf-8'):
    i,n,st,tot,use,tpl,att,mac=l.rstrip('\n').split('\t')
    G.append((int(i),n,int(st),int(tot),int(use),int(tpl),int(att),int(mac)))
un=[g for g in G if g[0] not in mapped]
cat={'1. Đang khoá':[g for g in un if g[2]==0],
     '2. Hoạt động - không có hàng':[g for g in un if g[2]!=0 and g[3]==0],
     '3. Hoạt động - chỉ hàng đã xoá':[g for g in un if g[2]!=0 and g[3]>0 and g[4]==0],
     '4. Hoạt động - còn hàng dùng':[g for g in un if g[2]!=0 and g[4]>0]}
o=openpyxl.Workbook(); ws=o.active; ws.title='Tổng hợp'
H=Font(bold=True,color='FFFFFF'); F=PatternFill('solid',fgColor='1ABC9C')
ws.append([f'{len(un)} / {len(G)} nhóm hàng (bảng groups, DB hrm_erp_giacty 19/10) KHÔNG có trong cột "ID nhóm hàng cũ" của sheet NewERP Green Power (file 17/10). "Hàng đã xoá" = products.status = 0.'])
ws.append(['Phân loại','Số nhóm','Tổng hàng','Hàng đang dùng','Mẫu hàng','Liên kết thuộc tính','Liên kết nhóm máy'])
for c in ws[2]: c.font=H; c.fill=F
for k,v in cat.items(): ws.append([k,len(v),sum(g[3] for g in v),sum(g[4] for g in v),sum(g[5] for g in v),sum(g[6] for g in v),sum(g[7] for g in v)])
for i,w in enumerate([36,10,12,14,12,18,18]): ws.column_dimensions[openpyxl.utils.get_column_letter(i+1)].width=w
head=['ID nhóm','Tên nhóm','Trạng thái','Tổng hàng (kể cả đã xoá)','Hàng đang dùng','Mẫu hàng','Số thuộc tính gán','Liên kết nhóm máy']
for k,v in cat.items():
    s=o.create_sheet(k[:31]); s.append(head)
    for c in s[1]: c.font=H; c.fill=F; c.alignment=Alignment(wrap_text=True)
    for g in sorted(v,key=lambda x:(-x[4],-x[3],x[1])): s.append([g[0],g[1],'Hoạt động' if g[2]==1 else 'Khoá',*g[3:]])
    for i,w in enumerate([9,50,11,14,12,10,12,12]): s.column_dimensions[openpyxl.utils.get_column_letter(i+1)].width=w
    s.freeze_panes='A2'; s.auto_filter.ref=f'A1:H{max(s.max_row,1)}'
o.save(out)
for r in ws.iter_rows(min_row=2,values_only=True): print(r)
print('khoá:',[(g[0],g[1],g[3],g[4]) for g in cat['1. Đang khoá']])
print('mapped nhưng khoá:',[(g[0],g[1]) for g in G if g[2]==0 and g[0] in mapped])
