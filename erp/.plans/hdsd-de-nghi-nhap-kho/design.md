# Design — HDSD màn Đề nghị nhập kho (ERP)

**Mục tiêu:** Tài liệu HDSD Word cho màn Đề nghị nhập kho (WarehouseImportRequest / PDNNK), làm tương tự HDSD Phiếu xuất hàng / Đề nghị xuất kho / Yêu cầu nhập hàng.

## Nguồn khảo sát (3 agent song song)
- **BE**: `app/Http/Controllers/Warehouse/WarehouseImportRequestsController.php` (786 dòng) + routes `warehouse_import_requests` (15 route, không middleware — quyền kiểm trong controller/model) + views index/all/forWarehouse.
- **Model**: `app/Model/Warehouse/WarehouseImportRequest.php` → `ImportModel` (TYPES) → `BaseModel`; detail `warehouse_import_request_details`, tab `warehouse_import_request_tabs` + `..._tab_products`, phân bổ `..._detail_accountings`.
- **FE**: `resources/views/warehouse/warehouse_import_requests/{index,all,forWarehouse,create,form,edit,show,history}.blade.php`. Stack Blade + AngularJS 1.3.9 + Yajra DataTables + Select2.

## Chốt nghiệp vụ cốt lõi
- Quy trình nhập kho 3 bước: **Yêu cầu nhập hàng (YCNH)** → **Đề nghị nhập kho (PDNNK — màn này)** → **Phiếu nhập kho (PNK)**.
- PDNNK luôn lập từ 1 YCNH đã duyệt; hàng hóa **kế thừa nguyên trạng** (form chỉ đọc bảng hàng, không thêm/xóa/sửa SL). Loại Nhập tách lập từ Yêu cầu xuất tách.
- Form chỉ có 3 input: **Phiếu YCNH (*)**, **Chọn kho nhập (*)** (tự set người duyệt = thủ kho kho đó), **Ghi chú**. KHÔNG có NCC/đính kèm/ô SL.
- Nút lưu: **Lưu** = status 3 (Đang tạo/nháp); **Lưu & Gửi** = status 2 (Chờ duyệt). Cần quyền **Kế toán kho**.
- Thủ kho: **Không duyệt** (modal Ghi chú duyệt → trả về status 3) / **Tạo phiếu nhập kho** — chỉ khi là thủ kho của kho + status 2 (`canApprove`).

## Reconcile trạng thái (điểm lệch giữa 2 report)
- **Nhãn hiển thị / dropdown lọc (controller)**: 1=Đang nhập kho, 2=Chờ duyệt, 3=Đang tạo, 4=Đã hạch toán, 5=Đã hủy, 6=Đã nhập kho, 7=Đang hạch toán.
- **Số status thực dùng trong code (model)**: 3=nháp, 2=chờ duyệt, 1=đã duyệt (badge hiện "Đang nhập kho"), 5=hủy. `display_status` là nhãn động theo mốc thời gian (Đã nhận đề nghị → Đang xếp hàng → Đã hoàn thành).
- **HDSD trình bày**: liệt kê đủ nhãn 1-7 trong bảng trạng thái + mô tả vòng đời thao tác (nháp → chờ duyệt → đang nhập kho → đã nhập kho) và nhãn động cho màn thủ kho.

## Quyền (nguyên văn)
"Xem đề nghị nhập kho theo tổng công ty / công ty / phòng ban / bộ phận" (4 cấp — KHÁC màn Phiếu xuất hàng chỉ có 3 cấp), "Thủ kho", "Kế toán kho".

## 3 màn danh sách
- index = đề nghị của tôi (created_by=self), có Tạo mới.
- all = theo phạm vi quyền, thêm cột "Người lập" + nút Xuất Excel, ẩn nháp người khác.
- forWarehouse = thủ kho (kho mình, ẩn status=3), không Tạo mới/Excel.

## Cấu trúc file (7 phần)
Bìa → Mục lục → Danh mục hình → TỔNG QUAN (thuật ngữ, lịch sử, giới thiệu+đường dẫn, quyền) → P1 Truy cập & bố cục → P2 Danh sách (quyền + lọc + cột + trạng thái + hành động) → P3 Lập phiếu → P4 Xem chi tiết & xử lý thủ kho → P5 Sửa & Hủy → P6 Lịch sử/In/Excel → P7 FAQ.

## Không làm (theo chốt của user, giống các HDSD trước)
- Chụp ảnh thật (Playwright) & đi sâu form: BỎ — dùng box "[Vị trí chèn ảnh]".

## Tái dựng
```bash
/usr/local/bin/python3 ERP/.plans/hdsd-de-nghi-nhap-kho/gen_hdsd_dnnk_erp.py
```
Output: `ERP/HDSD_luongchinh/HDSD_DeNghiNhapKho.docx` (chạy bằng python 3.12 `/usr/local/bin/python3`, dùng `finish_macos` — KHÔNG gọi `finish()` vì cần Windows/Word COM).
