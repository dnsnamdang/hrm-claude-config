# Gõ @ trong bình luận linh hoạt như khung chat (chưa có số Redmine) — @cuong61n

Nhánh: `gop_db` (worktree `worktrees/gop_db-client`). File: `hrm-client/components/comments/CommentEditor.vue`.

- [x] 2026-11-18 Gợi ý @ ở bình luận (nhiệm vụ, vấn đề…) làm giống khung chat `ChatComposer`:
  - tìm không dấu (gõ "tuan" ra "Tuấn"), tìm cả theo mã nhân viên, gõ được tên nhiều chữ;
  - dòng gợi ý có avatar + nhãn chuẩn "Tên - Mã phòng - Mã NV" (`employeeOptionText`);
  - ↑↓ chọn có xoay vòng và cuộn theo, Enter hoặc Tab để chèn; tối đa 8 dòng;
  - hộp gợi ý tự mở lên phía trên khi sát đáy màn hình; "@" chỉ tính khi đứng đầu hoặc sau khoảng trắng (email không bật gợi ý).
- [x] 2026-11-18 Avatar ảnh thật: `store.employees` không có ảnh ⇒ nạp từ `chat/directory` (cùng nguồn khung chat), cache theo employee_id; lỗi/thiếu ảnh ⇒ vòng tròn chữ cái.
- Kiểm (Playwright, cổng 3002, /assign/tasks → panel nhiệm vụ → tab Bình luận): gõ `@tuan` ra 8 người có ảnh thật, tìm không dấu OK.
- Trạng thái: sửa xong ở worktree gop_db, chưa commit.
- [x] 2026-11-18 Cho @ cả cộng tác viên (user chốt): `store.employees` ở /assign đã loại phòng CTV (`isNotCooperationOperation` ở store/actions.js) nên Nguyễn Mạnh Cường (CTV.01, phòng CTV_NV) không ra. Nguồn gợi ý đổi sang `chat/directory` (mọi NV đang hoạt động, có ảnh, ≤20 dòng, chống kết quả cũ về muộn); API lỗi ⇒ lọc tạm trên store. Không đụng quy tắc loại CTV của store.
- Kiểm (Playwright, 3002): gõ `@nguyen manh cuong` ra đúng "Nguyễn Mạnh Cường - CTV_NV - CTV.01" có ảnh, Enter chèn chip.
- Trạng thái: commit 9c9da3946 (bản đầu) đã deploy prod 18/11; bản bổ sung CTV mới sửa ở worktree gop_db, CHƯA commit/deploy.

## Thông báo @ trong bình luận — nhiệm vụ + vấn đề (2026-11-19)
- Hiện trạng đã rà (TaskCommentController / IssueCommentController, cùng khuôn): bình luận gốc báo người tạo/làm/duyệt/theo dõi (vấn đề thêm người hỗ trợ); trả lời báo tác giả bình luận cha; @ báo người được nhắc; react báo tác giả.
- Lỗi: BE tìm người được @ theo TÊN (`where fullname = … ->first()`) ⇒ trùng tên báo nhầm (Nguyễn Mạnh Cường có hồ sơ đã nghỉ + CTV.01); người vừa có vai trò vừa được @ nhận 2 thông báo.
- [x] 2026-11-19 BE: trait `Concerns/ResolvesCommentMentions` (dùng chung 2 controller): FE gửi `has_mention_ids=1` + `mention_ids[]` (employees.id) ⇒ chỉ tin id khớp tên trong `@[Tên]` + hồ sơ status=1; client cũ/app không gửi ⇒ tìm theo tên nhưng chỉ hồ sơ đang hoạt động và khớp đúng 1 người.
- [x] 2026-11-19 BE: người được @ không nhận thêm thông báo vai trò "Người bình luận" cho cùng bình luận (ưu tiên "nhắc đến").
- [x] 2026-11-19 FE `CommentEditor.vue`: chip @ mang `data-id`, submit gửi `mention_ids[]`.
- Kiểm (local, API :8003 + FE :3002): nhiệm vụ 1691 gửi qua UI ⇒ `task_comment_mention` vào đúng hồ sơ 2247 (CTV.01), không vào 1635 (đã nghỉ); vấn đề 161 qua curl 3 ca (có id / client cũ / id giả) đúng như thiết kế.
- Trạng thái: sửa ở worktree gop_db (api + client), CHƯA commit, CHƯA deploy prod.
- Chưa làm: phần trả lời bình luận chỉ báo tác giả cha (không báo vai trò) — giữ nguyên, chưa có yêu cầu đổi.

## App TPE_APP — gửi mã người được @ (2026-11-19)
- Hiện trạng: app tự có gợi ý @ ở `ui/task/task_comments_page.dart` (dùng chung nhiệm vụ + vấn đề), nguồn `meeting/getListEmployee` (status=1, KHÔNG loại CTV, `id` = employees.id), chèn `@[Tên]` và gửi `comment` + `parent_id`, không có mã người.
- [x] 2026-11-19 `_pickMention` lưu tên → employees.id; `_mentionIdsFor(text)` chỉ trả mã khi MỌI `@[Tên]` trong nội dung đều có mã (gõ tay / bản nháp khôi phục thiếu mã ⇒ null ⇒ không gửi cờ ⇒ BE tìm theo tên như bản cũ, không mất thông báo).
- [x] 2026-11-19 `_OutboxItem` giữ `mentionIds` ⇒ gửi lại khi lỗi mạng vẫn đủ mã; `createTaskComment(mentionIds:)` gửi `has_mention_ids=1` + từng dòng `mention_ids[]`.
- Kiểm: `dart analyze` 2 file sạch. CHƯA chạy thử trên simulator iOS/Android (chưa được yêu cầu test).
- Trạng thái: sửa ở `TPE_APP` nhánh `feature/app-phe-duyet` (nhánh này đang có sẵn file sửa dở khác, không phải của việc này), CHƯA commit.

## Kiểm lại tổng thể (2026-11-19)
- API nhiệm vụ 1691 (7 ca, định dạng giống app gửi): @ CTV + @ người làm ⇒ người làm chỉ nhận "nhắc đến" (không thêm "Người bình luận"), người tạo vẫn nhận vai trò; có cờ nhưng không @ ⇒ không báo ai; trả lời + @ ⇒ chỉ báo người được @; id không khớp tên ⇒ bỏ; @ trùng + id lặp ⇒ 1 thông báo; không cờ (app cũ) ⇒ tìm theo tên hồ sơ đang hoạt động; tự @ mình ⇒ không báo. Tất cả đúng.
- API vấn đề 161 (3 ca) + giao diện web vấn đề (gõ "@Đào Thị", Tab chọn): gửi `mention_ids=34` + cờ, 200, thông báo `issue_comment_mention` vào đúng người, console 0 lỗi.
- App: `dart analyze` sạch; kiểm bằng Dart thật (package dio của app) — form gửi đúng `has_mention_ids=1` + từng dòng `mention_ids[]`, tên lặp chỉ 1 mã, thiếu mã cho 1 tên ⇒ không gửi cờ.
- Local: chạy RIÊNG migration `2026_11_23_000001_issue_v2_resolution_text_and_extension_requests` (DB local thiếu bảng issue_extension_requests ⇒ mở chi tiết vấn đề 500, không liên quan code @). Còn 25 migration khác chưa chạy (của việc khác).
- CHƯA test trên simulator iOS / emulator Android: simulator iPhone 15 Pro đang do phiên Claude khác giữ (flutter run từ 18/11 17:21, log run.log của phiên b97fc1ff) — không chạm để khỏi phá việc đang chạy.

## Test app trên máy ảo (2026-11-19, user cho dùng lại simulator)
- iOS iPhone 15 Pro (hot restart phiên `flutter run` có sẵn, API :8003, TK DNS Admin) — nhiệm vụ 1691, step.sh 41–51, 0 lỗi Flutter, API toàn 2xx:
  - chọn gợi ý `@nguyen manh cuong` ⇒ app ra đúng CTV.01 (không loại CTV); chọn `@nguyen anh tuan` ra 2 người trùng tên, chọn 12510545 ⇒ thông báo "nhắc đến" vào ĐÚNG 12510545 (12010287 không nhận) + CTV.01; người làm/người giao nhận thông báo vai trò.
  - gõ tay `@[Nguyễn Mạnh Cường]` không chọn gợi ý ⇒ không có mã ⇒ BE tìm theo tên ⇒ vẫn báo CTV.01.
- Android emulator Pixel_4_API_29 (build mới `flutter run -d emulator-5554`, `adb reverse tcp:8003`, TK Đào Thị Thúy — người giao): chọn 12010287 (người còn lại của cặp trùng tên) ⇒ thông báo vào ĐÚNG 12010287; người gửi không tự nhận; người làm nhận thông báo vai trò. 0 lỗi Flutter.
- Chưa thử: gửi lại bình luận khi mất mạng, bấm gửi 2 lần liên tiếp, bình luận của VẤN ĐỀ trên app (cùng màn `task_comments_page.dart`, tham số `resource`), tài khoản không quyền.
