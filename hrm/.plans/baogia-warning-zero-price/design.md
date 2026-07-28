# baogia-warning-zero-price — Tóm tắt

**Màn:** `/assign/quotations` — Tạo/Sửa/Chi tiết báo giá, hành động **Gửi duyệt**.
**Phụ trách:** @manhcuong · **Ngày:** 2026-07-20

## Mục tiêu
Khi bấm "Gửi duyệt": (1) cảnh báo dòng đơn giá bán = 0đ (highlight cam + popup SKU/tên), (2) định tuyến duyệt theo độ "sạch": sạch → auto-duyệt thẳng; không sạch → luồng phân cấp ngưỡng cũ.

## Quyết định chốt
1. **Sạch → auto-duyệt luôn** (bỏ qua ngưỡng); **không sạch → ngưỡng cũ** (TP/BGĐ).
2. **Auto-duyệt = duyệt thẳng** (`DA_DUYET`, người duyệt = người tạo, không thao tác).
3. **Mọi ràng buộc giá 0 → cảnh báo** (đơn giá bán=0, giá vốn hàng tạm=0). Giữ chặn "giảm giá vượt đơn giá bán".
4. **"Không sạch"** = có hàng tạm (erp_product_id NULL) HOẶC dịch vụ HOẶC giảm giá mặt hàng (method=1) HOẶC giảm giá tổng (method=2) HOẶC có dòng đơn giá bán=0.

## Định nghĩa `isClean`
Mọi dòng hàng hoá là ERP · không dòng dịch vụ · `discount_method` NULL · mọi `quoted_price > 0`.

## Thay đổi chính
- **BE** `QuotationService`: nới `ensureAllPricesPositive()` (bỏ chặn giá 0); `submit()` định tuyến `isClean` → auto (`doSelfApprove`) / ngưỡng cũ; thêm `isClean()`, `submitCheck()`. Controller + route `POST /{id}/submit-check`.
- **FE** `edit.vue`: `openSubmit()` rà 0đ → highlight cam `row-zero-price` + popup `QuotationZeroPriceModal.vue` (mới) → định tuyến theo `auto_approved` (auto: toast + reload; không: mở `QuotationSubmitModal`).

## Không đụng
Logic ngưỡng phân cấp, tpApprove/bgdApprove/reject/finalize, index.vue chi tiết, permission seeder.

**Spec chi tiết:** `docs/superpowers/specs/2026-07-20-baogia-warning-zero-price-design.md`
