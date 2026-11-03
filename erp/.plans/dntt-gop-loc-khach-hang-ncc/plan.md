# DS Đề nghị thanh toán: gộp ô lọc Khách hàng và NCC thành 1 ô

Không Redmine · @junfoke · ERP `TanPhatDev`, nhánh `gop_db`

## Ngày 03/11/2026 (@junfoke)
- [x] 03/11/2026 — Theo yêu cầu: DS DNTT (`bill_payment_requests`) gộp 2 ô Khách hàng + NCC thành 1 ô "Khách hàng / Nhà cung cấp" (gõ tìm, API khách hàng `?all=1` vì KH và NCC chung bảng `customers`). `BillPaymentRequest` thêm lọc `partner_id` (khớp KH hoặc NCC ở đầu phiếu hoặc dòng chi tiết), giữ lọc `customer_id`/`supplier_id` cũ. Đối chiếu local: NCC 152 phiếu, KH 2 phiếu = ô cũ. Commit `f4e2c56efa`.
- [x] 03/11/2026 — Gộp tiếp ở DS DNTT chờ duyệt (`forApproved.blade.php`), chỉ đổi giao diện (dùng chung lọc). Commit `2397f6bddd`.
- [ ] Màn DNTT đã duyệt (`approved.blade.php`) còn 2 ô riêng — chờ user bảo có gộp không.
