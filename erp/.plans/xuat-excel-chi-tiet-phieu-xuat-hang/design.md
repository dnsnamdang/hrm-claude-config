# Design — Xuất excel chi tiết Phiếu xuất hàng (loại Xuất bán HĐ hàng hóa)

> Ngày: 2026-06-09 · Module: Warehouse / product_exports · Màn: `admin/warehouse/product_exports/all` + màn chi tiết `show`
> File mẫu: `/Users/nguyentrancu/Documents/TanPhat/HD2/Xuất bán_xuất excel PXH_06042026.xlsx` (2 sheet: không xuất thẳng / xuất thẳng)

## Mục tiêu & phạm vi
- Bổ sung chức năng **xuất Excel chi tiết 1 phiếu xuất hàng**, đúng layout file mẫu.
- **Chỉ áp dụng** loại **Xuất bán HĐ hàng hóa** (`ExportModel::XUAT_BAN_HD_HANG`, type=14 — verify lúc code).
- Hỗ trợ 2 trường hợp trong **cùng 1 blade**, rẽ nhánh theo `is_export_direct`:
  - `is_export_direct = 0`: **không xuất thẳng** (qua Phiếu xuất kho).
  - `is_export_direct = 1`: **xuất thẳng** (qua Phiếu YCXH).

## Quyết định chung
- Hướng triển khai: **A** — bám pattern `exportList` sẵn có (maatwebsite/excel `FromView` + blade), 1 blade dùng `@if($is_export_direct)`.
- Nút hiển thị **vô điều kiện** như "In phiếu" (không chặn trạng thái, không quyền riêng), nhưng **chỉ với type=14**.
- Đặt nút ở **cả 2**: dropdown action màn `all` + nút trên màn `show`.
- **Không merge ô** khi xuất (theo ghi chú mẫu): mỗi trường = 1 ô nhãn + 1 ô giá trị; dòng tiêu đề section là 1 dòng text; dòng phụ (kho kế toán) để trống các ô chung.

## Thành phần kỹ thuật
| Thành phần | Đường dẫn | Ghi chú |
| ---------- | --------- | ------- |
| Route | `routes/web.php` (nhóm product_exports ~1292-1307) | `GET /{id}/exportDetail` → `productExport.exportDetail` |
| Controller | `app/Http/Controllers/Warehouse/ProductExportsController.php` | method `exportDetail($id)` |
| Excel class | `app/ExcelExports/ProductExportDetailExcel.php` | `FromView, WithEvents, Exportable`; `forData()` + `view()` |
| Blade view | `resources/views/reports/exports/product_export_detail_export.blade.php` | 1 file, rẽ nhánh xuất thẳng |
| Nút list | `ProductExportsController@searchData` (cột action ~172-187) | thêm link khi `type==14` |
| Nút show | `resources/views/warehouse/product_exports/show.blade.php` | nút download khi `type==14` |

Tên file tải về: `PXH_{code}.xlsx`.

## Dữ liệu eager-load (controller)
`ProductExport::with([...])->findOrFail($id)` gồm: `products.product.model`, `products.unit`, `products.acc_warehouses`, `warehouse_export.warehouse`, `product_export_request`, `customer`, `employee_create.info.department`, `arrange_delivery.executors`, vận chuyển (chuyến xe + NV/cty chịu phí), hợp đồng (`firm_contract`/`contract`...). Chốt tên quan hệ cụ thể khi lập plan.

## Bố cục Excel theo section

### Header + tiêu đề
- Header công ty (biến `HEADER`). Tiêu đề "PHIẾU XUẤT HÀNG", `No: {code}`, `Ngày lập: {created_at}`.

### Section 1 — Thông tin chung (rẽ 2 ca)
- **Chung:** Loại yêu cầu (Xuất bán hàng), Xuất thẳng (Có/Không), Hợp đồng, Khách hàng, Ghi chú, Người lập, Ngày hạch toán, Người yêu cầu, Phòng yêu cầu.
- **Không xuất thẳng (=0):** thêm Phiếu xuất kho (`warehouse_export.code`), Kho xuất, Vận chuyển, Công ty vận chuyển, Thủ kho, Người nhận hàng.
- **Xuất thẳng (=1):** thay bằng Phiếu YCXH (`product_export_request.code`); bỏ Kho xuất / Vận chuyển / Thủ kho / Người nhận hàng.

### Section 2 — Bốc xếp (chỉ khi có `arrange_delivery`)
- Hiển thị **đúng 1** loại theo `rent_type`: TH1 thuê công ty **hoặc** TH2 thuê ngoài.
- Trường: Cách tính (thời gian/khối lượng), Loại hình thuê, Loại bốc xếp, Khối lượng/Số giờ, Đơn giá, Số tiền, VAT (8%), Số tiền sau VAT.
- Thuê ngoài (TH2) thêm: NCC (mã-tên), Tài khoản nợ, Mã phí, Vụ việc.
- Bảng chi tiết người nhận việc (`executors`: STT, Nhân viên, Số tiền) — **chỉ TH1**; TH2 không có.

### Section 3 — Vận chuyển (chỉ khi **không xuất thẳng** & có công ty vận chuyển)
- Trường: Số KM dự kiến, Số KM chốt, NV chịu phí (tổng), CP vận chuyển thực tế, Thuế, Công ty chịu phí (tổng).
- Chi tiết theo chuyến xe: STT, Chuyến xe, NV chịu phí, Công ty chịu phí.
- Xuất thẳng: **bỏ hẳn** section này.

### Section 4 — Hàng hóa + Tổng
- 18 cột đúng thứ tự mẫu: STT, Hàng hóa, Model, Mã hàng hóa, ĐVT, SL thực xuất, Kho kế toán, SL xuất, Đơn giá vốn, Thành tiền vốn, Giá niêm yết, Đơn giá bán, Thành tiền bán, Đơn giá sau giảm, Thành tiền sau giảm, % VAT, Số tiền VAT, Thành tiền sau VAT.
- 1 sản phẩm nhiều dòng kho kế toán (`acc_warehouses`): cột chung (STT/Hàng hóa/Model/Mã/ĐVT/SL thực xuất) chỉ ở **dòng đầu**, dòng phụ **để trống**; mỗi dòng phụ có Kho kế toán + SL xuất + đơn giá/thành tiền riêng.
- Tổng: Thành tiền bán, Tổng giảm giá, Tổng tiền trước thuế, Tiền VAT, Tổng tiền sau thuế, Tổng tiền vốn.

### Chữ ký
- "Người lập phiếu" / "Kế toán trưởng" + tên người lập.

## Cần verify khi lập plan / code
- Đúng constant/label "Xuất bán HĐ hàng hóa" (kỳ vọng type=14).
- Tên quan hệ + cột chính xác cho: bốc xếp thuê ngoài (tài khoản nợ/mã phí/vụ việc), chi tiết vận chuyển theo chuyến xe, người nhận hàng/thủ kho, tổng tiền vốn/bán/sau giảm.

## Ngoài phạm vi
- Các loại phiếu khác (KM, mượn, điều chuyển, dịch vụ, dự án, thực hiện HĐ...).
- Không đổi logic in phiếu / hạch toán hiện có.
