# Import khách hàng — bỏ bắt buộc Nhóm khách hàng (ERP) — @junfoke

Yêu cầu (chị nhờ qua chat 06/11/2026, khách phản ánh): form thêm khách hàng đã bỏ bắt buộc Nhóm khách hàng nhưng import Excel vẫn bắt.

## Ngày 06/11/2026 (@junfoke)
- [x] 06/11/2026 — Xử lý import khách hàng không còn bắt buộc Nhóm khách hàng (cột C) — `app/ExcelImports/CustomersImport.php`: cột C trống vẫn import, KH không có nhóm (giống thêm tay); có nhập thì vẫn phải đúng tên danh mục, sai báo "Nhóm khách hàng "…" không tồn tại" như cũ; MST đã có dạng NCC vẫn bật cờ khách hàng, có nhóm thì gắn. Chạy thử 3 dòng trên DB local rồi hoàn tác. Commit `18b24cff48` (gop_db, đã push).
