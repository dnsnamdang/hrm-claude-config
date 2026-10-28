# Brief T3 — ERP Phase 2c: chặn ghi 10 danh mục xe + menu trỏ HRM

Repo: `/Users/dnsnamdang/Documents/DNSMEDIA/websites/wt-erp-2d1`, nhánh **`feat/cdhh-2c-xe-erp`** (đã checkout — KHÔNG đổi nhánh, KHÔNG merge, KHÔNG push, KHÔNG git stash).
PHP `/opt/homebrew/opt/php@7.4/bin/php`. Trước mọi artisan/phpunit: `ls bootstrap/cache/config.php` phải không tồn tại, rồi `php artisan config:clear`. DB qua `.env` (DB gộp `hrm_erp_giacty`).
Đọc trước: `/Users/dnsnamdang/Documents/DNSMEDIA/websites/ERP-HRM/HRM/.plans/gop-db/quan-ly-hang-hoa/chuyen-danh-muc-xe/khao-sat-2c.md` + `plan-2c.md` (Đợt T3).

## Bối cảnh
User chốt 14/10 (Q2): sau Phase 2c, **10 danh mục xe chỉ ghi ở HRM**; ERP chặn ghi + menu trỏ HRM. Cơ chế có sẵn: middleware `productMovedToHrm:<khoá>` (`app/Http/Middleware/ProductMovedToHrm.php`, hằng `TARGETS`) — xem cách đợt C-b chặn 9 danh mục Phase 1 (`routes/web.php` quanh dòng 140–190, ví dụ origins) và menu `resources/views/layouts/topmenubar.blade.php` dòng ~20–35 (link `config('app.hrm_url_FE') . '/master-data/...'` kèm "(HRM)", `target="_blank"`).

## Việc
1. `TARGETS` thêm 10 khoá → đường HRM:
   `vehicle-manufacts` → `/master-data/vehicle-manufacts` · `vehicle-brands` → `/master-data/vehicle-brands` · `vehicle-models` → `/master-data/vehicle-models` · `vehicle-life` → `/master-data/vehicle-life` · `vehicle-categories` → `/master-data/vehicle-categories` · `vehicle-payloads` → `/master-data/vehicle-payloads` · `license-plates` → `/master-data/license-plates` · `external-drivers` → `/master-data/external-drivers` · `vehicles` → `/master-data/vehicles` · `fuels` → `/master-data/fuels`.
   Nếu trang báo có câu mô tả theo nhóm khoá (như PRICE_TARGETS) thì kiểm câu mặc định có hợp với danh mục xe không ("thông tin hàng hoá"?) — nếu câu nói về hàng hoá thì thêm nhóm khoá riêng với câu trung tính "Danh mục đã chuyển sang quản lý trên HRM".
2. `routes/web.php` — gắn `->middleware('productMovedToHrm:<khoá>')` (đứng TRƯỚC checkPermission nếu có, gắn theo từng route) cho mọi route GHI của 10 nhóm: `vehicle-manufacts`, `vehicle-brands`, `vehicle-models` (gồm `view-import` + 2 POST import), `vehicle_life`, `vehicle_categories`, `vehicle_payloads`, `license-plates`, `drives`, `vehicles` (store/update/delete/create/edit), `fuels`. Route ghi = store/update/delete (kể cả GET `/{id}/delete`), create/edit, import.
   **GIỮ không chặn**: `index`, `searchData`, `vehicleManufact.brands`, `vehicle.getRoadInfo`, và mọi route đọc khác. Trước khi quyết, grep toàn `resources/views` + `public/js` + `app` xem màn khác gọi route nào của 10 nhóm (vd form chuyến giao hàng gọi `vehicleManufact.brands`?) — route bị màn khác gọi thì giữ.
   Có thể gom group-level? KHÔNG — theo khuôn C-b gắn từng route.
3. Màn index ERP của 10 danh mục: ẩn nút Thêm / Sửa / Xoá (hoặc thay bằng link "Quản lý trên HRM") để không có nút chết; nếu khuôn C-b chỉ đổi menu mà giữ trang index nguyên trạng thì làm theo khuôn C-b và ghi rõ — nhưng nút bấm phải ra thông báo rõ ràng (middleware đã trả JSON/ trang 403 có link), không được im lặng.
4. Menu `topmenubar.blade.php`: khối "Xe" 9 mục + mục "Danh mục nhiên liệu" ở khối "Vận chuyển - Bốc xếp" ⇒ link HRM kiểu C-b, giữ nhãn ERP + " (HRM)". Kiểm `topmenubar_old.blade.php` có còn được include ở đâu không; không dùng thì để nguyên.
5. Kiểm: `php artisan route:list` không lỗi; với HTTP (chạy `php artisan serve --port=8090` NỀN, ghi PID, kill đúng PID khi xong — KHÔNG pkill theo tên): đăng nhập ERP local (tìm cách các đợt trước làm — ERP local tắt SSO; có thể dùng `actingAs` trong PHPUnit thay vì HTTP) và chứng minh: POST store `license-plates` + `drives` + `vehicles` + `fuels` + `vehicle-manufacts` ⇒ 403 JSON đúng message, GET `/{id}/delete` ⇒ trang 403 có link HRM, `searchData` 4 nhóm vẫn 200, `vehicle.getRoadInfo` vẫn chạy. Ưu tiên viết PHPUnit feature test (tìm test của ProductMovedToHrm đã có — mở rộng nó) phủ đủ 10 khoá. Số dòng bảng không đổi (license_plates 163 · drives 72 · vehicles 137 · fuels 4 · vehicle_manufacts/brands/models/life/categories/payloads giữ nguyên trước/sau).
6. Chạy PHPUnit liên quan + báo số (mốc cũ: 62 ca, 1 đỏ sẵn ExampleTest).

## Ràng buộc
- Giữ EOL từng dòng (`git diff --numstat` kiểm). Blade: không dùng `@json` với closure/->map.
- Commit tiếng Việt trên `feat/cdhh-2c-xe-erp`, kết thúc:
  ```
  Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
  Claude-Session: https://claude.ai/code/session_014JQzu8PhMym1qvYWURxtd3
  ```
- Không dispatch subagent. Lỗi ngoài luồng: ghi report, không vá.

## Report
Ghi vào `/Users/dnsnamdang/Documents/DNSMEDIA/websites/ERP-HRM/HRM/.plans/gop-db/quan-ly-hang-hoa/chuyen-danh-muc-xe/2c-t3-report.md`: commit, bảng route đã chặn / giữ (kèm lý do giữ), thay đổi menu/index, kết quả test, vấn đề ngoài luồng. Trả lời ngắn: trạng thái, commit, 1 dòng test, lo ngại.
