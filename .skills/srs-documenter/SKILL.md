# SRS Documenter — ERP TPE

## Mục đích
Generate tài liệu SRS (Software Requirements Specification) cho feature đã triển khai hoặc sắp triển khai, dựa trên code thực tế + design document + business rules.

## Khi nào dùng
- Feature đã code xong, cần tài liệu SRS để bàn giao / lưu trữ
- Cần SRS trước khi code để align với stakeholder
- BA / PM yêu cầu tài liệu đặc tả cho feature

## Input cần thiết

### Nếu feature đã code:
1. Tên feature + module
2. `.plans/[feature]/design.md` (nếu có)
3. `.plans/[feature]/plan.md` (danh sách task)
4. Code BE: Routes, Controller, Service, Entity, Migration
5. Code FE: Pages, Components chính

### Nếu feature chưa code:
1. Mô tả yêu cầu từ user / PM / BA
2. Wireframe / mockup (nếu có)
3. Business rules đã thống nhất

## Quy trình generate SRS

### Bước 1: Thu thập thông tin từ code

**BE — đọc theo thứ tự:**
```
1. Migration        → Database schema, data types, constraints
2. Entity/Model     → Relationships, constants (STATUS, TYPE), accessors
3. Routes           → API endpoints, HTTP methods
4. Request          → Validation rules (required, type, min/max...)
5. Controller       → Request flow, response format
6. Service          → Business logic, conditions, calculations
7. Transformer      → Response data structure
8. Console Command  → Scheduled jobs, cron logic
```

**FE — đọc theo thứ tự:**
```
1. Page component   → UI layout, user interactions
2. API calls        → Endpoints consumed, payload format
3. Computed/methods → Client-side validation, data transformation
4. Menu sidebar     → Navigation entry point
```

### Bước 2: Phân tích & tổng hợp

- Xác định **actors** (ai dùng feature: nhân viên, trưởng phòng, admin...)
- Liệt kê **use cases** từ API endpoints + UI flows
- Trích xuất **business rules** từ service layer (if/else, validate, calculate)
- Xác định **data model** từ migration + entity relationships
- Phát hiện **constraints** từ request validation + DB constraints
- Xác định **permissions** từ isShow trong menu + middleware

### Bước 3: Viết SRS theo template

---

## Template SRS

```markdown
# SRS: [Tên Feature]

| Thông tin | Chi tiết |
|-----------|----------|
| Module | [Assign / Human / Timesheet / ...] |
| Phiên bản | 1.0 |
| Ngày tạo | [YYYY-MM-DD] |
| Người tạo | [tên] |
| Trạng thái | Draft / Review / Approved |

---

## 1. Giới thiệu

### 1.1. Mục đích
[Feature này giải quyết vấn đề gì? Tại sao cần?]

### 1.2. Phạm vi
**Trong scope:**
- [Chức năng 1]
- [Chức năng 2]

**Ngoài scope:**
- [Không làm gì]

### 1.3. Thuật ngữ

| Thuật ngữ | Giải thích |
|-----------|-----------|
| [Term] | [Definition] |

---

## 2. Actors & Permissions

| Actor | Mô tả | Permissions |
|-------|-------|-------------|
| [Nhân viên] | [Ai?] | [Quyền gì?] |
| [Trưởng phòng] | [Ai?] | [Quyền gì?] |

---

## 3. Use Cases

### UC-01: [Tên use case]
| | |
|---|---|
| **Actor** | [Ai thực hiện] |
| **Precondition** | [Điều kiện trước] |
| **Main Flow** | |
| 1 | [Bước 1] |
| 2 | [Bước 2] |
| 3 | [Bước 3] |
| **Postcondition** | [Kết quả sau khi thực hiện] |
| **Alternative Flow** | [Nhánh phụ nếu có] |
| **Exception** | [Lỗi có thể xảy ra] |

### UC-02: [Tên use case]
...

---

## 4. Business Rules

| ID | Rule | Mô tả | Áp dụng tại |
|----|------|-------|-------------|
| BR-01 | [Tên rule] | [Chi tiết] | [UC nào / API nào] |
| BR-02 | [Tên rule] | [Chi tiết] | [UC nào / API nào] |

---

## 5. Data Model

### 5.1. Entity Relationship Diagram (text)

\`\`\`
[Entity A] 1──N [Entity B]
[Entity B] N──1 [Entity C]
\`\`\`

### 5.2. Bảng dữ liệu

#### Bảng: [table_name]

| Cột | Type | Nullable | Default | Mô tả |
|-----|------|----------|---------|-------|
| id | bigint PK | No | auto | |
| [field] | [type] | [Yes/No] | [default] | [mô tả] |

#### Bảng: [table_name_2]
...

### 5.3. Enum Values

| Entity | Constant | Value | Meaning |
|--------|----------|-------|---------|
| [Task] | [STATUS_DRAFT] | [1] | [Nháp] |

---

## 6. API Specification

### 6.1. [Tên endpoint]

\`\`\`
[METHOD] /api/v1/[path]
Auth: Bearer Token (JWT)
\`\`\`

**Request:**
| Field | Type | Required | Validate | Mô tả |
|-------|------|----------|----------|-------|
| [field] | [string] | [Yes] | [max:255] | [mô tả] |

**Response (200):**
\`\`\`json
{
  "message": "success",
  "status": 200,
  "data": {}
}
\`\`\`

**Error cases:**
| HTTP Code | Condition | Message |
|-----------|-----------|---------|
| 400 | [điều kiện] | [message] |
| 403 | [điều kiện] | [message] |

---

## 7. UI Specification

### 7.1. Màn hình [Tên]
- **Route**: `/assign/[path]`
- **Layout**: [mô tả layout]
- **Components chính**: [V2BaseButton, V2BaseFilterPanel...]

**Wireframe (text):**
\`\`\`
┌─────────────────────────────────┐
│  Header: [Breadcrumb] [Actions] │
├─────────────────────────────────┤
│  Filter: [...]                  │
├─────────────────────────────────┤
│  Table / Content                │
├─────────────────────────────────┤
│  Footer: [Pagination / Summary] │
└─────────────────────────────────┘
\`\`\`

**User interactions:**
| Action | Behavior | API call |
|--------|----------|----------|
| Click [nút] | [gì xảy ra] | [endpoint] |

---

## 8. Scheduled Jobs / Background

| Command | Schedule | Logic |
|---------|----------|-------|
| [artisan command] | [everyXMinutes] | [mô tả ngắn] |

---

## 9. Non-functional Requirements

- **Performance**: [yêu cầu hiệu năng nếu có]
- **Security**: [JWT auth, permission-based access]
- **Compatibility**: [PHP 7.4, Laravel 8, Nuxt 2, Vue 2]
- **Browser**: [Chrome, Firefox, Safari, Edge]

---

## 10. Phụ lục

### 10.1. File references

| Layer | File path |
|-------|-----------|
| Migration | `database/migrations/...` |
| Entity | `Modules/[Module]/Entities/...` |
| Controller | `Modules/[Module]/Http/Controllers/...` |
| Service | `Modules/[Module]/Services/...` |
| Routes | `Modules/[Module]/Routes/api.php` |
| FE Page | `pages/[module]/[page].vue` |
```

---

## Quy tắc viết SRS

### Nguyên tắc chung
- Viết bằng **tiếng Việt**, thuật ngữ kỹ thuật giữ tiếng Anh
- Mỗi use case phải có **precondition + postcondition**
- Business rules phải **truy vết được** tới code (ghi rõ file + dòng nếu cần)
- Data model lấy từ **migration thực tế**, không đoán
- API spec lấy từ **controller + request validation thực tế**
- Validation rules phải khớp **100%** với code trong Request class

### Nguồn dữ liệu ưu tiên
1. **Code** (migration, entity, service) — nguồn chính xác nhất
2. **design.md** trong `.plans/` — context về quyết định thiết kế
3. **plan.md** trong `.plans/` — scope đã thống nhất
4. **User mô tả** — bổ sung business context mà code không thể hiện

### Không được
- Không đoán response format — đọc transformer/resource
- Không đoán validation rules — đọc Request class
- Không đoán database schema — đọc migration
- Không thêm requirement mà code không có (trừ khi SRS cho feature chưa code)
- Không bỏ sót enum values — đọc constants trong Entity

## Output
- File markdown: `docs/srs/[feature-name].md`
- Nếu feature lớn, tách thành: `docs/srs/[feature-name]/` với nhiều file con
