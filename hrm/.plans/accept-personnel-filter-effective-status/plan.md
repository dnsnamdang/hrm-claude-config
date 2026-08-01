# Bổ sung lọc trạng thái "Có hiệu lực" — màn Tiếp nhận nhân sự

Người phụ trách: @khoipv

## Bối cảnh

Màn `decision/accept-personnel` cột trạng thái đã hiển thị "Có hiệu lực" (status = 5 Đã duyệt + ngày hiệu lực ≤ hôm nay) nhưng dropdown Bộ lọc chưa có option này. Màn `transfer-personnel` đã có sẵn pattern (gửi `status=7` = `Decision::STATUS_EFFECTIVE`).

## Tasks

### BE

- [x] `AcceptPersonnelService::filterAcceptPersonnel()` — xử lý `status = 7 (STATUS_EFFECTIVE)`: `decisions.status = 5` + `effective_date <= now`; đồng thời `status = 5 (STATUS_APPROVED)` chỉ lấy `effective_date > now` (giống TransferPersonnelService, khớp badge hiển thị)

### FE

- [x] `pages/decision/accept-personnel/index.vue` — thêm `{ id: 7, text: 'Có hiệu lực' }` vào `listStatus` (sau "Đã duyệt")

Ghi chú: Export excel dùng chung `index()` → tự ăn theo filter, không cần sửa thêm.
