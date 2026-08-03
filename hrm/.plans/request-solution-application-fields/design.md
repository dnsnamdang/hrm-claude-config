# Yêu cầu làm giải pháp — 3 trường Ứng dụng / Nhóm ngành / Nhóm giải pháp

**Tóm tắt** — chi tiết xem `docs/superpowers/specs/2026-06-26-request-solution-application-fields-design.md`.

## Mục tiêu
Bổ sung 3 trường vào màn **Yêu cầu làm giải pháp** (`request_solutions`) — form Tạo/Sửa, Xem chi tiết, Phê duyệt (Tiếp nhận):
- **Ứng dụng** (`application_id`): kế thừa từ dự án TKT liên kết (`project_key`), readonly, KHÔNG lưu cột (derive).
- **Nhóm ngành** (`scope_id`): cột mới, không bắt buộc, lọc theo Ứng dụng.
- **Nhóm giải pháp** (`industry_id`): cột mới, không bắt buộc, lọc theo Ứng dụng.

Thuật ngữ (đảo, đã xác nhận): Nhóm ngành = `scope_id`, Nhóm giải pháp = `industry_id`.

## Quyết định chính
- Ứng dụng derive từ dự án (không snapshot cột).
- Nhóm ngành/Nhóm giải pháp mặc định trống, user tự chọn.
- Validate ở FormRequest (`withValidator`): nullable, nếu có phải thuộc mapping scopes/industries của Ứng dụng dự án; dự án không có app → buộc rỗng.
- FE tái dùng pattern `optionsSelect` (getApplications/getScopes/getIndustries) như màn Giải pháp `InfoTab.vue`; khác ở chỗ không có app → options rỗng (không "hiện tất cả").

## Phạm vi
- Đích: `RequestSolution` (KHÔNG nhầm `Solution`).
- BE: migration 2 cột + relation scope/industry + RequestSolutionRequest + Service store/update + DetailRequestSolutionResource.
- FE: RequestSolutionForm + RequestTab (3 field, mirror InfoTab) + trang show.
- Ngoài phạm vi: cột danh sách, permission mới, màn Giải pháp, git.
