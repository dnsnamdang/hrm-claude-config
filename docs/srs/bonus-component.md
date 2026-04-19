# SRS: Thành phần tính thưởng (Bonus Component)

| Thông tin | Chi tiết |
|-----------|----------|
| Module | Payroll |
| Phiên bản | 1.0 |
| Ngày tạo | 2026-04-09 |
| Trạng thái | Draft |

---

## 1. Giới thiệu

### 1.1. Mục đích
Quản lý danh sách các thành phần dùng để tính thưởng cuối năm cho nhân viên. Mỗi thành phần có thể tính theo công thức tự động (dựa trên biến hệ thống từ HRM + ERP) hoặc nhập tay thủ công. Các thành phần này được sử dụng trong "Bảng chia thưởng cuối năm" (Bonus Distribution).

### 1.2. Phạm vi
**Trong scope:**
- CRUD thành phần tính thưởng
- Soạn công thức với biến hệ thống (HRM + ERP)
- Validate công thức trước khi lưu
- Tìm kiếm, phân trang danh sách

**Ngoài scope:**
- Tính toán thực tế thưởng cho nhân viên (thuộc module Bảng chia thưởng)
- Quản lý biến hệ thống (hardcode trong frontend)
- Phân quyền theo cấp (công ty/phòng ban)

### 1.3. Thuật ngữ

| Thuật ngữ | Giải thích |
|-----------|-----------|
| Thành phần tính thưởng | Một cấu phần trong công thức chia thưởng (VD: "Theo doanh số", "Theo thâm niên") |
| Mode formula | Thành phần tính theo công thức tự động |
| Mode manual | Thành phần nhập tay (% chia + số tiền) |
| Biến hệ thống | Giá trị lấy từ HRM (lương, thâm niên) hoặc ERP (doanh số, công nợ) |
| Công thức | Biểu thức toán học kết hợp biến hệ thống và hàm (IF, MAX, MIN...) |

---

## 2. Actors & Permissions

| Actor | Mô tả | Permissions |
|-------|-------|-------------|
| Admin / Kế toán trưởng | Người quản lý thành phần tính thưởng | Xem, tạo, sửa, xoá |
| Nhân viên kế toán | Người dùng thông thường | Xem danh sách (nếu có quyền vào module Payroll) |

---

## 3. Use Cases

### UC-01: Xem danh sách thành phần tính thưởng
| | |
|---|---|
| **Actor** | Admin / Kế toán |
| **Precondition** | Đã đăng nhập, có quyền vào module Payroll |
| **Main Flow** | |
| 1 | Vào menu Tính lương > Thành phần tính thưởng |
| 2 | Hệ thống hiển thị danh sách thành phần với các cột: STT, Mã TP, Tên, Loại, Công thức, Mô tả, Thao tác |
| 3 | Có thể tìm kiếm theo mã hoặc tên |
| 4 | Phân trang với tuỳ chọn 10/25/50/100 bản ghi |
| **Postcondition** | Hiển thị danh sách thành phần, sắp xếp theo thời gian cập nhật mới nhất |

### UC-02: Tạo mới thành phần tính thưởng
| | |
|---|---|
| **Actor** | Admin / Kế toán |
| **Precondition** | Đã đăng nhập, có quyền tạo |
| **Main Flow** | |
| 1 | Nhấn nút "Tạo thành phần" |
| 2 | Hệ thống mở modal tạo mới, tự sinh mã TP (format: TPxxx) |
| 3 | Nhập tên thành phần (bắt buộc) |
| 4 | Chọn cách tính: "Theo công thức" hoặc "Nhập thủ công" |
| 5 | Nếu chọn "Theo công thức": soạn công thức bằng cách chọn biến hệ thống, hàm, toán tử |
| 6 | Có thể validate công thức trước khi lưu |
| 7 | Nhấn "Lưu" |
| **Postcondition** | Thành phần được tạo, hiển thị trong danh sách |
| **Alternative Flow** | Nếu mã TP đã tồn tại → báo lỗi "Mã thành phần đã tồn tại" |
| **Exception** | Validation lỗi → hiển thị message lỗi tương ứng |

### UC-03: Sửa thành phần tính thưởng
| | |
|---|---|
| **Actor** | Admin / Kế toán |
| **Precondition** | Thành phần đã tồn tại |
| **Main Flow** | |
| 1 | Nhấn nút sửa (icon bút) trên dòng thành phần |
| 2 | Hệ thống mở modal với dữ liệu hiện tại |
| 3 | Sửa thông tin cần thay đổi |
| 4 | Nhấn "Lưu" |
| **Postcondition** | Thành phần được cập nhật, `updated_by` ghi nhận user hiện tại |
| **Exception** | Mã TP trùng với thành phần khác → báo lỗi |

### UC-04: Xoá thành phần tính thưởng
| | |
|---|---|
| **Actor** | Admin / Kế toán |
| **Precondition** | Thành phần đã tồn tại |
| **Main Flow** | |
| 1 | Nhấn nút xoá (icon thùng rác) trên dòng thành phần |
| 2 | Hệ thống hiển thị modal xác nhận "Bạn có chắc chắn muốn xoá?" |
| 3 | Nhấn "Xoá" |
| **Postcondition** | Thành phần bị xoá khỏi DB |
| **Exception** | Nếu thành phần đang được sử dụng trong Bảng chia thưởng → hiện tại chưa có check |

### UC-05: Soạn công thức
| | |
|---|---|
| **Actor** | Admin / Kế toán |
| **Precondition** | Đang ở modal tạo/sửa, mode = "Theo công thức" |
| **Main Flow** | |
| 1 | Gõ tên biến vào ô công thức → hệ thống gợi ý autocomplete |
| 2 | Hoặc nhấn vào biến trong danh sách "Biến hệ thống" để chèn |
| 3 | Hoặc nhấn vào hàm trong danh sách "Hàm tính toán" để chèn |
| 4 | Có thể tham chiếu thành phần khác bằng mã TP |
| 5 | Nhấn "Kiểm tra công thức" để validate |
| **Postcondition** | Công thức được soạn và validate thành công |
| **Alternative Flow** | Nếu công thức lỗi → hiển thị danh sách lỗi (biến không tồn tại, ngoặc sai, ...) |

---

## 4. Business Rules

| ID | Rule | Mô tả | Áp dụng tại |
|----|------|-------|-------------|
| BR-01 | Mã TP unique | Mã thành phần không được trùng trong hệ thống | UC-02, UC-03 |
| BR-02 | Mã TP max 50 ký tự | | UC-02, UC-03 |
| BR-03 | Tên max 255 ký tự | | UC-02, UC-03 |
| BR-04 | Mode chỉ có 2 giá trị | `formula` hoặc `manual` | UC-02, UC-03 |
| BR-05 | Formula nullable | Chỉ bắt buộc khi mode = formula (validate FE) | UC-02, UC-03 |
| BR-06 | Auto-gen mã TP | Frontend tự sinh TPxxx khi mở modal tạo mới | UC-02 |
| BR-07 | Audit trail | `created_by` ghi khi tạo, `updated_by` ghi khi sửa | UC-02, UC-03 |
| BR-08 | Sắp xếp danh sách | Theo `updated_at` DESC (mới nhất trước) | UC-01 |
| BR-09 | Tìm kiếm | Tìm theo `code` hoặc `name` (LIKE %keyword%) | UC-01 |
| BR-10 | Phân trang mặc định | 100 bản ghi/trang, có tuỳ chọn 10/25/50/100 | UC-01 |

---

## 5. Data Model

### 5.1. Entity Relationship

```
[BonusComponent] 1──N [BonusDistributionComponent]
[BonusComponent] N──1 [Employee] (created_by)
[BonusComponent] N──1 [Employee] (updated_by)
```

### 5.2. Bảng dữ liệu

#### Bảng: bonus_components

| Cột | Type | Nullable | Default | Mô tả |
|-----|------|----------|---------|-------|
| id | bigint PK | No | auto | |
| code | varchar(50) | No | | Mã thành phần (unique) |
| name | varchar(255) | No | | Tên thành phần |
| mode | varchar(20) | No | 'formula' | Cách tính: formula / manual |
| formula | text | Yes | null | Công thức tính |
| note | text | Yes | null | Mô tả / ghi chú |
| created_by | bigint | No | | ID người tạo (employees.id) |
| updated_by | bigint | Yes | null | ID người cập nhật |
| created_at | timestamp | Yes | | |
| updated_at | timestamp | Yes | | |

### 5.3. Enum Values

| Entity | Field | Value | Meaning |
|--------|-------|-------|---------|
| BonusComponent | mode | formula | Tính theo công thức |
| BonusComponent | mode | manual | Nhập tay thủ công |

---

## 6. API Specification

### 6.1. Danh sách thành phần

```
GET /api/v1/payroll/bonus-components
Auth: Bearer Token (JWT)
```

**Request (Query params):**
| Field | Type | Required | Mô tả |
|-------|------|----------|-------|
| page | integer | No | Trang hiện tại |
| limit | integer | No | Số bản ghi/trang (default: 10) |
| keyword | string | No | Tìm theo mã hoặc tên |

**Response (200):**
```json
{
  "data": [
    {
      "id": 1,
      "code": "TP001",
      "name": "Theo lương P1+P2",
      "mode": "formula",
      "formula": "luong_p1 + luong_p2",
      "note": "",
      "created_by": 1,
      "updated_by": null,
      "created_at": "09/04/2026 10:30:00",
      "updated_at": "09/04/2026 10:30:00"
    }
  ],
  "total": 5,
  "lastPage": 1,
  "currentPage": 1,
  "perPage": 100
}
```

### 6.2. Chi tiết thành phần

```
GET /api/v1/payroll/bonus-components/{id}
Auth: Bearer Token (JWT)
```

**Response (200):**
```json
{
  "data": {
    "id": 1,
    "code": "TP001",
    "name": "Theo lương P1+P2",
    "mode": "formula",
    "formula": "luong_p1 + luong_p2",
    "note": "",
    "created_by": 1,
    "updated_by": null
  }
}
```

**Error cases:**
| HTTP Code | Condition | Message |
|-----------|-----------|---------|
| 404 | ID không tồn tại | not found |

### 6.3. Tạo mới thành phần

```
POST /api/v1/payroll/bonus-components
Auth: Bearer Token (JWT)
```

**Request:**
| Field | Type | Required | Validate | Mô tả |
|-------|------|----------|----------|-------|
| code | string | Yes | max:50, unique | Mã thành phần |
| name | string | Yes | max:255 | Tên thành phần |
| mode | string | Yes | in:formula,manual | Cách tính |
| formula | string | No | | Công thức (nullable) |
| note | string | No | | Ghi chú |

**Response (200):**
```json
{ "message": "success", "status": 200 }
```

**Error cases:**
| HTTP Code | Condition | Message |
|-----------|-----------|---------|
| 422 | Mã trùng | Mã thành phần đã tồn tại |
| 422 | Thiếu mã | Bắt buộc nhập mã thành phần |
| 422 | Thiếu tên | Bắt buộc nhập tên thành phần |
| 422 | Mode sai | Cách tính không hợp lệ |

### 6.4. Cập nhật thành phần

```
PUT /api/v1/payroll/bonus-components/{id}
Auth: Bearer Token (JWT)
```

**Request:** Giống tạo mới. Validate `code` unique loại trừ ID hiện tại.

**Error cases:**
| HTTP Code | Condition | Message |
|-----------|-----------|---------|
| 404 | ID không tồn tại | not found |
| 422 | Validation lỗi | (giống tạo mới) |

### 6.5. Xoá thành phần

```
DELETE /api/v1/payroll/bonus-components/{id}
Auth: Bearer Token (JWT)
```

**Response (200):**
```json
{ "message": "delete success", "status": 200 }
```

**Error cases:**
| HTTP Code | Condition | Message |
|-----------|-----------|---------|
| 404 | ID không tồn tại | not found |

---

## 7. UI Specification

### 7.1. Màn hình Danh sách thành phần tính thưởng
- **Route**: `/payroll/bonus-component`
- **Layout**: Header + Search + Table + Pagination

**Wireframe:**
```
┌─────────────────────────────────────────┐
│  Thành phần tính thưởng    [Tạo TP]    │
├─────────────────────────────────────────┤
│  [Tìm kiếm...                        ] │
├─────────────────────────────────────────┤
│  STT | Mã TP | Tên | Loại | CT | Mô tả│
│  1   | TP001 | ... | CT   | ...| ...   │
│  2   | TP002 | ... | TT   | ...| ...   │
├─────────────────────────────────────────┤
│  Tổng: 5    [10|25|50|100] [< 1 2 >]   │
└─────────────────────────────────────────┘
```

**User interactions:**
| Action | Behavior | API call |
|--------|----------|----------|
| Nhập keyword | Tìm kiếm debounce 300ms | GET /bonus-components?keyword= |
| Click "Tạo thành phần" | Mở modal tạo mới | - |
| Click icon sửa | Mở modal sửa với data | GET /bonus-components/{id} |
| Click icon xoá | Mở modal xác nhận | - |
| Xác nhận xoá | Xoá và reload | DELETE /bonus-components/{id} |

### 7.2. Modal tạo/sửa thành phần
- **Layout**: Modal XL với form + formula editor

**Wireframe:**
```
┌─────────────────────────────────────────┐
│  Tạo thành phần tính thưởng      [X]   │
├─────────────────────────────────────────┤
│  [Mã TP*] [Tên thành phần*]            │
│  [Cách tính: Công thức ▼] [Ghi chú   ] │
│                                         │
│  ┌── Preview công thức ──────────────┐  │
│  │ luong_p1 + luong_p2              │  │
│  └───────────────────────────────────┘  │
│  ┌── Soạn công thức ────────────────┐  │
│  │ [textarea with autocomplete]      │  │
│  └───────────────────────────────────┘  │
│  [Kiểm tra công thức]                   │
│                                         │
│  Biến hệ thống:                         │
│  [luong_p1] [luong_p2] [ds_net_nv] ... │
│                                         │
│  Thành phần khác: [TP001] [TP002] ...   │
│  Hàm: [IF] [MAX] [MIN] [ROUND] ...     │
├─────────────────────────────────────────┤
│                        [Huỷ]   [Lưu]   │
└─────────────────────────────────────────┘
```

---

## 8. Biến hệ thống

### 8.1. Biến HRM (từ BonusVariableService)

| Code | Tên | Nguồn |
|------|-----|-------|
| luong_p1 | Lương P1 | employee_salary_histories.base_salary |
| luong_p2 | Lương P2 | employee_salary_histories.p2_salary |
| luong_p3 | Lương P3 | employee_salary_histories.p3_salary |
| tham_nien | Thâm niên (tháng) | Tính từ employee_infos.enter_date |
| so_thang_lam_viec | Số tháng làm việc trong năm | timesheet_summaries (đếm tháng đủ ngày công) |

### 8.2. Biến ERP — Nhân viên (từ BonusVariableAggregatorService)

| Code | Tên |
|------|-----|
| dstc_dk_dau_nam_nv | DSTC đăng ký đầu năm của NV |
| dstc_quyet_toan_nv | DSTC đã quyết toán của NV |
| dstc_hd_hieu_luc_nv | DSTC hợp đồng hiệu lực của NV |
| gia_tri_hd_hieu_luc_nv | Giá trị HĐ hiệu lực của NV |
| gia_tri_hd_truoc_thue_nv | Giá trị HĐ trước thuế của NV |
| ds_net_nv | Doanh số net của NV |
| ds_thuc_xuat_nv | Doanh số thực xuất của NV |
| so_tien_thuc_thu_nv | Tiền thực thu của NV |
| cong_no_kh_nv | Công nợ KH của NV |
| ty_le_ht_kh_ds_hd_nv | Tỷ lệ HT DS theo HĐ của NV |
| ty_le_ht_kh_dstc_hd_nv | Tỷ lệ HT DSTC theo HĐ của NV |
| ty_le_ht_kh_dstc_qt_nv | Tỷ lệ HT DSTC quyết toán của NV |
| ty_le_tong_th_ds_hd_nv | Tỷ lệ tổng TH DS theo HĐ của NV |
| ty_le_tong_th_dstc_hd_nv | Tỷ lệ tổng TH DSTC theo HĐ của NV |
| ty_le_tong_th_dstc_qt_nv | Tỷ lệ tổng TH DSTC QT của NV |

### 8.3. Biến ERP — Phòng ban (summary)

| Code | Tên |
|------|-----|
| dstc_dk_dau_nam_phong | DSTC đăng ký đầu năm của phòng |
| dstc_quyet_toan_phong | DSTC đã quyết toán của phòng |
| dstc_hd_hieu_luc_phong | DSTC hợp đồng hiệu lực của phòng |
| gia_tri_hd_hieu_luc_phong | Giá trị HĐ hiệu lực của phòng |
| gia_tri_hd_truoc_thue_phong | Giá trị HĐ trước thuế của phòng |
| ds_net_phong | Doanh số net của phòng |
| ds_thuc_xuat_phong | Doanh số thực xuất của phòng |
| so_tien_thuc_thu_phong | Tiền thực thu của phòng |
| cong_no_kh_phong | Công nợ KH của phòng |

### 8.4. Hàm tính toán

| Hàm | Cú pháp | Mô tả |
|-----|---------|-------|
| IF | IF(điều_kiện, giá_trị_đúng, giá_trị_sai) | Hàm điều kiện |
| MAX | MAX(a, b) | Giá trị lớn nhất |
| MIN | MIN(a, b) | Giá trị nhỏ nhất |
| ROUND | ROUND(number, digits) | Làm tròn |
| SUM | SUM(a, b, c) | Tổng |
| AVG | AVG(a, b, c) | Trung bình |
| ABS | ABS(number) | Giá trị tuyệt đối |
| CEILING | CEILING(number) | Làm tròn lên |
| FLOOR | FLOOR(number) | Làm tròn xuống |

---

## 9. Non-functional Requirements

- **Performance**: Danh sách phân trang, không load toàn bộ
- **Security**: JWT auth, chỉ user có quyền mới thao tác được
- **Compatibility**: PHP 7.4, Laravel 8, Nuxt 2, Vue 2
- **Browser**: Chrome, Firefox, Safari, Edge

---

## 10. Phụ lục

### 10.1. File references

| Layer | File path |
|-------|-----------|
| Migration | `Modules/Payroll/Database/Migrations/2026_04_01_000000_create_bonus_components_table.php` |
| Entity | `Modules/Payroll/Entities/BonusComponent.php` |
| Controller | `Modules/Payroll/Http/Controllers/Api/V1/BonusComponentController.php` |
| Service | `Modules/Payroll/Services/BonusComponentService.php` |
| Create Request | `Modules/Payroll/Http/Requests/CreateBonusComponentRequest.php` |
| Update Request | `Modules/Payroll/Http/Requests/UpdateBonusComponentRequest.php` |
| List Resource | `Modules/Payroll/Transformers/BonusComponentResource/BonusComponentListResource.php` |
| Detail Resource | `Modules/Payroll/Transformers/BonusComponentResource/BonusComponentDetailResource.php` |
| Routes | `Modules/Payroll/Routes/api.php` (lines 334-340) |
| FE Page | `pages/payroll/bonus-component/index.vue` |
