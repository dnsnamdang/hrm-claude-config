# Design — HDSD màn Phiếu xuất hàng (ERP)

**Màn:** Phiếu xuất hàng (ProductExport / PXH) — bước 4 (cuối) của quy trình xuất hàng.
Route `admin/product_exports`, mã phiếu `PXH-xxxxx`. Do Kế toán lập từ Phiếu xuất kho
(hoặc Yêu cầu xuất hàng / Yêu cầu xuất ghép khi xuất thẳng) để ghi nhận số liệu và **HẠCH TOÁN**.

## Nguồn khảo sát (Bước 1)
- Controller `app/Http/Controllers/Warehouse/ProductExportsController.php`.
- Model `app/Model/Warehouse/ProductExport.php` (extends ExportModel/BaseModel) + ProductExportDetail,
  ProductExportDetailAccounting (`product_export_detail_accounting`), ProductExportTab, ProductExportTabProduct.
- Views `resources/views/warehouse/product_exports/` (index, all, forAccounting, create, form, edit, show, formJs)
  + partials/classes/warehouse/ProductExport*.blade.php.
- routes/web.php (group product_exports, ~13 route, không có middleware checkPermission).
- Quyền 918/919/920 (nhóm "Quản lý phiếu xuất hàng", category "Kế toán") — CHỈ 3 cấp, không bộ phận.

## Điểm khác biệt so với HDSD Phiếu xuất kho
1. **Hạch toán là cốt lõi**: đơn giá bán / thành tiền / VAT / giá vốn trên bảng hàng + tài khoản Nợ/Có
   + mã phí / vụ việc + tab Hạch toán (bảng bút toán) ở màn xem chi tiết.
2. Do Kế toán lập từ Phiếu xuất kho (hoặc YCXH / xuất ghép cho xuất thẳng).
3. Chỉ 4 trạng thái (Đang tạo / Đã hoàn thành / Đang quyết toán / Đã quyết toán); lưu chỉ nhận 1 hoặc 3.
4. Quyền xem 3 cấp 918/919/920 + Kế toán kho / Super Admin.
5. **Phân bổ Kho kế toán** theo từng dòng hàng (nhiều kho / 1 hàng).
6. Không có xóa / duyệt lùi / pick; hành động dòng chỉ Sửa / In / In hạch toán (loại Xuất ghép).
7. "Lưu & Duyệt" (status 1) → sinh bút toán + trừ tồn kho kế toán + cập nhật PXK (Đã xử lý) + PDNXK (hoàn thành) + nhắc nợ.

## Generator
- `gen_hdsd_pxh_erp.py` — mirror `gen_hdsd_pxk_erp.py`. Helper `img_placeholder`, `clear_toc_cache`,
  `finish_macos` copy verbatim. `cover_title="(Màn hình: Phiếu xuất hàng)"`, `doc_title="HDSD - Phiếu xuất hàng"`.
- Output: `ERP/HDSD_luongchinh/HDSD_PhieuXuatHang.docx`.
- Không chèn ảnh thật — dùng box `[Vị trí chèn ảnh]` (theo chốt user, giống các HDSD trước).

## Cấu trúc tài liệu
TỔNG QUAN (thuật ngữ / lịch sử / giới thiệu + vị trí bước 4 / quyền) → PHẦN 1 Truy cập & bố cục →
PHẦN 2 Danh sách + phân quyền 918/919/920 + Kế toán kho → PHẦN 3 Lập & Hạch toán (nguồn, thông tin chung,
phân bổ kho kế toán + số lượng, TK Nợ/Có + mã phí/vụ việc, vận chuyển, bốc xếp, nút Lưu/Lưu & Duyệt, validate) →
PHẦN 4 Xem chi tiết & tab Hạch toán → PHẦN 5 Sửa phiếu → PHẦN 6 In & Excel → PHẦN 7 FAQ.

## Tái dựng
```bash
/usr/local/bin/python3 ERP/.plans/hdsd-phieu-xuat-hang/gen_hdsd_pxh_erp.py
```
Kết quả build: 10 Heading 1, 15 bảng, purge 7 media mồ côi, không sót tiêu đề khung (OK).
