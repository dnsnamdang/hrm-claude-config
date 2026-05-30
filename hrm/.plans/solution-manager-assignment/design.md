# Phân công quản lý giải pháp

@dnsnamdang | Khởi tạo: 2026-05-17

## Mục tiêu

Cho phép Trưởng phòng GP / PM phân công lại PM hoặc Leader hạng mục trong giải pháp khi có thay đổi nhân sự, đồng thời lưu lịch sử phân công đầy đủ.

## Scope

- 2 chức năng trong 1 popup: Phân công PM + Phân công Leader
- Lịch sử phân công (popup riêng)
- Áp dụng tất cả trạng thái giải pháp trừ **Đóng** (status=2)

## Quyền thực hiện

| Hành động | Ai được làm |
|---|---|
| Phân công PM | Trưởng phòng GP (created_by của solution) |
| Phân công Leader | Trưởng phòng GP HOẶC PM hiện tại |

## Vị trí UI

- Trang: `/assign/solutions/{id}/manager` → Tab "Nhân sự"
- Button "Phân công" đặt **bên trái** button "Thêm nhân sự"
- Button "Xem lịch sử phân công" đặt gần button Phân công

## Database

Bảng mới: `solution_manager_logs`

| Field | Type | Constraint |
|---|---|---|
| id | bigIncrements | PK |
| solution_id | unsignedBigInteger | FK solutions.id, indexed |
| solution_module_id | unsignedBigInteger | nullable (null = phân công PM) |
| type | enum('pm','leader') | NOT NULL |
| old_manager_id | unsignedBigInteger | FK employees.id |
| new_manager_id | unsignedBigInteger | FK employees.id |
| old_manager_new_role_id | unsignedBigInteger | nullable, FK project_roles.id |
| old_manager_module_id | unsignedBigInteger | nullable — module mà PM cũ được thêm vào (khi GP có modules) |
| note | text | NOT NULL, min 50 ký tự |
| company_id | unsignedBigInteger | nullable |
| department_id | unsignedBigInteger | nullable |
| part_id | unsignedBigInteger | nullable |
| created_by | unsignedBigInteger | nullable |
| updated_by | unsignedBigInteger | nullable |
| timestamps | | |

## Business Logic

### Phân công PM

1. Cập nhật `solutions.pm_id` = PM mới
2. Nếu chọn vai trò mới cho PM cũ:
   - GP **không** có module → thêm vào `solution_members` (member_id=PM cũ, project_role_id=vai trò mới, start_date=today)
   - GP **có** module → user chọn module → thêm vào `solution_module_members` (solution_module_id=module chọn, member_id=PM cũ, project_role_id=vai trò mới, start_date=today)
3. Nếu **không** chọn vai trò mới → PM cũ rời khỏi dự án (không thêm vào đâu)
4. Ghi log vào `solution_manager_logs`

### Phân công Leader

1. Cập nhật `solution_modules.leader_id` = Leader mới
2. Nếu chọn vai trò mới cho Leader cũ → thêm vào `solution_module_members` của chính hạng mục đó (start_date=today)
3. Leader mới nếu đang là member của hạng mục → **giữ nguyên** (không xóa record member)
4. Ghi log vào `solution_manager_logs`

### Danh sách chọn PM/Leader mới

- Nhân viên cùng `department_id` với giải pháp
- `employees.status = 1` (đang làm việc)
- Loại trừ PM/Leader hiện tại khỏi danh sách

## Popup Phân công (UI)

| Field | Component | Điều kiện | Validate |
|---|---|---|---|
| Loại phân công | Radio/Select: PM / Leader | Luôn hiện | Required |
| Hạng mục | V2BaseSelect modules | Chỉ hiện khi loại = Leader | Required |
| PM/Leader hiện tại | Text hiển thị (readonly) | Luôn hiện | — |
| Vai trò mới cho người cũ | V2BaseSelect project_roles | Luôn hiện | Không bắt buộc |
| Module cho PM cũ | V2BaseSelect modules | Chỉ hiện khi: loại=PM + GP có modules + có chọn vai trò mới | Required nếu hiện |
| PM/Leader mới | V2BaseSelect employees | Luôn hiện | Required |
| Ghi chú | Textarea | Luôn hiện | Required, min 50 ký tự |

## Popup Lịch sử phân công

| Cột | Mô tả |
|---|---|
| Ngày | created_at format DD/MM/YYYY |
| Loại | PM / Leader |
| Hạng mục | Tên module (trống nếu PM) |
| Người cũ | Tên employee cũ |
| Người mới | Tên employee mới |
| Vai trò mới (người cũ) | Tên role hoặc "Rời dự án" |
| Ghi chú | Nội dung note |
| Người thực hiện | Tên created_by |

Sắp xếp: mới nhất lên trên (created_at DESC)

## API Endpoints

| Method | URL | Mục đích |
|---|---|---|
| POST | `/assign/solutions/{solution}/manager/assign-manager` | Thực hiện phân công |
| GET | `/assign/solutions/{solution}/manager/assign-manager-logs` | Lấy lịch sử phân công |

## Edge Cases

- PM mới đang là Leader 1 hạng mục → vẫn cho phép (1 người có thể vừa PM vừa leader)
- Leader mới đang là member hạng mục → giữ nguyên record member, chỉ update leader_id
- Phân công PM khi GP có module nhưng không chọn vai trò mới → PM cũ rời dự án, không thêm vào đâu
- GP trạng thái Đóng → ẩn button Phân công hoàn toàn
