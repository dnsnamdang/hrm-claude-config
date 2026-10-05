# Plan — Đồng bộ tên thành phần lương với Bảng công chi tiết (#11328)

Nhánh: `tpe-develop-assign` · Repo: `hrm-api` (không đụng `hrm-client`)
Design: `.plans/salary-composition-name-match-timesheet/design.md`

## Phase 1 — Đổi tên + mô tả (BE, data-only)

- [x] 1.1 Migration `2026_09_08_000001_rename_system_salary_compositions_match_timesheet.php`
  - [x] Bảng map 10 mã: `code` / tên cũ / tên mới (9 mã Nhóm 1 + `THOI_GIAN_LAM_THEM_HUONG_LUONG_THEO_GIO_CO_HS` sửa dấu cách)
  - [x] Update `system_salary_compositions` theo `code`, **không lọc `status`**
  - [x] Update `salary_compositions` theo `code` **và** `name` = tên cũ (không đè tên người dùng tự sửa)
  - [x] Bỏ qua + `Log::warning` khi tên mới đã bị bản ghi khác chiếm
  - [x] `down()` đảo ngược đầy đủ
- [x] 1.2 Cùng migration: cập nhật `description` nêu rõ cách tính cho 5 mã
  (`TONG_VDM_QUY_DOI`, `BU_TRU_CONG_HANH_CHINH_SAU_QUYET_TOAN`, `TONG_CONG_HUONG_LUONG`,
  `CONG_CA_DEM`, `CONG_CONG_GIAM_TRU`) — chỉ ghi đè khi mô tả còn đúng bản gốc / đang rỗng
- [x] 1.3 Kiểm độ dài mô tả — dài nhất 208 ký tự, đều ≤ 255 (`description` là `varchar(255)`)

## Phase 2 — Bổ sung 3 thành phần lương mới (BE)

- [x] 2.1 Migration `2026_09_08_000002_add_system_salary_compositions_from_timesheet.php`
  - [x] `NGHI_THAI_SAN` — "Nghỉ thai sản" — cột (17)
  - [x] `TONG_CONG_DI_LAM` — "Tổng công đi làm" — cột (4)
  - [x] `TONG_NGHI_HUONG_LUONG` — "Cộng nghỉ hưởng lương" — cột (8)
  - [x] `type = 2`, `feature = 3`, `value_type = 1`, `status = 1`, `formula = null`
  - [x] Kiểm tra trùng `code` / trùng `name` trước khi insert; `down()` chỉ xoá khi chưa công ty nào lấy về dùng
- [x] 2.2 `CreateEmployeePayroll::calcData` — thêm 3 mã vào `$cham_congs` + 3 `case`
- [x] 2.3 `SalaryService::calcData` — thêm 3 mã vào `$cham_congs` + 3 `case`

## Phase 3 — Đồng bộ seeder

- [x] 3.1 `SystemSalaryCompositionSeeder`: sửa `name` 10 mã + `description` 5 mã (chỉ block đang hoạt động, bỏ qua block đã comment)
- [x] 3.2 `SystemSalaryCompositionSeeder`: thêm 3 block insert cho 3 mã mới (id 41, 42, 43)

## Phase 4 — Kiểm tra

- [x] 4.1 `php -l` sạch cho cả 5 file (2 migration mới + 3 file sửa)
- [x] 4.2 `git diff --stat` gọn (124 thêm / 17 sửa), CRLF nguyên vẹn — seeder 1407/1407 dòng còn `\r`
- [ ] 4.3 User tự chạy `php artisan migrate` (KHÔNG tự chạy — quy tắc không đụng DB)
- [ ] 4.4 Verify sau migrate: xem 4 bước ở cuối `design.md`

## Treo — chờ khách trả lời

- [ ] `CONG_DI_DUONG`: chốt nguồn dữ liệu (bảng tổng hợp công hay đề nghị thanh toán KT duyệt) rồi mới ghi mô tả
- [ ] Mục #24: tách VĐM theo từng hệ số — chờ khách chốt danh sách hệ số (hiện có 7 giá trị, 1 giá trị rỗng cần dọn trước)

## Treo — lỗi có sẵn, chờ quyết định riêng (chi tiết ở design.md)

- [ ] 3 thành phần luôn trả 0 (`BU_TRU_...` thiếu trong `$cham_congs`; `NGHi_KHONG_LY_DO` / `NGHi_HUONG_BHXH` sai hoa thường)
- [ ] `SalaryService::calcData` thiếu 9 mã so với `CreateEmployeePayroll::calcData`
- [ ] `TONG_VDM_QUY_DOI` lệch cột (3) do cách làm tròn
- [ ] `OvertimeHour::getAllRatio()` không lọc hệ số rỗng (cột rác `VĐM 1(x-)`) và không lọc `company_id`

---

### Checkpoint — 2026-09-08

Vừa hoàn thành: toàn bộ Phase 1-3 + kiểm tra Phase 4.1/4.2. Khách đã duyệt bảng đối chiếu
(file `Phản hồi_ Xác nhận tên thành phần lương.xlsx`), tài liệu gửi khách là
`Doi chieu ten thanh phan luong - Loi 11328.xlsx` ở thư mục gốc dự án.

File đã tạo/sửa (đều trong `hrm-api`, CHƯA commit):
- (mới) `Modules/Payroll/Database/Migrations/2026_09_08_000001_rename_system_salary_compositions_match_timesheet.php`
- (mới) `Modules/Payroll/Database/Migrations/2026_09_08_000002_add_system_salary_compositions_from_timesheet.php`
- (sửa) `Modules/Payroll/Jobs/CreateEmployeePayroll.php` — `$cham_congs` + 3 `case` trong `calcData`
- (sửa) `Modules/Payroll/Services/SalaryService.php` — `$cham_congs` + 3 `case` trong `calcData`
- (sửa) `Modules/Payroll/Database/Seeders/SystemSalaryCompositionSeeder.php` — 10 name, 5 description, 3 block mới

Đang làm dở: không có.

Bước tiếp theo: user chạy `php artisan migrate` rồi verify theo 4 bước ở `design.md`; song song hỏi
khách nốt 2 mục treo (nguồn Công đi đường, danh sách hệ số VĐM).

Blocked: 2 mục treo chờ khách; 4 lỗi có sẵn chờ user quyết có tách issue riêng không.
