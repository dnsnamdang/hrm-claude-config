# Plan — HSNS cho phép xóa file đã upload

## Phase 1 — FE
- [x] `components/common/AttachmentGallery.vue`: thêm prop `deletable` + emit `remove(index)`, nút ✕ góc trên phải (kiểu nút xóa của `V2BaseFile`), `@click.stop`
- [x] `EmployeeInfoForm.vue`: bật `deletable` cho 3 gallery (CCCD, Hộ chiếu, Bằng cấp)
- [x] `EmployeeInfoForm.vue`: thêm `removeEmployeeIdCard` / `removeEmployeePassport` / `removeEducationAttachment`
- [x] Reset `input[type=file].value` sau upload và sau khi xóa để chọn lại đúng file vừa xóa vẫn chạy
- [x] Verify bằng Playwright: nút ✕ hiện đủ, xóa đúng phần tử, không mở popup xem trước, 2 ô CCCD/Hộ chiếu độc lập

## Phase 2 — Chốt nhánh
- [x] Commit trên `tpe-develop-assign`: `327c1a5fa` ("fix lỗi", do user commit)
- [x] Cherry-pick sang nhánh `tpe`: `3d23c724c` (làm trong worktree `wt-hdld-client` vì `tpe` đang bị worktree đó giữ)
- [ ] Push lên remote — CHƯA làm, chờ user yêu cầu

### Checkpoint — 2026-09-23
Vừa hoàn thành: Phase 1 (FE) — đã verify trên dev server dựng từ `hrm-cursor/hrm-client`.
Đang làm dở: không.
Bước tiếp theo: user bấm Lưu thử trên môi trường dev để xác nhận BE nhận mảng đính kèm đã rút gọn; quyết định có push `tpe` / `tpe-develop-assign` lên remote không.
Blocked:
