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
