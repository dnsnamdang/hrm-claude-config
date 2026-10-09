# Design — HDSD màn Phiếu nhập kho (ERP)

**Mục tiêu:** Tài liệu HDSD Word cho màn Phiếu nhập kho (WarehouseImport / PNK), làm tương tự HDSD Đề nghị nhập kho / Phiếu xuất hàng.

## Nguồn khảo sát (3 agent song song)
- **BE**: `app/Http/Controllers/Warehouse/WarehouseImportsController.php` (2505 dòng) + routes `warehouse_imports` (chỉ `/forAccounting` gắn middleware `checkPermission:Kế toán kho`; còn lại kiểm quyền trong controller can*() + model searchByFilter) + nhóm con `excShortage`.
- **Model**: `app/Model/Warehouse/WarehouseImport.php` (1778 dòng) → `ImportModel` (TYPES 18 loại) → `BaseModel`; detail `warehouse_import_lots` (có lot_number, KHÔNG còn import_price), `warehouse_import_lot_details` (theo vị trí), tab `warehouse_import_tabs` + `..._tab_products`, tmp `TmpWarehouseImportLot`. `updateWarehouse()` = TĂNG TỒN thực tế. Hạch toán tách sang ProductImport.
- **FE**: `resources/views/warehouse/warehouse_imports/{index,all,forAccounting,discrepancy,create,form,edit,show,formJs}.blade.php` + partials classes + modals selectPosition/selectImportLot. Stack Blade + AngularJS 1.3.9 + Yajra DataTables + Select2.

## Chốt nghiệp vụ cốt lõi (đặc thù PNK, khác ĐNNK)
- Quy trình nhập kho: **YCNH → ĐNNK → Phiếu nhập kho (màn này) → Phiếu nhập hàng (hạch toán)**.
- PNK là bước **TĂNG TỒN KHO thực tế**: `store()` chỉ tạo nháp + tmp lot (đi xếp hàng); `update()` với status=2 (Lưu & Nhập) mới gọi `updateWarehouse()` cộng tồn + sinh **số lô (lot_number)**.
- Màn tạo mới FE tiêu đề **"Dự kiến vị trí"**; công việc chính là gán mỗi mặt hàng vào **vị trí kho** (Nhà/Dãy/Khoang) và nhập SL cho từng vị trí. SL thực nhập = tổng tự tính. Có checkbox "Áp dụng tất cả".
- Form 2 card: Thông tin chung (tabs Thông tin chung / **Vận chuyển** / **Bốc xếp**) + Chi tiết (Hàng hóa + tab hợp đồng).
- **Hạch toán/giá vốn/lô/ngày nhập KHÔNG ở màn này** → thuộc Phiếu nhập hàng (ProductImport), tạo qua nút "Tạo phiếu nhập hàng" (canApprove — Kế toán kho).
- **Không có màn Lịch sử (history)** cho PNK (khác ĐNNK) → HDSD bỏ mục Lịch sử.
- Nhánh phụ: **Xuất lại** (status Không duyệt → 4), **Nhập lại** (status Đã xuất lại → 5), **Báo hàng thừa/thiếu** (excShortage, status Đã hạch toán=1).

## Trạng thái & Tiến trình (2 cột riêng)
- **status (nhãn hiển thị)**: 1 Đã hạch toán · 2 Chờ duyệt · 3 Đang tạo · 4 Không duyệt · 5 Đã xuất lại · 6 Đã nhập lại · 7 Đang hạch toán · 8 Đã hủy.
- **step**: 2 Đang đi xếp hàng · 3 Đang nhập kho / Hoàn thành nhập kho (step=3 & status!=3). Cột Tiến trình bị ẩn ở màn Kế toán kho.

## Quyền (nguyên văn)
"Xem phiếu nhập kho theo tổng công ty / công ty / phòng ban" (3 cấp — KHÔNG có "theo bộ phận") + "Xem tất cả phiếu xuất nhập kho" (lọc theo kho thủ kho), "Thủ kho", "Kế toán kho", "Tạo/Duyệt phiếu báo hàng thừa, thiếu nhập kho". Chỉ route `/forAccounting` gắn middleware quyền.

## 4 màn danh sách
- index = theo quyền của user (type động), có Tạo mới + Excel + cột Tiến trình.
- all = theo phạm vi quyền (type 'all'), có Tạo mới + Excel + cột Tiến trình + cột Người lập.
- forAccounting = Kế toán kho (type 'approve', middleware), ẩn cột Tiến trình + không Excel.
- discrepancy = chờ báo thừa/thiếu, chỉ nút "Báo hàng thừa thiếu".

## Cấu trúc file (9 phần)
Bìa → Mục lục → Danh mục hình → TỔNG QUAN (thuật ngữ, lịch sử, giới thiệu+đường dẫn 4 bước, quyền) → P1 Truy cập & bố cục (4 màn danh sách) → P2 Danh sách (quyền + lọc + cột + trạng thái + tiến trình + hành động) → P3 Lập phiếu & dự kiến vị trí → P4 Vận chuyển & Bốc xếp → P5 Xem chi tiết & xử lý Kế toán kho → P6 Sửa/Hủy/Xuất lại/Nhập lại → P7 Báo hàng thừa/thiếu → P8 In ấn & Xuất Excel → P9 FAQ.

## Không làm (theo chốt của user, giống các HDSD trước)
- Chụp ảnh thật (Playwright) & đi sâu form: BỎ — dùng box "[Vị trí chèn ảnh]".

## Tái dựng
```bash
/usr/local/bin/python3 ERP/.plans/hdsd-phieu-nhap-kho/gen_hdsd_pnk_erp.py
```
Output: `ERP/HDSD_luongchinh/HDSD_PhieuNhapKho.docx` (chạy bằng python 3.12 `/usr/local/bin/python3`, dùng `finish_macos` — KHÔNG gọi `finish()` vì cần Windows/Word COM). Kết quả build: 12 Heading 1, 23 bảng, purge 7 media mồ côi, không sót tiêu đề khung.
