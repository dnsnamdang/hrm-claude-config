# Đối chiếu ERP ↔ HRM — Báo cáo thưởng theo quý

- Ngày chạy: 16/11/2026 · DB local `erp_hrm_check` (KHÔNG đụng DB remote của ERP `.env` — script ép config DB về local ngay sau LoadConfiguration và kiểm `database()` trước khi chạy)
- Kỳ: Q2/2026 (`2026-04-01` → `2026-06-30`), phạm vi Tổng công ty (ERP `is_all_company`, HRM scope ALL)
- ERP: `CommissionQuarterReportService::getData()` · HRM: `BonusQuarterReportService::rows()/tree()/totals()`
- Script: scratchpad `bq/erp.php`, `bq/hrm.php`, `bq/cmp.py`

| Chỉ tiêu | ERP | HRM |
|---|---:|---:|
| Số dòng (NV × HĐ) | 7,777 | 7,777 |
| Doanh số thực hiện | 212,587,768,846 | 212,587,768,846 |
| Thưởng thực hiện HĐ | 3,879,767,352 | 3,879,767,352 |
| Thưởng quý tạm tính | 1,738,360,172 | 1,738,360,172 |
| Thưởng quý thực tế | 1,638,097,369 | 1,638,097,369 |
| Tổng cộng | 5,517,864,721 | 5,517,864,721 |
| Quá hạn | 100,262,803 | 100,262,803 |

- Khoá (phòng, NV, loại HĐ, id HĐ): lệch 0 khoá, so từng ô 6 cột: **0 ô lệch**.
- 1 phòng: Phòng KD Khu vực 3 (id 108) — Tổng cộng ERP 1,477,084,468 = HRM 1,477,084,468.
- 1 NV: 21810660 - Bùi Sỹ Phú — ERP 1,078,956,847 = HRM 1,078,956,847 (37 HĐ).
- 4 dòng có Tổng cộng NULL ở cả 2 bên (kỳ không có quyết toán — design §7.4), hiển thị `-`.
- Cây HRM: 22 phòng; ERP không có dòng thiếu phòng ở kỳ này.

**Kết luận: KHỚP 100%.**
