# Plan đợt C-f — dữ liệu / runbook (N65 + N26) — 13/10/2026

> Nguồn: `cf-khao-sat.md` + Q-N65 / Q-N26 (đã chốt 13/10). ⏳ CHƯA được "làm".
> ERP worktree `wt-erp-2d1` — nhánh con `feat/cf-don-gia-hieu-luc` từ `feat/2d1-erp-khong-loi`. ⛔ Không merge vào gop_db.

## Task ERP
- [x] F1 Lệnh `price:cleanup-stale {--dry-run} {--today=}` (`app/Console/Commands/CleanupStalePricesCommand.php`, đăng ký Kernel, KHÔNG lên lịch):
  - (a) `product_expected_prices` status 2 + `effect_date < hôm nay` ⇒ `status = 3` (đóng, không áp); (b) cờ chờ duyệt mồ côi ở
    `product_unit_prices` / `product_company_units` / `product_units` (không còn `product_approve_prices` ↔ `product_approves` đang chờ) ⇒ cờ 0 +
    số đề nghị = số đang chạy.
  - Trước khi ghi: sao lưu CSV các dòng sẽ đổi (`storage/app/price-cleanup/<ts>/`); luôn xuất `gia-qua-han-2026.csv` (dòng năm hiện tại cho
    nghiệp vụ soát) + in tổng số theo nhóm. 1 transaction; chạy lại ⇒ 0.
  - `ProductExpectedPrice::STATUS_PENDING = 2`, `STATUS_APPLIED = 1`, `STATUS_EXPIRED = 3` (hằng mới, chú thích).
- [x] F2 Cron `product:update_price`: `effect_date <= ngày`, `orderBy(effect_date, id)`; `catch (\Throwable)` + rollBack (đang là `Exception`
  chưa import ⇒ không bắt được).
- [x] F3 PHPUnit (sqlite): dọn (quá hạn ⇒ 3, tương lai / hôm nay giữ; flag 1 quá hạn cũng đóng; cờ mồ côi xoá, cờ có yêu cầu chờ GIỮ; dry-run
  không ghi; chạy 2 lần ⇒ lần 2 = 0; file sao lưu + file 2026 có đủ dòng); cron áp cả ngày đã lỡ, mốc mới nhất thắng.

## Runbook (tài liệu, không phải source)
- [x] R1 `gia-theo-cong-ty/runbook-trien-khai.md` thêm **Phần 4 — Dữ liệu cũ ERP**: (1) N26 kiểm `MAX(product_histories.product_version_id)`
  vs `AUTO_INCREMENT` của `product_versions` ⇒ nếu AI ≤ max thì `ALTER TABLE product_versions AUTO_INCREMENT = max+1`; (2) N65 chạy
  `price:cleanup-stale --dry-run` ⇒ gửi `gia-qua-han-2026.csv` cho nghiệp vụ ⇒ chạy thật ⇒ chạy lại kiểm = 0; (3) xác nhận cron 01:00 bản mới.

## Kiểm
- Chạy thật trên BẢN SAO DB tạm (`hrm_erp_cf_tmp` dựng từ giacty 3 bảng giá + 2 bảng duyệt) — dry-run ⇒ số khớp 13.915 / 2.067 / 17;
  chạy thật ⇒ lần 2 = 0; cron `--date` hôm nay trên bản sao. Xong DROP bản sao. KHÔNG ghi giacty.
- PHPUnit ERP cả bộ.

## Phạm vi xin "làm"
| | |
|---|---|
| Repo / nhánh | ERP `wt-erp-2d1`, nhánh `feat/cf-don-gia-hieu-luc` từ `feat/2d1-erp-khong-loi`; merge LOCAL, push khi user báo; ⛔ không vào gop_db |
| File | `app/Console/Commands/CleanupStalePricesCommand.php` (mới), `UpdateProductPrice.php`, `app/Console/Kernel.php` (đăng ký lệnh), `app/Model/Product/ProductExpectedPrice.php` (hằng), test mới; runbook (tài liệu) |
| DB | giacty CHỈ ĐỌC; tạo + DROP 1 DB bản sao tạm `hrm_erp_cf_tmp` để chạy thử lệnh dọn. Không migration / seeder / quyền |

### Kết quả thực hiện — 2026-10-13
- ERP `feat/cf-don-gia-hieu-luc` ⇒ merge LOCAL vào `feat/2d1-erp-khong-loi` (CHƯA push; không nằm trong gop_db). Không cần sửa Kernel (lệnh tự nạp qua `load(Commands)`).
- **Thêm ngoài plan — chốt chặn trong cron**: đo giacty CHƯA dọn ⇒ cron mới `<=` sẽ áp **13.909** giá cũ (có giá 1,00 đ). Cron giờ dừng hẳn (exit 1, log "chạy price:cleanup-stale trước") khi còn dòng chờ quá 30 ngày (giacty: 13.468). Runbook Phần 4 ghi thứ tự bắt buộc.
- Chạy thật trên bản sao `hrm_erp_cf_tmp` (13 bảng chép từ giacty, đã DROP): dry-run 13.915 / 2.067 / 5·6·6 ⇒ thật (sao lưu đủ 4 file + `gia-qua-han-2026.csv` 2.067 dòng) ⇒ dry-run lại 0; cron trên bản sao "không có thay đổi giá"; giacty không ghi (status 2 vẫn 21.993).
- PHPUnit `CfCleanupStalePricesTest` 5 ca + ERP **108/108**; khai lệnh mới vào `tests/fixtures/price-readers.txt` (G3 whitelist).
- Runbook: `gia-theo-cong-ty/runbook-trien-khai.md` **Phần 4** (N26 SQL kiểm/chỉnh AUTO_INCREMENT, N65 các lệnh + lui + nhật ký chạy thử).

### Checkpoint — 2026-10-13 (C-f xong)
Vừa hoàn thành: F1–F3 + R1 + chạy thử trên bản sao.
Đang làm dở: không. DB bản sao đã DROP, file xuất thử đã xoá.
Bước tiếp theo: user cho push ERP · rồi A7 (phase 2c/3/4/5 thuộc lần prod này).
Blocked: —
