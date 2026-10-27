# Kho › Nhập kho — 4 màn còn lại (ERP → HRM) — Design

**Người phụ trách:** @junfoke — 2026-10-22 · Nhánh `feat/kho-nhap-kho-con-lai` (cả 2 repo, tách từ `develop`)
Plan: `.plans/gop-db/nhap-kho-con-lai/plan.md`

ĐNNK + PNK đã port (`/finance/warehouse-import-requests`, `/finance/warehouse-imports`). Đợt này 4 màn còn lại của menu ERP
`Kho › Nhập kho`, đặt ở phân hệ Kho (`/warehouse/...`).

## User chốt 22/10/2026

1. Làm trên nhánh mới.
2. Quyền: khai quyền HRM mới TÊN Y ERP (guard api, type 21 Kho), kiểm bằng trait `ChecksEmployeePermission` (khớp tên cả
   2 guard → role ERP vẫn chạy) — cùng khuôn Kiểm kê theo vị trí / Điều chuyển vị trí. Không gắn middleware checkPermission.
3. Bước nghiệp vụ SAU chưa port → **vẫn hiện nút, trỏ sang ERP** làm tiếp (FE ghép `ERP_URL`, như `SelfInventoryService::ERP_*_PATH`).
4. Được thêm nút vào Phiếu xuất kho HRM (cho màn Nhập lại điều chỉnh sai số liệu).

## Phase 1 — Chờ báo thừa, thiếu + Phiếu báo hàng thừa, thiếu nhập kho

| Màn | Nguồn ERP | HRM |
|---|---|---|
| Phiếu nhập kho chờ báo thừa, thiếu | `WarehouseImportsController@discrepancy` + `WarehouseImport::searchByDiscrepancyFilter` | `/warehouse/import-discrepancies` |
| Phiếu báo hàng thừa, thiếu nhập kho | `excShortage*` + `ExcShortageWarehouseImport(+Lot)` | `/warehouse/exc-shortage-imports` |

- Hàng đợi = PNK `status = 1`, `type IN (12,13,15,1,11,2)`, có lô `CAST(request_qty AS SIGNED) != CAST(qty AS SIGNED)`, chưa có phiếu báo.
- Phiếu báo: Đang tạo (1) → Chờ xử lý (2) → Đã xử lý (3, do phiếu xử lý hàng thiếu ERP set) / Không duyệt (6, sửa gửi lại).
  KHÔNG ghi tồn / kế toán. Mã `{mã cty}_BHNK-xxxxx` (giữ công thức ERP `generateCode`). File S3 thư mục `delivery_international_general`.
- Thông báo: Gửi → người có quyền "Duyệt phiếu báo hàng thừa, thiếu nhập kho"; Không duyệt → người tạo.
- Nút "Xử lý" (status 2 + quyền duyệt) → ERP `/admin/inventory/discrepancy/create?exc_shortage_warehouse_import_id=` (chưa port).
  Link HĐ → ERP (`/admin/orders/buy_contract2/{id}/show` khi step 1, `/admin/orders/inland_buy_contract_new/{id}/show`);
  PNK → HRM `/finance/warehouse-imports/{id}`; Yêu cầu nhập → HRM `/finance/product-import-requests/{id}`.
- Quyền (4, group "Xử lý thừa, thiếu nhập kho"): Xem … theo tổng công ty / theo công ty, Tạo phiếu báo (hoặc "Thủ kho" như
  ERP — HRM chưa có quyền "Thủ kho" ⇒ chỉ quyền Tạo), Duyệt phiếu báo.
- Sửa lỗi ERP: danh sách phiếu báo áp phạm vi như hàng đợi (ERP `type=all` không áp); lọc ngày (ERP `'=>'`); Không duyệt
  kiểm quyền duyệt; dữ liệu nguồn LEFT JOIN (ERP INNER JOIN lỗi khi PNK không có ĐNNK / YC nhập); `canView` chặn 404.

## Phase 2 — Phiếu nhập kho điều chỉnh kiểm kê (`warehouse_inventory_imports`)

Nguồn = Phiếu kiểm kê hàng hóa (SelfInventory, hàng THỪA `diff_qty > 0`); Gửi duyệt ghi tồn ngay (lô mới type 3
`NHAP_DIEU_CHINH`, `PhysicalStockWriter` thêm hàm mới); bước Kế toán kho "Tạo phiếu nhập hàng" (`inventory_imports`) → ERP.
Nút ở màn kiểm kê HRM đổi từ ERP sang màn HRM mới.

## Phase 3 — Phiếu nhập lại điều chỉnh sai số liệu (`warehouse_reimports`)

Nguồn = Phiếu xuất kho bị Kế toán kho "Không duyệt" (status 4) → thêm "Tạo phiếu nhập lại" vào Phiếu xuất kho HRM; ghi
tồn ngược (8 bảng, dùng lại lô cũ). "Tạo phiếu xuất lại" → chi tiết ở plan phase 3.
