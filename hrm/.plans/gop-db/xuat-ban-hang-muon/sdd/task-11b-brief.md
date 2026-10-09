# Task 11b — Brief: FE màn TẠO phiếu Yêu cầu xuất bán hàng mượn (PYCXBHM)

> Đây là **requirements** của bạn — dùng đúng giá trị verbatim ở đây. Stack: **Nuxt 2.14 / Vue 2 / Bootstrap-Vue 2.15 / Vuex 3**. KHÔNG service layer — gọi API qua `api.js` (đã có sẵn). Repo: `hrm-client`, nhánh `gop_db`. Làm việc trong `hrm-client/pages/finance/borrow-sell-requests/`.

## 0. Mục tiêu
Màn tạo phiếu YC xuất bán hàng mượn cho **2 loại HĐ**: HĐ hãng (Firm) và HĐ dịch vụ (WrService). Người dùng:
1. Chọn 1 hợp đồng (Firm hoặc WrService) → set `contractable_type` + `contractable_id`.
2. Chọn 1+ phiếu **xuất mượn** nguồn (list phẳng của chính mình) → mỗi phiếu cho biết SL khả dụng để bán theo từng SP.
3. Nhập SL bán cho từng (SP × phiếu nguồn), bị chặn bởi SL khả dụng.
4. Lưu → gọi `store`, điều hướng về chi tiết phiếu vừa tạo.

KHÔNG hạch toán, KHÔNG tồn kho (Phase 1 chỉ là chứng từ yêu cầu).

## 1. Files
- **Create** `pages/finance/borrow-sell-requests/create.vue` — page wrapper (route `/finance/borrow-sell-requests/create`; `index.vue` nút "Tạo phiếu" đã trỏ tới đây).
- **Create** `pages/finance/borrow-sell-requests/components/ContractPickerModal.vue` — modal chọn hợp đồng.
- **Create** `pages/finance/borrow-sell-requests/components/ExportRequestPickerModal.vue` — modal chọn phiếu xuất mượn nguồn (multi-select).
- **Create** `pages/finance/borrow-sell-requests/components/BorrowSellRequestForm.vue` — form chính: grid SP + nhập SL + build payload + submit.
- **KHÔNG sửa** `api.js` — 5 hàm cần dùng ĐÃ CÓ SẴN: `getContracts`, `getBorrowSellData`, `getExportRequests`, `getExportRequestData`, `store` (+ import `{ ... } from '../api'`).

## 2. Khuôn mẫu để COPY/ADAPT (đọc trước khi code — đừng phát minh lại)
- `pages/finance/product-export-requests/create.vue` (64 dòng) — khuôn page wrapper mỏng.
- `pages/finance/product-export-requests/components/ContractSearchModal.vue` (143 dòng) — **khuôn picker modal** (b-modal riêng, search + bảng + click chọn dòng, emit `@select`). ContractPickerModal + ExportRequestPickerModal đều theo khuôn này.
- `pages/finance/bill-incomes/components/BillIncomeForm.vue` (1308 dòng) — **khuôn form conventions**: `unsavedChangesMixin` + `markFormSaved()`, `formValidateMixin`, `V2Footer`, vee-validate realtime, map lỗi 422 vào `formError`, cờ quyền fail-closed.
- `pages/finance/product-export-requests/components/ProductExportRequestForm.vue` (1855 dòng) — khuôn **grid SP** (cấu trúc bảng nhập SL, cột, format số). Lấy ý tưởng bảng, đừng bê nguyên (nghiệp vụ khác).

## 3. API CONTRACT (đã verify từ code BE — dùng chính xác)
Tất cả gọi qua `dispatch` (Vuex) đã bọc trong `api.js`; base `/api/v1/` tự thêm.

### 3.1 `getContracts(dispatch, { type?, keyword? })` → `GET .../contracts`
- `type`: `1`=Firm, `2`=WrService, rỗng=cả 2. `keyword`: lọc code/customer_name.
- Trả `data` = **mảng phẳng**: `[{ id, code, customer_id, customer_name, contractable_type, type(1|2), type_name }]`.
- `contractable_type` là **class-string** BE trả sẵn — GIỮ NGUYÊN, đưa thẳng vào payload (đừng tự map).

### 3.2 `getBorrowSellData(dispatch, contractId, { contractable_type, vat_percent? })` → `GET .../contracts/{id}/borrow-sell-data`
- `contractable_type` = giá trị class-string ở 3.1. KHÔNG truyền `tab_ids` (BE tự nạp tất cả tab của HĐ).
- **Firm** trả: `{ tabs:[{ id, name, firm_contract_id }], products:[{ parent_id(=tab id), firm_contract_id, product_id, product_name, model_name, brand_id, unit_id, unit_name, unit_coefficient, code, avatar, price, allocated_price, price_with_extra, extra_price, vat_percent, qty(=SL còn bán được theo HĐ), contract_qty }], support_accounting:null }`.
- **WrService** trả: `{ products:[{ id, wr_service_contract_id, product_name, product_id, quantity, unit_id, exported_qty, price, extra_cost, allocated_price, annex_qty, type, vat_percent, extra_price, rebate_price, wr_service_contract_item_id, unit_coefficient, contract_qty }], sum_cost:0 }` (KHÔNG có `tabs`).
- Đây là **danh mục SP thuộc HĐ** + **giá chuẩn của HĐ** (dùng cho payload prices) + (Firm) nguồn `firm_tab_ids`.

### 3.3 `getExportRequests(dispatch, { keyword? })` → `GET .../export-requests`
- List **phẳng** phiếu xuất mượn của chính user (BE tự lọc self+type+status+borrow_status). KHÔNG theo hợp đồng.
- Trả mảng: `[{ id, code, created_at }]`. Dùng cho ExportRequestPickerModal.

### 3.4 `getExportRequestData(dispatch, exportRequestId)` → `GET .../export-requests/{id}`
- Trả `{ id, code, products:[{ id, product_export_request_detail_id, parent_id, product_id, product_name, code, model_name, brand_name, unit_name, unit_id, unit_coefficient, detail_type, base_exported_qty, borrow_returned_qty, vat_percent, price, allocated_price, extra_price, rebate_price, product_export_request_id, available }] }`.
- **`available`** = SL bán được tối đa của (phiếu nguồn × SP) — dùng làm cận trên ô nhập SL.
- Nếu phiếu không hợp lệ → BE trả **422** key `product_export_request_id`.

### 3.5 `store(dispatch, payload)` → `POST .../` (xem §5 payload). Trả `{ id, code, status }` khi 200.

## 4. LẮP GRID (thuật toán trung tâm)
Grid lái bởi **giao (SP của HĐ) × (phiếu nguồn đã chọn)**:
1. Chọn HĐ → `getBorrowSellData` → `contractProducts[]` (danh mục SP + giá HĐ). Với Firm, lưu `firmTabIds = distinct(contractProducts.parent_id)` (hoặc `tabs[].id`).
2. Mỗi lần chọn thêm phiếu nguồn (id) → `getExportRequestData(id)` → `breakdown.products[]`. Lưu theo `exportRequestId`.
3. Với mỗi `breakdown row` (mang `product_id`, `unit_id`, `available`, `product_export_request_id`): tìm SP tương ứng trong `contractProducts` **khớp theo `product_id` (+ `unit_id`)**.
   - **Khớp được** → tạo 1 dòng grid: hiển thị tên SP/mã/ĐVT (từ contractProduct), cột **"SL khả dụng" = `available`**, ô nhập **SL bán** (mặc định 0), giá lấy từ **contractProduct** (Firm: `price/extra_price/allocated_price/vat_percent`, `price_with_extra`; WrService: `price/extra_price/allocated_price/rebate_price/vat_percent`).
   - **Không khớp** (SP của phiếu nguồn không thuộc HĐ) → BỎ QUA dòng đó (khớp hành vi store: BE sẽ throw nếu gửi SP lạ).
4. Cùng 1 SP xuất hiện ở nhiều phiếu nguồn → nhiều dòng grid (mỗi dòng 1 phiếu nguồn), nhóm hiển thị theo SP là tùy chọn (đẹp hơn nhưng không bắt buộc).
5. Chặn nhập: `SL bán` phải `>= 0` và `<= available`. Với `unit_coefficient != 1` dùng `Math.floor(available)` làm cận (khớp `Calculator::isQtyExceeded` ở BE). Ô vượt cận → viền đỏ + không cho submit.

## 5. PAYLOAD `store` (đã verify từ `store()`+`syncProducts()` — gửi ĐÚNG shape này)
```js
{
  type: Number,                       // 1 | 2 (loại phiếu — mặc định 1; nếu spec màn không phân biệt, để 1)
  contractable_type: String,          // class-string từ getContracts (verbatim)
  contractable_id: Number,            // id HĐ đã chọn
  note: String | null,                // ghi chú (nullable, max 255)
  product_export_request_ids: [Number], // TẤT CẢ id phiếu nguồn đã chọn (>=1)
  products: [                         // gom theo SP-của-HĐ (mỗi SP 1 phần tử)
    // Firm: key theo product_id + unit_id
    { product_id, unit_id,
      price, extra_price, allocated_price, rebate_price, net_price, vat_percent, // giá từ contractProduct (Firm)
      details: [ { product_export_request_id, qty } ]   // 1 phần tử / phiếu nguồn có nhập qty>0 cho SP này
    },
    // WrService: THÊM wr_service_contract_item_id
    { wr_service_contract_item_id, product_id, unit_id, price, extra_price, allocated_price, rebate_price, net_price, vat_percent,
      details: [ { product_export_request_id, qty } ] }
  ],
  firm_tab_ids: [Number],             // CHỈ Firm — = firmTabIds (§4.1). BẮT BUỘC cho Firm (rỗng→BE throw). WrService: bỏ hẳn key này.
}
```
**QUY TẮC QUAN TRỌNG:**
- `details[].qty` chỉ gộp các phiếu nguồn có `qty > 0`. Một `products[]` phải có ≥1 detail qty>0, nếu không thì đừng đưa SP đó vào payload.
- **KHÔNG gửi `tabs[]`** (syncTabs là optional; Phase 1 bỏ qua — Ruling R-T11b-3). **KHÔNG gửi `product_export_request_detail_id`** (BE tự query). **KHÔNG gửi `support_accounting_*`**.
- Firm KHÔNG gửi `wr_service_contract_item_id`; WrService KHÔNG gửi `firm_tab_ids`.
- Các trường tổng (`vat_percent`, `sum_amount_*`) là nullable ở BE — có thể tính rồi gửi, hoặc bỏ qua (Phase 1 không bắt buộc). Nếu bỏ, đừng gửi key.

## 6. VALIDATE + XỬ LÝ RESPONSE
- **Vee-validate realtime** (màn mới, theo `.claude/skills/form-validate/SKILL.md`): chỉ trường bắt buộc FE tối thiểu là **đã chọn HĐ** + **đã chọn ≥1 phiếu nguồn** + **≥1 dòng SL bán > 0**. Nút Lưu disable tới khi đủ.
- **Thành công (200)**: `store` trả `{ id, code, status }`. Gọi `markFormSaved()` (mixin), toast "Tạo phiếu thành công" (hoặc message BE), **điều hướng** `this.$router.push('/finance/borrow-sell-requests/' + id)` (màn chi tiết T12 — có thể chưa tồn tại, cứ push).
  - `status` chỉ để hiển thị (ví dụ `10`=chờ TP duyệt do vượt hạn mức, `2`=chờ kế toán kho). **KHÔNG** có bước confirm/resubmit — BE tự set status, FE chỉ đọc.
- **Lỗi 422**: map `error.response.data.errors` vào `formError` (khuôn BillIncomeForm). 2 case đặc biệt (đọc từ `errors`):
  - `errors.change_price`: là **chuỗi JSON** mảng `[{product_id, unit_id}]` (SP sai giá, chỉ xảy ra với HĐ hãng loại "đơn hàng nguyên tắc"). Parse → **highlight** các dòng grid khớp `product_id+unit_id` (viền đỏ) + hiện `errors.products?.[0]` làm message. **Đây là chặn cứng — KHÔNG confirm/resubmit.** LƯU Ý: đây là kiểm tra **dữ liệu HĐ ở server** (giá lưu trên HĐ lệch giá catalog hiện tại) — KHÔNG phụ thuộc giá FE gửi lên; FE KHÔNG thể "gửi giá đúng" để tránh lỗi, chỉ hiển thị lỗi cho user. FE vẫn gửi `price/net_price/...` lấy từ contractProduct (loadFirm) như §5.
  - `errors.products` / `errors.contractable_id` / `errors.product_export_request_ids`: hiện message inline tương ứng.
- **Fail-closed quyền**: KHÔNG hard-code cờ quyền `= true`. Nếu màn cần cờ quyền, khởi tạo `false`, chỉ set từ `$store.state.permissions`. (Màn tạo phiếu này chủ yếu là nhập liệu — nếu không có cờ quyền riêng thì bỏ qua.)
- **Cảnh báo thoát chưa lưu**: dùng `@/utils/mixins/unsavedChangesMixin`, `markFormSaved()` sau khi lưu OK. KHÔNG tự viết `beforeRouteLeave`.
- **Modal/popup + select trong modal**: theo `.claude/skills/modal-popup/SKILL.md`. Nếu có `<select>`/dropdown **lồng trong modal** → BẮT BUỘC `V2BaseSelectInModal`. (2 picker là b-modal có bảng click-chọn, không phải dropdown — không cần V2BaseSelectInModal cho việc chọn dòng.)

## 7. Verify (ghi vào report)
- `cd hrm-client && npx eslint pages/finance/borrow-sell-requests/**/*.vue` (hoặc lệnh lint dự án) → 0 error trên file mới.
- Nếu build được: `npm run build`/`nuxt build` không lỗi ở các file này (nếu quá lâu, bỏ qua và ghi rõ).
- Rà tay theo checklist: (a) chọn Firm → grid có SP + cột SL khả dụng; (b) payload Firm có `firm_tab_ids`, WrService có `wr_service_contract_item_id`; (c) 422 change_price highlight đúng; (d) success push sang `/{id}`; (e) không hard-code cờ quyền `=true`; (f) `markFormSaved()` sau lưu.

## 8. Report
Ghi report đầy đủ vào `/Users/nguyentrancu/DEV/code/ERP-HRM/HRM/.plans/gop-db/xuat-ban-hang-muon/sdd/task-11b-report.md`. Trả về status (DONE/BLOCKED/...), danh sách file, 1 dòng verify, concerns. **KHÔNG commit.** **KHÔNG dispatch subagent nào** (không tạo reviewer/helper — review sẽ do controller làm sau report).
