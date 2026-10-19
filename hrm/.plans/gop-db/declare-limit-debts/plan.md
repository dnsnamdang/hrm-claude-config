# Khai báo hạn mức công nợ khách hàng — plan

> Người phụ trách: @khoipv · Nhánh: `develop` (con của `gop_db`) cả 2 repo
> Design: `design.md` · Spec: `docs/superpowers/specs/gop-db/2026-10-14-declare-limit-debts-design.md`

## Quyết định đã chốt (14/10/2026)
- Bảng KH → các dòng công ty, sửa thẳng trong bảng + nút Lưu từng khách (y ERP; đổi lại 14/10 — bỏ popup).
- 2 quyền mới tên y ERP (type 8). Không quyền vẫn thấy menu + xem mọi công ty (y ERP, đổi lại 14/10/2026).
- Giữ y ERP: lưu xoá hết dòng của KH rồi ghi lại dòng đang hiện; KH đã có dòng thì không hiện thêm công ty khác.

## Phase 1 — Port màn

### BE (`hrm-api`)
- [x] Seeder quyền 1707 `Quản lý khai báo hạn mức công nợ khách hàng`, 1708 `Xem khai báo hạn mức công nợ khách hàng` (type 8)
- [x] `Modules/Finance/Services/CustomerDebt/DeclareLimitDebtService.php` — danh sách KH + dòng hạn mức theo phạm vi, chi tiết 1 KH, lưu (xoá-ghi lại y ERP), lịch sử, export-rows
- [x] `Modules/Finance/Http/Controllers/V1/DeclareLimitDebtController.php` + route `finance/declare-limit-debts` (checkPermission)
- [x] Đăng ký `customer_limit_debts` vào `CatalogHistoryService::TABLES`
- [x] Smoke test API (HTTP kernel)

### FE (`hrm-client`)
- [x] `pages/finance/declare-limit-debts/index.vue` — SmartFilterPanel floating + cây 2 tầng + Cấu hình cột + Xuất Excel + Lịch sử
- [x] ~~popup Sửa `DeclareLimitDebtModal.vue`~~ → đã bỏ, chuyển sang sửa thẳng trong bảng (y ERP)
- [x] Sửa trong bảng: select Cách tính lãi + 2 ô tiền ở dòng công ty mình, nút Lưu từng khách, lỗi theo dòng, cảnh báo rời màn khi còn khách sửa dở
- [x] Menu `components/subsystem-menu/finance.js` — gắn link (không `isShow`, y ERP)
- [x] Đổi lại y ERP: bỏ `isShow` menu + bỏ checkPermission ở 4 route xem, PUT vẫn cần Quản lý
- [x] Compile check (vue-template-compiler + babel) + grep checklist skill
- [x] Xuất Excel gộp ô STT / Mã / Tên / MST theo khách (y rowspan ERP): BE `export-rows` trả `row_groups` + `merge_columns`; helper chung `utils/export/listExportFile.js` thêm gộp ô OPT-IN (`mergeRowGroups`) — màn khác không trả 2 khoá này thì file y cũ (user duyệt sửa helper 14/10/2026)
- [x] Bảng trên màn gộp ô STT / Mã / Tên / MST / Hành động theo khách (rowspan y ERP): mỗi dòng bảng = 1 dòng công ty; `V2BaseDataTable` thêm prop OPT-IN `cellSpan(item, column, index)` (user duyệt sửa component chung 14/10/2026 — màn khác không truyền thì y cũ); bỏ nền sọc chẵn/lẻ ở màn này
- [x] Lịch sử chỉ ghi phần thay đổi (user chốt 14/10/2026): `DeclareLimitDebtService::changedRows()` so từng công ty (thiếu dòng = dòng rỗng), chỉ log công ty có giá trị đổi → luôn ra "sửa thông tin" từng trường; hết log rác "thêm mới" 7 dòng trống ở lần khai đầu / "đã xóa" dòng trống

### Tài liệu
- [x] design.md + spec chi tiết

## Phase 2 — Fix Redmine #11717 (feedback tester 14/10/2026)

- [x] BE: tìm nhanh bỏ mã / tên KH, thay bằng SĐT (`customers.mobile`) + giữ MST/CMND
- [x] FE: placeholder ô tìm nhanh "Tìm theo SĐT hoặc MST/CMND khách hàng"
- [x] FE: thu nhỏ cột STT / Mã / Tên khách hàng
- [x] FE: nút Cấu hình cột đổi sang `V2BaseButton secondary size="sm"` như các màn khác (đang là V2BaseIconButton)
- [x] FE: nút Lưu từng khách màu teal (primary), khác nút Lịch sử
- [x] FE: khoảng trắng dưới bảng — KHÔNG phải do `min-vh-100` (đã trả lại): `<select>` ẩn của select2 ở ô Cách tính lãi là `position:absolute`, không có cha định vị nên bám `<body>`, thoát khung cuộn bảng → trang dài theo dòng cuối bảng (3.002px, đo Playwright). Bọc ô trong `position-relative` → trang còn 943px
- [x] FE: placeholder ô Cách tính lãi + 2 ô hạn mức về 12px
- [x] FE: Xuất Excel treo sau "Đã tải đủ dòng" — `mergeRowGroups` gọi `sheet.mergeCells` 171 nghìn lần, ExcelJS kiểm chồng lấn với MỌI ô gộp trước đó (O(n²), đo ~37 phút); gộp không qua vòng kiểm (nhóm không bao giờ chồng nhau) → 1,8s

### Checkpoint — 2026-10-14
Vừa hoàn thành: BE (quyền 1707/1708 trong seeder + đã chèn DB local, service, controller, 5 route có checkPermission, khoá lịch sử `customer_limit_debts`) + FE (danh sách cây 2 tầng, popup Sửa, menu). Smoke test HTTP kernel bằng role tạm (đã gỡ): không quyền → 403; chỉ Quản lý → chỉ dòng công ty mình, Lưu xoá dòng công ty khác (y ERP, có log "đã xóa"); Quản lý + Xem → 7-8 dòng, gửi kèm giá trị công ty khác bị bỏ qua, lưu không đổi gì thì không ghi; chỉ Xem → PUT 403, `is_can_edit` false; 422 khi hạn mức không phải số; KH không tồn tại 404; sort / lọc / phân trang / export-rows đúng (~0,4s/trang). Dữ liệu KH 1120 + 232397 và log test đã khôi phục theo id. Compile FE pass, grep checklist skill sạch.
Đang làm dở: —
Bước tiếp theo: user mở trình duyệt kiểm `/finance/declare-limit-debts` (chưa bấm thật: sửa trong bảng + Lưu từng khách + cảnh báo chưa lưu, Lịch sử, Xuất Excel, Cấu hình cột). Xuất Excel không lọc = ~336 nghìn dòng (42 nghìn KH × 8 công ty) — nặng ở trình duyệt.
Blocked:
