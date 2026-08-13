# Plan — Màn Danh mục công việc, lỗi thiết bị: vào màn là load dữ liệu ngay

Người phụ trách: @khoipv
Nhánh: `gop_db` (hrm-client)
Phạm vi: 1 file `pages/customer-care/device-errors/index.vue` — KHÔNG đụng Backend.

## Phase 1 — Bỏ chặn API danh sách + hiện đúng trạng thái đang tải

- [x] FE1. `data()`: `loading` khởi tạo `true` để bảng hiện spinner "Đang tải..." ngay khi vào màn,
      thay vì rơi vào nhánh empty của `V2BaseDataTable` và in nhầm "Không có dữ liệu phù hợp bộ lọc."
- [x] FE2. `mounted()`: gọi `loadData()` ngay, `loadOptionsData()` chạy nền (không `await`)
      → API danh sách không còn xếp hàng sau 2 API dropdown
- [x] FE3. `loadOptionsData()`: 2 request (`options-data`, `services/product-catalogs`) chạy song song
      bằng `Promise.all` thay vì tuần tự
- [x] FE4. Kiểm chứng bằng trình duyệt (Playwright, tài khoản DNS Admin): đo lại thời điểm
      request `device-errors?page=1&limit=20` bắn ra + xác nhận bảng hiện spinner rồi ra dữ liệu

### Checkpoint — 2026-08-13
Vừa hoàn thành: FE1-FE4, đã kiểm chứng trên trình duyệt.
Số đo sau khi sửa: cả 3 request (`options-data`, `product-catalogs`, `device-errors?page=1&limit=20`)
cùng bắt đầu tại mốc 20777ms (trước đó API danh sách phải chờ tới 27130ms trong khi 2 API kia
xong ở 19291/23171ms). Trong lúc chờ bảng hiện "Đang tải...", KHÔNG còn hiện
"Không có dữ liệu phù hợp bộ lọc."; kết quả cuối: 20 dòng/trang, `pagination.total = 2768`,
dropdown Loại 6 mục, dropdown Nhóm hàng hóa 884 mục.
Đang làm dở: không có.
Bước tiếp theo: anh Nam test lại trên máy mình; nếu ổn thì gộp về `gop_db`.
Blocked:

### Checkpoint — 2026-08-13 (ĐÓNG FEATURE)
Vừa hoàn thành: **feature HOÀN THÀNH** — user đã test trình duyệt xong và xác nhận PASS.
Sửa 1 file FE `pages/customer-care/device-errors/index.vue` (`loading: true` · `loadOptionsData()`
chạy nền · 2 request options gọi song song bằng `Promise.all`); không đụng BE.
Đang làm dở: không có.
Bước tiếp theo: không còn việc trong feature này. Đã chuyển sang mục "Hoàn thành" của `.plans/gop-db/STATUS.md`.
Chờ merge về `gop_db` theo quy trình chung (chưa commit — theo quy tắc project, không tự commit).
Blocked:

## Ghi chú ngoài phạm vi

Các API trên máy dev đang chậm ~3-8s/request (`user-profile` 8.3s, `options-data` 3.9s,
`product-catalogs` 3.9s). Sửa FE chỉ hết cảnh hiểu nhầm "không có dữ liệu" và rút ~8s chờ vô ích;
KHÔNG làm API nhanh lên. Nếu cần, mở task hiệu năng riêng.
