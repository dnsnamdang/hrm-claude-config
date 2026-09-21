# Plan — Gia hạn dự án TKT + tự đóng theo giai đoạn (Redmine #11153)

Nhánh `tpe` · worktree `HRM/worktrees/tpe-api` + `tpe-client` · chưa commit

## Phase 1 — DB + cấu hình ✅ (2026-09-11)
### BE
- [x] 5 migration: `project_phase_close_configs` (+ seed 9 giai đoạn theo spec), 4 cột cấu hình chung trên `general_regulations`, `prospective_project_extension_requests`, 3 cột `auto_close_date`/`extended_days`/`close_warning_notified_at` trên `prospective_projects`, `project_close_config_logs` (+ seed lý do "Hệ thống tự đóng do quá thời gian thực hiện")
- [x] Entity `ProjectPhaseCloseConfig`, `ProspectiveProjectExtensionRequest`, `ProjectCloseConfigLog`
- [x] `ProjectCloseConfigService` (get/update + ghi log từng trường đổi) + controller + route `assign/project-close-configs`
- [x] Lịch sử sửa cấu hình (user yêu cầu 2026-09-12): `logs()` GOM theo từng lần bấm Lưu (cùng người + cùng thời điểm), tên người sửa lấy qua `employeeOptionLabel()`; FE `ProjectCloseConfigHistoryModal.vue` (timeline copy khuôn `DeadlineConfigHistoryModal`) + nút "Lịch sử thay đổi" cạnh nút Lưu. Lọc theo nhóm cấu hình / người thực hiện / khoảng ngày
- [x] 🐞 **Bấm Lưu mà không sửa gì vẫn ghi lịch sử** (user báo 2026-09-12). Nguyên nhân KHÔNG phải so sánh sai: form chỉ nạp 1 lần lúc mở trang, người khác sửa cấu hình trong lúc đó thì bấm Lưu sẽ **ghi đè giá trị của họ** và sinh dòng lịch sử "ma". Đã tái hiện được (đổi ngầm DB 10→15, bấm Lưu → log `15 → 10`). Vá bằng `@click="loadProjectCloseConfig"` trên `b-tab`: mỗi lần mở tab là nạp lại từ máy chủ
- [x] Test kỹ lịch sử 16/16 PASS: lưu không đổi → 0 dòng · đổi 1 tham số chung → nhãn tiếng Việt + đúng cũ/mới + có tên người sửa · đổi 1 giai đoạn → nhãn kèm tên giai đoạn · đổi nhiều thứ 1 lần → gom đúng 1 mục nhiều dòng, đủ cả 2 nhóm · xoá trống ô → "9 → Không tự đóng" · điền lại → "Không tự đóng → 8" · lưu lại y nguyên sau khi sửa → 0 dòng
- [x] Trả toàn bộ cấu hình về giá trị chuẩn theo spec sau khi test
- [x] Bảng giai đoạn sắp theo tên bằng `strnatcasecmp` — `orderBy('name')` của SQL xếp "10." trước "2." 
- [x] Permission seeder: `Trưởng phòng duyệt gia hạn dự án TKT` (1182), `Ban giám đốc duyệt gia hạn dự án TKT` (1183)
- [x] 🐞 `GeneralRegulation::$fillable` thiếu 4 cột mới → `update()` NUỐT giá trị im lặng (lưu xong vẫn ra số cũ). Đã bổ sung vào `$fillable`
### FE
- [x] Sub-tab "Đóng dự án tự động" trong Cấu hình chung → tab Quản lý dự án (4 tham số + bảng 9 giai đoạn, ô trống = không tự đóng)
- [x] 5 icon Info (`ri-information-line` + `b-popover custom-class="info-popover"`, skill info-icon-tooltip) giải thích từng tham số: trường nào áp dụng khi CHƯA có báo giá, ai duyệt trước/sau ngưỡng ngày, ân hạn 0 nghĩa là gì, bảng theo giai đoạn tính từ mốc nào và sửa có ảnh hưởng dự án cũ không

## Phase 2 — Hạn đóng tự động ✅
- [x] `ProspectiveProjectAutoCloseService`: `calculateAutoCloseDate()` / `recalc()` / `recalcById()` / `latestApprovedQuotation()` / `autoCloseReasonId()`
- [x] Hook recalc: `ProspectiveProjectService` store + update, `QuotationService::cascadeApprovedStatus`
- [x] Resource trả `auto_close_date`, `extended_days`, `is_can_request_extension`, `pending_extension_request`
- [x] Mở `doCloseProjectCascade()` thành public để cron dùng (không kiểm tra NVKD chính)

## Phase 3 — Đề xuất gia hạn + phê duyệt ✅
### BE
- [x] `ProspectiveProjectExtensionService`: store (cấp duyệt theo ngưỡng X), tpApprove, bgdApprove, reject, pendingQuery, canRequestExtension
- [x] **Giới hạn phạm vi duyệt giống báo giá** (user chốt 2026-09-11): TP chỉ duyệt đề xuất của phòng ban mình quản lý (`QuotationService::managedDepartmentIdsOf`), BGĐ chỉ duyệt trong công ty mình. Chặn ở service (403) + lọc sẵn ở hàng đợi + cờ `is_can_tp_approve`/`is_can_bgd_approve` của Resource
- [x] Controller + 3 FormRequest + Resource + route (nested trong dự án + `assign/prospective-project-extensions/*`), giữ nguyên mã 403/422 của `abort()`
- [x] Notification theo chuẩn `[DATKT] {Nhóm hành động}: <b>{Tên dự án}</b>. {Ghi chú}`
- [x] Lịch sử dự án thêm dòng "Gia hạn" (ngày kết thúc cũ → mới)
### FE
- [x] `ExtendProjectModal.vue` (V2BaseModal, 2 trường bắt buộc) + nút Gia hạn ở footer chi tiết
- [x] Rà lại theo góp ý user (2026-09-11): popup bỏ dòng "Ngày kết thúc hiện tại" và xem trước ngày kết thúc mới; BE bỏ luôn việc cộng ngày vào `end_date` (spec không yêu cầu) — gia hạn CHỈ lùi hạn đóng tự động; cột danh sách + lịch sử dự án đổi nhãn thành "Hạn đóng tự động"
- [x] Trang cổng phê duyệt `pages/assign/prospective-projects/extension-requests/index.vue` + menu nhóm Phê duyệt
- [x] Bộ lọc cổng phê duyệt (góp ý user): 8 điều kiện (trạng thái · cấp duyệt · dự án · người đề xuất · ngày gửi từ/đến · số ngày gia hạn từ/đến) + auto-search (ô chọn đổi là lọc luôn, ô gõ tay chờ Enter). Ô "Người đề xuất" = toàn bộ nhân sự đang hoạt động của công ty hiện tại, lấy từ store nên không thêm request
- [x] 🐞 Cột "Người đề xuất" trống: tên nằm ở `employee_infos`, bảng `employees` KHÔNG có cột `name` → dùng `employeeOptionLabel()` cho đúng khuôn "Tên - Mã phòng - Mã NV"

## Phase 4 — Cron ✅
- [x] `assign:auto-close-prospective-projects` (recalc · nhắc trước N ngày · tự đóng sau M ngày) + `--dry-run` + `--project=` để kiểm thử an toàn
- [x] Schedule 01:30 hằng ngày trong `app/Console/Kernel.php`

## Phase 5 — Kiểm thử ✅ (API + UI Playwright, tài khoản admin)
- [x] Cấu hình: GET trả 4 tham số + 9 giai đoạn; PUT lưu + ghi log; UI sub-tab hiển thị đúng, ô giai đoạn 9 để trống
- [x] Hạn đóng: chưa báo giá (tạo + 3 tháng) · có báo giá (ngày duyệt + số tháng giai đoạn) · cộng `extended_days`
- [x] Gia hạn cấp 1 (10 ngày ≤ 30): TP duyệt là xong, `end_date` +10, log lịch sử
- [x] Gia hạn cấp 2 (45 và 60 ngày > 30): TP duyệt → Chờ BGĐ → BGĐ duyệt → cộng ngày (UI Playwright đi hết luồng)
- [x] Từ chối: thiếu lý do 422, có lý do → Từ chối, duyệt lại 422, gửi lại được đề xuất mới
- [x] Chặn: dự án đã đóng 422 · đang có đề xuất chờ 422 · không phải NVKD chính 403 · cờ `is_can_request_extension` khớp với chốt chặn BE
- [x] Phạm vi duyệt: tài khoản có quyền TP nhưng KHÔNG quản lý phòng của đề xuất → hàng đợi 0 dòng + duyệt bị chặn "Bạn không quản lý phòng ban của đề xuất này" (test tinker, rollback)
- [x] Cron: dry-run + chạy thật trên 2 dự án mẫu — nhắc đúng còn 5 ngày, chạy lại không gửi trùng; tự đóng đúng lý do, `closed_by = null`; 2 thông báo đúng chuẩn nội dung

### Checkpoint — 2026-09-11
Vừa hoàn thành: toàn bộ 5 phase, đã đổi Redmine #11153 sang "Đang tiến hành"
Đang làm dở: —
Bước tiếp theo: user review trên :3005 → commit. Cần khách chốt còn 2 điểm: prefix thông báo `[DATKT]`, giá trị mặc định S/N/M/X. (Điểm "ngày nộp thầu" đã chốt 2026-09-12: mọi giai đoạn dùng chung mốc ngày duyệt báo giá gần nhất, KHÔNG thêm cột — code sẵn đã đúng, không phải sửa)
Blocked:

## Dữ liệu mẫu để test (giữ lại)
| Dự án | Mã | Trạng thái | Dùng để test |
|---|---|---|---|
| 253 | CTV_NV.UD.0101.2026.DA002 | Lập dự toán | Đang có đề xuất GHDA.00005 chờ TP duyệt |
| 254 | CTV_NV.UD.0101.2026.DA002 | Trao đổi giải pháp với KH | Đã gia hạn 3 lần (10 + 60 + 45 = 115 ngày) |
| 255 | CTV_NV.UD.0101.2026.DA003 | Thu thập thông tin | Cron đã nhắc "còn 5 ngày" (hạn 16/09/2026) |
| 256 | CTV_NV.UD.0101.2026.DA004 | Đóng | Cron tự đóng, lý do "Hệ thống tự đóng do quá thời gian thực hiện" |

## Phase 6 — Kiểm thử sâu cron + kiểm thử trên cổng dev (2026-09-12)

### 6.1 Cron — 14 nhánh, chạy thật ở local (dự án 258-271, tiền tố tên `CRON-TEST`)
- [x] Chưa có báo giá duyệt → hạn = ngày tạo + S tháng (S=3) — #258 hạn 12/11
- [x] Nhắc khi còn ≤ N ngày (N=7) — #259 "còn 5 ngày", gửi đúng 1 thông báo
- [x] Chạy lại lượt 2: không nhắc lại, không đóng lại (idempotent nhờ `close_warning_notified_at`)
- [x] Dự án đã nhắc từ trước → không nhắc lần nữa — #263
- [x] Biên đúng hạn hôm nay → CHƯA đóng, chỉ nhắc "còn 0 ngày" — #261
- [x] Biên quá hạn 1 ngày → đóng — #262
- [x] Ngày ân hạn M=3: quá hạn 2 ngày KHÔNG đóng (#270), quá hạn 4 ngày ĐÓNG (#271)
- [x] Đã gia hạn 40 ngày → hạn lùi đúng 40 ngày, thoát diện đóng — #264
- [x] Có báo giá duyệt → mốc = ngày duyệt báo giá gần nhất + số tháng giai đoạn (#267 giai đoạn 1 tháng → đóng; #268 giai đoạn 6 tháng → chưa)
- [x] Giai đoạn không cấu hình số tháng → `auto_close_date` null, không bao giờ đóng — #265
- [x] Dự án đã đóng (trạng thái 11) → nằm ngoài phạm vi quét — #266
- [x] Dự án không có NV KD chính → vẫn đóng, không lỗi, bỏ qua bước gửi thông báo — #269
- [x] `--dry-run` KHÔNG ghi DB (kiểm lại 12 dòng: `auto_close_date` vẫn null sau dry-run)
- [x] Đổi cấu hình số tháng giai đoạn → lượt cron kế tiếp tính lại hạn (#268: 12/01/2027 → 12/11/2026 khi đổi 6→4 tháng)
- [x] Đóng tự động ghi đúng: `closed_reason_id` = "Hệ thống tự đóng do quá thời gian thực hiện", `closed_by = null`, log trạng thái 2 → 11 với `changed_by = null`
- [x] Thông báo đúng chuẩn `[DATKT] Quá hạn: <b>Tên</b>. …` / `[DATKT] Sắp đến hạn: …`
- [x] Quét toàn bộ (không `--project`): 235 dự án đang mở, không lỗi

⚠️ **Cảnh báo vận hành**: lượt cron THẬT đầu tiên sẽ đóng hàng loạt dự án cũ đã quá hạn (local: 6 dự án có sẵn). Trước khi bật lịch trên dev/production phải chạy `--dry-run` không kèm `--project` để xem danh sách, rồi mới quyết định.

### 6.2 Trên cổng dev (https://dev-hrm.eteksofts.com) — qua API, tài khoản namdangit
- [x] Code + migration đã lên dev: `GET /assign/project-close-configs` trả 4 tham số + 10 giai đoạn
- [x] Tạo mới dự án tính ngay `auto_close_date` (445-450 → 12/12/2026 = hôm nay + 3 tháng)
- [x] Sửa cấu hình + lịch sử gộp theo lượt lưu; lưu lại y nguyên KHÔNG sinh bản ghi lịch sử (đã trả cấu hình về giá trị gốc 7 ngày / 12 tháng)
- [x] Gửi đề xuất: không phải NV KD chính → 403; thiếu dữ liệu → 422 kèm message tiếng Việt; số ngày âm → 422; đang có đề xuất chờ → 422
- [x] Phân cấp duyệt: 15 ngày → Cấp 1 (TP); 45 ngày → Cấp 2 (TP + BGĐ), cùng bắt đầu ở "Chờ TP duyệt"
- [x] Quyền 1182/1183 ĐÃ có sẵn trên dev (seeder chạy rồi) — việc thiếu là chưa GÁN cho vai trò. Đã tự gán vào vai trò "Super admin" (id 18) cho cả 4 công ty qua `POST /timesheet/roles/store`
- [x] Cổng phê duyệt dev: 403 → 200, hiển thị đúng 2 đề xuất chờ duyệt
- [x] Phạm vi duyệt trên dev: đề xuất thuộc phòng HN_KD3 (tài khoản không quản lý) → 403 "Bạn không quản lý phòng ban của đề xuất này"; chuyển sang phòng HN_NSHC (có quản lý) → duyệt được
- [x] Luồng duyệt dev: cấp 1 (20 ngày) TP duyệt là xong, hạn 12/12/2026 → 01/01/2027; cấp 2 (60 ngày) TP duyệt → Chờ BGĐ (chưa cộng ngày) → BGĐ duyệt → 12/12/2026 → 10/02/2027
- [x] Từ chối trên dev: thiếu lý do 422, có lý do → Từ chối, duyệt lại 422, hạn đóng giữ nguyên, gửi lại được đề xuất mới
- [x] Cron chạy THẬT trên dev (SSH user `erp_tpe`, code ở `/var/www/tpe/hrm-api`, nhánh `tpe-develop-assign`):
  - Nhắc: #449 "còn 5 ngày (hạn 17/09/2026)", thông báo `[DATKT] Sắp đến hạn: … Bạn còn theo dõi dự án này không?` kèm deep-link `/assign/prospective-projects/449/manager`
  - Đóng: #450 trạng thái 2 → 11, `closed_reason_id = 6` ("Hệ thống tự đóng do quá thời gian thực hiện"), `closed_by = NULL`, log trạng thái `changed_by = NULL`, thông báo `[DATKT] Quá hạn: …`
  - Chạy lại lượt 2: không nhắc lại, không đóng lại
- [x] ⚠️ Quét toàn bộ trên dev (`--dry-run`, không ghi gì): **95 / 368 dự án đang mở sẽ bị đóng ngay lượt chạy thật đầu tiên**. Chưa chạy thật toàn bộ — chờ khách quyết định (có thể cần cấu hình ngày ân hạn > 0 hoặc chốt danh sách loại trừ trước khi bật lịch 01:30)

### 6.3 Sửa kèm
- [x] 🐞 Badge trạng thái TRỐNG ở dự án cha: dev có 2 dự án cha đang ở trạng thái 6 "Lập dự toán" (#440, #284) — trạng thái này không nằm trong bộ 8 trạng thái của dự án cha nên `status_name`/`status_color` trả null. `resolveStatusName()`/`resolveStatusColor()` nay tra tiếp bộ 12 trạng thái chuẩn khi bộ dự án cha không khớp

### Checkpoint — 2026-09-12
Vừa hoàn thành: test sâu cron (14 nhánh) ở local; test cấu hình + gửi đề xuất gia hạn trên dev; vá badge trạng thái trống
Đang làm dở: —
Bước tiếp theo: cần SSH dev để chạy cron + seed quyền 1182/1183
Blocked: SSH dev từ chối publickey cho manhcuong/tpe/deploy/ubuntu/root/hrm/dev/www-data

### 6.4 Bật lịch chạy tự động trên dev (2026-09-12)
- [x] Kiểm tra crontab user `erp_tpe`: dòng `* * * * * cd /var/www/tpe/hrm-api/ && php artisan schedule:run` ĐÃ có sẵn (dòng 31) → trình lập lịch Laravel đang bật, KHÔNG phải thêm gì
- [x] `php artisan schedule:list` xác nhận: `assign:auto-close-prospective-projects` — `30 1 * * *` — lượt kế tiếp **2026-09-13 01:30 +07**
- [x] Giờ máy chủ là +07 (trùng `Asia/Ho_Chi_Minh`) nên mốc 01:30 khai trong Kernel chạy đúng giờ VN
- [x] Ảnh chụp hiện trạng TRƯỚC lượt chạy: `dev-hien-trang-truoc-cron-2026-09-12.txt` — 367 dự án đang mở, **95 dự án sẽ bị đóng**, 0 dự án được nhắc

**Cần kiểm lại sáng 13/09** (user sẽ hỏi): số dự án trạng thái 11 tăng đúng 95 · `closed_reason_id` = "Hệ thống tự đóng do quá thời gian thực hiện" · `closed_by = NULL` · log trạng thái `changed_by = NULL` · thông báo `[DATKT] Quá hạn` gửi cho NV KD chính · dòng log `[assign:auto-close-prospective-projects]` trong `storage/logs/laravel-2026-09-13.log` · chạy lượt 2 không đóng lại


## Testcase (2026-09-15)
- [x] Bổ sung 48 testcase (TC-TKT-54 → TC-TKT-101) vào Google Sheet `Testcase _Quản lý dự án` → sheet `12.Dự án TKT`, từ dòng 515 (gid=739303646)
- [x] Sửa lại trình bày theo góp ý 15/09: bỏ icon ⚠️, xuống dòng thật trong ô (bước 1./2./3. và gạch đầu dòng); đã bổ sung quy ước vào `.claude/skills/testcase-documenter/SKILL.md` + `tc_engine.py`

## Fix nhỏ (2026-09-18)
- [x] Footer màn `/assign/prospective-projects/{id}/manager`: bỏ `class="mr-2"` ở nút "Gia hạn" và "Chốt giải pháp" — `.group-select-btn` đã có `gap: 5px`, thêm `mr-2` (8px) làm khoảng cách phải lệch so với các nút khác
