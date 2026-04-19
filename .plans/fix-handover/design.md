# Design: Bàn giao công việc (Handover)

## Mục đích
Quản lý quy trình bàn giao công việc khi nhân viên nghỉ việc, chuyển phòng ban, nghỉ thai sản, nghỉ dài hạn.

## Luồng trạng thái

```
Nháp (1) → [Gửi duyệt] → Chờ duyệt (2) → [Duyệt] → Đã duyệt (3) → [Tiếp nhận hết] → Hoàn tất (5)
                                ↓
                           [Từ chối] → Từ chối (4) → [Sửa + gửi lại] → Chờ duyệt (2)
```

| Status | Value | Màu | Ai thao tác | Điều kiện |
|--------|-------|-----|-------------|-----------|
| Nháp | 1 | #64748B (xám) | Người tạo | Tạo mới, sửa, xoá, gửi duyệt |
| Chờ duyệt | 2 | #D97706 (cam) | Trưởng phòng | Duyệt hoặc từ chối |
| Đã duyệt | 3 | #2563EB (xanh) | Người nhận | Accept/reject từng item |
| Từ chối | 4 | #B91C1C (đỏ) | Người tạo | Sửa lại + gửi duyệt lại |
| Hoàn tất | 5 | #16A34A (xanh lá) | Hệ thống | Tự động khi tất cả items xử lý xong |

## Cấu trúc dữ liệu

### Bảng handovers
- `code`: Mã phiếu (BG.YYYY.NNNN)
- `employee_id`: NV bàn giao
- `department_id`, `company_id`: Phòng ban, công ty
- `handover_date`: Ngày bàn giao
- `reason`: Lý do (1=Nghỉ việc, 2=Chuyển PB, 3=Thai sản, 4=Nghỉ dài hạn, 5=Khác)
- `note`: Ghi chú
- `status`: Trạng thái (1-5)
- `approved_by`, `approved_at`: Người duyệt + thời gian
- `reject_reason`: Lý do từ chối

### Bảng handover_items
- `handover_id`: FK phiếu bàn giao
- `itemable_type`: 'Task' hoặc 'Issue' (polymorphic)
- `itemable_id`: ID task/issue
- `receiver_id`: Người nhận bàn giao
- `handover_note`: Ghi chú cho item
- `receive_status`: 0=Chờ, 1=Đã nhận, 2=Từ chối
- `reject_reason`: Lý do từ chối item
- `received_at`: Thời gian xử lý

### Bảng handover_logs
- `handover_id`, `action`, `content`, `actor_id`, `meta`, `created_at`

## 6 trang FE

| Trang | URL | Layout | Mục đích |
|-------|-----|--------|----------|
| Danh sách | `/assign/handover` | default-sidebar | Tổng hợp tất cả phiếu, filter, search |
| Tạo/Sửa | `/assign/handover/add` | default-sidebar | Form tạo mới / sửa nháp / sửa bị từ chối |
| Chi tiết | `/assign/handover/{id}` | default-sidebar | Xem chi tiết + Duyệt/Từ chối (cho TP) |
| Tiếp nhận | `/assign/handover/{id}/receive` | default-sidebar | Receiver accept/reject từng item |
| Chờ duyệt | `/assign/handover/pending` | default-sidebar | DS phiếu chờ TP duyệt |
| Chờ tiếp nhận | `/assign/handover/receiving` | default-sidebar | DS items chờ receiver xác nhận |

## Components FE
- `HandoverForm.vue`: Form nhập ngày BG, lý do, ghi chú
- `HandoverInfoCard.vue`: Card hiển thị thông tin phiếu + banner từ chối
- `HandoverItemsTable.vue`: Bảng items theo tab Task/Issue, group theo dự án, bulk assign
- `HandoverTimeline.vue`: Lịch sử thao tác (log)

## API Endpoints

| Method | Endpoint | Mục đích | Permission |
|--------|----------|----------|------------|
| GET | `/assign/handovers` | Danh sách | Theo quyền xem |
| GET | `/assign/handovers/pending` | DS chờ duyệt | Duyệt bàn giao |
| GET | `/assign/handovers/receiving` | DS chờ tiếp nhận | — |
| GET | `/assign/handovers/available-items` | Tasks/Issues khả dụng | — |
| POST | `/assign/handovers` | Tạo phiếu | — |
| GET | `/assign/handovers/{id}` | Chi tiết | — |
| PUT | `/assign/handovers/{id}` | Sửa phiếu | Chỉ Nháp/Từ chối |
| DELETE | `/assign/handovers/{id}` | Xoá phiếu | Chỉ Nháp + người tạo |
| PUT | `/assign/handovers/{id}/submit` | Gửi duyệt | Chỉ người tạo |
| PUT | `/assign/handovers/{id}/approve` | Duyệt | Duyệt bàn giao |
| PUT | `/assign/handovers/{id}/reject` | Từ chối | Duyệt bàn giao |
| PUT | `/assign/handovers/items/{id}/accept` | Nhận item | Chỉ receiver |
| PUT | `/assign/handovers/items/{id}/reject` | Từ chối item | Chỉ receiver |

## Quyền
- `Xem danh sách bàn giao công việc theo tổng công ty`
- `Xem danh sách bàn giao công việc theo công ty`
- `Xem danh sách bàn giao công việc theo phòng ban`
- `Duyệt bàn giao công việc`

## Business Rules
1. Phiếu phải có ít nhất 1 item (task/issue)
2. Gửi duyệt: tất cả items phải có `receiver_id`
3. 1 task/issue chỉ nằm trong 1 phiếu active (không trùng)
4. TP duyệt có thể sửa: receiver, note, progress, deadline trước khi duyệt
5. Accept item → task/issue đổi assignee sang receiver
6. Reject item (sau khi TP đã duyệt) → assignee chuyển về TP đã duyệt phiếu (`handover.approved_by`); throw 423 nếu `approved_by` null (data integrity); notify cả creator + TP
7. Tất cả items xử lý xong → phiếu tự chuyển Hoàn tất
8. Phiếu bị từ chối → người tạo sửa + gửi lại
9. Notification: gửi duyệt → TP, duyệt → receiver, từ chối → người tạo, accept/reject item → người tạo, hoàn tất → người tạo + TP

## Chưa triển khai
- Xuất Excel (pending/receiving): hiện báo "đang phát triển"
