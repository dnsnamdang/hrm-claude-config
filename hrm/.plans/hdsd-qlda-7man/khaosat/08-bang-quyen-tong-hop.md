# Bảng quyền tổng hợp — module Giao việc / Quản lý dự án (7 màn)

## 0. Cơ chế nền — ĐỌC TRƯỚC

**Helper `checkPermissionList($query, [P_tổngCty, P_cty, P_phòng, P_bộphận, true], 'table')`** — `app/Helper/PermissionHelper.php:130-185`. Dừng ở quyền đầu tiên user có, theo thứ tự giảm dần:

| Quyền user có | Thấy dữ liệu nào |
|---|---|
| …theo tổng công ty | **Tất cả**, không lọc |
| …theo công ty | `company_id = current_company_role` **HOẶC** `created_by = mình` |
| …theo phòng ban | `department_id ∈ listManageDepartmentIds()` **HOẶC** `part_id ∈ listManagePartIds()` **HOẶC** `created_by = mình` |
| …theo bộ phận | `part_id ∈ listManagePartIds()` **HOẶC** `created_by = mình` |
| **Không có quyền nào** | Chỉ bản ghi `created_by = mình` |

Biến thể `checkPermissionListWithColumn(..., $column)` giống hệt nhưng cột "của mình" là `$column` thay vì `created_by`.

FE: `hasAPermission(name)` — `utils/mixins/CheckPermission.js:3`; helper cũ `hasPermission(name)` — `utils/mixins/Permission.js:47`.

⚠️ **Menu sidebar KHÔNG có phân quyền**: `components/menu-sidebar.js` — 0 lần xuất hiện chữ `permission`. Mọi mục menu hiện với mọi user; chặn nằm ở **dữ liệu** (list rỗng), không phải ở menu.

---

## 1. Dự án tiềm năng
| Tên quyền | Cho phép | Nút/tab | Endpoint |
|---|---|---|---|
| Xem danh sách dự án tiền khả thi theo tổng công ty (992) | Xem **mọi** dự án TKT | Lưới; mở khoá dropdown lọc Công ty | `GET /assign/prospective-projects` |
| Xem danh sách dự án tiền khả thi theo công ty (993) | Dự án cùng `company_id` + dự án mình tạo | như trên | như trên |
| Xem danh sách dự án tiền khả thi theo phòng ban (994) | Dự án phòng/bộ phận mình quản lý + mình tạo | như trên | như trên |
| Xem danh sách dự án tiền khả thi theo bộ phận (995) | Dự án bộ phận mình quản lý + mình tạo | như trên | như trên |

### Thao tác KHÔNG gắn quyền
Toàn bộ group route `api.php:295-318` **không có `checkPermission` nào**, controller/service **không có `isCurrentEmployeeHasPermission`**:
- **Tạo mới** (`POST`), **Sửa** (`PUT`), **Xóa** (`DELETE`), **Export Excel**.
- Nút "Tạo mới" không có `v-if`. Nút Xoá hiện theo **trạng thái + người tạo**: `can_delete = không có dự án con && created_by == mình && status == STATUS_DANG_TAO`.
- **Đóng dự án** / **Đóng dự án cha** / **Chốt giải pháp** — gate FE **chỉ theo vai trò dữ liệu**: `main_sale_employee_id == mình`. **Không có gate tương ứng ở BE.**

**Phân quyền theo cấp:** `checkPermissionList` chuẩn trên `prospective_projects`. Người không có quyền cấp nào vẫn thấy dự án **mình tạo**.

---

## 2. Thu thập thông tin dự án
| Tên quyền | Cho phép | Endpoint |
|---|---|---|
| Quản lý danh mục mẫu phiếu thu thập thông tin (1013) | Xem + Tạo/Sửa/Xoá/Khoá/Mở khoá/Sao chép/Export **mẫu phiếu** | `GET,POST /assign/form-templates`, `PUT/DELETE /{formTemplate}`, `/lock`, `/unlock`, `/copy-data`, `/export` |
| Quản lý danh mục câu hỏi khảo sát (982) | Tạo/Sửa/Xoá/Khoá/Export **câu hỏi khảo sát** | `POST /assign/questions`, `PUT/DELETE /{surveyQuestion}`, `/lock`, `/unlock`, `/export` |
| Xem danh mục câu hỏi khảo sát (997) | Chỉ xem danh sách câu hỏi | `GET /assign/questions` |

### Thao tác KHÔNG gắn quyền
- **Nhập/lưu câu trả lời phiếu thu thập**: `POST /assign/prospective-projects/{id}/save-form-answers` — không middleware, không gate. Bản meeting `POST /assign/meeting/{id}/project/{i}/save-form-answers` cũng vậy.
- **Xem lịch sử trả lời**: `GET /{prospectiveProject}/form-answer-histories`.
- **Đọc mẫu phiếu để render tab**: `/find-by-criteria`, `/snapshot/{id}`, `POST /snapshot/{id}/additional-questions`, `GET /{formTemplate}` — **cố ý không gắn** để user thường render được phiếu.
- Tab "Thu thập thông tin" **luôn hiện** cho mọi user mở được chi tiết dự án.

**Gap:** nhóm mẫu phiếu **không có quyền "Xem danh mục mẫu phiếu thu thập thông tin"** (chỉ có "Quản lý…") — khác các danh mục khác đều có cặp Quản lý/Xem. Hệ quả: user không có quyền quản lý **không mở được màn danh mục mẫu phiếu**.

---

## 3. Meeting
| Tên quyền | Cho phép |
|---|---|
| Xem danh sách meeting theo tổng công ty (1095) | Xem **mọi** meeting; mở chi tiết bất kỳ qua URL |
| Xem danh sách meeting theo công ty (1096) | Meeting cùng công ty + mình tạo |
| Xem danh sách meeting theo phòng ban (1097) | Meeting phòng/bộ phận mình quản lý + mình tạo |
| Xem danh sách meeting theo bộ phận (1098) | Meeting bộ phận mình quản lý + mình tạo |
| Quản lý danh mục loại meeting (989) / Xem danh mục loại meeting (1004) | CRUD / chỉ xem danh mục Loại meeting |

### Thao tác KHÔNG gắn quyền
Toàn bộ `Routes/Meeting/api.php:20-34` **không có `checkPermission`**: Tạo mới, Sửa, Xoá, Đổi trạng thái, Export, In. Nút Xoá chỉ theo trạng thái: `status === 0` (nháp).

**Phân quyền theo cấp (2 lớp):**
1. Meeting **Đang tạo (nháp)** chỉ **người tạo** thấy.
2. `checkPermissionList` chuẩn trên `meetings`.
3. **Mở rộng (OR)**: dù không có quyền cấp nào, vẫn thấy meeting **mình tạo** HOẶC **mình có tên trong "Thành phần — Phía Công ty"**.
Chi tiết/sửa qua URL dùng `Meeting::canView()`: true nếu là người tạo, hoặc `company_members`, rồi mới xét 4 quyền cấp.

---

## 4. Yêu cầu làm giải pháp & Giải pháp

### 4a. Yêu cầu làm giải pháp
| Tên quyền | Cho phép |
|---|---|
| Xem danh sách yêu cầu làm giải pháp theo tổng công ty (1007) | Xem mọi YCGP |
| … theo công ty (1008) | YCGP cùng công ty + YCGP mình là **người tiếp nhận** (`receive_id`) |
| … theo phòng ban (1009) | YCGP phòng/bộ phận mình quản lý + mình tiếp nhận |
| … theo bộ phận (1010) | YCGP bộ phận mình quản lý + mình tiếp nhận |
| **Tiếp nhận yêu cầu làm giải pháp (1012)** | (1) Mở màn **"YC chờ tiếp nhận"**; (2) bấm nút **Tiếp nhận**; (3) mở khoá quyền sửa/quản lý Giải pháp ở các trạng thái duyệt. Route `PUT /assign/request-solutions/{id}/receive` **có middleware** |

### 4b. Giải pháp
| Tên quyền | Cho phép |
|---|---|
| Xem danh sách làm giải pháp theo tổng công ty (1016) | Xem mọi giải pháp |
| … theo công ty (1017) / phòng ban (1018) / bộ phận (1019) | GP theo cấp + mình tạo |
| **Quản lý giải pháp (1044)** | **Đóng giải pháp** — `PUT /assign/solutions/{solution}/close` (**có middleware**) |
| Duyệt triển khai task (1020) | Quyết định hiển thị nút duyệt triển khai trong luồng hạng mục |

### Thao tác KHÔNG gắn quyền
- **YCGP**: Tạo, Sửa, Xoá, Export, Xem chi tiết.
- **Giải pháp**: Tạo, Sửa, Xoá, Export, **Tạo version mới**, và **toàn bộ 24 route `{solution}/manager`** (thêm thành viên, hồ sơ nghiệm thu + quyết định duyệt hồ sơ, phân bổ trọng số tiến độ, gán PM…).
- **Yêu cầu điều chỉnh giải pháp**: index/store/show/**accept**/**reject**.
- Nút Sửa/Xoá trên lưới GP theo **trạng thái + vai trò** (`can_edit`, `can_delete`), không theo quyền.

**Phân quyền theo cấp:**
- **YCGP**: `checkPermissionListWithColumn(..., 'receive_id')` — khác thường: "của mình" = **người tiếp nhận**, KHÔNG phải người tạo → người tạo YCGP mà không có quyền cấp nào sẽ **không thấy chính YC mình tạo**.
- **Giải pháp**: `checkPermissionList` rồi **mở rộng OR**: vẫn thấy GP nếu mình là `pm_id`, leader hạng mục, thành viên GP, hoặc thành viên hạng mục — kể cả phòng khác.
- **Màn "YC chờ tiếp nhận"**: không có quyền `Tiếp nhận yêu cầu làm giải pháp` → trả mảng rỗng. Có quyền thì lọc theo `implementation_type`: type=2 → `receive_dept` = phòng của user; type=3 → `receive_dept ∈ departmentsManager()`.

---

## 5. Yêu cầu báo giá
| Tên quyền | Cho phép |
|---|---|
| Xem tất cả danh sách Báo giá (1083) | Xem **mọi** báo giá (list, chi tiết, copy, export) |
| Xem danh sách Báo giá theo công ty (1084) / phòng ban (1085) / bộ phận (1086) | Phạm vi tương ứng + BG mình tạo |
| **Xây dựng giá bán theo phòng (1091)** | Dự án `implementation_type = 2`: mở màn **Yêu cầu XD giá**, tạo báo giá từ YCBG **của đúng phòng mình** |
| **Xây dựng giá bán theo công ty (1080)** | Dự án `implementation_type = 1/3`: mở màn YCBG toàn công ty, tạo báo giá từ YCBG |
| **Trưởng phòng duyệt giá Bom giải pháp (1081)** | Mở màn **Báo giá chờ duyệt**; **TP duyệt** BG `status=2` thuộc phòng mình quản lý; **Từ chối**. Route `pending-approval`, `tp-approve`, `reject` **đều có middleware** |
| **Ban giám đốc duyệt giá Bom giải pháp (1082)** | Mở màn Báo giá chờ duyệt; **BGĐ duyệt** BG `status=3` cùng công ty; Từ chối. `bgd-approve`, `reject` **có middleware** |
| **Xem giá vốn hàng hoá (1092)** | Nhìn thấy cột **giá vốn / thành tiền nhập**; thấy chênh lệch giá vốn khi sao chép BG; xuất Excel có cột giá vốn |
| Quản lý danh mục loại giảm giá (1090) | Màn `/assign/discount-types` |

### Thao tác KHÔNG gắn quyền
- **Yêu cầu xây dựng giá (pricing-requests)**: group `api.php:433-440` **không middleware nào**. Tạo, Sửa, **Gửi**, Xoá, Xem.
- **Báo giá**: `POST /assign/quotations` (tạo) chỉ gate khi **có** `pricing_request_id`; **báo giá tự lập** gate bằng vai trò dữ liệu `main_sale_employee_id == mình`. Không gắn quyền cho: `create-from-bom`, `PUT /{id}` sửa, `DELETE /{id}`, `submit` gửi duyệt, **`self-approve` tự duyệt**, `finalize` & `unfinalize` chốt/bỏ chốt, `apply-vat-bulk`, `allocate-discount`, `retry-sync`, `send-tmp-approval`, `pull-tmp-approval`, CRUD `service-items`, import/export Excel.
- Nút "Tạo báo giá" ở màn danh sách **không có `v-if` quyền**. Nút Xoá BG chỉ theo `status === 1 && creator_id === mình`.

**Phân quyền theo cấp:**
- **Báo giá**: `checkPermissionListWithColumn(..., 'created_by')` (list, chi tiết → ngoài scope trả **404**, copy-preview/copy/export).
- **Báo giá chờ duyệt** — logic riêng, KHÔNG dùng `checkPermissionList`: TP thấy `status=2` ∩ `department_id ∈ employee_manage_departments`; BGĐ thấy `status=3` ∩ `company_id` = công ty mình; có cả 2 → union; không quyền nào → `whereRaw('1=0')`.
- **Yêu cầu XD giá**: "theo phòng" → YCBG `department_id` = phòng mình ∩ dự án `implementation_type=2`; "theo công ty" → YCBG của dự án `implementation_type ∈ {1,3,null}`; **không có quyền nào → chỉ thấy YCBG `created_by = mình`**.

---

## 6. BOM giải pháp
| Tên quyền | Cho phép |
|---|---|
| Xem danh sách BOM List theo tổng công ty (1035) | Xem mọi BOM |
| … theo công ty (1031) / phòng ban (1032) / bộ phận (1033) | BOM theo cấp + BOM mình tạo |
| **Tạo BOM List (1034)** | Hiện nút **Tạo BOM**; vào màn Thêm mới / Sửa; hiện nút Sửa trên dòng — **FE-only** |
| **Xem giá vốn hàng hoá (1092)** | Thấy cột giá vốn trong BOM; được chọn **hàng ERP làm hàng con** |

### ⚠️ Cảnh báo — "Tạo BOM List" chỉ được kiểm ở FE
Group route `api.php:409-431` **không có `checkPermission` nào**, và grep `'Tạo BOM List'` trong toàn bộ `hrm-api/Modules` trả **0 kết quả**. `POST /assign/bom-lists`, `PUT /{bomList}`, `DELETE /{bomList}`, `/import`, `/copy-data`… gọi trực tiếp API **không cần quyền**. Trong HDSD nên mô tả quyền này là "quyền hiển thị nút", không phải rào chặn.

### Thao tác KHÔNG gắn quyền (BE)
Toàn bộ nhóm BOM: index, getAll, show, store, update, destroy, export, export-list, import-template, import/validate, import, logs, copy-data, tìm hàng ERP. Cấu hình duyệt giá BOM (`/assign/bom-price-approval-configs`) cũng không gate, kể cả `PUT /{id}`.

**Phân quyền theo cấp:** `checkPermissionListWithColumn(..., 'bom_lists', 'created_by')` chuẩn. Không có mở rộng theo thành viên.

---

## 7. Giao việc: Task & Issue
| Tên quyền | Cho phép |
|---|---|
| Xem danh sách task theo tổng công ty (1103) | Xem **mọi** task, bỏ qua 3 tầng lọc |
| Xem danh sách task theo công ty (1104) | Tầng 3: task có ≥1 người giữ vai trò thuộc công ty mình |
| Xem danh sách task theo phòng ban (1105) | Tầng 3 theo `department_id ∈ listManageDepartmentIds()` hoặc `part_id ∈ listManagePartIds()` |
| Xem danh sách task theo bộ phận (1106) | Tầng 3 theo `part_id ∈ listManagePartIds()` |
| **Duyệt triển khai task (1020)** | (1) Thấy thêm task của nhân viên thuộc phòng mình quản lý; (2) Hiện nút **Duyệt triển khai** khi task `PENDING_APPROVAL` và người xử lý thuộc phòng mình; (3) nhận thông báo khi task gửi duyệt |
| Xem danh sách issue theo tổng công ty (1099) / công ty (1100) / phòng ban (1101) / bộ phận (1102) | Tương tự Task |

### Thao tác KHÔNG gắn quyền
Group `api.php:701-744` **không có `checkPermission` nào**; controller cũng không gate:
- **Task**: Tạo, Sửa, Xoá, Xoá hàng loạt, Export, Báo cáo ngày, toàn bộ **comment**.
- **Issue**: Tạo, Sửa, Xoá, **Đổi trạng thái**, Export, comment.
- Nút Sửa/Xoá theo **vai trò + trạng thái**:
  - Task: `canEdit` = không có subtask && `created_by == mình`; `canDelete` = thêm `status == DRAFT`.
  - Task nhập kết quả: `canImportResult` = `assignee_id == mình` && status ∈ {TODO, IN_PROGRESS, REJECTED}; duyệt kết quả `canResultApprove` = `approver_id == mình` && status = REVIEW.
  - Issue: `canEdit` = `creator_id == mình` && status ∉ {CLOSED, COMPLETED}; `canDelete` = `creator_id == mình` && status = NEW.
- Nút "Tạo Task"/"Tạo Issue" không có `v-if` quyền.

### Phân quyền theo cấp — **3 tầng OR** (khác hẳn `checkPermissionList`)
Có quyền "theo tổng công ty" → return sớm, thấy tất cả. Ngược lại **hợp (OR)** 3 tầng:
- **Tầng 1 — vai trò cá nhân**: Task — người tạo, `assignee_id`, `approver_id`, `watchers`; **cộng thêm** nếu có quyền `Duyệt triển khai task` thì thấy task mà **người xử lý thuộc phòng mình quản lý**. Kèm kế thừa **Cha→Con** và **Con→Cha**. Issue — 6 vai trò: `creator_id`, `detected_by`, `assignee_id`, `approver_id`, `watchers`, `supporters`. **Không có kế thừa cha-con.**
- **Tầng 2 — thành viên dự án/giải pháp**: task/issue thuộc `solution_id` hoặc `project_id` mà mình là thành viên.
- **Tầng 3 — quản lý tổ chức**: bảng snapshot `task_org_units` / `issue_org_units` (giữ đơn vị của **mọi người giữ vai trò**), lọc theo quyền cấp cao nhất user có. Bộ lọc Công ty/Phòng ban/Bộ phận trên UI cũng chạy qua bảng này.

**Hệ quả:** user **không có quyền cấp nào** vẫn thấy đầy đủ task/issue mà mình giữ vai trò và task/issue của dự án/giải pháp mình tham gia.

---

## 8. Tổng hợp: thao tác KHÔNG được bảo vệ bởi bất kỳ quyền nào
Tất cả đều chỉ cần **đăng nhập**:

| Nhóm | Thao tác không gate |
|---|---|
| Dự án tiềm năng | Tạo / Sửa / Xoá / Export / Đóng dự án / Đóng dự án cha / Chốt giải pháp |
| Thu thập thông tin | Lưu câu trả lời phiếu (dự án & meeting), xem lịch sử trả lời, đọc snapshot mẫu phiếu, thêm câu hỏi bổ sung |
| Meeting | Tạo / Sửa / Xoá / Đổi trạng thái / Export / In |
| YCGP | Tạo / Sửa / Xoá / Export / Xem chi tiết |
| Giải pháp | Tạo / Sửa / Xoá / Tạo version / Export + **toàn bộ 24 route `{solution}/manager`** |
| YC điều chỉnh GP | index / store / show / **accept** / **reject** |
| BOM | **Toàn bộ** kể cả Tạo/Sửa/Xoá/Import (quyền `Tạo BOM List` chỉ có ở FE) + cấu hình duyệt giá BOM |
| YC xây dựng giá | Tạo / Sửa / **Gửi** / Xoá |
| Báo giá | Sửa / Xoá / Gửi duyệt / **Tự duyệt (self-approve)** / **Chốt & bỏ chốt** / áp VAT / phân bổ giảm giá / import-export Excel / đồng bộ ERP / CRUD dịch vụ |
| Task | Tạo / Sửa / Xoá / Xoá hàng loạt / Export / Báo cáo ngày / Comment |
| Issue | Tạo / Sửa / Xoá / **Đổi trạng thái** / Export / Comment |
| Menu | Không mục nào bị ẩn theo quyền |

Thay cho quyền, các thao tác trên được chặn bằng **vai trò dữ liệu + trạng thái** (người tạo / người xử lý / PM / Sale phụ trách / status), thể hiện qua `can_edit`, `can_delete`, `can_approve`, `can_import_result` trong Resource.

> **KHI VIẾT HDSD PHẢI TRÌNH BÀY ĐÚNG NHƯ VẬY**: "hiện nút khi bạn là <vai trò> và phiếu ở trạng thái <X>", KHÔNG mô tả là "cần quyền Y".

## 9. Quyền mồ côi
- **Trong phạm vi 7 màn này: KHÔNG có quyền mồ côi.**
- **Nửa mồ côi (chỉ FE, BE không kiểm)**: `Tạo BOM List` (1034).
- **Mồ côi thuộc phân hệ Giao việc nhưng ngoài 7 màn**: `Xem báo cáo theo dõi giải pháp theo phòng KD theo tổng công ty / công ty / phòng ban` (1063–1065); `Quản lý phiếu giao việc theo công ty` (35); `Quản lý phiếu đi công tác theo công ty` (36).
- **Thiếu quyền (gap)**: nhóm mẫu phiếu chỉ có `Quản lý danh mục mẫu phiếu thu thập thông tin`, **không có** `Xem danh mục mẫu phiếu thu thập thông tin`.
