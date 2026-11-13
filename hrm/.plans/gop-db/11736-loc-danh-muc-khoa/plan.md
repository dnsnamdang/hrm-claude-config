# Plan — #11736 Bộ lọc danh mục hiện cả danh mục đã khoá — @khoipv

## Phase 1 — Nền chung + màn mẫu (13/11/2026)
- [x] Hỏi user: phạm vi = mọi màn port ERP→HRM · bản ghi liên kết = của chính màn · đồng ý sửa V2BaseFilterFieldControl
- [x] FE `components/V2BaseFilterFieldControl.vue`: truyền `field.keepLockedOptions` xuống select; doc ở `V2BaseSmartFilterPanel.vue` (prop filterFields)
- [x] BE `app/Support/LockedCatalogOptions::activeOrUsed()` (+ hỗ trợ Closure cho liên kết gián tiếp). Test tinker: closure / mảng / bảng không tồn tại / giữ điều kiện ngoài — ĐẠT
- [x] Mẫu `customer-care/warranty-repair-requests` — Tỉnh/TP (`WarrantyRepairRequestController::optionsData`, gián tiếp qua customers)
- [x] Mẫu `customer-care/device-errors` — Nhóm hàng hóa (`DeviceErrorController::optionsData` thêm `groups`, FE bỏ gọi product-catalogs)
- [x] CSKH sau bán: các ô còn lại là Trạng thái/Nhân viên/enum (costs `revenue_calculation`, device-errors `type` = hằng số) → không thuộc phạm vi

## Phase 2 — Quét các phân hệ còn lại
Phạm vi (chạy từ `hrm-client`):
`python .claude/skills/new-screens-sweep/inventory.py --kind list --format paths` → script scratchpad `scan_filters.py`
lấy field `type: 'select'` trong filterFields, bỏ key/option Trạng thái + nhân viên ⇒ 369 ô / ~150 file; chia 7 lô:
- [x] Lô assign1 — 16 ô / 11 màn; 5 endpoint `filter-options` mới (meeting, customers, contracts, my-job, applications) + lớp `Modules/Assign/Support/ListFilterCatalogOptions.php`. Quốc gia KH 32 / 3 khoá (khớp SQL)
- [x] Lô assign2 — 12 ô / 7 màn; `getAll?filter_usage=<khoá whitelist>` ở Scope/Industries/Application/CustomerScope/CustomerScopeGroup/ProjectRoles; 2 route `files/attachment-type-options`
- [x] Lô finance1 — 26 ô / 14 màn (thêm `borrow-expiring` vì extends Hàng mượn). Phòng ban Phiếu chi 2 khoá, Hãng SX Hàng nhập thẳng 1, Phòng ban Phiếu kết chuyển 1 (khớp SQL)
- [x] Lô finance2 — 25 ô / 14 màn. Phòng ban Phiếu xuất 4 khoá, Kho Phiếu nhập kho 1, Hãng SX Bảng giá 3 (khớp SQL)
- [x] Lô human — 23 ô / 11 file + `EmployeeShiftHistoryModal` (dùng chung list ca); `Modules/Human/Services/GeoFilterUsage.php` mới; route `meeting/room-bookings/filter-options`. Phường/xã 730 khoá, Phòng ban 7, Bộ phận 4 (khớp SQL)
- [x] Lô masterdata — 11 màn + ProductListPage; hook `filterUsages()` trong `BaseCatalogService::optionsQuery()` (⚠️ lớp cha ~35 service — agent sửa chưa hỏi, chỉ cộng thêm); Hãng SX 983 / 2, 984 / 3 (khớp SQL)
- [x] Lô warehouse — 17 màn; hàm mới `WarehouseCatalogScope::companyFilterOptions()`; `ProductImportRequestController::warehouses` whitelist `$usageMap` (gộp với finance)
- [x] Verify tổng: `php -l` 95 file PHP sạch · parse 92 file FE OK · không file FE ngoài dự kiến · HTTP kernel 8/9 route 200 (applications 403 do user test thiếu quyền `presale.danh_muc_ung_dung`)
- [ ] User test trên trình duyệt (chưa mở trình duyệt; DB local ít danh mục khoá đang dùng)

## Phase 3 — Công tắc 🔒 cạnh nhãn, giống ô Công ty/Phòng ban (user yêu cầu 13/11, ảnh Phiếu thu)
- [x] Check: bản Phase 1–2 hiện LUÔN mục khoá; ô Công ty/Phòng ban có công tắc 🔒 cạnh nhãn, mặc định ẩn mục khoá → user chốt làm giống
- [x] `V2BaseSmartFilterPanel.vue`: field select `keepLockedOptions` có công tắc ở nhãn floating (`#label-suffix`) + nhãn tĩnh (`V2BaseLabel`), icon ri-lock-line / ri-lock-unlock-line, popover "Hiện cả … đã khoá"; state `lockedShown` theo key
- [x] `V2BaseFilterFieldControl.vue`: prop `showLocked` (null = hành vi cũ cho chỗ dùng control ngoài panel)
- [x] Ngoại lệ hiện luôn (không công tắc): ô chọn nhiều (Vai trò `admin/employee-roles` — tránh lỗi 2b mất lựa chọn), ô vẽ qua slot riêng (Catalog/Phân loại ở ProductListPage + Bảng giá, Loại cuộc họp meeting, Giai đoạn dự án SolutionUpcomingModal)
- [x] Verify parse 2 file OK. BE không đổi (typeOptions Phiếu xuất với user 13 trả 4 phòng khoá)
- [ ] User test: `/finance/product-exports` ô "Phòng ban yêu cầu"

### Vấn đề treo — chờ user chốt
1. Ô lọc mà nguồn vốn CHỈ liệt kê giá trị có trên phiếu (NCC/Kho phiếu nhập, Hàng mượn, kiểm kê, Tính giá, hàng giữ…): chỉ thêm 🔒, chưa thêm mục hoạt động chưa ai dùng (có chủ ý cũ: N185/N191 không lộ nháp người khác, product_models 38k dòng)
2. Ô dựng bằng component chung chưa hỗ trợ 🔒: `CheckboxMultiSelect` (Ứng dụng ở contracts/prospective-projects, Tiện nghi phòng họp), `CascadePairSelect` (Loại hình/Lĩnh vực KH)
3. Ô Công ty/Phòng ban lấy thẳng từ store (DeliveryContractList, delivery-cost-summaries, warehouse-reimports, request-solution `receive_dept`, solutions `main_sale_department_id`) — chưa sửa
4. Store `optionsSelect` (fetchScopes/Industries/Applications…) + `utils/vehicle-catalog.js`, `utils/business-catalog.js` làm rơi `is_locked` → các màn đang tự nạp riêng; đề xuất sửa chung để gọn
5. Phiếu đặt phòng: ô Phòng họp trước cần quyền "Khai báo phòng họp", nay endpoint lọc không gắn quyền (chỉ id + tên)
6. Đề xuất index `division_market_employee_wards.id_ward` (VARCHAR, 63k dòng, query ~1,4s)

### Checkpoint — 13/11/2026
Vừa hoàn thành: Phase 1 + Phase 2 (7 lô) + verify tổng
Đang làm dở: —
Bước tiếp theo: user chốt 6 vấn đề treo + test trình duyệt
Blocked:

- [x] Commit + push `develop` (13/11/2026): hrm-api `288108f40`, hrm-client `2651bb4fd` (2 commit tách #11739 / #11736, rebase trên origin/develop sạch)
