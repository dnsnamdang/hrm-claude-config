# Plan — Báo cáo meeting nhân viên theo thời gian (Redmine #11145)

Nhánh: `task_11145` (tách từ `tpe`) ở cả `hrm-api` và `hrm-client`.

## Phase 1 — BE: lọc trạng thái theo mốc thời gian (AC2, AC3)

- [x] `Meeting`: hằng `PAST_REPORT_STATUSES` = [Hoàn thành, Hủy], `FUTURE_REPORT_STATUSES` = [Chốt lịch]
- [x] `MeetingByEmployeesService::getFilteredQuery()` thay `whereIn(REPORT_STATUSES)` bằng điều kiện
      theo từng meeting: `(start_date <= now AND status IN past) OR (start_date > now AND status IN future)`
- [x] Rà lại MỌI chỗ khác trong service còn dùng `REPORT_STATUSES` (`getTotalMeetings`,
      `getMeetingsByType`, `getMeetingsByMode`, `getParticipantsByScope`, `getChartData`) — 2 số liệu lệch nhau là lỗi
- [x] Meeting `Hủy` không cộng thời lượng: `formatMeetingData()` trả `duration = 0`, và các hàm
      `calculateMeetingStatistics*` bỏ qua khi cộng tổng phút
- [x] Thêm đếm riêng số meeting `Hủy` cho từng cấp (công ty / phòng ban / nhân viên)

## Phase 2 — BE: 2 cột mới (AC4)

- [x] `formatMeetingData()` trả thêm `content` + `conclusion`
- [x] Kiểm `MeetingByEmployeesResource` có nuốt field mới không

## Phase 3 — FE: đổi tên + bộ lọc + 2 cột (AC1, AC4)

- [x] Đổi chữ ở 5 chỗ: menu `menu-sidebar.js`, tiêu đề trang, tiêu đề card bộ lọc, tiêu đề bảng, màn In
- [x] ~~Thêm ô lọc Phòng ban + Bộ phận~~ — KHÔNG PHẢI LÀM: `V2BaseCompanyDepartmentFilter` đã có sẵn
      đủ Công ty / Phòng ban / Bộ phận / Nhân viên. Khảo sát ban đầu đọc sót.
- [x] Bảng chi tiết: 2 cột `Nội dung meeting` + `Kết luận cuộc họp` ở dòng meeting, cắt gọn + tooltip
      (`conclusion` là longtext, đổ nguyên văn là tràn bảng)
- [x] Chip `Hủy` ở các dòng tổng hợp

## Phase 4 — FE: cấu hình cột khi In (AC5)

- [x] Nối `components/modal/column-customization-modal.vue` vào luồng In
- [x] `print.vue` nhận danh sách cột đã chọn và chỉ render đúng các cột đó

## Phase 5 — Verify

- [x] AC1-AC5 trên môi trường local (FE :3005 → API :8002 → DB `hrm_prod_30_3_26`)

## Checkpoint — 2026-09-12

Vừa hoàn thành: **XONG toàn bộ, verify AC1-AC5 trên giao diện thật** (FE :3005 → API :8002 → DB `hrm_prod_30_3_26`).

- AC1: tiêu đề trang / menu / card bộ lọc / bảng / màn In đều đổi; tên quyền + URL giữ nguyên
- AC2: lọc tháng 7/2026 → 26 meeting (22 Hoàn thành + 4 Hủy); 15 meeting Chốt lịch đã quá giờ bị loại
- AC3: tạm đẩy 2 meeting sang tương lai → chỉ meeting Chốt lịch lọt, meeting Lên lịch bị loại (đã trả lại giờ gốc)
- AC4: 2 cột mới hiện đúng ở dòng meeting, cắt gọn 2 dòng + tooltip
- AC5: popup chọn cột mở khi bấm In; bỏ 3 cột → tab in ra đúng 11 cột còn lại, colspan nhóm co theo
- Meeting Hủy: chip "Hủy" trên dòng, **0 phút**, dòng tổng ghi "Số meeting: 12 • Hủy: 2"

Bẫy gặp phải (ghi lại để lần sau khỏi mất công):
- `MeetingByEmployeesResource` **lọc trắng danh sách khoá** → `cancelled_count` phải khai thêm mới ra tới FE
- Component chọn cột dùng chung khai `b-form-checkbox :value="column.key"` → `isVisible` phải bằng
  CHÍNH `key` (không phải `true`), nếu không ô tick hiện ra rỗng dù cột đang bật

Còn lại: commit 2 repo, cập nhật Redmine #11145.
Blocked: 
