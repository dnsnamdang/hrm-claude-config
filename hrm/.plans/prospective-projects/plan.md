# Plan — Quản lý dự án TKT (/assign/prospective-projects)

## Fix: Label filter "Nhân viên" → "Nhân viên KD phụ trách" (2026-07-13)

- [x] FE: Đổi label `V2BaseLabel` "Nhân viên kinh doanh" → "Nhân viên KD phụ trách" (index.vue dòng 27)
- [x] FE: Đổi placeholder select `main_sale_employee_id` → "Nhân viên KD phụ trách" (index.vue dòng 32)
- [x] Xác nhận filter BE: `ProspectiveProjectService::index` đã filter `where('main_sale_employee_id', ...)` = đúng NV KD phụ trách (dòng 93-94) → không cần sửa BE

## Fix 2: Gộp 2 select nhân viên → chỉ còn "Nhân viên KD phụ trách" cascade (2026-07-13)

Bối cảnh: màn đang có 2 select — "Nhân viên" (của `V2BaseCompanyDepartmentFilter`, field `employee_id`, không dùng ở BE) và "Nhân viên KD phụ trách" (`main_sale_employee_id`). Gây hiểu nhầm.

- [x] FE: Ẩn select "Nhân viên" thừa → thêm `:disable_employee="true"` cho `V2BaseCompanyDepartmentFilter`
- [x] FE: Select "Nhân viên KD phụ trách" dùng options cascade theo Công ty→Phòng ban→Bộ phận (computed `mainSaleEmployeeOptions` + `mainSaleEmployeeAvailable`, replicate permission-scope + cascade của component)
- [x] FE: `:disabled="!filters.department_id"` — enable khi đã chọn Phòng ban (Bộ phận optional lọc thêm)
- [x] FE: Reset `main_sale_employee_id` khi đổi company/department/part (3 watcher)
- [x] Verify: BE `index()` filter `main_sale_employee_id` không đổi (đã đúng)

### Ghi chú
- `main_sale_employee_id` chính là "NV KD phụ trách" (xác nhận qua comment service dòng 1148). BE đã filter đúng, chỉ label FE gây hiểu nhầm.

### Checkpoint — 2026-07-13
Vừa hoàn thành: Fix 1 (đổi label) + Fix 2 (gộp 2 select nhân viên → 1 select "Nhân viên KD phụ trách" cascade Công ty→Phòng ban→Bộ phận, disable đến khi chọn Phòng ban). FE-only.
Đang làm dở: (không)
Bước tiếp theo: user build FE + test trên UI (chỉ còn 1 select nhân viên; chọn Phòng ban mới enable; lọc dự án theo NV KD phụ trách; đổi Công ty/Phòng ban → reset).
Blocked: (không)
# Plan — HDSD màn Dự án tiềm năng

## Phase 1 — Viết HDSD Word (Dự án tiềm năng / dự án tiền khả thi)

### Khảo sát
- [x] Khảo sát FE màn danh sách (index.vue, constants.js, add.vue)
- [x] Khảo sát FE form chi tiết + section (_id/manager|edit|index + components/*Section.vue)
- [x] Khảo sát FE tab báo giá/hồ sơ/giải pháp + modal Đóng dự án/Chốt giải pháp
- [x] Khảo sát BE (Controller/Service/Entity/Request/Migration) — trạng thái, cascade, validation, phân quyền

### Chụp ảnh thật (Playwright MCP, dev-hrm)
- [x] 01 Danh sách tổng quan
- [x] 02 Bộ lọc nâng cao
- [x] 03 Tuỳ chỉnh cột
- [x] 04 Form tạo mới (full)
- [x] 05 Modal chọn khách hàng
- [x] 06 Chi tiết tab Dự án
- [x] 07 Tab Báo giá
- [x] 08 Tab Hồ sơ
- [x] 09 Tab Thu thập thông tin
- [x] 10 Modal Đóng dự án
- [x] 11 Tab Giải pháp

### Dựng tài liệu
- [x] Generator python-docx (khung HDSD_KhachHang.docx) → 11 phần nội dung
- [x] Verify: 11 ảnh, 16 bảng, 14 Heading1, 11 caption, 0 broken embed
- [x] Output: HDSD_luongchinh/HDSD_DuAnTienKhaThi.docx

### Checkpoint — 2026-07-18
Vừa hoàn thành: Dựng xong HDSD_DuAnTienKhaThi.docx (11 phần, 11 ảnh thật, 16 bảng chi tiết từng trường).
Đang làm dở: (không)
Bước tiếp theo: User mở file review nội dung + ảnh; chỉnh nếu cần bổ sung ảnh Chốt giải pháp (chưa có dự án đủ điều kiện để chụp).
Blocked:

- [x] Viết tài liệu "Mô tả nghiệp vụ - Luồng trạng thái Dự án tiền khả thi.docx" (ma trận trạng thái dự án thường + dự án cha) — 20/08/2026

## 2026-08-20 — Ẩn mã dự án TKT trên toàn FE
- [x] Ẩn mọi chỗ hiển thị mã dự án tiền khả thi ở FE (45 file: danh sách/chi tiết TKT, báo giá, yêu cầu giá, BOM, hàng hoá dự án, giải pháp/hạng mục, họp + phiếu khảo sát, my-job, các màn báo cáo & bản in, dropdown chọn dự án). BE giữ nguyên: vẫn sinh & lưu code, quick-search vẫn lọc theo mã.
