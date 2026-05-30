# Cải thiện Testcase_baocao.xlsx — Plan

**Mục tiêu:** Sửa file `hrm-api/database/files/Testcase _baocao.xlsx` để end-user đọc hiểu được — chèn mô tả báo cáo, dịch jargon dev, mở rộng TC ngắn, thêm cột Giải thích nghiệp vụ.

**Spec:** `.plans/improve-testcase-baocao/design.md`

---

## Phase 1 — Chuẩn bị: đọc code 10 báo cáo, gom nội dung mô tả

### Đọc code + spec (BE + FE) để gom dữ kiện mô tả cho mỗi sheet
- [x] Sheet 17 (Theo dõi meeting theo dự án) — đọc `Modules/Assign/...MeetingByProjects*` + `pages/assign/report/meeting-by-projects/*` + `.plans/meeting-by-projects/design.md`
- [x] Sheet 18 (Meeting theo nhân viên) — đọc `Modules/Assign/...MeetingByEmployees*` + `pages/assign/report/meeting-by-employees/*` + `.plans/meeting-by-employees/design.md`
- [x] Sheet 23 (YCGP theo PBKD) — đọc `Modules/Assign/...SolutionRequestsByDepartment*` + `.plans/solution-requests-by-department/design.md`
- [x] Sheet 24 (Tổng hợp TKT theo PB NV) — tìm controller/page tương ứng + plan
- [x] Sheet 30 (Hiệu suất NV theo dự án) — đọc `.plans/performance-by-employee/design.md` + code
- [x] Sheet 31 (Hiệu suất theo giải pháp) — đọc `.plans/performance-by-solutions/design.md` + code
- [x] Sheet 35 (Version giải pháp) — đọc `.plans/solution-version-report/` hoặc `progress-version-snapshot/` + code
- [x] Sheet 36 (TH GP theo phòng ban) — đọc `.plans/solutions-work-summary-by-department/design.md` + code
- [x] Sheet 38 (Gantt nhân lực NV) — đọc code FE/BE trực tiếp
- [x] Sheet 39 (Phát triển KH theo NVKD) — đọc `.plans/customer-development-report/design.md` + code

### Output Phase 1
- [x] Tạo file `.plans/improve-testcase-baocao/sheet-data.md` — chứa 10 block (1 block/sheet), mỗi block 8 trường mô tả + dict TC khó cần giải thích nghiệp vụ
- [ ] Checkpoint: confirm với user nội dung mô tả từng sheet trước khi viết script

---

## Phase 2 — Viết script Python sửa Excel

### Setup
- [x] Tạo file `tools/improve_testcase_baocao.py`
- [x] Backup: copy `hrm-api/database/files/Testcase _baocao.xlsx` → `Testcase _baocao.xlsx.bak`

### Module dữ liệu
- [x] Hàm `get_sheet_data(sheet_name)`: trả về mô tả 8 dòng + dict TC giải thích nghiệp vụ + dict mở rộng cột I (port từ `sheet-data.md`)
- [x] Constant `JARGON_DICT`: bảng dịch chuẩn (xem design.md mục Thay đổi 2), apply theo thứ tự dài → ngắn

### Hàm xử lý 1 sheet
- [x] `insert_jargon_column(ws)`: chèn cột mới sau cột I, copy style header, set độ rộng + wrap
- [x] `fill_jargon_explanations(ws, tc_dict)`: điền nội dung vào cột J mới theo TC ID
- [x] `expand_short_expected(ws, expand_dict)`: append/replace nội dung cột I cho TC ngắn
- [x] `translate_actual_result(ws)`: quét cột K (cột J cũ sau shift), apply JARGON_DICT regex replace
- [x] `prepend_description_block(ws, desc_data)`: chèn 10 rows lên đầu (1 row trống + 1 row tiêu đề + 8 row label/content), set style

### Main flow
- [x] Hàm `process_sheet(wb, sheet_name)`: gọi 5 hàm trên theo thứ tự (insert col → fill jargon → expand short → translate actual → prepend block)
- [x] Lặp qua list 10 sheet, gọi `process_sheet`
- [x] Save file overwrite

### Edge cases trong script
- [x] Verify trước: chạy lượt đọc-only, in số rows chứa jargon ở mỗi sheet → kiểm dict đủ chưa
- [x] Verify formula ở J1..J5 (test summary) — cập nhật reference nếu có
- [x] Verify merged cells khối TEST SUMARY shift xuống đúng

---

## Phase 3 — Chạy + verify

- [x] Chạy script trên 1 sheet thử (sheet 17), 9 sheet còn lại comment-out
- [x] Mở file kiểm sheet 17: khối mô tả + cột giải thích + cột KQ thực tế đã dịch + layout không vỡ
- [x] Báo user xem sheet 17 trước, lấy feedback
- [x] Tinh chỉnh script (fix merged cells + shift formula cột/row)
- [x] Chạy full 10 sheet, save file
- [x] Quét nhanh từng sheet kiểm tra (A1/A2/A9/J16 + jargon check)
- [ ] Báo user nhận file cuối

---

## Checkpoint — 2026-05-22

**Vừa hoàn thành:** Phase 1 (10 agent gom dữ kiện) + Phase 2 (viết script `tools/improve_testcase_baocao.py`) + Phase 3 (chạy + fix 2 bug: merged cells không shift, formula không shift col/row sau insert).

**File đã sửa:** `hrm-api/database/files/Testcase _baocao.xlsx` — 10 sheet báo cáo đều có:
- Khối "MÔ TẢ BÁO CÁO" 9 dòng đầu sheet
- Cột mới "Giải thích nghiệp vụ" sau cột I
- Cột "KQ thực tế" đã dịch jargon dev sang tiếng Việt

**Backup giữ ở:** `Testcase _baocao.xlsx.bak`

**Bước tiếp:** User mở file kiểm tra — nếu OK thì xóa .bak + sheet-data.md (Phase 4).

---

## Phase 4 — Cleanup

- [ ] Xác nhận với user file OK
- [ ] Xóa file `.bak` (hoặc giữ tùy user)
- [ ] Xóa file tạm `sheet-data.md` nếu không cần
- [ ] Quyết định giữ/xóa script `tools/improve_testcase_baocao.py`

---

## Lưu ý

- Phase 1 tốn thời gian nhất. Có thể dispatch nhiều Explore subagent song song theo từng sheet để tăng tốc.
- Phase 2–3 chạy tuần tự sau khi Phase 1 confirm.
- Mọi thay đổi rollback được từ `.bak` — an toàn.
