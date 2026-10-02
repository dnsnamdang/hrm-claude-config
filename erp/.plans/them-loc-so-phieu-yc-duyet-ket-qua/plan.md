# Thêm ô lọc "Số phiếu yêu cầu" — Danh sách phiếu duyệt kết quả

**Người phụ trách:** @junfoke — Repo `TanPhatDev`, màn `/admin/customer-care/wr_approve_results`

## Bối cảnh
QA báo bộ lọc màn "Danh sách phiếu duyệt kết quả" thiếu ô tìm theo **Số phiếu y/c**, dù bảng
có cột này. Rà code: BE `WrAssignTask::searchByFilter()` **đã có sẵn** nhánh lọc `request_code`
(dòng ~556, lọc cả `AssemblyRequest` lẫn `AssignOtherRequest`) — chỉ thiếu ô nhập ở FE.

## Task
- [x] Rà BE `app/Model/Customers/WrAssignTask.php::searchByFilter` — xác nhận đã hỗ trợ `request_code`
- [x] Thêm ô lọc vào `resources/views/customercare/wr_approve_results/index.blade.php`
      (`search_columns`, sau "Số hợp đồng"), copy đúng pattern màn phiếu giao việc
      `resources/views/customercare/warranty_repair_assign_tasks/index.blade.php:66`
- [ ] User test trên browser: nhập mã YCGVK / YC công việc khác → ra đúng phiếu

## Checkpoint — 10/09/2026
Vừa hoàn thành: thêm 1 dòng `{data: 'request_code', search_type: "text", placeholder: "Số phiếu yêu cầu"}`
vào `index.blade.php` (giữ nguyên CRLF, `git diff` đúng 1 dòng thêm). BE không phải sửa.
Bước tiếp theo: user reload màn, thử lọc.
Blocked: không
