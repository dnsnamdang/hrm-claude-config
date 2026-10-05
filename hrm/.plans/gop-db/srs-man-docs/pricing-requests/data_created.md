# Dữ liệu tạo cho SRS "Yêu cầu tính giá bán" (05/10/2026, DB local_hrm_erp)

Không sửa / xoá dữ liệu có sẵn (ngoại trừ đổi mật khẩu tạm của 1 nhân viên — đã trả lại, xem cuối file).

## pricing_requests (bảng trống trước đó) — chèn bằng SQL, id 1–7
Tất cả gắn BOM tổng hợp đã duyệt `BOM-2026-00002` (id 2) · dự án id 5 (HN_KD2.UD.0100.2026.DA004, kiểu "Liên phòng ban") · giải pháp id 4 · version id 4.
`department_id` để NULL (luồng thật do BaseModel gán = phòng người lập).

| id | Mã | Trạng thái | created_by |
|---|---|---|---|
| 1 | YCBG-2026-00001 | 6 Dừng | 78 (Vũ Tuấn Việt) |
| 2 | YCBG-2026-00002 | 4 Đã có báo giá (gắn báo giá 91) | 78 |
| 3 | YCBG-2026-00003 | 3 Đang xây dựng giá | 78 (updated_by 13) |
| 4 | YCBG-2026-00004 | 2 Chờ xây dựng giá | 78 |
| 5 | YCBG-2026-00005 | 5 Đóng | 78 |
| 6 | YCBG-2026-00006 | 1 Đang tạo | 27 (Chu Khương Duy) |
| 7 | YCBG-2026-00007 | 2 Chờ xây dựng giá | 27 |

## quotations
- id 91 `BG-2026-00091` — tạo qua API thật `POST /assign/quotations` {pricing_request_id: 2, price_type_id: 1} bằng tài khoản admin
  (kèm 1 dòng quotation_product_prices + 1 dòng quotation_histories do service tự sinh). Sau đó SQL đặt status=4,
  approved_at=2026-09-24 15:10, approved_by=13 để khớp yêu cầu "Đã có báo giá".
- Dự án 5 đang ở trạng thái 6 (Dự toán) nên service không đổi trạng thái dự án.

## Mật khẩu tạm
- employees id 27 (duyck.kd1@tanphat.com, không có quyền xây dựng giá) đổi tạm sang `Test@12345` để chụp góc nhìn
  người lập yêu cầu (nút Sửa/Xóa), chụp xong ĐÃ TRẢ LẠI hash gốc
  `$2y$10$JVDIPiDo03CTaMKOFy5nt.j2ZgKM0TAZdeuBT/uOptV45ibJ62uYe`.

## Chỉ đọc (không ghi)
- Dự án 150 (tab Hồ sơ) — chỉ mở popup "Yêu cầu xây dựng giá" và bấm "Lưu và gửi" khi để trống để chụp lỗi validate
  (bị chặn ở FE, không gọi API ghi).

## Dọn dẹp (nếu cần)
```sql
DELETE FROM quotation_product_prices WHERE quotation_id = 91;
DELETE FROM quotation_histories WHERE quotation_id = 91;
DELETE FROM quotations WHERE id = 91;
DELETE FROM pricing_requests WHERE id BETWEEN 1 AND 7;
```
