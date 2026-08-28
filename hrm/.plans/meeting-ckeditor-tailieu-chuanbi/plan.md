# Plan — Meeting CKEditor + Tài liệu chuẩn bị (#11194)

## Phase 1 — BE (hrm-api, nhánh tpe)

- [x] Migration: thêm `type` (tinyint, default 1) vào `meeting_attachments`
- [x] Migration: đổi `meetings.note` + `meetings.conclusion` sang LONGTEXT (DB::statement, không transaction)
- [x] `MeetingAttachment`: thêm `type` vào `$fillable` + hằng số TYPE_REPORT / TYPE_PREPARE
- [x] `Meeting`: `attachments()` lọc type=1, thêm quan hệ `prepare_attachments()` type=2
- [x] `MeetingService::syncAttachments()`: nhận thêm `$type`, chỉ xoá/ghi đúng loại
- [x] `MeetingController` store/update: sync `prepare_attachments` (type=2); show/print load quan hệ mới
- [x] `MeetingCreateApiRequest` + `MeetingUpdateApiRequest`: bỏ `conclusion max:4000`, `note max:1000`; thêm rule `prepare_attachments`
- [x] Transformer/getDataForShow: trả `prepare_attachments`
- [x] Blade in `exports/meeting_record.blade.php`: xuất HTML đã lọc cho `conclusion` (thay `nl2br(e())`)

## Phase 2 — FE (hrm-client, nhánh tpe)

- [x] `GeneralInfo.vue`: "Mục tiêu / Nội dung" → `CompactReviewEditor` (giữ nguyên vị trí)
- [x] `GeneralInfo.vue`: thêm `FileAttachmentTable` "Tài liệu chuẩn bị cho buổi họp" (`form.prepare_attachments`)
- [x] `MeetingReport.vue`: "Kết luận cuộc họp" → `CompactReviewEditor`
- [x] `MeetingForm.vue` + `create.vue` + `_id/edit.vue`: khởi tạo `prepare_attachments: []`, map formError về tab Thông tin
- [x] `MeetingDetailDrawer.vue` + `MeetingMinutesModal.vue`: strip HTML khi hiển thị `note`/`conclusion`

## Phase 3 — Kiểm thử

- [x] Tạo mới / Sửa / Xem: 2 editor hiển thị đúng, lưu > 5.000 ký tự không lỗi (đã lưu 11.755 ký tự)
- [x] Upload pdf/docx/xlsx/png vào "Tài liệu chuẩn bị", lưu → mở lại tải xuống được
- [x] Tài liệu chuẩn bị không lẫn sang tab Biên bản và ngược lại
- [x] In biên bản: kết luận hiển thị đúng định dạng, không lộ thẻ HTML
- [x] Fix: bản in "Mục tiêu cuộc họp" lấy nhầm cột `content` (luôn rỗng, màn hình không ghi vào) → đổi sang `note`, fallback `content`, xuất HTML đã lọc (`meeting_record.blade.php` + `objectiveHtml` ở `MeetingController::renderTemplate`)
- [x] Fix: cột Dung lượng mất đơn vị sau khi lưu — thêm `normalizeAttachmentSize()` (`utils/helpers.js`), dùng ở `_id/edit.vue` + `_id/show.vue`
- [x] Fix: `FileAttachmentTable` truyền `variant="secondary"` không hợp lệ cho `V2BaseBadge` → đổi sang `muted` (hết Vue warning ở cả 5 màn dùng component)
- [x] Fix: 2 editor thiếu `:remove-buttons="''"` nên toolbar bị rút gọn — phải đủ nút như "Điều khoản báo giá" của màn Báo giá (`GeneralInfo.vue`, `MeetingReport.vue`)

### Checkpoint — 2026-08-24
Vừa hoàn thành: Phase 1 (BE) + Phase 2 (FE) của #11194. Migration đã chạy trên `hrm_prod_6_6`
(`meeting_attachments.type`, `meetings.note/conclusion` → LONGTEXT). Smoke test BE bằng tinker
(trong transaction, đã rollback): sync type=2 không đụng 3 tài liệu biên bản của meeting 50;
lưu conclusion 30.000 ký tự đọc lại nguyên vẹn.
Đang làm dở: không.
Bước tiếp theo: Phase 3 — test UI trên trình duyệt (dev server đang chạy FE :3000, BE :8000).
Blocked: không.

### Checkpoint — 2026-08-25
Vừa hoàn thành: Phase 3 — test UI thật trên trình duyệt với meeting test id=58.
4/4 AC đạt. Sửa thêm: bổ sung `:remove-buttons="''"` cho 2 CompactReviewEditor (toolbar đầy đủ).
Đã fix thêm 3 lỗi (dung lượng mất đơn vị, badge sai variant, bản in Mục tiêu lấy nhầm cột) —
verify lại trên trình duyệt OK. Bản in đã kiểm 3 trường hợp: note HTML giữ định dạng, note text
thuần in bằng nl2br, không có note thì ẩn hẳn section.
Tồn tại: "chuyển vị trí trường Mục tiêu" ở tiêu đề task chưa rõ chuyển đi đâu → GIỮ NGUYÊN vị trí cũ,
user hỏi lại TPE Lệ. Dữ liệu test giữ lại: meeting id=58 trên DB local.
Bước tiếp theo: chờ TPE Lệ trả lời về vị trí trường Mục tiêu.
Blocked: không.
