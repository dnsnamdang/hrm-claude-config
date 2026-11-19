# Biên bản meeting — "Ghi nhận nội dung meeting" + "Giao người xử lý" + hỏi Hoàn thành sau Lưu (web + app) — @namdangit

Yêu cầu user 08/11/2026. Nhánh: hrm-api + hrm-client `gop_db`, TPE_APP `develop`. Không migration, không quyền mới.

## Mục tiêu
- Biên bản không bắt mọi dòng phải có người thực hiện + hạn: nhiều nội dung chỉ để GHI NHẬN.
- Mobile: màn biên bản + nhập nội dung gọn hơn (mockup 09' / 10a' / 10b' trong `meeting-mobile.pen`, khung
  "BIÊN BẢN — vẽ lại 08/11", x 2900 y 12620 — user duyệt 08/11).
- Lưu biên bản xong hỏi Hoàn thành luôn, Hoàn thành xong về đúng màn đã mở (Danh sách meeting / Việc của tôi).

## Quyết định đã chốt
| # | Nội dung | Ai chốt |
|---|---|---|
| 1 | Mục "Các nội dung khác" → **"Ghi nhận nội dung meeting"** (form web, bản in, PDF, câu lỗi, nhãn app) | user |
| 2 | Dòng chỉ bắt buộc Nội dung. Ô tick **"Giao người xử lý"** → Người đề xuất (không bắt buộc) · Người thực hiện * · Hạn dự kiến * | user |
| 3 | Dòng không tick vẫn có nút "Giao" (giao nhiệm vụ) ở màn Chi tiết web; popup điền tên, người/hạn để trống | user (Q1) |
| 4 | Mobile: Người đề xuất + Người thực hiện chung 1 hàng; Hạn hàng riêng; danh sách gom 1 thẻ | user (duyệt mockup) |
| 5 | Lưu biên bản → hỏi "Có muốn xác nhận hoàn thành cuộc họp luôn?" — cả web và app | user (chọn 2) |
| 6 | KHÔNG thêm cột: tick suy từ "có người thực hiện"; BE trả `has_assignee` (accessor `MeetingReport`) | Claude |
| 7 | Payload gửi `reports[i].has_assignee`; **thiếu cờ ⇒ coi như tick** (app bản cũ trên prod giữ luật cũ) | Claude |
| 8 | Bỏ tick ⇒ BE gỡ người đề xuất / người thực hiện / hạn trước validate + khi lưu | Claude |
| 9 | Chỉ hỏi Hoàn thành khi: Chốt lịch · BE `can_complete` · ≥1 nội dung · có kết luận (web thêm: đang ở tab Biên bản). Hỏi xong không hỏi lần 2 | Claude (thêm sau khi thử thấy hỏi lúc thiếu kết luận là thừa) |
| 10 | Footer mobile theo quy ước 29/10: nút chính trái, Huỷ / Quay lại phải | Claude (quy ước có sẵn) |

## Thiết kế kỹ thuật (tóm tắt)
- **BE**: trait `Http/Requests/Meeting/NormalizesMeetingReportRows` (gắn Create + Update request, chạy trong
  `prepareForValidation`) → rule `required_if:reports.*.has_assignee,1` cho `executor_name` + `expected_deadline`.
  `MeetingService::syncReports` gỡ dữ liệu giao người khi `has_assignee = 0`. `MeetingReport::getHasAssigneeAttribute`.
- **Web**: `MeetingReport.vue` (ô tick dưới ô Nội dung, ẩn 3 cột → ô giữ chỗ col-6 có nút xoá), `MeetingForm.vue`
  (kiểm thiếu theo tick, `canOfferCompleteAfterSave()`, `backUrl` nhận `from=my-todo`), `_id/edit.vue` (`$confirm` sau
  lưu → `handleComplete()`; quay về theo `from`), `my-todo/index.vue` (Sửa meeting gửi `from=my-todo`).
- **App**: `meeting_report_item_page.dart`, `meeting_minutes_page.dart` (lưu xong `pop(true)` ⇒ Hub Hoàn thành),
  `meeting_hub_page.dart` (`_complete({confirm})`), `meeting_widgets.dart` (`MeetingSelectRow.maxLines`, mặc định 2).

## Ảnh hưởng / lưu ý
- Bản in, Excel, báo cáo meeting giữ đủ cột; dòng không giao để trống.
- Client khác gửi lại `reports` mà KHÔNG kèm `has_assignee` sẽ bị bắt buộc người thực hiện + hạn (cố ý, cho app cũ).
  Spec e2e dựng payload từ detail phải gửi lại `has_assignee`.
- E2E: hạ tầng meeting fixture tự dựng `e2e/utils/e2eMeetingFixture.ts`; 3 seed e2e trong `hrm-api/database` đọc chủ
  fixture theo `E2E_OWNER_EMAIL` → `TEST_EMAIL` (e2e/.env). Chi tiết ở plan.md.
