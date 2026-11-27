# Plan — Phiếu xuất kho (bản thật BE + FE)

> @khoipv · Bắt đầu 26/11/2026
> Demo: `demos/demo-phieu-xuat-kho.html` · Design: [design.md](design.md) · Spec: [2026-11-26-phieu-xuat-kho-design.md](../../docs/superpowers/specs/2026-11-26-phieu-xuat-kho-design.md)

## Phase 1 — Tìm hiểu & chốt hướng
- [x] 1. Đọc demo PXK + spec demo, code thật ĐNXK (`WarehouseExportRequestService`, entity, migration) + PNK (`writeStock`, `stock_balances` / `stock_serials` / `stock_ledgers`)
- [x] 2. Hỏi user: phạm vi (có làm Gửi bộ phận giao hàng không), phân quyền theo cấp, `is_can_delete`, các câu hỏi mở Q1–Q8 của demo
- [ ] 3. Viết spec + design, user duyệt
  - [x] 3a. Viết spec đầy đủ `docs/superpowers/specs/2026-11-26-phieu-xuat-kho-design.md`
  - [x] 3b. Viết tóm tắt `design.md`
  - [x] 3c. Reviewer (subagent) đọc spec → hỏi user những điểm chỉ user trả lời được (Q-F → Q-J); tham khảo cách hrm làm PXK
  - [x] 3d. User duyệt spec (26/11: "ok bạn cứ làm đi rồi mình sẽ test lại")
- [x] 4. Lên plan chi tiết BE / FE

## Phase 2 — BE (`hrm-thanhan-api/Modules/Warehouse`)
- [x] BE1. Migration `2026_11_27_000001_create_warehouse_exports_tables.php` — 5 bảng (`warehouse_exports`, `_items`, `_lots`, `_serials`, `_logs`), cột `close_reason / closed_by / closed_at` cho `warehouse_export_requests`, json `warehouse_exports` cho `column_customizations`; chỉ index. Hằng `StockSerial::STATUS_EXPORTED = 2`, `StockLedger::DOC_EXPORT = 'PXK'`
- [x] BE2. `PermissionsTableSeeder` id 534–536 (xem PXK theo tổng cty / cty / nhóm nghiệp vụ)
- [x] BE3. Entity `WarehouseExport` (trạng thái, cờ quyền) + `WarehouseExportItem / Lot / Serial / Log`
- [x] BE4. `Services/WarehouseExportService.php` — scope, list, filterOptions, requests (ĐNXK lập được), prepare (lô / seri / tồn khả dụng), save (validate §8, lô giữ HĐ trước), approve (§9 + cộng `contract_products.exported_qty`), delete, detail (thẻ kho, lịch sử), export Excel, notify
- [x] BE5. `WarehouseExportController` + `SaveWarehouseExportRequest` + routes + resource
- [x] BE6. ĐNXK: cờ `is_can_export / draft_export_id / is_can_close`, API Đóng phần còn lại (PUT), chặn Thu hồi / Trả lại khi có PXK nháp, chi tiết trả danh sách PXK, log `close / export`
- [x] BE7. PNK: số seri ≤ SL × hệ số (service + `receiptRules.js` FE)
- [x] BE8. Payroll `ExpectedQtyImport`: chặn khi HĐ đã có PXK đã duyệt
- [x] BE9. Fake data: mở rộng `ExportRequestFakeDataSeeder` + Clean
- [x] BE10. Kiểm BE: `php -l`, chạy thử service trong transaction (lập → duyệt → tồn / seri / thẻ kho / ĐNXK / HĐ) rồi rollback

## Phase 3 — FE (`hrm-thanhan-client/pages/warehouse`)
- [x] FE1. Menu Phiếu xuất kho
- [x] FE2. Màn danh sách V2 (bộ lọc, cột, xuất Excel, thao tác)
- [x] FE3. Form tạo / sửa (`components/ExportForm.vue` + `create.vue` / `_id/edit.vue`): chọn ĐNXK, bảng hàng → lô → seri, quét seri, popup chọn seri (trong form), `exportRules.js`, style `pxk-goods.scss`
- [x] FE4. Màn chi tiết: tab Hàng hóa / Thẻ kho / Lịch sử, nút Sửa / Duyệt / Xóa / In
- [x] FE5. `printExport.js` mẫu 02-VT
- [x] FE6. ĐNXK chi tiết: tab PXK, nút Lập PXK / Mở nháp, popup Đóng phần còn lại

## Câu hỏi đã chốt
- [x] Q-A. (26/11) Phạm vi → **dừng ở Đã xuất kho**; Gửi bộ phận giao hàng (luồng kho → KH, chưa có module) để đợt sau
- [x] Q-B. (26/11) Phân quyền theo cấp → **3 cấp như ĐNXK** (tổng cty / cty bán / nhóm nghiệp vụ) + thủ kho luôn thấy phiếu kho mình
- [x] Q-C. (26/11) `is_can_delete` → **phiếu Nháp + người lập phiếu**
- [x] Q-D. (26/11) User đồng ý giữ như demo: chỉ thủ kho kho đó lập / sửa / duyệt; 2 trạng thái Nháp → Đã xuất kho (không bỏ duyệt); không mang giá; ngày xuất ≥ ngày tạo ĐNXK, ≤ hôm nay
- [x] Q-E. (26/11) Cách nhập SL theo ĐVT → **PA 1**: SL dòng lô nhập theo ĐVT cơ bản (số nguyên, khớp tồn / seri); BE quy ngược ra ĐVT dòng ĐNXK (÷ hệ số) khi cộng `exported_qty`
- [x] Q-F. (26/11, sau khi xem hrm) SL lô → **PA 1 nhưng cho 3 số lẻ**; chỉ lô có seri bắt số nguyên (hrm: nhập theo ĐVT dòng, cho lẻ, nguyên khi hệ số ≠ 1)
- [x] Q-G. (26/11) **1 seri = 1 ĐVT cơ bản**; đồng ý sửa PNK: số seri ≤ SL × hệ số (hrm không quản lý seri trong kho)
- [x] Q-H. (26/11) Duyệt PXK **cộng dồn** `contract_products.exported_qty`
- [x] Q-I. (26/11) Import Excel SL đã xuất (`ExpectedQtyImport`) → **chặn khi HĐ đã có PXK đã duyệt**
- [x] Q-J. (26/11) **Bắt dùng hết lô giữ HĐ trước** tồn chung (BE chặn)

## Phase 4 — Test
- [ ] T1. User chạy `PermissionsTableSeeder` (quyền 534–536) + gán quyền cho vai trò
- [ ] T2. User test luồng: ĐNXK Chờ xuất kho → Lập PXK → Lưu nháp → Duyệt → tồn / seri / thẻ kho / ĐNXK Đang xuất kho → lập đợt 2 → Đóng phần còn lại → In 02-VT
- [x] T3. E2E Playwright `e2e/tests/warehouse/phieu-xuat-kho.spec.js` (user yêu cầu 26/11/2026) — ĐNXK 27 `PDNXK2611-0001` (FAKE-KHO-HN, thủ kho NV 15); token NV 15 sinh bằng `e2e/scripts/jwt.php`; afterAll trả nguyên trạng DB
  - [x] T3a. Danh sách PXK mở được
  - [x] T3b. ĐNXK → Lập phiếu xuất kho → gợi ý FEFO → xuất thiếu 1 dòng → Lưu nháp (tồn chưa trừ)
  - [x] T3c. ĐNXK có nháp: hiện "Mở PXK nháp", ẩn "Lập phiếu xuất kho" / "Đóng phần còn lại"
  - [x] T3d. Chi tiết PXK nháp → In (popup 02-VT + BẢN NHÁP)
  - [x] T3e. Duyệt → Đã xuất kho, tab Thẻ kho, tồn bị trừ, ĐNXK Đang xuất kho, exported_qty dòng ĐNXK + HĐ
  - [x] T3f. Lập nháp đợt 2 → Xóa
  - [x] T3g. ĐNXK → Đóng phần còn lại (nhập lý do) → Đã xuất kho, closed_qty, banner
  - [x] T3h. Sửa lỗi phát hiện khi chạy — không thấy lỗi app; chỉ sửa selector footer trong spec (gốc V2Footer là `div.footer`)
  - Kết quả 26/11/2026: **11/11 pass** (~1,9 phút); DB trả nguyên trạng (ĐNXK 27 về Chờ xuất kho, tồn lô 513–517, exported_qty HĐ = 0, không còn PXK / thẻ kho PXK)
  - Thêm `e2e/scripts/jwt.php` + `e2e/utils/jwt.js` (sinh token NV bất kỳ); làm mới `ACCESS_TOKEN` trong `e2e/.env` (NV 13)

## Phase 5 — Phản hồi test
- [x] P1. (27/11) Check: local có 2 ĐNXK Chờ xuất kho (27 `PDNXK2611-0001`, 30 `PDNXK2611-0004`) nhưng Tạo PXK không thấy → **không phải lỗi code**: cả 2 thuộc kho 24 "Kho Hà Nội (test)", thủ kho chỉ có NV 15 (Nguyễn Văn Sa) và NV 17 (Trần Thuỷ Tiên); `WarehouseExportService::requests()` chỉ trả ĐNXK của kho mà người đăng nhập là thủ kho (`warehouse_stockers`) — đúng chốt Q-D. Điều kiện còn lại đều đạt (trạng thái 3, còn SL 16, chưa có PXK nháp). FE `ExportForm.vue` không lọc thêm.
  - Cách test: đăng nhập NV 15 / 17, hoặc thêm người đang test làm thủ kho kho 24 ở danh mục Kho
- [x] P2. (27/11) Đổi điều kiện thủ kho → quyền. User chốt:
  - Quyền mới (seeder): **537 "Quản lý phiếu xuất kho"** (thêm / sửa / xóa), **538 "Duyệt phiếu xuất kho"**
  - Tạo mới (nút + ô chọn ĐNXK + nút "Lập PXK" ở ĐNXK): có 537 → mọi ĐNXK Chờ / Đang xuất kho còn hàng, chưa có PXK nháp, mọi kho
  - Sửa: Nháp + 537 · Duyệt: Nháp + 538 · Xóa: Nháp + 537 + người lập
  - Xem: chỉ theo 534–536 (bỏ "thủ kho luôn thấy phiếu kho mình")
  - ĐNXK: cờ `is_can_export` / Mở PXK nháp / Đóng phần còn lại đang theo thủ kho → đổi tương ứng
  - [x] P2a. Seeder 537, 538 (`Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php`)
  - [x] P2b. BE `WarehouseExport` (`PERM_MANAGE` / `PERM_APPROVE`, `userCanManage()` / `userCanApprove()`, bỏ `keeperWarehouseIds`), `WarehouseExportService` (scope bỏ OR thủ kho, `requests` không lọc kho + 403 khi thiếu quyền, `requestError`, `can_create`, "Lưu & duyệt" cần 538), ĐNXK `canExport` / `canClose` / `is_can_open_draft_export` (537 hoặc 538). Giữ nguyên: Trả lại ĐNXK vẫn theo thủ kho. Fake seeder bỏ qua PXK nháp khi NV chưa có 537
  - [x] P2c. FE: placeholder ô chọn ĐNXK, comment ở form / danh sách / chi tiết / ĐNXK (form đã có banner `loadError` hiện 403)
  - [x] P2d. `php -l` đạt; chạy thử trong transaction + rollback: không quyền → can_create false, requests 403; 537 → thấy 2 ĐNXK kho 24, sửa / xóa được nháp mình lập, không duyệt; 537 + 538 → duyệt được; prepare ĐNXK 27 OK
  - [ ] P2e. User chạy `PermissionsTableSeeder` (thêm 537, 538) + gán quyền cho vai trò rồi test tay
- [x] P3. (27/11) Bỏ nút "Gợi ý lại FEFO" ở form tạo PXK (`ExportForm.vue`: nút, modal `confirm-refefo-export`, hàm `askRefefo` / `refefo`). Giữ tự gợi ý lô lần đầu khi chọn ĐNXK (`suggestFefo` trong `loadPrepare`)
- [x] P4. (27/11) Soát lại toàn bộ so với `demos/demo-phieu-xuat-kho.html` (3 subagent: danh sách / form / chi tiết + in + ĐNXK). Logic BE (lô, seri, validate, duyệt, thẻ kho, đóng phần còn lại) khớp; lệch chủ yếu ở UI:
  - Cao: (a) danh sách cột Thao tác thành Duyệt → Sửa → Xóa → Lịch sử, thiếu In (`index.vue:515`); (b) cột Tổng SL xuất bị ẩn mặc định (`index.vue:313`); (c) popup Duyệt ở chi tiết không có cảnh báo xuất thiếu / cận date (`ExportDetail.vue:409`); (d) bản in theo ĐVT cơ bản, spec §11.4 ghi theo ĐVT dòng (`printExport.js:4`); (e) form thiếu chế độ thu gọn Thông tin chung; (f) thiếu chip trạng thái từng hàng; (g) dòng không lô để trống, không hiện "Không lô"
  - Thấp: nhãn ("Phiếu đề nghị", "Hợp đồng" ≠ "Chứng từ nguồn", "Gần hết hạn" ≠ "Cận date · n ngày"), thiếu ô Công ty bán / Loại xuất ở form, tab Thẻ kho ẩn khi Nháp, thứ tự nút footer chi tiết, lý do lỗi quét seri, toast sau duyệt, câu lỗi BE `SaveWarehouseExportRequest`
  - [ ] P4a. Chờ user chốt mục nào sửa
- [x] P5. (27/11) Màu bảng hàng hóa PXK lệch bảng dùng chung → theo màn tạo ĐNXK (`export_requests/create`): bỏ nền xám xanh #f3f7f6 của dòng nhóm + 2 rule nền thừa trong `exports/pxk-goods.scss`; giữ nền MISA, xanh #ddf1e9 cho lô đã nhập SL (như dòng tick ĐNXK), vàng cho dòng ĐỔI (er-goods)
- [x] P6. (27/11) Cột Loại tồn ở form PXK hiện chữ "grp" ở dòng mã hàng: key cột `kind` trùng field `kind` của dòng (grp/lot) → slot rỗng thì V2BaseFormTable in `item.kind`. Đổi key → `stock_kind`; dòng nhóm để trống, dòng lô hiện chip như demo (`Giữ cho HĐ` tím, tooltip số HĐ / `Tồn chung` xanh, căn giữa) — áp cả form + chi tiết (`.pxk-kind` trong pxk-goods.scss)
- [x] P7. (27/11) Bỏ dòng gợi ý dưới ô chọn ĐNXK ở form ("Chờ xuất kho · cần giao … · SL đề nghị còn xuất …") + computed `needTotal` không còn dùng
- [x] P8. (27/11) Bỏ tô xanh dòng đã tick (form ĐNXK) và lô đã nhập SL (form PXK): bỏ `is-active` ở `rowClass` 2 form + 2 rule `is-active` trong `er-goods.scss`. Giữ `is-warn` (vàng) dòng ĐNXK có cảnh báo SL, `is-swap` (vàng) dòng ĐỔI
- [x] P9. (27/11) Hỏi: ĐNXK chỉ lấy hàng HĐ đã được đề xuất? → Không theo contract_products/phiếu đề xuất, mà theo dòng **PXL đã duyệt** của HĐ có ô Xuất bán (`alloc_ton_ban + alloc_buy_ban > 0`), trừ NCC giao thẳng KH + SL đã đề nghị ở phiếu khác (`WarehouseExportRequestService::handlingLines`, spec ĐNXK §5 dòng 127). Đúng thiết kế, không sửa
- [x] P10. (27/11) ĐNXK chọn thêm hàng khác của HĐ (chưa có trên PXL). User chốt: phạm vi = `contract_products` của HĐ có hàng không nằm trên dòng PXL đã duyệt (giữ nguyên dòng PXL); SL tối đa = `cp.qty` (đã gồm phụ lục) − Σ(qty − closed_qty) ở ĐNXK khác cùng `contract_product_id`; tồn kho chỉ tham khảo; UI = nút "Thêm hàng khác của HĐ" mở popup chọn
  - [x] P10a. Migration `2026_11_27_000002`: `warehouse_export_request_products.contract_product_id` (nullable, index) + `supply_handling_id` / `supply_handling_product_id` nullable
  - [x] P10b. `WarehouseExportRequestService`: `contractLines()` (dòng HĐ ngoài PXL, khóa `c{cp_id}`), `prepare` trả chung `rows` (dòng HĐ có `is_extra`) + điền SL khi sửa, `buildProductLines` nhận `contract_product_id`, `contracts()` tính cả dòng HĐ còn SL; trừ SL đã đề nghị theo HĐ khỏi dòng PXL cùng hàng/ĐVT (PXL duyệt sau)
  - [x] P10c. PXK không đổi: dòng HĐ là dòng thường → `rowKey` `p…`, `addContractExported` tìm theo hàng
  - [x] P10d. FE `ExportRequestForm.vue`: nút + popup chọn hàng HĐ (V2BaseModal), dòng đã thêm có nút × trả về popup, dòng phụ "Hàng HĐ · chưa có trên phiếu xử lý"
  - [x] P10e. Cập nhật spec ĐNXK §4.2 + §5.4; chạy thử BE trong transaction rollback (HĐ 181: c5900 / c5901 hiện, chặn vượt SL HĐ, lưu dòng HĐ `supply_handling_*` NULL, sửa điền lại SL, phiếu khác thấy used, PXK `requestItems` gộp `p74-u2-…`, PXL lên sau trừ đúng 2 vào `used`); biên dịch thử template 2 file Vue đạt
  - Đã chạy migration local. File: `Migrations/2026_11_27_000002_…`, `WarehouseExportRequestService` (`deductContractUsed`, `contractLines`, `keptContractProductIds`, `contracts`, `prepare`, `save`, `buildProductLines`, `displayProducts.is_extra`), `SaveWarehouseExportRequestRequest` (parts `required_without` contract_product_id); FE `ContractGoodsPickerModal.vue` (mới), `ExportRequestForm.vue` (`extraPool`, `addExtra`, `removeExtra`), `exportRequestRules.js` (payload), `ExportRequestDetail.vue` (nhãn), `er-goods.scss` (`.er-extra-x`)
  - [ ] P10f. User test trình duyệt
- [x] P11. (27/11) ĐNXK: dòng hàng nào cũng xóa được + popup tick rồi bấm Chọn mới thêm (tham khảo `supply/purchase_orders/add`). User: "hàng nào cũng có thể xóa đi được chứ, button xóa tham khảo màn này cho tôi này supply/purchase_orders/add — với cả popup chọn hàng hóa để tick rồi bấm chọn thì mới thêm chứ"
  - [x] P11a. `ExportRequestForm.vue`: cột Thao tác đông cứng sau Tên hàng, `V2BaseIconButton danger` `ri-delete-bin-line` "Xóa hàng" cho MỌI dòng (PXL lẫn HĐ) + BaseConfirmModal xác nhận như đơn mua; dòng xóa trả về popup (giữ thứ tự gốc `_ord`); bỏ nút × cũ
  - [x] P11b. Popup đổi thành "Thêm hàng hóa": nguồn = mọi dòng chưa có trên bảng (dòng PXL đã xóa + hàng HĐ ngoài PXL); bấm dòng = tick/bỏ tick, chỉ nút Chọn mới thêm; dòng thêm vào tick sẵn + SL = SL còn lại
  - [x] P11c. `loadRows('keep')` (đổi kho) giữ đúng dòng đang ở bảng / popup cho cả dòng PXL; biên dịch thử template
  - File: `ExportRequestForm.vue` (cột `act`, `removeRow` / `doRemoveRow`, `addExtra` sắp theo `_ord`, `loadRows` inTable mới, bỏ `removeExtra`), `ContractGoodsPickerModal.vue` (tiêu đề "Thêm hàng hóa", `onRowClick` = tick, chip ĐỔI, dòng phụ PXL/HĐ, tô dòng đã tick), `er-goods.scss` (`.er-act` thay `.er-extra-x`); spec §5.4
  - [ ] P11d. User test trình duyệt
- [x] P12. (27/11) ĐNXK bỏ cột tick trên bảng hàng (đã có nút Xóa). User: "đã thêm button xóa rồi thì bỏ chọn đi chứ nhỉ, đầu tiên vào mặc định đã lấy hàng đã có pxl rồi, muốn thêm thì chọn ở popup"
  - [x] P12a. `ExportRequestForm.vue`: bỏ cột `sel` + toggleAll/allOn/selectableCount/isOff; dòng trên bảng = dòng đề nghị (selected luôn true). Chọn HĐ: dòng PXL còn SL → bảng, SL điền sẵn = SL còn lại; dòng PXL hết SL + hàng HĐ ngoài PXL → popup. Mở sửa: dòng đã có trên phiếu → bảng, còn lại → popup. Ô SL / ghi chú luôn nhập được
  - [x] P12b. `exportRequestRules.js`: lỗi `lines` khi bảng trống → "Thêm ít nhất 1 dòng hàng để đề nghị xuất"; đổi chữ "Số dòng chọn" / xác nhận đổi chứng từ
  - [x] P12c. Biên dịch thử + cập nhật spec §5.4
  - File: `ExportRequestForm.vue` (bỏ cột `sel`, `toggleAll` / `allOn` / `selectableCount` / `isOff`, `loadRows` dựng bảng/popup mới, helper `filledQty`, ô SL/ghi chú bỏ `:disabled`, "Số dòng hàng"), `exportRequestRules.js` (lỗi `lines` khi bảng trống); spec §5.4
  - [ ] P12d. User test trình duyệt
- [x] P13. (27/11) Fix: lập / sửa ĐNXK xong (Lưu nháp / Gửi kho) không về màn danh sách — `save()` đang `router.push` sang màn chi tiết, lệch spec ("Lưu nháp về danh sách như PNK"). User: "sao khi tôi lập phiếu đề nghị xuất kho xong nó không quay về màn danh sách vậy?" → đổi về `/warehouse/export_requests` cho cả 2 nút
- [x] P14. (27/11) Fix PXK: lô lẫn hàng không seri (VD PNK 46 HC-NT-018 lô LOT-9100 SL 16 chỉ 1 seri → 15 không seri) — khi phần không seri đã đủ SL đề nghị thì popup chọn seri "tối đa 0", bấm Bỏ chọn hết xong không chọn lại được; quét seri bị báo "Vượt SL đề nghị". User: "chỗ chọn seri ví dụ tôi bấm bỏ chọn tất cả thì hiện tại đang không có chỗ chọn lại"
  - [x] P14a. `exportRules.js` `setSerials(lot, ids, cap)`: thêm trần SL lô — seri + không seri vượt trần thì bớt phần không seri (seri thay chỗ hàng không seri)
  - [x] P14b. `ExportForm.vue` `openPicker`: tối đa seri = SL đề nghị − lô khác (không trừ phần không seri); popup hiện "phần không seri sau khi áp dụng"; `applyPicker` truyền trần
  - [x] P14c. `doScan`: vượt SL đề nghị nhưng lô còn phần không seri → seri thay 1 đơn vị không seri (SL lô giữ nguyên) thay vì báo lỗi
  - [ ] P14d. User test trình duyệt (PXK từ ĐNXK có HC-NT-018)
- [ ] P15. (27/11) Đổi D8 + D5 theo user: HC-NT-018 ĐVT cơ bản mL (1 Chai = 500 mL), PNK nhập 16 Chai có 1 seri → PXK hiểu 1 seri = 1 mL, còn 7999 mL không seri. User: "nhập 16 chai có seri là 09012000 nhưng khi tạo phiếu xuất kho nó lại lấy dvt là ml và tính là 1 seri và 7999 không seri". Chốt: **1 seri = 1 ĐVT lúc nhập kho** (lưu hệ số theo seri) + **ô SL lô PXK theo ĐVT dòng đề nghị** (Chai), sổ tồn / bảng lô PXK vẫn lưu ĐVT cơ bản
  - [x] P15a. BE migration `stock_serials.unit_factor` decimal(15,6) default 1 (SL cơ bản / seri) + backfill theo hệ số dòng PNK (`order_qty_base / order_qty`); entity fillable
  - [x] P15b. BE PNK: `serialMax` = SL lô (ĐVT đơn mua), câu lỗi bỏ "theo ĐVT cơ bản"; `writeStock` ghi `unit_factor`. FE `receiptRules.js` khớp
  - [x] P15c. BE PXK `lotOptions`: seri kèm `unit_factor`, phần không seri = SL − Σ hệ số seri (cả phần PXK nháp khác giữ)
  - [x] P15d. BE PXK `validateItems`: `lots.*.qty` theo ĐVT dòng → quy cơ bản; seri tính theo hệ số; bỏ luật "lô có seri SL nguyên"; câu lỗi theo ĐVT dòng. `prepare` trả `qty_pick` theo ĐVT dòng
  - [x] P15e. FE PXK `exportRules.js` + `ExportForm.vue`: ô SL lô / tồn / không seri / tổng hiện theo ĐVT dòng, tính seri theo hệ số (setSerials / autoSerials / suggestFefo / computeLines / popup / quét)
  - [x] P15f. FE chi tiết PXK + bản in: SL lô hiện theo ĐVT dòng (thẻ kho giữ ĐVT cơ bản)
  - [x] P15g. Spec PXK D5 / D8 / §6 cập nhật
  - [ ] P15h. User chạy migration + test PNK 46 / PXK HC-NT-018 — (27/11) user báo lỗi "Unknown column unit_factor" (Screenshot_73) do chưa migrate → Claude đã chạy riêng migration `2026_11_27_000003` bằng `--path` (KHÔNG chạy `2026_11_07_000003_set_purchase_delivery_notes_waiting_receipt_status` đang chờ, ngoài feature); backfill seri 149/150 HC-NT-018 = 500; prepare ĐNXK 36 trả đúng (LOT-9100: 8000 mL, 1 seri 500 + 7500 không seri). Còn chờ user test trình duyệt
- [x] P16. (27/11) Duyệt PXK xong phải về màn danh sách. User: "khi tôi duyệt phiếu xuât kho thì phải quay ra màn danh sách chứ"
  - [x] P16a. `ExportForm.vue` `save()`: Lưu nháp + Duyệt xuất kho (tạo / sửa) → `/warehouse/exports` (như PNK `ReceiptForm` và ĐNXK P13), thay vì sang màn chi tiết
  - [x] P16b. `ExportDetail.vue` `doApprove()`: duyệt thành công → `/warehouse/exports`; lỗi thì ở lại tải lại như cũ
  - [x] P16c. Spec §11 footer ghi hành vi điều hướng

### Checkpoint — 27/11/2026
Vừa hoàn thành: P15a–g — `stock_serials.unit_factor` (migration + backfill, PNK ghi hệ số), PXK BE `lotOptions` / `validateItems` / `prepare` / duyệt theo ĐVT dòng + hệ số seri, FE `exportRules.js` (lineFactor / toLine / serF / serBase, setSerials(line, lot, ids, capBase), autoSerials(line, …), suggestFefo, computeLines `sum` cơ bản + `sum_q` ĐVT dòng), `ExportForm.vue` (cột ĐVT, SL đề nghị, tồn, tổng, popup seri / quét theo hệ số), `ExportDetail.vue` + `printExport.js` theo ĐVT dòng; spec D5 / D8 / §6 / §7 / §8 / §10b / §11
Đang làm dở: —
Bước tiếp theo: user chạy `php artisan module:migrate Warehouse` rồi test PNK 46 → PXK HC-NT-018 (16 Chai có seri). Danh sách PXK cột "Tổng SL" vẫn Σ ĐVT cơ bản (chưa đổi, hỏi user)
Blocked:

### Checkpoint — 26/11/2026
Vừa hoàn thành: FE4 màn chi tiết PXK (`exports/components/ExportDetail.vue`, `exports/_id/index.vue`), FE5 bản in 02-VT (`exports/printExport.js`), FE6 nối ĐNXK chi tiết (tab Phiếu xuất kho, nút Lập PXK / Mở PXK nháp / Đóng phần còn lại, banner đã đóng, cột Đã đóng)
Đang làm dở:
Bước tiếp theo: user chạy seeder quyền rồi test luồng (T1, T2); sửa theo phản hồi
Blocked:
