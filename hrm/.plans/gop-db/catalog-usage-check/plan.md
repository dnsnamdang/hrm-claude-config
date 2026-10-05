# Plan — catalog-usage-check

**Người phụ trách:** @junfoke — 2026-10-03 · Nhánh `feat/catalog-usage-check` (worktree `.worktrees/catalog-usage`, cả 2 repo)

## Phase 0 — Khảo sát
- [x] Quét 21 danh mục ERP→HRM: màn nào trỏ tới (schema gop_db + code ERP/HRM) — 02/10/2026
- [x] Xuất Excel chi tiết + bản gọn 4 cột gửi QA
- [x] Chốt rule với user (Xóa chặn khi đã dùng; Khóa chỉ chặn khi còn con Hoạt động; bỏ KH; làm cả phần @khoipv)

## Phase 1 — Nền
- [x] Tạo worktree + nhánh từ `develop` (vendor copy thật, KHÔNG junction)
- [x] Helper `app/Support/CatalogUsage.php` + test tinker

## Phase 2 — Địa lý (Quốc gia, Khu vực, Tỉnh/TP, Quận/huyện, Phường/xã)
- [x] BE tham chiếu xóa + chặn BE + chặn khóa khi còn con Hoạt động (lock + update)
- [x] Resource `is_can_delete` / `is_can_lock` cả trang; FE ẩn nút

## Phase 3 — Kế toán + Ngân hàng (Tài khoản, Loại TK, Tiền tệ, Ngân hàng, Vụ việc, Nguồn vốn)
- [x] BE + FE theo spec mục 4

## Phase 4 — CSKH (Lỗi thiết bị, Serial)
- [x] BE + FE

## Phase 5 — Kiểm chứng
- [x] Review diff toàn bộ, `php -l`, tinker trên gop_db
- [x] Gọi thẳng API xóa/khóa 8 ca bị chặn (Quốc gia/Khu vực/Phường/Ngân hàng) → 400 đúng câu, DB không đổi
- [x] Playwright xem ảnh: Quốc gia, Ngân hàng, Phường/xã
- [x] Cập nhật STATUS + checkpoint
- [x] Commit + merge `develop` (api e84617c28/06f166850 · client 0c39eb2e9/c6ae8dc30), chưa push
- [ ] QA test theo file Excel

## Checkpoint — 2026-10-03
- Vừa hoàn thành: code xong Phase 2-4 (hrm-api 37 file + helper mới, hrm-client 9 file), kiểm tinker + API + Playwright.
- Đang làm dở: không.
- Bước tiếp theo: push `develop` khi user đồng ý; gửi QA file Excel bản gọn.
- Blocked: không. Lưu ý: chưa test được nhánh "ngân hàng chỉ dùng qua chi nhánh" và serial chỉ nằm ở `wr_import_result_extend_products` (local không có dữ liệu).
