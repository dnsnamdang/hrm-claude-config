# Plan — Bổ sung số 0 đầu mã số thuế khách hàng

**Phụ trách:** @khoipv
**Ngày:** 2026-09-22

## Phase 1 — Phân tích dữ liệu
- [x] Đọc file `danh_sach_khach_hang (3) (1).xls` (1129 bản ghi = toàn bộ bảng `category_customers`)
- [x] Thống kê độ dài `tax_code`: 0 ký tự = 32, 9 số = **323**, 10 số = 704, 11 số = 1, 12 số = 1, 14 ký tự (10 số + "-" + 3 số) = 68
- [x] Đối chiếu DB `thanhan_stag_22092026` → xác nhận 323 bản ghi thật sự thiếu số 0 ở đầu (không phải lỗi export Excel)

## Phase 2 — BE
- [x] Viết `database/seeders/UpdateTaxCodeMissingLeadingZeroSeeder.php`
  - **Chốt: điều kiện `tax_code REGEXP '^[0-9]{9}$'`** (MST VN luôn 10 số, 9 số = rớt số 0), quét toàn bảng
  - Đã thử phương án nhúng cứng 323 mã KH từ file Excel nhưng **bỏ**, quay về bản regex cho gọn (@khoipv chốt 22/09/2026)
  - ⚠️ Hệ quả: trên production, KH **ngoài** file mà MST 9 số cũng sẽ được sửa — đã biết và chấp nhận
  - Backup CSV ra `storage/app/backup_tax_code_<timestamp>.csv` trước khi sửa
  - `toBase()` để không đụng `updated_at`
  - Chạy lại nhiều lần vẫn an toàn (idempotent)
- [x] Chạy seeder trên DB `thanhan_stag_22092026` → **323/323** bản ghi, backup tại `storage/app/backup_tax_code_20260922_230201.csv`
- [x] Kiểm tra lại số liệu sau khi chạy: 9 số = 0, 10 số = 1027 (704 + 323)
- [x] Test rollback + chạy lại: khôi phục 323 bản ghi từ backup CSV → chạy lại → đúng 323/323
- [x] Test idempotent: chạy lần 2 → "Không có bản ghi nào cần cập nhật", 323 dòng bỏ qua

### Checkpoint — 2026-09-22
Vừa hoàn thành: viết + chạy seeder `UpdateTaxCodeMissingLeadingZeroSeeder` trên staging (323 bản ghi)
Đang làm dở: không
Bước tiếp theo: chạy seeder trên DB production khi deploy
Blocked:
