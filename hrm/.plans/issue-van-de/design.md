# Vấn đề (Issue) — Đổi tên, chuẩn hoá quy trình 3 bước, liên kết Dự án / Meeting / Phòng ban

- **Redmine**: #11290 — `[PL8 - Giao việc & Bàn giao, Issue]`
- **Nhánh**: `tpe` (client :3005 · api :8005)
- **Phụ trách**: @cuong61n
- **Spec chi tiết**: `docs/superpowers/specs/2026-09-12-issue-van-de-design.md`

## Mục tiêu

1. Đổi toàn bộ nhãn hiển thị `Issue` → `Vấn đề` trên giao diện.
2. Chuẩn hoá quy trình 3 bước: Phát hiện → Xử lý → Báo cáo.
3. Cho phép Vấn đề gắn với Dự án, Meeting, hoặc chỉ nội bộ Phòng ban.

## Chia phase

| Phase | Nội dung | Trạng thái |
| --- | --- | --- |
| 1 | Đổi tên `Issue` → `Vấn đề` + Bước 1 (Bộ phận xử lý, Vấn đề phòng ban) | Đang làm |
| 2 | Bước 2 — nút "Giao nhiệm vụ" ở chi tiết Vấn đề (tạo Task liên kết) | Chưa làm |
| 3 | Bước 3 — Báo cáo kết quả xử lý + chọn người nhận báo cáo | Chưa làm |
| 4 | Tab "Vấn đề" riêng của Dự án (song song tab Vấn đề giải pháp) | Chưa làm |
| 5 | Icon "Giao Vấn đề" ở bảng Nội dung công việc khác trong Biên bản họp | Chưa làm |

## Quyết định đã chốt

- **Chỉ chọn Bộ phận, không chọn người xử lý** → `assignee_id` để TRỐNG, Vấn đề ở trạng thái `new`,
  bắn thông báo cho Trưởng bộ phận (`parts.part_lead_id` nếu chọn tới Bộ phận, ngược lại
  `departments.department_lead_id`). Trưởng bộ phận phân công sau. (chốt 2026-09-12)
- **Phân loại Vấn đề suy ra từ dữ liệu sẵn có**, KHÔNG thêm cột `issue_scope`:
  có `solution_id` → Vấn đề giải pháp · chỉ `project_id` → Vấn đề dự án · không có cả 2 → Vấn đề phòng ban.
  (chốt 2026-09-12)
- **`project_id` / `solution_id` chuyển sang nullable ngay Phase 1** để tạo được Vấn đề nội bộ phòng ban.
  (chốt 2026-09-12)
- **Icon "Giao Vấn đề" ở biên bản họp LƯU liên kết ngược** `meeting_id` + `meeting_report_id` để tránh
  tạo trùng và truy được nguồn gốc. (chốt 2026-09-12 — làm ở Phase 5)
- **4 quyền nhóm `Issue` chỉ đổi `display_name` + `group`, GIỮ NGUYÊN `name`** (`Xem danh sách issue
  theo tổng công ty|công ty|phòng ban|bộ phận`). Lý do: `name` là khoá check ở
  `IssueService.php:122,171,177,185` và `pages/assign/issues/index.vue:716-719`, đồng thời đã lưu trong
  `role_has_permissions` — đổi `name` là mọi role mất quyền. Màn phân quyền hiển thị bằng
  `display_name` (`components/setting/Permission.vue:47`) nên user vẫn thấy đúng chữ mới. (chốt 2026-09-12)
- **KHÔNG đổi** route `/assign/issues`, tên bảng, tên biến/component, class CSS — đổi là vỡ link đã chia
  sẻ mà không được gì.
