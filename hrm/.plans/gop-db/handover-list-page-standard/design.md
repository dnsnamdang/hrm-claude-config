# Design — Chuẩn hoá màn Danh sách phiếu bàn giao theo skill `list-page`

Người phụ trách: @khoipv · Nhánh: `gop_db` (cả `hrm-api` và `hrm-client`)
Spec chi tiết: `docs/superpowers/specs/gop-db/2026-09-07-handover-list-page-standard-design.md`

## Mục tiêu

Đưa `/assign/handover` về đúng khuôn `list-page` như 18 màn `assign/*` đã làm trước đó.

## Hiện trạng trước khi sửa

- Ô đầu bảng gộp **mã + tên nhân viên + 2 dòng phụ (Phòng ban / Cập nhật) + 3 icon thao tác**.
  Không có cột Hành động.
- 8 cột, **không cột nào khai `width`**; không `fixed-layout`.
- Slot `#toolbar` thay cả khối tiêu đề bảng → màn **mất tiêu đề "Danh sách phiếu bàn giao"**;
  toolbar chỉ có đúng 1 nút "Tạo phiếu".
- **Không có** cấu hình cột hiển thị (khai `isVisible` nhưng không có modal), **không có** xuất
  Excel, **không có** giữ bộ lọc khi quay lại, **không có** hành động Lịch sử.
- `handleFilterChange(filters)` nhận sai kiểu payload → nhét khoá rác `key`/`value` vào `filters`.
- `HandoverService::index()` sắp xếp bằng `orderBy($request->sort_field, $request->sort_dir)` —
  nhận thẳng chuỗi từ URL, không whitelist, không chốt `id desc`.
- FE tự so `item.created_by === currentEmployee.id` để quyết được Sửa/Xóa.
- Ô lọc **Bộ phận** ghi vào `filters.part_id` mà bảng `handovers` **không có cột `part_id`**.

## Quyết định chính

| Việc | Chốt |
| --- | --- |
| Cột định danh | **Mã phiếu**, `sticky` + `locked`, link sang `/assign/handover/{id}` |
| Hành động | Sửa · Xóa là 2 nút chính; Lịch sử vào `⋮`; **bỏ "Xem"** |
| Số cột | **18** (thêm Ghi chú, Ngày gửi duyệt, Người duyệt, Ngày duyệt, Lý do từ chối, Người cập nhật, Ngày cập nhật), mặc định hiện hết |
| Trạng thái | Chữ + màu do BE trả; Từ chối `#B91C1C` → `#DC2626` (4 mã còn lại đã đúng bảng) |
| Cờ Sửa/Xóa | Chuyển **nguyên điều kiện đang có ở FE** về BE (`is_can_edit` / `is_can_delete`) |
| Lịch sử | Popup mới `HandoverHistoryModal` bọc `SystemInfoSection` — dùng chung với khối Lịch sử ở màn chi tiết |
| Xuất file | **Lần đầu có**: route + `export()` + `ExportColumnRegistry['handovers']` 19 cột + `DynamicExport` |
| Bộ lọc | `V2BaseFilterPanel` → `V2BaseSmartFilterPanel`, 5 mục / 6 ô; tắt ô Bộ phận (BE không có cột) |

## Điểm đáng nhớ

- Bảng `handovers` **rỗng trên DB dev** → phải dựng 5 phiếu giả trong transaction rồi `ROLLBACK`
  để kiểm chứng; bề rộng cột lấy theo khuôn mã sinh tự động `BG.YYYY.NNNN` (12 ký tự).
- "Đã duyệt" giữ `#2563EB` (nhóm Đang thực hiện) chứ không lấy `#16A34A`: ở luồng bàn giao, duyệt
  xong phiếu mới **bắt đầu** giao/nhận việc, còn `#16A34A` đã dành cho "Hoàn tất".
- 2 màn cùng module `/assign/handover/pending` và `/assign/handover/receiving` dùng chung
  `HandoverResource` → hưởng lây khoá mới, nhưng **giao diện chưa chuẩn hoá**.
