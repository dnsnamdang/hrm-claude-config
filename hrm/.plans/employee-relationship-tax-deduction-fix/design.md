# Design — Fix thông tin thân nhân (employee_info) @khoipv

## Mục tiêu
Sửa 2 lỗi tab "Thông tin thân nhân" màn Hồ sơ nhân sự (/human/employee_info):
- (a) Mã số thuế (MST) người phụ thuộc điền/hiển thị theo CCCD của người phụ thuộc.
- (b) Tích "Kê khai giảm trừ gia cảnh" nhưng vẫn lưu được dù bỏ trống "Thời điểm bắt đầu tính giảm trừ".

## Giải pháp
### (a) MST = CCCD người phụ thuộc — FE only
- Ô CCCD `@input` → method `syncDependentTaxCode(index, value)` set `tax_code = value`.
- Khi load bản ghi cũ: map `relationships`, nếu có `identity_card_number` thì `tax_code = identity_card_number` (hiển thị MST theo CCCD).
- Giữ ô MST editable (không readonly); không sửa service dùng chung ở BE.

### (b) Bắt buộc thời điểm bắt đầu giảm trừ — BE + FE
- BE: 2 FormRequest bật lại rule `relationships.$index.deduction_start_date = required` khi `deduction_declaration == 1`, kèm message "Bắt buộc phải nhập". CHỈ field này (không bật 4 field khác cùng block comment cũ).
- FE: guard trong `submitSave` (theo pattern module: `formError` + span `field-required`), chặn submit + toast khi có dòng tích giảm trừ mà trống ngày bắt đầu. Với luồng duyệt: bỏ qua guard khi `status != 3` (từ chối không validate).

## Phạm vi file
- BE: `Modules/Human/Http/Requests/CreateEmployeeInfoRequest.php`, `SaveEmployeeInfoUpdateRequest.php`
- FE: `components/human-components/employee_info/EmployeeInfoForm.vue` + `request-update/EmployeeInfoForm.vue` + `request-update/EditEmployeeInfoForm.vue` + `my-info-request/EmployeeInfoForm.vue`
- KHÔNG đụng `my-info-request/EditEmployeeInfoForm.vue` (bảng thân nhân rút gọn).

## Không làm / lưu ý
- Không sửa `EmployeeInfoService::syncEmployeeRelationships()` (hàm dùng chung).
- Không bật lại regex 12 số CCCD / 10-12 số MST (đang comment, ngoài scope).
- Index formError theo index hiển thị `v-for`; quirk lệch index khi có dòng thiếu tên là pre-existing, không đụng.
