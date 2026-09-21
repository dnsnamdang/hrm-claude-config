# Design — Liên kết Nhiệm vụ với Dự án, Meeting, Phòng ban (#11456)

Redmine: http://quanly.dnsmedia.vn/issues/11456 — @cuong61n
Nhánh: `tpe-develop-assign` (hrm-api + hrm-client)
Spec chi tiết: `docs/superpowers/specs/2026-09-18-task-lien-ket-nhiem-vu-design.md`
Phụ thuộc: #11453 (`.plans/task-nhiem-vu/`) — đã có `task_type` / `batch_id`.

## Mục tiêu

1. **Dự án**: chi tiết dự án TKT có tab "Nhiệm vụ" = task theo `project_id`; ẩn tab "Nhiệm vụ giải pháp".
2. **Meeting**: chi tiết meeting có tab "Nhiệm vụ"; bảng biên bản mỗi dòng có icon "Giao nhiệm vụ" mở popup tạo task điền sẵn.
3. **Phòng ban**: bỏ bắt buộc dự án / giải pháp / hạng mục / meeting → tạo được nhiệm vụ nội bộ; link động chỉ cho chọn nơi mình là thành viên.
4. Nhiệm vụ gắn với **Vấn đề**: KHÔNG làm (Mr Nam pending 17/09).

## Quyết định đã chốt (18/09/2026)

| Vấn đề | Chốt |
|---|---|
| Lưu liên kết meeting | Cột `tasks.meeting_id` (1-1), không pivot |
| Dòng biên bản đã giao | Lưu `tasks.meeting_report_id` + badge "Đã giao N nhiệm vụ", vẫn cho giao thêm |
| Người thực hiện ngoài công ty | Chỉ kế thừa người có `employee_id` |
| Icon Giao nhiệm vụ | Chỉ màn Chi tiết meeting |
| Tab Nhiệm vụ ở chi tiết Dự án | Lọc `project_id` (gồm cả task giải pháp thuộc dự án) + thêm cột Giải pháp |
| Link động | Áp cho tất cả, kể cả admin |
| 3 bản `TasksTab` cũ | Không refactor; tạo component chung mới `TaskListTab.vue` cho 2 chỗ mới |

## Giải pháp kỹ thuật

- `tasks`: `solution_id` NOT NULL → nullable; thêm `meeting_id`, `meeting_report_id` (nullable + index).
- BE: bỏ required ở `TaskStoreRequest`/`TaskUpdateRequest`; `index()` thêm filter `meeting_id`;
  **phân quyền không đổi** (nhiệm vụ phòng ban lộ diện qua Tầng 1 vai trò cá nhân + Tầng 3 `task_org_units`).
- Link động: param `mine=1` cho `prospective-projects/getAll`, `solutions/getAll`, `meetings/getAll`,
  dùng lại `getMySolutionIds()` / `getMyProjectIds()` của `TaskService`; luôn giữ ngoại lệ `&id=` để giá trị đang chọn không mất.
- FE: component chung `components/assign/task/TaskListTab.vue` nhận `scope` (`project_id` | `meeting_id`),
  dùng ở tab Nhiệm vụ của chi tiết dự án và chi tiết meeting.

## Ngoài phạm vi (đã báo, chưa làm)
- `getProjectOptions` / `getSolutionOptions` còn `per_page=10000`.
- Nhiệm vụ gắn với Vấn đề (Issue).

## Cần user quyết (phát hiện khi kiểm thử 18/09)

1. **Hạn dự kiến trong quá khứ**: biên bản cũ có "Hạn dự kiến" đã qua; kế thừa sang nhiệm vụ thì rule
   "Không được là ngày trong quá khứ" chặn lưu, user phải tự sửa ngày. Chọn: (a) giữ nguyên như hiện tại,
   (b) không kế thừa khi hạn đã qua (để trống), hay (c) kế thừa nhưng đẩy về hôm nay.
2. **Link động áp cho cả admin**: đúng chốt 18/09, nhưng hệ quả là DNS Admin không chọn được giải pháp nào
   ở form Tạo nhiệm vụ (không là thành viên giải pháp). Lối tạo nhiệm vụ cho giải pháp vẫn còn qua tab
   Nhiệm vụ trong màn Giải pháp (giá trị khoá sẵn). Có muốn mở ngoại lệ cho quyền "xem toàn công ty" không?

## Lỗi có sẵn phát hiện khi kiểm thử (đã sửa, ngoài phạm vi task)

- `getMyProjectIds()` luôn rỗng vì đọc cột `prospective_project_id` không bao giờ được ghi (164/164 dòng = 0).
  Ảnh hưởng cả Tầng 2 phân quyền xem danh sách Nhiệm vụ — thành viên phòng ban hỗ trợ dự án không thấy
  nhiệm vụ của dự án mình. Đã sửa bằng join qua `prospective_project_support_departments`.
- Migration `2026_09_15_000002_add_lifecycle_to_solution_members` chưa chạy trên DB dev `hrm_prod_6_6` làm
  `GET assign/solutions/{id}` trả 500. Đã chạy migration đó để test tiếp (không phải thay đổi của task này).

## Quyết định UI bộ lọc tab Nhiệm vụ (18/09/2026)

| Vấn đề | Chốt |
|---|---|
| Nhãn floating bị cắt cụt khi ô có giá trị | `.advanced-filters { overflow: visible }` trong `<style scoped>` (V2BaseFilterPanel để `overflow: hidden` cho animation thu gọn; KHÔNG dùng `!important` để animation vẫn clip đúng) |
| Khoảng cách giữa 2 hàng ô lọc | **`row-gap: 7px`** — user chốt 18/09: phải bằng khoảng cách "ô tìm nhanh → hàng lọc đầu". **Khác màn mẫu `prospective-projects` (18px)** — nếu sau này muốn đồng bộ thì đổi cả màn mẫu + skill, đừng sửa ngược riêng tab này |
| Cách khai khoảng cách | Dùng `row-gap` trên `.filter-grid`, KHÔNG dùng `mb-2` trên từng ô |
