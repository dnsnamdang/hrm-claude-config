# Plan — Đơn mua hàng sửa theo demo

> Người phụ trách: @khoipv · Bắt đầu: 21/10/2026
> Spec: `docs/superpowers/specs/2026-10-21-don-mua-hang-theo-demo-design.md`

## Phase 0 — Chuẩn bị
- [x] 1. Brainstorming: chốt phạm vi (4 tab: Thông tin chung · Hàng hóa · Giao nhận & vận chuyển · Điều khoản thanh toán), so màn thật với demo
- [x] 2. Viết spec chi tiết + design tóm tắt (user cho "làm như demo", không chờ duyệt)
- [x] 3. Lên plan chi tiết theo Phase → BE/FE

## Phase 1 — BE: DB + Entity
- [x] 1.1 Migration thêm cột `purchase_orders` (+ backfill `buyer_company_id`, ánh xạ `ship_method` cũ)
- [x] 1.2 Migration thêm `purchase_order_products.purchase_contract_product_id`
- [x] 1.3 Migration bảng `purchase_delivery_points`, `purchase_delivery_costs`
- [x] 1.4 Entity `PurchaseDeliveryPoint`, `PurchaseDeliveryCost`; `PurchaseOrder` thêm STATUS_DONE, SHIP_*, quan hệ, accessor `dest`, `is_can_confirm`

## Phase 2 — BE: Service + API
- [x] 2.1 `PurchaseOrderService`: `headerData` loại mảng mới; tính phí; sync points/costs; copy `buyer_company_id` xuống dòng
- [x] 2.2 Bỏ cấp phát nhu cầu cho dòng theo HĐ TM
- [x] 2.3 API `contracts`, `contract-pool/{id}` (tính bought/remain), `unproposed-goods`, `warehouses`, `customer-addresses`, `employees`
- [x] 2.4 API `confirm-received`, `points/{point}/delivered` → status 6
- [x] 2.5 `StorePurchaseOrderRequest`: rule mới, chặn vượt còn lại, hàng nội bộ khi giao KH, bỏ required cũ
- [x] 2.6 `DetailPurchaseOrderResource` + list resource trả thêm trường
- [x] 2.7 Status 6 ở `SupplyReportService::purchaseDocMeta`, `productSupplierMap` và các chỗ lọc status DMH

## Phase 3 — FE
- [x] 3.1 `constants.js`: status 6, SHIP_METHOD mới, COST_NAMES / CARRIERS
- [x] 3.2 `PurchaseOrderForm.vue`: 4 tab, defaultForm, payload, tabOfKey, nạp HĐ
- [x] 3.3 `GeneralTab.vue` theo demo §12
- [x] 3.4 `ShipTab.vue` mới
- [x] 3.5 `GoodsPickerModal.vue` 2 chế độ
- [x] 3.6 `ProductsTab.vue`: bỏ Cty mua, chip, khoá dòng HĐ, chặn vượt, tổng NCC
- [x] 3.7 `PaymentTab.vue`: nạp từ HĐ, khối chi phí VC đơn vị VC
- [x] 3.8 `_id/index.vue`: nút xác nhận nhận/giao; `index.vue`: status 6, cột HĐ mua / Cty mua

## Phase 4 — Kiểm tra
- [x] 4.1 `php -l` các file BE, chạy migrate
- [x] 4.2 Kiểm tra cú pháp FE (máy không có eslint local — dùng vue-template-compiler parse template + script các file sửa: OK); `php -l` BE OK
- [x] 4.4 Đổi thứ tự tab: Điều khoản thanh toán lên trước Giao nhận & vận chuyển (cả thứ tự nhảy tab khi có lỗi)
- [x] 4.5 Bỏ số tiền mặc định 1.500.000 của chi phí vận chuyển — để trống cho người dùng tự nhập (BE đã báo "Số tiền phải lớn hơn 0." khi bỏ trống)
- [x] 4.6 Chọn HĐ mua → khoá ô Công ty mua (= Bên A của HĐ), Mã NCC, MST (lấy theo NCC của HĐ); BE ép buyer_company_id = main_company_id của HĐ; bỏ cảnh báo "Công ty mua ≠ Bên A"
- [x] 4.7 Bỏ chọn HĐ mua (về đơn lẻ) → xoá Công ty mua + NCC (kèm Mã NCC, MST, địa chỉ, người liên hệ) đã lấy theo HĐ cũ
- [x] 4.8 Popup chọn hàng (GoodsPickerModal) phân trang ở FE 20/50/100 dòng như popup HĐ mua — giữ lựa chọn qua các trang, checkbox đầu bảng theo trang
- [x] 4.9 Tăng tốc BE `PurchaseContractService::unproposedGoodsOf`: tra hệ số ĐVT 1 lần cho mọi HĐ thay vì từng HĐ (8,7s → ~2,5s, vẫn 3.912 dòng) — dùng chung cho popup đơn mua + HĐ mua
- [x] 4.10 Popup chọn hàng đơn mua lẻ: hàng HĐ bán chưa tạo phiếu đề xuất gom thành nhóm cuối bảng (dòng tiêu đề nhóm, nguồn "HĐ bán · chưa đề xuất", ghi chú riêng, thêm lọc Nguồn) như khi chọn HĐ mua
- [x] 4.11 Popup chọn hàng: cột "SL còn lại HĐ bán" (SL HĐ bán gồm phụ lục − đã mua trên HĐ mua TM + đơn mua lẻ/NT, tính cả Nháp/Chờ duyệt; BE `SaleContractRemainService`) + dòng Tổng, như demo
- [x] 4.12 Popup chọn hàng đơn lẻ: bỏ 2 khung ghi chú (nguồn Cần đi mua + hàng HĐ bán chưa đề xuất) → chuyển thành tooltip ⓘ ở cột "Còn cần mua" và dòng tiêu đề nhóm
- [x] 4.13 Popup chọn hàng: ô tìm gõ bị trễ → sắp xếp + chuỗi tìm dựng 1 lần (Intl.Collator), lọc sau khi ngừng gõ 250ms; bộ lọc dùng chung size md (ô tìm chốt 34px bằng select)
- [x] 4.14 Popup chọn hàng: ghi chú giao thẳng KH → tooltip ⓘ cột "Khách hàng SD"; ghi chú hàng HĐ bán chưa đề xuất (chế độ HĐ mua) → tooltip ⓘ dòng tiêu đề nhóm (nội dung theo chế độ)
- [x] 4.15 Tab Thông tin chung: nút thêm nhanh người liên hệ chuyển thành icon ⊕ (mdi-plus-circle plus-icon) cạnh nhãn như màn sale/project/add; chưa chọn NCC thì mờ + tooltip "Chọn nhà cung cấp trước"
- [x] 4.16 Kho nhận: lấy toàn bộ kho vật lý đang hoạt động (bảng `warehouses`), bỏ lọc theo Công ty mua + bỏ watcher xoá kho khi đổi Công ty mua
- [x] 4.17 Thủ kho tiếp nhận: đổi ô hiển thị thành ô chọn (thủ kho của kho nhận, `warehouses.stockers`); cột mới `purchase_orders.warehouse_keeper_id` (migration 2026_10_21_000004, index, không FK); BE kiểm thủ kho thuộc kho; đổi kho → bỏ thủ kho cũ, kho có 1 thủ kho thì chọn sẵn; chi tiết đơn hiện thủ kho. Kèm sửa `headerData` loại các khoá chỉ hiển thị (`warehouse_keeper`, `pickup_employee_name`…) — trước đó bị fill vào model → lỗi Unknown column khi lưu
- [x] 4.18 Dropdown "Hợp đồng mua" ở form lập/sửa đơn chỉ hiện HĐ còn SL chưa mua: API `contracts?available=1` bỏ HĐ thương mại đã duyệt có tổng (SL HĐ − đã mua) ≤ 0 theo từng dòng × mục đích (HĐ nguyên tắc luôn giữ); sửa đơn truyền `exclude_order_id` (không tính SL của chính đơn) + `include_ids` (giữ HĐ đang gắn). Bộ lọc màn danh sách vẫn lấy đủ HĐ
- [ ] 4.3 User test tay trên trình duyệt (tạo đơn lẻ / theo HĐ TM / HĐ NT, giao thẳng KH, xác nhận nhận/giao)

### Checkpoint — 2026-10-21
Vừa hoàn thành: 3.5–3.8 (popup chọn hàng 2 chế độ, ProductsTab bỏ Cty mua + chip HĐ/còn lại + khoá giá/CK/ĐVT dòng HĐ + khối tổng phí VC, PaymentTab tổng NCC + khối phí trả ĐVVC, chi tiết có khối Giao nhận + xác nhận nhận/giao, danh sách cột + lọc HĐ mua / Công ty mua); BE thêm rule `carrier_pay_when`, lọc `purchase_contract_ids` (0 = đơn lẻ)
Đang làm dở: —
Bước tiếp theo: user test tay trên trình duyệt (4.3)
Blocked:
