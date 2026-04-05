# Kế hoạch phát triển tính năng Bàn giao công việc (Handover) - Version 1

## Tổng quan

Tính năng cho phép nhân viên tạo phiếu bàn giao công việc (task/issue) cho người khác khi nghỉ việc, chuyển phòng ban, nghỉ thai sản, nghỉ dài hạn, hoặc lý do khác.

## Luồng nghiệp vụ (3 bước)

1. **Nhân viên tạo phiếu** → chọn task/issue cần bàn giao → chỉ định người nhận cho từng item → gửi duyệt cho trưởng phòng
2. **Trưởng phòng duyệt** → xem xét, có thể sửa người nhận/ghi chú → phê duyệt hoặc từ chối (kèm lý do)
3. **Người nhận xác nhận** → từng người nhận chấp nhận hoặc từ chối từng item → chấp nhận sẽ đổi assignee → hoàn thành khi tất cả item đã xử lý

## Trạng thái phiếu bàn giao

| Status | Giá trị | Màu | Mô tả |
|--------|---------|-----|-------|
| Nháp (Draft) | 1 | gray | Mới tạo, chưa gửi duyệt |
| Chờ duyệt (Pending) | 2 | warning/orange | Đã gửi, chờ trưởng phòng duyệt |
| Đã duyệt (Approved) | 3 | primary/blue | Trưởng phòng đã duyệt, chờ người nhận xác nhận |
| Từ chối (Rejected) | 4 | danger/red | Trưởng phòng từ chối |
| Hoàn thành (Completed) | 5 | success/green | Tất cả item đã được xử lý |

## Trạng thái item bàn giao

| Status | Giá trị | Mô tả |
|--------|---------|-------|
| Chờ tiếp nhận (Pending) | 0 | Chưa xử lý |
| Đã tiếp nhận (Accepted) | 1 | Người nhận chấp nhận → đổi assignee |
| Từ chối (Rejected) | 2 | Người nhận từ chối → giữ assignee cũ |

## Lý do bàn giao

| Reason | Giá trị | Label |
|--------|---------|-------|
| Nghỉ việc | 1 | Nghỉ việc |
| Chuyển phòng ban | 2 | Chuyển phòng ban |
| Nghỉ thai sản | 3 | Nghỉ thai sản |
| Nghỉ dài hạn | 4 | Nghỉ dài hạn |
| Khác | 5 | Khác |

---

## Cấu trúc Database

### Bảng `handovers`
- `id` - Primary key
- `code` - Mã tự sinh dạng BG.YYYY.STT (ví dụ: BG.2026.001)
- `employee_id` - Nhân viên bàn giao
- `department_id` - Phòng ban
- `company_id` - Công ty
- `handover_date` - Ngày bàn giao
- `reason` - Lý do (1-5)
- `note` - Ghi chú
- `status` - Trạng thái (1-5)
- `approved_by` - Người duyệt
- `approved_at` - Thời gian duyệt
- `reject_reason` - Lý do từ chối
- `created_by`, `updated_by`, `timestamps`

### Bảng `handover_items`
- `id` - Primary key
- `handover_id` - FK tới handovers
- `itemable_type` - Polymorphic (Task/Issue)
- `itemable_id` - ID của task/issue
- `receiver_id` - Người nhận bàn giao
- `handover_note` - Ghi chú cho item
- `receive_status` - Trạng thái tiếp nhận (0-2)
- `reject_reason` - Lý do từ chối
- `received_at` - Thời gian xử lý
- `timestamps`

### Bảng `handover_logs`
- `id` - Primary key
- `handover_id` - FK tới handovers
- `action` - Hành động (created, submitted, approved, rejected, resubmitted, item_accepted, item_rejected, completed)
- `content` - Nội dung log
- `actor_id` - Người thực hiện
- `meta` - JSON data bổ sung
- `created_at`

---

## API Endpoints

### Phiếu bàn giao (HandoverController)
| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET | `/v1/assign/handovers` | Danh sách phiếu bàn giao |
| POST | `/v1/assign/handovers` | Tạo phiếu mới |
| GET | `/v1/assign/handovers/{id}` | Chi tiết phiếu |
| PUT | `/v1/assign/handovers/{id}` | Cập nhật phiếu (draft/rejected) |
| DELETE | `/v1/assign/handovers/{id}` | Xóa phiếu (draft only) |
| PUT | `/v1/assign/handovers/{id}/submit` | Gửi duyệt |
| PUT | `/v1/assign/handovers/{id}/approve` | Phê duyệt |
| PUT | `/v1/assign/handovers/{id}/reject` | Từ chối |

### Item bàn giao (HandoverItemController)
| Method | Endpoint | Mô tả |
|--------|----------|-------|
| PUT | `/v1/assign/handovers/items/{itemId}/accept` | Tiếp nhận item |
| PUT | `/v1/assign/handovers/items/{itemId}/reject` | Từ chối item |

---

## Quyền hạn (Permissions)

| ID | Tên | Mô tả |
|----|-----|-------|
| 1026 | handover.view.corporation | Xem danh sách bàn giao theo tổng công ty |
| 1027 | handover.view.company | Xem danh sách bàn giao theo công ty |
| 1028 | handover.view.department | Xem danh sách bàn giao theo phòng ban |
| 1029 | handover.approve | Duyệt bàn giao công việc |

---

## Cấu trúc Frontend

### Pages (hrm-client/pages/assign/handover/)
| File | Mô tả |
|------|-------|
| `index.vue` | Danh sách phiếu bàn giao (filter: status, reason, department, date range) |
| `add.vue` | Tạo mới / Sửa phiếu bàn giao |
| `pending.vue` | Danh sách chờ duyệt (cho trưởng phòng) |
| `receiving.vue` | Danh sách chờ tiếp nhận (cho người nhận) |
| `_id/index.vue` | Chi tiết & duyệt phiếu (cho trưởng phòng) |
| `_id/receive.vue` | Xác nhận tiếp nhận item (cho người nhận) |

### Components (hrm-client/pages/assign/handover/components/)
| File | Mô tả |
|------|-------|
| `HandoverForm.vue` | Form thông tin cơ bản (ngày, lý do, ghi chú) |
| `HandoverItemsTable.vue` | Bảng task/issue - 2 tab (Tasks/Issues), group by project, bulk assign |
| `HandoverInfoCard.vue` | Card hiển thị thông tin phiếu (readonly) |
| `HandoverTimeline.vue` | Timeline lịch sử hành động |

### Menu (menu-sidebar.js)
- **Bàn giao công việc** (group):
  - "Danh sách bàn giao" → `/assign/handover`
  - "Tạo phiếu bàn giao" → `/assign/handover/add`
- **Phê duyệt** (group):
  - "Duyệt bàn giao công việc" → `/assign/handover/pending`
- **Quản lý công việc** (group):
  - "Chờ tiếp nhận BG" → `/assign/handover/receiving`

---

## Backend Files

### Models (Modules/Assign/Entities/)
- `Handover.php` - Model chính, constants trạng thái/lý do, generateCode(), relationships
- `HandoverItem.php` - Model item, polymorphic (Task/Issue), relationships
- `HandoverLog.php` - Model log, action constants, ACTION_COLORS

### Controllers (Modules/Assign/Http/Controllers/Api/V1/)
- `HandoverController.php` - CRUD + submit/approve/reject
- `HandoverItemController.php` - receiving/accept/reject item

### Services (Modules/Assign/Services/)
- `HandoverService.php` - Business logic chính (index, pending, receiving, store, update, submit, approve, reject, acceptItem, rejectItem)

### Requests (Modules/Assign/Http/Requests/Handover/)
- `HandoverRequest.php` - Validate tạo/sửa phiếu
- `HandoverRejectRequest.php` - Validate từ chối phiếu (reject_reason min 10)
- `HandoverItemRejectRequest.php` - Validate từ chối item (reject_reason min 10)

### Transformers (Modules/Assign/Transformers/HandoverResource/)
- `HandoverResource.php` - List view (kèm counts: total/accepted/rejected/pending items)
- `DetailHandoverResource.php` - Detail view (kèm items + logs)
- `HandoverItemResource.php` - Item detail (nested task/issue info)

### Routes
- `Modules/Assign/Routes/api.php` (lines 606-622)

### Migration
- `Modules/Assign/Database/Migrations/2026_03_26_000001_create_handovers_table.php`

### Permissions
- `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php` (lines 957-961)

---

## Tài liệu thiết kế

| File | Mô tả |
|------|-------|
| `docs/superpowers/specs/2026-03-26-handover-design.md` | Spec thiết kế backend |
| `docs/superpowers/specs/2026-03-26-handover-frontend-design.md` | Spec thiết kế frontend |
| `docs/superpowers/plans/2026-03-26-handover-implementation.md` | Plan triển khai backend |
| `docs/superpowers/plans/2026-03-26-handover-frontend.md` | Plan triển khai frontend |

## HTML Mockups
| File | Mô tả |
|------|-------|
| `docs/handover.html` | Mockup danh sách & tạo phiếu |
| `docs/handover-approve.html` | Mockup trang duyệt phiếu |
| `docs/handover-receive.html` | Mockup trang tiếp nhận |

---

## Trạng thái hiện tại

**Giai đoạn: TEST**

- Backend: Đã hoàn thành (migration, models, controllers, services, routes, permissions, transformers)
- Frontend: Đã hoàn thành (pages, components, menu integration)
- Đang ở giai đoạn kiểm thử (test) chức năng

---

## Ghi chú kỹ thuật

- Mã phiếu tự sinh: `BG.YYYY.STT` (ví dụ: BG.2026.001)
- Polymorphic relationship cho items (Task/Issue)
- Permission-based filtering: xem theo tổng công ty/công ty/phòng ban
- Timeline log cho mọi hành động
- Auto-complete khi tất cả items đã xử lý (accepted/rejected)
- Khi accept item → đổi assignee của task/issue sang người nhận
- Khi reject item → giữ nguyên assignee cũ
