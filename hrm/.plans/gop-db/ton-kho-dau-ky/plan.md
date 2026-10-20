# Khai báo tồn kho đầu kỳ — Plan

> Design: `.plans/gop-db/ton-kho-dau-ky/design.md` · Nhánh `feat/chuyen-doi-hang-hoa` (cả 2 repo)

## Phase 0 — Khảo sát (xong 20/10)

- [x] Đọc ERP (controller, model, import, 3 view, class JS, popup hàng `begin_stock`), đếm dữ liệu gop_db
- [x] User chốt: quyền riêng · sửa lỗi ghi tồn ERP · thêm tay áp luật khớp kế toán như Import · mở rộng PhysicalStockWriter (không ảnh hưởng luồng cũ)

## Phase 1 — BE (xong 20/10)

- [x] Quyền `Khai báo tồn kho đầu kỳ` (type 21, group "Tồn kho đầu kỳ") cuối `PermissionsTableSeeder` — đã `permission:sync` local (id 101163)
- [x] `PhysicalStockWriter`: THÊM `importBeginning` / `adjustBeginning` / `removeBeginning` (+ helper riêng). 3 hàm cũ không đổi 1 dòng (diff chỉ có dòng thêm)
- [x] `Modules/Finance/Services/BeginningStock/BeginningStockService.php`: danh sách + phạm vi, cờ "đã giao dịch" theo lô cả trang, form/product-infos, thêm, sửa nhóm, xoá nhóm, import (gom nhóm), export-rows
- [x] `BeginningStockController` + route `finance/beginning-stocks` (checkPermission, import tối đa 200 dòng)
- [x] `ExportColumnRegistry::COLUMNS['beginning_stocks']`

## Phase 2 — FE (xong 20/10)

- [x] `pages/warehouse/beginning-stocks/index.vue` (V2 list, lọc, Import, Xuất Excel FE, Cấu hình cột, Sửa/Xoá theo cờ BE)
- [x] `create.vue` + `components/BeginningStockForm.vue` (Công ty / Kho, popup chọn hàng dùng chung, bảng hàng × vị trí, popup vị trí của Phiếu nhập kho, Lưu / Lưu và tiếp tục)
- [x] `components/EditGroupModal.vue` (sửa SL cả nhóm, tổng = SL kế toán)
- [x] Menu `warehouse.js` mục "Khai báo tồn kho đầu kỳ" có link + isShow quyền

## Phase 3 — Kiểm (xong 20/10)

- [x] Script HTTP kernel có rollback: 403 khi chưa quyền, phạm vi công ty, thêm (chia 2 vị trí) / sửa / xoá — 8 bảng tồn khớp, xoá về đúng như trước; chặn lệch kế toán, trùng vị trí, khai trùng, công ty ngoài phạm vi, hàng đã giao dịch, 404 dòng công ty khác; import 207 bỏ dòng lỗi
- [x] Playwright bấm thật: danh sách, form Thêm (báo đỏ lệch, Thêm vị trí tự điền phần còn lại, chọn vị trí), Lưu, popup Sửa (báo lệch, lưu), Xoá, Import (validate / bỏ dòng lỗi / import), Xuất Excel (đọc file)
- [x] Popup chọn hàng (`product-picker`) — bấm thật sau khi gop_db local chạy đủ migration nhánh (20/10): chọn hàng chưa khai vào form, hàng đã khai bị chặn
- [x] PHPUnit `Modules/Finance/Tests/Feature/BeginningStockApiTest.php` 15/15 (sau migrate); Finance/MasterData còn 6 ca đỏ không liên quan

## Checkpoint — 2026-10-20

- **Vừa hoàn thành:** đủ BE + FE + kiểm + test; đã commit local (chưa push). DB local về đúng mốc (10.357 tồn đầu, 10.098 kế toán), quyền tạm đã gỡ.
- **Bước tiếp theo:** push; deploy chạy `PermissionsTableSeeder`; admin gán quyền vào vai trò.
- **Còn ngỏ:** ERP vẫn cho khai tay không kiểm khớp kế toán (không đụng ERP).
