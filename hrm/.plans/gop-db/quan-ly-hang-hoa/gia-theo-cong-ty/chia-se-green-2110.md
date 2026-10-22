# Chia sẻ hàng ETEK GREEN + DTTDETEK nhận hàng — 21/10/2026 (sau go-live)

Yêu cầu user 21/10: chép toàn bộ hàng ETEK GREEN (9) cho TPE (1), Sài Gòn (4), Vinh (3), Hải Phòng (2), DTTDETEK (8);
DTTDETEK (8) nhận toàn bộ hàng của 1·4·3·2·9. Làm trên bản sao prod `hrm_erp_21_10` (dump 21/10 20:25, app prod đang down).

## Câu đã chốt (21/10)
| # | Câu | Chốt |
|---|---|---|
| 1 | "Toàn bộ hàng" | Chỉ hàng **Đang KD tại công ty chủ**, đủ 6 loại giá (luật B5 cũ) |
| 2 | Cặp đã có sẵn ở công ty nhận | 572 cặp TPE "Đang nhập thông tin" (lấy về sáng 21/10, giá 0 hết) ⇒ **điền giá chủ + Đang KD**; 7 cặp "Chờ tính giá" (TPE 3, Vinh 4) ⇒ giữ nguyên |
| 3 | Hệ số | Nhân hệ số công ty nhận như B5 (chỉ 7 mã Green ở SG có hệ số 1,073–1,158) |
| 4 | 1 lần hay tự động | **1 lần** (backfill). Tự động chép về sau = feature riêng, chưa làm |
| 5 | Hàng của 8 cho đi? | Không — 8 chỉ nhận; 7 (Green cũ) không tham gia |

## Luật (config `price.price_copy_receivers`)
9 ⇒ 1·2·3·4·8 · 1·2·3·4 chép lẫn nhau + cho 8 · 8 chỉ nhận · 7 tự quản.
Công ty nhận status 1 bộ giá RỖNG (mọi giá 0, pcu 5 cột 0, không chờ duyệt, không giá dự kiến) ⇒ điền đúng dòng đang có
(giữ id) + status 3; có ô đã nhập ⇒ bỏ qua cả cặp (`recv_entering_has_data`). Trạng thái khác ⇒ bỏ qua (`recv_has_status`).

## Code (hrm-api `gop_db`, chưa commit — user cho phép sửa 21/10)
- `config/price.php` — bảng chủ ⇒ nhận thay `shared_price_company_ids`; tự quản còn `[7]`.
- `CompanyPriceBackfill` — `receiverMap()` (nhận cả nhóm kiểu cũ), B5 theo bảng, nhánh điền (`pcu.recv_fill` / `upp.recv_fill` / `pcc.recv_fill`), B0 `pcu_foreign` theo bảng.
- `CompanyPriceBackfillReport` — 3 khoá đếm mới. `BackfillCompanyPricesCommand` / `CompareCompanyPricesCommand` / `CompanyPriceComparator` đọc bảng mới.
- Test `CompanyPriceBackfillTest`: ca config mới + ca `bang_chep_2110_green_dien_bo_gia_rong_va_chep_cho_8`.

## Ghi chú ngoài phạm vi
- ERP `app/Console/Commands/PriceSnapshotCommand.php` gõ cứng `[1,2,3,4]`.
- ERP `Company::TAN_PHAT_CLUSTER` / `Employee::dataCompanyIds()` — cụm 1·2·3·4 xem chung dữ liệu hàng hoá; 8/9 chỉ xem của mình ⇒ kiểm hàng chép có hiện ở màn/picker của 8 và 9 không (sau khi chạy local).

## Trạng thái
- 21/10: sửa code + test xanh; dry-run local — số ở mục dưới. CHƯA chạy thật (hỏi riêng). Lên prod cần commit/push/deploy hrm-api (hỏi riêng).

## Test (21/10)
- `CompanyPriceBackfillTest` 14/14 xanh (367 assertion) · `ProductPriceSetWriteTest` 7/7.
- Cả bộ `Modules/MasterData` 620 ca: 3 đỏ KHÔNG liên quan — `ExpectedPriceApplyTest::chot_chan…` cần dữ liệu thật Cty 1 có giá dự kiến quá hạn >30 ngày (prod đã dọn ở go-live 8.5 ⇒ 0 dòng); `ProductReadApiTest::so_query…` (N+1, 14 vs 18 query) và `TempProductVisibilityTest::catalog_tab…` — không đụng code chép giá. Chạy cần `memory_limit=-1` (2G hết bộ nhớ ở ca ~594).
- Bẫy gặp khi dry-run: pcu "lấy về" có `sale_max_percent_coefficient` = 1.00 (mặc định cột) ⇒ lần đầu coi là "đã nhập" (572 cặp rơi vào `recv_entering_has_data`); sửa `PCU_EMPTY_VALUES`.

## Dry-run local `hrm_erp_21_10` (21/10, sau sửa)
| Công ty nhận | Cặp chép mới | Cặp điền (lấy về rỗng) | Cặp hệ số cũ ⇒ KD | Dòng giá mới | Bỏ qua |
|---|---|---|---|---|---|
| 1 TPE | 1.392 (Green) | 572 | 0 | 8.352 + 3.432 điền | 3 Chờ tính giá |
| 2 HP | 1.967 | 0 | 0 | 11.802 | — |
| 3 Vinh | 1.963 | 0 | 0 | 11.778 | 4 Chờ tính giá |
| 4 SG | 1.959 | 0 | 8 (38 dòng giá nhân hệ số) | 11.802 | — |
| 8 DTTDETEK | 30.275 (từ 1·2·3·4·9) | 0 | 0 | 184.440 (+2.540 giá dự kiến) | — |
Tổng ghi 311.361 dòng · B0 sạch · owner_not_ready 4 (chủ 1: 3, chủ 4: 1).

## Chạy thật local `hrm_erp_21_10` (21/10 ~23:08, user cho phép, phương án (a) gồm 8 dòng hệ số cũ SG)
- Ghi 311.361 dòng = dry-run (pep Cty 1 = 119: dry-run 57 chạy TRƯỚC khi sửa PCU_EMPTY_VALUES, +62 pep của 572 cặp điền). B6 đạt.
- **Không đụng dữ liệu go-live**: checksum (COUNT + SUM CRC32 + BIT_XOR MD5 từng dòng) 4 bảng pcu/upp/pep/pcc cho mọi dòng `created_at < 2026-10-21`, trừ 8 pcc SG (id 1711,2271,2272,2274,2280,2282,2285,2292) ⇒ TRƯỚC = SAU giống hệt (134.868 / 800.347 / 103.122 / 115.497 dòng). Script `scratchpad/cks.sh` — ⚠️ lần đầu lọc 8 dòng theo `status IS NULL` nên sau chạy báo lệch giả; phải trừ bằng id cố định.
- Chạy lần 2 = 0 dòng. `product-price:compare --company=8`: 30.275 cặp, lệch 1 = `ETGN-EG-SM5273` pcu.cost_price — chủ (9) sửa giá vốn ở HRM 21/10 13:46 (60tr), `product_units` cũ = 0 ⇒ chép đúng, lệnh so với cột cũ.
- ERP `dataCompanyIds()` chỉ dùng ở `getProductsAndPrices` (route đã comment, màn chuyển sang HRM) + duyệt hàng tạm ⇒ không chặn hàng chép.

## Còn lại
- Lên prod: commit + push hrm-api `gop_db` ⇒ deploy VPS `/var/www/tpe/hrm-api` ⇒ (app đang down) chạy `danh_muc_green_2110.sql` + `product-price:backfill-company --dry-run` ⇒ đối chiếu số local ⇒ checksum trước ⇒ chạy thật ⇒ checksum sau ⇒ lần 2 = 0.

## DB SẠCH để đưa lên prod: `hrm_erp_21_10_prod` (21/10 23:16–23:3x)
`hrm_erp_21_10` bị rác test (bộ phpunit MasterData chạy trên DB `.env`: 6 catalog_histories mồ côi + companies.id=1 updated_by 999) ⇒ KHÔNG dùng làm bản prod, giữ làm dev (`.env` vẫn trỏ nó).
Dựng lại từ dump 20:25 ⇒ checksum gốc trùng `hrm_erp_21_10` trước chạy ⇒ `danh_muc_green_2110.sql` (827 · 299 · 1063 · 112) ⇒ `DB_DATABASE=hrm_erp_21_10_prod php artisan product-price:backfill-company` (311.361 dòng, B6 đạt; lần 2 = 0) ⇒ checksum dòng trước 21/10 giống hệt ⇒ quét dòng mới sau lúc nạp: chỉ catalog_histories 112 · pcc 38.128 · pcu 38.601 · pep 3.018 · product_families 17 · product_types 95 · upp 231.606 (+ products.product_type_id 827, không đổi updated_at). KHÔNG chạy test/mở app trên DB này.
Bảng phụ `zz_green2110_*` (4) để lui — DROP sau nghiệm thu.

## Chạy prod 22/10
- B3 danh mục 00:05: khớp local (827 · 299 · 1063 · 112).
- B4 checksum trước 05:0x: TRÙNG dump (134.868 / 800.347 / 103.122 / 115.497) ⇒ cron 01:00 `product-price:apply-expected` KHÔNG chạy (app `artisan down` ⇒ scheduler bỏ qua, không có evenInMaintenanceMode).
- ~~Việc treo `SOLA-TP-BC26K`~~ — KHÔNG phải việc treo (soát lại 05:07): chủ là Cty 1 (giá 1 / 0, đã chép cho 2·3·4 từ go-live); 2 giá dự kiến 1 đ ngày 22/10 là của CHÍNH Sài Gòn (công ty nhận) ⇒ không dính lệnh chép; Cty 8 nhận đúng giá chủ. Cron áp cho SG khi app mở lại.
- B5 dry-run prod 05:0x: khớp từng ô bản thử (311.361 · pep 3.018).
- B6 prod: chạy thật 311.361 dòng, B6 đạt; lần 2 = 0. B7: checksum dòng trước 21/10 GIỐNG HỆT · 0 cặp Đang KD thiếu info_entered_at · DTTDETEK 30.275 cặp Đang KD (user xác nhận "đúng kỳ vọng").
- Còn: mở app (B8); DROP 4 bảng `zz_green2110_*` sau nghiệm thu; local còn DB nháp `hrm_erp_21_10_prod`, `hrm_erp_21_10_kiem` (xoá khi user cho phép).
- 22/10 user chốt "hàng xoá": KHÔNG xử lý. Hàng đã xoá (status 0) không chép giá (lệnh vốn bỏ qua); khi cần dùng lại ⇒ khôi phục trên phần mềm rồi đi quy trình lấy về / chia sẻ hàng hoá bình thường.
- 22/10: user chạy tay `product-price:apply-expected` trên prod ⇒ Cty 4 áp 2 giá (SOLA-TP-BC26K, hiệu lực 22/10, cron 01:00 bị bỏ qua do app bảo trì).
