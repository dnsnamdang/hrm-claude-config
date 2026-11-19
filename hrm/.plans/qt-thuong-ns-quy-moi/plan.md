# Plan: Port "Quyết toán thưởng năng suất quý (mới)" ERP → HRM

**Spec:** `.plans/qt-thuong-ns-quy-moi/design.md`
**Worktree:** `HRM/.worktrees/hrm-api-qtnsq` + `HRM/.worktrees/hrm-client-qtnsq`, nhánh `feature/qt-thuong-ns-quy-moi` (từ `origin/develop`)
**Khuôn HRM:** `bill-adjust-depts` (BE `Modules/Finance/{Entities/BillAdjustDept,Services/BillAdjustDept*,Http/Controllers/...}`; FE `pages/finance/bill-adjust-depts`)

## Trạng thái
- Bắt đầu: 2026-11-04 · Tiến độ: 6/6 code xong, đang kiểm Phase 3

## Global constraints
- Ghi bảng ERP có sẵn, không migration tạo bảng. `invoiceable_type` = `App\Model\Accounting\BillProductivitySettlementQuarter`.
- Quyền mới type 8 qua `$this->perm([...])` trong `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php`, không `id`.
- Nhãn "Người tạo"/"Ngày tạo". Số định dạng `en-US` / `number_format($x)`. Badge trạng thái do BE trả `status_text`+`status_color`.
- FE màn mới chỉ dùng `V2Base*`, popup `V2BaseModal`, confirm `$confirm`, nút trong `V2Footer`, `unsavedChangesMixin`, 4 mixin danh sách + `ColumnCustomizationModal`, filter `floating`.
- Thao tác xong quay về danh sách.

## Phase 1 — Backend

- [x] **T1 Entity + tính toán** — 3 Entity (`Modules/Finance/Entities/BillProductivitySettlementQuarter/*`), `BillProductivitySettlementQuarterCalculator` (port `calculateSettlementCombined` + `getDataAdBonusByContract*` + công thức lũy tiến/chia thưởng, hàm thuần tách riêng để test). Test unit công thức lũy tiến + chia TBP/TP.
- [x] **T2 CRUD + quyền + phạm vi + ghi sổ** — Service list/scope/show/store/update/approve/destroy (unique dept-kỳ-năm, generateCode lock, sync nhân viên & HĐ server-side), `...AccountingService` (6411/3351), FormRequest, Resource (status_text/color, is_can_edit/is_can_delete/is_can_approve), Controller, routes `checkPermission`, 4 quyền seeder, form-options (năm, kỳ theo cty, phòng/bộ phận), regulation (thang phòng). Feature test: scope, unique, approve ghi sổ ΣNợ=ΣCó, xoá chặn khi status 3.
- [x] **T3 Xuất Excel + In** — export-rows danh sách (12 cột), export chứng từ `QTTNSTQ_{code}.xlsx`, print-data (letterhead theo company của phiếu).

## Phase 2 — Frontend

- [x] **T4 Danh sách + menu** — `index.vue` (cột/lọc theo design §3, export FE `listExportFile`), link menu finance.js:375.
- [x] **T5 Form tạo/sửa + chi tiết** — `add.vue`, `_id/edit.vue`, `_id/index.vue`, `components/SettlementQuarterForm.vue`, `ContractDetailModal.vue`, `RegulationModal.vue`, bảng 2 tầng.
- [x] **T6 Bản in** — `_id/print.vue` ngang 297mm.

## Phase 3 — Kiểm
- [x] Đối chiếu ERP (bước 5) + ngang bill-adjust-depts (5b), checklist skill, Playwright: tạo → lập QT → lưu → duyệt → kiểm account_details → in/xuất → xoá. (2026-11-04 13:25, PASS — xem checkpoint)

## Phase 4 — Lịch sử
- [x] **T7 Lịch sử** (skill entity-history, khuôn `BillAdjustDeptHistoryService`) — BE `BillProductivitySettlementQuarterHistoryService` ghi `catalog_histories` (tạo/sửa/đổi trạng thái/xoá; bảng con `employee_rows` key employee_id + `attachment_rows`), khai `CatalogHistoryService::TABLES`. FE `CatalogHistoryModal` ở danh sách (menu ⋮) + `SystemInfoSection` ở chi tiết.

## Phase QA — Redmine #12031–#12035 (06/11/2026)
- [x] #12031 Danh sách: sort mặc định, bỏ nút Xem, sort 2 cột tổng, "Tạo mới", thêm Người/Ngày cập nhật (cả file xuất).
- [x] #12032 Form: tiêu đề khối cỡ chuẩn, sắp lại Năm–Phòng ban–Kỳ / Từ–Đến–Ngày HT / Bộ phận + Ghi chú, chữ bảng 12px.
- [x] #12033 Popup hợp đồng: badge vai trò sau tên, link đủ mọi hợp đồng, phân trang, nới rộng không đè menu, thu hẹp cột Khách hàng. Copy pattern `components/report/V2BaseReportModal.vue:223`.
- [x] #12034 Chi tiết: nút Sửa, Duyệt, Xóa, In, Xuất Excel, Quay lại; trạng thái lên tiêu đề; bỏ Mã phiếu; sửa hở/lệch tiêu đề bảng khi cuộn.
- [x] #12035 Excel 1 phiếu bỏ Trạng thái (giữ logo, xem design §5). In: phòng ban in hoa dưới dòng Kỳ, bỏ Mã phiếu, tiêu đề NV/TBP/TP/STT trên 1 dòng.
- [ ] #12035 Xuất Excel danh sách báo lỗi trên dev: CHƯA tái hiện được ở local, chưa sửa. Đã thử luồng thật, phiếu nháp (BE, 4 tài khoản), dòng rỗng/null/mã toàn số (FE) đều thành công. Cần response lỗi của `export-rows` trên dev (Network/log).

## Checkpoint

### Checkpoint — 2026-11-06 — QA #12031–#12035 đã commit trên develop (chưa push)
Commit: api `d011eb69b`, client `659126842`. Feature test 7/7. Playwright đạt phần đã sửa; riêng lỗi xuất Excel danh sách của #12035 chưa tái hiện được, chưa sửa. Local không nhúng được logo vì `companies.header` là path tương đối tới ảnh không có ở máy này, chưa kiểm được logo trong file Excel 1 phiếu.

### Checkpoint — 2026-11-04 13:50 — Lịch sử XONG, đã commit (chưa push)
Commit: api `542ed5694` + `3451ae03a`, client `3a7da560c` + `de4b6ca63`, nhánh `feature/qt-thuong-ns-quy-moi`.
Script BE 19/19 PASS; feature test 7/7. Playwright: tạo → sửa ghi chú → duyệt ⇒ đúng 3 dòng (Tạo mới / Ghi chú cũ→mới / Đang tạo→Đã hạch toán), không diff thừa khi lưu lại bảng NV; hiện đủ ở popup danh sách lẫn khối Lịch sử chi tiết.
Đã dọn: phiếu 35 + con + account_details 1002976–1003011, catalog_histories của bảng, quyền gán tạm role 18/emp 13.
Đã push nhánh feature lên origin (2 repo). Còn: merge develop chờ user.

### Checkpoint — 2026-11-04 13:25 — Phase 3 XONG (chưa commit)
Playwright :3002/:8002: Thêm (kỳ 1 + PHÒNG THIẾT BỊ Ô TÔ 2 → 18 NV) → Lưu (TPE.QTHHQ1126.0002, 18 NV/702 HĐ) → Sửa nạp đủ → Chi tiết Duyệt (confirm → status 3, ghi sổ 18 Nợ TK216 + 18 Có TK117 = 84,855,615.17 mỗi bên) → nút còn In/Xuất/Quy chế/Quay lại → Xuất Excel 200 → In → Xóa phiếu status 1 (cascade sạch). Console chỉ lỗi socket :8891.
Sửa thêm: print.vue bảng ma trận 10px + nowrap ô số (trước bị ngắt "20,051,410,⏎226").
Đã dọn: phiếu 29/30/31 + con + account_details 1002928–1002967, role_has_permissions role 18 & employee_has_permissions emp 13 cho 101909–101912.
Còn: Lịch sử (phase sau), commit/push chờ user.

### Checkpoint — 2026-11-04 13:20
Vừa hoàn thành: BE+FE code xong (chưa commit, worktree hrm-api-qtnsq / hrm-client-qtnsq); 7/7 feature test BE xanh; tính kỳ 2/2026 phòng 105 khớp phiếu ERP #19 (44,829,052 / 7,607,263).
Đang làm dở: Playwright trên client worktree :3002 (API :8002) — chờ webpack compile.
Bước tiếp theo: bấm thật luồng danh sách → tạo → lập QT → lưu → duyệt → account_details → in/xuất → xoá.
Blocked: worktree vendor phải là thư mục thật (symlink từng gói) + copy riêng laminas-zendframework-bridge và phpunit/phpunit (2 gói này require autoload theo realpath → nạp trùng autoload repo chính).
