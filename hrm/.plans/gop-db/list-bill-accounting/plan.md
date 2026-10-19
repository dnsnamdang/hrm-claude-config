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

## Fix — Cột "Hạch toán riêng" hiện số 0 (15/10, user báo)
- [x] Nguyên nhân: slot `cell-accounting` chỉ có 1 thẻ `<i v-if>` → dòng accounting=0 slot rỗng, V2BaseDataTable rơi về nội dung mặc định in `0`
- [x] Bọc `<span class="field-line">` luôn render; verify render SSR cũ ra `0` / mới ra ô trống, compile sạch
- [ ] User F5 kiểm trên trình duyệt

## Fix — Xuất Excel: logo to hơn bảng (15/10, user báo)
- [x] Nguyên nhân: xuất qua `DynamicExport` (blade chèn logo cỡ gốc) — bảng 4 cột hẹp hơn ảnh
- [x] Chuyển sang khuôn chung `utils/export/listExportFile.js` (logo trải bằng bề rộng bảng): BE `GET /export-rows` (`ListBillAccountingService::exportRows()`), bỏ `/export` + mục `ExportColumnRegistry[list_bill_accountings]`; FE `runExport` → `exportListFile`
- [x] Verify: php -l, smoke test export-rows (lọc type / theo fields / phân trang), compile FE
- [ ] User xuất thử trên trình duyệt xem logo

## Fix — Xuất Excel: bỏ nút lọc ở hàng tiêu đề (15/10, user yêu cầu)
- [x] Hàm chung `listExportFile.js`: thêm tuỳ chọn `autoFilter` (mặc định true → màn khác không đổi)
- [x] Màn này truyền `autoFilter: false`; verify dựng file thật: mặc định có `<autoFilter>`, false thì không
- [ ] User xuất thử trên trình duyệt


## Dời menu sang Bán hàng (15/10)
- [x] Gỡ mục khỏi `components/subsystem-menu/admin.js`, thêm vào `sale-hub.js` › Quy chế - Thiết lập › Thiết lập (route giữ `/admin/...`)
- [ ] User mở trình duyệt kiểm sidebar Bán hàng
