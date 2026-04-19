---
name: api-documenter
description: Generate tài liệu API specification cho endpoints đã triển khai
---

# API Documenter — ERP TPE

## Mục đích
Tạo tài liệu API cho dev mobile hoặc bên thứ 3 tích hợp, dựa trên code BE hiện có.

## Khi nào dùng
- Cần tạo tài liệu cho dev mobile triển khai feature
- Cần document API cho team khác tích hợp
- Cần review lại API endpoints của 1 module/feature

## Quy trình tạo tài liệu

### Bước 1: Thu thập thông tin
1. Đọc route file: `Modules/[Module]/Routes/api.php`
2. Đọc controller: xác định method, request validation, response format
3. Đọc service: business logic, validation rules
4. Đọc transformer/resource: response data structure
5. Đọc migration: database schema

### Bước 2: Viết tài liệu

**Template cho mỗi endpoint:**
```markdown
### [Tên chức năng]

[Mô tả ngắn]

\`\`\`
[METHOD] /api/v1/[endpoint]
\`\`\`

**Request body / Query params:**
\`\`\`json
{
  "field": "value (type, bắt buộc/optional) — mô tả"
}
\`\`\`

**Response (200):**
\`\`\`json
{
  "message": "success",
  "status": 200,
  "data": { ... }
}
\`\`\`

**Quy tắc validate:**
- [liệt kê rules]
```

### Bước 3: Bổ sung context

- Luồng hoạt động tổng quan (flow diagram dạng text)
- Giải thích các trường enum (status, type, cycle_type...)
- Gợi ý UI nếu có
- Checklist triển khai cho đội nhận tài liệu

## Format tài liệu

```markdown
# Tài liệu [Feature] — [Đối tượng nhận]

## 1. Tổng quan
- Mục đích
- Luồng hoạt động

## 2. API Endpoints
### 2.1. [Endpoint 1]
### 2.2. [Endpoint 2]
...

## 3. Data Structure
- Bảng DB liên quan
- Enum values
- Relationship

## 4. Business Rules
- Validate
- Permission
- Cron/Schedule (nếu có)

## 5. Gợi ý UI (nếu có)

## 6. Checklist triển khai
```

## Output
- File markdown trong `docs/[feature-name]-[audience].md`
- VD: `docs/notify-task-report-mobile.md`

## Quy tắc
- Đọc code thực tế, KHÔNG đoán response format
- Ghi rõ type + required/optional cho mỗi field
- Cung cấp request/response mẫu với data thực tế
- Liệt kê tất cả enum values với mô tả
- Auth header: `Authorization: Bearer {JWT token}`
- Base URL: `/api/v1`
