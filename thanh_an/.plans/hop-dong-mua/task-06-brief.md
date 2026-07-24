# Task 6 — FE: Trang danh sách Hợp đồng mua (index.vue + constants.js)

Implementer FE. Nuxt 2.14 (Vue 2) + Bootstrap-Vue 2.15, tại `D:\laragon\www\dns\hrm-thanhan-client`. Tiếng Việt. KHÔNG git commit. KHÔNG đọc node_modules/.

Menu đã được thêm sẵn (mục "Hợp đồng mua" → `/supply/purchase_contracts`, quyền `Xem hợp đồng mua`). BE đã xong: `GET /supply/purchase-contracts`, `DELETE /supply/purchase-contracts/{id}`.

## File

- Tạo: `hrm-thanhan-client/pages/supply/purchase_contracts/index.vue`
- Tạo: `hrm-thanhan-client/pages/supply/purchase_contracts/constants.js`

## Đọc trước (mẫu style list module Supply — COPY sát cấu trúc)

- `hrm-thanhan-client/pages/supply/supply_handlings/index.vue` (mẫu chính: PageHeader, bộ lọc b-collapse, b-table sticky, phân trang, confirm-delete-selected, `$store.dispatch('apiGet'/'apiDelete')`, `buildQueryString`, `getNumericalOrder`).
- `hrm-thanhan-client/pages/supply/supply_handlings/constants.js` (mẫu để biết cấu trúc STATUS_OPTIONS/TYPE_OPTIONS/PAGE_OPTIONS — đọc rồi viết bản cho HĐ mua).

## constants.js — nội dung

```js
export const PAGE_OPTIONS = [10, 25, 50, 100]

// Trạng thái HĐ mua (khớp BE PurchaseContract::STATUSES)
export const STATUS = {
    DRAFT: 1,
    PENDING: 2,
    APPROVED: 3,
    REJECTED: 4,
    CANCELED: 5,
}

export const STATUS_OPTIONS = [
    { id: 1, text: 'Nháp' },
    { id: 2, text: 'Chờ duyệt' },
    { id: 3, text: 'Đã duyệt' },
    { id: 4, text: 'Từ chối' },
    { id: 5, text: 'Hủy' },
]

// Loại HĐ (khớp BE PurchaseContract::TYPES)
export const TYPE_OPTIONS = [
    { id: 1, text: 'Nguyên tắc' },
    { id: 2, text: 'Thương mại' },
]
```
(Đối chiếu format option [{id,text}] với base-select2 trong mẫu — nếu mẫu dùng key khác như {value,label} thì theo đúng mẫu.)

## index.vue — yêu cầu

Bám cấu trúc `supply_handlings/index.vue`, khác ở:

1. **Tiêu đề / breadcrumb:** title `'Hợp đồng mua'`, items `[{ text: 'Cung ứng' }, { text: 'Hợp đồng mua' }]`.

2. **Nút "Thêm mới" (khác mẫu — mẫu không có):** đặt cạnh nút Bộ lọc, chỉ hiện khi có quyền `Lập hợp đồng mua`. Dùng cách kiểm quyền GIỐNG các trang khác trong client (tìm helper/directive phân quyền đang dùng, ví dụ `$can(...)`, `checkPermission`, hoặc directive `v-permission` — đọc 1-2 trang list khác trong `pages/supply` hoặc `pages/` để biết cách chuẩn của dự án; KHÔNG bịa). Bấm → `this.$router.push('/supply/purchase_contracts/add')`.

3. **Bộ lọc (formFilter)** — key phải KHỚP tham số BE `getList`: `number` (input "Số hợp đồng"), `name` (input "Tên hợp đồng"), `type` (base-select2 TYPE_OPTIONS), `status` (base-select2 STATUS_OPTIONS), `sign_time_from` (base-date-picker "Ngày ký từ"), `sign_time_to` (base-date-picker "Ngày ký đến"). Cùng `page`, `per_page`.

4. **Cột bảng (fields):**
   - stt (STT)
   - code (Mã HĐ, sortable)
   - number (Số HĐ)
   - name (Tên HĐ, tdClass min-w-200)
   - type_name (Loại)
   - supplier_name (Nhà cung cấp, min-w-200)
   - sign_time (Ngày ký, text-center)
   - total_amount (Giá trị HĐ, text-right) — format tiền VN: viết method `formatCurrency(v)` trả `Number(v||0).toLocaleString('vi-VN')`, dùng qua slot `cell(total_amount)`.
   - status (Trạng thái, text-center)
   - created_by_name (Người tạo)
   - created_at (Ngày tạo, text-center, sortable)
   - actions (Thao tác, text-center)

5. **Badge trạng thái — KHÁC mẫu (QUAN TRỌNG):** BE trả `status_color` là **variant Bootstrap** (`secondary`/`warning`/`success`/`danger`/`dark`), KHÔNG phải mã màu CSS. Vì vậy PHẢI render bằng:
   ```html
   <template v-slot:cell(status)="{ item }">
       <b-badge :variant="item.status_color">{{ item.status_name }}</b-badge>
   </template>
   ```
   (KHÔNG dùng `:style="{ backgroundColor: item.status_color }"` như mẫu — sẽ sai vì 'warning' không phải màu.)

6. **Cột thao tác (actions)** theo cờ từ BE:
   - Luôn có nút **Xem** → `this.$router.push('/supply/purchase_contracts/' + item.id)`.
   - `v-if="item.is_can_edit"` nút **Sửa** → `this.$router.push('/supply/purchase_contracts/' + item.id + '/edit')`.
   - `v-if="item.is_can_approve"` nút **Duyệt** → điều hướng tới trang xem để duyệt: `this.$router.push('/supply/purchase_contracts/' + item.id)`.
   - `v-if="item.is_can_delete"` nút **Xóa** → mở modal confirm-delete-selected (giống mẫu: set `this.deleteId = item.id` rồi `this.$bvModal.show('modal-delete-selected')`).
   (Dùng đúng icon/asset img như mẫu: eyes.svg / pen.svg / trash.svg; nút duyệt dùng `<i class="mdi mdi-check-circle-outline">` như mẫu.)

7. **API:**
   - Lấy danh sách: `this.$store.dispatch('apiGet', 'supply/purchase-contracts' + buildQueryString(params))`; đọc `response.data.data` + `response.data.meta.total` (giống mẫu).
   - Xóa: `this.$store.dispatch('apiDelete', 'supply/purchase-contracts/' + this.deleteId)`, toast thành công/thất bại, reload `getData()`.
   - `params` gồm `...formFilter`, `sort_by: this.sortBy`, `sort_desc: this.sortDesc ? 1 : 0`.

8. **Sort mặc định:** `sortBy: 'created_at'`, `sortDesc: true`. watch page/per_page/sortBy/sortDesc → getData (giống mẫu). `mounted(){ this.getData() }`.

9. Giữ style `<style lang="scss" scoped>` phần `.paging` copy từ mẫu.

## Verify

- Bảo đảm cú pháp `.vue` hợp lệ (SFC template/script/style đóng mở đúng). Nếu chạy được `npx eslint` cho 2 file thì chạy; nếu môi trường không có, kiểm tay kỹ (import đúng đường dẫn tương đối, tên biến khớp, không thiếu dấu).
- KHÔNG chạy `nuxt build` toàn dự án (nặng). Chỉ đảm bảo file tự nhất quán.

## Report

Ghi vào `D:\laragon\www\dns\.plans\hop-dong-mua\task-06-report.md`. Trả về: STATUS, file tạo, cách kiểm quyền nút Thêm (helper/directive nào của dự án bạn đã dùng + trang tham chiếu), và concern nếu có (đặc biệt nếu format option base-select2 hay cách phân quyền khác giả định).
