# Sổ chi tiết tài khoản — lọc Loại chứng từ lỗi (2026-11-09)

Màn: `/admin/accounting/account_details/account-detail-book`, nhánh gop_db.
File: `app/Services/Reports/AccountDetailReportService.php` hàm `filter()` khối `invoiceable_types`.

## Nguyên nhân
1. Chỉ chọn loại không phải Phiếu xuất/nhập (vd Phiếu chi): `$type` chưa gán → "Undefined variable: type" → 500.
2. `$type` là mảng từ `explode`, so `== ProductExport::class` luôn sai → lọc loại con PXH/PNK (Xuất bán, Xuất KM…) chưa từng chạy.
3. Nếu sửa bằng `whereIn('pe.type')` sẽ (a) loại mất dòng Phiếu chi khi chọn lẫn, (b) lỗi ở `getDeptBegin` vì query đó không join `pe/pi`.

## Sửa
- [x] Gom điều kiện OR: loại thường → `invoiceable_type IN (...)`; PXH/PNK có loại con → `invoiceable_type = X AND invoiceable_id IN (select id from product_exports/product_imports where type IN (...))`.
- [x] Kiểm: chỉ Phiếu chi; Phiếu chi + Xuất bán; chỉ Xuất bán; số dư đầu kỳ chạy được (query không join pe).

## Kết quả kiểm (prod hrm_erp_gop, phiên READ ONLY, TK 3311, 01/01–09/11/2026)
- Chỉ Phiếu chi: 1576 dòng, toàn BillPayment, số dư đầu kỳ chạy được (trước sửa: 500).
- Chỉ Xuất trả NCC (type 4): 10 dòng, đúng 10 bút toán PXH type 4 trên 3311.
- Phiếu chi + Xuất trả NCC: 1586 = 1576 + 10; đầu kỳ cộng đúng.
- Xuất bán (type 1): 0 dòng — đúng, 3311 chỉ có PXH type 14/4/15. Trước sửa sẽ ra cả 41 dòng PXH.
