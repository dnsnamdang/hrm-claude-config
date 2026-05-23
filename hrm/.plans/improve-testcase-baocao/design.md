# Cải thiện file Testcase_baocao.xlsx — Design

## Mục đích

File `hrm-api/database/files/Testcase _baocao.xlsx` hiện không đủ thân thiện với người đọc end-user (QA/nghiệp vụ): cột "KQ thực tế" còn nhiều thuật ngữ kỹ thuật (tên trường DB, hằng số trạng thái), cột "Expected Result" ở nhiều testcase quá ngắn, và file thiếu phần giải thích chung mỗi báo cáo (lấy dữ liệu ở trạng thái nào, "thời gian" trong filter nghĩa là ngày gì, quy tắc cộng dồn).

Cải thiện file để người không phải dev đọc một mình cũng hiểu được.

## Phạm vi

Chỉ sửa 10 sheet báo cáo chính trong file. Các sheet khác giữ nguyên.

| Sheet | Báo cáo | Feature folder tham chiếu |
|---|---|---|
| 17. BC Theo dõi meeting | Meeting theo dự án | `.plans/meeting-by-projects/` |
| 18. Báo cáo meeting | Meeting theo nhân viên | `.plans/meeting-by-employees/` |
| 23. BC giải pháp theo PBKD | YCGP theo phòng kinh doanh | `.plans/solution-requests-by-department/` |
| 24. BC tổng hợp TKT theo PB NV | Dự án TKT theo phòng/NV | `.plans/customer-development-report/` hoặc tương đương |
| 30. BC hiệu suất NV theo DA | Hiệu suất NV theo dự án | `.plans/performance-by-employee/` |
| 31. BC hiệu suất làm việc theo GP | Hiệu suất theo giải pháp | `.plans/performance-by-solutions/` |
| 35. BC Version | Theo dõi chỉ số hoàn thành GP theo version | `.plans/solution-version-report/` / `progress-version-snapshot` |
| 36. BC TH GP theo Phòng ban | Tổng hợp GP theo phòng | `.plans/solutions-work-summary-by-department/` |
| 38. BCPBNL GANTT NV | Gantt nhân lực NV | (đọc trực tiếp code FE) |
| 39. BC phát triển KH theo NVKD | Phát triển KH theo NV KD | `.plans/customer-development-report/` |

## Format kết quả

Giữ 1 file `Testcase _baocao.xlsx` duy nhất, chỉ sửa 10 sheet trên. Backup file gốc thành `Testcase _baocao.xlsx.bak` trước khi chạy.

### Thay đổi 1 — Chèn khối "Mô tả báo cáo" lên đầu mỗi sheet

Chèn các rows mới phía trên hàng header testcase hiện tại. Hàng header testcase (`Module | Nhóm chức năng | TC ID | Chức năng | ...`) hiện ở hàng 6 → sẽ dời xuống ~hàng 16.

Khối mô tả gồm 8 dòng (mỗi dòng: cột A = label, cột B trở đi merge = nội dung):

1. **Mục đích báo cáo** — 1 câu, end-user friendly.
2. **Đối tượng được tính vào báo cáo** — entity nào, ở trạng thái nào (vd: "Cuộc họp đã hoàn thành thuộc dự án TKT đang hoạt động").
3. **Đối tượng bị ẩn / không tính** — các trạng thái/case không xuất hiện (vd: "Cuộc họp lên lịch, đang diễn ra, đã huỷ; dự án TKT ở trạng thái Nháp").
4. **Bộ lọc thời gian áp dụng cho** — giải thích rõ filter "thời gian" lọc theo ngày nào (vd: "Ngày cuộc họp diễn ra, không phải ngày tạo lịch họp").
5. **Cấu trúc cây phân cấp** — các cấp + ý nghĩa.
6. **Quy tắc cộng dồn ở dòng cấp cha** — cấp cha tổng những gì, đếm như thế nào.
7. **Phân quyền cấp** — các quyền có thể được cấp + ý nghĩa từng quyền (toàn tổng công ty / 1 công ty / 1 phòng / chỉ của mình).
8. **Ghi chú đọc bảng** (nếu có) — vd: "Khu vực thống kê tổng dưới bảng là tổng của toàn bộ kết quả sau filter, không phụ thuộc trang đang xem".

Style:
- Row label (cột A): nền xám nhạt, font đậm.
- Row content (cột B–S merge): wrap text, font thường.
- Có 1 dòng tiêu đề "MÔ TẢ BÁO CÁO" merge toàn dòng, nền vàng nhạt, đậm.
- Để 1 dòng trống ngăn cách giữa khối mô tả và khối "TEST SUMARY" gốc.

### Thay đổi 2 — Viết lại cột J ("KQ thực tế") theo ngôn ngữ end-user

Quét toàn bộ ô cột J của 10 sheet, thay các thuật ngữ dev bằng diễn đạt tiếng Việt thường. Bảng dịch chuẩn (áp dụng across sheets):

| Thuật ngữ dev | Ngôn ngữ end-user |
|---|---|
| `STATUS_TAO_NHAP` / `STATUS_DANG_TAO` / `Draft` | "trạng thái Đang tạo (bản nháp)" |
| `prospective_project.customer_name` | "tên khách hàng của dự án" |
| `meetings.code – meetings.name` | "mã – tên cuộc họp" |
| `start_date` / `start_time` / `end_time` | "ngày họp" / "giờ bắt đầu" / "giờ kết thúc" |
| `duration` | "thời lượng (phút)" |
| `total_duration` | "tổng thời lượng" |
| `meeting_type_name` | "tên loại cuộc họp" |
| `meeting_type_counts` | "số lượng theo từng loại cuộc họp" |
| `mode_id = 1` | "Trực tiếp" |
| `mode_id = 2` | "Online" |
| `total_participants` | "tổng số người tham gia" |
| `unique employee_id` | "đếm không trùng theo nhân viên" |
| `creator_name` | "tên người tạo" |
| `created_by → employee_infos.fullname` | "họ tên nhân viên đã tạo" |
| `current_page = 1` | "tự động về trang 1" |
| `time_mode = month` | "chế độ thời gian = Tháng/Năm" |
| `meeting_reports` | "biên bản cuộc họp" |
| `project_status_name` | "trạng thái hiện tại của dự án" |
| `name` (field reference) | "tên / tiêu đề" |
| `code` (field reference) | "mã" |
| Format `PREFIX-YYYY-NNNNN` | "mã định danh tự sinh (vd YCGP-2026-00012)" |

Các ô đã viết tiếng Việt rõ ràng (không chứa thuật ngữ dev) → giữ nguyên. Không sửa cho có.

### Thay đổi 3 — Mở rộng cột I ("Expected Result") cho các TC quá ngắn

Các TC ngắn dưới ~120 ký tự sẽ được rà soát và mở rộng. Đặc biệt nhóm phân quyền `TC-ROLE-01..05` ở các sheet 18, 23, 24, 30, 31, 35, 36 — hiện chỉ có 1 câu, sẽ viết thêm:
- Ai có quyền này (vai trò mẫu).
- User thấy gì cụ thể (phạm vi).
- User KHÔNG thấy gì (tương phản).
- 1 ví dụ ngắn.

Sheet 17 (BC Theo dõi meeting) đã viết khá đầy đủ → ít sửa.

### Thay đổi 4 — Chèn cột mới "Giải thích nghiệp vụ"

Vị trí: chèn cột mới ngay sau cột I (Expected Result), trước cột J (KQ thực tế) — trở thành cột J mới, các cột phía sau dồn 1 vị trí.

Header: "Giải thích nghiệp vụ" (font đậm, nền xám nhạt, wrap, rộng ~50 ký tự).

Nội dung:
- Chỉ điền cho các TC phức tạp hoặc dễ hiểu sai (filter, phân quyền, tính toán, cộng dồn, modal chip…).
- TC đơn giản (hiển thị header, expand/collapse, validation cơ bản) → để trống.
- Mỗi ô: 1–3 câu, có ví dụ cụ thể.

Ví dụ TC lọc thời gian:
> Bộ lọc thời gian ở báo cáo này lọc theo NGÀY HỌP THỰC TẾ (ngày cuộc họp đã diễn ra), không phải ngày tạo lịch. Chọn từ 01/01 → 31/03 sẽ chỉ thấy các cuộc họp đã họp trong quý I, kể cả nếu lịch được tạo từ tháng trước.

Ví dụ TC số người tham gia cấp cha:
> Số người tham gia ở dòng Phòng ban đếm UNIQUE: 1 nhân viên dự 5 cuộc họp chỉ tính là 1 người. Ở dòng cuộc họp thì là tổng số người dự cuộc họp đó (gồm cả khách).

## Cách triển khai

Viết 1 script Python (openpyxl) đặt tại `tools/improve_testcase_baocao.py` (hoặc thư mục tạm). Script:

1. Mở `hrm-api/database/files/Testcase _baocao.xlsx`, copy ra `.bak`.
2. Với mỗi sheet trong 10 sheet target:
   - Đọc nội dung mô tả + bảng dịch jargon từ data đã chuẩn bị sẵn trong script (mỗi sheet 1 dict).
   - Chèn cột "Giải thích nghiệp vụ" ngay sau cột I (`ws.insert_cols(idx=10)`).
   - Copy header style từ cột I sang cột J mới.
   - Điền giải thích nghiệp vụ vào các TC có trong dict (key = TC ID).
   - Chèn rows mô tả lên đầu (`ws.insert_rows(idx=1, amount=10)`), điền nội dung + style.
   - Cập nhật các merged cells (nếu có) bị ảnh hưởng — `MergedCellRange.shift(row_shift=10)` đã được openpyxl tự xử lý phần lớn, nhưng cần verify.
   - Quét cột J cũ (giờ là cột K sau khi chèn cột mới), áp bảng dịch jargon (regex/replace từng cặp).
   - Mở rộng cột I ở các TC ngắn theo data đã chuẩn bị.
3. Save file.

Trước khi viết script, đọc:
- Code BE: `Modules/Assign/Http/Controllers/Api/V1/*Report*Controller.php` + Service tương ứng.
- Code FE: `hrm-client/pages/assign/report/*` (vue files).
- `.plans/` của từng feature liệt kê ở bảng phạm vi.

Để biết chính xác từng sheet:
- Báo cáo lấy entity nào, từ bảng nào, trạng thái nào được tính.
- Filter "thời gian" trong code lọc theo cột nào → diễn dịch ra ngày gì với end-user.
- Permission key nào áp dụng cấp nào.

## Out of scope

- Không sửa testcase đã viết đúng (cột I rõ ràng, cột J không có jargon).
- Không thêm testcase mới (không phải nhiệm vụ — chỉ làm rõ TC hiện có).
- Không sửa 4 sheet không phải báo cáo (BOM list cũ, YCGP, Dự án TKT, "Bản sao của...").
- Không đổi tên TC ID, không đổi trật tự cột hiện có (trừ chèn 1 cột mới).

## Edge case / Lưu ý kỹ thuật

- **Merged cells trong khối TEST SUMARY (rows 1–5)** — sẽ bị shift xuống khi insert rows lên trên, openpyxl xử lý OK với `insert_rows()`. Cần test 1 sheet trước.
- **Style khi chèn rows mới**: openpyxl `insert_rows()` không tự copy style → script phải set style thủ công cho các ô mô tả.
- **Cột J cũ chứa formula** (J1..J5 là test summary count) → khi chèn cột "Giải thích nghiệp vụ", các formula refer tới cột J cần được cập nhật. Kiểm tra trước khi chèn — nếu không có formula thì OK, nếu có thì phải rebuild công thức.
- **Wrap text** cho ô mô tả + ô "Giải thích nghiệp vụ" để xuống dòng tự nhiên.
- **Row height** của row "MÔ TẢ BÁO CÁO" + 8 dòng nội dung: nên set auto-fit hoặc đủ lớn để wrap đọc được.
- **Validate sau khi chạy**: mở từng sheet trong Excel/Numbers, kiểm tra format không vỡ, đọc lại 1-2 TC bị sửa.

## Kết quả mong đợi

Người đọc bất kỳ (không phải dev) mở 1 sheet bất kỳ trong 10 sheet đã sửa:
1. Đọc khối "MÔ TẢ BÁO CÁO" đầu sheet → hiểu báo cáo là gì, lấy dữ liệu nào, filter thời gian nghĩa là gì, quy tắc cộng dồn.
2. Đọc cột "Expected Result (chi tiết)" → đủ chi tiết kể cả với TC phân quyền.
3. Gặp TC khó hiểu → đọc cột "Giải thích nghiệp vụ" có ví dụ cụ thể.
4. Đọc cột "KQ thực tế" → không gặp tên trường DB / hằng số code / từ tiếng Anh kỹ thuật.
