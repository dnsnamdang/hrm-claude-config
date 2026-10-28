# Phiếu YC hạch toán bổ sung — tỷ giá 3 số lẻ + tổng cột Số tiền

@junfoke · Repo `TanPhatDev`, nhánh `gop_db` · Màn `/admin/income-expenditure/addition_accounting_requests/create`

## Yêu cầu (12/10/2026)
- Ô Tỷ giá cho nhập số thập phân, tối đa 3 chữ số sau dấu chấm.
- Bảng chi tiết (loại 2 - ĐC công nợ KH, loại 6 - ĐC công nợ NCC) có dòng tổng cột Số tiền.

## Lỗi sẵn có phát hiện kèm
FE gửi tỷ giá dạng chuỗi đã format (`"26,123"`), BE không validate → MySQL cắt còn `26`.
DB gop_db đang có tỷ giá 26 / 31 / 286 / 316... là dữ liệu đã hỏng do lỗi này.

## Task
- [x] JS `partials/AdditionAccountingRequest.blade.php`: getter/setter tỷ giá 3 số lẻ (chặn số thứ 4, giữ phần lẻ đang gõ dở), gửi số thuần `_exchange_rate`; thêm `total_detail_money`
- [x] `form.blade.php`: dòng "Tổng cộng" ở 2 bảng chi tiết (loại 2 và 6)
- [x] `AdditionAccountingStoreRequest`: rule `exchange_rate` nullable|numeric|min:0|regex 3 số lẻ
- [x] Migration `2026_10_12_000000_change_exchange_rate_decimal_addition_accounting_requests` (double(16,2) → decimal(16,3)) — **CHƯA CHẠY, chờ user**
- [x] Verify Playwright local :8001 — gõ `26123.4567` → `26,123.456`, submit 26123.456; tổng 1,500,000.5 + 2,300,000 = 3,800,000.5, cập nhật khi thêm/xoá dòng
- [ ] Chạy migration (local + server)
- [x] Commit — `3aebbbe04f` (user commit 12/10)

### Checkpoint — 2026-10-12
Vừa hoàn thành: code + verify browser
Đang làm dở: —
Bước tiếp theo: user duyệt chạy migration + commit
Blocked: chờ user xác nhận đổi DB
