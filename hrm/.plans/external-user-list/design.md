# Quản lý học viên ngoài công ty — Design Summary

**Owner:** @junfoke  
**Module:** Training (FE: hrm-client) + Elearning (BE: elearning_learners)  
**Trạng thái:** Đang làm

## Mục tiêu

Tạo trang admin trong hrm-client để quản lý danh sách external learners — những người đăng ký học elearning qua form hoặc Google Auth (không phải nhân viên nội bộ).

## Scope

- **Xem** danh sách learner ngoài với bộ lọc + phân trang
- **Khoá / Mở khoá** tài khoản learner
- **Xem nhanh** thông tin chi tiết qua modal
- **Xuất Excel** danh sách

## Không làm

- Không tạo/sửa/xóa user
- Không phân quyền theo cấp (company/department/part)
- Không tính courses stats (chưa có bảng enrollment cho learner — hiển thị placeholder)

## Quyết định lớn

| Quyết định | Chọn | Lý do |
|------------|------|-------|
| Vị trí trang | hrm-client/pages/training/ | Admin HRM quản lý, không phải learner tự quản lý |
| API module | Modules/Training | Trang hiển thị ở Training, query bảng elearning_learners |
| Phân quyền | 1 quyền duy nhất, không phân cấp | External user không thuộc cơ cấu tổ chức |
| DB migration | Thêm field vào elearning_learners | company, position, interests, auth_source |

## Spec chi tiết

→ Xem `docs/superpowers/specs/2026-05-25-external-user-list-design.md`
