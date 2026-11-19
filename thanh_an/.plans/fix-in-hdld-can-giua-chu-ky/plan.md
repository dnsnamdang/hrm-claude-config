# Fix: In HĐLĐ — tên công ty xuống dòng, khối chữ ký không căn giữa — @khoipv

URL: `https://demothanhan.dnsmedia.vn/human/employment-contract/145/print`
Ảnh lỗi: tên "CÔNG TY CỔ PHẦN PHÁT TRIỂN DỊCH VỤ THIÊN BÌNH" bị tách 2 dòng; "NGƯỜI LAO ĐỘNG / NGƯỜI SỬ DỤNG LAO ĐỘNG" + dòng "(Kí...)" lệch, không nằm giữa cột.

## Phase 1 — Điều tra (XONG)

- [x] FE `pages/human/employment-contract/_id/print.vue` chỉ `v-html` nguyên HTML BE trả về, không tự dàn trang
- [x] BE `EmploymentContractController::print()` lấy `employment_contracts.print_template` (bản chụp lúc tạo/sửa HĐ), rỗng mới lấy `print_templates.template` → lỗi nằm ở **nội dung mẫu in (dữ liệu)**, không phải code
- [x] Soi mẫu ở DB local (HĐ 87 / mẫu 9 — cùng nội dung điều 5 như ảnh; HĐ 145 chỉ có trên demo, không truy cập được):
  - Đầu trang: bảng 2 cột cố định `width:300px` / `359px`, chữ 20px. Đo bằng Times New Roman Bold: tên cty 558px + quốc hiệu 436px = 994px > khổ in ~872px (Bootstrap in: `.container` min-width 992px − padding 60×2) → buộc xuống dòng
  - Khối chữ ký: 1 đoạn `text-align:left` + hàng chục dấu cách để đẩy chữ sang phải → khi in co giãn khác màn hình nên lệch
- [x] Đo cỡ chữ vừa 1 dòng: 16px → 446 + 349 = 795px (+ padding) < 872px

## Phase 2 — Fix (dữ liệu mẫu in)

- [x] Soạn đoạn HTML thay thế: [doan-html-thay-the.html](doan-html-thay-the.html) — đầu trang bỏ width cố định, chữ 16px; chữ ký dùng bảng 2 cột 50/50 căn giữa
- [ ] User dán vào mẫu in tại `/human/report_templates` (nút Nguồn của CKEditor) → HĐ tạo mới sẽ đúng
- [x] User gửi HTML hiện tại của HĐ 145 → ghép sẵn bản đầy đủ: [hd-145-mau-in-da-sua.html](hd-145-mau-in-da-sua.html) (chỉ đổi bảng đầu trang + khối chữ ký; thân HĐ giữ nguyên; đã kiểm đủ 18 loại biến `{{...}}` (TEN_CONG_TY ×3), thẻ mở/đóng khớp)
- [x] User test bản 1: đầu trang dồn hết 1 dòng (tên cty + quốc hiệu sát nhau) → không đạt. User chốt ngắt: "CÔNG TY CỔ PHẦN PHÁT TRIỂN" / "DỊCH VỤ THIÊN BÌNH"
- [x] Sửa đầu trang (cả 2 file): chữ về 20px như cũ; tên cty bọc `inline-block max-width:345px` (đo Times Bold 20px: "...PHÁT TRIỂN" ≈ 318px, thêm "DỊCH" ≈ 376px) → ngắt đúng chỗ; quốc hiệu `nowrap`; 2 cột cách nhau 24px
- [ ] User sửa HĐ 145 → tab "Mẫu in" → dán tương tự (HĐ đã tạo dùng bản chụp riêng, sửa mẫu gốc không tự cập nhật) → Lưu → in lại kiểm tra

## Checkpoint — 2026-11-16

Vừa hoàn thành: xác định nguyên nhân + soạn đoạn HTML thay thế
Đang làm dở: —
Bước tiếp theo: user dán HTML vào mẫu in + HĐ 145 trên demo, in thử
Blocked: không truy cập được DB demo để sửa trực tiếp
