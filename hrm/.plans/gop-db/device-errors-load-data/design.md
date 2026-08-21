# Design — Màn Danh mục công việc, lỗi thiết bị: vào màn là load dữ liệu ngay

Người phụ trách: @khoipv — nhánh `gop_db`

## Hiện trạng / triệu chứng

Vào `/customer-care/device-errors`, bảng hiện chữ "Không có dữ liệu phù hợp bộ lọc." dù bảng
`device_errors` có 2768 bản ghi. Đợi đủ lâu (~30s trên máy dev) thì dữ liệu vẫn hiện ra.

## Nguyên nhân gốc (đo bằng `performance.getEntriesByType('resource')` trên trình duyệt)

| Request | Bắt đầu | Mất |
| --- | --- | --- |
| `device-errors/options-data` | 19.3s | 3.9s |
| `services/product-catalogs` | 23.2s | 3.9s |
| `device-errors?page=1&limit=20` | **27.1s** | 3.8s |

`mounted()` viết `await this.loadOptionsData()` rồi mới `await this.loadData()`, mà
`loadOptionsData()` gọi 2 API tuần tự chỉ để đổ dropdown bộ lọc → API danh sách bị xếp hàng
sau ~8 giây.

Trong khoảng chờ đó `loading` vẫn `false` (khởi tạo ở `data()`), nên `V2BaseDataTable` rơi vào
nhánh `v-else-if="!data.length"` và in `emptyText` — người dùng đọc thành "màn không có dữ liệu".

KHÔNG phải lỗi phân quyền (route gate `Quản lý danh mục công việc - lỗi thiết bị` — tài khoản
Super admin có quyền, API trả 200 + 2768 dòng), KHÔNG phải lỗi query
(`DeviceErrorService::list()` chạy trực tiếp trả `total=2768`).

Đối chiếu màn `customer-care/levels` (chạy tốt): `mounted()` chỉ gọi `loadData()`, không có bước
tải dropdown chặn phía trước.

## Quyết định

Chỉ sửa FE, 1 file `pages/customer-care/device-errors/index.vue`:

1. `loading` khởi tạo `true` → vào màn hiện spinner "Đang tải...", không hiện nhầm empty text
2. `mounted()` gọi `loadData()` ngay; `loadOptionsData()` chạy nền, không `await`
3. 2 request trong `loadOptionsData()` chạy song song bằng `Promise.all`

Không đụng Backend / query / phân quyền. Xem `plan.md` cho danh sách task.

Spec chi tiết (điều tra đã loại trừ gì, tác động lan tỏa, nghiệm thu):
`docs/superpowers/specs/gop-db/2026-08-13-device-errors-load-data-design.md`
