# STATUS.md — Phần GỘP DATABASE (nhánh `gop_db`)

> File này chỉ theo dõi các feature làm trên nhánh `gop_db` (hoặc nhánh checkout ra từ `gop_db`).
> Feature trên nhánh khác → ghi ở `.plans/STATUS.md`.

## ⚠️ Nền tảng — đọc TRƯỚC khi làm việc trên nhánh `gop_db`

**`.plans/gop-db/design.md`** — nhánh `gop_db` (cả 2 repo) gộp DB ERP + HRM thành DB duy nhất `local_hrm_erp`.
Ảnh hưởng tới MỌI feature làm trên nhánh này: bảng trùng tên ưu tiên bản ERP (bản HRM đổi tên `hrm_*`, 24 bảng),
`roles`/`permissions`/`files`/`groups` là của **ERP** — dữ liệu HRM nằm ở `hrm_*`;
riêng **`employees` + `employee_infos` đã gộp chung từ 2026-08-03** → `auth()->user()->id` là id nhân viên
duy nhất, `hrm_employees` là bảng cũ bỏ đi (xem mục 0b của design.md);
`mysql2` vẫn trỏ DB ERP CŨ (nguồn bug id lệch); kèm 7 gotcha bắt buộc biết khi port màn ERP → HRM.
Việc gộp DB **không có migration trong repo** → không tái tạo được từ code, phải xin dump.

**Quy tắc bắt buộc (chi tiết ở `CLAUDE.md` mục "Phần GỘP DATABASE"):**
- Nhận biết bằng **nhánh git đang đứng**, không đoán theo tên feature: đang ở `gop_db` hoặc nhánh checkout ra từ `gop_db` → áp dụng quy tắc này
- Tài liệu: feature làm trên nhánh đó nằm trong **`.plans/gop-db/[feature]/`**, spec chi tiết ở `docs/superpowers/specs/gop-db/`
- Code: chỉ làm **trên nhánh `gop_db`** hoặc nhánh **checkout ra từ `gop_db`**, merge trả về `gop_db`
- KHÔNG dùng `mysql2` / `DB_CONNECTION_SECOND` cho tính năng mới

## Tài liệu TC + HDSD theo form mẫu của team (2026-08-13)

Sinh lại **testcase** theo form mẫu chuẩn (17 cột, 2 khối summary DNS/TP) và **HDSD Word**
cho **7 màn chuyển phân hệ của @junfoke** — tổng **623 test case** và **7 file HDSD**.
Ảnh HDSD chụp thật trên cổng dev `hrm-crm.eteksofts.com` (22 ảnh, chỉ để local).

| Màn hình | TC | P0 | HDSD |
| --- | --- | --- | --- |
| Danh mục tiền tệ | 117 | 49% | 17 trang |
| Danh mục tài khoản | 128 | 66% | 16 trang |
| Danh mục loại tài khoản | 104 | 61% | 16 trang |
| Cấp dịch vụ bảo dưỡng | 75 | 56% | 11 trang |
| Danh mục ghi chú kiểm tra bảo dưỡng | 75 | 55% | 11 trang |
| Danh mục serial thiết bị làm dịch vụ | 67 | 63% | 11 trang |
| Cập nhật nhanh giá dịch vụ | 57 | 63% | 11 trang |

Đóng gói thêm 2 engine dùng chung vào skill (trước đây mỗi feature phải nhân bản ~1.300 dòng):
`.claude/skills/testcase-documenter/assets/tc_engine.py` và
`.claude/skills/hdsd-documenter/assets/hdsd_engine.py`.
Generator của từng màn nằm cùng thư mục tài liệu (`gen_testcase*.py`, `gen_hdsd*.py`).

Đã xóa 2 file `testcase.xlsx` bản cũ (format 15 cột, gộp nhiều màn) ở `finance-account-catalog` và
`customer-care-maintenance-catalogs` — user chốt 2026-08-13, thay bằng file tách theo từng màn.

## Tài liệu SRS + Testcase (2026-08-07)

Đã sinh `srs.html` + `srs.docx` + `testcase.xlsx` cho **6 màn nghiệp vụ của @junfoke**
(tổng 438 test case, P0 54-62%).
Bám code thật: validation lấy từ Request class, schema từ Entity, API từ Routes, business rule từ Service.

| Feature | TC | Feature | TC |
| --- | --- | --- | --- |
| finance-account-catalog | 98 | customer-care-cost-catalog | 82 |
| finance-currency-catalog | 68 | customer-care-serial-catalog | 58 |
| customer-care-maintenance-catalogs | 74 | customer-care-service-price-config | 58 |

**Chưa sinh:** `bank-account-catalog` và `customer-care-services-catalog` (của @khoipv — chủ feature tự làm);
nhóm hạ tầng/refactor (tach-phan-he-erp-hrm, bo-sung-menu-phan-he, chuyen-code-phan-he,
customer-cut-mysql2, banks-cut-mysql2) — không phải màn nghiệp vụ.

⚠️ **2 việc phát hiện khi soát code để viết tài liệu:**

1. `PermissionsTableSeeder` khai TRÙNG quyền tiền tệ: id 1115/1116 và 1117/1118 cùng `name` cùng guard `api`
   → chạy seeder trên DB sạch sẽ nổ lỗi trùng khóa. Cần bỏ 1 cặp.
2. `bank-account-catalog` (@khoipv) có design.md + plan.md, code đã xong nhưng **chưa có mục trong STATUS.md này**
   → nhờ @khoipv bổ sung.

## Đang làm

- update-style-bao-cao-cu (feature lớn, mỗi báo cáo 1 folder con) → @namdangit → .plans/gop-db/update-style-bao-cao-cu/design.md
  Khuôn: skill mới `HRM/.claude/skills/report-styles` (04/10, mẫu = báo cáo tổng hợp CSKH tiềm năng; chưa commit repo hrm-claude-config).
  Báo cáo 1 — meeting-by-projects: **CODE XONG 05/10 (SDD 10 task, review từng task), CHƯA push/merge.** Nhánh
  `gop_db-update-style-meeting-by-projects` (worktree `websites/wt-update-style-mbp`): api 85a1c59d7..c66df46e7 (11 commit),
  client a6ad678d0..7e02f5b74 (3 commit). PHPUnit `tests/Feature/MeetingByProjects` 28/28. Không migration/seeder/quyền mới.
  Nới `Meeting::canView` cho 1060/1061. E2E spec `e2e/tests/assign/meeting-by-projects{.api,}.spec.ts` ĐÃ VIẾT, CHƯA CHẠY.
  Review tổng xong + sửa (api e5a334044, PHPUnit 23/23). Sổ quyết định: `meeting-by-projects/sdd-ledger.md`.
  05/10: đã nới canView khớp phạm vi báo cáo · e2e API 8/8 + UI 7/7 passed · ĐÃ PUSH nhánh 2 repo (api c66df46e7, client 7e02f5b74).
  ĐÃ MERGE gop_db 05/10 (api 8de764f79, client 2f04d1dfb).
  Server worktree: api 8018 · client 3018.
  Báo cáo 2 — meeting-by-employees: **ĐÃ MERGE gop_db 05/10 (api 9696baa26, client 6c0b509de).** Nhánh
  `gop_db-update-style-meeting-by-employees` (worktree `websites/wt-update-style-mbe`): api 8de764f79..5b7934f3e, client 2f04d1dfb..b442bc862.
  PHPUnit `tests/Feature/MeetingByEmployees` 40/40 + liên quan 97/97. Không migration/seeder/quyền mới (giữ 1057/1058/1059). Nới canView theo
  phạm vi báo cáo. E2E `e2e/tests/assign/meeting-by-employees{.api,}.spec.ts` ĐÃ VIẾT, CHƯA CHẠY. Sổ: `meeting-by-employees/sdd-ledger.md`.
  Bổ sung 05/10: lọc Trạng thái + popup theo loại + popup NV tham gia — ĐÃ MERGE gop_db (api 60aa9bfa0, client 81b715269).
  Server worktree: api 8019 · client 3019.
  ### Checkpoint — 2026-10-05 (wrap up, báo cáo 2)
  Vừa hoàn thành: báo cáo 2 meeting-by-employees + bổ sung (lọc trạng thái, popup loại, popup NV tham gia) — ĐÃ MERGE + PUSH gop_db.
  Đang làm dở: không.
  Bước tiếp theo: chạy e2e meeting-by-employees khi user yêu cầu; kiểm staging (logo, tài khoản 1058, cột Chốt lịch); chọn báo cáo cũ thứ 3.
  Ngoài luồng (chưa vá): q báo cáo 1 không escape %/_; Excel người tham gia dùng chung bị cột SĐT đè cột Đơn vị.
  Blocked: 
  ### Checkpoint — 2026-10-05 (wrap up)
  Vừa hoàn thành: báo cáo meeting-by-projects code xong + review tổng (xem checkpoint cuối `meeting-by-projects/plan.md`).
  Đang làm dở: không. Bước tiếp theo: chờ lệnh merge gop_db. Blocked: chờ user.

- quan-ly-hang-hoa / **Phase 2d cây catalog** (Chương · Mục · Tiểu mục) → @namdangit → .plans/gop-db/quan-ly-hang-hoa/chuyen-cay-catalog/plan.md
  Trạng thái: **CODE XONG (04/10/2026) — ĐÃ PUSH nhánh `origin/feat/p2d-cay-catalog` (04/10, cả 2 repo), ⛔ KHÔNG merge vào gop_db (nhánh production — user chốt 04/10).** Nhánh `feat/p2d-cay-catalog` (từ gop_db 27f222a83 / 6e31e81ae)
  ở thư mục chính cả 2 repo; api 7 commit, client 3 commit (gồm 1 lượt sửa sau review cuối: N+1 is_can_lock, trùng tên khi thiếu lĩnh vực, khoá ô Trạng thái, báo lỗi ô lọc). PHPUnit `BusinessCatalogTreeTest` 12/12 +
  `ProductClassificationCatalogTest` 11/11; Playwright MCP đo đủ (bảng ở plan.md "Nhật ký kiểm"); e2e spec
  `e2e/tests/master-data/business-catalog-tree.api.spec.ts` **6/6 passed** (04/10, --project=api --no-deps --workers=1, 41s, dọn sạch).
  🔑 Migration `chapters`: + `internal_business_scope_id` (FK), `scope_id` thành nullable — ĐÃ chạy vào DB local `hrm_erp`.
  🔑 Quyền **1670–1675** (KHÔNG phải 1657–1662: 1660/1661 đã bị nhánh `gop_db-bao-cao-nhu-cau-dich-vu` seed vào DB dùng chung).
  6 quyền chỉ INSERT thẳng + gán role 18 — **KHÔNG chạy cả PermissionsTableSeeder** (nó xoá 1660/1661 của nhánh kia).
  ⚠️ 2 nhánh này phải kiểm `uniq -d` id quyền khi merge vào gop_db.
  ### Checkpoint — 2026-10-04 (wrap up lần 2)
  Vừa hoàn thành: 2-A (`15610ea2a`) + 2-B (api `40d3e9028`, client `e9d46129b`) đã vào nhánh chung `feat/chuyen-doi-hang-hoa`; 2-C chốt xong, 2-C3 Catalog code xong (chưa commit).
  Đang làm dở: commit 2-C3 chờ user.
  Bước tiếp theo: commit + merge 2-C3 vào nhánh chung → đợt 2-C1 Tạo + sửa.
  Blocked: 
  ### Checkpoint cũ — 2026-10-04 (wrap up)
  Vừa hoàn thành: Phase 2d xong + sửa 4 lỗi review cuối; e2e 6/6 passed.
  Đang làm dở: không.
  Bước tiếp theo: (1) ✅ đã push nhánh + đã merge vào NHÁNH CHUNG `feat/chuyen-doi-hang-hoa` (04/10) — ⛔ KHÔNG merge vào gop_db; (2) màn hàng hoá — đợt 2-A XONG 04/10 (`quan-ly-hang-hoa/2a-nen-csdl/plan.md`, api `15610ea2a` đã vào nhánh chung `feat/chuyen-doi-hang-hoa` + push; 3 migration đã chạy vào hrm_erp) → đợt 2-B XONG 04/10 (`quan-ly-hang-hoa/2b-doc/plan.md`; api `40d3e9028` · client `e9d46129b` đã vào nhánh chung + push; PHPUnit 8/8, e2e 4/4 + 6/6; quyền 1652/1653 đã INSERT vào hrm_erp) → đợt 2-C: chốt G1–G11 + B1–B5 (`quan-ly-hang-hoa/2c-ghi/chot.md`), plan 4 đợt con (`2c-ghi/plan.md`); **2-C3 Catalog CODE XONG 04/10** trên `feat/p2c3-catalog` (api+client), CHƯA commit, PHPUnit 6/6, e2e popup chưa chạy; quyền 1655 đã INSERT hrm_erp → tiếp: user duyệt commit/merge nhánh chung, rồi 2-C1, trước đây: chọn đợt đầu trong 5 đợt
  (`quan-ly-hang-hoa/SO-CHOT-VA-TON.md` mục 2c, đề xuất 2-A Nền CSDL) → khảo sát + plan → xin phép code.
  Blocked: 

- bao-cao-nhu-cau-dich-vu → @namdangit → .plans/gop-db/bao-cao-nhu-cau-dich-vu/plan.md
  Trạng thái: **ĐÃ MERGE + PUSH gop_db (04/10/2026): hrm-api b211161a1 · hrm-client 01a5d1b92 (lượt 2) — CHỜ DEPLOY.**
  PHPUnit `--filter ServiceDemand` 39/39 · E2E API 19/19 · UI 16 xanh + 1 skip (ca 15: DB local thiếu phiếu CCTT lập được báo giá).
  Tiêu đề bảng sticky trong vùng cuộn riêng (FE 9d09740d1); prepick-tracking không có sticky (không sửa).
  **Checklist deploy:** (1) `php artisan migrate` (2 migration Assign 2026_10_05_*) · (2) INSERT tay quyền 1660/1661 (KHÔNG chạy seeder — truncate) + cache:clear · (3) `assign:backfill-service-demands --dry-run` trên prod, kiểm số ≠ 0, rồi chạy thật · (4) cron `assign:close-expired-service-demands` 01:25 đã khai trong Kernel.
  Lượt 2 (04/10): nới Meeting::canView cho quyền 1660/1661 trên meeting có nhu cầu · cột Hợp đồng chỉ đếm HĐ có hiệu lực · prefix NCDV được duyệt. PHPUnit 45/45 · e2e API 21/21 · UI 16+1 skip. Worktree đã xoá.
  ### Checkpoint — 2026-10-04 (wrap up)
  Vừa hoàn thành: feature xong + merge/push gop_db (lượt 2). Đang làm dở: không.
  Bước tiếp theo: deploy theo checklist trên. Blocked: —
  Tài liệu: `.plans/gop-db/bao-cao-nhu-cau-dich-vu/` (design.md 27 quyết định · plan.md · mockup.html) + spec `docs/superpowers/specs/gop-db/2026-10-04-bao-cao-nhu-cau-dich-vu-design.md`.
- quan-ly-phong-hop → @namdangit → .plans/gop-db/quan-ly-phong-hop/plan.md
  📊 **30/09/2026:** file báo giá `quan-ly-phong-hop/bao-gia-quan-ly-phong-hop.xlsx` (3 cấp, 89.75 công,
  kèm 3 chức năng mới chưa spec: dọn phòng · đánh giá phòng · đổi phòng). Đã sửa marker xung đột lọt vào
  merge `8ad4b904d` ở `MeetingRoomModal.vue` → fix ở client `976e1eb32` (đã push). Chi tiết: checkpoint cuối plan.md.
  Trạng thái: **Phase 8 "Yêu cầu dịch vụ" — CODE DONE + ĐÃ ĐO TRÊN TRÌNH DUYỆT (23/09/2026), CHƯA
  COMMIT, còn nợ bộ e2e**.
  Phase 1→4 + đợt Task 65-86 code done (20/09/2026, đã push); Phase 7e (nút thẻ trạng thái vỡ chữ)
  xong 22/09 ở client `7bc8bcb1f`. Phase 5 (check-in QR + job nền + đặt lặp định kỳ) và Phase 6
  (báo cáo) chưa mở.

  **Phase 8 — Yêu cầu dịch vụ trên phiếu đặt phòng (trà, nước, hoa quả…)** — user chốt 11 quyết định
  ngày 23/09/2026, spec: `docs/superpowers/specs/gop-db/2026-09-23-yeu-cau-dich-vu-phong-hop-design.md`,
  tóm tắt ở cuối `design.md`. Gồm: danh mục mới `meeting_room_services` + màn `/meeting/room-services`;
  bảng con `meeting_room_booking_services` (món + số lượng + ghi chú, snapshot tên/đơn vị); 4 cột
  trạng thái dịch vụ trên phiếu (NULL = không kèm dịch vụ); 3 mốc thông báo `[DPH]`; cột + ô lọc ở
  `/meeting/bookings`. ⚠️ **Kéo theo đổi `meeting_rooms.manager_employee_id` (1 người) → bảng nối
  `meeting_room_managers` (nhiều người) + bắt buộc khai ≥ 1**, đụng 10 chỗ BE (lọc phạm vi xem phiếu,
  gate duyệt, người nhận thông báo, sort, import/export, lịch sử danh mục) và 4 chỗ FE. Không thêm
  quyền mới.

  **Đã làm xong trong ngày 23/09/2026** (toàn bộ ở working tree, CHƯA commit):
  khối A — phòng họp nhiều người phụ trách (bảng nối `meeting_room_managers`, backfill, drop cột cũ,
  sửa 12 chỗ BE/FE đọc cột cũ) · khối B — danh mục Dịch vụ phòng họp: **chỉ mới xong BE** (bảng + 10 route + `/options`), **màn FE
  `/meeting/room-services` CHƯA làm** ·
  khối C — yêu cầu dịch vụ trên phiếu (2 bảng, 2 endpoint xử lý có `lockForUpdate`, 4 mốc thông báo
  `[DPH]`, cột + ô lọc) · nhóm D — vá `V2BaseModal` thiếu `subtitleFullText`, gom nhóm nút footer
  popup về 8px, chuẩn hoá message validate, **bổ sung 53 mục tiếng Việt vào lang file dùng chung**.
  Kiểm: toàn bộ suite PHPUnit **231 tests/681 assertions** giữ đúng mức đỏ có sẵn (5E+2F);
  đo thật trên trình duyệt cả luồng tạo phiếu → xác nhận dịch vụ → ca 409 khi 2 người cùng bấm.
  ⚠️ **Còn nợ (chặn bàn giao)**: **màn FE danh mục Dịch vụ phòng họp (T128–T130)** — chưa có chỗ nào
  trên giao diện để thêm/sửa/khoá món, hiện phải seed hoặc sửa thẳng DB.
  ⚠️ **Còn nợ**: bộ e2e `meeting-room-service.{api.spec,spec}.ts` chưa viết (user chốt chạy sau);
  spec e2e cũ của `meeting/bookings` cần rà theo bố cục nút mới.
  ⚠️ **Đụng tài sản dùng chung**: `hrm-api/resources/lang/vi/validation.php` (+53 câu) và
  `hrm-client/locales/vi.json` (5 → 31 key) — ảnh hưởng toàn hệ thống, cần nêu khi review/PR.

  **Đợt 20/09/2026 (Task 65-86, xem checkpoint cuối `plan.md`)** — 22 task theo yêu cầu user:
  màn **Cấu hình phân hệ** `/meeting/settings` theo khuôn hub "Phê duyệt" (cấu hình giờ mở cửa,
  2 mốc nhắc nhận/trả phòng, cờ cho đặt ngoài giờ, lịch sử theo từng hub) + lệnh nền
  `meeting:send-booking-reminders`; **chọn phòng biết trống/bận**: API
  `GET meeting/rooms/availability` (trống · chờ duyệt · bận + gợi ý khung giờ trống gần nhất),
  chống tranh phòng khi 2 người đặt cùng lúc; **quy hết việc đặt phòng về form Đặt phòng** —
  form meeting và màn danh sách meeting chỉ còn nút "Đăng ký phòng" mở popup đó, gate bằng cờ
  `can_book_room` (chỉ người tạo hoặc người chủ trì); "Danh sách phòng họp" chuyển về nhóm
  **Danh mục**; form phòng họp **thêm nhanh tiện nghi** bằng popup lồng.
  ✅ **ĐÃ COMMIT + PUSH** (20/09/2026): `hrm-api` `296aeab93` + `0833f1a41`, `hrm-client` `1791c98ac`
  + `bee1c02d3` — cả 2 repo sạch, ngang `origin/gop_db`; Task 65-86 nằm trong 2 commit 20:15.
  ⚠️ **Bộ e2e đợt này CHƯA CHẠY** (user chốt chỉ chạy khi yêu cầu) và thư mục `HRM/e2e` **không nằm
  trong repo git nào** → spec sửa/bổ sung chỉ có trên máy, chưa theo commit nào.

  **Đợt review 1 (Phase 3.5, task 25-36 trong plan.md)** — 4 quyết định user chốt + 6 lỗi phát sinh:
  1. Bộ 4 quyền danh mục gộp còn **1 quyền "Khai báo phòng họp"** (id 1574; xoá 1575-1577).
  2. **Công ty nào tạo thì phòng thuộc công ty đó** — bỏ select Công ty ở form; sửa/khoá/mở khoá/xoá
     chỉ với phòng công ty mình (chặn ở BE, 403); danh sách vẫn xem mọi công ty + lọc theo công ty.
     DROP `department_id`/`part_id` khỏi `meeting_rooms` (để lại thì `BaseModel` tự điền theo NGƯỜI TẠO).
  3. **Lịch sử thay đổi cho 2 màn danh mục** — bảng chung `catalog_histories`, mục Lịch sử ở menu ⋮,
     khối Lịch sử thu gọn cuối popup Xem.
  4. Chuẩn hoá theo skill: chữ nút Khoá/Mở khoá, popup Xem (footer 1 nút + dòng mô tả bản ghi),
     khoảng cách ô `mb-2`, và **màn danh sách phòng họp theo `list-page`** (STT sticky, bộ cột mặc
     định 7 cột, popup Cấu hình cột, sort có whitelist BE, Người tạo chỉ hiện TÊN, bỏ giây ở cột ngày).

  Lỗi phát sinh đã sửa: component dùng chung `V2BaseRowActions` đóng menu ⋮ ngay khi vừa mở (scroll
  listener) — user duyệt sửa; e2e cấp quyền bằng SQL phải xoá cache spatie (24h) mới có tác dụng;
  2 ca e2e chờ sai mốc / đỏ theo đồng hồ.
  Quản lý phòng họp (phân hệ Meeting). Phase 1 = nền tảng + 2 màn danh mục: module BE mới `Modules/Meeting`,
  9 migration (6 bảng + `meetings.meeting_room_id` + 5 cột cấu hình `general_regulations` + FK/unique),
  2 bộ API (phòng họp, tiện nghi), 2 màn FE `/meeting/rooms` + `/meeting/room-amenities`, đăng ký menu,
  5 quyền mới (id 1574-1578).
  ✅ **ĐÃ MERGE VỀ `gop_db`** (19/09/2026): API `da27321d1`, Client `616df00b9` — worktree
  `hrm-worktrees/phong-hop-{api,client}` đã xoá, code nay nằm ở checkout chính. Chưa push.
  ⚠️ Khi merge phát hiện **trùng id quyền** (git không báo xung đột vì khác dòng): `gop_db` đã cấp
  1574-1585 cho "Danh mục hàng hóa" → quyền phòng họp đánh số lại **1586-1589**. Bài học: lấy id
  quyền NỐI TIẾP id lớn nhất ĐANG CÓ ngay trước khi commit, đừng lấy theo lần đọc trước đó.
  Test: `e2e/tests/meeting` — 14 ca API + 14 ca UI, xanh, đã chạy lại nhiều lần, không flaky.
  Đọc `.plans/gop-db/quan-ly-phong-hop/plan.md` mục "LƯU Ý KHI DEPLOY" trước khi đưa lên môi trường khác
  (kiểm mã trùng trước migration unique; migration có bước xoá dòng pivot mồ côi; cân nhắc trước khi chạy
  `PermissionsTableSeeder`). Nhật ký thực thi + mọi quyết định: `.plans/gop-db/quan-ly-phong-hop/.sdd/progress.md`.
  **Phase 2 (đặt phòng + duyệt) ĐÃ XONG**: bảng phiếu + luật chống trùng có khóa (mutex phòng, có test 2
  kết nối DB chứng minh), duyệt/từ chối/hủy + tự từ chối phiếu trùng, 5 loại thông báo `[DPH]`, màn
  `/meeting/bookings` + modal đặt phòng, 2 quyền mới (1579-1580).
  Test chốt 19/09/2026: chạy 1 lượt CẢ thư mục `e2e/tests/meeting` → **124 passed / 0 failed /
  0 "did not run"** (trước đợt này chạy cả thư mục chỉ ra 44 passed + 29 "did not run"),
  PHPUnit **39 tests / 80 assertions**, rác `E2E%` sau khi chạy = 0.
  ⚠️ Chạy e2e phải truyền `API_BASE=http://127.0.0.1:8001 BASE_URL=http://127.0.0.1:3001`
  (file `e2e/.env` trỏ cổng của checkout chính) + `--no-deps --workers=1`.
  Phase 4-6 (nối Meeting, check-in + job nền, báo cáo) chưa làm.
  Còn nợ: màn **Tiện nghi phòng họp** chưa rà theo `list-page` (thiếu STT, Người tạo/Ngày tạo,
  popup Cấu hình cột, sort) — chờ user quyết.

- quan-ly-hang-hoa (FOLDER LỚN) → @namdangit → .plans/gop-db/quan-ly-hang-hoa/design.md
  📊 **Bảng danh mục hàng hoá cho nghiệm thu (25/09/2026):**
  `quan-ly-hang-hoa/danh-sach-danh-muc-hang-hoa.xlsx` — 3 sheet: *Danh mục hàng hoá* (**31 dòng / 5
  nhóm**: 6 làm mới · 11 chuyển ERP · 6 danh mục Xe · 3 xe chưa mở · 5 sẽ bỏ, kèm bảng dữ liệu + số
  dòng thật, 11 danh mục Phase 1 đang quản **51.636 bản ghi**), *Lộ trình phần hàng hoá* (13 phase
  0→8 kèm trạng thái), *Ghi chú & bằng chứng* (quyền, e2e, đối chiếu dữ liệu, việc còn treo).
  📌 **Đầu mối quay lại: `.plans/gop-db/quan-ly-hang-hoa/SO-CHOT-VA-TON.md`** — gom quyết định
  đã chốt · việc đang chặn · việc để sau · bẫy đã trả giá.
  Trạng thái: **MỞ FOLDER 20/09/2026** — mới có design.md tổng quan, chưa mở phase code nào.
  Chuyển quản lý hàng hoá ERP → HRM + quy hoạch lại catalog phân loại. Phạm vi user chốt 20/09:
  **CHUYỂN 14 danh mục** (hàng hóa · hàng tạm · cập nhật nhanh · model · code đặt hàng · ĐVT ·
  thuộc tính · đơn vị thuộc tính · thương hiệu · hãng sản xuất · xuất xứ · file đính kèm · mã màu ·
  thuế suất) · **BỎ 5 danh mục** (4 màn nhóm "Quản lý catalog": lĩnh vực/chương/nhóm công việc/
  cụm công việc + Danh mục nhóm hàng hóa `groups` 893 dòng) · **GIỮ NGUYÊN ERP**: Danh mục hàng
  hóa gốc, cả nhóm "Hàng hóa có sẵn" (11 màn, bảng riêng `pi_*`) và "Đồng bộ hàng hoá" (5 màn).
  9 phase bám thứ tự user note (thêm **2b** + **2c** ngày 21/09): (0) 6 danh mục phân loại mới — XONG · (1) chuyển **11 danh mục
  liên quan** (model · code đặt hàng · ĐVT · thuộc tính · đơn vị thuộc tính · thương hiệu · hãng
  sản xuất · xuất xứ · file đính kèm · mã màu · thuế suất) · (2) **mockup mới rồi chuyển theo
  mockup — user chốt danh sách và tạo/sửa là MỘT việc**, mockup gồm đúng 2 màn: danh sách hàng hoá
  + tạo/sửa hàng hoá · **(2b) chuyển 4 danh mục Xe sang HRM** (Hãng xe 56 · phân loại xe 322 ·
  model xe 1.281 · đời xe 61) · **(2c) 5 danh mục Xe công ty / vận chuyển** (dòng xe · tải trọng ·
  biển số · lái xe ngoài · danh mục xe) · (3) phân quyền hàng hoá theo công ty · (4) popup tìm kiếm hàng hoá
  dùng chung · (5) gỡ 5 danh mục bỏ · (6) Danh mục hàng tạm (`tmp_products`) · (7) luồng Tính giá.
  Mỗi phase 1 folder con, chỉ tạo khi bắt đầu phase đó.
  ❓ **"Cập nhật nhanh hàng hóa" chưa chốt nằm ở phase nào** — chạy trên `products` nhưng không
  nằm trong 2 màn mockup của Phase 2. Cần user quyết trước khi mở Phase 2.
  ⚠️ `tax_rates` và `attributes` vừa nằm trong 14 danh mục cần chuyển, vừa đã bị Phase 0 tham chiếu
  (`product_types.vat_percent_tax_rate_id`, `product_type_attributes`) → Phase 1 phải giữ nguyên id.
  ⚠️ "Tính chất hàng hóa" bên ERP chưa từng là danh mục — là enum fix cứng ở `products.product_type`.
  Phase 0 (#11421 của @junfoke) đã chuyển vào làm folder con của folder lớn này.

- quan-ly-hang-hoa / **Phase 1** chuyen-danh-muc-lien-quan → @namdangit →
  .plans/gop-db/quan-ly-hang-hoa/chuyen-danh-muc-lien-quan/plan.md

- quan-ly-hang-hoa / **Phase 2b** chuyen-danh-muc-xe → @namdangit →
  .plans/gop-db/quan-ly-hang-hoa/chuyen-danh-muc-xe/plan.md
  Trạng thái: 🟢 **CODE XONG — 6/6 màn** (22/09 bổ sung Dòng xe 11 · Tải trọng xe 31 theo yêu cầu
  user), chờ nghiệm thu. e2e chung lên **119 ca (17 màn × 7)**, nhóm menu "Xe" 4 → 6 mục. Nhánh
  `feat/p1-danh-muc-hang-hoa` (cùng nhánh Phase 1 + Phase 2), 5 commit, hai repo sạch.
  4 màn: Hãng xe 56 · Loại xe 322 · Model xe 1.281 · Đời xe 61 — dùng CHUNG bảng ERP, không di trú.
  Quyền **1620–1627** (8 quyền, `group = 'Danh mục hàng hóa'`). Menu: phân hệ Danh mục chung,
  nhóm **"Xe"** 4 mục.
  🧪 **e2e: 111 ca API + 23 ca UI, tất cả xanh.** `product-catalog-common.api.spec.ts` lên **105 ca
  (15 màn × 7)** · `vehicle-catalog.api.spec.ts` **mới, 6 ca** (unique theo cha · mở khoá sinh trùng
  tên bị chặn · cặp Hãng/Loại xe lệch 422 · getAll bỏ bản ghi khoá) · `product-catalog-ui.spec.ts`
  thêm 5 ca cho 4 màn Xe. Chạy Node 20 + `--project=api|chromium --no-deps --workers=1`.
  📐 **Số đo:** chặn N+1 ở cột `is_can_delete` — Hãng xe 56 dòng **387 query → 2**, số query không
  đổi theo số dòng (10 hay 100 dòng đều 2–4); đối chiếu **236 dòng, 0 lệch** với phép đếm thật.
  Lọc dây chuyền đo từ DOM: Loại xe **320 → 27** option khi chọn Toyota (= đúng DB), đổi sang Honda
  ra **35 model** (= đúng DB).
  🔐 Gate quyền kiểm **cả 2 chiều**: có quyền 200, thu hồi + xoá cache spatie → **403** ở index /
  store / export, và nhóm menu "Xe" biến mất.
  🐞 **4 lỗi im lặng bắt được** (test xanh không thấy, chỉ lộ khi mở trình duyệt / gọi API thật):
  nhóm menu khai `children` thay `subItems` nên cả nhóm biến mất · id popup xác nhận số ít lệch
  `catalogSlug` số nhiều nên popup không mở · `resetKeys` không xoá giá trị cấp con nên request vẫn
  kèm id cũ · đặt việc xoá ở `watch` thì muộn 1 nhịp, bắn thừa 1 request sai.
  🔴 **PHÁT HIỆN LỖI Ở PHASE 1 — chưa sửa, chờ user quyết:** 11 màn bảng ERP của Phase 1 so
  `Number(status) === 2` trong `toggleLock()`, mà bảng ERP khoá bằng **0** ⇒ bấm "Mở khoá" gọi nhầm
  `/lock` và hiện toast "Khóa thành công" trong khi bản ghi vẫn khoá. 11 file × 4 dòng.
  Chi tiết + cách sửa ở mục "Việc bàn giao" trong `chuyen-danh-muc-xe/plan.md`.
  📌 Còn tồn: Import 4 màn (chờ chốt màn import Model xe của ERP) · chặn route sửa bên ERP + cho
  `VehicleLife::searchByFilter()`/`getForSelect()` lọc `status` (đợt "sửa ERP để không lỗi").
  Yêu cầu user: *"Chuyển toàn bộ danh mục phân loại xe, dòng xe, model xe,... sang HRM"*.
  Phạm vi lõi 4 màn, khuôn `BaseCatalog*` như Phase 1, quy mô ERP **801 dòng controller + 5 blade**:
  Hãng xe `vehicle_manufacts` 56 · phân loại xe `vehicle_brands` 322 · model xe `vehicle_models`
  1.281 · đời xe `vehicle_life` 61.
  ✅ **PHẠM VI ĐÃ CHỐT 21/09/2026** — user: *"Lấy đúng 4 màn lõi, phần còn lại tách phase riêng"*.
  5 màn còn lại của menu Xe (dòng xe 11 · tải trọng 31 · biển số 163 · lái xe ngoài 110 · danh mục
  xe 137) → **Phase 2c**. Nhờ đó câu "dòng xe là bảng nào" hết chặn: theo nhãn menu ERP nó là
  `vehicle_categories` — danh mục **xe vận chuyển** ("Xe tải thùng kín", "Xe cẩu", "Xe đầu kéo"),
  `products` không dùng ⇒ rơi vào 2c. Thứ menu gọi *"phân loại xe"* (`vehicle_brands` 322) mới là
  ô **"Loại xe"** trên form hàng hoá ⇒ nằm trong 4 màn lõi.
  ⚠️ **Dùng chung bảng ERP, KHÔNG di trú** — `vehicle_manufacts.id` đang bị 10 bảng trỏ tới, dữ liệu
  sống: `productables` 13.165 · `customer_has_vehicle_manufacts` 1.560 · `firm_contracts` 253 ·
  `wr_service_contracts` 104 · `vehicles` 137 · `product_vehicle_model_has_life` 48.736.
  🪤 **5 bẫy đã đo trước:** (1) `vehicle_brands` mang 3 tên gọi khác nhau (route "Thương hiệu xe" /
  menu "phân loại xe" / form hàng hoá "Loại xe") và **khác** `brands` đã port ở Phase 1 · (2) không
  áp được rule "tên unique toàn bảng" của Phase 0 — `vehicle_models` có **112 tên trùng**, nhưng
  trùng trong cùng cha chỉ **1 cặp** ⇒ unique theo cha + dọn 1 cặp bẩn · (3) `vehicle_life` **không
  có cột `status` lẫn `note`** ⇒ nền BaseCatalog phải nới, bỏ nút Khoá · (4) 3 bảng xe không có cột
  `code` ⇒ `hasCodeField()` false ở **cả Service lẫn Request** · (5) trạng thái 1/0 kiểu ERP.
  📌 Việc kèm: 4 màn × 1 cặp quyền Xem/Quản lý (⚠️ bên ERP 4 route group này **không có
  `checkPermission`** — siết quyền ở HRM là đổi hành vi, phải báo user) · màn import của Model xe
  giữ hay bỏ · đặt menu FE ở phân hệ nào.
  🔗 Không chặn Phase 2: tab 6 "Phân loại xe" chỉ ĐỌC 3 bảng này qua `GET /products/vehicle-options`
  (`cf5c489a9`), hai phase chạy độc lập được.

- quan-ly-hang-hoa / **Phase 2c** chuyen-danh-muc-xe-cong-ty → @namdangit → (chưa có folder)
  Trạng thái: ⬜ **TÁCH RA 21/09/2026 — chưa code, chưa tạo folder con.** Spec tạm ở
  `.plans/gop-db/quan-ly-hang-hoa/design.md` mục "Phase 2c".
  Phần còn lại của menu ERP **Xe**, user chốt tách riêng vì **không dính hàng hoá** — không màn nào
  của quản lý hàng hoá đọc 5 bảng này. Quy mô **1.026 dòng controller + 9 blade**:
  dòng xe `vehicle_categories` 11 · tải trọng `vehicle_payloads` 31 · biển số `license_plates` 163 ·
  lái xe ngoài `vehicle_drivers` 110 · **danh mục xe `vehicles` 137** (riêng màn này 314 dòng + 5 blade).
  ⚠️ **Thứ tự bắt buộc: 2c SAU 2b.** `vehicles` là màn tổng hợp, FK trỏ tới **6 danh mục**:
  `vehicle_manufact_id` + `vehicle_brand_id` + `vehicle_model_id` (⟵ Phase 2b) và `license_plate_id`
  + `vehicle_category_id` + `vehicle_payload_id` (⟵ trong 2c). Làm trước 2b là thiếu 3 ô chọn.
  ⚠️ **Danh mục thứ 6 nằm NGOÀI menu Xe:** `vehicles.fuel_id` → `fuels` (4 dòng, `fuel.index`, menu
  "Vận chuyển - Bốc xếp") — phải gom vào 2c, không thì màn Danh mục xe thiếu ô Nhiên liệu. Đây là
  màn **duy nhất** cả nhóm đã có gate quyền sẵn (`checkPermission:Quản lý loại nhiên liệu`).
  ⚠️ `vehicle_categories` bị **13 bảng `delivery_*` / `vehicles`** tham chiếu ⇒ dùng chung bảng ERP,
  không di trú, y như 2b.
  ❓ Chưa chốt: để trong folder lớn quản lý hàng hoá hay tách hẳn thành feature riêng
  (`.plans/gop-db/chuyen-danh-muc-xe-cong-ty/`) — về nội dung nó không thuộc quản lý hàng hoá.

- quan-ly-hang-hoa / **Phase 2** man-danh-muc-hang-hoa → @namdangit →
  .plans/gop-db/quan-ly-hang-hoa/man-danh-muc-hang-hoa/plan.md
  📌 **WRAP UP 02/10/2026 — VÒNG SỬA MOCKUP SAU CHỐT §36 XONG** (T114–T129, §36a–§36n). Mockup
  448 → **459 KB**, console 0 lỗi, hai repo không đụng. Tồn mới gom thành **nhóm F (9 câu)** trong
  `man-danh-muc-hang-hoa/ton-chot-truoc-code.md` — nặng nhất **F1/F2 tab Nhóm máy lưu Loại sản phẩm
  hay mã thiết bị** (đổi CSDL). Bước tiếp: user trả lời F + duyệt 11 câu tooltip → chốt tiếp B1…E.
  🔄 **VÒNG SỬA MOCKUP SAU CHỐT §36 (01/10/2026)** — form hàng hoá: card *Thông tin hàng hoá* lên
  trước *Phân loại*; *Trọng lượng* · *Kích thước* + card *Thông số cơ bản* sang đầu tab *Thông số kỹ
  thuật* (§36a); bỏ ô *Mã hàng hoá* + *Trạng thái* khỏi tab Thông tin chung (§36b); Công ty quản lý lên hàng 1, Định mức công lắp đặt sang tab Thông số kỹ thuật (§36c); tab Mua hàng bỏ % giảm giá thanh lý, SL tối thiểu nhập mua lên sau HS Code (§36d); bỏ checkbox thuế BVMT, ô hệ số luôn hiện + không bắt buộc (§36e); popup Xây dựng catalog: bỏ lọc/cột Công ty, nút mở/thu cây + từng lĩnh vực, thêm cột STT · Ảnh · Thông số cơ bản (§36f); icon ⓘ định nghĩa cho 5 ô nhóm Phân loại (§36g); tab Nhóm máy bỏ logic cũ — chọn 1 mã thiết bị ⇒ hiện 4 cấp phân loại (§36h, 4 hệ quả chờ chốt) + dòng giải thích "phụ kiện dùng cho toàn bộ hàng hoá thuộc 4 cấp" (§36i) + dòng chữ "Đang khai báo thiết bị có sử dụng Phụ tùng/phụ kiện: [Tên hàng]" (§36k → §36l); ⓘ cho toàn bộ trường tab Quản trị hàng hoá — 9 câu đề xuất chờ duyệt (§36m); ⓘ cho 2 tab chính (§36n). Chốt tồn tạm dừng ở B1 trong lúc sửa mockup.
  📌 **WRAP UP 01/10/2026 — CHỐT TỒN TRƯỚC CODE.** Danh sách tồn lưu thành
  `man-danh-muc-hang-hoa/ton-chot-truoc-code.md` + `.xlsx` (22 câu A–E + 6 xác nhận + 2 phụ).
  ✅ **Nhóm A (CSDL, 8 câu) chốt theo đề xuất** (design §35a): trạng thái theo công ty ở
  `product_company_coefficients` · lấy hàng = tham chiếu · hướng B NOT NULL cho giá + dữ liệu quản
  trị · tách giá vốn sang `product_company_units` · bảng nối `product_business_catalogs`.
  🟡 Đang ở **B1** (quyền xem 3 màn chỉ đọc) — user muốn làm rõ thêm. ⚠️ Nhánh đã có 4 quyền
  **1616–1619** theo mô hình 1 màn cũ, phải xử lý cùng nhóm B. Còn B2–B3 · C · D · E · câu phụ.
  📌 **WRAP UP 30/09/2026** — session chạy trọn **§33 13 vòng góp ý** rồi **chốt mockup (§34)**;
  spec kỹ thuật (CSDL · API · quyền · ràng buộc) đã bổ sung vào
  `docs/superpowers/specs/gop-db/2026-09-21-man-danh-muc-hang-hoa-design.md`.
  Hai repo **không có thay đổi nào** của đợt này (đúng §22).
  ✅ **MOCKUP PHASE 2 ĐÃ CHỐT — 30/09/2026 (§34).** Bản chốt `mockup-luong-xay-dung-hang-hoa.html`
  **448 KB: 11 màn + 13 popup** (8 mục menu · form hàng hoá 2 tầng tab · form yêu cầu/phiếu tính giá)
  và `mockup-bao-cao-hang-hoa.html` 69 KB — **console 0 lỗi cả hai**, 0 chỗ còn tên cấp cũ.
  Nghiệm thu đo thật: Kho dữ liệu **153** · Kho công ty **150** · Nhập thông tin **13** ·
  Đang kinh doanh **32** · Yêu cầu **4** · Phiếu **2**; 5 popup chính mở/đóng được.
  🚧 **Từ đây không sửa giao diện nữa** — muốn đổi thì mở vòng mới. Cổng chặn còn lại: **24 câu tồn**
  (5 nhóm A–E đã gom kèm đề xuất, **chưa chốt**) + 1 câu phụ: `mockup-hang-hoa.html` (3,2 MB, bản
  21/09 đã lỗi thời) **xoá hay giữ**.
  🔄 **ĐỔI TÊN 2 CẤP (30/09)** — **Nhóm công việc → Mục**, **Cụm công việc → Tiểu mục** trên toàn
  giao diện (nhãn, cột bảng, ô lọc, popup, toast, mục lục); **tên bảng `job_groups`/`job_clusters`
  giữ nguyên**. Cây nay đọc: *Lĩnh vực Công ty kinh doanh → Chương → Mục → Tiểu mục*.
  🔄 **VÒNG 13 (30/09)** — phần chọn catalog trong tab *Quản trị hàng hoá* chuyển sang **4 CỘT
  kiểu ERP** (bám `catalogs/groups/form.blade.php`): khảo sát thấy ERP lưu `classify` là **danh sách
  nhánh** ⇒ trùng đúng mô hình §33 nên bê nguyên được. Bổ sung thứ ERP thiếu: **ô tìm từng cột**,
  **số đang chọn**, **bảng nhánh đã gắn** (STT La Mã + nút gỡ). Bỏ tick cấp trên ⇒ gỡ nhánh thuộc nó
  kèm toast, không im lặng xoá.
  🐞 Đợt thay khối **nuốt mất 2 hàm dùng chung** `cumKey`/`duongNhanh` ⇒ cả trang trắng; và lần đo
  đầu tưởng code hỏng vì trình duyệt trả **bản cũ trong cache** (phải đổi CỔNG MỚI khi kiểm demo).
  🔄 **VÒNG 12 (29/09)** — panel **cây 4 cấp** trong popup Xây dựng catalog vẽ lại cho dễ đọc:
  phân cấp bằng **kiểu chữ** (cấp 1 chữ HOA xám dính đầu · cấp 2 đậm đen · cấp 3 thường xám ·
  cấp 4 số teal, cấp duy nhất chọn được) + **đường nối dọc 1px** + **số thứ tự `I. · 1. · 1.1 ·
  1.1.1`**; badge đếm **chỉ ở cấp 4**, cấp trên chỉ hiện số khi đang đóng.
  🔄 **VÒNG 11 (29/09)** — màn *Kho dữ liệu hàng hoá* thêm cột **Công ty đang kinh doanh** (chip
  xanh, 2 công ty đầu + `+N` rê chuột xem hết) — tách bạch *“hàng của ai”* (Công ty quản lý) với
  *“ai đang bán”*. Rót thêm dữ liệu demo để có mã 2–4 công ty cùng kinh doanh.
  🔄 **VÒNG 10 (29/09)** — form Yêu cầu tính giá nay **chọn hàng hoá bằng POPUP**: nút *Chọn hàng
  hoá* → popup (lọc thương hiệu / công ty · tick · *Chọn tất cả N kết quả lọc* · phân trang 20/50/100 ·
  **loại trừ mã đã có trong yêu cầu**); bảng trong phiếu chỉ còn hàng đã chọn, mỗi dòng có nút xoá.
  Dữ liệu demo rót **2 mã/thương hiệu** ⇒ 4 nhóm **4·3·3·3** (trước 9·8·5·11).
  🔄 **VÒNG 9 (29/09)** — phiếu **Yêu cầu tính giá**: thêm cột **STT**, dòng cha đánh **La Mã I–IV**,
  dòng con **1-2-3** lại từ đầu mỗi nhóm; dữ liệu demo cân lại còn **4 nhóm 9·8·5·11**; người tiếp
  nhận (và người đang đăng nhập) chuyển về **Phòng XNK**; **bỏ màn Phân công** khỏi demo (HRM đã có).
  🐞 Dữ liệu demo từng dồn vào 2 nhóm vì **thương hiệu và trạng thái cùng lấy `i % 10`** trong hàm
  sinh — phải cho lệch pha, nếu không nhìn bảng tưởng nghiệp vụ lệch.
  🔄 **VÒNG 8 (29/09)** — **Phân công phụ trách hãng sản xuất** (bảng `assign_employee_manufactures`):
  thêm màn *Phân công phụ trách hãng SX*; nút **Lập phiếu tính giá** nay **gate theo người được phân
  công** — không phải người đó thì ẩn hẳn nút, chỉ còn chữ *"Chờ <tên> lập phiếu"*; hãng chưa phân
  công thì báo *"Chưa phân công người phụ trách"*. Đổi người đi theo **Bàn giao công việc** sẵn có.
  ⚠️ Khi code: `assign_employee_manufactures` cần **UNIQUE (employee_id, manufacture_id)** + chặn
  một hãng có 2 người phụ trách; gate phải ở **BE**, FE chỉ ẩn nút.
  🔄 **VÒNG 7 (29/09) — Yêu cầu ↔ Phiếu tính giá thành 1 – n.** Mỗi **nhóm** (Thương hiệu – Hãng SX)
  trên yêu cầu có nút **Lập phiếu tính giá** riêng (bỏ nút ở cấp yêu cầu); phiếu mang `brand`, chỉ
  nạp hàng của nhóm, người lập = **người phụ trách nhóm**; màn danh sách yêu cầu bung nhóm và hiện
  `2/4 nhóm đã duyệt giá`; yêu cầu chỉ đóng khi **mọi nhóm** duyệt xong. Đo: 1 yêu cầu → **2 phiếu**
  (PTG-03180 Launch · PTG-03181 Bosch), hai người lập khác nhau.
  🐞 3 class nhóm khai lồng trong `tr.nhom-cha` ⇒ màn danh sách **mất sạch style** (badge dính tên
  hãng) — số liệu DOM vẫn đúng, chỉ nhìn ảnh mới thấy.
  🔄 **VÒNG 6 (29/09)** — **Yêu cầu tính giá gom nhóm**: bỏ 2 ô *Thương hiệu* / *Hãng sản xuất* ở
  form Phiếu tính giá; bảng hàng hoá của form Yêu cầu tính giá **tự gom cha–con** theo *Thương hiệu
  — Hãng sản xuất*, **dòng cha hiện người tiếp nhận** (`Tên - Mã phòng - Mã nhân viên`); tick cha =
  tick cả nhóm. Đo: 33 hàng → **4 nhóm**; chọn 2 thương hiệu khác nhau ra **một** yêu cầu duy nhất.
  🔴 Tồn mới: một yêu cầu nhiều nhóm thì **tách nhiều phiếu tính giá theo nhóm hay một phiếu chung?**
  ⇒ vòng chốt nay **27 câu**.
  🔄 **VÒNG 5 (29/09)** — bỏ **badge số** trên menu (`veDem` đổi sang `datDem` guard null) · menu
  *Kho hàng hoá Công ty* → **Dữ liệu hàng hoá công ty** · thêm **bảng mục lục màn hình** (là gì ·
  dùng để làm gì · dữ liệu lấy vào) ở đầu màn Ghi chú, 8 mục menu + 5 màn/popup phụ · **bỏ ô lọc
  Đơn vị tính** ở mọi màn và 2 popup (cột ĐVT vẫn giữ).
  🔄 **VÒNG 4 (29/09) — XẾP LẠI MENU + TÁCH 2 MÀN KHO.** Menu 8 mục theo đúng danh sách user:
  Ghi chú · **Chính sách giá bán nội bộ** · **Kho dữ liệu hàng hoá** (MỚI, toàn bộ hàng hoá MỌI công
  ty, có nút **Lấy về** + lấy hàng loạt) · **Kho hàng hoá Công ty** (màn kho cũ đổi tên) · **Hàng hoá
  nhập thông tin** · **Hàng đang kinh doanh** · Yêu cầu tính giá · Phiếu tính giá.
  ❌ **BỎ HẲN màn "Chờ tính giá"** (user: *"giờ đều phải qua phiếu tính giá"*) — gỡ nav, section,
  `veBang2`, `BO_LOC.l2`, `cotHien.l2`, nút *Tính giá*; nút **Lưu** ở form nay về *Kho hàng hoá Công ty*.
  ✅ 2 tồn của vòng 4 **đã có đáp án** (user chốt cùng ngày): **giữ cả hai** popup *Xem hàng hoá
  Công ty khác* lẫn màn Kho dữ liệu hàng hoá · nút **Tính giá** chuyển sang màn **Kho hàng hoá Công
  ty**, chỉ hiện ở 2 trạng thái *Chờ tính giá bán* / *Đang tính giá* (các trạng thái khác ẩn hẳn).
  ⇒ vòng chốt trước khi code vẫn là **26 câu**.
  🔄 **VÒNG 3 (29/09)** — popup **mặc định thu gọn** bộ lọc nâng cao (trạng thái mở của lần trước
  còn nguyên trên DOM), thêm nút **mở toàn màn hình** (1460×418 → 1512×773, cây 224→471px, footer
  vẫn ghim đáy), ô lọc toàn hệ thống nhỏ lại **36px → 32px**.
  🔄 **VÒNG 2 (29/09)** — user góp ý 13 việc, đã sửa hết: bộ lọc màn Kho về đúng khuôn
  `V2BaseSmartFilterPanel` (mặc định = tìm nhanh + 4 cấp catalog, phần còn lại vào *Tìm kiếm nâng
  cao*) · menu bỏ chữ "Công ty" · cột Catalog chỉ hiện **tên Cụm**, hover mới bung 4 cấp · mọi ô
  **không xuống dòng** · bỏ barcode dưới mã · bỏ icon hamburger trên topbar · popup thêm 4 cột,
  **trần 100 mã/lượt**, **phân trang 20/50/100**, click ô Mã/Tên là tick, **đổi thứ tự 2 tab** +
  dải "Đang xem cụm", **10 ô lọc nâng cao**. Kèm 2 việc bắt buộc: **sinh 140 mã demo** và
  **phân trang thật cho 4 lưới danh sách** — 13 dòng cũ không tái hiện nổi phân trang lẫn trần 100.
  🐞 Lỗi vòng 2: `dongBoThanhCuon()` chạy lúc màn còn **ẩn** ⇒ `scrollWidth = 0`, thanh cuộn trên đặt
  **0px** (kéo mà bảng không đi) — phải đo lại ngay khi màn hiện. Mockup 388 KB → **403 KB**.
  🟢 **CHECKPOINT 29/09/2026 — §33 XÂY DỰNG CATALOG KINH DOANH, mockup xong, chờ user duyệt.**
  Thêm **1 màn** *Kho dữ liệu hàng hoá Công ty* (tất cả hàng hoá công ty, **mọi trạng thái**, gồm cả
  hàng lấy về từ công ty khác) + **1 popup** *Xây dựng catalog kinh doanh* (cây 4 cấp có số đếm ·
  2 tab Thêm/Gỡ · **chọn tất cả N kết quả lọc** · **dán danh sách mã** · giỏ chờ `+N/−M` + Hoàn tác
  + Lưu một lần); sửa màn *Hàng hoá đang kinh doanh* (vào màn phải **đang kinh doanh + đã xếp
  catalog**, 4 ô lọc catalog lên đầu, dòng nhắc số hàng chưa xếp, **bỏ** nút xây dựng catalog) và
  form hàng hoá (4 ô select → **bảng danh sách nhánh**). Mockup 325 KB → **388 KB**, console 0 lỗi,
  **không đụng dòng source nào**.
  ⚠️ **§33 ĐẢO 2 điểm chốt ngày 28/09**: catalog của (hàng hoá × công ty) nay là **NHIỀU nhánh** và
  **bắt buộc đủ 4 cấp tới Cụm công việc**; chỗ lưu chuyển từ 4 cột trên `product_company_coefficients`
  sang **bảng nối** `product_id × company_id × job_cluster_id` (tên bảng chưa chốt).
  🐞 4 lỗi tự bắt được: ô tick không mang class `dinh` ⇒ **mọi cột dính mất toạ độ** · `nangCapSelect`
  bọc select nên `style="width"` khai trên `<select>` **mất tác dụng** · biến `catTam` **rò nhánh khai
  dở sang hàng hoá khác** · ô lọc khoá mất tên trường.
  🔴 **Vòng chốt trước khi code nay là 26 câu** (14 cũ + 4 của §29f + **8 mới của §33i**), nặng nhất:
  45.890 hàng đang kinh doanh **chưa có catalog** ⇒ bật điều kiện lọc ngay là màn danh mục trắng trơn;
  và "Chọn tất cả N kết quả lọc" phải có endpoint **gán theo BỘ LỌC**, không gửi 45.890 id.
  🟢 **WRAP UP 28/09/2026 — MOCKUP PHASE 2 ĐÃ ĐỦ 4 MẢNG, CHỜ USER DUYỆT.** Cả đợt **không đụng dòng
  source nào** ở `hrm-api` / `hrm-client` (đúng §22); mockup 269 KB → **325 KB**, console 0 lỗi.
  Gồm: **§29** phiếu tính giá cho hàng lấy từ công ty khác (4 màn + 2 popup, dựng lại đúng phiếu thật
  PTG-03178 ⇒ giá nhập kho **13,108,986** khớp từng đồng) · **§29g** gỡ tab *Giá bán* khỏi form ·
  **§30** cây 4 cấp lĩnh vực vào tab *Quản trị hàng hoá* (riêng theo công ty, tối thiểu 3 cấp) +
  form chia **2 tầng tab** · **§31** rà soát form ERP sửa **9 lỗi** · **§32** xếp lại nhóm *Phân loại*
  (hiển thị cha → con, nhập từ cấp con) và tab *Mua hàng* (3 khối).
  🍎 Giao diện theo phong cách Apple: tab cha **segmented control iOS** (thumb trượt), tab con
  **stepper**, **24 ô tick/ô chọn** vẽ lại.
  🔜 **Bước tiếp:** user duyệt → chốt **4 tồn §29f** (gate giá vốn liên công ty · yêu cầu tính giá có
  bước duyệt không · phiếu gom nhiều công ty quản lý · lưu vết chính sách lúc tính giá) → gộp với
  **14 tồn** ở sổ chốt thành **một vòng chốt duy nhất** rồi mới mở code.
  🟢 **CHECKPOINT 28/09/2026 — FORM HÀNG HOÁ CHIA 2 TẦNG TAB + CATALOG 4 CẤP (§30g).**
  **Tab CHA:** *Thông tin hàng hoá* (5 tab con: Thông tin chung · Thông số kỹ thuật · Mua hàng ·
  Phân loại xe · Nhóm máy) | *Quản trị hàng hoá* (khối **Dữ liệu quản trị** cũ + khối mới
  **Phân loại theo lĩnh vực kinh doanh** 4 cấp).
  🍎 **Hình thức chốt 28/09:** tab cha là **segmented control kiểu iOS** — track
  `rgba(118,118,128,.12)` bo 10px, **viên trắng TRƯỢT** bằng `transform` easing
  `cubic-bezier(.32,.72,0,1)` 340ms, bóng 3 lớp, nhấn lún `scale(.96)`, vạch phân cách mảnh, icon
  hộp / thanh trượt. Đo thật: thumb x=73 → **229 (giữa đường)** → 253, có trượt chứ không nhảy;
  thu cửa sổ 900px vẫn bám đúng mục. Tab con là **STEPPER** (vòng tròn số + đường nối, step đã qua mang **dấu ✓**,
  step đang mở nền primary `#1abc9c` + quầng sáng); **chấm đỏ trên tab cha** khi còn ô bắt buộc chưa
  khai, khai đủ là tắt ngay.
  🐞 **2 lỗi TRÙNG TÊN CLASS** (chỉ lộ khi chụp ảnh nhìn, số liệu DOM vẫn "đúng"): `.step` trùng
  `.step` của Sơ đồ luồng ⇒ mỗi bước bị **bọc khung card** + kéo rộng 250px → đổi `.fstep*`;
  `.loi` trùng `.loi{display:none}` của popup Import ⇒ **3 ô select biến mất** khi báo lỗi → đổi
  `.o-loi`. Bài học: file mockup đã 313 KB, **đặt class mới phải grep trước**.
  ✅ Đo bằng Playwright (console 0 lỗi): lọc dây chuyền **xoá sạch cấp dưới** + khoá ô cấp dưới ·
  lĩnh vực khoá hiện **🔒 Khác** · **riêng theo từng công ty** (cùng mã `TPE-CN-2T-4500`: TÂN PHÁT =
  *Dịch vụ ô tô…*, TÂN PHÁT SG = *Công nghiệp…*, đổi ô "Đang làm việc tại" là vẽ lại) · validate
  **tối thiểu 3 cấp** tô đỏ đúng 3 ô, Cụm công việc không bị tô · hàng công ty khác mở thẳng tab
  *Quản trị hàng hoá*, tab cha kia + 5 tab con **mờ**.
  ⚠️ Bẫy ghi lại: chỉ số tab con **không còn trùng `data-i`** (0·1·2·**4**·5) ⇒ chỗ khoá/mở tab phải
  đọc `data-i`; mỗi thanh tab một id riêng (`#tab-cha` · `#tab-chinh` · `#tab-dvt`).
  📄 Spec `man-danh-muc-hang-hoa/design.md` §30g · ảnh `anh-mockup/30-*.png`.

  🔍 **RÀ SOÁT FORM NHẬP THEO ERP 28/09 (§31)** — bóc **42 ô + 19 khối** của
  `products/form.blade.php` kèm **kiểu điều khiển thật**, đối chiếu với mockup. **Sửa 9 lỗi:**
  **Model** (input → **SELECT** `product_models` 39.796 dòng + nút [+], bắt buộc) · **Code đặt hàng**
  (→ SELECT `order_codes` 8.664) · **3 ô thuế NK/chống bán phá giá** (→ SELECT `tax_rates` + nút [+]) ·
  **Tính thuế BVMT** (ô chọn Có/Không tự bịa → **checkbox**, hệ số **khoá khi chưa tick**) ·
  **Đơn vị bảo hành** (bỏ "Giờ chạy máy" bịa → **Ngày/Tháng/Năm**) · **Phụ kiện tiêu chuẩn**
  (textarea → **CKEditor**, trả lời luôn tồn cũ ở §26) · tiêu đề khối *"sửa chữa – bảo hành"* →
  **"bảo dưỡng"**. Hover tab cha nay giống lúc active (viên trắng nhạt, đo thật).
  🐞 **Lỗi của chính đợt rà:** bản rà đầu kết luận "thiếu khối Đơn vị tính + Thông số cơ bản" và đã
  thêm 2 khối — **SAI**, mockup vốn có sẵn (đủ hơn: cột *Bắt buộc*/*In tem*, cột *Quy đổi*); script
  chỉ quét nhãn `v2-label` nên **không thấy trường nằm trong BẢNG**, lại còn chèn ra **ngoài
  `.tpane`** nên hiện ở cả tab Mua hàng và không bị khoá theo quyền. Đã gỡ sạch.
  📌 Bài học ghi §31b: rà form phải quét **cả `<th>`**, và **nhìn ảnh** — mọi số liệu DOM trước đó
  đều "đúng", chỉ ảnh mới lộ.

  🔄 **XẾP LẠI NHÓM PHÂN LOẠI + TAB MUA HÀNG 28/09 (§32).** Nhóm *Phân loại* chốt cuối:
  **HIỂN THỊ CHA → CON, NHẬP TỪ CẤP CON** — hàng 1 là *Tính chất hàng hoá · Nhóm chức năng · Nhóm
  sản phẩm* (**tự điền, chỉ đọc**), hàng 2 là **Loại sản phẩm** (select + nút [+], ô duy nhất phải
  chọn) + *Đặc tính sản phẩm* (không thuộc cây nên ở cuối). Đọc từ trái sang, trên xuống ra đúng
  đường dẫn cây; chọn Loại sản phẩm là 3 ô cha tự điền theo. (Trong ngày đã thử bản cascade cha→con 4 lần
  chọn rồi bỏ — giữ trong `<details>` của §32a.)
  ⚠️ **Ràng buộc để suy ngược đúng:** mỗi *Loại sản phẩm* phải thuộc **đúng một** *Nhóm sản phẩm*.
  Dữ liệu demo có **3/7 loại nằm ở 2 nhánh** nên đã tách lại (*Bình chứa khí nén · Phụ tùng lọc gió ·
  Thiết bị phụ trợ gara*) ⇒ 0/10 loại trùng nhánh. Khi làm thật: chặn ở khâu **khai danh mục Loại
  sản phẩm**, không phải ở form hàng hoá.
  Tab *Mua hàng* tách **3 khối đúng việc**: **Khai báo hải quan** (tên khai báo · HS Code) ·
  **Thuế** (4 ô thuế **đều SELECT + nút [+]**, % VAT bổ sung nút [+] và dấu `*`; checkbox BVMT +
  hệ số) · **Đặt hàng** mới (SL tối thiểu nhập mua · % giảm giá thanh lý — 2 ô này vốn bị xếp nhầm
  vào Hải quan / Thuế).
  🐞 **Lỗi bắt được:** `datVaiForm` quét mọi input/select của pane để mở/khoá theo quyền nên **xoá
  luôn trạng thái khoá riêng** — tạo mới thì 3 cấp dưới của cây mở hết thay vì chờ chọn cấp trên
  (đúng y lỗi đã gặp với ô *Hệ số thuế BVMT*). Sửa: đặt lại cả hai **sau** vòng phân quyền.
  🍎 **Ô tick / ô chọn kiểu Apple (§32d):** bỏ ô mặc định trình duyệt, vẽ lại **24 ô** (20 checkbox
  + 4 radio) — 18×18 bo 5px, viền `rgba(60,60,67,.30)`, tick rồi nền `#1abc9c` + **✓ trắng vẽ ra**
  bằng animation `.2s cubic-bezier(.32,.72,0,1)` (cùng nhịp với thumb segmented control); radio là
  chấm trắng 6px; nhấn lún `scale(.9)`, bàn phím có quầng sáng; ô khoá mà đang tick giữ nền teal
  nhạt để vẫn đọc được trạng thái. Đã kiểm **không phá công tắc `.sw`** của màn Chính sách giá.
  ⚠️ Bẫy khi đo: đọc màu **ngay sau khi tick** vẫn ra màu cũ vì `transition .18s` chưa chạy xong.

  📝 **SỬA SPEC 27/09/2026 — CÂY 4 CẤP LĨNH VỰC: KHÔNG BỎ NỮA (§30).** Đảo quyết định cũ ở mục B
  của `quan-ly-hang-hoa/design.md` (trước xếp cả 4 màn *Quản lý catalog* vào diện BỎ ở Phase 5):
  **bỏ MÀN Lĩnh vực** (`scopes` 14) → thay bằng **Danh mục lĩnh vực Công ty kinh doanh** của HRM
  (`internal_business_scopes` 8 dòng, màn `/assign/internal-business-scopes` **đã có sẵn**, quyền
  1177/1178) · **chuyển 3 danh mục còn lại sang HRM** (Chương 65 · Nhóm công việc 106 · Cụm công
  việc 2) → mở **Phase 2d** · **4 cấp đưa vào tab Dữ liệu quản trị theo công ty** của form hàng hoá.
  🔍 **Khảo sát đo được:** cây thật là `scopes → chapters → job_groups → job_clusters`;
  **cây KHÔNG gắn vào hàng hoá mà gắn vào NHÓM HÀNG HOÁ** — `product_group_classifies` **1.019
  dòng** sống, còn `product_classifies` (gắn thẳng hàng hoá) **tồn tại nhưng 0 dòng**; bộ lọc thật
  nằm ở `Product::searchByFilter` **4 chỗ**, đều đi vòng qua `products.group_id`.
  ⚠️ **`scopes` KHÔNG xoá được** — 1.058 tham chiếu sống ngoài nhánh hàng hoá (`industry_scopes` 424 ·
  `prospective_projects` 325 · `application_scopes` 249 · `solutions` 39 · `request_solutions` 21)
  ⇒ Phase 5 sửa lại thành "gỡ MÀN của `scopes` + `groups`, **giữ cả 2 bảng**".
  ✅ **User chốt tiếp 27/09: BỎ HẾT DỮ LIỆU CATALOG CŨ, LÀM MỚI HOÀN TOÀN** (§30d) — bỏ
  `product_group_classifies` **1.019** + dữ liệu 3 danh mục (**65 · 106 · 2**); đã soát: không phân
  hệ nào khác dùng (`pi_product_group_classifies` 0 dòng, `subject_lessons.chapter_id` 0 dòng và
  đào tạo có bảng riêng `subject_chapters`). ⇒ **tồn ánh xạ 14→8 tự mất**, 3 màn HRM khởi đầu rỗng.
  ⚠️ `scopes` (14) **vẫn giữ nguyên**, không nằm trong diện bỏ.
  🔴 **Thứ tự bắt buộc khi cắt dữ liệu cũ:** dựng bảng mới + 3 màn → khai dữ liệu xong → **rồi mới**
  chuyển 4 chỗ lọc của `Product::searchByFilter` và xoá bảng nối cũ. Làm ngược là **338 màn lọc theo
  lĩnh vực trả về 0 hàng hoá**.
  ✅ **27/09 chốt nốt 2 tồn cuối (§30f):** catalog 4 cấp **riêng theo từng công ty** (nằm trong tab
  *Dữ liệu quản trị*) · **tối thiểu 3 cấp** tới *Nhóm công việc*, *Cụm công việc* để trống được.
  ⇒ **§30 hết tồn**, đủ điều kiện dựng mockup 4 ô lọc dây chuyền.
  ✅ **ĐÍNH CHÍNH quan trọng:** con số *"`scopes` còn 1.058 tham chiếu sống"* ghi hôm trước là **SAI** —
  đếm bằng `JOIN … ON scope_id = scopes.id` trong khi **`scopes` (ERP) trùng dải id 1–8 với
  `hrm_scopes` (35 dòng) / `internal_business_scopes` (8)**. Đo lại bằng model: 8 bảng có dữ liệu
  (`application_industries` 781 · `industry_scopes` 424 · `prospective_projects` 325 …) **đều là bảng
  HRM `Modules/Assign`** trỏ `hrm_scopes`. ⇒ `scopes` chỉ có `chapters` + `product_group_classifies`
  dùng, **xoá sạch data an toàn** (user chốt 27/09).
  📋 **11 vấn đề phát sinh do bỏ data — đã note vào §30e + sổ chốt mục 5:** nặng nhất là
  `Common/SearchController` (popup hàng hoá dùng chung của **338 màn**) · `Product::searchByFilter`
  4 nhánh lọc · **129 chỗ / 15 file ERP** gọi `ProductGroupClassify` (Quotations · OrderRequests ·
  ProductApproves · GroupsImport…) · 4 view ô chọn phân loại · 4 màn ERP rỗng phải gỡ · **16 quyền
  `web` 100091–100106** · đồng bộ CRM còn sót trong `Scope.php`/`Chapter.php`.
  ⚠️ **KHÔNG xoá nhầm** `hrm_scopes` (35) và `internal_business_scopes` (8) — của phân hệ Giao việc.

  🟢 **CHECKPOINT 27/09/2026 — ĐÃ GỠ TAB "GIÁ BÁN" KHỎI FORM HÀNG HOÁ (§29g).** Form hàng hoá còn
  **đúng 6 tab thông tin**; toàn bộ việc tính giá đi bằng cặp chứng từ *Yêu cầu tính giá → Phiếu
  tính giá*. Gỡ kèm: footer vai tính giá · 4 hàm dựng tab giá · 3 hàm bước tính giá cũ · **vai
  `'gia'`** trong 3 mức quyền §26c-bis (nay còn `full` / `chiQuanTri`).
  🔗 **Nối lại 3 lối vào để không có nút chết:** nút *Tính giá* ở màn Chờ tính giá → mở **đúng phiếu
  đang dở**, chưa có thì mở phiếu mới từ yêu cầu đang chờ, không có yêu cầu thì toast nhắc · mục
  *Sửa giá* ở menu màn kinh doanh **bỏ hẳn** (thuộc Phase 8 Quản lý giá) · sơ đồ luồng bước 2 đổi
  thành *"Tính giá bán bằng chứng từ"*.
  📦 Dữ liệu demo bổ sung `YCTG-00309` · `YCTG-00310` · phiếu dở `PTG-03178` cho 2 mã **TÂN PHÁT tự
  tạo** đang ở *Chờ tính giá* / *Đang tính giá* — để thấy luồng chứng từ áp cho **cả hàng tự tạo**.
  ✅ Đo lại: form 6 tab · khoá theo công ty vẫn đúng (5/6 tab `khoa` khi mở hàng công ty khác) ·
  menu màn kinh doanh hết *Sửa giá* · **2/2 hàng ở màn Chờ tính giá truy được về chứng từ** · chạy
  lại trọn luồng (168,000,000 × 1,25 ⇒ **210,000,000** ⇒ duyệt ⇒ Đang kinh doanh) · console 0 lỗi.

  🟢 **CHECKPOINT 26/09/2026 — MOCKUP PHIẾU TÍNH GIÁ CHO HÀNG LẤY TỪ CÔNG TY KHÁC (§29): XONG,
  CHỜ USER DUYỆT.** Hai repo **không đụng dòng source nào** (đúng §22); mockup dựng vào
  `mockup-luong-xay-dung-hang-hoa.html` (269 KB → **309 KB**), xem ở cổng 8899 → menu trái
  *Yêu cầu tính giá* / *Phiếu tính giá*.
  🔑 **5 đáp án user chốt:** **MỌI hàng đều qua chứng từ tính giá** (⇒ tab *Giá bán* trong form hàng
  hoá sẽ bị gỡ, và đây cũng là lời đáp cho **tồn 26g-1** về việc trùng luồng hỏi giá của ERP) · ô giá
  mua **để trống, người tính giá tự nhập** · hiện **cả 2 tỷ lệ** Nhập khẩu / Tồn kho, không chọn nguồn ·
  khối tham khảo nêu cách tính + % · **giá vốn công ty quản lý CHỈ hiện khi cách tính theo giá vốn**,
  **giá bán luôn hiện** · **giữ nguyên** ngoại tệ · tỉ giá · thuế NK · tab Chi phí của ERP.
  🧩 **Đã dựng:** 4 màn (Yêu cầu tính giá + form · Phiếu tính giá + form 3 tab *Hàng hoá / Chi phí /
  Tính giá* đúng khuôn ERP) · 2 popup (**Tạm tính giá mua từ Công ty quản lý** · Chọn yêu cầu tính giá) ·
  2 mục menu trái · cột **Chính sách giá nội bộ** + nút **Tạm tính** theo từng hàng hoá; hãng chưa khai
  chính sách ⇒ badge cam *Chưa cấu hình*, **vẫn lập phiếu được**.
  🧮 **Khảo sát ERP + công thức đo trên dữ liệu thật (8/8 dòng khớp):** `Giá nhập kho = Thành tiền sau
  thuế + Tổng chi phí + Chi phí khác`, chi phí % tính trên giá **chưa** thuế, giá bán = hệ số × giá nhập
  kho (làm tròn **trăm**), TMĐT = bán lẻ × 1,3. Dựng lại **PTG-03178** trên mockup ra **13,108,986** —
  khớp từng đồng với DB. 🐞 Class JS của ERP trên `develop_01` lại cộng từ giá **chưa** thuế (ra
  12,100,946) — **lệch với 100% dữ liệu đã lưu**, phải chốt lại khi viết BE.
  🐞 **5 lỗi im lặng tự bắt bằng Playwright:** đổi đơn vị tiền tệ **mất trắng giá vừa nhập** · tỉ giá
  không đổi theo tiền tệ · số chứng từ **nhảy số** · bảng bị bóp (`width:100%` ⇒ ô nhập còn **36px**) ·
  dòng giá cao **73px** do badge + nút rơi 2 dòng (sửa còn 45px).
  📄 Spec: `man-danh-muc-hang-hoa/design.md` **§29** (+ 5 việc treo ở §29f) · ảnh thật
  `man-danh-muc-hang-hoa/anh-mockup/29-*.png`.
  🔜 **Bước tiếp:** user duyệt §29 → gộp **5 tồn của §29f** vào vòng chốt 14 tồn → rồi mới mở code.

  🟢 **CHECKPOINT 24/09/2026 (WRAP UP) — MÀN CHÍNH SÁCH GIÁ BÁN NỘI BỘ (§28): MOCKUP XONG SAU 10
  VÒNG SỬA, CHỜ USER DUYỆT.** Hai repo **không đụng dòng source nào** (đúng §22); mockup nằm trong
  `mockup-luong-xay-dung-hang-hoa.html` (133 KB → **269 KB**), xem ở cổng cố định 8899 → menu trái
  *Cấu hình giá bán nội bộ*.
  🧩 **Hình thức chốt cuối:** lưới **hãng gộp dòng · mỗi CÔNG TY MUA một dòng · giá trị cấu hình là
  cột**; *Cách tính* ở cấp hãng kèm ghi chú dấu (`+ % trên giá vốn` / `− % trên giá bán`); **lưu theo
  từng hãng** (payload 1 hãng, tránh formdata khổng lồ); cột Hành động là **button** *Lưu · Xem trước
  giá · Lịch sử* (+ *Bỏ khỏi lưới* chỉ với hãng chưa lưu lần nào, **hãng đã khai không xoá được**);
  bộ lọc 1 hàng (tìm hãng · **Công ty mua** · **toggle** *Chỉ công ty đã khai*); thanh tiêu đề có
  **Cách khai báo** (Hệ số theo công ty / **Hệ số chung** — chỉ khai ở công ty mua đầu danh sách,
  còn lại kế thừa) · **Chọn hãng** · **Import Excel** (cam) · **Xuất Excel** (xanh lá); popup
  **Lịch sử** theo đúng `entity-history/ui-base.md`, popup **Import** theo `V2BaseImportModal`;
  cảnh báo chưa lưu bằng **popup phần mềm** (đã gỡ `beforeunload`).
  🏢 Demo: công ty bán **TÂN PHÁT** · 6 công ty mua **ETEK POWER · ETEK GREEN · ETEK · TÂN PHÁT SG ·
  CN HẢI PHÒNG · CN VINH**; hãng lấy **thật** từ `manufactures` (1.071, 59 hãng khoá hiện 🔒).
  🐞 **9 lỗi im lặng tự bắt bằng Playwright cả đợt:** mất tick khi đổi từ khoá · `th rowspan`+sticky
  đè dòng đầu · bật *Hệ số chung* xoá sạch hãng chưa khai ở công ty đầu · *"Rời đi"* mà màn đứng im ·
  chữ ô chọn bị cắt · tooltip ⓘ tràn khung nhìn · mất viền cột *Cập nhật gần nhất* · dòng cao so le ·
  dòng lỗi bảng import không ăn nền hồng.
  🔜 **Bước tiếp:** user duyệt → mockup **nơi hiện số gợi ý** (§28e) → **vòng chốt 14 tồn** (6 câu sổ
  chốt mục 3 + 8 câu §26g) + **4 tồn riêng của màn** (§28f: quyền · trần % · hãng chưa có hàng hoá ·
  công ty mua ngừng hợp tác) → rồi mới mở code.

  🟢 **CHECKPOINT 24/09/2026 — THÊM MÀN CẤU HÌNH GIÁ BÁN NỘI BỘ (§28), chờ duyệt.**
  Hai repo sạch, **không đụng dòng source nào** (đúng §22). Màn dựng thẳng vào
  `mockup-luong-xay-dung-hang-hoa.html` (133 KB → **222 KB**) để đứng cạnh ô *"Đang làm việc tại"* —
  đổi công ty là thấy ngay **công ty nào cũng có thể là công ty CHỦ**.
  ✅ 8 đáp án user chốt (ghi `design.md` §28): khoá theo **Hãng sản xuất** (`manufactures`) ·
  2 nguồn hàng **hard-code** (nhập khẩu nguyên lô / tồn kho) · theo giá bán thì hệ số áp **cả 6 loại
  giá** · **chỉ là số GỢI Ý**, không ghi vào bảng giá · mỗi công ty tự khai bộ của mình · **không có
  ngày hiệu lực**, có lịch sử chi tiết · hãng chưa cấu hình thì **cảnh báo lúc lấy hàng về** ·
  **độc lập** với `manufacture_expect_prices` (dừng 12/2022) và `company_price_types`.
  🧮 Công thức **tuỳ gốc tính**: theo giá vốn = `× (1 + %)` (cộng, lãi nội bộ) · theo giá bán =
  `× (1 − %)` (trừ, chiết khấu). Đo thật: 42,500,000 → 42,925,000 / 43,350,000; Bán lẻ 53,500,000 →
  52,965,000 / 52,430,000.
  🔁 **Vòng 2 trong ngày — user chốt lại hình thức màn:** *"một màn hình vừa là form khai báo vừa thể
  hiện được từng công ty có chính sách như thế nào"*. Bỏ cặp *danh sách + popup form*, thay bằng
  **MỘT LƯỚI NHẬP TẠI CHỖ**: dòng = **hãng sản xuất** · cột *Cách tính* ở cấp hãng · **nhóm cột theo
  từng công ty mua** (mỗi công ty 2 ô % nhập thẳng) · thanh ghim đáy **Huỷ thay đổi / Lưu** một lần
  cho cả lưới, ô vừa đổi tô vàng. Menu ⋮ mỗi dòng: **Xem trước giá** · Lịch sử · Bỏ hãng khỏi lưới.
  **Popup chọn hãng (1.071 hãng) nay chỉ để KÉO HÃNG VÀO LƯỚI**, không nhập liệu trong popup — tìm
  theo mã/tên, tick nhiều, tick-tất-cả theo dòng đang hiện, 80 dòng/lượt, hãng đã có trên lưới thì
  khoá tick; hãng khoá (59/1.071) hiện **🔒**.
  🐞 **2 lỗi im lặng tự bắt bằng Playwright:** (1) tiêu đề **2 tầng** dùng `th rowspan=2` +
  `position:sticky` ⇒ hàng tiêu đề tầng 2 **đè lên dòng dữ liệu đầu tiên**, mất hết ô nhập của dòng 1
  (đếm DOM vẫn đủ ô, phải nhìn ảnh mới thấy) — bỏ sticky cho `th`, chỉ giữ dính trái 2 cột định danh;
  (2) tick hãng rồi gõ từ khoá khác là **mất tick** (tick 3 hãng Bosch, gõ "launch" còn 1) — giữ
  trong mảng tạm, cập nhật ngay mỗi lần tick.
  🔁 **Vòng 3 (cùng ngày) — 5 yêu cầu nữa:** nhãn *"Nhập khẩu nguyên lô"* → **"Nhập khẩu"** ·
  **LƯU THEO TỪNG HÃNG** (nút Lưu mọc ngay trên dòng có thay đổi, payload chỉ 1 hãng; nút chân màn
  là *"Lưu N hãng đã đổi"* — gửi cả lưới thì payload quá lớn) · **mỗi công ty mua một màu nền cột**
  (6 tông nhạt, tránh vàng vì vàng = ô chưa lưu, tránh đỏ vì đỏ = lỗi) · **cảnh báo còn thay đổi
  chưa lưu** ở CẢ 3 lối rời (đổi màn · đổi ô "Đang làm việc tại" · đóng/tải lại tab) ·
  demo 6 công ty mua: Tân Phát Power · Tân Phát Green · Tân Phát Sài Gòn · CN Hải Phòng · CN Vinh ·
  ETEK. Đo: sửa 2 hãng ⇒ nút Lưu mọc đúng 2 dòng; lưu riêng 1 hãng ⇒ toast *"gửi 1 bản ghi, 4 công
  ty nhận"*, còn đúng 1 hãng chưa lưu; đổi công ty khi chưa lưu ⇒ popup chặn + ô chọn tự trả về công
  ty cũ. 🐞 Thêm 2 lỗi tự bắt: *"Rời đi, bỏ thay đổi"* mà **màn đứng im** (đếm thay đổi từ DOM cũ →
  phải vẽ lại trước khi chạy việc đang chờ) và chữ ô chọn bị cắt *"Theo giá vốr"*.
  🔁 **Vòng 4 (cùng ngày) — ĐỔI TRỤC BẢNG theo yêu cầu user:** *"công ty thành row, các giá trị cấu
  hình là col"*. Bỏ kiểu mỗi công ty một nhóm 2 cột (bảng phình ngang, 8 công ty là phải cuộn 421px).
  Nay **ô Hãng + ô Cách tính gộp dòng (`rowspan`)**, **mỗi công ty mua là một DÒNG**, cột là
  *Công ty mua · Nhập khẩu (%) · Tồn kho (%) · Cập nhật gần nhất · Hành động*; **Cách tính khai một
  lần cho cả hãng**. Nút *"Lưu hãng này"* + menu ⋮ nằm trong ô gộp; thêm nút **Xoá** tỷ lệ của riêng
  một công ty và tick *"Chỉ hiện công ty đã khai"* (30 → 14 dòng). Đo: `rowspan=6` đúng số công ty ·
  **0 cuộn ngang** ở cả 2 độ phân giải · nút Lưu chỉ mọc ở hãng có thay đổi · toast *"gửi 1 bản ghi,
  5 công ty mua"* · footer ghim đáy không che dòng cuối (804 < 852).
  🔁 **Vòng 5 (cùng ngày) — 6 yêu cầu:** cột Hành động thành **button** *Lưu · Xem trước giá · Lịch sử*
  (+ *Bỏ khỏi lưới* CHỈ với hãng vừa chọn vào chưa lưu — **hãng đã khai báo không xoá được**) ·
  **bỏ thao tác xoá theo công ty** · **đổi lại màu định danh công ty** (vạch trái đậm + nền 7% + tên
  in cùng màu) · **Cập nhật gần nhất hiện `dd/mm/yyyy HH:mm:ss` theo TỪNG công ty** (đụng công ty nào
  mới đổi mốc công ty đó) · **popup Lịch sử dựng đúng `.claude/skills/entity-history/ui-base.md`**
  (3 nhóm hành động cố định · ô Người thực hiện lấy từ danh sách nhân sự `MÃ PHÒNG - Tên` · timeline
  mới→cũ · cũ đỏ → mới xanh · ghi chú nền vàng · footer chỉ nút Đóng); mỗi lần Lưu sinh log thật, bỏ
  chính sách của một công ty ghi vào nhóm *Thay đổi trạng thái*.
  🔁 **Vòng 6 (cùng ngày) — 4 yêu cầu:** đổi tên + thứ tự công ty mua (**ETEK POWER · ETEK GREEN ·
  ETEK · TÂN PHÁT SG · CN HẢI PHÒNG · CN VINH**, công ty bán TÂN PHÁT) · bộ lọc thêm **Công ty mua**
  (chọn 1 công ty ⇒ 30 → 5 dòng) · thêm **tuỳ chọn toàn cục "Cách khai báo: Hệ số theo công ty /
  Hệ số chung"** · chế độ **Hệ số chung** chỉ cho nhập ở **công ty đầu danh sách** (10 ô nhập / 50 ô
  khoá kèm nhãn *"kế thừa từ ETEK POWER"*), gõ ở công ty đầu là các công ty còn lại đổi theo ngay.
  🐞 **1 lỗi mất dữ liệu im lặng tự bắt được:** lan toả bản đầu lấy đúng công ty đầu làm gốc ⇒ hãng
  chưa khai ở công ty đó bị **xoá sạch** chính sách (5 hãng còn 3, không báo gì). Sửa: công ty đầu
  trống thì lấy **dòng đã khai đầu tiên** làm gốc.
  🔁 **Vòng 7 (cùng ngày):** đổi khái niệm **Công ty chủ → Công ty bán**, **Công ty nhận → Công ty
  mua** (đổi cả 4 tài liệu) · ô lọc *"Chỉ công ty đã khai"* đổi từ checkbox sang **toggle** đúng số đo
  `custom-switch` của app (28×16px, knob dịch 12px, bật `#1abc9c`), có nhãn *Hiển thị* nên thẳng hàng
  với ô *Công ty mua* · **dời "Cách khai báo" lên thanh tiêu đề bảng** cạnh nút *Chọn hãng*, chú thích
  dài gom vào **icon ⓘ** (thanh lọc 107px → 77px, header 55px, không xuống dòng ở 1366).
  🔁 **Vòng 8-9:** bỏ chữ *"kế thừa từ …"* (làm lệch dòng, chuyển vào `title`) · vá **viền phải cột
  *Cập nhật gần nhất*** (cột Hành động là ô gộp nên dòng thường dính rule `td:last-child`) · hãng mới
  chọn hiện **ở đầu bảng** · bỏ chú *"áp cho cả hãng"*, thay bằng **dấu công thức** `+ % trên giá vốn`
  / `− % trên giá bán` · ghim chiều cao dòng 38px cho khỏi so le · **cảnh báo chưa lưu chuyển sang
  popup của phần mềm** đúng chữ skill `unsaved-changes` (*"Thông tin chưa lưu"* · *"Bạn có thông tin
  chưa lưu. Có chắc chắn muốn thoát?"* · nút **Thoát** / **Ở lại**), **gỡ hẳn `beforeunload`** —
  user chốt không dùng hộp thoại trình duyệt.
  🔁 **Vòng 10:** thêm **Import Excel** (cam) + **Xuất Excel** (xanh lá) theo `button-convention`;
  popup import dựng theo `V2BaseImportModal` (3 nhóm nút · bảng xem trước tô dòng lỗi + ghi lý do
  ngay dưới ô sai · toggle *Chỉ dòng lỗi* · chỉ nạp dòng hợp lệ, nạp xong vẫn phải bấm Lưu);
  thêm **icon ⓘ cho 2 cột tỷ lệ** (Nhập khẩu = bán nguyên lô nhập khẩu về thẳng kho công ty mua ·
  Tồn kho = xuất bán từ kho); bỏ dòng phụ cạnh tiêu đề bảng.
  🐞 **Lỗi tự bắt (vòng 10):** dòng lỗi bảng import **không ăn nền hồng** vì `table.tbl td` đè
  `.dong-loi td` — đếm class vẫn đủ 2 dòng, chỉ nhìn ảnh mới lộ.
  🐞 **Lỗi tự bắt:** tooltip ⓘ căn giữa làm bảng 300px **tràn khỏi khung nhìn** (phải 1475 > 1464) →
  neo theo mép phải; đo lại 1600 `1161…1461`, 1366 `927…1227`.
  📐 Đo đủ ở 1600×900 + 1366×768, **0 lỗi console**: 4/2/0 hãng theo 3 công ty bán · nhóm cột đổi
  theo công ty đang làm việc · nhập tại chỗ tô vàng + đếm "thay đổi chưa lưu" · Lưu/Huỷ thay đổi
  chạy đúng · validate tô đỏ đúng ô sai (150%) và ô khai thiếu, **không lưu gì** · xem trước khớp
  công thức · ca thật **8 công ty (17 cột)** cuộn ngang 421px mà cột định danh vẫn dính trái ·
  **hồi quy 3 màn cũ + form hàng hoá vẫn chạy**.
  🔜 **Bước tiếp:** user duyệt → mockup **nơi hiện số gợi ý** (popup *Xem hàng hoá Công ty khác* /
  màn Tính giá — §28e) → rồi mới vào vòng chốt **14 tồn** (6 câu `SO-CHOT-VA-TON.md` mục 3 + 8 câu
  §26g). Tồn riêng của màn này: quyền · trần % · hãng chưa có hàng hoá · công ty mua ngừng hợp tác.

  🟢 **CHECKPOINT 23/09/2026 (b) — THÊM MOCKUP BÁO CÁO HÀNG HOÁ THEO CÔNG TY, chờ duyệt.**
  Hai repo sạch, nhánh `feat/p1-danh-muc-hang-hoa`, **không đụng dòng source nào** (đúng §22).
  📦 `man-danh-muc-hang-hoa/mockup-bao-cao-hang-hoa.html` — 1 file 68 KB, 0 tài nguyên ngoài.
  **Ma trận 29 mã × 8 công ty thật**, ô giao nhau là trạng thái; 4 cột định danh dính trái; khối
  8 cột công ty + 2 cột đếm (*Khai thác* / *Kinh doanh*) đặt ngay sau tên nên ma trận hiện ra
  **không cần cuộn ngang** ở cả 1600×900 lẫn 1366×768.
  ✅ 4 quyết định chốt (ghi `design.md` §27): ma trận (không phải 2 tab) · "đang sử dụng" =
  **có bản ghi trạng thái** · dùng lại bộ cột màn danh sách · **không có kỳ**, là ảnh chụp hiện trạng.
  ✅ **3 vòng sửa theo góp ý user (chốt cuối ngày)**: (1) **4 mục trạng thái ở chú giải đầu bảng bấm
  được để lọc nhanh**, kèm số lượt dùng, dùng CHUNG `stChon` với ô lọc "Trạng thái" nên đồng bộ hai
  chiều · (2) **bỏ dải ghi chú giả định** khỏi giao diện (*"khách không cần đọc"*), nội dung chuyển
  vào §27f + chú thích trong nguồn, vùng bảng cao thêm 484 → 548px · (3) nhãn **`CHỦ` → `QUẢN LÝ`**
  (đổi cả cột *Vai trò* trong popup cho khỏi lệch chữ).
  🐞 **7 lỗi giao diện tự bắt bằng Playwright**: `table-layout:fixed` không khai tổng bề rộng làm
  cột dính lệch (khai 150px ra thật 132px) · thanh lọc 155px/2 hàng thay vì 68px/1 hàng · trang
  975px trong khung 900px sinh 2 thanh cuộn lồng nhau · nhãn nhóm căn giữa ô colspan 950px rơi ra
  ngoài khung nhìn · tiêu đề 2 cột đếm bị cắt · placeholder ô tìm bị cắt · số đếm trong panel ô chọn
  nhiều rỗng (khai thẻ mà không đổ dữ liệu).
  📐 **5 nguồn cùng một số**: **80 chấm trên ma trận = 80 "Tổng lượt dùng" = 80 tổng cột *Khai thác*
  = 15+14+7+44 của 4 ô trạng thái = Σ 8 số của ô lọc Công ty**; lọc bỏ 3 công ty + 1 trạng thái thì
  cả 4 cùng về **44**, gõ "Fusheng" ra **13**, tắt TPE ra **61**. 0 lỗi console, xanh ở cả
  1600×900 lẫn 1366×768.
  👁 Xem mockup: cổng cố định **8899** (`http://127.0.0.1:8899/mockup-bao-cao-hang-hoa.html`),
  sửa file xong phải Cmd+Shift+R vì cổng cố định có cache.
  🔴 **Phụ thuộc:** báo cáo chỉ đứng được nếu **tồn 26g-5** chốt là **tham chiếu**; chốt là "chép mã
  mới cho từng công ty" thì ma trận sụp. Nguồn dữ liệu trực tiếp là **tồn 26g-2**.
  ❓ Còn tồn riêng của màn: quyền xem · Excel dạng ma trận hay dạng phẳng · ma trận vừa khít tới 8
  công ty, mở công ty thứ 9+ phải tính lại.

  🟢 **CHECKPOINT 23/09/2026 (a) — MOCKUP LUỒNG 3 BƯỚC XONG, CHỜ USER DUYỆT.** Hai repo sạch, nhánh
  `feat/p1-danh-muc-hang-hoa`, **không đụng dòng source nào** trong đợt này (đúng §22).
  User đưa **"Logic xây dựng hàng hoá"**: quy trình **3 bước** — *Đang nhập thông tin* →
  *Chờ tính giá bán* → (*Đang tính giá*) → *Đang kinh doanh*, và **trạng thái quản lý theo TỪNG
  CÔNG TY** (cùng mã hàng, TPE đang kinh doanh mà Power mới đang nhập thông tin). Kèm nút
  **"Xem hàng hoá Công ty khác"** để công ty B lấy hàng của A về khai tiếp.
  📦 **Sản phẩm của đợt:** `man-danh-muc-hang-hoa/mockup-luong-xay-dung-hang-hoa.html` —
  **1 file 132 KB, 0 tài nguyên ngoài**, nháy đúp là chạy. Gồm 6 màn bấm được trọn luồng:
  ghi chú & sơ đồ luồng · 3 màn danh sách theo trạng thái · form 6 tab · màn tính giá
  (tab con theo từng ĐVT, mỗi ĐVT một bảng **đủ 6 loại giá** của `price_types`) · popup lấy hàng
  công ty khác (12 cột, 16 ô lọc, phóng to toàn màn hình).
  ✅ **Quyết định mới đã chốt** (ghi `design.md`): §26 quy trình 3 bước theo công ty ·
  **§26c-bis 3 mức quyền sửa** (công ty tạo ra sửa cả 6 tab · công ty lấy hàng về chỉ sửa tab
  *Dữ liệu quản trị* · vai tính giá khoá hết, chỉ làm tab *Giá bán*) · **§26d-bis** bảng bộ ba
  Hãng/Loại/Model × Đời xe — **chốt luôn tồn §3.3 "Đời xe hiển thị thế nào"** · §26d-ter tab Nhóm
  máy · **§26f bộ cột danh sách** (13 cột mặc định + cấu hình 26 cột; **bỏ** trường *Trạng thái đồng
  bộ*; màn kinh doanh **không có giá vốn**, cột giá là *"Giá bán lẻ"*).
  🎨 **Style: bám `assets/scss/sale-theme.scss`** — bộ style chốt của 14 phân hệ hub. Vòng 2 em đo
  `getComputedStyle` mà không biết file này nên lấy nhầm nền trắng cho đầu cột; đúng phải là
  gradient teal `#eafcfe→#d2f4f9` + chữ `#0a7c88` + gạch `2px #20d9ea`. Đã ghi vào memory.
  🐞 **11 lỗi giao diện tự bắt bằng Playwright** (test xanh / đọc code đều không thấy): nút cách
  24px thay vì 12px · cụm nút Hành động xuống 2 dòng · thanh nút treo lơ lửng · menu ⋮ bị khung cuộn
  cắt mất mục cuối · ô tìm lệch 10px · rail mở làm nội dung trôi 58px · 2 `onchange` trên cùng thẻ
  select · `:hover` không kiểm được bằng sự kiện giả lập · tab cấp 1 nuốt trạng thái tab con · toạ độ
  cột dính tính theo bề rộng khai báo nên che mất cột · thừa `</div>` làm nội dung tụt xuống.
  🔜 **Bước tiếp:** user duyệt mockup → quay lại **8 tồn `design.md` §26g** (nặng nhất: *lấy hàng
  công ty khác = chép hay tham chiếu* và *trạng thái theo công ty lưu bảng nào*) → rồi mới mở code.

  🟡 **CHECKPOINT 22/09/2026 — YÊU CẦU ĐỔI LỚN, đang ở giai đoạn CHỐT SPEC.** Hai repo sạch,
  nhánh `feat/p1-danh-muc-hang-hoa` (api +29, client +28 commit chưa merge).
  ⚠️ **User chốt quy trình mới (§22): CHỐT SPEC + MOCKUP TRƯỚC, không động source dự án** cho tới
  khi được yêu cầu. Mockup không tính là source (thư mục riêng, sẽ xoá).
  **6 quyết định đổi phạm vi trong một ngày** (§17→§25): giá **tách khỏi form** → mở **Phase 8**
  "Quản lý giá hàng hoá" · **mỗi công ty một bảng giá độc lập** · tab Dữ liệu quản trị **bỏ tab
  lồng theo Công ty**, công ty nào khai của công ty đó · 2 cờ khai báo chuyển sang **Loại sản phẩm**
  (cấp lá) · **giữ bảng `groups`** với vai trò Nhóm máy (Phase 5 chỉ gỡ MÀN, KHÔNG xoá bảng) ·
  nguyên tắc **bám ERP đang chạy, không bám mockup**.
  🔴 **ĐANG CHẶN — 1 câu quyết định cả đợt migration (§25d):** "bảng giá độc lập theo công ty" có
  gồm **giá vốn / giá mua ngoài** không, hay chỉ 6 loại giá bán? Có ⇒ phải tách tầng giá khỏi
  `product_units` (thêm bảng `product_company_units`, sửa 34 file ERP); không ⇒ chỉ thêm
  `company_id` vào `product_unit_prices`.
  🔴 **Và §24f — hai hướng đang ngược nhau:** giá đang theo hướng A (nullable, giữ giá trị chung,
  ERP 0 file sửa), dữ liệu quản trị đã chốt hướng B (NOT NULL, xoá cột chung, 71 file phải rà).
  Cần chốt MỘT hướng.
  ✅ **Task C1 xong** — sinh mã hàng hoá. Dựng lại mã cho cả 45.890 hàng hoá: khớp **45.659
  (99,50%)**; 231 chỗ lệch chứng minh được là dữ liệu đổi sau khi mã chốt, không phải lỗi port.
  9 ca PHPUnit xanh. Kèm hàng rào **mã sinh MỘT LẦN, giữ mãi mãi** (hook `updating` ở model).
  🐞 **Bẫy lớn nhất hôm nay:** `iconv('ASCII//TRANSLIT')` cho kết quả **khác nhau theo máy chạy** —
  model `THANH ĐỒNG` ra `THANHDONG` trên Linux (đúng mã đang lưu) nhưng `THANHDNG` trên macOS. Mã
  không sinh lại khi sửa nên lệch một lần là lệch vĩnh viễn. Thay bằng bảng bỏ dấu cố định.
  🐞 Mockup: 9 nút icon render ra **ô vuông trống** (`V2BaseIconButton` không có prop `icon`/
  `variant` — icon phải qua slot) · card "Phụ tùng ô tô" **trùng ở 2 tab** · `can_retail` còn sót ở
  `ExportColumnRegistry` + `CatalogHistoryService` sau khi cột đã gỡ.
  ⚠️ **Số file ERP bị ảnh hưởng đã đính chính** (grep thô đếm cả bảng khác trùng tên cột):
  `min_stock_qty` **29** · `guarantee_type` **42** · chuỗi giá **34** — không phải 42/86/44.
  📌 Việc đã lỡ làm vào source thật TRƯỚC khi có §22, **chờ user quyết giữ hay gỡ**: 2 cờ trên màn
  Loại sản phẩm · 2 màn Dòng xe/Tải trọng xe · 6 màn danh mục Xe · Task C1.
  🟡 **CHECKPOINT 21/09/2026 cuối ngày — ĐỢT A + ĐỢT B XONG, 48/122 bước.** Nhánh
  `feat/p1-danh-muc-hang-hoa` (cả 2 repo), 9 commit, hai repo sạch, chưa merge về `gop_db`.
  BE đã chạy thật: `GET /products` (danh sách, 12 cột, 11 bộ lọc) · `GET /products/{id}` (chi tiết
  5 tab) · `GET /products/form-options` (14 danh mục, 13 query / 163 ms / 179 KB) ·
  `GET /products/option-search` · `GET /products/vehicle-options`. Entity `Product` + 17 model con.
  📐 **Số đo chốt:** danh sách 5 query cho cả 20 lẫn 100 dòng · chi tiết 22–27 query bất kể số dòng
  con · index `products_updated_at_id_index` đưa sắp xếp mặc định từ **119 ms → 0 ms**
  (rows 42.391 → 20, hết filesort).
  🐞 **4 bẫy im lặng bắt được, đã ghi vào docblock:** (1) **KHÔNG** `SoftDeletes` cho `products` dù
  bảng có `deleted_at` — 175 hàng hoá `status=1` vẫn còn `deleted_at`, bật trait là mất hút 175 mã;
  (2) quyền `Quản lý giá` **chỉ có ở guard `web`** nên `isCurrentEmployeeHasPermission` luôn false
  → gate giá vốn là **cổng chết**; phải đọc CHÉO GUARD qua `roles`/`employee_has_roles` (bảng dùng
  chung, 133 nhân viên đang giữ); (3) **KHÔNG** `morphedByMany()` cho `productables` — cột
  `productable_type` lưu nguyên văn class ERP, khai bằng class HRM là khớp 0 dòng và ghi ra dòng
  ERP không đọc được; (4) `tax_rates` **không** lọc theo `is_sales_tax`/`is_purchases_tax` —
  0/40 dòng bật cờ, lọc là ô chọn rỗng sạch.
  🚗 **Tab 6 "Phân loại xe"** (user chốt 21/09): đưa nguyên khối "Phụ tùng ô tô" của ERP sang,
  bỏ bắt buộc. BE `cf5c489a9`, mockup `3b1f98798` (đã đo DOM bằng Playwright: 6 tab, 3 select2,
  **0 phần tử bắt buộc**, lưới đủ 12 cột, footer không đè).
  🔴 **ĐANG CHỜ USER CHỐT 3 CÂU** (`design.md` §15d) trước khi code tiếp: (1) "Nhóm máy" trỏ vào
  bảng `groups` — **chính là danh mục Phase 5 đã chốt bỏ**, mà `products.group_id` trỏ tới ở cả
  45.890 dòng; (2) phạm vi danh mục xe chuyển sang HRM (4 bảng của màn hàng hoá hay cả 9 bảng
  `vehicle_*`); (3) cách hiển thị "Đời xe" — dữ liệu là bộ BA hàng hoá × Model xe × Đời xe. Thêm 1
  điểm cần xác nhận: 2 checkbox trên Tính chất hàng hoá **đảo lại** quyết định "tab hiện với mọi
  Tính chất".
  ⚠️ **ĐÍNH CHÍNH**: bản ghi trước nói *"Đời xe bỏ hẳn vì bảng `vehicle_lifes` không tồn tại"* là
  **SAI** (tra nhầm tên số nhiều). Bảng thật `vehicle_life` **61 dòng**, bảng nối
  `product_vehicle_model_has_life` **48.736 dòng / 91 hàng hoá**. Đã sửa `design.md` §15.
  **Mở 21/09/2026.** Mockup màn DANH SÁCH + màn TẠO/SỬA hàng hoá (user chốt: 2 màn là MỘT việc),
  rồi port sang HRM theo mockup. Khảo sát ERP xong → `man-danh-muc-hang-hoa/khao-sat.md`.
  ⚠️ Quy mô khác hẳn Phase 1: `products` 59 cột / 45.890 dòng, **171 bảng có FK trỏ vào nó**,
  controller 4.623 dòng, model 8.122 dòng, form 95KB × 2, 17 khối form, 29 cột danh sách.
  🔴 2 phát hiện đổi cục diện: (1) "Tính chất hàng hóa" bên ERP là **enum chuỗi cứng**
  `products.product_type`, không phải danh mục; "Loại hàng hóa" là cột JSON `product_cate`.
  (2) `products` **chưa có cột nào** trỏ tới cây phân loại Phase 0, còn `group_id` (nhóm cũ, thuộc
  nhóm BỎ ở Phase 5) thì 45.890/45.890 dòng đều có giá trị → Phase 2 phải thêm FK + **quy đổi
  45.890 hàng hoá** sang cây mới (Phase 0 đã ghi việc này là "ngoài phạm vi đợt đó").
  ✅ **21/09/2026 — user đã đưa tài liệu 6 tab** (lưu nguyên văn ở `man-danh-muc-hang-hoa/yeu-cau-khach.md`).
  Đã chốt **8 quyết định** (xem `man-danh-muc-hang-hoa/design.md`), nổi bật:
  · tab 5 + tab 6 "theo từng công ty" → **tách sang Phase 3**
  · `product_cate`, `product_type`, `group_id` → **không ánh xạ, để trống**; sửa `SearchController`
    bỏ 2 điều kiện lọc theo enum cũ (dòng `!= 'service_product'` vô điều kiện làm hàng hoá
    `product_type` trống **biến mất khỏi popup của 338 màn** — `NULL <> 'x'` cho ra NULL)
  · `can_retail` · `groups.rate_liquidation` · `groups.checksheet_id` → **bỏ hẳn**
  · quy chế hoa hồng theo tính chất hàng hoá → **chỉ tồn tại ở service đã chết**, bỏ qua
  · **Thông số cơ bản đổ theo Nhóm sản phẩm** (không phải Loại sản phẩm) → phải **nâng bảng nối
    `product_type_attributes` lên cấp `product_families`** và chuyển ô "Thuộc tính" sang màn Nhóm
    sản phẩm. Cả 3 bảng đang 0 dòng nên sửa bây giờ không mất dữ liệu.
  🎨 **Mockup đã dựng, CHỜ USER DUYỆT** — là TRANG NUXT THẬT (dữ liệu tĩnh), không phải HTML vẽ lại:
  `/master-data/mockup-hang-hoa` (danh sách) · `/master-data/mockup-hang-hoa/form` (5 tab).
  File `hrm-client/pages/master-data/mockup-hang-hoa/` — **xoá sau khi chốt**.
  Qua **5 vòng sửa** theo góp ý: gộp còn 5 tab · card **Đơn vị tính** ở tab 1 · tab **Giá bán** lồng
  2 tầng **Công ty → Đơn vị tính** (khuôn ERP `form.blade.php:969-1150`) · tab **Dữ liệu quản trị**
  cũng theo công ty · **Bảo hành + Hệ số công nghệ** chuyển vào đó · bổ sung **thao tác đầy đủ**
  (cột Hành động 6 thao tác, xoá hàng loạt, footer Sao chép/In tem/Lịch sử) · thêm lại cột
  **Giá công thức** (chỉ đọc).
  Đã kiểm Playwright mỗi vòng: 12 cột · 5 tab · **0 hàng lỗi bố cục**.
  🐞 Tự bắt 4 lỗi của mockup: **slot `V2BaseDataTable` phải là `#cell-<key>="{ item }"`** (viết kiểu
  Bootstrap-Vue là im lặng ra giá trị thô — đã lưu memory) · `sticky:'right'` không tồn tại · ô
  "Serial number" thêm nhầm (`products.serial_number` 0/45.890 dòng) · đo trang có **tab lồng** phải
  lấy con trực tiếp của `.tab-content` cấp 1.
  ➕ **Vòng 5-6:** icon cho 15 card (dùng slot `#title` sẵn có, **không sửa component dùng chung**;
  chỉ lấy icon đã xuất hiện thật trong repo để né bẫy 2 bản Remix Icon) · **"Đặc điểm" → CKEditor 5**
  (khớp `ck-editor` của ERP; chọn CKEditor 5 vì là chuẩn 25 màn, không dùng bản 4 dành cho mẫu in).
  📤 **BẢN HTML ĐỘC LẬP GỬI KHÁCH:** `man-danh-muc-hang-hoa/mockup-hang-hoa.html` (**3,1 MB**) —
  nháy đúp là mở, **không cần server/internet**, chuyển màn + chuyển tab lồng đều chạy.
  Script xuất lại: `e2e/xuat-mockup.js`. Đã kiểm trên đúng `file://`: **0 tài nguyên lỗi**.
  ✅ **Đã commit** `3863a9bc7` (mockup), không merge.
  🐞 Thêm 3 bẫy khi xuất HTML: Chromium mới không có phiên đăng nhập · `remixicon.css` có **2 khối
  `src:`** (thay 1 khối là icon thành ô vuông rỗng) · 5 font cục bộ `/_nuxt/assets/fonts/*` không
  tồn tại khi mở `file://`. ⚠️ **Đo bề rộng icon > 0 KHÔNG đủ** để kết luận icon đúng — phải so bề
  rộng font icon vs font thường (64px vs 46px) hoặc `document.fonts.check`.
  🔑 **Quyết định 13 (21/09):** user sẽ **chặn toàn bộ route tạo/sửa hàng hoá ERP** ⇒ bỏ được 4 mối
  lo (BB-7 rule required · đồng bộ validate · `code_2025`/`code_2020` · va chạm mã). Còn đúng một
  việc: **làm ERP đọc được hàng hoá thiếu `group_id` mà không nổ**.
  🔴 `->group->cột` xuất hiện **>100 chỗ, KHÔNG chỗ nào null-safe** → PHP 7.4 nổ
  `Trying to get property of non-object`. **~37 chỗ phải sửa** trên 10 file còn sống; nặng nhất
  **`SearchController` 11 chỗ** — callback DataTables chạy TỪNG DÒNG nên **một** hàng hoá thiếu nhóm
  làm **nổ cả popup** ở 338 màn (nặng hơn BB-6: không chỉ "biến mất" mà là **crash**).
  Kế hoạch + 8 bước kiểm: `man-danh-muc-hang-hoa/sua-erp-de-khong-loi.md`.
  🎯 **Quyết định 12 (21/09) — TIÊU CHÍ NGHIỆM THU ĐỔI:** user chốt *"chuyển hàng hoá trước, quản
  lý giá/duyệt giá/tính giá chuyển dần; mục tiêu quan trọng là ERP vẫn chạy ổn định"*.
  ⇒ Phase 2 nghiệm thu theo **"ERP không vỡ"**, không phải "màn HRM chạy được".
  Hợp đồng + 14 bước nghiệm thu: `man-danh-muc-hang-hoa/hop-dong-tuong-thich-erp.md` — **6 bất
  biến**, nặng nhất: **BB-1** sửa giá phải đi qua luồng duyệt (màn ERP **không ghi giá trực tiếp** —
  đường đó đã comment tắt; nhánh đang chạy theo cờ `$is_approve` tính từ `companies.is_new_company`
  / `is_new_brand` / `new_brand_ids`; **1/8 công ty đang bật**) · **BB-2** không có quyền
  `Quản lý giá` thì không đụng gì tới giá · **BB-6** `product_type` trống ⇒ hàng hoá mới **vô hình
  với 338 màn** → **phải sửa `SearchController` TRƯỚC khi bật màn HRM**.
  🔑 **Quyết định 11 (21/09):** luồng **Tính giá → HRM, tách thành Phase 7** (4 controller 1.160
  dòng · 3 model 2.271 · 18 view 2.413 · 39 route) · **lịch sử dùng `catalog_histories` của HRM**,
  không ghi `product_histories` · **BỎ `product_versions`** (nó chỉ là cái nhóm thay đổi của một lần
  lưu — `catalog_histories` đã gom sẵn; giữ 113.768 dòng cũ, chỉ ngừng ghi).
  🔑 **Quyết định 10 (21/09):** *"Toàn bộ luồng ghi hàng hoá chuyển sang HRM. ERP chỉ dùng, không
  ghi nữa."* → `man-danh-muc-hang-hoa/phan-tich-song-song-erp-hrm.md`.
  Phạm vi thật: **16 nơi** ERP đang ghi vào bảng hàng hoá (không phải 3) — gồm **3 job nền** dễ sót
  vì chạy ngoài request. 🔴 Mâu thuẫn cần chốt: **luồng Tính giá `PriceCalculate`** đang GHI giá vào
  hàng hoá (3.120 phiếu, mới nhất 14/09/2026) nhưng thuộc Mua hàng — chuyển hay là ngoại lệ?
  Rủi ro **KHÔNG tự biến mất** khi ERP hết ghi: `product_histories` (319.303 dòng) +
  `product_versions` (113.768) do ERP ghi **rải rác trong controller, không qua observer** → HRM
  không port là lịch sử đứt im lặng.
  ✅ Sửa nhận định sai: `Modules/Finance` của HRM là **Tài chính**, KHÔNG phải kho (kho vẫn ở ERP);
  Finance chỉ ĐỌC hàng hoá, **0 chỗ ghi**.
  🐞 Mockup đang vẽ mã `TP.0012345` — **sai khuôn thật** (`CH-RRI32`, `HN-90915-YZZE1:01`), phải sửa.
  🔄 **Quyết định 14 (21/09):** ĐẢO NGƯỢC 8c — **thuộc tính nối lên LOẠI SẢN PHẨM**, giữ nguyên
  `product_type_attributes` của Phase 0 (bỏ được 2 migration + việc chuyển ô giữa 2 màn; endpoint
  thành `attributes-by-type`). Và **HOÃN lịch sử hàng hoá** khỏi Phase 2 — lịch sử bị đổi ở **nhiều
  luồng** (màn hàng hoá · duyệt giá · Tính giá · duyệt hàng tạm), `product_histories` 319.303 dòng
  do **8 file / 26 chỗ** ghi, không đơn giản như danh mục HRM. ⚠️ Trong lúc chờ: sửa hàng hoá từ HRM
  **không để lại vết ở đâu cả**.
  📋 **PLAN THỰC THI đã viết** (21/09) — user chốt *"chuyển đổi hàng hoá trước, các vấn đề note lại
  sẽ brainstorm sau"*. **20 task / 125 bước**, 6 đợt:
  **A** nền+CSDL (nhánh · 2 cột `products` · nâng bảng nối lên Nhóm sản phẩm · gỡ `can_retail` ·
  4 quyền 1612-1615) · **B** BE đọc (Entity · `form-options` gom 13 danh mục · list + detail có gate
  giá vốn) · **C** BE ghi (sinh mã + retry · tạo · **sửa qua luồng duyệt giá** · 2 endpoint phụ ·
  lịch sử `catalog_histories`) · **D** FE 4 task (chuyển mockup thành màn thật) · **E** làm ERP không
  lỗi (`SearchController` 11 chỗ + `Product.php` + 9 file) · **F** Excel + **nghiệm thu 14 bước**.
  ⚠️ **Task A0 cần user chốt trước:** mở nhánh Phase 2 từ `gop_db` (sau khi merge Phase 1) hay từ
  `feat/p1-danh-muc-hang-hoa` — Phase 2 **phụ thuộc Phase 1** vì form dùng 11 danh mục đó.
  📄 **Spec kỹ thuật đã viết** (21/09):
  `docs/superpowers/specs/gop-db/2026-09-21-man-danh-muc-hang-hoa-design.md` — 2 cột mới trên
  `products` (`product_type_id`, `product_characteristic_id`, **nullable**, **không khai FK** vì 171
  bảng tham chiếu) · **nâng `product_type_attributes` → `product_family_attributes`** (làm sớm vì cả
  3 bảng đang 0 dòng, để lâu phải di trú) · gỡ `can_retail` · 13 endpoint + `GET /form-options` gom
  11 danh mục về 1 request · validate · **4 quyền id 1612-1615** · hiệu năng · 3 việc treo · cách kiểm.
  Đã tự soát: 9/9 số liệu + 5/5 đường dẫn file trong spec khớp thực tế.
  ⏳ **Chờ khách chốt 3 việc:** cách tính **"Giá công thức"** (đường dữ liệu đứt từ 2020, không nơi
  nào trong ERP tính ra nó) · việc **bỏ 2 điều kiện lọc** trong `SearchController` (nới lỏng hành vi
  đang chạy: 30 hàng dịch vụ lọt vào popup của 338 màn, báo giá dịch vụ chọn được 45.890 thay vì
  12.426) · **"Phụ kiện tiêu chuẩn"** có đổi sang CKEditor như "Đặc điểm" không (ERP cũng dùng
  `ck-editor` cho ô này).
  💰 **Khảo sát ĐVT ↔ Giá bán (21/09)** → `man-danh-muc-hang-hoa/khao-sat-don-vi-tinh-gia-ban.md`.
  User chốt: **giữ nguyên toàn bộ logic quản lý giá, chỉ BỎ đồng bộ CRM**.
  ERP vốn ĐÃ có giá theo ĐVT *và* theo thời gian — 3 tầng: `product_units` (46.560) →
  `product_unit_prices` (264.646 = 46.560 × 6 loại giá) → `product_expected_prices` (95.266,
  `effect_date`, 2.495 dòng còn ở tương lai) + luồng **duyệt giá** bằng cột `*_wait_approve`.
  Phần chết KHÔNG port: bảng `product_prices` (dừng 05/02/2021, không có `unit_id`) và cột
  **Giá công thức** (BE không trả → luôn rỗng; đã gỡ khỏi mockup).
  ⚫ **Bỏ đồng bộ CRM nhánh hàng hoá** — đã ngừng từ 08/10/2025, `MATE_API_USE_CRM` không khai
  trong `.env`. ⚠️ **Nhánh nhân sự VẪN SỐNG** (`Employee`/`EmployeeInfo` mới nhất 14/09/2026,
  `Department`, `Part`, `Company`) — không gỡ nhầm. 🔑 8 model trong nhánh hàng hoá chính là các
  danh mục đã port ở **Phase 1** → đồng bộ CRM vốn đã bị bỏ qua từ đó; quyết định này khép lỗ hổng.
  📌 **Việc note để xử lý sau:** quy đổi 45.890 hàng hoá sang cây mới · thay các chỗ lọc sang danh
  mục mới (10 chỗ cơ học + 12 chỗ nhánh cứng) · 176 view · 3 cờ nghiệp vụ thay `product_type`
  (hàng hoá làm dịch vụ / báo giá dịch vụ / thiết bị của khách hàng) · xoá cột.
  Trạng thái: 🟢 **PHASE 1 CODE XONG 20/09/2026 — 11/11 màn**, 15/15 task, chờ user nghiệm thu.
  Nhánh `feat/p1-danh-muc-hang-hoa` (cả 2 repo): hrm-api 13 commit, hrm-client 11 commit.
  ⚠️ **CẦN CHERRY-PICK `221cda7b2` VỀ `gop_db` NGAY**: `app/Services/CatalogHistoryService.php`
  trên chính `origin/gop_db` đang **hỏng cú pháp** (vết merge nhánh Phòng họp + #11421, thiếu
  `]],` ở mục `meeting_room_settings`) -> MỌI thao tác ghi lịch sử danh mục đều fatal, ảnh hưởng
  6 màn #11421 + 2 màn Phòng họp + 18 màn danh mục cũ. Bộ test #11421 không bắt được vì tạo bản
  ghi bằng `Model::create()` trực tiếp, không qua service.
  11 màn: xuất xứ 113 · đơn vị thuộc tính 103 · model 39.796 · đơn vị tính 145 · thuộc tính 446 ·
  thương hiệu 1.250 · hãng sản xuất 1.071 · code đặt hàng 8.664 · file đính kèm 8 · mã màu 0 ·
  thuế suất 40. Nền `BaseCatalog*` bị đụng 2 lần, cả 2 lần `ProductClassificationCatalogTest` vẫn
  **OK (11 tests, 21 assertions)**; ô chọn của màn Loại sản phẩm vẫn đủ 444 thuộc tính + 40 thuế suất.
  🐞 **6 lỗi IM LẶNG bắt được khi làm** (test xanh không bắt được, phần lớn chỉ lộ khi mở trình
  duyệt / gọi API thật): cú pháp `CatalogHistoryService` · `LogsCatalogHistory` hard-code
  `status === 2` nên bản ghi ERP khoá bị ghi nhãn `unlock` · `entity-type="origins"` sót ở 4 màn
  copy · lệch tên component làm popup màn Thuộc tính không mở · rule mã ghi cứng `unique:brands`
  ở 3 màn (đã tạo thật 3 dòng trùng mã rồi mới lộ) · `OrderCodeService` thiếu `parentConfig()` nên
  validate import báo hợp lệ mà ghi xuống nổ NOT NULL.
  Kiểm chứng cuối: **11/11 bảng khớp chính xác số dòng mốc ban đầu, 0 bản ghi rác**; 74 mục trong
  `CatalogHistoryService::TABLES` và `ExportColumnRegistry`; 22/22 quyền 1590-1611; khoá cấu hình
  không trùng nhau lẫn không trùng 6 màn Phase 0; grep tự kiểm skill `erp-to-hrm-screen` sạch;
  gate quyền kiểm cả 2 chiều (403 khi thu hồi).
  🧪 **Bộ e2e Phase 1 (21/09)**: `e2e/tests/master-data/product-catalog-common.api.spec.ts`
  **77 ca (11 màn × 7) — 77 passed** + `product-catalog-ui.spec.ts` **18 ca — 18 passed**.
  Chạy: Node 20 + `--project=api|chromium --no-deps --workers=1`. ⚠️ `HRM/e2e` không trong git.
  🐞 Bộ UI bắt thêm **3 lỗi FORM** mà test API không thấy: modal Thương hiệu + Hãng sản xuất
  **thiếu hẳn ô Công ty**; cả 4 màn có mã dùng `V2BaseCodeInput` prefix cứng `CSKD.` (mâu thuẫn
  rule BE vì mã ERP là chuỗi tự do); và 4 màn đó hiện tooltip của "chính sách kinh doanh".
  Đã vá ở `4ff39a185`.
  ⚠️ Bẫy Playwright mất 7 lượt mới ra: `hasText: /^Lưu$/` khớp 0 phần tử — regex KHÔNG được chuẩn
  hoá khoảng trắng và tên nút còn dính glyph icon; phải lọc bằng CHUỖI rồi loại "Lưu & Tiếp tục".
  Dữ liệu sau khi chạy e2e: 11/11 bảng y hệt trước, 0 bản ghi rác.
  ⚠️ DB local đã đụng: `permissions` 1.710→1.744 · `role_has_permissions` 16.654→16.688 (cấp 34
  quyền cho role #18) · hãng #394 hoàn nguyên đủ trường nhưng `updated_by/updated_at` mang dấu vết
  lần sửa thử. 61 migration vẫn cố ý chưa chạy.
  ✅ **21/09 — ĐÃ COMMIT toàn bộ, CHƯA merge** (user chốt chỉ commit ở nhánh hiện tại):
  `hrm-api` `19027c245` · `hrm-client` `810d2e089` + `371d63a5a`. Hai repo sạch; nhánh vượt
  `gop_db` local 16/15 commit. `php -l` sạch, diff không phình do CRLF.
  ✅ **`221cda7b2` KHỎI cherry-pick**: `origin/gop_db` đã có bản vá y hệt ở `68ecde36e "fix bug"`
  (cùng hash nội dung `1a05f29eb..277787f3b`) → merge lúc nào cũng sạch.
  ⚠️ **`origin/gop_db` đã đi trước**: +3 commit (api), +6 commit (client — **119 file**: migrate
  SmartFilterPanel các màn Finance, đổi URL `regulation-config`). Khi merge phải `pull` trước và
  **chạy lại e2e** vì bộ lọc dùng chung vừa bị đụng.
  ⚠️ **Bộ e2e KHÔNG nằm trong git** — 77 ca API + 18 ca UI ở `HRM/e2e/` chỉ có trên máy.
  🔁 **Cập nhật 21/09 (chiều)** — user chốt **bỏ ô Công ty** ở Thương hiệu / Hãng sản xuất, máy chủ
  tự gán `company_id` theo NGƯỜI TẠO (đường SỬA không đụng vào). Đảo ngược điểm 1 của 3 lỗi form ở
  trên. Cùng lúc dọn **bố cục 6/11 màn** cho mỗi hàng đủ 12 cột (Đơn vị tính đang cộng ra 15 → rớt
  dòng), và vá **1 gate quyền chết im lặng**: màn Loại file đính kèm khai FE
  `'Quản lý danh mục LOẠI file đính kèm'` lệch seeder `'Quản lý danh mục file đính kèm'` → mất sạch
  Tạo mới/Sửa/Xoá/Khoá mà console sạch và 77 ca API vẫn xanh. Thêm 11 ca e2e đo bố cục popup (cũng
  là chốt chặn cho gate quyền: không bấm được "Tạo mới" thì ca đỏ). **Chưa commit** — 4 file
  `hrm-api`, 7 file `hrm-client`.
  🔧 **Môi trường đã chuẩn bị (20/09):** chạy chọn lọc 12 migration `Modules/MasterData` (7 bảng
  Phase 0 trước đó KHÔNG tồn tại trên DB local) + chèn tay 12 quyền 1574-1585 (1.710 → 1.722).
  Bộ test Phase 0 từ **11 ERROR → OK (11 tests, 21 assertions)** = mốc gốc để so sau khi sửa nền.
  ⚠️ DB local còn **61 migration pending** — CỐ Ý không chạy (có `drop_hrm_customer_tables` và
  3 migration `backfill_created_by...`). Cần rà riêng trước khi deploy.
  Dựng **11 màn danh mục** bên HRM trên ĐÚNG 11 bảng ERP đang chạy (model 39.796 · code đặt hàng
  8.664 · đơn vị tính 145 · thuộc tính 446 · đơn vị thuộc tính 103 · thương hiệu 1.250 · hãng sản
  xuất 1.071 · xuất xứ 113 · file đính kèm 8 · mã màu **0** · thuế suất 40).
  **KHÔNG migration bảng mới** — DB đã gộp, HRM và ERP dùng chung y hệt một bảng; chỉ 22 quyền mới
  (guard `api`, id 1590-1611, group 'Danh mục hàng hóa').
  8 quyết định user chốt: giữ trạng thái **0/1** của ERP (HRM tự quy đổi, chuẩn HRM là 1/2) ·
  2 quyền/màn · hãng sản xuất **chỉ CRUD** (3 màn con KPI ở lại ERP) · **giữ nguyên màn ERP cũ**,
  không đụng repo ERP · có Lịch sử đủ 2 nơi · cả 11 màn có Import + Xuất Excel · **mở rộng nền
  `BaseCatalog*` của Phase 0** thay vì dựng nền thứ hai (sửa 5 chỗ trong 4 file) · hãng sản xuất
  **KHÔNG** ghi đè `company_id` sang `products`.
  ⚠️ **Phát hiện nặng nhất:** `ManufacturesController@update` của ERP (dòng 271-276) mỗi lần Lưu
  hãng ghi lại `company_id` cho MỌI hàng hoá của hãng — hãng #394 = **4.514 dòng**, và **367 hàng
  hoá** đang lệch sẵn → port nguyên là âm thầm đổi công ty 367 dòng đó. Đã chốt KHÔNG port.
  ⚠️ Màn Thuộc tính **bỏ trường "Nhóm hàng hoá"** (pivot `attribute_groups` 2.434 dòng trỏ bảng
  `groups` nằm trong nhóm BỎ); vai trò đó Phase 0 đã thay bằng `product_type_attributes`.
  ⚠️ `tax_rates.created_by/updated_by` là **varchar** (giá trị thật vẫn là id) → ép kiểu khi join.
  ⚠️ 8/11 bộ quyền guard `web` của ERP đang **dùng chung** với nhóm "Hàng hoá có sẵn" (vẫn ở ERP)
  → tuyệt đối không đổi tên, không xoá.
  3 đợt: (1) sửa nền + xuất xứ/đơn vị thuộc tính/model — chốt chặn chứng minh không vỡ Phase 0 ·
  (2) đơn vị tính/thuộc tính/thương hiệu/hãng SX → rồi code đặt hàng (`barcodes.manufacture_id`
  NOT NULL) · (3) file đính kèm/mã màu/thuế suất.
  Khảo sát: `.plans/gop-db/quan-ly-hang-hoa/chuyen-danh-muc-lien-quan/khao-sat.md`
  Spec: docs/superpowers/specs/gop-db/2026-09-20-chuyen-danh-muc-lien-quan-design.md

- finance-borrow-extend-request → @namdangit → .plans/gop-db/finance-borrow-extend-request/plan.md
  Trạng thái: 🟢 **XONG 9/9 phase + nghiệm thu trình duyệt (24/09). CHƯA commit — chờ user chốt.**
  Nhánh `feat/finance-borrow-extend-request` ở CẢ 2 repo (tách từ `origin/gop_db`).
  Màn ERP `borrowExtendRequest` — 1 action, 2 preset (`?type=all` / `?type=for-approve`); route
  `forAccounting` là route chết, không port. BE: entity + history + notify + 12 route + 2 bản in + 1
  migration bảng MỚI `borrow_extend_request_history`. FE: danh sách + tạo + chi tiết/duyệt + 2 popup.
  E2E tầng service 48/48 đạt (rollback sạch).
  ⚠️ GOTCHA: mã trạng thái 3/4/5 **KHÁC NGHĨA** với màn sinh đôi `prepick-extend-requests`
  (3 = Không duyệt / 4 = Chờ TP / 5 = Chờ BGĐ, bên hàng giữ là Đang tạo / Chờ BGĐ / Chờ TP).
  ⚠️ GOTCHA: **KHÔNG tạo quyền mới** — 6 quyền đã có; `due_configs` id=25 cũng có sẵn.
  ⚠️ 11 lỗi ERP đã vá bên HRM (design.md mục 9), trong đó **#6 là LỖ PHÂN QUYỀN**: vào URL trần
  (không `?type=`) thì người không có quyền xem vẫn thấy toàn bộ 1.210 phiếu của công ty (đúng ra 18).
  Tóm tắt: `.plans/gop-db/finance-borrow-extend-request/design.md`

- finance-borrow-stock-list → @namdangit → .plans/gop-db/finance-borrow-stock-list/plan.md
  Trạng thái: 🟢 **XONG — user xác nhận dữ liệu 2 cổng đã khớp trên dev (24/09).**
  Lỗi: màn "Hàng sắp hết hạn mượn" port NHẦM biến thể. ERP có 2 màn ở 2 phân hệ dùng chung
  truy vấn — `expiringBorrow` (Thông báo, bó `created_by=mình`) và `accountingExpiringBorrow`
  (Kế toán kho → Mượn hàng, không bó người). Mục menu HRM ứng với bản KẾ TOÁN mà lại làm bản
  cá nhân ⇒ **74 → 6 phiếu**. Đã bỏ `created_by` khỏi `applyExpiringWindow()`, đo lại 74 ✓.
  Nhánh `feat/finance-borrow-stock-list` ở CẢ 2 repo. Verify bắt được 2 lỗi đã sửa: khoá
  `code` của dòng con trùng `column.key` của dòng cha (bảng tự điền mã hàng sang cột Yêu
  cầu) · deep watcher Vue 2 đưa newVal/oldVal cùng object nên bộ lọc không tải lại bảng.
  2 màn báo cáo CHỈ ĐỌC port từ ERP: `Danh sách hàng mượn` (`warehouseInfo.borrowIndex`) và
  `Hàng sắp hết hạn mượn` (`warehouseInfo.expiringBorrow`). Bảng 2 tầng: phiếu mượn → mặt hàng.
  Nguồn là `product_export_requests` (type=3, borrow_status=2, còn nợ) — KHÔNG bảng mới, KHÔNG migration.
  User chốt: siết quyền theo cấp (ERP không kiểm gì) · dòng mở rộng ▸ thay `rowspan` ·
  bỏ 2 biến thể Kế toán kho.
  ⚠️ GOTCHA: **KHÔNG tạo quyền mới** — 3 quyền `Xem phiếu hàng mượn theo …` đã có
  (`web` 100890-892 / `api` 1565-1567), 3 màn hàng mượn khác đang dùng.
  ⚠️ GOTCHA: đừng nhầm `BorrowStockService` (tồn đang treo ở luồng khác, ĐÃ CÓ) với
  `BorrowStockReportService` (báo cáo, sắp viết) — y như cặp `PrepickStockService` / `…ReportService`.
  Khuôn copy: cặp màn song sinh bên hàng giữ (`finance-prepick-stock-list` + `finance-prepick-expiring`).
  ⚠️ GOTCHA: **lỗi ERP** — ô lọc Kho đổ dropdown từ `accounting_warehouses` nhưng query lọc
  `warehouses`; id trùng nhau nhưng là kho KHÁC ⇒ ERP chọn kho này lọc ra kho kia. Bản HRM
  lấy đúng `warehouses` và chỉ kho đang có phiếu mượn (7 thay vì 55).
  ⚠️ **ĐÃ BƠM DỮ LIỆU DEMO VÀO DB LOCAL** (user cho phép 23/09): 6 phiếu đổi `created_by`→13
  và `return_date` để test đủ 3 badge + màn Sắp hết hạn. Sao lưu ở bảng
  `_bak_borrow_test_20260923`, khôi phục bằng
  `.plans/gop-db/finance-borrow-stock-list/khoi-phuc-du-lieu-test.sql`.
  **Phải khôi phục trước khi chạy harness đối chiếu quyền HRM vs ERP.**
  Tóm tắt: `.plans/gop-db/finance-borrow-stock-list/design.md`

- task-11566-audit-name (#11566) → @namdangit → .plans/gop-db/task-11566-audit-name/plan.md
  Trạng thái: code xong trên `gop_db`, CHƯA commit (03/10/2026) — 202 file BE + 13 FE. Chờ user review, chốt mã 255/50, test.

- admin-tra-soat-theo-phieu (#11523) → @namdangit → .plans/gop-db/admin-tra-soat-theo-phieu/plan.md
  Trạng thái: đã push nhánh `task_11523` + merge vào `develop` (30/09/2026). Chưa merge về gop_db; server cần chạy migration.

- department-lead-employee-id → @namdangit → .plans/gop-db/department-lead-employee-id/plan.md
  Trạng thái: ✅ **Đã deploy PROD + migrate (25/09/2026)** — commit `484ee95fd` + `32246d20c` trên `gop_db`. Còn: nghiệp vụ chốt 14 phòng ERP ghi khác HRM cũ.
  PROD sau gộp DB: `departments.department_lead_id`/`parts.part_lead_id` là `employees.id` (nghĩa ERP) nhưng HRM đọc như
  `employee_infos.id` → 75/84 phòng, 20/25 bộ phận hiện sai trưởng. Chốt: giữ nghĩa ERP, HRM quy đổi bằng custom cast.

- vehicle-catalogs → @namdangit → .plans/gop-db/vehicle-catalogs/plan.md
  Trạng thái: 🟢 **BE + FE xong, đã test API thật (22/09/2026). Chưa verify trình duyệt, chưa commit.**
  Port 5 danh mục Xe từ ERP sang nhóm menu "Danh mục xe" của phân hệ Danh mục chung:
  Hãng xe · Dòng xe · Phân loại xe · Model xe · Đời xe (dùng lại bảng ERP `vehicle_*` trên DB gộp).
  Chốt: thêm cột `code` + sinh mã cho 1.730 bản ghi cũ; **giữ nguyên `status` 1/0 của ERP**, HRM
  ánh xạ 0 ⇄ 2 ở Entity; xóa bị chặn khi còn danh mục con hoặc còn bản ghi nghiệp vụ tham chiếu
  (`products.model_id` gần 39.000 dòng); đủ Xuất Excel + Import 5 màn; 10 quyền mới id 1590–1599.
  Có sửa 1 file dùng chung (user duyệt): thêm hook `duplicateNameScopeColumns()` vào
  `ImportsCatalogRows` để giữ luật trùng tên theo cấp cha của ERP.

- user-profile-performance → @namdangit → .plans/gop-db/user-profile-performance/plan.md
  Trạng thái: 🟡 **Mới lên plan (22/09/2026), chưa code.** Chờ user chốt phạm vi Phase 2–3.
  Giảm tải API `user-profile` (1,45 MB · 0,5–0,7 s CPU · 37 query, chạy ở mọi lần tải trang).
  Đã đo: departments 442 KB (86% là 2 quan hệ lồng) · permissions trả TRÙNG 2 lần 199 KB ·
  employees 258 KB. Không tách endpoint lazy vì `state.departments` dùng ở 119 file.
  Hạ tầng đã sửa cùng ngày (ngoài repo): bật `gzip_types` cho nginx server dev → payload −91%;
  `pm.max_children` 5 → 12. Chi tiết: `.plans/gop-db/user-profile-performance/design.md`.

- smart-filter-panel-migration → @namdangit → .plans/gop-db/smart-filter-panel-migration/plan.md
  Trạng thái: 🟢 **XONG Phase 0–6, đã verify trên trình duyệt** (21/09/2026). **Chưa commit, chưa push.**
  Gom toàn bộ bộ lọc về **một** panel: 56 file chuyển `V2BaseFilterPanel` → `V2BaseSmartFilterPanel`,
  51 file đã dùng Smart nhưng thiếu `floating` được bật + dọn placeholder trùng nhãn.
  `components/V2BaseFilterPanel.vue` **đã xoá**.
  4 component dùng chung được bổ sung (user duyệt từng cái): panel truyền `required`;
  panel + `V2BaseFilterFieldControl` nhận `in-modal` (→ `V2BaseSelectInModal`);
  control nhận `field.multiple`; `V2BaseFieldCategoryApplicationFilter` nhận `floating`.
  Skill `list-page` đã chốt: panel duy nhất · `floating` bắt buộc · khoảng cách trên/dưới khối lọc `pb-2` (12px).
  **Đã verify Playwright** (20 màn): sửa thêm 6 lỗi UI — nhãn float đè chip, viền đôi ô chọn nhiều,
  ô chọn nhiều 42px, 62 ô ngày 32px, 9 ô tìm-từ-xa thiếu `height`, ô Tag 32px (gốc chung:
  CSS `.ff` thua specificity CSS riêng của control). Gộp nốt 31 cặp "từ ngày – đến ngày" ở 30 màn.
  Kết quả: 0 màn thiếu `floating`, 0 màn tách ô ngày, mọi ô lọc cao đúng 36px. Tổng 113 file.
  Bước tiếp: user duyệt rồi commit/push.

- quy-hoach-lai-menu-phan-he → @junfoke → .plans/gop-db/quy-hoach-lai-menu-phan-he/plan.md
  Trạng thái: **CODE DONE CẢ 5 NHÓM + VERIFY BROWSER khung menu** (16/09/2026).
  Sắp xếp lại nhóm/phân hệ/menu `hrm-client` theo 5 sheet của sơ đồ chốt 04/09/2026 —
  tách 3 phân hệ mới (Meeting, CSKH trước bán, An toàn 5S), đổi tên hàng loạt, dời chức năng.
  ⚠️ Đọc sheet phải xem **màu nền + gạch ngang** (CSV không mang): gạch = bỏ/chuyển đi, vàng = làm sau.
  Đã tách `/human/settings` thành 3 màn mới (Tính lương / Quản trị hệ thống / Bảo hiểm) và cho
  menu ngang hiện xám mờ mục chưa có màn (sửa `Topbar.vue`).
  Thêm 4 phân hệ: Meeting · An toàn 5S · CSKH trước khi bán · Tra cứu - thông báo.
  ⚠️ 3 lỗi do menu mới đã sửa: màn chọn phân hệ vỡ khi phân hệ thiếu `image`, cánh hoa cắt mất
  phân hệ thứ 9, menu ngang tràn.
  **Cập nhật 16/09 (chiều) — Phase 11:** đã GỘP phân hệ `decision` vào `operation`, đổi tên
  **"Văn bản nội bộ"** (subtext "Quyết định, Quy chế công ty") — đảo quyết định #5 của design.md.
  36 link dời sang `operation-hub.js`, xoá `default-menu/decision.js`, 143 page `/decision/*`
  chuyển `layout: 'default-sidebar'` (Topbar chỉ dựng 2 cấp, menu hub 3 cấp). Verify DOM +
  `doi-chieu-menu.py` 0 lệch/22 phân hệ + test ca không quyền.
  **Cập nhật 17/09 (Phase 16-21):** user duyệt lại TỪNG PHÂN HỆ. Xong 3 phân hệ — CSKH trước bán ·
  Bán hàng · Công việc (dời màn giữa phân hệ, dựng menu Báo cáo/Phê duyệt theo kiểu hub, tách mục
  lên cấp 1, gom nhóm Bàn giao công việc). Thêm: popup topbar đổi tên nhóm lõi thành **QUẢN TRỊ** +
  đổi thứ tự 5 nhóm; Kho/Mua hàng/Vận chuyển gắn `erpPath` đi thẳng ERP.
  Chốt phiên: **28 phân hệ · 357 link · 3 link trùng** (ngoại lệ có sẵn), `doi-chieu-menu.py`
  **0 mục thiếu / 22 phân hệ**. Spec đầy đủ đã viết:
  `docs/superpowers/specs/gop-db/2026-09-16-quy-hoach-lai-menu-phan-he-design.md`.
  **Bước tiếp:** duyệt nốt các phân hệ còn lại (Meeting · Văn bản - Hồ sơ pháp lý · Tài chính ·
  CSKH sau bán · nhóm NHÂN SỰ), rồi làm nhóm A của "DANH SÁCH TREO" cuối `plan.md`
  (verify từng màn con + chạy e2e).
  Spec: docs/superpowers/specs/gop-db/2026-09-16-quy-hoach-lai-menu-phan-he-design.md | Tóm tắt: .plans/gop-db/quy-hoach-lai-menu-phan-he/design.md

- bao-cao-ket-qua-du-an-tkt → @namdangit → .plans/gop-db/bao-cao-ket-qua-du-an-tkt/plan.md
  Trạng thái: **CODE XONG + REVIEW TỔNG XONG, CHỜ MERGE (14/09/2026)**. BE + FE + fixture e2e xong,
  bộ e2e **22 ca xanh** (11 API + 11 UI). **21 commit** (10 hrm-client + 11 hrm-api) trên nhánh
  **`tpe-bao-cao-ket-qua-du-an-tkt`**, tách từ **đỉnh `tpe`** ở **cả 2 repo**
  (`hrm-api` `f36a89ae` · `hrm-client` `c07c4a2a`). `merge-tree` với `tpe`: **0 conflict**.
  ✅ **ĐÃ MERGE VÀO `tpe` (14/09/2026), KHÔNG CONFLICT** — user tự merge:
  `hrm-api` `769061693` (kèm `8ca563f93` merge `tpe-develop-assign` vào trước)
  · `hrm-client` `12b6f4f6e`.
  ⛔ **CHƯA PUSH** — `tpe` đang đi trước `origin/tpe` **86 commit** (hrm-api) / **80 commit**
  (hrm-client). Cây làm việc 2 repo sạch.

  ⭐ **REVIEW TỔNG BẮT ĐƯỢC 1 LỖI MÀ CẢ 21 CA E2E ĐỀU KHÔNG THẤY** (bài học lớn nhất của feature):
  `buildLevel()` nhánh không-có-bộ-phận truyền `parentKey` TRẦN, không ghi dấu đã bỏ qua cấp Bộ phận;
  `applyDrillKey()` chỉ lọc AND trên chiều CÓ MẶT trong key ⇒ `dept:5+emp:88` khớp cả dự án có lẫn
  không có bộ phận. Bấm số `1` trên bảng, popup ra `3` dự án — 2 cái thừa đã đếm ở node `part:9` bên
  trên nên **bị liệt kê ở 2 popup khác nhau**; Excel + bản in sai theo.
  **Vì sao lọt lưới:** bảng theo dõi VẪN ĐÚNG (2 đẳng thức bất biến + cha = tổng con đều xanh) — lỗi
  nằm ở ĐƯỜNG TỪ BẢNG SANG POPUP, mà không ca nào so *"số vừa bấm = total của popup"*. Hệ tự kiểm
  canh BẢNG, không canh CẦU NỐI. Đã sửa (gắn `part:0`) + thêm **ca 10** chặn cả lớp lỗi này.
  ⚠️ DB local có **0 cặp (phòng ban, nhân viên)** kích hoạt được lỗi ⇒ ca 10 tự nó xanh cả trước lẫn
  sau khi sửa; giá trị thật đã chứng minh bằng dữ liệu giả rồi xoá sạch. **Kiểm trên production:**
  `SELECT COUNT(*) FROM (SELECT main_sale_department_id d, main_sale_employee_id e,
  SUM(main_sale_part_id IS NULL OR main_sale_part_id=0) n, SUM(main_sale_part_id>0) h
  FROM prospective_projects WHERE IFNULL(is_parent_project,0)=0 GROUP BY 1,2 HAVING n>0 AND h>0) t;`

  **Thay đổi 14/09 theo yêu cầu user:** ô Công ty vẫn BẮT BUỘC chọn, KHÔNG có mục "Tất cả công ty",
  nhưng **mặc định đổi từ `companies[0]` sang CÔNG TY CỦA USER ĐĂNG NHẬP**. Trước đó user mở màn ra
  số của pháp nhân khác công ty mình, "Xoá lọc" cũng nhảy sang pháp nhân đó. BE trả `default_company_id`
  clamp qua `clampCompanyId()`; công ty hồ sơ không nằm trong danh sách được phép thì rơi về công ty
  đầu danh mục (ô bắt buộc, để rỗng là màn chết).
  Màn báo cáo **MỚI** `/assign/report/prospective-project-results` — theo dõi kết quả thực hiện Dự án TKT
  trong kỳ (Thành công / Thất bại / Đang triển khai) trên 3 trục: Phòng ban · Thị trường · Lĩnh vực Công ty KD.
  Màn `report/prospective-projects` cũ **GIỮ NGUYÊN**, không đụng.
  ℹ️ Tài liệu để trong `.plans/gop-db/` để nằm cạnh cụm mockup báo cáo anh em, **nhưng code làm trên
  nhánh con tách từ `tpe`** (user chốt 13/09) — không phải nhánh `gop_db`.
  **5 quyết định đã chốt (13/09/2026):**
  (1) Cột `Giá trị`: Thành công → giá trị HĐ · Đang triển khai → kỳ vọng · Thất bại → **không hiển thị**, kèm icon ⓘ giải thích.
  (2) ⚠️ **Giá trị hợp đồng TREO** — user đang phát triển **hợp đồng HRM lập từ báo giá HRM**, sẽ KHÔNG dùng HĐ ERP
  ⇒ phase 1 dự án Thành công **chưa có số**: giữ cột `Giá trị HĐ`, mọi ô hiện `—` (không hiện 0), BE tách
  `contractAmountFor()` trả `null` để sau nối đúng 1 chỗ. Hướng cũ `.plans/hrm-quotation-to-erp-contract/` **bị thay thế**.
  (3) `expected_contract_amount` khuyết **42%** (ô "Giá trị HĐ kỳ vọng" không bắt buộc, đo 78/134) → **để trống**,
  KHÔNG lấy `estimated_budget` thay thế.
  (4) Phân quyền: **3 quyền MỚI 1184–1186** (tổng công ty / công ty / phòng ban), tách khỏi 1054–1056 của màn cũ.
  (5) Migration **vá log** cho dự án Thất bại lập trước 18/05/2026 (user chốt "vá luôn").
  **3 phát hiện rút ngắn plan:** 12 bước tiến trình + 3 tên mới **đã có sẵn** trong `ProspectiveProject::STATUS` ·
  bảng `prospective_project_status_logs` + hook ghi log **đã có và đáng tin** (Redmine #11426 vá 4 chỗ đổi bước bằng
  query builder) · `ProspectiveProject::statusAt()` **đã có** ở dòng 686 nhưng chưa ai dùng — và **N+1**, service
  phải tự tính hàng loạt bằng 1 query gom.
  ⚠️ **Bẫy đã đo:** migration backfill `2026_05_18_000002` chỉ sinh **1 dòng log/dự án** (`changed_at = created_at`,
  `status_to` = trạng thái HIỆN TẠI) ⇒ dự án lập trước 18/05/2026 bị khai "đã đóng ngay từ ngày lập" →
  **biến mất khỏi báo cáo, im lặng, không lỗi**. DB local không dính (dự án sớm nhất 03/07/2026), production có.
  Chỉ vá được nhóm **Thất bại** (`closed_at` phủ 11/11 = 100%); nhóm Thành công 9/10/12 **không có mốc nào để suy ngược**
  ⇒ báo cáo chỉ chính xác tuyệt đối với dự án lập từ 18/05/2026 trở đi.
  ⚠️ HĐ ERP `buy_contract2` (923 dòng) **không có cột nào trỏ về dự án TKT**; `prospective_project_id` chỉ có ở 8 bảng.
  Mockup đã duyệt: `bao-cao-ket-qua-du-an-tkt.html` — `__TKT_CHECK__()` trả `ok: true`, 0 dòng sai.
  Spec: docs/superpowers/specs/gop-db/2026-09-13-bao-cao-ket-qua-du-an-tkt-design.md (13 chương) ·
  Design: .plans/gop-db/bao-cao-ket-qua-du-an-tkt/design.md + logic-bao-cao.md ·
  Plan: .plans/gop-db/bao-cao-ket-qua-du-an-tkt/plan.md (20 task / 92 bước, tất cả đã đánh `[x]`).
  **Tự kiểm cuối (Task 18) — 5 lệnh bắt buộc:** 3 lệnh grep (số kiểu `vi-VN` ở FE, `number_format`
  kiểu VN ở BE, cờ quyền hard-code `= true`) đều **RỖNG** trong phạm vi feature · `git diff --stat`
  2 repo toàn **file mới**, không CRLF nào bị phá · hiệu năng lúc mở màn **2 request** (đúng giới hạn
  ≤2), endpoint chính đáp trong **152ms** (< 2s).
  **Đối chiếu Vue thật vs mockup (Task 17):** 6/8 khớp tuyệt đối, 2 chỗ lệch đã sửa và verify lại —
  thứ tự ô lọc (cặp Từ ngày/Đến ngày dời lên ngay sau ô Kỳ) và bề rộng ô Công ty (292px demo → 340px
  theo tên công ty thật dài hơn). Chi tiết đo ở `design.md` mục *Đối chiếu Vue thật với mockup*.
  ⚠️ **Blocker môi trường phát hiện khi kiểm Lịch sử (không phải bug của feature này):** trang chi
  tiết dự án TKT trên **DB local** trả 500 vì bảng `prospective_project_extension_requests`
  (migration `2026_09_11_000003`, tính năng "gia hạn thời gian triển khai" #11153) chưa được chạy —
  chặn cả việc mở mục Lịch sử qua trình duyệt. Đã verify logic log qua tinker thay thế (đọc đúng,
  không trùng mốc); cần verify lại qua trình duyệt trên môi trường đã chạy đủ migration.
  **Còn nợ:** giá trị hợp đồng vẫn `—` mọi dòng (chờ hợp đồng HRM từ báo giá HRM, sửa `contractAmountFor()`
  khi có) · dự án Thành công lập trước 18/05/2026 không suy được mốc đóng · `expected_contract_amount`
  khuyết 42% · `V2BaseTableScroll.vue` port trùng `gop_db`/`permiss_manager` → merge sẽ conflict
  add/add (nội dung giống hệt, lấy bản nào cũng được) · SRS + testcase chưa làm.
  **Deploy môi trường khác — đúng 3 bước:** (1) `php artisan migrate` (1 migration vá log) · (2)
  insert thủ công 3 quyền 1184–1186 + gán role (`role_has_permissions` cần `company_id`), **KHÔNG**
  chạy `PermissionsTableSeeder` (truncate cả bảng `permissions`) · (3) deploy code BE+FE, không có
  cron mới.
  **Bước tiếp theo:** người điều phối review sạch → commit Task 18 → merge nhánh con vào `tpe` ở cả
  2 repo → deploy theo checklist trên.

- bao-cao-theo-doi-giu-hang → @namdangit → .plans/gop-db/bao-cao-theo-doi-giu-hang/plan.md
  Trạng thái: **ĐÃ MERGE + PUSH gop_db (03/10/2026: hrm-api 0d35c84ca · hrm-client f416ab17e · ERP 04b61efc24) + SRS + testcase XONG — CHỜ DEPLOY. ⚠️ ERP prod ĐÃ chạy code ghi root → kiểm ngay DB prod có cột `root_objectable_*` chưa (chưa có = tạo hàng giữ trên ERP đang lỗi). Checkpoint wrap up 03/10 trong plan.md**. Chưa động vào code thật.
  **Chốt 02/10:** chứng từ gốc lưu cột `root_objectable_id/type` (sửa 3 chỗ HRM + **5 chỗ ERP** + backfill) · quyền mới không gán sẵn role · giữ ô Bộ phận · nút Gia hạn dòng xa hạn → màn gia hạn báo rõ lý do · **màn cũ `/finance/prepick-stocks` GIỮ SONG SONG**, báo cáo mới ở `/sale/prepick-tracking` (Bán hàng › Báo cáo › nhóm mới "Hàng giữ") · nhánh `gop_db-bao-cao-theo-doi-giu-hang` cả 3 repo. Chi tiết: bảng cuối `design.md`.
  Tài liệu: `.plans/gop-db/bao-cao-theo-doi-giu-hang/` (design.md 49 mục quyết định · plan.md · mockup HTML) + spec đầy đủ 13 chương ở `docs/superpowers/specs/gop-db/2026-09-12-bao-cao-theo-doi-giu-hang-design.md`. Mockup qua 15 vòng chỉnh, verify Playwright mỗi vòng (ĐO DOM bằng số, không nhìn ảnh), console 0 lỗi.
  **Bổ sung vòng 10 (14/09):** ô lọc **Bộ phận** (cascade sau Phòng ban, 3 trạng thái, mục "Chưa phân bộ phận") · popup đưa 3 cột Ngày bắt đầu giữ / Hạn giữ hiện tại / Số lần gia hạn lên ngay sau "SL đang giữ" · **ghim 3 cột đầu popup** khi cuộn ngang · **In / Xuất Excel** thật (4 đường: 2 nút thanh tiêu đề + 2 nút popup, đều lấy TOÀN BỘ theo bộ lọc, không theo trang).
  ⚠️ **Dữ liệu BỘ PHẬN gần như TRỐNG trên DB thật** — đo `hrm_erp`: chỉ **5/74 nhân viên** đang giữ hàng có bộ phận, **63/2.412 dòng (2,6%)**, **1/17 phòng** đang giữ hàng có chia bộ phận (25 bộ phận / 84 phòng toàn hệ thống). Vì vậy bộ phận chỉ là **Ô LỌC**, KHÔNG thành cấp của cây (thêm cấp thì 16/17 nhánh đẻ "Chưa phân bộ phận" ôm gần hết bảng). Ô lọc phải xử 3 trạng thái, không bao giờ để rỗng im lặng. **Cần hỏi nghiệp vụ** có kế hoạch gán bộ phận cho NV kinh doanh không.
  ⚠️ **Bẫy GHIM CỘT — mất 3 lần đo mới ra:** popup mở kèm `transform: scale(.96)`, mà `getBoundingClientRect` trả toạ độ SAU transform → mọi khoảng cách bị nhân 0,96 (đo 301.44px thay vì 314px), ghim lệch 13px, 3 cột đè nhau, **màn hình không báo lỗi gì**. `ResizeObserver` KHÔNG cứu được (transform không đổi kích thước layout). Phải dùng **`offsetLeft`** — số đo layout, miễn nhiễm transform. 2 bẫy phụ: `border-collapse: collapse` làm ô ghim mất viền (vẽ lại bằng `box-shadow inset`) · nền ô ghim phải ĐẶC, đổi đúng theo hover.
  ⚠️ **Bẫy đổ HTML ra text phẳng (bản in / Excel):** các mẩu `<span>` dính liền — `"VT.00611-Ống thủy lực"`, `"Công ty CP Đóng tàu Hạ Long21TPHP-176"` → chèn khoảng trắng **2 phía** mỗi span, mã phụ `.code-sub` tách bằng `" · "`. Thụt lề cây phải dùng **khoảng trắng CỨNG ` `** (HTML gộp dấu cách thường, Excel cắt khoảng trắng đầu ô).
  **Bổ sung vòng 11 (14/09):** 2 nút **Gia hạn** / **Huỷ giữ** (icon + chữ, dạng viền) nằm TRONG ô "Hạn giữ hiện tại" — KHÔNG tách cột riêng (bảng vẫn 15 cột). Chỉ hiện ở chế độ **"Hàng giữ của tôi"**: ngoài chế độ đó là hàng người khác đứng tên. Cả 2 là ĐIỀU HƯỚNG sang màn lập phiếu → không hỏi xác nhận (`button-convention` 6c).
  ⚠️ **Nút "Gia hạn" ở dòng TRONG HẠN là nút chết** — màn lập phiếu gia hạn (`getDataToCreate()`) chỉ nhận lô `expire_date <= hôm nay + configs.warning_day`, nên dòng còn xa hạn bấm sang đó **không thấy dòng nào**. Đã nêu rủi ro, user vẫn chọn hiện ở mọi dòng ⇒ **lúc code BE BẮT BUỘC** xử 1 trong 2: màn gia hạn báo rõ lý do khi dòng chưa tới ngưỡng, hoặc hỏi khách để nới điều kiện.
  ⚠️ **Huỷ giữ trừ tồn FIFO theo `expire_date` tăng dần** trên bộ 4 (hàng hoá × NV × khách × công ty) — bấm ở một dòng **không đảm bảo huỷ đúng dòng đó**. Thực tế 2.300/2.355 nhóm (97,7%) chỉ còn 1 dòng nên đa số trùng khớp, nhưng màn lập phiếu hủy phải cho thấy rõ đang hủy lô nào, đừng hứa "hủy đúng dòng vừa bấm".
  ⚠️ **Bẫy nhét nút vào ô dữ liệu:** bản in/Excel lấy chữ từ chính ô HTML nên ô hạn giữ đổ ra `"03/08/2026 quá hạn 40 ngày Gia hạn Huỷ giữ"` — phải **gỡ hẳn `.row-acts`** trước khi lấy text.
  **Rà nút theo `button-convention` (15/09):** phát hiện & sửa **5 lỗi ở nút CŨ** — "In báo cáo" là chữ bị cấm (→ "In danh sách") · "Xuất Excel danh sách" 4 từ vượt trần 3 từ (→ "Xuất Excel") · Thoát/Huỷ không đứng cuối footer · 4 nút Đóng/Hủy thiếu icon · nút Xuất Excel trong popup tô teal trong khi nút cùng việc ở thanh tiêu đề xanh lá (→ `#16a34a`). **3 điểm vẫn lệch skill do USER CHỐT:** nhãn "Huỷ giữ" (thay "Hủy") · nút trong bảng icon+chữ (thay `V2BaseIconButton`) · nút Huỷ giữ dạng viền (thay `primary status="danger"` nền đỏ đặc).
  ℹ️ **`button-convention` tự mâu thuẫn về nút In**: mục 2 xếp `primary`, mục 2b xếp `secondary/tertiary`. Mockup xử theo ngữ cảnh (In = action chính của popup chọn chế độ in → primary; In danh sách ở footer popup chi tiết = bổ trợ → secondary). Nên làm rõ trong skill.
  Thiết kế lại màn **`/finance/prepick-stocks`** (giữ nguyên URL) thành báo cáo theo dõi, style port nguyên khối từ `../bao-cao-ket-qua-du-an-tkt/`.
  **5 quyết định đã chốt:** tồn giữ **HIỆN TẠI**, không có bộ lọc Kỳ · 2 tiêu chí **Theo nhân viên** (Phòng ban ▸ NV ▸ Hàng hoá) và **Theo hàng hoá** (Hàng hoá ▸ NV) · chỉ tiêu **Tổng / Trong hạn / Đến hạn / Hết hạn** · **KHÔNG** đụng màn `/finance/prepick-expiring` · cấp tổng đo bằng **SỐ LÔ GIỮ**, số lượng + đơn vị chỉ hiện ở dòng hàng hoá.
  ⚠️ **Lý do đo bằng số lô:** `prepick_details.qty` là đơn vị cơ bản của từng mặt hàng (cái/kg/mét/bộ) — cộng số lượng ở cấp Phòng ban/Nhân viên ra con số vô nghĩa. Màn cũ né được vì tầng 1 luôn là 1 mặt hàng.
  **Bổ sung vòng 2:** ngưỡng "Đến hạn" (chỉ đúng hôm nay) đổi thành **"Sắp hết hạn" có ô cấu hình số ngày** ngay trên thanh lọc (mặc định `configs.warning_day` = 7) · thêm cột **Tồn hiện tại** + **SL đang giữ** (chỉ có số ở dòng hàng hoá, tự ẩn khi bảng không render dòng hàng hoá) · thêm cột **Số lần gia hạn** bấm ra popup lịch sử xếp CŨ → MỚI · bỏ cột Tỷ trọng quá hạn · popup danh sách lô đổi "Hạn giữ" → **"Hạn giữ hiện tại"**.
  **Bổ sung vòng 3:** cột chính đo **KÉP theo cấp** — dòng Phòng ban/NV = **số mã hàng** (`14 Mã`), dòng Hàng hoá = **số lượng** theo ĐVT đang chọn (`157 Cái`); 3 cột hạn đi theo cùng đơn vị đó (⚠️ ở dòng tổng **đếm chồng lấn**, cộng 3 cột > cột chính: đo thật 14 Mã vs 25) · bộ cột hàng hoá **bám đúng ERP `prepickIndex.blade.php`** (Mã · Đơn vị có select đổi ĐVT · Model · Thương hiệu · Tồn hiện tại · SL giữ), **bỏ cột Kho** vì `prepick_details` không có kho · 5 cột thuộc tính hàng hoá tự ẩn khi bảng chưa render dòng hàng hoá.
  ⚠️ **Gotcha BE nặng nhất — "Số lần gia hạn" KHÔNG cộng lên dòng tổng, cũng KHÔNG đếm gộp theo nhân viên:** gia hạn phát sinh trên **từng lần yêu cầu giữ**, `moveToExpireDate()` lại **trừ lô cũ, cộng sang lô MỚI** chứ không sửa `expire_date`. Đo trên 2.412 lô đang tồn: đếm log trên chính lô → tối đa **3 lần** (SAI, chỉ thấy lần cuối) · đếm theo **CHUỖI lần ngược của từng lô** → tối đa **10 lần** (ĐÚNG, TB 1,31 · 206 lô ≥ 5 lần) · gộp theo bộ 4 NV×KH×hàng hoá → **15 lần** (SAI, gộp nhiều lần giữ). Cột này **chỉ nằm trong popup danh sách lô**. Chứng từ gốc cuối chuỗi: Phiếu xuất giữ 1.794 · Nhập hàng cho khách 341 · Điều chuyển giữ 93 · không xác định 184.
  **Bổ sung vòng 4:** ô "Hạn giữ hiện tại" tô màu theo ngưỡng cảnh báo (xanh/vàng/đỏ, cùng bảng màu 3 cột hạn) · bảng có hàng hoá **luôn có cột ĐVT riêng**, các ô số **bỏ hậu tố đơn vị** (dòng tổng vẫn giữ nhãn "Mã") · popup **luôn giữ 2 cột Mã hàng + Tên hàng** kể cả khi mở từ đúng 1 hàng hoá · **mã hàng là cột riêng đứng TRƯỚC tên hàng** ở cả bảng chính lẫn popup · mọi tiêu đề popup dùng khuôn **"Mã hàng - Tên hàng"**.
  **Bổ sung vòng 5:** "Số lượng" → **"Số lượng giữ"** · **bỏ cột Mã hàng riêng** (làm vỡ cấu trúc cây), gộp lại thành **"Mã hàng - Tên hàng"** trong 1 ô với style mã riêng (`.prd-code`) — áp toàn báo cáo · **sort** 4 cột Mã-Tên hàng / Nhân viên / Hạn giữ / Ngày bắt đầu giữ (chu kỳ A→Z → Z→A → về mặc định) · popup hiện nhân viên dạng **"Tên - Phòng ban"** · bảng chi tiết thêm **Số hợp đồng** + **Tổng thanh toán** (bấm ra popup phiếu thu) — giữ hàng có 2 kiểu theo/không theo hợp đồng, đều có khách hàng (thật: 501/1.673 phiếu), tiền lấy `bill_income_details` lọc `objectable_type = FirmContract`, cộng `income_money_real` (thật: 6.734 dòng / 26.349 tỷ) · **thứ tự mặc định toàn báo cáo**: chứng từ MỚI → CŨ, riêng hàng giữ **quá hạn nhiều nhất → trong hạn**.
  **Bổ sung vòng 6:** cột **Tồn hiện tại** chỉ còn ở tiêu chí **Hàng hoá** (bỏ khỏi popup chi tiết và khỏi tiêu chí Nhân viên — tồn là số của cả công ty, so với số giữ của từng lô/từng người là so 2 đại lượng không so được) · thêm bộ lọc **Hình thức giữ** (Tất cả / Giữ theo hợp đồng / Không theo hợp đồng) · **sửa định nghĩa đo**: quyết định theo DÒNG chứ không theo cấp — dòng gom đúng 1 mã hàng thì đo bằng **số lượng**, gom nhiều mã mới đo bằng **số mã** (định nghĩa cũ "cấp Nhân viên = số mã" sai ở tiêu chí Hàng hoá vì ở đó số mã luôn = 1).
  **Bổ sung vòng 7:** **bỏ chế độ đổi đơn vị** trên báo cáo, luôn quy về ĐVT cơ bản (đổi được thì mỗi người xem một kiểu, số trên màn lệch số xuất Excel) · khối tổng hợp 1 đổi thành **"Tình trạng theo yêu cầu giữ"** — đếm theo CHỨNG TỪ GỐC: Tổng yêu cầu đang giữ hàng · Yêu cầu sắp hết hạn · Yêu cầu đã hết hạn (⚠️ 2 nhóm sau **chồng lấn**: 1 yêu cầu đẻ nhiều lô hạn khác nhau) · popup sort được **7 cột** (thêm Phòng ban, SL đang giữ, Khách hàng).
  **Bổ sung vòng 8:** tiêu đề cột có sort **không đổi màu nền khi hover** (nền header sáng + chữ teal, tô nền teal đậm là mất chữ — phải ghi đè cả rule hover sẵn có trong style gốc) · khối hạn giữ thêm ô **"NV có hàng giữ quá hạn"** (đếm distinct nhân viên có ≥ 1 lô quá hạn, khác "Yêu cầu đã hết hạn" vì 1 người ôm nhiều yêu cầu).
  **PHÂN TRANG (chốt 13/09/2026, đã làm vào mockup):** bảng chính phân trang theo **NODE CẤP 1** (mỗi trang N node + toàn bộ cấp con), mặc định 25, chọn 10/25/50/100 — KHÔNG phân trang theo dòng render vì bảng là cây, bung/thu sẽ đẩy nội dung chạy sang trang khác. ⚠️ **Dòng TỔNG + dải tổng hợp luôn tính trên TOÀN BỘ dữ liệu đã lọc**, khi làm BE là 2 truy vấn tách bạch. STT chạy tiếp theo toàn bộ (trang 2 bắt đầu từ 11). Popup phân trang theo dòng, mặc định 20; popup gia hạn/phiếu thu không phân trang. Sort chạy trên toàn bộ rồi mới cắt trang → đổi sort phải về trang 1. BE: sort ở server, cấp sâu nhất lazy load (1 NV có tới 151 mã), In/Excel lấy toàn bộ.
  **PHÂN QUYỀN (chốt 13/09/2026):** báo cáo dùng **ĐÚNG 1 quyền** `Xem báo cáo giữ hàng theo tổng công ty` — có quyền thì ô Công ty hiện kèm mục "Tất cả công ty", không quyền thì **ẩn hẳn ô** và khoá theo công ty trong hồ sơ nhân sự. ⚠️ **Quyền này CHƯA TỒN TẠI trong bảng `permissions`** (gần nhất là `Xem phiếu hàng giữ theo tổng công ty` id 100839 — của màn PHIẾU, đừng dùng nhầm), phải thêm vào `PermissionsTableSeeder`. KHÔNG dùng bộ 3 quyền phạm vi mà `PrepickStockReportService` đang áp cho màn cũ. BE phải tự ép `company_id` theo hồ sơ, không đọc giá trị FE gửi lên; nút "Xoá lọc" KHÔNG được reset `company` (mở rộng quyền xem bằng 1 cú bấm). Mockup demo trạng thái không quyền bằng `?noPerm=1`. **KHÔNG gate vào màn** — màn mới KHÔNG dùng quyền `Quản lý giữ hàng` (id 100427) của màn cũ; mọi user đăng nhập đều vào được. **Không giới hạn phòng ban**: không có quyền thì vẫn xem toàn bộ hàng giữ của công ty mình. Tức quyền duy nhất đó chỉ quyết định PHẠM VI CÔNG TY, không quyết định được vào màn hay không.
  **Lối tắt "Hàng giữ của tôi"**: nút bật/tắt đầu thanh lọc, ép tiêu chí Theo nhân viên + công ty/phòng ban/nhân viên của người đăng nhập + bung tới cấp Hàng hoá; tắt bằng chính nút đó thì khôi phục bộ lọc trước khi bật, còn đổi tay ô khác thì tắt cờ nhưng giữ lựa chọn mới. BE lấy `auth()->id()`, KHÔNG dùng `auth()->user()->info->id`.
  ⚠️ **KHÔNG gọi dòng `prepick_details` là "LÔ"** — hệ thống đã có lô hàng THẬT ở `warehouse_import_lots` (36.613 bản ghi, `lot_number` UNIQUE, `remain_qty`), còn hàng giữ không gắn lô nhập / không gắn kho / không có số lô. 1 dòng `prepick_details` = tổ hợp duy nhất (NV × KH × hàng hoá × công ty × HẠN GIỮ), đã kiểm 2.412 dòng / 0 nhóm trùng. Giao diện chỉ đếm theo **YÊU CẦU GIỮ** (chứng từ gốc) và **MÃ HÀNG**.
  ⚠️ **ĐỊNH NGHĨA CHỐT 13/09/2026 — "1 yêu cầu giữ = PHIẾU + MÃ HÀNG + NHÂN VIÊN"** (1 phiếu xin giữ 5 mã = 5 yêu cầu). Đây là đơn vị đếm CHI TIẾT, không phải đếm chứng từ: thật là **2.412 dòng / 2.410 yêu cầu / chỉ 593 phiếu** — gần như mỗi dòng là một yêu cầu, chỉ 2 trường hợp một yêu cầu còn nhiều dòng (gia hạn tách một phần số lượng). Khoá đếm `source|product_id|employee_id` phải dùng CHUNG ở tổng hợp và ở bộ lọc popup, nếu không con số 2 nơi lệch nhau. Cột popup đổi thành **"Phiếu giữ gốc"** vì nó hiện mã chứng từ.
  ⚠️ **BE BẮT BUỘC lần ngược chuỗi gia hạn về CHỨNG TỪ GỐC trước khi đếm** — gia hạn đẻ bản ghi `prepick_details` MỚI. Đếm thô theo `objectable` của chính bản ghi ra 2.411 vs đếm đúng 2.410 (chồng ít vì gia hạn thường rút HẾT bản ghi cũ), NHƯNG **1.111/2.412 bản ghi còn hàng (46%) mang `objectable_type = PrepickExtendRequestDetail`** → đếm thô làm cột "Phiếu giữ gốc" hiện mã phiếu GIA HẠN ở 46% số dòng, sai chứng từ. Nếu recursive CTE nặng thì cân nhắc denormalize `root_objectable_id/type` ghi trong `moveToExpireDate()` — nhưng `prepick_details` là bảng DÙNG CHUNG với ERP, phải hỏi trước khi thêm cột.
  ⚠️ **Popup phiếu thu KHÔNG hiện "Còn phải thu"** — nó chỉ gom phiếu thu, chưa phải công nợ; `giá trị HĐ − đã thu` không bằng công nợ (còn giảm giá, thuế, bù trừ). Công nợ phải đọc từ nghiệp vụ công nợ.
  ⚠️ **Bẫy đã trả giá khi port style:** `.rsum-tb { min-width: 1280px }` là số cứng của bảng **10 cột** màn TKT — bảng 7 cột giữ nguyên số đó thì màn 1200px sinh cuộn ngang và **cắt mất 2 cột cuối**; 3 cột hạn giữ tô màu xanh/vàng/đỏ phải **trả lại màu teal ở ô TIÊU ĐỀ**, không thì chữ trắng trên nền header sáng, tàng hình; `.minutes-modal__body` là **flex column** nên nhiều `.drill-wrap` xếp chồng bị co sập còn **2px** (bảng bên trong cao 297px) — phải bọc mỗi nhóm trong 1 flex item `flex: 0 0 auto`; và `.drill-table { min-width: 1740px }` (số cứng bảng 14 cột màn mẫu) làm bảng 7 cột tràn ngang, mọi chỉnh `colgroup` vô tác dụng — **đúng cái bẫy đã ghi ở feature `bao-cao-ke-hoach-lam-viec-nhan-vien`**; đổi thứ tự cột trong `colgroup` mà quên đổi thứ tự render ô làm **toàn bảng lệch 1 nhịp** (cột Mã hiện ra tên hàng, cột tên bị bóp còn 1 chữ/dòng); và `.drill-table { min-width: 1740px }` **dính lần 2** ở popup phiếu thu thêm sau — mỗi popup mới đều phải thêm selector override, nếu không bảng bị cắt cột cuối im lặng.
  **03/10:** nhánh `gop_db-bao-cao-theo-doi-giu-hang` cả 3 repo (CHƯA push/merge), worktree `websites/wt-giu-hang/`; checkpoint + số đo + sổ Ruling ở `plan.md` / `sdd-ledger.md`. ⚠️ Deploy: migrate + `prepick:backfill-root` TRƯỚC khi deploy code ERP/HRM, sau deploy chạy lại `--all`.
  **Bước tiếp theo:** user quyết nguồn "Tổng thanh toán" (local = 0 mọi HĐ) · 3 chỗ lệch mockup · merge `gop_db` mới (đi trước 74 commit) vào nhánh rồi merge về `gop_db`.
  **~~Blocked~~ (đã chốt 02/10, giữ để tra cứu):** (1) quyền `Xem báo cáo giữ hàng theo tổng công ty` CHƯA tồn tại, phải thêm `PermissionsTableSeeder` · (2) cách lấy chứng từ gốc: recursive CTE mỗi lần chạy hay denormalize `root_objectable_id/type` — cột mới trên bảng DÙNG CHUNG với ERP nên phải hỏi trước · (3) chốt cỡ trang + ngưỡng lazy load sau khi đo thời gian phản hồi trên dữ liệu thật · (4) hỏi nghiệp vụ về kế hoạch gán **bộ phận** cho NV kinh doanh (hiện 2,6% dòng có bộ phận → ô lọc gần như luôn ở trạng thái khoá).

- dieukhoan-per-company (GIAI ĐOẠN 2) → @namdangit → .plans/gop-db/dieukhoan-per-company/plan.md
  Trạng thái: **G1 XONG + COMMIT/PUSH gop_db; G2 ĐÃ VIẾT SPEC + PLAN (Task 14-22) — chờ user duyệt plan + chốt 1 điểm mở trước khi code (24/09/2026). Chưa code G2.** Plan G2 (9 task: migration→ERP đọc/ghi→HRM service→FE ẩn field→e2e) append trong plan.md, self-review sạch. **ĐIỂM MỞ cần user chốt:** tab `chung` (logo/header, KHÔNG trong 17 field) buộc cũng flip per-company vì migration bỏ singleton — đề xuất flip luôn (transparent UI); cần OK trước Task 20. Cơ chế đã khoá: config-store giữ `scope_type='global'` làm bộ chọn store, chỉ đổi `scope_id` 0→companyId + thêm `WHERE company_id` (KHÔNG remap sang scope_type='company' — sẽ vỡ store-routing). G1 (2 thư viện điều khoản per-company + tweak bảng) đã nghiệm thu. G2 = migrate 17 field regulation-config từ configs-singleton (global) sang configs-per-company. Spec: `docs/superpowers/specs/gop-db/2026-09-24-config-per-company-g2-design.md`. **5 quyết định chốt (24/09):** (1) `configs` ADD `company_id`, backfill singleton→cty1, clone mọi công ty trong `companies` + clone `contract_rows`; (2) `Config::getConfig($col,$companyId)` resolve param→auth company→fallback cty1, sửa 1 chỗ gốc + 4 điểm `Config::first()`; (3) ConfigsController ERP → per-company (hướng A, giữ màn admin); (4) 17 field sang cơ chế company-scope sẵn có (version scope_type='company'); (5) ẩn 2 cột chết `quotation_footer`+`coefficient_cost_price_service` khỏi UI HRM, KHÔNG drop. Console BorrowWarning/PrepickWarning lặp per-company = điểm regression trọng yếu. **Bước tiếp:** user duyệt plan G2 + chốt điểm mở (flip `chung`) → chọn execution mode (subagent-driven / inline) → Task 14 (migration).

- warehouse-import-request-list-actions → @namdangit → .plans/gop-db/warehouse-import-request-list-actions/plan.md
  Trạng thái: **CODE + VERIFY PLAYWRIGHT XONG, chờ user duyệt commit/push (19/09/2026).** Ticket "[ERP => HRM] Phiếu đề nghị nhập kho - Danh sách": bổ sung cột hành động đầy đủ ở `/finance/warehouse-import-requests`. **FE-only** (`pages/finance/warehouse-import-requests/index.vue`) — BE `WarehouseImportRequestResource` đã trả đủ 5 cờ. 3 quyết định user chốt: (1) GIỮ header "Thao tác", chỉ bổ sung nút; (2) "duyệt nhanh" = Option A deep-link ERP (nút "Tạo phiếu nhập kho" mở `warehouse_imports/create?warehouse_import_request_id=`, HRM không có route duyệt); (3) gom nút vào menu ⋮ theo màn chuẩn. Dùng `V2BaseRowActions` (maxInline 3): Sửa · Tạo phiếu nhập kho · Từ chối(danger) · In · Hủy(danger), mỗi nút `visible` theo cờ; Mã phiếu → `nuxt-link` chi tiết; Từ chối/Hủy dùng `base-confirm-modal`, In dùng `reportPrintPreviewMixin`+`ReportPrintPreviewModal`. **Verify Playwright:** danh sách trống với emp 48 (thiếu quyền) → bơm 4 mock row client-side (KHÔNG đụng DB) đủ tổ hợp cờ; xác nhận A/B = 3 inline, C (5 cờ) = 2 inline + menu ⋮ chứa Từ chối/In/Hủy, D = 1 inline, Mã phiếu là link, nút danger có class `is-danger`. FE giữ LF. CÒN: KHÔNG commit/push tới khi user duyệt.

- warehouse-export-request-list-functions → @namdangit → .plans/gop-db/warehouse-export-request-list-functions/plan.md
  Trạng thái: **ĐANG LÀM ticket mới "Bảng danh sách - 8 cải tiến" (19/09/2026) — CODE + VERIFY PLAYWRIGHT XONG, chờ user duyệt commit/push.** Ticket "[ERP => HRM] Phiếu đề nghị xuất kho - Danh sách" (Nguyễn Minh Hằng → Trần Cư): 8 yêu cầu Bảng danh sách. Đã code cả 8 (BE 5 file: Service+history, CatalogHistoryService, Entity `updater`, Resource 3 field, Controller eager-load+`$sortMap`; FE 2 file: `index.vue` cột/sort/lịch sử/nhãn + `_id/index.vue` SystemInfoSection). Item 4 (Lịch sử) làm ĐỦ 2 nơi (popup danh sách + SystemInfoSection chi tiết, cả 2 gọi catalog-histories 200). **Verify Playwright đầy đủ (emp 48):** header "Người tạo" + 4 cột mới; sort Loại→`type_name` 200 đúng thứ tự type; Mã YCXH `v2-cell-link` xanh không icon; ô trống render "" không "—"; popup + block Lịch sử mở OK 200. DB test reassign 3 phiếu `created_by=48` đã REVERT (13/13/202), `catalog_histories` 0 dòng. `php -l` sạch 5 file, FE LF. CÒN: KHÔNG commit/push tới khi user duyệt. Chi tiết task ở cuối plan.md.
  Ticket TRƯỚC (thiếu chức năng, 4 chức năng) đã **HOÀN THÀNH + COMMIT/PUSH (18/09/2026)**: API `6c49752a4` (feature `077e5ddce`), Client `a83e986b9` (feature `821fa4865`) — merge `origin/gop_db` không conflict, push OK cả 2 repo.
  Ticket Redmine "[ERP => HRM] Đề nghị xuất kho - Danh sách - Thiếu chức năng" (Nguyễn Minh Hằng → Trần Cư, Cao). Màn `/finance/warehouse-export-requests` (module Assign) thêm 4 chức năng **Cài đặt bộ lọc · Xuất excel danh sách · In bộ giấy tờ đi đường · In đề nghị** + dọn vi phạm quy ước. Mirror sibling `product-export-requests`. Quyết định §1 (In giấy tờ đi đường = Lệnh điều động 55 + Phiếu xuất kho đi đường 59, bỏ passport PDF) ĐÃ CHỐT hướng A+A1.
  **Đã xong:** BE cả 4 chức năng + route (session trước). FE `index.vue` rewrite hoàn chỉnh (V2BaseSmartFilterPanel floating 11 ô lọc, ExportFieldsModal+ExcelJS, reportPrintPreviewMixin, 5 nhóm task 1-5 = [x], LF 0 CRLF) + `components/export-excel.js`.
  **Verify Playwright ĐẦY ĐỦ:** (a) màn render đủ; API index/type-options/customizations 200; org block ẩn = ĐÚNG fail-closed (DNS Admin thiếu quyền id 1531-1534). (b) **In đề nghị** (print-data) + **In giấy tờ đi đường** (print-move-data) HTTP 200, template hợp lệ — đề nghị có letterhead đúng công ty, move gồm 2 tài liệu Lệnh điều động + Phiếu xuất kho nối page-break. (c) **Xuất Excel**: BE `/export` trả đúng 11 field khớp FE columns, dựng file ExcelJS đọc lại đúng cấu trúc/format/data. (d) **Filter keys**: 12 key FE khớp 100% BE `applyFilters`. (e) `php -l` sạch 4 file BE, LF giữ nguyên. Verify data-dependent chạy bằng 3 phiếu tạm reassign `created_by=13` (35230/35232/35235), đã **revert về gốc** (205/318/209) + verify DB sạch. Ghi nhận cũ: bấm Tìm kiếm bắn 2 request trùng = pattern DÙNG CHUNG canonical, không tự sửa lệch 1 màn; console error `GET /menu-settings 400` là global.
  **Còn lại:** không. Đã commit + push lên `gop_db` cả 2 repo (user duyệt "Tất cả thay đổi"). Kèm trong commit có thay đổi liền kề: API `WarehouseImportRequestResource` (is_can_deny loại type 11), Client `product-export-requests` (tách `ProductExportRequestForm.vue`).

- product-export-request-print-export → @namdangit → .plans/gop-db/product-export-request-print-export/plan.md
  Trạng thái: **HOÀN THÀNH CẢ 3 CHỨC NĂNG — verify Playwright (18/09/2026). Chưa commit/push.** Port 3 chức năng menu ⚙ màn "Danh sách yêu cầu xuất hàng" ERP sang HRM (`/finance/product-export-requests`, module Assign).
  **Phase 1 (In yêu cầu)** ✅: mẫu ERP `report_templates` id 13 · BE `ProductExportRequestPrintService` (9 cột + footer suy line-sum, nhánh Giảm giá/VAT có điều kiện) + `printData()` (scopedQuery) + route `GET /{id}/print-data` · FE nút "In yêu cầu" + `reportPrintPreviewMixin` + `ReportPrintPreviewModal`. Verify: bản in đủ field, số quốc tế, ca có/không Giảm giá đúng math.
  **Phase 2 (Xuất excel Bkav 22 cột)** ✅: BE `ProductExportRequestBkavExport` (FromView + WithColumnWidths; DonGia = price+extra_price mirror mẫu 13; 3 ô số = SỐ THẬT + data-format `#,##0`) + blade `exports/assign/product_export_request_bkav` + `exportProductList($id)` + route `GET /{id}/export-product-list` · FE nút "Xuất excel danh sách hàng" (`ri-file-excel-2-line`) + `downloadExcel`. Verify Playwright: click dòng PYCXH-40338 → tải đúng file, đọc lại PhpSpreadsheet: 22 header đúng, ô SL/ĐG/TT kiểu SỐ fmt `#,##0`, bề rộng cột khớp, endpoint 200 xlsx.
  **Phase 3 (In biên bản giao nhận, `print_templates` type 12)** ✅: BE `ErpPrintTemplate` + `handoverTemplates()` (mẫu type 12) + `handoverEmployees()` (NV cùng cty, format `Tên - Mã phòng - Mã NV`) + `ProductExportRequestHandoverPrintService` (4 biến thể bảng chi tiết) + `printHandoverData($id, Request)` 5 tham số + 3 route `handover-templates|handover-employees|print-handover-data` · FE `components/HandoverPrintModal.vue` (V2BaseModal + V2BaseSelectInModal, chỉ thu tham số → `@preview`) + nút "In biên bản giao nhận" (`ri-file-list-3-line`) + `openHandoverPrint`/`onHandoverPreview` dùng lại `ReportPrintPreviewModal`. Verify Playwright PYCXH-40338: modal 5 trường; select mẫu nạp 8 (type 12), select NV nạp 394 đúng format; bấm In rỗng → đủ 4 lỗi bắt buộc (employee_id không bắt buộc); điền hợp lệ + chọn mẫu 160 → `@preview` payload đúng → render bản in thật "BIÊN BẢN BÀN GIAO THIẾT BỊ SƠ BỘ".
  (Test tạm cấp quyền role 18/perm 100870/cty 1 phục vụ cả 3 phase → **đã hoàn tác cuối Phase 3** (deleted 1, remaining 0) + flush Spatie cache; DB sạch, hành vi phân quyền production khôi phục; file test đã xóa.)
  **Bước tiếp theo:** không còn — chờ yêu cầu mới (chưa commit/push theo ràng buộc).

- bao-cao-ke-hoach-lam-viec-nhan-vien → @namdangit → .plans/gop-db/bao-cao-ke-hoach-lam-viec-nhan-vien/plan.md
  Trạng thái: **ĐANG LÀM (Phase 4) — Task 9/10 xong, ĐÃ MERGE `gop_db` (22/09/2026)**.
  Toàn bộ tính năng xong: quyền 3 cấp (id **1612-1614**) · gom **5 nguồn** thành cặp (phiếu × người) ·
  cây 3 cấp Phòng ban ▸ Bộ phận ▸ Nhân viên · popup gộp theo phiếu + drawer · in (trần 2.000 dòng) +
  Excel. **39 unit test xanh (122 assertions).**
  Merge fast-forward vào `gop_db`: `hrm-api bf0711d6e` · `hrm-client 07a9a6dc4`. **CHƯA PUSH.**
  Worktree `wt-bao-cao-klv` (nhánh `gop_db-bao-cao-ke-hoach-lam-viec`) vẫn còn, server kiểm chạy ở
  `:8010` (API) / `:3010` (client).
  ⚠️ **CÒN TASK 10** — e2e + rà chuẩn bàn giao, **chưa chạy**. 4 việc quan trọng: xác nhận đúng role
  bộ e2e dùng (Task 1 tự suy `role_id=18`) · kiểm **index** `assign_requests.from_time` &
  `meetings.start_date` & `assign_jobs.time_start_request` · chạy thử **seeder trọn bộ trên DB nháp**
  (cả phase chỉ INSERT tay 3 dòng) · viết 2 spec e2e.
  ⚠️ Nợ bàn giao: **letterhead chỉ kiểm được tới mức URL** ở local (thiếu `ERP_URL`) · `tasks.start_time`
  vẫn thiếu · bảng `issues` **rỗng toàn DB local** nên nhánh issue chưa từng chạy với dữ liệu thật ·
  `EmployeeWorkPerformancePrintService` **mirror logic cột của FE** (FE đổi `ALL_COLUMNS` mà quên sửa
  BE thì bản in lệch với màn, im lặng).
  Chi tiết + **~25 ruling** đã chốt trong phase: `.sdd/progress.md`. Spec code-level: `design-phase4.md`.
  Màn báo cáo **MỚI**, không thay `meeting-by-employees` hay `task-manager-by-employees`. Theo dõi **khối lượng công việc** của Phòng ban ▸ Bộ phận ▸ Nhân viên, gom **5 nguồn** đang nằm rải rác: `meetings` · `tasks` · `issues` · `assign_business` · `assign_jobs`. Định nghĩa chỉ tiêu bám đúng hằng số trạng thái trong `hrm-api/Modules/Assign` (có bảng tra trong `design.md`).
  Style port nguyên khối từ `../../bao-cao-phat-trien-thi-truong-khach-hang/`; danh mục tổ chức dùng chung bộ **2 công ty · 10 phòng ban · 2 bộ phận · 43 nhân viên** của màn đó.
  **5 quyết định lõi:** 10 cột (5 loại + Tổng · Đã HT · Tỷ lệ HT) · tính vào kỳ theo **GIAO NHAU (overlap)**, không theo ngày tạo · 1 đầu việc tính cho **MỌI người tham gia** (đếm cặp chứng từ × người nên dòng cha luôn = tổng dòng con) · nháp + huỷ/từ chối **vẫn nằm trong Tổng** ⇒ tách **4 nhóm trạng thái chia hết tổng** · **bỏ mọi chỉ số bình quân**.
  Kỳ mặc định 09/2026: **1.040 đầu việc · 37/43 NV có việc · hoàn thành 51,0%**.
  ⚠️ **Nợ backend:** `tasks` có `due_time` nhưng **KHÔNG có `start_time`** → muốn giờ bắt đầu của Task đúng như mockup thì phải bổ sung cột, nếu không BE chỉ trả `00:00`.
  ⚠️ **Bẫy đã trả giá (chi tiết ở `design.md` mục "Gotcha"):** `.drill-table { min-width: 1740px }` là số cứng của bảng **14 cột** màn mẫu — port sang bảng ít cột hơn thì nó ép giãn và khiến **mọi chỉnh `colgroup` vô tác dụng**; `scrollWidth` của phần tử chứa icon ⓘ luôn bị tooltip `::after` thổi phồng nên **không dùng để kết luận chữ bị cắt** (đo bằng `Range` thay thế); đặt `overflow:hidden` lên nhãn có icon ⓘ sẽ **cắt mất tooltip**.
  ℹ️ Feature nằm trong `.plans/gop-db/` để ở cạnh cụm mockup báo cáo anh em (design.md trỏ đường dẫn tương đối sang đó), **nhưng 2 repo đang đứng ở nhánh `tpe`** — không phải nhánh con của `gop_db`. Mockup không đụng code repo nên không ảnh hưởng; khi port sang Vue thật cần chốt lại nhánh.
  **Bước tiếp theo:** chờ user chốt mockup → SRS + testcase (nếu cần) → port Vue `pages/assign/report/` → API BE.

- theo-doi-thuc-hien-hop-dong → @namdangit → .plans/gop-db/theo-doi-thuc-hien-hop-dong/plan.md
  Trạng thái: **PHASE 1 XONG — MOCKUP HTML 7 TAB + VERIFY PLAYWRIGHT 1440×900 (02/09/2026)**. Chưa động vào code thật.
  Nguồn: `THEO DÕI THỰC HIỆN HỢP ĐỒNG.docx` (họp 25/08/2026). Màn **mới, độc lập** với `/assign/contracts/{id}`.
  6 tab: Thông tin chung · **Cung ứng** · **Giao hàng & nghiệm thu** · Tài chính (4 tab con) · Thiết kế & giám sát · Bảo hành.
  Khảo sát: module HĐ **đã có sẵn** 4 trạng thái + `sign_date`/`effective_date`/`expiry_date`/`execution_deadline_days`/`EFFECTIVE_COND_*`/`EXEC_BASE_*` + `ContractPaymentTermsTable` + guard `getCanExportAttribute` → mockup bám vào, không vẽ lại.
  Nghiệp vụ lõi tab Cung ứng: `Giữ hàng + Đang đi mua ≥ SL ký` cho từng mã, chưa đủ thì tô đỏ + **chặn tạo YC xuất hàng**.
  ⚠️ Phát hiện lỗi có sẵn ở `mockup-chi-tiet-bao-gia`: `thead` sticky **không bao giờ dính** vì `.tblwrap{overflow-x:auto}` không cuộn dọc (đo `theadTop: -124`) — cần sửa kèm khi port sang code thật.
  **Vòng 2 (02/09/2026):** sidebar thu gọn rail 62px (burger bật/tắt) · **bỏ stepper** (màn chỉ áp dụng HĐ *Có hiệu lực*) · rút nhãn tab bỏ số thứ tự (7 tab vừa khít, dư 0px) · **thiết kế lại khối tổng hợp 7 tab theo mockup `bao-cao-ket-qua-cham-soc-khach-hang-tiem-nang.html`** (card `.rsum` có Thu gọn + box tint `.rsum-blk` + hàng `.rsum-kpi` border-left, track 5px). Sửa lỗi số liệu: tổng *Đang đi mua* 218→**217**, *Đã phân bổ* 1.676→**1.675** (cân đúng 1.675+92=1.767=tổng SL ký).
  **Vòng 3 (02/09/2026):** tab Thông tin chung **bỏ hết summary tài chính** (chỉ theo dõi ở tab Tài chính) · gỡ trùng lặp với thanh tiêu đề (mã HĐ / khách hàng / trạng thái / giá trị / số ngày còn lại — đo được 0 lần trong tab) · **chia lưới thông tin HĐ thành 4 nhóm chủ đề** (6·6·3·3 ô, không nhóm nào lẻ ô).
  **Vòng 4 (02/09/2026):** card đổi tên **Thông tin chung** với 4 nhóm *Thông tin hợp đồng (9 ô) · Thông tin khách hàng (6) · Hiệu lực & thời hạn (9) · File đính kèm (bảng 4 file)* · card timeline → **Tiến độ thực hiện theo các mốc thời gian** · **bỏ hết note điều hướng sang tab khác** (đo 0 lần toàn trang). Không còn bảng nào phải cuộn ngang ở cả 7 tab.
  **Vòng 5 (02/09/2026):** nhóm *Thông tin hợp đồng* 12 ô (**Số hợp đồng đứng đầu**), *Thông tin khách hàng* 9 ô (**Mã KH · Tên KH · MST lên trước**) — **nới nguyên tắc gỡ trùng lặp**: trường định danh vẫn nằm trong nhóm của nó · **tô màu nhận diện 7 tab** (`--tc`/`--tcl`: xanh dương · teal · cam · xanh lá · tím · hồng · hổ phách), chiều cao 7 tab đồng đều 35px, không tràn khung.
  **Vòng 6 (03/09/2026):** bỏ meta *Người lập/Tạo lúc* · thanh tiêu đề thêm **KD phụ trách** · bỏ 4 trường *Mẫu in · Người nhận cảnh báo · Cảnh báo giao hàng · Cảnh báo hết hiệu lực* → nhóm 10·9·6 ô (ô *Thời gian bảo hành* tràn hết hàng để không lẻ dòng; gộp *Ngày bàn giao mặt bằng* vào *Mốc tính thời hạn*).
  **Vòng 7 (03/09/2026):** **mở ô nhập tay** đúng các trường tài liệu ghi bắt buộc — Thông tin chung 6 ô (Ngày ký · Điều kiện hiệu lực · Ngày có hiệu lực · Mốc tính thời hạn · Ngày đạt mốc · Thời hạn thực hiện) + **Ngày hết hiệu lực khoá `TỰ TÍNH`** kèm công thức; Tài chính 5 ô (lý do vượt dự toán — dòng chưa nhập viền đỏ; ngày đạt mốc + nút đính kèm biên bản); Thiết kế 2 ô; Giao hàng 6 ô. **Không** mở nhập ở tab Cung ứng (SL sinh từ phiếu giữ / đơn mua).
  **Vòng 8 (03/09/2026):** **bỏ tab *Hàng hoá ký***, gộp dịch vụ vào tab **Cung ứng & dịch vụ** (2 bảng: phương án cung ứng 9 mã + *Dịch vụ đã ký* 4 gói với % tiến độ & trạng thái hạch toán) → còn **6 tab**; timeline **bỏ chip Đúng hạn ở mốc Ký hợp đồng** (chỉ kiểm soát đúng hạn từ các mốc sau khi ký). ⚠️ Tự bắt lỗi: card dịch vụ chèn rơi ngoài `pane#p3` (hiện ở mọi tab) — đã sửa.
  **Chốt 03/09/2026:** **bỏ hẳn đơn giá / thành tiền / VAT từng đầu mục** — màn theo dõi chỉ giữ số lượng ở cấp đầu mục, tiền chỉ ở cấp tổng (thanh tiêu đề + tab Tài chính).
  **Vòng 9 (03/09/2026):** bảng cung ứng — header có viền đồng nhất thân bảng · dòng *Đang đi mua* thêm **số YCĐH** (PO xuống dòng phụ) · dòng *Giữ hàng* thêm **Hạn giữ** (có chip cảnh báo sắp hết hạn) · cột **Đã về kho → Tồn kho khả dụng** (đổi cả nội dung thành số tồn dùng được, để quyết Giữ hàng hay Đặt hàng) · dòng đủ phương án bỏ nút *Sửa phương án* · bảng chi tiết thêm tiêu đề 8 cột. ⚠️ Tự bắt lỗi: cùng số PO ghi 2 NCC khác nhau giữa tab Cung ứng và Tài chính — đã gán lại theo bảng công nợ NCC.
  **Vòng 10 (03/09/2026):** **logic Hiệu lực & thời hạn chạy thật** — *Kể từ ngày ký* → ngày hiệu lực = ngày ký; *Theo bảo lãnh* → hiện thêm **Số bảo lãnh + Ngày bảo lãnh duyệt**, hiệu lực lấy theo ngày bảo lãnh; *Theo đặt cọc lần đầu* → lấy ngày phiếu thu đặt cọc đầu tiên (nguồn ở tab Tài chính, **nối sau**). Ngày có hiệu lực + Ngày hết hiệu lực đều là ô `TỰ TÍNH` có dòng nguồn/công thức động. Chạy thử 8 kịch bản Playwright.
  **Vòng 11 (03/09/2026):** tab Cung ứng — hàng KPI đổi sang **“Tình hình đặt mua”** (Tổng đặt mua 4 đơn mua · **Số lượng đã về kho 121** · **Số lượng đang mua 96**, 2 ô sau bấm ra **popup chi tiết từng mã**); thêm 2 cột **SL đã xuất / SL còn lại**, dựng lại bảng để **mọi cột sau tính theo SL còn lại** (mã đã giao đủ → trạng thái *Đã xuất đủ*). Cân bằng số học 9/9 dòng, 0 lỗi; tổng 1.767/1.458/309/1/216/217/92.
  **Vòng 12 (03/09/2026):** dòng *Giữ hàng* tình trạng **chỉ còn Còn hạn / Quá hạn** (suy từ Hạn giữ) · **bỏ toàn bộ 7 dòng ghi chú quy tắc** (toàn trang 0 lần chữ “Quy tắc”) · **popup dựng lại theo khung `.ticket-drawer` của mockup Báo cáo CSKH tiềm năng** (drawer trượt phải, header gradient + icon tròn + chip trắng mờ) · khối *Hàng hoá cần cung ứng* đổi **Đã phân bổ → Số lượng đã giao 1.458 (82,5%)**, sửa luôn số cũ 1.675 đã lỗi thời.
  **Vòng 13 (03/09/2026):** popup đổi từ drawer trượt phải sang **`.minutes-modal` căn giữa màn hình** (đúng khung popup của mockup mẫu) · bảng trong popup **cuộn được + tiêu đề cột dính** (`max-height:56vh`) · **Tồn kho khả dụng ≤ 0 thì bỏ nút *Giữ hàng***, chỉ còn *Đặt hàng*.
  **Vòng 14 (03/09/2026):** **tab Tài chính chia 4 tab con** — *Giá trị & thanh toán* · *Công nợ NCC* · *Công nợ KH* · *Dự toán*, mỗi tab con có **thống kê + cảnh báo riêng**; bổ sung **bảng phiếu chi NCC** (7 dòng) và **bảng phiếu thu KH** (6 dòng); tách bảng công nợ cũ thành *điều khoản* (tab 1) và *tình hình thu* (tab 3). Cân bằng số học khớp 100% (phiếu chi = đã trả · phiếu thu = đã thu · tổng 5 đợt = giá trị HĐ).
  **Vòng 15 (03/09/2026):** **tab Giao hàng & nghiệm thu lên vị trí 3** · cột *Nội dung giao* rút thành `N mã · M đơn vị` **bấm ra popup chi tiết mã + SL trong đợt** · demo **1 đợt nhiều PXK** (đợt 2: PXK-1326 + PXK-1331) · cột *Đã giao* **bấm ra popup serial** (mã vật tư không quản lý serial thì popup nói rõ). 12 popup bấm thử toàn bộ, 0 lỗi. ⚠️ Tự bắt 2 lỗi: link serial gắn nhầm cột *SL ký* ở 3 dòng; đợt 3 còn 5 ngày chứ không phải 6.
  **Vòng 16 (03/09/2026):** header popup **dùng chung 1 gradient xanh** `#0a1c3d → #0e7490` (đúng `.minutes-modal__header` của mockup CSKH), bỏ màu theo ngữ cảnh — đo 12/12 popup chỉ còn 1 gradient.
  **Vòng 17 (03/09/2026):** đổi nhãn tab **“Cung ứng & dịch vụ” → “Cung ứng”** (nội dung giữ nguyên).
  **[06/09 wrap up]** Mockup chốt ở **vòng 17**. Mở bằng `file://` (file tự chứa, 0 tham chiếu ngoài) hoặc HTTP **cổng cố định 8700**. Thư mục có thêm `QLHD_mockup.html` = bản sao user tự đặt tên.
  **CÒN:** (a) user duyệt UI mockup vòng 17; (a2) nối ngày đặt cọc thật từ phiếu thu ở tab Tài chính (đang hard-code) + chốt có bỏ ô *NV kinh doanh* trong nhóm HĐ không (đã có ở tiêu đề); (b) mockup nhóm A (trường + luồng 7 trạng thái trong form HĐ) và nhóm C (3 báo cáo) — user chốt làm sau; (c) màn danh sách HĐ đang thực hiện — làm sau.

- **cai-dat-phan-he — Cài đặt phân hệ (ẩn/hiện phân hệ + từng mục menu)** → @namdangit →
  `.plans/gop-db/cai-dat-phan-he/design.md` · `plan.md` ·
  spec `docs/superpowers/specs/gop-db/2026-09-14-cai-dat-phan-he-design.md`
  Trạng thái: **XONG TOÀN BỘ, ĐÃ TEST TAY** (2026-09-14) — chưa commit.
  Màn mới `/timesheet/setting/subsystems` liệt kê đủ 24 phân hệ + ~600 mục menu để tick ẩn/hiện,
  mặc định có tick. Bảng mới `menu_settings` chỉ lưu mục BỊ TẮT; key = đường dẫn nhãn
  (`finance::Thu chi::Phiếu thu`) vì ~345 mục placeholder không có link.
  Màn đọc thẳng registry `components/subsystems.js` → **menu thêm mới sau này tự có mặt**, không phải sửa gì.
  Lọc cắm vào 6 bề mặt sẵn có (topbar · sidebar cây · sidebar hub · lưới Tổng quan hub · màn chọn phân hệ ·
  dropdown chuyển phân hệ) + middleware FE chặn gõ thẳng URL → `/feature-unavailable`.
  3 checkbox ERP/Quyết định/Cơm rời khỏi màn Cài đặt (vẫn ghi song song key cũ `use_erp`/`use_decision`/`use_rice`);
  **"Sử dụng CRM" ở lại** vì `use_crm` là cờ đồng bộ CRM Mate, không phải phân hệ.
  ⚠️ **Trùng mục đích với `prod-cutover` Phần B** (allowlist fail-closed cho PROD, chưa code) —
  cut-over PROD phải seed sẵn danh sách ẩn, không dựng cơ chế thứ hai. Xem mục 6 của spec.

- **prod-cutover — Đưa `gop_db` lên PROD (1 nhánh, 2 môi trường)** → @namdangit →
  `.plans/gop-db/prod-cutover/design.md` · `plan.md` ·
  spec `docs/superpowers/specs/gop-db/2026-09-04-prod-cutover-design.md`
  Trạng thái: **SPEC XONG (Phase 0), CHƯA CODE** (2026-09-04).
  Kịch bản: ERP chạy code `master`, HRM chạy `gop_db`, **dùng chung 1 DB gộp**; PROD và dev
  **chung 1 nhánh** — PROD chỉ mở 7 phân hệ HRM đã nghiệm thu, dev thấy đủ để port tiếp.
  ⚠️ **Khảo sát phát hiện bản gộp `local_hrm_erp` đang có lỗi dữ liệu THẬT, âm thầm**:
  FK của ERP **2.313 → 10** (556 bảng có FK còn 7); **736 dòng ERP trỏ NHẦM sang vai trò HRM**
  + 1.820 mồ côi sau khi `ReconcileAuthSeeder` dời `roles.id +100000` mà chỉ remap 4/15 bảng —
  gồm `companies.deputy_role` sai ở **8/8 công ty** (VD: đáng lẽ "Tổng giám đốc" → đang trỏ
  "Quản lý Giải pháp DATKT SG"); `MergeProdSeeder` **DROP 14 bảng ERP** thay bằng bản HRM
  (`majors` 156 dòng → **0**, `areas` → **1/20**, ERP `master` vẫn dùng cả hai);
  `notifications` bị TRUNCATE (154k + 688k → **299**); nhóm `SHARE` ghi đè chéo theo id làm
  **77 khách hàng** bị ghi dữ liệu của khách khác.
  Nguồn lỗi nằm trong `Modules/Timesheet/Database/Seeders/GopDb/` → chạy pipeline đó lên PROD
  sẽ tái hiện y hệt. **Phải vá pipeline + dựng cổng nghiệm thu trước khi cut-over.**
  Đã chốt: cấu hình bật/tắt phân hệ **lưu trong DB (runtime)**, cắt **theo phân hệ** + chặn
  link lẻ; nhánh PROD hiện tại là `tpe`; ranh giới = 17 thư mục `pages/` mới + 3 màn
  (`/assign/contracts`, `/human/districts`, `/human/hamlets`); mức chặn BE **hoãn**.
  **PROD CHƯA gộp DB** (user xác nhận 2026-09-04) → còn kịp vá pipeline trước khi chạy thật.
  ✅ Đã có **cổng nghiệm thu**: `php artisan gopdb:health-check` (`app/Console/Commands/GopDb/HealthCheckCommand.php`)
  — CHỈ SELECT, chạy trên PROD an toàn. `--mode=pre` cảnh báo cái gì sắp mất, `--mode=post` đo cái gì đã hỏng,
  exit code 0/1/2 cắm được vào pipeline deploy. Danh sách nhóm bảng đọc từ `MergeProdSeeder` bằng Reflection.
  Bước tiếp: Phase 1 (vá pipeline gộp) hoặc Phase 3 (ẩn menu PROD) — chờ chọn.

- **finance-bill-adjust-dept — Phiếu kế toán (ERP `bill_adjust_dept` → HRM)** → @khoipv →
  `.plans/gop-db/finance-bill-adjust-dept/design.md` · `plan.md` ·
  spec `docs/superpowers/specs/gop-db/2026-08-28-finance-bill-adjust-dept-design.md`
  Trạng thái: **CODE XONG BE + FE (52/54 task) — CHỜ USER MỞ TRÌNH DUYỆT** (2026-08-28).
  BE 20 file mới + 4 file sửa · FE 9 file mới + 1 file sửa (menu) · 0 bảng mới · 2 quyền mới
  (id 1551-1552) · 4 morphMap bổ sung.
  Kiểm chứng: **150 phiếu ERP / 403 dòng bút toán / 33 cột khớp tuyệt đối với sổ cái ERP**;
  phạm vi quyền khớp SQL 6/6 NV; vòng đời đầy đủ chạy trong transaction rồi rollback;
  4/5 luật validate chặn đúng; 10 endpoint smoke test 200; FE 9/9 compile sạch.
  **ĐÃ TEST PLAYWRIGHT + ĐỐI CHIẾU TRỰC TIẾP VỚI ERP (2026-08-28)**: 20/20 bộ lọc khớp tuyệt đối;
  bấm thật danh sách / sort / phân trang / ghi nhớ lọc / 3 popup / cửa vào từ Phiếu YCĐC /
  duyệt-ghi-sổ / xoá / in / xuất Excel. **Tìm và sửa 7 lỗi** (ô lọc NVKD chết, Excel danh sách
  mất 9/11 cột, cột Phòng ban sai nguồn, bản in lệch ERP 6 điểm, ô chỉ-đọc còn là input, popup
  xuất không đóng, popup hợp đồng trả id thay vì tên). Chứng minh được ô lọc "STK ngân hàng"
  của ERP nổ HTTP 500. Chi tiết ở `plan.md` Phase 10.
  Còn lại: phần chưa kiểm chứng được (nhánh code chết + 2 cửa vào chưa có màn nguồn + phiếu ngoại tệ).
  **Checkpoint 2026-09-30**: fix validate bắt buộc theo skill form-validate — kiểm hết 1 lượt, toast
  chung + tự cuộn tới ô lỗi đầu, câu lỗi bỏ trống đổi thành "Bắt buộc phải nhập" (5 ô), thêm lỗi
  inline Loại tiền + bảng định khoản rỗng. FE only, compile sạch, CHƯA mở trình duyệt.
  Mắt xích cuối của luồng đã port dở: Đề nghị điều chỉnh công nợ / Hạch toán bổ sung → **Phiếu kế
  toán → ghi sổ cái `account_details`**. User chốt *"làm hệt ERP"*: đủ 5 cửa vào tạo phiếu, quyền
  xem 2 cấp, sửa/xóa = Đang tạo + đúng người lập, ô chọn hợp đồng bán lấy **cả `hrm_contracts` lẫn
  `firm_contracts`**.
  ⚠️ Feature này **gỡ ràng buộc "HRM không ghi sổ cái"** mà `finance-bill-adjust-dept-request` từng
  chốt (quyết định #3) — sổ cái dùng chung với cổng ERP, sai/trùng là lệch số kế toán thật.
  Nền: 12.628 phiếu · 33.409 dòng chi tiết · 0 bảng mới · 2 quyền mới · 4 morphMap phải bổ sung.

- org-filter-locked-options → @namdangit → .plans/gop-db/org-filter-locked-options/plan.md
  Trạng thái: **XONG BE + FE, ĐÃ VERIFY PLAYWRIGHT trên :3002/:8003** (2026-08-24). Chưa commit.
  Mục tiêu: bộ lọc chung `V2BaseCompanyDepartmentFilter` (Công ty/Phòng ban/Bộ phận/Nhân viên) có công tắc 🔒 theo TỪNG ô để hiện cả mục đã khoá; mặc định vẫn chỉ hiện mục đang hoạt động.
  BE: `OrgOptionController` + route `GET /api/v1/org-options?type=company|department|part|employee` (trả full kèm `is_locked`); `Employee::getAll($onlyActive = false)` + `userProfile()` gọi `getAll(true)` → store.employees bỏ nhân sự đã nghỉ.
  FE: prop `keepLockedOptions` cho `V2BaseSelect`/`V2BaseSelectInModal`; component lazy load khi bật công tắc, KHÔNG cache danh mục khoá vào Vuex; tắt công tắc vẫn giữ giá trị đang chọn.
  Bước tiếp: commit lên `gop_db`.

- thiet-ke-lai-phan-quyen → @namdangit → .plans/gop-db/thiet-ke-lai-phan-quyen/plan.md
  Trạng thái: **PHASE 1 XONG — ĐÃ CÓ MÀN THẬT TRÊN `hrm-client` + `hrm-api`, VERIFY PLAYWRIGHT 1440** (2026-09-02). Chưa commit.
  Màn: `/admin/roles` (danh sách chức vụ) + `/admin/roles/{id}` (ma trận). Menu: Quản trị hệ thống → Phân quyền. 3 route cũ (`timesheet/setting/roles`, `.../add/{id}`, `human/roles`) đã redirect sang màn mới.
  **Mở rộng phạm vi so với kế hoạch cũ: phục vụ CẢ HRM LẪN ERP** (DB đã gộp). Danh sách gộp 120 chức vụ + cột `Hệ`; form ma trận nạp đúng bộ quyền theo `guard` của chức vụ — KHÔNG cho gán chéo guard (quyền `web` gán vào role `api` sẽ ăn bên HRM nhưng câm bên ERP vì spatie lọc guard), BE chặn bằng validate.
  **Mô hình chốt: 1 DÒNG = 1 `group`** (đo 3 cách trên 1.687 quyền: suy tên 848 dòng · suy+gộp 721 · theo `group` **288**). Ô gói nhiều quyền gốc thành nút `n/N` mở popup nên KHÔNG mất độ mịn: 285 ô checkbox + 200 ô popup. Bất biến `selfCheck()`: **1.687/1.687 quyền có chỗ, không rơi dòng nào**.
  Phân hệ quyền ERP: map `group_category` → registry (`Danh mục`→9 · `Kinh doanh`→23 · `Kho`→21 · `Kế toán`→25 · `Mua hàng`→20 · `CSKH`→24 · `Cấu hình hệ thống`→10). Quyền `api` `type = NULL` (78 quyền Chấm công) quy về type 1 ở BE — trước đó chúng KHÔNG hiện trên màn phân quyền cũ.
  `approve_scope`: `hrm-api/config/permission_scopes.php` khoá theo **permission ID**, khai sẵn **20 bản ghi** (17 quyền ERP + 3 bản HRM của chức năng đã chuyển: `Duyệt hợp đồng` 100041/1141, `TP duyệt đề nghị thanh toán` 100203/1154, `TP duyệt yêu cầu nhập hàng` 100984/1166). 122 quyền duyệt còn lại hiện nhãn `Toàn công ty` + viền đứt ⚠ "chưa khai".
  Verify 18 ca đo bằng số từ DOM/DB, 0 lỗi console — gồm cả **ca không có quyền** (matrix/lưu đều `403`) và **ca chặn chéo guard** (DB không đổi). 3 lỗi tự phát hiện & sửa: sticky chết do `#wrapper`/`.content-page` `overflow:hidden`; dải phân hệ đặt `top` nhầm trên `<tr>`; cột "Quyền đang có" lệch 82 vì đếm cả dòng trỏ quyền đã xoá.
  **[03/09/2026] Màn danh sách chức vụ chuyển sang CHUẨN LIST-PAGE** (1 file FE `pages/admin/roles/index.vue`, chưa commit): `V2BaseFilterPanel` (tìm nhanh + lọc *Hệ*) · `V2BaseDataTable` (title, columns, rowActions, `getNumericalOrder`, cột *Chức vụ* là link mở ma trận, `V2BaseBadge` cho *Hệ*) · `V2BaseButton` trong slot `#actions` · thêm `PageTitleMixin`, gỡ 138 dòng CSS `rl-*`. Sửa kèm lỗi có sẵn: `exportExcel` bỏ sót `guard` nên xuất Excel không theo bộ lọc Hệ. **KHÔNG bật sortable** vì `RoleService::index` chỉ nhận `keyword`+`guard`, sắp xếp cứng `roles.id desc`. ⚠️ Tự bắt 2 lỗi: `V2BaseBadge variant="secondary"` không hợp lệ (25 warning console → đổi `brand`/`muted`); `pageSize=25` không có trong `pageSizeOptions [5,10,20,50,100]` → đổi về 10. Verify Playwright 1440: 0 class `rl-*` còn lại, lọc/tìm/làm mới/phân trang/đổi số dòng/popup/2 nút hành động đều đúng, console 0 lỗi. **Còn treo:** chạy ca không có quyền bằng tài khoản thứ hai.
  **[03/09/2026] Màn phân quyền 1 chức vụ chuyển sang CHUẨN PHÂN HỆ** (3 file, chưa commit): tiêu đề bỏ khối tự chế `pr-head`, đẩy lên **topbar qua `PageTitleMixin`** (`pageTitle` + `pageTitleInfo`) · bộ lọc ma trận `pm-filter` → **`V2BaseFilterPanel`** (tìm nhanh + 3 lọc nâng cao bằng `V2BaseSelect`), tách *Mở tất cả/Thu gọn* và *Cấp hàng loạt* ra thanh `.pm-tools` riêng (thao tác, không phải điều kiện lọc) · nút *Lưu* từ `GrantedPanel` xuống **`V2Footer` sticky** (`submit_form` + `url-back`) — vì `V2Footer` không có disabled nên chốt `!dirty` chuyển vào trong `save()` (toast cảnh báo, không bắn request rỗng), gỡ nút chết + 2 prop `saving`/`dirty` ở `GrantedPanel` · **màu phân hệ về MỘT tông** (`SUBSYSTEM_HUE`, bỏ bảng 12 `HUES`). Verify Playwright 1440: 0 class `pr-*` còn lại · 7 dải phân hệ đo được **1 màu nền / 1 màu chữ / 1 màu viền** · cuộn hết xuống hở 16px **không bị footer đè** (`body.has-v2-footer` padding 66px) · bấm Lưu khi chưa sửa ra toast đúng (chứng minh footer gọi đúng `save()`) · tick 84→104 rồi bỏ tick về 84 · console 0 lỗi. **Còn treo:** chưa chạy POST lưu thật (tránh sửa quyền chức vụ 100123 trên DB local).
  **[03/09/2026] Bố cục màn phân quyền:** bộ lọc **trải trọn chiều ngang** (1195/1205px), panel *Quyền đã phân* **chia màn cùng cấp với bảng** — panel đưa vào slot `side` của `PermissionMatrix`, trong component tách `.pm-split` 2 cột (`.pm-col-main` = công cụ + bảng · `.pm-col-side` = panel), gỡ `.pr-grid`. ⚠️ Tự gây & tự bắt lỗi: `align-items: start` làm cột phải co bằng chiều cao panel → **`position: sticky` của panel mất khoảng dính**, đo được `panelTop: -469` khi cuộn; sửa thành `stretch`. Verify: 2 cột cùng `top=182` không chồng nhau · `thead` dính 60 · panel dính 96→64 khi cuộn · cuộn hết hở 16px không bị footer đè · console 0 lỗi.
  **[06/09 wrap up]** Kiểm lại sau khi session khác sửa thêm `pages/admin/roles/index.vue` + `_id.vue` (05/09 11:15–11:16, khả năng là Phase 2 `code`): **toàn bộ phần chuẩn hoá 2 màn vẫn nguyên và chạy đúng** — list-page 7 cột + phân trang 1–10/119, màn ma trận bộ lọc full width 1267/1277px, 2 cột cùng cấp, 7 dải phân hệ 1 màu, footer 2 nút; **0 class tự chế còn sót**, console 0 lỗi cả 2 màn. Vẫn **CHƯA COMMIT**.
  ⚠️ **Seeder chạy lại 2026-09-02**: quyền `api` 597 → 722. Seeder **xoá 3 quyền khách hàng cũ** (166/168/169) không tạo lại → **49 dòng gán của 12 chức vụ thành mồ côi** (Super admin 15, Admin_TPE 6…). Bộ thay thế là `Quản lý khách hàng` type 9 (id 1517–1522). **Chưa có migration chuyển đổi** — cần quyết định viết migration hay cấp lại tay.
  ⚠️ **2 việc RIÊNG vẫn treo, không phụ thuộc Phase 1:** (a) **89 quyền "ma"** — gate trỏ vào quyền không tồn tại trong seeder nên vĩnh viễn trả `false` (HRM 28/44 chỗ · ERP 61/120 chỗ), danh sách ở `.plans/gop-db/thiet-ke-lai-phan-quyen/gate-quyen-ma.md`; (b) seeder khai **trùng tên** `Quản lý danh mục tiền tệ` (id 1115 và 1117) + `Xem danh mục tiền tệ` (1116 và 1118) — DB hiện KHÔNG có `unique(name,guard_name)` nên seeder chạy lọt, nhưng 2 bản trùng vẫn hiện 2 dòng giống hệt trên màn.
  **[09/09/2026] ĐÃ COMMIT (tài liệu trước đó ghi "chưa commit" là SAI):** `hrm-api` `38f616746` "step 1" (51 file, +2555/−267) · `hrm-client` `b6b4b0763` "step1" (30 file, +2873/−56), cùng ngày 06/09 16:36, nhánh `permiss_manager` (con của `gop_db`), mỗi repo 1 commit ahead, cây sạch, **chưa push**.
  **[09/09/2026] PHASE 3 HOÀN THÀNH 13/13 TASK — 18 commit local, CHƯA PUSH.** `hrm-api` 14 commit (`38f6167..3afdefb9d`+) · `hrm-client` 4 commit (`b6b4b0763..45decc4df`), cây sạch cả 2 repo, nhánh `permiss_manager`.
  **Nghiệm thu:** `permission:audit` 720 quyền khai · **8/10 chốt sạch** (còn chốt1=21 quyền ma, chốt5=37 quyền duyệt — nợ có sẵn) · `phpunit tests/` **67/67** · **seeder chạy THẬT 2 lượt trên `hrm_erp`: checksum KHÔNG ĐỔI**, `api=720 web=965 role_has_permissions=15087` nguyên vẹn · `/admin/roles/8` = **176 quyền (16/135/16/9)** khớp tuyệt đối baseline · ca fail-closed đúng.
  **Kết quả cốt lõi:** seeder permission trước đây KHÔNG AI DÁM CHẠY (3 seeder Finance ghi thẳng trong docblock "KHÔNG chạy file đó" vì nó `delete()` sạch rồi tạo lại — từng làm 49 dòng gán của 12 chức vụ thành mồ côi) nay **chạy nhiều lần vô hại trên DB thật**. Kiến trúc: lớp cơ sở `PermissionSeeder` (7 luật kiểm TĨNH trước khi chạm DB, `updateOrInsert` theo id, không bao giờ xoá, cuối lượt BÁO quyền lạ chứ không xoá) + `TimesheetPermissionSeeder` (78 quyền) + `LegacyPermissionSeeder` (642 quyền/11 phân hệ) + orchestrator ~30 dòng. Chốt 2 hạ **2→0**, thêm chốt **8/9/10**, tất cả đã chứng minh "biết đỏ" bằng tiêm lỗi thật.
  **Gate nay hiểu CẢ `name` LẪN `code`:** 21 file BE (14 bản sao `isCurrentEmployeeHasPermission` + middleware + trait Finance) — KHÔNG gom 14 bản làm một vì chúng khác ngữ nghĩa thật (2 bản lọc `current_company_role`, 12 bản dùng `getAllPermissions()`). Reviewer quét **toàn bộ 1.685 quyền × 2 nhân viên × 2 nhánh dữ liệu**: gọi bằng tên vẫn true, bằng code cũng true, **LOST = 0**. Sau đó 78 hằng số `TimesheetPermission` đổi sang code, **không đụng 253 chỗ gọi**; đối chiếu 78/78 khớp DB.
  ⚠️ **LỖI NGHIÊM TRỌNG chỉ Playwright mới bắt được:** 12 task + >20 lượt review + 67/67 test xanh đều KHÔNG thấy — mở trình duyệt thì **menu Chấm công trả 404 cho người có đủ 78/78 quyền**. `components/menu.js` khai `isShow` bằng hằng số (nay là code), `middleware/checkPermission.js:51` chỉ so `.name`. Vòng sửa 1: 11 file. Re-review tìm thêm `pages/timesheet/dashboard/index.vue` tự định nghĩa hàm kiểm quyền riêng → **4 thẻ thống kê bị ẩn IM LẶNG**; vòng 2 chữa nốt + phòng ngừa `hub.js` (dùng chung 16 phân hệ). **Bài học: "vào được trang" KHÔNG chứng minh gate bên trong còn sống — phải đo nội dung render ra DOM.**
  ⚠️ **4 lỗi trong chính spec/plan, do review bắt:** (a) `MD5(GROUP_CONCAT(...))` bị MySQL cắt ở **1024 byte** trong khi chuỗi thật **302.131 byte** → mọi phép "khớp" trước đó là GIẢ, phải `SET SESSION group_concat_max_len` cùng kết nối; (b) chú thích "mảng PHP không cho trùng khoá" SAI — PHP nuốt im lặng dòng trùng id, đã đổi sang soi mã nguồn + **fail-closed khi mất khả năng soi**; (c) test mẫu dùng model không implement `Authenticatable`; (d) `expectsOutputToContain()` chỉ có từ Laravel 9.
  ⛔ **3 seeder Finance CỐ Ý KHÔNG đăng ký vào orchestrator** (ngược bản spec đầu, đã sửa spec+plan): `AdditionAccountingRequestPermissionSeeder` khai id **1177–1180**, mà trên DB đó là 4 quyền phân hệ Giao việc (`type=4`), **1179/1180 mỗi cái có 2 dòng gán thật** (role 18, 100124) → gọi vào là âm thầm đổi ý nghĩa quyền đang dùng. Cả 3 **không kế thừa `PermissionSeeder`** (kế thừa `Seeder` trơn + `const PERMISSIONS`) nên **10 chốt không bảo vệ chúng** — đây là đường DUY NHẤT còn lại có thể phá dữ liệu quyền. Xử lý đúng: cấp lại id theo dải finance **2700–2799** rồi mới đăng ký (task riêng).
  🔎 **[10/09/2026] NGHIỆM THU VỚI USER — 2 lỗi phát hiện thêm, ĐÃ SỬA** (`hrm-client` `1be777456` + `80ca37862`, nâng client lên 7 commit). User hỏi *"quyền Phân ca chưa thấy ở bản mới"*. Kết quả điều tra: **KHÔNG mất quyền** (78/78 quyền Chấm công đều trong ma trận, 3 quyền phân ca 412/413/414 đủ cả) nhưng **UI giấu mất**: BE gom 3 quyền thành 1 mục "Phân ca" 3 cấp → FE có quy tắc `>1 mục → nút n/N` nên *1 mục 3 cấp* rơi vào nhánh **checkbox trơn KHÔNG NHÃN, KHÔNG TOOLTIP**, mà lại nằm ở cột "Quyền khác" — cột duy nhất không suy được tên từ tiêu đề. Đo toàn hệ: **23 ô** kiểu này, 1 ô giấu nhiều cấp.
  ⚠️ **Lỗi thứ hai nghiêm trọng hơn: tự hạ cấp quyền âm thầm.** `itemPatch()` khi bật mục có phạm vi thì thêm cấp **hẹp nhất** + xoá các cấp còn lại. Ngữ nghĩa 3 quyền phân ca là **thang loại trừ** (gate xét công ty → phòng ban → bộ phận, trúng trước thì dừng), nhưng dữ liệu thật có **12/15 cặp (chức vụ × công ty) đang giữ CẢ 3 cấp** (Super admin 5 công ty, Admin_TPE, Admin_CN Sài Gòn/Vinh/Hải Phòng, HCNS_CN Sài Gòn) → một cú **"Cấp tất cả"** hạ quyền phân ca của họ **từ toàn công ty xuống chỉ bộ phận**, KHÔNG mở popup nên không ai biết. (Mở màn rồi bấm Lưu mà không đụng gì thì an toàn — có chốt `dirty`.)
  **Đã sửa theo 2 hướng user chốt:** (1) mọi checkbox đơn có **tooltip tên quyền gốc**, mục **nhiều cấp** đổi thành **nút `n/N`** mở popup chọn phạm vi — đo thật role 19: nút `3/3`, tooltip *"Phân ca — 3 cấp: Công ty · Phòng ban · Bộ phận"*; (2) **không tự hạ cấp** — bật lại mục ĐÃ có quyền thì giữ nguyên cấp đang có, chỉ mục CHƯA có quyền mới mặc định cấp hẹp nhất. Áp cho **cả hai** đường: `PermissionMatrix.itemPatch()` và `ItemListModal.toggle()` (nút bật-tất-cả trong popup — lỗ hổng thứ hai). `pickLevel()` giữ nguyên vì đó là user chủ động chọn bậc.
  🔴 **[10/09/2026] LỖ HỔNG CÓ SẴN phát hiện khi trả lời user — CHƯA SỬA, chờ quyết:** quyền **"Quản lý ca làm việc" (id 8)** chỉ có tác dụng ở FE (ẩn/hiện nút Thêm mới · Sửa · Khoá · Mở khoá · Xoá ở `/timesheet/timeworking/working-shift`, và chặn vào màn thêm/sửa ca). **BE KHÔNG kiểm quyền này ở đâu cả** — grep cả tên lẫn code trong `hrm-api` ra 0 chỗ, và nhóm route `Modules/Timesheet/Routes/api.php:80-89` chỉ có `auth:api`, không `checkPermission` → **ai đăng nhập được cũng gọi thẳng API để thêm / xoá / khoá ca làm việc**. Vi phạm 2 quy định CLAUDE.md ("FE không được coi là đã chặn"; route store/update/destroy/toggle phải gắn `checkPermission`). **KHÔNG do Phase 3** (Phase 3 không đụng route, `git log` xác nhận). Vá đề xuất: gắn `checkPermission:CA_LAM_VIEC_MANAGE` cho 3 route ghi, giữ route đọc; rà 9 chức vụ đang giữ quyền trước khi siết. (Lưu ý đính chính: hệ thống KHÔNG có quyền tên "Quản lý phân ca"; id 8 là quyền ĐỊNH NGHĨA ca làm việc, còn 412/413/414 là quyền XẾP nhân viên vào ca — hai việc khác nhau.)
  📌 **Quy tắc id quyền MỚI (chốt Phase 3):** `2000 + (type−1)×100`, rộng 100 (timesheet 2000–2099 · payroll 2100–2199 · human 2200–2299 · assign 2300–2399 …); dải **1565–1999 để trống** làm đệm cho nhánh chưa merge. Quyền cũ giữ nguyên id lộn xộn. `permission_scopes.php` nay khoá **hai kiểu**: 11 quyền HRM theo `code`, 17 quyền ERP theo `id`.
  **Việc PHẢI làm trước khi tách phân hệ tiếp theo:** (1) sửa **14 dòng Transformer** Training/Assign (`getAllPermissions()->pluck('name')` truyền xuống `canXxx()`) — chưa hỏng vì 0 dòng chạm quyền Chấm công, nhưng vỡ ngay khi đổi hằng số của chính 2 module đó; (2) **37 quyền duyệt chưa khai `approve_scope`** (chốt 5) — nợ DUY NHẤT cấp quyền RỘNG hơn dự kiến, ngược fail-closed.
  ⚠️ `.env` đã đổi `DB_DATABASE` `hrm_tpe` → **`hrm_erp`** (DB gộp). Dump an toàn 643K + bản `.env` cũ nằm trong scratchpad session.
  Spec Phase 3: docs/superpowers/specs/gop-db/2026-09-09-seeder-permission-cau-truc-design.md (mục **7b** = lý do không đăng ký Finance) · Plan: mục "Phase 3" cuối `.plans/gop-db/thiet-ke-lai-phan-quyen/plan.md` · Ảnh: `.plans/gop-db/thiet-ke-lai-phan-quyen/screenshots/2026-09-09-phase3-admin-roles-8.png`
  Lịch sử: **[09/09/2026] mở Phase 3** — brainstorm + spec + plan 13 task. 6 quyết định chốt: seeder phục vụ **cả cài mới lẫn đồng bộ DB đang chạy** · quyền DB không còn khai thì **chỉ BÁO, không xoá** · upsert khoá theo **`id`** (đo được: 590 id chung giữa `hrm_tpe` và `hrm_erp`, **0 id lệch tên**), `code` là khoá duy nhất thứ hai · **1 file seeder / phân hệ** đặt trong module · id quyền mới theo công thức **2000 + (type−1)×100**, chừa trống 1565–1999 làm đệm · gate nhận **cả name lẫn code**, sửa **cả 14 bản sao + middleware + trait Finance + 3 hàm FE**, KHÔNG gom 14 bản (2 bản lọc `current_company_role`, 12 bản dùng `getAllPermissions()` — khác ngữ nghĩa thật).
  Quyền cũ **giữ nguyên 100%** đợt này (user tự rà lại theo từng màn sau); ngoại lệ duy nhất là bỏ 2 dòng khai trùng tiền tệ 1117/1118 — không bỏ thì seeder không chạy nổi.
  ⚠️ 3 cái bẫy đã ghi vào spec/plan: (a) `PermissionAuditService::declaredPermissions()` đọc seeder bằng **regex `Permission::create`** → tách file mà quên sửa là báo 78 quyền ma GIẢ, mốc kiểm chứng "722 quyền khai, chốt 1 vẫn 21"; (b) 644 quyền legacy phải khai thêm **`code` + `type` theo dòng**, không thì DB cài mới có `code = NULL` (unique cho phép nhiều NULL → **không nổ**, chỉ âm thầm chết mọi gate theo code); (c) bỏ `delete()` phải làm **cùng lượt** với tách file, không thì ai chạy seeder cũ sẽ xoá sạch 78 quyền Chấm công.
  ⚠️ `.env` đang trỏ `DB_DATABASE=hrm_tpe` — DB HRM thuần (593 quyền, **chưa có cột `code`**). DB gộp đúng là **`hrm_erp`** (965 web + 720 api, code backfill đủ). Task 1 đổi `.env` + `mysqldump` 2 bảng trước khi chạy gì.
  Số nền đo 09/09: audit 722 quyền khai · chốt 1 = 21 quyền ma (Assign 8 · Decision 6 · Training 5 · Human 2, **Chấm công 0**) · chốt 2 = 2 · chốt 5 = 37 · phpunit **7/7 xanh**. Còn dùng chuỗi tên quyền: BE Assign 235 · Training 156 · Human 79 · Payroll 35 · Decision 33 · Rice 16 · Finance 5; FE 365 chỗ.
  Spec Phase 3: docs/superpowers/specs/gop-db/2026-09-09-seeder-permission-cau-truc-design.md · Plan: mục "Phase 3" cuối `.plans/gop-db/thiet-ke-lai-phan-quyen/plan.md`
  Bước tiếp: user rà màn thật → chốt hình → viết e2e tự động; rà gate 122 quyền duyệt để khai `approve_scope`.

- menu-quan-ly-cong-viec → @namdangit → .plans/gop-db/menu-quan-ly-cong-viec/plan.md
  Trạng thái: **IMPLEMENT XONG + VERIFY PLAYWRIGHT 1440 — ĐÃ COMMIT + PUSH lên `gop_db`** (2026-08-10).
  Mục tiêu: đưa phân hệ Quản lý công việc (`assign`) + Đào tạo (`training`) sang sidebar hub navy+teal như các phân hệ mới.
  **Phase 2 (Đào tạo):** thêm `'training'` vào `HUB_SUBSYSTEMS` (training không có nút lẻ → chỉ 1 dòng). Verify `/training/courses`: rail "ĐÀO TẠO" + 12 nhóm, panel bung OK. Cùng file `hub.js`.
  Đã làm: (1) thêm `'assign'` vào `HUB_SUBSYSTEMS`; (2) 3 màn lẻ cấp 1 (my-todo/my-job/tasks daily-report) → nút rail đi thẳng qua `deriveHubNavLinks`+`hubNavLinksFor` (hub.js) + render trong `SaleHubSidebar.vue`, KHÔNG đổi mảng groups; (3) 6 nhóm ERP xám mờ tự động. Dashboard overview ngoài phạm vi.
  Verify: assign my-todo rail navy+teal + 3 nút lẻ + highlight đúng; click nhóm bung panel (12 chức năng); nhóm ERP xám; regression Bán hàng (/sale/dashboard) 0 error, không nút lẻ.
  File đụng: `components/subsystem-menu/hub.js`, `components/sale/SaleHubSidebar.vue`.
  Bước tiếp: user review giao diện → OK thì commit 2 file lên `gop_db`.
  Spec: docs/superpowers/specs/gop-db/2026-08-10-menu-quan-ly-cong-viec-design.md | Tóm tắt: .plans/gop-db/menu-quan-ly-cong-viec/design.md

- ke-hoach-phat-trien-thi-truong → @namdangit → .plans/gop-db/ke-hoach-phat-trien-thi-truong/plan.md
  Trạng thái: **THÊM FILE BÁO CÁO THỨ 2 — "Báo cáo tổng hợp nhu cầu khách hàng" (Task 60→66)** (wrap up 2026-08-20, verify Playwright 1440, 0 lỗi console). Desktop DONE, chờ user review; RESPONSIVE vẫn hoãn.
  **File MỚI:** `bao-cao-ket-qua-cham-soc-khach-hang-tiem-nang.html` (xem qua `python3 -m http.server 8952` trong thư mục feature) — layout bám ảnh Excel "Báo cáo tổng hợp nhu cầu khách hàng", style tái dùng nguyên token + component của file báo cáo meeting. Nội dung: **toolbar 7 bộ lọc** (Kỳ xem theo thời gian bắt đầu họp · Lĩnh vực KD · Khách hàng · cascade Công ty ▸ Phòng ban ▸ Bộ phận ▸ Kinh doanh chủ trì) · **KPI** (tổng nhu cầu / tổng giá trị đầu tư / khách hàng / chưa có dự án TKT) + 3 khối phân bổ · **bảng outline 3 cấp** `I` Lĩnh vực KD → `1` Thị trường → `1.1` Khách hàng, 10 cột, sticky header + TỔNG CỘNG · **2 chế độ cột** (CHI TIẾT 10 cột ↔ TỔNG HỢP 4 cột, ẩn hết cột rỗng) · nút **"+ TẠO MỚI"** cột Dự án TKT → popup tạo dự án (mã `TKT.YYYY.<viết tắt KH>`) → trạng thái **"Đã lập dự án TKT"** · **click tên meeting → drawer chi tiết meeting** (khung `.ticket-drawer` của file báo cáo meeting, 4 khối + nút Tạo dự án TKT) · Xuất Excel + In báo cáo (tổng hợp/chi tiết, A4 ngang) bám chế độ đang xem · data demo **26 nhu cầu / 18 KH / 4 lĩnh vực / 3 thị trường**.
  Treo thêm: chốt Lĩnh vực KD có cần **chọn nhiều** không (hiện select đơn theo yêu cầu "dùng đúng select như file mẫu", ảnh Excel ghi "select chọn nhiều").
  **File báo cáo ĐỘC LẬP:** `bao-cao-ket-qua-meeting-theo-thi-truong.html` (xem qua `python3 -m http.server 8931` trong thư mục feature). File `...-mockup-meeting.html` nay chỉ còn **2 tab** (Công việc của tôi · Lịch meeting) — tab 3 đã gỡ.
  **Task 44→59 (2026-08-19):** bảng OUTLINE 3 cấp `I / 1 / 1.1` (bỏ rowspan) + cột STT · **2 chế độ cột**: TỔNG HỢP (mặc định tới cấp Khách hàng, mỗi phòng ban 1 cột + Tổng, ẩn cột chi tiết; dòng meeting hiện dấu tick, dòng nhóm hiện số) ↔ CHI TIẾT (13 cột) · cột **Phòng ban** (của người chủ trì) + bộ lọc cascade **Công ty ▸ Phòng ban ▸ Người chủ trì** (lọc phòng/công ty → chỉ hiện cột phòng đó ở bảng/summary/Excel/bản in) · **sắp xếp mọi cột dữ liệu** (từ "Thời gian" sang phải, asc→desc→mặc định; giữ cấu trúc nhóm) · **sticky** hàng tiêu đề + dòng TỔNG CỘNG (dời lên đầu bảng) · click cả dòng meeting → panel chi tiết (drawer của Lịch meeting) · click số ở dòng TỔNG CỘNG → **popup danh sách meeting** kèm nút In + Xuất Excel riêng · **nút In báo cáo** (popup chọn In tổng hợp / In chi tiết, A4 ngang, bám bộ lọc) · **dải tổng hợp thiết kế lại** (4 ô KPI + thanh xếp chồng trạng thái + thanh ngang phòng ban/thị trường), bộ lọc chuyển LÊN TRÊN dải này + nút Ẩn/Hiện tổng hợp · bỏ hẳn nhận dạng "KH mới", tên meeting chữ thường, tăng tương phản 3 cấp màu · **data demo 30 meeting / 11 KH / 3 thị trường** (Hà Nội 14 · TP.HCM 8 · Đà Nẵng 8), phòng ban cân đối 11/11/8.
  Treo: chốt tên 2 công ty demo (tạm Tân Phát ETEK / Tân Phát Sài Gòn) · xử lý bản copy lệch `quan_ly_cong_viec_ca_nhan.html`.
  **Task 43 (2026-08-11):** cột Khách hàng nâng thành ô gộp `rowspan` (đặt sau Thị trường, bỏ khỏi từng dòng meeting, header vẫn 13 cột) → nhóm meeting theo khách hàng; meeting trong 1 KH xếp **cũ→mới**; KH mới vẫn nổi đầu; ô gộp giữ badge KH mới + nút "Xem lịch sử meeting"; Xuất Excel đồng bộ thứ tự. Chỉ sửa `...-mockup-meeting.html` (bản copy `quan_ly_cong_viec_ca_nhan.html` nay đã LỆCH). Helper mới: `groupTicketsByCustomer()`/`buildCustomerGroupCellHtml()`.
  → File chính `...-mockup-meeting.html` (bản copy `quan_ly_cong_viec_ca_nhan.html`): **3 tab** — (1) **Công việc của tôi** (My To Do, tab đầu mặc định: Task/Issue/Cá nhân, nhóm theo thời gian thu gọn/mở rộng đúng màn thật) · (2) **Lịch meeting** (màu nền thẻ theo trạng thái, nút Thêm meeting, drawer nút theo trạng thái) · (3) **Kết quả meeting theo thị trường** (bảng + lọc Thị trường/Trạng thái/Loại/Kỳ + Xuất Excel + KH mới phát triển + cột Dự án TKT + chấm công GPS chỉ Hoàn thành + summary lưới text). Bản `...-mockup.html` (gốc 3 loại) giữ nguyên.
  File: `ke-hoach-phat-trien-thi-truong-mockup.html` (self-contained). Style navy+teal đồng bộ menu Bán hàng.
  **PIVOT v2:** bỏ tab → **1 màn LỊCH phiếu công việc** (Tháng/Tuần). 4 loại phiếu thẻ màu: Phiếu công tác (teal) · Meeting (xanh dương) · Phiếu giao việc (tím) · Task (cam), mỗi thẻ = màu loại + giờ + badge trạng thái (Chờ duyệt/Đang thực hiện/Hoàn thành/Từ chối). 32 phiếu mock.
  Toolbar: Tháng/Năm · Phòng ban · Nhân viên · Người theo dõi · Thị trường · **Loại phiếu · Trạng thái** · Tìm kiếm + **Xóa lọc** — TẤT CẢ lọc thật (re-render lịch + 4 box đếm theo loại). Click thẻ → popover → "Xem chi tiết" → drawer đầy đủ. Đã BỎ footer Đánh giá/Ghi chú.
  v1 (2 tab: accordion thị trường + KPI trạng thái KH) giữ làm phụ lục trong spec.
  **Phase 6 (bám style thật + visual):** khảo sát UI thật `/sale/quotations` → dựng lại filter theo `V2BaseFilterPanel` (card trắng + header teal + quick search + [Tìm kiếm]/[Làm mới] + khối nâng cao lưới 4 cột), lọc AND chạy đúng; 4 box compact; calendar nâng cấp header teal + phân biệt cuối tuần/hôm nay.
  **Phase 7 (tinh chỉnh — feedback lần 2):** (1) chip góc phải = **lọc nhanh theo loại**. (2) **Summary ngữ cảnh**: Loại=Tất cả→box; Loại=1 loại→dải breakdown. (3) **De-bold** chữ ô ngày. (4) **Thiết kế lại** hôm nay/T7/CN tinh tế.
  **Phase 8 (bám dữ liệu THẬT — khảo sát app):** BỎ Phiếu giao việc → **3 loại** (Phiếu công tác/Meeting/Task). Mỗi loại dùng **trường + trạng thái THẬT** khảo sát từ `/assign/assign_business`, `/assign/meeting`, `/assign/tasks`: Công tác(6 tt)/Meeting(4)/Task(4+Quá hạn). Card/popover/drawer đổ đúng bộ trường riêng theo loại; badge màu semantic. Filter Trạng thái **động theo loại**; summary breakdown theo bộ trạng thái thật của loại. Verify Playwright 1440. (Data spec: mục 3B/5B/9B.)
  Concern nhỏ chờ user: khi lọc đồng thời Loại + 1 Trạng thái, dải breakdown chỉ còn 1 mục ≠0.
  **Phase 9 (single-user + gọn filter):** BỎ card bộ lọc trên; màn theo dõi **1 user** (topbar "Lịch công việc — Nguyễn Văn A"); chỉ giữ **Thị trường + Trạng thái** trong **header card calendar**.
  **Phase 10 (màu + card + data + summary):** (1) Task KHÔNG lọc theo Thị trường (chip Task → disable Thị trường). (2) Đổi màu 3 loại tương phản mạnh: công tác `#0d9488` / meeting `#4f46e5` / task `#ea580c`. (3) Thẻ item: dòng1 **icon tròn loại** + tiêu đề, dòng2 **thời gian "Từ - Đến"** + badge trạng thái. (4) Data demo chuẩn: ngày tương lai KHÔNG Hoàn thành/Quá hạn. (5) Summary chọn 1 loại thành **stat-card ấn tượng** (số lớn + pills trạng thái). Verify Playwright 1440.
  **Phase 11 (drawer):** Bỏ popover — click thẻ mở **thẳng drawer**; redesign drawer ấn tượng (header banner gradient theo loại + khối card per-type, meeting có link Meet); **thu nhỏ font + nén gọn** drawer (460px). Verify Playwright 1440.
  **Bổ sung filter:** "Loại meeting" (`#filter-meeting-type`) chỉ hiện khi chọn Meeting (Tất cả + 8 loại distinct), lọc thật, ẩn/reset khi đổi loại — cùng cơ chế disable Thị trường cho Task.
  **Phase 12 (phiếu nhiều ngày):** thêm `endDate` + phiếu multi-day 3 loại (có vắt tuần). View Tháng: **thanh trải** theo lane toàn cục, cắt theo tuần, bo góc/mũi tên ‹› khi còn tiếp, DOM 6 khối tuần (lane layer + day layer chung grid → thẳng hàng). View Tuần: span cột dải "Cả ngày". Drawer "Từ dd/MM – dd/MM", đếm 1 lần/phiếu. Sau đó: multi-day NẰM DƯỚI số ngày, "+N khác" chỉ khi >3, nền transparent bớt chói, **border chia ngày rõ** (liền mạch qua 3 lớp). Verify Playwright 1440.
  **Phase 13 (biến thể CHỈ-MEETING):** clone `...-mockup-meeting.html` (bản gốc 3 loại giữ nguyên) rồi rút gọn về chỉ Meeting: bỏ 3 chip/legend/logic loại, filter luôn hiện Thị trường+Trạng thái(meeting)+Loại meeting, summary luôn stat-card Meeting, topbar "Lịch Meeting", màu indigo, giữ multi-day/drawer/border. Verify Playwright 1440.
  **2 file mockup:** `...-mockup.html` (3 loại, meeting = **tím** indigo) + `...-mockup-meeting.html` (chỉ Meeting, màu = **xanh ngọc** `#06b6d4`). Đã thêm Tên khách hàng trên thẻ (cả 2). Chạy qua http.server (vd port 8912).
  **Bản meeting — 2 TAB:** (1) **Lịch meeting** (calendar như cũ) · (2) **Meeting theo thị trường** = **BẢNG** meeting-centric (theo mẫu mới): header 2 tầng navy, gộp rowspan **Thị trường**; cột: Meeting(Tên/Loại/Thời gian/Địa điểm) · Người chủ trì · Thành phần tham gia(Khách hàng/Thành phần công ty/Thành phần bên KH) · Kết quả meeting(Trạng thái/Biên bản họp-Lý do huỷ). Mỗi meeting 1 dòng; địa điểm online→"Trực tuyến"+link. Field `ketQua`, `nguoiChuTri`, `bienBan`.
  **Bảng tab2 tinh chỉnh (Task 32):** header 2 hàng đồng màu navy; Thị trường = **tỉnh/thành** (bỏ vùng miền + bỏ meeting nội bộ khỏi tab2); chỉ click **Tên meeting** (link) mở drawer; trạng thái dạng **badge**; meeting **Hoàn thành → nút "Xem biên bản" → popup biên bản** đúng mẫu app thật (bảng Nội dung-vấn đề/Phương án xử lý/Người đề xuất/Người thực hiện/Hạn dự kiến + Kết luận cuộc họp); summary thêm **thống kê theo thị trường**.
  **Tinh chỉnh (Task 33):** summary 2 nhóm "Theo trạng thái" + "Theo thị trường" cùng 1 hàng; header bảng tab2 = màu header lịch (teal); +3 meeting Hoàn thành có thị trường (4 nút "Xem biên bản"); thành phần Cty/KH = **chip avatar**; drawer chi tiết: nhãn + tiêu đề khối **chữ thường** (bỏ uppercase), font nhỏ, ít bold.
  **Task 34:** Thành phần công ty = chip **avatar**; Thành phần bên KH = tên + **chức vụ**; ô Khách hàng có nút **"Xem lịch sử meeting"** → popup liệt kê các lần meeting với KH đó.
  **Phase 15 (2026-08-10):** (Task 35) popup lịch sử meeting sort mới→cũ + cột nhân sự + header teal chung + nút Xem biên bản. (36) header bảng 1 cấp + cột "Phiếu công tác/Lịch sử chấm công" (popup chấm công GPS tab theo người) + hover row đậm hơn. (37) lọc Thị trường/Trạng thái/Loại + **Kỳ** (Hôm nay/Tuần/Tháng/Quý/Năm/Tuỳ chọn) + **Xuất Excel**. (38) nút "Thêm meeting" quick-add + drawer nút theo trạng thái (Sửa/Duyệt/Xem biên bản). (39) **KH mới phát triển** (badge+highlight, đưa lên đầu) + cột **Dự án TKT** (chỉ Hoàn thành). (40) summary nhóm Tổng hợp (dự án/KH mới/tỷ lệ HT) + đổi **lưới text** (bỏ chip); chấm công CHỈ meeting Hoàn thành; đổi tên tab2 → "Kết quả meeting theo thị trường". (41) thêm tab **Công việc của tôi** (My To Do) làm tab đầu + đổi tên màn **"Quản lý lịch làm việc cá nhân"** + topbar gọn; group thu gọn/mở rộng đúng `TodoGroupHeader.vue`/`TodoMainList.vue`; chỉ Task/Issue/Cá nhân. (42) lịch meeting **màu nền thẻ theo trạng thái**.
  Bước tiếp: user review desktop → chỉnh → chốt (có tách file riêng cho "Công việc của tôi"?) → responsive → port Vue + đồng bộ My To Do với data thật.
  Spec: docs/superpowers/specs/gop-db/2026-08-08-ke-hoach-phat-trien-thi-truong-design.md | Tóm tắt: .plans/gop-db/ke-hoach-phat-trien-thi-truong/design.md

- menu-ban-hang → @namdangit → .plans/gop-db/menu-ban-hang/plan.md
  Trạng thái: **PORT STYLE "CHỐT" VÀO CODE THẬT — DONE + VERIFY PLAYWRIGHT** (wrap up 2026-08-08). Client nhánh `update_sidebar_menu` (con `gop_db`), API `menu_phan_he_2026`. Tất cả CHƯA commit.
  Áp style navy+teal (port từ mockup chi-tiet-bao-gia) cho **14 phân hệ hub** (`HUB_SUBSYSTEMS`) qua `.sale-theme`, KHÔNG sửa V2 chung:
  · Sidebar navy + ribbon lụa (bg data-URI) + box tên phân hệ sát đỉnh nổi bật + icon phân hệ tô trắng glow + **màu icon menu theo mockup** (palette `CAT_COLORS`).
  · Topbar navy gradient + **wave line sáng mép dưới** (`::after`). Header bảng **#20d9ea** (gradient nhẹ + viền + `nowrap`). Tiêu đề card teal.
  · Panel menu: icon ngữ cảnh cấp 2 (`SCAT_ICONS` trong `SaleHubSidebar.vue`) + nền gradient + accent **xanh** đồng bộ (override `--acc`).
  · Form báo giá (tạo/sửa/xem): Thông tin chung lưới ô + "Loại tiền tệ" 1 dòng + **chip Bảng giá (xanh) / Giảm giá (cam)** + Giảm giá đưa lên header card "Chi tiết báo giá".
  File đụng: `assets/scss/sale-theme.scss`, `components/sale/SaleHubSidebar.vue`, `pages/sale/quotations/_id/index.vue` (client) + `Modules/Assign/Routes/api.php` (API — **alias route `sale/quotations`** fix 404 "không tìm được báo giá": FE gọi sale/quotations nhưng BE chỉ có assign/quotations).
  Bước tiếp: user review 14 phân hệ hub + form báo giá → OK thì báo @junfoke + commit/merge về `gop_db`; BE làm migration route `sale/*` đúng bài (thay cho alias tạm).
  Spec: docs/superpowers/specs/gop-db/2026-08-04-menu-ban-hang-design.md | Tóm tắt: .plans/gop-db/menu-ban-hang/design.md

- mockup-chi-tiet-bao-gia → @namdangit → .plans/gop-db/mockup-chi-tiet-bao-gia/plan.md
  Trạng thái: **MOCKUP ĐÃ QUA 6 PHASE TINH CHỈNH UI — chờ duyệt/định hướng tiếp** (2026-08-06, nhánh `gop_db`).
  File mockup HTML tĩnh mô phỏng màn Chi tiết báo giá thật (`/assign/quotations/80` = BG-2026-00080, *Đang tạo*):
  `chi-tiet-bao-gia-mockup.html`, self-contained (inline CSS + SVG, không CDN). Đủ 8 khối + menu flyout đầy đủ (port từ menu-mockup).
  Đã tinh chỉnh qua các phase (xem plan.md P0–P6):
  · **Màu nhận diện = NỀN màn chọn phân hệ** (navy `#0a1c3d→#1e57a0` + chủ đạo `#2E71C3`), KHÔNG dùng màu nhóm tím.
  · Topbar + sidebar navy hiện đại: glow mềm, active pill phát sáng, icon menu mỗi mục 1 màu.
  · Nền sidebar: **bó ~44 đường sóng ribbon** (SVG sinh bằng script, giống ảnh minimalistic gradient wave user gửi).
  · Card Thông tin chung **thu gọn được** (chevron → summary 1 hàng → đẩy bảng lên).
  · Tiêu đề card teal `#0a99a7`; header bảng teal nhạt + chữ teal (phương án B); button primary/outline/ghost.
  Verify bằng Playwright (qua http.server, Playwright chặn file://). Chạy tại `http://127.0.0.1:8899/`.
  Mục đích: SÂN THỬ NGHIỆM UI — CHƯA áp vào code thật; việc áp vào Vue thật thuộc `update-style-ban-hang`.
  Bước tiếp: tinh chỉnh bó sóng/animation/responsive, hoặc chốt để chuyển sang áp code thật.
  Spec: docs/superpowers/specs/gop-db/2026-08-06-mockup-chi-tiet-bao-gia-design.md | Tóm tắt: .plans/gop-db/mockup-chi-tiet-bao-gia/design.md

- update-style-ban-hang → @namdangit → .plans/gop-db/update-style-ban-hang/plan.md
  Trạng thái: **✅ DESIGN + SPEC + PLAN ĐÃ DUYỆT — chưa code (chờ chạy Phase 0 / note phần đầu tiên)** (2026-08-06, nhánh `gop_db`).
  Đổi style màn Bán hàng thật (`pages/assign/*`, dùng component V2 chung) theo **MISA**, **Cách A**: gate `.sale-theme` ở `default-sidebar.vue` (`isSaleSubsystem`) + 1 file `assets/scss/sale-theme.scss` (tokens teal từ demo kế toán). Chỉ Bán hàng, portable sau. KHÔNG sửa V2 dùng chung. Working mode: tăng dần theo ảnh MISA user note, verify Playwright.
  Plan: Phase 0 (Task 0.1–0.4 setup scaffold, cụ thể) + Phase 1+ backlog (bảng/filter/nút/badge/card/topbar — cụ thể hoá khi user note).
  Bước tiếp: chạy **Phase 0** → chờ user note phần đầu tiên (ảnh MISA + tên thành phần).
  Spec: docs/superpowers/specs/gop-db/2026-08-05-update-style-ban-hang-design.md | Tóm tắt: .plans/gop-db/update-style-ban-hang/design.md

- redesign-man-chon-phan-he → @namdangit → .plans/gop-db/redesign-man-chon-phan-he/plan.md
  Trạng thái: **CODE DONE + ĐÃ VERIFY TRÊN APP THẬT** (2026-08-03, nhánh `menu_phan_he_2026`). Còn: báo @junfoke + merge về `gop_db`.
  Thiết kế lại giao diện màn chọn phân hệ (`pages/index.vue`) sang **bố cục BÔNG HOA** trên nền xanh gradient tối:
  **nhụy tròn** ở giữa (hexagon TP pulse + vòng conic 4 màu xoay + **3 nhị** = lõi Thông tin NS/Danh mục/Quản trị, BỎ ERP),
  **4 cánh** = 4 nhóm nghiệp vụ (panel kính mờ, mũi nhọn hướng tâm, màu riêng, tagline, bỏ số thứ tự), gân sáng nối tâm→cánh,
  hiệu ứng glass/glow/float/hover. CHỈ đổi trình bày, registry vẫn là nguồn dữ liệu. Đã sửa: `subsystems.js` (`tagline`/`desc`/`erpGhost`/`erpLink`),
  `pages/index.vue` (viết lại bố cục hoa), `layouts/system.vue` (nền tối; chỉ index.vue dùng).
  ⚠️ 2 điểm đã xử lý: (1) **ghi đè có chủ đích** quyết định "ẩn hẳn" Mua hàng/Kho/Vận chuyển của `bo-sung-menu-phan-he` →
  hiện BÌNH THƯỜNG (không mờ) + desc riêng, click hiện toast "Tính năng đang phát triển" (chờ ERP làm xong gắn `erpLink`) — **CẦN BÁO @junfoke**.
  (2) Remix Icon: đã đo codepoint 26/26 LỆCH giữa v2.4.0 bundled & v4.3.0 CDN → **không dùng `ri-*`**, badge dùng SVG `image` tô trắng (`brightness(0) invert(1)`),
  nút Đăng xuất inline SVG. Verify desktop bằng mockup dùng chính SVG dự án (nhiều vòng, user đã duyệt concept).
  **Đã polish nhiều vòng (v3):** điểm sáng spark thay hexagon; **2 vòng nhụy xoay ngược chiều**; lá almond + **viền ánh sáng** (mask-composite); fit **1 màn không scroll** + greeting sát top;
  **icon nhóm** (gom vào `SUBSYSTEM_GROUP_META.icon`, dùng chung màn hoa + switcher); tăng tương phản chữ; box-shadow lá chỉ khi hover; nền lá mờ hơn.
  **Popup chuyển phân hệ (SubsystemSwitcher)** cũng đồng bộ: mỗi nhóm full-width + phân hệ 3 cột, badge tròn màu nhóm, icon nhóm, ghim **sát mép phải + sát topbar**, shortLabel, ghost→toast, bỏ nhóm ERP + bỏ số thứ tự.
  File thêm: `components/SubsystemSwitcher.vue`, `components/BasicSubsystem.vue` (CSS ghim dropdown).
  Bước tiếp: **user chạy hrm-client (Node 14)** soi 2 màn thật (chọn phân hệ sau login + popup icon lưới topbar): animation, hover, sát topbar/phải, toast; test cờ use_rice/use_erp/is_use_decision.
  ⚠️ Môi trường phiên làm là Node 12 → chưa chạy Nuxt dev để test end-to-end.
  Spec: docs/superpowers/specs/gop-db/2026-08-03-redesign-man-chon-phan-he-design.md | Tóm tắt: .plans/gop-db/redesign-man-chon-phan-he/design.md

- wr-service-quotation (chứng từ 3) → @namdangit → .plans/gop-db/wr-service-quotation/plan.md
  📌 24/09/2026 — user chốt 4 việc treo: **bỏ** khối "Người duyệt" ở phiếu bảo hành · **không sửa**
  phạm vi Super Admin · **chưa làm** testcase/mô tả nghiệp vụ bản HRM · **giữ** phiếu thử id 10370.
  Luồng dịch vụ hết việc nhỏ treo; còn Phụ lục bổ sung/giảm + 4 mảng hợp đồng phụ thuộc phân hệ khác.
  Trạng thái: **HOÀN THÀNH CODE + ĐÃ TEST BE VÀ GIAO DIỆN** (2026-08-21). Chưa sinh testcase /
  mô tả nghiệp vụ. Cột "Giá vốn" khoá sau quyền `Xem giá vốn hàng hoá` (user chốt) — đã cấp quyền
  đó cho vai trò Super admin trên DB local để test.
  Port màn ERP "Phiếu cung cấp thông tin làm báo giá" — chứng từ THỨ 3 của dây chuyền dịch vụ.
  Phạm vi user chốt 2026-08-21: **chỉ chứng từ 3** (chứng từ 4 Báo giá dịch vụ để đợt sau), tiền
  **tính ở giao diện như ERP**, khối Phiếu bảo hành **giữ dữ liệu nhưng chưa dựng màn**.
  BE: 11 entity + service + notifier + print service + request + controller + 2 resource,
  13 route, 3 quyền mới (id 1515–1517), **KHÔNG migration** (12 bảng ERP đã có trên DB gộp).
  FE: 11 file `pages/customer-care/wr-information-requests/` + `utils/wrServiceQuotationMoney.js`
  + 1 mục menu; nút "Tạo phiếu cung cấp thông tin" ở chứng từ 2 đã nối sang màn này.
  ⚠️ Bảng dữ liệu **dùng chung với Báo giá dịch vụ** qua cột `type` — mọi truy vấn phải kèm `type`.
  Verify: toàn luồng chạy thật trên DB gộp (danh sách/lọc/xuất/in · prefill · lưu nháp · gửi đi kèm
  thông báo đúng người · từ chối · xoá trả trạng thái 2 chứng từ trước); module tính tiền FE đối
  chiếu **39 phiếu thật** khớp tuyệt đối với bản tính ở máy chủ; 11 file `.vue` compile sạch.
  Test GIAO DIỆN trên cổng 3002: lập phiếu · sửa số lượng · thêm dịch vụ · thêm thiết bị bảo dưỡng
  + gói · chuyển Sửa chữa ↔ Bảo hành · lưu · in · xoá · cảnh báo chưa lưu — **tìm và sửa 2 lỗi**:
  thiếu cờ quyền giá vốn ở màn lập mới, và **Lưu nháp luôn thất bại** vì cột `quotation_term`
  NOT NULL nhận `null` (đã thêm `fillDefaults()`).
  ⚠️ Nút "Tạo báo giá dịch vụ" chưa điều hướng được (chứng từ 4 chưa port) — tạm báo toast.

- warranty-repair-handle-request → @namdangit → .plans/gop-db/warranty-repair-handle-request/plan.md
  Trạng thái: **HOÀN THÀNH CODE + ĐÃ TEST + ĐÃ GIAO TÀI LIỆU** (2026-08-21).
  Tài liệu kèm theo: `testcase.xlsx` (87 TC), `Mô tả nghiệp vụ - Phiếu xử lý yêu cầu.docx`,
  testcase bản ERP ở `erp/.plans/warranty-repair-handle-request-erp/` (57 TC).
  Nút "Tạo phiếu cung cấp thông tin" nay đã nối sang chứng từ 3 (không còn báo toast).
  Port màn ERP "Phiếu xử lý yêu cầu" (`/admin/customer-care/warranty_repair_handle_requests`) —
  chứng từ THỨ 2 của dây chuyền dịch vụ, lập từ Phiếu yêu cầu kiểm tra sửa chữa – bảo hành.
  Đã khảo sát: 6 trạng thái · 4 quyền · 3 bảng (`warranty_repair_handle_requests` 5.259 dòng) ·
  mỗi dòng thiết bị chọn LỖI THIẾT BỊ (nhiều) + HÀNH ĐỘNG (Tư vấn điện thoại / CCTT làm báo giá).
  Mọi dòng đều "Tư vấn điện thoại" → phiếu và phiếu yêu cầu gốc đều thành "Đã tư vấn điện thoại";
  ngược lại → "Chờ CCTT", báo cho người có QUYỀN "Tạo phiếu cung cấp thông tin", phiếu yêu cầu gốc
  thành "Đã xử lý".

- warranty-repair-request → @namdangit → .plans/gop-db/warranty-repair-request/plan.md
  Trạng thái: **HOÀN THÀNH CODE + ĐÃ TEST + ĐÃ GIAO TÀI LIỆU** (2026-08-20).
  Code đã chuyển về đúng phân hệ CSKH (`Modules/CustomerCare`, `/customer-care/warranty-repair-requests`,
  menu CSKH → Kiểm tra bảo hành sửa chữa). Tài liệu kèm theo: `testcase.xlsx` (97 TC),
  `Mô tả nghiệp vụ - …docx` (11 chương), testcase bản ERP ở `erp/.plans/warranty-repair-request-erp/`.
  Port màn ERP "Yêu cầu kiểm tra sửa chữa – bảo hành" (`/admin/customer-care/warranty_repair_requests`)
  — chứng từ ĐẦU TIÊN của dây chuyền 9 chứng từ phân hệ Dịch vụ.
  Scope user chốt: **full như ERP** (3 tab · CRUD · Chuyển phòng tiếp nhận · Từ chối · In phiếu ·
  In danh sách · Xuất Excel), giữ đủ **9 trạng thái**, bảng thiết bị đủ **3 nguồn** tp/tpc/ncck,
  **copy nguyên tên quyền ERP**.
  BE: 8 file `Modules/CustomerCare` + 12 route + 4 quyền (id 1177–1180). **KHÔNG có migration** —
  2 bảng `warranty_repair_requests` (5.625 dòng) / `warranty_repair_request_products` đã có sẵn.
  FE: 9 file `pages/customer-care/warranty-repair-requests/` + 1 mục menu.
  Dùng lại đồ có sẵn: popup KH `ChooseErpCustomerModal`, thiết bị KH
  `assign/customers/{id}/equipment`, 2 mẫu in ERP `report_templates` 277/278.
  Verify: 3 tab + Resource + 2 mẫu in chạy thật trên DB gộp; 9 file `.vue` compile sạch.
  ⚠️ Nút "Tạo phiếu xử lý yêu cầu" chưa điều hướng được (màn đó chưa port) — tạm báo toast.
  📌 Session này còn sửa **tài sản chung**: bổ sung quy tắc "BE trả `status_color`" + bảng 9 mã màu
  chuẩn vào `.claude/skills/list-page/SKILL.md` (mục 3c-1, 3c-2) và `CLAUDE.md` → cần PR riêng.

- customer-export-file (Phase 7) → @khoipv → .plans/gop-db/customer-export-file/plan.md
  Trạng thái: **XONG CODE, CHỜ USER TEST TRÌNH DUYỆT** (2026-08-17). Chuyển việc dựng file
  CSV/Excel/PDF của `/assign/customers` từ BE sang **build ở FE** theo yêu cầu user.
  BE thêm `GET assign/customers/export-rows` (JSON theo trang, dùng chung bảng cột với 3 endpoint
  xuất file cũ — 2.000 dòng/lượt ~0,85s, RAM 60MB). FE thêm `utils/export/customerExportFile.js`
  (ExcelJS + jsPDF/autoTable + font DejaVu subset 78KB, import động).
  ⚠️ Team phải `npm install` sau khi kéo nhánh (thêm `jspdf` + `jspdf-autotable`).
  ⚠️ Chưa đo được thời gian DỰNG file ở trình duyệt với 17.5k dòng — nhất là PDF (~600 trang).
  3 endpoint export cũ của BE vẫn giữ nguyên, chưa xoá.

- history-action-groups → @dnsnamdang → .plans/gop-db/history-action-groups/plan.md
  Trạng thái: **CODE DONE + ĐÃ TEST (2026-08-15)**. Chuẩn hoá bộ lọc "Loại hoạt động" của khối/popup
  Lịch sử về **đúng 3 nhóm cố định dùng chung cho cả 10 màn**: `create` Tạo mới · `update` Thay đổi
  thông tin · `status` Thay đổi trạng thái. Trước đây mỗi entity tự khai danh mục riêng (KH 5 loại,
  task 3, phiếu bàn giao 8) + nhãn gắn tên đối tượng nên mỗi màn một dropdown.
  Mấu chốt: **nhóm chỉ dùng để LỌC, nhãn chi tiết từng dòng vẫn giữ trên timeline** → không màn nào
  mất khả năng lọc (7 hành động của Phiếu bàn giao đều là chuyển trạng thái → gom vào `status`).
  BE: `SystemLogService` thêm `ACTION_GROUP_LABELS`/`ACTION_GROUP_MAP`/`groupOfAction()`, `finalize()`
  gắn `action_group` cho mọi log, `getFilterOptions()` trả 3 nhóm cho mọi type.
  ⚠️ Bẫy đã tránh: mở cố định cả `performers` thì `performerOptions()` không lọc được công ty cho 9 loại
  còn lại → liệt kê **toàn bộ 783 nhân viên**; nên `performers` vẫn chỉ trả cho `customer`.
  FE: `SystemInfoSection.vue` + `CustomerHistoryModal.vue` lọc theo `action_group`, options hard-code 3 nhóm.
  Đã ghi vào tài sản chung: skill `entity-history` §0a + `CLAUDE.md` (nguyên tắc **bản ghi đã khoá thì
  không cho sửa/xoá — chặn ở BE bằng 423, FE chỉ ẩn nút**).
  Bước tiếp: user review. **Chưa port sang `tpe-develop-assign`** (nhánh đó cũng có khối Lịch sử) — chờ chốt.

- filter-customization → .plans/gop-db/filter-customization/plan.md
  Trạng thái: **CODE DONE Phase 1–3 — chờ chạy migration + user test** (2026-08-12, nhánh `gop_db`, cả 2 repo).
  Cho user tự chọn trường lọc hiển thị + **kéo thả sắp xếp vị trí** (popup "Cài đặt bộ lọc"), giống "Tuỳ chỉnh cột" nhưng cho bộ lọc; mặc định hiện đủ. UX tham chiếu demo kế toán `demo 3/assets/app.js` (`setupFilterSettings` chưa kéo thả + `setupColumnConfig` có kéo thả) → ghép 2 cái, lưu BE thay localStorage.
  Chốt: bảng mới **generic** `filter_customizations (created_by, table, config json)` unique(created_by, table) — KHÔNG copy schema cột-mỗi-màn của `column_customizations` (Entity đó 25 cột trong `$casts`, thêm màn là phải migration); khoá màn = tên bảng chính (`'customers'`); `config = [{key,isVisible}]`, thứ tự mảng = thứ tự hiển thị, không lưu label; bỏ tick = **ẩn hẳn + reset giá trị lọc** (tránh lọc ngầm); không có field locked; **component mới**, KHÔNG sửa `V2BaseFilterPanel`.
  BE (`gop_db-api`): migration + `FilterCustomization` (có khai `$table`) + Service + FormRequest + Controller + 2 route `human/filter-customizations`, không thêm quyền.
  FE (`gop_db-client`): `components/V2BaseSmartFilterPanel.vue` (schema field + slot escape hatch `#field-<key>` + `wrapperClass`/`hideLabel`/`resetKeys` cho field gom nhiều control) + `components/modal/filter-customization-modal.vue` (checkbox + vuedraggable). **Merge DB ↔ schema nằm trong component**: key mất khỏi FE → bỏ hẳn, key mới → append cuối và hiện ⇒ bổ sung trường lọc sau này không lỗi.
  Pilot: `pages/assign/customers/index.vue` — 15 field khai báo bằng `filterFields`, khối Công ty/PB/NV và CascadePairSelect đi qua slot. Class wrapper đổi `advanced-filters` → `smart-advanced-filters` để dropdown CascadePairSelect không bị cắt (rule scoped cũ ở page đã bỏ).
  Spec: docs/superpowers/specs/gop-db/2026-08-12-filter-customization-design.md
  Bước tiếp: chạy `php artisan migrate` (module Human) → build FE → user test popup Cài đặt bộ lọc trên `/assign/customers`.

- customer-list-empty-placeholder → .plans/gop-db/customer-list-empty-placeholder/plan.md
  Trạng thái: **CODE DONE — CHỜ USER TEST TRÌNH DUYỆT** (2026-08-12, nhánh `gop_db`, 2 file).
  Ô "không có dữ liệu" ở màn `/assign/customers` hiển thị không đồng nhất: mọi cột ra `—` (em dash),
  riêng **SĐT ra `-`** vì `CustomerListResource` tự chèn sẵn chuỗi `'-'` từ BE (cả khi trống lẫn khi
  bị che do không phải KH của mình) → FE nhận chuỗi khác rỗng nên `|| '—'` không chạy.
  Fix: BE trả `null`, placeholder do FE quyết định; popup chọn KH thêm slot fallback `#cell()`
  (7 cột trước đây để ô trắng, riêng SĐT ra `-`) → tất cả về `—`.
  Giữ nguyên `'-'` trong file xuất CSV/Excel (`CustomerExportFormatter::taxCodeOrMobile`) — theo mẫu ERP,
  ngữ cảnh file bàn giao khác màn hình. Không migration, không quyền mới.

- khai-quy-che-cau-hinh → @namdangit → .plans/gop-db/khai-quy-che-cau-hinh/plan.md
  Trạng thái: **Slice 1 (Công nợ versioning) + Slice 2 (tổng quát hoá + 2 tab scalar chietkhau/kythuat)
  + Slice 3a (hạ tầng scope `global` → bảng `configs` singleton, chứng minh qua tab baogia ở tầng service/cron)
  ĐỀU ĐÃ CODE + test XONG. Final whole-branch review (opus) từng slice CLEAN/SẠCH, không finding chặn** (2026-09-14).
  Chờ USER QA trình duyệt + quyết định commit (git chưa được uỷ quyền).
  Test Slice 3a: 4 suite xanh — GlobalScope 4/4 · Congno 14/14 byte-identical · Scalar 5/5 · Registry 6/6 (CR=0 cả 8 file).
  Slice 3a thực thi bằng SDD, ledger: `hrm-api/.superpowers/sdd/2026-09-14-khai-quy-che-slice3a-global-scope-infra/progress.md`.
  Kiến trúc: `RegulationTabRegistry` (registry-driven, per-field store config/company) + `RegulationConfigService` generic
  theo `tab_key` + scope (company→`companies`/`company_regulation_histories`; global→`configs`/`regulation_config_histories` MỚI)
  + controller/route generic `regulation-config/{tabKey}` (mới cho scope company) + FormRequest rule động.
  Slice 3a thêm: 2 migration (3 cột `companies` cho hanghoa/dieukhoan 3b + bảng `regulation_config_histories`).
  Backlog Slice sau (từ review, non-blocking): [Slice 3b] snapshot-wipe — global version ghi TRỌN 10 field config,
  field thiếu = null xoá cột → controller/FE 3b PHẢI round-trip đủ 10 field config; getTabConfig trả kèm `payload`
  cho modal hẹn; field non-API bị drop âm thầm ở modal hẹn; congnoLoading race.
  Data-hygiene ĐÃ XONG (user chốt "làm như ERP có"): đã `UPDATE configs SET customer_register_expiry=30`
  (khớp ERP ConfigSeeder); 5 cột nullable vốn đã NULL đúng ERP-fresh, is_equipment=1 giữ nguyên.
  Đã fix test (backup đủ 10 cột store=config) nên không làm bẩn DB thêm.
  Spec hoàn thiện 13 tab: `docs/superpowers/specs/gop-db/2026-09-14-khai-quy-che-hoan-thien-cac-tab-design.md`.
  Plan Slice 2: `docs/superpowers/plans/gop-db/2026-09-14-khai-quy-che-slice2-generalize-scalar-tabs.md`.
  Plan Slice 3a: `docs/superpowers/plans/gop-db/2026-09-14-khai-quy-che-slice3a-global-scope-infra.md`.
  **Slice 3d — tab `khac` (scope PHÒNG BAN) XONG BE + FE** (2026-09-14): thêm scope `department` (ghi thẳng 3 cột
  `departments` risk_fund/profit_percent/max_value_contract của 1 phòng ban; lịch sử → `regulation_config_histories`
  scope_type='department' scope_id=department_id, KHÔNG dùng company_regulation_histories vì cột buộc company_id).
  BE: `RegulationConfigService` (SCOPE_DEPARTMENT + storeForScopeType + applyVersion/applyDueVersions/updateVersion/
  recomputeDiffChain nhánh department) · controller (`departments()` endpoint + resolveScopeId/refreshScopeId/
  assertDepartmentInCompany, tab scope=department đọc/ghi theo department_id, gate PB thuộc công ty hiện tại) ·
  route `regulation-config-departments` · FormRequest thêm `department_id`. Test: RegulationKhacDepartmentTest 3/3 +
  registry unit (khac=department scalar) — full MasterData suite 61 passed. FE: `index.vue` fetchTab/applyTabToModel/
  onSave/curTabIsApi/watch curGroup scope-aware (DEPT_API_TABS=['khac'], gửi department_id GET+POST, đổ vào
  model.department.groups); picker phạm vi thay mock SCOPE_UNITS bằng phòng ban THẬT (endpoint mới, selectedDeptId int,
  re-fetch khi đổi phòng); `data.js` nhãn khac khớp registry BE. CR=0 index.vue+data.js.
  **Slice 3d — tab `themquy` (ladder, scope PHÒNG BAN) XONG BE + FE** (2026-09-14): `departments.conditions_quarter_bonus`
  (json bậc thang GIỮ ĐÚNG khoá ERP money_from/money_to/percent + comparator) + `rate_reward_progressive_tp/tbp/nv`.
  **Ruling B**: lịch sử → `RegulationConfigHistory` scope=department (KHÔNG dual-write bảng audit ERP
  `department_condition_quarter_bonus_histories` — test assert count=0). BE: registry themquy (type=json input='ladder',
  item_rules percent 0-100, 3 decimal) + FormRequest `validateQuarterBonusLadder` (per-row from<to + ∑tp/tbp/nv=100).
  FE `index.vue`: DEPT_API_TABS=['khac','themquy']; verbar inline "Ngày áp dụng" + pending-queue cancel-only (ẩn nút sửa
  vì ladder không dùng modal hẹn); bảng bậc thang V2BaseSelect(ladderFromOps/ToOps)+V2BaseCurrencyInput(money rỗng=INF)+
  V2BaseInput%; addLadderRow/removeLadderRow; applyTabToModel/collectTabValuesFromModel nhánh themquy (ladder+progressive);
  ladderRateValid tô đỏ #dc2626 + chặn onSave; cancelPending nhận cả DEPT_API_TABS. `data.js` mock ladder → object khoá ERP.
  Test: RegulationThemquyDepartmentTest 3/3 + registry unit `registers_themquy_as_department_ladder_tab` — MasterData suite
  65 passed. CR=0 index.vue+data.js.
  **Slice 3d — tab `hoahong` (GRID per-dòng, scope PHÒNG BAN) XONG BE + FE (2026-09-15) → Slice 3d ĐÓNG**:
  tab phức tạp nhất, mỗi dòng lưới = 1 bản ghi `regulations` (objectable_type App\Model\Common\Department,
  objectable_id=department_id), KHÔNG staging version — 2 cột nullable effective_date/status ghi THẲNG `regulations`.
  BE: migration đã chạy; registry SHAPE_GRID 18 field metadata (loại khỏi mọi helper scalar); controller show() rẽ
  getGridConfig + storeGridRow/updateGridRow/destroyGridRow (gate currentCompanyId + assertDepartmentInCompany, ownership
  403, actorId=auth()->id()), route version rẽ 404 cho tab grid; RegulationCommissionRowRequest (condition_sale_type
  required_if type=1; value_end gt start; ∑department/part/employee=100 VÀ ∑*_bonus_contract=100; conditions_commissions
  [from_day<to_day, receive_percent 0..100]); ScheduleRegulationVersionRequest guard isGridTab; service statusForEffective/
  fillGridRow (sale_type=0 khi type≠1, after_commission_type ép=1)/presentGridRow (is_applied/is_pending/status_text)/
  getGridConfig/CRUD/applyDueGridRows (cron flip pending→applied theo dòng); history buildGridHistoryDiff numeric-aware
  TRƯỚC save (đã FIX bug false-diff decimal Laravel-8). Routes POST/PUT/DELETE `regulation-config/{tabKey}/grid[/{rowId}]`.
  Test: RegulationHoahongGridTest 10/10 + registry unit `registers_hoahong_as_department_grid_tab` — full MasterData suite
  **76/76**. CR=0 (4 file BE LF nguyên trạng). NOT committed (rule gop_db).
  **FE grid wiring hoahong XONG (2026-09-15)** — đủ 6 bước bàn giao: GRID_DEPT_TABS=['hoahong'] (ngoài DEPT_API_TABS);
  fetchGridTab GET `.../hoahong?department_id=` → applyGridConfig {fields→gridFieldOptions, rows OBJECT}; tbody row-object
  (gridOptLabel/gridNetText/fmtPercent/fmtDate + pill is_pending/is_applied, cột Thao tác gate canEditRegulation); modal reg
  bind 18 key BE + effective_date (condition_sale_type chỉ khi Number(condition_type)===1, condition_compare_type disabled
  'Giá net', conditions_commissions sub-table); openReg/saveReg (guard 2 nhóm ∑=100, POST/PUT `.../grid[/{id}]`, map 422
  inline)/deleteReg ($confirm→apiDelete `.../grid/{id}?department_id=`); import V2BaseCheckbox. **Ruling**: KHÔNG gọi
  markFormSaved (trang KHÔNG dùng unsavedChangesMixin — sibling scalar-tab onSave cũng không). CR=0 index.vue+data.js (LF).
  Chưa QA trình duyệt (code chưa deploy dev).
  **Slice 3f — Lịch sử quy chế THẬT (①A) + Dirty-guard rời trang (②A) XONG (2026-09-15) → Slice 3f ĐÓNG**:
  ①A thay mock `HIST` ở FE bằng endpoint BE thật `GET /v1/master-data/regulation-config-history?scope=company|department[&department_id=]`
  (gate `checkPermission:Cài đặt cấu hình` + `guard()` 403 + `currentCompanyId()`; scope ∉ {company,department}→422;
  department bắt buộc department_id + assertDepartmentInCompany). `RegulationConfigService::getHistory()` GỘP 4 nguồn/scope,
  sort created_at desc (tie-break `_seq` ổn định vì PHP 7.4 usort không stable), cắt 50 SAU sort, trả MẢNG VỊ TRÍ 6 phần tử
  `[timeStr, whoName, contentStr, scopeAppliedName, noteStr, isScheduledBool]`. Nguồn: company =
  `regulation_config_histories`(company scope_id + global 0) + `company_regulation_histories`(company_id) +
  `regulation_scheduled_versions` pending(company+global); department = `regulation_config_histories`(department) +
  `regulation_histories`(department_id, logs json) + scheduled pending(department). Format: time `d/m/Y H:i`,
  who="code - fullname" (join employees↔employee_infos 1 query, KHÔNG N+1), content "{label}: {old} → {new}" nối "; ",
  number_format QUỐC TẾ, bool→Có/Không, null/''→"—", >3 field → 3 + " …(+N)", scheduled prefix "Hẹn phiên bản mới — ".
  ②A: `index.vue` dùng `unsavedChangesMixin` (unsavedSnapshotSource→this.model), `guardLeaveDirty()` $confirm khi đổi
  tab/scope/phòng ban lúc đang sửa → xác nhận thì `revertCurrentTab()` re-fetch bỏ edit dở RỒI `markFormPristine()`
  (KHÔNG markFormSaved — cảnh báo vẫn bật cho lần sửa sau); reset baseline sau onSave/onCancel/saveVer/cancelPending/
  saveReg/deleteReg; beforeRouteLeave built-in. `data.js` gỡ export HIST + SCOPE_UNITS (CURRENT_COMPANY giữ, còn dùng).
  Review độc lập (opus) APPROVED không blocker (2 MEDIUM + 3 LOW + 2 NIT) → fix round 1 xử M1(sort stable)/M2(revert thật)/
  L1($type company field)/L2(null-safe created_at)/L3(3 test HTTP 403/422). Test: RegulationHistoryTest 6 (3 service + 3 HTTP)
  → full MasterData suite **82/82 PASS**. CR=0 cả 6 file (4 BE + 2 FE). NOT committed (rule gop_db).
  **FEATURE KHÉP VỀ MẶT CODE**: đủ 14 tab đều BE (registry 14 key) + FE (API_TABS 11 company + DEPT_API_TABS khac/themquy +
  GRID_DEPT_TABS hoahong) + test — KHÔNG còn tab mock. Slice 3b/3c (mixed/json/subtable) đã gộp vào wiring registry chung
  (đóng cùng 3d), Slice 3e (rà quyền + số quốc tế + line-ending + review cuối whole-branch) đã `[x]` hết. Lịch sử thật (①A)
  + dirty-guard (②A) có đủ.
  Chưa làm (đều NGOÀI PHẠM VI theo spec mục 11 — YAGNI): bước duyệt phiên bản (change_approver), diff JSON per-dòng,
  lưu version_id trên chứng từ, version-hoá 2 field fixed (Thuế vận tải/Ngày khai báo công nợ đầu kỳ), due_configs matrix.
  Backlog nhỏ non-blocking (LOW/NIT): comment double-limit-50, test HTTP cap-50/join>3 ở tầng service.
  Bước tiếp: user QA trình duyệt toàn màn (chưa deploy dev) → quyết định commit/merge về gop_db.
  **#13 Quy chế thưởng năm (port ERP "Cấu hình thưởng cuối năm công ty") — ✅ HOÀN THÀNH + ĐÃ COMMIT/PUSH gop_db**
  (24/09/2026): slice độc lập ĐÃ XONG và ĐÃ đẩy remote (khác phần còn lại của feature cha còn chờ QA/commit).
  Chi tiết đầy đủ chuyển xuống mục **## Hoàn thành** — hrm-api `bd3366c07` / hrm-client `4fbe1fc1f`
  (đều rebase sạch lên origin/gop_db, đã push, HEAD = origin/gop_db).
  --- (lịch sử) ---
  **UI mock XONG · MAPPING ERP XONG · đang brainstorm cơ chế "hẹn ngày áp dụng"** (2026-09-09).
  Gộp 1 màn HRM `/master-data/regulation-config` 3 miền cấu hình/quy chế ERP: (1) Cấu hình chung công ty
  (11 nhóm form), (2) Quy chế kinh doanh theo phòng ban (hoa hồng/lũy tiến/khác), (3) MỚI: "hẹn ngày áp dụng".
  Hướng A (port bảng ERP có sẵn). UI đã xong (mock): `pages/master-data/regulation-config/index.vue` + `data.js`
  + menu master-data. **Mapping ERP (đã dò 2026-09-09)**: Miền 1 = `configs` (singleton toàn hệ thống) +
  `companies`/`company_rule_commissions` (company_id) + `due_configs`/`company_due_configs` (công nợ); Miền 2 =
  `regulations` (polymorphic objectable_type Department/Part) + cột trực tiếp trên `departments`.
  ⚠️ **Phát hiện then chốt**: ERP KHÔNG có versioning theo ngày hiệu lực — chỉ overwrite + audit-log diff
  (`company_regulation_histories`, `regulation_histories`, `due_config_histories`). → "Hẹn ngày áp dụng" là phần
  HRM thiết kế mới hoàn toàn. Bước tiếp: chốt schema versioning → viết spec đầy đủ → duyệt → code (slice đầu:
  Cấu hình chung). Spec: docs/superpowers/specs/gop-db/2026-09-09-khai-quy-che-cau-hinh-design.md

- xuat-ban-hang-muon → @namdangit → .plans/gop-db/xuat-ban-hang-muon/plan.md
  Trạng thái: **CODE DONE Phase 1 (SDD) — FINAL REVIEW CLEAN, chờ USER QA + quyết định commit** (2026-09-04). Review tổng nhánh ra 1 defect D1 (escalation vượt hạn mức không kích hoạt) → đã fix (BE tự tính giá trị phiếu server-side `computeAmounts()` + persist cột `sum_amount_*`) → scoped re-review PASS. Port luồng "xuất bán
  hàng mượn" ERP → HRM (Module Finance) cho cả 3 loại HĐ (Firm/WrService/HĐ mới `hrm_quotation_id` — HĐ mới đi
  chung nhánh Firm). **Phase 1** = phiếu YC xuất bán hàng mượn (`BorrowSellRequest`, `PYCXBHM`), KHÔNG hạch toán/tồn.
  Execute qua subagent-driven (ledger `.plans/gop-db/xuat-ban-hang-muon/sdd/progress.md`). **XONG toàn bộ 13 task**:
  T1–T8 BE, T9 api.js, T10 list, T11a BE 2 endpoint nguồn + siết canBorrowSell (fix R-T11a-FIX-1), T11b FE create
  page (create.vue + 2 picker modal + BorrowSellRequestForm), T12 FE detail/print/deny/history, T13 unit test
  Calculator PASS + doc. Mọi task review SPEC PASS / QUALITY APPROVED, KHÔNG load-bearing defect. **CHƯA commit** (chờ user).
  Còn lại: (1) review tổng nhánh (broad whole-branch, model mạnh) — đang chạy; (2) **USER QA trên browser**:
  đăng nhập từng cấp quyền tạo Firm/WrService/HĐ mới, vượt/không vượt hạn mức (TP→BGD), duyệt/từ chối, in,
  xác nhận `account_details`/tồn KHÔNG đổi + regression type-9 (Nhập bán mượn trả lại); (3) hỏi user commit.
  Footprint chưa commit — hrm-api: `Modules/Finance/{Entities/BorrowSellRequest,Services/BorrowSellRequest,
  Http/Controllers/V1/BorrowSellRequestController,Http/Requests/BorrowSellRequest,Transformers/BorrowSellRequestResource,
  Tests/Unit/BorrowSellRequestCalculatorTest}` + `Routes/api.php` + hợp nhất type-9 (xoá
  `Entities/ProductImportRequest/BorrowSellRequest.php`, sửa `ProductImportRequestService.php`,
  `Entities/Concerns/ChecksEmployeePermission.php`); hrm-client: `pages/finance/borrow-sell-requests/*` +
  `components/subsystem-menu/finance.js`.
  **Phase 2** = `BorrowSell` (phiếu BÁN thực tế, `PXBHM-`) + hạch toán bán: **CODE DONE 14/14 task (SDD) + final whole-branch review XONG (SHIP-with-nits) đã adjudicate** (2026-09-07). Ledger `sdd/progress-phase2.md`, report `sdd/final-review-report.md`. BE đã commit 10 commit (c562527e0^..8b9e77bd6). Final review: 0 Blocker/0 High/1 Medium(F1)/3 Low. **F1 FIXED** (updateWarehouse nhánh WrService bổ sung cộng `exported_qty` cấp-2 lồng — map 3 FQN→bảng + increment atomic + unit test 4/4; Firm sub-claim = false-positive nhánh tabs/KM đã bỏ) — **CHƯA commit** (2 file: BorrowSellService.php + BorrowSellStoreTest.php). F2 park (FU-6 comment sai vị trí gate), F3/F4 đóng by-design. Delta additive objectable_id/type (uncommitted). FE uncommitted (quy ước Phase 1 FE): `pages/finance/borrow-sells/**` + nút "Lập phiếu bán" + menu link. QA V1-V8 PASS. Bước tiếp: **chờ user cho phép commit BE fix F1 + QA browser** (FE giữ uncommitted; Phase 1 BE staged không đụng).

- product-import-list → @namdangit → .plans/gop-db/product-import-list/plan.md
  Trạng thái: **CODE DONE Phase 1-4 — chờ user QA** (2026-08-28). Bổ sung cho màn **Phiếu nhập hàng**
  (`/finance/product-imports`, `Modules/Finance`): (1) **bộ quyền 4 cấp** hiện trong màn Phân quyền —
  id **1543-1546** guard `api` group "Phiếu nhập hàng" (tổng công ty / công ty / phòng ban / bộ phận),
  đã thêm id 1546 vào `PermissionsTableSeeder` + chèn thẳng 4 dòng vào DB gộp (trước đó 1543-1545 có trong
  seeder nhưng CHƯA có trong DB nên nhóm quyền không hiện); (2) **bộ lọc** viết lại mirror màn Phiếu xuất
  hàng — `V2BaseCompanyDepartmentFilter` (công ty/phòng ban/bộ phận/người lập) + loại + trạng thái + khoảng
  ngày lập + keyword; (3) **tuỳ chỉnh cột** (`ColumnCustomizationModal` table `finance_product_imports`) +
  cột **Người lập** (`creator_name`).
  BE: `ProductImport` thêm nhánh **bộ phận** vào `applyViewScope()`/`canView()` (`isPartManager`/`managePartIds`
  mirror `ProductImportRequest`); `searchByFilter()` nhận thêm company/department/part/employee/start_date/end_date
  + `->with('creator.info')`; route mới `GET finance/product-imports/filter-options`. `php -l` sạch.
  **Phase 5 (2026-08-28)**: BỎ role-18 bypass — trước đó `canView()` + `isBigBoss/isBoss/isManager/isPartManager`
  có vế `currentEmployeeIsSuperAdmin()` khiến role 18 (DNS admin) tự thấy hết, song song với 4 quyền → user
  chốt bỏ, để 4 quyền điều khiển hoàn toàn. Vẫn GIỮ trait `ChecksEmployeePermission` làm hàm đọc quyền (query
  theo TÊN quyền mọi guard — ĐÚNG cho gop_db, khớp với FE `hasAPermission`; KHÔNG đổi sang helper global
  `isCurrentEmployeeHasPermission` vì nó bị bug model_type='App\Employee' trên DB gộp).
  ⚠️ Hệ quả: **role 18 KHÔNG còn tự thấy hết** — phải gán "Xem phiếu nhập hàng theo tổng công ty" qua màn
  Phân quyền (nhóm "Phiếu nhập hàng" nay đã hiện). Còn giữ 2 nhánh nghiệp vụ hợp lệ ngoài 4 quyền: kế toán
  kho cùng công ty (chi tiết) + người tạo phiếu (`created_by`).
  Bước tiếp: user QA trên UI (lọc theo cấp tổ chức, tuỳ chỉnh cột, cột Người lập) + gán 4 quyền cho các role
  qua màn Phân quyền.

- de-nghi-nhap-kho → @namdangit → .plans/gop-db/de-nghi-nhap-kho/plan.md
  Trạng thái: **P1 (Backend) XONG · P2 (Frontend) XONG — chờ user QA** (2026-08-25). Port màn **Đề nghị nhập kho** (ERP
  `WarehouseImportRequest`, mã `PDNNK`) — tầng 2 luồng nhập kho 3 tầng (cha `ProductImportRequest`/PYCNH đã port).
  Scope A: chỉ chứng từ (Lập từ YCNH + list + chi tiết + Thủ kho duyệt + Từ chối + Hủy + In); KHÔNG đụng tồn/hạch toán (tầng 3 tách sau).
  Mirror sibling **Đề nghị xuất kho** (Module Assign) sang **Module Finance**. Bộ status WIR riêng (1..7),
  đổi status cha YCNH inline theo ERP: lập→7, gửi→1, thủ kho duyệt→4, từ chối→7, hủy→6 (giết YCNH — đúng ERP nhập).
  GÁC tầng 3: tabs cha-con, `warehouse_exported_qty` type 4/9, `WarehouseImportRequestDetailAccounting`, tồn/sổ.
  Spec: `docs/superpowers/specs/gop-db/2026-08-25-de-nghi-nhap-kho-design.md`.
  Bước tiếp: **user QA trên trình duyệt** (login Kế toán kho lập/sửa/hủy; thủ kho duyệt/từ chối) rồi đóng feature (tầng 3 tách sau). FE đã xong: 4 trang `pages/finance/warehouse-import-requests/` + rewire nút ở màn YCNH.

- nhap-ban-tra-lai-hd21 → @namdangit → .plans/gop-db/nhap-ban-tra-lai-hd21/plan.md
  Trạng thái: **Phase 1 CODE DONE · Phase 2 SPEC XONG — chờ user review spec** (2026-08-27). Phase 2 = màn **Phiếu nhập hàng
  (ProductImport)** HRM (chưa từng có bên HRM), khung generic mở rộng mọi loại nhập, đợt này xử lý type 4 loại 21.
  Spec Phase 2: `docs/superpowers/specs/gop-db/2026-08-27-product-import-hrm-design.md` (2 đường vào: A qua kho ERP redirect / B nhập thẳng).
  Phase 1 BE+FE xong: migration `emplement_contract_*`,
  `searchForImportType`/`dataForSaleReturn`/`guardBusinessRules`/`fillFromExportRequest` nhánh loại 21, modal +cột "Số HĐ".
  Verify bằng DB smoke test dữ liệu thật (phiếu 35676/HĐ13). CHỜ: chưa có phiếu xuất loại-21 status=5 để E2E store()→duyệt TP.
  Mở luồng **Nhập hàng bán trả lại** (import type 4 `BAN_TRA_LAI`) cho hàng bán theo **HĐ HRM loại 21** (`XUAT_BAN_HOP_DONG`),
  bắt chước nguyên quy tắc loại **xuất bán hãng 14 ERP**, chỉ đổi nguồn HĐ ERP (`firm_contract`) → HĐ HRM (`Contract` polymorphic).
  Đã xác nhận: HĐ 21 có đủ tương đương type 14 (`support_accounting` chung bảng `firm_support_accountings`,
  quyết toán qua `Contract.status` 11/12, dòng `product_export_request_tab_products` có `qty/exported_qty/returned_qty`);
  khác: HRM PER không có status 13 (loại 21 hoàn tất = status **5**), query quyết toán dùng khóa thường.
  **Phase 1** = nửa trước (lập+validate+duyệt giá), tận dụng code type-4 đã port. **Phase 2** = màn ProductImport (nhập kho thực+returned_qty+hạch toán) — SPEC XONG.
  **PENDING**: type 9 (bán mượn trả) loại 21 — chờ phiếu xuất bán hàng mượn loại 21.
  Bước tiếp: user review spec Phase 2 → writing-plans → code (Entities → Service → hạch toán → Controller/FE → nút entry → E2E).

- hop-dong-xuat-hang → @namdangit → .plans/gop-db/hop-dong-xuat-hang/plan.md
  Trạng thái: **HẠCH TOÁN XUẤT HÀNG (task 9.15) — BE DONE + TEST E2E PASS** (2026-08-20, nhánh `hop-dong` con của `gop_db`).
  Phiếu xuất hàng HĐ HRM loại **20** (xuất sản xuất) + **21** (xuất bán) khi Hoàn tất (status=1): trừ tồn kế toán+vật lý,
  tính giá vốn FIFO (ghi đè export_price), ghi sổ `account_details` bám sát ERP "bán hàng theo hãng".
  - Loại 21: đủ 8 cụm (doanh thu 1311/5111/33311, giảm trừ 5213/33311/1311, giá vốn **Nợ632/Có155** — dùng 155 thay 1561,
    thưởng 5211/35241, TNCN 35241/3335, hoa hồng tháng/quý 6411/35241, quỹ rủi ro 6411/35241).
  - Loại 20: chỉ giá vốn **Nợ1541/Có1561**; auto sinh phiếu nhập cha **Nợ155/Có1541** (khép vòng WIP→thành phẩm).
  - **Accuracy gate**: đối chiếu phiếu bán-hãng ERP thật (PXH id=4) → khớp TỪNG ĐỒNG. Cost engine khớp 6 ca thật (P2).
  - **E2E**: dựng data mới (kho+tồn+BOM), chạy trọn `ProductExportService::createFromWarehouseExport(status=1)` → cả 2 loại cân đối ΣNợ=ΣCó lệch 0.
  Files: `Modules/Assign/Services/{ProductExportPostingService,WarehouseExportAccountingService,ProductExportService,ContractParentImportService}.php`,
  `Modules/Finance/Entities/Account/{AccountDetail,AccountDetailRef}.php`.
  **HOÃN** (tách feature): DebtRemindersJob (cần model `ContractStateDelivery` HRM chưa có), hạch toán bốc xếp (arrange_delivery).
  Bước tiếp: FE màn tạo/hoàn tất phiếu xuất hàng (2 nút Lưu nháp status=3 / Hoàn tất status=1 → `POST /assign/warehouse-exports/{id}/product-exports`) — CHƯA có.

- base-popup-bao-cao → @namdangit → .plans/gop-db/base-popup-bao-cao/plan.md
  Trạng thái: **XONG PHASE 1 + PHASE 2, ĐÃ CHẠY E2E THẬT** (18/09/2026), chờ user quyết 1 file chưa commit.
  Tách vỏ dùng chung cho popup báo cáo: `components/report/V2BaseReportModal.vue` (481 dòng) +
  `utils/mixins/reportDrillListMixin.js` (146 dòng); thêm slot `header` + prop `noEnforceFocus` vào
  `components/modal/V2BaseModal.vue` (dùng chung 30 màn, mặc định giữ nguyên hành vi cũ).
  Chuyển 3 popup: CSKH tiềm năng (1307→871), phát triển thị trường (1204→1050), kết quả dự án TKT
  (888→916 — có bổ sung nút "Xoá lọc" + chip lọc nhanh vốn bị thiếu). 3 popup GIỮ NGUYÊN 3 chiến
  lược dữ liệu khác nhau: lọc server / lọc client / BE lo hết (popup TKT KHÔNG dùng mixin).
  17 commit trên `gop_db` của `hrm-client`, **chưa push**.
  ⚠️ **`hrm-api/database/e2e_provision.php` đã sửa nhưng CHƯA COMMIT**: nó trỏ 5 bảng `hrm_*` đã bị
  `ReconcileEmployeesSeeder` gộp và xoá, khiến `api-setup` đổ và **mọi spec UI của HRM không chạy được**.
  Sửa về tên thật (`employees`, `roles`, `company_employees`, `employee_has_roles`,
  `role_has_permissions`) là gỡ tắc cho cả team — cần user duyệt diff.
  ⚠️ Đã đụng DB local: gán quyền 1187 cho role 18 (báo cáo phát triển thị trường vốn gán cho 0 role
  → không ai xem được ở cấp trên "self"); lệnh gỡ nằm trong `.sdd/progress.md`.
  Test: `tkt-result-report` 22/22 xanh; `customer-market-development` 7 xanh + 2 đỏ sẵn;
  `potential-customer-care` 25+ xanh khi loại ca đỏ sẵn, 3 ca của đợt này đều xanh. 5 ca đỏ còn lại
  đều là ĐỎ SẴN (2 ca API, 1 ca màn tạo dự án TKT, 2 ca test bám giả định dữ liệu cũ) — có bằng chứng
  từng ca trong `.sdd/progress.md`.
  Nhật ký thực thi + toàn bộ quyết định (21 ruling) + 8 lỗi tìm thấy trong chính các bài test:
  `.plans/gop-db/base-popup-bao-cao/.sdd/progress.md`.
- **finance-addition-accounting-request — Sửa lỗi + chuẩn hoá màn (Phase 12-20)** → @khoipv →
  `.plans/gop-db/finance-addition-accounting-request/plan.md`
  **Đợt 2026-09-30 (Phase 31) — CODE XONG, CHỜ USER MỞ TRÌNH DUYỆT. Chưa commit.** Loại Khác: popup
  **Chọn nhân viên** có sort Mã/Tên + gộp 2 ô tìm thành 1 ô "Mã / Tên nhân viên"; popup **Chọn nhà cung cấp**
  có sort Mã/Tên — ⚠️ popup này DÙNG CHUNG, user chốt bật cho mọi màn (Đề nghị thu/chi tiền, Báo có, Điều chỉnh
  công nợ…). BE 2 file (whitelist sort) · FE 3 file. Đã kiểm hàm tìm kiếm với dữ liệu thật + compile FE.
  **Phase 32**: ô Loại yêu cầu có nút × xoá nhanh (bỏ `:allowClear="false"`, xoá đi qua `onChangeType`).
  **Phase 33**: URL phiếu không tồn tại (vd `/31658`) báo lỗi 2 lần — trang Chi tiết + form con cùng nạp phiếu;
  nay trang Chi tiết chỉ dựng form sau khi nạp thành công, 404 → "Không tìm thấy dữ liệu" + về danh sách
  (cả màn Sửa). FE 2 file, chỉ compile — chưa mở trình duyệt.
  **Phase 34**: 3 popup tra cứu (Phiếu xác nhận bảo hành / Phiếu xử lý hàng thiếu / Nhân viên — `RecordSearchModal`)
  + popup **Chọn nhà cung cấp** (⚠️ DÙNG CHUNG các màn Tài chính) chuyển sang `V2BaseDataTable` — phân trang theo base
  như popup "Hàng đang giữ" (20/50/100 dòng). FE 3 file, chỉ compile — chưa mở trình duyệt.

  **Đợt 2026-09-21 (Phase 14-20) — CODE XONG, CHỜ USER NGHIỆM THU. Chưa commit, chưa push (cả 2 repo).**

  | Phase | Nội dung | Phạm vi |
  | --- | --- | --- |
  | 14 | **Nền header xám trên cổng dev, local nhìn đúng.** Class `section-header` chỉ nằm trong `<style>` **non-scoped** của `V2BaseFormSection.vue`/`CustomerForm.vue` → bản `nuxt dev` nạp sẵn nên "ăn ké", build production tách chunk theo route thì rule biến mất. **Local KHÔNG tái hiện được**, đừng dùng local nghiệm thu nhóm lỗi này | FE 3 file |
  | 15 | Màn **Chi tiết** bỏ badge trạng thái ở header card (cả 2 nhánh: loại 7 và form readonly); giãn dòng `mb-3` → `mb-2` (15 chỗ) | FE 2 file |
  | 16 | Ô **Diễn giải** lên cùng hàng với **Tỷ giá** (chuyển sang `form-row` thứ nhất — Bootstrap tự lấp chỗ trống, không cần `v-if` riêng cho loại 1) | FE 1 file |
  | 17 | **Vá ERP**: `getInformationDiscrepancy()` nổ 500 khi chọn Phiếu xử lý hàng thiếu — `groupBy` trên truy vấn `SUM` làm `first()` trả null rồi `->toArray()` fatal. Bỏ `groupBy` + chặn null. Đối chiếu dữ liệu thật: có dòng khớp thì SUM **y hệt bản cũ** | **repo `erp`** 1 file |
  | 18 | **Lưu nháp chỉ bắt buộc Loại yêu cầu.** BE đã rẽ `required` theo `status` từ trước nhưng **sót `gt:0`**, mà form khởi tạo `money: 0` → nháp luôn 422. Nháp dùng `min:0` | BE 1 · FE 1 |
  | 19 | Lỗi hiện qua **`V2BaseError`** thay `<div class="invalid-feedback">` thô (14 khối); bỏ `focusFirstError()` tự viết → util chung `utils/scrollToFirstError.js` (`V2BaseError` render `.v2-error`, giữ hàm cũ là mất luôn tính năng cuộn) | FE 3 file |
  | 20 | Câu lỗi `required` thống nhất **"Bắt buộc phải nhập"** đúng như BE trả về; ô vừa bắt buộc vừa phải > 0 tách 2 câu theo trạng thái ô | FE 3 file |

  Không migration, không quyền mới. Bản ghi test sinh ra khi nghiệm thu lưu nháp: **`PYCHTBS-002065`** (phiếu nháp, user xoá được ở màn danh sách).

  **⚠️ 6 việc chờ user quyết:**
  1. Bỏ badge trạng thái ở **màn Sửa** nữa không (Phase 15 chỉ bỏ ở màn Chi tiết)
  2. Vá 2 màn **Bán hàng mượn** (`borrow-sell-requests`, `borrow-sells`) dính đúng lỗi nền header xám của Phase 14
  3. Hằng **`insurance_plan_id = 1`** nghi lọc sai → loại 5 luôn ra Số tiền 0 ở cả ERP lẫn HRM (xem `design.md` mục Rủi ro)
  4. Bên ERP: chặn null cho truy vấn đầu của `getInformationDiscrepancy()` + `supplier[0]` trong blade (cùng loại lỗi, chưa sửa vì đổi hợp đồng trả về)
  5. Việt hoá message rule `gt` — sửa `resources/lang/vi/validation.php` là đụng **lang dùng chung toàn hệ thống**, hay khai `messages()` cục bộ trong FormRequest?
  6. Có chuyển màn sang **vee-validate realtime** (bỏ cờ `touched`) theo skill `form-validate` không — đụng ~20 ô ở 3 file

  **Đợt trước (Phase 12-13, 2026-09-10) — vẫn chờ user nghiệm thu trình duyệt:**
  Trạng thái: **CODE XONG — CHỜ USER MỞ TRÌNH DUYỆT NGHIỆM THU** (2026-09-10). Yêu cầu user: (1) ô trống thì để trống, bỏ dấu `—`;
  (2) cột *Ngày gửi* / *Ngày duyệt* hiện thêm giờ (2 cột DB vốn là `datetime`, resource cắt mất giờ);
  (3) cột *Số tiền* in kèm đơn vị tiền như màn Phiếu đề nghị thanh toán; (4) **bỏ ô *Bộ phận*** khỏi
  bộ lọc tổ chức, chỉ còn Công ty – Phòng ban.
  **Phase 13 (2026-09-10)**: popup chọn hợp đồng ở màn Tạo thiếu nguồn `firm_contracts` → KH gốc ERP
  gần như không chọn nổi hợp đồng (firm 19.936 HĐ/4.102 KH so với `hrm_contracts` 34 HĐ/29 KH), lại
  còn hiện nhầm phiếu bảo hành và hợp đồng của người khác. Thêm nhánh `usage=addition_accounting_request`
  vào `BillIncomeRequestService::searchSellContracts()` port đúng nhánh ERP
  `addition_accounting_request_sell_contract`. Đối chiếu tay đôi với service ERP: 3/4 cặp KH-NV trùng
  khớp tuyệt đối, cặp còn lại lệch có chủ đích (hợp đồng HRM tự sinh).
  Phạm vi: 2 file (BE `AdditionAccountingRequestListResource` · FE `pages/finance/addition-accounting-requests/index.vue`),
  không migration, không quyền mới. File Excel danh sách hiện giờ luôn (user đồng ý), ô Số tiền trong
  Excel vẫn là số thuần vì đã có cột *Loại tiền* riêng.

## Hoàn thành

- finance-bill-adjust-dept-request (fix 03/10, Phase 47) → @khoipv → .plans/gop-db/finance-bill-adjust-dept-request/plan.md
  Hoàn thành: 2026-10-05 — đã fix lỗi popup chọn hợp đồng hiện HĐ của khách bên kia (popup mở trước khi prop objectId kịp cập nhật).

- bao-cao-tong-hop-cskh-tiem-nang → @namdangit → .plans/gop-db/bao-cao-tong-hop-cskh-tiem-nang/plan.md
  Hoàn thành: 2026-10-04 — **ĐÃ MERGE + PUSH gop_db + DEPLOY VPS (user xác nhận)**. hrm-api `85a1c59d7` · hrm-client `a6ad678d0`; nhánh feature `gop_db-bao-cao-tong-hop-cskh-tiem-nang` đã push.
  Màn `/assign/report/potential-customer-tracking` (CSKH trước bán › Báo cáo thị trường): nhu cầu Đang theo dõi + dự án TKT tiến trình 2→9 theo Phòng ▸ Sales ▸ KH, tại thời điểm xem. Quyền 1676–1678 (type 29) + nới `Meeting::canView` cho quyền báo cáo; 4 nhóm quyền báo cáo thị trường chuyển type 4 → 29.
  PHPUnit 21 ca (+45 dịch vụ xanh) · e2e 13/13. Spec: docs/superpowers/specs/gop-db/2026-10-04-bao-cao-tong-hop-cskh-tiem-nang-design.md

- finance-declare-debt-beginning → @junfoke → .plans/gop-db/finance-declare-debt-beginning/plan.md
  Chuyển Hoàn thành: 2026-10-03 — đã push `develop` cả 2 repo. Còn: chạy SQL quyền 1615-1622 trên server · bấm thử Import + tải Excel.
  Trạng thái: 🟢 **CODE XONG BE + FE, đã kiểm API + Playwright (01/10/2026)**, nhánh `develop`. **Đã commit vào `develop`** (soát git 03/10). Port 2 màn Khai báo đầu kỳ công nợ KH + NCC.
  Còn lại: chạy SQL quyền 1615-1622 trên server · bấm thử Import + tải Excel trên giao diện.
  Spec: docs/superpowers/specs/gop-db/2026-10-01-finance-declare-debt-beginning-design.md | Tóm tắt: .plans/gop-db/finance-declare-debt-beginning/design.md

- catalog-usage-check → @junfoke → .plans/gop-db/catalog-usage-check/plan.md
  Chuyển Hoàn thành: 2026-10-03 — đã merge + push `develop` cả 2 repo. Còn: QA test theo file Excel.
  Trạng thái: 🟢 **CODE XONG BE + FE, đã kiểm tinker + API + Playwright (03/10/2026)**, nhánh `feat/catalog-usage-check` → **ĐÃ MERGE vào `develop` (03/10/2026), chưa push.** Commit `hrm-api` e84617c28 (merge 06f166850) · `hrm-client` 0c39eb2e9 (merge c6ae8dc30).
  Check Xóa/Khóa cho 20 danh mục chuyển ERP→HRM theo khảo sát màn đang dùng (Excel ở thư mục gốc). Xóa: chặn khi đã dùng; Khóa: chỉ chặn khi còn danh mục con Hoạt động.
  Spec: docs/superpowers/specs/gop-db/2026-10-03-catalog-usage-check-design.md | Tóm tắt: .plans/gop-db/catalog-usage-check/design.md

- lookup-stock-companies → @junfoke → .plans/gop-db/lookup-stock-companies/plan.md
  Chuyển Hoàn thành: 2026-10-03 — đã push `develop` cả 2 repo. Còn: đối chiếu popup trên dev · chốt quyền xuất Excel.
  Trạng thái: 🟢 **CODE XONG BE + FE, đã đối chiếu ERP + Playwright (02/10/2026)**, nhánh `develop`. **Đã commit vào `develop`** (soát git 03/10).
  Port màn ERP "Báo cáo hàng có thể bán theo công ty" → `/lookup/stock-companies` (phân hệ Thông báo) + popup Hàng đang về.
  Còn lại: đối chiếu popup trên dev (local `order_stock_progress` = 0 dòng) · chốt quyền xuất Excel (ERP id 507 không có trên DB gộp).
  Spec: docs/superpowers/specs/gop-db/2026-10-02-lookup-stock-companies-design.md | Tóm tắt: .plans/gop-db/lookup-stock-companies/design.md

- buy-service-request → @junfoke → .plans/gop-db/buy-service-request/plan.md
  Chuyển Hoàn thành: 2026-10-03 — code đã vào `develop` + `gop_db` (verify trọn luồng + đối chiếu ERP 292/298 từ 23/09); dòng "bắt đầu code" bên dưới là cũ. Còn: nghiệm thu cột NCC trên cổng dev.
  Trạng thái: 📄 **Xong Phase 0 (design + plan + spec), đã tạo nhánh, bắt đầu code** (22/09/2026).
  Scope: port màn **Yêu cầu mua dịch vụ** (ERP `buy_service_requests`) — đầu chuỗi 4 màn Mua dịch vụ.
  BE `Modules/Finance`, FE `/finance/buy-service-requests`, menu phân hệ **Bán hàng** (`sale-hub.js:153`).
  3 màn sau (HĐ mua dịch vụ · YC hạch toán · Hạch toán) **giữ ở ERP**; nút "Lập hợp đồng" trỏ `ERP_URL`.
  ⚠️ GOTCHA: `syncDetails()` xóa-rồi-insert dòng chi tiết → phải GIỮ `contracted_qty` (cột do ERP ghi),
  không thì phiếu đã lập hợp đồng bị reset tiến độ. Trạng thái 6/7 cũng chỉ đọc.
  Có làm **Lịch sử thay đổi** đủ 2 nơi → thêm bảng MỚI `buy_service_request_history` (không đụng bảng ERP).
  ⚠️ Dump `gop_db` ở local THIẾU `customers` (user xác nhận) → cột NCC trống ở local là bình thường,
  phải nghiệm thu trên cổng dev. Phase 1 xong: migration history + 5 quyền (1586-1590) + 3 entity.
  Phase 1-3 XONG: 5 quyền (1586-1590) · bảng history · 3 entity · 14 route · service đọc+ghi ·
  history + notify. Test end-to-end 2 kịch bản đã chạy, DB dọn sạch về 81 phiếu / 98 dòng.
  Phase 1-4 XONG (BE đủ: đọc · ghi · 2 nấc duyệt · lịch sử · thông báo · in 417/416 · xuất Excel).
  Đã rà tài liệu pull 22/09: bỏ `messages()` khỏi FormRequest (dùng lang file), xuất Excel theo
  4 mắt xích `ExportColumnRegistry` + `DynamicExport`; plan Phase 5/6 cập nhật theo skill mới.
  Phase 1-5 XONG. Màn danh sách đã verify trên trình duyệt (lọc, badge, xuất Excel, menu Bán hàng).
  ⚠️ Ô lọc đo ra 32px trong khi skill list-page ghi 36px — màn khuôn `product-natures` cũng 32px
  trên cùng bản `gop_db`, chờ user quyết có sửa component dùng chung không.
  Phase 6 + 6b XONG, đã verify TRỌN LUỒNG trên trình duyệt (lưu, 2 nấc duyệt, in, lịch sử 2 nơi,
  xóa) — console 0 lỗi, dọn sạch dữ liệu test. 5 lỗi thật tự phát hiện đã sửa (chi tiết ở plan.md).
  ⚠️ Lịch sử dùng bảng CHUNG `catalog_histories` + trait `LogsCatalogHistory` ⇒ KHÔNG còn migration.
  Phase 8 XONG: đối chiếu HRM vs ERP trên 149 nhân viên x 2 preset → 292/298 khớp; 6 chỗ lệch đều
  do cơ chế dùng chung (5 Super admin - chủ ý; 1 do trait cộng phòng của chính mình - chờ quyết).
  Tìm ra + sửa 1 lỗi: preset 'chờ tôi duyệt' không lọc phòng ban cho TP. Checklist grep sạch 8/8.
  2/3 điểm treo đã chốt (23/09): ô lọc 32px là TÀI LIỆU sai → đã sửa 3 file skill theo code;
  trait cộng phòng của chính mình → GIỮ NGUYÊN (quy ước chung phân hệ Tài chính), đã ghi docblock+spec.
  Còn lại: cột NCC trống ở local do dump thiếu `customers` → nghiệm thu trên cổng dev rồi merge gop_db.
  Spec: docs/superpowers/specs/gop-db/2026-09-22-buy-service-request-design.md | Tóm tắt: .plans/gop-db/buy-service-request/design.md

- finance-product-import-request → @junfoke → .plans/gop-db/finance-product-import-request/plan.md
  Chuyển Hoàn thành: 2026-10-03 — xong Phase 1-16 (lần cuối 22/09). Còn: user review trên dev + đóng 16 issue Redmine; mục [ ] lẻ xem plan.md.
  Trạng thái: **XONG PHASE 1-15** (2026-08-21) — gồm 16 bug tester redmine 11074-11089, các đợt phản hồi bổ sung,
  Phase 15 bỏ tab preset + 2 nút mở sang ERP (màn Kho chưa port).
  Port màn "Phiếu Yêu cầu nhập hàng" sang Tài chính; 8 loại phiếu + 4 luồng duyệt, 0 migration.
  Còn nợ: `V2Footer` dùng chung vẫn để nút In xanh + chữ "Không duyệt" (lệch chuẩn, ảnh hưởng mọi màn).
  Bước tiếp: user review trên dev rồi đóng 16 issue Redmine.
  Chi tiết + gotcha: plan.md

- finance-accounting-prepick-cancel → @junfoke → .plans/gop-db/finance-accounting-prepick-cancel/plan.md
  Chuyển Hoàn thành: 2026-10-02 (dọn mục Đang làm) — code đã vào nhánh chung; mục [ ] lẻ còn lại xem plan.md.
  Trạng thái: 🟢 **Code xong + verify (29/09), CHƯA commit.** Worktree `.worktrees/accounting-prepick-cancel`
  (cả 2 repo, nhánh `feat/finance-accounting-prepick-cancel`). Còn: user commit, đối chiếu 2 cổng trên dev.
  Port màn ERP `accounting_prepick_cancels` (Kế toán → Giữ hàng) — màn cuối nhóm Giữ hàng. GHI TỒN THẬT.
  ⚠️ GOTCHA: `prepick_logs` ghi `AccountingPrepickCancelDetailCustomer` + **id dòng KH** (không phải id phiếu);
  lô tra theo công ty NV chủ lô, `company_id` phiếu = công ty người lập.
  Spec: `docs/superpowers/specs/gop-db/2026-09-28-finance-accounting-prepick-cancel-design.md` | Tóm tắt: `design.md`

- dong-bo-luu-va-tiep-tuc → @junfoke → .plans/gop-db/dong-bo-luu-va-tiep-tuc/plan.md
  Chuyển Hoàn thành: 2026-10-02 (dọn mục Đang làm) — code đã vào nhánh chung; mục [ ] lẻ còn lại xem plan.md.
  Trạng thái: **CODE XONG (FE), đang verify tay** (2026-09-05). Redmine #11177.
  Mục tiêu: mọi màn Tạo mới đều có nút "Lưu và tiếp tục" — lưu xong ở lại màn, form về trắng.
  Phạm vi: 3 popup danh mục (vụ việc, mã phí, nguồn vốn) + 26 trang Tạo mới của Tài chính & CSKH.
  Hạ tầng mới: `utils/mixins/saveAndContinueMixin.js` (form) + `saveAndContinuePageMixin.js` (trang vỏ, remount bằng `:key`).
  Không áp dụng: màn không có Tạo mới (Cập nhật nhanh giá dịch vụ, Danh sách hàng giữ, Danh mục serial) và màn Tạo bắt buộc đi từ yêu cầu nguồn trên URL (Phiếu xuất hàng, Nhập/Xuất kho, Phiếu giữ hàng kho).
  Spec: docs/superpowers/specs/gop-db/2026-09-05-dong-bo-luu-va-tiep-tuc-design.md | Tóm tắt: .plans/gop-db/dong-bo-luu-va-tiep-tuc/design.md

- product-classification-catalogs (Redmine #11421) → @junfoke → .plans/gop-db/quan-ly-hang-hoa/product-classification-catalogs/plan.md
  Chuyển Hoàn thành: 2026-10-02 (dọn mục Đang làm) — code đã vào nhánh chung; mục [ ] lẻ còn lại xem plan.md.
  Trạng thái: 🟢 **XONG CẢ 5 PHASE (29/29 task), đã verify trên trình duyệt** (18/09/2026).
  **Chưa commit, chưa push.**
  ⚠️ 1 điểm lệch checklist chờ user quyết: `V2BaseImportToolbar` (component DÙNG CHUNG) chỉ cho
  Import khi hết dòng lỗi, khác rule "vẫn import được, chỉ lấy dòng hợp lệ".
  Import/Xuất Excel: 18 route mới, payload import dùng khoá chung `rows`.
  BE: 7 bảng + 12 quyền (id 1574-1585, group 'Danh mục hàng hóa', type 9) + 36 route + 11/11 test xanh.
  FE: menu nhóm "Hàng hóa" + 6 màn `pages/master-data/*` (index + modal) theo khuôn customer-scopes.
  6 danh mục mới phân hệ Danh mục chung: Tính chất hàng hóa · Nhóm chức năng · Nhóm sản phẩm ·
  Loại sản phẩm · Chính sách kinh doanh · Đặc tính sản phẩm. 7 bảng mới, **không đụng cây cũ**
  `scopes/chapters/job_groups/job_clusters/groups`. Danh mục để trống, dùng chung toàn hệ thống,
  giao diện danh sách + modal theo khuôn `pages/assign/customer-scopes/`.
  ⚠️ `product_families` (mới, Nhóm sản phẩm) KHÁC `groups` (nhóm hàng hóa cũ của ERP, 886 dòng).
  Nhánh: `feat/11421-danh-muc-quy-hoach-hang-hoa` từ `gop_db` ở cả 2 repo.
  Spec: docs/superpowers/specs/gop-db/2026-09-18-product-classification-catalogs-design.md

- **catalog-import-export — Import + Export cho các màn Danh mục đã chuyển ERP → HRM** → @junfoke →
  Chuyển Hoàn thành: 2026-10-02 (dọn mục Đang làm) — code đã vào nhánh chung; mục [ ] lẻ còn lại xem plan.md.
  `.plans/gop-db/catalog-import-export/design.md` · `plan.md` ·
  spec `docs/superpowers/specs/gop-db/2026-09-10-catalog-import-export-design.md`
  Trạng thái: **XONG TOÀN BỘ 20/20 TASK, CHỜ NGHIỆM THU** (2026-09-11). Nhánh
  `feat/catalog-import-export` (tách từ `gop_db`), **chưa commit**.
  Kết quả: **13 màn có Import**, **9 màn có thêm Export**. Mỗi màn đã chạy thật: validate ra đúng
  số dòng hợp lệ/lỗi với đúng thông báo, import ghi đúng DB + Lịch sử thay đổi, không đẻ danh mục
  cha, export khớp `total` của danh sách; dữ liệu thử đều đã xoá.
  Không dựng framework mới: mixin `FinanceImportMixin` đổi tên thành `CatalogImportMixin` dùng chung,
  file mẫu **sinh động tại FE** từ chính `importColumns` qua hàm mới `buildImportTemplate()`.
  Có 19 unit test PHPUnit (`CurrencyImportValidationTest` 10, `ProvinceImportValidationTest` 9).
  ⚠️ **GOTCHA phải biết khi sửa tiếp** (chi tiết trong `plan.md`):
  · 3 lớp `ApiController` khác nhau — **9/13 controller KHÔNG có `responseBadRequest()`**;
  · `nations` không có cột `code`, mã nằm ở `country_code`;
  · khoá chống trùng thật: Tiền tệ/Quốc gia/Ngân hàng/Ghi chú BD trùng **2 khoá**, Tỉnh/TP theo
    (quốc gia+khu vực), Phường/xã theo (tỉnh+tên), Costs theo nhóm `type IS NULL`;
  · cột trạng thái trên bảng đặt key riêng (`workStatus`, `nationStatus`…) nên phải khai
    `exportFieldKeyMap`, không thì popup rớt cột Trạng thái.
  🐞 **Đã sửa 3 lỗi CÓ SẴN gặp dọc đường** (ngoài phạm vi feature, user duyệt sửa):
  · `NationService` sort `nations.code` → cột thật `country_code`, bấm sắp xếp cột Mã quốc gia trả
    500 (nay 200);
  · màn Phường/xã **chưa bao giờ ghi được Lịch sử thay đổi** — `wards.id` không AUTO_INCREMENT
    nhưng model khai `incrementing = true` nên `getKey()` = 0 làm `logCatalogCreate()` thoát sớm;
  · N+1 `Ward::canDelete()` (1 query/dòng) khiến API danh sách Phường/xã mất 23s/5.000 dòng →
    gom 1 query còn **3s**; đã đối chiếu 200 bản ghi, 0 sai lệch kết quả `can_delete`.

- **finance-product-transfer — Phiếu điều chuyển hàng (ERP `product_transfers` → HRM)** → @junfoke →
  Chuyển Hoàn thành: 2026-10-02 (dọn mục Đang làm) — code đã vào nhánh chung; mục [ ] lẻ còn lại xem plan.md.
  `.plans/gop-db/finance-product-transfer/khao-sat.md` · `design.md` · `plan.md`
  Trạng thái: **MỚI KHẢO SÁT XONG — chưa có dòng code nghiệp vụ nào** (2026-09-04).
  Nhánh riêng `feat/finance-product-transfer` (hrm-api + hrm-client, tách từ `gop_db`).
  Màn ERP `Warehouse\ProductTransfersController`, mã `PDCH-`, bảng đã có sẵn 309 phiếu trên DB gộp
  (không cần migration bảng chính). Chuyển hàng giữa 2 **kho kế toán** trong cùng 1 kho vật lý;
  2 trạng thái, "Duyệt" = hạch toán ngay (ghi `accounting_stocks` + `accounting_stock_logs` + bút toán
  Nợ 156/Có 156), hạch toán rồi khoá vĩnh viễn.
  ⚠️ GOTCHA: mục menu "Phiếu điều chuyển hàng" TRƯỚC ĐÂY bị gán nhầm link sang màn **Phiếu yêu cầu
  chuyển hàng** (`product-transfer-requests`) — 2 màn KHÁC nhau, ERP để ở 2 nhóm menu khác nhau.
  Đã trả về đúng chỗ 2026-09-04 (Task 0.2). Đừng gán link màn khác vào mục đó nữa.
  ⚠️ GOTCHA: **KHÔNG** mở rộng `AccountingStockService` cho màn này — `in_acc_warehouse` chỉ là SUM
  thô của kho kế toán đang chọn, không trừ pending; màn tự query. (Bản khảo sát đầu ghi sai.)
  Chốt với user: sửa 13 lỗi ERP theo chuẩn HRM · tách 2 method FIFO khỏi
  `WarehouseExportAccountingService` (chỉ 1 caller) · CÓ làm lịch sử thao tác (ERP không có) ·
  KHÔNG làm huỷ phiếu/đảo bút toán.
  Bước tiếp theo: viết spec → Phase 1 tách FIFO + test hồi quy màn Phiếu xuất hàng.

- finance-prepick-expiring → @junfoke → .plans/gop-db/finance-prepick-expiring/plan.md
  Chuyển Hoàn thành: 2026-10-02 (dọn mục Đang làm) — code đã vào nhánh chung; mục [ ] lẻ còn lại xem plan.md.
  Trạng thái: **XONG — ĐÃ MERGE VÀO `gop_db`** (2026-09-04), cả 2 repo ahead origin/gop_db 2 commit,
  **chưa push** (user tự đẩy lên dev).
  Nhánh `feat/finance-prepick-expiring` (cả 2 repo, tách từ `gop_db`), worktree
  `.worktrees/finance-prepick-expiring` — tái sử dụng worktree cũ của finance-product-import-request.
  Port màn "Hàng sắp hết hạn giữ" bản KẾ TOÁN (`warehouseInfo.accountingExpiringPrepick`) sang
  Tài chính / nhóm Giữ hàng. Dùng lại ~90% `PrepickStockReportService` — chỉ thêm cờ `expiring_only`.
  ⚠️ User chốt **GIỮ NGUYÊN điều kiện ngày ngược nghĩa của ERP** (lô đã quá hạn trong `warning_day`
  ngày qua, KHÔNG phải sắp tới hạn) → cột Trạng thái không bao giờ ra "Trong hạn". Đừng sửa nhầm.
  Không migration (dùng lại quyền 100427 + 100839/840/841). Đã nghiệm thu: bấm thật trên trình duyệt,
  5 nhánh phân quyền qua HTTP, và đối chiếu bộ cột/bộ lọc + ngữ nghĩa cửa sổ ngày trên ERP dev.
  ⚠️ Merge có 2 xung đột đều do nhánh export-request vào trước, đã gộp cả 2 phía:
  `PrepickExtendRequestService` (thêm cả `PrepickApprovalRouteService` lẫn `PrepickConfigService`)
  và `subsystem-menu/finance.js` (giữ cả link màn mới lẫn 2 link Yêu cầu/Phiếu xuất giữ).
  ⚠️ `vendor` của worktree `.worktrees/gop-db` là SYMLINK sang checkout chính -> chạy PHP ở đó là
  nạp code nhánh khác, số liệu sai. Test code sau merge phải làm ở worktree có vendor riêng.

- finance-prepick-export-request → @junfoke → .plans/gop-db/finance-prepick-export-request/plan.md
  Chuyển Hoàn thành: 2026-10-02 (dọn mục Đang làm) — code đã vào nhánh chung; mục [ ] lẻ còn lại xem plan.md.
  Trạng thái: **XONG BE + FE, ĐÃ VERIFY PLAYWRIGHT LUỒNG ĐẦY ĐỦ** (lập YCXG → duyệt 3 cấp → lập
  PXG → duyệt → sinh lô giữ hàng đúng). Nhánh `feat/finance-prepick-export-request` (cả 2 repo,
  tách từ `gop_db`) — **chưa commit**.
  Port CẶP màn "Yêu cầu xuất giữ" + "Phiếu xuất giữ" sang Tài chính / nhóm Giữ hàng, đủ 6 loại.
  ⚠️ Hai màn phải đi CÙNG ĐỢT: PXG duyệt là nơi DUY NHẤT sinh lô `prepick_details` mà 4 màn giữ
  hàng đã port đang tiêu thụ.
  ⚠️ Có đụng 2 thứ dùng chung: `AccountingStockService` (thêm `in_promotion`) và tách
  `PrepickApprovalRouteService` — đã test lại Gia hạn + Điều chuyển, lệch 0/300 phiếu.
  ⛔ Chưa nghiệm thu được loại 1-4: local 0 phiếu (4 bản dump ERP đều vậy, nghi nhánh code chết).
  **Vòng QA 04-05/09/2026 (#11302 · #11304 · #11308 · #11311 · #11312 · #11313)**: đã sửa 11 điểm —
  link YCXG mở tab mới; lịch chặn ngày quá khứ/quá trần; mẫu in đổi width px sang %; khối Lịch sử
  có Thu gọn/Xem lịch sử (cả 2 màn); gộp 2 tầng header "Số lượng"; bổ sung Mã KH/SĐT/Địa chỉ/ĐC
  giao hàng/Phòng ban ở màn Thêm; cột "Có thể giữ" mất số (buildQueryString sinh `product_ids=`
  không có `[]`); chặn SL đề nghị vượt tồn ngay lúc gửi duyệt; xoá lỗi cũ khi đổi hợp đồng; chặn
  tệp > 13 MB ngay ở FE. **Chưa chạy thử trên trình duyệt** (code chưa deploy lên dev).
  **Vòng QA 05/09 đợt 2 (#11314 · #11315)** — ô ĐVT: (a) select dùng `v-model` trên BẢN SAO dòng của
  `visibleRows` nên ĐVT chọn xong không vào `form.products`, payload vẫn gửi đơn vị cũ; (b) BE trả
  "Có thể giữ" theo ĐƠN VỊ GỐC, thiếu phép chia hệ số của ERP `updateInStock()`; (c) FE tự điền
  ĐVT đầu danh sách nên "không chọn" vẫn lưu được. Đã sửa cả 3, thêm nhãn ĐVT kèm hệ số, nạp lại
  danh sách ĐVT ở màn Sửa, và trừ tồn khuyến mại cho khớp bước Duyệt giữ hàng.
  **Vòng QA 07/09 (#11321 · #11322)** — #11321 (2 thùng duyệt ra 2 lọ) đã hết nhờ bản 05/09, kiểm
  trực tiếp trên dev. #11322 (bấm Sửa mất ĐVT) là lỗi MỚI do bản 05/09 lộ ra: select2 tự bắn
  `change` rỗng lúc options chưa nạp xong -> handler xoá sạch ĐVT/đơn giá của phiếu dù màn vẫn
  hiện "Lọ". Đã chặn ở `onUnitChange` (bỏ qua khi chưa có options + bỏ qua cú change lặp).
  **Vòng QA 09/09 (#11365 · #11368 · #11370)** — #11368: cấp duyệt của dòng từ chối nay đọc từ
  bảng lịch sử (trạng thái ngay trước hành động) thay vì gán vào dòng cuối có dấu duyệt.
  #11365: URL id sai -> toast tiếng Việt + đưa về danh sách (câu "Item Not Found!" nằm ở
  `Handler` dùng chung, chưa đụng). #11370: ẩn ô khoá rỗng (Hợp đồng/Địa chỉ), bỏ toast trùng với
  dòng trống của bảng; nút "Không duyệt" của ERP là bản sao nút Lưu (cùng `submit(3)`) nên KHÔNG
  port — chờ user trả lời QA.
  Bước tiếp: chạy migration `2026_09_03_000001_...` trên dev · gỡ 3 quyền tạm của emp 781 ·
  commit (chi tiết ở cuối Phase 13 của plan.md).
  Chi tiết + gotcha: plan.md | Tóm tắt: .plans/gop-db/finance-prepick-export-request/design.md
  Spec: docs/superpowers/specs/gop-db/2026-09-03-finance-prepick-export-request-design.md

- finance-prepick-stock-list → @junfoke → .plans/gop-db/finance-prepick-stock-list/plan.md
  Chuyển Hoàn thành: 2026-10-02 (dọn mục Đang làm) — code đã vào nhánh chung; mục [ ] lẻ còn lại xem plan.md.
  Trạng thái: **XONG PHASE 0-8** (2026-08-21) — Phase 8 là đợt vá QA redmine 11116. Nhánh `feat/finance-prepick-stock-list`.
  Port màn **Danh sách hàng giữ** sang Tài chính / nhóm Giữ hàng — báo cáo CHỈ ĐỌC, bảng 3 tầng
  Hàng hoá → Nhân viên → Khách hàng, không migration.
  Bước tiếp: user đối chiếu 2 cổng trên dev + test quyền `Xem phiếu hàng giữ theo phòng ban`.
  Chi tiết + gotcha: plan.md

- finance-prepick-cancel → @junfoke → .plans/gop-db/finance-prepick-cancel-request/plan.md
  Chuyển Hoàn thành: 2026-10-02 (dọn mục Đang làm) — code đã vào nhánh chung; mục [ ] lẻ còn lại xem plan.md.
  Trạng thái: **XONG PHASE 0-13** (2026-09-04) — Phase 10 vá QA redmine 11094/11149/11150/11151/11152/11154,
  Phase 11 bỏ tab preset (1 màn = `all` của ERP, nút duyệt theo quyền), Phase 12 rà màn Phiếu hủy
  theo quy tắc chung (bỏ tự kéo số về trần, duyệt xong về danh sách, nút In trắng, 4 icon ⓘ),
  Phase 13 vá QA redmine 11295/11296.
  Nhánh `feat/finance-prepick-cancel`. Port 2 màn `Yêu cầu hủy hàng giữ` + `Phiếu hủy hàng giữ` sang
  Tài chính / nhóm Giữ hàng — **màn đầu tiên của HRM ghi tồn kho thật** (duyệt = trừ FIFO
  `prepick_details` + ghi `prepick_logs`). 2 migration (2 bảng lịch sử).
  **Tài liệu bàn giao ĐỦ CẢ 2 MÀN** — mỗi màn 1 bộ 3 file: màn Yêu cầu hủy hàng giữ (05/09)
  `SRS - Yeu cau huy hang giu.docx` + `HDSD_Yeu cau huy hang giu.docx` + `testcase.xlsx`;
  màn Phiếu hủy hàng giữ (09/09) `SRS - Phieu huy hang giu.docx` (33 trang) +
  `HDSD_Phieu huy hang giu.docx` (26 trang) + `testcase - Phieu huy hang giu.xlsx` (111 TC).
  ⚠️ GOTCHA màn Phiếu hủy khác màn Yêu cầu: chỉ 2 cấp phạm vi (không có cấp phòng ban),
  không có Sửa/Xóa, và có 2 lối vào màn lập phiếu.
  Bước tiếp: user bấm tay trên dev + test bằng tài khoản `Quản lý giữ hàng` không phải Super admin;
  giữ 6 bảng `bak_*_20260815` tới lúc đó. BA đọc duyệt 3 tài liệu màn Phiếu hủy.
  Chi tiết + gotcha: plan.md

- finance-product-import-direct-transfer → @junfoke → .plans/gop-db/finance-product-import-direct-transfer/plan.md
  Chuyển Hoàn thành: 2026-10-02 (dọn mục Đang làm) — code đã vào nhánh chung; mục [ ] lẻ còn lại xem plan.md.
  Trạng thái: **XONG PHASE 0-9 + ĐỦ 3 TÀI LIỆU BÀN GIAO** (2026-09-03) — Phase 8 vá 9 bug QA redmine 11092-11108,
  Phase 9 bỏ tab preset; 28/08 sinh testcase 157 TC + HDSD 29 trang; 03/09 bổ sung SRS 45 trang và
  sửa lại TC/HDSD mục ô Số lượng theo hành vi mới (lọc ký tự ngay khi gõ, không còn báo đỏ).
  Port màn "Phiếu chuyển hàng nhập thẳng" sang Tài chính / nhóm Điều chuyển; 1 migration (bảng lịch sử).
  Tài liệu: `testcase - Phieu chuyen hang nhap thang.xlsx` | `HDSD_Phieu chuyen hang nhap thang.docx` |
  `SRS - Phiếu chuyển hàng nhập thẳng.docx` (13 chức năng FR-01..FR-13, 17 quy tắc nghiệp vụ)
  ⚠️ GOTCHA: bản in phiếu bị tràn khối ký ra ngoài khung giấy; ô rỗng danh sách còn hiện dấu `—`.
  Bước tiếp: user so cạnh nhau 2 cổng trên dev + test bằng tài khoản Kế toán kho không phải Super admin.
  Chi tiết + gotcha: plan.md

- unsaved-changes-catalogs → @junfoke → .plans/gop-db/unsaved-changes-catalogs/plan.md
  Chuyển Hoàn thành: 2026-10-02 (dọn mục Đang làm) — code đã vào nhánh chung; mục [ ] lẻ còn lại xem plan.md.
  Trạng thái: **CODE DONE, CHƯA TEST TRÌNH DUYỆT** (2026-08-12). Popup "Thông tin chưa lưu" khi thoát
  form — đợt 1: 14 màn danh mục CSKH + Tài chính, thêm 2 mixin mới, không sửa mixin cũ.
  Bước tiếp: ~147 form trang + ~180 modal của các phân hệ cũ (đợt 2/3).
  Chi tiết + gotcha: plan.md | Spec: docs/superpowers/specs/gop-db/2026-08-12-filter-customization-design.md

- list-page-action-column → @junfoke → .plans/gop-db/list-page-action-column/plan.md
  Chuyển Hoàn thành: 2026-10-02 (dọn mục Đang làm) — code đã vào nhánh chung; mục [ ] lẻ còn lại xem plan.md.
  Trạng thái: **CODE DONE — CHỜ USER VERIFY UI** (2026-08-12). Chuẩn hoá cột "Hành động" màn danh sách
  (mẫu `/assign/customers`) + component dùng chung `V2BaseRowActions.vue`.
  Chi tiết + gotcha: plan.md

- fix-employee-fk-remap → @junfoke → .plans/gop-db/fix-employee-fk-remap/plan.md
  Chuyển Hoàn thành: 2026-10-02 (dọn mục Đang làm) — code đã vào nhánh chung; mục [ ] lẻ còn lại xem plan.md.
  Trạng thái: **CODE DONE, DRY PASS — CHƯA CHẠY THẬT** (2026-08-04). Vá 42 cột / 20.231 dòng FK
  `employees` bị `ReconcileEmployeesSeeder` bỏ sót khi gộp DB (trỏ SAI NGƯỜI, hỏng im lặng).
  ⚠️ TUYỆT ĐỐI không chạy lại `ReconcileEmployeesSeeder` trên DB đã gộp khi `hrm_employees` còn tồn tại
  (164 id vừa là id HRM cũ của người này vừa là id ERP mới của người khác).
  Bước tiếp: user backup DB → chạy `GOP_DB_APPLY=1` cho `FixMissedEmployeeFkSeeder`.
  Chi tiết + gotcha: plan.md | Spec: docs/superpowers/specs/gop-db/2026-08-04-fix-employee-fk-remap-design.md | Tóm tắt: .plans/gop-db/fix-employee-fk-remap/design.md

- customer-cut-mysql2 → .plans/gop-db/customer-cut-mysql2/plan.md
  Chuyển Hoàn thành: 2026-10-02 (dọn mục Đang làm) — code đã vào nhánh chung; mục [ ] lẻ còn lại xem plan.md.
  Trạng thái: **HOÀN TẤT + ĐÃ TEST** (2026-08-01, nhánh `gop_db`). Khách hàng còn ĐÚNG 1 luồng `/assign/customers`.
  Gồm: cắt hết `mysql2` khỏi luồng KH (35 file) · xoá 6 bảng `hrm_customer_*` + migration `2026_08_01_000001_drop_hrm_customer_tables` (đã test round-trip) ·
  gỡ toàn bộ tầng sync 2 chiều · xoá màn `/human/customers` + `/timesheet/setting/customers` · chuyển 10 picker sang luồng mới · thêm `GET assign/customers/search`.
  Test: 52/52 endpoint HTTP + 12 màn browser + luồng ghi (tạo/sửa/thêm liên hệ, có rollback). **7 lỗi thật đã sửa** (xem plan.md Phase 11-12).
  ⚠️ Đọc trước khi làm tiếp trên nhánh này: `.plans/gop-db/design.md`.

- finance-bill-adjust-dept-request (đợt fix 30/09, Phase 43-46) → @khoipv → .plans/gop-db/finance-bill-adjust-dept-request/plan.md
  Hoàn thành: 2026-10-02 — xong đợt fix 30/09. Lỗi "Phải lớn hơn 0" ở ô Số tiền tự ẩn realtime; câu lệch tổng tiền dùng V2BaseError; link mã HĐ trong popup Chọn nhanh + Chọn hợp đồng (ContractSearchModal dùng chung 5 màn); link Số phiếu báo có ở danh sách; Excel chi tiết phiếu sửa bề rộng cột, dòng ký và logo. Không migration.

- borrow-export-request (đợt fix 30/09) → @khoipv → .plans/gop-db/borrow-export-request/plan.md
  Hoàn thành: 2026-10-02 — xong đợt 6 fix 30/09. Ô tìm nhanh chỉ theo mã; validate SL xuất từng hàng tại ô nhập (FE + BE); từ chối xong về danh sách đã mở; id không tồn tại báo "Không tìm thấy dữ liệu"; bỏ "Đang tạo" khỏi ô lọc; nút "Quay lại" về màn trước đó.

- customer-care-service-import — import Excel nhiều sheet cho màn Danh mục gói bảo dưỡng (`/customer-care/services`) → @khoipv → .plans/gop-db/customer-care-service-import/plan.md
  Hoàn thành: 2026-09-22 — user xác nhận đã xong (code + chạy thật trên trình duyệt, import 4 gói test `ZZTEST-GBD-A/B/C/D` id 244/245/247/248). Nhánh `gop_db` cả 2 repo, đã commit + push (`hrm-api` 7450ca1e2 · `hrm-client` 54a584c68, cùng ngày 2026-09-22), không migration, không quyền mới — gate bằng quyền sẵn có `Thêm danh mục gói bảo dưỡng`. Màn này từng bị loại khỏi scope `catalog-import-export` vì có bảng chi tiết; file mẫu 5 sheet (gói · cấp bảo dưỡng · nội dung kiểm tra · hệ số công ty · hàng hoá) nối nhau bằng khoá Mã gói, sinh động ở FE từ chính cấu hình cột của modal. BE: `ServiceImportService.php` mới + 2 route `import/validate` / `import`, ghi bằng cách gọi lại `ServiceService::store()` nên `logCatalogCreate()` vẫn chạy, mỗi gói 1 transaction riêng. FE: `ServiceImportModal.vue` riêng nhưng dùng lại `V2BaseImportToolbar` + `V2BaseImportTable` — **không sửa component dùng chung của 15 màn kia** — thêm `utils/import-multi-sheet-helper.js`; file mẫu dựng bằng ExcelJS (SheetJS bản cộng đồng không ghi được định dạng ô): header nền `D9E1F2` đậm + viền, dòng gợi ý nền `FFF2CC`, đóng băng 2 dòng đầu + cột Mã gói, bộ lọc trên tiêu đề, bám file mẫu tĩnh của màn `finance/type-accounts`. Không đính kèm PDF trong luồng import (user chốt 22/09): gói import xong để trống hồ sơ, bổ sung file ở màn Sửa. 🐞 Chạy thật bắt được `service_levels.benefit_coefficient` NOT NULL không default → ô "Hệ số công nghệ" để trống truyền null làm SQL nổ 1048, đã sửa thành trống quy về 1. ⚠️ Tồn: chưa xoá 4 gói test id 244/245/247/248; cột "Dung lượng" khối đính kèm luôn `—` là nợ có sẵn của `V2BaseAttachmentSection`, không phải do import. Spec: docs/superpowers/specs/gop-db/2026-09-22-customer-care-service-import-design.md

- khai-quy-che-cau-hinh #13 — Quy chế thưởng năm (port ERP "Cấu hình thưởng cuối năm công ty") → @namdangit → .plans/gop-db/khai-quy-che-cau-hinh/plan.md (#13)
  Hoàn thành: 2026-09-24 — code BE+FE XONG, test 7/7 PASS, Playwright verify, **đã commit + push gop_db** cả 2 repo:
  hrm-api `bd3366c07` · hrm-client `4fbe1fc1f` (rebase sạch lên origin/gop_db, HEAD = origin/gop_db). Đây là 1 slice
  ĐỘC LẬP của feature lớn `khai-quy-che-cau-hinh` (feature cha vẫn ở "Đang làm" — các slice khác còn chờ user QA/commit).
  Nhóm MỚI "Quy chế thưởng năm" trong scope **Theo công ty** của màn `khai-quy-che-cau-hinh`. User chốt: khai **theo
  công ty**, **KHÔNG hẹn ngày**, **Approach A** = `SHAPE_DEPT_GRID` (registry const mới) + lưu **replace-all theo
  company_id** vào bảng ERP `company_bonus_end_year_configs` có sẵn (0 dòng) — KHÔNG migration/bảng mới. Lưới 6 cột:
  department_id · bonus_rate · settlement_type (1=DSTC quyết toán · 2=Lợi nhuận phòng · 3=Lợi nhuận công ty) ·
  reserve_fund_percent **XOR** reserve_fund_value (không cùng >0) · max_risk_reserve_fund. GIỮ gate `Cài đặt cấu hình`
  (khác ERP ungated — HRM fail-closed). KHÔNG ghi lịch sử (ERP cũng không). Entity buộc `extends Model` (bảng ERP) →
  service tự gán created_by/updated_by = actorId ở MỌI đường ghi. BE: `RegulationTabRegistry` (SHAPE_DEPT_GRID) ·
  `CompanyBonusEndYearConfig` entity · `RegulationConfigService` (getDeptGridConfig/saveDeptGrid replace-all trong
  transaction + nullIfBlank) · controller `saveDeptGrid` + route POST `regulation-config/{tabKey}/dept-grid` (trong
  group middleware `checkPermission:Cài đặt cấu hình`) · `RegulationDeptGridRequest` (dept required + không trùng,
  settlement_type in:1,2,3, reserve XOR, thông báo tiếng Việt kèm số dòng). FE: `data.js` thêm nhóm `thuongnam`
  (name "Quy chế thưởng năm", type dept-grid) + renderer dept-grid. **Kèm theo**: RENAME nhóm scope-phòng "Quy chế hoa
  hồng / năng suất" → "Quy chế thưởng" (data.js) — user chốt "Giữ, gộp vào commit #13". Test:
  `RegulationDeptGridTest` 7 test / 29 assertions PASS (chạy DB thật erp_hrm_check, companyId=1, actorId=999,
  setUp snapshot + tearDown restore vì test replace-all/empty xoá sạch dòng công ty). Spec:
  docs/superpowers/specs/gop-db/2026-09-24-khai-quy-che-thuong-nam-design.md

- bom-list-list-page-standard — chuẩn hoá màn Danh sách BOM List (`/assign/bom-list`) theo skill `list-page` → @khoipv → .plans/gop-db/bom-list-list-page-standard/plan.md
  Hoàn thành: 2026-09-10 — user xác nhận đã xong (code + kiểm chứng API/compile 2026-09-07). Nhánh `gop_db` cả 2 repo, chưa commit, không migration, không quyền mới. BE: 6/6 mã màu trạng thái nằm ngoài bảng 9 mã chuẩn quy về đúng nhóm; thêm `isCanEdit()`/`isCanDelete()` khớp guard của service; whitelist `SORTABLE_COLUMNS` + chốt `id desc` (trước `orderBy($request->sort_field)` trần); ngày bỏ giây; registry `bom_lists` 23 cột + `exportList()` chuyển sang `DynamicExport` — bỏ blade phải tự map từng khoá cột (đổi tên cột trên lưới là file ra rỗng đúng cột đó). FE: `V2BaseSmartFilterPanel`, tách cột gộp `code_name` và gỡ tối đa 6 icon thao tác khỏi ô mã, cột Hành động cuối bảng (Sửa · Xóa + `⋮` Sao chép · In · Lịch sử), thêm 3 cột Phòng của người tạo · Người/Ngày cập nhật, `fixed-layout` 17 cột đủ `width` = `minWidth`, `columnCustomizationMixin`, lần đầu có popup chọn trường xuất file, 2 request `per_page=10000` hoãn tới khi mở panel lọc, `loadSeq`, `handleSort`/`handleReset` hết bắn 2 request. Kiểm chứng trên 11 BOM thật: index 200 (32 query/10 dòng), 2 khoá sort đúng + key lạ về mặc định, export .xlsx 18 dòng = 11 dữ liệu + 7 dòng khung, `exportFields` ↔ registry 23 = 23. Màn đã có sẵn hành động Lịch sử (`BomListLogModal`) nên không nợ như các màn khác. Spec: docs/superpowers/specs/gop-db/2026-09-07-bom-list-list-page-standard-design.md

- contract-list-page-standard — chuẩn hoá màn Danh sách hợp đồng (`/assign/contracts`) theo skill `list-page` → @khoipv → .plans/gop-db/contract-list-page-standard/plan.md
  Hoàn thành: 2026-09-10 — user xác nhận đã xong (code + kiểm chứng API/compile trên dữ liệu thật 2026-09-07). Nhánh `gop_db` cả 2 repo, chưa commit, không migration, không quyền mới. BE: 10/10 mã màu trạng thái quy về bảng 9 mã chuẩn; 4 cờ `is_can_edit`/`is_can_delete`/`is_can_approve`/`is_can_liquidate` = quyền AND trạng thái, hỏi quyền **1 lần cho cả trang** thay vì 4 truy vấn mỗi dòng; thêm `updater_name` + 3 ngày dạng chữ; tách `buildListQuery()` dùng chung index/export + whitelist sort nhận cả khoá `*_text` của FE và **chốt `id desc`**; registry `contracts` 13 cột + route/`export()` mới. FE: `V2BaseSmartFilterPanel` (nhóm Công ty/Phòng ban/Bộ phận/Người lập gom 1 field `org`); **bộ lọc trạng thái liệt kê đủ 10 trạng thái** — bản cũ chỉ 4 nên không lọc được các bước xuất hàng / quyết toán dù dữ liệu thật có đủ; Mã hợp đồng thành `nuxt-link`; cột Hành động cuối bảng (Sửa · Xóa · Duyệt · Thanh lý, "Không duyệt" không đưa vào); thêm 5 cột; `fixed-layout` 15 cột đủ `width` = `minWidth`; **lần đầu có cấu hình cột hiển thị và nút Xuất Excel**; `loadSeq`. Kiểm chứng trên 42 hợp đồng thật: index 200 (47 query/10 dòng), 4 khoá sort đúng, export .xlsx 49 dòng, `exportFields` ↔ registry 13 = 13; cờ thao tác đúng theo từng trạng thái và **fail-closed** với tài khoản không có 4 quyền; điều kiện hiện nút ở danh sách khớp màn chi tiết. Chưa làm: hành động Lịch sử (module Assign chưa có `LogsCatalogHistory`; hợp đồng có bảng `contract_histories` riêng dùng ở màn chi tiết). Spec: docs/superpowers/specs/gop-db/2026-09-07-contract-list-page-standard-design.md

- meeting-list-page-standard — chuẩn hoá màn Danh sách meeting (`/assign/meeting`) theo skill `list-page` → @khoipv → .plans/gop-db/meeting-list-page-standard/plan.md
  Hoàn thành: 2026-09-10 — user xác nhận đã xong (code + kiểm chứng API/compile trên dữ liệu thật 2026-09-07). Nhánh `gop_db` cả 2 repo, chưa commit, không migration, không quyền mới. 🐞 3 lỗi có sẵn: `MeetingController::index()` dùng biến `$sortMapping` **không tồn tại**; `MeetingCriteria` chạy trước nên `orderByDesc('updated_at')` ở đó luôn thắng, mọi `orderBy` của controller chỉ là khoá phụ (bấm sort cột Tên/Mã không ăn); meeting của nhân viên đã xoá quan hệ gây **500** vì thiếu null-guard `creator`. Ô lọc **Nhân viên** ghi vào `employee_id` mà BE không đọc (ô lọc chết) → tắt, thay bằng ô Người tạo đúng khoá; `initialStateForm` sửa `company_name` → `company_id` (bấm "Làm mới" trước đây không xoá được ô Công ty). BE thêm `STATUS_COLORS` + `MODES` (trước `STATUS` chỉ có tên class CSS `text-brand`, không dùng được cho badge), whitelist sort 9 khoá, registry `meetings` 21 cột + export `.xls` → `.xlsx` cột động, eager load 8 quan hệ + bỏ `TpCustomer::find(null)` → **175 → 70 truy vấn/10 dòng**. FE: panel 11 mục/13 ô; tách ô gộp `meetingInfo` (mã + tên + 3 dòng phụ + 6 icon) thành 6 cột; cột Hành động cuối bảng; **bỏ toàn bộ `v-html` + 4 hàm dựng HTML + listener `document.addEventListener('click')`**; thêm cột Địa điểm; `fixed-layout` 18 cột đủ `width` = `minWidth`; lần đầu có popup chọn trường xuất file; `loadData()` là request đầu tiên (bản cũ chờ `customers/search?limit=20000` xong mới nạp danh sách). Kiểm chứng trên 37 meeting thật: 70 query, 4 trạng thái đúng bảng màu, 4 khoá sort + 3 bộ lọc đều ăn, export .xlsx 44 dòng, `exportFields` ↔ registry 21 = 21. ⚠️ `MeetingResource` còn dùng chung ở `MyJobController`/`SolutionController`/`SolutionModuleController` → 3 màn đó hưởng lây khoá mới + định dạng ngày. Spec: docs/superpowers/specs/gop-db/2026-09-07-meeting-list-page-standard-design.md

- pricing-request-list-page-standard — chuẩn hoá màn Danh sách yêu cầu xây dựng giá (`/assign/pricing-requests`) theo skill `list-page` → @khoipv → .plans/gop-db/pricing-request-list-page-standard/plan.md
  Hoàn thành: 2026-09-10 — user xác nhận đã xong (code + kiểm chứng API/compile 2026-09-07). Nhánh `gop_db` cả 2 repo, chưa commit, không migration, không quyền mới. 🐞 3 chức năng CHẾT có sẵn: nút "Làm mới" gọi `this.loadData()` — hàm không tồn tại nên ném TypeError, ô lọc bị xoá mà danh sách giữ nguyên kết quả cũ; nút "Sửa nháp" ở danh sách **không bao giờ hiện** vì FE so `item.created_by` mà Resource không trả khoá đó (`Number(undefined)` = NaN); màn **Sửa** và màn **chi tiết** khoá toàn bộ form với MỌI phiếu do đọc `$store.state.auth?.user?.id` không tồn tại — nay cả 3 chỗ đọc cờ `is_can_edit` của máy chủ. BE: whitelist sort 10 khoá + chốt `id desc`, tách `buildListQuery()` dùng chung index/export, tìm nhanh thêm Người yêu cầu bằng EXISTS, 6 mã màu về bảng chuẩn, Resource trả khoá phẳng + `is_can_edit`/`is_can_delete`, registry `pricing_requests` 20 cột + route export đặt TRƯỚC `/{id}`. FE: panel 5 ô, Mã YCBG thành `nuxt-link`, cột Hành động cuối bảng (Sửa · Xóa · Tạo báo giá) — **thêm hành động Xóa lần đầu** (endpoint `DELETE` có sẵn, FE chưa từng gọi), thêm 3 cột, `fixed-layout` 16 cột đủ `width` = `minWidth`, lần đầu có cấu hình cột + Xuất Excel; màn chi tiết thêm nút Xóa cho khớp danh sách. Kiểm chứng: bảng `pricing_requests` đang rỗng → dựng dữ liệu thật trong transaction rồi rollback; 5 khoá sort đúng, tìm nhanh theo mã và theo tên người yêu cầu đều ăn, export .xlsx kể cả khi 0 dòng, `exportFields` ↔ registry 20 = 20; cờ quyền 3 chiều fail-closed. ⚠️ **Chờ user quyết (chưa sửa)**: người có quyền "Xây dựng giá bán theo công ty/phòng" KHÔNG thấy phiếu nháp của chính mình — nhánh phạm vi ở `index()` thay điều kiện "của tôi" bằng `whereIn('status', [2..6])` mà nháp là status 1; sửa là đổi phạm vi dữ liệu người dùng nhìn thấy nên không tự quyết. Spec: docs/superpowers/specs/gop-db/2026-09-07-pricing-request-list-page-standard-design.md

- product-project-list-page-standard — chuẩn hoá màn Danh sách hàng hoá làm dự án (`/assign/product-project`) theo skill `list-page` → @khoipv → .plans/gop-db/product-project-list-page-standard/plan.md
  Hoàn thành: 2026-09-10 — user xác nhận đã xong (code + kiểm chứng API/compile trên dữ liệu thật 2026-09-07). Nhánh `gop_db` cả 2 repo, chưa commit, không migration, không quyền mới. 🐞 2 lỗi có sẵn: `sort_field` bị **bỏ qua hoàn toàn** — bấm sort cột nào cũng chỉ đổi chiều theo ngày tạo (nay whitelist 3 khoá + `resolveSortKey()`); `dedupUnionRows()` không chốt khoá cuối nên 2 dòng cùng giá trị có thứ tự không xác định → lật trang thấy bản ghi lặp/mất (nay chốt `row_id desc`). BE thêm `erp_sync_status_color` (3 mã chuẩn) + `product_attributes_text` (hạ HTML TSKT về chữ cho file Excel), registry `product_projects` 19 cột, export `.xls` → `.xlsx` cột động. FE: `V2BaseSmartFilterPanel` 7 ô; `fixed-layout` 17 cột đủ `width` = `minWidth` **đo trên 181 dòng thật** (max + phân vị 95, không ước lượng); ô tham chiếu ghép `MÃ - Tên`; thêm cột Ngày tạo; Trạng thái đồng bộ bỏ `.pp-chip` tự chế sang `V2BaseBadge`; `columnCustomizationMixin`; lần đầu có popup chọn trường xuất file; `loadData()` bắn đầu tiên + `loadSeq`; bỏ 15 chỗ `'—'` và 4 khối CSS chết; màu chữ trong ô đồng bộ màn mẫu `/assign/customers` (rà cùng đợt 4 màn: customers 18 ô · solutions 21 · prospective-projects 10 · product-project 13). Kiểm chứng: index 200 với 181 dòng, 3 khoá sort đúng + key lạ về mặc định, export .xlsx thật, `fields=` còn đúng 3 cột, `exportFields` ↔ registry 19 = 19. ⚠️ **Màn chỉ đọc, không có cột Hành động** (routes chỉ có index + export + picker); TSKT trong file Excel nối dòng bằng " · " vì blade dùng chung `exports/dynamic.blade.php` in bằng `{{ }}` — muốn xuống dòng thật phải sửa file chung của 18 màn, cần hỏi trước. Spec: docs/superpowers/specs/gop-db/2026-09-07-product-project-list-page-standard-design.md

- prospective-project-list-page-standard — chuẩn hoá màn Danh sách dự án tiền khả thi (`/assign/prospective-projects`) theo skill `list-page` → @khoipv → .plans/gop-db/prospective-project-list-page-standard/plan.md
  Hoàn thành: 2026-09-10 — user xác nhận đã xong (code + kiểm chứng API/compile trên dữ liệu thật 2026-09-07). Nhánh `gop_db` cả 2 repo, chưa commit, không migration, không quyền mới. BE: whitelist sort 13 khoá + chốt `id desc` (trước `orderBy($request->sort_field)` trần); subquery `creator_name`/`updater_name` không leftJoin; `STATUS_COLORS` + `PARENT_STATUS_COLORS` theo bảng 9 mã chuẩn; ngày `d-m-Y` → `d/m/Y H:i` và **bỏ khoá trùng `customer_need_solution_date`** đang ghi đè bản đã format; gỡ N+1 + eager load 12 quan hệ → **147 → 56 query/10 dòng**; 3 danh mục cứng chuyển từ FE/blade về hằng trên Entity; registry `prospective_projects` 32 cột + export ép `tree = false` để file phẳng có cả dự án con. FE: tách cột gộp `projectInfo`, thêm 7 cột, cột Hành động cuối bảng (Sửa · Xóa + `⋮` Tạo giải pháp · Tạo yêu cầu làm GP), `V2BaseBadge` thay 5 rule CSS `.pj-status-*`, `columnCustomizationMixin` thay ~80 dòng viết tay, lần đầu có popup chọn trường xuất file, giữ nguyên cây cha–con. Phase 4 theo phản hồi user cùng ngày: cột Khách hàng/Khách hàng cuối 240 → 260px, dòng phụ đổi xám `#6b7280` (`.text-muted` bị 4 file scss toàn cục ép thành ĐỎ), cột Mã 170 → 210px vì mã dài tới 26 ký tự, **gộp NV KD phụ trách + Phòng ban + Bộ phận thành 1 cột** (bảng 29 → 27 cột, file xuất vẫn giữ 3 cột riêng), thử ghim cột Tên rồi bỏ theo yêu cầu user. Kiểm chứng: 27/27 cột đủ `width` = `minWidth`, `exportFields` ↔ registry 32 = 32 và 32/32 khoá có thật trong Resource, sort 3 khoá đúng + chuỗi tiêm SQL về mặc định, export 109 KB, `fields=` còn 3 cột. ⚠️ **Bộ lọc giữ nguyên `V2BaseFilterPanel`** (user chốt 2026-09-07) nên 3 quy tắc của skill chưa áp cho màn này. Spec: docs/superpowers/specs/gop-db/2026-09-07-prospective-project-list-page-standard-design.md

- quotation-list-page-standard — chuẩn hoá màn Danh sách báo giá (`/assign/quotations`) theo skill `list-page` → @khoipv → .plans/gop-db/quotation-list-page-standard/plan.md
  Hoàn thành: 2026-09-10 — user xác nhận đã xong (code + kiểm chứng API/compile trên dữ liệu thật 2026-09-07). Nhánh `gop_db` cả 2 repo, chưa commit, không migration, không quyền mới. BE: 6/7 mã màu trạng thái báo giá + bảng trạng thái báo giá tổng quy về bảng 9 mã chuẩn, thêm `APPROVAL_LEVEL_COLORS`; whitelist `QUOTATION_SORTABLE_COLUMNS` + `applyQuotationSort()` chốt `id desc`; Resource `updated_at` format lại (trước trả THÔ chuỗi ISO) + `updater_name` + 4 khoá phẳng `bom_code`/`bom_name`/`project_code`/`project_name` (blade xuất file không đọc được mảng lồng); registry `quotations` 20 cột + route `exportList()` mới đặt TRƯỚC `/{id}` — ⚠️ khác hẳn `exportExcel()` sẵn có là xuất CHI TIẾT 1 báo giá để sửa rồi nạp lại. FE: `V2BaseSmartFilterPanel`, tách cột gộp `code_name` và gỡ 6 icon thao tác khỏi ô mã, cột Hành động cuối bảng (Sửa · Xóa + `⋮` Sao chép · In · Lịch sử phê duyệt), thêm 3 cột, Cấp duyệt + Đồng bộ ERP đổi sang `V2BaseBadge` (bỏ 3 class `.badge-level-*` nền đậm chữ trắng), `fixed-layout` 20 cột đủ `width` = `minWidth`, **lần đầu có nút Xuất Excel danh sách**, `loadSeq`. 🐞 Sửa lỗi "Làm mới" ném TypeError (`this.loadData()` không tồn tại, tên đúng là `fetchData`) — rà bằng grep phát hiện **màn thứ ba cùng lỗi là `/assign/quotations/pending-approval`**, đã sửa luôn. Kiểm chứng trên 75 báo giá thật: index 200 (57 query/10 dòng), 5 trạng thái đúng bảng màu, `updated_at` = `27/07/2026 16:55`, 3 khoá sort đúng, export .xlsx 82 dòng, `exportFields` ↔ registry 20 = 20. ⚠️ `/assign/quotations/pending-approval` và `/assign/summary-quotations` dùng chung `QuotationResource` nên hưởng lây phần sửa. Spec: docs/superpowers/specs/gop-db/2026-09-07-quotation-list-page-standard-design.md

- request-solution-list-page-standard — chuẩn hoá màn Danh sách yêu cầu làm giải pháp (`/assign/request-solution`) theo skill `list-page` → @khoipv → .plans/gop-db/request-solution-list-page-standard/plan.md
  Hoàn thành: 2026-09-10 — user xác nhận đã xong (code + kiểm chứng API/compile trên dữ liệu thật 2026-09-07). Nhánh `gop_db` cả 2 repo, chưa commit, không migration, không quyền mới. BE: 5 mã màu lệch bảng chuẩn quy về đúng nhóm (đáng chú ý "Yêu cầu bổ sung" `#DC2626` → `#F59E0B` — đỏ là ngôn ngữ của từ chối, không phải "cần bổ sung"); thêm 3 quan hệ + `isCanEdit()`/`isCanDelete()`; whitelist sort + chốt `id desc`; Resource trả `solution_code`/`solution_pm_name`/`solution_pm_phone` — **2 cột trên bảng vốn in cứng dấu gạch**; Người tạo/cập nhật chỉ còn TÊN, ngày bỏ giây; registry `request_solutions` 24 cột + export `.xls` → `.xlsx`. Hiệu năng đo bằng số: bỏ `find()` từng dòng, bỏ `->load()` thừa, cache static quyền + `departmentsManager()` → **115 → 54 truy vấn và 5,4s → 0,28s** trên 10 dòng. FE: panel gom nhóm `org`, tách cột gộp `request` + gỡ 4 icon thao tác khỏi ô mã, cột Hành động cuối bảng (Sửa · Xóa · Làm giải pháp · Hủy yêu cầu), 2 cột Mã GP / PM làm GP render dữ liệu thật, thêm 4 cột người/ngày, `fixed-layout` 22 cột đủ `width` = `minWidth`, `columnCustomizationMixin` + popup chọn trường xuất file, `loadData()` bắn đầu tiên + `loadSeq`, xoá hàm chết `deleteOne()` dùng `confirm()` trình duyệt + toast giả "(demo)". Kiểm chứng trên 18 yêu cầu thật: 4 khoá sort đúng, export .xlsx 25 dòng, `exportFields` ↔ registry 24 = 24, cờ quyền fail-closed với người khác. ⚠️ `/assign/request-solution/pending` dùng chung Resource nên hưởng lây (giao diện màn đó đã chuẩn hoá 2026-09-08). Spec: docs/superpowers/specs/gop-db/2026-09-07-request-solution-list-page-standard-design.md

- solution-module-list-page-standard — chuẩn hoá màn Danh sách hạng mục dự án (`/assign/solution-modules`) theo skill `list-page` → @khoipv → .plans/gop-db/solution-module-list-page-standard/plan.md
  Hoàn thành: 2026-09-10 — user xác nhận đã xong (code + kiểm chứng API/compile trên dữ liệu thật 2026-09-07). Nhánh `gop_db` cả 2 repo, chưa commit, không migration, không quyền mới. BE: 2 mã màu lệch bảng chuẩn ("Chờ duyệt hồ sơ trình duyệt" `#F59E0B` → `#D97706` vì `#F59E0B` là nhóm Cảnh báo, khác nghĩa; "Đã duyệt" `#10B981` → `#16A34A`); whitelist sort + chốt `id desc`; eager load `employee_create.info`/`employee_update.info`; Resource trả `creator_name`/`updater_name`/`updated_at` chỉ lấy `fullname`; registry `solution_modules` 13 cột + route/`export()` mới đặt TRƯỚC `/{solutionModule}`. FE: `V2BaseSmartFilterPanel`, tách cột gộp `solutionModuleInfo` + gỡ 3 icon thao tác khỏi ô mã, cột Hành động cuối bảng (Sửa · Lưu và duyệt) — **bỏ hành động "Quản lý" trùng với link ở cột Mã** và bỏ `@row-click` điều hướng; thêm 4 cột người/ngày; `fixed-layout` 13 cột đủ `width` = `minWidth` (Mã hạng mục lấy bậc L 260px vì mã dài tới 35 ký tự); **lần đầu có cấu hình cột và nút Xuất Excel**; `loadData()` bắn ĐẦU TIÊN — bản cũ `await loadFilterOptions()` tải `assign/solutions/getAll?per_page=10000` xong mới nạp bảng, chỉ để đổ options cho 1 ô lọc trong panel đang thu gọn (nay hoãn tới khi mở panel, `per_page` hạ còn 1.000). Kiểm chứng trên dữ liệu thật (5 hạng mục, tài khoản test thấy 3): index 200 trả đủ trường mới, `status_color` đúng bảng, 2 khoá sort đảo đúng + key lạ về `created_at desc`, export .xlsx 10 dòng, `exportFields` ↔ registry 13 = 13. ⚠️ **Không tài khoản nào đang có 4 quyền "Xem danh sách hạng mục dự án theo tổng công ty / công ty / phòng ban / bộ phận"** (kiểm bằng SQL) — mọi người chỉ thấy hạng mục mình liên quan; không phải lỗi đợt này nhưng nghiệp vụ cần thì phải gán quyền. Spec: docs/superpowers/specs/gop-db/2026-09-07-solution-module-list-page-standard-design.md

- task-list-page-standard — chuẩn hoá màn Danh sách task (`/assign/tasks`) theo skill `list-page` → @khoipv → .plans/gop-db/task-list-page-standard/plan.md
  Hoàn thành: 2026-09-10 — user xác nhận đã xong (code + kiểm chứng API/compile trên dữ liệu thật 2026-09-07). Nhánh `gop_db` cả 2 repo, chưa commit, không migration, không quyền mới. 🐞 `TaskService` sắp xếp bằng `orderBy($request->sort_field, $request->sort_dir)` nhận thẳng chuỗi từ URL → nay whitelist 12 khoá + chốt `id desc`. BE: 5/10 mã màu trạng thái về bảng chuẩn + thang màu ưu tiên RIÊNG; Resource thêm `status_color`, `priority_name`/`priority_color`, `deadline_state_text`/`_color`, ngày bỏ giây, `updated_by_name` bỏ tiền tố mã nhân viên; bỏ N+1 (3 chỗ `Employee::find()->info`, `->load('priorityLevel')` chạy từng dòng phá luôn eager load) + hằng `LIST_RELATIONS` 15 quan hệ dùng chung index/export → **325 → 67 truy vấn/10 dòng**; registry `tasks` 27 cột + export thay `TaskExport` blade 13 cột cứng. FE: panel 15 mục/17 ô; tách ô gộp `taskInfo` (mã + tên + 3 dòng phụ + chip tag + 6 icon) thành 7 cột; cột Hành động cuối bảng (Sửa · Xóa + `⋮` Nhập kết quả · Duyệt · Lịch sử); bỏ 4 hàm tô màu tự chế → `V2BaseBadge` với màu BE trả; thêm 5 cột (Tình trạng hạn · Tag · Ngày tạo · Người/Ngày cập nhật); `fixed-layout` 22 cột đủ `width` = `minWidth` + bỏ đoạn tự gán `sticky: index < 3` (cột kéo đi đâu cũng ghim → offset `left` sai); lần đầu có popup chọn cột xuất file và **lọc nhiều tag mới gửi được hết** (trước `buildQueryString` chỉ gửi tag cuối); `loadSeq` + `suppressFilterWatch`; **xoá ~450 dòng code chết**. ⚠️ Khối lọc nhanh chuyển từ slot `toolbar` sang `left-actions` — `toolbar` thay cả khối tiêu đề nên **màn đang mất tiêu đề bảng**. Kiểm chứng trên 14 task thật: 67 truy vấn (trước 325), 4 trạng thái + 3 mức ưu tiên đúng thang màu, 4 khoá sort + 3 bộ lọc đều ăn, export .xlsx 21 dòng / 28 cột, `exportFields` ↔ registry 27 = 27. ⚠️ `TaskResource` còn dùng ở `MyJobController` và báo cáo → hưởng lây khoá mới + định dạng ngày. Spec: docs/superpowers/specs/gop-db/2026-09-07-task-list-page-standard-design.md

- finance-prepick-transfer-request — port màn **Phiếu yêu cầu điều chuyển hàng giữ** (ERP `warehouse/prepick_transfer2` → HRM `/finance/prepick-transfer-requests`) → @junfoke → .plans/gop-db/finance-prepick-transfer-request/design.md · plan.md
  Hoàn thành: 2026-09-10 — user xác nhận đã xong (code + Playwright bấm thật 2026-08-25, vá QA redmine 11279/11296 ngày 2026-09-04). Nhánh riêng `feat/finance-prepick-transfer-request` (cả 2 repo, tách từ `gop_db`). Dùng chung bảng ERP `prepick_transfer2` + `prepick_transfer2_details` giữ nguyên schema, **chỉ 1 migration thêm bảng lịch sử của HRM** (`2026_08_24_000001_create_prepick_transfer_request_history_table`, đã chạy); không tạo quyền mới. Đủ luồng: danh sách + bộ lọc, form lập/sửa, chi tiết + 3 cấp duyệt, in, xuất Excel, đính kèm, lịch sử. Kiểm chứng Playwright: 10 cột đúng thứ tự, 3 badge đúng mã màu chuẩn, cột Hành động đổi theo trạng thái, 4 bộ lọc đối chiếu SQL khớp từng con số (16 = 16 · 230 = 230 · 2 = 2), sort + phân trang + cấu hình cột + popup Lịch sử đều đúng, mọi lần test đều hoàn nguyên DB và đối chiếu 4 bảng `bak_*_20260824` **0 chênh lệch**. 🐞 Bắt được bug `markFormSaved()` gọi ngay sau khi nạp dữ liệu → cờ `unsavedIgnore` bật vĩnh viễn nên cảnh báo "chưa lưu" không bao giờ hiện; **đã vá luôn cho 2 màn đang chạy** (Gia hạn + Phiếu hủy hàng giữ) và bỏ 43 chỗ `|| '—'` + 7 `placeholder="—"` ở 3 màn Giữ hàng cũ. Thêm util dùng chung `utils/scrollToFirstError.js` (bấm Lưu là nhảy tới đúng dòng lỗi) gom 4 khối cuộn viết tay của nhóm Giữ hàng. QA 11279: một hàng đang giữ cho 2 khách/2 hạn phải thêm được 2 dòng — popup đổi từ loại theo `product_id` sang **loại theo LÔ** (`exclude_lot_ids[]`), 2 màn Hủy/Gia hạn giữ nguyên cách cũ. Tồn: xoá 4 bảng `bak_*_20260824` sau khi user nghiệm thu. Spec: docs/superpowers/specs/gop-db/2026-08-24-finance-prepick-transfer-request-design.md

- bom-list-customer-filter-remote — sửa lỗi ô lọc Khách hàng màn BOM List → chưa ghi người phụ trách → .plans/gop-db/bom-list-customer-filter-remote/plan.md
  Hoàn thành: 2026-09-10 — user xác nhận đã xong (code 2026-08-19). Bỏ `assign/customers/search?limit=20000` ở `pages/assign/bom-list/index.vue` — nạp 43k khách hàng làm **BE PHP fatal "Allowed memory size exhausted"**; đổi ô lọc sang `V2BaseSelectRemote` + `fetchCustomers(q, limit=30)` theo khuôn `/sale/warranty-repair-requests`; giữ nhãn KH khi tự điền theo dự án TKT hoặc quay lại màn (`customerInitialOption` + localStorage). Không migration, không quyền mới.

- fe-build-toi-uu — giảm thời gian `yarn run build` của `hrm-client` mỗi lần deploy lên `hrm-crm.eteksofts.com` → chưa ghi người phụ trách → .plans/gop-db/fe-build-toi-uu/plan.md
  Hoàn thành: 2026-09-10 — user xác nhận đã xong Phase 1 (đo 2026-08-17). Bật `build.cache` + `build.parallel` trong `nuxt.config.js` (trước cả 2 đang bị comment); đo thật trên bản clone `gop_db-client` (Node 14.21.3, 10 core): **baseline 223s → dựng cache 195s → sửa 2 file 134s → sửa 1 file 96s**; kiểm chứng cache không trả bundle cũ bằng chuỗi marker. Còn lại: cập nhật `~/build_hrm_crm.sh` trên server (bỏ qua build khi không có file FE đổi; chỉ `yarn install --frozen-lockfile` khi `package.json`/`yarn.lock` đổi; **bỏ `npm install` vì trộn npm với yarn làm xoá `node_modules/.cache`**) — file này nằm ngoài repo. Phase 2 chờ user quyết: gỡ 11 thư viện 0 import, gộp 4 bộ chart về `apexcharts`, đổi `node-sass@4` → dart-sass.

- quotation-pending-approval-list-page-standard — chuẩn hoá màn Báo giá chờ duyệt (`/assign/quotations/pending-approval`) theo skill `list-page` → @khoipv → .plans/gop-db/quotation-pending-approval-list-page-standard/plan.md
  Hoàn thành: 2026-09-10 — user xác nhận đã xong (code + kiểm chứng API/compile trên dữ liệu thật 2026-09-08). BE 4 file · FE 1 file, không migration, không quyền mới; dùng chung `QuotationResource` + `applyListFilters()` với màn `/assign/quotations` nên phần truy vấn hưởng sẵn. Sửa 3 lỗi có sẵn: whitelist sort thiếu đúng khoá MẶC ĐỊNH của màn (`sort_field = 'submitted_at'` không có trong `QUOTATION_SORTABLE_COLUMNS` → âm thầm rơi về `created_at desc`) cùng `customer_name`/`price_approval_level`/`status` — bổ sung 6 khoá; Resource trả `submitted_at` thô trong khi các mốc khác đã format ở BE; registry `quotations` thiếu hẳn khoá `submitted_at` nên cả 2 màn báo giá không xuất được cột Ngày gửi duyệt. Thêm `pendingApprovalExport()` + route export gắn cùng middleware quyền với route danh sách. FE: `V2BaseSmartFilterPanel` 6 mục (bản cũ 2 ô trong khi BE nhận sẵn 12 khoá lọc), tách cột gộp "Mã BG • BOM" và gỡ nút thao tác khỏi ô mã, cột Hành động cuối bảng (Duyệt + Lịch sử phê duyệt), Cấp duyệt bỏ 2 class badge tự chế sang `V2BaseBadge`, `fixed-layout` 17 cột đủ `width` = `minWidth`, lần đầu có xuất Excel, `columnCustomizationMixin`, `loadSeq`, `$safeLoading*`, `fetchData()` bắn ngay thay vì chờ 2 request không liên quan. Bỏ 2 cột "Người duyệt"/"Ngày duyệt" — ⚠️ bài học đo đạc: đếm thô `status IN (3,4)` ra 38 dòng (38 có `approved_at`) suýt cho kết luận ngược, chạy đúng `getPendingApproval()` với tài khoản có quyền duyệt mới ra 13 dòng (0 `approved_at`, 13/13 `submitted_at`); các màn "chờ duyệt" còn lại phải chạy đúng hàm service của màn chứ không đếm `WHERE status = X`. Spec: docs/superpowers/specs/gop-db/2026-09-08-quotation-pending-approval-list-page-standard-design.md

- handover-pending-list-page-standard — chuẩn hoá màn Phiếu bàn giao chờ duyệt (`/assign/handover/pending`) theo skill `list-page` → @khoipv → .plans/gop-db/handover-pending-list-page-standard/plan.md
  Hoàn thành: 2026-09-10 — user xác nhận đã xong (code + kiểm chứng API/compile 2026-09-08). BE 3 file · FE 1 file, không migration, không quyền mới; màn thứ 3 (cuối) của cụm phiếu bàn giao, trước giờ là nhánh code song song nên không hưởng gì từ 2 đợt chuẩn hoá 2026-09-07. Sửa 3 lỗi có sẵn: bộ lọc "Ngày gửi duyệt từ/đến" lọc nhầm cột `updated_at` thay vì `submitted_at` (mà `updated_at` đổi mỗi lần sửa phiếu nên khoảng ngày người dùng chọn ra sai phiếu); `pending()` chốt cứng `orderBy('created_at','desc')` nên màn không sắp xếp được cột nào dù `applyHandoverSort()` whitelist 13 khoá đã có sẵn cùng service (⚠️ service này đặt tên `applyHandoverSort`, không phải `applySort`); nút Xuất Excel là nút chết — gọi lại chính API danh sách rồi báo "đang phát triển", nay dùng `DynamicExport` + registry `handovers` chung với màn danh sách. FE: `V2BaseSmartFilterPanel` 8 mục (trước không có auto-search), ô Giải pháp bỏ `disabled` cứng thành ô chọn thật cascade theo Dự án, Mã phiếu đổi sang `nuxt-link` và gỡ nút thao tác khỏi ô đó, cột Hành động cuối bảng (Duyệt + Lịch sử), lần đầu có sắp xếp cột / cấu hình cột / giữ bộ lọc / popup chọn trường xuất file, `fixed-layout` 15 cột đủ `width` = `minWidth`, `loadSeq`, `$safeLoading*`. Bỏ hẳn 6 khoá vì trạng thái của màn quyết định (`approver_name`/`approved_at`/`reject_reason` và 3 con số nhận/từ chối/chờ luôn 0/0/tổng). ⚠️ Bảng `handovers` RỖNG trên DB dev → kiểm chứng bằng 3 phiếu giả trong transaction rồi rollback; chưa thử 4 bộ lọc đi qua `items` (câu lọc giữ nguyên bản cũ). Spec: docs/superpowers/specs/gop-db/2026-09-08-handover-pending-list-page-standard-design.md

- request-solution-pending-list-page-standard — chuẩn hoá màn Yêu cầu làm giải pháp chờ duyệt (`/assign/request-solution/pending`) theo skill `list-page` → @khoipv → .plans/gop-db/request-solution-pending-list-page-standard/plan.md
  Hoàn thành: 2026-09-10 — user xác nhận đã xong (code + kiểm chứng API/compile trên dữ liệu thật 2026-09-08). BE 3 file · FE 1 file, không migration, không quyền mới; dùng chung `RequestSolutionResource` với màn `/assign/request-solution` nhưng trước giờ là nhánh code song song. Sửa 6 lỗi có sẵn: `pending()` đẩy thẳng `$request->sort_field` vào `orderBy()` (không whitelist, không chốt `id desc`) dù `applySort()` có sẵn cùng service; thiếu 5 eager load mà `index()` đã bổ sung → 4 cột luôn rỗng + N+1; không có quyền thì `pending()` trả mảng `[]` còn `exportPending()` gọi `->get()` trên đó → fatal 500; FE `canReceive()` hard-code `return true` dù entity đã có `isCanReceive()`; `handleFilterChange()` nhận sai kiểu payload nên nhét 2 khoá rác `key`/`value` vào filters rồi gửi lên API; `handleSort`/`handleReset` bắn 2 request mỗi thao tác. Export chuyển từ `RequestSolutionPendingExport` (.xls cột cứng) sang `DynamicExport` + registry `request_solutions` dùng chung. FE: `V2BaseSmartFilterPanel` 5 mục, tách cột gộp "Mã • Tên yêu cầu" và gỡ 4 icon thao tác khỏi ô đó, cột Hành động cuối bảng chỉ còn Tiếp nhận + Yêu cầu bổ sung thông tin (bỏ Xem, bỏ Từ chối và Hủy yêu cầu — 2 hành động phủ quyết chỉ đặt ở màn chi tiết), `fixed-layout` 19 cột đủ `width` = `minWidth`, lần đầu có cấu hình cột + popup chọn trường xuất file, `loadSeq`, `$safeLoading*`. Bỏ hẳn 3 cột (Người tiếp nhận YC · Mã GP · PM làm GP) và ô lọc `receiver_by` vì rỗng theo ĐỊNH NGHĨA của màn — `receive_id` chỉ ghi từ trạng thái Đã tiếp nhận trở đi. Spec: docs/superpowers/specs/gop-db/2026-09-08-request-solution-pending-list-page-standard-design.md

- issue-list-page-standard — chuẩn hoá màn Quản lý Issue (`/assign/issues`) theo skill `list-page` → @khoipv → .plans/gop-db/issue-list-page-standard/plan.md
  Hoàn thành: 2026-09-10 — user xác nhận đã xong (code + kiểm chứng API/compile 2026-09-08). BE 6 file · FE 1 file, không migration, không quyền mới. Sửa 3 lỗi có sẵn: `IssueService::index()` đẩy thẳng `$request->sort_field` vào `orderBy()` — gõ tay tên cột lạ trên thanh địa chỉ là 500, nay có `SORTABLE_COLUMNS` 5 khoá + chốt `orderByDesc('issues.id')`; bản đồ nhãn "Loại issue"/"Nguồn phát hiện" viết lại ở FE thiếu 3 giá trị nên issue mang giá trị đó in ra mã thô (nay dùng chung `DetailIssueResource::ENUM_MAPS` đổi `private` → `public`); `creator.info` + `employee_update.info` không eager load → N+1 ngay trên câu danh sách. Thêm `issue_type_text`/`detected_from_text`/`due_status_text` + màu/`tags_text` ở Resource, `creator_name` đọc đúng quan hệ mà bộ lọc dùng, ô tìm nhanh thêm người tạo bằng `EXISTS`, `Issue::STATUS_DATA` sửa 4 mã màu về bảng 9 màu chuẩn, registry `issues` 25 cột + export chuyển từ `IssueExport` (.xls cột cứng) sang `DynamicExport`. FE: `V2BaseSmartFilterPanel` 13 mục (thêm ô Loại issue mà BE nhận `issue_type` từ lâu), tách cột gộp "Mã-Tên issue" và gỡ 5 nút thao tác khỏi ô Mã, cột Hành động cuối bảng (Sửa · Xóa + `⋮` Xử lý · Lịch sử), thêm 6 cột gồm cả Ngày tạo (cột bắt buộc trước không có), `fixed-layout` 25 cột đủ `width` = `minWidth`, lần đầu có popup chọn trường xuất file, `columnCustomizationMixin`, `loadSeq` + `suppressFilterWatch` (4 nút lọc nhanh trước bắn 2 request mỗi lần bấm), `$safeLoading*`. ⚠️ Bảng `issues` RỖNG trên DB dev → kiểm chứng bằng issue giả trong transaction rồi rollback. Spec: docs/superpowers/specs/gop-db/2026-09-08-issue-list-page-standard-design.md

- finance-addition-accounting-request — sửa màn Phiếu yêu cầu hạch toán bổ sung theo yêu cầu user (Phase 11) → @khoipv → .plans/gop-db/finance-addition-accounting-request/plan.md
  Hoàn thành: 2026-09-10 — user xác nhận đã xong (code + smoke test API 18/18 pass 2026-09-07). BE 5 file · FE 5 file, không migration, không quyền mới. Yêu cầu user: màn Tạo bỏ 2 ô "Người tạo"/"Phòng ban" — người lập chuyển sang góc phải header card "Thông tin chung" dạng `Người lập - Ngày lập` như ERP; dropdown Loại yêu cầu đủ 7 loại chọn được y hệt ERP (`EDITABLE_TYPES` nay gồm cả loại 7, và ERP cũng không có nhánh form riêng cho loại này). Lòi ra 2 lỗi nặng ngoài yêu cầu ban đầu: 2 FormRequest dùng `$this->get()` mà FE gửi JSON body → `type`/`object_type`/`status` luôn null nên rule rẽ theo loại KHÔNG BAO GIỜ chạy — loại 2/6 (1.894/1.937 phiếu) không lập nổi vì bị đòi `money` + `note` là 2 trường màn hình không có, và từ chối không cần nhập lý do; vá xong thì nhánh lưu nháp lần đầu được chạy, lộ tiếp `exchange_rate` là cột NOT NULL → lưu nháp bỏ trống tỷ giá là 500. ⚠️ Hệ quả đã biết của loại 7 nhập tay (giống hệt ERP): 3 bảng riêng của loại 7 rỗng nên màn Chi tiết/In vẫn rẽ sang layout Phối hợp kinh doanh, phiếu không có phòng hỗ trợ nên người chỉ có quyền xem cấp công ty không thấy nó trong danh sách và 2 nút Từ chối / Lập phiếu kế toán không hiện. Còn nợ: rà nốt 18 FormRequest khác cùng lỗi `$this->get()` (Finance 7 · CustomerCare 7 · Payroll 4). Spec: docs/superpowers/specs/gop-db/2026-08-25-finance-addition-accounting-request-design.md

- handover-receiving-list-page-standard — chuẩn hoá màn Phiếu bàn giao chờ tiếp nhận (`/assign/handover/receiving`) theo skill `list-page` → @khoipv → .plans/gop-db/handover-receiving-list-page-standard/plan.md
  Hoàn thành: 2026-09-10 — user xác nhận đã xong (code + kiểm chứng API/compile 2026-09-07). BE 4 file sửa + 1 file mới (`ReceivingHandoverResource.php`) · FE 1 file, không migration, không quyền mới. Lỗi gốc: đơn vị dòng sai nên phân trang hỏng — màn hiển thị theo PHIẾU nhưng API trả từng CÔNG VIỆC đã phân trang rồi FE gom `handover_id` bằng JS, hệ quả là số dòng mỗi trang không đều, cột "Số công việc" chỉ đếm phần việc rơi vào trang đó, 1 phiếu hiện lại ở trang sau với con số khác, `meta.total` và ô "Tổng" sai theo 2 kiểu, và con số đếm không phân biệt người nhận; nay `HandoverService::receivingHandovers()` trả thẳng `Handover` + 4 `withCount` dùng lại đúng closure lọc → `my_total_items`/`my_accepted_items`/`my_rejected_items`/`my_pending_items` (`Handover::items()` không có điều kiện `receiver_id`, quên là đếm cả việc của người khác). 2 lỗi khác: nút Xuất Excel là nút chết (nay có route + `receivingExport()` + registry `handover_receiving` 15 cột) và ô lọc Giải pháp bị `disabled` cứng. Thêm whitelist sắp xếp 7 khoá + chốt `id desc`, ô tìm nhanh thêm mã phiếu. FE: bỏ đoạn gom `handover_id` bằng JS, `V2BaseSmartFilterPanel` 6 mục, Mã phiếu đổi sang `nuxt-link` và gỡ nút thao tác khỏi ô đó, cột Hành động cuối bảng (Tiếp nhận + Lịch sử), thêm 4 cột, nhãn ô đếm ghi rõ "Công việc của tôi", `fixed-layout` 14 cột đủ `width` = `minWidth`, lần đầu có cấu hình cột / giữ bộ lọc / sắp xếp cột, ô "Tổng" lấy `pagination.total`. ⚠️ Dùng Resource riêng chứ không đụng `HandoverResource` của 2 màn kia vì ngữ nghĩa đếm khác; 2 bảng `handovers` + `handover_items` RỖNG trên DB dev → kiểm chứng bằng dữ liệu giả trong transaction rồi rollback. Spec: docs/superpowers/specs/gop-db/2026-09-07-handover-receiving-list-page-standard-design.md

- handover-list-page-standard — chuẩn hoá màn Danh sách phiếu bàn giao (`/assign/handover`) theo skill `list-page` → @khoipv → .plans/gop-db/handover-list-page-standard/plan.md
  Hoàn thành: 2026-09-10 — user xác nhận đã xong (code + kiểm chứng API/compile 2026-09-07). BE 6 file · FE 1 file sửa + 1 file mới (`HandoverHistoryModal.vue`), không migration, không quyền mới. Sửa 3 lỗi có sẵn: `handleFilterChange(filters)` nhận sai kiểu payload nên mỗi lần đổi ô lọc lại nhét 2 khoá rác `key`/`value` vào filters và gửi lên API trong khi ô lọc thật không được gán giá trị; `HandoverService::index()` sắp xếp bằng chuỗi nhận thẳng từ URL, không whitelist, không chốt `id desc` (nay 13 khoá); ô lọc Bộ phận ghi vào `part_id` mà bảng `handovers` không có cột đó → ô lọc chết, đã tắt. BE thêm: màu Từ chối `#B91C1C` → `#DC2626` (giữ "Đã duyệt" `#2563EB` vì duyệt xong phiếu mới BẮT ĐẦU giao/nhận việc), chuyển nguyên điều kiện Sửa/Xóa từ FE về BE thành `isCanEdit()`/`isCanDelete()`, Resource thêm `updated_by_name` + 2 cờ quyền + 4 mốc thời gian bỏ giây, bổ sung eager load, và route + `export()` + registry `handovers` 19 cột — màn này trước giờ không có xuất Excel. FE: `V2BaseSmartFilterPanel` 5 mục, tách ô gộp "Mã phiếu • Nhân viên BG" thành 4 cột, cột Hành động cuối bảng (Sửa · Xóa + Lịch sử trong `⋮`, bỏ Xem) với popup `HandoverHistoryModal` bọc `SystemInfoSection` dùng chung với màn chi tiết, thêm 5 cột, `fixed-layout` 18 cột đủ `width` = `minWidth`, lần đầu có cấu hình cột hiển thị / xuất Excel / giữ bộ lọc, nút toolbar chuyển sang slot `actions` (slot `toolbar` thay cả khối tiêu đề nên màn đang mất tiêu đề). ⚠️ Sửa `HandoverResource` dùng chung nên 2 màn `/assign/handover/pending` + `/receiving` hưởng lây khoá mới và ngày bỏ giây; bảng `handovers` RỖNG trên DB dev → kiểm chứng bằng 5 phiếu giả trong transaction rồi rollback. Spec: docs/superpowers/specs/gop-db/2026-09-07-handover-list-page-standard-design.md

- assign-list-page-standard (loạt 15 màn) — chuẩn hoá danh sách `assign/*` theo skill `list-page` → @khoipv → .plans/gop-db/<màn>-list-page-standard/plan.md (solution, industry-group, application, customer-scope, meeting-type, survey-question, attachment-type, internal-business-scope, solution-group, customer-scope-group, project-item, project-role, form-template, reason-project-failure, discount-type)
  Hoàn thành: 2026-09-05 — user xác nhận đã xong. FE theo skill đầy đủ + BE mức tối thiểu (whitelist sort, tên người tạo/cập nhật bằng subquery, popup chọn trường xuất file qua `ExportColumnRegistry` + `DynamicExport`); hành động dòng = Sửa + Xóa là 2 nút chính, còn lại vào `⋮`; cố ý KHÔNG làm "Lịch sử thay đổi" và cấu hình cột mặc định hiện HẾT cột (2 ngoại lệ user chốt so với skill); bề rộng cột theo mục 15b, bảng bật `fixed-layout`. Không migration, không quyền mới. Sửa luôn loạt lỗi CÓ SẴN gặp dọc đường: `scopes` vs `hrm_scopes` ở màn nhóm ngành (500 ở Create/Edit/lọc, cả local lẫn dev) và `InternalBusinessScope::isCanLockUpdate()` cùng họ; thiếu cờ `is_can_delete`/`is_can_edit`/`is_can_lock_update` ở vài Resource; `ignoredFields` khai cả trong `data` lẫn `computed` (Vue 2 che computed); cột chết "Dùng ở dự án" ở màn vai trò dự án; 2 lỗi N+1 ở `FormTemplatesResource` (`whenLoaded()` trả object nên LUÔN truthy → nạp lười cả cây section từng dòng; `questions_count` đếm bằng cách nạp hết câu hỏi) — 4 query/dòng về 0; `ReasonProjectFailureResource` 43 query về 7; `DiscountTypeResource` cùng lỗi đó, ảnh hưởng cả `getAll` của dropdown báo giá; màn Loại giảm giá chưa từng có Xuất Excel nên thêm mới route + controller export; `$refs...?.loadData?.()` và id modal sai tên ở 2 màn (popup không mở, im lặng). Kiểm chứng mỗi màn: compile SFC + AST đối chiếu định danh template, cột bảng ↔ trường xuất FE ↔ registry BE, mọi cột đủ `width` + `minWidth`, smoke test API (index/sort/keyword/export).

- project-phase-list-page-standard — chuẩn hoá màn Danh sách giai đoạn dự án theo skill `list-page` → @khoipv → .plans/gop-db/project-phase-list-page-standard/plan.md
  Hoàn thành: 2026-09-05 — user xác nhận đã xong; làm theo khuôn 2 màn user chỉ định (nhóm ngành + ứng dụng), BE 6 file sửa · FE 1 file viết lại, không migration. BE: whitelist sort 4 cột; subquery người tạo/cập nhật; tìm nhanh thêm người tạo (EXISTS); thêm lọc Mã/Tên/Mức độ ưu tiên; `status_text` + ngày `d/m/Y H:i`; `is_can_delete` tính từ subquery đếm (bỏ 1 query/dòng); export chuyển sang `DynamicExport` (`.xls` → `.xlsx`, cột động) và nới quyền route export cho người chỉ có quyền xem. FE: `V2BaseSmartFilterPanel` 8 ô; tách cột Mã (link mở modal Xem) / Tên; cột Hành động cuối bảng với `V2BaseRowActions` (bỏ "Xem", Khoá/Mở khoá rời khỏi ô Trạng thái); `V2BaseBadge`; 4 cột Người tạo/Ngày tạo/Người cập nhật/Ngày cập nhật; cấu hình cột + nhớ bộ lọc + popup chọn trường xuất file; `fixed-layout` đủ 12 cột; gỡ code chọn nhiều dòng. Cố ý bỏ hành động Lịch sử (module Assign chưa có `LogsCatalogHistory`, giống 2 màn mẫu). Kiểm chứng: compile + AST, smoke test API, đọc lại file xuất, đối chiếu cột bảng ↔ file ↔ registry 10 = 10.

- borrow-export-request — Yêu cầu xuất hàng mượn, port ERP `borrow_export_requests` → HRM → @khoipv → .plans/gop-db/borrow-export-request/design.md · plan.md
  Hoàn thành: 2026-09-05 — user xác nhận đã xong (code + test Playwright toàn luồng 2026-09-04). BE 12 file mới + 4 file sửa · FE 7 file mới + 2 file sửa (menu) · 0 bảng mới · KHÔNG migration · 3 QUYỀN MỚI guard `api` id 1565-1567 (trùng tên quyền ERP guard `web` 100890-100892). User chốt: port đầy đủ như ERP; nút "Tạo phiếu xuất hàng mượn" báo "chưa triển khai" (màn `borrow_exports` chưa port); chỉ 2 mục menu — bỏ mục `Chờ duyệt → Hàng mượn` của ERP, người duyệt lọc bằng ô Trạng thái (preset `for-approve` giữ chạy cho link cũ). Tách `BorrowStockService` dùng chung để tính "Đang mượn" cho 3 luồng tranh cùng lượng hàng (port `ProductExportRequestDetail::getReturningQty()` mà HRM chưa từng có). ⚠️ Sửa CÓ CHỦ Ý 3 chỗ so với ERP: màu trạng thái (nháp xám / chờ duyệt vàng thay vì đỏ hết); bỏ dòng ép cứng `company_id` cuối `searchByFilter()` (nó triệt tiêu quyền "tổng công ty"); `canView()` cộng 3 nhánh quyền cấp (ERP cho trưởng phòng thấy phiếu ở danh sách nhưng bấm vào ra `not_found`). ⚠️ Khối File đính kèm dùng LẠI `AttachmentSection.vue` của màn Đề nghị thanh toán — component chung được thêm 3 prop (`apiBase`/`allowedExtensions`/`maxSizeMb`) với mặc định đúng giá trị cũ nên màn Đề nghị thanh toán không đổi hành vi. Kiểm chứng trên dữ liệu thật: 11 endpoint (10× 200, 1× 422 đúng nghiệp vụ); phạm vi danh sách ↔ `canView()` khớp 100% trên 60 nhân viên; vòng đời ghi 7/7 chạy trong transaction rồi rollback sạch; bản in lấy letterhead theo `company_id` trên phiếu; `export-request-data` không lộ giá vốn. Playwright bấm thật tìm và sửa 4 lỗi: sort "Ngày duyệt" chết do FE gửi `approved_time` còn BE khai `approvedTime`; tiêu đề tab hiện nguyên thẻ HTML của badge; tên người lập trống ở màn Tạo (sai khoá store, đúng là `current_employee_info.fullname`); toast lỗi upload ra tiếng Anh (câu tiếng Việt nằm trong `errors`, không phải `message`). Vòng đời ghi chạy thật rồi dọn sạch, DB về đúng 292 phiếu / 686 dòng / 990 chi tiết. Chưa kiểm chứng được: đổi ĐVT khi hàng có nhiều đơn vị (dữ liệu thật chỉ 1 ĐVT/hàng) và bản in trên máy in thật. Còn nợ 2 việc chờ user quyết: `ProductExportRequest::dataForBorrowReturn()` của màn Yêu cầu nhập hàng thiếu phép trừ `returning_qty` so với ERP (đề xuất trả nhiều hơn số thực còn mượn); gộp 3 bản chép `manageableDepartmentIds()` ở nhóm Prepick về trait dùng chung (đã đưa lên trait, chưa gỡ bản cũ). Spec: docs/superpowers/specs/gop-db/2026-09-04-borrow-export-request-design.md

- finance-bill-payment-authorization — bộ tài liệu bàn giao (SRS + testcase + HDSD) màn Phiếu ủy nhiệm chi → @khoipv → .plans/gop-db/finance-bill-payment-authorization/plan.md (mục "Phase T")
  Hoàn thành: 2026-09-05 — sinh 3 tài liệu cùng thư mục feature, kèm 3 generator `gen_srs.py`/`gen_testcase.py`/`gen_hdsd.py` commit cùng chỗ để tái sinh: `SRS - Phiếu ủy nhiệm chi.docx` (form chuẩn 2026-08-28, 4 chương, 11 chức năng FR-01…FR-11, 38 bảng, 23 ảnh, 43 trang), `testcase.xlsx` (149 TC, P0 63%, 20 TC phân quyền + 10 section La Mã, bộ kiểm tra thuật ngữ sạch), `HDSD_Phiếu ủy nhiệm chi.docx` (13 Heading 1, 13 bảng, 23 ảnh, 38 trang, có mục hướng dẫn riêng cho từng quyền). 25 ảnh thật ở `unc_shots/` chỉ để local, KHÔNG commit; chụp bằng tài khoản DNS Admin trên cổng dev, chỉ mở form/hộp thoại rồi Hủy nên không ghi dữ liệu.

- finance-prepick-extend-request — port màn **Yêu cầu gia hạn hàng giữ** (ERP → HRM `/finance/prepick-extend-requests`) → @junfoke → .plans/gop-db/finance-prepick-extend-request/design.md · plan.md
  Hoàn thành: 2026-09-04 — user test tay 2026-08-24 ("tạm ổn"), Phase 10 vá QA redmine 11276/11277/11278/11296 xong 2026-09-04. Nhánh riêng `feat/finance-prepick-extend-request` (cả 2 repo, tách từ `gop_db`); dùng chung bảng ERP, **chỉ 1 migration thêm bảng lịch sử của HRM** (`2026_08_22_000001_create_prepick_extend_request_history_table`, đã chạy), **không tạo quyền mới** (đọc qua `ChecksEmployeePermission`). Đủ luồng: danh sách, form thêm/sửa, chi tiết + duyệt 3 cấp TP → BGĐ → KT, lịch sử, in (khổ ngang theo user chốt), xuất Excel, đính kèm theo mẫu `BillPaymentAttachmentService` (S3 `prepick_extend_request`, ≤ 13 MB). Playwright chạy thật luồng Lưu nháp → Gửi duyệt → TP duyệt → (BGĐ) → KT duyệt, đối chiếu `prepick_details` + `prepick_logs` trước/sau bằng SQL; 6 lệnh grep tự kiểm của skill sạch. QA: **11276** cột "Cần gia hạn" mặc định = số ĐANG GIỮ (ERP làm việc này trong class JS nên nhìn DB thấy 0 mà màn ERP vẫn hiện số); **11277** lịch chọn "Hạn giữ mới" mất cột Chủ nhật — gốc ở component dùng chung `V2BaseDatePicker` ghim `left` không kẹp mép phải màn hình, đã kẹp trong `[8px, innerWidth - popupWidth - 8px]` (⚠️ sửa file dùng chung); **11278** thêm nút Sửa/Xóa cho phiếu nháp ở màn Chi tiết. 📏 Phần "giá trị vượt ngưỡng" của 11278 **KHÔNG PHẢI LỖI — tester báo nhầm**: đối chiếu code ERP thì ERP cũng không chặn tạo phiếu vượt ngưỡng (ngưỡng tiền chỉ dùng để RẼ NHÁNH DUYỆT) và cũng không cho TP/BGĐ/KT sửa số lượng lúc duyệt; chạy thật `needBoardApproveByLines()` trên `gop_db` cho đúng kết quả — lô của tài khoản test toàn hàng giá 1đ nên tester không dựng được dữ liệu đủ tiền. Tồn: soát nốt checklist A→H của skill và xoá 4 bảng `bak_*_20260822`. Spec: docs/superpowers/specs/gop-db/2026-08-22-finance-prepick-extend-request-design.md

- finance-addition-accounting-request (port gốc) — port màn ERP **Phiếu yêu cầu hạch toán bổ sung** sang phân hệ Tài chính, route `/finance/addition-accounting-requests` → @khoipv → .plans/gop-db/finance-addition-accounting-request/plan.md
  Hoàn thành: 2026-08-26 — user xác nhận xong. 6 loại tạo mới + loại 7 chỉ xem/in, dừng ở *Chờ duyệt*. BE 17 file mới · FE 10 file mới · 24 route · **4 quyền id 1177–1180** · **0 migration** (dùng chung 5 bảng ERP). Vá **10 lỗi/lỗ hổng của ERP** — nặng nhất: route xoá là **GET** không gate, `store()` gán thẳng `status` — cùng 7 lỗi FE chỉ Playwright bắt được. (Đợt sửa theo yêu cầu user sau đó là mục Phase 11 hoàn thành 2026-09-10 ở trên.) Spec: docs/superpowers/specs/gop-db/2026-08-25-finance-addition-accounting-request-design.md

- catalog-docs (loạt 10 màn danh mục) — bộ tài liệu SRS + HDSD + Testcase cho 6 màn Địa lý · 3 màn Tài chính · 1 màn Công việc-lỗi thiết bị → @junfoke → .plans/gop-db/geo-catalogs-docs/plan.md · finance-catalogs-docs/plan.md · device-error-catalog-docs/plan.md
  Hoàn thành: 2026-08-20 — user chốt phạm vi 2026-08-17, giao **30 file = 10 SRS + 10 HDSD + 10 testcase, tổng 587 TC** (Địa lý 327 · Tài chính 147 · Lỗi thiết bị 113), kèm generator `gen_srs.py`/`gen_testcase.py`/`gen_hdsd.py` + file cấu hình commit cùng thư mục để tái sinh. ⚠️ **Phát hiện phải nêu trong tài liệu: 6 màn địa lý (`/human/nations` · `areas` · `provinces` · `districts` · `wards` · `hamlets`) KHÔNG gắn quyền ở bất kỳ endpoint nào** — kể cả Thêm/Sửa/Xóa/Khóa, ai đăng nhập cũng sửa được danh mục dùng chung toàn hệ thống; ngược lại 3 màn Tài chính (`works` · `cost-debts` · `source-capitals`) mỗi màn đúng 1 quyền cho cả xem lẫn sửa. Nghiệp vụ đáng nhớ của màn lỗi thiết bị: **trùng tên xét theo TỪNG LOẠI** (6 loại) nên đổi ô Loại khi sửa sẽ kiểm tra lại trùng tên trong loại mới; nút Xóa cần CẢ HAI điều kiện đang Hoạt động VÀ chưa phát sinh chứng từ; 4 ô để trống thì hệ thống tự điền, trong đó 2 ô lấy theo cấu hình công ty nên **hai người ở hai công ty khác nhau ra kết quả tính khác nhau** — đúng thiết kế. ⚠️ Lúc chụp ảnh, bảng `catalog_histories` chưa migrate trên local nên cửa sổ Lịch sử phải chụp ở cổng dev.

- dong-bo-quy-tac-chung — đồng bộ bộ quy tắc chung (đã chốt ở màn Khách hàng) sang **20 màn danh mục** → @dnsnamdang → .plans/gop-db/dong-bo-quy-tac-chung/plan.md
  Hoàn thành: 2026-08-17 — bắt đầu 2026-08-15, user soi lại nhiều đợt và chốt bổ sung 3 lần giữa chừng. Áp 2 quy tắc nghiệp vụ (lọc "Loại hoạt động" của Lịch sử = 3 nhóm cố định; **bản ghi đã khoá không cho sửa/xoá — chặn ở BE bằng 423 qua middleware dùng chung**, FE ẩn nút + chặn vào thẳng URL `/edit`) và 15 quy tắc giao diện của skill `list-page`/`button-convention` cho: 6 màn CSKH (`device-errors`, `services`, `levels`, `note-maintenances`, `costs`, `service-price-config`, `serials`) · 6 màn địa lý · 3 màn tài chính + `banks`/`account-banks`/`product-transfer-requests`. Kèm 4 hạ tầng dùng chung mới: **lịch sử thay đổi cho 18 màn danh mục** (bảng `catalog_histories` + trait `LogsCatalogHistory` + `CatalogHistoryModal`), popup chuẩn hoá, **popup "Chọn trường xuất file" cho 10 màn có nút Xuất**, và bộ lọc "Người thực hiện" trong lịch sử. 🐞 Lỗi gốc đáng nhớ tìm ra khi user báo "cột Người cập nhật vẫn trống": `Nation` kế thừa `Model` THUẦN nên không có hook audit → `nations.updated_by` luôn NULL; còn `Area`/`Province`/`Ward` giữ 2 hook đồng bộ ERP thời chưa gộp DB — sau khi gộp, `TpArea` trỏ về CHÍNH bảng `areas` nên hook ghi đè và đóng dấu `updated_by` bằng **id bảng `employee_infos`** trong khi cột lưu `employees.id` → join ra rỗng. Đã gỡ hẳn 3 hook + set tay `created_by`/`updated_by` trong `NationService`, đo lại bằng tinker. Có migration (bảng `catalog_histories` + 2 migration bổ sung người tạo cho danh mục tài chính). Đợt cuối rà lại 20/20 màn theo toàn bộ skill + xử lý phản hồi Redmine #11073 (ghi chú #12–#27).

- finance-bill-adjust-dept-request — Phiếu yêu cầu điều chỉnh công nợ → @khoipv → .plans/gop-db/finance-bill-adjust-dept-request/plan.md
  Hoàn thành: 2026-09-03 — user nghiệm thu đã xong (18 phase gốc xác nhận 2026-08-24; mở lại 2026-09-03 fix 4 việc, 2 FE + 2 BE, không migration). Phase 20: đổi khách hàng/NCC ở một dòng phải XOÁ hợp đồng cũ — ERP xoá ở 4 chỗ (`BillAdjustDeptRequestDetail`/`DetailItem` × `chooseCustomer`/`chooseSupplier`), HRM thiếu hẳn nên phiếu lưu xuống DB là cặp "KH A + hợp đồng của KH B", `contractable_id` trỏ sai, bước tạo phiếu kế toán ghi sổ nhầm công nợ (lỗi dữ liệu, không phải hiển thị). Phase 21: lệch tổng tiền báo inline ở cột Số tiền bên "Điều chỉnh đến" (dòng cuối của nhóm) kèm số thiếu/thừa, trước chỉ 1 toast chung nên bảng nhiều nhóm không biết nhóm nào. Phase 22 + 22b + 22c: lỗi 422 của BE đổ về đúng từng ô (`details.1.items.0.customer_new_id` → ô Khách hàng dòng "đến" nhóm 1, viền đỏ); dịch câu lỗi `gt`/`integer`/`array`/`string`/`boolean` ngay trong Request (user chốt KHÔNG sửa `lang/vi/validation.php` dùng chung); toast rút về "Vui lòng kiểm tra dữ liệu nhập", chỉ lỗi không có chỗ inline (vd `status`) mới đọc nguyên văn. Phase 22d: Từ chối xong về màn danh sách — `changeStatus()` (dùng chung Gửi duyệt + Từ chối) thêm cờ `backToList`, Gửi duyệt vẫn `$router.go(0)`; popup lý do chỉ đóng khi thành công (trước lỗi cũng đóng, mất lý do vừa gõ). Kiểm chứng Playwright bấm Gửi duyệt thật: 422 hiện đúng ô, 2 ô Số tiền báo "Phải lớn hơn 0", 4 ca toast ra câu chung, nhóm khớp tiền không báo gì. Chưa kiểm chứng: phiếu NCC ngoại tệ (16 cột) · màn sửa phiếu có dữ liệu thật. Còn nợ: Excel phiếu lệch ERP · nút "Chọn nhanh hợp đồng" · SRS/testcase/HDSD · dọn 6 phiếu `TEST.DNDCCN.*` · `lang/vi/validation.php` còn ~52 khoá tiếng Anh. ⚠️ Bài học: lượt đầu user báo "vẫn chưa được" là do HMR Nuxt 2 giữ component cũ, code đã đúng — sửa FE mà trình duyệt không đổi thì Ctrl+Shift+R trước khi nghi code. Spec: docs/superpowers/specs/gop-db/2026-08-17-finance-bill-adjust-dept-request-design.md

- finance-bill-income-report — bộ tài liệu bàn giao (SRS + HDSD + testcase) → @khoipv → .plans/gop-db/finance-bill-income-report/plan.md (mục "Phase T")
  Hoàn thành: 2026-09-05 — sinh 3 tài liệu cho màn Phiếu báo có + màn phụ Tổng hợp tiền về ngân hàng, kèm 3 generator commit cùng chỗ: `SRS - Phieu bao co.docx` (form 2026-08-28, 4 phần, 16 chức năng FR-01…FR-16, 14 quy tắc nghiệp vụ, 58 trang), `HDSD_Phieu_bao_co.docx` (8 phần + TỔNG QUAN, click-by-click từng trường + giá trị điền sẵn + mục hướng dẫn theo từng quyền, 44 trang), `testcase.xlsx` (204 TC, P0 54%, 13 section La Mã + 13 TC phân quyền gồm 5 TC gọi thẳng chức năng bỏ qua giao diện). Ảnh chụp thật 27 tấm trong `bir_shots/` — KHÔNG commit. ⚠️ Cổng dev hrm-crm thiếu 3 chunk giao diện nên không mở được màn Tạo/Sửa/Chi tiết; ảnh form + popup + chi tiết + màn tổng hợp phải chụp trên bản chạy local (cùng DB gộp). Cấu hình cột của tài khoản DNS Admin đã đưa về mặc định để ảnh đúng chuẩn.

- finance-bill-income-report — sửa lỗi màn Phiếu báo có (Phase F) → @khoipv → .plans/gop-db/finance-bill-income-report/plan.md (mục "Phase F")
  Hoàn thành: 2026-09-03 — user xác nhận đã xong. 9 việc báo trong 1 phiên: tách cột Số tài khoản / Tên tài khoản ở bảng chi tiết (trước đó cả 2 cột đều in "số - tên"); nút Duyệt màn chi tiết về teal #1abc9c; nút thứ 2 của form đổi nhãn "Lưu và duyệt" (cờ `save_and_approve`, trước khai nhầm `save_and_submit_approve`); toast mở phiếu đã bị xóa ở tab khác → "Không tìm thấy dữ liệu" (chỉ với 404); dựng lại file mẫu import (viền, tiêu đề teal, ngày dd/mm/yyyy, ô tiền `#,##0`); nút Quay lại màn Điều chỉnh công nợ về đúng phiếu qua `?back_url=`. 3 lỗi validate: cột Số tiền chưa bao giờ báo bắt buộc (`min:0` + FE quy ô rỗng thành 0 → đổi `gt:0`, dữ liệu thật 10.207 dòng không có dòng nào money=0); ô Diễn giải đầu phiếu thiếu `:invalid` + `<V2BaseError>` nên chỉ ra toast chung → nối lỗi inline; nới trần Diễn giải 255 → 500 ký tự cả 2 ô. CÓ MIGRATION `2026_09_03_000001_widen_note_on_bill_income_reports_table` (đã chạy, 0 dòng ảnh hưởng); cột chi tiết là TEXT nên chỉ thêm rule. ⚠️ Bảng dùng chung 2 cổng — diễn giải > 255 ký tự hiện nguyên vẹn bên ERP, chưa rà bố cục màn/bản in ERP.

- ⚠️ base-confirm-modal — sửa COMPONENT DÙNG CHUNG, cả team cần biết → @khoipv → components/modal/base-confirm-modal.vue
  Hoàn thành: 2026-09-03 — user chốt sửa ở component chung thay vì vá từng màn. Popup xác nhận tự bật `danger` (nút đỏ + icon cảnh báo) khi `text-accept` bắt đầu bằng "Xóa"/"Xoá", trừ "Xóa trắng"; prop `danger` đổi mặc định false → null (chưa chỉ định) nên màn nào truyền thẳng `:danger` vẫn được tôn trọng. Lý do: ~101 chỗ hỏi xóa qua popup này quên truyền `danger`. Đã chạy hàm suy luận trên toàn bộ `text-accept` đang có: chỉ nhóm "Xóa" đổi màu, Khóa/Mở khóa/Duyệt/Xác nhận/Xóa trắng giữ nguyên.

- finance-bill-payment-request — nới validate Lưu nháp → @khoipv → .plans/gop-db/finance-bill-payment-request/plan.md (mục "Nới validate LƯU NHÁP")
  Hoàn thành: 2026-09-03 — user xác nhận đã xong. Lưu nháp (`status = 1`) chỉ còn bắt buộc Loại chi; bỏ `required` của lý do chi, hình thức TT, tiền tệ, tỷ giá, ngày chốt, đối tượng nhận tiền và toàn bộ `details.*`, rule định dạng giữ nguyên. Sửa BE 2 file (`BillPaymentRequestStoreRequest` — Update kế thừa; `BillPaymentRequestService::masterPayload()`), FE không đụng vì mọi thông báo "Bắt buộc nhập" đều do BE trả. Không migration. Quyết định này THAY ràng buộc 2026-08-22 (dòng chi tiết đã thêm phải đủ hợp đồng + số tiền). Nút Lưu và gửi duyệt (`status = 2`) không đổi. ⚠️ 4 cột `reason`/`type_payment`/`type_money_id`/`exchange_rate` NOT NULL không default → service phải đổ mặc định (TM · VNĐ · tỷ giá 1 · lý do rỗng), thiếu là lưu nháp trả 500.

- finance-bill-payment-authorization — lịch sử thay đổi màn Ủy nhiệm chi (Phase L) → @khoipv → .plans/gop-db/finance-bill-payment-authorization/plan.md (mục "Phase L")
  Hoàn thành: 2026-09-03 — VERIFIED Playwright. Màn này trước đó CHƯA có gì (không nằm trong whitelist, BE chỉ ghi log cho màn Đề nghị, FE trống) → bổ sung đầy đủ như 2 màn phiếu trước, dùng bảng chung `catalog_histories` + trait `LogsCatalogHistory`, FE `CatalogHistoryModal` + `SystemInfoSection`. Không quyền riêng, không migration. Khác 2 màn kia: UNC không có Gửi duyệt / Duyệt / Hủy (RULING U-UNC-6) — chỉ Lưu (status 1) và Lưu và duyệt (status 3) nên dòng `change_status` chỉ sinh ở `update()`; bảng không có cột tổng; dòng chi tiết nhận diện bằng hợp đồng / nhân viên, không có khách hàng - NCC.

- finance-bill-payment — lịch sử thay đổi màn Phiếu chi tiền (Phase L) → @khoipv → .plans/gop-db/finance-bill-payment/plan.md (mục "Phase L")
  Hoàn thành: 2026-09-03 — VERIFIED Playwright. Trước đó chỉ log đổi trạng thái; nay đầy đủ: tạo / sửa / bảng chi tiết theo từng dòng / duyệt kèm số chi / hủy kèm lý do / xóa. Không migration. ⚠️ Điểm rủi ro đã kiểm: `BillPaymentDetailResource` ĐỌC NGƯỢC `catalog_histories` (bảng `bill_payments` không có cột `note`) để dựng `cancel_reason` / `cancel_note` / `approve_note` — đã chụp baseline 2 dòng log thật trước/sau khi sửa whitelist, diff rỗng.

- finance-bill-income — lịch sử thay đổi màn Phiếu thu tiền (Phase L) → @khoipv → .plans/gop-db/finance-bill-income/plan.md (mục "Phase L")
  Hoàn thành: 2026-09-03 — VERIFIED Playwright. Làm theo skill `entity-history` §5.1 + màn danh sách khách hàng, phạm vi ĐẦY ĐỦ như màn Phiếu báo có (không theo bản rút gọn của Phiếu chi tiền): tạo mới / thay đổi thông tin / bảng chi tiết theo từng dòng / duyệt kèm số thực thu (tách 2 dòng log) / hủy kèm lý do / xóa. Không quyền riêng, không migration — bảng chung `catalog_histories` + trait `LogsCatalogHistory`, FE `CatalogHistoryModal` (popup màn danh sách) + `SystemInfoSection` (khối trong màn chi tiết).

- finance-bill-income-report — Phiếu báo có, port ERP `bill_income_report` → HRM → @khoipv → .plans/gop-db/finance-bill-income-report/design.md + plan.md
  Hoàn thành: 2026-09-03 — user xác nhận đã xong (nghiệm thu 2026-08-24, Phase 8 xong code 2026-08-28). Port `admin/income-expenditure/bill_income_report` sang phân hệ Tài chính, route `/finance/bill-income-reports` + `/summarize-money`. Phạm vi: danh sách; tạo/sửa/xóa nháp; duyệt kèm ghi bút toán sổ cái; chi tiết + cờ "Không báo tiền về"; 3 loại thu; Tổng hợp tiền về ngân hàng + xuất Excel chọn trường; Import Excel sao kê; Lịch sử thay đổi. KHÔNG thay đổi schema (lịch sử dùng bảng chung `catalog_histories`); 3 quyền mới id 1539-1541 (guard `api`, tên trùng ERP). Bút toán HRM sinh khớp 100% bút toán ERP đã ghi (7 phiếu thật / 38 bút toán / 24 cột denormalize). Phase 8 sửa theo phản hồi, chỉ màn danh sách: "Ngày lập/Người lập" → "Ngày tạo/Người tạo"; "Diễn giải" → "Ghi chú" (cột + ô lọc, áp cả màn Tổng hợp tiền về ngân hàng); thêm cột Người cập nhật (BE trả `updated_by_name`) + Ngày cập nhật mặc định ẩn trong popup Cấu hình cột — 2 file BE + 2 file FE, không migration, không quyền mới. Spec: docs/superpowers/specs/gop-db/2026-08-24-finance-bill-income-report-design.md

- finance — sửa nhanh 3 màn Phiếu thu / Phiếu chi / Ủy nhiệm chi → @khoipv →
  `.plans/gop-db/finance-bill-income/plan.md` · `.plans/gop-db/finance-bill-payment/plan.md` ·
  `.plans/gop-db/finance-bill-payment-authorization/plan.md`
  Trạng thái: **HOÀN THÀNH — user xác nhận xong** (2026-08-28). Commit `gop_db`: client `5e4d559` · api `d00a4c0`.
  Icon nút Duyệt 2 màn danh sách về `ri-checkbox-circle-line` · Ủy nhiệm chi: mặc định Loại chi
  "Chi trả nhà cung cấp", Lưu nháp chỉ bắt buộc Loại chi (nới RULING U-UNC-3) · Phiếu thu: bỏ popup
  duyệt, "Số tiền thực thu" vào bảng chi tiết màn xem, duyệt không ghi đè `sum_money` (hết lệch cột
  "Số tiền" so ERP, không nắn dữ liệu cũ) · Phiếu chi màn Tạo bám lại ERP: Số phiếu đề nghị lên đầu,
  xếp lại 10 trường, Loại chi 5 → 7, thêm 3 khối chỉ đọc (Đối tượng nhận tiền / Tài khoản nhận tiền /
  Ngân hàng trung gian). Không migration. Màn Đề nghị thanh toán: user chốt KHÔNG sửa.

- finance-bill-payment-request → @khoipv → .plans/gop-db/finance-bill-payment-request/plan.md
  Trạng thái: **HOÀN THÀNH — user xác nhận xong** (2026-08-26).
  Phase 11 sửa xuất Excel loại chi 12: `paidMoneyForDetail()` chọn `billable_type` theo dòng
  (hết lệch 254 ô / 70 phiếu; ăn sang màn chi tiết + màn in — 3 đầu ra 1 số) · ô tiền ghi **CHUỖI**
  kiểu VN qua `WithCustomValueBinder` (user chốt, đánh đổi: mất SUM/lọc/pivot) · letterhead nhúng
  `companies.header` theo `company_id` của phiếu + trải hết bề rộng bảng.
  BE 3 file + 1 blade · không migration · không đụng FE.
  📄 Bộ tài liệu bàn giao (Phase 15 — 2026-08-28): `testcase - Phiếu đề nghị thanh toán.xlsx`
  (191 TC) · `HDSD_Phiếu đề nghị thanh toán.docx` (54 trang, 30 ảnh thật) ·
  `SRS - Phiếu đề nghị thanh toán.docx` (67 trang, FR-01…FR-15, BR-01…BR-18).
  3 generator kèm theo; ảnh nguồn `dntt_chi_shots/` chỉ để local, không commit.

- finance-bill-income-request → @khoipv → .plans/gop-db/finance-bill-income-request/plan.md
  Trạng thái: **HOÀN THÀNH — user xác nhận xong** (2026-08-26).
  Port màn ERP "Phiếu đề nghị thu tiền" (7 phase, xong 2026-08-14) + 6 đợt sửa sau nghiệm thu:
  cấu hình cột hiển thị + 2 cột Người/Ngày cập nhật · bỏ hẳn "Người nộp" (cột · ô lọc · bản in),
  đổi nhãn "Lý do nộp" → "Lý do thu" · popup Chọn khách hàng: SĐT khớp từ **đầu số**, ẩn dòng bị che
  SĐT (`hide_masked_mobile`), ô MST và ô SĐT lọc **độc lập** (`tax_code_only`, MST khớp đầu mã).
  ⚠️ Đánh đổi user đã chốt: gõ mảnh giữa/đuôi SĐT-MST **không ra kết quả** — phải gõ đủ số.
  Spec: docs/superpowers/specs/gop-db/2026-08-13-finance-bill-income-request-design.md
  📄 Bộ tài liệu bàn giao (Phase 14 — 2026-08-28): `testcase - Phiếu đề nghị thu tiền.xlsx`
  (156 TC) · `HDSD_Phiếu đề nghị thu tiền.docx` (40 trang, 25 ảnh thật) ·
  `SRS - Phiếu đề nghị thu tiền.docx` (50 trang, FR-01…FR-12, BR-01…BR-17).
  3 generator kèm theo; ảnh nguồn `dntt_shots/` chỉ để local, không commit.

- finance-3-man-sua-theo-phan-hoi (2026-08-22) → @khoipv → **HOÀN THÀNH — user xác nhận xong**.
  Plan: `finance-bill-income-request` (8.8-8.11) · `finance-bill-income` (K, L, M) ·
  `finance-bill-payment-request` (5 task phụ) — sửa theo phản hồi trên 3 màn đã nghiệm thu.
  **Lịch sử thay đổi** cho Đề nghị thu tiền + Đề nghị thanh toán (popup ⋮ + khối Lịch sử, ghi vào
  `catalog_histories`, không migration/permission mới); mở rộng `CatalogHistoryService` hỗ trợ khoá
  dạng BẢNG (diff `~ / - / +`) — thuần thêm, đã test hồi quy màn danh mục cũ.
  **Đề nghị thu tiền:** cột + ô lọc Người nộp, dòng Tổng cộng, mở 2 tab trả **409** thay vì báo thiếu
  quyền, bỏ nút Xem chi tiết. **Phiếu thu:** in/Excel lấy `bill_incomes.payer`, preview khớp bản in,
  mã phiếu đề nghị mở tab mới. **Đề nghị thanh toán:** Lưu nháp bỏ bắt buộc chi tiết/file/ngân hàng,
  loại chi 6+CK tự đổ ngân hàng người lập, loại chi 6 port nguồn hợp đồng `bonus-contracts`.
  Đụng 7 file `hrm-api` + 7 file `hrm-client`. Bước tiếp: commit lên `gop_db` (lúc nghiệm thu chưa commit).

- finance-bill-payment (Phiếu chi — logo bản in) → @khoipv → .plans/gop-db/finance-bill-payment/plan.md
  Trạng thái: **HOÀN THÀNH — user xác nhận xong** (2026-08-21).
  Áp cùng cách xử lý logo như Phiếu thu (dùng nguyên `companies.header`, lấy công ty theo
  `bill_payments.company_id`) → 162/1.305 phiếu hết in nhầm logo công ty khác.
  Sửa 1 file `BillPaymentPrintService.php`; `BillPaymentExport` đã có sẵn trait letterhead.

- finance-bill-income (Phiếu thu — logo bản in/Excel) → @khoipv → .plans/gop-db/finance-bill-income/plan.md
  Trạng thái: **HOÀN THÀNH — user xác nhận xong** (2026-08-21). Xong code + data local.
  Logo bản in/Excel phiếu thu chuyển sang dùng chung cách của màn Báo giá (dùng nguyên
  `companies.header`, chỉ ghép `ERP_URL` khi giá trị còn tương đối) và lấy công ty theo
  `bill_incomes.company_id` thay vì công ty người tạo → 133 phiếu `TPSG.*` hết mất logo,
  497 phiếu về đúng logo công ty trên phiếu. Sửa 1 file `BillIncomePrintService.php`.
  **Chuẩn hoá dữ liệu dùng chung**: 8 dòng `companies.header` + 8 dòng `companies.logo` trên
  `gop_db` local đổi từ `/uploads/...` sang `https://erp.eteksofts.com/uploads/...` — vì file ảnh
  nằm trên đĩa ERP, gộp DB không kéo file sang, mà domain HRM không phục vụ `/uploads` (404).
  Hưởng lợi cả màn Báo giá (đang mất logo trên `gop_db` vì lý do y hệt).
  ⚠️ **Dev/production chưa chạy 2 câu UPDATE** — rollback ở
  `.plans/gop-db/finance-bill-income/rollback-companies-header-logo.sql`.

- customer-permission-to-master-data → @khoipv → .plans/gop-db/customer-permission-to-master-data/plan.md
  Trạng thái: **HOÀN THÀNH — user xác nhận xong** (2026-08-21). Chuyển nhóm quyền khách hàng sang
  phân hệ **Danh mục chung** (11 quyền id 1517-1526 + giữ 167), chỉ sửa `PermissionsTableSeeder.php`.
  ⚠️ Seeder vẫn còn lỗi trùng id 1117/1118 (dòng ~1130) → phải bỏ 1 cặp mới seed được trên DB sạch.

- finance-bill-income + finance-bill-payment (xuất Excel) → @khoipv → .plans/gop-db/finance-bill-income/plan.md (F1-F5) · .plans/gop-db/finance-bill-payment/plan.md (G1-G6)
  Trạng thái: **HOÀN THÀNH — user xác nhận xong** (2026-08-21). Vá 3 lỗi file Excel (thiếu logo,
  cột hẹp, "number formatted as text") cho Phiếu thu + Phiếu chi, cả 3 bố cục 1/4/12: số thô +
  `data-format="#,##0"`, `WithColumnWidths`, trait `EmbedsCompanyLetterhead`.
  Quy tắc gói thành skill `.claude/skills/export-excel/SKILL.md` — **tài sản chung, cần PR**.

- finance-bill-payment-authorization → @khoipv → .plans/gop-db/finance-bill-payment-authorization/plan.md
  Trạng thái: **HOÀN THÀNH — user xác nhận xong** (2026-08-21). Port màn **Phiếu ủy nhiệm chi**
  (`/finance/bill-payment-authorizations`) — cặp song sinh chuyển khoản của Phiếu chi.
  BE 11 file mới + 3 sửa · FE 6 mới + 1 sửa menu · 2 quyền api 1515-1516 · không migration.
  Test Playwright 25/25 · replay sổ cái 62/63 · dọn dữ liệu test 8/8 chỉ số về baseline.
  🚨 **6 ruling cố ý giữ điểm hở (U-UNC-1…6)** — đọc §8 spec trước khi "sửa lỗi", nặng nhất là
  U-UNC-1 giữ nguyên lỗi cộng dồn của ERP (bút toán Có = tiền DÒNG CUỐI, lệch 111,3 tỷ / 433 phiếu).
  ⚠️ Có sửa file dùng chung `PaymentEmployeeTable.vue` (thêm prop `excludeFields`) và vá lỗi 403
  chọn đề nghị cho cả Phiếu chi lẫn Phiếu thu (2 endpoint mới gate bằng `isAccountant()`).
  📌 Còn lại: nhánh loại 4 + bảng phân bổ phiếu xuất hàng chưa có dữ liệu thật · SRS/testcase/HDSD.
  Spec: docs/superpowers/specs/gop-db/2026-08-20-finance-bill-payment-authorization-design.md | Tóm tắt: .plans/gop-db/finance-bill-payment-authorization/design.md

- finance-bill-payment → @khoipv → .plans/gop-db/finance-bill-payment/plan.md
  Trạng thái: **HOÀN THÀNH — user test trình duyệt xong** (2026-08-20). Port màn ERP
  `admin/income-expenditure/bill_payments` (Phiếu chi tiền) sang HRM phân hệ Tài chính, 23/23 task,
  đủ 5 loại chi: nhánh A (1/2/6/12) lập từ đề nghị duyệt 1 cấp · nhánh B (loại 4 Chi thu nhập nhân viên)
  lập trực tiếp, duyệt 2 cấp KT trưởng → Thủ quỹ, ghi sổ cái gộp theo `identify_number`.
  1 màn danh sách duy nhất, in 2 liên 3 mẫu ERP, xuất Excel, chuông.
  BE 21 file mới + 7 sửa · FE 9 mới + 2 sửa · 18/18 unit test PASS · không migration.
  Sổ cái diff từng trường với ERP: nhánh A khớp 20/20 phiếu, nhánh B 5/5.
  📌 Còn treo: 5 điểm chờ user quyết + 1 lỗi feature CŨ (Phiếu thu in "đồng đồng",
  `BillIncomePrintService:155`) — xem design.md.
  **Bộ tài liệu bàn giao (Phase N, 2026-09-03)**: `testcase.xlsx` **152 TC** (P0 70%, form 17 cột),
  `HDSD_Phiếu chi tiền.docx` **47 trang**, `SRS - Phiếu chi tiền.docx` **57 trang** (form 2026-08-28,
  14 chức năng FR-01→FR-14, 17 quy tắc BR). 25 ảnh chụp thật → `pc_shots/` (chỉ để local);
  riêng màn IN chụp trên cổng LOCAL vì trang in tự bật hộp thoại in và khoá phiên điều khiển.
  **KHÔNG ghi gì vào DB dev** — dev đã sẵn phiếu Đang tạo + Chờ chi tiền; các popup Duyệt/Hủy/Xóa
  chỉ mở để chụp rồi Đóng.
  Spec: docs/superpowers/specs/gop-db/2026-08-19-finance-bill-payment-design.md | Tóm tắt: .plans/gop-db/finance-bill-payment/design.md

- cut-erp-sync → @khoipv → .plans/gop-db/cut-erp-sync/plan.md
  Trạng thái: **HOÀN THÀNH — user test trình duyệt xong** (2026-08-20). Dọn phần đồng bộ HRM → ERP
  trong module Nhân sự sau khi gộp DB (các khối `use_erp` ghi lại chính bảng vừa ghi, có nguy cơ đè
  nhầm tài khoản). Gỡ 5 khối `boot()` · sync password/status ở `EmployeeService` · `setConnection('mysql2')`
  ở 2 model · 6 lệnh `Config::set(database.default)` ở `AuthController` · 2 job sync → no-op.
  Giữ có chủ đích `Group`↔`TpGroup`, nhánh `use_crm`, các chỗ `use_erp` chỉ đọc.
  Diff 13 file, -557/+105 · không migration · không đụng FE.
  📌 Bug tiềm ẩn CHƯA sửa: `Group::boot()` gọi `TpGroup::find($model->code)` → có thể thêm dòng thừa
  vào `department_groups`.
  Spec: docs/superpowers/specs/gop-db/2026-08-19-cut-erp-sync-design.md | Tóm tắt: .plans/gop-db/cut-erp-sync/design.md

- employee-create-bank-null → @khoipv → .plans/gop-db/employee-create-bank-null/plan.md
  Trạng thái: **HOÀN THÀNH — user test trình duyệt xong** (2026-08-20). Fix lỗi 500
  `Creating default object from empty value` khi tạo mới nhân viên có nhập tài khoản ngân hàng
  (`EmployeeInfoService.php:1317`) — `TpEmployeeInfo` chạy connection `mysql2` nằm ngoài transaction
  nên không đọc được dòng `employee_infos` vừa INSERT. Sửa 3 file BE, không migration, không đụng FE.
  📌 Nợ kỹ thuật cố ý: nhánh `use_erp` / model `Tp*` vẫn đọc-ghi qua connection thừa (đã xử ở cut-erp-sync).
  Spec: docs/superpowers/specs/gop-db/2026-08-19-employee-create-bank-null-design.md | Tóm tắt: .plans/gop-db/employee-create-bank-null/design.md

- finance-bill-income → @khoipv → .plans/gop-db/finance-bill-income/plan.md
  Trạng thái: **HOÀN THÀNH — user test trình duyệt xong** (2026-08-20). Port màn ERP
  `admin/income-expenditure/bill_incomes` (Phiếu thu tiền) sang HRM phân hệ Tài chính, 18/18 task:
  BE đầy đủ (entity, quyền, lọc, CRUD, dựng + ghi bút toán sổ cái, duyệt/hủy, in 2 liên, Excel);
  FE 1 màn danh sách gộp 4 chế độ (bỏ `?mode=`) + form + chi tiết + trang in + menu.
  Task 17 đối chiếu ngược ERP: 11/11 cột · 10/10 ô lọc, sửa 2 lệch (thiếu nút Sửa/Xóa ở chi tiết,
  danh sách chưa dùng mixin CheckPermission). Verify: phpunit 36 tests OK · php -l sạch · parse 8/8 Vue ·
  baseline DB khớp tuyệt đối.
  📌 Ruling U4 (user chốt 2026-08-19): đồng bộ ngược trạng thái sang Phiếu đề nghị thu tiền GIỮ NGUYÊN
  LOGIC ERP — 3 điểm hở (xóa không trả trạng thái · hủy là ngõ cụt · lưu nháp không đổi trạng thái)
  KHÔNG phải bug, đừng sửa ở lượt review sau.
  📌 Còn lại: 1 lượt review tổng toàn nhánh + phân loại ~45 minor đã park · chưa kiểm chứng 2 nhánh phân bổ
  (DB 0 dòng) và in phiếu loại thu 3 · 4 file sửa ở Task 17 chưa commit.
  **Bộ tài liệu bàn giao (Phase M, 2026-09-03)**: `testcase.xlsx` **169 TC** (P0 61%, form 17 cột),
  `HDSD_Phiếu thu tiền.docx` **44 trang**, `SRS - Phiếu thu tiền.docx` **52 trang** (form 2026-08-28,
  13 chức năng FR-01→FR-13, 16 quy tắc BR). 26 ảnh chụp thật → `pt_shots/` (chỉ để local); 3 ảnh mục
  Lịch sử chụp trên cổng LOCAL vì cổng dev chưa deploy Phase L. Đã tạo + xóa 1 phiếu nháp
  `TPE.PT0926.00001` trên dev để chụp Sửa/Xóa (dữ liệu trả nguyên trạng 2.379 phiếu);
  **KHÔNG bấm Duyệt/Hủy trên phiếu thật** vì 2 thao tác đó không hoàn tác được.
  Spec: docs/superpowers/specs/gop-db/2026-08-18-finance-bill-income-design.md

- customer-export-file (Phase 7) → @khoipv → .plans/gop-db/customer-export-file/plan.md
  Trạng thái: **HOÀN THÀNH — user test trình duyệt xong** (2026-08-20). Chuyển việc dựng file
  CSV/Excel/PDF của `/assign/customers` từ BE sang build ở FE: BE thêm `GET assign/customers/export-rows`
  (JSON theo trang, 2.000 dòng/lượt ~0,85s, RAM 60MB) · FE thêm `utils/export/customerExportFile.js`
  (ExcelJS + jsPDF/autoTable + font DejaVu subset 78KB, import động).
  ⚠️ Team phải `npm install` sau khi kéo nhánh (thêm `jspdf` + `jspdf-autotable`).
  📌 3 endpoint export cũ của BE vẫn giữ nguyên, chưa xoá.

- finance-bill-payment-request → @khoipv → .plans/gop-db/finance-bill-payment-request/plan.md
  Trạng thái: **HOÀN THÀNH — user test trình duyệt xong** (2026-08-18). Đã commit:
  `hrm-api` `decc26df7` · `hrm-client` `ba4518877` (đợt sửa UI danh sách 2026-08-18);
  port gốc xong 2026-08-15, commit `hrm-api` `6eed9d2a6` · `hrm-client` `8c0ffb424`.
  Port màn ERP "Phiếu đề nghị thanh toán" → `/finance/bill-payment-requests` (phân hệ Tài chính),
  **duyệt 5 cấp**, 4 loại chi. 8 phase / 29 task · 17 route BE · 12 file FE · 9 quyền id 1153–1161 ·
  dùng chung bảng ERP `bill_payment_requests`. Đợt sửa UI gồm 6 việc màn danh sách (bỏ nút Xem chi tiết ·
  popup Cấu hình cột · 2 cột Người/Ngày cập nhật · chuẩn hoá 3 cột ngày · đổi tiêu đề cột KH/NCC ·
  sửa sắp xếp cột) — chi tiết + số liệu đo ở Checkpoint cuối `plan.md`.
  ⚠️ Có sửa component dùng chung `components/V2BaseSelectRemote.vue` (18 màn) — chỉ Việt hoá chữ
  Select2, không đổi hành vi (user chốt 2026-08-18).
  ⚠️ DB local còn dữ liệu test: `employee_manage_departments` id 368 · `departments.id = 111` ·
  8 phiếu `TEST.DNTT-CHI.*` (seeder có câu lệnh dọn).
  📌 Chưa làm: SRS / testcase / HDSD · chưa đối chiếu trực tiếp giao diện ERP.
  📌 Nợ ghi sổ (KHÔNG tự làm): `bill_payment_request_details` thiếu index `bill_payment_request_id`
  — bảng dùng chung ERP+HRM, muốn thêm phải hỏi user.
  🔧 **Đang sửa tiếp (2026-08-24)**: bổ sung cột **"Số tiền chi"** cho bảng chi tiết màn xem (thiếu
  từ đợt port — Task 7.1 Bước 2 có ghi nhưng chưa làm). BE đọc `payment_money_approve` sang uỷ nhiệm
  chi / phiếu chi gắn với phiếu. Code xong, **chờ user test trình duyệt, chưa commit**.
  Đã làm luôn cho **màn IN + file Excel** (đối chiếu ERP: cả 2 đầu ra bên đó đều có cột này);
  tiêu đề cột Excel đổi `Số tiền duyệt` → `Số tiền chi` cho khớp ERP.
  🔧 **Đang sửa tiếp (2026-08-24, đợt 2)**: bug user báo — màn tạo mới, **loại chi 12** (CP vận chuyển
  NCC) chọn NCC **nước ngoài** (`customer_type = 3`, ca `KORSOL`) thì khối ngân hàng trắng trơn và
  **không gửi duyệt được**. Nguyên nhân ở **nguồn dữ liệu**: `party-banks` chỉ đọc
  `customer_has_bank_accounts` + cột cũ trên `customers`, còn tài khoản NCC nước ngoài nằm ở
  **`supplier_banks`** — bảng này chỉ nhánh hiển thị "NCC nước ngoài" (loại chi 1) mới dùng. ERP dính y hệt.
  **User chốt giữ nguyên giao diện cũ** (khối trong nước 5 ô), chỉ sửa BE: `partyBanks()` thêm nguồn
  dự phòng `supplier_banks` khi 2 nguồn kia rỗng (map cả danh sách → NCC nhiều tài khoản vẫn có
  dropdown chọn), `StoreRequest` nới đúng 3 ô Chi nhánh/Tỉnh-TP mà bảng đó không có.
  BE 2 file · FE 0 thay đổi hành vi · không migration. Code xong, **chờ user test trình duyệt, chưa commit**.
  📌 Nợ ghi sổ (cần user quyết): bản in loại 12 + NCC nước ngoài thừa 3 dòng Phí/IBAN/Swift toàn `—` ·
  mở lại phiếu NCC nước ngoài loại 1 ở màn xem/sửa bị mất khối ngân hàng (lỗi có sẵn).
  🔧 **Đang sửa tiếp (2026-08-24, đợt 3)** — XUẤT EXCEL + MÀN IN, 3 việc:
  · **Yêu cầu user:** cột "Số tiền chi" chỉ in khi phiếu ở trạng thái **Duyệt phiếu chi** (status 8);
    dòng Tổng cộng **gộp** các cột mô tả đầu bảng (STT + [chuyến xe] + [NCC] + [hợp đồng]) thành 1 ô.
  · **Bug user báo:** cột "Nhà cung cấp" trống trên Excel/bản in phiếu 4197. Gốc: FE lưu phiếu chỉ gửi
    `supplier_id`, KHÔNG gửi `*_code`/`*_name` (`BillPaymentRequestForm.vue` :1436) → snapshot dòng chi
    tiết luôn NULL với phiếu tạo từ HRM (1/1593 dòng, phần còn lại là dữ liệu port từ ERP).
    Màn danh sách + màn chi tiết đã có fallback sẵn, chỉ nhánh in/Excel thì không → đã thêm fallback
    sang quan hệ trong `detailObjectName()` + `objectName()`.
  · **Bám lại cấu trúc ERP** (user chốt qua 4 câu hỏi): tiêu đề bảng **2 dòng** (ô đơn vị tiền ở dòng
    dưới) · phiếu **ngoại tệ dùng bảng riêng** của ERP (2 cặp nguyên tệ/VND, bỏ 3 cột duyệt theo cấp,
    lấy cấp duyệt cao nhất > 0) · đổi nhãn `KT trưởng/BGD` + `Số hợp đồng nhập mua` / `Số đơn hàng/Hợp đồng` ·
    **bỏ cột Khách hàng/Nhân viên** (3 nhánh `type_*_cash()` của ERP xét khoá không tồn tại → luôn false,
    là code chết) · thêm dòng "Nhà cung cấp:" đầu phiếu cho loại 12 và loại 1 + HĐ + CK ·
    định dạng số `#,##0.##` khớp `formatCurrency($n, 2)`, riêng 2 cột quy đổi VND dùng `#,##0`.
  Toàn bộ cờ bố cục gom vào `BillPaymentRequestPrintResource::columns` làm nguồn duy nhất cho cả FE lẫn Excel.
  BE 3 file (`PrintResource`, `Service`, blade export) + `BillPaymentRequestExport` · FE 1 file (`_id/print.vue`) ·
  không migration. Verify: đối chiếu bộ cột FE↔BE trên **15 phiếu** đủ loại 1/2/6/12 × TM/CK × VND/RUPEE/IDR
  × 7 trạng thái — **lệch 0**; dựng file .xlsx thật đọc lại bằng PhpSpreadsheet (merge tiêu đề, dòng đơn vị,
  kiểu ô số đều đúng). Code xong, **chờ user test trình duyệt, chưa commit**.
  📌 Nợ ghi sổ đợt 3 (cần user quyết): (1) snapshot `*_code`/`*_name` dòng chi tiết vẫn không được ghi khi
  lưu phiếu → phiếu không giữ tên đối tượng tại thời điểm lập, nên vá ở BE; (2) loại chi 6 có 0/537 dòng
  gắn `employee_id` (đối tượng ở cấp phiếu); (3) nhánh loại 1 không hợp đồng + loại chi 3 chưa test được
  (DB 0 dòng); (4) khối 5 chữ ký vẫn chiếm cứng 10 cột, chưa rải `colspan` theo số cột bảng.
  Spec: docs/superpowers/specs/gop-db/2026-08-14-finance-bill-payment-request-design.md | Tóm tắt: .plans/gop-db/finance-bill-payment-request/design.md

- form-validate-base → @khoipv → .plans/gop-db/form-validate-base/plan.md
  Trạng thái: **HOÀN THÀNH — user test đủ 23/23 màn** (2026-08-14).
  Gắn được `v-validate` thẳng lên `V2Base*` → lỗi hiện realtime. 2 mixin mới (`v2ValidateMixin`,
  `formValidateMixin`), 7 component base, 7 rule mới ở `plugins/vee-validate.js` (thuần thêm).
  Theo skill `form-validate`: FE chỉ `required` ô **Tên**, còn lại BE trả 422; **message BE chuẩn hoá
  đúng bằng câu FE nói** (14 FormRequest).
  Còn lại (không chặn): PR cập nhật `.claude/skills/form-validate/SKILL.md` (bỏ `data-vv-value-path`).
  Spec: docs/superpowers/specs/gop-db/2026-08-14-form-validate-base-design.md | Tóm tắt: .plans/gop-db/form-validate-base/design.md

- device-errors-load-data → @khoipv → .plans/gop-db/device-errors-load-data/plan.md
  Trạng thái: **HOÀN THÀNH — user test xong** (2026-08-13). Màn `customer-care/device-errors` hiện
  "không có dữ liệu" oan do `loading` khởi tạo `false` và 2 API dropdown chạy tuần tự trước `loadData()`.
  Sửa 1 file FE, không đụng BE.
  Spec: docs/superpowers/specs/gop-db/2026-08-13-device-errors-load-data-design.md

- pagination-100-rows → @khoipv → .plans/gop-db/pagination-100-rows/plan.md
  Trạng thái: **HOÀN THÀNH — user test xong** (2026-08-13). Thêm option **100** dòng/trang: sửa đúng
  1 chỗ — default `pageSizeOptions` của `components/V2BaseDataTable.vue` (user chốt sửa thẳng component
  dùng chung, 93 file cùng ăn). BE không phải sửa.
  ⚠️ Muốn thêm `200`/`500` sau này phải sửa BE trước — 3 chỗ cap `min(100, …)` sẽ âm thầm ghim lại 100.
  📌 Repo có **2 component phân trang song song** default lệch nhau (`V2BaseDataTable` vs `V2BasePagination`).
  Spec: docs/superpowers/specs/gop-db/2026-08-13-pagination-100-rows-design.md

- customer-date-no-future → @khoipv → .plans/gop-db/customer-date-no-future/plan.md
  Trạng thái: **HOÀN THÀNH — user test xong** (2026-08-13). Chặn ngày tương lai ở 3 ô ngày màn KH,
  **2 lớp** (FE `:disabled-date` + BE `before_or_equal:today`) vì `V2BaseDatePicker` cho gõ tay.
  📌 Không phải sửa component dùng chung — `disabledDate` đã có sẵn prop. Sửa 1 chỗ `CustomerForm.vue`
  → 5 màn cùng ăn. KH đang có ngày tương lai vẫn hiện, chỉ chặn từ lần sửa sau.
  Spec: docs/superpowers/specs/gop-db/2026-08-13-customer-date-no-future-design.md

- chuyen-menu-nhom-giai-phap → @khoipv → .plans/gop-db/chuyen-menu-nhom-giai-phap/plan.md
  Trạng thái: **HOÀN THÀNH — user xác nhận** (2026-08-12). Đưa **Nhóm giải pháp** + **Ứng dụng** từ
  Bán hàng sang **Danh mục dùng chung** (chỉ menu, 3 file `subsystem-menu/*`).
  📌 Lần sau **không đề xuất tách** `/assign/customer-scope-groups` lên cấp 1 — đã thử, user đổi ý, đã hoàn tác.
  ⚠️ Nợ chung với đợt Nhóm ngành: 4 quyền vẫn `group = 'Danh mục'` nên màn Phân quyền vẫn xếp ở tab Giao việc.
  Spec: docs/superpowers/specs/gop-db/2026-08-12-chuyen-menu-nhom-giai-phap-design.md

- chuyen-menu-nhom-nganh → @khoipv → .plans/gop-db/chuyen-menu-nhom-nganh/plan.md
  Trạng thái: **HOÀN THÀNH — user test xong** (2026-08-12). Đưa **Nhóm ngành** từ Bán hàng sang
  **Danh mục dùng chung** (chỉ menu, 3 file).
  ⚠️ KHÔNG đổi `type` quyền 983/998: `Permission.vue` gom khối chỉ theo `group`, đổi sẽ kéo nhầm cả
  29 quyền Giao việc.
  📌 Bẫy khi test: tài khoản dev đang đăng nhập có **0 quyền** → mọi màn gated bị đẩy về 404.
  Spec: docs/superpowers/specs/gop-db/2026-08-12-chuyen-menu-nhom-nganh-design.md

- customer-history → @khoipv → .plans/gop-db/customer-history/plan.md
  Trạng thái: **HOÀN THÀNH — user test xong** (2026-08-12). Lịch sử thay đổi KH ở cả màn danh sách
  (modal) và chi tiết (`SystemInfoSection`), dùng lại base của báo giá: bảng `customer_history` +
  endpoint chung `GET /assign/system-logs/{type}/{id}`. Không permission riêng.
  🐛 Phát hiện khi test, CHƯA sửa gốc: `CustomerForm.buildPayload()` gửi cố định `district_id: null`
  ⇒ **mỗi lần lưu KH cũ là xoá Quận/Huyện trong DB** (mới chỉ ẩn khỏi log qua `CUSTOMER_HIDDEN_FIELDS`).
  Spec: docs/superpowers/specs/gop-db/2026-08-11-customer-history-design.md

- customer-lock → @khoipv → .plans/gop-db/customer-lock/plan.md
  Trạng thái: **HOÀN THÀNH — user test xong** (2026-08-12). Khóa/Mở khóa KH (`status` 0/1), gate bằng
  quyền ERP `Xóa khách hàng`, không thêm permission/migration. 2 route POST (ERP dùng GET).
  📌 Popup chọn KH dùng chung đã lọc `status: 1` sẵn; các ô LỌC vẫn hiện KH khóa (user chốt).
  Spec: docs/superpowers/specs/gop-db/2026-08-11-customer-lock-design.md

- customer-care-service-price-config → @junfoke → .plans/gop-db/customer-care-service-price-config/plan.md
  Trạng thái: **HOÀN THÀNH — user test trình duyệt xong** (2026-08-12), nhánh `gop_db`.
  Chuyển "Cập nhật nhanh giá dịch vụ" từ ERP sang CSKH — màn danh mục thứ 6 của phân hệ.
  Chi tiết + gotcha: plan.md | Spec: docs/superpowers/specs/gop-db/2026-08-06-customer-care-service-price-config-design.md | Tóm tắt: .plans/gop-db/customer-care-service-price-config/design.md

- customer-column-config → @khoipv → .plans/gop-db/customer-column-config/plan.md
  Trạng thái: **HOÀN THÀNH — user test xong** (2026-08-11). Cấu hình cột hiển thị cho
  `/assign/customers` (18 cột, lưu DB qua `column-customizations`), khoá STT + Mã-Tên bằng cách không
  truyền vào modal dùng chung.
  ⚠️ 4 cột cần 5 leftJoin làm COUNT chậm 3,7 lần → gate sau cờ `with_extra_columns`.
  ⚠️ Modal chung dùng `:value="column.key"` ⇒ cột hiện mặc định PHẢI khai `isVisible: '<đúng key>'`.
  📌 Ghi nhận không sửa: `ColumnCustomizationService` nhét thẳng `$request->table` vào tên cột SQL.
  Spec: docs/superpowers/specs/gop-db/2026-08-10-customer-column-config-design.md

- customer-form-group → @khoipv → .plans/gop-db/customer-form-group/plan.md
  Trạng thái: **HOÀN THÀNH — user test xong** (2026-08-11). Thêm trường **Nhóm khách hàng** vào
  `CustomerForm.vue` (5 màn cùng ăn) + nối dữ liệu thật cho cột "Nhóm KH" ở danh sách.
  🐛 Sửa kèm lỗi MẤT DỮ LIỆU có sẵn: `syncGroups()` xoá-rồi-ghi vô điều kiện trong khi form chưa bao
  giờ gửi `groups` ⇒ mỗi lần sửa KH trên HRM là xoá sạch nhóm do ERP gán.
  Spec: docs/superpowers/specs/gop-db/2026-08-10-customer-form-group-design.md

- customer-export-file → @khoipv → .plans/gop-db/customer-export-file/plan.md
  Trạng thái: **HOÀN THÀNH — user test xong** (2026-08-11). 3 nút Xuất CSV / Excel / PDF cho
  `/assign/customers`, dùng quyền ERP có sẵn. Sửa 3 lỗi của bản ERP (thiếu header, CSV không BOM,
  mất số 0 đầu). 17.542 KH: CSV ~13s · XLSX ~44s (mẫu chuẩn HRM), RAM đỉnh 266 MB.
  ⚠️ Team phải `composer install` sau khi kéo nhánh (thêm `barryvdh/laravel-dompdf ^1.0`).
  ⚠️ **CÒN NỢ**: PDF không xuất nổi toàn bộ 17.544 KH (dompdf memory exhausted, fatal không bắt được);
  chọn 1 trong 3 hướng: chặn số dòng / nâng `memory_limit` riêng / đẩy queue + mail.
  Spec: docs/superpowers/specs/gop-db/2026-08-10-customer-export-file-design.md

- customer-import-excel → @khoipv → .plans/gop-db/customer-import-excel/plan.md
  Trạng thái: **HOÀN THÀNH — user test xong** (2026-08-11). Import Excel 25 cột cho `/assign/customers`
  (`V2BaseImportModal` 4 bước, gọi lại `CustomerService::save()`); danh mục tra theo tên, KHÔNG tự tạo
  mới; trùng MST/CCCD báo lỗi, chỉ tạo mới.
  Spec: docs/superpowers/specs/gop-db/2026-08-10-customer-import-excel-design.md

- customer-care-serial-catalog → @junfoke → .plans/gop-db/customer-care-serial-catalog/plan.md
  Trạng thái: **CODE DONE + ĐÃ VERIFY (BE + trình duyệt)** (2026-08-06). Chuyển "Danh mục serial thiết bị
  làm dịch vụ" (21.632 dòng) sang CSKH — 1 màn READ-ONLY + Xuất Excel, quyền 1126.
  Còn treo: user rà bằng mắt; chốt cách lọc 13 bản ghi `status` 0/3.
  Chi tiết + gotcha: plan.md | Spec: docs/superpowers/specs/gop-db/2026-08-06-customer-care-serial-catalog-design.md | Tóm tắt: .plans/gop-db/customer-care-serial-catalog/design.md

- chuyen-code-phan-he → @junfoke → .plans/gop-db/chuyen-code-phan-he/plan.md
  Trạng thái: **XONG 3 phân hệ + Phase 17-19 (chuẩn hub 14/17 phân hệ), ĐÃ VERIFY TRÌNH DUYỆT** (2026-08-06).
  Giai đoạn 2 của `tach-phan-he-erp-hrm`: đưa CODE về đúng phân hệ (Danh mục chung 10 màn, BHXH 7 màn,
  Bán hàng 27 màn — 98 cặp redirect giữ URL cũ, 6 migration quyền).
  Còn nợ: 7 màn địa lý-ngân hàng chưa có permission; bộ quyền KH cũ của HRM (166-169) còn song song.
  Bước tiếp: các phân hệ còn lại chưa tới lượt chuyển code.
  Chi tiết + gotcha: plan.md | Spec: docs/superpowers/specs/gop-db/2026-08-04-chuyen-code-phan-he-master-data-insurance-design.md
  và docs/superpowers/specs/gop-db/2026-08-06-hub-menu-customer-care-finance-design.md | Tóm tắt: .plans/gop-db/chuyen-code-phan-he/design.md

- customer-docs → @junfoke → .plans/gop-db/customer-docs/plan.md
  Trạng thái: **DONE** (2026-08-15) — bộ 3 tài liệu (TC 235 case / SRS / HDSD 38 trang) cho màn
  Danh mục khách hàng `/assign/customers` (code do @khoipv làm).
  Chi tiết + gotcha: plan.md

- customer-care-cost-catalog → @junfoke → .plans/gop-db/customer-care-cost-catalog/plan.md
  Trạng thái: **BE + FE DONE, verify BE xong** (2026-08-03). Chuyển "Danh mục dịch vụ sửa chữa và chi phí
  khác" (`costs`, `kind_of=2`) sang CSKH; Phase 5 cắt luôn `erp-cost-catalog` sang luồng mới.
  ⚠️ Còn nhiều chỗ dùng `mysql2` ngoài phạm vi danh mục chi phí (AssignBusinessController, QuotationService…).
  Bước tiếp: user verify bằng mắt `/customer-care/costs`.
  Chi tiết + gotcha: plan.md | Spec: docs/superpowers/specs/gop-db/2026-08-03-customer-care-cost-catalog-design.md | Tóm tắt: .plans/gop-db/customer-care-cost-catalog/design.md

- finance-product-transfer-request → @khoipv → .plans/gop-db/finance-product-transfer-request/plan.md
  Trạng thái: **HOÀN THÀNH — user xác nhận** (2026-08-07), đã commit `hrm-api 3a0acce08` ·
  `hrm-client ed0abb049`. Port màn ERP "Phiếu yêu cầu chuyển hàng" sang Tài chính, 2 cổng song song
  cùng bảng, HRM chỉ ghi status 2↔3. SQL DEPLOY đã chạy môi trường thật (quyền 1129–1133).
  ⚠️ **CHƯA mở task, còn nợ team**: middleware `CheckPermission` hỏng trên `gop_db` (spatie bỏ sót role
  gán từ ERP do `model_type` mismatch) → cần TASK RIÊNG rà mọi route đang gắn `checkPermission`.
  **Đợt chỉnh 2026-08-13 (Phase 8) — CHỜ USER TEST**: chuẩn hoá footer 2 màn sang `V2Footer`
  (nhãn "Lưu nháp"/"In"/"Quay lại", popup xác nhận khi Gửi duyệt; mất icon spinner ở 3 nút).
  **Bộ tài liệu bàn giao (Phase 9, 2026-09-03)**: `testcase.xlsx` **188 TC** (P0 50%, form 17 cột —
  đã XÓA bản 15 cột cũ ngày 07/08 theo yêu cầu user), `HDSD_Phiếu yêu cầu chuyển hàng.docx`
  **48 trang**, `SRS - Phiếu yêu cầu chuyển hàng.docx` **52 trang** (form 2026-08-28, 14 chức năng
  FR-01→FR-14, 16 quy tắc BR). 31 ảnh chụp thật trên `hrm-crm.eteksofts.com` → `pycch_shots/`
  (chỉ để local). 3 generator `gen_testcase.py` / `gen_hdsd.py` / `gen_srs.py` commit kèm.
  Spec: docs/superpowers/specs/gop-db/2026-08-05-finance-product-transfer-request-design.md

- customer-care-services-catalog → @khoipv → .plans/gop-db/customer-care-services-catalog/plan.md
  Trạng thái: **CODE DONE P1–P5, user xác nhận** (2026-08-05). Port "Danh mục gói bảo dưỡng"
  (207 dòng + 5 bảng con) sang `/customer-care/services`: 12 route, form 5 khối, in template 191.
  🐛 Đã sửa 2 lỗi CRITICAL `key_word` shape `{text}` (88/207 gói có nguy cơ hỏng màn báo giá DV ERP).
  ⚠️ Bug HỆ THỐNG chưa sửa (file chung, cần báo team): `V2BaseSelect.vue:59` rớt option `id = 0`.
  ⚠️ **Khi DEPLOY phải chạy tay 3 SQL** (chi tiết `sdd-progress.md` Task 1.5).
  **Đợt chỉnh 2026-08-13 (Phase 11j–11l) — CHỜ USER TEST**: Excel hết cảnh báo "Number stored as text",
  đổi chữ "dịch vụ" → "gói bảo dưỡng", form dùng `V2Footer` (nút Lưu mất icon spinner — user đã chốt).
  Tồn: checklist "Verify tổng thể" cuối plan.md chưa tick.
  **Phase 12 (2026-08-17) — BỘ TÀI LIỆU BÀN GIAO XONG**: `testcase.xlsx` (171 TC, P0 63%, engine
  17 cột), `SRS - Danh mục gói bảo dưỡng.docx` (form 4 chương, FR-01…FR-11, 37 trang),
  `HDSD_Danh muc goi bao duong.docx` (31 trang) — sinh lại được bằng `gen_testcase.py` /
  `gen_srs.py` / `gen_hdsd.py`. Chờ user chốt 2 điểm: xuất Excel + in + xem danh sách hiện KHÔNG
  gắn quyền, và xuất Excel không áp bộ lọc màn hình (giữ nguyên như ERP).
  Spec: docs/superpowers/specs/gop-db/2026-08-04-customer-care-services-catalog-design.md | Ledger: .plans/gop-db/customer-care-services-catalog/sdd-progress.md

- bo-sung-menu-phan-he → @junfoke (Phase 11: @khoipv) → .plans/gop-db/bo-sung-menu-phan-he/plan.md
  Trạng thái: **CODE DONE + KIỂM THỬ TỰ ĐỘNG PASS** (Phase 0-9: 2026-08-03; Phase 11 dọn nhãn menu
  Danh mục chung: 2026-08-12; Phase 13 gán link nhóm `Yêu cầu` phân hệ Bán hàng: 2026-09-22).
  Khai 355 mục menu trên 14 phân hệ, chỉ đụng `hrm-client`.
  ⚠️ Bug đã phát hiện, CHƯA SỬA (không thuộc feature): mục "Khách hàng" khai TRÙNG ở `master-data.js`
  và `sale.js` → `/assign/customers` luôn ra sidebar Danh mục chung.
  ➕ **Redmine #11408 (22/09/2026)**: mục cấp 1 ĐI THẲNG ("Ngân hàng", "Ngân hàng câu hỏi khảo sát") không vào được
  Gần đây / Yêu thích — `allScreens` của rail và màn Tổng quan chỉ dựng từ `groups`, bỏ qua `navLinks`.
  Đã sửa + verify: `hrm-client` **4e972236c** (chưa push).
  Bước tiếp: Phase 10 — verify trình duyệt thật.
  Chi tiết + gotcha: plan.md | Spec: docs/superpowers/specs/gop-db/2026-08-01-bo-sung-menu-phan-he-design.md | Tóm tắt: .plans/gop-db/bo-sung-menu-phan-he/design.md

- customer-care-maintenance-catalogs → @junfoke → .plans/gop-db/customer-care-maintenance-catalogs/plan.md
  Trạng thái: **CODE DONE + VERIFIED (BE)** (2026-08-03). 2 màn ĐẦU TIÊN của phân hệ CSKH: "Cấp dịch vụ
  bảo dưỡng" + "Danh mục ghi chú kiểm tra bảo dưỡng", quyền 1115-1118.
  Còn nợ: `ErpPermissionHelper` + `Modules/Assign` vẫn qua `mysql2`.
  Bước tiếp: user verify `/customer-care/levels` + `/customer-care/note-maintenances`.
  Chi tiết + gotcha: plan.md | Spec: docs/superpowers/specs/gop-db/2026-08-03-customer-care-maintenance-catalogs-design.md | Tóm tắt: .plans/gop-db/customer-care-maintenance-catalogs/design.md

- finance-currency-catalog → @junfoke → .plans/gop-db/finance-currency-catalog/plan.md
  Trạng thái: **CODE DONE + VERIFIED (BE + cron)** (2026-08-03) — màn thứ 3 của phân hệ Tài chính.
  Kèm chuyển cron tỷ giá sang HRM (`finance:update-exchange-rate`, 03:00) và đã tắt lịch bên ERP.
  ⚠️ Trước khi lên thật: `hrm-api/.env` chưa cấu hình mail nên `emailOutputTo` chưa gửi được.
  Bước tiếp: user verify bằng mắt `/finance/currencies`.
  Chi tiết + gotcha: plan.md | Spec: docs/superpowers/specs/gop-db/2026-08-03-finance-currency-catalog-design.md | Tóm tắt: .plans/gop-db/finance-currency-catalog/design.md

- finance-account-catalog → @junfoke → .plans/gop-db/finance-account-catalog/plan.md
  Trạng thái: **PHASE 1-10 CODE DONE + VERIFIED** (2026-09-04; Phase 10 đưa form Tạo/Sửa về bố cục
  ERP — redmine 11300) — 2 màn "Danh mục tài khoản" +
  "Danh mục loại tài khoản"; màn đầu tiên của phân hệ Tài chính nên dựng luôn khung `Modules/Finance`.
  Bước tiếp: Phase 7 đối chiếu 2 cổng (cần bật ERP local) + tạo 2 file mẫu Excel trong `hrm-client/static/`.
  Chi tiết + gotcha: plan.md | Spec: docs/superpowers/specs/gop-db/2026-07-30-finance-account-catalog-design.md | Tóm tắt: .plans/gop-db/finance-account-catalog/design.md

- tach-phan-he-erp-hrm → @junfoke → .plans/gop-db/tach-phan-he-erp-hrm/plan.md
  Trạng thái: **XONG GIAI ĐOẠN 1 (khung phân hệ + menu)** (2026-07-30), đã test thật 9 màn trên dev.
  Quy hoạch lại 24 phân hệ / 5 nhóm theo Sơ đồ tổng thể v1.6; dựng base 17 phân hệ mới.
  Bước tiếp: user test 17 màn edit/detail. Giai đoạn 2 = `chuyen-code-phan-he`.
  Chi tiết + gotcha: plan.md | Spec: docs/superpowers/specs/gop-db/2026-07-30-tach-phan-he-erp-hrm-design.md | Tóm tắt: .plans/gop-db/tach-phan-he-erp-hrm/design.md
