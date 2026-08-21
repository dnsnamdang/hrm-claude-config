# Phase 3 — Khảo sát luồng CÓ dữ liệu chờ duyệt (DB dev erp2326)

> Đếm toàn hệ thống (chưa lọc company). Ưu tiên backfill luồng count>0 + là "duyệt" thật.

| # | Luồng | Model | Trạng thái "chờ duyệt" | Count | Ghi chú |
|---|---|---|---|---|---|
| 1 | Quyết toán HĐ | `App\Model\Sale\SettlementContract` | DOI_TP_DUYET=2 · DOI_BGD_DUYET=3 · DOI_KT_DUYET=4 (DA_DUYET=5 mới xong) | **283** | Multi-step 3 cấp TP→BGD→KT |
| 2 | Đề nghị thanh toán | `App\Model\IncomeExpenditure\BillPaymentRequest` | AWAITING_MANAGE=2 · ACCOUNTING_DEPT=3 · CHIEF_ACCOUNTANT=4 · BOARD_OF_MANAGER=5 · CREATE_BILL=6 | **128** | 5 bước; status=6 (93 phiếu) = "đợi tạo phiếu chi" — cân nhắc có tính "duyệt" không |
| 3 | Chuyến xe | `App\Model\Warehouse\DeliveryTrip` | status=1 (CHUA_THANH_TOAN) | 111 | ⚠️ "chờ HẠCH TOÁN" không phải duyệt — cân nhắc bỏ |
| 4 | YC sửa chữa BH | `App\Model\Customers\WarrantyRepairRequest` | STATUS_WAITING_HANDLE=2 | 106 | ⚠️ "chờ XỬ LÝ" không phải ký duyệt — cân nhắc bỏ |
| 5 | YC nhập hàng | `App\Model\Warehouse\ProductImportRequest` | CHO_DUYET=2 (33) · CHO_TP_DUYET=12 (4) | **37** | Multi-level |
| 6 | HĐ trong nước | `App\Model\Order\InlandBuyContractNew` | CHO_DUYET=2 (all type=tự do) | **25** | |
| 7 | YC xuất hàng | `App\Model\Warehouse\ProductExportRequest` | CHO_DUYET=2 (19) · DOI_TP_DUYET=10 (1) · DOI_BGD_DUYET=11 (2) | **22** | Multi-level (status = cấp) |
| 8 | Phiếu thu tiền | `App\Model\IncomeExpenditure\BillIncome` | STATUS_AWAITING_APPROVE=2 | 9 | |
| 9 | PI nhập khẩu | `App\Model\Order\PurchaseInvoice` | CHO_DUYET=2 | 3 | |
| 10 | Phiếu chi | `App\Model\IncomeExpenditure\BillPayment` | STATUS_AWAITING_APPROVE=2 · ACCOUNTING_APPROVE=5 | 2 | |
| — | Báo giá dự án | `App\Model\Sale\ProjectQuotation` | CHO_DUYET=4 | **0** | Đã backfill (P3-1); chưa có data |

## Bài học quan trọng
- **"Chờ duyệt" = UNION nhiều status** cho luồng nhiều bước (settlement, bill_payment_request, product_export/import). Mỗi status = 1 cấp → map status → `required_permission` + `level` (khác firm_contract dùng approver_id).
- Quyền/status THẬT phải lấy từ model + `HomeController@approveList` (survey/config đoán có thể SAI — vd project_quotation quyền thật "Duyệt báo giá dự án" chứ không phải "Duyệt báo giá").
- Vài luồng KHÔNG phải "ký duyệt" (delivery_trip=chờ hạch toán, warranty_repair=chờ xử lý, bill_payment_request status=6=đợi tạo phiếu chi) → cân nhắc bỏ/không tính.

## Thứ tự đề xuất làm (duyệt thật + có data)
1. product_export_request (22, multi-level status → cấp) — mẫu multi-level theo status
2. product_import_request (37)
3. inland_buy_contract (25)
4. settlement_contract (283) — 3 cấp
5. bill_payment_request (128) — 5 bước (chốt status=6 có tính không)
6. bill_income (9) · purchase_invoice (3) · bill_payment (2) — đơn giản
