# #11937 — Popup chọn hàng báo giá: SL KM có thể xuất, SL có thể lắp ráp, "Toàn bộ tồn kho"

Redmine: http://quanly.dnsmedia.vn/issues/11937 · @junfoke · Logic ở `hrm-api` (ERP chỉ hiển thị qua proxy)

## Ngày 30/10/2026 (@junfoke)
- [x] 30/10/2026 — Tạo nhánh `task_11937` từ `gop_db` (TanPhatDev + hrm-api worktree `.worktrees/gop-db`). Theo user: logic đã chuyển hết sang HRM → làm ở HRM, không làm lẫn 2 bên; merge `develop` → `gop_db` ở hrm-api (conflict `ProductExportService.php`, lấy dòng `develop` có `updater_name`) + hrm-client (sạch).
- [x] 30/10/2026 — HRM: `SellableStockReader::promoByCompanyForProducts()` (SL KM có thể xuất theo từng công ty, port `Product::stockCompanies()` ERP) + `subqueryAllCompanies()`; `ProductPickerService` thêm cột `promo_by_company` + lọc `in_stock_all_companies` (vẫn giữ Đang KD + catalog); `ProductPickerRequest` validate tham số mới (422 tiếng Việt).
- [x] 30/10/2026 — ERP: proxy chuyển tiếp `in_stock_all_companies`; popup thêm cột **SL KM có thể xuất** (`TPE: 712 · TPHP: 1`) + **SL có thể lắp ráp** (bấm mở modal công thức lắp ráp); công tắc **Toàn bộ tồn kho** loại trừ với "Còn tồn" + tooltip; bật cho mọi popup báo giá (popup báo cáo chọn 1 hàng thì không).
- [x] 30/10/2026 — Kiểm: SL KM khớp ERP 5/5, SL lắp ráp 8/8; TPE Còn tồn 5,637 / Toàn bộ tồn kho 7,071; lọc ~0,5s. ERP local không gọi được HRM local (JWT_SECRET khác) → test giao diện bằng JSON thật trả qua Playwright.
- [x] 30/10/2026 — Đẩy: hrm-api `gop_db` (`e0f6e694f`), `task_11937` (`bc0d9bba3`) → merge `develop` (`c224f04cc`); hrm-client `gop_db` (`8a5304470`); ERP `task_11937` (`ced49437e3`) → merge `develop_02` (`f67c7f0304`).
