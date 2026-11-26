# #11297 Chú thích ký hiệu bảng công / báo cáo cơm + ghi chú dưới ô tích phiếu công tác, PGV — @junfoke

Nhánh `task_11297` (tách từ `origin/gop_db`, cả hrm-api + hrm-client). develop chỉ nhận cherry-pick commit của task.
Redmine: http://quanly.dnsmedia.vn/issues/11297

## Ngày 25/11/2026 (@junfoke)
- [x] 25/11/2026 — Tính năng mới #11297: khối chú thích ký hiệu nền vàng (component mới `V2BaseHighlightNote`, hằng số dùng chung `utils/constants/symbol-legends.js`, partial blade chú thích cho Excel xuất ở BE):
  - Bảng công chi tiết (web + Excel FE, thử 649 NV), Bảng công tổng hợp (web + Excel BE), Báo cáo cơm chi tiết (web + Excel BE). Ký hiệu bảng công (KLD, M, VS, GV, CT) đối chiếu nơi sinh ở BE — khớp.
  - Ghi chú dưới ô tích: phiếu đi công tác (dưới "Đủ công ngày xuất phát"), phiếu giao việc (dưới Checkin/Checkout — màn tạo, sửa, sửa PGV cá nhân). Form phân hệ Dự án & giao việc không sửa (issue chỉ nêu Chấm công).
  - Lên develop: api `d9614e0da`, client `e010bcba2` (nhánh task: api `0b8afaeab`, client `788f78338`).
- [x] 25/11/2026 — Theo user: Excel BC cơm chi tiết dùng đúng ký hiệu như web (`1-CA`, `0-H`, `1-KLH`, thêm `0-CCT` chờ cơm thường; bếp hủy + ô không thực đơn để trống thay vì `0`/`-`; chú thích 14 dòng giống web) — sửa `ReportRiceDetailExport.php` + `report_rice_detail.blade.php`; so 210 ô (7 NV × 30 ngày) khớp web, thử đủ trạng thái 0–6.
- [x] 25/11/2026 — Phản hồi QA: Excel BC cơm chi tiết đưa chú thích lên ĐẦU file (dưới tiêu đề, cách bảng 1 dòng trống); gộp 2 dòng "Để trống" thành 1; `(TC)` → `0(TC)` (cả web). Api `262b29790`, client `41722ae94` (develop). Kiểm file thật 1.145 dòng.

## Ngày 26/11/2026 (@junfoke)
- [x] 26/11/2026 — Phản hồi QA (hiểu lầm lần trước): Excel Bảng công tổng hợp (BE) + Bảng công chi tiết (FE) cũng đưa chú thích lên đầu file. Api `de2370660`, client `124f18989` (develop). Lưu ý báo QA: Excel bảng công chi tiết cố định phần đầu khi cuộn ⇒ giờ 15 dòng đứng yên (gồm chú thích).
- [x] 26/11/2026 — Đưa #11297 lên **prod**: gom 2 commit sửa sau vào `task_11297` (api `ae62784ab`, client `c01463736`) rồi merge `--no-ff` vào `gop_db` (api `2dadd1c19`, client `f2695a6b7`, đã push). Không migration. Xuất thử cả 2 file trên code gop_db sau merge.
  - Suýt nhầm: câu "fix xong thì cho task 10972 lên prod" thực ra là #11297 — bản merge #10972 vào gop_db chuẩn bị sẵn chưa push, đã bỏ.

## Checkpoint — 2026-11-26
Vừa hoàn thành: #11297 lên develop + gop_db (prod).
Bước tiếp theo: QA kiểm prod. Lưu ý server dev/prod phải trỏ `DB_DATABASE_TPE` tới DB có bảng `rice_*`, không thì BC cơm lỗi.
Blocked:
