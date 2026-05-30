# Customer Development Report — Design (tóm tắt)

**Mã báo cáo:** QLDA_BC_10 — Báo cáo kết quả phát triển khách hàng theo nhân viên kinh doanh
**Người phụ trách:** @manhcuong
**Spec chi tiết:** `docs/superpowers/specs/2026-05-18-customer-development-report-design.md`

## Mục tiêu

Theo dõi hiệu quả phát triển khách hàng của từng NVKD theo 2 góc nhìn song song trong 1 kỳ báo cáo:

- **Nhóm A — Phát triển KH mới:** KH tổ chức tạo trong kỳ. Key unique = (customer_id, NVKD). NVKD = `main_sale_employee_id` của PP, hoặc `customers.created_by` nếu KH chưa có PP nào (→ "Chưa tiềm năng").
- **Nhóm B — Kết quả chăm sóc trong kỳ:** PP tạo trong kỳ. Key unique = (customer_id, main_sale_employee_id).

→ 1 KH có thể xuất hiện ở nhiều NVKD ở cả 2 nhóm, không trùng tại cùng 1 NVKD.

Bảng tổng hợp 3 cấp: Công ty → Phòng ban → Nhân viên KD. 5 bucket trạng thái x 2 nhóm + cột Số lượng tổng.

## Quyết định lớn

1. **Bảng mới `prospective_project_status_logs`** lưu lịch sử thay đổi status của ProspectiveProject. Backfill thô từ `created_at + created_by` của PP hiện có. Ghi log qua model event `updating` khi `status` đổi.
2. **Mapping bucket ↔ status:**
   - Chưa tiềm năng: KH chưa có PP (chỉ áp dụng nhóm A — nhóm B luôn = 0)
   - Đang trao đổi → status 2
   - Đang làm GP → status 3, 4, 5, 6
   - Đang thương thảo → status 7, 8
   - Đang thực hiện HĐ → status 9, 10
   - Loại khỏi báo cáo: status 1 (Đang tạo), 11 (Đóng), 12 (Kết thúc & lưu trữ)
3. **Thời điểm chốt status** = log gần nhất có `changed_at ≤ to` (ngày cuối kỳ).
4. **Ưu tiên status cao nhất** khi 1 KH/cặp có nhiều PP.
5. **NVKD:**
   - Nhóm A → `main_sale_employee_id` của PP (mỗi NVKD 1 dòng); KH không có PP → `customers.created_by`
   - Nhóm B → `prospective_projects.main_sale_employee_id`
6. **Phạm vi customer:** chỉ `customer_type = 2` (Tổ chức).
7. **Phân quyền theo cấp** dùng `checkPermissionList` + scope filter theo company/dept/part.
8. **UI:** copy style từ `pages/assign/report/solution-versions/index.vue`.
9. **Modal chi tiết:** click vào số trong bảng → popup danh sách KH/PP, cột: #, Khách hàng, NVKD, Công ty/PB/BP, Nhóm trạng thái, Dự án TKT gần nhất, #Meeting, #PP, #YCGP, #BG, #HĐ, GT HĐ.

## Bộ lọc

- Công ty / Phòng ban / Bộ phận / Nhân viên KD (cascade)
- Nhóm khách hàng (bucket)
- Lĩnh vực / Ngành hàng / Ứng dụng (cascade theo PP)
  - Nhóm A: loại KH không có PP match
  - Nhóm B: loại PP không match
- Kiểu thời gian: năm / quý / tháng / custom
- **Bỏ:** Nguồn khách hàng

## Scope

- BE: 1 migration + 1 seeder backfill + 1 model + 1 service + 1 controller + 4 route + log hook trong ProspectiveProject model
- FE: 1 trang `/assign/report/customer-development` + 1 modal danh sách + i18n menu
