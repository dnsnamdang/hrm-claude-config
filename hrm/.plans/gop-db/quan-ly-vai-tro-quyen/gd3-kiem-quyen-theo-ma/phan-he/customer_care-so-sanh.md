# customer_care — so sánh mốc trước / sau (GĐ3 Task 8.13, 28/10/2026)

- Mốc: 130 route (ERP 104 + hrm-api 26) × 7 tài khoản (13 pv4, 207 pv3, 337 pv2, 110 pv1, 244 trộn/CSKH, 661 công ty 4, 144 không mã) = **910 ô**.
- Trước chụp 2 lần (code HEAD): **khác 0 ô**. 4 route trang chủ (`admin/topSale` ×3, `admin/approveList`) chụp lại riêng 2 lần sau khi sửa URL (lượt đầu khai thiếu tiền tố `admin/`), 0 khác, ghép vào cả 2 bản trước.
- Sau (`customer_care-sau.json`) vs trước: **910/910 khớp, 0 lệch**. Không ô U8.
- Ô lỗi sẵn (cả trước lẫn sau, không do quyền): `admin/topSale` 500 mọi tài khoản (thiếu tham số/ngày), `report/quotationCountSearchData` 500 (bảng `quotations` đã bỏ sau gộp DB), `warranty_reports/searchData` 500 ở 4 tài khoản (`WarrantyReport::employees()` không tồn tại — nhánh isRole).
- Không chụp HTTP (phủ bằng golden ERP / PHPUnit hrm-api): xem cuối `customer_care-routes.md`.
- Playwright ERP (13/207/244/144 × 15 trang, trước/sau): cờ is_*/show_select_*, trang không quyền, số link CSKH, dòng "Đang xem … tổng số" — 60/60 ô giống hệt.
