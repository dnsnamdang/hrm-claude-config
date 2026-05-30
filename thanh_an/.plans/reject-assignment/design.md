# Từ chối phân công dự toán — Tóm tắt Design

> Người phụ trách: @khoipv
> Ngày: 2026-05-20
> Spec chi tiết: `docs/superpowers/specs/2026-05-20-reject-assignment-design.md`

## Mục tiêu

Thêm chức năng "Từ chối phân công" trên màn dự toán. Khi dự toán ở trạng thái "Chờ phân công" (DA_DUYET = 2), người có quyền "Phân công báo giá" có thể từ chối → nhập lý do → dự toán chuyển sang trạng thái "Hủy dự toán" (HUY_DU_TOAN = 17, trạng thái cuối cùng).

## Scope

- **DB:** Thêm 3 cột (`reason_reject_assignment`, `rejected_by`, `rejected_at`) + constant `HUY_DU_TOAN = 17`
- **BE:** API mới `PUT /projects/{id}/reject-assignment`, method `canRejectAssignment()`, cập nhật Resource
- **FE danh sách:** Nút icon từ chối + modal lý do + status mới (filter, color, text)
- **FE chi tiết:** Nút từ chối + modal + hiển thị thông tin từ chối khi status = 17

## Quyết định lớn

| Quyết định | Lý do |
|-----------|-------|
| API endpoint riêng (không dùng chung assign-employee) | Tách biệt logic, dễ maintain, follow pattern hiện có |
| Status mới = 17 (không reuse status cũ) | Rõ ràng, không conflict với logic hiện có |
| Trạng thái cuối, không khôi phục | Yêu cầu nghiệp vụ |
| Quyền dùng chung "Phân công báo giá" | Cùng đối tượng sử dụng |
