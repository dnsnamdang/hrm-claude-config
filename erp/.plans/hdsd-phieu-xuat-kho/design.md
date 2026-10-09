# Design — HDSD màn Phiếu xuất kho (ERP)

**Mục tiêu:** Tài liệu HDSD Word cho màn Phiếu xuất kho (WarehouseExport / PXK), làm tương tự HDSD Đề nghị xuất kho / Yêu cầu xuất hàng.

## Nguồn khảo sát (Bước 1 hdsd-documenter)
- BE: `app/Http/Controllers/Warehouse/WarehouseExportsController.php`
- Model: `app/Model/Warehouse/WarehouseExport.php` (extends `ExportModel`) + `WarehouseExportLot(_Detail/_Package).php` + `TmpWarehouseExportLot(_Detail).php` + `WarehouseExportTab(_Product).php`
- Views: `resources/views/warehouse/warehouse_exports/` (index, create, form, edit, re_export, pick, show, formJs)
- Routes: `routes/web.php` (admin/warehouse/warehouse_exports)
- Quyền: `PermissionsTableSeeder` — Thủ kho (81), Xem tất cả phiếu xuất nhập kho (133), Xem phiếu xuất kho theo tổng công ty/công ty/phòng ban (915/916/917 — CHỈ 3 cấp, KHÔNG có bộ phận), Kế toán kho.

## Đặc thù màn (khác Đề nghị xuất kho)
1. **Chọn LÔ + VỊ TRÍ + SL xuất** theo từng lô (nhóm cột Vị trí | Lô | Tồn | SL xuất) — điểm khác biệt cốt lõi.
2. **Luồng 2 giai đoạn:** lập phiếu (lô tạm, bước "Đang đi lấy hàng") → Phiếu đi lấy hàng (pick, chia nhóm/phân công NV) → Xuất kho (lô thật, trừ tồn, gửi).
3. Chỉ **3 cấp quyền xem** (không có bộ phận).
4. **8 trạng thái** (Đang tạo / Chờ duyệt / Đang hạch toán / Đã hạch toán / Không duyệt / Đã nhập lại / Đã xuất lại / Đã hủy) + cột `step` (tiến trình).
5. **Nhập lại / Xuất lại** khi bị từ chối.
6. **Đính kèm chứng từ bắt buộc** khi Gửi (Lưu & Xuất, status 2).
7. Nhiều loại in/biên bản (phiếu xuất kho, phiếu lấy hàng, dự kiến, biên bản giao nhận - bàn giao).
8. Màn xem chi tiết KHÔNG hiện đơn giá/thành tiền cho hàng hóa (chỉ SL).
9. Phiếu do **Thủ kho** lập từ 1 Đề nghị xuất kho đang chờ duyệt (lập PXK = duyệt PDNXK). Kế toán kho: "Tạo phiếu xuất hàng" / "Không duyệt".

## Generator
- `gen_hdsd_pxk_erp.py` — mirror `../hdsd-de-nghi-xuat-kho/gen_hdsd_dnxk_erp.py`.
- Dùng `HdsdBuilder` (`HRM/.claude/skills/hdsd-documenter/assets/hdsd_engine.py`).
- KHÔNG chèn ảnh thật → box `[Vị trí chèn ảnh]` (helper `img_placeholder`).
- macOS: dùng `finish_macos` (KHÔNG gọi `finish()` — cần PowerShell/Word COM chỉ có trên Windows): save → `clear_toc_cache` (blank text cache field TOC) → `_set_update_fields` → `_purge_orphan_media`. Word tự dựng lại mục lục khi mở.

## Output
`ERP/HDSD_luongchinh/HDSD_PhieuXuatKho.docx` (12 Heading 1, 16 bảng, purge 7 media mồ côi, không sót tiêu đề khung).

## Tái dựng
```bash
/usr/local/bin/python3 ERP/.plans/hdsd-phieu-xuat-kho/gen_hdsd_pxk_erp.py
```
