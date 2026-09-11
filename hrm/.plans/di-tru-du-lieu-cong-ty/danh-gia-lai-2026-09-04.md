# Chạy lại & đánh giá di trú ETEK GREEN — 2026-09-04 (bản 2, đã test UI)

> Đối chiếu bảng feedback TPE: Google Sheet *Bảng xử lý và test dữ liệu gộp cổng*,
> sheet `HRM_Test gộp cổng ETEK, EP, EG` (dòng 13–130).
> Nhánh code `dong_bo_du_lieu` (hrm-api `a6da6faa4`, commit cuối **22/06/2026**).
>
> **Lưu ý quan trọng:** code KHÔNG thay đổi từ sau lần TPE test (02/07/2026) → mọi khác biệt
> so với bảng feedback đều phải giải thích được, không thể quy cho "đã sửa code".
>
> Bản 1 của tài liệu này đánh giá chỉ dựa trên đếm số dòng trong DB nên **kết luận sai nhiều mục**.
> Bản 2 này test trực tiếp trên giao diện bằng Playwright với 2 tài khoản
> (admin ETEK GREEN `uyendtt.hr@etekgreen.com` — công ty 9, và admin tổng `namdangit@gmail.com` — công ty 1).

## 1. Điều kiện chạy

| Mục | Giá trị |
|---|---|
| Nguồn | `local_hrm_green` (1 công ty, 126 hồ sơ) |
| Đích | `hrm_prod_6_6` (8 công ty), backup 1.1G trước khi chạy |
| Lệnh | `company:migrate-full --source-db=local_hrm_green --run=etekgreen --rice-parent=2 --no-erp --confirm` |
| Kết quả | company_id mới = **9**, 25.188 dòng, bù phép 432,5 ngày, hạ quyền 14 dòng |
| Môi trường test | FE `localhost:3000`, BE `127.0.0.1:8000`, cùng DB `hrm_prod_6_6` |

## 2. LỖI CÒN TỒN TẠI — đã dựng lại được trên giao diện

### 2.1 ⚠️ Định biên: map SAI BẢNG, hiện nhầm nhóm của công ty khác (dòng 30, 49)

Đây là lỗi nặng nhất tìm được, và là **lỗi của engine di trú**.

`department_manpowers.working_position_group_id` ở nguồn thực chất trỏ tới bảng **`rank_groups`**
(app join đúng như vậy: `DepartmentManpowerService.php:45,73`).
Nhưng catalog khai:

```php
// config/company_migration.php:361 (và :243 cho working_positions)
'working_position_group_id' => 'OWNED:working_position_groups',   // SAI — phải là rank_groups
```

Kết quả trên màn **Bảng định biên theo quy mô** của ETEK GREEN:

| Tình trạng | Số dòng |
|---|---|
| Cột "Nhóm chức vụ" trống | 26/29 |
| Hiện **"LÃNH ĐẠO."** — là nhóm ngạch của **TPE (company_id = 1)** | 6 |

Tức không chỉ mất dữ liệu mà còn **hiện nhầm dữ liệu công ty khác lên màn công ty EG**.
API `human/department-manpowers/assignment_missions/?company_id=9` trả `"working_position_group_name": null`
→ cùng gốc với dòng 49 "Mất nhóm chức vụ".

→ **Sửa**: đổi cả 2 chỗ thành `'OWNED:rank_groups'`, chạy lại `company:migrate-tables` cho công ty đã di trú.

### 2.2 ⚠️ Bảng nhân sự theo định biên — lỗi 500, không hiển thị (dòng 44)

Mở màn `/human/report/manpower_report` → *"Tổng số bản ghi: 0"* + *"Lỗi máy chủ. Vui lòng thử lại sau."*

Log: `Trying to get property 'id' of non-object` tại `DepartmentManpowerService.php:228`
(`$position->working_position->id`).

Nguyên nhân: `WorkingPosition` có global scope `FilterByCompanyManagerScope` lọc theo công ty người dùng
quản lý. Sau gộp cổng, báo cáo duyệt qua định biên của **nhiều công ty**; gặp định biên công ty ngoài
phạm vi → `working_position` trả NULL → 500. Trước khi gộp DB chỉ 1 công ty nên không bao giờ lỗi.

→ **Sửa**: lọc `company_id` ở query báo cáo, hoặc `?->` / bỏ qua dòng khi quan hệ NULL.

### 2.3 ⚠️ Admin công ty thành viên duyệt được đơn của công ty khác (dòng 81, liên quan 54)

Đăng nhập admin ETEK GREEN → `/timesheet/attendance/approve` hiện **14 đơn xin nghỉ, 100% của TPE**
(PHÒNG DỰ ÁN TRỌNG ĐIỂM, PHÒNG QUẢN TRỊ THÔNG TIN…), **0 đơn của EG**.

Gốc: `Modules/Timesheet/Services/AttendanceService.php:62` — nhánh `NSHC duyệt đơn xin nghỉ`
chỉ lọc trạng thái, **không lọc `company_id`**:

```php
if (isCurrentEmployeeHasPermission('NSHC duyệt đơn xin nghỉ')) {
    $q->orWhere('attendance_status', AttendanceStatus::CHO_NSHC_DUYET);   // thiếu company_id
}
```

Đây là lỗ hổng phân quyền chỉ lộ ra sau khi gộp cổng. Mức độ: nhân sự công ty A **duyệt được** đơn nghỉ
của công ty B.

### 2.4 Danh mục máy chấm công / địa điểm không lọc công ty (dòng 65, 66)

Đăng nhập admin ETEK GREEN:
- `/timesheet/location-conn-info` → **9/9 địa điểm**, gồm "Văn phòng Sài Gòn" (TPE), "VPSG" (TPSG), "Kho Liên Ninh" (TPE)
- `/timesheet/conn-info` → thấy "Máy chấm công khuôn mặt bảo vệ", "Lắp đặt Liên Ninh" của TPE

Dữ liệu đã có `company_id = 9` riêng (79 địa điểm, 241 thiết bị), **nhưng màn không lọc**.
TPE báo đúng — bản 1 của tài liệu này kết luận "đã dùng riêng" là **sai**.

### 2.5 Ba màn khác cũng không gate công ty (dòng 21, 41, 103)

| Màn | Kết quả test | File |
|---|---|---|
| Danh mục công ty | Admin EG thấy **9/9 công ty** (cả TPE, cả bản EG cũ id=7) | `Modules/Human/Services/CompanyService.php:42` |
| Quản lý thông báo nội bộ | Admin EG thấy **10 thông báo của TPE** ("Thông báo nghỉ lễ 02.09.2026"…) | `Modules/Human/Services/SelfNotificationService.php:32` |
| Mẫu bảng lương | `index()` không lọc `company_id` | `Modules/Payroll/Services/SalaryTemplateService.php:18` |

Cùng nhóm với 2.3 và 2.4 — sửa theo pattern đã đúng ở `SalaryCompositionService`:
`where('company_id', auth()->user()->current_company_role)`.

Ngoài ra ở màn Quy định làm thêm, phần "Thiết lập chức vụ không được làm thêm" liệt kê cho admin EG
cả **4 công ty** (TPE, ETEK, TPSG, EG).

### 2.6 Danh mục năng lực / ngạch lương xoá được dù đang dùng (dòng 27, 28)

```php
// Modules/Human/Services/CompetencyService.php:131
public function delete($id) {
    $entity = $this->_model->where('id', $id)->first();
    if (!empty($entity)) { $entity->status = 0; $entity->save(); }   // không kiểm tra đang dùng
}
```

Không có bất kỳ ràng buộc nào. Đúng như TPE ghi *"năng lực đang sửa/xóa được"* — **lỗi còn nguyên**.
Bản 1 kết luận "đã hết lỗi" vì chỉ đếm thấy 53 năng lực sang đủ — đó là đo sai thứ cần đo.

### 2.7 Ảnh nhân sự hỏng (dòng 34)

Mở hồ sơ NV EG (id 1618 — Phan Thị Hoa): thẻ ảnh trỏ
`http://localhost:3000/uploads/1702523614z...jpg`, `naturalWidth = 1` → **ảnh không tải được**.
Trên prod sẽ là `hrm-crm.eteksofts.com/uploads/...` → 404.

Số liệu: EG có **22/125 NV** dùng đường dẫn tương đối `/uploads/...` (ảnh trên server EG cũ) + 4 bản ghi
`id_images`; TPE thì 791/791 đều là URL S3 đầy đủ.

### 2.8 Danh mục ngân hàng chưa map được (dòng 17)

Chỉ **5/12** ngân hàng EG khớp TPE. Hai bên viết khác nhau và mã cũng khác quy ước:

| EG | TPE |
|---|---|
| Ngân hàng TMCP Quân đội (`MB`… mã EG là `MB`) | Ngân hàng Thương mại Cổ phần Quân đội |
| Ngân hàng TMCP Đầu tư và Phát triển Việt Nam | Ngân hàng Thương mại cổ phần Đầu tư và Phát triển Việt Nam |
| Ngân hàng TMCP Đông Nam Á | Ngân hàng TMCP Đông Nam Á (SeABank) |
| Ngân hàng TMCP Phương Đông / Quốc tế Việt Nam | (TPE chưa có) |
| mã `VCB`, `ICB` | mã `VIETCOMBANK`, … |

Hệ quả đo được: **2/4 tài khoản ngân hàng của NV EG bị `bank_id = NULL`**.

### 2.9 Tên công ty và 31 danh mục bị gắn hậu tố "(ETEK GREEN)"

Công ty mới mang tên **"CÔNG TY CỔ PHẦN GIẢI PHÁP ETEK GREEN (ETEK GREEN)"** — vì `companies.name`
unique mà bản ghi cũ (id=7) vẫn giữ tên gốc. Hậu tố này hiện trên **mọi dropdown chọn công ty**.

Unique guard cũng đổi tên 31 bản ghi danh mục khác: `ranks` 2, `titles` 6, `competencies` 14,
`working_position_groups` 4, `priority_levels` 4, `roles` 1 — ví dụ "NHÂN VIÊN 1 (ETEK GREEN)",
"Năng lực nhân viên 5 (ETEK GREEN)". API "Nhiệm vụ theo BP/NV" trả `rank_name: "NHÂN VIÊN 1 (ETEK GREEN)"`
→ người dùng nhìn thấy trực tiếp.

→ **Sửa**: pre-step đổi tên bản ghi trùng ở đích trước khi chạy (như design đã chốt), để bản mới lấy tên gốc.

### 2.10 Các thiếu sót khác (đo trên DB)

| Vấn đề | Số liệu |
|---|---|
| Cột Người tạo / Người cập nhật rỗng | 1.454 lượt FK `created_by`/`updated_by` không map được (industries 234, questions 148, titles 134…) |
| Bộ phận mất trưởng | 7/45 (người phụ trách cũ là tài khoản DNS Admin bị loại theo `skip_emails`) |
| Hồ sơ cơm mồ côi | 19 `rice_employee_infos` trỏ NV không còn ở HR |
| Danh mục loại HĐLĐ bị bỏ | 5 dòng ở nguồn có `company_id = NULL` nhưng filter là `company_id=1` |
| Cấu hình cơm chưa re-tag | `rice_menus` (151), `rice_menu_days` (387), `rice_settings` (23), `rice_setting_locations`, `rice_conn_infos` vẫn `company_id=1`; EG chỉ có 1 dòng `rice_menu_day_companies` |

## 3. Mục ĐÃ HẾT LỖI — có bằng chứng trên giao diện

| Dòng | TPE báo | Kết quả test lại |
|---|---|---|
| 58 | Quy định làm thêm **chưa gộp** ("EG, EP tự khai") | Form `/timesheet/setting/overtime` của EG **có đủ dữ liệu**: tối thiểu 60 phút, tối đa 100 giờ/tháng, liên tục 300/30. API `overtime_regulations/show` trả bản ghi id=6 `company_id=9` |
| 99 | Báo cáo phép **không lấy được dữ liệu** | `/timesheet/report/attendance_report` ra **71 NV EG** đủ cột: phép ngoài PM, tổng được dùng, đã dùng, còn lại. Bù phép 432,5 ngày đã cộng đúng (nguồn 310,5 → đích 743,0) |
| 45 | Bảng NS và quỹ lương **thừa 1 NV** | Báo cáo ra 72 trong khi công ty có 71 NV. Nguyên nhân: NV **Nguyễn Đức Anh (id 1714) kiêm nhiệm 2 phòng** nên bị đếm 2 lần — đây là cách báo cáo vốn hoạt động (nguồn cũng có bản ghi kiêm nhiệm này), **không phải lỗi di trú** |
| 122, 123, 125 | Đăng ký cơm chưa gộp / phải gộp bản ghi tương lai | Sau `relink-rice`, công ty cơm EG về đúng tenant TPE (`parent_id=1, company_id=9`), giữ nguyên **7.551 đăng ký**, trong đó **58 bản ghi ngày tương lai**. Giả thuyết: lần TPE test chạy bằng `db:seed --class=CompanyMigrationSeeder` (runbook cũ) nên **chưa chạy bước cơm** — bước này phải chạy tay, hoặc dùng `company:migrate-full` |

## 4. Không kiểm chứng được trong môi trường local

| Dòng | Lý do |
|---|---|
| 95 — Báo cáo tổng hợp chấm công ("số ngày nghỉ không lý do") | Màn ra 0 bản ghi vì dữ liệu chấm công cũ **không được gộp** theo chốt. Cần TPE test trên prod sau khi có chấm công mới |
| 121 — Thực đơn / máy check-in cơm dùng chung | Dữ liệu cơm ở local quá mỏng (6 dòng `rice_menu_day_companies` toàn hệ thống) |
| 19, 20 — Sơ đồ tổ chức | Là quyết định nghiệp vụ, chưa có chức năng để test |
| Phân hệ cơm dưới tài khoản EG | Admin EG bị chặn `/rice/personal-registration` và `/rice/menu-board` — cần rà lại quyền cơm cho công ty gộp |

## 5. Việc cần làm, theo thứ tự ưu tiên

**Sửa engine di trú:**
1. `working_position_group_id` → `OWNED:rank_groups` (2 chỗ trong `config/company_migration.php:243,361`) — đang hiện nhầm nhóm của TPE
2. Chuẩn hoá map `banks` (`TMCP` ↔ `Thương mại Cổ phần`, bỏ phần trong ngoặc) + bổ sung 2 ngân hàng TPE thiếu
3. Ghép domain EG cũ cho ảnh còn là đường dẫn tương đối (hoặc copy sang S3 TPE)
4. Pre-step đổi tên bản ghi trùng ở đích trước khi chạy → bỏ hậu tố "(ETEK GREEN)"
5. Filter `company_id=1 OR company_id IS NULL` cho danh mục kiểu `labor_contracts`
6. Fallback `created_by`/`updated_by` về admin công ty mới thay vì NULL
7. Bổ sung bước gán EG vào `rice_menu_day_companies` của TPE trong `relink-rice`

**Sửa app (lỗ hổng chỉ lộ ra sau khi gộp cổng — nên ưu tiên ngang engine):**
8. `AttendanceService::approve()` — thêm lọc `company_id` (nhân sự công ty A đang duyệt được đơn công ty B)
9. `DepartmentManpowerService` báo cáo — chặn 500 khi quan hệ NULL + lọc công ty
10. Lọc công ty cho: danh mục máy chấm công, địa điểm máy chấm công, danh mục công ty, thông báo nội bộ, mẫu bảng lương
11. Thêm ràng buộc xoá cho danh mục năng lực / ngạch lương (`CompetencyService::delete` và tương tự)

**Chờ TPE chốt:**
12. Có gộp đơn/phiếu chờ duyệt & phiếu tương lai không (dòng 74–93). Hiện `attendances`, overtime, công tác
    nằm trong skip list; nguồn còn 13 đơn chờ duyệt. Phương án rẻ: EG duyệt hết đơn trước cutover
13. Rà quyền phân hệ cơm cho công ty gộp (admin EG hiện không vào được)

---

*Ghi chú môi trường test: đã đặt mật khẩu tạm `Test@12345` cho `uyendtt.hr@etekgreen.com` trên DB local
để đăng nhập kiểm tra (chưa khôi phục). Mật khẩu `namdangit@gmail.com` giữ nguyên.*
