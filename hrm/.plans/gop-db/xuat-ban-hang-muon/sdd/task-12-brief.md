# Task 12 — Brief: FE màn CHI TIẾT + IN + duyệt/từ chối + lịch sử (PYCXBHM)

> Requirements của bạn — dùng đúng giá trị verbatim. Stack: **Nuxt 2.14 / Vue 2 / Bootstrap-Vue 2.15 / Vuex 3**. KHÔNG service layer — gọi API qua `api.js`. Repo: `hrm-client`, nhánh `gop_db`. Làm trong `hrm-client/pages/finance/borrow-sell-requests/`.

## 0. Mục tiêu
Màn xem 1 phiếu YC xuất bán hàng mượn: hiển thị đầu phiếu + danh sách SP (+ tabs nếu Firm) + các nút hành động theo cờ quyền BE trả về (Từ chối / TP duyệt / Chuyển BGD / BGD duyệt / In / Lịch sử). Có trang IN riêng (layout print) và modal Lịch sử.

## 1. Files
- **Create** `pages/finance/borrow-sell-requests/_id/index.vue` — trang chi tiết.
- **Create** `pages/finance/borrow-sell-requests/_id/print.vue` — trang in (layout `print`).
- **Create** `pages/finance/borrow-sell-requests/components/BorrowSellRequestHistoryModal.vue` — modal lịch sử.
- **Modify** `pages/finance/borrow-sell-requests/api.js` — THÊM 1 helper `histories` (xem §3.6). KHÔNG sửa/di chuyển các helper khác.

## 2. Khuôn mẫu để COPY/ADAPT (đọc trước — cùng luồng duyệt Từ chối/TP/BGD)
- `pages/finance/product-import-requests/_id/index.vue` (1100 dòng) — **khuôn trang chi tiết** cùng bộ nút Từ chối / duyệt cấp / chuyển BGD / BGD duyệt + modal comment khi Từ chối. Bê cấu trúc layout, cách gọi API duyệt, toast, reload sau hành động.
- `pages/finance/product-import-requests/_id/print.vue` (260 dòng) — **khuôn trang in** (layout `print`, bảng SP, nút "In" gọi `window.print()`).
- `pages/finance/product-import-requests/components/ProductImportRequestHistoryModal.vue` (70 dòng) — **khuôn modal lịch sử** (b-modal + bảng, có empty-state).

> LƯU Ý khác biệt module: borrow-sell dùng `api.js` riêng (import `{ ... } from '../api'` / `'../../api'` tùy độ sâu). product-import-requests KHÔNG có api.js (gọi store trực tiếp) — **CHỈ tham khảo cấu trúc UI/luồng, KHÔNG bê cách gọi API**. Gọi API theo §3 dưới.

## 3. API CONTRACT (đã verify từ BE — dùng chính xác). Tất cả qua helper trong `api.js`.
Helpers ĐÃ CÓ SẴN: `show(dispatch, id)`, `deny(dispatch, id, comment)`, `managerApprove(dispatch, id)`, `switchBoardOfManager(dispatch, id)`, `boardOfManagerApprove(dispatch, id)`, `printData(dispatch, id)`.

### 3.1 `show(dispatch, id)` → `GET .../{id}` → trả object chi tiết (BorrowSellRequestDetailResource):
```
{ id, code, type(1|2), type_name, status, status_name, note, comment,
  contractable_id, contractable_type, contract_code, firm_contract_tab_id, vat_percent,
  customer_id, customer_name, customer_address, customer_mobile,
  customer_contact_name, customer_contact_phone, contact_address, delivery_place,
  created_by, creator_name, created_at, approved_time,
  products:[{ id, product_id, code, product_name, unit_id, unit_name, brand_name, model_name,
              contract_qty, qty, approved_qty, unit_coefficient, vat_percent,
              details:[{ id, product_export_request_id, product_export_request_detail_id, product_id, unit_id, qty, approved_qty }] }],
  tabs:[{ id, firm_contract_id, firm_contract_tab_id, name }],
  // CỜ QUYỀN — dùng để enable/disable nút (KHÔNG hard-code true):
  is_can_view, is_can_edit, is_can_approve, is_can_deny, is_can_manager_approve, is_can_board_approve }
```
- `status`: 1=Đã duyệt, 2=Chờ duyệt, 3=Đang tạo, 4=Không duyệt, 10=Chờ TP duyệt, 11=Chờ BGD duyệt. `status_name` BE trả sẵn — hiển thị trực tiếp.
- `tabs` rỗng với HĐ dịch vụ (chỉ Firm có). `comment` = lý do từ chối (hiện khi status=4).

### 3.2 Nút → API (map chính xác):
| Nút | Cờ enable | Helper | Payload |
|---|---|---|---|
| Từ chối | `is_can_deny` | `deny(dispatch, id, comment)` | mở modal nhập `comment` (bắt buộc), rồi gọi |
| TP duyệt | `is_can_manager_approve` | `managerApprove(dispatch, id)` | {} |
| Chuyển BGD | `is_can_manager_approve` | `switchBoardOfManager(dispatch, id)` | {} |
| BGD duyệt | `is_can_board_approve` | `boardOfManagerApprove(dispatch, id)` | {} |
| In | `is_can_view` | điều hướng trang in `/finance/borrow-sell-requests/{id}/print` | — |
| Lịch sử | `is_can_view` | mở modal, gọi `histories` (§3.6) | — |

- Nút hiển thị nhưng **disable** khi cờ = false (quy ước dự án: disable, KHÔNG ẩn). Cờ khởi tạo từ response, KHÔNG hard-code `= true`.
- Mỗi API duyệt/từ chối trả `{ message }` (200). Sau khi gọi thành công → toast message BE + **reload** chi tiết (gọi lại `show`) để cập nhật status + cờ nút.
- BE có thể trả **403** ("Không đủ quyền!") hoặc **422** (ValidationException) → hiện toast lỗi từ `error.response.data.message`, KHÔNG đổi state.

### 3.3 `printData(dispatch, id)` → `GET .../{id}/print-data` (BorrowSellRequestPrintResource) → trả **DỮ LIỆU CÓ CẤU TRÚC** (KHÔNG phải HTML — render bằng template Vue, KHÔNG `v-html`):
```
{ code, type_name, contract_code, note, created_at, creator_name,
  customer_name, customer_address, customer_mobile, customer_contact_name, customer_contact_phone,
  contact_address, delivery_place,
  products:[{ stt, code, product_name, model_name, unit_name, qty }] }
```

### 3.6 THÊM vào `api.js` (chưa có):
```js
export const histories = (dispatch, id) =>
  dispatch('apiGetMethod', `${BASE}/${id}/histories`)
```
→ `GET .../{id}/histories`. **Phase 1 BE trả `[]` (stub — chưa có dữ liệu lịch sử).** Modal PHẢI render empty-state gọn khi rỗng. KHÔNG cố dựng dữ liệu lịch sử giả. (Ruling R-T12-1: giữ modal + wiring để Phase 2 fill `histories()`, hiển thị "Chưa có lịch sử" khi rỗng.)

## 4. `_id/index.vue` — yêu cầu
- Load bằng `show(dispatch, this.$route.params.id)` trong `asyncData`/`fetch`/`mounted` (theo khuôn import-requests).
- Đầu phiếu: mã phiếu (`code`), trạng thái (`status_name` — badge màu theo status), loại (`type_name`), mã HĐ (`contract_code`), người tạo (`creator_name`), ngày tạo, ghi chú (`note`). Khối khách hàng: customer_name/address/mobile/contact_*/delivery_place. Nếu status=4 hiện `comment` (lý do từ chối).
- Bảng SP: STT, mã (`code`), tên (`product_name`), model, ĐVT (`unit_name`), SL yêu cầu (`qty`), SL duyệt (`approved_qty`), VAT%. (Với Firm có thể nhóm/hiện theo `tabs[].name` — tùy chọn, không bắt buộc.)
- Thanh nút theo §3.2. Modal Từ chối: 1 textarea `comment` bắt buộc (không rỗng) → gọi `deny`.
- Sau mọi hành động thành công: toast + reload `show`.

## 5. `_id/print.vue` — yêu cầu
- `layout: 'print'` (giống import-requests print.vue). Load `printData`. Render bảng SP + đầu phiếu + khối khách hàng bằng template thường (KHÔNG v-html). Nút "In" gọi `window.print()`. Không có nút duyệt.

## 6. `BorrowSellRequestHistoryModal.vue` — yêu cầu
- b-modal + bảng lịch sử. Nhận `id` (prop hoặc method `open(id)`), gọi `histories(dispatch, id)`. Render rows; nếu mảng rỗng → empty-state "Chưa có lịch sử thay đổi". Theo khuôn ProductImportRequestHistoryModal.vue.

## 7. Ràng buộc dự án (bắt buộc)
- Cờ quyền **fail-closed**: khởi tạo `false`, chỉ set từ response `is_can_*`. TUYỆT ĐỐI không `= true`.
- Select lồng trong modal (nếu có) → `V2BaseSelectInModal`. (Màn này hầu như không có select — modal Từ chối chỉ có textarea.)
- UI text + comment tiếng Việt. Nút bấm theo `.claude/skills/button-convention/SKILL.md`; modal theo `.claude/skills/modal-popup/SKILL.md`.
- KHÔNG cần `unsavedChangesMixin` (đây là màn xem, không phải form nhập).

## 8. Verify (ghi vào report)
- `npx eslint` (hoặc lint dự án) trên 3 file mới + api.js → 0 error.
- Rà tay: (a) mở chi tiết 1 phiếu mỗi status → nút enable/disable đúng theo cờ; (b) Từ chối mở modal comment, gọi đúng endpoint; (c) TP/BGD duyệt gọi đúng helper, reload sau đó; (d) trang in render đủ dữ liệu snapshot khách hàng + bảng SP; (e) modal Lịch sử hiện empty-state khi `[]`; (f) không có cờ quyền hard-code `=true`; (g) `histories` helper thêm đúng vào api.js.

## 9. Report + process
- Ghi report đầy đủ vào `/Users/nguyentrancu/DEV/code/ERP-HRM/HRM/.plans/gop-db/xuat-ban-hang-muon/sdd/task-12-report.md` (status, file list, verify, rulings/assumptions, concerns).
- **KHÔNG commit/push git. KHÔNG dispatch subagent nào. KHÔNG đọc `vendor/`, `node_modules/`.**
