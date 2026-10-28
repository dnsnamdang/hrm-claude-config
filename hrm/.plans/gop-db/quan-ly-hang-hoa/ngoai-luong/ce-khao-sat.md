# Khảo sát đợt C-e — N1: bảo hành / tồn tối thiểu theo công ty ở ERP (13/10/2026, chỉ đọc)

> ERP worktree `wt-erp-2d1` @ `ad57aec450` (nhánh chung `feat/2d1-erp-khong-loi`). DB `hrm_erp_giacty`.
> Luật đọc (cùng HRM `AdminData::source`, §24c / Q-N1): dòng `product_company_coefficients` của **công ty liên quan**; công ty
> chưa có dòng ⇒ lùi cột chung `products`. Chứng từ ⇒ công ty chứng từ (`DocumentCompany::of/ofOrUser`, như giá G3).

## Hiện trạng dữ liệu (đo giacty 13/10)
- pcc 113.782 dòng, 113.484 có trạng thái (4 công ty); 108.488 có `guarantee`, 113.484 có `min_stock_qty`.
- Dòng có trạng thái **khớp 100%** cột chung (0 lệch bảo hành, 0 lệch tồn tối thiểu) — nhờ backfill N72.
- ⇒ Hôm nay ERP chưa sai số; lệch bắt đầu khi HRM sửa tab Quản trị theo công ty / công ty lấy về để trống (L2) / hàng mới HRM.
- ERP: chưa chỗ nào đọc 3 ô này từ pcc; model `ProductCompanyCoefficient` trơn; `Product::company_coefficients()` có sẵn.

## Kiểm kê chỗ đọc (agent rà + kiểm tay mẫu) — ~31 file sống, ~25 file đã chặn/chết (bỏ)

| Nhóm | Chỗ | File | Công ty có sẵn |
|---|---:|---:|---|
| A. Chép vào chứng từ lúc lập/sửa (`$line->guarantee = $product->guarantee`) | 20 | 17 | đều đứng cạnh lời gọi giá đã dùng `DocumentCompany` (Quotation, Contract, phụ lục HĐ/HĐ dịch vụ, báo giá DV, báo giá dự án nhóm/tab, phân tích dự án, Firm báo giá/HĐ/đơn nguyên tắc ×2, biên bản bàn giao ×3) |
| B. Hiển thị (chi tiết hàng hoá ERP, chi tiết bảo hành, in báo giá mẫu) | 6 | ~9 | chi tiết hàng: công ty người dùng; bảo hành: công ty biên bản; báo giá mẫu: không có cột công ty (giá đang lấy công ty người dùng) |
| C. Báo cáo | 5 | 7 | Cảnh báo đặt hàng tồn kho (`company_id` bắt buộc — Q-N1 đã chốt); **Chuyển kho / tồn kho** (`StockTransferReportService`, công ty TUỲ CHỌN); **Báo cáo CSKH** (hạn bảo hành từng dòng, nhiều nguồn chứng từ); **Tổng hợp bán hàng** (`SummarySaleReportService`, lọc công ty có thể rỗng = mọi công ty) |
| D. Job / lệnh | 1 | 1 | `database/seeds/SyncImageProductToCRM` (đẩy 1 lần sang CRM, không công ty) |
| E. API / JSON cho JS | 4 | 3 | `SearchController` 2 endpoint tồn kho-mua (có công ty), `Product::dataFor/getData` (đã có tham số công ty); nhiều `select('products.*')` gửi cột thô nhưng không JS nào dùng |
| F. Bỏ qua | — | ~25 | route đã chặn `productMovedToHrm` (form/ghi hàng hoá), job sinh template không ai gọi, xuất đã gỡ ở C-c, nhãn lịch sử, chép dòng→dòng (không đọc hàng hoá) |

Lõi: 2 accessor `Product::guarantee_data` (:273) và `guarantee_day` (:840) KHÔNG nhận công ty — đang dùng khắp A/B/E.

## Hướng sửa (dự kiến)
- `App\Product`: `adminRowFor(int $companyId)` (nạp 1 lần / dùng quan hệ đã eager) ⇒ `guaranteeFor`, `guaranteeTypeFor`, `guaranteeDataFor`,
  `guaranteeDayFor`, `minStockQtyFor($companyId)`; luật lùi cột chung giống HRM `AdminData::source` (có dòng ⇒ đọc dòng kể cả NULL).
- Báo cáo SQL: join `product_company_coefficients` theo công ty + `COALESCE` lùi cột chung (khuôn `SearchController::onlyTradingProducts`, `PriceSql`).
- Accessor cũ `guarantee_data` / `guarantee_day` (không công ty): giữ cho chỗ đã chặn/chết; chỗ sống đổi sang `*For($companyId)`.
- Test PHPUnit (sqlite :memory:) cho helper + 1–2 luồng chép chứng từ; Playwright ERP: báo giá / HĐ thêm hàng có pcc khác cột chung.

## Chốt
| # | Câu | Đáp án |
|---|---|---|
| C-e-1 | Báo cáo Chuyển kho / tồn kho (`StockTransferReportService`) khi KHÔNG chọn công ty: tồn tối thiểu lấy thế nào | ✅ 13/10 user: **báo cáo BẮT BUỘC chọn công ty** ⇒ tồn tối thiểu luôn của công ty đã chọn (FE bắt chọn + BE chặn ở xem / in / xuất / job mail) |
| C-e-2 | Báo cáo CSKH + Tổng hợp bán hàng (hạn / số tháng bảo hành từng dòng, có thể nhiều công ty) | ✅ 13/10 user: **BỎ QUA 2 báo cáo này, note lại để sau tính** ⇒ N90 (`CustomerCareReportService`, `SummarySaleReportService` vẫn đọc cột chung) |

## Tự chốt (khuôn có sẵn, không phải nghiệp vụ mới)
- Chứng từ không có cột `company_id` (contracts, project_quotations…) ⇒ công ty người lập — đúng luật giá G3 (`DocumentCompany::of`).
- Chi tiết hàng hoá ERP còn mở + báo giá mẫu (không cột công ty) ⇒ công ty người dùng đang làm việc — như giá G3.
- `SyncImageProductToCRM` (seeder chạy tay 1 lần) + `products.*` thô gửi JS không ai đọc ⇒ không sửa, ghi chú.
- Job/cron không gọi `DocumentCompany::user()` (ném lỗi khi không đăng nhập) — công ty luôn truyền tường minh.
