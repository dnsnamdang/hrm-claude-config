# SRS: BOM List — Quản lý danh mục hàng hoá giải pháp

| Thông tin | Chi tiết |
|-----------|----------|
| Module | Assign (Quản lý dự án) |
| Phiên bản | 1.0 |
| Ngày tạo | 2026-04-13 |
| Trạng thái | Approved |

---

## 1. Giới thiệu

### 1.1. Mục đích
BOM List (Bill of Materials) quản lý danh mục hàng hoá/dịch vụ cần thiết cho mỗi giải pháp hoặc hạng mục trong dự án. Hỗ trợ tạo, phân nhóm, tổng hợp BOM từ nhiều hạng mục, xây dựng giá và phê duyệt giá theo quy chế nội bộ.

### 1.2. Phạm vi

**Trong scope:**
- CRUD BOM List (tạo, sửa, xem, xoá)
- Phân loại: BOM Thành phần / BOM Tổng hợp
- Phân nhóm hàng hoá trong BOM
- Import/Export Excel danh sách sản phẩm
- Xuất Excel danh sách BOM
- Gộp BOM con vào BOM tổng hợp
- Workflow duyệt BOM (qua hồ sơ trình duyệt giải pháp)
- Workflow xây dựng giá + phê duyệt giá 3 cấp
- Cấu hình ngưỡng duyệt giá (giá trị đơn hàng + tỷ suất lợi nhuận)
- Lịch sử phê duyệt giá
- Phân quyền xem theo cấp (công ty / phòng ban / bộ phận)

**Ngoài scope:**
- Quản lý kho / xuất nhập kho
- Đặt hàng / mua hàng từ nhà cung cấp
- Báo giá gửi khách hàng (output từ BOM đã duyệt giá)

### 1.3. Thuật ngữ

| Thuật ngữ | Giải thích |
|-----------|-----------|
| BOM | Bill of Materials — Danh mục vật tư / hàng hoá |
| BOM Thành phần | BOM chứa danh sách sản phẩm trực tiếp (type=1) |
| BOM Tổng hợp | BOM gộp từ nhiều BOM con (type=2) |
| BOM cấp Giải pháp | BOM tổng hợp không gắn hạng mục, gắn trực tiếp giải pháp |
| BOM cấp Hạng mục | BOM gắn hạng mục cụ thể trong giải pháp |
| Hàng cha | Sản phẩm chính trong BOM (parent, parent_id = null) |
| Hàng con | Sản phẩm phụ thuộc hàng cha (child, parent_id != null) |
| Nhóm hàng | Phân loại sản phẩm theo nhóm trong BOM (vd: Nhóm điều khiển, Nhóm cảm biến) |
| V | Giá trị đơn hàng = Tổng thành tiền bán (quy đổi VNĐ) |
| M | Tỷ suất lợi nhuận = ((Tổng bán − Tổng nhập) / Tổng nhập) × 100% |
| PM | Project Manager — Quản lý dự án |
| TP | Trưởng phòng |
| BGĐ | Ban giám đốc |

---

## 2. Actors & Permissions

### 2.1. Phân quyền xem danh sách

| Permission | Mô tả | Phạm vi dữ liệu |
|-----------|-------|-----------------|
| Xem tất cả danh sách BOM List | Xem toàn bộ BOM (trừ status Đang tạo của người khác) | Tất cả |
| Xem danh sách BOM List theo công ty | Xem BOM cùng công ty + BOM do mình tạo | company_id |
| Xem danh sách BOM List theo phòng ban | Xem BOM cùng phòng ban quản lý + BOM do mình tạo | department_id |
| Xem danh sách BOM List theo bộ phận | Xem BOM cùng bộ phận quản lý + BOM do mình tạo | part_id |

### 2.2. Phân quyền thao tác

| Permission | Mô tả |
|-----------|-------|
| Tạo BOM List | Tạo mới + sửa BOM (status 1, 2) |
| Xây dựng giá Bom giải pháp | Truy cập màn làm giá, nhập giá nhập/bán |
| Trưởng phòng duyệt giá Bom giải pháp | Duyệt/từ chối giá cấp TP (status 9) |
| Ban giám đốc duyệt giá Bom giải pháp | Duyệt/từ chối giá cấp BGĐ (status 9, 10) |

Tất cả permissions thuộc group `BOM List`, type = 4, guard = `api`.

---

## 3. Use Cases

### UC-01: Tạo BOM List

| | |
|---|---|
| **Actor** | Nhân viên có quyền "Tạo BOM List" |
| **Precondition** | Dự án TKT + Giải pháp đã tồn tại |
| **Main Flow** | |
| 1 | Vào menu Dự án TKT → BOM Giải pháp → Tạo mới |
| 2 | Nhập thông tin: Tên BOM, Dự án, Giải pháp, Hạng mục (tuỳ chọn), Khách hàng, Loại BOM, Tiền tệ |
| 3 | Thêm sản phẩm (hàng cha/con) — nhập thủ công hoặc chọn từ ERP |
| 4 | Phân nhóm hàng hoá (tuỳ chọn) |
| 5 | Lưu nháp (status=1) hoặc Lưu BOM (status=2) |
| **Postcondition** | BOM được tạo với mã tự sinh BOM-YYYY-NNNNN |
| **Alternative Flow** | Import sản phẩm từ Excel thay vì nhập thủ công |
| **Validation** | Tên BOM unique. Khi lưu (không phải nháp): Tên, Dự án, Giải pháp, Khách hàng bắt buộc |

### UC-02: Sửa BOM List

| | |
|---|---|
| **Actor** | Nhân viên có quyền "Tạo BOM List" |
| **Precondition** | BOM ở status Đang tạo (1) hoặc Hoàn thành (2) |
| **Main Flow** | |
| 1 | Từ danh sách, click icon Sửa hoặc vào chi tiết → Sửa |
| 2 | Chỉnh sửa thông tin + sản phẩm |
| 3 | Lưu nháp hoặc Lưu BOM |
| **Exception** | BOM ở status khác 1, 2 → không cho sửa, redirect về trang chi tiết |

### UC-03: Xoá BOM List

| | |
|---|---|
| **Actor** | Người tạo BOM + có quyền "Tạo BOM List" |
| **Precondition** | BOM ở status Đang tạo (1) + do chính user tạo |
| **Main Flow** | Từ danh sách, click icon Xoá → xác nhận → xoá BOM + products + groups + relations |

### UC-04: Tạo BOM Tổng hợp (gộp BOM con)

| | |
|---|---|
| **Actor** | Nhân viên có quyền "Tạo BOM List" |
| **Precondition** | Chọn loại BOM = Tổng hợp |
| **Main Flow** | |
| 1 | Chọn loại BOM = Tổng hợp |
| 2 | Click "Chọn BL con" → chọn các BOM con cùng dự án + giải pháp |
| 3 | Hệ thống gộp sản phẩm từ BOM con vào BOM tổng hợp |
| **Business Rules** | |
| | Các BOM con phải có cùng cấu trúc nhóm hàng |
| | Sản phẩm trùng KHÔNG gộp số lượng — giữ nguyên từng dòng |
| | BOM con phải cùng loại tiền tệ |
| | BOM cấp GP: chỉ chọn BOM tổng hợp hạng mục ở status "Đã duyệt" (4) |
| | 1 GP/HM chỉ có 1 BOM tổng hợp trên 1 version |

### UC-05: Xem chi tiết BOM

| | |
|---|---|
| **Actor** | Nhân viên có quyền xem |
| **Main Flow** | Click vào BOM → xem readonly toàn bộ thông tin + sản phẩm |
| **Footer Buttons** | Quay lại (luôn hiện), Sửa (nếu status 1/2), Xuất Excel, Yêu cầu XD giá (nếu đủ ĐK), Duyệt/Từ chối giá (nếu đủ ĐK), Lịch sử phê duyệt |

### UC-06: Export Excel sản phẩm BOM

| | |
|---|---|
| **Actor** | Nhân viên có quyền xem |
| **Main Flow** | Từ chi tiết BOM → Xuất Excel → chọn fields → download file .xlsx |
| **Output** | File Excel với dòng tiêu đề, header, data theo nhóm hàng |

### UC-07: Import Excel sản phẩm vào BOM

| | |
|---|---|
| **Actor** | Nhân viên có quyền "Tạo BOM List" |
| **Precondition** | BOM loại Thành phần, status cho sửa |
| **Main Flow** | Tải template → điền data → upload → validate → import |

### UC-08: Xuất Excel danh sách BOM

| | |
|---|---|
| **Actor** | Nhân viên có quyền xem |
| **Main Flow** | Từ danh sách BOM → Xuất Excel → xuất theo filter + cột hiển thị |

### UC-09: Yêu cầu xây dựng giá

| | |
|---|---|
| **Actor** | PM (hoặc nhân viên) |
| **Precondition** | BOM tổng hợp cấp GP + status = Đã duyệt (4) |
| **Main Flow** | |
| 1 | Click "Yêu cầu xây dựng giá" (từ danh sách hoặc chi tiết) |
| 2 | Xác nhận popup |
| 3 | BOM chuyển status → Chờ xây dựng giá (7) |
| 4 | Notification gửi cho users có quyền "Xây dựng giá Bom giải pháp" |

### UC-10: Xây dựng giá BOM

| | |
|---|---|
| **Actor** | Nhân viên có quyền "Xây dựng giá Bom giải pháp" |
| **Precondition** | BOM status = Chờ XD giá (7) hoặc Đang XD giá (8) |
| **Main Flow** | |
| 1 | Vào menu Phê duyệt → BOM chờ xây dựng giá → click BOM |
| 2 | Màn làm giá: chỉ sửa được Giá nhập + Giá bán |
| 3 | Footer realtime: Tổng nhập, Tổng bán, Tỷ suất LN%, Cấp duyệt dự kiến |
| 4a | Lưu nháp → status=8 → redirect về danh sách |
| 4b | Gửi duyệt → validate giá > 0 → tính cấp → popup confirm → xử lý |
| **Postcondition** | Cấp 1: tự duyệt → status=11. Cấp 2: → status=9. Cấp 3: → status=10 |

### UC-11: Duyệt giá BOM (TP/BGĐ)

| | |
|---|---|
| **Actor** | TP (status 9) hoặc BGĐ (status 9, 10) |
| **Precondition** | BOM ở status Chờ TP/BGĐ duyệt giá + user có quyền tương ứng |
| **Main Flow** | |
| 1 | Vào menu Phê duyệt → BOM chờ duyệt giá |
| 2a | Duyệt → popup confirm → status=11 + notify người làm giá |
| 2b | Từ chối → popup nhập lý do (bắt buộc) → status=8 + notify người làm giá |
| **Alternative** | Duyệt/Từ chối từ trang chi tiết BOM |

### UC-12: Cấu hình ngưỡng duyệt giá

| | |
|---|---|
| **Actor** | Admin (quyền cấu hình phân hệ) |
| **Main Flow** | |
| 1 | Vào Danh mục & Cấu hình → Cấu hình duyệt giá BOM |
| 2 | Sửa ngưỡng: Giá trị đơn hàng (VNĐ) — chỉ sửa "Đến", "Từ" cấp sau tự cập nhật |
| 3 | Sửa ngưỡng: Tỷ suất LN (%) — sửa "Từ" cấp 1,2 → "Đến" cấp dưới auto |
| 4 | Lưu cấu hình → ghi audit log |

### UC-13: Xem lịch sử phê duyệt giá

| | |
|---|---|
| **Actor** | Nhân viên có quyền xem BOM |
| **Precondition** | BOM đã từng vào flow pricing (status ≥ 7 hoặc có price_requested_at) |
| **Main Flow** | Click icon Lịch sử → modal timeline hiển thị toàn bộ actions |

---

## 4. Business Rules

| ID | Rule | Mô tả | Áp dụng tại |
|----|------|-------|-------------|
| BR-01 | Mã BOM tự sinh | Format: BOM-YYYY-NNNNN (auto-increment) | UC-01 |
| BR-02 | Tên BOM unique | Không trùng tên trong toàn hệ thống | UC-01, UC-02 |
| BR-03 | Draft mode | Lưu nháp (status=1): bỏ required Tên/Dự án/GP/KH | UC-01, UC-02 |
| BR-04 | Chỉ sửa status 1, 2 | BOM ở status khác → không cho sửa | UC-02 |
| BR-05 | Chỉ xoá status 1 + người tạo | Chỉ người tạo mới xoá + chỉ status Đang tạo | UC-03 |
| BR-06 | BOM cấp GP = Tổng hợp | GP có hạng mục con → BOM cấp GP chỉ được loại Tổng hợp | UC-04 |
| BR-07 | Unique aggregate per version | 1 GP/HM chỉ có 1 BOM tổng hợp trên cùng 1 version | UC-04 |
| BR-08 | Gộp BOM: cùng cấu trúc | BOM con phải cùng cấu trúc nhóm hàng | UC-04 |
| BR-09 | Gộp BOM: không gộp qty | Sản phẩm trùng giữ nguyên, không cộng số lượng | UC-04 |
| BR-10 | Gộp BOM: cùng tiền tệ | BOM con phải cùng loại tiền tệ với BOM tổng hợp | UC-04 |
| BR-11 | BOM cấp GP chọn BOM con Đã duyệt | Chỉ gộp BOM tổng hợp hạng mục status=4 | UC-04 |
| BR-12 | Ẩn BOM Đang tạo | Status=1 chỉ hiện cho người tạo | Danh sách |
| BR-13 | Cấp duyệt giá | Final = MAX(Level_V, Level_M) | UC-10 |
| BR-14 | Quy đổi VNĐ | V = Tổng bán × exchange_rate (từ currency BOM) | UC-10 |
| BR-15 | M% không quy đổi | Tỷ suất LN là tỷ lệ, không phụ thuộc tiền tệ | UC-10 |
| BR-16 | Validate giá > 0 | Tất cả sản phẩm phải có giá nhập + giá bán > 0 trước khi gửi duyệt | UC-10 |
| BR-17 | Từ chối bắt buộc lý do | Khi từ chối giá phải nhập lý do | UC-11 |
| BR-18 | Từ chối → Đang XD giá | BOM bị từ chối quay về status=8 để sửa lại | UC-11 |
| BR-19 | Dịch vụ không có con | Sản phẩm loại Dịch vụ không được thêm hàng con | UC-01 |
| BR-20 | Dịch vụ không có Model/Brand/Origin | Sản phẩm loại Dịch vụ clear 3 trường này | UC-01 |

---

## 5. Data Model

### 5.1. Entity Relationship

```
ProspectiveProject 1──N BomList
Solution           1──N BomList
SolutionModule     1──N BomList
Customer           1──N BomList
TpCurrency         1──N BomList

BomList 1──N BomListProduct
BomList 1──N BomListGroup
BomList 1──N BomListRelation (parent)
BomList 1──N BomPricingHistory

BomListGroup 1──N BomListProduct

BomPriceApprovalConfig 1──N BomPriceApprovalConfigLog
```

### 5.2. Bảng dữ liệu

#### Bảng: bom_lists

| Cột | Type | Nullable | Default | Mô tả |
|-----|------|----------|---------|-------|
| id | bigint PK | No | auto | |
| name | string | No | | Tên BOM (unique) |
| code | string | No | | Mã BOM (unique, auto: BOM-YYYY-NNNNN) |
| prospective_project_id | integer | Yes | | FK dự án TKT |
| solution_id | integer | Yes | | FK giải pháp |
| solution_module_id | integer | Yes | | FK hạng mục (null = cấp GP) |
| customer_id | integer | Yes | | FK khách hàng |
| note | text | Yes | | Ghi chú |
| bom_list_type | integer | Yes | | 1=Thành phần, 2=Tổng hợp |
| status | tinyint | No | 1 | Trạng thái (1-11) |
| currency_id | bigint | Yes | | FK loại tiền tệ |
| solution_version_id | bigint | Yes | | FK version giải pháp |
| solution_module_version_id | bigint | Yes | | FK version hạng mục |
| company_id | integer | Yes | | FK công ty (phân quyền) |
| department_id | integer | Yes | | FK phòng ban (phân quyền) |
| part_id | integer | Yes | | FK bộ phận (phân quyền) |
| price_requested_by | bigint | Yes | | PM yêu cầu XD giá |
| price_requested_at | timestamp | Yes | | Thời gian yêu cầu |
| price_approved_by | bigint | Yes | | Người duyệt giá |
| price_approved_at | timestamp | Yes | | Thời gian duyệt |
| price_rejected_reason | text | Yes | | Lý do từ chối |
| price_approval_level | tinyint | Yes | | Cấp duyệt (1/2/3) |
| created_by | integer | Yes | | Người tạo |
| updated_by | integer | Yes | | Người cập nhật |
| created_at, updated_at | timestamp | | | |

#### Bảng: bom_list_products

| Cột | Type | Nullable | Default | Mô tả |
|-----|------|----------|---------|-------|
| id | bigint PK | No | auto | |
| bom_list_id | integer | Yes | | FK BOM |
| bom_list_group_id | integer | Yes | | FK nhóm hàng |
| parent_id | integer | Yes | | FK hàng cha (null = hàng cha) |
| product_project_id | integer | Yes | | FK hàng hoá dự án |
| erp_product_id | bigint | Yes | | FK sản phẩm ERP |
| product_type | tinyint | No | 1 | 1=Hàng hoá, 2=Dịch vụ |
| model_id | integer | Yes | | FK model |
| brand_id | integer | Yes | | FK thương hiệu |
| origin_id | integer | Yes | | FK xuất xứ |
| unit_id | integer | Yes | | FK đơn vị tính |
| qty_needed | float(16,2) | Yes | | Số lượng |
| product_attributes | text | Yes | | Thông số kỹ thuật |
| estimated_price | float(16,2) | Yes | | Giá nhập |
| quoted_price | float(16,2) | Yes | | Giá bán |

**Computed fields (appends):** import_total, sale_total, profit_margin

#### Bảng: bom_list_groups

| Cột | Type | Nullable | Mô tả |
|-----|------|----------|-------|
| id | bigint PK | No | |
| bom_list_id | integer | No | FK BOM |
| name | string | No | Tên nhóm |
| sort_order | integer | No (default 0) | Thứ tự |

#### Bảng: bom_list_relations

| Cột | Type | Nullable | Mô tả |
|-----|------|----------|-------|
| id | bigint PK | No | |
| parent_bom_list_id | integer | Yes | BOM cha (tổng hợp) |
| child_bom_list_id | integer | Yes | BOM con |

#### Bảng: bom_price_approval_configs

| Cột | Type | Nullable | Mô tả |
|-----|------|----------|-------|
| id | bigint PK | No | |
| type | enum | No | order_value / profit_margin |
| level | tinyint | No | 1/2/3 |
| min_value | decimal(15,2) | Yes | Ngưỡng dưới (null = −∞) |
| max_value | decimal(15,2) | Yes | Ngưỡng trên (null = +∞) |
| description | text | Yes | Auto-generated |
| updated_by | bigint | Yes | |

#### Bảng: bom_pricing_histories

| Cột | Type | Nullable | Mô tả |
|-----|------|----------|-------|
| id | bigint PK | No | |
| bom_list_id | bigint | No | FK BOM |
| action | string | No | request_pricing / save_draft / submit_pricing / self_approve / approve / reject |
| from_status | tinyint | Yes | Status trước |
| to_status | tinyint | Yes | Status sau |
| approval_level | tinyint | Yes | Cấp duyệt |
| note | text | Yes | Lý do từ chối |
| performed_by | bigint | No | Người thực hiện |
| created_at | timestamp | Yes | |

### 5.3. Enum Values

#### BOM List Status

| Value | Constant | Tên | Màu | Ghi chú |
|-------|----------|-----|-----|---------|
| 1 | STATUS_DANG_TAO | Đang tạo | #FF9800 | Chỉ người tạo thấy |
| 2 | STATUS_HOAN_THANH | Hoàn thành | #4CAF50 | |
| 3 | STATUS_CHO_DUYET | Chờ duyệt | #2196F3 | Qua hồ sơ trình duyệt GP |
| 4 | STATUS_DA_DUYET | Đã duyệt | #9C27B0 | |
| 5 | STATUS_DA_DUOC_TONG_HOP | Đã được tổng hợp | #9E9E9E | |
| 6 | STATUS_KHONG_DUYET | Không duyệt | #F44336 | |
| 7 | STATUS_CHO_XAY_DUNG_GIA | Chờ xây dựng giá | #FF9800 | |
| 8 | STATUS_DANG_XAY_DUNG_GIA | Đang xây dựng giá | #03A9F4 | |
| 9 | STATUS_CHO_TP_DUYET_GIA | Chờ TP duyệt giá | #673AB7 | |
| 10 | STATUS_CHO_BGD_DUYET_GIA | Chờ BGĐ duyệt giá | #E91E63 | |
| 11 | STATUS_DA_DUYET_GIA | Đã duyệt giá | #009688 | |

#### BOM List Type

| Value | Constant | Tên | Màu |
|-------|----------|-----|-----|
| 1 | TYPE_COMPONENT | Thành phần | #607D8B |
| 2 | TYPE_AGGREGATE | Tổng hợp | #3F51B5 |

#### Product Type

| Value | Tên |
|-------|-----|
| 1 | Hàng hoá |
| 2 | Dịch vụ |

---

## 6. API Specification

Base URL: `/api/v1/assign`

### 6.1. Danh sách BOM List

```
GET /bom-lists
Auth: Bearer Token (JWT)
```

**Request (Query):**

| Field | Type | Required | Mô tả |
|-------|------|----------|-------|
| keyword | string | No | Tìm theo mã/tên BOM |
| company_id | integer | No | Lọc công ty |
| department_id | integer | No | Lọc phòng ban |
| part_id | integer | No | Lọc bộ phận |
| prospective_project_id | integer | No | Lọc dự án |
| solution_id | integer | No | Lọc giải pháp |
| solution_module_id | integer | No | Lọc hạng mục |
| customer_id | integer | No | Lọc khách hàng |
| created_by | integer | No | Lọc người tạo |
| status | integer | No | Lọc trạng thái |
| bom_list_type | integer | No | Lọc loại BOM |
| created_at_from | date | No | Từ ngày |
| created_at_to | date | No | Đến ngày |
| sort_field | string | No | Cột sort (default: created_at) |
| sort_dir | string | No | asc/desc (default: desc) |
| page, per_page | integer | No | Phân trang |

**Response (200):** Paginated list với fields từ BomListListResource (code, name, project, solution, module, customer, status, PM, phòng GP, phòng KD, NV KD, version, pricing fields...)

### 6.2. Chi tiết BOM

```
GET /bom-lists/{id}
```

**Response (200):** DetailBomListResource — full BOM data + products + groups + sub_bom_list_ids + currency

### 6.3. Tạo BOM

```
POST /bom-lists
```

**Request (JSON Body):** name, prospective_project_id, solution_id, solution_module_id, customer_id, note, bom_list_type, currency_id, status, groups (array products), bom_groups (array), sub_bom_list_ids (array)

### 6.4. Cập nhật BOM

```
PUT /bom-lists/{id}
```

**Validation:** Chỉ status 1, 2 mới cho sửa. Cùng payload như tạo.

### 6.5. Xoá BOM

```
DELETE /bom-lists/{id}
```

### 6.6. Yêu cầu xây dựng giá

```
POST /bom-lists/{id}/request-pricing
```

**Validate:** status=4, type=aggregate. **Result:** status→7, notify users quyền build-price.

### 6.7. Lưu nháp giá

```
PUT /bom-lists/{id}/save-pricing-draft
```

**Request:** `{ products: [{ id, estimated_price, quoted_price }] }`
**Validate:** status IN (7,8). **Result:** update prices, status→8.

### 6.8. Tính cấp duyệt (không đổi status)

```
GET /bom-lists/{id}/calculate-pricing-level
```

**Response:** `{ total_import, total_sale, profit_margin_percent, exchange_rate, currency_code, total_sale_vnd, total_import_vnd, level }`

### 6.9. Gửi duyệt giá

```
POST /bom-lists/{id}/submit-pricing
```

**Validate:** status IN (7,8), giá > 0. **Result:** tính level, set price_approval_level. Cấp 1→giữ status. Cấp 2→status=9. Cấp 3→status=10.

### 6.10. Tự duyệt giá (cấp 1)

```
POST /bom-lists/{id}/self-approve-pricing
```

**Validate:** price_approval_level=1, status IN (7,8). **Result:** status→11.

### 6.11. Duyệt giá (TP/BGĐ)

```
POST /bom-lists/{id}/approve-pricing
```

**Validate:** status IN (9,10), user có quyền tương ứng. **Result:** status→11, notify người làm giá.

### 6.12. Từ chối giá

```
POST /bom-lists/{id}/reject-pricing
```

**Request:** `{ reason: "..." }` (bắt buộc)
**Validate:** status IN (9,10). **Result:** status→8, ghi reason, notify người làm giá.

### 6.13. Lịch sử phê duyệt

```
GET /bom-lists/{id}/pricing-history
```

**Response:** Array timeline entries: action, action_label, from/to status, level, note, performed_by_name, created_at.

### 6.14. Cấu hình duyệt giá

```
GET  /bom-price-approval-configs          → 6 rows config
GET  /bom-price-approval-configs/logs     → audit log paginated
PUT  /bom-price-approval-configs/{id}     → update ngưỡng + ghi log
```

### 6.15. Các API khác

```
GET  /bom-lists/getAll                    → tất cả BOM (cho dropdown)
GET  /bom-lists/currencies                → danh sách tiền tệ
GET  /bom-lists/export-list               → xuất Excel danh sách
GET  /bom-lists/{id}/export               → xuất Excel sản phẩm BOM
GET  /bom-lists/import-template           → tải template import
POST /bom-lists/import/validate-data      → validate data import
POST /bom-lists/{id}/import/validate      → validate trước import
POST /bom-lists/{id}/import               → import sản phẩm
GET  /bom-lists/erp-products              → tìm sản phẩm ERP
GET  /bom-lists/{id}/bom-products         → tìm sản phẩm trong BOM
GET  /bom-lists/pending-pricing           → DS BOM chờ XD giá (status 7,8)
GET  /bom-lists/pending-price-approval    → DS BOM chờ duyệt giá (status 9,10)
```

---

## 7. UI Specification

### 7.1. Danh sách BOM List (`/assign/bom-list`)

**Filter:** Quick search + Advanced (Công ty→PB→BP cascading, Dự án→GP→HM cascading, KH, Người tạo, Trạng thái, Loại BOM, Ngày tạo)

**Table:** V2BaseDataTable với sticky columns, column customization, hover row-actions

**Row Actions:** Xem | Sửa (status 1,2) | Export | YC xây dựng giá (status 4, aggregate, GP-level) | Lịch sử (status≥7) | Xoá (status 1, người tạo)

### 7.2. Tạo/Sửa BOM (`/assign/bom-list/add`, `/assign/bom-list/:id/edit`)

**Component:** BomBuilderEditor — InfoCard (thông tin BOM) + TableCard (bảng sản phẩm) + FooterBar (Quay lại, Lưu nháp, Lưu BOM)

### 7.3. Chi tiết BOM (`/assign/bom-list/:id`)

**Component:** BomBuilderEditor viewOnly + contextual footer buttons

### 7.4. Màn làm giá (`/assign/bom-list/:id/pricing`)

**Component:** BomBuilderEditor pricingMode — chỉ unlock Giá nhập + Giá bán. Thu gọn card thông tin. Footer: Tổng nhập | Tổng bán | Quy đổi VNĐ (nếu khác VND) | Tỷ suất LN% | Cấp duyệt dự kiến | Quay lại | Lưu nháp | Gửi duyệt

### 7.5. BOM chờ XD giá (`/assign/bom-list/pending-pricing`)

**Menu:** Phê duyệt → BOM chờ xây dựng giá (quyền: Xây dựng giá Bom giải pháp)

**Cột:** STT | Mã•Tên BOM | Dự án | GP | Version GP | Phòng GP | PM | Phòng KD | NV KD | KH | Người YC | Ngày YC | Trạng thái

### 7.6. BOM chờ duyệt giá (`/assign/bom-list/pending-price-approval`)

**Menu:** Phê duyệt → BOM chờ duyệt giá (quyền: TP hoặc BGĐ duyệt giá)

**Cột:** STT | Mã•Tên BOM | Dự án | GP | Version GP | Phòng GP | PM | Phòng KD | NV KD | KH | Cấp duyệt | Ngày gửi | Trạng thái

**Row Actions:** Xem | Duyệt (xanh) | Từ chối (đỏ) | Lịch sử

### 7.7. Cấu hình duyệt giá (`/assign/settings/price-approval`)

**Menu:** Danh mục & Cấu hình → Cấu hình duyệt giá BOM

**2 section:**
- Giá trị đơn hàng (VNĐ): 3 rows, input V2BaseCurrencyInput cho "Đến", "Từ" auto
- Tỷ suất LN (%): 3 rows, input number cho "Từ" cấp 1,2 → "Đến" cấp dưới auto. Cấp 3 Từ=−∞

**Audit log** timeline bên dưới

---

## 8. Status Flow Diagram

```
[1 Đang tạo] ──Lưu──→ [2 Hoàn thành]
                              │
                    (qua hồ sơ trình duyệt GP)
                              ↓
                       [3 Chờ duyệt]
                         ↙        ↘
              [6 Không duyệt]   [4 Đã duyệt]
                                     │
                         (gộp vào BOM GP)──→ [5 Đã được tổng hợp]
                                     │
                        (YC xây dựng giá)
                                     ↓
                       [7 Chờ xây dựng giá]
                                     │
                          (lưu nháp giá)
                                     ↓
                      [8 Đang xây dựng giá] ←──(từ chối)──┐
                                     │                      │
                         (gửi duyệt giá)                   │
                           ↙    |    ↘                      │
                     Cấp 1  Cấp 2  Cấp 3                  │
                       ↓       ↓       ↓                    │
                 (tự duyệt) [9 Chờ TP] [10 Chờ BGĐ]───────┘
                       ↓       ↓       ↓          (duyệt)
                       └───────┴───────┘──────→ [11 Đã duyệt giá]
```

---

## 9. Approval Level Matrix

### Công thức

```
V = SUM(quoted_price × qty_needed) × exchange_rate  (quy đổi VNĐ)
M = ((Tổng bán − Tổng nhập) / Tổng nhập) × 100%
Final_Level = MAX(Level_V, Level_M)
```

### Ma trận quyết định (mặc định)

|  | M ≥ 20% (L1) | 10% ≤ M < 20% (L2) | M < 10% (L3) |
|--|--------------|--------------------|--------------| 
| V ≤ 1B (L1) | **Cấp 1** — Tự duyệt | **Cấp 2** — TP | **Cấp 3** — BGĐ |
| 1B < V ≤ 20B (L2) | **Cấp 2** — TP | **Cấp 2** — TP | **Cấp 3** — BGĐ |
| V > 20B (L3) | **Cấp 3** — BGĐ | **Cấp 3** — BGĐ | **Cấp 3** — BGĐ |

Các ngưỡng có thể cấu hình tại `/assign/settings/price-approval`.

---

## 10. Non-functional Requirements

- **Tech Stack**: PHP 7.4, Laravel 8, Nuxt 2 (Vue 2), MySQL, Redis
- **Auth**: JWT (tymon/jwt-auth)
- **Permission**: spatie/laravel-permission
- **Excel**: maatwebsite/excel (FromView + WithEvents)
- **Notification**: Database + Broadcast channel (Redis publish + bell icon)
- **Browser**: Chrome, Firefox, Safari, Edge

---

## 11. Phụ lục — File References

| Layer | File path |
|-------|-----------|
| Migration | `database/migrations/2026_03_18_*` ~ `2026_04_13_*` (12 files) |
| Entity | `Modules/Assign/Entities/BomList.php`, `BomListProduct.php`, `BomListGroup.php`, `BomListRelation.php`, `BomPriceApprovalConfig.php`, `BomPriceApprovalConfigLog.php`, `BomPricingHistory.php` |
| Controller | `Modules/Assign/Http/Controllers/Api/V1/BomListController.php`, `BomPriceApprovalConfigController.php` |
| Service | `Modules/Assign/Services/BomListService.php`, `BomPriceApprovalConfigService.php` |
| Request | `Modules/Assign/Http/Requests/BomList/BomListStoreRequest.php` |
| Resource | `Modules/Assign/Transformers/BomListResource/BomListListResource.php`, `DetailBomListResource.php` |
| Routes | `Modules/Assign/Routes/api.php` |
| FE Pages | `pages/assign/bom-list/index.vue`, `add.vue`, `_id/edit.vue`, `_id/index.vue`, `_id/pricing.vue`, `pending-pricing/index.vue`, `pending-price-approval/index.vue` |
| FE Config | `pages/assign/settings/price-approval/index.vue` |
| FE Components | `pages/assign/bom-list/components/BomBuilderEditor.vue`, `BomBuilderTableCard.vue`, `BomBuilderInfoCard.vue`, `BomBuilderFooterBar.vue`, `BomPricingHistoryModal.vue`, `BomExportModal.vue` |
| Menu | `components/menu-sidebar.js` |
| Permission | `database/migrations/2026_03_29_110000_add_bom_list_permissions.php`, `2026_04_12_200003_add_bom_pricing_permissions.php` |
