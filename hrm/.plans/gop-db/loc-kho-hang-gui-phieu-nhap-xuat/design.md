# Lọc kho hàng gửi ở các phiếu/yêu cầu nhập–xuất

**Phụ trách:** @namdangit · **Nhánh:** `gop_db` (cả ERP + hrm-api + hrm-client) · **Ngày:** 2026-09-17

## Mục tiêu
Cấu hình `companies.consignment_warehouse_ids` (JSON mảng **id kho kế toán** = "kho hàng gửi",
khai ở tab *Công nợ & tài chính* màn quy chế-cấu hình HRM) phải chi phối dropdown chọn kho ở các
phiếu/yêu cầu nhập–xuất, theo LOẠI phiếu.

## Quy tắc (từ ảnh Redmine + yêu cầu bổ sung của user)
1. **YC nhập hàng + Đề nghị nhập kho, loại "Nhập gửi" (type 14):** dropdown **kho vật lý** chỉ hiện
   những kho vật lý CÓ gắn ít nhất 1 kho kế toán là kho hàng gửi (aw.id ∈ consignment_ids).
2. **YC xuất hàng + Đề nghị xuất kho, loại "Xuất gửi" (type 12):** như (1) cho kho vật lý.
3. **Phiếu nhập hàng, loại "nhập gửi" (14):** dropdown **kho kế toán** chỉ hiện kho hàng gửi
   (aw.id ∈ consignment_ids) thuộc kho vật lý đã chọn.
4. **Phiếu xuất hàng, loại "xuất gửi" (12):** như (3) cho kho kế toán.
5. **(bổ sung)** Các loại KHÁC nhập gửi/xuất gửi: dropdown **kho kế toán** KHÔNG hiện kho hàng gửi
   (loại trừ aw.id ∈ consignment_ids).

## Data model (đã xác nhận)
- `warehouses` = kho vật lý; `accounting_warehouses` = kho kế toán, có `warehouse_id` (→ kho vật lý,
  NULL nếu nhập/xuất thẳng), `company_id`, `status`. 1 kho vật lý → N kho kế toán.
- `companies.consignment_warehouse_ids` = text JSON mảng **id accounting_warehouses**, per company.
  Rỗng `[]`/NULL ⇒ chưa cấu hình: rule 1–4 ra dropdown RỖNG (đúng nghĩa), rule 5 loại trừ tập rỗng
  (Laravel `whereNotIn([])` = `1=1`) nên không ảnh hưởng gì. Xử lý graceful, không cần guard tay.
- Type "gửi": ERP nhập 14 / xuất 12 (`public/js/constant.js`); HRM `NHAP_GUI=14`, export `=== 12`
  (`ProductExportRequestController:598 // Xuất hàng gửi`).

## Kiến trúc giải pháp
- **Nguồn sự thật id kho hàng gửi:**
  - ERP: accessor `Company::getConsignmentWarehouseIdsAttribute` (mirror `promo_warehouse_ids`) +
    `Warehouse::getConsignmentWarehouse()` (mirror `getPromoWarehouse()` — trả kho vật lý gắn kho hàng gửi).
  - HRM: helper trong service đọc `companies.consignment_warehouse_ids` của công ty hiện tại.
- **Kho vật lý (requests):** loại 14/12 → dùng danh sách kho vật lý "gắn kho hàng gửi"; loại khác giữ nguyên.
- **Kho kế toán (vouchers):** loại 14/12 → chỉ aw.id ∈ consignment_ids của kho vật lý đã chọn;
  loại khác → loại trừ aw.id ∈ consignment_ids. Luôn giữ `includeIds` (kho khoá phiếu đang dùng).

## Điểm chạm
- **ERP** (Angular filter phía client + model): `Company.php`, `Warehouse.php`, `AccountingWarehouse.php`;
  blade: product_import_requests, warehouse_import_requests, product_export_requests,
  warehouse_export_requests, product_imports, product_exports (create/edit).
- **HRM-api:** ProductImportRequestService/Controller, WarehouseImportRequestController, ProductImportController;
  ProductExportRequestController, WarehouseExportRequestController, ProductExportController.
- **HRM-client:** các form tương ứng dưới `pages/finance/`.

## Quyết định đã chốt
- Scope: **cả ERP và HRM** (user chốt qua AskUserQuestion).
- Rỗng `[]` xử lý tự nhiên bằng ngữ nghĩa `whereIn/whereNotIn` của Laravel, KHÔNG guard tay.
- Kho vật lý loại KHÁC gửi: KHÔNG đổi (yêu cầu 5 chỉ nói về kho kế toán).
