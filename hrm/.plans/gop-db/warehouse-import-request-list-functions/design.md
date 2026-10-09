# Design — Chức năng màn "Danh sách đề nghị nhập kho" (Lỗi #11400)

> Nhánh: `gop_db` · Phụ trách: @namdangit · Ngày: 19/09/2026
> Màn: `hrm-client/pages/finance/warehouse-import-requests/` (PDNNK, module Finance)
> Redmine **Lỗi #11400 — [ERP => HRM] Kế toán - HH-DV-VC - Nhập hàng - Phiếu đề nghị nhập kho: Danh sách**

## Nguồn yêu cầu

Ticket của Lê Huyền Trang. Làm SONG SINH với màn Đề nghị xuất kho (ĐNXK,
`pages/finance/warehouse-export-requests/`) đã hoàn thành trước — bê y hệt pattern.
5 yêu cầu cho bảng DANH SÁCH (+ đồng bộ màn chi tiết):

1. Đổi nhãn cột người tạo **"Người lập" → "Người tạo"**.
2. Thêm đúng 4 cột: **Ngày cập nhật (updated_at), Người cập nhật (updater),
   Người yêu cầu (requester), Người duyệt (approver)**.
3. **Ẩn nút Xem chi tiết** → click vào Mã phiếu để vào chi tiết
   (ĐÃ XONG ở ticket cột-hành-động trước, commit `bd39c0419`).
4. Thêm **Xem lịch sử** ở CẢ list VÀ detail (BE log qua `LogsCatalogHistory`/
   `CatalogHistoryService`; FE `CatalogHistoryModal` ở list + `SystemInfoSection` ở detail).
5. Thêm **sort** cho cột **Mã YCNH (product_import_request_code), Khách hàng, Loại (type_name)**.

## Quyết định đã CHỐT

1. **Yêu cầu #5 "Khách hàng" = cột "Nhà cung cấp" (supplier_name) đang có** — danh sách 4 cột
   mới ở #2 KHÔNG có cột khách hàng, nên bên đối tác trên màn nhập là "Nhà cung cấp". → cho
   `supplier_name` sortable, KHÔNG thêm cột khách hàng mới. Sort supplier_name cần join
   `customers` theo `supplier_id` (Supplier model = bảng customers, xem memory).
2. **Người cập nhật = quan hệ `employee_update`** (BaseModel), KHÁC export dùng `updater`.
3. **Người yêu cầu = `productImportRequest.employee_create`** (KHÁC export dùng
   `productExportRequest.creator`).
4. **Lịch sử ở list = menu action trong `V2BaseRowActions`** (icon `ri-history-line`,
   luôn hiện, KHÔNG gắn permission) — theo entity-history §5.1; màn export dùng nút icon
   rời vì nó không dùng V2BaseRowActions, nhưng màn nhập đã chuyển sang V2BaseRowActions
   (ticket trước) nên gộp vào menu cho nhất quán.
5. **catalogColumns = `['type','warehouse_id','note','details_rows']`** — không có
   bear_the_shipping; không snapshot customer_name (màn nhập dùng quan hệ supplier/customer).
   KHÔNG đưa `status` vào catalogColumns (entity-history §3a) → đổi trạng thái ghi dòng
   `change_status` riêng.
6. **Lý do từ chối phải vào `note` của log** (entity-history §4.1) → `deny()` gọi
   `logCatalogStatus(..., $comment)`.
7. Ô trống bảng đồng bộ về `''` (như màn export), thay cho `'—'` hiện tại.

## Giải pháp

### BE
- `WarehouseImportRequestResource`: thêm `updater_name` (employee_update.info.fullname),
  `requester_name` (productImportRequest.employee_create.info.fullname),
  `updated_at` (Carbon `d/m/Y H:i`).
- `V1/WarehouseImportRequestController::index()`: thêm sortMap
  (type_name→type; product_import_request_code join product_import_requests;
  supplier_name join customers theo supplier_id); eager-load thêm
  `employee_update.info`, `productImportRequest.employee_create.info`.
- `WarehouseImportRequestService`: `use LogsCatalogHistory` + catalogTable/catalogColumns/
  catalogDisplay/detailRows/numText/statusText/logStatusChanged; ghi log ở
  createFromImportRequest (create), updateDraft (update + status), deny (status + note),
  cancel (status).
- `CatalogHistoryService::TABLES`: đăng ký `warehouse_import_requests` nhãn tiếng Việt trung
  tính (type→Loại nhập, warehouse_id→Kho nhập, note→Ghi chú, details_rows→Bảng chi tiết hàng
  hóa), KHÔNG có status.

### FE
- `index.vue`: đổi nhãn creator_name; thêm 4 cột (updated_at center, updater_name,
  requester_name, approver_name) + cell template; thêm `sortable:true` cho type_name,
  product_import_request_code, supplier_name; thêm action `history` (icon `ri-history-line`,
  luôn hiện) + goHistory + `<CatalogHistoryModal>`; ô trống `'—'`→`''`.
- `_id/index.vue`: thêm `<SystemInfoSection entity-type="warehouse_import_requests" ...>`.

## Verify
- Playwright (mock client-side, emp 48 thiếu quyền) như ticket trước: xác nhận 4 cột mới,
  nhãn "Người tạo", sort 3 cột, menu có "Xem lịch sử", detail có mục Lịch sử.
- BE log: KHÔNG chạy trên DB thật; kiểm bằng đọc code + (nếu cần) tinker trên erp_hrm_check.
