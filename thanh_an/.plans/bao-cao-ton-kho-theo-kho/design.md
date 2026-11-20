# Báo cáo tồn kho hàng hóa theo kho — Design (tóm tắt)

> Người phụ trách: @khoipv · Bắt đầu: 20/11/2026
> Demo gốc: `c:\Users\Admin\Desktop\demo nhập kho\bc_ton_kho_theo_kho.html`
> Spec chi tiết: [docs/superpowers/specs/2026-11-20-bao-cao-ton-kho-theo-kho-design.md](../../docs/superpowers/specs/2026-11-20-bao-cao-ton-kho-theo-kho-design.md)

## Mục tiêu
Xem tồn **hiện tại** từng mã hàng trên từng kho → bung lô / HSD / seri / mục đích (tồn chung hay giữ KH), cảnh báo cận date (≤ 90 ngày) / hết hạn. Đúng ngay sau khi duyệt phiếu nhập kho.

## Scope
- Có: bộ lọc (kho nhiều, nhóm hàng, hãng-nước SX, ĐVT, KH giữ, cảnh báo date, mã / tên, khoảng tổng tồn, tìm nhanh), KPI 5 ô, bảng mã → kho → chi tiết lô, Xuất Excel (1 dòng / lô), In 2 chế độ.
- Không: xem tồn quá khứ (để Thẻ kho), giá trị tiền, sửa tồn, khái niệm "quản lý theo lô/seri".

## Quyết định lớn
| | Quyết định | Ai |
|---|---|---|
| Dữ liệu | Hướng **A**: đọc thẳng `stock_balances`, không bảng tổng hợp | user |
| Seri | Thêm `stock_serials.balance_id` (HSD trống so `NULL = NULL` không khớp, seri thiếu HĐ) + bù dữ liệu | user |
| Quyền | Như Cung ứng: quyền "Xem báo cáo tồn kho" = mọi kho, không phân cấp; tạm mở bằng config như PNK | user / call |
| Lỗi KH | Mục đích giữ KH thiếu `customer_id` → lấy từ `contracts.customer_id` (code + bù dữ liệu) | call |
| Bảng | `V2BaseDataTable` + `cellSpan` + `row-expand`, header 1 tầng, không sửa base | call |
| Excel | 1 dòng / lô, seri nối chuỗi | call |
| Cấu hình cột | Cột mới `column_customizations.warehouse_stock_report` | call — chờ user |

## API
`/v1/warehouse/stock-report`: `GET /` (phân trang theo mã + KPI) · `GET /lots` (chi tiết khi bung) · `GET /rows` (Excel / in) · `GET /filter-options`.

## FE
`pages/warehouse/reports/stock-by-warehouse/index.vue` (V2) · menu Kho → "Báo cáo" → "Tồn kho theo kho".
