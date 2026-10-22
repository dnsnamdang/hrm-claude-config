# Lịch sử chỉnh sửa hàng hoá (HRM) — thiết kế

> 21/10/2026 · nhánh `gop_db` (đã go-live) · theo skill `entity-history` (khuôn chuẩn mới).
> Mở lại mục §14b `man-danh-muc-hang-hoa/design.md` (trước go-live đã HOÃN lịch sử hàng hoá).

## 1. Đã chốt với user (21/10)

| # | Câu | Chốt |
|---|---|---|
| H1 | Track trường nào | **Toàn bộ form + tab Quản trị theo công ty**. Giá bán KHÔNG (đã có log riêng `product_prices`) |
| H2 | Thao tác nào | **Mọi luồng ghi hàng hoá**: tạo, sửa, lấy về, khoá/mở khoá, xoá, phát hành, đổi trạng thái, duyệt/từ chối hàng tạm, gán catalog, luồng duyệt giá đổi trạng thái hàng |
| H3 | Ai xem | Quyền ERP có sẵn **"Xem lịch sử chỉnh sửa hàng hóa"** (id 101050, seeder ERP khai, bảng `permissions` dùng chung) |
| H4 | Log cũ ERP (`product_histories` 324.413 dòng + `product_versions` 116.787) | **HRM tính từ go-live 21/10**, log cũ xem ở màn ERP `productHistory` — không chuyển dữ liệu, không đọc legacy |

## 2. Hiện trạng (khảo sát 21/10)

- HRM chưa ghi gì: `ProductWriteService` docblock ghi rõ "không lịch sử". Không có endpoint đọc.
- Màn danh sách `components/product/ProductListPage.vue` (5 vỏ warehouse/trading/company/entering/temp): menu ⋮ chưa có Lịch sử.
- Màn chi tiết `pages/master-data/products/_id/index.vue`: chưa có khối Lịch sử.
- Mẫu gần nhất: `ProductPriceHistoryModal.vue` (V2BaseModal + `SystemInfoSection` + endpoint riêng có gate) và
  `GATED_TABLES` `position_transfers` (khoá ảo dạng BẢNG do `loadVirtualRows()` dựng, endpoint riêng có gate).

## 3. Thiết kế

### 3.1 Lưu
- Bảng chung `catalog_histories`, `table_name = 'products'`, `table_id = products.id`. KHÔNG tạo bảng mới, không migration.
- Khai `products` vào **`CatalogHistoryService::GATED_TABLES`** (không vào `TABLES` — route chung không gate quyền).
- Ngừng hẳn ghi `product_histories` / `product_versions` (đã chốt §11b/§11c), dữ liệu cũ giữ nguyên.

### 3.2 Snapshot (giá trị HIỂN THỊ, không id)
Service mới `Modules/MasterData/Services/Product/ProductHistoryService.php`: `snapshot(int $productId): array` đọc từ DB
(không từ request) ⇒ chụp TRƯỚC và SAU mỗi thao tác rồi `logUpdate()` — 1 lần lưu = 1 dòng log nhiều khoá.

**Trường thường (`products`)**: Tên, Tên tiếng Anh, Tên thường gọi, Barcode, Ghi chú, Model, Code đặt hàng, Thương hiệu,
Hãng sản xuất, Xuất xứ, Loại sản phẩm, Đặc tính, Trọng lượng, Kích thước, Định mức, Phụ kiện tiêu chuẩn, Thông số kỹ thuật,
Tính năng đặc biệt, Tên hải quan, Mã HS, SL mua tối thiểu, 4 thuế (lưu nhãn `tax_rates`), Thuế BVMT (hệ số / "Không"),
Hệ số công nghệ, Ảnh đại diện. Nhãn = nhãn ô trên form. Chuẩn hoá: 0/''/null ⇒ null, số bỏ `.00` thừa.

**Khoá dạng BẢNG** (§3b/§4b skill — `__key` ghép cặp, `__name` tên dòng, `__brief` cột "thuộc về"):

| Khoá | Nguồn | `__key` | `__name` | Cột |
|---|---|---|---|---|
| `unit_rows` Đơn vị tính | `product_units` | id | tên ĐVT | Hệ số quy đổi |
| `attribute_rows` Thuộc tính | `attribute_products` | attribute_id | tên thuộc tính | Giá trị, Đơn vị, In |
| `recipe_rows` / `accessory_rows` / `install_accessory_rows` / `repair_accessory_rows` (4 nhóm hàng kèm) | 4 bảng kit | product con id | mã - tên hàng | Số lượng (nếu có) |
| `tech_attachment_rows` Tài liệu kỹ thuật | `product_tech_attachments` | url | tên tệp | Loại tài liệu — GIỮ nguyên URL (§3b) |
| `gallery_rows` / `video_rows` Ảnh / Video | `product_galleries` / `product_videos` | url | tên tệp | — |
| `vehicle_rows` Phân loại xe | `product_vehicle_model_has_life` | model × đời | dòng xe - model - đời | — (xem T2) |
| `machine_group_rows` / `machine_rows` | `productables` | id đích | tên nhóm máy / mã-tên máy | — |
| `company_rows` Quản trị theo công ty | `product_company_coefficients` | company_id | tên công ty | Chính sách KD, Tồn tối thiểu, Bảo hành, Loại BH |
| `supplier_rows` Nhà cung cấp | `product_suppliers` | company × NCC | tên NCC | `__brief` = Công ty |
| `catalog_rows` Catalog kinh doanh | `product_business_catalogs` | company × tiểu mục | đường dẫn catalog | `__brief` = Công ty |

**Trạng thái theo công ty** (`product_company_coefficients.status`) KHÔNG nằm trong `company_rows` — đổi trạng thái ghi
dòng RIÊNG (§3a skill): `lock` / `unlock` / `change_status`, nội dung "Công ty X: <cũ> → <mới>", lý do (nếu thao tác có) vào `note`.

### 3.3 Điểm ghi (mọi luồng — H2)

| Luồng | Hàm | Action |
|---|---|---|
| Tạo | `ProductWriteService::store` | `create` |
| Sửa đầy đủ / sửa chung / tab Quản trị | `update` / `updateCommon` / `updateAdmin` | `update` |
| Lấy về | `take` | `change_status` ("Công ty X: — → Nhập thông tin") |
| Khoá / Mở khoá / Đổi trạng thái / Phát hành | `ProductLifecycleService::lock/unlock/setStatus/release` | `lock` / `unlock` / `change_status` |
| Xoá (mềm) | `destroy` / `destroyTemp` | `delete` (`hardDelete` xoá luôn log của hàng — như đang xoá product_histories) |
| Hàng tạm | `TempProductService::create/update`; `PriceAskingRequestWriter::tempApprove/tempSave/tempReject` | `create` / `update` / `approved` / `rejected` (+ lý do) |
| Gán catalog | `ProductCatalogService::sync` | `update` (khoá `catalog_rows`) |
| Duyệt giá đổi trạng thái hàng | `ProductPriceApprovalService` :542 / :749 | `change_status` |

### 3.4 Đọc
- `GET master-data/products/histories/{id}` + `.../histories/filter-options` — gate "Xem lịch sử chỉnh sửa hàng hóa"
  (xem T3), trả DTO chuẩn qua `CatalogHistoryService::getLogs('products', $id)`; người thực hiện qua `HistoryPerformerOptions`.

### 3.5 FE (đủ 2 nơi — §5.1 skill)
- **Danh sách** `ProductListPage.vue`: menu ⋮ thêm `Lịch sử` (icon `ri-history-line`), chỉ hiện khi có quyền; popup
  `components/product/ProductHistoryModal.vue` = khuôn `ProductPriceHistoryModal` (V2BaseModal + SystemInfoSection,
  endpoint riêng). Tiêu đề "Lịch sử hàng hoá: <Tên>" (không kèm mã).
- **Chi tiết** `_id/index.vue`: `SystemInfoSection` NGOÀI card, sát dưới, full ngang (khuôn `meeting/_id/show.vue`),
  thu gọn sẵn, `v-show`; chỉ dựng khi có quyền.

## 4. Chốt thêm 21/10 (hết treo)

- **T1 — chỉ CÔNG TY ĐANG LÀM VIỆC.** Thông tin chung của hàng ai cũng thấy; dữ liệu Quản trị / NCC / catalog / trạng thái của
  công ty khác bị ẩn. Cách lưu: tách 2 nguồn trong `catalog_histories` (không migration):
  - `('products', products.id)` — thông tin chung + bảng con chung (§3.2 trừ 3 khoá dưới).
  - `('product_company_admin', product_company_coefficients.id)` — `company_rows` (4 ô), `supplier_rows`, `catalog_rows` và
    dòng trạng thái lock/unlock/change_status của ĐÚNG công ty đó (giống log giá `product_prices` đang khoá theo pcc.id).
  - 1 lần lưu form đầy đủ đổi cả 2 phần ⇒ 2 dòng log (cùng thời điểm, cùng người). Đọc: gộp log `products` + log pcc của
    công ty đang làm việc, sắp mới → cũ. Bỏ cột "Công ty" khỏi `__brief` (đã ngầm hiểu là công ty đang làm).
- **T2 — Phân loại xe**: 1 lần lưu đổi ≤ 50 dòng xe thì liệt kê từng dòng; > 50 ghi gọn "Phân loại xe: thêm N dòng, xoá M dòng".
- **T3 — Gate**: có quyền "Xem lịch sử chỉnh sửa hàng hóa" tại CÔNG TY ĐANG LÀM VIỆC (`PermissionService` như R22).
  Không có quyền ⇒ API 403, FE ẩn mục menu + khối chi tiết.

## 5. Kiểm
- Script test TỪNG TRƯỜNG MỘT (§7a skill): mỗi cột `products`, mỗi cột mỗi bảng con, thêm/xoá 1 dòng mỗi bảng con, đổi nhiều
  trường 1 lần, không đổi gì, lưu lại lần 2 — bọc transaction rollback. Mỗi luồng ở §3.3 ít nhất 1 ca.
- PHPUnit: có quyền / không quyền (đọc 403) — [[always-test-permission-cases]].
- Playwright MCP: popup danh sách + khối chi tiết giống nhau, 4 bộ lọc, ẩn khi không quyền; thêm spec e2e.
