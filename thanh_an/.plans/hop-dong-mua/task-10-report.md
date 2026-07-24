# Task 10 — Report: Trang xem chi tiết + Duyệt / Từ chối

## STATUS: DONE

## File
- Tạo mới: `hrm-thanhan-client/pages/supply/purchase_contracts/_id/index.vue`
  (route `/supply/purchase_contracts/{id}` — trang XEM read-only)

## Nội dung đã làm
- `mounted()` → `getDetail()`: dispatch `apiGetMethod 'supply/purchase-contracts/{id}'`, gán `detail = res.data` (khớp CHÍNH XÁC cách `_id/edit.vue` load detail — cùng endpoint, cùng shape đầu vào cho form). Loading spinner khi tải; lỗi → toast + về danh sách.
- Render `<PurchaseContractForm mode="show" :initial="detail" />` (form tự nạp readonly 3 tab, tự có PageHeader riêng).
- Thanh hành động trên cùng (`text-right`):
  - **Quay lại** → `/supply/purchase_contracts`.
  - **Sửa** — `v-if="detail.is_can_edit"` → `/supply/purchase_contracts/{id}/edit`.
  - **Duyệt** (variant success) + **Từ chối** (variant danger) — chỉ hiện khi `canApprove` = `detail.is_can_approve && hasAPermission('Duyệt hợp đồng mua')`.
- Modal Từ chối (`b-modal#purchase-contract-reject`): `b-form-textarea` bind `reason_deny`, label dùng `<Required />` (không viết `*` trần). Validate rỗng trước khi gửi.
- Sau approve/reject thành công → toast + `getDetail()` reload lại detail (không rời trang).
- `hasAPermission` dùng qua global mixin (`plugins/global-mixins.js` → `CheckPermission`), không cần import.

## Action Vuex dùng cho approve/reject
- **Approve**: `apiPutMethod { url: 'supply/purchase-contracts/{id}/approve', payload: {} }` (bọc `msgBoxConfirm` xác nhận).
- **Reject**: `apiPutMethod { url: 'supply/purchase-contracts/{id}/reject-approve', payload: { reason_deny } }`.
- Cả hai NHẤT QUÁN với `PurchaseContractForm` (Form dùng `apiPutMethod`/`apiPostMethod` {url,payload}). Đã kiểm `store/actions.js`: `apiPutMethod`, `apiGetMethod` tồn tại.

## Ghi chú lựa chọn kỹ thuật
- GET detail dùng `apiGetMethod` (trả body → `res.data` là object detail) thay vì `apiGet` (trả full response) — để KHỚP TUYỆT ĐỐI với `_id/edit.vue`, đảm bảo `initial` truyền vào Form đúng shape mà `applyInitial` mong đợi. Brief gợi ý tên `apiGet` nhưng edit.vue (sibling, cùng endpoint, đã chạy) dùng `apiGetMethod`; ưu tiên nhất quán với sibling.

## Verify
- SFC hợp lệ, import path đúng (`../components/PurchaseContractForm.vue`, `@/components/common/Required.vue`).
- `node --check` script block → parse OK.
- KHÔNG chạy nuxt build (theo ràng buộc).

## Concern
- Tên trạng thái/quyền: nút Duyệt/Từ chối phụ thuộc cờ `is_can_approve` do BE trả trong DetailResource; nếu BE chưa expose cờ này ở endpoint detail thì nút sẽ không hiện (cần xác nhận BE Task tương ứng đã set `is_can_approve`/`is_can_edit` trong detail resource, không chỉ ở list resource).
- Endpoint `reject-approve` nhận đúng key `reason_deny` (đã theo §4 contract). Nếu BE đổi tên field lý do → cần chỉnh lại.
- Chuỗi quyền `'Duyệt hợp đồng mua'` hard-code trong page; nếu muốn tập trung có thể thêm hằng `PERM_APPROVE` vào `constants.js` (chưa làm để tránh sửa file dùng chung khi chưa cần).
