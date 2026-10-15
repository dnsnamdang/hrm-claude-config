# Khảo sát hàng tạm ĐANG CÓ trên HRM (BOM list / Báo giá) — 12/10/2026

> Chỉ đọc code worktree `wt-chuyen-doi-hang-hoa` + SELECT `hrm_erp_giacty`. Bổ sung cho `khao-sat-be-erp.md` / `khao-sat-fe-erp.md`.

## 1. Không có bảng hàng tạm riêng
Hàng tạm HRM = **dòng BOM / dòng báo giá có `erp_product_id IS NULL`** (không cờ riêng; `SHOW TABLES LIKE '%product_project%'` = 0).

| Bảng | Dòng | Hàng tạm | Cột chính | Ghi chú |
|---|---:|---:|---|---|
| `bom_list_products` | 436 | 73 hàng + 1 dịch vụ | name, code (`HHB`+id — `BomListService.php:2336-2338`), model_id, brand_id, origin_id, unit_id, qty_needed, product_attributes (TSKT), note, estimated_price, product_type 1/2, parent_id, erp_product_id, erp_sync_status (0 cả 436) | không `company_id`, `created_by` (lấy `bom_lists.created_by`); `product_project_id` NULL cả 436 |
| `quotation_product_prices` | 6.288 | 510 (353 có mã HHB/HHBG) | như trên + quoted_price, vat_percent, chiết khấu, `erp_tmp_product_id` (0 dòng), `bom_list_product_id`, created_by | mã `HHBG` (`QuotationService.php:2601,2615`); không `company_id` |

## 2. Tạo ở đâu
Popup chung `hrm-client/pages/assign/quotations/components/QuotationProductSearchModal.vue` — nút "Thêm hàng tạm" (:61), 2 tab "Tái sử dụng" (:277) / "Thêm mới thủ công".
Dùng ở: BOM `BomBuilderEditor.vue:196`, `BomBuilderAddProductModal.vue:73,164`, nhân bản `BomBuilderTableCard.vue:330`; báo giá tự lập `pages/assign/quotations/_id/edit.vue:1321`.
Bắt buộc (`:1545-1560`): **Tên, ĐVT, Thương hiệu, Xuất xứ, Nhóm hàng** (nếu BOM có nhóm). Không bắt buộc: Model, TSKT, SL, ghi chú, giá dự kiến/báo giá.
⇒ **ÍT HƠN nhiều** so với trường bắt buộc tab "Thông tin hàng hoá" của form hàng hoá HRM (Loại SP, hãng SX, VAT, ảnh…).

## 3. Vòng đời hiện tại (chưa từng chạy trên dữ liệu)
- `TmpProductSyncService::sendApproval` (`Modules/Assign/Services/TmpProductSyncService.php:21-86`) — chỉ báo giá Trúng thầu (`QuotationController.php:739`): đẩy dòng `erp_product_id NULL` sang ERP `sync-from-hrm` ⇒ ghi `erp_tmp_product_id`; `pullStatus` (:92-137) ghi `erp_product_id` khi ERP duyệt ⇒ dòng đổi thành hàng thật. `quotations.tmp_sync_status` NULL cả 206.
- `QuotationErpSyncService::createTmpProducts` (:105-129) — duyệt báo giá ⇒ INSERT thẳng `tmp_products` status 2 (thiếu cột NOT NULL), không map ngược.
- BOM không có đường đồng bộ (`ProductProjectController.php:220`).

## 4. Màn "Danh sách hàng tạm" `/assign/product-project`
Chỉ xem: UNION dòng BOM tổng hợp Đã duyệt + báo giá tự lập Đã duyệt/Trúng thầu (`ProductProjectController.php:184-229`), gộp trùng mã trong dự án, ẩn hàng ERP gốc. Cột: Mã, Tên, Mã BOM, Model, Dự án, Giải pháp, Thương hiệu, Xuất xứ, ĐVT, TSKT, Hàng cha, Ghi chú, Mã ERP, Trạng thái đồng bộ. Không gate quyền (`api.php:476` chỉ `auth:api`). Endpoint `reuseChildren` (`only_temp`) phục vụ tab "Tái sử dụng".

## 5. YCHG chưa nhận được dòng chưa có mã
`price_asking_request_products.product_id` **bigint NOT NULL** (6.729 dòng); `PriceAskingRequestWriter.php:68,151-162,212` chỉ nhận `product_ids`, báo "Không tồn tại" nếu không khớp; `PriceCalculateRequestService.php:246,341` dựa `product_id`.
