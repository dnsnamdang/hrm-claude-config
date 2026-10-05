# -*- coding: utf-8 -*-
"""Sơ đồ quy trình luồng sale tự làm (Pillow)."""
from PIL import Image, ImageDraw, ImageFont
OUT='/Users/manhcuong/Desktop/dns/HRM/.plans/gop-db/hdsd-feedback-0210/quy-trinh-gp-sale-tu-lam/uml/flow.png'
FD='/System/Library/Fonts/Supplemental/'
R=FD+'Arial Unicode.ttf'; B=FD+'Arial Bold.ttf'
f=lambda p,s: ImageFont.truetype(p,s)
W,H=1800,2330
im=Image.new('RGB',(W,H),'white'); d=ImageDraw.Draw(im)
NAVY=(15,52,96); TEAL=(13,148,136); GREY=(100,116,139); LINE=(71,85,105)
def wrap(text, font, maxw):
    out=[]
    for para in text.split('\n'):
        words=para.split(' '); cur=''
        for w_ in words:
            t=(cur+' '+w_).strip()
            if d.textlength(t,font=font)<=maxw: cur=t
            else: out.append(cur); cur=w_
        out.append(cur)
    return out
def box(x,y,w,h,title,body,fill=(236,253,245),border=TEAL,num=None):
    d.rounded_rectangle([x,y,x+w,y+h],radius=18,fill=fill,outline=border,width=4)
    tx=x+28
    if num:
        d.ellipse([x+18,y+18,x+70,y+70],fill=border); s=str(num)
        ft=f(B,30); d.text((x+44-d.textlength(s,font=ft)/2,y+26),s,font=ft,fill='white'); tx=x+88
    ft=f(B,30); yy=y+24
    for ln in wrap(title,ft,w-(tx-x)-24): d.text((tx,yy),ln,font=ft,fill=NAVY); yy+=38
    fb=f(R,25); yy+=6
    for ln in wrap(body,fb,w-56): d.text((x+28,yy),ln,font=fb,fill=(31,41,55)); yy+=34
def status(x,y,w,lines):
    h=24+len(lines)*36
    d.rounded_rectangle([x,y,x+w,y+h],radius=12,fill=(248,250,252),outline=(203,213,225),width=2)
    yy=y+14
    for lb,val in lines:
        d.text((x+18,yy),lb,font=f(R,23),fill=GREY); d.text((x+18+d.textlength(lb,font=f(R,23))+6,yy),val,font=f(B,23),fill=(30,64,175)); yy+=36
    return h
def arrow(x1,y1,x2,y2,label=None,lx=None,ly=None):
    d.line([x1,y1,x2,y2],fill=LINE,width=5)
    import math
    a=math.atan2(y2-y1,x2-x1); L=22
    p=[(x2,y2),(x2-L*math.cos(a-0.4),y2-L*math.sin(a-0.4)),(x2-L*math.cos(a+0.4),y2-L*math.sin(a+0.4))]
    d.polygon(p,fill=LINE)
    if label: d.text((lx,ly),label,font=f(B,26),fill=(180,83,9))
# tiêu đề
t='QUY TRÌNH QUẢN LÝ GIẢI PHÁP — LUỒNG SALE TỰ LÀM'
d.text(((W-d.textlength(t,font=f(B,44)))/2,36),t,font=f(B,44),fill=NAVY)
t2='(Dự án TKT có Cách triển khai dự án = Tự triển khai; người thực hiện: Nhân viên KD chính của dự án)'
d.text(((W-d.textlength(t2,font=f(R,27)))/2,100),t2,font=f(R,27),fill=GREY)
X=120; BW=900; SX=X+BW+50; SW=W-60-(X+BW+50)
y=170
box(X,y,BW,150,'Tạo dự án TKT, chọn Cách triển khai: Tự triển khai','Bấm Lưu → dự án sang Thu thập thông tin dự án. Nhập đủ phiếu thu thập thông tin (nếu có).',num=1)
status(SX,y+20,SW,[('Dự án:','Thu thập thông tin dự án')])
arrow(X+BW/2,y+150,X+BW/2,y+215)
# quyết định
cy=y+300; cx=X+BW/2
d.polygon([(cx,cy-85),(cx+250,cy),(cx,cy+85),(cx-250,cy)],fill=(255,251,235),outline=(217,119,6),width=4)
q='Có cần làm GP?'; d.text((cx-d.textlength(q,font=f(B,30))/2,cy-18),q,font=f(B,30),fill=(146,64,14))
# nhánh Không
arrow(cx+250,cy,SX-10,cy,'Không',cx+290,cy-42)
box(SX,cy-110,SW,220,'Không làm giải pháp','Dự án chỉ có các thẻ Dự án, Nhiệm vụ, Meetings, Báo giá, Gia hạn, Thu thập thông tin. Tạo báo giá trực tiếp ở thẻ Báo giá.',fill=(254,243,199),border=(217,119,6),num=7)
arrow(cx,cy+85,cx,cy+165,'Có',cx+16,cy+95)
y=cy+170
box(X,y,BW,190,'Tạo giải pháp','Không qua Yêu cầu làm giải pháp; NVKD tạo là PM; không có hạng mục — phân công nhân sự ngay trên giải pháp. Bấm Lưu và gửi (không qua PM/Leader duyệt).',num=2)
status(SX,y+30,SW,[('Giải pháp:','Đang triển khai'),('Dự án:','Đang làm giải pháp')])
arrow(cx,y+190,cx,y+250)
y+=255
box(X,y,BW,120,'Thực hiện giải pháp','Giao nhiệm vụ, xử lý vấn đề, lập BOM tổng hợp (không bắt buộc).',num=3)
arrow(cx,y+120,cx,y+180)
y+=185
box(X,y,BW,195,'Tạo hồ sơ trình duyệt giải pháp → Lưu & Duyệt','Hồ sơ được duyệt ngay, không qua Trưởng phòng. Có BOM tổng hợp Hoàn thành thì tự gắn vào hồ sơ; không có BOM thì bắt buộc đính kèm ít nhất 1 tài liệu.',num=4)
status(SX,y+30,SW,[('Hồ sơ:','Đã duyệt'),('Giải pháp:','Đã duyệt giải pháp'),('Dự án:','Trao đổi giải pháp với khách hàng'),('BOM:','Đã duyệt')])
arrow(cx,y+195,cx,y+255)
y+=260
box(X,y,BW,160,'Tạo báo giá từ hồ sơ đã duyệt','Thẻ Hồ sơ của dự án, nút Tạo báo giá (chỉ khi hồ sơ có BOM). Không qua Yêu cầu xây dựng giá.',num=5)
status(SX,y+30,SW,[('Giải pháp:','Chờ làm giá'),('Dự án:','Lập dự toán')])
arrow(cx,y+160,cx,y+220)
y+=225
box(X,y,BW,155,'Chốt giải pháp','Chọn hồ sơ đã duyệt, đính kèm file khách hàng xác nhận, bấm Lưu & gửi thông báo.',num=6)
status(SX,y+30,SW,[('Hồ sơ:','Đã chốt'),('Giải pháp:','Chốt giải pháp'),('Dự án:','Lập dự toán')])
y+=200
# ghi chú khác luồng thường
d.rounded_rectangle([X,y,W-120,y+300],radius=16,fill=(239,246,255),outline=(37,99,235),width=3)
d.text((X+28,y+20),'Khác luồng thường (Triển khai theo Phòng / Liên phòng ban)',font=f(B,30),fill=(30,64,175))
items=['Không có bước Yêu cầu làm giải pháp, tiếp nhận yêu cầu, PM duyệt, Leader duyệt hạng mục.',
'Giải pháp không có hạng mục; người tạo giải pháp tự động là PM.',
'Hồ sơ trình duyệt tự duyệt khi bấm Lưu & Duyệt; BOM không bắt buộc (thay bằng tài liệu đính kèm).',
'Báo giá tạo thẳng từ BOM của hồ sơ, không qua Yêu cầu xây dựng giá.',
'Chỉ dự án Tự triển khai mới được chọn Không làm giải pháp.']
yy=y+70
for it in items:
    d.text((X+40,yy),'•  '+it,font=f(R,25),fill=(31,41,55)); yy+=44
im=im.crop((0,0,W,y+330)); im.save(OUT); print(im.size)
