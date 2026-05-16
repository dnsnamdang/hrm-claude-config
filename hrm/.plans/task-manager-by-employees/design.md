# Design: Báo cáo phân bổ nguồn lực dạng Gantt theo nhân viên (QLDA_BC_V2_11)

## Mục đích
Màn báo cáo hiển thị phân bổ nguồn lực (task) của nhân viên theo dạng Gantt trên trục thời gian. Dữ liệu group theo Phòng ban → Nhân viên, mỗi nhân viên hiển thị số task, giờ làm, % sử dụng công suất và lịch Gantt.

## Scope — Giai đoạn 1

### Có
- Hiển thị bảng + Gantt đầy đủ
- Filter, pagination, modal chi tiết
- Tính % công suất dựa trên giờ công ca làm việc thực tế (SUM labour_hour từ phân ca)

### Không (giai đoạn sau)
- Export Excel (ExcelJS client-side)
- Filter vai trò trong dự án

## Bộ lọc
- Công ty, Phòng ban, Bộ phận (V2BaseCompanyDepartmentFilter)
- Nhân viên, Dự án
- Chế độ thời gian: Hôm nay / Tuần hiện tại / Tháng hiện tại / Tuỳ chọn
- Từ ngày / Đến ngày (auto-set theo chế độ, chỉ edit khi "Tuỳ chọn")
- Khoảng công suất: < 60% / 60-100% / > 100%
- Checkbox: Chỉ NV có task

## Backend

### API Endpoint
```
GET /api/v1/assign/report/task-manager-by-employees
```

### Query Parameters
| Param | Type | Required | Mô tả |
|-------|------|----------|--------|
| `company_id` | int | no | Lọc theo công ty |
| `department_id` | int | no | Lọc theo phòng ban |
| `part_id` | int | no | Lọc theo bộ phận |
| `employee_id` | int | no | Lọc theo nhân viên |
| `project_id` | int | no | Lọc theo dự án |
| `time_mode` | string | yes | `today`, `week`, `month`, `custom` |
| `from_date` | date | yes | Ngày bắt đầu (YYYY-MM-DD) |
| `to_date` | date | yes | Ngày kết thúc (YYYY-MM-DD) |
| `utilization_range` | string | no | `lt60`, `60_100`, `gt100` |
| `has_task_only` | bool | no | Chỉ nhân viên có task |
| `page` | int | no | Trang hiện tại (default 1) |
| `per_page` | int | no | Số department/trang (default 10) |

### Response Structure
```json
{
  "data": [
    {
      "department_id": 1,
      "department_name": "Phòng Dự án",
      "company_name": "Công ty ABC",
      "summary": {
        "employee_count": 5,
        "total_tasks": 23,
        "capacity_hours": 200.0,
        "task_hours": 168.5,
        "utilization_pct": 84.3
      },
      "employees": [
        {
          "employee_id": 10,
          "employee_name": "Nguyễn Văn An",
          "employee_code": "NV001",
          "position": "PM dự án",
          "summary": {
            "total_tasks": 5,
            "capacity_hours": 40.0,
            "task_hours": 32.5,
            "utilization_pct": 81.3,
            "free_hours": 7.5,
            "overload_hours": 0,
            "status": { "label": "Phân bổ hợp lý", "color": "#16a34a" }
          },
          "tasks": [
            {
              "id": 101,
              "code": "TASK-001",
              "title": "Phân tích yêu cầu module HR",
              "project_code": "PRJ_ERP_01",
              "project_name": "Triển khai ERP HRM",
              "start_date": "2026-04-06",
              "due_date": "2026-04-08",
              "estimated_hours": 12.0,
              "status": { "value": 4, "label": "Đang thực hiện", "color": "blue" },
              "progress_pct": 60
            }
          ]
        }
      ]
    }
  ],
  "meta": { "current_page": 1, "per_page": 10, "total": 3, "last_page": 1 },
  "summary": { "total_departments": 3, "total_employees": 15, "total_tasks": 58 },
  "gantt": {
    "from_date": "2026-04-06",
    "to_date": "2026-04-12",
    "days": [{ "date": "2026-04-06", "day": 6, "dow": "T2", "is_today": true }]
  }
}
```

### Backend Files
```
Modules/Assign/
├─ Http/Controllers/Api/V1/TaskManagerByEmployeesReportController.php
├─ Services/Report/TaskManagerByEmployeesReportService.php
├─ Transformers/TaskManagerByEmployeesResource/TaskManagerByEmployeesReportResource.php
└─ Routes/api.php  (thêm route)
```

### Logic xử lý Service
1. Query employees theo filter (company, department, part, employee)
2. Query tasks overlap khoảng thời gian: `start_date <= to_date` AND `due_date >= from_date`
3. Filter project_id nếu có
4. Tính `capacity_hours` = SUM(labour_hour) từ phân ca của nhân viên trong khoảng thời gian (bảng shift_detail_employee_dates + working_shifts)
5. Tính `task_hours` = SUM(estimated_hours)
6. Tính `utilization_pct` = task_hours / capacity_hours × 100
7. Status: < 60% → amber "Cần phân thêm task" | 60-100% → green "Phân bổ hợp lý" | > 100% → red "Vượt tải"
8. Lọc utilization_range, has_task_only
9. Group theo department, paginate theo số department
10. Build gantt.days array

### Trạng thái task mapping
| Value | Label | Color |
|-------|-------|-------|
| 1 | Nháp | gray |
| 2 | Chờ phê duyệt | orange |
| 3 | Chờ bắt đầu | blue |
| 4 | Đang thực hiện | blue |
| 5 | Tạm dừng | yellow |
| 6 | Chờ duyệt KQ | purple |
| 7 | Từ chối KQ | red |
| 8 | Hoàn thành | green |
| 9 | Huỷ | gray |
| 10 | Từ chối triển khai | red |

## Frontend

### Cấu trúc files
```
pages/assign/report/task-manager-by-employees/
├─ index.vue                    (trang chính)
├─ components/
│  ├─ GanttChart.vue            (component Gantt CSS Grid)
│  └─ TaskDetailModal.vue       (modal chi tiết task)
```

### Layout trang chính
```
<div class="v2-styles">
  ├─ Header (tiêu đề + range label)
  ├─ V2BaseFilterPanel
  │  ├─ Row 1: V2BaseCompanyDepartmentFilter, V2BaseSelect (Dự án), V2BaseSelect (Chế độ thời gian)
  │  ├─ Row 2: V2BaseDatePicker (Từ/Đến ngày), V2BaseSelect (Khoảng công suất), Checkbox (Chỉ NV có task)
  │  └─ Buttons: Tìm kiếm, Làm mới
  ├─ Card báo cáo
  │  ├─ Header: tiêu đề + nút Ẩn/Hiện Gantt
  │  ├─ Table (overflow-x: auto, sticky columns trái)
  │  │  ├─ thead: STT | Nhân viên | Task | Giờ làm | Giờ task | % sử dụng | Trạng thái | Lịch Gantt
  │  │  └─ tbody: Row phòng ban (summary) + Row nhân viên (data + GanttChart inline)
  │  └─ V2BasePagination
  └─ TaskDetailModal
```

### GanttChart.vue
- CSS Grid: `repeat(days.length, minmax(32px, 1fr))`
- Lane algorithm: xếp task không chồng nhau
- Màu: xanh lá (bình thường), cam (sắp hạn), đỏ (quá hạn)
- Click thanh → emit task-click → mở modal

### TaskDetailModal.vue
- Bảng: # | Mã task | Tên task | Dự án | Ngày bắt đầu | Hạn | Trạng thái | Tiến độ | Giờ ước tính
- Footer: tổng task + tổng giờ
- V2BaseBadge cho trạng thái

### Sticky Columns
| Cột | Sticky left | Width |
|-----|-------------|-------|
| STT | 0 | 50px |
| Nhân viên | 50px | 190px |
| Task | 240px | 70px |
| Giờ làm | 310px | 70px |
| Giờ task | 380px | 70px |
| % sử dụng | 450px | 70px |
| Trạng thái | 520px | 110px |

Cột Lịch Gantt: không sticky, scroll tự do.

## Giai đoạn sau (không thuộc scope hiện tại)
1. Export Excel (ExcelJS client-side)
2. Filter vai trò trong dự án
