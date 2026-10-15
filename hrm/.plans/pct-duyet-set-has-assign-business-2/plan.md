# PCT: tạo=chưa duyệt(2), duyệt=đã duyệt(1) → ERP gate nhập KQ (Cách 1b, không backfill)

## has_assign_business (wr_assign_tasks, ERP qua mysql2)
0 = chưa có PCT | 1 = PCT đã duyệt (giữ nghĩa cũ) | 2 = PCT chưa duyệt (mới)

## Đã sửa (hrm-api Module Assign, php -l sạch)
- [x] TpWrAssignTask (Assign): PCT_DA_DUYET=1, PCT_CHUA_DUYET=2.
- [x] AssignRequest::syncWrAssignTask (tạo/sửa PCT): set has_assign_business = PCT_CHUA_DUYET(2) (trước là 1).
- [x] AssignBusinessController@store (duyệt PCT, status_request==3): loop assignBusinessTasks → set PCT_DA_DUYET(1).
- [x] TpWrAssignTaskService filter "đang giao": whereIn [PCT_DA_DUYET(1), PCT_CHUA_DUYET(2)].
- [ ] Rà luồng duyệt PCT khác (update() status_request==3 nếu có) — set =1 tương tự khi test.

## KHÔNG cần backfill prod (giữ nghĩa =1). 
## Lưu ý: dữ liệu cũ =1 (kể cả PCT đang-tạo cũ) sẽ được coi là "đã duyệt" → chấp nhận theo Cách 1b.
## Branch: (nhánh Assign đang làm)
