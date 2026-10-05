# Plan — Lịch sử xem phiếu đề xuất cung ứng

> Phụ trách: @khoipv · Ngày: 2026-09-18
> Design: `.plans/lich-su-xem-de-xuat-cung-ung/design.md`
> Spec: `docs/superpowers/specs/2026-09-18-lich-su-xem-de-xuat-cung-ung-design.md`

## Phase 0 — Brainstorm & chốt design

- [x] 0.1 Chốt yêu cầu: điểm ghi log (chỉ inbox), phạm vi NV (toàn hệ thống), mức thời gian (chỉ lần đầu), vị trí nút (chỉ inbox)
- [x] 0.2 Fill spec đầy đủ + design.md

## Phase 1 — BE

- [x] 1.1 Migration `2026_09_18_000001_create_supply_proposal_views_table` — unique(proposal, employee), index employee, không khóa ngoại
- [x] 1.2 Entity `SupplyProposalView` + 2 hằng source
- [x] 1.3 `SupplyProposalService::markViewed()` — insertOrIgnore theo `auth()->user()->id`, idempotent
- [x] 1.4 `SupplyProposalService::handlerEmployeeIds()` (private) — NV có quyền 514 qua vai trò + gán trực tiếp, chỉ tài khoản active
- [x] 1.5 `SupplyProposalService::viewHistory()` — union 3 tập (có quyền / đã xem / đã lập PXL), gộp PXL theo người, sắp xếp đã xem trước
- [x] 1.6 Controller `markViewed()` + `viewHistory()`
- [x] 1.7 Routes: `POST /{supplyProposal}/mark-viewed`, `GET /{supplyProposal}/view-history`
- [x] 1.8 Chạy migrate + verify bằng tinker với dữ liệu thật

## Phase 2 — FE

- [x] 2.1 `constants.js` — thêm `VIEW_SOURCE = { VIEW: 1, CREATE_HANDLING: 2 }`
- [x] 2.2 Component mới `components/ViewHistoryModal.vue` — bảng 6 cột, badge trạng thái xem, link PXL
- [x] 2.3 `inbox.vue` — nút "Lịch sử xem phiếu" ở cột Thao tác + nhúng modal
- [x] 2.4 `inbox.vue` — `markViewed()` gọi trước điều hướng ở `onViewClick` và `onCreateHandlingClick`, nuốt lỗi
- [x] 2.5 Verify compile template + `php -l`

## Phase 3 — Verify

- [x] 3.1 Test API bằng tinker/curl: ghi 2 lần chỉ 1 dòng, danh sách trả đúng người
- [ ] 3.2 @khoipv click-through trên trình duyệt

### Checkpoint — 2026-09-18
Vừa hoàn thành: BE (migration + entity + service + controller + route) và FE (constants `VIEW_SOURCE`, `components/ViewHistoryModal.vue`, nút "Lịch sử xem phiếu" + `markViewed()` ở `inbox.vue`). Verify BE bằng script bootstrap Laravel trên DB `thanhan_stag_07052026`: gọi `markViewed` 3 lần cho 2 người → đúng 2 dòng log (idempotent); `viewHistory` trả 10 NV có quyền, hiện `PXL-2026-0001 (Đã duyệt)` cho người đã lập phiếu. Đã xóa dữ liệu test. Template 2 file Vue compile sạch.
Đang làm dở: không
Bước tiếp theo: 3.2 — @khoipv click-through trên trình duyệt (mở inbox, bấm Xem / Tạo phiếu xử lý rồi mở popup Lịch sử xem phiếu kiểm tra)
Blocked:

## Phase 4 — Chuẩn hóa cột Thao tác (theo yêu cầu 18/09/2026)

- [x] 4.1 `inbox.vue` — dựng mảng `rowActions(item)` + `inlineActions()` / `moreActions()` thay cho các nút `v-if` rời
- [x] 4.2 `inbox.vue` — template lặp nút ngoài + dropdown bánh răng `fa fa-cog`
- [x] 4.3 Skill mới `.claude/skills/button-convention/SKILL.md` — quy tắc <=3 hiện hết / >3 thì 2 nút + bánh răng
- [x] 4.4 `docs/conventions.md` — thêm 1 dòng quy tắc ở mục Quy tắc Frontend, trỏ sang skill
- [x] 4.5 Verify: compile template sạch + test 4 kịch bản chia nút

### Checkpoint — 2026-09-18 (lần 2)
Vừa hoàn thành: áp quy tắc cột Thao tác của màn `contract/contract` vào `inbox.vue`. Test 4 kịch bản: không quyền → 2 nút; có quyền chưa cho từ chối → 3 nút hiện hết; có quyền + từ chối được → 4 nút (Xem, Tạo phiếu xử lý ở ngoài; Từ chối, Lịch sử xem phiếu vào bánh răng); phiếu đã xử lý → 2 nút.
Đang làm dở: không
Bước tiếp theo: 3.2 — @khoipv click-through trên trình duyệt
Blocked:

- [x] 4.6 Đồng bộ cấu trúc skill theo bên `hrm`: chuyển `thanh_an/.skills/` → `thanh_an/.claude/skills/`, symlink `dns/.claude/skills`, thêm bảng "Skill bắt buộc đọc theo ngữ cảnh" vào `CLAUDE.md`
- [x] 4.7 Sửa `hrm-claude-config/thanh_an/.gitignore`: dòng `.claude/` (ignore cả thư mục → skill không được track) đổi thành `.claude/settings.local.json` + `.claude/settings.json`, giống bên `hrm`

### Checkpoint — 2026-09-18 (lần 3)
Vừa hoàn thành: đồng bộ cấu trúc skill giống bên `hrm` — 9 skill nằm ở `thanh_an/.claude/skills/`, symlink `dns/.claude/skills`, bảng "Skill bắt buộc đọc theo ngữ cảnh" trong `CLAUDE.md`, và sửa `.gitignore` để git track được skill (trước đó `.claude/` bị ignore nên move = xóa sạch skill khỏi repo).
Đang làm dở: không
Bước tiếp theo: 3.2 — @khoipv click-through popup lịch sử xem phiếu trên trình duyệt (cần build lại client); và tự commit PR config (đã đủ file, không tự commit theo quy tắc)
Blocked:

- [x] 4.8 Fix UI cột Thao tác: nút dính sát nhau → container `.action-cell` (flex + `gap: 6px`); icon Lịch sử `text-secondary` tàng hình (theme đặt `$secondary: $white` trên nền `.btn-secondary #e5f1fe`) → bỏ class màu, ăn theo màu chữ nút `#0070f4`. Cập nhật 2 bẫy này vào `button-convention/SKILL.md`
- [x] 4.9 Popup lịch sử xem phiếu: mở rộng `size="lg"` → `size="xl"`; đổi cột **Công ty** → **Phòng ban** (BE join `departments` qua `employee_infos.department_id`, trả `department_name` thay `company_name`)
- [x] 4.10 Thêm cột **Trạng thái xem** (của chính người đăng nhập) ra ngoài bảng inbox: BE `inbox()` selectSub `my_viewed_at` từ `supply_proposal_views` theo `auth()->user()->id`; Resource trả `my_viewed_at`; FE thêm field + badge Đã xem/Chưa xem (đồng bộ màu với popup)
- [x] 4.11 Bên ngoài bảng inbox: cột Trạng thái xem chỉ để badge Đã xem / Chưa xem, bỏ thời điểm (thời điểm giữ trong popup). Gỡ `fmtDateTime` + `import dayjs` khỏi `inbox.vue`
- [x] 4.12 Popup: mã phiếu xử lý đổi từ `@click` + `$router.push` sang `<nuxt-link target="_blank">` → mở tab mới, popup không bị đóng, hỗ trợ ctrl/giữa chuột
- [x] 4.13 Popup: bỏ trạng thái phiếu xử lý `({{ h.status_name }})` ở cột Phiếu xử lý đã lập, chỉ còn mã phiếu (gỡ cả SCSS `.vh-pxl-status`)

## Phase 5 — Áp quy tắc button cho toàn phân hệ Cung ứng (18/09/2026)

- [x] 5.1 `supply/contract_render/index.vue` — 2 nút điều hướng (`to`), không cần bánh răng
- [x] 5.2 `supply/purchase_contracts/index.vue` — Xem → Duyệt → Sửa → Xóa
- [x] 5.3 `supply/purchase_orders/index.vue` — như trên
- [x] 5.4 `supply/supply_handlings/index.vue` — như trên (cờ duyệt là `can_approve`)
- [x] 5.5 `supply/supply_proposals/index.vue` — Xem → Duyệt/Từ chối (BGĐ) → Gửi → Sửa → Thu hồi → Xóa
- [x] 5.6 `supply/supply_proposals/inbox.vue` — đồng bộ markup chung (thêm `:to`, `a.handler && a.handler()`)
- [x] 5.7 Bỏ khối SCSS `.btn-small` bị chèn trùng (5 màn đã có sẵn khối này)
- [x] 5.8 Cập nhật `button-convention/SKILL.md`: template chung hỗ trợ `to`, thứ tự nút chuẩn, bẫy chèn trùng `.btn-small`, danh sách màn tham chiếu
- [x] 5.9 Verify: 6 file compile sạch + test chia nút từng kịch bản

### Checkpoint — 2026-09-18 (lần 4)
Vừa hoàn thành: chuẩn hóa cột Thao tác cho toàn bộ 6 màn danh sách của phân hệ Cung ứng theo skill button-convention.
Đang làm dở: không
Bước tiếp theo: @khoipv build client + click-through kiểm tra thực tế
Blocked:
- [x] 5.10 Nút **Quay lại** ở 4 màn Cung ứng (`purchase_contracts/_id`, `purchase_orders/_id`, `supply_handlings/add`, `supply_proposals/add`): đổi từ `$router.push('<màn danh sách>')` sang `$router.back()`, fallback về màn danh sách khi `window.history.length <= 1` (mở bằng tab mới / dán link)
