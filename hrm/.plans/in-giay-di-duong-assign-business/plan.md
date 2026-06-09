# Plan — In Giấy đi đường cho Phiếu công tác (assign_business)

Mẫu giống `/timesheet/jobassignment/:id/print`. Theo file mẫu `giay_di_duong_PCT.xlsx` (2 sheet = 2 TH):
in mỗi nhân viên 1 tờ; nút In ở dropdown hành động màn danh sách.

Phân nhánh theo `business_type`:
- **PCT kỹ thuật (type 1)**: "Đến"/"Về việc" để trống (dòng chấm); bảng 9 dòng để trống hết.
- **PCT khác (type 2)**: "Đến" = `place`; "Về việc" = `job_note`; bảng dòng 1 có "Nơi đến" = `places[0].place`,
  cột Đi = from_time (Giờ HH:mm / Ngày DD/MM/YYYY), cột Đến = to_time; các dòng còn lại trống.

## Phase 1 — In giấy đi đường

### BE
- [x] `AssignBusinessService::getDataPrint($id)` — trả code, business_type, place, job_note, first_place, from_time, to_time, employees[{fullname, code, work_position, department, is_leader}]
- [x] `AssignBusinessController::print($id)` — gọi service, trả responseJson
- [x] Route `GET /assign/assign_business/{id}/print`

### FE
- [x] `pages/assign/assign_business/_id/print.vue` — copy mẫu timesheet, map dữ liệu PCT, phân nhánh type 1/2, bảng 9 dòng
- [x] Thêm dropdown item "In giấy đi đường" ở `pages/assign/assign_business/index.vue` → `/assign/assign_business/:id/print`
- [x] Thêm style header toolbar (back-arrow + nút In) copy từ `business_trip_assigns/print.vue` cho giống họ màn print timesheet
- [x] Fix bug format ngày: escape `[ngày]` trong moment (ký tự `y` bị hiểu là token → "ngà2026")

### Chỉnh cho khớp timesheet (vòng 2)
- [x] Dòng "Từ–đến": bỏ giờ/phút → "Từ ngày DD tháng MM năm YYYY đến hết ngày DD…" (giống timesheet)
- [x] Bảng: bỏ nhãn "Giờ:/Ngày:", ô NGÀY GIỜ hiển thị ngày + giờ (DD/MM/YYYY + HH:mm:ss) căn giữa như timesheet; type-2 dòng 1 điền from/to, type-1 để trống

### Chỉnh layout theo timesheet (vòng 3)
- [x] Chức vụ và Thuộc phòng tách mỗi cái 1 hàng riêng (info-field--full), không để ngang
- [x] Bảng table-layout fixed + colgroup: cột NGÀY GIỜ (ĐI/ĐẾN) rộng hơn (15% mỗi cột)
- [x] Ô NGÀY GIỜ có nhãn "Giờ:"/"Ngày:" (note text) căn trái, mọi dòng

### Verify (Playwright, đăng nhập namdangit@gmail.com)
- [x] PCT kỹ thuật (12844): Đến/Về việc trống, bảng 9 dòng trống, dòng "Từ…đến hết" = ngày DD tháng MM năm YYYY
- [x] PCT khác (12816): Đến=place, Về việc=job_note, bảng dòng 1 = "DD/MM/YYYY / HH:mm:ss" căn giữa
- [x] UI khung/header/bảng/định dạng ngày khớp `timesheet/jobassignment/27928/print`

### Còn khác timesheet (theo file xlsx — chờ user chốt)
- [ ] Có dòng "Số phiếu: PCT-…" (timesheet không có)
- [ ] Ký "Trưởng phòng/ TBP" (timesheet "Trưởng bộ phận")
- [ ] PCT kỹ thuật: Đến/Về việc để trống cho NV tự điền (timesheet điền sẵn)
