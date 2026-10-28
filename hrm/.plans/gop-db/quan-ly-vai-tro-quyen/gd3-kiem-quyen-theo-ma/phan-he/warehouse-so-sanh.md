# So sánh mốc TRƯỚC / SAU phân hệ warehouse (7c, 28/10/2026)

| Chỉ tiêu | Giá trị |
|---|---|
| Tổng số ô (72 route x 5 tài khoản) | 360 |
| Ô giống hệt (status, so_dong, ids_hash, cờ `co`) | 360 |
| Ô khác | 0 |

Kiểm bằng `ScopeSnapshot.php diff` ("Khác nhau: 0 ô") và so lại độc lập bằng script Python trên bốn trường status / so_dong / ids_hash / co: cùng kết quả, không có ô thiếu hay thừa.

Bảng ô khác: (không có).
