# Plan — Báo cáo tồn kho kế toán hiện dòng đã hết tồn

- [x] Truy nguyên nhân: HAVING `SUM(asl.value_after) > 0` cộng dồn số dư từng log
- [x] Đối chiếu DB `hrm_erp_gop` kho LN02 (id 2): 3 mã SUM(change)=0, SUM(value_after)>0
- [x] Sửa HAVING `app/Product.php` + `app/ProductTemplate.php` (biểu thức đầy đủ, không alias)
- [x] Verify tinker: LN02 → 0 dòng; kho id 1 → 4,704 dòng (4,703 SL>0 + 1 lệch giá trị), tổng dòng khớp Summary; ProductTemplate chạy OK
- [x] Commit `283c9dd334` + push `origin/gop_db` (rebase lên `bddfec1e21`)

### Checkpoint — 2026-10-10
Vừa hoàn thành: fix + verify + commit/push gop_db
Đang làm dở:
Bước tiếp theo: deploy gop_db lên erp.eteksofts.com, user xác nhận lại màn kho LN02
Blocked:
