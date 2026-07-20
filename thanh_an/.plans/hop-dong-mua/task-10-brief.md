# Task 10 — FE: Trang xem chi tiết + Duyệt / Từ chối

Implementer FE (Nuxt 2 / Vue 2 / Bootstrap-Vue) tại `D:\laragon\www\dns\hrm-thanhan-client`.

Task 6-9 xong: danh sách, form (add/edit), 3 tab. Task này tạo trang XEM read-only (tái dùng form mode=show) + hành động Duyệt / Từ chối.

## Đọc trước
1. `D:\laragon\www\dns\.plans\hop-dong-mua\fe-form-contract.md` — §4 (API: show, approve, reject-approve).
2. `pages/supply/purchase_contracts/components/PurchaseContractForm.vue` — đã hỗ trợ `mode="show"` (readonly, ẩn footer) + prop `initial`.
3. `pages/supply/purchase_contracts/_id/edit.vue` (Task 7) — cách load detail theo id để tham chiếu.
4. `pages/supply/purchase_contracts/index.vue` — cách dùng mixin `hasAPermission(...)` + modal confirm.

## File
- Tạo: `pages/supply/purchase_contracts/_id/index.vue`  (route `/supply/purchase_contracts/{id}` — trang xem)

(Không tạo trang duyệt riêng — nút Duyệt/Từ chối nằm ngay trên trang xem, đúng như list điều hướng `is_can_approve` → trang xem.)

## Yêu cầu `_id/index.vue`

- `mounted()` (hoặc asyncData): đọc `this.$route.params.id`; `apiGet 'supply/purchase-contracts/' + id` → `detail`. Loading spinner khi tải.
- Render:
  - Thanh hành động trên cùng (text-right), hiển thị theo cờ từ `detail`:
    - Nút **Sửa** (`v-if="detail.is_can_edit"`) → `$router.push('/supply/purchase_contracts/' + id + '/edit')`.
    - Nút **Duyệt** (`v-if="detail.is_can_approve && hasAPermission('Duyệt hợp đồng mua')"`, variant success) → gọi `approve()`.
    - Nút **Từ chối** (cùng điều kiện, variant danger) → mở modal nhập lý do → `reject()`.
    - Nút **Quay lại** → `$router.push('/supply/purchase_contracts')`.
  - `<PurchaseContractForm mode="show" :initial="detail" />` (form tự nạp readonly toàn bộ 3 tab).
- `approve()`: confirm → `apiPut 'supply/purchase-contracts/' + id + '/approve'` (dùng `apiPutMethod` {url, payload:{}} hoặc action phù hợp — theo cách Form đang gọi apiPutMethod). Thành công → toast + reload detail (hoặc về danh sách). 
- `reject()`: modal (b-modal) nhập `reason_deny` (textarea, bắt buộc — dùng `<Required />` cho label) → `apiPutMethod { url:'supply/purchase-contracts/'+id+'/reject-approve', payload:{ reason_deny } }`. Thành công → toast + reload detail.
- Dùng mixin `hasAPermission` như `index.vue` (global, không cần import).
- Lưu ý action name Vuex: Form dùng `apiPutMethod`/`apiPostMethod` ({url, payload}) và `apiGet`. Dùng NHẤT QUÁN các action đó (kiểm store để chắc chắn action tồn tại; nếu cần GET method thì `apiGet` như Form).

## Verify
- SFC hợp lệ; import path đúng. node --check script nếu có thể.
- KHÔNG chạy nuxt build.

## Report
Ghi `D:\laragon\www\dns\.plans\hop-dong-mua\task-10-report.md`. STATUS + file + action Vuex dùng cho approve/reject + concern.
