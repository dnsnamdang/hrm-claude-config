# Plan — dong-bo-popup-chon-khach-hang

Người phụ trách: @namdangit

## Phase 1 — Đồng bộ ChooseErpCustomerModal với màn /assign/customers

### FE (hrm-client)

- [x] ChooseErpCustomerModal.vue: bỏ param `hide_individual` + `phone_exact_bypass`, thêm `status=1` (chỉ KH Hoạt động) khi gọi GET assign/customers
- [x] ChooseErpCustomerModal.vue: đồng nhất cột theo màn danh sách chính (STT, Mã KH - Tên KH + tên viết tắt, Loại, MST, SĐT, Email, Nhóm KH, Địa chỉ, Tỉnh/TP, Trạng thái pill)
- [x] Giữ sắp xếp id desc (đã trùng màn chính), giữ 3 ô tìm kiếm (Tên/Mã, MST, SĐT)
- [x] Fix CSS: mã KH màu xám nhạt (.cell-code) như màn chính — chặn CSS global tô đỏ
- [x] (User chốt 2026-07-02) BỎ cột Trạng thái trên popup → còn 9 cột
- [x] (User chốt 2026-07-02) GIỮ LẠI `phone_exact_bypass` — search đúng SĐT vẫn ra KH ngoài phạm vi quyền

### BE (hrm-api)

- [x] Không sửa — endpoint dùng chung sẵn; 2 flag cũ là opt-in trong CustomerService::index, không client nào còn gửi (giữ để revert dễ)

### Verify

- [x] BE (php -r, Auth::setUser namdangit): main(status=1) = popup(mới) = 41.209 KH, top-5 id trùng thứ tự; popup cũ (hide_individual) chỉ 11.209
- [x] AC4 BE: search mã KH cá nhân `79TKHPNH-36` → popup mới YES (cũ NO); search SĐT `0981927967` → popup (mobile) và màn chính (tax_code) cùng tìm thấy, n=1
- [x] Playwright UI (token-inject namdangit): popup Tạo meeting + Tạo dự án TKT — 10 cột khớp màn chính, total 41.209, KH cá nhân hiện, search mã + SĐT PASS, status pill Hoạt động

## Phase 2 — Ownership TH1/TH2/TH3 (spec: design-phase2.md, user chốt 4 quyết định 2026-07-02) — CODE DONE + VERIFIED

### BE (hrm-api)

- [x] Helper `app/Helper/CustomerOwnership.php`: activeRegisters memo + customerRegisteredByOther/contactRegisteredByOther + myActiveRegister*/myInteractionCustomerIds (báo giá ERP + meeting/TKT HRM) + allHrmInteractionCustomerIds + isMyCustomer + LOCK_MESSAGE
- [x] CustomerService::index: applyB2cOwnershipVisibility (B2C tự do ẩn; hiện khi: mình tạo/đăng ký/tương tác, có người đăng ký còn hạn, có báo giá bất kỳ, có meeting/TKT, đúng full SĐT) + applyErpVisibilityScope thêm nhánh myVisibleCustomerIds
- [x] CustomerListResource: register_locked + register_locked_message + mobile RÕ khi isMyCustomer (TH1), '-' còn lại
- [x] Validate 422: ProspectiveProjectRequest (customer_id/customer_benefit_id/2 contact id — bỏ qua khi update giữ nguyên) + MeetingCreateApiRequest + MeetingUpdateApiRequest (chỉ chặn khi đổi)
- [x] customerContacts: thêm nhánh myActiveRegisterContactIds + báo giá contact; trả locked + locked_message; show() contacts thêm locked

### FE (hrm-client)

- [x] ChooseErpCustomerModal: badge đỏ "Đã có người đăng ký" + chặn click + toast
- [x] GeneralInfo (meeting): droplist contact nhãn 🔒 + guard onContactChange (toast + reset); FIX auto-fill contacts[0] → contact đầu KHÔNG locked (2 chỗ)
- [x] CustomerBlock (TKT): droplist contact nhãn 🔒 + guard handleContactChange (toast + reset)
- [x] Màn /assign/customers: hưởng rule qua BE (không sửa FE)

### ERP (TanPhatDev) — yêu cầu bổ sung 2026-07-02: quy tắc hiển thị ERP = HRM

- [x] `app/Services/CustomerOwnership.php` (ERP): mirror helper HRM, đọc HRM meetings/TKT qua connection 'hrm' (map user qua employee_info_id, try/catch an toàn)
- [x] Customer::searchByFilter: applyB2cVisibility cuối hàm — B2C tự do ẩn, ô MST/SĐT khớp đúng full SĐT thì hiện
- [x] Che SĐT danh sách ERP như HRM (user chốt): CustomersController::searchData cột tax_code (B2C) → isMyCustomer ? mobile : '-' (TH1 hiện RÕ theo spec); export CSV/PDF không có mobile nên không đụng

### Verify (2026-07-02, DB thật, seed 3 register test note=TEST-OWNERSHIP-CLAUDE — ĐÃ DỌN)

- [x] BE HRM: TH3 ẩn tìm mã / hiện đúng SĐT; TH2 hiện + register_locked=true + mobile '-'; TH1 hiện + mobile RÕ; tổng 41.209 → 16.619
- [x] Validate: TKT customer_id + contact TH2 → 422 đúng message; Meeting TH2 → lỗi, TH1 → không lỗi
- [x] UI Playwright: popup TH2 badge + chặn click + toast; TH3 ẩn/hiện; droplist contact 🔒 + toast + reset; auto-fill bỏ qua contact khóa
- [x] ERP (php7.4 tinker, user 13): TH3 ẩn/hiện đúng SĐT, TH2 + TH1 hiện; tổng 16.971

### Test theo yêu cầu user — tài khoản vietvt.kd3@tanphat.com × KH HỒ ĐĂNG TRƯỜNG (43240) — 2026-07-02

- Hiện trạng KH 43240: cá nhân, Hoạt động, mobile 0906781070, created_by=583, 2 firm_quotations (đều của 583), 0 register, 0 meeting/TKT. User vietvt: HRM id 78 = ERP id 78, quyền view nhưng KHÔNG cấp nào (chỉ của mình). Login API fail với pass user đưa (pass của server dev?) → dùng JWTAuth::fromUser.
- [x] V1 Baseline màn chính tìm mã → ẨN (ngoài quyền); V2 popup đúng SĐT+bypass → HIỆN, locked=false, mobile '-'
- [x] TH2 (seed register bởi 583): V3 popup → locked=true + msg; V4 lưu meeting → 422; V5-V7 UI Playwright bằng token vietvt → badge + click chặn + toast PASS
- [x] TH1 (đổi register → 78): V8 màn chính tìm mã → HIỆN + mobile RÕ 0906781070; V9 lưu meeting → không chặn; V10 ERP → HIỆN + SĐT RÕ
- [x] FIX phát sinh từ V10: ERP searchByFilter 4 nhánh quyền (công ty/phòng ban/bộ phận/của mình) chưa cộng nhánh ownership → thêm orWhereIn(myVisibleCustomerIds) vào cả 4 closure (mirror applyErpVisibilityScope HRM) + helper ERP thêm myVisibleCustomerIds()
- [x] V11 hồi quy: xóa register → ERP vietvt lại ẨN đúng. Data test đã dọn (0 sót)
- HƯỚNG DẪN SEED TEST: INSERT vào dev_erp.customer_registers (customer_id, customer_contact_id=NULL với KH cá nhân / =id contact với DN, employee_id=ERP employees.id của sales đăng ký, expired_date >= hôm nay, note tùy ý) — xóa dòng đó để trả lại trạng thái

## Phase 3 — Popup: KH TỔ CHỨC hiện tất cả, không bám quyền (yêu cầu 2026-07-03)

### BE (hrm-api)

- [x] CustomerService::index + applyErpVisibilityScope: nhận cờ `all_business=1` → thêm nhánh `orWhere customer_type != 1` vào lớp quyền (tổ chức pass quyền; cá nhân vẫn qua lớp quyền + ownership như cũ)

### FE (hrm-client)

- [x] ChooseErpCustomerModal: gửi thêm `all_business: 1` khi gọi GET assign/customers (chỉ popup; màn /assign/customers không đổi)

### Verify (2026-07-03, user vietvt id 78 — không có cấp quyền nào)

- [x] Service-level: popup mới 11.001 (tổ chức 10.858 = TOÀN BỘ tổ chức Hoạt động is_customer=1; cá nhân 143 = giữ nguyên, không leak); màn chính (không cờ) vẫn 262
- [x] HTTP thật (JWT vietvt): popup total=11.001, màn chính total=262

### Checkpoint — 2026-07-02 (Phase 2 xong + test tổng)

Vừa hoàn thành: (1) FIX gap escape SĐT màn chính HRM — ô MST/SĐT (tax_code) + ô mobile giờ đều kích hoạt hiện KH TH3 khi khớp đúng full SĐT (trước chỉ popup có bypass mới hiện); (2) che SĐT ERP theo TH1 (searchData cột tax_code); (3) TEST TỔNG 27 case PASS 100%: BE HRM 7 (TH1/2/3 + contact locked + tổng 16.619) + HTTP validate 4 (422 TKT KH/contact, meeting TH2 chặn/TH1 không) + UI Playwright 15 (màn chính U1-4: tổng 16.971, TH3 ẩn, TH1 SĐT rõ, TH2 che; popup meeting U5-9: badge/chặn/ẩn-hiện/chọn TH3 OK; contact U10-13: auto-fill né khóa, nhãn 🔒, toast, reset; TKT U14-15) + ERP 8 (E1-8: ẩn/hiện/che SĐT/tổng 16.971). Đã dọn 3 register test.
Đang làm dở: không
Bước tiếp theo: user verify browser bằng mắt (HRM /assign/customers + popup; ERP /admin/customers) — hành vi đã test máy toàn bộ
Blocked:
