# Design — Xuất Excel danh sách hàng hóa từ báo giá đã duyệt

## Mục tiêu
Gộp danh sách hàng hóa (theo mã hàng) từ các báo giá `firm-quotations` đã duyệt, xuất ra file Excel.
Báo cáo **chạy 1 lần (ad-hoc)** qua tinker — không thêm route/menu/phân quyền.

## Bộ lọc báo giá (`firm_quotations`)
- `company_id = 1` (Tân Phát)
- `status = 2` (`FirmQuotation::DA_DUYET` — Đã duyệt)
- `type IN (1, 2)` (`BG_HANG` = báo giá hãng, `BG_DU_AN` = báo giá dự án) — **bỏ** `BG_HD_NGUYEN_TAC` (3)
- `created_at >= '2026-03-01 00:00:00'` (đến hiện tại, không chặn ngày cuối)

## Nguồn hàng hóa
- **Chỉ** bảng `firm_quotation_tab_products` (tab products).
- KHÔNG lấy: group products (`firm_quotation_group_products`), khuyến mãi, combo.
- Bao gồm cả hàng tạm (`tmp_product`) — vì các cột cần (code/tên/model/ĐVT/SL) đã lưu denormalized trên dòng tab product.

## Gộp & cấu trúc output
Gộp theo **Mã hàng (`code`)**, cộng dồn số lượng.

| Cột Excel | Nguồn |
|---|---|
| Mã hàng | `firm_quotation_tab_products.code` |
| Tên hàng | `product_name` |
| Model | `model_name` |
| ĐVT | `unit_name` |
| SL | `SUM(quantity)` theo `code` |

- Sắp xếp: **Mã hàng A→Z**.
- Tên/Model/ĐVT: lấy theo dòng đầu gặp của mỗi mã.
- Dòng có `code` rỗng/null: gộp chung vào nhóm mã rỗng (giữ, không bỏ) — số lượng nhỏ, xử lý sau nếu cần.

## Triển khai (bổ sung: tải qua web)
Query gộp được tách ra static `FirmQuotationProductListExcel::fetchData()` (1 nguồn dùng chung). 2 cách lấy file:
- **Web (khuyên dùng — không cần php local):** `GET /admin/sale/firm-quotations/exportProductList`
  → `FirmQuotationController@exportProductList` trả `(new FirmQuotationProductListExcel($data))->download('danh_sach_hang_hoa_bao_gia.xlsx')`.
  URL đầy đủ: `https://erp.eteksofts.com/admin/sale/firm-quotations/exportProductList`. Route chưa gắn `checkPermission` (đang sau auth `sso.check`/`userLogin`); có thể thêm quyền sau.
- **Tinker (ad-hoc):** như dưới.

## Triển khai (phương án A — ad-hoc)
1. **`database/seeds/UpdateDB.php`** — thêm method `exportQuotationProductsList()`:
   - Query `firm_quotation_tab_products tp` JOIN `firm_quotations q` theo bộ lọc trên.
   - `SELECT tp.code, tp.product_name, tp.model_name, tp.unit_name, SUM(tp.quantity) as qty GROUP BY tp.code, tp.product_name, tp.model_name, tp.unit_name`.
   - Gộp lại theo `code` (PHP) phòng trường hợp cùng mã khác tên/model/ĐVT → sum qty, lấy mô tả dòng đầu.
   - Sắp xếp theo `code` ASC.
   - Build mảng rows → gọi ExcelExport → lưu file → echo đường dẫn.
2. **`app/ExcelExports/FirmQuotationProductListExcel.php`** — maatwebsite `FromArray` + `WithHeadings` (5 cột tiếng Việt).
3. **Lưu file**: `storage/app/exports/firm_quotation_products_<timestamp>.xlsx`. In ra đường dẫn tuyệt đối khi chạy xong.

## Cách chạy
```
php artisan tinker
>>> (new \UpdateDB)->exportQuotationProductsList()
```
(Class `UpdateDB` không có namespace — classmap `database/seeds`. Nếu báo không tìm thấy, thử `(new UpdateDB)`.)

## Lưu ý / Rủi ro
- Tinker local trỏ thẳng **DB production `erp_new`** — method chỉ SELECT + ghi file (read-only với DB), an toàn.
- Cần môi trường php chạy được (php@7.4 trên máy hiện lỗi thiếu `libaspell` → chạy ở server hoặc máy có php hoạt động).
- Đã chốt nguồn chỉ tab products → không có rủi ro cộng trùng tab+nhóm.

## Quyết định đã chốt (brainstorming)
- Gộp theo mã hàng (không giữ từng dòng/từng báo giá).
- Lọc theo `created_at >= 1/3/2026`.
- Chỉ hàng chính, nguồn = `firm_quotation_tab_products`.
- Loại báo giá: hãng + dự án. Công ty: chỉ Tân Phát (id=1).
- Chạy 1 lần qua tinker.
