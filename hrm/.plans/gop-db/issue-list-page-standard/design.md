# Design — Chuẩn hoá màn "Quản lý Issue" theo skill `list-page`

Người phụ trách: @khoipv · Nhánh: `gop_db` (cả `hrm-api` và `hrm-client`)
Spec chi tiết: `docs/superpowers/specs/gop-db/2026-09-08-issue-list-page-standard-design.md`

## Mục tiêu

Đưa `/assign/issues` về đúng khuôn `list-page`: bộ lọc schema, cột định danh là link, cột Hành
động ở cuối bảng, cấu hình cột, xuất file có chọn trường, và **chặn 1 lỗ hổng sort ở BE**
(`orderBy($request->sort_field)` không whitelist).

## Hiện trạng trước khi sửa

- Bộ lọc còn `V2BaseFilterPanel` cũ (12 ô nhập cứng trong slot, có `title`/`subtitle` riêng),
  user không bật/tắt được ô lọc; ô gõ tay (không có) — nhưng 2 ô ngày và 10 ô chọn đều nằm trong
  slot nên panel không đếm được số ô.
- Cột **"Mã-Tên issue"** gộp 1 cột, không phải link; **nút thao tác nằm bên trong ô đó** (5 nút
  `<button>` tự dựng, có cả "Xem").
- **Không cột nào khai `width`** → bảng 17 cột tự co giãn theo dữ liệu từng trang.
- Chữ trong ô **in đậm toàn bộ** (`font-weight-bold` ở 12 chỗ) và **21 chỗ chèn `'—'`** khi rỗng.
- **Thiếu cột Ngày tạo** (bắt buộc theo skill); "Người tạo" có nhưng key `createdName`.
- Cấu hình cột viết tay trong page (`getFields`/`updateColumns`/`defaultTableColumns`) thay vì
  `columnCustomizationMixin`; **STT và Mã-Tên không `locked`** nên user ẩn được cột định danh.
- Nút **Xuất Excel tải thẳng file `.xls`**, không hỏi chọn trường; BE dùng `IssueExport` cột cứng.
- `$nuxt.$loading` gọi thẳng trong `exportExcel()`; `handleSort`/`handleReset` gọi `loadData()`
  trong khi deep watcher cũng gọi → 2 request mỗi lần.
- BE `IssueService::index()` nhận **thẳng `sort_field`** từ query đẩy vào `orderBy` (không
  whitelist) — gõ tay tên cột lạ là 500, và FE mới gửi key cột (`issueCode`) sẽ nổ.
- Ô tìm nhanh chỉ tìm `title` + `issue_code`, **không tìm theo người tạo** như skill quy định.
- Màu trạng thái lệch bảng 9 mã chuẩn ở 3 trạng thái (Đã đóng, Hoàn thành, Từ chối).

## Quyết định chính

| Việc | Chốt |
| --- | --- |
| Kiểu màn | **Danh mục dùng modal** (không có route chi tiết) → cột định danh là `<button class="v2-cell-link">` mở modal Xem (skill mục 3a), **bỏ hành động "Xem"** |
| Cột định danh | **Mã issue** (`issueCode`), `sticky` + `locked`; Tiêu đề tách thành cột riêng |
| Số cột | **24**, mặc định **hiện hết** (chốt 2026-09-05 cho cả loạt màn `assign/*`), `fixed-layout` |
| Hành động | Sửa · Xóa (2 nút chính) + menu `⋮`: Xử lý · Lịch sử |
| Bộ lọc | `V2BaseSmartFilterPanel`, **13 mục** (thêm "Loại issue" — BE vốn đã nhận `issue_type` nhưng FE chưa có ô) |
| Sort | Whitelist `SORTABLE_COLUMNS` 6 khoá ở BE + chốt `id desc`; key lạ về mặc định `created_at desc` |
| Xuất file | Popup chọn trường + `ExportColumnRegistry['issues']` 22 cột + `DynamicExport` (bỏ `IssueExport` cột cứng) |
| Nhãn hiển thị | BE trả thêm `issue_type_text` / `detected_from_text` / `due_status_*` — **bỏ 3 hàm map ở FE** (skill mục 3c) |
| Màu trạng thái | Sửa 3 mã về bảng 9 màu chuẩn; "Mở lại" xếp nhóm *Chờ xử lý* `#D97706` |

## Điểm đáng nhớ

- `updated_by_name` cũ lấy từ accessor `employee_update_name` của `BaseModel` → ra **`MÃ - Tên`**,
  trái quy tắc "Người tạo/cập nhật chỉ hiện TÊN" (skill mục 6). Đổi sang `info->fullname`.
- Bảng `issues` **rỗng trên DB dev** → kiểm chứng bằng dữ liệu giả trong transaction rồi `ROLLBACK`
  (giống cách đã làm ở màn Phiếu bàn giao chờ tiếp nhận).
- 4 nút lọc nhanh (Tôi phụ trách / Tôi phát hiện / Tôi theo dõi / Tôi duyệt đóng) **giữ nguyên**,
  chỉ chuyển từ slot `#toolbar` (thay cả khối tiêu đề bảng) sang `#left-actions`.
- `quick_scope` không phải điều kiện lọc thật — nó chỉ set 1 trong 4 khoá `assignee_id` /
  `detected_by` / `watching_id` / `approver_id`. "Làm mới" vẫn xoá nó như mọi ô lọc khác.
