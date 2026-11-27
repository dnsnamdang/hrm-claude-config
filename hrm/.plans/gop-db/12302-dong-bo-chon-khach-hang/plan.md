# #12302 [ERP => HRM] Đồng bộ lại UI chọn khách hàng (+ NCC) — @khoipv

Redmine: http://quanly.dnsmedia.vn/issues/12302 (Tài chính, Web App, mở 25/11/2026)
Yêu cầu: ô chọn KH ở form Tạo mới / Cập nhật đang 2 kiểu (popup ở `finance/bill-adjust-dept-requests/create`,
gõ 2 ký tự ở `sale/order-requests/add`) → đồng bộ 1 kiểu. Đồng bộ cả chọn NCC.
User chốt 27/11: **theo kiểu POPUP**.

## Khuôn
- Ô: `V2BasePickerInput` (skill select-and-input-state mục 2d) — `@open` mở popup, `@clear` dọn đủ dữ liệu kéo theo.
- KH: `components/modals/ChooseErpCustomerModal.vue` (id `choose-erp-customer`, bắn `event {type:'choiceCustomer', data}`;
  nguồn `assign/customers` all_business=1 status=1; `scope-all` khi nguồn cũ không giới hạn quyền).
- NCC: `pages/finance/bill-income-requests/components/SupplierSearchModal.vue` (prop `modalId`, bắn `choose(row)`;
  nguồn `finance/bill-income-requests/search-suppliers`, customers.is_supplier=1).
- Màn mẫu: `pages/sale/order-requests/components/OrderRequestForm.vue` + `OrderRequestProductRow.vue`.

## Phạm vi (lệnh kiểm kê)
`grep -rnE -A12 "<V2BaseSelectRemote" pages components | grep fetch` + grep `:options=".*(customer|supplier)"`
→ lọc tay: chỉ form Tạo/Sửa (bỏ ô lọc ở màn danh sách / báo cáo).

Không đổi (giữ nguyên, lý do):
- `finance/prepick-cancel-requests` — chỉ KH của NV giữ hàng (`employee_id`), popup chung không lọc được
- `finance/addition-accounting-requests` ô NCC `supplierChoices` — chọn trong vài NCC của chứng từ nguồn
- `finance/product-import-requests` `fetchPartners`, `components/finance/declare-debt` `fetchObjects` — đối tượng hỗn hợp (KH/NCC/NV…)
- `components/product/detail/ProductTabAdmin.vue` — chỉ xem
- Ô lọc trên danh sách / báo cáo / popup báo cáo (ngoài phạm vi "tạo mới và cập nhật")

## Tasks
- [x] Đọc issue, kiểm kê màn, chốt kiểu popup
- [x] Màn mẫu: Yêu cầu đặt hàng (`sale/order-requests`) — ô KH từng dòng → popup
- [x] Lô A (KH): inland-order-requests, product-prepick-requests, prepick-transfer-requests, delivery-cost-asking-requests, firm-warranty-requests
- [x] Lô B (NCC Tài chính): buy-service-accounting-requests, buy-service-requests, buy-service-accountings, product-exports/create, product-imports (CostTable + ProductImportForm), warehouse-imports (ArrangeDeliveryForm + _id/barcode)
- [x] Lô C (NCC khác): master-data/vehicles AddVehicleModal, transport/delivery-contracts ContractForm, transport/delivery-cost-summaries ImportQuotationModal, customer EquipmentTab, AddExternalEquipmentModal, ProductFormAdmin, ProductBarcodeModal
- [x] Verify: compile toàn bộ file sửa (vue-template-compiler + babel), grep không còn V2BaseSelectRemote KH/NCC trong phạm vi

### Kết quả 27/11
- 21 file FE đã đổi, `vuecheck.js` OK 21, không còn hàm fetchCustomers/fetchSuppliers thừa. Chưa test trình duyệt.
- **Bỏ qua** `finance/buy-service-requests` (Yêu cầu mua dịch vụ): API cũ lọc NCC `status=1` (quy tắc ERP), popup `search-suppliers` không lọc status → cần thêm tham số BE (`only_active`) nếu muốn đổi. CHỜ USER.
- Khác hành vi cần user biết:
  - Xe (`master-data/vehicles`) + Hàng hoá (`ProductFormAdmin`): API cũ chỉ NCC hoạt động, popup ra cả NCC khoá.
  - Bảo hành hãng + Hỏi giá vận chuyển: API cũ ra cả bản ghi thuần NCC, popup KH chỉ `is_customer=1`.
  - Hạch toán mua DV + Thêm thiết bị ngoài: trước chỉ nạp 50 NCC đầu, nay tìm được toàn bộ.

### Checkpoint — 2026-11-27
Vừa hoàn thành: đổi ô chọn KH/NCC 21 file sang V2BasePickerInput + popup
Đang làm dở: —
Bước tiếp theo: user test trình duyệt; chốt có sửa BE để đổi màn Yêu cầu mua dịch vụ + lọc NCC khoá không
Blocked: chờ quyết định user

### Bổ sung 27/11 (user chốt: sửa cả 2 mục)
- [x] BE `BillIncomeRequestService::searchSuppliers` nhận `only_active=1` → `status = 1` (không gửi thì như cũ). tinker: 9547 / 9537
- [x] FE `SupplierSearchModal` thêm prop `onlyActive` (hàm dùng chung — user đồng ý)
- [x] Bật `only-active` cho Xe (`AddVehicleModal`) + Hàng hoá (`ProductFormAdmin`)
- [x] Đổi Yêu cầu mua dịch vụ (`BuyServiceRequestForm` + `BuyServiceDetailTable`) sang popup `only-active`, modal id `choose-buy-service-supplier`
- vuecheck OK 5, php -l OK. Chưa test trình duyệt.
