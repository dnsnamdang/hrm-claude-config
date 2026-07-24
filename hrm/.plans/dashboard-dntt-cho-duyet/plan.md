# Plan — Dashboard box DNTT chờ duyệt (@khoipv)

## Phase 1 — BE
- [x] `WaitingApproveService.php`: import `PaymentBusinessRequest`, thêm
      `countPaymentBusinessRequestTpWaitingApprove()` (status=CHO_TP_DUYET, whereIn department_id listManageDepartmentIds)
- [x] `WaitingApproveService.php`: thêm `countPaymentBusinessRequestKtWaitingApprove()` (status=CHO_KT_DUYET, cùng scope)
- [x] `DashboardService.php`: gọi 2 count + append 2 item vào `$jobsWaitingApprove` (dưới HSTT công tác),
      isShow = ['TP Duyệt đề nghị thanh toán'] / ['KT Duyệt đề nghị thanh toán'], link status=2 / status=3

## Phase 2 — FE
- [x] `payment_business_request/index.vue` `mounted()`: nếu có `$route.query.status` → gán `formFilter.status`
      (Number) trước `getData()`, để bấm link lọc sẵn đúng trạng thái

## Phase 3 — Verify
- [x] `php -l` 2 file BE sạch
- [x] Kiểm tra logic: tên quyền khớp seeder (975/980), scope listManageDepartmentIds, link status=2/3
- [ ] (tồn) User verify UI: đăng nhập TK có quyền 975/980 → thấy 2 dòng, count đúng, bấm link lọc đúng status

## Phase 4 — Đổi scope sang dùng lại màn danh sách (user chốt lại 2026-07-17)
- [x] `WaitingApproveService.php`: thêm private `applyPaymentBusinessRequestScope()` nhân bản phân cấp
      Criteria (tổng cty/cty/phòng ban/bộ phận theo quyền Xem 976/977/978/1022); 2 method count gọi helper
- [x] Import `PaymentBusinessRequestEmployee`; KHÔNG sửa Criteria (hàm dùng chung)
- [x] `php -l` sạch

## Checkpoint
### Checkpoint — 2026-07-17 (bản 2)
Vừa hoàn thành: Đổi scope box từ "chỉ phòng ban công ty hiện tại" → dùng lại scope màn danh sách (4 cấp theo quyền Xem, tổng công ty thấy tất cả công ty). Nhân bản Criteria vào helper applyPaymentBusinessRequestScope, không sửa Criteria. php -l sạch. Số đếm giờ khớp màn danh sách khi lọc status 2/3.
Đang làm dở: (không)
Bước tiếp theo: user verify UI — TK tổng công ty thấy tất cả công ty; TK công ty/phòng ban thấy đúng phạm vi; count khớp danh sách lọc status
Blocked:
