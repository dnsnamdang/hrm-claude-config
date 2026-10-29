# Revert điều chuyển kho chi nhánh về logic cũ (hủy giữ trước) + chặn tại YCXH

## Bối cảnh
Màn YCXH: `/admin/warehouse/product_export_requests?type=all`.
- **YCXH** = `product_export_requests` (Yêu cầu xuất hàng). **YCCH** = `product_transfer_requests` (Yêu cầu chuyển hàng).
- `type = 7` = `XUAT_DIEU_CHUYEN_KHO_CHI_NHANH` (điều chuyển kho chi nhánh, chéo công ty).
- YCXH `hasMany` YCCH qua `product_transfer_requests.product_export_request_id`. DB đã hỗ trợ 1:n.
- YCCH **chỉ** dùng cho điều chuyển chi nhánh (controller `:425-426` require YCCH chỉ khi type 7).

## Vấn đề (logic hiện tại cần đổi)
Từ commit `e97d3aa74c`/`373737c252`/`4ba07a032e`, điều chuyển chi nhánh **xuất thẳng từ hàng giữ của KD**
(export_from_prepick), + guard "1 YCXH chỉ gồm YCCH của **cùng 1 người** tạo" → thực tế **1 YCXH : 1 KD**.
→ Mỗi luồng điều chuyển phải duyệt nhiều phiếu rời.

## Yêu cầu (user chốt)
1. Điều chuyển chi nhánh **qua kho** (non-direct) quay về **logic cũ**: xuất **từ tồn tự do**, buộc **hủy giữ trước**.
2. Cho **1 YCXH : n YCCH của nhiều KD** → gộp duyệt.
3. **Chặn (B1 triệt để)** tại bước **lập YCXH** điều chuyển chi nhánh: quét toàn bộ YCCH được thêm → gom
   theo từng KD → nếu KD nào **còn giữ** (`PrepickDetail.qty > 0`) sản phẩm mình điều chuyển tại **công ty nguồn**
   → chặn, báo cần hủy giữ trước.
4. **Ngoại lệ (user lưu ý):** YCXH tích **"xuất thẳng"** (`is_export_direct`) **GIỮ NGUYÊN** hành vi cũ
   (vẫn xuất theo giữ + vẫn ràng buộc 1 YCXH : 1 KD). Chỉ luồng **non-direct** mới revert + chặn + cho n KD.

## Phát hiện then chốt (xác minh trong code)
- `ProductExportRequest.php:63`: YCXH type 7 → `company_id = export_company_id`. Tức **"gửi đến công ty"
  (`export_company_id`) chính là công ty nguồn** = pool giữ.
- `ProductExport.php:1409/1423`: logic trừ giữ dùng `$this->company_id` (= `export_company_id`). → giữ của KD ở `export_company_id`.
- **Công tắc trừ giữ duy nhất** = `WarehouseExportRequest::getCanExportFromPrepickAttribute()` (`can_export_from_prepick`,
  dùng ở `:945`). Nếu trả `false` cho non-direct type 7 → `export_prepick_qty = 0` → `ProductExport:1386-1453`
  tự bỏ qua. **Không cần sửa `ProductExport`.**
- Cả direct lẫn non-direct đều chạy `ProductExport::updateWarehouse`; khác nhau chỉ ở `export_from_prepick`.
- Commit `4ba07a032e` (pending_prepicks ở `Product::getAccountingStockDetail`): **GIỮ** — vẫn đúng cho direct type 7
  (còn `export_prepick_qty`), vô hại với non-direct (sau revert `export_prepick_qty = 0`). Không revert.

## Thiết kế

### A. Revert xuất-theo-giữ — CHỈ non-direct
- `WarehouseExportRequest::getCanExportFromPrepickAttribute()` (:613-621): nhánh type 7 thêm điều kiện
  `&& is_export_direct` (lấy từ `product_export_request->is_export_direct`). Non-direct type 7 → xuất từ tồn.
- `getTransferRequesterId()` + usages (:692, :922): chỉ còn tác dụng khi `export_prepick_qty` được tính
  (= direct type 7, 1:1 → `first()` đúng). Giữ nguyên; verify non-direct validate đi nhánh tồn đúng.
- **Không** sửa `ProductExport.php:1386-1453` (tự bỏ qua).
- FE `formJs.blade.php`: `can_export_prepick` + `employee_id` cho type 7 chỉ bật khi `is_export_direct`.

### B. Ràng buộc 1 YCXH : 1 KD — có điều kiện
- `ProductExportRequestsController.php:701-711` (store) + `:1214-1223` (update): guard
  `count(created_by) > 1 → lỗi` **chỉ giữ khi `is_export_direct`**; non-direct bỏ.
- FE same-creator block (`:219-226`) + `checkWithCreator` (`:239-253`): chỉ chặn khi xuất thẳng.

### C. Chặn hủy giữ tại YCXH — CHỈ non-direct
- Trong khối type 7 ở store/update, khi `!is_export_direct`:
  - `$sourceCompanyId = $request->export_company_id`.
  - Quét `$request->product_transfer_requests` → mỗi YCCH: `created_by` (KD) + products (`ProductTransferRequestProduct`).
  - Với mỗi (KD, product): tổng `PrepickDetail` `where product_id, employee_id=KD, company_id=$sourceCompanyId, qty>0`.
  - Tổng > 0 → gom lỗi theo KD, trả `responseErrors`:
    > "Kinh doanh [tên] đang giữ [N] [tên SP] tại công ty nguồn. Cần hủy giữ trước khi lập yêu cầu xuất điều chuyển."
- Direct **không** áp (vẫn xuất theo giữ).

### D. Đã kiểm
- `ProductImportDirectDetail` không tự trừ prepick; direct vẫn qua `updateWarehouse`, switch là `export_from_prepick`.
- `4ba07a032e`: GIỮ (lý do ở trên).

## Ràng buộc
- DB = PROD `hrm_erp_gop` → chỉ sửa code + SELECT xác minh, **KHÔNG ghi DB**.
- `php -l` sạch; không đụng hàm dùng chung nếu chưa hỏi.
- Không commit/push khi chưa yêu cầu.
