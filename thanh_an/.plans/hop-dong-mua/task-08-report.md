# Task 8 — Report: Tab Hàng hóa + Popup chọn hàng

## STATUS: DONE

Đã điền nội dung `ProductsTab.vue` (thay placeholder) và tạo mới `GoodsPickerModal.vue`. Cả 2 file pass:
- `node --check` script block → SYNTAX OK
- `vue-template-compiler.compile` template → TEMPLATE OK (không lỗi)

Chưa chạy `nuxt build` (theo ràng buộc).

## File

- Thay nội dung: `hrm-thanhan-client/pages/supply/purchase_contracts/components/ProductsTab.vue`
- Tạo mới: `hrm-thanhan-client/pages/supply/purchase_contracts/components/GoodsPickerModal.vue`

## Cách emit / merge (modal ↔ ProductsTab)

Kiến trúc: **modal build line thô — ProductsTab gộp theo mã** (merge-by-code giữ ở ProductsTab, đúng gợi ý brief).

1. `ProductsTab` truyền xuống modal:
   - `:visible.sync="goodsModalVisible"`
   - `:exclude-codes="excludeCodes"` — computed = danh sách `product_hh_code` + `product_code` của mọi dòng đang có.
2. Modal `@show` → `fetchPool()` gọi `apiGet 'supply/purchase-contracts/goods-pool' + buildQueryString({ exclude_codes })`, nhận `{demand, catalog}` (đọc `res.data.data || res.data`).
3. Modal map sang ứng viên (§5): mỗi ứng viên mang sẵn `_line` (line object KEY BE) + field hiển thị. `demand` → `proposed_qty=total_buy_qty`, `order_qty=Σ buyQty`, `purposes=lines.map(...)`; `catalog` → `proposed_qty=null`, `order_qty=0`, `purposes=[]`.
4. Bấm "Thêm vào hợp đồng" → `confirm()` emit **`add`** với mảng line đã clone sâu (`this.$emit('add', lines)`) rồi emit `update:visible=false`.
5. `ProductsTab.onAddLines(lines)` lặp `mergeLine(line)`:
   - key = `product_hh_code` (rỗng → `product_code`).
   - chưa có → `this.products.push(line)`.
   - đã có → cộng dồn `proposed_qty` (sumQty), ghép `purposes` (bỏ trùng theo proposal+customer, dùng `ex.purposes.push`), `order_qty = Σ buyQty` nếu có phiếu / cộng dồn trực tiếp nếu không phiếu.
   - Nhờ gộp tuần tự, 2 ứng viên **cùng mã trong 1 lần chọn** (vd 2 phiếu FT4) cũng tự gộp thành 1 dòng.

## Xác nhận MUTATE IN-PLACE

Không có chỗ nào reassign `this.products = ...`. Mọi thay đổi trên chính mảng prop:
- Thêm dòng: `this.products.push(line)`
- Xóa dòng: `this.products.splice(idx, 1)`
- Sửa field từng phần tử (order_qty/price/note/purposes/proposed_qty): gán trực tiếp key **sẵn có** của object (reactive Vue 2).
- `buyQty` (có thể thiếu ở bản ghi cũ) dùng `this.$set(pp, 'buyQty', v)`.
- Khi ghép purposes vào object thiếu key dùng `this.$set(ex, 'purposes', [])` trước khi push.
- `visibleRows` (bộ lọc) chỉ tạo view `{p, idx}` giữ **idx gốc** để mutate/splice đúng phần tử — không đụng thứ tự mảng thật.

## Pass-through mã (chống lật ngược)

`product_code` / `product_hh_code` mang y nguyên từ goods-pool, không hoán đổi. Cột "Mã hàng" hiển thị `product_hh_code`. Gộp trùng + `lineKey` theo `product_hh_code` (rỗng → `product_code`). Bộ lọc "Mã hàng" khớp `product_hh_code`, fallback `product_code`.

## Đã port từ demo (đổi key BE)

`COLUMNS/visibleCols` (qua `isTm` + v-if cột tm), `cellFor` (render cell theo template), `productRow/renderProducts`, `oqWarn/oqTip`, `propSum/buySum/orderQtyOf/amountOf/hasPurposes`, `matchFilter`, `removeRow`, `addPoolItem/poolToLine/sumQty` (→ `mergeLine`), popup `gmCandidates/gmMatch/gmPurpose/gmPill/gmRenderRows/openGoodsModal`. Cảnh báo màu (`oq-over` đỏ / `oq-under` vàng), dòng TỔNG CỘNG (chỉ TM), khối tổng + bằng chữ (`docSo` từ `@/utils/numberToWords`). CSS `.product-table/.inp-oq/.cell-purpose*/.total-row/.oq-legend` port vào `<style lang="scss" scoped>`.

## Concern / lưu ý cho task sau

1. **Shape response goods-pool:** đọc `res.data.data || res.data` rồi `.demand/.catalog`. Nếu BE trả thẳng `{data:{demand,catalog}}` hay `{demand,catalog}` đều chạy; nếu BE bọc khác (vd `res.data.result`) cần chỉnh `fetchPool`.
2. **exclude_codes format:** `buildQueryString` render mảng thành `exclude_codes=A&exclude_codes=B` (KHÔNG có `[]`). Nếu BE Laravel muốn nhận `exclude_codes[]` thì dùng `buildQuery` thay vì `buildQueryString`. Cần xác nhận BE parse kiểu nào.
3. **Field hiển thị của demand thiếu:** `producer_country` / `product_trade_name` / `specification` có thể không có trong `demand[]` (§5 chỉ liệt kê tối thiểu) → hiện rỗng. Nếu BE bổ sung thì tự map (đã đọc `row.producer_country` v.v.).
4. **Tổng giá trị hiển thị 2 nơi:** Form (footer) và ProductsTab (khối bằng chữ) — theo demo, chấp nhận trùng. Nếu muốn 1 chỗ, bỏ khối trong tab.
5. **Không có kéo-thả sắp xếp dòng** (demo chỉ có `.drag-handle` tĩnh, chưa gắn sortable) → giữ nguyên như demo; `sort_order` do Form set khi build payload.
6. Chưa test tương tác thực (cần API `goods-pool` chạy). Logic gộp/cảnh báo đã đối chiếu 1:1 với demo.
