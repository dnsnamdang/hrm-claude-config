# Check trùng mảng hàng hóa: thêm điều kiện cùng phòng ban — @khoipv

## Bối cảnh
Màn Khách hàng → tab "Người phụ trách" (`pages/category/customer/components/PersonChargeComponent.vue`).

Hiện tại: 2 nhân viên **cùng nhóm nghiệp vụ** thì không được phụ trách cùng mảng hàng hóa
(cơ chế: `getArrayProductOptionsFiltered()` ẩn mảng đã bị dòng khác cùng nhóm chọn khỏi dropdown).

Yêu cầu: thêm điều kiện **cùng phòng ban trong hồ sơ nhân sự**.
- Cùng nhóm nghiệp vụ **VÀ** cùng phòng ban → giữ nguyên, không cho trùng mảng
- Cùng nhóm nghiệp vụ **nhưng khác phòng ban** → **cho phép** trùng mảng

Ví dụ user đưa: nhóm "CN AV-HCM", Đặng Xuân Hùng phụ trách Roche + Nhãn khoa.
Nguyễn Thị Kim EM cùng nhóm đó → nếu cùng phòng ban với Hùng thì vẫn bị chặn 2 mảng này;
nếu khác phòng ban thì được chọn Roche / Nhãn khoa.

## Dữ liệu
Không cần API mới: `category/master-data/employees` (`EmployeeResource`) đã trả sẵn `department_id`
(= `employee_infos.department_id`, **inner join** `departments` nên NV hiện trong dropdown luôn có phòng ban).

Phòng ban lấy theo **hồ sơ nhân sự hiện tại** (tra `employeeOptions` theo `item.id`),
fallback `item.department_id` đã lưu — vì khi edit, `DetailCategoryCustomerResource:118` trả
`department_id` là **snapshot lúc lưu**, NV chuyển phòng thì snapshot cũ sẽ sai.

## Phase 1 — FE
- [x] Thêm helper `getEmployeeDepartmentId(item)` — resolve phòng ban theo hồ sơ nhân sự hiện tại
- [x] `getArrayProductOptionsFiltered()`: điều kiện loại option đổi từ
      `cùng group_permission_id` → `cùng group_permission_id VÀ cùng department_id`
- [x] Dòng chưa xác định được phòng ban (chưa chọn NV) → không lọc, hiện toàn bộ mảng
- [x] Đồng bộ `validateForm()` (hiện là **code chết**, add.vue/edit.vue không gọi) theo cùng quy tắc
- [x] Giữ CRLF của file, verify compile bằng `vue-template-compiler`

## Phase 2 — BE
Không có. BE (`CustomerService::store/update`) vốn không validate trùng → không đụng.

## Ngoài phạm vi vòng này
- **Import Excel** (`PersonChargeImport::validateDuplicateDepartmentProducts()`) vẫn chặn theo
  nhóm nghiệp vụ, **chưa** xét phòng ban → sau khi user duyệt màn hình sẽ đồng bộ tiếp.

## Verify (chạy thật, 8/8 PASS)
Script Node: parse SFC bằng `vue-template-compiler`, nạp phần script rồi gọi thẳng method với dữ liệu giả.
- Template compile sạch
- Cùng nhóm + CÙNG phòng ban → Kim EM chỉ còn "Sinh hoá" (vẫn chặn Roche / Nhãn khoa)
- Cùng nhóm + KHÁC phòng ban → thấy đủ 3 mảng (yêu cầu mới)
- Khác nhóm + cùng phòng ban → đủ 3 mảng (không hồi quy)
- Chưa chọn NV / chưa chọn nhóm → không lọc
- Snapshot `department_id` cũ = 99 nhưng hồ sơ hiện tại = 10 → vẫn chặn theo phòng 10
- `validateForm()`: cùng phòng trùng Roche → 1 lỗi; khác phòng trùng Roche → 0 lỗi

### Checkpoint — 2026-09-17
Vừa hoàn thành: toàn bộ Phase 1 — `PersonChargeComponent.vue` (thêm `getEmployeeDepartmentId()`, sửa `getArrayProductOptionsFiltered()` và `validateForm()`), giữ CRLF.
Đang làm dở: không có.
Bước tiếp theo: build lại client + hard refresh → user test trên màn Khách hàng, tab Người phụ trách.
Blocked:

---

## Phase 3 — Import Excel (bổ sung 17/09/2026)
File: `Modules/Payroll/ExcelImports/PersonChargeImport.php` — `validateDuplicateDepartmentProducts()`
- [x] Lấy thêm phòng ban từ `employee_infos.department_id` → `departments` (tên phòng để báo lỗi)
- [x] Điều kiện so cặp: `cùng group_permission_id` → `cùng group_permission_id VÀ cùng department_id`
- [x] NV chưa gán phòng ban trong hồ sơ nhân sự → bỏ qua, ghi `Log::warning` (giống nhánh không có nhóm nghiệp vụ)
- [x] Sửa thông báo lỗi: trước đây gọi **nhóm nghiệp vụ** là "phòng" gây hiểu nhầm →
      nay ghi rõ `cùng nhóm nghiệp vụ "X" và cùng phòng ban "Y"`
- [x] Sửa lỗi tiềm ẩn: `Employee::where('employee_info_id', $employee_infos->id)` gọi **trước**
      `if (!$employee_infos)` → đảo thứ tự, tránh null property khi mã NV sai

## Phase 4 — Chốt chặn ở BE khi lưu từ màn hình (bổ sung 17/09/2026)
File: `Modules/Category/Http/Requests/StoreCategoryCustomerRequest.php` — thêm `withValidator()`
- [x] Dùng chung cho cả `store()` và `update()` (2 action đều nhận request này)
- [x] Phòng ban lấy từ **hồ sơ nhân sự** (`employees` → `employee_infos` → `departments`),
      **không tin `department_id` trong payload** FE gửi lên
- [x] Chặn khi cùng `group_permission_id` **VÀ** cùng `department_id` **VÀ** trùng mảng hàng hóa
- [x] Lỗi gắn vào key `person_charge_business.<index>.array_product_id` của **dòng sau** →
      FE hiện đúng chỗ nhờ `base-helper-error` sẵn có, không phải sửa thêm FE
- [x] Thiếu nhân viên / nhóm nghiệp vụ / phòng ban → bỏ qua (không đủ căn cứ so trùng)
- [x] Gộp nhiều mảng trùng vào 1 message/dòng (vì `BaseRequest::failedValidation` chỉ lấy message đầu mỗi key)

## Verify Phase 3 + 4 (chạy thật trên DB, 11/11 PASS)
`php artisan tinker` với fixture thật — cặp **cùng phòng ban**: NV.00035 + NV.00037 (nhóm *Kế toán* id 1, phòng *Phòng Kế toán* id 87); cặp **khác phòng ban**: NV.00002 + NV.00004 (cùng nhóm *Ban Giám Đốc* id 3, phòng 90 vs 83). Đã in `groupOf()` để xác nhận 2 cặp thật sự cùng nhóm nghiệp vụ.

**A. Khi lưu từ màn hình (6/6)** — cùng nhóm + cùng phòng + trùng mảng → báo lỗi, đúng key `person_charge_business.1.array_product_id` · cùng nhóm + khác phòng + trùng mảng → **không lỗi** · cùng phòng + khác mảng → không lỗi · không chọn mảng nào → không lỗi · khác nhóm + cùng phòng → không lỗi.

**B. Khi import Excel (5/5)** — cùng nhóm + cùng phòng + trùng mảng → báo lỗi · cùng nhóm + khác phòng + trùng mảng → **không lỗi** · cùng phòng + khác mảng → không lỗi · mảng rỗng cả 2 dòng → không lỗi (không hồi quy fix 16/09) · cùng phòng nhưng **khác khách hàng** → không lỗi.

### Checkpoint — 2026-09-17 (lần 2)
Vừa hoàn thành: Phase 3 + Phase 4. Đã đồng bộ cả 3 điểm (màn hình / import / chốt chặn BE) theo cùng một quy tắc.
Đang làm dở: không có.
Bước tiếp theo: build lại client + hard refresh, BE chạy lại → user test màn Khách hàng và import file Excel thật.
Blocked:

## Phase 5 — Fix bug: số dòng báo lỗi import sai (user báo 17/09/2026)
File: `Modules/Payroll/ExcelImports/PersonChargeImport.php` + `CategoryCustomerImport.php`

User import `Mau up du lieu khach hang DNS 08.09.2026 (3).xlsx`, lỗi trùng mảng "Nhãn khoa" báo **dòng 5**
nhưng dòng 5 thật trong file là khách hàng khác hẳn.

**Root cause (đã tái hiện, xác nhận 100%):**
`validateDuplicateDepartmentProducts()` dùng `$this->rows->groupBy(...)` — Laravel `Collection::groupBy()`
mặc định **KHÔNG preserve key** → `$index` trong `foreach ($rows as $index => $row)` là vị trí **trong nhóm
khách hàng** (0,1,2,3…), không phải dòng file. KH "Bệnh viện Đa khoa Nông nghiệp" có 4 dòng
(key gốc 724, 1013, 1793, 2180); NV.00059 là phần tử thứ 4 → index 3 → `3 + 2 = 5`.
Bug có sẵn từ trước, không do thay đổi Phase 1-4 gây ra. **Nội dung lỗi đúng**, chỉ số dòng sai.

- Dòng Excel thật: **1794** (NV.00054) và **2181** (NV.00059)
- Offset đúng của luồng này: `readPersonChargeSheet()` giữ key gốc từ `toArray()` (header key 0)
  → **dòng Excel = key + 1**, đúng bằng công thức `CategoryCustomerImport` đang dùng cho `validateRow`

**Việc cần làm:**
- [x] `groupBy($callback, true)` — giữ key gốc để `$index` là chỉ số dòng thật trong `$this->rows`
- [x] Error trả về đổi `line_row` (đã cộng sẵn offset sai) → `index` (key gốc, chưa cộng gì),
      để caller tự áp offset của luồng mình — tránh 2 luồng nạp dữ liệu lệch offset
- [x] `CategoryCustomerImport:222` đổi `$error['line_row']` → `$error['index'] + 1`,
      thống nhất với `$index + 1` mà chính nó dùng cho validateRow sheet Người phụ trách
- [x] Verify lại bằng chính file Excel user gửi: phải ra dòng **2181**

**Verify Phase 5 (chạy trên chính file Excel user gửi, 6/6 PASS):**
- Lỗi cũ báo dòng **5** → nay báo dòng **2181**, đúng dòng của NV.00059 trong file
- Chạy toàn bộ sheet 2202 dòng: đối chiếu từng lỗi với dòng gốc → **không lỗi nào lệch**
- Toàn sheet chỉ có **1 lỗi trùng mảng duy nhất** (dòng 2181) — nội dung lỗi vốn đã đúng từ đầu
- Chạy lại bộ verify Phase 3+4: **11/11 PASS**, không hồi quy
  (fixture cũ NV.00035 đã bị gỡ khỏi nhóm nghiệp vụ trong DB → đổi sang cặp
  NV.00051 + NV.00046, nhóm *CN VL- HCM* id 22, phòng *Phòng Kho* id 89)

### Checkpoint — 2026-09-17 (lần 3)
Vừa hoàn thành: Phase 5 — fix bug số dòng báo lỗi import sai (`groupBy` reset key).
Đang làm dở: không có.
Bước tiếp theo: user import lại file Excel để xác nhận thông báo lỗi nay chỉ đúng dòng 2181.
Blocked:
