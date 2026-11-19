# Xuất Excel — Danh mục tài khoản nhân viên (`/human/employee`)

> Người phụ trách: @khoipv — Bắt đầu 29/10/2026
> Design: [design.md](design.md) · Spec: [docs/superpowers/specs/2026-10-29-xuat-excel-tai-khoan-nhan-vien-design.md](../../docs/superpowers/specs/2026-10-29-xuat-excel-tai-khoan-nhan-vien-design.md)
> Tham khảo: xuất Excel màn Hồ sơ nhân sự (`/human/employee_info`, `getEmployeeByField` + `EmployeeInfoExport` + `export-modal`)

## Yêu cầu
- Nút "Xuất excel" ở màn danh sách tài khoản → mở popup chọn trường (giống HSNS) → tải file `.xls`.
- Xuất theo bộ lọc đang áp dụng (công ty kê khai trong tài khoản, phòng ban, nhóm quyền, trạng thái, email, SĐT), không phân trang.
- Quyền: như màn danh sách — `Quản lý tài khoản nhân viên`.

## Trường xuất
1 Mã nhân viên · 2 Tên nhân viên · 3 Email · 4 SĐT công ty · 5 Công ty (kê khai trong tài khoản) · 6 Phòng ban (nhóm quyền là phòng ban — như cột bảng) · 7 Vị trí công việc · 8 Ngày tạo · 9 Ngày cập nhật · 10 Trạng thái

## Phase 1 — BE
- [x] Route `GET /human/employee/export` (đặt trước `/{id}`)
- [x] `EmployeeController::export` — dùng `EmployeeService::getEmployees` với limit lớn, map dữ liệu
- [x] `app/ExcelExport/EmployeeAccountExport.php` + blade `exports/employee_account_report.blade.php`

## Phase 2 — FE
- [x] `pages/human/employee/index.vue`: nút Xuất excel + `export-modal` + `exportExcel()` (gửi formFilter, map company → account_company_id)

## Fix
- [x] Xuất báo 403 "Không có quyền": `exportExcel()` gọi `$axios` thô không gắn token (chỉ action `apiGet` gắn) → BE không nhận ra user → 403. Sửa: gắn `Authorization: Bearer <access_token>` vào header như màn gói thầu (`pages/bid_package/bid_package/index.vue`). Màn HSNS không lỗi vì API `getEmployeeByField` không check quyền.

## Kiểm tra
- [x] `php -l` controller + export class OK, route `api/v1/human/employee/export` đã đăng ký
- [x] Chạy thử local (bỏ qua check quyền): 112 tài khoản đang hoạt động, file .xls đọc lại đủ 10 cột, SĐT giữ số 0 đầu
- [x] User test trên UI (build client) — OK 29/10/2026

### Checkpoint — 29/10/2026 (wrap up)
Vừa hoàn thành: BE `EmployeeController::export` + `EmployeeAccountExport` + blade `employee_account_report`; FE nút Xuất excel + export-modal ở `pages/human/employee/index.vue`; fix 403 (gắn Bearer token khi tải file)
Đang làm dở: —
Bước tiếp theo: — (đã commit + push `master` 29/10: API 7d1c7b29, Client 02ff6824)
Blocked:
Treo (chưa làm, chờ user quyết): API xuất HSNS `getEmployeeByField` không check quyền — gọi không token vẫn tải được danh sách nhân sự
