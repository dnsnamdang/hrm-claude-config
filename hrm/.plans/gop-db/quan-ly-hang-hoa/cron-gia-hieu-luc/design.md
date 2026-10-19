# Chuyển cron áp giá hiệu lực ERP ⇒ HRM (17/10/2026)

Thuộc go-live Chuyển đổi hàng hoá (lên prod cùng 1 lần — [[chuyen-doi-hang-hoa-len-prod-mot-lan]]).

## Vì sao
- Hàng hoá + giá theo công ty đã ở HRM; cron ERP `product:update_price` (01:00) ghi lịch sử vào `product_versions/product_histories`
  ERP ⇒ popup Lịch sử giá HRM (`catalog_histories`, `product_prices`) KHÔNG thấy các lần tự áp.
- ERP báo kết quả bằng file HTML `public/price_logs` + email `PRICE_EMAIL_*` + màn Nhật ký giá ERP ⇒ không theo công ty, khó dùng.

## Chốt với user (17/10)
| # | Câu | Chốt |
|---|---|---|
| C1 | Tiện dụng gồm | Lịch sử giá HRM hiện lần tự áp · thông báo chuông · màn Nhật ký áp giá trên HRM · thông báo app mobile theo công ty cho người có quyền màn "Cập nhật giá bán" (bản port màn ERP "Cập nhật nhanh giá" `products/editPrices`, quyền **"Cập nhật giá bán hàng hoá"**) |
| C2 | Vị trí màn | Màn riêng "Nhật ký áp giá" dưới "Cập nhật giá bán" (menu Tài chính) |
| C3 | Khi nào báo | Có giá áp + khi công ty bị chốt chặn; không có gì ⇒ im lặng. Mỗi công ty 1 thông báo / lần chạy |
| C4 | Chốt chặn | TÁCH THEO CÔNG TY (ERP đang toàn cục) |
| C5 | Gỡ chặn | Trên màn Nhật ký: tab "Giá quá hạn chưa áp" — Áp ngay / Đóng, không áp (từng dòng + hàng loạt) |
| C6 | Log cũ ERP | KHOÁ màn Nhật ký giá ERP (khuôn `productMovedToHrm`); tắt cron + email ERP |
| C7 | Quyền | Dùng lại: XEM = "Cập nhật giá bán hàng hoá" HOẶC "Duyệt giá bán hàng hoá" tại công ty; XỬ LÝ quá hạn = "Cập nhật giá bán hàng hoá" tại công ty của dòng. Không thêm quyền |
| C8 | Đợt | Cùng go-live Chuyển đổi hàng hoá |
| C9 | Lưu log | Bảng mới `product_price_apply_logs` (hướng A) |
| C10 | Mockup | Không — làm theo khuôn list-page có sẵn ("triển khai luôn") |

## Thiết kế
### 1. Command HRM `product-price:apply-expected {date?} {--company=}` — 01:00, `withoutOverlapping`, `Asia/Ho_Chi_Minh`
Theo từng công ty (công ty có dòng giá hiệu lực chờ), mỗi công ty 1 transaction:
1. Chốt chặn: còn `status 2` có `effect_date < date − 30 ngày` của công ty ⇒ bỏ qua công ty, báo "bị chặn".
2. Lấy `status 2`, `effect_date <= date`, `flag ≠ 1` (hoặc NULL), sắp `effect_date, id`, `lockForUpdate` (chạy trùng ERP không áp đôi).
3. Áp vào `product_unit_prices` của công ty: price / coefficient / sale_max_percent; dòng có yêu cầu duyệt (`product_approve_prices` ↔
   `product_approves`) ⇒ giữ `*_wait_approve` + cờ (N58), ngược lại đồng bộ số đề nghị = số mới, cờ 0 (y luật ERP).
   pep ⇒ `status 1`.
4. Ghi `product_price_apply_logs` mỗi pep + `ProductPriceHistoryService` mỗi (ĐVT × công ty): người thực hiện "Hệ thống",
   nội dung "Áp giá hiệu lực ngày dd/mm/yyyy".
5. Lỗi 1 công ty ⇒ rollback riêng công ty đó, chạy tiếp công ty khác, `report()`.

### 2. Bảng `product_price_apply_logs`
`id, run_at, company_id, product_id, product_unit_id, unit_id, price_type_id, expected_price_id, effect_date,
old_price, old_coefficient, old_sale_max_percent, new_price, new_coefficient, new_sale_max_percent,
action (1 Tự áp · 2 Áp ngay · 3 Đóng không áp), kept_pending (bool), created_by (NULL = Hệ thống), created_at` + index (company_id, run_at).

### 3. Thông báo — chuông + app (1 lệnh `sendNotification` chế độ command), người nhận = holders "Cập nhật giá bán hàng hoá" tại công ty
- Có áp: `[GIA] Đã áp: <b>N giá hiệu lực</b>. Ngày dd/mm/yyyy` ⇒ `/finance/product-price-logs?company_id=&date=`.
- Bị chặn: `[GIA] Chưa áp giá hiệu lực: <b>N giá quá hạn</b> cần xử lý` ⇒ `/finance/product-price-logs?tab=stale&company_id=`.

### 4. Màn `/finance/product-price-logs` "Nhật ký áp giá"
- Tab "Đã áp" (list-page): lọc ngày áp, công ty, mã hàng, loại giá, hành động; cột thời gian · công ty · mã/tên · ĐVT · loại giá ·
  giá cũ → mới · hệ số · ĐMGG · ngày hiệu lực · hành động · người thao tác. Không giá vốn.
- Tab "Giá quá hạn chưa áp": pep `status 2`, `effect_date < hôm nay`, theo công ty có quyền; nút Áp ngay / Đóng, không áp
  (từng dòng + hàng loạt, xác nhận) — gate "Cập nhật giá bán hàng hoá" tại công ty của dòng; ghi log + lịch sử.

### 5. ERP + triển khai
- Bỏ lịch `product:update_price` (+ email, file HTML) ở `app/Console/Kernel.php`; lệnh giữ để chạy tay khẩn cấp.
- Khoá màn Nhật ký giá ERP (`productMovedToHrm`).
- Runbook: kiểm `schedule:run` HRM trên máy chủ; bật cron HRM cùng cửa sổ tắt cron ERP; N65 dọn quá hạn TRƯỚC (local 17/10:
  13.472 dòng chờ > 30 ngày — Cty 1: 13.295, Cty 4: 177).

## 6. Kết quả code 17/10/2026 — ĐÃ PUSH nhánh con (api `3aa91aefd` · client `04f519042` · ERP `0dce021a2c`), CHƯA merge nhánh chung
Nhánh: hrm-api + hrm-client `feat/cdhh-cron-gia-hieu-luc` (từ nhánh chung `dbd9ebbb2` / `862ea0ef6`) · ERP `feat/2d1-cron-gia-hieu-luc` (từ `af4e31d0dd`).

**Điều chỉnh so với thiết kế (đã báo user):**
- Màn Nhật ký theo **công ty đang làm** (như Cập nhật giá bán — P5), không nhận company_id; deep-link thông báo công ty khác ⇒ ghi chú "đổi công ty đang làm".
- Nhóm hành động thông báo theo skill notification-convention: có áp = `Cập nhật`, bị chặn = `Quá hạn`.
- Dòng `flag = 1` (đang chờ duyệt SỬA giá hiệu lực) không tính vào chốt chặn và không hiện ở tab quá hạn (việc của màn Duyệt giá) — giống ERP bỏ qua khi áp.

**hrm-api:** migration `2026_10_17_100001_create_product_price_apply_logs_table` (ĐÃ CHẠY `hrm_erp_giacty`) · `ExpectedPriceApplier` · `ProductPriceLogService` ·
`ProductPriceLogController` + route `master-data/product-price-logs` (xem 1657|1658; `stale/apply|close` 1657) · `ApplyExpectedPricesCommand`
(`product-price:apply-expected {date?} {--company=}`) + lịch 01:00 `app/Console/Kernel.php` · `ProductPriceNotifier::expectedApplied/expectedBlocked`
(+ `holderInfoIds`, `sendAsSystem`) · nhãn lịch sử `expected_applied` / `expected_closed` (`CatalogHistoryService`) · `tests/fixtures/price-readers.txt` +1.
Sửa lỗi phát hiện bằng test: nhiều mốc của cùng dòng giá trong 1 lần chạy ⇒ "giá cũ" mốc sau = giá mốc vừa áp.
**hrm-client:** `pages/finance/product-price-logs/index.vue` (2 tab) · menu Tài chính › Quản lý giá - CTKM "Nhật ký áp giá".
**ERP:** bỏ lịch `product:update_price` (+ email, file HTML) · `productMovedToHrm:price-logs` cho 2 route `price_logs` · test cập nhật 269⇒271 route chặn.

**Kiểm:**
- PHPUnit HRM `ExpectedPriceApplyTest` 3/3 (63 assert: áp theo công ty, mốc mới nhất thắng, tương lai + flag 1 không áp, nhật ký cũ→mới, lịch sử "Hệ thống",
  thông báo hệ thống đúng câu + link, chạy lại không áp đôi, chốt chặn tách công ty, giữ đề nghị chờ duyệt, quyền 403 / chỉ Duyệt / Cập nhật, Áp ngay / Đóng,
  dòng công ty khác 422). Liên quan xanh: ProductPriceScreenApi 32, ProductPriceApprovalApi 26, PriceCalculateApi 13, PriceReaderWhitelist 2, PriceReadPoints 9,
  ProductPriceSetWrite 7, ProductPriceReader 5. ERP toàn bộ 207 OK (4 skip như cũ).
- Playwright MCP (3031/8031, e2e_assign cty 1, ghi bị chặn): tab Đã áp (payload dựng bằng service thật trong transaction ROLLBACK) 11 cột, badge 3 màu
  rgba(…,.1), "Hệ thống", deep-link `?date=` lọc sẵn 17/10/2026; cảnh báo "Còn 13,289 giá … tạm dừng tự áp"; tab Giá quá hạn (API thật 13,657) — nút hàng loạt
  khoá khi chưa chọn, chọn 2 ⇒ xác nhận ⇒ 1 POST `stale/apply {ids:[69,322]}`; `can_handle:false` ⇒ 0 ô tick / 0 thanh hàng loạt / không cột Hành động;
  `?company_id=4` ⇒ ghi chú công ty khác; menu có link. Sửa sau đo: cột Hàng hoá bị kéo ~700px ⇒ giới hạn 240px + "…"; số 13289 ⇒ 13,289.
  ERP `/admin/sale/price_logs` ⇒ 403 "Chức năng đã chuyển sang HRM" + nút mở HRM `/finance/product-price-logs`; AJAX ⇒ JSON 403 + redirect_url.
- KHÔNG chạy command áp giá thật vào giacty. Không có spec e2e (ngoài phạm vi đã xin).

## 7. Runbook bổ sung (go-live)
1. N65 `price:cleanup-stale` (ERP) dọn quá hạn TRƯỚC — nếu không, Cty 1 / 4 bị chặn ngay ngày đầu (local 17/10: 13.289 / 177).
2. Deploy ERP nhánh có commit bỏ lịch ⇒ `crontab -l` ERP vẫn gọi `schedule:run` (các cron khác) nhưng không còn `product:update_price`.
3. HRM: `php artisan migrate` (bảng nhật ký) · kiểm `crontab` HRM có `* * * * * cd <HRM_API> && php artisan schedule:run` · chạy thử
   `php artisan product-price:apply-expected` (in bảng theo công ty) · sáng hôm sau mở Tài chính › Nhật ký áp giá + kiểm chuông.
4. Không bật lại lịch ERP (2 hệ thống cùng áp ⇒ lịch sử đôi; dòng đã áp tự bỏ qua nhờ khoá dòng nhưng log ERP/HRM lệch).

## 8. Test VPS dev (`hrm_crm`) 17–18/10/2026
- Deploy Lối A: hrm-api `518cb1b62` · migrate đủ · seeder điều kiện thanh toán · `queue:restart` (phải `sudo -u www-data`) · worker queue database có sẵn.
- **Crontab `hrm_crm` chưa từng có `schedule:run`** ⇒ user chốt bật TOÀN BỘ lịch HRM (crontab `www-data`, 17/10 19:35) — cron chạy mỗi phút, không lỗi log.
- Chốt chặn: 0 công ty bị chặn (N65 đã dọn 15/10).
- Cty 3 chạy tay `apply-expected 2026-10-18 --company=3` ⇒ áp 8 giá (gồm `ENEO-210-V5040` 94,000 → 104,000), nhật ký + lịch sử "Hệ thống" đúng, chạy lại không áp đôi.
  ⚠️ 1 dòng dữ liệu có sẵn: `LUTR-SL-4012` Bán lẻ 7,040,000 → **1 đ** (giá hiệu lực 1 đ ngày 17/10 — áp đúng luật; user chưa xác nhận chủ đích).
- Thông báo ban đầu 0 người nhận ⇒ phát hiện lỗi luật chọn người nhận (quyền tick ở công ty nằm trên VAI TRÒ, không phải công ty gán vai trò) ⇒ sửa 10 hàm (xem `phien-sau.md` 0b), hrm-api `518cb1b62` ⇒ Cty 3 có 7 người nhận.
- 18/10 áp đúng ngày 19/10 (tinker gọi `ExpectedPriceApplier::apply` + `expectedApplied`) ⇒ **user xác nhận nhận thông báo chuông + giá áp thành công.**
- Chưa test trên VPS: bước 5 (chốt chặn theo công ty + Đóng / Áp ngay ở tab quá hạn), bước 6 (quyền màn Nhật ký). Môi trường chỉ có web (không app mobile).

## 9. Còn mở
- Đề xuất chưa trả lời: (a) runbook thêm bước soát giá hiệu lực đang chờ ≤ 1 đ / giảm sâu trước go-live (lần chạy đầu áp mọi giá trong 30 ngày); (b) tuỳ chọn `--only-date` + `--dry-run` cho lệnh chạy tay.
- `LUTR-SL-4012` Cty 3 giá Bán lẻ 1 đ trên VPS — hỏi nghiệp vụ có chủ đích không.
- Middleware `checkPermission` gộp quyền mọi công ty (không xét công ty đang làm) — có sẵn, ngoài đợt; lệch với luật theo công ty.
