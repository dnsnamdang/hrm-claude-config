# Meeting — dọn file rác trên S3 (tài liệu chuẩn bị + tài liệu kèm biên bản)

Vấn đề: chọn file là upload thẳng lên S3; đổi file / xoá dòng / thoát không lưu → file cũ nằm lại S3 mãi.
Chốt 2026-10-01: làm cả 2 lớp.

## Phase 1 — Dọn file

### BE
- [x] `CmcS3Helper`: thêm keyFromUrl / isTemporaryUrl / promoteTemporary (copy tmp → thư mục chính) / deleteByUrl / deleteTemporaryOlderThan
- [x] `files/upload` nhận `temporary=1` → đẩy vào `tanphat_hrm/tmp/` (mặc định giữ nguyên hành vi cũ cho mọi màn khác)
- [x] `MeetingService::syncAttachments`: file tạm → chuyển sang `tanphat_hrm/`; file cũ bị bỏ/đổi → xoá S3 SAU commit (`DB::afterCommit`); file tạm hết hạn → 422 tại dòng
- [x] `MeetingController::destroy`: xoá meeting thì xoá luôn file S3 sau commit
- [x] Lệnh `files:clean-temporary` (xoá file tmp > 48h) + đăng ký schedule hằng ngày

### FE
- [x] `FileAttachmentTable`: prop `temporaryUpload` (mặc định false, không ảnh hưởng 8 màn khác)
- [x] Meeting: bật `temporary-upload` ở Tài liệu chuẩn bị; tab Biên bản upload kèm `temporary=1`
- [x] Payload lưu meeting bỏ object `File` (trước đây gửi lại nguyên file lần 2, cột `file` ghi rác `/tmp/phpXXX`)

### Kiểm thử
- [x] Test helper trên S3 thật: upload tmp → chép sang chính → xoá; URL lạ / ngoài phạm vi bị từ chối; lệnh dọn chạy được, schedule 02:30
- [x] Test luồng UI (Playwright) + đối chiếu portal CMC: tạo (A→B, thêm C rồi xoá) / Sửa đổi B→D / nút Thay đổi D→E / file tạm quá hạn báo lỗi tại dòng / tab Biên bản / xoá hết dòng / xoá meeting / dọn tmp — đạt hết

### Checkpoint — 2026-10-01
Vừa hoàn thành: code + test đầy đủ (UI + S3 portal)
Đang làm dở: —
Bước tiếp theo: user review, deploy kèm kiểm cron schedule:run trên prod
Blocked:
