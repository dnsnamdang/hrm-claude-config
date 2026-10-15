# Plan T7 — Chặn ERP luồng tính giá + nghiệm thu tổng + chạy thử runbook — 12/10/2026

> Nguồn: `design.md` §10, §11, §12 · `ton.md` Q18, D12 · `khao-sat-be-erp.md` §1, mục "Nơi đọc" · khuôn G6 (`gia-theo-cong-ty/g6-plan.md`,
> ERP commit `02568c4fc8`) · runbook `gia-theo-cong-ty/runbook-trien-khai.md` (nhật ký thử 10/10).
> ✅ **User cho "LÀM" 12/10/2026** — đúng phạm vi mục 5.
> Môi trường: ERP worktree `wt-erp-2d1` nhánh `feat/2d1-erp-khong-loi` (sạch, khớp origin; `.env` trỏ `hrm_erp_giacty`, `HRM_URL_FE=http://127.0.0.1:3031`) ·
> HRM worktree `wt-chuyen-doi-hang-hoa` nhánh chung `feat/chuyen-doi-hang-hoa` (api `1e194fe5c`, client `58965aa63`).

## 0. Hiện trạng (đo 12/10)

| Mục | Đo được |
|---|---|
| Middleware | `app/Http/Middleware/ProductMovedToHrm.php` có 9 đích (`product-*`, `manufacturers`, `brands`, `price-edit`, `price-approve`, `stopped`); đích `{id}` thiếu id ⇒ `FALLBACK_PATH`. Trang báo `errors/moved_to_hrm.blade.php` có 2 câu mô tả (luồng giá / thông tin hàng). Đang gắn **66 route** (test `ProductMovedToHrmRoutesTest` + `G6PriceRoutesMovedToHrmTest`) |
| Route 4 chứng từ | `routes/web.php:2246-2295`: YCHG **15** · YCTG **11** · PTG **9** · KQ **4** = **39**, + `product.getDataForPriceAsking` (`:600`) = **40**. ⚠️ design §10 ghi "41" — đếm lại theo `name(...)` chỉ ra 40 (dòng `:524` là route đã comment). Chưa route nào gắn `productMovedToHrm` |
| Menu `topmenubar` | 5 link `route(...)`: `:327` YCHG · `:931` PTG (`?type=all`) · `:1534` YCHG · `:1536` YCTG · `:2383` YCHG chờ duyệt (`?type=approve`). Dòng `:1537` đã comment |
| Dashboard | `HomeController.php:1394-1443` — 3 thẻ: "Yêu cầu hỏi giá chờ duyệt" (PTKD), "Yêu cầu hỏi giá cần XNK duyệt", "Yêu cầu tính giá chờ duyệt" (KTMH) |
| Audit | `ProductWriteAuditObserver::WHITELIST_ROUTES` còn `'PriceCalculate.*'` (`:31`) |
| Thông báo ERP | 9 điểm `route('Price…show', …, false)` trong `PriceAskingRequest.php` / `PriceCalculateRequest.php` — chỉ chạy từ route sẽ bị chặn ⇒ không sinh thông báo mới. Thông báo CŨ trong DB trỏ `/admin/orders/price_*/{id}/show` ⇒ đi vào trang báo có link HRM đúng phiếu (xem E3) |
| Nơi đọc khác | `Product::checkPriceAsked()`, 3 controller `getDataForPriceAsking` không có route, class JS `partials/classes/order/Price*` chỉ dùng ở view bị chặn ⇒ để nguyên (design §10) |
| KQ → YCHG | `price_calculate_results` có sẵn `price_asking_request_id`, `price_calculate_request_id` (đủ 3.119/3.119 dòng có `price_calculate_id`); `price_calculate_requests.group_id` ⇒ dựng được link nhóm |
| Đích HRM | YCHG `/sale/price-asking-requests[/{id}]` · YCTG `/sale/price-calculate-requests[/{id}]` · PTG `/finance/price-calculates[/{id}]` · KQ = YCHG `?group={g}&show_result=1` (khớp link thông báo T5) |
| Đĩa | còn 48 GB (bản sao cần ≈ 11 GB) |

## 1. Tự chốt (theo design / khuôn G6 — ghi để duyệt)

| # | Chốt |
|---|---|
| E1 | Thêm 4 nhóm đích vào `TARGETS`: `asking-list/asking-show`, `calc-request-list/calc-request-show`, `calc-list/calc-show`, `calc-result` (đặc biệt — xem E3). Tham số middleware là khoá đích, gắn THEO TỪNG ROUTE như G6, giữ tên route |
| E2 | Ánh xạ route ⇒ đích: `index`, `create`, `store`, `searchData` ⇒ danh sách HRM; mọi route có `{id}` (`show/edit/delete/print/update/approve…/getDataFor…`) ⇒ trang chi tiết HRM của đúng phiếu. `product.getDataForPriceAsking` ⇒ danh sách YCHG (chỉ AJAX ⇒ JSON 403). Bỏ query `?type=` (HRM tự lọc theo quyền) |
| E3 | KQ `{id}` ⇒ middleware tra `price_calculate_results` (1 truy vấn) lấy YCHG + nhóm ⇒ `/sale/price-asking-requests/{ychg}?group={g}&show_result=1`; không tra được ⇒ danh sách YCHG. KQ `index/searchData` ⇒ danh sách YCHG (KQ không có màn riêng — Q20) |
| E4 | Trang báo: thêm câu mô tả thứ 3 cho luồng tính giá ("Hỏi giá, yêu cầu tính giá, phiếu tính giá nay được quản lý trên HRM theo từng công ty."). Không đổi khuôn trang |
| E5 | Menu 5 link ⇒ HRM như G6: `rtrim(config('app.hrm_url_FE'), '/') . '/…'`, `target="_blank" rel="noopener"`, nhãn thêm "(HRM)"; giữ nguyên `@if` quyền bao quanh. `:2383` (chờ duyệt) ⇒ danh sách YCHG HRM |
| E6 | Bỏ 3 thẻ dashboard (D12) — xoá 3 khối `if` ở `HomeController`; import model không còn dùng thì gỡ |
| E7 | Gỡ `'PriceCalculate.*'` khỏi whitelist audit. Cron `product:update_price` giữ nguyên |
| E8 | Không xoá route / controller / view / model ERP (design §10 — xoá route là vỡ `route()` ở mọi trang). Không sửa `Product::checkPriceAsked()` |
| E9 | Test ERP: file mới `Tests\Feature\PriceFlowRoutesMovedToHrmTest` khuôn G6 (không DB cho đích tĩnh; KQ cần DB đọc — dùng phiếu có sẵn trên `hrm_erp_giacty`, chỉ đọc). Cập nhật `ProductMovedToHrmRoutesTest` (đếm route chặn 66 ⇒ 106). Chạy cả bộ ERP liên quan 2-D1 + G3 + G6 |

## 2. Nghiệm thu tổng (Phase 7)

| # | Hạng mục | Cách | Ghi chú |
|---|---|---|---|
| N1 | PHPUnit HRM | `MasterData` toàn bộ (đang 397) + whitelist đọc giá | không DB ghi thật |
| N2 | PHPUnit ERP | bộ chặn route (E9) + G3 + 2-D1 | |
| N3 | Playwright MCP trên ERP | đăng nhập ERP local: 5 link menu mở HRM đúng màn (đo `href`, `target`); trang chủ không còn 3 thẻ (đếm DOM); gõ thẳng 4 loại URL cũ (list / show YCHG · YCTG · PTG · KQ) ⇒ 403 + đúng 1 link HRM đúng phiếu; POST ⇒ JSON 403 | cần ERP chạy local — `config:clear` trước (memory cache trỏ production) |
| N4 | e2e HRM toàn Phase 7 | T1 chính sách giá · T3 YCHG · T4 YCTG · T5 PTG + G4/G5 giá | **CHỈ chạy khi user bảo** (`--no-deps --workers=1`, cổng 3031/8031) |
| N5 | Soát chéo | `git grep` marker xung đột cả 3 repo; `uniq -d` id quyền seeder; route HRM mới đều có gate | |

## 3. Chạy thử runbook trên bản sao tạm (§11)

1. Viết §11 vào `gia-theo-cong-ty/runbook-trien-khai.md` thành mục riêng "Luồng tính giá" (thứ tự chạy SAU bước M3 của giá theo công ty): SQL kiểm 30 phiếu chéo công ty (D1), kiểm trùng trước UNIQUE, migrate 12 file `2026_10_11_*`, seeder `InternalPricePolicyPermissionSeeder` + `PriceCalculationPermissionSeeder` (KHÔNG PermissionsTableSeeder), `price-asking:backfill-groups --dry-run` ⇒ thật ⇒ lại (0), `price-asking:close-stale --before=2026-06-01`, deploy ERP chặn, gán quyền, nhắc 5 công ty chưa có phân công XNK.
2. Bản sao: `mysqldump --single-transaction … <nguồn> | mysql hrm_erp_runbook7` (≈ 12,5 phút) — nguồn `hrm_erp` (T7-Q1 = A); trên bản sao `migrate:rollback --step=2` (M1/M2 giá công ty) như lần 10/10.
3. Chạy trọn runbook (giá theo công ty + luồng tính giá) bằng code nhánh chung, trỏ DB bản sao qua biến môi trường trên từng lệnh (`DB_DATABASE=hrm_erp_runbook7 php artisan …`) — KHÔNG sửa `.env`.
4. Ghi nhật ký thời gian + số dòng từng bước như lần 10/10; so số với dry-run.
5. `DROP DATABASE hrm_erp_runbook7`; kiểm DB nguồn không đổi (batch max, số dòng bảng luồng giá).

## 4. Tồn — hỏi lần lượt

| # | Câu | Đề xuất | Chốt |
|---|---|---|---|
| T7-Q1 | Bản sao tạm lấy từ DB nào? (A) `hrm_erp` — gần production nhất, chưa có migration Phase 7, có sẵn M1/M2 giá công ty nên phải `rollback --step=2` như 10/10 rồi chạy trọn 2 runbook; (B) `hrm_erp_giacty` — đã chạy hết T1–T6, chỉ thử được lệnh idempotent, không thử được migrate thật | A | ✅ 12/10 user: **A — bản sao từ `hrm_erp`**, lùi M1/M2 rồi chạy trọn 2 runbook |
| T7-Q2 | Menu `:931` "Phiếu tính giá hàng hoá" nằm trong khối Kế toán cạnh "Cập nhật giá bán (HRM)" — giữ link (trỏ HRM) hay bỏ hẳn? Các link YCHG / YCTG cũng vậy | Giữ, trỏ HRM (nhất quán G6, người quen đường cũ vẫn tìm thấy) | ✅ 12/10 user ("tiếp đi" — theo đề xuất): **A — giữ 5 link, trỏ HRM** (tab mới, nhãn "(HRM)", giữ `@if` quyền) |
| T7-Q3 | Nghiệm thu N4 (e2e) chạy trong T7 không? | Có — 1 lượt cuối sau khi chặn ERP, khi user bảo | ✅ 12/10 user: **A — chạy e2e** (chạy ngay 12/10, trước khi code T7) |

## 5. Phạm vi sẽ xin "làm"

| | |
|---|---|
| Repo / nhánh | **ERP** `wt-erp-2d1`: nhánh con `feat/t7-chan-erp-tinh-gia` từ `feat/2d1-erp-khong-loi`; merge LOCAL, không push |
| File ERP | `app/Http/Middleware/ProductMovedToHrm.php` · `resources/views/errors/moved_to_hrm.blade.php` · `routes/web.php` (40 route, chỉ thêm `->middleware(...)`) · `resources/views/layouts/topmenubar.blade.php` (5 link) · `app/Http/Controllers/HomeController.php` (bỏ 3 thẻ) · `app/Observers/ProductWriteAuditObserver.php` · `tests/Feature/PriceFlowRoutesMovedToHrmTest.php` (mới) + `ProductMovedToHrmRoutesTest.php` |
| HRM | Không sửa source. Chỉ `.plans/` (runbook) |
| DB | `hrm_erp_giacty`: chỉ ĐỌC (test KQ, Playwright). Tạo `hrm_erp_runbook7` (bản sao) ⇒ chạy migrate + seeder + backfill TRÊN BẢN SAO ⇒ DROP. Không ghi `hrm_erp` / `hrm_erp_giacty` |
| Không đụng | `gop_db`; `report_templates`; xoá route/controller/view ERP; cron ERP |

## 6. Kết quả e2e N4 (12/10 — user "chạy e2e", chạy TRƯỚC khi code T7)

- Lượt 1 (4 spec: `sale/internal-price-policy` · `sale/price-asking-request` · `sale/price-calculate-request` · `finance/price-calculate`, `--no-deps --workers=1`, 3031/8031):
  17 passed · 1 flaky · 2 failed · 8 did not run · **24,8 phút**. 2 ca đỏ đều là quá giờ (`beforeAll` 30s / 180s, trang chỉ có vòng tải — snapshot `status + img`),
  log API thưa request 07:44 → 07:57 → 08:16, load average máy **36,9** (tiến trình khác trên máy) ⇒ môi trường, không phải lỗi code.
- Lượt 2 (2 spec đỏ, máy đã hạ tải): **12/12 passed (1,3 phút)**.
- Tổng: T1 9/9 + T5 7/7 (lượt 1) + T3 + T4 12/12 (lượt 2) = **28/28 xanh**. afterAll dọn sạch (0 phiếu / 0 phân công tạo sau 07:00 trên `hrm_erp_giacty`).
- Không có spec riêng G4/G5 (đã ghi T5) — phần duyệt giá G5 nằm trong `finance/price-calculate` P5.

## 7. Kết quả code (12/10 — user "làm")

- ERP nhánh `feat/t7-chan-erp-tinh-gia` commit **`d90b7b3e6f`** ⇒ merge LOCAL `feat/2d1-erp-khong-loi` **`443c812553`** (chưa push; +2 so với origin).
  - Middleware 7 đích mới; đích `{id}` thiếu/sai id lùi về danh sách CÙNG chứng từ (không về danh sách hàng hoá); KQ tra `price_calculate_results`
    ⇒ `/sale/price-asking-requests/{ychg}?group={g}&show_result=1` (YCTG chưa gom nhóm ⇒ YCHG không kèm nhóm; KQ thiếu YCHG ⇒ danh sách YCHG).
  - 40 route gắn `productMovedToHrm` (đứng trước `checkPermission` cấp route). Menu 5 link ⇒ HRM. Dashboard bỏ 3 thẻ (gỡ 2 import thừa). Audit gỡ `PriceCalculate.*`.
  - Test: `PriceFlowRoutesMovedToHrmTest` mới (7 ca, KQ dựng 2 bảng trên sqlite :memory:); `ProductMovedToHrmRoutesTest` 66 ⇒ 106;
    `G6PriceRoutesMovedToHrmTest` bỏ ràng buộc "PTG không bị chặn" + `getDataForPriceAsking` khỏi danh sách giữ; `ProductBarcodeAndAuditTest` PTG không còn trắng.
  - PHPUnit ERP **69 ca: 68 xanh + `ExampleTest` đỏ sẵn (N45)**.
- N3 Playwright (script Node, ERP 8090 trên `hrm_erp_giacty`, tài khoản `TEST_EMAIL` e2e — chỉ đọc, không role tạm):
  - 9/9 URL cũ (list · `?type=approve` · show YCHG / YCTG / PTG · KQ show · KQ list) ⇒ **403**, title "Chức năng đã chuyển sang HRM", câu mô tả luồng tính giá,
    **đúng 1** link HRM `_blank` đúng đích (KQ 3120 ⇒ `/sale/price-asking-requests/4283?group=4056&show_result=1`).
  - 3 POST (store / approve / PTG update, kèm `X-Request-ID`) + 2 AJAX GET ⇒ **403 JSON** `redirect_url` đúng phiếu — controller không chạy.
    (Thiếu `X-Request-ID` thì `PreventDuplicateSubmission` chặn trước với "Missing Request ID" — middleware có sẵn, không liên quan.)
  - Trang chủ: 0 thẻ trong 3 thẻ đã bỏ; menu **0 link cũ** `/admin/orders/price_*`; 3 link mới hiện (`_blank`, `noopener`, nhãn "(HRM)"):
    Phiếu Yêu cầu hỏi giá · Phiếu tính giá hàng hóa · Phiếu yêu cầu tính giá. 2 link sau quyền "Tổng hợp đặt hàng" (`:1534`, `:2383`) tài khoản đo
    không có quyền ⇒ chỉ kiểm bằng nội dung file (test `test_khong_con_loi_vao_luong_tinh_gia_erp`: 3 link `/sale/price-asking-requests`), không cấp role tạm (phạm vi chỉ đọc DB).
  - Server 8090 đã tắt đúng tác vụ.

## 8. Chạy thử runbook (12/10) — ĐẠT

- Bản sao `hrm_erp` ⇒ `hrm_erp_runbook7` (505 s, 1.869 bảng); lùi M1/M2; chạy trọn phần 1 (giá theo công ty) + phần 2 (luồng tính giá) bằng code nhánh chung,
  trỏ DB qua biến môi trường từng lệnh (không sửa `.env`). Mọi điểm dừng đạt: backfill giá 1.042.374 = dry-run, compare **0 lệch**, M3 đạt;
  12 migration Phase 7 đạt; seed 1656/1657/1658/1662–1664 idempotent; backfill nhóm 4.029 (= T2), chạy lại 0; close-stale 45 ⇒ chạy lại 0; `migrate:status` 0 chờ.
- Kiểm 9.1 trên dữ liệu local: phiếu chéo công ty còn dở **30** ⇒ production phải dọn về 0 ở ERP trước (D1).
- `DROP DATABASE hrm_erp_runbook7`; `hrm_erp` gốc không đổi.
- Runbook ghi vào `gia-theo-cong-ty/runbook-trien-khai.md` **Phần 2** (mục 8–9 + nhật ký).

## 9. Soát chéo N5 (12/10)

- Marker xung đột: hrm-api / hrm-client / ERP worktree **0**.
- Id quyền: `PermissionsTableSeeder` (bỏ dòng comment) 0 id trùng, trên cả nhánh feature lẫn `origin/gop_db` (ref 10/10, chưa fetch).
  Id feature 1652–1658, 1662–1664, 1670–1675 không đụng id `gop_db` (1660/1661 là cùng quyền có sẵn từ gop_db; gop_db dùng 1676–1698).
  ⚠️ Kiểm lại sau khi fetch `gop_db` mới nhất lúc merge prod.
- Gate route HRM mới: đã phủ ở PHPUnit T1–T6 (ca 403 không quyền); không kiểm lại.

### Checkpoint — 2026-10-12 (T7)
Vừa hoàn thành: T7 — ERP chặn luồng tính giá (merge LOCAL `443c812553`, PHPUnit 68 + 1 đỏ sẵn), Playwright ERP đạt, chạy thử runbook 2 phần đạt + DROP, soát chéo.
**PHASE 7 XONG (local).** Chưa push ERP (+2 commit so với origin `feat/2d1-erp-khong-loi`); HRM chỉ đổi `.plans/`.
✅ 2 link menu sau quyền "Tổng hợp đặt hàng": user cho cấp quyền tạm trên dev local (12/10) ⇒ role tạm 110981 (quyền web 100071 @ Cty 1, gán NV e2e 1180) ⇒ DOM đủ **5/5** link HRM `_blank` `noopener` nhãn "(HRM)", 0 link cũ, 9/9 trang báo vẫn đạt; gỡ role, số dòng roles 129 / rhp 18.418 / ehr 1.720 = trước.
✅ ĐÃ PUSH ERP `origin/feat/2d1-erp-khong-loi` @ `443c812553` (12/10).
Bước tiếp theo: Phase 6 hàng tạm (user mở 12/10).
