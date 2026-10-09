# Task P2-12 Report — Màn TẠO phiếu xuất bán hàng mượn (create.vue + BorrowSellForm.vue)

## Status: DONE

## 2 file tạo
- `pages/finance/borrow-sells/create.vue` — trang vỏ (mirror `pages/finance/borrow-sell-requests/create.vue`, ~29 dòng). `name: 'BorrowSellCreate'`, `pageTitle()` → `'Lập phiếu xuất bán hàng mượn'`, `mixins: [PageTitleMixin, unsavedChildFormMixin]`, `layout: 'default-sidebar'`.
- `pages/finance/borrow-sells/components/BorrowSellForm.vue` — form thật.

## Tên hàm chụp mốc unsaved thực dùng
Brief đề nghị ưu tiên `captureFormSnapshot()` nhưng mixin `@/utils/mixins/unsavedChangesMixin` KHÔNG có hàm đó — hàm thật để "chốt lại mốc thủ công sau khi nạp xong dữ liệu" là **`markFormPristine()`** (đọc source mixin dòng 131-135). Đã dùng đúng tên này trong `loadRequest()`:
```js
this.$nextTick(() => this.markFormPristine())
```
Sau khi lưu thành công vẫn gọi `markFormSaved()` (đúng brief B5/B6) trước khi `$router.push`.

## totalColumns cuối
`totalColumns() { return this.hasRebatePrice ? 16 : 15 }` — đúng verbatim brief B3.

Số cột thực tế đã giữ trong bảng (leaf columns, không tính rowspan header):
1. STT
2. Tên hàng hóa (kèm sub-line Model/Mã/Thương hiệu)
3. ĐVT
4. SL HĐ (contract_qty)
5. Đã xuất kho (exported_qty)
6. Bán hàng mượn (groupBorrowSellQty, cảnh báo đỏ khi `groupBorrowSellExceedsContract`)
7. Phiếu nguồn (export_request_code)
8. Bán (ô nhập `d.qty`, kèm hiển thị cận `/ {{ max_qty }}` ngay cạnh ô — thay cho cột "Đang mượn" riêng của Phase 1, vì Phase 2 không có SL "đang mượn" mà chỉ có `max_qty = approved_qty`)
9. Giá niêm yết
10. **Chiết khấu** — chỉ khi `hasRebatePrice`
11. Đơn giá bán
12. Thành tiền
13. Đơn giá sau giảm
14. Thành tiền sau giảm
15. VAT
16. Thành tiền sau VAT

= 15 cột cơ bản, 16 khi có Chiết khấu — khớp `totalColumns()`.

**Khác biệt so với khuôn Phase 1 cần lưu ý:** Phase 1 có 3 sub-cột "Chi tiết" (Phiếu mượn / Đang mượn / Bán), Phase 2 chỉ có 2 (Phiếu nguồn / Bán) vì cận `max_qty` được hiển thị lồng ngay trong ô Bán (`/ {{ d.max_qty }}`) thay vì tách cột riêng — giảm 1 cột so với khuôn, đã tính đúng vào `totalColumns`.

## Payload xác nhận (Ruling T8-payload — verbatim)
```js
buildPayload() {
    const products = []
    this.productGroups.forEach((g) => {
        const details = g.details
            .filter((d) => (Number(d.qty) || 0) > 0)
            .map((d) => ({ product_export_request_detail_id: d.product_export_request_detail_id, qty: Number(d.qty) || 0 }))
        if (!details.length) return
        products.push({ objectable_id: g.objectable_id, objectable_type: g.objectable_type, details })
    })
    return { borrow_sell_request_id: Number(this.requestId), products }
}
```
CHỈ có `borrow_sell_request_id` + `products[].{objectable_id, objectable_type, details[].{product_export_request_detail_id, qty}}`. KHÔNG có field tiền/giá nào được gửi.

## Kết quả grep tự kiểm
```
grep -nE "ContractPicker|ExportRequestPicker|rebuildGrid|selectedExportRequests|change_price|_priceError|can[A-Za-z]*\s*=\s*true" \
  pages/finance/borrow-sells/create.vue pages/finance/borrow-sells/components/BorrowSellForm.vue
```
→ 0 matches (sạch). Đã xác nhận không còn tham chiếu ContractPickerModal, ExportRequestPickerModal, rebuildGrid, selectedExportRequests, `change_price`/`markPriceErrors`, `_priceError`, và không có pattern hard-code cờ quyền `= true`.

Đã kiểm thêm:
- Tag balance template (`div/table/thead/tbody/tr/td/th/template`) — cân bằng, không lệch.
- Tất cả component import (`V2BaseInput`, `V2BaseLabel`, `V2BaseError`, `V2BaseTableScroll`, `V2BaseButton`) và mixin (`unsavedChildFormMixin`, `unsavedChangesMixin`, `formValidateMixin`) đều tồn tại đúng path.
- `V2BaseButton` prop `tertiary` tồn tại (dòng 29 `V2BaseButton.vue`) — dùng đúng cho nút "Quay lại" theo button-convention (B7).
- Gate fail-closed `is_can_create_borrow_sell` (BE trả, KHÔNG hardcode true) trong `loadRequest()`.

## eslint
Không chạy được — project không có eslint local (Node 14.21.3, không có `node_modules/.bin/eslint`, `npx eslint` sẽ kéo bản mới không tương thích Node 14, đúng như brief đã lường trước). Đã thay bằng grep tự kiểm + kiểm tra cân bằng thẻ template bằng script Node thủ công (xem trên) thay cho lint.

## Concerns
- Không có concern chặn merge. Ghi chú nhỏ: cột "Bán hàng mượn" (groupBorrowSellQty) + cảnh báo `groupBorrowSellExceedsContract` được giữ lại trong UI dù `hasGridQtyViolation` (dùng để validate submit) KHÔNG include điều kiện này — đúng ý brief B3 (getter vẫn giữ để hiển thị cảnh báo trực quan, nhưng validate submit chỉ chặn theo `max_qty` per-detail, không chặn theo excess-of-contract ở cấp nhóm). Nếu sau này muốn chặn cứng luôn cả trường hợp vượt hợp đồng thì cần bổ sung vào `hasGridQtyViolation`/`validateBeforeSubmit` — hiện tại brief không yêu cầu nên chưa thêm.
- Chưa test thực tế qua trình duyệt (không được yêu cầu chạy `nuxt build`/dev server trong task này).
