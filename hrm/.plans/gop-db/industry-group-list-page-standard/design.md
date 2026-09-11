# Chuẩn hoá màn Danh sách nhóm ngành theo skill `list-page`

- **Người phụ trách:** @khoipv
- **Nhánh:** `gop_db` (cả `hrm-api` + `hrm-client`)
- **Màn:** `/assign/industry-groups` — `hrm-client/pages/assign/industry-groups/index.vue`
- **Ngày:** 2026-09-05 · Làm ngay sau [solution-list-page-standard](../solution-list-page-standard/design.md)

## Mục tiêu

Đưa màn danh mục Nhóm ngành về đúng `.claude/skills/list-page/SKILL.md`. Đây là **màn danh mục dùng
modal** (không có route chi tiết) nên áp mục 3a của skill.

## Hiện trạng lệch chuẩn

| Điểm | Hiện tại | Chuẩn |
| --- | --- | --- |
| Panel lọc | `V2BaseFilterPanel` + `title`/`subtitle` riêng, 8 ô hard-code trong slot | `V2BaseSmartFilterPanel` + schema `filterFields` |
| Ô lọc gõ tay | Gõ 1 ký tự = 1 request (deep watcher không loại ô text) | `textFilterKeys()` — chờ Enter / nút Tìm kiếm |
| Cột định danh | 1 cột gộp `Mã - Tên`, chứa luôn 3 nút thao tác | Tách `Mã` (button `.v2-cell-link` mở modal Xem) / `Tên` |
| Hành động | Xem / Sửa / Xóa nhét dưới tên, disable + tooltip | Cột "Hành động" cuối, `V2BaseRowActions`, bỏ "Xem", ẩn thay vì disable |
| Nút Khóa/Mở khóa | Nằm TRONG ô Trạng thái | Chuyển sang cột Hành động (menu `⋮`) |
| Trạng thái | `v-html` + `status-pill` tự dựng | `V2BaseBadge` `variant` brand/required |
| Người tạo / Ngày tạo | Là dòng phụ trong cột gộp | Cột riêng, bắt buộc |
| Cấu hình cột | không có | `columnCustomizationMixin` |
| Xuất Excel | tải thẳng cả bảng, `$nuxt.$loading` | Popup chọn trường + `$safeLoading` |
| Sort | BE whitelist chỉ có `updated_at` | Mã / Tên / Ngày tạo / Ngày cập nhật |
| Ô tìm nhanh | Placeholder ghi "người tạo, người cập nhật" nhưng BE chỉ tìm mã + tên | BE tìm thêm người tạo (EXISTS) |
| Ô rỗng | in `—` | Để trống |

## 3 bug có thật phát hiện khi soát (không phải do lần sửa này)

1. **Tạo mới / Sửa nhóm ngành nổ 500** — `Unknown column 'internal_business_scope_id' in 'field list'`.
   Migration `2026_08_22_000002_..._to_scopes_table` thêm cột vào bảng **`scopes` của ERP**, trong khi
   entity `Scope` khai `$table = 'hrm_scopes'` (bảng HRM đã đổi tên khi gộp DB).
2. **Lọc theo Lĩnh vực Công ty kinh doanh nổ 500** — cùng gốc, cộng thêm câu lọc viết cứng tiền tố
   `scopes.` trong `ScopeService::index()`.
3. **Cột Lĩnh vực Công ty kinh doanh luôn trống** trên danh sách — hệ quả của (1).

Đã đo lại trên **cổng dev `hrm-crm.eteksofts.com`**: cùng lỗi 500, `internal_business_scope_name` = null
→ bug đang chạy thật, không phải khác biệt dữ liệu local.

**Cách sửa:** migration mới thêm cột vào `hrm_scopes` (nullable, có index rút gọn tên).
**KHÔNG backfill** — nhóm ngành nào thuộc lĩnh vực nào là dữ liệu nghiệp vụ, gán bừa "Khác" là bịa số
liệu; bản ghi cũ để trống, người dùng chọn lại khi sửa.

## Quyết định

- **Lịch sử thay đổi**: KHÔNG làm (user chốt 2026-09-05 — tôi tự thêm rồi phải gỡ). Skill có yêu cầu
  nhưng đó không phải phạm vi user giao; muốn làm thì mở việc riêng.
- **Hành động**: 2 nút chính = Sửa + Xóa; menu `⋮` = Khoá - Mở khoá, Lịch sử.
- **Nút Khoá bị ẩn khi chưa khoá hết danh mục con** (skill: ẩn thay vì disable) → lý do chuyển sang
  `title` của badge Trạng thái để user vẫn biết vì sao.
- **Bộ cột mặc định 7 cột**: STT · Mã nhóm ngành · Tên nhóm ngành · Người tạo · Ngày tạo · Trạng thái ·
  Hành động. Lĩnh vực Công ty kinh doanh, Số nhóm giải pháp, Số ứng dụng, Mô tả, Người/Ngày cập nhật
  khai đủ nhưng mặc định ẩn — user tự bật ở "Cấu hình cột hiển thị".
