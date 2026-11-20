# Chấm công qua WiFi công ty — tóm tắt

> @namdangit · Trạng thái: **ĐANG BRAINSTORM (19/11/2026)**, chưa code, chưa chọn nhánh
> Spec chi tiết: `docs/superpowers/specs/2026-11-19-cham-cong-wifi-design.md`

## Mục tiêu
Nhân viên hay **quên chấm công** ⇒ điện thoại tới văn phòng, bắt WiFi công ty thì **tự ghi giờ vào**, không mở app.

## Cách làm đã chọn
Hệ điều hành đánh thức app khi vào vùng văn phòng (geofence) → app kiểm đang bắt WiFi công ty (theo BSSID) →
tự gửi lượt chấm qua API chấm công hiện có (vẫn qua cổng thiết bị đã đăng ký, ca, bán kính).
Loại: router báo về server (phụ thuộc phần cứng, MAC ngẫu nhiên); chỉ nhắc (không tự động — giữ cho giờ ra).

## Đã chốt
- Chỉ tự chấm **giờ vào**; giờ ra chấm tay + app **nhắc** khi quá giờ tan ca chưa chấm.
- Bật **theo nơi chấm** (văn phòng có khai WiFi).

## Đề xuất chờ xác nhận
Chỉ ca làm việc · 1 lần/ca · trong khung quanh giờ vào ca · không ảnh, đánh dấu "Tự động (WiFi)" · nhận WiFi theo BSSID, thêm bằng nút "Thêm WiFi đang kết nối" trên app.

## Đang chờ user
Cấu hình ở đâu: (1) danh mục mới "Văn phòng chấm công WiFi" — Claude khuyên · (2) khai WiFi trong nơi chấm từng ca.
Còn 7 câu hỏi khác — spec §7.

## Liên quan
Màn app `ui/check_in_out` do @cuong61n thiết kế lại (`.plans/app-cham-cong/`) — phối hợp trước khi sửa.
Nơi chấm của ca hiện là JSON chép trong `working_shifts.place`, không có danh mục văn phòng.
