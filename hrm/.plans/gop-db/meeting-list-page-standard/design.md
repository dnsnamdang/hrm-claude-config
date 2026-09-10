# Design — Chuẩn hoá màn Danh sách meeting theo skill `list-page`

Người phụ trách: @khoipv · Nhánh: `gop_db` (cả `hrm-api` và `hrm-client`)
Spec chi tiết: `docs/superpowers/specs/gop-db/2026-09-07-meeting-list-page-standard-design.md`

## Mục tiêu

Đưa `/assign/meeting` về đúng khuôn `list-page` như 16 màn `assign/*` đã làm trước đó: cột định
danh là link, cột Hành động ở cuối bảng, badge lấy chữ + màu từ BE, bảng `fixed-layout` khai đủ
`width` = `minWidth`, có cấu hình cột + popup chọn trường xuất file.

## Hiện trạng trước khi sửa

- Ô đầu bảng gộp **mã + tên + 3 dòng phụ (Người tạo / Ngày tạo / Cập nhật) + tối đa 6 icon thao tác**
  qua `V2BaseTitleSubInfo`. Không có cột Hành động.
- Trạng thái / Loại / Hình thức / Biên bản vẽ bằng **chuỗi HTML tự dựng + `v-html`**; trạng thái
  đoán bằng `String.includes('hoàn thành')` — đổi một chữ trong tên là badge đổi màu.
- Link "Xem biên bản" là `<a href="javascript:void(0)">` bắt sự kiện bằng listener trên `document`.
- 10 cột, **không cột nào khai `width`**; không có `fixed-layout`.
- `MeetingController::index()` đọc biến `$sortMapping` **chưa hề được khai báo** trong file.
- `MeetingCriteria` tự `orderBy` → mọi `orderBy` của controller chỉ còn là khoá phụ.
- `index()` để `with([])` → **175 truy vấn cho 10 dòng**.
- Xuất Excel: `MeetingExport` cột cứng, file `.xls`, không cho chọn cột.

## Quyết định chính

| Việc | Chốt |
| --- | --- |
| Cột định danh | **Mã meeting** (40/40 bản ghi có mã), `sticky` + `locked`, link sang `/assign/meeting/{id}/show` |
| Hành động | Sửa · Xóa là 2 nút chính; In biên bản · Tạo phiếu công tác khác · Lịch sử vào `⋮`; **bỏ "Xem"** |
| Số cột | **18** (thêm Địa điểm, Người tạo/Ngày tạo/Người cập nhật/Ngày cập nhật thành cột riêng), mặc định hiện hết |
| Trạng thái | Chữ + màu do BE trả (`status_name` / `status_color`), quy về bảng 9 mã màu chuẩn |
| Sắp xếp | Chuyển hẳn về controller (`SORTABLE_COLUMNS` + chốt `id desc`); **bỏ khối sắp xếp trong `MeetingCriteria`** |
| Xuất file | `ExportColumnRegistry['meetings']` 21 cột + `DynamicExport` + popup chọn trường, file `.xlsx` |
| Bộ lọc | `V2BaseFilterPanel` → `V2BaseSmartFilterPanel`, 11 mục / 13 ô |

## Điểm đáng nhớ

- Ô lọc **Nhân viên** của `V2BaseCompanyDepartmentFilter` ghi vào khoá `employee_id` mà
  `MeetingCriteria` **không đọc** → ô lọc chết. Đã tắt (`disable_employee`) và thay bằng ô
  **Người tạo** (`created_by`, BE có xử lý).
- `initialStateForm` khai `company_name` trong khi component ghi vào `company_id` → "Làm mới"
  không xoá được ô Công ty. Đã đổi về `company_id`.
- Nhãn trạng thái trong bộ lọc ("Lưu nháp / Lên lịch hẹn / Đã chốt lịch") **khác** chữ badge trên
  bảng ("Đang tạo / Lên lịch / Chốt lịch") → đã đồng bộ theo `Meeting::STATUS`.
- Hiệu năng: **175 → 70 truy vấn / 10 dòng** nhờ eager load + bỏ `find(null)` khi meeting không có
  khách hàng.
