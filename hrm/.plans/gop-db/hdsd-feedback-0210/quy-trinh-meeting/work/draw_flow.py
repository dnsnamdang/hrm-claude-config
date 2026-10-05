from PIL import Image, ImageDraw, ImageFont
F='/System/Library/Fonts/Supplemental/Arial.ttf'; FB='/System/Library/Fonts/Supplemental/Arial Bold.ttf'
W,H=2000,1060
im=Image.new('RGB',(W,H),'white'); d=ImageDraw.Draw(im)
fb=ImageFont.truetype(FB,30); f=ImageFont.truetype(F,24); fs=ImageFont.truetype(F,22); ft=ImageFont.truetype(FB,36)
def box(x,y,w,h,title,sub,col,fill):
    d.rounded_rectangle((x,y,x+w,y+h),radius=18,outline=col,width=4,fill=fill)
    tw=d.textlength(title,font=fb); d.text((x+(w-tw)/2,y+18),title,font=fb,fill=col)
    yy=y+62
    for s in sub:
        sw=d.textlength(s,font=fs); d.text((x+(w-sw)/2,yy),s,font=fs,fill='#374151'); yy+=30
    return (x,y,w,h)
def arrow(p1,p2,col='#374151',label=None,lo=(0,-34)):
    d.line([p1,p2],fill=col,width=4)
    import math
    a=math.atan2(p2[1]-p1[1],p2[0]-p1[0]); L=18
    d.polygon([p2,(p2[0]-L*math.cos(a-0.4),p2[1]-L*math.sin(a-0.4)),(p2[0]-L*math.cos(a+0.4),p2[1]-L*math.sin(a+0.4))],fill=col)
    if label:
        for i,t in enumerate(label.split('\n')):
            tw=d.textlength(t,font=f); mx=(p1[0]+p2[0])/2; my=(p1[1]+p2[1])/2
            d.text((mx-tw/2+lo[0],my+lo[1]+i*28),t,font=f,fill=col)
t='Sơ đồ vòng đời một cuộc họp (meeting)'; d.text(((W-d.textlength(t,font=ft))/2,25),t,font=ft,fill='#111827')
Y=330; BW,BH=300,190
start=(40,Y+55,170,80)
d.rounded_rectangle((40,Y+55,210,Y+135),radius=40,fill='#16A34A'); tw=d.textlength('Tạo mới',font=fb); d.text((125-tw/2,Y+77),'Tạo mới',font=fb,fill='white')
b0=box(260,Y,BW,BH,'Lưu nháp',['Chỉ người tạo thấy để','soạn tiếp, chưa gửi lịch'],'#64748B','#F8FAFC')
b1=box(760,Y,BW,BH,'Lên lịch',['Đã gửi lịch họp tới','thành phần tham gia;','thành viên xác nhận tham dự'],'#0EA5E9','#F0F9FF')
b2=box(1260,Y,BW,BH,'Chốt lịch',['Chốt thời gian, địa điểm;','điểm danh, lập biên bản,','kết luận'],'#2563EB','#EFF6FF')
b3=box(1650,Y-270,BW,BH,'Hoàn thành',['Đã họp và có biên bản;','khóa chỉnh sửa,','vẫn In biên bản được'],'#16A34A','#F0FDF4')
b4=box(1010,Y+420,BW,BH,'Hủy',['Bắt buộc chọn lý do hủy;','khóa chỉnh sửa'],'#6B7280','#F9FAFB')
bx=box(260,Y+420,BW,BH,'Xóa',['Xóa hẳn cuộc họp','(chỉ khi đang Lưu nháp)'],'#DC2626','#FEF2F2')
arrow((210,Y+95),(260,Y+95))
arrow((560,Y+95),(760,Y+95),label='Lưu và Lên lịch',lo=(0,-40))
arrow((1060,Y+95),(1260,Y+95),label='Lưu và Chốt lịch',lo=(0,-40))
arrow((1560,Y+40),(1720,Y-80),'#16A34A')
    
arrow((410,Y+190),(410,Y+420),'#DC2626',label='Xóa',lo=(40,-14))
# lưu nháp -> chốt lịch thẳng (cong lên)
d.line([(410,Y),(410,Y-110),(1380,Y-110)],fill='#2563EB',width=3); arrow((1380,Y-110),(1380,Y),'#2563EB')
tw=d.textlength('Lưu và Chốt lịch ngay từ Lưu nháp / Tạo mới',font=f); d.text((895-tw/2,Y-150),'Lưu và Chốt lịch ngay từ Lưu nháp / Tạo mới',font=f,fill='#2563EB')
arrow((910,Y+190),(1100,Y+420),'#6B7280')
arrow((1410,Y+190),(1250,Y+420),'#6B7280')
lab=['Hủy (người tạo, trước giờ bắt đầu)','hoặc hệ thống TỰ HỦY khi quá hạn','nhập biên bản (sau giờ kết thúc + N ngày)']
for i,s in enumerate(lab): d.text((1370,Y+430+i*30),s,font=f,fill='#6B7280')
n=['Ghi chú: Sửa được ở Lưu nháp, Lên lịch, Chốt lịch (người tạo hoặc người chủ trì). Hủy và Xóa chỉ người tạo.',
   'Bấm Lưu và Lên lịch ở trạng thái Lên lịch: gửi lại thông báo lịch họp cho thành phần tham gia.']
for i,s in enumerate(n): d.text((60,H-90+i*34),s,font=f,fill='#374151')
for i,t in enumerate(['Hoàn thành','(đã tới giờ họp; đủ điểm','danh, biên bản, kết luận)']): d.text((1690,Y-50+i*30),t,font=f,fill='#16A34A')
im.save('uml/overview.png'); print(im.size)
