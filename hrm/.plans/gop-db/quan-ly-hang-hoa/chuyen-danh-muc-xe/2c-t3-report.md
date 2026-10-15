# Report T3 — ERP Phase 2c: chặn ghi 10 danh mục xe + menu trỏ HRM

Repo wt-erp-2d1 · nhánh `feat/cdhh-2c-xe-erp` · commit **4c553e300a** (chưa push/merge). Trạng thái: DONE_WITH_CONCERNS.

## Route đã chặn (35) — `productMovedToHrm:<khoá>` gắn từng route
| Nhóm (prefix) | Khoá | Route chặn |
|---|---|---|
| vehicle-manufacts | vehicle-manufacts | POST /, POST /{id}, GET /{id}/delete |
| vehicle-brands | vehicle-brands | POST /, POST /{id}, GET /{id}/delete |
| vehicle-models | vehicle-models | POST /, POST /{id}, GET /{id}/delete, GET /view-import, POST import-brand, POST import-model |
| vehicle_life | vehicle-life | POST /, POST /{id}, GET /{id}/delete |
| vehicle_categories | vehicle-categories | POST /, POST /{id}, GET /{id}/delete |
| vehicle_payloads | vehicle-payloads | POST /, POST /{id}, GET /{id}/delete |
| license-plates | license-plates | POST /, POST /{id}, GET /{id}/delete |
| drives | external-drivers | POST /, PUT /{id}, GET /{id}/delete |
| vehicles | vehicles | GET /create, GET /{id}/edit, POST /, POST /{id}, GET /{id}/delete |
| fuels | fuels | POST /, POST /{id}, GET /{id}/delete |

## Route giữ (không chặn)
- `index` + `searchData` của cả 10 nhóm: màn xem và nguồn dữ liệu bảng.
- `vehicleManufact.brands` (GET /vehicle-manufacts/{id}/brands): AJAX đọc, chỉ form tạo model xe (đã bỏ) gọi; là route đọc nên giữ theo brief.
- `vehicle.getRoadInfo`: vận chuyển (công thức/chuyến giao hàng) đọc.
- Grep resources/app/public/js: không màn nào ngoài 10 index gọi route ghi của 10 nhóm. Các partial `createX` chỉ được include trong chính index của nhóm đó.
  `partials/sale/createVehicle.blade.php` (gọi `vehicles.store`, route không tồn tại) không được include ở đâu — code chết có sẵn, không đụng.

## Middleware / trang báo
- `ProductMovedToHrm::TARGETS` +10 khoá → `/master-data/<khoá>` (đúng theo brief); thêm `VEHICLE_TARGETS` + biến `isVehicle`.
- `errors/moved_to_hrm.blade.php`: câu mặc định nói về "hàng hoá" → thêm nhánh riêng cho xe: "Danh mục đã chuyển sang quản lý trên HRM."

## Index + menu
- 10 màn index theo khuôn C-b (E4): bỏ nút Thêm mới (thay comment), bỏ `<th>Hành động</th>` + cột `action` trong JS, bỏ `@include('partials.sale.createX')` (8 màn), bỏ `addColumn('action')` ở 10 controller (searchData).
  Giữ nguyên (code chết, không có nút nào kích hoạt): modal sửa + handler `.edit` trong view — không dọn để diff gọn.
- `topmenubar.blade.php`: 9 mục khối "Xe" + "Danh mục nhiên liệu" ở khối "Vận chuyển - Bốc xếp" → `config('app.hrm_url_FE')/master-data/<khoá>`, `target=_blank`, nhãn ERP + " (HRM)".
- `topmenubar_old.blade.php`: không được include ở đâu (grep resources/app) → để nguyên.

## Kiểm
- `php artisan route:list`: không lỗi, 35 route có middleware.
- PHPUnit toàn bộ (sqlite mặc định): 185 ca, OK, 4 skipped (4 ca DB-thật mới, tự skip dưới sqlite) — không còn ca đỏ (ExampleTest nay xanh).
- `ProductMovedToHrmRoutesTest`: danh sách chặn 233 → 268, cập nhật ngoại lệ checkPermission cấp group (3 nhóm); 13 ca / 2140 assertion xanh.
- `VehicleRoutesMovedToHrmTest` (không DB): 10 nhóm POST store + update ⇒ 403 JSON đúng message + redirect_url; GET /{id}/delete ⇒ trang 403 có đúng 1 link HRM + câu trung tính, không có câu hàng hoá; create/edit xe + view-import + 2 POST import ⇒ chặn.
- `VehicleRoutesMovedToHrmDbTest` (chạy với `-c` phpunit trỏ mysql `hrm_erp_giacty`, config tạm đã xoá): 4 ca xanh, 83 assertion — POST store `license-plates` `drives` `vehicles` `fuels` `vehicle-manufacts` (+5 nhóm còn lại) ⇒ 403; số dòng 10 bảng trước = sau (license_plates 163 · drives 72 · vehicles 137 · fuels 4 · manufacts 56 · brands 322 · models 1281 · life 61 · categories 11 · payloads 31); 0 dòng 'T3-RAC'; index 10 nhóm 200; searchData 10 nhóm 200 và không còn key `action`; `brands` 200; `getRoadInfo` 200 JSON; menu có đúng 1 link HRM mỗi khoá, 0 link ERP cũ.

## Lo ngại / ngoài luồng
1. **Chưa kiểm bằng Playwright trên trình duyệt thật** (brief không yêu cầu; quy tắc root có). Đã có: index render 200 + bảng searchData không action; chưa đo DOM (số cột th khớp cột JS, không lỗi JS). Cần 1 lượt Playwright trước khi merge.
2. Thứ tự middleware: 3 nhóm (vehicle_categories, vehicle_payloads, fuels) có `checkPermission` ở cấp GROUP (có từ trước) ⇒ chạy trước productMovedToHrm. Hệ quả: người thiếu quyền vẫn nhận phản hồi của checkPermission, người có quyền nhận 403 chuyển HRM. Không đổi cấu trúc group theo khuôn C-b (attachment_types cũng vậy); test đã ghi ngoại lệ.
3. Search-header của vài màn index vốn lệch số `<th>` so với cột (có sẵn); không sửa.
4. Menu "Xe" + "Nhiên liệu" mở HRM bằng tab mới, nếu người dùng ERP chưa có quyền xem các màn `/master-data/...` trên HRM sẽ thấy 403 của HRM (quyền gate phía HRM — T1/T2).
5. Untracked `.env.bak-hrm_erp` trong worktree có sẵn từ trước, không phải của task này, không commit.
