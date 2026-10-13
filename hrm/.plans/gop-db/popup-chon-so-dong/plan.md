# Plan — Popup chọn: số dòng/trang 10 / 20 / 50 / 100

Tóm tắt: `design.md`

## Phạm vi (lập 2026-10-06)

Lệnh lập phạm vi (hrm-client, nhánh `gop_db`):
1. `python3 .claude/skills/new-screens-sweep/inventory.py --root hrm-client --kind modal --has "V2BasePagination|page-size-options|pageSizeOptions|V2BaseDataTable"` → 48 popup có phân trang (lẫn popup xem)
2. Lọc popup CHỌN: file có `<V2BaseModal|b-modal>` + phân trang + `$emit` sự kiện chọn (`select|choose|apply|picked|selected|event`) — script `pick.py` (scratchpad)
3. Bổ sung theo tên file `*Search*Modal|*Picker*|Choose*Modal|Popup*` có V2Base (bắt thêm `QuotationProductSearchModal`, `customer-care/*SearchModal`)

Lệnh VERIFY (phải RỖNG): mọi file trong danh sách dưới phải import `pickerPagination`:
```bash
cd hrm-client && grep -L "pickerPagination" $(sed -n 's/^- \[.\] `\(.*\)`.*/\1/p' ../.plans/gop-db/popup-chon-so-dong/plan.md)
```

### Tasks
- [x] Tạo `utils/pickerPagination.js`
- [x] Màn mẫu: `pages/finance/bill-income-reports/components/ExportRequestSearchModal.vue`

Components dùng chung:
- [x] `components/finance/prepick/PrepickStockSearchModal.vue` (đổi default prop 20/[20,50,100])
- [-] `components/finance/prepick/PrepickLotSearchModal.vue` — BỎ: không phân trang (docblock: danh sách ngắn)
- [x] `components/finance/declare-debt/DeclareDebtContractPicker.vue`
- [x] `components/modals/ChooseErpCustomerModal.vue` ([10,25,50,100])
- [x] `components/customer-care/CustomerEquipmentPickerModal.vue` (phân trang phía FE, hằng PAGE_SIZE)

Assign / CSKH:
- [x] `pages/assign/quotations/components/QuotationProductSearchModal.vue` (popup chọn hàng hoá dùng chung)
- [x] `pages/customer-care/device-errors/components/CostSearchModal.vue`
- [x] `pages/customer-care/services/components/GroupSearchModal.vue`
- [x] `pages/customer-care/services/components/ProductSearchModal.vue`
- [x] `pages/customer-care/wr-quotations/components/InformationRequestSearchModal.vue`

Finance:
- [x] `pages/finance/addition-accounting-requests/components/RecordSearchModal.vue`
- [x] `pages/finance/bill-adjust-depts/components/BillAdjustDeptRequestPickerModal.vue`
- [x] `pages/finance/bill-adjust-depts/components/ContractPickerModal.vue`
- [x] `pages/finance/bill-adjust-depts/components/ExportRequestSearchModal.vue`
- [x] `pages/finance/bill-adjust-depts/components/ObjectSearchModal.vue`
- [x] `pages/finance/bill-income-reports/components/ExportRequestSearchModal.vue`
- [x] `pages/finance/bill-income-reports/components/ProductExportSearchModal.vue`
- [x] `pages/finance/bill-income-requests/components/ContractSearchModal.vue`
- [x] `pages/finance/bill-income-requests/components/SupplierSearchModal.vue`
- [x] `pages/finance/bill-incomes/components/IncomeRequestSearchModal.vue`
- [x] `pages/finance/bill-payment-authorizations/components/PaymentRequestSearchModal.vue`
- [x] `pages/finance/bill-payments/components/PaymentRequestSearchModal.vue`
- [x] `pages/finance/borrow-export-requests/components/ExportRequestPickerModal.vue`
- [x] `pages/finance/borrow-exports/components/BorrowExportRequestPickerModal.vue`
- [x] `pages/finance/borrow-extend-requests/components/BorrowPickerModal.vue`
- [x] `pages/finance/borrow-sell-requests/components/ContractPickerModal.vue`
- [x] `pages/finance/prepick-cancels/components/RequestSearchModal.vue`
- [x] `pages/finance/prepick-transfer-requests/components/ContractSearchModal.vue`
- [x] `pages/finance/product-export-requests/components/ContractSearchModal.vue`
- [x] `pages/finance/product-import-direct-transfers/components/StockSearchModal.vue`
- [x] `pages/finance/product-import-requests/components/ExportRequestSearchModal.vue`
- [x] `pages/finance/product-imports/components/ProductImportRequestSearchModal.vue`
- [x] `pages/finance/product-imports/components/WarehouseImportSearchModal.vue`
- [x] `pages/finance/product-prepick-requests/components/ContractSearchModal.vue`

Chờ user chốt:
- [ ] `pages/assign/meeting/components/PopupStaff.vue` — đang `[10, 25, 50, 100, 1000]` (1000 để chọn hàng loạt nhân sự?)

Ngoài phạm vi (không có phân trang): `assign/contracts/ContractQuotationSearchModal`,
`customer-care/wr-quotations/SelectPrintTemplateModal`, `finance/borrow-sell-requests/ExportRequestPickerModal`,
`finance/product-export-requests/{EmplementContract,FirmContract,TransferRequest}SearchModal`,
`components/customer-care/ChooseEquipmentTypeModal`.

- [ ] Verify grep rỗng · `git diff --stat` không đụng file ngoài danh sách · Playwright mở thử vài popup
- [x] Cập nhật skill: trỏ `utils/pickerPagination.js` (modal-popup §4b, list-page, erp-to-hrm-screen) + sửa comment `V2BasePagination.vue`

### Checkpoint — 2026-10-06
Vừa hoàn thành: 32 popup + `AccountingPrepickCancelForm` (bỏ prop đè) + comment `V2BasePagination`. Verify:
không file nào thiếu `pickerPagination`, không còn `[20, 50, 100]` / `[10, 25` / `[10, 20, 50]`, không import thừa,
36 file qua kiểm cú pháp (vue-template-compiler + @babel/parser). Hằng đóng băng (`Object.freeze`).
Đang làm dở: —
Bước tiếp theo: user chốt (1) PopupStaff `[…, 1000]`; (2) 8 popup chỉ có nút Trước/Sau, chưa có ô chọn số
dòng: `bill-adjust-depts/{ContractPicker,ExportRequestSearch,ObjectSearch}Modal`, `borrow-extend-requests/BorrowPickerModal`,
`borrow-sell-requests/ContractPickerModal`, `product-import-requests/ExportRequestSearchModal`,
`product-imports/{ProductImportRequest,WarehouseImport}SearchModal` — nay mặc định 10 (3 popup bill-adjust + borrow-sell
trước là 20) mà user không đổi được; (3) kiểm Playwright (client :3000 + API :8000 đang tắt).
Blocked: chờ user
