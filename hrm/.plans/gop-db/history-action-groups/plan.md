# Plan — Chuẩn hoá bộ lọc "Loại hoạt động" của Lịch sử

Nhánh: `gop_db` · @dnsnamdang

## Phase 1 — BE (`worktrees/gop_db-api`)

- [x] `SystemLogService`: thêm `GROUP_CREATE/UPDATE/STATUS`, `ACTION_GROUP_LABELS` (3 nhãn), `ACTION_GROUP_MAP` (14 action)
- [x] `SystemLogService::groupOfAction()` — action chưa khai mặc định vào `status`
- [x] `SystemLogService::finalize()` — trả thêm `action_group` cho MỌI dòng log (áp cho cả 10 loại)
- [x] `SystemLogService::getFilterOptions()` — trả 3 nhóm cố định cho mọi `$type`
- [x] Giữ nguyên `performers`: chỉ trả cho `customer`, loại khác rỗng (tránh liệt kê 783 nhân viên)

## Phase 2 — FE (`worktrees/gop_db-client`)

- [x] `components/assign/SystemInfoSection.vue` (khối Lịch sử màn chi tiết): `actionOptions` = 3 nhóm cố định, bỏ suy từ log; lọc theo `action_group` (fallback `action`)
- [x] `components/assign/customer/CustomerHistoryModal.vue` (popup màn danh sách): sửa y hệt để 2 nơi khớp nhau (skill §5.1)

## Phase 3 — Áp nguyên tắc "đã khoá thì không cho sửa" cho màn Khách hàng

Phát hiện khi user hỏi lại: nguyên tắc mới ghi vào CLAUDE.md nhưng màn KH **chưa hề áp dụng**.
Đã kiểm chứng bằng API thật: `POST /assign/customers/43712` (KH `status = 0`) trả **HTTP 200** và
**ghi đè dữ liệu** — `save()` còn xoá luôn các field không gửi (hamlet, gara_name, apartment_number,
date_of_birth, is_supplier, is_manufacturer, short_name) và 2 quan hệ (nhóm KH, hãng xe).
Đã khôi phục nguyên trạng từ snapshot `customer_versions.id = 59083`.

### BE
- [x] `TpCustomer`: hằng `STATUS_ACTIVE/STATUS_LOCKED` + `isLocked()` / `isCanEdit()` — nguồn chân lý duy nhất
- [x] Middleware mới `CheckCustomerNotLocked` → trả **423** kèm message tiếng Việt
- [x] Đăng ký alias `customerNotLocked` ở `app/Http/Kernel.php`
- [x] Gắn cho **13 route ghi** của khách hàng (thông tin chung, người liên hệ, tài liệu/ảnh, xoá file, thiết bị cũ/ngoài, serial)
- [x] KHÔNG gắn cho: `unlock` (lối thoát duy nhất), `lock`, route tạo mới, mọi route chỉ đọc

Dùng middleware thay vì `if` trong từng controller vì 1 KH có ~18 endpoint ghi — rải điều kiện chắc chắn sót.

### FE
- [x] `pages/assign/customers/index.vue`: nút **Sửa** ở cột Hành động thêm điều kiện `&& isActive`
- [x] `components/assign-components/customer/CustomerForm.vue`: vào thẳng URL `/edit` của KH đã khoá → toast + `$router.replace` về màn Chi tiết (loại trừ `modalMode` = xem nhanh trong popup)
- [x] **Footer màn CHI TIẾT**: `:menu="{ edit: perm.edit && isCustomerActive }"` — user phát hiện lúc đầu
      tôi chỉ sửa màn danh sách, để lệch màn chi tiết (vẫn còn nút Sửa ở KH đã khoá)

**Đối xứng sau khi sửa** (cùng 1 bản ghi, 2 màn phải khớp):

| Bản ghi | Dòng ở màn danh sách | Footer màn chi tiết |
| --- | --- | --- |
| KH đã khoá (43712) | Mở khóa · Quản lý · Lịch sử | Quản lý · Mở khóa · Quay lại |
| KH hoạt động (8) | **Sửa** · Khóa · Quản lý · Lịch sử | **Sửa** · Quản lý · Khóa · Quay lại |

### Test
| Ca | Kết quả |
| --- | --- |
| Sửa thông tin chung KH đang khoá | **423** + DB không đổi |
| Thêm người liên hệ / cập nhật tài liệu KH đang khoá | **423** |
| GET chi tiết KH đang khoá | 200 (chỉ đọc vẫn xem được) |
| Mở khoá KH đang khoá | 200, `status` → 1 (không bị middleware chặn) |
| Sửa sau khi đã mở khoá | 200 |
| Vào URL `/43712/edit` trên trình duyệt | Đá về `/assign/customers/43712` + toast đúng |

⚠️ **Còn hở, chưa xử lý**: 3 route serial dùng param `{serialId}` (`updateSerial`, `changeSerial`,
`deleteSerial`) không mang `customer_id` nên middleware không suy ra được KH → **chưa được bảo vệ**.
Muốn chặn thì phải tra ngược serial → customer trong middleware hoặc trong controller. Chờ user chốt.

## Phase 4 — Tài sản chung

- [x] `.claude/skills/entity-history/SKILL.md`: thêm §0a + cập nhật câu hỏi §0.3 + checklist
- [x] `CLAUDE.md`: nguyên tắc "bản ghi đã khoá thì không cho sửa/xoá — chặn ở BE bằng 423, FE chỉ ẩn nút"
- [x] `CLAUDE.md` + `.claude/skills/list-page/SKILL.md` §7.2: nguyên tắc **hành động màn chi tiết phải
      khớp màn danh sách của đúng bản ghi đó — giống cả điều kiện hiện/ẩn, không chỉ giống danh sách nút**.
      Skill trước đây mới nói "footer có đủ hành động như dòng danh sách" nên không chặn được lỗi lệch
      điều kiện; đã bổ sung ví dụ sai điển hình + cách tự kiểm bằng 2 bản ghi khác trạng thái.

## Đã test (2026-08-15, FE :3002 / BE :8003, DB `local_hrm_erp`)

| Hạng mục | Kết quả |
| --- | --- |
| `filter-options` cho customer | 3 nhóm đúng thứ tự + 783 performers (giữ nguyên) |
| `filter-options` cho task / issue / handover / meeting / bom-list | **3 nhóm giống hệt nhau**, `performers` rỗng ✓ |
| Ánh xạ `groupOfAction` | Verify đủ **14 action** đang tồn tại + action lạ + `null` → đúng nhóm |
| Log KH 43712 | `lock` → `action_group = status`, `action_label` vẫn "Khóa khách hàng" |
| UI màn chi tiết KH 43712 | Dropdown đúng 3 option; timeline vẫn hiện "Khóa khách hàng" |
| Lọc thật | "Thay đổi trạng thái" → 1 mục; "Tạo mới" → 0 mục ✓ |
| Lint/compile | `php -l` sạch; 2 file `.vue` compile + parse OK |

### Checkpoint — 2026-08-15
Vừa hoàn thành: chuẩn hoá 3 nhóm hoạt động cho toàn bộ 10 màn có Lịch sử + ghi vào skill/CLAUDE.md.
Đang làm dở: —
Bước tiếp theo: user review. **Chưa port sang nhánh `tpe-develop-assign`** — nhánh đó cũng có
`SystemInfoSection.vue` + `SystemLogService`, nếu muốn đồng nhất cả 2 nhánh thì cần làm riêng
(xem mục dưới).
Blocked:

### Chưa làm — cần user quyết
Nhánh `tpe-develop-assign` (`hrm-client` + `hrm-api`) cũng có khối Lịch sử dùng chung. Thay đổi này
mới chỉ áp cho nhánh `gop_db`. Port sang nhánh kia hay để lần merge sau tự mang theo — chờ user chốt.

## Fix 2026-08-17 — Lịch sử danh mục địa danh ghi id thay vì tên

- [x] BE: thêm `app/Services/LocationNameResolver.php` (id → tên, cache theo request) cho nations/areas/provinces/districts/wards/hamlets
- [x] BE: `HamletService` — snapshot dựng lại đủ Quốc gia / Tỉnh-TP / Quận-Huyện suy từ `ward_id` (bảng `hamlets` chỉ có `ward_id` nên đổi cả Tỉnh/TP + Phường/xã mà log chỉ hiện Phường/xã); log update gọi thẳng `CatalogHistoryService::logUpdate`
- [x] BE: `WardService` / `DistrictService` / `ProvinceService` — `catalogDisplay` đổi khoá ngoại sang tên (cùng lỗi)
- [x] BE: `CatalogHistoryService::TABLES['hamlets']` thêm nhãn `nation_id` => Quốc gia
- [x] Test tinker: đổi ward khác tỉnh → 1 log 3 dòng Tỉnh/TP + Quận/Huyện + Phường/xã đều ra TÊN; đã xoá log test + trả lại dữ liệu

### Rà các màn khác dùng chung popup Lịch sử (2026-08-17)

- [x] Quét 18 service dùng `LogsCatalogHistory` + 2 màn log kiểu version (`accounts`, `type_accounts`) + `SystemLogService` (10 loại đối tượng Assign)
- [x] FE: bỏ cột Hành động + nút "Lịch sử" ở `pages/customer-care/serials/index.vue` (bảng `serials` không có chỗ nào ghi log → popup luôn rỗng; màn chỉ đọc). Giữ nguyên khai báo `serials` trong `CatalogHistoryService::TABLES` phòng khi sau này bổ sung ghi log
- [ ] **CHƯA SỬA (user để xem lại)** — Task / Vấn đề (Giao việc) log ra id thô: `SystemLogService::diffSnapshot()` chỉ map nhãn cho `status`, nên `assignee_id`, `approver_id`, `approved_by`, `parent_id`, `project_id`, `solution_id`, `solution_module_id`, `watcher_ids`, `priority`, `mode` (Task) và `creator_id`, `assignee_id`, `approver_id`, `detected_by`, `severity`, `impact_level`, `issue_type`, `detected_from`, `root_cause_group`, `tags` (Vấn đề) hiện ra số. Snapshot lưu id nên sửa ở tầng ĐỌC là log cũ cũng đúng theo
- [x] Không dính: tài khoản ngân hàng công ty (đã đổi `currency_id` → tên), `accounts` (`displayValue` đủ type/is_account_follow_dept/status), `type_accounts` (code hiện tại đúng, chỉ 2 dòng log cũ 04/08 còn lưu `2 → 1`), khu vực (lưu `nation_name`), khách hàng (`CustomerHistoryService` tra tên đủ), vụ việc / mã phí / tiền tệ / nguồn vốn / ngân hàng / quốc gia / mức độ / ghi chú bảo trì / lỗi thiết bị / dịch vụ / chi phí / phiếu chuyển hàng (không có select FK trong cột theo dõi)

## Fix 2026-08-18 — Lịch sử Đường/phố còn hiện Quận/Huyện (form đã bỏ ô này với VN)

- [x] BE: `HamletService` bỏ `district_id` khỏi `catalogColumns()` + `catalogSnapshot()` (log MỚI không còn dòng Quận/Huyện)
- [x] BE: `CatalogHistoryService` thêm `HIDDEN_FIELDS['hamlets'] = ['district_id', 'Quận/Huyện']`, lọc trong `changesOf()` → log CŨ đã ghi cũng không hiện; bỏ nhãn `district_id` khỏi `TABLES['hamlets']`
- [x] BE: `WardService` thêm `code` vào `catalogColumns()` + nhãn `'code' => 'Mã số'` trong `TABLES['wards']` (sửa Mã số ở màn Phường/xã trước đây không ghi lịch sử); đã rà 5 màn địa danh còn lại (quốc gia / khu vực / tỉnh-TP / quận-huyện / đường-phố) — cột theo dõi khớp đủ ô nhập trên form

## Rà soát 2026-08-18 — quét toàn bộ 22 bảng có Lịch sử (đối chiếu ô nhập trên form ↔ cột theo dõi ↔ nhãn)

Cách rà: liệt kê `catalogColumns()` của 19 service dùng `LogsCatalogHistory` + 2 màn log kiểu
version (`accounts`, `type_accounts`), so với `V2BaseLabel` trên form FE và với bản đồ nhãn
`CatalogHistoryService::TABLES`.

Đã sửa:
- [x] `costs` — ô "ĐM giảm giá (%)" sửa KHÔNG vào lịch sử: `discount` nằm ở bảng `company_costs` (mỗi công ty một mức) chứ không phải cột của `costs`, trait đọc `$model->discount` luôn ra null. Override `catalogSnapshot()` (alias `baseCatalogSnapshot`) đọc theo công ty hiện tại + `update()` gọi thẳng `logUpdate` với snapshot fresh (khuôn `HamletService`)
- [x] `services` — "Công ty quản lý" + "Hệ số giá bán gói bảo dưỡng" sửa không vào lịch sử → thêm `company_id` (log lưu TÊN công ty) + `coefficient_cost_price_service` vào cột theo dõi
- [x] `services` — sửa "Định mức đàm phán giá (%)" / "VAT (%)" hiện tên cột thô (`sale_max_percent`, `vat_percent`) vì thiếu nhãn → bổ sung nhãn (kèm nhãn cho hệ số giá bán)
- [x] `company_accounts` — đổi Ngân hàng hiện dòng `bank_name` (cột denormalized được theo dõi nhưng `TABLES` chỉ khai `bank_id`) → thêm nhãn `bank_name` => Ngân hàng, giữ `bank_id` cho log cũ
- [x] `banks` — đổi Logo không vào lịch sử (`logo` có nhãn nhưng không nằm trong cột theo dõi) → thêm `logo`, hiển thị TÊN FILE thay vì URL S3 dài 85 ký tự

Không phải lỗi (đã kiểm, ghi lại để lần sau khỏi rà lại): `levels` / `note_maintenances` (nhãn
`status`/`note` thừa — form không có ô đó, màn không có Khóa/Mở khóa), `device_errors`,
`currencies`, `works`, `cost_debts`, `source_capitals`, `nations`, `areas`, `provinces`,
`districts`, `hamlets`, `wards`, `accounts`, `type_accounts`, `bill_adjust_dept_requests`,
`product_transfer_requests` (form chỉ sửa Ghi chú) — cột theo dõi khớp form, snapshot đều chụp
TRƯỚC khi fill, mọi đường ghi (tạo / sửa / khóa / mở khóa / xóa) đều có log.

### Chưa sửa — cần user quyết
- `services`: file đính kèm (`attachments`) và các bảng con (gói bảo dưỡng con, công ty áp dụng, nhóm hàng hóa) đổi không sinh log. Muốn log thì phải tóm tắt kiểu `details_summary` như phiếu điều chỉnh công nợ
- `product_transfer_requests`: bảng chi tiết hàng hóa đổi không sinh log; `approver_id` có nhãn nhưng không theo dõi (chỉ đổi qua luồng duyệt, đã có log `change_status`)
- Task / Vấn đề (Giao việc) vẫn log id thô (mục đã ghi ở phần rà 2026-08-17)
