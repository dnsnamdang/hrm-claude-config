# Design — Siết quyền màn Danh mục nguyên nhân thất bại dự án

Phụ trách: @khoipv · Nhánh: `fix-bug-11092026` (cả 2 repo) · Ngày: 14/09/2026

Màn: `/assign/reason_project_failure` · Quyền 990 (Quản lý) / 1005 (Xem).

> Màn **Lý do hủy cuộc họp** (`/assign/meeting_cancel_reason`) dựng cùng khuôn và dính đúng các lỗi
> dưới đây; việc siết quyền màn đó theo dõi riêng ở `.plans/danh-muc-ly-do-huy-cuoc-hop/`.

## Vấn đề

User cấp cho tài khoản test **chỉ quyền "Xem danh mục nguyên nhân thất bại dự án"** nhưng vào màn
`/assign/reason_project_failure` vẫn bấm được Sửa / Xoá / Khoá.

## Kết luận điều tra

BE **không** fail-open. Mọi route ghi đều đã gắn `checkPermission:Quản lý danh mục nguyên nhân thất
bại dự án` và trả 403 đúng (đã đo bằng JWT thật trên DB local, dữ liệu không suy suyển). Cảm giác
"vẫn làm được" đến từ 3 thứ ở tầng giao diện:

1. `pages/assign/reason_project_failure/index.vue` chỉ dùng cờ `canManage` để ẩn **Tạo mới** và
   **Import Excel**; ba nút **Sửa / Xoá / Khoá-Mở khoá** trong bảng không gate → vẫn hiện, vẫn bấm.
2. Route `GET /assign/reason_project_failures/{id}` (xem chi tiết) không gắn `checkPermission`, nên
   modal Sửa mở ra và nạp đủ dữ liệu, gõ sửa thoải mái — chỉ tới lúc bấm Lưu mới 403.
3. Trong màn này cả 3 chỗ gọi API đều `if (status === 403) return` (không toast tại chỗ), modal
   cũng không tự đóng; chỉ còn toast chung từ `plugins/axios.js`. Nhìn như thao tác vẫn chạy.

## Quyết định

- **FE**: thêm `v-if="canManage"` cho 3 nút Sửa / Xoá / Khoá-Mở khoá. Giữ nguyên kiểu nút
  `<button>` inline — KHÔNG refactor sang `V2BaseIconButton`, vì nhánh `gop_db` đã chuẩn hoá màn
  này riêng (`.plans/gop-db/reason-project-failure-list-page-standard/`), đụng vào sẽ khó merge.
- **BE**: gắn `checkPermission:Quản lý…|Xem…` cho route xem chi tiết (`show`).
- **Cố ý KHÔNG gate `GET /getAll`**: đó là dropdown của modal Đóng dự án tiềm năng
  (`CloseProjectModal.vue`); route đóng dự án không gắn `checkPermission` nên người đóng dự án có
  thể không có quyền danh mục — gate vào là họ không đóng được dự án. Dữ liệu trả về chỉ là id +
  tên danh mục đang active.
- Cờ quyền vẫn fail-closed: `canManage` đọc từ `hasAPermission(...)`, không hard-code.

## Phạm vi thay đổi

| Repo | File |
| --- | --- |
| `hrm-client` | `pages/assign/reason_project_failure/index.vue` (3 chỗ `v-if`) |
| `hrm-api` | `Modules/Assign/Routes/api.php` (1 route thêm middleware) |

Không migration, không quyền mới, không đụng hàm dùng chung.

Chi tiết kiểm chứng: `plan.md` cùng thư mục.

## Bổ sung 14/09/2026 — nút Xuất Excel

Rà sang màn Lý do hủy cuộc họp thì lộ thêm một chỗ hở mà màn này cũng có: nút **Xuất Excel** không
gate, trong khi BE `GET /export` đòi quyền Quản lý.

Quyết định: **giữ BE `/export` chỉ nhận quyền Quản lý**, FE ẩn nút cho khớp. Lý do: 14/15 màn danh
mục trong `Modules/Assign/Routes/api.php` đều gắn export bằng đúng quyền "Quản lý danh mục …"; nới
thành `Quản lý|Xem` là mở rộng quyền truy cập và lệch convention. Nếu nghiệp vụ muốn người chỉ Xem
cũng xuất được thì sửa 1 dòng middleware — nhưng nên sửa đồng loạt cả 15 màn, không sửa lẻ.

| Repo | File | Thay đổi |
| --- | --- | --- |
| `hrm-client` | `pages/assign/reason_project_failure/index.vue` | thêm 1 chỗ `v-if="canManage"` (Xuất Excel) |
