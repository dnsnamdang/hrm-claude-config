# Meeting — CKEditor + Tài liệu chuẩn bị (Redmine #11194)

Người phụ trách: @cuong61n · Nhánh: `tpe` (cả hrm-api + hrm-client) · Ngày: 2026-08-24
Task: http://quanly.dnsmedia.vn/issues/11194

## Mục tiêu

Màn Quản lý Meeting → Lịch meeting (Tạo mới / Sửa / Chi tiết):

1. Tab **Thông tin** — trường "Mục tiêu / Nội dung" (`meetings.note`): textarea → CKEditor.
2. Tab **Biên bản** — trường "Kết luận cuộc họp" (`meetings.conclusion`): textarea → CKEditor,
   bỏ giới hạn ký tự ở cả FE và BE.
3. Tab **Thông tin** — thêm vùng "Tài liệu chuẩn bị cho buổi họp", upload/xem/tải/xoá như
   "Import tài liệu kèm biên bản", nhưng **lưu tách bạch** với tài liệu biên bản.

## Quyết định đã chốt (2026-08-24, user chốt)

| Vấn đề | Chốt |
| --- | --- |
| Tiêu đề task ghi "Chuyển vị trí trường Mục tiêu" nhưng mô tả/AC không nói chuyển đi đâu | **Giữ nguyên vị trí**, chỉ đổi sang CKEditor (đúng mô tả + AC1) |
| Bản CKEditor | Dùng `components/shared/CompactReviewEditor.vue` — đúng khuôn màn `/assign/quotations/create` (CKEditor 4 qua `$loadCKEditorPrint`), đang dùng khắp phân hệ Giao việc |
| Nơi lưu tài liệu chuẩn bị | Thêm cột `type` vào `meeting_attachments` (1 = kèm biên bản, 2 = chuẩn bị) |
| UI vùng upload | Component chung `components/FileAttachmentTable.vue` (skill thắng spec về hình thức UI) |

## Ảnh hưởng dây chuyền (note/conclusion từ text thuần → HTML)

- `meetings.note` (text) và `meetings.conclusion` (text) → **LONGTEXT** (HTML + tiếng Việt 3 byte/ký tự
  vượt 64KB rất nhanh khi bỏ giới hạn).
- BE bỏ `conclusion max:4000`, `note max:1000` ở cả `MeetingCreateApiRequest` và `MeetingUpdateApiRequest`.
- Nơi hiển thị `conclusion`/`note` bằng `{{ }}` phải strip tag: `MeetingDetailDrawer.vue` (tab Lịch meeting
  của Todo), `MeetingMinutesModal.vue` (báo cáo theo thị trường). Export Excel biên bản đã có `toPlainText`.
- Bản in `resources/views/exports/meeting_record.blade.php` đang `nl2br(e($meeting->conclusion))` →
  phải xuất HTML (đã lọc) thay vì escape, nếu không bản in hiện nguyên thẻ `<p>`.

## Ghi nhận thêm (KHÔNG sửa trong task này)

Bảng `meetings` có cả `content` (longtext) lẫn `note` (text). Bản in lấy mục "Mục tiêu cuộc họp" từ
`content`, nhưng FE chỉ ghi vào `note` → mục đó luôn rỗng khi in. Đây là lỗi có sẵn, ngoài phạm vi #11194.

Spec chi tiết: `docs/superpowers/specs/2026-08-24-meeting-ckeditor-tailieu-chuanbi-design.md`
