# Plan — Cho phép phân ca chi tiết chọn ngày quá khứ

## Phase 1 — Bỏ chặn ngày quá khứ
- [x] BE: bỏ rule `after_or_equal:today` của `start_at` + message `start_at.after` trong `CreateWorkShiftDetailRequest`
- [x] FE: bỏ `:disabled-date` chặn quá khứ ở ô Ngày bắt đầu, ô Ngày kết thúc chỉ còn chặn `< start_at` (`shift-detail/components/FormComponent.vue`)

### Checkpoint — 2026-08-24
Vừa hoàn thành: bỏ chặn ngày quá khứ ở cả FE và BE (áp dụng cho cả màn Thêm và Sửa vì dùng chung FormComponent + FormRequest).
Đang làm dở: không có.
Bước tiếp theo: user test chọn ngày quá khứ; nếu dùng thật cần xử lý tiếp 3 tác dụng phụ đã cảnh báo (công định mức tính live, timesheet_details không sinh lại cho ngày quá khứ, delete() chỉ xoá ngày > hôm nay).
Blocked:
