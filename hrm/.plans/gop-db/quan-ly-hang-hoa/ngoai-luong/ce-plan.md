# Plan đợt C-e — N1: bảo hành / tồn tối thiểu theo công ty ở ERP — 13/10/2026

> Nguồn: `ce-khao-sat.md` (kiểm kê ~31 file sống + chốt C-e-1, C-e-2). ⏳ CHƯA được "làm".
> ERP worktree `wt-erp-2d1` — nhánh con `feat/ce-bao-hanh-ton-toi-thieu-cong-ty` từ `feat/2d1-erp-khong-loi`. DB `hrm_erp_giacty`.
> ⛔ Không merge vào `gop_db` (ERP lẫn HRM).

## Luật đọc (một nguồn)
Dòng `product_company_coefficients` của công ty liên quan; công ty CHƯA có dòng ⇒ lùi cột chung `products` (giống HRM `AdminData::source`;
có dòng ⇒ đọc dòng kể cả ô NULL). Chứng từ ⇒ `DocumentCompany::of/ofOrUser` (công ty chứng từ, bảng không có `company_id` ⇒ người lập).

## Task ERP
- [x] E1 Nền — `App\Product`: `adminRowFor(int $companyId)` (dùng quan hệ `company_coefficients` nếu đã nạp, không thì 1 query) +
  `guaranteeFor / guaranteeTypeFor / guaranteeDataFor / guaranteeDayFor / minStockQtyFor($companyId)`; tách phần tính ngày / chữ khỏi
  2 accessor cũ để dùng chung. Hàm SQL dùng chung `joinAdminRow($query, $alias, $companyId)` + biểu thức `COALESCE(pcc.col, products.col)`
  (khuôn `PriceSql` / `SearchController::onlyTradingProducts`). Model `ProductCompanyCoefficient` khai cast 3 ô.
- [x] E2 Nhóm A — chép vào chứng từ (17 file, 20 chỗ): đổi `$product->guarantee(_type)` ⇒ `*For($companyId)` với công ty đã tính sẵn cho giá
  ở cùng hàm (Quotation, Contract, ContractAdditionAnnex ×2, ServiceContractAdditionAnnex, ServiceQuotation ×2, ProjectQuotationGroup/Tab,
  ProjectAnalysisGroup — dòng có thể là TmpProduct ⇒ giữ cột của hàng tạm, FirmQuotation ×2, FirmContract, FirmQuotationService (nạp
  công ty phiếu), FirmContractService, PrincipleOrderService ×2, HandoverAcceptanceRecord (+ calculateWarrantyDays), 2 controller biên bản
  bàn giao (điền sẵn `warranty_time_days` / JSON — công ty hợp đồng).
- [x] E3 Nhóm B — hiển thị: chi tiết hàng hoá ERP (`products/formShow`, `product2/formShow`, `product_versions/show` — công ty người dùng,
  ô Bảo hành + SL tồn tối thiểu), recipe trong `getDataForEdit / getDataForVersion` (đã có `$companyId`), chi tiết bảo hành
  (`HandoverAcceptanceRecord::getData` — công ty biên bản), in báo giá mẫu (`QuotationTemplateProduct` — công ty người dùng như giá).
- [x] E4 Nhóm C — báo cáo:
  - Cảnh báo đặt hàng tồn kho (`Product::stockSearchData` :7717/:8190 + `WarehouseWarningReportController` + 2 view): tồn tối thiểu theo
    `company_id` của bộ lọc (Q-N1: chế độ tổng công ty ⇒ CỘNG các công ty).
  - Chuyển kho / tồn kho (`StockTransferReportService` 12 chỗ): tồn tối thiểu theo công ty đã chọn; **C-e-1: bắt buộc chọn công ty** —
    view `orders/reports/stock_transfer/index` bỏ lựa chọn "tất cả", mặc định công ty người dùng, báo lỗi nếu trống; BE `searchData` /
    `printList` / `exportList` (+ `StockTransferReportMailJob`) thiếu `company_id` ⇒ trả lỗi rõ, không chạy gộp.
  - CSKH + Tổng hợp bán hàng: **KHÔNG sửa** (C-e-2) — ghi N90.
- [x] E5 Nhóm E — API/JSON: `SearchController::searchProductStockBuyer(Api)` `time_guarantee` ⇒ `guaranteeDataFor($companyId)`;
  `Product::dataFor / getData` `guarantee_data` ⇒ theo `$companyId`. `select('products.*')` thô: không sửa (không JS đọc) — ghi chú.
- [x] E6 PHPUnit (sqlite :memory:): helper (có dòng / dòng NULL / chưa dòng ⇒ lùi cột chung; ngày theo ngày/tháng/năm); 1–2 luồng chép
  (Quotation::syncProducts, ServiceQuotation) dùng công ty phiếu, không dùng công ty người dùng; báo cáo chuyển kho thiếu công ty ⇒ lỗi.
  + cả bộ ERP.

## Kiểm
- Dữ liệu thử (transaction/tự dọn): 1 hàng có pcc công ty 1 bảo hành ≠ cột chung, công ty 2 chưa dòng.
- Playwright ERP 8090 (role tạm, gỡ khi xong): báo giá công ty 1 thêm hàng đó ⇒ dòng mang bảo hành công ty 1; chi tiết hàng hoá ERP hiện
  số công ty đang làm việc; Cảnh báo đặt hàng tồn kho 1 công ty / tổng công ty (cộng); Chuyển kho: không chọn công ty ⇒ bị chặn, chọn ⇒
  tồn tối thiểu đúng công ty; console sạch.
- Checksum bảng chứng từ không đổi ngoài dữ liệu thử; bảng quyền về mốc.

## Ghi lại (không làm)
- N90: Báo cáo CSKH (`CustomerCareReportService`) + Tổng hợp bán hàng (`SummarySaleReportService`) vẫn đọc bảo hành cột chung — user tính sau.
- `database/seeds/SyncImageProductToCRM` (seeder 1 lần) không sửa.

## Phạm vi xin "làm"
| | |
|---|---|
| Repo / nhánh | ERP `wt-erp-2d1`, nhánh `feat/ce-bao-hanh-ton-toi-thieu-cong-ty` từ `feat/2d1-erp-khong-loi`; merge LOCAL, push khi user báo; ⛔ không vào gop_db |
| File | ~28 file: Product.php, ProductCompanyCoefficient, ~17 file chép chứng từ (nhóm A), formShow ×2 + product_versions/show, QuotationTemplateProduct, HandoverAcceptanceRecord, SearchController, Product::stockSearchData + WarehouseWarningReportController (+2 view), StockTransferReportService + StockTransferReportController + StockTransferReportMailJob + view stock_transfer/index, test mới |
| DB | `hrm_erp_giacty`: chỉ đọc + dữ liệu thử tự dọn + role tạm Playwright. Không migration/seeder/quyền mới |

### Kết quả thực hiện — 2026-10-13
- ERP `feat/ce-bao-hanh-ton-toi-thieu-cong-ty` `39b38e4a20` ⇒ merge LOCAL `d7226cd1b9` vào `feat/2d1-erp-khong-loi` (CHƯA push; kiểm: không nằm trong `origin/gop_db`).
- **Tự chốt khi làm**: chỉ đọc dòng khi công ty ĐANG DÙNG hàng (`status` NOT NULL) — 298 dòng hệ số cũ status NULL, 23 dòng trong đó bảo hành trống trong khi cột chung có số ⇒ đọc nguyên luật "có dòng ⇒ dòng" sẽ làm chứng từ ERP mất bảo hành so với hôm nay. (HRM `AdminData::source` hiện vẫn đọc mọi dòng — lệch nhẹ ở đúng 23 ca này, ghi N91.)
- Ngoài kiểm kê: `product_versions/show` là màn chết ("Đang phát triển") — bỏ; RuleContract / RuleContractAnnex chép từ dòng báo giá (không đọc hàng hoá) — bỏ; bản in báo giá / HĐ đọc accessor của DÒNG chứng từ — không đổi. Cảnh báo đặt hàng tồn kho thực tế luôn chạy theo 1 công ty (query `aw.company_id = công ty chọn`) ⇒ đọc theo công ty đó (không có chế độ cộng).
- Báo cáo Luân chuyển: FE thêm `company_id` vào điều kiện bắt buộc (nhãn `required-label`, lỗi dưới ô, toast) + chặn In / Xuất; BE `requireCompany()` ở `searchData` (JSON lỗi) / `printList` / `exportList` (quay lại + thông báo).
- PHPUnit: `CeCompanyGuaranteeMinStockTest` 9 ca (có dòng / chưa dòng / status NULL / để trống, quan hệ đã nạp 0 query, hàng tạm, SQL cùng luật, chi tiết, biên bản, chặn thiếu công ty); ERP **103/103**.
- Luồng chép THẬT (tinker, transaction rollback, giacty): `Quotation::syncProducts` báo giá #276 công ty 1 ⇒ dòng **3 năm** (dòng công ty), ép công ty 2 ⇒ **12 tháng**; rollback sạch (0 dòng).
- Playwright ERP 8090 (role tạm `CE_UAT_TMP` 118813 — đã gỡ; dữ liệu thử pcc 12891 công ty 1 = 3 năm / tồn 777, đã trả về 12 tháng / 30):
  chi tiết hàng 4011 ô Bảo hành 3 · Năm · SL tồn tối thiểu 777; Cảnh báo đặt hàng (POST thật) công ty 1 ⇒ 777, công ty 2 ⇒ 30; Luân chuyển: bỏ trống công ty ⇒ lỗi "Bắt buộc chọn" dưới ô + toast, KHÔNG gửi request; BE searchData thiếu công ty ⇒ `success:false` "Vui lòng chọn công ty để xem báo cáo"; printList thiếu công ty ⇒ chuyển hướng; có công ty: công ty 1 ⇒ 777, công ty 2 ⇒ 30 (~5–6s/lượt, join theo khoá unique `(product_id, company_id)`); popup chọn hàng báo giá: 4011 "3 Năm", hàng khác giữ "12 Tháng"; console không lỗi JS mới.
- Sau dọn: roles 130 · rhp 20.958 · ehr 1.718 về mốc; 0 dòng lệch pcc ↔ cột chung (như trước khi thử); server tắt đúng PID. Log ERP 1 lỗi DataTables do request thử thiếu `columns` (không phải code).

### Ghi lại thêm
- N90 (C-e-2): Báo cáo CSKH + Tổng hợp bán hàng vẫn đọc bảo hành cột chung — user tính sau.
- N91: HRM `AdminData::source` đọc cả dòng hệ số cũ status NULL (23 dòng bảo hành trống) — lệch ERP (ERP lùi cột chung). Cân nhắc đồng bộ luật khi xoá cột chung.

### Checkpoint — 2026-10-13 (C-e xong)
Vừa hoàn thành: E1–E6 + kiểm (PHPUnit 103/103, chép thật trong transaction, Playwright ERP).
Đang làm dở: không. Server 8090 tắt, role tạm gỡ, dữ liệu thử trả về.
Bước tiếp theo: (ĐÃ PUSH ERP `d7226cd1b9`) · C-f (N65 lệnh dọn + cron, N26 AUTO_INCREMENT runbook) · A7.
Blocked: —
