# Design (tóm tắt) — Chặn ký tự , và : trong tên 5 danh mục KH

## Mục tiêu
Cấm ký tự dấu phẩy (,) và dấu hai chấm (:) trong **tên** (`name`) của 5 danh mục khi tạo mới / cập nhật / import Excel. Chặn ghi DB ở backend; frontend hiển thị lỗi.

## Phạm vi 5 danh mục (đều thuộc module Assign)
| Danh mục | Bảng | FormRequest | Service import | FE dir |
|---|---|---|---|---|
| Lĩnh vực kinh doanh KH | customer_scopes | CustomerScopeRequest | CustomerScopeService | customer-scopes |
| Loại hình hoạt động KH | customer_scope_groups | CustomerScopeGroupRequest | CustomerScopeGroupService | customer-scope-groups |
| Nhóm ngành | scopes | ScopeRequest | ScopeService | industry-groups |
| Nhóm giải pháp | industries | IndustriesRequest | IndustriesService | solution-groups |
| Ứng dụng | applications | ApplicationsRequest | ApplicationService | application |

## Quyết định chính
- **Validate chủ yếu ở backend** (theo chốt user). FE chỉ hiển thị lỗi tương ứng, chỉ check khi bấm Lưu.
- Rule BE: `not_regex:/[,:]/` trên field `name`, **bắt buộc dùng array-syntax** cho rule (pattern chứa `,` → pipe-string sẽ bị Laravel cắt nhầm tham số).
- Message thống nhất: `không được chứa ký tự dấu phẩy (,) và dấu hai chấm (:)`.
- Import: thêm `preg_match('/[,:]/', $name)` trong `validateImportData` (chỉ cột `name`, KHÔNG đụng cột mã quan hệ vốn dùng `,`/`:` làm ký tự phân tách như catCode/customerScopeCode/groupCode).
- FE modal tạo/sửa: KHÔNG sửa — đã có sẵn hiển thị lỗi `name` từ 422 (formError['name'] / error.name).
- FE `importValidationRules` (5 index.vue): thêm check ký tự cho preview import nhất quán với server.

## Không đụng
Migration, permission, hàm dùng chung. Không chạm cột code/description.

## Verify (tinker)
- Rule not_regex: tên hợp lệ pass; "a,b" và "a:b" bị chặn + message chuẩn.
- CustomerScopeGroupService::validateImportData: dòng name có `,`/`:` → isValid=false + đúng message.

Chi tiết đầy đủ: docs/superpowers/specs/2026-07-14-catalog-name-validate-special-chars-design.md
