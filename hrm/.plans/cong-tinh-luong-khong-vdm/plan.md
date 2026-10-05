# Plan — Công tính lương (không VĐM, không đi đường) — Redmine #11457

## Phase 1 — Bảng công chi tiết (FE) ✅

- [x] `pages/timesheet/timesheet_details/index.vue`: chèn `<b-th>` "Công tính lương (13)" + tooltip `(13) = (1)+(8)-(11)` ngay trước cột tổng cũ
- [x] Đổi số hiệu cột cũ: (13)→(14) + tooltip `(14) = (4)+(8)-(11)+(12)`; (14)→(15)…(17)→(18); (18)→(19) + tooltip `(19) = (15)+(16)+(17)+(18)`
- [x] `getData()`: `item.push(...)` giá trị cột mới, chèn sau `cong_truy_thu`, KHÔNG cap công định mức
- [x] Kiểm `openDetail()` vẫn đúng offset `+2` / `+22` — cột mới ở offset 23, không đụng
- [x] `components/export-excel/timesheet_details.vue`: thêm `row.cong_tinh_luong` + `columns.push` + tiêu đề, đổi số hiệu

## Phase 2 — Bảng công tổng hợp ✅

- [x] `pages/timesheet/timesheet_summaries/_id/index.vue`: thêm `<b-th>` "Công tính lương (13) = (1)+(8)-(11)" + đổi số hiệu (13)→(14), (14)→(15)…(18)→(19)
- [x] Thêm `<b-td>` giá trị cột mới (chỉ đọc, tính inline từ các ô đang nhập nên tự cập nhật khi sửa tay)
- [x] `colspan` dòng tên phòng ban 30 → 31
- [x] ~~BE trả thêm field~~ — KHÔNG cần: FE cộng inline từ `working_general` + `work_day_phep`/`holiday`/`work_day_che_do` − `punishment_rule` (đều đã có sẵn)
- [x] Export Excel: KHÔNG phải sửa `components/export-excel/timesheet_month_summaries.vue` (component này đã bị comment ở dòng 31, không dùng). Export thật chạy ở BE → sửa `hrm-api/resources/views/exports/timesheet_summary_detail.blade.php`

## Phase 3 — Thành phần lương hệ thống (BE) ✅

- [x] `SystemSalaryCompositionSeeder.php`: thêm bản ghi id 41 `CONG_TINH_LUONG` / "Công tính lương", type=2, feature=3, value_type=1, description ghi rõ công thức
- [x] `Jobs/CreateEmployeePayroll.php`: thêm vào `$cham_congs` + `case 'CONG_TINH_LUONG'`
- [x] `Services/SalaryService.php`: thêm y hệt (switch nhân bản 2 nơi)
- [x] Chạy seeder trên DB local (`hrm_prod_local`), màn `/payroll/salarycomposition/system-category` đã thấy `CONG_TINH_LUONG` / "Công tính lương" (39 → 40 bản ghi, id 41)

## Phase 4 — Kiểm thử ✅ (22/09/2026, Playwright + tinker, DB `hrm_prod_local`, kỳ 06/2026)

- [x] BE `calcData('CONG_TINH_LUONG')` khớp công thức trên 6 nhân viên (cả 2 đường: `SalaryService` và mảng `$cham_congs`)
- [x] Bảng công chi tiết: tiêu đề đủ (1)…(19), không trùng số; Ngô Thị Hằng 21 + 3 − 0,05 = **23,95** ✅; Trần Hồng Nhung CTL **24** vs Tổng (14) **45,06** (chênh đúng phần VĐM 21,06) ✅
- [x] Tooltip cột mới hiện `(13) = (1)+(8)-(11)` ✅
- [x] Popup "Chi tiết công đi đường" (offset cứng +2) và ô truy thu (+22) vẫn mở đúng — cột mới ở offset 23 không phá
- [x] Excel bảng công chi tiết (FE dựng): cột "Công tính lương (13)" nằm trước "Tổng công tính lương (14)", số khớp màn hình trên 6 NV có VĐM
- [x] Bảng công tổng hợp: cột mới hiện ở **cả 2 kiểu xem** (Tổng hợp / Chi tiết), giá trị 23,95 khớp
- [x] Sửa tay ô Phép 3 → 5 thì cột (13) tự nhảy 23,95 → 25,95 (tính inline, không cần bấm Lưu) ✅ — đã tải lại trang, DB không đổi
- [x] Excel bảng công tổng hợp (BE blade): có cột mới, Ngô Thị Hằng ra 23,95 | 23,95 ✅

Ảnh: `.plans/cong-tinh-luong-khong-vdm/screenshots/`

## Công cụ test

- `seed-test-data.php` — script tạo data test 6 ca (công thường / phép / lễ / chế độ / đi muộn-về sớm / làm thêm) cho 1 NV + 1 tháng, in kèm bảng giá trị kỳ vọng. Đã chạy và đối chiếu khớp 100% (22/09/2026, mã 10610024 tháng 08/2026).
- `huong-dan-tao-data-test.md` — hướng dẫn tạo data test cho QA: nguồn dữ liệu 2 màn, thứ tự tạo, 2 cột chỉ test được ở bảng tổng hợp, cách xoá, 3 cái bẫy.

---

### Checkpoint — 22/09/2026
Vừa hoàn thành: code Phase 1-3 + chạy seeder + test đủ 3 màn và 2 file Excel. Tất cả khớp công thức.
Đang làm dở: không.
Bước tiếp theo: chờ task Redmine #11457 duyệt giá → commit/push (chưa commit theo quy ước).
Blocked: ⚠️ `SystemSalaryCompositionSeeder` `truncate()` bảng `system_salary_compositions` trước khi insert — chạy trên server thật cần cân nhắc, hoặc thay bằng 1 lệnh insert riêng cho id 41.
