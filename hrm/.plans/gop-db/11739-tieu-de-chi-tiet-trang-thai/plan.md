# #11739 — [ERP => HRM] Đồng bộ trạng thái trong xem chi tiết

Phụ trách: @khoipv · Phân hệ: Tài chính · Nhánh: develop (từ gop_db)
Redmine: http://quanly.dnsmedia.vn/issues/11739

Yêu cầu: tiêu đề màn xem chi tiết hiển thị dạng `Chi tiết <tên màn>: <mã phiếu (nếu có)> <Badge trạng thái>`.

Khuôn đã có (37 màn): `utils/page-title-status.js::buildStatusTitle(title, statusName, hex)` → pageTitle (v-html top-menu),
tab trình duyệt dùng chữ trơn. Mẫu: `pages/finance/division-market-departments/_id/index.vue`.

Phạm vi (lệnh): `for f in pages/finance/*/_id/index.vue; do grep -q buildStatusTitle $f || echo $f; done`
Verify: lệnh trên phải chỉ còn các màn ghi "bỏ qua" bên dưới.

## Tasks
- [x] Thêm export mới `statusTypeHex(type)` vào utils/page-title-status.js (BE nhiều phiếu trả status_type bootstrap thay vì hex) — không đổi buildStatusTitle
- [x] Màn mẫu: finance/bill-incomes/_id/index.vue
- [x] Áp đồng loạt các màn còn lại (subagent theo lô)
- [x] Verify bằng lệnh phạm vi + compile template
- [x] pages/finance/accounting-prepick-cancels/_id/index.vue (bỏ qua — phiếu không có trạng thái)
- [x] pages/finance/accounts/_id/index.vue
- [x] pages/finance/addition-accounting-requests/_id/index.vue
- [x] pages/finance/bill-adjust-dept-requests/_id/index.vue
- [x] pages/finance/bill-adjust-depts/_id/index.vue
- [x] pages/finance/bill-income-reports/_id/index.vue
- [x] pages/finance/bill-income-requests/_id/index.vue
- [x] pages/finance/bill-incomes/_id/index.vue
- [x] pages/finance/bill-payment-authorizations/_id/index.vue
- [x] pages/finance/bill-payment-requests/_id/index.vue
- [x] pages/finance/bill-payments/_id/index.vue
- [x] pages/finance/borrow-export-requests/_id/index.vue (user chốt 13/11 gắn badge, thay quyết định 05/09)
- [x] pages/finance/borrow-exports/_id/index.vue
- [x] pages/finance/borrow-extend-requests/_id/index.vue
- [x] pages/finance/business-target-departments/_id/index.vue
- [x] pages/finance/business-target-employees/_id/index.vue
- [x] pages/finance/buy-service-accounting-requests/_id/index.vue
- [x] pages/finance/buy-service-accountings/_id/index.vue
- [x] pages/finance/buy-service-requests/_id/index.vue
- [x] pages/finance/closing-entries/_id/index.vue (bỏ qua — không có trạng thái)
- [x] pages/finance/declare-debt-beginnings/_id/index.vue (bỏ qua — không có trạng thái)
- [x] pages/finance/declare-debt-supplier-beginnings/_id/index.vue (bỏ qua — không có trạng thái)
- [x] pages/finance/inventory-audit-reports/_id/index.vue
- [x] pages/finance/inventory-exports/_id/index.vue
- [x] pages/finance/inventory-imports/_id/index.vue
- [x] pages/finance/prepick-cancel-requests/_id/index.vue
- [x] pages/finance/prepick-cancels/_id/index.vue
- [x] pages/finance/prepick-extend-requests/_id/index.vue
- [x] pages/finance/prepick-transfer-requests/_id/index.vue
- [x] pages/finance/price-calculates/_id/index.vue
- [x] pages/finance/product-import-direct-transfers/_id/index.vue
- [x] pages/finance/product-prepick-requests/_id/index.vue
- [x] pages/finance/product-transfer-requests/_id/index.vue
- [x] pages/finance/product-transfers/_id/index.vue
- [x] pages/finance/self-inventory-request-alls/_id/index.vue
- [x] pages/finance/self-inventory-requests/_id/index.vue (user chốt 13/11 gắn badge trên title, thân form vẫn không có trạng thái)
- [x] pages/finance/service-accounting/_id/index.vue
- [x] pages/finance/transfer-product-allocations/_id/index.vue
- [x] pages/finance/warehouse-export-requests/_id/index.vue
- [x] pages/finance/warehouse-prepick-requests/_id/index.vue
- [x] pages/finance/wr-accounting-service-requests/_id/index.vue
- [x] pages/finance/wr-accounting-services/_id/index.vue
- [x] Thêm: 4 màn đã có badge từ trước (borrow-sell-requests, borrow-sells, product-import-requests, product-imports) đẩy HTML vào tab trình duyệt → tách plainTitle
- [x] BE: TransferProductAllocation thêm STATUSES/statusMeta + status_text/status_color trong getData() (chữ "Đã phân bổ"/"Đang tạo", màu tự chọn — chờ user chốt)
- [x] BE: PrepickCancelService::detailData() trả thêm status/status_name/status_color (theo statusMeta như list)
- [x] FE form: BusinessTargetDepartmentForm / BusinessTargetEmployeeForm emit thêm status_text/status_color
- [x] Chốt 13/11: user đồng ý gắn badge cả 5 màn có quyết định cũ trái quy tắc

Verify: vue-template-compiler + @babel/parser 42 file sạch; php -l sạch. Chưa mở trình duyệt.

### Checkpoint — 2026-11-13
Vừa hoàn thành: 35 màn chi tiết Tài chính có tiêu đề "Chi tiết <tên>: <mã>" + badge trạng thái
Đang làm dở: không
Bước tiếp theo: user chốt chữ/màu trạng thái Phân bổ hàng (đang "Đã phân bổ"/"Đang tạo" xám, ERP "Đã duyệt"/đỏ); user mở trình duyệt kiểm
Blocked:

- [x] Commit + push `develop` (13/11/2026): hrm-api `288108f40`, hrm-client `2651bb4fd` (2 commit tách #11739 / #11736, rebase trên origin/develop sạch)
