# Perf — API báo cáo theo dõi thực hiện HĐ (Task 5)

Đo 10/11/2026 trên DB gộp local `erp_hrm_check` (account_details 971.949 dòng, 88.355 dòng TK 1311).
Harness: phpunit scratch gọi `MonitorContractReportService::search()` (trang 1, 30 HĐ) + từng nguồn `query()->get()`.
Lưu ý: sổ cái thật dừng ở 07/09/2026 → kỳ 10/2026 có 0 dòng (chỉ đo chi phí rỗng).

## Kết quả

| Phạm vi | Kỳ | hrm | firm | wr | search() | số dòng |
|---|---|---|---|---|---|---|
| ALL (4) | 1 tháng 10/2026 | 0.06s | 1.24s | 0.34s | **1.59s** | 0 |
| ALL (4) | 1 năm 01/11/2025–31/10/2026 | 0.97s | 16.09s | 2.78s | **20.90s** | 16.038 (firm 14.364 / wr 1.673 / hrm 1) |
| COMPANY (3) | 1 tháng | — | — | — | **1.71s** | — |
| COMPANY (3) | 1 năm | 0.87s | 15.68s | 5.02s | **17.59s** | 9.338 |
| ALL / COMPANY | chỉ `contract_code` (không kỳ) | 0.04 / 0.09s | 1.32 / 1.04s | 0.07 / 0.02s | **1.35s / 1.10s** | 1 |

→ contract_code đẩy vào id-set từng nguồn: query không kỳ còn ~1.3s (trước đó firm kỳ trống ~23s).

## Nút cổ chai: firm main query (12.7s / 1 năm ALL)

Per-query (DB::listen, ALL 1 năm): firm idsWithLedgerInPeriod 1.25s · rowIds 0.22s · **firm main 12.7s** · wr ids 0.29s · wr main 1.64s · hrm 0.92s.

Tách từng leftJoinSub của firm (lọc 16.073 rowIds):

| sub | thời gian | dòng |
|---|---|---|
| fsa latestSupportAccounting | 0.16s | 15.371 |
| fp tabProducts | 0.69s | 15.889 |
| **export** (product_export_details ⨝ product_exports type 14 ⨝ fctp) | **3.59s** | 11.004 |
| borrow / import / rc / sac / annex | 0.07–0.19s mỗi cái | |
| acc ledgerCollectedInPeriod | 1.03s | 14.364 |
| debt ledgerDebt (lũy kế toàn thời gian) | 1.15s | 14.364 |
| **rev** ledgerRevenueInPeriod | **4.11s** | 13.200 |

EXPLAIN:
- **rev**: `ad` type=ref key=`account_details_contractable_type_index` rows≈479.457 filtered 13% "Using where; Using temporary" — optimizer chọn index 1 cột contractable_type (một nửa bảng) thay cho `idx_ad_131_report(account_id, invoiceable_date_accounting, …)`.
  Thử tay: `FORCE INDEX(idx_ad_131_report)` 3.84s → **1.10s**; `FORCE INDEX(idx_contractable)` 10.1s.
- **export**: `pe` key=`product_exports_type_index` (ref const type=14) rows≈15.542 filtered 10% "Using temporary"; `ped` qua `parent_id_foreign`; `fctp1` qua `firm_contract_id_index`. Không có index (type, status, created_at) / (firm_contract_id, type) — period `whereDate(pe.created_at)` không sargable.

## Đã thử
- Đổi `applyPeriod` từ `whereDate` sang khoảng nửa mở `[start, end+1d)` (sargable): **không đổi** (rev 4.23s, export 3.71s) vì optimizer vẫn chọn index contractable_type / type → ĐÃ REVERT.
- Không thêm index/hint: kể cả FORCE INDEX cho rev (−3s) + index ghép cho export thì firm vẫn ≫ 2s (Σ sub ≈ 11s + join/group trên 16k dòng), mà FORCE INDEX là chuỗi raw dễ vỡ.

## Ghi chú (e) — HRM mv/mva
HRM 1 năm 0.87–0.97s chỉ với 1 HĐ trong kỳ → đúng là chi phí cố định quét subquery chứng từ (mv/mva) không bị khoá bởi id-set. Dưới 1s ở khối lượng hiện tại, chưa tối ưu; sẽ tăng khi HĐ HRM nhiều lên.

## Hướng đề xuất (chưa làm)
1. Đẩy rowIds vào TRONG từng sub (đã có) + FORCE INDEX(idx_ad_131_report) cho 3 sub sổ cái (rev/acc), cân nhắc index `account_details(contractable_type, account_id, invoiceable_date_accounting)`.
2. Index `product_exports(firm_contract_id, type, status, created_at)` cho export.
3. Về UX: kỳ 1 năm toàn tập đoàn nên tính bất đồng bộ (job + cache) hoặc giới hạn kỳ ≤ 3 tháng ở FE; ERP gốc cũng chạy cùng khối SQL này.

## Fix round 1 — cache tập dòng (10/11/2026)
`MonitorContractReportService::cachedRows()` — `Cache::remember` 5 phút, khoá = md5(auth id, current_company_role, mức phạm vi, bộ lọc trừ page/per_page/limit). Dùng cho cả `search()` và `exportRows()`.

ALL 1 năm (01/11/2025–31/10/2026), export 2.000 dòng/lượt, tổng 16.260 dòng phẳng (9 lượt):

| driver | lượt 1 | lượt 2 | lượt 3 | search trang 5 (cùng lọc) |
|---|---|---|---|---|
| array | 18.43s | 0.05s | 0.05s | 0.12s |
| file (driver .env local) | 18.40s | 0.12s | 0.11s | 0.19s |

→ Xuất 1 năm: ~9 × 20s ≈ 3 phút còn ~18s + 8 × 0.1s. Lượt đầu vẫn chậm (nút cổ chai firm ở trên chưa đổi).
(redis local không chạy nên không đo được driver redis.)

## Fix round 2 — FORCE INDEX + thêm index (10/11/2026)

Máy local đang tải nặng (load average 5–22, Zalo/mds/session khác) nên số dao động ±30%. Mỗi cấu hình chạy 2 lượt xen kẽ trong cùng khung giờ; "trước" = code `ead87b1aa` + không có 2 index mới. 1 tháng = **07/2026** (tháng gần nhất có sổ cái, 2.110 HĐ — kỳ 10/2026 ở bảng trên có 0 dòng nên không đại diện).

### Trước → sau (search(), trang 1)

| Phạm vi | Kỳ | firm trước | firm sau | wr trước | wr sau | search() trước | search() sau |
|---|---|---|---|---|---|---|---|
| ALL (4) | 1 năm 01/11/2025–31/10/2026 | 16,3–27,5s | **8,9–9,0s** | 2,3–4,2s | 1,2–1,5s | 23,4–33,7s | **11,7–11,9s** |
| COMPANY (3) | 1 năm | 14,1–20,4s | 7,4–8,4s | 2,2–4,8s | 1,7s | 18,5–30,3s | **10,6–13,8s** |
| ALL (4) | 1 tháng 07/2026 | 6,9–9,8s | 2,5–2,9s | 1,3–2,5s | 0,6s | 7,3–12,0s | **3,2–3,5s** |
| COMPANY (3) | 1 tháng 07/2026 | 3,3–5,8s | 1,8–2,0s | 0,8–1,3s | 0,4–0,5s | 4,0–6,5s | **2,5–3,5s** |

Từng subquery firm, ALL 1 năm (15.383 HĐ, best-of-N, kết quả hash trùng trước/sau):

| sub | trước | sau | do đâu |
|---|---|---|---|
| rev ledgerRevenueInPeriod | 9,0s | 1,3–2,0s | FORCE INDEX `idx_ad_131_report` |
| export (PXK type 14) | 7,7s | 1,4–3,0s | index `idx_fctp_contract_product` |
| acc ledgerCollectedInPeriod | 2,0s | 1,1–1,3s | index `idx_ad_ctype_account_date` |
| debt ledgerDebt | 2,2s | 1,8s | index `idx_ad_ctype_account_date` |
| wr acc / debt / rev | 0,44 / 0,49 / 0,65s | 0,12 / 0,15 / 0,2s | index mới + FORCE INDEX |

### Index thêm — migration `hrm-api/database/migrations/2026_11_10_000001_add_monitor_contract_report_indexes.php`

Theo khuôn `2026_10_12_000001_add_customer_debt_report_indexes` (đã tạo `idx_ad_131_report` ở hrm-api): `ALTER TABLE … ADD INDEX …, ALGORITHM=INPLACE, LOCK=NONE`, bỏ qua nếu đã có, `down()` chỉ drop khi có.

| index | cột | lý do | dựng ở local |
|---|---|---|---|
| `firm_contract_tab_products.idx_fctp_contract_product` | (firm_contract_id, product_id) | PXK khớp dòng HĐ theo (HĐ, SP); trước chỉ có index firm_contract_id → đọc ~1,55 triệu dòng HĐ cho 36k dòng PXK (HĐ lớn tới 365 dòng) | 0,6s (105k dòng) |
| `account_details.idx_ad_ctype_account_date` | (contractable_type, account_id, invoiceable_date_accounting) | Thực thu / Phải thu–Đã thu TK 1311 theo loại HĐ; optimizer tự chọn | ~11–13s (972k dòng) |

Đã thử, KHÔNG thêm: `product_exports(type, status, firm_contract_id, created_at)` — optimizer chuyển sang quét cả `product_export_details` (88k), không nhanh hơn (1,37s → 1,56s). Nút cổ chai thật của export là join dòng HĐ, không phải `product_exports`.

### FORCE INDEX — chỉ cho subquery doanh thu (rev), firm + wr

`ContractSourceFilters::accountDetailsFrom($index, $idCount)` → `account_details as ad FORCE INDEX (idx_ad_131_report)`, dùng trong `ledgerRevenueInPeriod` (firm + wr truyền `count($rowIds)`; HĐ HRM không truyền → không ép).
- **Chỉ ép khi ≥ 1.000 HĐ**: ít HĐ (lọc mã HĐ, phạm vi hẹp) optimizer chọn `idx_contractable` nhanh hơn — đo firm rev: 1 HĐ 0,00s vs ép 1,48s · 300 HĐ 0,29s vs 1,51s · 1.000 HĐ 1,31s vs 1,62s · 1.500 HĐ 2,29s vs 1,55s · 3.000 HĐ 8,7s vs 2,0s.
- **Chỉ ép khi index có trong DB**: tra `information_schema.statistics` 1 lần / request (`RequestCache`), không có thì để optimizer tự chọn (FORCE INDEX tên không tồn tại là lỗi SQL).
- acc / debt KHÔNG ép: ép `idx_ad_131_report` không nhanh hơn (acc 2,04s = 2,04s, debt 2,2s → 2,8s; wr acc 0,44 → 2,75s).
- Ép `idx_ad_ctype_account_date` cho rev ngang `idx_ad_131_report` (firm 1,5–1,9s vs 1,3–1,7s) → giữ `idx_ad_131_report` (đã có từ 12/10, ít phụ thuộc migration mới).

### Kiểm tra
- 6 file test `MonitorContract*Test.php` pass (Api/WrSource lỗi 1 lần deadlock `INSERT permissions` do session khác chạy test cùng DB, chạy lại pass).
- Đối số HRM dump lại 07/2026 và Q2/2026: file `hrm_*.json` **trùng từng byte** với bản trước khi sửa → firm 1.774/1.796, wr 270/314 (07/2026); firm 6.127/6.229, wr 750/798 (Q2) không đổi.

### Còn lại (1 năm ALL vẫn ~12s > mục tiêu 8s)
firm main ~9s = tổng nhiều sub cỡ 1–2s (rev 1,5, debt 1,8, acc 1,2, export 1,4–3, fp 1,5) + join/GROUP BY 15k dòng; search() cộng thêm hrm ~1s (mv/mva quét cố định) + wr ~1,3s. Không còn sub nào áp đảo → index/hint thêm không gỡ được nhiều. Hướng tiếp: tính bất đồng bộ (job + cache sẵn, đã có `cachedRows()`), hoặc giới hạn kỳ ≤ 3 tháng ở FE.
