# Plan: Che mờ SĐT khách hàng — Meeting & Dự án TKT

@manhcuong · Module Assign · Spec: docs/superpowers/specs/2026-06-23-masking-sdt-khach-hang-design.md

## Phase 1 — Helper + Masking BE

### BE
- [x] Tạo `app/Helper/CustomerPhoneVisibility.php` (`canView`+`decide`+`apply`+`maskCustomer`+`maskMembersPhone`, cache context/request, dùng `current_company_role`/`listManage*` theo `Meeting::canView()`)
- [x] Mask `MeetingResource.php` (list): customer_contact_phone, customer_members[].phone, customer.mobile, customer.contacts[].phones
- [x] Mask `MeetingTransformer.php` (detail/edit/store/update): cùng tập field
- [x] Mask `MeetingService::getDataForShow()`: projects[].customer_contact_phone theo quyền TKT (per-project)
- [x] Mask `ProspectiveProjectResource.php` (list): customer_contact_phone
- [x] Mask `DetailProspectiveProjectResource.php`: customer_phone, customer_contact_phone, meetings[].customer_contact_phone, customer.contacts[].phones
- [x] Mask blade `exports/meetings.blade.php` (gọi helper từng dòng)
- [x] Mask blade `exports/prospective_projects.blade.php`
- [x] Unit test `CustomerPhoneVisibilityTest` (decide 5 nhánh full + che + apply + maskMembersPhone) — 8/8 pass
- [x] `php -l` các file sửa — sạch

### FE
- [ ] Rà soát render `|| '-'` ở list/detail TKT + meeting (không sửa logic, chỉ đảm bảo hiển thị `-` gọn) — BE trả '-' nên các binding sẵn có tự hiển thị; cần mắt user xác nhận UI

### Verify
- [x] Playwright login namdangit (DNS Admin) → UI /assign/prospective-projects render OK, full path (có quyền tổng cty TKT) hiện SĐT thật, không lỗi console, không vỡ layout
- [x] Verify nhánh che `-` end-to-end qua CHÍNH resource thật + tầng auth/permission thật (actingAs, read-only): TKT#3 → owner(211)=full, namdangit(13 tổng cty)=full, low-priv(25 không quyền/không owner)=`-` cho customer_phone+contact_phone+contacts+list. Meeting#3 → owner(224)=full, low-priv(25)=`-` cho contact_phone+members_phone+customer.mobile+tab Dự án TKT
- [x] Export blade dùng cùng `canView`+ternary (canView=false→`-` đã chứng minh) — masking đồng bộ
- Ghi chú: tài khoản namdangit có quyền "TKT tổng công ty" + không có quyền meeting + toàn bộ data company_id=1 → không trigger được nhánh che qua UI bằng chính account này; đã chứng minh nhánh che qua actingAs nhân viên khác. Muốn xem `-` trực tiếp trên UI: đăng nhập 1 tài khoản sales không sở hữu/không quản lý các bản ghi này.

## Phase 2 — Bugfix: `-` round-trip khi Sửa meeting (validation 400)

### BE
- [x] `MeetingUpdateApiRequest::prepareForValidation()`: nếu `customer_contact_phone` = `-` (MASK) → khôi phục SĐT thật đang lưu trong DB trước khi validate (validation pass + không ghi đè null/`-` lên số thật). Áp cả `customer_members[].phone` = `-` → khôi phục theo `id` bản ghi thành viên (thành viên mới không id → null). FE không sửa.
- [x] `php -l` file sửa — sạch
- [x] Verify tinker: Meeting#11 (số rỗng) gửi `-` → null (pass nullable); Meeting#3 (số `0936488882`) gửi `-` → giữ nguyên `0936488882`; gửi số mới `0912345678` → giữ số mới. OK 100%

## Checkpoint
### Checkpoint — 2026-06-23
Vừa hoàn thành: Phase 1 BE + VERIFY. Helper `CustomerPhoneVisibility` + masking ở 5 resource/transformer + getDataForShow + 2 blade; unit test 8/8; php -l sạch. Verify: full path qua browser (namdangit) + cả 2 nhánh full/che qua resource thật bằng actingAs (TKT + Meeting + tab TKT). Kết quả đúng 100%.
Đang làm dở: không
Bước tiếp theo: chờ user quyết định (1) có cần mask API picker chọn KH không; (2) có cần xem `-` trực tiếp trên UI bằng tài khoản sales khác không. Nếu OK → kết thúc feature.
Blocked:
