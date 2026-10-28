# Plan Phase 5 — Gỡ màn Lĩnh vực + Nhóm hàng hoá ở ERP (giữ bảng) — 13/10/2026

> Nguồn: `khao-sat.md`. ⏳ CHƯA được "làm". ERP `wt-erp-2d1`, nhánh `feat/p5-go-man-scope-group` từ `feat/2d1-erp-khong-loi`. ⛔ Không merge vào gop_db.

## Task ERP
- [x] P1 `routes/web.php`: 11 route `groups` (trừ `groups.searchData`) + 5 route `scope.*` gắn `productMovedToHrm:stopped-generic` (GET ⇒ trang "Chức năng đã ngừng sử dụng.", POST/PUT ⇒ 403 JSON như C-b).
- [x] P2 Menu: bỏ link "Danh mục nhóm hàng hoá" (`topmenubar:27`, `sidebar:59`) + "Danh mục lĩnh vực" (`topmenubar:40`); `topmenubar_old` cùng 2 link (kiểm còn include ở đâu).
- [x] P3 Test: `ProductMovedToHrmRoutesTest` thêm 16 route vào danh sách chặn, `groups.searchData` vào danh sách trắng; cả bộ ERP.

## Kiểm (Playwright ERP 8090, role tạm gỡ khi xong)
- Menu không còn 2 link; GET `/admin/groups`, `/admin/groups/create`, màn Lĩnh vực ⇒ trang ngừng; POST store ⇒ 403; select2 Nhóm ở màn Dịch vụ / Lỗi thiết bị vẫn tải `groups.searchData` 200; console sạch.

## Phạm vi xin "làm"
| | |
|---|---|
| Repo / nhánh | ERP `wt-erp-2d1`, nhánh `feat/p5-go-man-scope-group`; merge LOCAL, push khi user báo; ⛔ không vào gop_db |
| File | `routes/web.php`, `layouts/topmenubar.blade.php`, `layouts/sidebar.blade.php`, (`topmenubar_old.blade.php`), `tests/Feature/ProductMovedToHrmRoutesTest.php` |
| DB | không ghi (role tạm Playwright). Không migration / seeder / quyền |

### Kết quả — 2026-10-13
- ERP `feat/p5-go-man-scope-group` ⇒ merge LOCAL `3aaae676fe` vào `feat/2d1-erp-khong-loi` (CHƯA push; không nằm trong gop_db). `topmenubar_old` không còn được include ⇒ không sửa.
- PHPUnit ERP 108/108 (`ProductMovedToHrmRoutesTest` 233 route chặn, `groups.searchData` trắng).
- Playwright ERP 8090 (role tạm `P5_UAT_TMP` 118814 — đã gỡ; roles 130 · rhp 20.958 · ehr 1.718 về mốc): `/admin/groups`, `/create`, `/{id}/edit`, `/admin/sale/scopes` ⇒ 403 trang "Chức năng đã ngừng sử dụng"; POST `/admin/groups` + `/admin/sale/scopes` ⇒ 403 JSON đúng câu, DB không có bản ghi thử; `groups.searchData` 200 (5 dòng); menu: khối "Quản lý catalog" còn "Danh mục chương", không còn "Danh mục nhóm hàng hóa" / "Danh mục lĩnh vực" / sidebar "Nhóm hàng hóa"; console không lỗi JS mới. Server tắt đúng PID.

### Checkpoint — 2026-10-13 (Phase 5 xong)
Vừa hoàn thành: P1–P3 + kiểm.
Đang làm dở: không.
Bước tiếp theo: user cho push ERP · khảo sát phase A7 tiếp theo (3 / 4 / 2c).
Blocked: —
