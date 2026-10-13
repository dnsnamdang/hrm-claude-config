# Fix: điều chuyển kho chi nhánh không trừ giữ (prepick) của người yêu cầu

## Bối cảnh
Luồng "Xuất điều chuyển kho chi nhánh" (ProductExportRequest type=7) **xuất qua kho** (`is_export_direct=0`) khi xuất xong KHÔNG trừ "giữ" (PrepickDetail) của người yêu cầu điều chuyển → kế toán phải hủy giữ thủ công.

## Root cause (đã xác nhận bằng data — PER 1043, giữ 1831)
- Hàng phân bổ 100% từ tồn (`export_from_stock`), `export_from_prepick=0` → khối trừ prepick chung không chạy.
- Nhánh xử lý điều chuyển sẵn có (`ProductExport` ~dòng 1236) chỉ chạy khi `is_export_direct=1` và trừ `ProductImportDirectDetail` (không phải PrepickDetail).
- "Giữ từ mua nhập khẩu" (`ProductImportDetailCustomer`) tạo CẢ `ProductImportDirectDetail` (xuất thẳng) LẪN `PrepickDetail` (xuất qua kho). Xuất qua kho phải trừ PrepickDetail nhưng bị bỏ sót.

## Fix
- [x] `ProductExport` (sau nhánh xuất thẳng, trước `DB::transaction` xuất kho): thêm nhánh — khi `!is_export_direct && type==XUAT_DIEU_CHUYEN_KHO_CHI_NHANH` → trừ `PrepickDetail` của **người yêu cầu** (`product_transfer_requests->first()->created_by`) tại **cty nguồn** (`$this->company_id`), theo `export_qty`, FIFO theo `expire_date`, ghi `PrepickLog`.
- [x] `php -l` sạch + dry-run xác nhận query khớp đúng giữ 1831.
- [ ] Test E2E: tạo phiếu điều chuyển mới + xuất → giữ giảm đúng SL.

## Quyết định thiết kế
- Trừ FIFO theo `expire_date`, **không lọc customer** (nhất quán với nhánh xuất thẳng dùng ProductImportDirectDetail vốn không có customer). Nếu cần khớp customer theo từng dòng điều chuyển → follow-up.

## Dữ liệu test (local dev_erp_2)
- Giữ mẫu: prepick_details.id=1831 (emp 222 SG, product 40412, cty 1 HN, customer 8, qty 20).
- Tài khoản (mk `Tanphat@123`): 222 honghv.kd5 (tạo YC điều chuyển), 429 phuongtt.ktsg (duyệt), 787 loitt.qttt (tạo phiếu xuất).
- Ca đã chạy code CŨ: PTR 4227 → PER 1043 (giữ KHÔNG trừ — đúng bug).

CHƯA commit — chờ test E2E.

---

## Phase 2 — Regression: khối "--- Trừ PREPICK ---" luồng chuẩn lọc customer làm điều chuyển chi nhánh luôn báo lỗi

### Bối cảnh phát sinh (2026-08-12) — phiếu xuất we#31381 (CH-TDH)
Sau khi refactor bỏ patch trừ giữ riêng (comment `ProductExport` dòng 1293-1296) → chuyển trừ giữ điều chuyển sang **luồng chuẩn**: `getCanExportFromPrepick` giờ tính cả type=7 → `export_from_prepick>0` → khối "--- Trừ PREPICK ---" (dòng 1379-1436) chạy. Nhưng khối này lọc `->where('customer_id', $this->customer_id)` (dòng 1392, 1404) → với điều chuyển chi nhánh `customer_id=NULL` → chỉ khớp giữ KHÔNG gắn khách.

### Root cause (xác nhận bằng data prod erp_new)
- Bất đối xứng customer_id: bước ĐỀ NGHỊ (`getAccountingStockDetail`, dòng 2426 `if (!empty($customer_id))`) bỏ qua filter khách khi phiếu không khách → cộng dồn mọi giữ của NV yêu cầu điều chuyển → `export_prepick_qty>0`. Bước TRỪ (main-loop) lại ép `customer_id IS NULL`.
- **Toàn hệ thống: 0 dòng prepick `customer_id IS NULL` & qty>0 (cả 2541 giữ đều gắn khách).** → nhánh trừ giữ điều chuyển KHÔNG BAO GIỜ khớp → luôn ném "Xuất nhiều hơn lượng prepick hiện có".
- Ý định thiết kế gốc "không lọc customer" (mục Quyết định thiết kế trên) bị mất khi refactor sang luồng chuẩn.
- Record 31381: giữ 56254 (NV412/KH2566/cty1) tạo 10/08 qty=1 → đề nghị chốt export_prepick_qty=1 (11/08 08:39) → giữ bị HUỶ (11/08 08:48, qty=0) → phiếu xuất lập 09:09 báo lỗi. Ngay cả sau fix B, record này giữ đã=0 → cần xử lý riêng.

### Quyết định (user chốt 2026-08-12): **Cách B**
Điều chuyển chi nhánh trừ giữ của **đúng nhân viên yêu cầu điều chuyển** (chéo công ty), **KHÔNG quan tâm giữ cho khách nào** ở cty nguồn. Đối xứng với nhánh xuất thẳng (`ProductImportDirectDetail`, dòng 1248-1262 vốn không lọc customer).

### Fix
- [x] `ProductExport` khối "--- Trừ PREPICK ---" (dòng 1390-1409): bỏ filter `customer_id` khi `type==XUAT_DIEU_CHUYEN_KHO_CHI_NHANH` (2 query sum + get, dùng `->when(!$is_transfer_branch, ...)`). Các loại khác giữ nguyên lọc customer.
- [x] `php -l` sạch.
- [x] Xử lý record 31381 (user chọn Cách a — 2026-08-12): giữ 56254 đã tự huỷ (qty=0), FE dùng `export_prepick_qty` STALE từ đề nghị (ProductExport.blade dòng 236-267, KHÔNG tính live). Đề nghị 32162 có **3 dòng** (CH-TDH/CH-MHDT/CH-GTD:01) đều `export_prepick_qty=1` & giữ NV412/cty1 hiện = 0 → phải sửa cả 3. Tồn kho2/cty1 đủ (47044=2 free2, 47045=2 free2, 47046=2 free1). Đã chạy prod `erp_new`: `UPDATE warehouse_export_request_details SET export_prepick_qty=0 WHERE parent_id=32162 AND export_prepick_qty>0` → 3 dòng. User mở lại form → export_from_prepick=0, xuất theo tồn.
- [ ] Cách C (re-clamp) — user chưa làm, để follow-up chống tái diễn giữ huỷ/giảm sau đề nghị.
- [ ] Test E2E lại: tạo phiếu điều chuyển mới của NV có giữ theo khách → xuất → giữ giảm đúng.

