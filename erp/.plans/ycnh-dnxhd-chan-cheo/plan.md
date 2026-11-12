# #11460 — Chặn chéo YCNH trả lại ↔ Đề nghị xuất hóa đơn

Luật (user chốt): cùng HĐ (gồm PLBS) + cùng mã hàng.
- ĐNXHĐ đang xử lý = status 1/2/5 (đang tạo / chờ duyệt / không duyệt), dòng need_export=1.
- YCNH trả lại đang xử lý = type 4/9, is_complete=0, status ∉ {5,6}, dòng qty>0.

## Tasks
- [x] T1 Service `app/Services/Warehouse/ReturnExportBillGuard.php` (resolve HĐ gốc, 2 hàm dựng câu báo lỗi)
- [x] T2 TH1: chặn YCNH type 4/9 khi lưu (store + update) — `Warehouse/ProductImportRequestsController` + `CRM/Warehouse/ProductImportRequestsController`
- [x] T3 TH2: chặn PNK type 4/9 — `Warehouse/ProductImportsController@store`
- [x] T4 TH3: chặn ĐNXHĐ store/update — `IncomeExpenditure/ExportBillRequestController`
- [x] T5 php -l + test dữ liệu local
- [x] T6 Commit, push develop_02 + gop_db, Redmine → Code xong chờ test

### Checkpoint — 2026-11-11
Vừa hoàn thành: T1–T6. develop_02 36ea953050. KHÔNG đẩy gop_db: gop_db chưa có màn ĐNXHĐ (không có ExportBillRequest) → câu query TH1/TH2 sẽ lỗi bảng.
Test local (transaction rollback): 4 phiếu YCNH type 4/9 (firm + wr) → TH3 chặn đúng mã, hàng khác không chặn; ĐNXHĐ giả status 2 → TH1 chặn, status 3 → không chặn.
Bước tiếp theo: chờ tester.
Blocked:
