# Plan — Sửa UI màn Tạo Yêu cầu xuất hàng (`/finance/product-export-requests/create`)

> Phụ trách: @namdangit · Nhánh: `gop_db` · Tạo: 2026-09-15
> Chuẩn tham chiếu ("làm chuẩn"): `/finance/bill-payment-requests/create`
> File chính FE: `hrm-client/pages/finance/product-export-requests/components/ProductExportRequestForm.vue`
> File chính BE: `hrm-api/Modules/Assign/Http/Controllers/Api/V1/ProductExportRequestController.php`

Nguồn: Redmine + 4 ảnh chụp màn. 3 nhóm bug.

## Fix #2 — Thanh nút form (viền trắng đè menu + thứ tự "Quay lại")
- [x] FE: thay khối tự dựng `.export-actionbar` (`position:fixed; left:0; right:0; padding-left:80px`) bằng `<V2Footer>` — footer chuẩn `right:0` content-width, KHÔNG đè sidebar, tự render "Quay lại" ở CUỐI (đúng skill list-page 7.2 + button-convention).
  - menu: `{ submit_and_draft: true, save_and_submit_approve: true, submit_and_continue: !isEdit }`
  - `@submitAndDraft="onSubmitClick(3)"` · `@saveAndSubmitApprove="onSubmitClick(2)"` · `@submitAndContinue="onSubmitClick(3, true)"` · `@goBack="$emit('back')"`
- [x] FE: bỏ inline `padding-bottom: 72px` ở div gốc (V2Footer tự thêm spacer `body.has-v2-footer`).
- [x] FE: gỡ SCSS `.export-actionbar` (đã chết).
- [x] FE: import + đăng ký `V2Footer`.

## Fix #3 — "Kho xuất" hiển thị "Mã - tên" (đang chỉ hiện tên)
- [x] BE `createData()`: `->get(['id', 'name'])` → `->get(['id', 'code', 'name'])`.
- [x] BE `editData()`: dựng nhãn kho merge = `"<code> - <name>"` (áp cho cả Kho xuất + Kho nhập, giữ được kho đã khoá).
- [x] FE `fetchWarehouses()`: label = `w.code ? \`${w.code} - ${w.name}\` : w.name` (null-guard). Áp cho cả 2 select (Kho xuất + Kho nhập, chung `warehouseOptions`).

## Fix #1 — Section header + form đính kèm theo chuẩn bill-payment
**Hướng đã chốt: Cách A** — bê nguyên `AttachmentSection` (prop `apiBase` nên BE-agnostic) + 3 endpoint BE; section header đổi từ `.c-section`/icon badge màu sang `V2BaseFormSection` (nền trắng, icon xanh brand) như bill-payment.

- [x] BE `ProductExportRequestController`: thêm `uploadFiles` (`POST /upload-files` → `CmcS3Helper::putFiles` trả mảng URL), `attachmentSizes` (`GET /{id}/attachment-sizes` → map `{file_path: file_size}` từ bảng `files`), `deleteFile` (`DELETE /{id}/files?file_url=` → gate canEdit, xoá row `files` theo file_path + object S3). Const `S3_FOLDER`.
- [x] BE `store`/`update`: sau khi lưu gọi `persistAttachmentUrls($id, attachment_urls)` — ghi URL vào bảng `files` (append, bỏ URL đã có, tên suy từ basename). Thêm rule `attachment_urls`/`attachment_urls.*` vào base `rulesForType`.
- [x] BE Routes: `POST /upload-files` (tĩnh, TRƯỚC `/{id}`), `GET /{id}/attachment-sizes`, `DELETE /{id}/files`. Giữ lại route `/{id}/attachments` cũ (không dùng nữa nhưng vô hại).
- [x] FE `ProductExportRequestForm`: thay khối `.attach-block` tự dựng bằng `<AttachmentSection api-base="assign/product-export-requests">` (khối riêng, sibling — không lồng trong "Thông tin chung"); `pendingFiles` đổi thành `[{url,name,size}]`; computed `attachmentFileUrls`; handlers `onAddUploadedFile`/`removePendingAttachment`/`replaceAttachment`/`removeSavedAttachment`; payload thêm `attachment_urls`; gỡ 4 method + SCSS `.attach-*` cũ. Import + đăng ký `AttachmentSection`.
- [x] FE section header: 2 khối `.c-section` → `<V2BaseFormSection>` với `#title` (icon xanh brand + text) + `#actions` (meta người tạo / nút "Thêm hàng hoá"). Gỡ SCSS `.c-section`/`.section-header`/`.sec-goods`/`.section-body`, thêm `.text-brand` + `.header-meta`. Import + đăng ký `V2BaseFormSection`.
- [x] FE `create.vue` + `_id/edit.vue`: gỡ lời gọi `uploadPendingFiles(id)` sau lưu (đính kèm nay gửi kèm `attachment_urls[]`).

### Checkpoint — 2026-09-15 (Fix #1 code xong + verify tĩnh)
Vừa hoàn thành: Fix #1 (Cách A) — BE 3 endpoint + persist attachment_urls, FE AttachmentSection + V2BaseFormSection. Cả 3 fix đã code xong.
Đã verify (mức tối đa môi trường cho phép):
- FE: 5 SFC (form, create, edit, AttachmentSection, V2BaseFormSection) compile SẠCH bằng `vue-template-compiler` của chính project (Node 14). CR=0.
- FE: dev server :3000 phục vụ route `/finance/product-export-requests/create` HTTP 200, không có marker "Failed to compile / Build error".
- BE: routes `upload-files` (dòng 689, tĩnh — trước `/{id}`), `attachment-sizes` (705), `files DELETE` (706) có mặt; methods `uploadFiles/attachmentSizes/deleteFile/persistAttachmentUrls` + const `S3_FOLDER` + rule `attachment_urls` có mặt; `php -l` sạch cả Routes + Controller.
BLOCKED — verify Playwright trực quan CHƯA chạy được: checkout này KHÔNG có Playwright MCP, KHÔNG có thư mục `e2e/`, và máy chỉ có Node 12/14 (harness cần Node 20). Cần user chạy `--project=setup` + bộ e2e trên môi trường có Node 20, hoặc tự mắt nhìn tại http://127.0.0.1:3000/finance/product-export-requests/create (2 dev server đang chạy).
Bước tiếp theo: chờ user xác nhận cách verify trực quan (mở trình duyệt xem, hoặc bổ sung harness Playwright).

## Ghi chú
- Line ending: file FE + BE đều LF → giữ LF.
- Draft = status 3, Gửi duyệt = status 2 (khác bill-payment draft=1, không đổi).
