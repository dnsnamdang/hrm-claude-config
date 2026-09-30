# Plan — Nhóm nghiệp vụ áp dụng theo nghiệp vụ

> @khoipv — trạng thái: **KHẢO SÁT + DEMO UX, CHƯA CHỐT, CHƯA SỬA DÒNG CODE NÀO**

## Phase 0 — Khảo sát (xong)

- [x] Xác định chức năng cột "Không cần duyệt" / "Không gửi duyệt theo nhóm này" = `group_permission_employees.is_leader`
- [x] Dựng lại công thức duyệt: `quyền (LOẠI phiếu) AND listManageEmployeeIdsByGroup() (NGƯỜI)`
- [x] Xác nhận `group_permissions` / `group_permission_managers` không có cột module
- [x] Đếm call site helper: **91 chỗ**, tất cả gọi trần không tham số
- [x] Kết luận: **không thể cấu hình** "1 người duyệt chỉ hợp đồng, không duyệt đơn nghỉ của cùng nhóm người" với schema hiện tại
- [x] Ghi nhận khác biệt: Báo giá / Hợp đồng có nhánh `|| created_by == self` (tự duyệt được), Đơn xin nghỉ **không có** → rủi ro phiếu kẹt

## Phase 0b — Rà độ phủ quyền theo call site thật (xong 17/09/2026)

> User hỏi: "ô tích module có bao quát hết các quyền trong phân hệ đó không?" → **KHÔNG**. Rà 91 call site / 37 file:

- [x] Đếm call site theo file: `CategoryDashboardService` 26 · `Timesheet/DashboadService` 10 · 17 file Timesheet ~27 · 14 file Category ~26 · `Training/BaseService` 1 · `Human/EmploymentContractService` 1 (bị comment) · `PermissionHelper` 2
- [x] **Phân hệ 0 call site** — `Modules/Supply` (13 quyền Cung ứng) và `Modules/Assign`: không dùng nhóm nghiệp vụ, ô tích vô nghĩa → bỏ khỏi danh sách (giữ lại dạng disabled để giải thích)
- [x] **Thiếu sót đã bổ sung** — `Modules/Training` (Đào tạo) lọc qua `BaseService.php:33`, 1 dòng chi phối ~40 service con
- [x] **Đặt lại tên** — "Giao việc" thực chất là `JobAssignmentNote` trong **Timesheet**, không phải `Modules/Assign`
- [x] **Quyền KHÔNG đi qua nhóm nghiệp vụ** (ô tích không chặn được), đã đọc từng hàm để xác nhận:
  - `Quotation::canBGDApprove()` — `BGĐ duyệt báo giá`
  - `BidPackage::canBGDApprove()` (`BidPackage.php:270`) — `BGD duyệt kết quả thầu`
  - `Attendance::canBGDApprove()` (`Attendance.php:215`) — `Ban giám đốc duyệt đơn xin nghỉ`
  - `AcceptanceReport.php:119` — `Duyệt biên bản nghiệm thu`
  - `ContractLiquidation.php:108` — `Duyệt biên bản thanh lý`
  - `Contract.php:370` — `Duyệt hợp đồng kết xuất cung ứng`
  - `Project.php:148` — nhánh `Phân công báo giá` có scope nhưng **đang bị comment**
- [x] Danh sách nghiệp vụ chốt lại **8 ô sống**: contract · quotation · bid_package · project · timesheet · business_trip · job_assignment · training
- [x] Gắn nhãn **ĐỦ** / **MỘT PHẦN** cho từng ô ngay trên màn để tránh hiểu nhầm
- [x] Cập nhật demo: thêm tab 3 "Độ phủ quyền — rà theo call site"

## Phase 1 — Demo UX (xong)

- [x] Tạo `demos/demo-nhom-nghiep-vu-theo-nghiep-vu.html` (3 tab: Cấu hình nhóm · Mô phỏng phạm vi duyệt · Ghi chú kỹ thuật)
- [x] Cập nhật `demos/README.md`

## Phase 2 — Chốt với user (chưa làm)

- [x] **Chốt cách chia: theo PHÂN HỆ của màn `timesheet/setting/roles` (cột `permissions.type`)** — chọn phân hệ nào thì áp dụng cho **tất cả quyền** trong phân hệ đó (user chốt 17/09/2026)
- [ ] Chốt: 5 phân hệ **0 call site** (2 Tính lương, 3 HCNS, 7 Cung ứng, 15 Danh mục) — ẩn hẳn hay hiện mờ?
- [ ] Chốt: phân hệ **Đào tạo không có quyền nào** trong bảng `permissions` — có seed thêm để cấu hình được không?
- [ ] Chốt: có bổ sung scope nhóm cho các quyền cấp BGĐ + biên bản nghiệm thu/thanh lý/kết xuất cung ứng không (**đổi luật nghiệp vụ**, không phải đổi cấu hình)
- [ ] Chốt: phân hệ Cung ứng có cần chia theo nhóm nghiệp vụ không (hiện 0 call site, muốn có phải thêm mới hoàn toàn)
- [ ] Chốt: phạm vi đặt ở **nhóm** (mỗi nhóm 1 bộ nghiệp vụ) hay ở **từng người duyệt trong nhóm**
- [ ] Chốt xử lý phiếu kẹt: validate cảnh báo khi lưu, hay thêm màn tra cứu "nhân viên chưa được phủ nghiệp vụ nào"
- [ ] **Xin phê duyệt sửa hàm dùng chung** `listManageEmployeeIdsByGroup` / `listManageEmployeeInfoIdsByGroup` / `listEmployeeInfoHasPermission` (91 call site)

## Phase 3 — BE (chưa làm)

- [ ] Migration bảng `group_permission_modules (group_permission_id, module)` — chỉ index, không khóa ngoại
- [ ] Entity `GroupPermissionModule` + quan hệ ở `GroupPermission`
- [ ] Migration dữ liệu: nhóm đang có → insert đủ mọi module (giữ nguyên hành vi)
- [ ] Helper nhận `$module = null` (null = hành vi cũ)
- [ ] `GroupPermissionService::store/update` lưu module; Resource trả về `modules`
- [ ] Sửa call site cần tách: `Contract.php:342,435`, `Attendance.php:149,154,161`, `PermissionHelper.php:120` (định tuyến thông báo)

## Phase 4 — FE (chưa làm)

- [ ] `group-permission/add.vue` + `_id/edit.vue`: multi-select "Áp dụng cho nghiệp vụ" (dùng `base-select2`, label kèm `<Required />`)
- [ ] `group-permission/_id/index.vue`: hiển thị chỉ-xem
- [ ] Validate FE: bắt buộc chọn ít nhất 1 nghiệp vụ

## Phase 5 — Kiểm thử (chưa làm)

- [ ] Hồi quy: sau migration dữ liệu, không ai mất quyền duyệt đang có
- [ ] Ca tách: nhóm chỉ bật Hợp đồng → duyệt được HĐ, không duyệt được đơn nghỉ
- [ ] Thông báo đi đúng người (không còn "nhận báo cần duyệt nhưng mở ra không có nút")

## Checkpoint — 2026-09-17 (lần 2)

Vừa hoàn thành: đổi ô tích sang **9 phân hệ của màn roles** (`permissions.type`) theo yêu cầu user, sửa demo (danh sách ô, schema `group_permission_types`, helper nhận **tên quyền** thay vì tên module), cập nhật design/README/STATUS. Trước đó: rà độ phủ theo 91 call site thật (Phase 0b)
Đang làm dở: không
Bước tiếp theo: user chốt Phase 2 — 3 câu (5 phân hệ 0 call site ẩn hay hiện mờ · có thêm scope cho quyền BGĐ/biên bản không · phân hệ Đào tạo có seed quyền không) + cho phép sửa hàm dùng chung
Blocked: chưa được phép sửa `PermissionHelper.php` (hàm dùng chung, 91 call site)
