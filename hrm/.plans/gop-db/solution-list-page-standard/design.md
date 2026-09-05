# Chuẩn hoá màn Danh sách làm giải pháp theo skill `list-page`

- **Người phụ trách:** @khoipv
- **Nhánh:** `gop_db` (cả `hrm-api` + `hrm-client`)
- **Màn:** `/assign/solutions` — `hrm-client/pages/assign/solutions/index.vue`
- **Ngày bắt đầu:** 2026-09-05

## Mục tiêu

Đưa màn danh sách làm giải pháp về đúng chuẩn `.claude/skills/list-page/SKILL.md`.

## Hiện trạng lệch chuẩn

| Điểm | Hiện tại | Chuẩn |
| --- | --- | --- |
| Panel lọc | `V2BaseFilterPanel` + `title`/`subtitle` riêng, 18 ô hard-code trong slot | `V2BaseSmartFilterPanel` + schema `filterFields`, title mặc định |
| Cột định danh | 1 cột gộp `Mã-Tên giải pháp`, chứa luôn nút thao tác | Tách `Mã giải pháp` (link, sticky+locked) / `Tên giải pháp` (chữ thường) |
| Hành động | 5 nút nhét dưới tên (Xem/Quản lý/Sửa/Duyệt/Xóa) | Cột "Hành động" cuối bảng, `V2BaseRowActions`, bỏ "Xem" |
| Người tạo / Ngày tạo | không có cột | Bắt buộc, đứng trước Trạng thái |
| Cột mặc định | hiện cả 20 cột | 8 cột (7 chuẩn + Khách hàng) |
| Ô rỗng | ~20 chỗ in `—` | Để trống |
| Cấu hình cột | tự merge ~40 dòng trong page | `columnCustomizationMixin` |
| Xuất Excel | tải thẳng cả bảng, `$nuxt.$loading` | Popup chọn trường + `$safeLoading` |
| Sort | BE `orderBy($request->sort_field)` không whitelist | `SORTABLE_COLUMNS` |
| Auto-search | deep watcher không reset về trang 1; ô gõ tay cũng bắn API | reset `currentPage = 1`; `textFilterKeys()` |

## Quyết định (user chốt 2026-09-05)

1. **Phạm vi**: FE đầy đủ + BE tối thiểu (whitelist sort, tên người tạo, popup chọn trường xuất Excel).
   **Chưa làm** audit log → màn tạm **không có** hành động "Lịch sử" (skill mục 1 yêu cầu có; ghi nợ lại).
2. **Hành động**: 2 nút chính = **Sửa** + **Xóa**; menu `⋮` = Quản lý giải pháp, Lưu và duyệt / Giao cho Leader.
   Bỏ hẳn "Xem" — bấm Mã giải pháp vào chi tiết.
3. **Bộ lọc**: giữ hiện đủ 18 ô như hiện tại (chuyển sang schema `filterFields`, user tự tắt bớt ở popup "Cài đặt bộ lọc").

## Bộ cột mới

Mặc định hiện: `STT` → `Mã giải pháp` → `Tên giải pháp` → `Khách hàng` → `Người tạo` → `Ngày tạo` → `Tiến trình GP` → `Hành động`.

Các cột còn lại khai đủ nhưng `isVisible: false`: Yêu cầu làm GP, Dự án, Khách hàng cuối, Giai đoạn dự án,
Mức độ ưu tiên, Phòng làm GP, PM phụ trách, Ngày hoàn thành GP, Version, Phòng KD, KD phụ trách chính,
Nhóm ngành, Nhóm giải pháp, Ứng dụng, Loại hình hoạt động KH, Lĩnh vực kinh doanh KH, Người cập nhật, Ngày cập nhật.

⚠️ Khoá cột đổi (`solutionInfo` → `solutionCode` + `solutionName`, `status` → `solutionStatus`) là **có chủ ý**:
cấu hình cột đã lưu của user (`column_customizations.solutions`) ghim theo khoá, giữ khoá cũ thì cột nằm sai chỗ.

## Nợ lại

- **Hành động "Lịch sử"** — `solutions` chưa có audit log (chỉ có `solution_manager_logs` ghi việc giao PM/Leader).
  Cần làm theo skill `entity-history` ở đợt sau.
