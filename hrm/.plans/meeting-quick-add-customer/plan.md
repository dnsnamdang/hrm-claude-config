# Plan — Tạo nhanh khách hàng trên Form Meeting

- Feature: meeting-quick-add-customer
- Phụ trách: @khoipv
- Spec: `docs/superpowers/specs/2026-07-17-meeting-quick-add-customer-design.md`
- Plan chi tiết (bite-sized): `docs/superpowers/plans/2026-07-17-meeting-quick-add-customer.md`

## Phạm vi
CHỈ FE — sửa 1 file `hrm-client/pages/assign/meeting/components/GeneralInfo.vue`.
Không BE / migration / permission / git.

## Task tổng quát

### FE — GeneralInfo.vue
- [x] Task 1: Nạp quyền tạo KH (`assign/customers/my-permissions` → `canCreateCustomer`) + copy CSS `.quick-add-btn`
- [x] Task 2: Import + đăng ký + render `QuickAddCustomerModal` (@created)
- [x] Task 3: Nút "+ Thêm nhanh khách hàng" trong label + `openQuickAddCustomer` (AC1, AC2, AC3)
- [x] Task 4: `handleCustomerCreated` auto-select KH vừa tạo qua `handleCustomerEvent` (AC4)
- [ ] Task 5: Verify E2E form Tạo/Cập nhật (AC1–AC5) + regression — CẦN dev server FE (tạo KH thật, cần user)

## Ghi chú ngoài phạm vi (không sửa trong task này)
- Bug pre-existing: `GeneralInfo.vue` khai báo computed `isFromProject` 2 lần (~dòng 651 & 713) — trùng key, có sẵn từ trước, nằm ngoài vùng diff. Nêu để cân nhắc sửa riêng.
- `hasCustomer` vừa là prop (default true) vừa là computed (theo loại meeting) — computed override, nút dùng đúng giá trị. Vấn đề đặt tên cũ.

### Checkpoint — 2026-07-17
Vừa hoàn thành: Task 1–4 (code trong GeneralInfo.vue), task-review SPEC ✅ + QUALITY Approved, đã áp Minor fix (thêm catch + console.error vào handleCustomerCreated).
Đang làm dở: Task 5 — E2E verify (chưa chạy, cần dev server FE 3000 + tài khoản có quyền tạo KH; sẽ tạo KH thật cần dọn).
Bước tiếp: user bật FE dev server → verify AC1–AC5 trên browser (hoặc xác nhận để tôi drive Playwright, có dọn KH test sau).
Blocked: cần môi trường FE chạy để verify.
