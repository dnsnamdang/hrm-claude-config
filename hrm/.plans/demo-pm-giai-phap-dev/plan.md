# Dữ liệu demo PM giải pháp trên cổng dev + rà quyền màn Quản lý giải pháp — @cuong61n

Môi trường: dev-hrm.eteksofts.com (DB `hrm_erp_test`, nhánh develop). Không có số Redmine (việc hỗ trợ demo).

## Phase 1 — Trả lời quyền truy cập (06/11/2026)
- [x] 06/11/2026 Rà ai mở được `/assign/solutions` + `/assign/solutions/{id}/manager`. Kết quả: danh sách không chặn vào màn, dữ liệu lọc theo 4 quyền "Xem danh sách làm giải pháp theo…" hoặc tham gia (PM/leader/thành viên). Nút "Quản lý giải pháp" theo `Solution::isCanManage()` (PM, người tạo, hoặc có quyền "Tiếp nhận yêu cầu làm giải pháp" + đúng phòng nhận; trạng thái Nháp/Đóng thì ẩn). Lỗ hổng: gõ thẳng URL manager thì ai cũng xem được (FE không kiểm `is_can_manage`, BE `show` không gate, chỉ chặn thành viên bị khoá) — đã báo user, CHƯA sửa, chờ chốt hướng.

## Phase 2 — Dữ liệu demo cho namdangit làm PM (06/11/2026)
- [x] 06/11/2026 Gán `solutions.pm_id = 13` (namdangit) cho 13 giải pháp có sẵn đủ trạng thái: 29 (Chờ PM duyệt), 2/15/21/27 (Đang triển khai), 4/30/37/38 (Đã duyệt GP), 3/33 (Đã duyệt giá), 23 (Chờ làm giá), 26 (Chốt GP). Đồng bộ `request_solutions.pm_id` cho 5 phiếu yêu cầu có PM trùng PM cũ (id 2, 4, 16, 20, 22). Không đụng GP 41–43 (tester 867 đang dùng).
- [x] 06/11/2026 Kiểm: đăng nhập API dev bằng namdangit → `GET assign/solutions` trả cả 13 GP với `is_can_manage = true`.
- [ ] Sau demo trả lại PM cũ — câu SQL hoàn tác:
  - solutions: 2→212, 3→149, 4→987, 15→505, 21→260, 23→76, 26→44, 27→48, 29→65, 30→66, 33→661, 37→40, 38→661
  - request_solutions: 2→212, 4→149, 16→48, 20→65, 22→661
