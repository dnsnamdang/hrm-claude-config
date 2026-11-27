# Redmine 27/11/2026 — vé Mới + Phản hồi giao Trần Cư (13 vé) — plan

Nguồn: dự án fix-bug-dao-tao-danh-gia. Ảnh + mô tả: scratchpad phiên 38983c55 `rm/details.txt`, `rm/img/`.

## Cụm A — BC công nợ KH quá hạn `/sale/customer-debt-overdue`
- [x] #12325 khuôn compare-contract-by-province-report: nút bộ lọc, tuỳ chỉnh cột, '-' → trống, phân trang mặc định 10 bỏ 200, size chữ
- [x] #12327 x clear nhanh dropdown, ô thông tin báo cáo như ERP, màu/layout bảng như mẫu, In giống màn khác + có dữ liệu

## Cụm B — YC đặt hàng `/sale/order-requests`
- [x] #12297 xuất Excel danh sách
- [x] #12298 Tạo mới, icon tuỳ chỉnh cột, Ngày/Người tạo, lịch sử, cột Ngày/Người cập nhật, người dạng mã - tên - phòng
- [x] #12301 khung + placeholder; clear Thương hiệu bị chèn / clear trước khi Đồng ý
- [x] #12304 "Chi tiết", textarea ghi chú cao 1 dòng, bảng chi tiết theo form, nút Lưu nháp trước Lưu và gửi

## Cụm C — Phiếu YC hãng bảo hành `/finance/firm-warranty-requests`
- [x] #12299 bộ lọc đủ như ERP, tuỳ chỉnh cột, sort mã/ngày, In
- [x] #12300 css + Lưu và tiếp tục, placeholder, thiếu trường khi tạo mới, bảng như ERP, file đính kèm chuẩn, Lưu nháp validate 1 trường
- [x] #12303 hàng hoá cần BH dạng table như ERP; dropdown Hợp đồng không ra dữ liệu

## Cụm D — Báo cáo (Phản hồi)
- [x] #12209 BC tổng hợp bán hàng: phân trang chậm sau bấm số thống kê; In giới hạn 2000; xuất Excel lỗi; lọc "Đến nhóm mặt hàng/Đến hàng hoá"
- [x] #12213 BC thu nhập BH: hiệu năng; ô chọn lọc luôn; link đủ số thống kê; lọc "Đến phòng ban/Đến NV"; icon bị cắt; bảng chi tiết theo form
- [x] #12313 các màn báo cáo: ô chọn bấm là lọc luôn, ô nhập cần Enter/Tìm kiếm — đồng bộ + ghi vào skill chung

## Cụm E
- [x] #12316 mã phiếu tự sinh có mã công ty đầu (TPE.YCLDBG.20260084) cho 12 màn, chỉ bản ghi mới

### Checkpoint — 27/11/2026 15:48
Vừa hoàn thành: code 13 vé (5 cụm agent song song, chưa commit). Kiểm local Playwright: A (dữ liệu, trống thay '-', phân trang), B danh sách (Tạo mới/Xuất Excel/cột cập nhật), C tạo mới (bảng 8 cột, Lưu và tiếp tục), D #12213 (chọn Kỳ → tự tìm; popup tổng khớp 573,945,352). #12209 không mở được bằng tài khoản test (thiếu quyền menu) — agent đã đo qua API. Template 415 là mẫu ERP có sẵn. Không có code ERP/HRM parse tiền tố mã (#12316).
Đang làm dở: —
Bước tiếp theo: user duyệt → commit từng vé (tách hunk OrderRequestWriteService.php giữa #12298/#12304 và #12316) → push develop / gop_db → Redmine "Code xong chờ test"
Blocked: chờ user

### Checkpoint — 27/11/2026 16:40
Vừa hoàn thành: cột người #12298 đổi sang `employeeOptionLabel()` (Tên - Mã phòng - Mã NV); commit tách vé + push develop — hrm-api a92d4a153 (#12316), 27cf07590 (B), 62791821c (C), d65aee2e9 (#12209), 4867f5b8c (#12213); hrm-client 1dedf1ef6 (#12316), c3cd55df3 (A), 45fb31572 (B), 8af89114f (C), adc7b70b0 (#12209), 45b8e3b2b (#12313), 91902f838 (#12213). Redmine 13 vé → Code xong chờ test.
Đang làm dở: —
Bước tiếp theo: gop_db KHÔNG cherry-pick — gop_db chưa có các màn này (order-requests, firm-warranty, inland, delivery-cost-asking, customer-debt-overdue, sales-income-summary bản mới…); đợi port cả màn sang gop_db.
Blocked: —
