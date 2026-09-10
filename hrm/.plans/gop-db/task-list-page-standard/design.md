# Design — Chuẩn hoá màn Danh sách task theo skill `list-page`

Người phụ trách: @khoipv · Nhánh: `gop_db` (cả `hrm-api` và `hrm-client`)
Spec chi tiết: `docs/superpowers/specs/gop-db/2026-09-07-task-list-page-standard-design.md`

## Mục tiêu

Đưa `/assign/tasks` về đúng khuôn `list-page` như 17 màn `assign/*` đã làm trước đó, giữ nguyên
2 nét riêng của màn này: **lọc nhanh theo vai trò của tôi** (4 nút tròn) và **lọc theo Tag**.

## Hiện trạng trước khi sửa

- Ô đầu bảng gộp **mã + tên + 3 dòng phụ + chip tag + tối đa 6 icon thao tác**. Không có cột Hành động.
- Trạng thái và Ưu tiên tô màu bằng **4 hàm dựng style ở FE** (`getTaskStatusLabel`,
  `getTaskStatusStyle`, `getPriorityLevelStyle`, `hexToRgb`) — bảng màu chép cứng trong `.vue`.
- 15 cột, **không cột nào khai `width`**; không `fixed-layout`; sticky gán theo vị trí (`index < 3`).
- Slot `#toolbar` thay cả khối tiêu đề bảng → màn **mất luôn tiêu đề "Danh sách task"**.
- `TaskService::index()` sắp xếp bằng `orderBy($request->sort_field, $request->sort_dir)` — nhận
  thẳng chuỗi từ URL, không whitelist, không chốt `id desc`.
- `TaskResource` gọi `Employee::find()` 3 lần/dòng + `->load('priorityLevel')` mỗi dòng →
  **325 truy vấn cho 10 dòng**.
- Xuất Excel: `TaskExport` cột cứng (13 cột), file `.xls`, không cho chọn cột; query string dùng
  `buildQueryString` nên **lọc nhiều tag chỉ gửi được tag cuối cùng**.
- ~450 dòng code chết trong `.vue` (tìm khách hàng, `getNameScale`, `getStatusLabel`,
  `getProgressClass`, `getNameInvestmentType`, `getNameFundingSource`…) không nơi nào gọi.

## Quyết định chính

| Việc | Chốt |
| --- | --- |
| Cột định danh | **Mã task**, `sticky` + `locked`, là `<button class="v2-cell-link">` mở popup Xem — task KHÔNG có màn chi tiết riêng (skill mục 3a) |
| Hành động | Sửa · Xóa là 2 nút chính; Nhập kết quả · Duyệt · Lịch sử vào `⋮`; **bỏ "Xem"** |
| Số cột | **22** (thêm Tag, Tình trạng hạn, Ngày tạo, Người cập nhật, Ngày cập nhật thành cột riêng), mặc định hiện hết |
| Trạng thái | Chữ + màu do BE trả; 5/10 mã màu lệch bảng 9 mã chuẩn → quy về đúng nhóm |
| Ưu tiên | Thang màu **RIÊNG** (`Task::PRIORITIES`), BE trả `priority_name` + `priority_color` |
| Lọc nhanh + Tag | Giữ nguyên, chuyển sang slot `left-actions` để không mất tiêu đề bảng |
| Xuất file | `ExportColumnRegistry['tasks']` 27 cột + `DynamicExport` + popup chọn trường, `.xlsx` |
| Bộ lọc | `V2BaseFilterPanel` → `V2BaseSmartFilterPanel`, 15 mục / 17 ô |

## Điểm đáng nhớ

- **Quan hệ `Task::priorityLevel()` luôn trả null**: nó trỏ sang bảng `priority_levels` (id 5-8)
  còn cột `tasks.priority` lưu 1/2/3. Vì thế FE mới phải tự chế hằng `PRIORITY_LEVELS`. Nguồn
  chuẩn nay đặt ở `Task::PRIORITIES`, BE trả thẳng tên + màu.
- **`canEdit()` và `canDelete()` mỗi hàm bắn 1 truy vấn `subtasks()->exists()`** → 2 truy vấn/dòng;
  `canStartApprove()` hỏi quyền TRƯỚC khi xét trạng thái → thêm 3 truy vấn/dòng kể cả dòng không
  thể duyệt. Đã nhớ kết quả + đảo thứ tự điều kiện.
- Hiệu năng: **325 → 67 truy vấn / 10 dòng**.
- `task_tags` hiện **rỗng** trên DB dev nên cột Tag và ô lọc Tag chưa có dữ liệu thật để xem;
  đã kiểm bằng tham số giả (`tags[]=99999` → 0 dòng) để chắc bộ lọc có ăn.
