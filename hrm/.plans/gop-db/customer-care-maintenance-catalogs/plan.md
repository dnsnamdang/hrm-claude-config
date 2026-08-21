# Plan — 2 danh mục bảo dưỡng (phân hệ CSKH)

> Phụ trách: @junfoke · Tạo 2026-08-03
> Design: `.plans/gop-db/customer-care-maintenance-catalogs/design.md`

## Phase 0 — Khảo sát ERP

- [x] Route `levels` + `note_maintenances`, 2 controller `Sale\LevelController` /
      `Sale\NoteMaintenanceController`, 2 model, 5 file view, 4 request class
- [x] Soi bảng: `levels` 29 dòng (không audit), `note_maintenances` 11 dòng (có
      `created_by`/`updated_by` varchar lưu ERP employee id)
- [x] Xác định phân hệ đích: **CSKH** (`customer-care`, `permissionType = 24`) theo sheet gộp
- [x] Đếm ràng buộc xóa thật: `level_id` ở 6 bảng, `note_maintenance_id` ở 1 bảng (9/11 đang dùng)
- [x] Phát hiện 4 lỗi/thiếu sót bản ERP (xem design.md)

## Phase 1 — Gỡ bỏ lớp map ERP employee (user báo giữa chừng)

- [x] ~~Tách `app/Helper/ErpEmployeeHelper.php`~~ → **user báo đã gộp `employees` +
      `employee_infos`, chỉ còn 1 bảng** nên helper là thừa. Đã xóa hẳn + revert `composer.json`
- [x] Kiểm chứng trước khi gỡ: commit `gộp bảng employees: HRM đọc lại bảng employees chung`,
      `TpEmployee::$table = 'employees'`, bảng tạo lại 2026-08-03 08:48; `hrm_employees` là bản cũ
      (lệch 290 id, 164 `employee_info_id`) → **không dùng nữa**
- [x] `FinanceService`: 3 hàm map → 1 hàm `currentEmployeeId()` = `auth()->user()->id`
- [x] Xóa `Modules\Finance\Entities\ErpEmployee`, chuyển 4 quan hệ sang
      `Modules\Human\Entities\Employee` (cùng bảng `employees`)
- [x] Model dùng chung không có accessor `display_name` → thêm `employeeDisplayName()` vào
      `Account` / `TypeAccount` để ghép `"MÃ - Họ tên"`, **không sửa model dùng chung**
- [x] Đổi request attribute `erp_employee_id` → `current_employee_id`
- [x] Bộ lọc Người tạo/Người cập nhật 2 màn tài khoản: bỏ bước map, dùng thẳng id
- [x] Verify 3 màn Tài chính cũ vẫn chạy: tên người tạo hiện đúng
      (`created_by=34` → `11710160 - Đào Thị Thúy`), 39 route Finance còn nguyên
- [x] Không còn tham chiếu `hrm_employees` nào trong `app/` và `Modules/`

## Phase 2 — BE: dựng nội dung `Modules/CustomerCare` (module trước đó rỗng hoàn toàn)

- [x] `Entities/Level/Level.php` — `USED_BY` **6 bảng**, `usedIn()` / `isCanDelete()`
- [x] `Entities/NoteMaintenance/NoteMaintenance.php` — `USED_BY` 1 bảng; `created_by`/`updated_by`
      là **varchar** nên ép chuỗi khi ghi
- [x] 2 Resource, 2 Service, 2 Request, 2 Controller
- [x] `Routes/api.php` — **16 route** dưới `/v1/customer-care`
- [x] 2 lớp Excel export + 2 blade

## Phase 3 — Quyền (4 quyền ĐẦU TIÊN của phân hệ CSKH, `type = 24`)

- [x] id **1115-1118** vào seeder, `group = 'Danh mục dịch vụ bảo dưỡng'` (duy nhất toàn hệ thống)
- [x] Insert tay vào DB local + cấp cho cùng bộ vai trò/công ty của quyền 1107
- [x] Khối "Phân hệ CSKH" trên màn Phân quyền **đã có sẵn** nhờ đợt sắp xếp theo registry
      (xem [[project_permission_screen_subsystem_order]]) — không phải sửa `Permission.vue`

## Phase 4 — FE

- [x] Mở khóa 2 mục trong `components/subsystem-menu/customer-care.js`
- [x] `pages/customer-care/levels/index.vue` + `components/modal/customer-care/level-modal.vue`
- [x] `pages/customer-care/note-maintenances/index.vue` +
      `components/modal/customer-care/note-maintenance-modal.vue`
- [x] Áp sẵn 3 bài học đã rút: `key` cột sortable trùng tên trường BE, ép `Number()` cho `meta`,
      `page`/`per_page` tách khỏi `filters` + `DedupeLoadMixin`

## Phase 5 — Verify

- [x] Chặn xóa trên dữ liệu thật: `Cấp 1 (6T)` → *Gói bảo dưỡng, Cấp bảo dưỡng của gói dịch vụ,
      Báo giá dịch vụ*; ghi chú id 1 → *Cấp bảo dưỡng của gói dịch vụ*; tìm được cả bản ghi
      xóa được (`Cấp 2 (6T)`, 4 ghi chú)
- [x] CRUD round-trip cả 2 màn, `key_name` tự viết HOA, `description` rỗng → NULL
- [x] Validate: rỗng / trùng tên / trùng ký hiệu / mô tả > 255 ký tự
- [x] Lọc + sort + getAll + export xlsx (80KB mỗi file)
- [x] 16 route CSKH + 39 route Finance đăng ký đủ
- [x] `php -l` toàn bộ + compile 4 file Vue
- [x] DB nguyên trạng: `levels` 29, `note_maintenances` 11
- [ ] ⏳ Chưa verify bằng mắt trên browser (chưa đăng nhập được phiên Playwright)

## Phase 6 — Bugfix: ẩn/disable nút Xóa khi ghi chú đang được dùng (@junfoke)

- [x] BE: `NoteMaintenanceResource` trả thêm `can_delete` (dùng `isCanDelete()` sẵn có của entity)
- [x] FE: nút Xóa ở list disable + tooltip khi `item.can_delete === false` (thay vì luôn cho bấm rồi mới toast chặn)

### Checkpoint — 2026-08-05
Vừa hoàn thành: rà nguyên nhân — entity đã có `isCanDelete()`/`usedIn()`, controller đã chặn, nhưng Resource không trả cờ và FE luôn hiện nút Xóa
Đang làm dở: sửa Resource + trash button trong index.vue
Bước tiếp theo: verify trên browser (ghi chú id 1 đang dùng → nút Xóa xám/disable; ghi chú xóa được → bấm bình thường)
Blocked:

## Phase 7 — Bugfix: màn Levels trùng 2 bộ lọc tìm kiếm (@junfoke)

- [x] Component chung `V2BaseFilterPanel`: thêm prop `showAdvancedToggle` (default true) để ẩn nút "Tìm kiếm nâng cao"
- [x] `pages/customer-care/levels/index.vue`: bỏ trường "Tên cấp" ở nâng cao (trùng ô tìm nhanh — BE `LevelService::index` lọc cả `keyword` lẫn `name` trên cùng cột `name`), set `:showAdvancedToggle="false"`, dọn `name` khỏi filter + import `V2BaseLabel`/`V2BaseInput` không dùng

### Checkpoint — 2026-08-05
Vừa hoàn thành: gộp 2 bộ lọc tên cấp về 1 ô tìm nhanh, ẩn toggle nâng cao rỗng
Đang làm dở: —
Bước tiếp theo: verify browser (màn levels chỉ còn 1 ô tìm nhanh, không còn nút "Tìm kiếm nâng cao"; các màn khác dùng V2BaseFilterPanel vẫn còn toggle như cũ)
Blocked:

## Việc còn lại

- [ ] ⚠️ **Rà `ErpPermissionHelper` sau khi gộp bảng**: `app/Helpers/ErpPermissionHelper.php` vẫn
      đọc qua `mysql2` (DB ERP cũ), còn được gọi ở `Modules/Assign` (CustomerService,
      MeetingController, ProductProjectController, CustomerManagerService) và
      `app/Helper/CustomerOwnership.php`. Gộp bảng xong thì phần này nên bỏ luôn — ngoài phạm vi
      2 màn này
- [ ] Chạy seeder quyền trên môi trường thật (local đã insert tay)

## Phase — Tai lieu ban giao (2026-08-13)

- [x] `testcase - Cap dich vu bao duong.xlsx` — 75 TC (P0 56%)
- [x] `testcase - Danh muc ghi chu kiem tra bao duong.xlsx` — 75 TC (P0 55%)
- [x] `HDSD_Cap dich vu bao duong.docx` — 11 trang
- [x] `HDSD_Danh muc ghi chu kiem tra bao duong.docx` — 11 trang
- [x] Generator chung: `gen_testcase.py`, `gen_hdsd.py`; anh nguon `hdsd_shots/` (CHI LOCAL)
- [x] Da xoa `testcase.xlsx` cu (format 15 cot) — user chot 2026-08-13
- [x] User cap quyen "Quan ly ghi chu kiem tra bao duong" -> da CHUP LAI anh danh sach
      (co du nut Tao moi / Sua / Xoa) va bo sung anh cua so Them; sinh lai ca TC va HDSD.
      Phat hien them: ca 2 man deu co nut "Luu & Tiep tuc" — truoc do tai lieu ghi thieu


---

## Làm lại 3 loại tài liệu theo form mới — 18/08/2026

> @junfoke · Bản tài liệu cũ (12–13/08) làm theo **form SRS 6 chương đã bị thay**. User yêu cầu
> dựng lại theo form 4 phần chốt ngày 17/08 và xoá các file không đạt chuẩn.

### Đã xoá
- `srs.docx` và `srs.html` — bản HTML/docx generic của đợt đầu, không theo form nào.
- Các `HDSD_*.docx` / `testcase*.xlsx` bản 13/08 (tên không dấu) — đã có bản mới thay thế.
- Thư mục `hdsd_shots/` cũ — ảnh mới nằm ở thư mục `*_shots/` riêng của từng nhóm.

### Bộ sinh dùng chung
Ba thư viện mới đặt ở `.plans/gop-db/_catalog_docs_lib/`, dùng chung cho cả 7 màn:

| File | Vai trò |
|---|---|
| `catalog_srs.py` | Dựng SRS đủ 4 phần, sinh mục 2.x theo danh sách `funcs` của từng màn |
| `catalog_tc.py` | Dựng testcase, tự sinh ca kiểm tra bắt buộc / trùng từ danh sách `truong` |
| `catalog_hdsd.py` | Dựng HDSD click-by-click, bảng ô nhập + bảng lỗi + câu hỏi thường gặp |

Mỗi feature chỉ còn 1 file cấu hình (`*_config.py`) và 3 driver mỏng gọi thư viện chung.

⚠️ `tc_engine` dùng chung chỉ hỗ trợ **tối đa 10 mục La Mã**. Màn nào nhiều chức năng hơn
(Danh mục tài khoản) thì `catalog_tc.py` tự **gộp nhóm cuối** — kết xuất, in ấn, tùy chỉnh hiển
thị và trải nghiệm — vào một mục, thay vì sửa engine dùng chung.

### Kết quả nhóm này

- [x] Ảnh: **16** trong `mt_shots/`, chụp trên cổng dev `hrm-crm.eteksofts.com`
- [x] `SRS - Cấp dịch vụ bảo dưỡng.docx` — 23 trang, 30 bảng, 14 ảnh, FR-01…FR-09, BR-01…BR-06
- [x] `SRS - Danh mục ghi chú kiểm tra bảo dưỡng.docx` — 24 trang, 30 bảng, 14 ảnh
- [x] `testcase - Cấp dịch vụ bảo dưỡng.xlsx` — **70 TC**, P0 53%
- [x] `testcase - Danh mục ghi chú kiểm tra bảo dưỡng.xlsx` — **72 TC**, P0 54%
- [x] `HDSD_Cấp dịch vụ bảo dưỡng.docx` — 15 trang · `HDSD_Danh mục ghi chú…docx` — 15 trang

### Ghi nhận khi chụp ảnh

**Tài khoản test chỉ có quyền XEM ở màn Ghi chú.** Tài khoản `namdangit@gmail.com` có
`Xem ghi chú kiểm tra bảo dưỡng` nhưng **không có** `Quản lý ghi chú kiểm tra bảo dưỡng`.
Hệ quả: nút Tạo mới / Sửa / Xóa bị ẩn — đúng thiết kế, và tình cờ là bằng chứng sống cho
mục phân quyền của tài liệu.

⚠️ **Còn thiếu 1 ảnh**: hộp thoại xác nhận Xóa của màn Ghi chú. Luồng xóa gọi kiểm tra tình
trạng sử dụng trước khi mở hộp thoại, máy chủ trả về từ chối vì thiếu quyền nên hộp thoại
không mở được. Cần cấp quyền `Quản lý ghi chú kiểm tra bảo dưỡng` cho tài khoản test rồi
chụp bổ sung; SRS hiện dùng ảnh danh sách cho mục này.

**Cần kiểm chứng trên dữ liệu**: 6 bản ghi test (`Trang test 002`…`007`, tạo 04/08/2026) đều
trả về không xóa được, dù mới tạo và nhiều khả năng chưa gắn vào gói dịch vụ nào. Chưa đủ căn
cứ kết luận là lỗi — cần soi dữ liệu bảng liên kết cấp bảo dưỡng để xác nhận.
