# Plan — Bắt buộc field khi gửi duyệt gói thầu lên TP

**Người phụ trách:** @khoipv
**Plan chi tiết (TDD):** `docs/superpowers/plans/2026-06-08-bid-package-send-approve-required-fields.md`

## Phase 1 — Backend

- [x] BE: Thêm `use BidPackage` vào `StoreBidPackageRequest`
- [x] BE: Thêm 4 rule có điều kiện (`status == CHO_DUYET_KET_QUA`) trong `rules()`
- [x] BE: Thêm 5 message tiếng Việt trong `messages()`
- [x] Test thủ công: Gửi duyệt thiếu field → 422
- [x] Test thủ công: `execution_time = 0` → chặn bởi `gt:0`
- [x] Test thủ công: Lưu nháp / Lưu và gửi vẫn để trống được
- [x] Test thủ công: Gửi duyệt đủ field → thành công

## Checkpoint

### Checkpoint — 2026-06-08
Vừa hoàn thành: code BE xong (import + 4 rule + 5 message), `php -l` pass
Đang làm dở: không
Bước tiếp theo: người dùng kiểm thử thủ công 4 case trên UI gói thầu
Blocked:

### Checkpoint — 2026-06-08 (DONE)
Vừa hoàn thành: kiểm thử thủ công 4 case đều pass → feature hoàn thành
Đang làm dở: không
Bước tiếp theo: không — đã chuyển sang "Hoàn thành" trong STATUS.md
Blocked:
