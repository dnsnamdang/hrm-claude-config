# Test Cases: Báo cáo chỉ số hoàn thành giải pháp theo version (QLDA_BC_10)

## 1. API — Dữ liệu báo cáo chính

### TC-01: Load báo cáo không có filter
- **Bước**: GET `/api/v1/assign/report/solution-versions`
- **Kỳ vọng**: Trả về danh sách companies phân cấp, mỗi company có departments → solutions → versions. Có summary + meta pagination

### TC-02: Load báo cáo với filter công ty
- **Bước**: GET `/api/v1/assign/report/solution-versions?company_id=1`
- **Kỳ vọng**: Chỉ trả về solutions thuộc company_id=1

### TC-03: Load báo cáo với filter phòng ban
- **Bước**: GET `/api/v1/assign/report/solution-versions?department_id=5`
- **Kỳ vọng**: Chỉ trả về solutions thuộc department_id=5

### TC-04: Load báo cáo với filter PM (employee_id)
- **Bước**: GET `/api/v1/assign/report/solution-versions?employee_id=10`
- **Kỳ vọng**: Chỉ trả về solutions có created_by=10

### TC-05: Load báo cáo với filter khách hàng
- **Bước**: GET `/api/v1/assign/report/solution-versions?customer_id=3`
- **Kỳ vọng**: Chỉ trả về solutions có prospective_project.customer_id=3

### TC-06: Load báo cáo với filter giải pháp cụ thể
- **Bước**: GET `/api/v1/assign/report/solution-versions?solution_id=1`
- **Kỳ vọng**: Chỉ trả về versions của solution_id=1

### TC-07: Load báo cáo với filter version cụ thể
- **Bước**: GET `/api/v1/assign/report/solution-versions?version_id=5`
- **Kỳ vọng**: Chỉ trả về version có id=5

### TC-08: Load báo cáo với filter thời gian
- **Bước**: GET `/api/v1/assign/report/solution-versions?from_date=2026-01-01&to_date=2026-03-31`
- **Kỳ vọng**: Chỉ trả về versions có start_date trong khoảng

### TC-09: Phân trang
- **Bước**: GET `/api/v1/assign/report/solution-versions?per_page=5&current_page=1`, rồi `current_page=2`
- **Kỳ vọng**: Page 1 trả 5 solutions (kèm versions), page 2 trả tiếp. meta.total đúng tổng số solutions

### TC-10: Dữ liệu rỗng
- **Bước**: GET `/api/v1/assign/report/solution-versions?company_id=99999`
- **Kỳ vọng**: Trả về companies=[], summary.total_versions=0, meta.total=0

---

## 2. API — Tính toán số liệu

### TC-11: Số giờ được giao
- **Kiểm tra**: Cột estimated_hours của mỗi version = SUM(tasks.estimated_hours) WHERE solution_version_id = version.id
- **Verify**: So sánh với query trực tiếp `SELECT SUM(estimated_hours) FROM tasks WHERE solution_version_id = X`

### TC-12: Số giờ thực tế
- **Kiểm tra**: Cột actual_hours = SUM(task_result_progress_logs.hours) qua JOIN tasks WHERE solution_version_id
- **Verify**: So sánh với query trực tiếp

### TC-13: Hiệu suất
- **Kiểm tra**: efficiency = estimated_hours / actual_hours × 100
- **Edge case**: actual_hours = 0 → efficiency = 0 (không chia cho 0)

### TC-14: Số ngày thực hiện
- **Kiểm tra**: days = end_date - start_date (solution_versions)
- **Edge case**: start_date hoặc end_date NULL → days = 0

### TC-15: Cộng tổng dồn lên giải pháp
- **Kiểm tra**: Dòng solution = SUM tất cả versions con (task_count, estimated_hours, actual_hours)
- **Verify**: Cộng tay các version con, so sánh

### TC-16: Cộng tổng dồn lên phòng ban và công ty
- **Kiểm tra**: Dòng dept = SUM tất cả solutions con. Dòng company = SUM tất cả depts con

### TC-17: Trạng thái giải pháp
- **Kiểm tra**: Dòng solution hiển thị trạng thái + màu của version cao nhất (cuối cùng)

### TC-18: Ngày bắt đầu / ngày chốt giải pháp
- **Kiểm tra**: min_start_date = MIN(versions.start_date), max_approved_at = MAX(versions.approved_at)

### TC-19: Summary KPI
- **Kiểm tra**: total_versions = tổng số version, avg_days = trung bình số ngày (chỉ tính version có cả start_date và end_date), efficiency = tổng estimated / tổng actual × 100

---

## 3. API — Popup chi tiết

### TC-20: Chi tiết nhân sự tham gia
- **Bước**: GET `/api/v1/assign/report/solution-versions/{versionId}/members`
- **Kỳ vọng**: Trả danh sách nhân sự từ solution_version_members, thứ tự PM → Leader → Thành viên
- **Kiểm tra**: Giờ tham gia = SUM(progress_logs.hours) WHERE task.assignee_id = member_id AND task.solution_version_id

### TC-21: Chi tiết nhân sự — version chưa có member
- **Bước**: GET members cho version chưa chạy seeder
- **Kỳ vọng**: Trả mảng rỗng []

### TC-22: Chi tiết hạng mục
- **Bước**: GET `/api/v1/assign/report/solution-versions/{solutionId}/modules`
- **Kỳ vọng**: Trả danh sách hạng mục với tên, leader, giờ giao, giờ thực tế

### TC-23: Chi tiết hạng mục — giải pháp không có module
- **Bước**: GET modules cho solution không có hạng mục
- **Kỳ vọng**: Trả mảng rỗng []

---

## 4. API — Filter options

### TC-24: Load filter options
- **Bước**: GET `/api/v1/assign/report/solution-versions/filter-options`
- **Kỳ vọng**: Trả customers + solutions (companies/departments/employees do V2BaseCompanyDepartmentFilter tự load)

---

## 5. API — Xuất Excel

### TC-25: Xuất Excel thành công
- **Bước**: GET `/api/v1/assign/report/solution-versions/export`
- **Kỳ vọng**: Trả file .xls, tên file "bao_cao_giai_phap_theo_version.xls"

### TC-26: Xuất Excel với filter
- **Bước**: GET `/api/v1/assign/report/solution-versions/export?company_id=1`
- **Kỳ vọng**: File Excel chỉ chứa data của company_id=1

### TC-27: Nội dung Excel
- **Kiểm tra**:
  - Title "Báo cáo theo dõi chỉ số hoàn thành giải pháp theo version" center
  - Header 2 dòng (nhóm cột + cột con)
  - Phân cấp: Công ty (xanh) → Phòng (xanh nhạt) → Giải pháp (xám nhạt) → Version (trắng)
  - Date format DD/MM/YYYY
  - Dòng giải pháp hiện trạng thái + ngày bắt đầu + ngày chốt
  - Đánh giá hiệu suất: Hiệu suất cao / trung bình / thấp / Chưa có dữ liệu

---

## 6. Frontend — Giao diện

### TC-28: Load trang báo cáo
- **Bước**: Truy cập `/assign/report/solution-versions`
- **Kỳ vọng**: Hiện filter panel (collapsed), bảng với dòng tổng + các dòng công ty, loading spinner khi đang load

### TC-29: Expand/Collapse từng cấp
- **Bước**: Click mũi tên ở dòng Công ty → Phòng → Giải pháp
- **Kỳ vọng**: Mở/đóng các dòng con tương ứng, icon mũi tên đổi hướng

### TC-30: Button "Xem chi tiết"
- **Bước**: Click "Xem chi tiết"
- **Kỳ vọng**: Expand tất cả (Company → Dept → Solution → Version), text đổi thành "Chỉ xem cấp gốc"
- **Bước tiếp**: Click "Chỉ xem cấp gốc"
- **Kỳ vọng**: Collapse tất cả về cấp công ty

### TC-31: Toggle từng cấp độc lập với button Xem chi tiết
- **Bước**: Click "Xem chi tiết" → collapse 1 công ty bằng mũi tên → click "Chỉ xem cấp gốc" → click "Xem chi tiết"
- **Kỳ vọng**: Tất cả expand lại bình thường

### TC-32: Filter — Tìm kiếm
- **Bước**: Mở filter, chọn Công ty, bấm Tìm kiếm
- **Kỳ vọng**: Loading spinner hiện, sau đó bảng chỉ hiện data của công ty đã chọn

### TC-33: Filter — Làm mới
- **Bước**: Chọn nhiều filter, bấm Làm mới
- **Kỳ vọng**: Tất cả filter reset về trống, bảng load lại data đầy đủ

### TC-34: Filter — Cascade Giải pháp → Version
- **Bước**: Chọn 1 giải pháp trong filter
- **Kỳ vọng**: Dropdown Version enabled, load danh sách version của giải pháp đó

### TC-35: Popup Chi tiết nhân sự
- **Bước**: Click số ở cột "Số nhân sự tham gia" (dòng version)
- **Kỳ vọng**: Mở popup hiện danh sách nhân sự: PM đầu tiên → Leader → Thành viên. Có cột Giờ tham gia

### TC-36: Popup Chi tiết hạng mục
- **Bước**: Click số ở cột "Số hạng mục" (dòng solution hoặc version)
- **Kỳ vọng**: Mở popup hiện danh sách hạng mục: tên, leader, giờ giao, giờ thực tế

### TC-37: Trạng thái version
- **Bước**: Xem cột "Trạng thái version"
- **Kỳ vọng**: Hiển thị V2BaseBadge với màu tương ứng từ Solution::STATUSES

### TC-38: Đánh giá hiệu suất
- **Bước**: Xem cột "Đánh giá hiệu suất"
- **Kỳ vọng**:
  - ≥ 100%: V2BaseBadge xanh "Hiệu suất cao"
  - 80-99%: V2BaseBadge vàng "Hiệu suất trung bình"
  - < 80%: V2BaseBadge đỏ "Hiệu suất thấp"
  - 0: V2BaseBadge xám "Chưa có dữ liệu"

### TC-39: Pagination
- **Bước**: Nếu có > 15 giải pháp, chuyển trang
- **Kỳ vọng**: "Hiển thị X–Y / Z giải pháp" đúng, bảng load data trang mới

### TC-40: Đổi số dòng/trang
- **Bước**: Đổi select "Số dòng/trang" từ 15 sang 50
- **Kỳ vọng**: Bảng load lại với 50 giải pháp/trang

### TC-41: Xuất Excel từ UI
- **Bước**: Click "Xuất Excel"
- **Kỳ vọng**: Download file "bao_cao_giai_phap_theo_version.xls", toast "Xuất Excel thành công"

### TC-42: In báo cáo
- **Bước**: Click "In báo cáo"
- **Kỳ vọng**: Mở dialog in trình duyệt

### TC-43: Scroll ngang đồng bộ
- **Bước**: Scroll thanh trượt phía trên
- **Kỳ vọng**: Bảng phía dưới scroll theo, và ngược lại

### TC-44: Dòng tổng "Tổng toàn bộ version"
- **Bước**: Xem dòng đầu tiên trong bảng
- **Kỳ vọng**: Background xanh đậm, hiện: X giải pháp • Y version • Thời gian TB: Z ngày • Hiệu suất giờ: W%

---

## 7. Snapshot nhân sự (solution_version_members)

### TC-45: Seeder backfill
- **Bước**: Chạy `php artisan db:seed --class=SolutionVersionMembersSeeder`
- **Kỳ vọng**: Tất cả version hiện có được snapshot members (PM + Leaders + Members)

### TC-46: Snapshot khi tạo version mới
- **Bước**: Tạo version mới cho giải pháp đã duyệt
- **Kỳ vọng**: Version cũ được snapshot members trước khi tạo version mới

### TC-47: Thứ tự nhân sự trong snapshot
- **Kiểm tra**: Query `SELECT * FROM solution_version_members WHERE solution_version_id = X`
- **Kỳ vọng**: Có PM (role='PM'), Leaders (role='Leader hạng mục'), Members

### TC-48: Loại bỏ duplicate
- **Bước**: 1 employee vừa là PM vừa là member hạng mục
- **Kỳ vọng**: Chỉ 1 record, role = 'PM' (ưu tiên cao nhất)

---

## 8. Edge Cases

### TC-49: Giải pháp chưa có task nào
- **Kỳ vọng**: task_count=0, estimated_hours=0, actual_hours=0, efficiency=0, đánh giá="Chưa có dữ liệu"

### TC-50: Version chưa có ngày chốt (approved_at=NULL)
- **Kỳ vọng**: Cột "Ngày chốt" hiện "—"

### TC-51: Version chưa có end_date
- **Kỳ vọng**: Số ngày thực hiện = 0

### TC-52: Giải pháp không có hạng mục
- **Kỳ vọng**: module_count=0, click popup hạng mục hiện "Không có dữ liệu hạng mục"

### TC-53: Nhiều giải pháp cùng công ty
- **Kỳ vọng**: Gộp chung 1 dòng công ty, cộng tổng đúng
