# Icon "Xem mẫu phiếu thu thập thông tin" cạnh Nhóm giải pháp — Tóm tắt

**Phụ trách:** @manhcuong · **Ngày:** 2026-06-17 · Feature nhỏ (1 phase, chỉ FE)
**Spec đầy đủ:** `docs/superpowers/specs/2026-06-17-prospective-project-form-template-icon-design.md`

## Mục tiêu
Thêm icon tài liệu cạnh trường "Nhóm giải pháp" ở form Tạo mới / Cập nhật dự án TKT,
làm lối tắt mở nhanh (tab mới) mẫu Phiếu thu thập thông tin tương ứng nhóm giải pháp.

## Quyết định lớn
- **Chỉ FE**, sửa 1 file: `prospective-projects/components/ProjectInfoSection.vue` (dùng chung add + edit).
- **BE không đổi** — tái dùng `GET /v1/assign/form-templates/find-by-criteria?industry_id=...` (trả Published hoặc 404).
- Tiêu chí khớp: **chỉ `industry_id`** (Nhóm giải pháp). Link đích: **chi tiết** `/assign/form-templates/:id`.
- Icon: Remix Icon `ri-file-text-line`; tooltip qua `b-popover` (pattern info-tip sẵn có).

## Trạng thái icon
| Trạng thái | Màu | Click | Tooltip |
|---|---|---|---|
| Chưa đủ 2 field | `#94a3b8` | ✗ | (ẩn) |
| Đủ 2 field, có mẫu | `#16a34a` | ✓ → tab mới | "Xem chi tiết mẫu phiếu thu thập thông tin" |
| Đủ 2 field, chưa có mẫu | `#94a3b8` | ✗ | "Chưa cấu hình mẫu phiếu thu thập thông tin" |

## Lưu ý thuật ngữ
`scope_id` = Nhóm ngành · `industry_id` = Nhóm giải pháp (tên field ngược label).
