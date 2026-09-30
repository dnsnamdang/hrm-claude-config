# Plan — Tối ưu hiệu năng API dự án tiền khả thi (getAll / index / getForMeeting)

> Nhánh: **`tpe`** — code sửa ở worktree `HRM/worktrees/tpe-api` (đã hoàn tác thay đổi lỡ làm ở `hrm-api`/`tpe-develop-assign`).

## Phase 1 — BE: gỡ N+1 ở ProspectiveProjectResource
- [x] `getAll()`: eager load 12 quan hệ Resource đang đọc từng dòng (hằng `RESOURCE_EAGER_RELATIONS`)
- [x] `getAll()`: `withCount('children')` + `canDelete()` đọc `children_count` thay cho `exists(parent_id)` mỗi dòng
- [x] `getAll()`: addSelect `is_in_permission_scope` (như `index()`) để `canEdit()` không chạy lại kiểm tra quyền từng dòng
- [x] Resource: cache `Employee`/`EmployeeInfo`/`Department` theo request + ưu tiên quan hệ đã eager load
- [x] Thêm relation `ProspectiveProject::solutionEmployee()` để eager load được
- [x] Áp cùng bộ eager load cho `index()` và `getForMeeting()`
- [x] Đối chiếu JSON trước/sau (3 mức quyền: tổng công ty / phòng ban / không quyền): `getAll` và `index` giống hệt từng byte; `getForMeeting` chỉ thêm `children_count` (null → 0)

### Checkpoint — 2026-09-14
Vừa hoàn thành: Phase 1 (BE). Đo local 260 dòng, `per_page=10000`:
- `getAll`: 4.892 query / 2,12s → **81 query / 0,25s**
- `index`: 3.421 query / 1,25s → **81 query / 0,16s**
- `getForMeeting`: 280 query / 0,11s → **31 query / 0,06s**
Đang làm dở: không
Đã kiểm: 7 endpoint qua HTTP đều 200, JSON trước/sau giống hệt (trừ `children_count` null→0); màn danh sách chạy trên UI, 0 lỗi console.
Bước tiếp theo: (tuỳ user) Phase 2 — thêm chế độ `light=1` trả gọn cho ~20 màn FE đang gọi `getAll?per_page=10000` chỉ để đổ dropdown (payload hiện ~1MB / 260 dòng).
Blocked: không
