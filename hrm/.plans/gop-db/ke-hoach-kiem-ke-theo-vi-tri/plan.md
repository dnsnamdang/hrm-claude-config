# Kế hoạch kiểm kê theo vị trí — Plan

> @khoipv · nhánh `develop` (từ `gop_db`) · Spec: `docs/superpowers/specs/gop-db/2026-10-17-ke-hoach-kiem-ke-theo-vi-tri-design.md`

## Phase 0 — Khảo sát
- [x] Khảo sát nghiệp vụ màn ERP `position_inventories` (bảng nghiệp vụ bước 1 skill erp-to-hrm-screen)
- [x] Chốt phạm vi + quyền + phân hệ với user (17/10: chỉ màn Kế hoạch; phạm vi như ERP; Tạo/Sửa/Xóa không quyền; xóa = Đang tạo + người tạo)

## Phase 1 — BE (`Modules/Finance`)
- [x] B1. 2 quyền xem mới trong `PermissionsTableSeeder` (type 8) + `permission:sync --dry-run` (chỉ dry-run, CHƯA sync thật vào DB local)
- [x] B2. Entities `PositionInventory/*` (khai `$table`, quan hệ, STATUSES + status_type, global scope `type=0`, `scopedQuery()`, `canView/canEdit/canDelete/canCreateResult`, `generateCode`)
- [x] B3. `PositionInventoryService`: list + filter + sort + export-rows + filter-options + detail
- [x] B4. `PositionInventoryWriteService`: form-options, structure, positions (Lấy vị trí), store/update (lưu snapshot FE gửi như ERP), destroy, thông báo khi Gửi
- [x] B5. FormRequest + Controller + routes `/position-inventories`
- [x] B6. Lịch sử: đăng ký `position_inventories` trong `CatalogHistoryService::TABLES` + trait log create/update/change_status/delete + endpoint `/{id}/histories` (+ filter-options) chặn theo canView
- [x] B7. In phiếu (template 51) + in danh sách (template 284, trần 2.000 dòng) + Xuất Excel 1 phiếu (`PositionInventoryExport` + blade `finance::exports.position_inventory`)
- [x] B8. Smoke test tinker: list theo 4 mức (SA / tổng công ty giả lập / công ty giả lập / không quyền), tạo/sửa/xóa, 409, 404, in, xuất — pass; đã dọn id test 115, 116

### Checkpoint — 2026-10-17 (Phase 1 BE)
Vừa hoàn thành: B1–B8 (BE). API contract thực tế ghi trong báo cáo subagent.
Đang làm dở: —
Bước tiếp theo: F1 (FE danh sách) theo API contract; user quyết 2 điểm lệch spec: (1) canView mở cho thủ kho được "Lập phiếu kiểm kê" (deep-link thông báo), (2) `members.*.role_id` bắt buộc (cột NOT NULL).
Blocked: test thông báo + quyền theo công ty thật cần `permission:sync` local + quyền ERP `Lập phiếu kiểm kê kho theo vị trí` (DB local chưa có quyền này).

## Phase 2 — FE (`pages/finance/position-inventories`)
- [x] F1. Danh sách `index.vue` (4 mixin, SmartFilterPanel floating, cột, sort, Cấu hình cột, Xuất Excel ExcelJS, In danh sách, popup Lịch sử)
- [x] F2. `PositionInventoryForm.vue` (4 card, cây tick 4 cấp, Lấy vị trí, bảng chi tiết rowspan, Hội đồng, validate inline, unsaved, Lưu và tiếp tục)
- [x] F3. `create.vue` / `_id/edit.vue` / `_id/index.vue` (chi tiết + SystemInfoSection + nút theo cờ, 404)
- [x] F4. Menu `finance.js` `erpPath` → `link`
- [x] F5. Checklist skill erp-to-hrm-screen (grep tự kiểm) + compile

### Checkpoint — 2026-10-17 (Phase 2 FE)
Vừa hoàn thành: F1–F5. File: `pages/finance/position-inventories/` (index.vue, create.vue, _id/index.vue, _id/edit.vue,
components/PositionInventoryForm.vue, ScopePicker.vue, DetailTable.vue, row-actions.js, export-excel.js) + menu `finance.js`.
Bám màn: danh sách/row-actions/export ← warehouse-imports; form V2BaseFormCard + V2Footer #custom-actions + Lưu và tiếp tục
← prepick-cancels / buy-service-requests; letterhead Excel ← lookup/stock-companies; xuất 1 phiếu ← bill-incomes (downloadExcel).
Lịch sử dùng endpoint riêng: SystemInfoSection/CatalogHistoryModal `endpoint-base=finance/position-inventories`,
entity-type=id, entity-id='histories'. Kiểm: parse vue-template-compiler + babel OK; nuxt dev :3000 build chunk không lỗi; grep skill sạch.
Đang làm dở: —
Bước tiếp theo: V2 — user mở trình duyệt kiểm (chưa bấm thật: ô lọc phụ thuộc, cây tick, Lấy vị trí, Lưu/Gửi, 422 inline, In, Xuất, Lịch sử).
Blocked:

## Phase 3 — Kiểm chứng (Playwright, user yêu cầu 17/10)
- [x] V1. Test Playwright màn danh sách: load 1 request, sort 4 cột, phân trang, đổi số dòng, tìm nhanh, 10 ô lọc (khớp DB), nhớ bộ lọc, Cấu hình cột (khoá STT/Số phiếu/Hành động, lưu theo user), Xuất Excel (chọn cột), In danh sách, popup Lịch sử, menu "…"
- [x] V2. Test Thêm / Sửa / Chi tiết: validate đỏ cùng lúc + QLDA_001, cây tick 4 cấp, Lấy vị trí, hội đồng (trùng NV, tự điền chức vụ), Lưu / Lưu và gửi / Lưu và tiếp tục, Xóa (cây con sạch), nút theo trạng thái, sửa phiếu đã gửi → đá về chi tiết, 404 (id sai / phiếu kiểm kê / nháp người khác), In + Xuất Excel 1 phiếu, cảnh báo chưa lưu, link ERP Lập phiếu kiểm kê
- [x] V3. Đối chiếu dữ liệu ghi với phiếu ERP (111) từng bảng; thông báo thủ kho test trong transaction rồi rollback (cùng công ty → 1 thông báo, khác công ty → 0)
- [x] Fix L1: đổi số dòng/trang từ trang > 1 bắn 2 request trùng → `fetchData` bỏ request trùng URL đang chạy + chặn response cũ ghi đè (index.vue)
- [x] Fix L2: bảng Chi tiết — cột Lô vỡ 4 dòng, cột SL/Cộng bị cắt, tiêu đề không dính → max-height 600 + thead sticky + lô nowrap (DetailTable.vue)
- [x] Fix L3: tick 1 khoang làm mất vị trí tự do đã tick — b-form-checkbox "Chọn hết" vọng `change` khi prop đổi → bỏ sự kiện trùng trạng thái hiện tại (ScopePicker.vue)
- [x] Fix L4 (nghiệp vụ ERP): lưu kế hoạch phải sinh 1 dòng `position_inventory_item_product_detail_results` / lô (qty = SL lô, ĐVT cơ sở, real_qty 0) như ERP — thiếu thì phiếu kiểm kê ERP lập từ kế hoạch HRM không có dòng nhập kết quả (PositionInventoryWriteService::syncItems)
- [x] Fix L5: bản In danh sách cột "Người lập" → "Người tạo" (PositionInventoryPrintService)
- [x] Fix L6: cột Lô file Excel 1 phiếu 22 → 40 (PositionInventoryExport)
- [x] User chốt 17/10: bỏ trạng thái trong form + trên thanh tiêu đề; card đổi sang khuôn chi tiết Phiếu nhập kho (`.card` + `.section-header`, 3 cột); "Lưu và gửi" KHÔNG popup xác nhận (như ERP `submit(3)/submit(1)`)
- [x] Dọn dữ liệu test theo id (117, 118 + log) — về đúng baseline

### Checkpoint — 2026-10-17 (Playwright)
Vừa hoàn thành: test Playwright toàn màn + 6 fix + 3 chỉnh theo user. Dữ liệu test đã dọn.
Đang làm dở: —
Bước tiếp theo: user xem lại trên trình duyệt; còn mở: lịch sử chưa ghi thay đổi PHẠM VI (vị trí tick không có tồn); khối Lịch sử chi tiết chỉ nạp khi bấm mở (chưa hiện badge số mốc sẵn); chưa test bằng tài khoản không quyền trên trình duyệt (đã test qua API ở B8).
Blocked: DB local thiếu quyền ERP `Lập phiếu kiểm kê kho theo vị trí` (id 471 seeder ERP) → local không ai nhận thông báo; quyền HRM mới chưa `permission:sync` thật.

## Phase 4 — E2E (user yêu cầu 17/10: dựng bộ e2e, tài khoản DNS Admin)
- [x] E1. Dựng `HRM/e2e/` theo skill playwright-setup (Node 20, @playwright/test local, storageState, POM, utils/select2)
- [x] E2. Page Object `PositionInventoryPage` + spec `tests/finance/position-inventory.spec.ts` (danh sách / lọc / sort / phân trang / tạo / sửa / gửi / xóa / lưu và tiếp tục / 404 / in / xuất / lịch sử / chưa lưu), tự dọn dữ liệu theo id
- [ ] E3. Chạy `npx playwright test --list` + chạy thật, sửa tới khi xanh; dọn dữ liệu test về baseline

### Checkpoint — 2026-10-17 (E2E — user bảo DỪNG)
Vừa hoàn thành: dựng `HRM/e2e/` (Node 24 local, token JWT DNS Admin trong `.env`, POM `pages/PositionInventoryPage.ts`,
spec `tests/finance/position-inventory.spec.ts` 22 ca). Lượt chạy đủ gần nhất: 20/22 xanh; 2 ca đỏ do test (nút ẩn trong menu "…",
chờ filter-options cố định 2,5s) → đã sửa, chạy riêng A2/A7/B1 xanh; A6 đỏ do regex `house_id` khớp nhầm `warehouse_id` → đã sửa regex.
Đang làm dở: lượt chạy lại toàn bộ (sau khi sửa regex) bị DỪNG theo yêu cầu user — chưa có kết quả xanh 22/22.
Bước tiếp theo: chạy `cd e2e && npx playwright test` (Node 24) xác nhận 22/22; xem vì sao afterAll không dọn phiếu 119 ở lượt 2 (đã dọn tay).
Blocked: —
Dữ liệu: đã dọn tay phiếu 119 + log 119/120 → về baseline (75 phiếu, 15 kế hoạch, catalog_histories max 983).

## Phase 5 — Fix sau bàn giao (19/10)
- [x] Fix L7: bản In danh sách — khối "Ngày… / Người lập" ra GIỮA trang. Mẫu ERP 284 (cả 285 của màn Kiểm kê theo vị trí) dùng bảng ký `class="block no-border"` 4 ô → CSS §3b chia đều 4 cột. Dựng lại bảng ký theo khuôn màn trước (mẫu 387/471: 3 cột, không `block`, ô ký 243px sát mép phải) — trait `Finance/Services/Concerns/AlignsListSignatureRight` dùng cho PositionInventoryPrintService + PositionInventoryResultPrintService
- [x] Fix #11770 (bộ lọc danh sách): (1) Công ty → khối chuẩn `V2BaseCompanyDepartmentFilter` (Công ty + Phòng ban, công tắc 🔒 xem cả công ty đã khoá) + BE lọc `department_id`; (2) Người tạo = toàn bộ nhân viên (`$store.state.employeeOptions`), không chỉ người đã tạo phiếu; (3) cột Ngày kiểm kê mặc định hiện icon sort trung tính (sort_field rỗng, BE vẫn mặc định created_at giảm dần)

### Checkpoint — 2026-10-19 (#11770)
Vừa hoàn thành: bộ lọc danh sách — khối chuẩn Công ty – Phòng ban (`V2BaseCompanyDepartmentFilter`, có công tắc 🔒 xem đơn vị đã khoá; `is_all_company` lấy cờ BE, `is_company` theo quyền "Xem kế hoạch kiểm kê theo vị trí theo công ty"), BE lọc `department_id` trong phạm vi; Người tạo = `$store.state.employeeOptions`; bỏ `creators`/`companies` + `employeeOptions()` thừa ở BE; sort mặc định rỗng → icon trung tính. e2e A1/A6 sửa kỳ vọng. Kiểm: parse vue + php -l; tinker lọc phòng ban 71 → 5 = DB 5.
Đang làm dở: —
Bước tiếp theo: user mở trình duyệt kiểm (chưa bấm thật trên UI).
Blocked:
- [x] Fix #11771 (cột danh sách): Ngày kiểm kê kèm giờ (`created_at` → `d/m/Y H:i`); thêm cột Ngày cập nhật (`updated_at_full`) + Người cập nhật (`updater_name`, join `updated_by`) ở danh sách + Xuất Excel. Bản In danh sách giữ nguyên mẫu ERP (đã có giờ ở Ngày kiểm kê)

### Checkpoint — 2026-10-19 (#11771)
Vừa hoàn thành: #11771 — tinker listRows ra đúng giờ + người cập nhật (TPE-KHKKVT-00138: 19/10/2026 11:33 / 11:57 / DNS Admin); parse vue + js + php -l OK.
Đang làm dở: —
Bước tiếp theo: user mở trình duyệt kiểm #11770 + #11771.
Blocked:
- [x] Fix #11772 (màn Tạo): (2) dấu * cho Ngày kiểm kê (4 cột Nhà/Dãy/Khoang/Vị trí đã có ở commit 88e64a7e5, dev chưa deploy); (3) "Chọn hết" riêng từng nhóm ở ScopePicker như ERP; (4) dấu × xoá nhanh ô tìm của 4 cột; (5) bảng Chi tiết hở giữa 2 tầng tiêu đề khi cuộn → `border-collapse: separate` (DetailTable — dùng chung màn Phiếu kiểm kê); (6) nút "Thêm dòng" lên ngang tiêu đề khối Hội đồng kiểm kê
- [x] #11772 (1) "Cắt bớt khoảng trắng" — chỉ dính bản build dev: CSS toàn cục thêm đè `.py-2` = 0.75rem!important + `h6 {margin:10px 0}` → đầu khối 50px (local 37). Bỏ `py-2`, chốt `padding: 8px 10px` + `h6 {margin:0; line-height:1.5}` trong style scoped (PositionInventoryForm). Giả lập trên dev: 50 → 38px

### Checkpoint — 2026-10-19 (#11772)
Vừa hoàn thành: #11772 mục 2-6. Kiểm bằng e2e headless (kho HP - Hải Phòng): Chọn hết nhóm Tầng 1 tick đúng 1 dãy, × xoá ô tìm về rỗng, Lấy vị trí rồi cuộn trong khung bảng → 2 tầng tiêu đề liền, Thêm dòng nằm ở header. File probe đã xoá.
Đang làm dở: mục 1 (khoảng trắng) — chưa rõ chỗ.
Bước tiếp theo: user xác nhận mục 1; deploy dev để tester thấy dấu * 4 cột.
Blocked:

### Checkpoint — 2026-10-19 (#11772 mục 1)
Vừa hoàn thành: #11772 đủ 6 mục. Mục 1 đo thật trên dev-hrm (headless, chép profile Playwright MCP) + giả lập rule mới → 38px.
Đang làm dở: —
Bước tiếp theo: deploy dev cho tester kiểm #11770–#11772; màn Phiếu kiểm kê theo vị trí (warehouse/position-inventory-results) có thể dính cùng lỗi đầu khối nếu dùng `py-2` + h6.
Blocked:

## Phase 6 — Fix #11773 (Xem chi tiết, 20/10)
- [x] (1) In: cột Công ty 6% → mã liền `DTTDETEK` tràn đè cột Lô → Công ty 10% (Tên hàng 24 → 21%) + ô in `overflow-wrap: anywhere` (PositionInventoryPrintService::detailTable, Excel không đổi)
- [x] (2) Tag trạng thái cạnh tiêu đề màn chi tiết (`buildStatusTitle`, như Phiếu nhập kho) — thay quyết định 17/10; trong form vẫn không hiện trạng thái
- [x] (3) Bảng Chi tiết hở đầu tiêu đề khi cuộn — đo trên dev: bản dev CHƯA có fix #11772 (`border-collapse: separate`), chữ lọt qua dải viền 1px của bảng. Không sửa thêm, chờ deploy
- [x] (4) Lịch sử: bỏ khoá `details_rows` (từng lô) ở kế hoạch → 4 khoá phạm vi `house_rows/row_rows/space_rows/position_rows` (Nhà / Dãy / Khoang / Vị trí, `__brief`), Kho giữ `warehouse_id`. Log cũ giữ nhãn cũ
- [x] (5) Popup lịch sử: dải 3px trên bộ lọc dính lộ chữ (sticky `top:-5px` không bù padding 0.5rem của `.v2-modal-body`) → `.si-borderless .si-filter-sticky { top: -0.5rem }` — component DÙNG CHUNG `SystemInfoSection.vue`, user duyệt 20/10 → đã sửa (chỉ áp chế độ popup `si-borderless`)

### Checkpoint — 2026-10-20 (#11773)
Vừa hoàn thành: mục 1, 2, 4 (php -l + tinker: bản in 11 cột 100%, log đổi phạm vi rollback ra đúng Khoang/Vị trí, không đổi → 0 log); mục 3 xác nhận là #11772 chưa deploy.
Đang làm dở: —
Bước tiếp theo: deploy dev (kèm #11772) cho tester kiểm #11773; mục 5 đo trên dev bằng CSS tiêm: hở 3px → 0.
Blocked:

## Phase 7 — Vị trí nút "Lấy vị trí" (21/10)
- [x] Chuyển nút "Lấy vị trí" từ cuối khối lên góc phải tiêu đề khối "Phạm vi kiểm kê" (slot `#actions` của V2BaseFormSection) — PositionInventoryForm.vue
