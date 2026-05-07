# Yêu cầu điều chỉnh giải pháp — Design Summary

## Mục tiêu
Cho phép KD (người tạo dự án TKT) gửi yêu cầu điều chỉnh giải pháp khi GP đã được duyệt, để TP/PM xem xét và tạo version mới nếu tiếp nhận.

## Scope
- Entity mới: `solution_adjustment_requests` với code `YCDCGP.NNNNN`
- 3 status: Đã gửi → Tiếp nhận / Từ chối
- UI: Tab con trong tab "Giải pháp" của Dự án TKT (danh sách + popup tạo/xem)
- Notification cho TP + PM khi tạo phiếu
- Không xóa, không nháp, không sửa phiếu đã gửi

## Quyết định lớn
- **Phương án A**: Entity riêng (không mở rộng `request_solutions`) — flow đơn giản hơn, tách biệt rõ ràng
- Khi tiếp nhận chỉ đánh dấu, TP/PM tự tạo version mới thủ công
- Phiếu bị từ chối → tạo phiếu mới, không sửa phiếu cũ
- Quyền tạo: chỉ `prospective_project.created_by`
- Quyền xử lý: PM (`solution.pm_id`) hoặc TP (qua `departmentsManager()`)

## Spec chi tiết
→ `docs/superpowers/specs/2026-05-06-request-solution-adjustment-design.md`
