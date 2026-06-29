# Báo giá (Quotation) — Design (tóm tắt)

## Mục tiêu
Lập phiếu báo giá BÁN gửi khách hàng (trường học), có quy trình duyệt nội bộ và xuất PDF.

## Scope
- Phân hệ Kinh doanh: BE `Modules/Sale` (`/v1/sale/quotations`), FE `pages/sale/quotation`.
- CRUD báo giá: header (KH + người liên hệ + ngày + hiệu lực) + dòng hàng (hàng hoá, ĐVT, SL, đơn giá tay, VAT) + chiết khấu tổng phiếu.
- Quy trình: Nháp → (Gửi duyệt) → Chờ duyệt → Đã duyệt/Từ chối. Đã duyệt = khóa.
- Xuất PDF (BE dompdf), phân quyền theo cấp tổ chức.

## Quyết định lớn
- Mã `BG-YYYY-NNNNN`. 4 trạng thái (Nháp/Chờ duyệt/Đã duyệt/Từ chối) — badge BE.
- Chiết khấu chỉ ở cấp tổng phiếu (%/tiền); không CK theo dòng.
- VAT từng dòng (mặc định từ products.vat), phân bổ CK theo tỉ lệ để tính VAT.
- is_can_delete = chỉ Nháp; is_can_edit = Nháp/Từ chối.
- Gửi duyệt: người tạo. Duyệt/Từ chối: quyền `Duyệt báo giá`.
- PDF: barryvdh/laravel-dompdf (cần composer require).
- Permission (5) thêm vào Timesheet PermissionsTableSeeder.
- Ngoài phạm vi: CK theo dòng, điều khoản TT/ghi chú, tệp đính kèm, chuyển sang đơn hàng.

## Link spec chi tiết
- docs/superpowers/specs/2026-06-25-quotation-design.md
