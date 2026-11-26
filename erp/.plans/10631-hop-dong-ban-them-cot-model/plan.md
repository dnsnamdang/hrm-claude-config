# #10631 — Plan: Hợp đồng bán thêm cột Model

Design: `design.md`. Small change — 3 file (1 BE + 2 FE). Branch `develop_02`.
Vị trí cột chuẩn: **Tên hàng → Model → Mã hàng**, bind `<% product.model_name %>`.

## Tasks
- [x] **T1 (BE):** `FirmContractAnnexService::getDataForAnnex()` dòng 94-97 — thêm `'fctp.model_name'`, `'fctp.model_id'` vào SELECT. `php -l` sạch.
- [x] **T2 (FE — PL giảm Xem):** `sale/firm/annexes/show.blade.php` — thêm `<th rowspan="2">Model</th>` (giữa :169 Tên hàng / :170 Mã hàng) + `<td><% product.model_name || '' %></td>` (giữa :193/:194).
- [x] **T3 (FE — ĐHNT):** `sale/firm/orders/form.blade.php` tab Hàng hóa — thêm `<th rowspan="2">Model</th>` sau "Tên hàng" (:299) + `<td><% product.model_name %></td>` sau ô product_name (:319).

## Verify (Playwright trên ERP :8001, DB test, tài khoản thật)
- [x] màn **tạo** PL giảm (HĐ 29984) → thêm hàng qua picker → cột Model có data: GSAQ, INOX400. Vị trí STT·Ảnh·Tên hàng·**Model**·Mã hàng. Grid rỗng lúc đầu là ĐÚNG thiết kế (hàng chỉ vào qua `addProduct`).
- [x] màn **xem** PL giảm (annex 29867) → Model hiện + data "XECMANG9PCS" (Tên hàng·Model·Mã hàng).
- [x] ĐHNT màn **xem** (29949) tab Hàng hóa → Model hiện + data "CI4/SL 15W40 5L".
- [x] HĐ bán (29984) spot-check → Model 3 dòng (GSAQ/INOX400/INOX300), không hồi quy.

## Checkpoint
2026-11-26: **CODE XONG + VERIFY XONG trên dev.** 3 file (1 BE + 2 FE), `php -l` sạch, `git diff --stat` = 5+/1−.
- Gốc 0-dòng grid từng nghi: `getDataForAnnex()` trả **mảng** (`->toArray()`), không phải object — BE thực tế trả đủ model_name/model_id (tinker HĐ 29984 = 3 hàng, HĐ 2 = 16 hàng, tất cả có model_name). FE `annexes/form.blade.php` đã có sẵn cột Model (166/206) từ NHÓM 1, bind `form.products`; hàng vào qua `addProduct` lấy từ `_parent_contract.final_products` → `BaseChildClass` copy mọi key (gồm model_name) → render.
- Ảnh: scratchpad `.playwright-mcp/10631-{tao,xem}-plgiam-model-col.png`, `10631-dhnt-hanghoa-model-col.png`.
- ✓ PUSH develop_02 `5b20012bc5` (2026-11-26). CHƯA gop_db.

### Checkpoint — 2026-11-26 (wrap up cuối ngày)
Vừa hoàn thành: code + verify Playwright 4/4 màn; push ERP develop_02 `5b20012bc5`; Redmine đã chuyển "Đang tiến hành" khi nhận vé.
Đang làm dở: (không)
Bước tiếp theo: gop_db khi user yêu cầu; cập nhật Redmine sang "Code xong chờ test" nếu chưa.
Blocked: (không) — CHƯA gop_db.
