# Task 6 — Report: Trang danh sách Hợp đồng mua (FE)

## STATUS: DONE

## File tạo
- `hrm-thanhan-client/pages/supply/purchase_contracts/index.vue`
- `hrm-thanhan-client/pages/supply/purchase_contracts/constants.js`

## Cách kiểm quyền nút "Thêm mới"
- Dùng global mixin của dự án: `this.hasAPermission(name)` (định nghĩa tại `hrm-thanhan-client/utils/mixins/CheckPermission.js`, đọc từ `$store.state.permissions`). Mixin được đăng ký toàn cục nên gọi trực tiếp trên `this`, không cần import.
- Trong `mounted()`: `this.hasPermissionCreate = this.hasAPermission('Lập hợp đồng mua')` → binding `v-if="hasPermissionCreate"` trên nút Thêm mới.
- Tên quyền lưu trong `constants.js` (`PERM_CREATE = 'Lập hợp đồng mua'`).
- Trang tham chiếu chuẩn: `pages/contract/contract/index.vue` (dòng 13 `v-if="hasPermission"`, dòng 657 `this.hasPermission = this.hasAPermission('Lập hợp đồng')`) và `pages/category/customer/index.vue` (dòng 535). Đây là pattern phổ biến toàn dự án (grep `hasAPermission` ra nhiều trang list).

## Bám sát brief
- Badge trạng thái: dùng `<b-badge :variant="item.status_color">{{ item.status_name }}</b-badge>` (KHÔNG dùng backgroundColor như mẫu, vì BE trả variant Bootstrap).
- Bộ lọc key khớp BE getList: `number`, `name`, `type`, `status`, `sign_time_from`, `sign_time_to` + `page`, `per_page`.
- Cột `total_amount` format tiền VN qua `formatCurrency(v) => Number(v||0).toLocaleString('vi-VN')`, render bằng slot.
- Actions: Xem (luôn có) → `/{id}`; Sửa `is_can_edit` → `/{id}/edit`; Duyệt `is_can_approve` → `/{id}`; Xóa `is_can_delete` → modal `modal-delete-selected`.
- API: `apiGet 'supply/purchase-contracts' + buildQueryString(params)`, đọc `response.data.data` + `response.data.meta.total`; `apiDelete 'supply/purchase-contracts/{id}'`.
- Sort mặc định `created_at` desc; watch page/per_page/sortBy/sortDesc; `mounted` gọi getData. Style `.paging` copy từ mẫu.
- base-select2 option dùng format `{ id, text }` — đúng như mẫu supply_handlings.

## Concern
- Nút Duyệt: mẫu supply_handlings dùng cờ `item.can_approve`, nhưng brief yêu cầu `item.is_can_approve` → đã dùng `is_can_approve` theo brief. Cần chắc BE trả đúng field này trong resource danh sách.
- Chưa có route `add` / `{id}` / `{id}/edit` (các task khác) — điều hướng sẽ 404 cho tới khi các trang đó được tạo. Đây là điều đã dự kiến theo scope task.
- Không chạy được `npx eslint` (không có binary trong node_modules); đã kiểm tay: import đường dẫn tương đối đúng, SFC cân bằng, biến khớp.
