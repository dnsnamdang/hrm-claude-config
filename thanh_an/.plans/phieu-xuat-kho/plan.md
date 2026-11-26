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

### Checkpoint — 26/11/2026
Vừa hoàn thành: FE4 màn chi tiết PXK (`exports/components/ExportDetail.vue`, `exports/_id/index.vue`), FE5 bản in 02-VT (`exports/printExport.js`), FE6 nối ĐNXK chi tiết (tab Phiếu xuất kho, nút Lập PXK / Mở PXK nháp / Đóng phần còn lại, banner đã đóng, cột Đã đóng)
Đang làm dở:
Bước tiếp theo: user chạy seeder quyền rồi test luồng (T1, T2); sửa theo phản hồi
Blocked:
