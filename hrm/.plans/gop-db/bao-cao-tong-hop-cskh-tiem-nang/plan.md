# Plan — Báo cáo tổng hợp chăm sóc khách hàng tiềm năng

> Spec: `docs/superpowers/specs/gop-db/2026-10-04-bao-cao-tong-hop-cskh-tiem-nang-design.md` · Design: `design.md` · Mockup: `mockup.html`
> Nhánh `gop_db-bao-cao-tong-hop-cskh-tiem-nang` (api + client) · worktree `websites/wt-bao-cao-tong-hop-cskh/`
> ✅ 04/10/2026 user cho phép: code BE+FE trong worktree, INSERT tay 3 quyền 1676–1678 vào hrm_erp local + cache:clear. KHÔNG migration, KHÔNG chạy seeder, KHÔNG commit/push.

## Phase 1 — Backend (`hrm-api`)

- [x] T1. Seeder: 3 quyền id 1676–1678, nhóm "Báo cáo tổng hợp CSKH tiềm năng", type 4 (kiểm `uniq -d` id sau khi thêm)
- [x] T2. Test trước (TDD): `tests/Feature/Assign/PotentialCustomerTrackingTest.php` — nguồn dữ liệu, Sales COALESCE, phòng hiện tại, hạn/soon, chăm sóc gần nhất, khớp số bảng = tổng hợp = popup
- [x] T3. Test quyền: tổng công ty / công ty / phòng ban / không quyền (role tạm + xoá cache spatie)
- [x] T4. `PotentialCustomerTrackingService`: `items()` (2 nguồn + gắn tổ chức batch + hạn hàng loạt + chăm sóc gần nhất), quyền, bộ lọc
- [x] T5. `index()` (cây Phòng ▸ Sales ▸ KH ▸ lá, tổng hợp, phân trang theo Phòng) · `itemList()` · `filterOptions()`
- [x] T6. Controller + 6 route `report/potential-customer-tracking` (không `checkPermission`)
- [x] T7. Xuất Excel cây + Excel popup (skill `export-excel`) · `print-list-data` + PrintService (skill `print-page`)
- [x] T8. Chạy PHPUnit `--filter PotentialCustomerTracking` xanh

> Phase 1 xong 04/10: PHPUnit `--filter "ServiceDemand|PotentialCustomerTracking"` 62/62 (17 mới). Đột biến kiểm test: bỏ quyền → 4 đỏ, phòng cứng → 3 đỏ.
> Dữ liệu thật local: 7 query, ~50ms (16 phòng · 152 nhu cầu · 282 dự án · 99 Sales). Quyền phòng ban = `listManageDepartmentIds()` (phòng được phân công quản lý, như báo cáo CSKH tiềm năng).
> File: `Services/Report/PotentialCustomerTracking{Service,PrintService}.php` · `Http/Controllers/Api/V1/PotentialCustomerTrackingReportController.php` · `Export/PotentialCustomerTracking{,List}Export.php` · 4 blade `exports|prints/assign/potential_customer_tracking_*` · 6 route · seeder +3 quyền · `tests/Feature/PotentialCustomerTracking/` (Fixture + ReportApiTest 13 + ExportPrintTest 4)

## Phase 2 — Frontend (`hrm-client`)

- [x] T9. `api.js` · `format.js` · `index.vue` (SmartFilterPanel 8 ô, nút In / Xuất Excel)
- [x] T10. `TrackingSummary.vue` (2 khối, ẩn chỉ tiêu 0, drill)
- [x] T11. `TrackingTable.vue` (4 cấp, ô chọn cấp bung, dòng TỔNG, V2BaseTableScroll, sticky, CSS cấp 4)
- [x] T12. `ItemListModal.vue` (V2BaseReportModal + reportDrillListMixin) + MeetingDetailDrawer + popup lịch sử meeting dùng lại
- [x] T13. In danh sách / Xuất Excel (màn chính + popup)
- [x] T14. Menu `presale.js`
- [x] T15. Kiểm bằng Playwright MCP: đo DOM so mockup (1600 + 1366), có quyền / không quyền
- [x] T16. Viết e2e `e2e/tests/assign/potential-customer-tracking{.api,}.spec.ts` + `e2e/utils/potentialCustomerTrackingFixture.ts` (13 ca; tsc sạch, `--list` đọc được) — ✅ đã chạy 04/10 (user yêu cầu): API 7/7 · UI 6/6

> Phase 2 xong 04/10: kiểm bằng Playwright MCP trên server WORKTREE (Nuxt 3017 · API 8017), đo DOM ở 1600 + 1366:
> 8 ô lọc 2×4 · không quyền: ô Công ty khoá, số 0 · quyền tổng công ty (role tạm, ĐÃ GỠ): 16 phòng / 152 NC / 282 DA, ẩn tiến trình 0 ·
> cây 4 cấp thụt 30/52/74/96 · tiêu đề dính · 2 thanh cuộn · popup 152/152 khớp TỔNG, footer trong màn · panel meeting z 1060 trên popup có khối
> "Nhu cầu làm dự án" · popup lịch sử meeting dùng lại · bản in + 2 Excel OK · lọc Loại / Tiến trình (chọn nhiều) bằng thao tác chuột thật OK.
> Lỗi tự bắt + sửa: (1) khối tổng hợp 10 ô bị bóp -> nhãn 2 dòng, ô cao 58px (sửa: khối NC rộng theo nội dung, ô xuống hàng) ·
> (2) `buildQueryString` ghi mảng không `[]` -> link Excel mất lọc tiến trình (sửa: gửi chuỗi "7,8", BE nhận cả 2 dạng + PHPUnit).
> PHPUnit `--filter PotentialCustomerTracking` 17/17 (108 assertion).

## Checkpoint

### Checkpoint — 2026-10-04
Vừa hoàn thành: brainstorm + mockup chốt + spec + design + plan; tạo worktree 2 repo (nhánh mới từ origin/gop_db, đã gỡ upstream, copy vendor/node_modules thật, autoload trỏ đúng worktree)
Đang làm dở: —
Bước tiếp theo: chờ user cho phép code (phạm vi ở câu hỏi cuối session)
Blocked: chờ phép code
- 04/10: chạy riêng migration 2026_09_28_100000_add_due_days_snapshot vào hrm_erp local (user cho phép); 22 migration khác vẫn chưa chạy

### Checkpoint — 2026-10-04 (code xong)
Vừa hoàn thành: Phase 1 BE (T1–T8) + Phase 2 FE (T9–T16); kiểm Playwright MCP đạt; e2e đã viết chưa chạy
Đang làm dở: —
Bước tiếp theo: user review trên http://127.0.0.1:3017/assign/report/potential-customer-tracking (worktree) → quyết chạy e2e / commit + push nhánh feature (KHÔNG merge gop_db)
Blocked: chờ user

## Phase 3 — Sửa sau khi chạy e2e (04/10, user cho phép nới Meeting::canView)

- [x] T17. Fixture e2e: bảng `scopes` (DB gộp) không có cột `internal_business_scope_id` -> lấy 3 scope id bất kỳ
- [x] T18. e2e ca 4 bắt lỗi THẬT: người chỉ có quyền báo cáo bấm mã meeting -> 403, panel trống (kiểm MCP bằng tài khoản e2e quyền rộng nên không lộ). Test trước `tests/Feature/PotentialCustomerTracking/MeetingViewPermissionTest.php` (đỏ 3/4) -> thêm `Meeting::canViewByPotentialCustomerTracking()` -> xanh
- [x] T19. PHPUnit `--filter "PotentialCustomerTracking|ServiceDemand"` 66/66 · e2e API 7/7 + UI 6/6 (chạy lại toàn bộ sau sửa)

### Checkpoint — 2026-10-04 (e2e xong)
Vừa hoàn thành: chạy e2e theo yêu cầu, sửa fixture + nới Meeting::canView; toàn bộ xanh
Đang làm dở: —
Bước tiếp theo: user quyết commit + push nhánh feature (KHÔNG merge gop_db)
Blocked: chờ user

### Checkpoint — 2026-10-04 (merge local)
Vừa hoàn thành: commit 2 repo + merge --no-ff vào gop_db LOCAL (origin/gop_db không đổi từ lúc tách nhánh, 0 marker xung đột)
Đang làm dở: —
Bước tiếp theo: user tự kiểm rồi push `gop_db` + nhánh feature ở cả 2 repo (user chọn CHƯA push)
Blocked: —

## Phase 4 — Quyền nằm sai phân hệ (04/10, user báo: không thấy quyền ở CSKH trước bán)

- [x] T20. Điều tra: tài khoản namdangit (DNS Admin, id 13) chưa có 1676–1678 -> mức "không quyền" -> bảng + ô Phòng ban trống (ĐÚNG thiết kế). Gốc thật: seed `type = 4` (Giao việc) trong khi phân hệ CSKH trước bán là `permissionType: 29`; màn Phân quyền gom theo `type`
- [x] T21. User chọn chuyển CẢ nhóm báo cáo thị trường: 1179–1181 · 1187–1189 · 1660–1661 · 1676–1678 sang type 29 (seeder + UPDATE hrm_erp local; role_has_permissions 14/14 giữ nguyên). Kiểm màn `/timesheet/setting/roles/add/100010`: khối CSKH trước bán 19 quyền / 7 nhóm, Giao việc không còn 4 nhóm này
- [x] T22. Commit `edf4ce768` + merge lại gop_db LOCAL `85a1c59d7` (chưa push)

### Checkpoint — 2026-10-04 (quyền về đúng phân hệ)
Vừa hoàn thành: đổi type quyền báo cáo thị trường, merge lại gop_db local
Đang làm dở: —
Bước tiếp theo: user cấp quyền 1676/1677/1678 cho role (màn Phân quyền › CSKH trước bán) rồi xem lại báo cáo; push khi user đồng ý
Blocked: —

## Phase 5 — Commit · merge · push · deploy (04/10)

- [x] T23. Push `gop_db` (api `b211161a1..85a1c59d7` · client `01a5d1b92..a6ad678d0`, fast-forward) + nhánh feature cả 2 repo
- [x] T24. Deploy VPS (user tự chạy): `migrate:status` sạch · INSERT 1676–1678 type 29 · UPDATE type 29 cho 1179–1181, 1187–1189, 1660–1661 · cache:clear · build client

### Checkpoint — 2026-10-04 (wrap up)
Vừa hoàn thành: feature xong toàn bộ — merge + push gop_db, user đã deploy VPS
Đang làm dở: —
Bước tiếp theo: (tuỳ chọn) gán quyền 1676–1678 cho role trên production · dọn worktree `websites/wt-bao-cao-tong-hop-cskh/` · cân nhắc tách công thức "sắp hết hạn" (3 bản chép: cron, CustomerDemandService, báo cáo này) thành hàm dùng chung
Blocked: —

## Phase 6 — Bộ phận + Ngân sách dự kiến (07/10/2026, user chốt)

- Bộ lọc thêm ô **Bộ phận** (theo bộ phận HIỆN TẠI của Sales, chỉ bộ phận của phòng đang chọn, không lấy bộ phận đã khoá).
- Cây Phòng ban ▸ **Bộ phận** ▸ Sales ▸ Khách hàng ▸ NC/DA: phòng không chia bộ phận bỏ cấp; Sales chưa gán bộ phận ở phòng
  có chia → nhóm "Không thuộc bộ phận" cuối phòng. Ô chọn cấp thêm "Đến Bộ phận". Bản in / Excel / popup có cấp này.
- Cột "Giá trị dự án" → **"Ngân sách dự kiến"** = `prospective_projects.estimated_budget` (thay `expected_contract_amount`).
  Đo DB local: có ngân sách 273/282 dự án (giá trị HĐ dự kiến chỉ 151/282).
- **Dự án cha (có dự án con) KHÔNG đưa vào báo cáo**, chỉ lấy dự án con (tránh cộng trùng ngân sách). DB local: 1 cặp.

- [x] T25. BE service: estimated_budget · bỏ dự án cha · part_id/part_name theo Sales · lọc part_id · cây có cấp Bộ phận · danh mục bộ phận
- [x] T26. BE bản in + Excel: cấp Bộ phận + đổi tên cột · unit test
- [x] T27. FE: ô lọc Bộ phận · TrackingTable cấp Bộ phận + ô chọn cấp + tên cột/tooltip · popup
- [x] T28. Kiểm Playwright MCP + cập nhật e2e: spec UI ca 1 (9 ô / 3 hàng đủ 12 cột) + ca 3 (cây theo độ sâu thật, dòng lá
      class `rsum-tb__row--leaf`); .api.spec dùng `salesOf()` (Sales nằm trong parts khi phòng có bộ phận). Biên dịch được
      (16 ca), CHƯA chạy — user: "e2e chạy sau".

### Checkpoint — 2026-10-07
Vừa hoàn thành: T25–T28. Unit `PotentialCustomerTracking*` 24/24 xanh (3 ca mới `PotentialCustomerTrackingPartBudgetTest`;
4 ca Feature cũ đổi fixture `expected_contract_amount` → `estimated_budget` + tiêu đề Excel mới).
Đo: 3/16 phòng có bộ phận (KDTM 4 bộ phận); "Đến Bộ phận" chỉ bung 3 phòng đó; lọc "Kinh doanh dự án" → 13 việc, ô Sales
co còn 1; popup từ dòng bộ phận gửi part_id, 47 dòng = 47 nhu cầu của bộ phận; dự án 67 = ngân sách DB; dự án cha 159
không còn trong báo cáo. Giữa chừng dev server Nuxt (PID 43570, chạy 13 ngày) treo — user cho khởi động lại, build sạch.
Lưu ý dữ liệu: tổng Ngân sách dự kiến 4,625 tỷ+ vì vài dự án nhập ngân sách rất lớn (vd dự án 67 = 1,600 tỷ) — dữ liệu
nhập tay, không phải lỗi tính.
Bước tiếp theo: chạy e2e khi user yêu cầu · user kiểm trên app.
- [x] T29. (07/10, user hỏi) Nhóm "Không thuộc bộ phận": DB local KHÔNG có ca thật (mọi Sales ở 3 phòng có bộ phận đều đã gán)
      → thêm unit test dữ liệu giả, bắt được LỖI: sắp nhóm so khoá `'0'` nhưng PHP đổi khoá mảng thành số 0 → nhóm bị xếp
      theo tên thay vì đứng cuối. Sửa: so `part_id === null` của dòng. Unit 25/25 xanh.

### Checkpoint — 2026-10-07 (wrap up)
Vừa hoàn thành: Phase 6 T25→T29 (Bộ phận, Ngân sách dự kiến, bỏ dự án cha, sửa nhóm Không thuộc bộ phận đứng cuối); ĐÃ COMMIT + PUSH gop_db (api e20e02e04, client c62d1a79b)
Đang làm dở: —
Bước tiếp theo: deploy production · chạy e2e potential-customer-tracking{,.api} khi user yêu cầu (spec đã sửa, biên dịch được)
Blocked: —
