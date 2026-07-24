# Task 7 — Report: Khung form + Tab Thông tin chung + add/edit (HĐ mua)

**@khoipv** · FE Nuxt2/Vue2/Bootstrap-Vue · `hrm-thanhan-client`

## STATUS: DONE

Đã tạo khung form 3 tab, Tab Thông tin chung đầy đủ (port từ demo), 2 placeholder tab, add/edit, util docSo. Cú pháp SFC cân đối (kiểm tay + balance check), docSo test runtime đúng.

## File đã tạo

| File | Vai trò |
|---|---|
| `utils/numberToWords.js` | **MỚI** — export `docSo(n)` (số → chữ VNĐ), dùng chung Task 8/9 |
| `pages/supply/purchase_contracts/constants.js` | **BỔ SUNG** — thêm `TYPE`, `PAYMENT_MODE(_OPTIONS)`, `DELIVERY_METHOD_OPTIONS`, `DELIVERY_COST_PAYER_OPTIONS`, `PAY_DON_TERMS`, `DEFAULT_CONDITION_HTML` (giữ nguyên các export cũ của Task list) |
| `pages/supply/purchase_contracts/components/PurchaseContractForm.vue` | **MỚI** — chủ state (form/progressRows/payTerms/products), 3 tab, footer, save wiring |
| `pages/supply/purchase_contracts/components/GeneralTab.vue` | **MỚI** — Tab Thông tin chung: HĐ + Bên B + Giao nhận + Điều khoản HĐ (CKEditor) + Điều khoản thanh toán (NT/TM dot/don) |
| `pages/supply/purchase_contracts/components/ProductsTab.vue` | **MỚI** — placeholder mỏng (Task 8) |
| `pages/supply/purchase_contracts/components/PrintTab.vue` | **MỚI** — placeholder mỏng (Task 9) |
| `pages/supply/purchase_contracts/add.vue` | **MỚI** — `<PurchaseContractForm mode="add" />` |
| `pages/supply/purchase_contracts/_id/edit.vue` | **MỚI** — fetch detail (`apiGetMethod`) rồi truyền `:initial` + `mode="edit"` |

`index.vue` (list, đã có sẵn) không sửa — nó điều hướng `/add`, `/:id`, `/:id/edit` đúng với file mới.

## Cơ chế truyền state Form ↔ GeneralTab: **direct object/array prop mutation** (KHÔNG dùng .sync)

- Form truyền `:form`, `:progress-rows`, `:pay-terms`, `:products`, `:total-amount` xuống dưới dạng **prop object/array**; các tab con mutate trực tiếp field/phần tử (`this.form.x = …`, `progressRows.push/splice`, `payTerms[i].enabled = …`).
- Đây là **convention thực tế của module contract** (`ConditionComponent.vue`, `GeneralComponent.vue` cùng làm y hệt: mutate `formSubmit.*` từ prop). Cùng reference nên phản ánh về Form không cần emit; reactivity Vue 2 OK cho gán field có sẵn + array mutation methods.
- Chọn cách này thay cho `.sync` (mà brief nêu ví dụ) vì `.sync` trên object header sẽ phải emit `update:form` cho từng field-edit → rườm rà, không phải cách module đang dùng. Đã ghi rõ để nhất quán.

## Editor dùng cho `condition`

- **CKEditor** qua plugin `$loadCKEditor` (Vue.prototype, `plugins/ckeditor.js`), pattern lấy từ `pages/contract/contract/components/ConditionComponent.vue`.
- GeneralTab: `<textarea ref="conditionEditor" data-height="320">` + `mounted() { this.$loadCKEditor(...).then(editor => { on 'change' → form.condition = getData(); on 'instanceReady' → setData(form.condition); readonly → setReadOnly(true) }) }` + `watch form.condition → setData` + `beforeDestroy → editor.destroy()`.
- Seed mặc định: Form gán `form.condition = DEFAULT_CONDITION_HTML` khi `mode==='add'` và condition rỗng (chuỗi port từ demo `SEED.dieuKhoanHTML`).

## Util docSo (Task 8/9 tái dùng)

- Path: `D:\laragon\www\dns\hrm-thanhan-client\utils\numberToWords.js` → `export function docSo(n)` (và default export).
- Import: `import { docSo } from '@/utils/numberToWords'`. Form dùng cho `totalWords`.
- Test runtime OK: `85.950.000 → "Tám mươi lăm triệu chín trăm năm mươi nghìn đồng./."`, `1.000.000.000 → "Một tỷ đồng./."`, `0 → "Không đồng"`.

## Bám contract (fe-form-contract.md)

- **State §2**: form đầy đủ 40+ field header đúng key; `progressRows=[{label,pct,time}]`, `payTerms` 4 dòng `{term_code,enabled,max_days,max_value,max_orders}`, `products:[]`.
- **API §4**: reads dùng `apiGet` (trả axios response → `res.data.data`), writes dùng `apiPostMethod`/`apiPutMethod` (`{url,payload}`) — vì `apiPost/apiPut` positional không truyền được cả url+params qua Vuex dispatch. Detail edit dùng `apiGetMethod` (→ `res.data`). Endpoint `companies`/`suppliers`/`next-code`/`supply/purchase-contracts`.
- **Payload §6**: `{...form, status, products.map(+sort_order), payment_terms (chỉ TM+don), progress (chỉ TM+dot, map label/pct/time/sort_order)}`. total_amount không gửi.
- **Validate §7**: bắt buộc `main_company_id, supplier_id, number, name, products.length>=1` → toast liệt kê thiếu.
- **Nạp edit §8**: `applyInitial()` merge header cùng key, products pass-through, payTerms merge theo term_code (đủ 4 dòng), progressRows từ detail.progress (rỗng → 1 dòng trống).
- Tiền: `toLocaleString('vi-VN')` hiển thị, lưu số thô (`parseMoney` strip `\D`).
- Label bắt buộc: **toàn bộ dùng `<Required />`** (import `@/components/common/Required.vue`), không có `*` trần.
- Base component: base-select2 / base-date-picker / b-form-input / b-form-textarea / b-form-checkbox / b-tabs — không HTML thuần.

## Concern / lưu ý cho Task 8-10

1. **Shape API companies/suppliers**: code đọc `res.data.data || res.data` và map field `{code,name,address,tax,phone,bank_no,bank_name,bank_branch,representative,title,auth_doc}` (snake_case theo §4). Nếu BE trả camelCase/`text` khác → chỉnh `onSelectCompany/onSelectSupplier` + `companyOptions`.
2. **Cơ chế products**: ProductsTab (Task 8) nhận `:products` prop và phải **mutate in-place** (push/splice) — không gán `this.products = [...]` (mất reactivity 2 chiều vì không .sync). Nếu Task 8 cần replace mảng → đổi sang `.sync` + emit, đồng bộ luôn Form.
3. **`base-date-picker` valueType = `YYYY-MM-DD`**: `sign_time/end_time/progress.time` lưu chuỗi `YYYY-MM-DD`. `computeDuration` parse `new Date(str)` OK. Cần khớp format BE trả về khi edit.
4. **CKEditor async**: editor load bất đồng bộ; đã cover seed/edit qua cả `instanceReady.setData` lẫn `watch form.condition`. Ở mode show set `setReadOnly(true)`.
5. **type từ base-select2** có thể là string; mọi so sánh dùng `Number(form.type)`. `onTypeChange` ép `Number` + tự set `payment_mode` (`dot` khi TM, `null` khi NT).
6. Chưa chạy `nuxt build` (ràng buộc). Chưa có eslint binary trong node_modules → đã kiểm cân đối tag/brace/paren bằng script + node --check cho 2 file JS thuần; SFC review tay.
7. Nút "Duyệt/Từ chối" ở mode show **chưa** thêm (brief Task 7 chỉ footer add/edit). Màn chi tiết `_id/index.vue` (Task 10) sẽ xử lý approve/reject theo §4.
