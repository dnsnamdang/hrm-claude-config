# Design — HDSD màn Đề nghị xuất kho (ERP)

**Màn:** Đề nghị xuất kho (Phiếu đề nghị xuất kho / PDNXK) — route `admin/warehouse/warehouse_export_requests`.
Bước 2 trong quy trình xuất hàng: Yêu cầu xuất hàng → **Đề nghị xuất kho** → Phiếu xuất kho → Phiếu xuất hàng.

## Nguồn khảo sát
- Controller: `app/Http/Controllers/Warehouse/WarehouseExportRequestsController.php`
- Model: `app/Model/Warehouse/WarehouseExportRequest.php` (extends `ExportModel`) + Detail + Tab/TabProduct
- Views: `resources/views/warehouse/warehouse_export_requests/` (index, forWarehouse, all[disabled], create, edit, form, formJs, show)
- Routes: `routes/web.php` ~1199-1215; `PermissionsTableSeeder.php`
- 3 report khảo sát (scratchpad): `dnxk_be_report.md`, `dnxk_model_report.md`, `dnxk_fe_report.md`

## Điểm khác YCXH/YCNH (đã phản ánh trong tài liệu)
1. KHÔNG có nút "Tạo mới" trên danh sách — đề nghị lập từ màn Yêu cầu xuất hàng (Kế toán kho).
2. KHÔNG có xóa — chỉ Hủy (status 3 → 5), soft, do người lập.
3. Quyền kiểm trong controller/model (không middleware checkPermission trên route).
4. Duyệt bởi **Thủ kho** (theo kho), không phải TP/BGĐ. Thủ kho: tạo phiếu xuất kho / điều chuyển / từ chối.
5. Tab theo hợp đồng hãng (firm_contract_tab), không theo kho.
6. Chỉ chọn KHO, không chọn lô (lô ở bước Phiếu xuất kho).
7. Hai chế độ in: In đề nghị (print) + In bộ giấy tờ đi đường (printMove).
8. Không chặn công nợ/hạn mức.

## Nội dung file
TỔNG QUAN → PHẦN 1 Truy cập & bố cục → PHẦN 2 Danh sách + quyền (911/912/913, 914 chưa dùng, Kế toán kho, Thủ kho, TP kế toán) → PHẦN 3 Lập & Sửa (từ YCXH) → PHẦN 4 Xem & xử lý (Thủ kho) → PHẦN 5 Hủy → PHẦN 6 In & Excel → PHẦN 7 Màn Thủ kho/chờ duyệt → PHẦN 8 FAQ.

## Kỹ thuật dựng (macOS)
- python `/usr/local/bin/python3` (3.12, có python-docx + lxml).
- Dùng `HdsdBuilder` từ `HRM/.claude/skills/hdsd-documenter/assets/hdsd_engine.py`.
- KHÔNG gọi `finish()` (PowerShell/Word COM = Windows). Dùng `finish_macos()`:
  `doc.save()` → `clear_toc_cache()` (blank text cache trong field TOC) → `_set_update_fields()` → `_purge_orphan_media()`. Word tự dựng lại mục lục khi mở.
- Không chèn ảnh thật — dùng box `[Vị trí chèn ảnh]`.

## Tái dựng
```bash
/usr/local/bin/python3 ERP/.plans/hdsd-de-nghi-xuat-kho/gen_hdsd_dnxk_erp.py
```
Output: `ERP/HDSD_luongchinh/HDSD_DeNghiXuatKho.docx` (11 Heading 1, 16 bảng, purge 7 media, không sót tiêu đề khung).
