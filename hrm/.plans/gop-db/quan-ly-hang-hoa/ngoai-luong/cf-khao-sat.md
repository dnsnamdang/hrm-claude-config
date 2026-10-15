# Khảo sát đợt C-f — dữ liệu / runbook (13/10/2026, chỉ đọc)

> Mục: N65 (giá hiệu lực quá ngày + cờ chờ duyệt mồ côi + cron) · N26 (AUTO_INCREMENT `product_versions`). Chốt sẵn: Q-N65, Q-N26 (13/10).
> ERP worktree `wt-erp-2d1` @ `d7226cd1b9`. DB `hrm_erp_giacty`.

## N65 — số đo giacty 13/10
| Nhóm | Số |
|---|---:|
| `product_expected_prices` status 2 (chờ hiệu lực) đã QUÁ NGÀY | **13.915** (flag NULL 13.800 · flag 1 = 6 · flag 0 = 109) |
| … trong đó năm 2026 (xuất danh sách cho nghiệp vụ soát) | **2.067** |
| status 2 còn tương lai (không đụng) | 8.078 |
| Cờ chờ duyệt mồ côi: `product_unit_prices` (3 cờ) · `product_company_units` · `product_units` | **5 · 6 · 6 = 17** — `product_approves` đang **0 dòng** ⇒ không yêu cầu duyệt nào còn chờ, cả 17 đều mồ côi |

Cron `product:update_price` (ERP `UpdateProductPrice.php`, `dailyAt('01:00')`): lọc `effect_date = hôm nay` ⇒ ngày nào cron không chạy / lỗi là dòng
của ngày đó treo mãi (nguồn của 13.915 dòng). Thêm: `catch (Exception $e)` không import ⇒ là `App\Console\Commands\Exception`, KHÔNG bắt được
lỗi thật (transaction không rollback chủ động, lỗi văng ra ngoài).

Ai đọc `pep.status`: HRM chỉ đọc `status = 2 AND effect_date > hôm nay` (giá tương lai) — `ProductPriceHistoryService:76`,
`ProductPriceListService:289`; ERP chỉ đọc `status 2` (áp) / `1` (đã áp). ⇒ mã mới **3 = đóng, quá hạn không áp** không lọt vào màn nào.

## N26 — product_versions
Local: AUTO_INCREMENT `product_versions` 176.616 > max `product_histories.product_version_id` mồ côi 175.610 ⇒ hết rủi ro; 59.710 dòng mồ côi giữ
nguyên (Q-N26). Prod chưa đo ⇒ bước kiểm + chỉnh trong runbook.

## Tự chốt (kỹ thuật)
- Lệnh dọn đặt ở **ERP** (cron + bảng cùng chỗ): `php artisan price:cleanup-stale` — `--dry-run` (chỉ đếm + xuất file), mặc định sao lưu dòng
  sẽ đổi ra `storage/app/price-cleanup/<thời điểm>/` (CSV) TRƯỚC khi ghi; idempotent (chạy lại ⇒ 0 dòng).
- "Đóng" = `status = 3` (+ `updated_at`), KHÔNG đổi giá, KHÔNG áp. Danh sách 2.067 dòng 2026 xuất CSV (mã hàng, tên, công ty, loại giá, ĐVT,
  giá hiện hành, giá hiệu lực, ngày hiệu lực, người tạo).
- Xoá cờ mồ côi = cờ về 0 + số đề nghị (`*_wait_approve`) = số đang chạy (đúng cách cron làm sau khi áp); chỉ dòng KHÔNG có yêu cầu duyệt đang chờ.
- Cron: `effect_date <= hôm nay`, áp theo `effect_date, id` tăng dần (nhiều mốc cùng 1 dòng giá ⇒ mốc mới nhất thắng); sửa `catch` → `\Throwable`.
