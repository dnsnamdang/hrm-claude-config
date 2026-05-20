# Đính kèm file cho người thân — Tóm tắt

> **Spec chi tiết:** `docs/superpowers/specs/2026-05-20-family-attachment-design.md`

## Mục tiêu
Cho phép đính kèm file (mọi định dạng, tối đa 5 file/người thân) cho từng thành viên gia đình trong Thông tin nhân sự. Hỗ trợ cả flow edit trực tiếp và flow yêu cầu cập nhật (bảng tạm).

## Quyết định thiết kế
- **Lưu trữ:** Bảng riêng `employee_relationship_attachments` (1 row = 1 file), không dùng JSON column
- **Upload:** Tái sử dụng `FileController::uploadImage()` + S3 hiện có
- **UI:** Danh sách file hiển thị ngay trong hàng người thân (không popup), gồm tên file + dung lượng + nút xóa/tải
- **Flow tạm:** Bảng `employee_relationship_attachment_tmps` song song, copy sang chính khi approve

## Scope
- 2 bảng mới (chính + tạm)
- 2 model mới + cập nhật 2 model cũ
- Cập nhật 2 service (EmployeeInfoService + EmployeeInfoUpdateRequestService)
- Cập nhật 1 component FE (EmployeeInfoForm.vue)
