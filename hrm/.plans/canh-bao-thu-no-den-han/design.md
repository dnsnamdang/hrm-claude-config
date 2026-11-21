# Cảnh báo thu nợ đến hạn — port ERP → HRM

Spec đầy đủ: `docs/superpowers/specs/2026-11-21-canh-bao-thu-no-den-han-design.md` (chờ duyệt 21/11/2026).

## Đối chiếu ERP (21/11/2026)

- ERP local (`TanPhatDev/.env`) trỏ DB khác (`hrm_erp_test`) → chạy **nguyên văn SQL của ERP `WarningDebtDueDateService::getData`** (inner + outer group theo HĐ gốc) trên DB HRM `erp_hrm_check`, so với `CustomerDebtDueWarningReportService::rows()`.
- Người xem: NV công ty 1 (N = 15), cấp tạm quyền `sale.canh_bao_thu_no_den_han.view` phạm vi Tổng công ty trong transaction → rollback (không ghi dữ liệu). Script: scratchpad `recon.php`.

| Đến ngày | Số HĐ ERP | Số HĐ HRM | Tổng còn phải thu (cả 2) | Thiếu | Thừa | Lệch debt > 1đ |
|---|---|---|---|---|---|---|
| 2026-11-21 | 2,204 | 2,204 | 594,653,332,564 | 0 | 0 | 0 |
| 2026-10-31 | 2,204 | 2,204 | 594,653,332,564 | 0 | 0 | 0 |

- Hai mốc ra cùng số vì DB local chỉ có bút toán TK 131 tới 07/09/2026 → toàn bộ 2,204 HĐ rơi nhóm **Quá hạn**; nhóm Sắp đến hạn / Đến hạn được kiểm bằng test fixture (`CustomerDebtDueWarningReportTest`).
