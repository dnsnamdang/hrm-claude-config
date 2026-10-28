# Brief T1 + T2 — A3 (2-E) BE hrm-api

Repo `/Users/dnsnamdang/Documents/DNSMEDIA/websites/wt-chuyen-doi-hang-hoa/hrm-api`, nhánh **`feat/cdhh-2e-excel`** (đã checkout — KHÔNG đổi nhánh/merge/push/stash). DB dev `hrm_erp_giacty` (root, mật khẩu `.env`). PHP `/opt/homebrew/opt/php@7.4/bin/php`; trước artisan/phpunit: `ls bootstrap/cache/config.php` không tồn tại + `php artisan config:clear`. API 8031 đang chạy từ worktree này — không kill.
Đọc trước (nguồn yêu cầu): `/Users/dnsnamdang/Documents/DNSMEDIA/websites/ERP-HRM/HRM/.plans/gop-db/quan-ly-hang-hoa/excel-nghiem-thu-2e/khao-sat.md` — đặc biệt §1, §2.1, §4 "Điểm tự chốt kỹ thuật" 1–8, §5 (T1, T2) và **§6 chốt của user** (bản cuối, đè lên đề xuất cũ). Skill: `HRM/.claude/skills/export-excel` (đọc SKILL.md; bám repo thật nếu lệch). Tuân thủ `HRM/CLAUDE.md`.

## T1 — quyền 1654 "Xuất excel danh sách hàng hoá"
- Seeder riêng idempotent `Modules/MasterData/Database/Seeders/ProductExportPermissionSeeder.php` theo khuôn `ProductPricePermissionSeeder` (G6): chèn id 1654 nếu chưa có (kiểm cả theo id và theo name), không truncate. `group`/`type` lấy cùng nhóm với 1652/1653/1655 (đọc seeder chính).
- Thêm dòng giữ chỗ 1654 vào `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php` cạnh 1652/1653/1655 (sửa comment "1654 + 1656 seed ở đợt dùng tới" cho đúng). Giữ EOL.
- Test seeder (chạy 2 lần không nhân đôi).
- Runbook: thêm bước chạy seeder vào `/Users/dnsnamdang/Documents/DNSMEDIA/websites/ERP-HRM/HRM/.plans/gop-db/quan-ly-hang-hoa/gia-theo-cong-ty/runbook-trien-khai.md` (mục seeder quyền).
- **Được phép**: chạy đúng seeder riêng này vào `hrm_erp_giacty` (`php artisan db:seed --class=...`). KHÔNG chạy seeder khác.

## T2 — BE export-rows 5 màn
- `GET master-data/products/{screen}/export-rows` (screen ∈ whitelist 5 màn đúng key màn hiện có — tra routes/`ProductService::index` để lấy đúng tên screen, gồm màn Hàng tạm Phase 6 nếu nằm route khác thì khai theo khuôn màn đó), dùng lại đúng bộ lọc + gate quyền màn hiện tại, cộng `checkPermission` 1654 (fail-closed, không bypass super admin). Trả `{headings, widths, rows, total, page, limit}`, trần 5.000/lượt; tham số `fields[]` theo registry (key lạ bỏ qua).
- `app/ExcelExport/ExportColumnRegistry.php`: 5 khoá màn (khớp `columnScreenKey` FE — tra `hrm-client/utils/product-list-screens.js`), key cột trùng key cột màn / `ProductListResource`. **Kho dữ liệu không có cột Catalog**; 4 màn kia có cột Catalog = tên **Tiểu mục** của công ty đang làm, nhiều nhánh nối `"\n"`. **Không có cột giá nào.** Không cột ảnh. Số trả float, mã/barcode chuỗi.
- Không dùng `ProductListResource` cho export (N+1) — map bằng query gộp theo trang; đo thời gian 1 trang 5.000 dòng trên giacty (< ~2–3s; ghi số).
- PHPUnit `ProductExportApiTest`: đúng cột theo fields, key lạ bỏ, catalog nhiều nhánh ra nhiều dòng trong ô (tự dựng fixture), Kho không có catalog, 403 thiếu 1654, 403 thiếu quyền màn, phân trang + trần limit, không có trường giá trong output.
- **Bước 14'** (nghiệm thu "ERP không vỡ"): PHPUnit ép va chạm UNIQUE `products_code_unique` để chạy đường retry trong `ProductWriteService` (~dòng 88–113) — chiếm mã giữa generate và save (mock/spy generator hoặc chèn bản ghi chiếm mã trong callback), chứng minh lưu thành công với mã khác, không nhân bản dòng. File test phù hợp (vd `ProductCodeRetryTest`).
- Chạy file test mới + cả bộ `Modules/MasterData` (mốc 532/532), báo số.

## Ràng buộc
Giữ EOL; comment tiếng Việt; commit chia hợp lý trên nhánh, cuối message:
```
Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_014JQzu8PhMym1qvYWURxtd3
```
Lỗi ngoài luồng: ghi report, không vá. Không dispatch subagent. Không đổi CLAUDE.md/cấu hình.

## Report
`excel-nghiem-thu-2e/t12-report.md`: commit, endpoint (method/path/quyền/tham số/JSON mẫu 1 dòng mỗi màn), danh sách key cột theo màn (FE T3 dùng), số đo hiệu năng, kết quả test, việc ngoài luồng. Trả lời ngắn: trạng thái, commit, 1 dòng test, lo ngại.
