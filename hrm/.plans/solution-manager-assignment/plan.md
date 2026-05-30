# Plan: Phân công quản lý giải pháp

@dnsnamdang | Khởi tạo: 2026-05-17

---

## Phase 1 — Backend: Database + Model + Service

### BE-1: Migration + Model
- [x] Tạo migration `create_solution_manager_logs_table`
- [x] Tạo Model `SolutionManagerLog` với relationships (solution, solutionModule, oldManager, newManager, oldManagerNewRole, creator)
- [x] Tạo Resource `SolutionManagerLogResource`

### BE-2: Service logic
- [x] Thêm method `assignManager(Request, Solution)` trong `SolutionService`
- [x] Thêm method `getAssignManagerLogs(Solution)` trong `SolutionService`

### BE-3: Request + Controller + Route
- [x] Tạo `AssignManagerRequest` (FormRequest) với validation rules
- [x] Thêm method `assignManager` trong `SolutionController`
- [x] Thêm method `assignManagerLogs` trong `SolutionController`
- [x] Đăng ký 2 routes trong `Modules/Assign/Routes/api.php`

---

## Phase 2 — Frontend: UI Components

### FE-1: Button Phân công + quyền hiển thị
- [x] Thêm button "Phân công" trong `HumanResourceTab.vue` (bên trái "Thêm nhân sự")
- [x] Thêm button "Xem lịch sử phân công"
- [x] Logic ẩn/hiện: ẩn khi solution status = 2 (Đóng)
- [x] Logic quyền: button Phân công chỉ hiện cho Trưởng phòng GP hoặc PM

### FE-2: Popup Phân công
- [x] Tạo component `AssignManagerModal.vue` trong `components/manager/`
- [x] Radio chọn loại: PM / Leader
- [x] Select hạng mục (hiện khi chọn Leader)
- [x] Hiển thị PM/Leader hiện tại (readonly)
- [x] Select vai trò mới cho người cũ (không bắt buộc)
- [x] Select module cho PM cũ (hiện khi: loại=PM + GP có modules + có chọn vai trò)
- [x] Select PM/Leader mới (employees cùng department, status=1)
- [x] Textarea ghi chú (validate min 50 ký tự)
- [x] Submit → gọi API → reload danh sách nhân sự + đóng modal
- [x] Hiển thị lỗi validation inline

### FE-3: Popup Lịch sử phân công
- [x] Tạo component `AssignManagerHistoryModal.vue` trong `components/manager/`
- [x] Gọi API lấy logs
- [x] Hiển thị bảng: Ngày | Loại | Hạng mục | Người cũ | Người mới | Vai trò mới | Ghi chú | Người thực hiện
- [x] Sort mới nhất lên trên

---

## Checkpoint

### Checkpoint — 2026-05-17
Vừa hoàn thành: Phase 1 + Phase 2 (BE + FE) + SRS + Testcase
Đang làm dở: Không
Bước tiếp theo: Deploy + test trên staging
Blocked:
