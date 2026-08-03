# Task 8 — FE: Tab Hàng hóa + Popup chọn hàng

Implementer FE (Nuxt 2 / Vue 2 / Bootstrap-Vue) tại `D:\laragon\www\dns\hrm-thanhan-client`.

Task 7 đã tạo khung form. Task này ĐIỀN nội dung 2 component (ProductsTab đang là placeholder mỏng — thay hẳn nội dung) và tạo GoodsPickerModal.

## Đọc trước (BẮT BUỘC)

1. `D:\laragon\www\dns\.plans\hop-dong-mua\fe-form-contract.md` — đặc biệt §3 (line object + logic SL/cảnh báo/gộp), §5 (map goods-pool → line, exclude_codes), §0 (quy ước).
2. `D:\laragon\www\dns\demos\demo-lap-hop-dong-mua.html` — port: `COLUMNS`, `visibleCols`, `cellFor`, `productRow`, `renderProducts`, `renderTotals`, `oqWarn/oqTip`, `propSum/buySum/orderQtyOf/amountOf/hasPurposes`, `removeRow`, `matchFilter`, và popup: `openGoodsModal`, `gmCandidates`, `gmMatch`, `gmPurpose`, `gmPill`, `gmRenderRows`, `addPoolItem`, `poolToLine`, `sumQty`. Giữ nguyên hành vi, chỉ đổi tên field sang KEY BE (§3) và nguồn dữ liệu sang API (§5).
3. `hrm-thanhan-client/pages/supply/purchase_contracts/components/PurchaseContractForm.vue` — để biết prop truyền vào ProductsTab: `:products` (Array, mutate in-place), `:contract-type` (Number 1/2), `:readonly` (Boolean).
4. `hrm-thanhan-client/pages/supply/supply_proposals/components/GoodsPickerModal.vue` — KHUÔN kiến trúc popup chọn hàng của module (b-modal, cách gọi API, tick chọn, style). Bám sát.
5. `hrm-thanhan-client/pages/supply/purchase_contracts/components/ProductsTab.vue` (placeholder hiện tại) — thay nội dung.

## File

- Thay nội dung: `pages/supply/purchase_contracts/components/ProductsTab.vue`
- Tạo: `pages/supply/purchase_contracts/components/GoodsPickerModal.vue`

## Quy tắc CỐT LÕI

- **MUTATE IN-PLACE:** ProductsTab nhận `products` (prop array do Form sở hữu). Mọi thay đổi phải `this.products.push(...)`, `this.products.splice(...)`, hoặc gán field từng phần tử `this.$set(item, 'order_qty', v)` — TUYỆT ĐỐI KHÔNG `this.products = [...]` (reassign làm mất liên kết với Form). Với Vue 2, khi cần thêm field mới vào object item dùng `this.$set`.
- **Key line theo BE (§3), pass-through mã:** không hoán đổi `product_code`/`product_hh_code`. Cột "Mã hàng" hiển thị `product_hh_code`. Gộp trùng theo `product_hh_code` (rỗng → `product_code`).
- `<Required />` không cần ở bảng (không có label field bắt buộc kiểu form), nhưng nếu có nhãn bắt buộc thì dùng component đó.

## ProductsTab.vue — yêu cầu

- Prop: `products` (Array, required), `contractType` (Number), `readonly` (Boolean).
- Nút "Chọn hàng hóa" (mở GoodsPickerModal) + nút "Bộ lọc" (toggle khối lọc: Tên hàng, Mã hàng, checkbox "Không có phiếu đề xuất"). Ẩn nút khi readonly.
- Bảng hàng (product-table): cột động theo `contractType` (port COLUMNS/visibleCols — Nguyên tắc ẩn SL đề xuất/SL mua/Thành tiền/Ghi chú):
  - STT · Mã hàng (product_hh_code, monospace) · Tên hàng hóa (product_name + product_trade_name phụ) · Quy cách · ĐVT · Hãng nước SX · **Mục đích mua** · **SL đề xuất mua** (propSum, readonly) · **SL mua** (input, cảnh báo màu) · Đơn giá có VAT (input tiền) · Thành tiền · Ghi chú (input) · Xóa.
  - **Cột Mục đích mua:** liệt kê từng `purposes[]` (proposal / customer / saleContract nếu có + badge "ĐX {qty}"); khi Thương mại có ô "Mua" nhập `buyQty` từng phiếu → sửa buyQty thì `order_qty = Σ buyQty` + cập nhật cảnh báo; nhiều phiếu → header "Gộp N phiếu"; không phiếu → "Mua ngoài phiếu đề xuất". Nút bỏ gắn tất cả phiếu (unlink) → purposes=[], proposed_qty=null, giữ order_qty hiện tại.
  - **SL mua (order_qty):** input số; mặc định = proposed_qty; lệch → class cảnh báo: lớn hơn `oq-over` (đỏ), nhỏ hơn `oq-under` (vàng); không phiếu (proposed_qty=null) → không cảnh báo. Port CSS class từ demo (đưa vào `<style scoped>`).
  - **Đơn giá:** nhập số thô, hiển thị format VN; đổi → cập nhật Thành tiền + tổng.
  - Dòng **TỔNG CỘNG** (chỉ Thương mại) đầu bảng: Σ SL đề xuất, Σ SL mua, Σ thành tiền.
- Khối "Tổng giá trị hợp đồng (đã gồm VAT)" + "Bằng chữ" (chỉ Thương mại) — dùng `import { docSo } from '@/utils/numberToWords'`. (Form cũng hiển thị tổng; ở đây hiển thị trong tab là được, không bắt buộc trùng — theo demo có khối này trong tab hàng hóa.)
- CSS: port các class `.product-table`, `.inp-oq.oq-over/.oq-under`, `.cell-purpose*`, `.total-row`, `.oq-legend` từ `<style>` demo vào `<style lang="scss" scoped>`.
- Bộ lọc: lọc hiển thị theo tên/mã/không-phiếu (port matchFilter) — chỉ lọc VIEW, không xóa khỏi products.

## GoodsPickerModal.vue — yêu cầu

- Dùng b-modal (id ví dụ `modal-goods-picker`) hoặc overlay như supply_proposals GoodsPickerModal — theo khuôn module.
- Khi mở: gọi `apiGet 'supply/purchase-contracts/goods-pool' + buildQueryString({ exclude_codes })` với `exclude_codes` = danh sách `product_hh_code` (và product_code) đã có trong products. Nhận `{ demand:[...], catalog:[...] }`.
- Map sang candidate list (port gmCandidates + §5): mỗi ứng viên có nguồn "Theo phiếu" (demand) / "Không theo phiếu" (catalog). Hiển thị bảng: checkbox, STT, Tên hàng, Mã hàng (product_hh_code), ĐVT, Hãng nước SX, SL đề xuất mua (demand: total_buy_qty; catalog: —), Phiếu đề xuất, Khách hàng, (Công ty nếu có), Nguồn (pill "Theo phiếu đề xuất" / "Không theo phiếu"; nếu mã đã có trong HĐ → pill "Ghép vào dòng sẵn có").
- Tìm kiếm (tên/mã/hãng/phiếu/khách) + lọc nguồn (Tất cả / Theo phiếu / Không theo phiếu) — port gmMatch. Chọn tất cả (indeterminate) như demo.
- Nút "Thêm vào hợp đồng": với mỗi item đã tick → chuyển thành line object (§5) và **emit `add`** danh sách line cho ProductsTab. ProductsTab thực hiện gộp theo mã (port addPoolItem/poolToLine, mutate in-place `products`) rồi đóng modal.
  - (Có thể để logic gộp trong ProductsTab, modal chỉ emit line thô; hoặc modal build sẵn line rồi ProductsTab gộp. Chọn cách rõ ràng, giữ merge-by-code ở ProductsTab.)

## Verify
- Cú pháp SFC hợp lệ; import path đúng; eslint 2 file nếu binary có, không thì kiểm tay.
- KHÔNG chạy nuxt build.

## Report
Ghi `D:\laragon\www\dns\.plans\hop-dong-mua\task-08-report.md`. Trả về: STATUS, file, cách emit/merge (modal↔ProductsTab), xác nhận mutate in-place, và concern.
