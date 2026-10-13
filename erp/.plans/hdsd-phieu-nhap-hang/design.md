# Design — HDSD màn Phiếu nhập hàng (ERP)

**Mục tiêu:** Tài liệu HDSD Word cho màn Phiếu nhập hàng (ProductImport / PNH), làm tương tự HDSD Phiếu nhập kho / Đề nghị nhập kho.

## Nguồn khảo sát (3 agent song song)
- **BE**: `app/Http/Controllers/Warehouse/ProductImportsController.php` (~1820 dòng) + routes `product_imports` (routes/web.php 1514-1527, KHÔNG middleware — quyền kiểm trong controller/model). Route: create, all, forAccounting, exportList, edit, getDataForShow, show, index, searchData, store, update, print. KHÔNG có approve/deny/cancel.
- **Model**: `app/Model/Warehouse/ProductImport.php` (2284 dòng) → `ImportModel` (TYPES 18 loại) → `BaseModel`; detail `product_import_details` (CÓ lưu giá: supplier_price/import_price/price/total/vat/thuế/chi phí), `product_import_detail_accountings` (phân bổ kho kế toán), `product_import_detail_customers` (phân bổ KH). Bút toán qua morph `accounting` (AccountDetail) sinh trong `getDataCreateDept()`. `updateWarehouse()` = cập nhật tồn kho kế toán + giá vốn khi status=1.
- **FE**: `resources/views/warehouse/product_imports/{index,all,forAccounting,create,edit,form,show,formJs}.blade.php`. Stack Blade + AngularJS 1.3.9 + Yajra DataTables + Select2.

## Chốt nghiệp vụ cốt lõi (đặc thù PNH, khác PNK)
- Quy trình nhập kho: **YCNH → ĐNNK → Phiếu nhập kho (tăng tồn) → Phiếu nhập hàng (màn này — HẠCH TOÁN/GIÁ VỐN)**.
- PNH LƯU GIÁ (supplier_price/import_price/total/VAT/thuế) — khác hẳn PNK không lưu giá. Công việc chính: khai giá NCC, thuế, chi phí, **phân bổ kho kế toán** (acc_warehouses), **phân bổ chi phí** (số lượng/giá trị), **phân bổ hàng giữ**.
- Tạo từ **Phiếu nhập kho** (`?warehouse_import_id=`, nút trên PNK show) hoặc trực tiếp từ **YCNH** khi `is_import_direct` (nhập thẳng).
- **CHỈ 2 trạng thái**: `3` Đang tạo (nháp, sửa được) · `1` Đã hoàn thành (đã duyệt/hạch toán).
- **KHÔNG có route/nút approve/deny/cancel/xóa**. "Duyệt" = bấm **Lưu & Duyệt** (submit status=1); **Lưu** = submit status=3. Nút Lưu KHÓA tới khi `allocated_complete`.
- `canEdit()` = status==3 && người tạo. `canView()` = Kế toán kho cùng cty / 3 cấp quyền xem / người tạo / admin / nhập thẳng+KTK / buyer_id-summary_user_id khi hoàn thành.
- Khi status=1: `updateWarehouse()` cập nhật AccountingStock/Log + giá vốn, đóng phiếu nhập kho (status=1) + YCNH (status=9). `updateUnitCostPriceOfProducts` đang TẮT.
- **need_allocation**: loại Mua nước ngoài / Điều chuyển chi nhánh → sau duyệt chuyển sang màn Phân bổ hàng.

## Bút toán (getDataCreateDept, TYPE_DEPT=Nợ/TYPE_HAS=Có)
- Mua trong nước/tự do/zitec (2/15/16): Nợ 1541/Nợ 1331/Có 3311; kết chuyển giá vốn Nợ 1561/Có 1541.
- Mua nước ngoài mới (11): chi phí Nợ 1541/1331/Có 3311; kết chuyển Nợ 1561/Có 1541.
- Nhập ghép(8)/tách(10): Nợ account_debt/Có account_has (supplier_price×import_qty) + work_id.
- Bán/mượn trả lại (4/9): doanh thu 5112/33311/1311, chiết khấu 5211, giảm trừ 5213, giá vốn 157/632/1561, hoa hồng/thưởng/TNCN 35241/6411/3335/3341.
- Bốc xếp: Nợ 642/154 / Có 33481.
- TK cứng hiển thị FE: type2 (3311/1561/1331/1562), type11 (3311/1561/1331), type4 (5212/1561/632/5211/5213/33311), type9 (5212/157/632/5211/5213/33311).

## Quyền (nguyên văn — PermissionsTableSeeder 1252-1255, group Kế toán)
"Xem phiếu nhập hàng theo tổng công ty / công ty / phòng ban" (3 cấp — KHÔNG có "theo bộ phận"). Core: "Kế toán kho" (id 80). Liên quan: Ban kiểm soát/BGD duyệt giá nhập hàng trả lại (339/340), báo cáo chi phí nhập hàng theo HĐ (695/696).

## 3 màn danh sách
- index = theo quyền user (type 'index'), có Tạo mới + Excel + cột "Phiếu yc nhập hàng".
- all = theo cấp quyền (is_big_boss/is_boss/is_manager), nhiều lọc, thêm cột Người lập, có Excel; ẩn nháp người khác.
- forAccounting = lọc theo accounting_warehouse_ids, cột gọn (đối tác→"Nhà cung cấp", bỏ Số HĐ/Phiếu yc/Người yêu cầu), KHÔNG Excel.

## Cấu trúc file (9 phần)
Bìa → Mục lục → Danh mục hình → TỔNG QUAN (thuật ngữ, lịch sử, giới thiệu+đường dẫn 4 bước, quyền) → P1 Truy cập & bố cục (3 màn) → P2 Danh sách (quyền + lọc + cột + 2 trạng thái + hành động) → P3 Lập/sửa — Thông tin chung + tab Bốc xếp → P4 Bảng hàng hóa, giá & phân bổ → P5 Các loại chi phí → P6 Lưu, Duyệt & Xem chi tiết (tab Hạch toán bút toán Nợ/Có) → P7 Sửa & phân bổ hàng sau duyệt → P8 In & Excel → P9 FAQ.

## Không làm (theo chốt của user, giống các HDSD trước)
- Chụp ảnh thật (Playwright) & đi sâu form: BỎ — dùng box "[Vị trí chèn ảnh]".

## Tái dựng
```bash
/usr/local/bin/python3 ERP/.plans/hdsd-phieu-nhap-hang/gen_hdsd_pnh_erp.py
```
Output: `ERP/HDSD_luongchinh/HDSD_PhieuNhapHang.docx` (python 3.12 `/usr/local/bin/python3`, dùng `finish_macos` — KHÔNG gọi `finish()` vì cần Windows/Word COM). Kết quả build: 12 Heading 1, 19 bảng, purge 7 media mồ côi, không sót tiêu đề khung.
