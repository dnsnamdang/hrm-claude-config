# Bỏ bắt buộc Thông tin nhân viên — QĐ giải thể phòng ban

Yêu cầu: phòng ban không có nhân viên vẫn giải thể được → màn thêm/sửa QĐ giải thể không được bắt buộc phần "Thông tin nhân viên".

## Phase 1 — Kiểm tra & sửa

### Khảo sát

- [x] Tái hiện trên UI (Playwright): chọn phòng ban không có nhân viên → Lưu / Sửa đều thành công (BE + FE không chặn cứng)
- [x] Xác nhận BE: `DepartmentDissolutionRequest` không require `employee_infos`; `store()` đã bọc `if ($employee_infos)`; flow duyệt (`syncLockDepartment`) không phụ thuộc nhân viên

### FE

- [x] `pages/decision/department-dissolution/components/FormComponent.vue` — bỏ `<Required />` ở label "Thông tin nhân viên" (dùng chung cho add / edit / show / approve)

### Kiểm thử

- [x] Tạo QĐ giải thể PHÒNG KẾ TOÁN TÀI VỤ (0 nhân viên) → lưu thành công
- [x] Sửa QĐ đó → lưu thành công
- [x] Xoá bản ghi test sau khi kiểm thử

### Checkpoint — 2026-07-03

Vừa hoàn thành: bỏ dấu bắt buộc "Thông tin nhân viên" + verify e2e cả add/edit với phòng ban 0 nhân viên
Đang làm dở: (không)
Bước tiếp theo: (hoàn thành — chờ user kiểm tra lại trên UI)
Blocked:

Ghi chú: validate từng dòng (Phương án xử lý, Thời gian xử lý) khi phòng ban CÓ nhân viên vẫn giữ nguyên là bắt buộc.
