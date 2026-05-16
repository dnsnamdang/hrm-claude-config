# Yêu cầu điều chỉnh giải pháp — Design Summary

## Mục tiêu
Cho phép KD (người tạo dự án TKT) gửi yêu cầu điều chỉnh giải pháp khi GP đã được duyệt, để TP/PM xem xét và tạo version mới nếu tiếp nhận.

## Scope
- Entity mới: `solution_adjustment_requests` với code `YCDCGP.NNNNN`
- 3 status: Đã gửi (1) → Tiếp nhận (2) / Từ chối (3)
- 2 màn hình UI:
  - **Màn KD**: Dự án TKT → Tab "Giải pháp" → Tab con "YCĐC GP" — tạo + xem
  - **Màn TP/PM**: Quản lý GP (`/assign/solutions/:id/manager`) → Tab "YC Điều chỉnh" — xem + duyệt
- Notification cho TP + PM khi tạo phiếu, click → đúng màn hình + tab
- Không xóa, không nháp, không sửa phiếu đã gửi

## Quyết định lớn
- **Entity riêng** (không mở rộng `request_solutions`) — flow đơn giản, tách biệt rõ ràng
- Khi tiếp nhận chỉ đánh dấu, TP/PM tự tạo version mới thủ công
- Phiếu bị từ chối → tạo phiếu mới, không sửa phiếu cũ
- Quyền tạo: chỉ `main_sale_employee_id` (KD phụ trách dự án)
- Quyền xử lý: PM (`solution.pm_id`) hoặc TP (qua `departmentsManager()`)
- GP phải ở status ≥ Đã duyệt GP: {11, 13, 15, 17}
- Lưu `solution_version_id` snapshot tại thời điểm tạo phiếu
- BaseConfirmModal emit `@event` (không phải `@confirm`)
- Cột Hành động chỉ hiện trên màn TP/PM, buttons luôn hiển thị (không hover)
- Popup chi tiết dạng table bordered text gọn (không dùng input disabled)

## Data model
- Bảng: `solution_adjustment_requests` (16 cột)
- FK: prospective_project_id, solution_id, solution_version_id, processed_by
- File đính kèm: bảng `files` chung (`table='solution_adjustment_requests'`)

## API
- Base: `/api/v1/assign/prospective-projects/{id}/solution-adjustment-requests`
- 5 endpoints: GET / | POST / | GET /{id} | PUT /{id}/accept | PUT /{id}/reject

## Files
- BE: 8 files mới (Migration, Entity, Controller, Service, 2 Resource, 2 Request) + sửa api.php
- FE: 1 file mới (SolutionAdjustmentTab.vue) + sửa 2 file (2 manager.vue)

## Tài liệu
- Spec chi tiết: `docs/superpowers/specs/2026-05-06-request-solution-adjustment-design.md`
- SRS: `docs/srs/solution-adjustment-request-SRS.html`
- Test cases: `docs/srs/solution-adjustment-request-testcases.html` + `.xlsx` (47 TC)
