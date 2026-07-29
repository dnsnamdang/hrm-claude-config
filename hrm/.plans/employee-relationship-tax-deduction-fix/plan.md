# Plan — Fix thông tin thân nhân (employee_info)

@khoipv

## Bối cảnh
Màn Hồ sơ nhân sự → tab thông tin thân nhân (/human/employee_info):
- (a) Mã số thuế người phụ thuộc chưa hiển thị/điền theo CCCD người phụ thuộc.
- (b) Tích "Kê khai giảm trừ gia cảnh" nhưng KHÔNG bắt buộc điền "Thời điểm bắt đầu tính giảm trừ" → vẫn lưu thành công.

## Quyết định (user chốt)
- (a) Auto điền MST = CCCD người phụ thuộc (FE-only auto-fill, không sửa service dùng chung).
- (b) Bắt buộc `deduction_start_date` khi `deduction_declaration = 1` — cả BE + FE inline (style module employee_info: `formError` + span `field-required`).
- Áp dụng TẤT CẢ luồng: form chính + request-update + my-info-request.
- CHỈ bật required cho `deduction_start_date` (không bật lại 4 field khác trong block comment: birth_certificate_number/place, identity_card_date/place).

## Tasks

### BE (issue b)
- [x] `CreateEmployeeInfoRequest.php`: bật rule `relationships.$index.deduction_start_date = required` khi `deduction_declaration == 1` + message
- [x] `SaveEmployeeInfoUpdateRequest.php`: tương tự + message
- CHỈ bật `deduction_start_date` (không bật lại 4 field khác trong block comment)

### FE (issue a — auto MST = CCCD) + (issue b — inline guard)
- [x] `EmployeeInfoForm.vue` (form chính): (a) `@input` CCCD → `syncDependentTaxCode`; normalize map khi load; (b) guard submitSave chặn khi thiếu deduction_start_date
- [x] `request-update/EmployeeInfoForm.vue` (guard có `status != 3` để không chặn từ chối duyệt)
- [x] `request-update/EditEmployeeInfoForm.vue`
- [x] `my-info-request/EmployeeInfoForm.vue`
- [~] `my-info-request/EditEmployeeInfoForm.vue`: KHÔNG cần — bảng thân nhân rút gọn (không có cột giảm trừ/CCCD/MST người phụ thuộc; `tax_code` ở đó là của nhân viên)

### Verify
- [x] php -l 2 file request → sạch
- [x] Parse 4 file .vue (vue-template-compiler + @babel/parser) → ALL OK
- [ ] Test browser: tích giảm trừ + để trống ngày → chặn + lỗi inline; nhập CCCD → MST tự điền (chờ user)

### Bổ sung 2026-07-28 — dấu (*) header cột "Thời điểm bắt đầu tính giảm trừ"
- [x] `EmployeeInfoForm.vue` (form chính, màn /human/employee_info/:id): thêm `<span class="field-required">(*)</span>` vào header cột, hiện khi có ≥1 dòng tick "Kê khai giảm trừ gia cảnh" (computed `hasDeductionDeclaration`)
- [x] `request-update/EmployeeInfoForm.vue`: tương tự
- [x] `request-update/EditEmployeeInfoForm.vue`: tương tự
- [x] `my-info-request/EmployeeInfoForm.vue`: tương tự
- [~] `my-info-request/EditEmployeeInfoForm.vue`: KHÔNG cần — bảng thân nhân rút gọn, không có cột giảm trừ
- [~] `EmployeeInfoShow.vue` + view_change_histories.vue: KHÔNG sửa — màn xem read-only, không có input bắt buộc
- [x] Verify: vue-template-compiler compile template 4 file → OK hết

### Checkpoint — 2026-07-28
Vừa hoàn thành: thêm (*) động ở header cột Thời điểm bắt đầu tính giảm trừ cho cả 4 form (form chính + request-update x2 + my-info-request)
Đang làm dở: không
Bước tiếp theo: user test browser (tick/bỏ tick checkbox → (*) hiện/ẩn)
Blocked: không
