# Plan — Danh sách loại phiếu hạch toán (@khoipv)

## Phase 1 — Port màn danh sách

### BE
- [x] Entity `Modules/Finance/Entities/ListBillAccounting.php` (`$table`, hằng `TYPES` chép ERP)
- [x] Service `ListBillAccountingService::index()` — keyword (name), type, sort name/type, mặc định id asc như ERP
- [x] Resource `ListBillAccountingResource` (type_name, accounting_text)
- [x] Controller `ListBillAccountingController` index / types / export (DynamicExport)
- [x] Route `v1/finance/list-bill-accountings` (không middleware quyền)
- [x] `ExportColumnRegistry` khoá `list_bill_accountings`
- [x] Smoke test API

### FE
- [x] `pages/admin/list-bill-accountings/index.vue` (khuôn `pages/finance/currencies/index.vue`)
- [x] Menu `components/subsystem-menu/admin.js` — nhóm dưới "Danh mục mẫu in"
- [x] Compile check

### Checkpoint — 2026-10-13
Vừa hoàn thành: BE (entity/service/resource/controller/route/export) + FE (index.vue + menu admin.js). Smoke test API 5/5 = 200 (list, lọc type+keyword, sort type_name desc, types, export 82KB). Compile FE pass, grep checklist sạch.
Đang làm dở: —
Bước tiếp theo: user mở trình duyệt kiểm /admin/list-bill-accountings (menu Quản trị hệ thống, dưới Danh mục mẫu in).
Blocked:
