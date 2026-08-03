# Design — Reset prepick_details qty=0 (company_id = 4)

Người phụ trách: @namdangit

## Mục tiêu
Đưa toàn bộ bản ghi `prepick_details` có `company_id = 4` và `qty > 0` về `qty = 0`,
đồng thời ghi log tương ứng vào `prepick_logs` để giữ vết thay đổi.

## Scope
- 1 method data-fix trong `TanPhatDev/database/seeds/UpdateDB.php`, chạy qua tinker
  (theo Data Fix Pattern của dự án). Không đụng controller/route/FE.

## Hiện trạng dữ liệu (DB local `erp2326`, tại thời điểm khảo sát)
- `prepick_details` company_id=4: tổng 13.435 bản ghi
  - qty > 0: **1.644** (tổng qty = 3.514, max 60) ← đối tượng reset
  - qty = 0: 11.791 · qty < 0: 0
- `prepick_logs` hiện có: 54.658 → sau khi chạy dự kiến +1.644 = 56.302

## Quyết định thiết kế
- **Log ghi TRƯỚC khi đổi qty**: `qty_before = qty cũ`, `change = -qty`, `qty_after = 0`,
  `prepick_detail_id = id`. Các cột NOT NULL của `prepick_logs` là `qty_before/change/qty_after` (decimal).
- **`objectable_id` / `objectable_type` để null** — thao tác reset thủ công hàng loạt,
  không gắn chứng từ nguồn. Nếu cần truy vết theo loại phiếu điều chỉnh → bổ sung sau.
- **`chunkById(500)`** thay vì `get()` toàn bộ: an toàn với 1.644+ bản ghi, và vì paginate theo
  `id` (không theo `qty`) nên không bị lệch trang dù đang update chính cột `qty` trong điều kiện lọc.
- **Bọc transaction**: lỗi giữa chừng rollback cả `prepick_details` lẫn `prepick_logs`.
- Class `UpdateDB` ở **global namespace** → gọi `(new \UpdateDB)->...`.

## ⚠️ Rủi ro môi trường (quan trọng — phát hiện trong session)
`bootstrap/cache/config.php` (05/08/2025) cache cứng DB **production** `erp.eteksofts.com:33061/erp_new`.
Khi file này tồn tại, Laravel bỏ qua `.env` → mọi lệnh artisan/tinker chạy lên production.
`.env` lại ghi `DB_DATABASE=erp_8825` (không tồn tại local; local thật là `erp2326`).
→ Trước khi chạy seeder BẮT BUỘC: `config:clear` + sửa `.env` sang `erp2326` + verify resolve.
Chi tiết các bước ở `plan.md`.

## Cách chạy (sau khi đã fix môi trường)
```
php artisan tinker --execute="(new \UpdateDB)->resetPrepickDetailQtyCompany4();"
```

## Trạng thái
Code + lint xong. **Chưa chạy** — chờ xử lý config cache & xác nhận DB local đích (`erp2326`).
