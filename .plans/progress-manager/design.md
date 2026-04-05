# Design: Progress Manager — Quản lý tiến độ giải pháp

## Mục đích
Thêm tab "Tiến độ" trong chi tiết giải pháp (Solution) và hạng mục (Solution Module), cho phép phân bổ trọng số % và theo dõi tiến độ thực tế.

## Scope

### Làm:
- Tab Tiến độ ở 2 cấp: Giải pháp + Hạng mục (vị trí: sau Meeting, trước Quản lý files)
- Cấp GP: 2 mode (có hạng mục → phân bổ theo module, không → phân bổ theo task)
- Cấp HM: chỉ mode task
- Bảng phân bổ trọng số với input % editable
- Hiển thị tiến độ thực tế (TT%) + trạng thái + progress bar
- Bộ lọc task (mode task): keyword, assignee, date range, status
- Auto-save: debounce 1s sau khi thay đổi weight
- Validate tổng trọng số = 100%
- Weight summary: "Đã phân bổ: X% - Chưa phân bổ: Y%" (căn phải)

### Quyền edit:
- Cấp GP: chỉ PM (`requestSolution.pm_id`)
- Cấp HM: chỉ Leader hạng mục (`solutionModule.leader_id`)

## Data Structure

### DB — Cột mới
- `solution_modules.weight` — unsignedTinyInteger, default 0
- `tasks.weight` — unsignedTinyInteger, default 0

### API Endpoints

**Cấp GP:**
- `GET /api/v1/assign/solutions/{solution}/manager/progress`
- `PUT /api/v1/assign/solutions/{solution}/manager/progress/weights`

**Cấp HM:**
- `GET /api/v1/assign/solution-modules/{module}/manager/progress`
- `PUT /api/v1/assign/solution-modules/{module}/manager/progress/weights`

**Response format:** `{ mode: 'module'|'task', items: [...], total_weight: number }`
**PUT body:** `{ mode: 'module'|'task', items: [{id, weight}] }`

## UI

### Weight summary (căn phải, cùng hàng tiêu đề)
- "Đã phân bổ: X%" (xanh lá nếu = 100, xanh dương nếu < 100)
- "Chưa phân bổ: Y%" (xanh lá nếu = 0, đỏ nếu > 0)

### Mode 1: Có hạng mục (chỉ cấp GP)
- Bảng: STT | Mã HM | Tên HM | Leader | Deadline | Version | Phân bổ (%) | Tiến độ TT (%) | Trạng thái

### Mode 2: Theo task
- Bộ lọc: Tìm kiếm | Người thực hiện | Ngày giao | Trạng thái
- Bảng: STT | Mã task | Tên CV | Người TH | Phân bổ (%) | Tiến độ TT (%) | Trạng thái

### Progress bar
- Màu: >= 80% xanh lá, >= 50% xanh dương, >= 20% vàng, < 20% đỏ

## Architecture — Component dùng chung

`ProgressTab.vue` dùng chung cho cả 2 cấp qua 3 props:
- `apiPrefix` — base URL cho API calls
- `canEdit` — boolean, quyết định input hay text readonly
- `humanResourceUrl` — URL lấy danh sách nhân viên cho filter

## Files

| File | Mô tả |
|------|-------|
| `hrm-api/database/migrations/2026_04_02_000001_add_weight_to_solution_modules_table.php` | Migration weight cho modules |
| `hrm-api/database/migrations/2026_04_02_000002_add_weight_to_tasks_table.php` | Migration weight cho tasks |
| `hrm-api/Modules/Assign/Routes/api.php` | 4 routes (2 GP + 2 HM) |
| `hrm-api/Modules/Assign/Http/Controllers/Api/V1/SolutionController.php` | getProgress, updateWeights |
| `hrm-api/Modules/Assign/Http/Controllers/Api/V1/SolutionModuleController.php` | getModuleProgress, updateModuleWeights |
| `hrm-api/Modules/Assign/Services/SolutionService.php` | getProgressData, getProgressByModules, getProgressByTasks, updateProgressWeights |
| `hrm-api/Modules/Assign/Services/SolutionModuleService.php` | getModuleProgressData, updateModuleProgressWeights |
| `hrm-api/Modules/Assign/Entities/Task/Task.php` | Thêm `weight` vào fillable |
| `hrm-client/pages/assign/solutions/components/manager/ProgressTab.vue` | Component dùng chung |
| `hrm-client/pages/assign/solutions/_id/manager.vue` | Tích hợp cấp GP |
| `hrm-client/pages/assign/solution-modules/_id/manager.vue` | Tích hợp cấp HM |
