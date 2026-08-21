# PLAN — PL8: Thông tin hệ thống ở màn Xem chi tiết (#10814)

Nhánh: `tpe-develop-assign` (hrm-api + hrm-client) · Spec: `docs/superpowers/specs/2026-08-06-pl8-thong-tin-he-thong-design.md`

## Phase 1 — Màn mẫu: Báo giá

### BE
- [x] Tạo `Modules/Assign/Services/SystemLogService.php` + adapter `quotation` (đọc `quotation_histories`, map DTO chuẩn, kèm actor_code/department_name)
- [x] Tạo `Modules/Assign/Http/Controllers/Api/V1/SystemLogController.php`
- [x] Thêm route `GET /assign/system-logs/{type}/{id}` (nhóm `auth:api`)
- [x] `php -l` + gọi thử endpoint với 1 báo giá có lịch sử

### FE
- [x] Tạo `components/assign/SystemInfoSection.vue` (thu gọn mặc định, lazy load, timeline kiểu TaskHistoryModal)
- [x] Nhúng vào `pages/assign/quotations/_id/index.vue` (cuối nội dung, trước footer-bar)
- [x] Rà action màn danh sách báo giá vs footer chi tiết → bổ sung nút thiếu
- [x] Đổi tiêu đề phân vùng "Thông tin hệ thống" → "Lịch sử" (theo yêu cầu user)

## Phase 2 — 5 trang chi tiết còn lại
- [x] ~~Migration `assign_entity_logs`~~ → BỎ: đối tượng chưa có bảng log thì dựng log từ cột audit sẵn có (created_by/updated_by/approved_by/closed_by), không thêm bảng mới
- [x] Adapter: `bom-list`, `handover`, `prospective-project`, `meeting`, `request-solution`
- [x] Nhúng component vào 5 màn + `handover/_id/receive.vue` (thay `HandoverTimeline` luôn-hiện)
- [x] Chuẩn hoá mã phiếu đứng đầu tiêu đề 5 màn
- [x] Bỏ nút "Lịch sử" ở footer màn chi tiết Báo giá + BOM (đã có phân vùng dưới trang)

## Phase 3 — 3 màn xem chi tiết dạng modal
- [x] Adapter `task`, `issue`, `project-item`
- [x] Nhúng component vào `CreateTaskModal`, `CreateIssueModal`, `AddProjectItemModal` (chỉ khi đã có id)
- [x] Mã task/issue đứng đầu tiêu đề modal

### Checkpoint — 2026-08-06 (Phase 2+3)
Vừa hoàn thành: nhân bản phân vùng Lịch sử ra 8 đối tượng còn lại.
- BE: `SystemLogService` viết lại theo kiến trúc row-chuẩn → `finalize()` (batch load nhân viên + phòng ban, sort mới→cũ). 9 adapter: quotation, bom-list, handover, prospective-project, request-solution, meeting, project-item, task, issue. Task/Issue tự diff snapshot JSON ở BE (port từ `TaskHistoryModal.vue`).
- FE: nhúng `SystemInfoSection` vào bom-list/_id, handover/_id (index + receive), prospective-projects/_id, request-solution/_id, meeting/_id/show, CreateTaskModal, CreateIssueModal, AddProjectItemModal.
- Verify: chạy thử 8 adapter bằng script bootstrap Laravel (PHP 7.4) → đều trả đúng người/phòng ban/thời gian/diff trạng thái. `handovers` và `issues` đang 0 bản ghi trong DB local nên chưa có dữ liệu thật để xem.
Bước tiếp theo: user xem UI 8 màn → phản hồi.

### Checkpoint — 2026-08-06 (Playwright verify Phase 2+3)
Đã test thật trên :3000 (namdangit@gmail.com), 7 màn có dữ liệu đều đạt:
- BOM 52 → tiêu đề `BOM-2026-00052 — Chi tiết BOM List`, 1 dòng "Tạo mới"
- Dự án TKT 101 → `ND.2026.CON2 — …`, 2 dòng (Chỉnh sửa gần nhất / Tạo dự án)
- YCGP 11 → `TPE.YCP.TC.26.0011 — …`, 2 dòng
- Meeting 15 (`/assign/meeting/15/show`) → `TPE.MET.NB.26.0014 — Chi tiết meeting`, 1 dòng
- Modal Task → header `TPE.TASK.NB.26.0004 — Chi tiết Task`, 6 dòng, diff trạng thái đỏ→xanh (ảnh preview-task-modal.png)
- Modal Hạng mục dự án → 1 dòng, đúng người + phòng ban
- Báo giá 221 → footer còn `Quay lại / Xuất Excel / In / Sao chép` (đã bỏ nút Lịch sử), phân vùng 5 dòng
API: issue/handover trả 200 + 0 dòng (DB local chưa có bản ghi); type sai → 400 "Loại đối tượng không hợp lệ".
Console: không lỗi mới do feature. Lỗi có sẵn trên nhánh (KHÔNG phải do task này): `menu` undefined ở `request-solution/_id/index.vue:17`, `fields` trùng data ở `ChooseErpCustomerModal`, 404 `form-templates/find-by-criteria`.
Ghi nhận: nút "Lịch sử" ở footer màn Báo giá đã bỏ theo yêu cầu; `BomListLogModal` vẫn còn code nhưng không còn nút mở.

### Checkpoint — 2026-08-06
Vừa hoàn thành: Phase 1 (màn Báo giá) — BE `SystemLogService` + `SystemLogController` + route `GET assign/system-logs/{type}/{id}`; FE `components/assign/SystemInfoSection.vue` nhúng cuối `pages/assign/quotations/_id/index.vue`. Verify tinker: adapter quotation trả đúng DTO (mã NV, họ tên, phòng ban, thời gian, nhãn+màu hành động), type sai → lỗi "Loại đối tượng không hợp lệ".
Đang làm dở: không.
Bước tiếp theo: user build FE, xem `/assign/quotations/{id}` → duyệt UI phân vùng → nhân bản Phase 2 (5 trang chi tiết) và Phase 3 (3 modal).
Blocked: `php artisan route:list` lỗi sẵn có trên nhánh (`Modules\Decision\Http\Controllers\DecisionController` không tồn tại — controller nằm trong thư mục `V1`), không liên quan feature này.
Ghi nhận: rà action màn Báo giá — footer chi tiết đã có đủ (Sửa/Sao chép/In/Lịch sử/Xoá) + nhiều hơn danh sách (Xuất Excel, TP duyệt, BGĐ duyệt, Từ chối); không thiếu nút nào.

### Checkpoint — 2026-08-06 (Playwright verify)
Vừa hoàn thành: test thật trên `http://127.0.0.1:3000` (tài khoản namdangit@gmail.com).
- `/assign/quotations/260`: phân vùng thu gọn mặc định → bấm "Xem lịch sử" hiện 1 dòng "Tạo báo giá" đúng mã NV/tên/phòng ban. Ảnh: preview-thu-gon.png
- `/assign/quotations/221` (báo giá TỔNG, 5 log): timeline đủ Hủy chốt/Từ chối/Gửi duyệt/Tạo, diff trạng thái đỏ→xanh, ghi chú duyệt hiện khối vàng. Ảnh: preview-mo-rong.png
- Lazy load: chưa mở → 0 request; mở → 1 request 200; đóng/mở lại → không gọi thêm. Console 0 lỗi.
Bug đã fix trong lúc test: báo giá TỔNG dùng bộ trạng thái riêng → log cũ hiện số thô ("8"). Sửa `SystemLogService::quotationLogs` lấy `getStatusListByType($isSummary)` + fallback bộ còn lại → "Hết hiệu lực".
Bước tiếp theo: user duyệt UI → làm Phase 2.
