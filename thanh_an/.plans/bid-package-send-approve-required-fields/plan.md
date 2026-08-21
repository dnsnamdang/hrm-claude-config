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

## Phase 2 — Bổ sung 3 field khi gửi duyệt (2026-08-04)

Yêu cầu: bắt buộc thêm 3 field khi gửi duyệt, giống nhóm thời điểm mời/đóng thầu:
`posted_time` (Ngày đăng tải), `khlcnt_code` (Mã KHLCNT), `khlcnt_type` (Phân loại KHLCNT).

- [x] BE: `posted_time` → có điều kiện `required` khi gửi duyệt
- [x] BE: `khlcnt_code` → đổi từ `nullable|max:255` sang có điều kiện `required|max:255` khi gửi duyệt
- [x] BE: `khlcnt_type` → thêm mới, có điều kiện `required` khi gửi duyệt
- [ ] Test thủ công: Gửi duyệt thiếu 1 trong 3 field → 422; lưu nháp vẫn để trống được

### Checkpoint — 2026-08-04
Vừa hoàn thành: sửa `StoreBidPackageRequest` thêm điều kiện required cho 3 field (dùng chung cho store + update)
Đang làm dở: không
Bước tiếp theo: người dùng kiểm thử trên UI
Blocked:
