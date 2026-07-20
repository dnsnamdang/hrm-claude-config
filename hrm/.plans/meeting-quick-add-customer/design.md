# Tạo nhanh khách hàng trên Form Meeting — Tóm tắt

- **Người phụ trách**: @khoipv
- **Ngày**: 2026-07-17
- **Spec đầy đủ**: `docs/superpowers/specs/2026-07-17-meeting-quick-add-customer-design.md`

## Mục tiêu
Thêm nút "+ Thêm nhanh khách hàng" trên form Tạo mới / Cập nhật Meeting (Lịch meeting),
tạo nhanh KH ngay trong luồng lập meeting rồi tự động chọn KH vừa tạo vào form.
Pattern giống hệt màn "Tạo dự án tiền khả thi".

## Phạm vi
- **CHỈ Frontend** (`hrm-client`). Không migration, không permission mới, không đụng backend.
- Sửa 1 file: `pages/assign/meeting/components/GeneralInfo.vue`.
- Tái dùng `components/modals/QuickAddCustomerModal.vue` (nhúng `CustomerForm modal-mode`) +
  API `POST assign/customers` sẵn có.

## Quyết định lớn (đã chốt)
1. Gate nút theo **quyền tạo KH** (`assign/customers/my-permissions` → `data.create`) —
   nút hiện khi `!isShow && hasCustomer && canCreateCustomer`.
2. Tái dùng `QuickAddCustomerModal` sẵn có (form KH đầy đủ), không tạo form rút gọn.
3. Auto-select bằng chính `handleCustomerEvent` của Meeting (re-fetch KH theo `code`),
   không copy logic đổ field của tiền khả thi.

## AC → giải pháp
- AC1/AC2: `v-if` dựa `hasCustomer` (computed sẵn theo `meeting_type.has_customer`).
- AC3: modal nhúng `CustomerForm modal-mode`, nút Đóng chỉ `hide()`.
- AC4: `submitSave` POST → `created` → `handleCustomerCreated` → `handleCustomerEvent` đổ field.
- AC5: `GeneralInfo.vue` dùng chung create/edit/show; `isShow` chặn nút ở màn Xem.

## Rủi ro cần verify
- KH vừa tạo (POST assign/customers) phải xuất hiện khi query theo `code` (cùng nguồn picker).
- Ownership KH cá nhân B2C: KH tự tạo thuộc quyền (TH1) → phải hiện khi query theo code.
