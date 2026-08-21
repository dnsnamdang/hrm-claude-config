# Fix: Link Phiếu công tác (PCT) ở màn Timekeeper trỏ nhầm sang PGV

**Owner:** @junfoke
**Màn:** /timesheet/timekeeping/timekeeper — cột "Ca/Phiếu"

## Bug
Click link `PCT-xxxxx` (job_type_enum = `business_trip`) điều hướng sang màn PGV
(`/timesheet/jobassignment/{id}`) thay vì màn Phiếu công tác.

## Nguyên nhân
`pages/timesheet/timekeeping/timekeeper/index.vue` — nhánh `v-if="item.job_type_enum == 'business_trip'"`
dùng cùng href `/timesheet/jobassignment/${item.job_id}` như nhánh `jobassignment`.
Route đúng của phiếu công tác là `/timesheet/business_trip_assigns/add/${id}` (theo `business_trip_assigns/index.vue` redirectToUrl).

## Task
- [x] Sửa href nhánh `business_trip` → `/timesheet/business_trip_assigns/add/${item.job_id}`
