# Plan — Tối ưu API getPersonnel (màn /human/personnel)

Nhánh: `tpe` (cả hrm-api). Triệu chứng: 500 "Allowed memory size 134217728 bytes exhausted" tại JsonResponse.php:87 trên kasaco.
Baseline local (63 phòng ban / 538 NV, limit=5): **2.00s · 5687 query · peak 110.5MB · json 1.79MB**.

## Phase 1 — BE: bỏ N+1 ở accessor (EmployeeInfo)
- [x] `getSalaryHistoryEffectiveAttribute` / `getSalaryHistoryLastAttribute`: lọc trên `salaryHistories` đã eager load, cache kết quả trong instance
- [x] `getValueSalaryHistoryEffectiveAttribute`: gọi 1 lần thay vì 8 lần
- [x] `getRankAttribute` / `getCompetencyAttribute`: dùng collection đã load, không query lại
- [x] `getContractTypeAttribute` / `getLaborContractStatusAttribute`: dùng quan hệ đã load nếu có
- [x] `getPositionWorkAttribute`: dùng `workPositions` đã load nếu có

## Phase 2 — BE: EmployeeService::getPersonnel
- [x] Cache cờ quyền 1 lần, không gọi `isCurrentEmployeeHasPermission` trong vòng lặp phòng ban
- [x] Eager load đủ quan hệ accessor cần (salaryHistories.rank/.competency, decision hợp đồng, workPositions)
- [x] Xử lý theo lô phòng ban (chunk), chỉ giữ dữ liệu chi tiết cho trang hiện tại → RAM O(1 trang)
- [x] Thêm option `view` (personnel | relationship | null=full): view=personnel không load/trả thân nhân

## Phase 3 — BE: Resource + FE
- [x] `PersonnelListResource` map đúng field theo `view`, không đổ model thô
- [x] Bỏ nhân bản `relationships` / `relationships_map` / `relationships_slice` (3 bản)
- [x] FE `pages/human/personnel/index.vue` gửi `view=personnel`; `pages/human/employee-relationships/index.vue` gửi `view=relationship`

## Phase 4 — Đo lại & bàn giao
- [x] Đo lại query/RAM/thời gian, so với baseline
- [x] Đối chiếu 12 chỉ số `statistical` trước/sau phải khớp tuyệt đối

### Checkpoint — 2026-09-03
Vừa hoàn thành: Phase 1-3 (accessor EmployeeInfo, EmployeeService xử lý theo lô + cache quyền + eager load, PersonnelListResource map theo view, FE 2 màn gửi view).
Đo lại trên DB local `hrm_prod_6_6` (63 phòng ban / 538 nhân viên), limit=5:

| Chỉ số | Trước | Sau |
|---|---|---|
| Thời gian | 2,00s | 0,41s |
| Số query | 5.687 | 401 |
| RAM (trừ nền PHP) | ~60MB | ~26MB |
| JSON trả về | 1,79MB | 0,028MB (view=personnel) |

Đối chiếu đúng đắn: 17 kịch bản (phân trang, lọc thân nhân/lương/hợp đồng/công ty/bộ phận…) × 3 mức quyền
(tổng công ty / công ty / không quyền) — **kết quả khớp tuyệt đối 51/51**, gồm cả 12 chỉ số thống kê.

Bước tiếp theo: user test trên UI thật (2 màn /human/personnel và /human/employee-relationships, cả In và Xuất Excel), rồi deploy kasaco.
Blocked: (không)


## Phase 5 — Test hồi quy đầy đủ (2026-09-03)
- [x] So accessor "eager load" vs "query cũ" trên toàn bộ 1.085 nhân viên × 10 accessor → 10.850 giá trị, lệch 0
- [x] So lịch sử lương với SQL gốc (effective / last / rank / competency / tổng thu nhập) → lệch 0
- [x] 17 kịch bản service × 3 mức quyền (tổng công ty / công ty / không quyền) → 51/51 khớp
- [x] 45 request HTTP × 3 tài khoản → 36 giống hệt; 9 còn lại là case lỗi (xem bên dưới)
- [x] So từng field FE dùng giữa payload cũ và view=personnel / view=relationship → 54 cặp, lệch 0
- [x] 20 endpoint module Quyết định + Nhân sự (dùng chung accessor đã sửa) → giống hệt 20/20
- [x] Xuất Excel (nhân sự + thân nhân): so từng ô sau khi convert CSV → giống hệt (616 và 1.685 dòng)
- [x] UI Playwright: màn /human/personnel (6 kịch bản lọc/phân trang) + /human/employee-relationships + màn In

### Lỗi do thay đổi này gây ra — đã phát hiện và sửa trong quá trình test
1. Cột **Tổng thu nhập của nhân viên kiêm nhiệm** hiện số thay vì "-" (Resource gọi thẳng accessor
   trong khi service cố ý không gán trường này cho người kiêm nhiệm) → sửa: đọc từ attributes đã gán.
2. Payload đường cũ (view=null) bị **thừa** `role`, `work_position`, `salary_histories[].rank/competency`,
   pivot `department_id`, và **thiếu** `current_decision_labor_contract`, `working_histories`
   → sửa: chỉ eager load cho màn mới, ẩn quan hệ phụ trợ, khôi phục 2 quan hệ cũ.
3. `salary_history_last` đổi kết quả khi 1 nhân viên có 2 dòng lương trùng `start_date`
   (SQL `order by start_date desc` không xác định thứ tự) → sửa: thêm tie-break `id desc` cho cả 2 nhánh.

### Khác biệt còn lại so với bản gốc (cần user xác nhận)
- **Cột STT khi có bộ lọc**: bản gốc hiện "11", "21", "V.21" (do `list_employees` trả object có khóa
  lệch sau `filter()`, FE nối chuỗi `index+1`); bản mới trả mảng nên hiện đúng "1", "2", "V.1".
  Phần dữ liệu các cột còn lại khớp tuyệt đối (hash bỏ cột STT giống hệt).
- **Màn In**: bản gốc trả 500 (memory exhausted / Undefined index cooperation_type) → bản mới chạy 0,95s.

### Lỗi CÓ SẴN phát hiện khi test (không do thay đổi này, chưa sửa)
- `page` âm (vd page=-3) → 500 `str_repeat()` tại `Modules/Human/Helper/Helper.php:209`
- Bản in: cột "Loại hợp đồng lao động" là `<b-td></b-td>` rỗng cứng trong `print.vue`
- Bản in: nhân viên cấp phòng ban không có Chức vụ / Chức danh (BE không trả 2 quan hệ này cho nhóm đó)
- Ô lọc `fullname` gửi lên nhưng service không xử lý → lọc theo tên không có tác dụng
- Console FE màn nhân sự: computed `permissions` trùng `data`, component `<confirm-delete-selected>`
  chưa đăng ký, `Duplicate keys detected: ep-x-y`

### Hiệu năng đo qua HTTP thật (DB local: 63 phòng ban / 538 nhân sự)
| Endpoint | Trước | Sau |
|---|---|---|
| `getPersonnel` limit=5 | 2,09-2,26s · 1,88MB | **0,52s · 30KB** |
| `getPersonnel/print` | **500 memory exhausted** | **200 · 0,95s · 553KB** |
| Xuất Excel nhân sự | 5,84s | **2,77s** |
| Xuất Excel thân nhân | 3,84s | **2,20s** |
| Số query (limit=5) | 5.687 | **340** |


## Phase 6 — Sửa nhóm lỗi có sẵn (2026-09-03, theo yêu cầu "sửa đi")
- [x] `page` âm / `limit`=0 gây 500: `Helper::intToNumberRoman()` trả rỗng khi số <= 0; Resource kẹp `page>=1`, `limit>=1`
- [x] Lọc theo họ tên (`fullname`) trước đây bị service bỏ qua → đã lọc ở cả nhân viên phòng ban và bộ phận,
      **so khớp cả khi gõ không dấu** (`nguyen` → `Nguyễn`) qua `Helper::convertVNToLatin`, và thêm vào `narrowingKeys`
- [x] Bản in: cột "Loại hợp đồng lao động" là ô rỗng cứng trong `print.vue` → đổ `contract_type.name`
- [x] Bản in: nhân viên cấp phòng ban thiếu Chức vụ / Chức danh → Resource trả `work_position`/`role`
      cho cả nhóm này (eager load kèm để không N+1)
- [x] `print.vue`: bỏ `<div v-if="index < data.length - 1">` dùng biến ngoài phạm vi v-for (không bao giờ render, chỉ sinh cảnh báo)
- [x] `index.vue` + `print.vue`: key `ep-...` trùng giữa các phòng ban → thêm chỉ số phòng ban vào key
- [x] `index.vue`: data `permissions` trùng tên computed của mixin `Permission` → đổi thành `filterPermissions`
      (trước đây object cờ từ API ghi đè mảng quyền hệ thống, làm mọi hàm kiểm tra quyền của mixin luôn trả false)
- [x] `index.vue`: đăng ký component `confirm-delete-selected` đang dùng trong template

### Kết quả sau Phase 6
- Console màn danh sách: **152 lỗi → 0**; màn In: **81 lỗi → 0**
- 45 request HTTP × 3 tài khoản: 34 giống hệt, 11 khác đều là lỗi đã sửa (500 → success) và lọc theo tên nay có tác dụng
- 20 endpoint module Quyết định/Nhân sự: giống hệt 20/20
- Excel (nhân sự + thân nhân): giống hệt từng ô
- Accessor: 10.850 giá trị lệch 0; lịch sử lương vs SQL gốc lệch 0
- So từng field FE dùng: chỉ lệch đúng `chuc_vu`/`chuc_danh` của nhân viên cấp phòng ban — chính là bug đã sửa
- Bảng màn danh sách (trang mặc định): hash khớp tuyệt đối với bản gốc (-1321612214 / 5279 ký tự)
- Hiệu năng: danh sách **0,53s / 33KB**; bản in **0,83s / 596KB** (trước: 2,1s và 500 memory exhausted)


## Phase 7 — Lỗi 500 trên kasaco sau khi deploy (2026-09-03)

Tái hiện trên DB prod kasaco đã lấy về local (`local_kasaco`: 20 phòng ban / 2.586 nhân sự, riêng
1 phòng có **1.060 người**; bảng rất rộng: `decision_labor_contracts` 79 cột, `employee_salary_histories` 58 cột).

Nguyên nhân: kasaco chạy **BE mới + FE chưa gửi `view`** → rơi vào nhánh cũ (trả đủ mọi quan hệ).
Đo được nhánh đó trên dữ liệu kasaco: **peak 477MB, JSON 105MB, 7-9s** → luôn vượt `memory_limit` 128MB.
Bản gốc cũng đúng nhánh này, nên đây chính là lỗi ban đầu.

- [x] Chia lô theo **số nhân viên** (`PERSONNEL_CHUNK_EMPLOYEES = 400`) thay vì số phòng ban —
      kasaco chỉ 20 phòng ban nên chia theo phòng ban gần như vô tác dụng
- [x] `select` cột hẹp cho `salaryHistories`, `decisionLaborContracts`, `currentDecisionLaborContract`
      và `employee_infos` (96 cột → 13 cột) ở màn mới; đường cũ giữ `select *`
- [x] Phòng ban **ngoài trang đang xem** chỉ nạp quan hệ tối thiểu để tính thống kê
- [x] Bản in + 2 chức năng Xuất Excel dùng đúng `view` thay vì nhánh cũ
- [x] Fallback ở controller: client cũ không gửi `view` → suy ra từ `display_type`
      (có = màn nhân sự, không có = màn thân nhân), đồng bộ vào request để Resource map đúng
- [x] `rowspan = 0` (nhân viên chưa khai thân nhân) → `max(1, ...)`: bootstrap-vue coi 0 là prop
      không hợp lệ, sinh 2.452 cảnh báo mỗi lần render; file Excel không đổi vì blade vốn quy 0 → 1
- [x] Màn thân nhân: sửa cùng 3 lỗi như màn nhân sự (data `permissions` đè computed của mixin,
      key `ep-`/`rp-` trùng giữa phòng ban, component `confirm-delete-selected` chưa đăng ký)
- [x] Màn thân nhân: `getFields()` đọc `data.employee_relationships` khi API trả `null` → TypeError

### Kết quả trên DB kasaco
| Request | Trước | Sau |
|---|---|---|
| `getPersonnel` (FE cũ, không `view`) | **500** | **200 · 0,9s · 929KB** |
| `getPersonnel?view=personnel` | — | 200 · 0,87s · 929KB |
| `getPersonnel?view=relationship` | — | 200 · 0,56s · 487KB |
| Bản in (`limit=9999999`) | 500 | 200 · 0,81s |
| Xuất Excel nhân sự / thân nhân | 500 | 200 · 3,7s / 2,0s |
| Peak bộ nhớ (màn danh sách) | 477MB | **~26MB** (ngoài nền PHP) |
| Console màn thân nhân | 194 lỗi | 3 (2 cảnh báo `fields`, 1 ảnh 404) |

### Hồi quy trên DB cũ (hrm_prod_6_6) sau các thay đổi trên
- Accessor 10.850 giá trị: lệch 0 · lịch sử lương vs SQL gốc: lệch 0
- 17 kịch bản × 3 quyền: chỉ lệch `rowspan` và **chỉ ở cặp 0 → 1** (đúng thay đổi chủ ý)
- So từng field FE dùng: chỉ lệch `chuc_vu`/`chuc_danh` của nhân viên cấp phòng ban (bug đã sửa ở Phase 6)
- 20 endpoint module Quyết định/Nhân sự: giống hệt 20/20 · Excel: giống hệt từng ô
- UI màn danh sách: hash bảng khớp tuyệt đối bản gốc (-1321612214 / 5279), console 0 lỗi

### Còn tồn (chưa sửa, cần user quyết)
- Màn thân nhân: `data.fields` trùng computed `fields` của vee-validate (cả `index.vue` và
  `ExportRelationshipModal.vue`). Hiện màn vẫn chạy đúng, nhưng đây là bẫy đã biết; đổi tên biến
  đụng nhiều chỗ nên chưa tự sửa.


## Phase 8 — Rà soát ảnh hưởng chéo (2026-09-03)
- [x] Quét toàn repo xem còn client nào gọi `human/employee/getPersonnel`:
      3 màn báo cáo (`assign_task_by_province`, `assign_task_department_by_customer`,
      `human/report/departments`) có method `getCompanies()` gọi endpoint này nhưng **không nơi nào gọi
      method đó** → code chết, không ảnh hưởng. `decision/dashboard` gọi endpoint khác
      (`decision/dashboard/personnel`). Không tìm thấy lời gọi nào từ app mobile.
- [x] Màn thân nhân còn 1 lời gọi `getPersonnel` không tham số chỉ để lấy cờ quyền → thêm
      `page=1&limit=1&view=relationship`: payload 487KB → 3KB
- [x] `Helper::intToNumberRoman` dùng ở 6 nơi khác — thay đổi chỉ áp cho số <= 0, trước đây các
      giá trị đó làm vỡ `str_repeat()`, nên không nơi nào đang phụ thuộc hành vi cũ
- [x] Tie-break `id desc` khi trùng `created_at`: DB TPE 0 nhóm trùng; DB kasaco 6 nhóm nhưng cả 6
      đều cùng `rank_id`/`competency_id` → không đổi kết quả trên dữ liệu thật
- [x] Smoke 20 endpoint module Quyết định + Nhân sự trên chính DB kasaco: tất cả 200
- [x] UI màn thân nhân trên DB kasaco: cờ quyền lọc vẫn đúng, bảng 1.321 dòng, 1.266 nhân sự

### Chưa kiểm (nêu rõ để không hiểu nhầm là đã bao phủ)
- Chưa chạy thử một kỳ **tính lương** (Payroll) hay **chấm công** (Timesheet) đầu-cuối. Mới chứng minh
  10 accessor của `EmployeeInfo` trả kết quả giống hệt trên toàn bộ 1.085 nhân viên và smoke 20 endpoint.
- Chưa test trên môi trường kasaco thật, chỉ chạy code local với DB prod kasaco đã lấy về.


## Phase 9 — Test sâu Payroll / Timesheet + khoá rủi ro accessor (2026-09-03)

### Rủi ro NGHIÊM TRỌNG phát hiện và đã khoá
Có 4 nơi eager load `salaryHistories` / `decisionLaborContracts` **KÈM ĐIỀU KIỆN LỌC**
(`IncreaseSeniorityService`, `TransferPersonnelService`, `AppointPersonnelService`,
`RenewLaborContractController`). Bản trước của tôi cho accessor tính trên bất kỳ quan hệ nào đã
`relationLoaded` → nếu nơi đó đọc accessor sẽ nhận **kết quả sai**. Đã chứng minh bằng test:
bật nhánh collection trên tập bị lọc cho ra `contract_type = NULL`, `labor_contract_status = 'none'`
thay vì `'effective'/'expired'`.

- [x] Thêm cờ `EmployeeInfo::$eagerRelationsAreComplete` — accessor CHỈ tính trên collection khi nơi
      gọi khẳng định đã nạp đầy đủ quan hệ; mặc định `false` nên mọi module khác giữ nguyên nhánh cũ
- [x] `EmployeeService::markEagerRelationsComplete()` bật cờ ở 3 điểm nạp đầy đủ
- [x] Test mô phỏng đúng cách 3 service kia eager load (có điều kiện) rồi đọc 8 accessor:
      **3.200 giá trị / 400 nhân viên, lệch 0** (trước khi có cờ: lệch hàng loạt)

### Hồi quy đầy đủ chạy lại sau thay đổi này (DB hrm_prod_6_6)
| Bộ test | Kết quả |
|---|---|
| Accessor eager ĐẦY ĐỦ + cờ (10.850 giá trị) | lệch 0 |
| Accessor eager CÓ ĐIỀU KIỆN, không cờ (3.200 giá trị) | lệch 0 |
| Lịch sử lương vs SQL gốc | lệch 0 |
| 17 kịch bản × 3 quyền | chỉ lệch `rowspan` (0 → 1, chủ ý) |
| So từng field FE dùng | chỉ lệch `chuc_vu`/`chuc_danh` (bug đã sửa ở Phase 6) |
| 45 request HTTP × 3 tài khoản | 42 mã 200, 3 mã 404 (route tự bịa) |
| **26 endpoint Payroll + Timesheet + Nhân sự** | **giống hệt 26/26** |
| 20 endpoint Quyết định/Nhân sự | giống hệt 20/20 |
| Excel (2 file) | giống hệt từng ô |
| UI màn danh sách | hash khớp tuyệt đối bản gốc (-1321612214 / 5279), console 0 lỗi |

### Trên DB kasaco (sau tất cả thay đổi)
Cả 7 luồng đều 200: view=personnel 0,94s · view=relationship 0,54s · FE cũ có display_type 0,94s ·
FE cũ không tham số 0,60s · bản in 1,27s · Excel nhân sự 3,67s · Excel thân nhân 2,11s.


## Phase 10 — Bug lọc Chức danh / Chức vụ (2026-09-03)

Phát hiện khi rà lần cuối: lọc theo **Chức danh** hoặc **Chức vụ** làm **mất sạch nhân viên thuộc
bộ phận**. Đo trên DB kasaco: chức danh id=129 có 521 nhân viên ở bộ phận → API trả về **0**.

Nguyên nhân: nhánh bộ phận lọc bằng `$emp->title_id` / `$emp->working_position_id` — hai giá trị này
là ALIAS do accessor `Department::employeeInfoActive` tự join, chỉ tồn tại ở nhân viên **cấp phòng ban**.
Nhân viên thuộc bộ phận lấy qua quan hệ `Part::employeeInfoActive` nên 2 alias đó là null → lọc loại hết.

- [x] Fallback về cột thật `employee_role_id` / `employee_work_position_id` cho nhánh bộ phận
- [x] Kiểm chứng lại: chức danh 521/521, chức vụ 1.137/1.192 — 55 người còn lại thuộc công ty khác,
      bị loại đúng theo quyền "xem theo công ty" của tài khoản test (không phải lỗi)

### Hồi quy sau thay đổi này
- 17 kịch bản × 3 quyền: chỉ lệch `rowspan` (0 → 1, chủ ý)
- 45 request HTTP: 42 mã 200, 3 mã 404 (route tự bịa)
- 26 endpoint Payroll + Timesheet + Nhân sự: giống hệt 26/26
- Excel 2 file: giống hệt từng ô
- So field FE dùng: chỉ lệch `chuc_vu`/`chuc_danh` (bug đã sửa ở Phase 6)
- Trên kasaco: 9 luồng (kể cả 2 bộ lọc vừa sửa) đều 200


## Phase 11 — Chạy thật kỳ tính lương đầu-cuối (2026-09-03)

Chạy trực tiếp job `CreateEmployeePayroll::dispatchSync` (đúng code path màn Tính lương gọi khi bấm
"Tính lương cho nhân viên") trên **5 kỳ lương thật** của DB kasaco, mỗi kỳ chạy 2 lần: bản gốc và bản
tối ưu, giữa 2 lượt khôi phục lại 4 bảng từ backup để 2 lượt cùng xuất phát điểm.

| Kỳ lương | Dòng lương | Dòng chi tiết | Tổng thu nhập | Kết quả |
|---|---|---|---|---|
| #152 KSCHN_BO_Viettel_T09/2025 | 9 | 315 | 103.190.621đ | giống hệt |
| #150 KSCHN_BO_Viettel_T10/2025 | 9 | 315 | 98.355.308đ | giống hệt |
| #145 Bảng lương tháng 09/2025 | 8 | 328 | 155.285.971đ | giống hệt |
| #134 Bảng lương tháng 09/2025 | 5 | 195 | 448.879.215đ | giống hệt |
| #182 KSCHN_BO_Vinaphone_T09/2025 | 5 | 180 | 60.967.409đ | giống hệt |

**Tổng: 36 dòng lương + 1.333 dòng chi tiết, lệch 0.** So sánh từng cột của `salary_employees` và
`salary_employee_data` (bỏ id/timestamp), không chỉ tổng tiền.

- [x] Backup 4 bảng (`salary`, `salary_employees`, `salary_data`, `salary_employee_data`) trước khi chạy
- [x] Khôi phục sau mỗi lượt; kiểm tra cuối: 10 / 50 / 14 / 1.762 bản ghi — **khớp đúng backup**,
      không còn kỳ lương tạm nào sót lại
