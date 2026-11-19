# Đối chiếu số Báo cáo tổng hợp bán hàng — HRM ↔ ERP

> 16/11/2026 · DB local `erp_hrm_check` (chỉ SELECT) · ERP worktree `wt-bonus-month-erp` = develop_02 ca185e425e
> (`SummarySaleReportService` không đổi so với origin/develop_02) · HRM worktree `wt-sale-summary-api`.

## Cách so

- ERP: `SummarySaleReportService(['is_all_company'=>true])->getData(type=all, date_from/date_to[, company_id])`,
  tồn đầu/cuối tắt (không so — đã đối chiếu ở màn mặt hàng).
- HRM: `SaleByProductReportService::forSummary()->report($r, false)`, phạm vi `all`, tham số
  `period=custom&from&to[&company_id]`.
- So theo `product_id` 6 cột `exported_qty, real_qty, allocated_price_amount, export_price_amount, diff, profit_loss`,
  ngưỡng |Δ| ≤ 1 đồng. Loại khỏi phép so các hàng có dòng HĐ HRM trong kỳ (xuất `emplement_contract_type` = HĐ HRM
  hoặc bán mượn `contractable_type` = HĐ HRM) — ERP không có phần này.
- Script: scratchpad `sale-parity/erp.php` + `sale-parity/hrm.php` (không commit).

## Kết quả — 0 lệch

| Kỳ | Phạm vi | Dòng ERP | Dòng HRM | Loại (HĐ HRM) | Lệch | Σ Thành tiền vốn | Σ Lãi lỗ |
|---|---|---:|---:|---:|---:|---:|---:|
| 05/2026 | Tổng công ty | 1,490 | 1,490 | 0 | **0** | 36,945,917,519.92 | 141,486,312,890.37 |
| 05/2026 | Công ty 1 | 1,290 | 1,290 | 0 | **0** | 28,599,366,393.47 | 141,145,133,954.69 |
| 2025 | Tổng công ty | 4,805 | 4,805 | 0 | **0** | 413,892,047,566.81 | 799,375,039,274.76 |
| 2025 | Công ty 1 | 4,021 | 4,021 | 0 | **0** | 350,127,729,513.60 | 776,757,936,889.79 |
| 2026 | Tổng công ty | 4,997 | 4,997 | 4 | **0** | 326,943,734,576.15 | 872,414,661,784.00 |
| 2026 | Công ty 1 | 4,268 | 4,268 | 4 | **0** | 271,186,185,736.00 | 852,349,968,908.51 |

Σ các cột còn lại (SL bán, SL thực tế, tiền phân bổ, chênh lệch) cũng Δ = 0.00 ở cả 6 tổ hợp.

## Kết luận

- Không phát hiện lỗi ERP mới → **không vá ERP**. Nghi vấn hệ số ĐVT hàng mượn đã kết luận không phải lỗi (design §6).
- Phạm vi "Công ty" (mức 3, công ty mình OR phiếu mình tạo) không so riêng qua người dùng thật; logic `applyScope`
  dùng chung với màn mặt hàng đã đối chiếu trước đó, và có test `test_summary_scope_company_and_all`.
