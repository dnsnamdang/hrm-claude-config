# Design (tóm tắt) — Báo cáo Kết quả meeting theo thị trường

> Spec đầy đủ: `docs/superpowers/specs/2026-08-16-meeting-by-market-design.md`
> Branch: `meeting-schedule` (api + client) · @dnsnamdang · 2026-08-16

## Mục tiêu
Báo cáo **độc lập** liệt kê meeting **có gắn khách hàng**, nhóm **Thị trường (Tỉnh của KH) → Khách hàng → Meeting**, bám mockup tab 3 (`.plans/gop-db/ke-hoach-phat-trien-thi-truong/ke-hoach-phat-trien-thi-truong-mockup-meeting.html`). Tách khỏi màn Lịch meeting / Todo.

## Quyết định đã chốt
- **Vị trí:** trang mới `pages/assign/report/meeting-by-market/` (index + print + components), layout `default-sidebar`, thêm menu Báo cáo. BE: route group `assign/report/meeting-by-market` + Controller + Service riêng (không nhồi ReportController).
- **Phạm vi meeting:** chỉ meeting có `customer_id`; trạng thái Lên lịch/Chốt lịch/Hoàn thành/Hủy (bỏ Đang tạo).
- **Thị trường = Tỉnh của KH:** `meeting.customer_id → ERP customers.province_id → provinces.name` (qua `mysql2`, batch 2 connection, không join xuyên DB). KH không tỉnh → "Chưa xác định thị trường".
- **13 cột** bám mockup: Thị trường · KH · Tên meeting (link) · Loại · Thời gian · Địa điểm · Chủ trì (= `meeting.created_by`) · TP công ty(+N) · TP KH(+N) · Trạng thái · Biên bản/Lý do huỷ · Dự án TKT · Phiếu công tác/Chấm công.
- **Bộ lọc:** Kỳ + cascade Công ty→Phòng ban→Bộ phận→Nhân viên (`V2BaseCompanyDepartmentFilter`) + Thị trường + Trạng thái + Loại meeting + Xuất Excel.
- **Phân quyền fail-closed:** 3 quyền mới (tổng công ty/công ty/phòng ban) trong `PermissionsTableSeeder`; không quyền → chỉ meeting mình tạo/mình dự. FE cờ quyền mặc định `false` (KHÔNG `|| true`). Route KHÔNG chặn cứng — scoping trong service để giữ fallback "của chính mình".
- **Popup:** Biên bản từ `MeetingReport` (content/solution/proposer/executor/deadline + conclusion); Chấm công GPS từ `timesheets` (job_type=`new_business_trip`, job_id=assign_request.id).

## Phụ thuộc bắt buộc (đã chốt)
- Thêm cột `assign_requests.meeting_id` (nullable) + sửa `AssignBusinessForm.vue` & BE store để **lưu meeting_id** khi tạo phiếu công tác từ meeting. Không hồi tố phiếu cũ.

## Lưu ý
- Bug tham chiếu: `meeting-by-projects/index.vue:501-504` dùng `hasAPermission(...) || true` (fail-open) — KHÔNG copy.
- Nhánh `meeting-schedule` (không phải gop_db) → `mysql2` dùng bình thường.
