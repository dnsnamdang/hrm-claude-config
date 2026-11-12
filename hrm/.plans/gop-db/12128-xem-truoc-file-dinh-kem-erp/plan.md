# #12128 — Plan

Design: `design.md` · Spec: `docs/superpowers/specs/gop-db/2026-11-12-12128-xem-truoc-file-dinh-kem-erp-design.md`

## Phase 1 — Khảo sát
- [x] Đọc issue (không ảnh, không ghi chú)
- [x] Khảo sát ERP: 211 file `document-item`, ~25 màn dùng partial `upload_files`, ~70 link lẻ, `gallery-file`, `ng-app` ở body
- [x] S3 CMC trả `application/octet-stream`, không CORS ⇒ không nhúng thẳng URL; ~10.100 file S3 / 45 file local
- [x] Đối chiếu HRM `FilePreviewModal.vue` (Google Viewer / Office Online / img / text)

## Phase 2 — Code (TanPhatDev, nhánh `task_12128`)
- [x] `partials/common-js/file-preview.blade.php`: popup + `window.FilePreview` + directive `a` + xem file chưa lưu
- [x] Include trong `layouts/app.blade.php`

## Phase 3 — Verify (local 8318, BBBGNT 8461)
- [x] 4 ô file có đúng 1 nút 👁; docx (Office Online), jpg, pdf (Google ~10s), xlsx đều hiển thị
- [x] zip → "Định dạng file chưa hỗ trợ xem trước" + Tải xuống; Esc đóng
- [x] Link lẻ icon + tên cùng URL → 1 nút sau tên; link menu không bị gắn; xoá URL → gỡ nút
- [x] File txt vừa chọn ở màn tạo → xem nội dung, ẩn Tải xuống
- [x] Lỗi `infdig` / `select2Employee` trên màn có sẵn từ trước (đã so sánh khi bỏ include)

## Phase 4 — Bàn giao
- [x] Commit `720745e500` trên `task_12128` → merge `develop_02` (`3422b02fdb`) → push origin (12/11)
- [ ] QA test trên dev
- [x] User cho merge: `task_12128` → `gop_db` (`5d33749939`) → push origin (12/11)

## Phase 5 — Đổi kiểu thẻ file theo ảnh mẫu user (12/11 chiều)
- [x] Thẻ file: icon Material Symbols màu theo loại, tên, "Xem trước", nút tải góc phải; ✕ (màn sửa) sang góc trái
- [x] Bấm thẻ / link = xem trước; chỉ icon tải mới tải; Ctrl/Shift/chuột giữa giữ hành vi cũ
- [x] Verify local (playwright-b): thẻ, bấm tên/icon/hint mở popup, icon tải chỉ tải, ✕ chỉ xoá, link lẻ, header popup
- [x] Verify màn SỬA thật (BBBGNT 7426, tạm gán created_by=13 rồi trả 244): thẻ có ✕ trái + tải phải, bấm tên = xem, tải chỉ tải, ✕ chỉ xoá
- [x] Ô file mới chọn cũng thành thẻ (icon theo loại, tên, "Xem trước", bấm = xem blob, không mở lại hộp chọn file); `$applyAsync` để tên file hiện ngay
- [x] Ô "+" cùng hàng thẻ: cùng kích thước 120×116, bo 10px
- [x] Thẻ thu về 96×96 (cũ 80×80, bản đầu 120×116 to quá); khung chứa thêm `fp-wrap` tự xuống dòng (406 khung `d-flex` không wrap)
- [x] Ô chọn 1 file KHÔNG có ✕ (vd trong bảng) giữ nguyên, chỉ thêm 👁; file xem trước đọc từ input LÚC BẤM; bỏ qua ô "+" có input
- [x] Test: 12 thẻ / 14 thẻ khung d-flex trơn → xuống 2–3 hàng không tràn; ô bảng 150px vừa; thêm/xoá nhiều lần ở màn BaseFile (BBBGNT) khớp
- [x] PHÁT HIỆN lỗi CÓ SẴN (tắt partial vẫn y hệt): danh sách `track by $index` + Lưu đọc `#document{index}` (vd Đề nghị thanh toán):
      thêm A,B,C → xoá B → thêm D,E → xoá A → thêm F: hiện C,D,E,F nhưng GỬI A,B,D,F. Ngoài phạm vi #12128 — chờ user quyết
- [x] User cho sửa luôn: 12 form bỏ `track by $index` ở `addition_attachments` (khuôn `bill_adjust_depts` vốn không track) +
      handler `.attachments` đọc `+$(this).attr('data-index')` (`.data()` cache chỉ số cũ). Verify ĐNTT + Bàn giao công việc:
      hiện = model = gửi đi qua 3 vòng, chọn lại file sau khi xoá dòng vẫn đúng. Commit `3b198f270d` → `develop_02` `0e19c3a2c0` → push
- [x] Thẻ: padding 15px trên / 10px dưới + `space-between` (theo ảnh user). Commit `fb17375071` → `develop_02` `02b11a8a71` → push
- [x] Commit `314e69c331` trên `task_12128` → merge `develop_02` (`c1ee29a80a`) → push origin (12/11)

## Checkpoint — 2026-11-12
- Vừa hoàn thành: code + verify local, đã lên `origin/develop_02`.
- Đang làm dở: không.
- Bước tiếp theo: chờ QA (nhờ rà thêm màn có link lẻ: chi phí đính kèm nhập hàng, báo giá hãng); đạt thì merge vào `gop_db`.
- Blocked: không.
