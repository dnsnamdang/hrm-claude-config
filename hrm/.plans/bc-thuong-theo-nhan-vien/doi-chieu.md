# Đối chiếu số HRM ↔ ERP — Báo cáo thưởng theo nhân viên

Ngày chạy: 14/11/2026. DB: `erp_hrm_check` @ 127.0.0.1:3306 (chỉ đọc; 2 bên đều bị ép về DB này, đã in tên DB + host trước khi query).
Người xem: NV id 13 (công ty 1), mã quyền `sale.bao_cao_thuong_theo_nhan_vien.view` scope 4 (Tập đoàn). HRM `BonusEmployeeScope::level()` = all; ERP `permissionScope` = 4.
Cách chạy: gọi thẳng service 2 bên (HRM `BonusEmployeeReportService::rows/totals/detailRows`; ERP `BonusBusinessEmployeeReportService::bonusBusinessEmployeeSearchData` + `getDetailByEmployee`, bản đã vá commit 0d5743c1ae), không qua HTTP.

## Kết quả

| Khoảng ngày | Dòng NV HRM | Dòng NV ERP | Phòng (H/E) | Dòng lệch | Tổng lệch | Popup so (NV) | Popup lệch |
|---|---|---|---|---|---|---|---|
| 01/06/2026 – 30/06/2026 (tháng; có cả HĐ hãng + HĐ DV) | 130 | 130 | 20 / 20 | **0** | **0** | 130 | **0** |
| 01/04/2026 – 30/06/2026 (quý) | 152 | 152 | 21 / 21 | **0** | **0** | 152 | **0** |

So từng `(department_id, employee_id)` trên 3 cột + `total` (sai số ≤ 0,005). Tổng cuối khớp:
- Tháng 6: TTHHD 869,304,533 · TNST 326,126,868 · TNSQ 526,815,379 · Tổng 1,722,246,780
- Quý 2: TTHHD 3,879,767,352 · TNST 1,061,683,252 · TNSQ 1,639,429,880 · Tổng 6,580,880,484

Popup: so từng dòng (loại HĐ, id HĐ, mã HĐ, mã KH, 3 cột) cho mọi NV; tháng 6 có 2,662 dòng popup (2,359 HĐ hãng + 303 HĐ DV), quý có 7,777 dòng; đều khớp.

## NV mẫu HĐ hãng + HĐ DV trùng contractable_id

NV id 24, toàn bộ 2025-01-01 → 2026-12-31: popup 1,073 dòng HRM = 1,073 dòng ERP, giống hệt. Có 8+ id trùng giữa 2 loại, ví dụ id 91:
- WrServiceContract 91 → HDDV_TPE_HN_KD1_25_0005_MECHOANKIEM · KH 29TPHPCU-23 · 154,256 / 40,079 / 40,079
- FirmContract 91 → HĐ_TPE_HN_KD1_25_0004_L00343 · KH 15TPHNNG-1 · 126,000 / 23,940 / 47,880
→ 2 dòng, mã HĐ/KH đúng loại ở cả 2 bên.

## Chưa làm
- Playwright màn ERP: không làm — màn ERP cần đăng nhập, không có thông tin đăng nhập an toàn cho worktree trỏ local; không dùng cách bỏ qua xác thực. Màn HRM đã chụp ở Task 4.
- Không đối chiếu phạm vi scope 1-3 ở bước này (đã có test đơn vị Task 2/3).

## Ghi chú deploy (STATUS)
- Chạy `permission:catalog-sync` nếu sửa `platforms` của mã `sale.bao_cao_thuong_theo_nhan_vien.view`.
- ERP vá 4 lỗi cũ (lộ cả phòng, popup ngoài phạm vi, lọc bộ phận chưa tới NV, in/xuất chỉ trang hiện tại) — cần báo user khi bàn giao.

Script: /private/tmp/claude-501/-Users-nguyentrancu-DEV-code-ERP-HRM/c9f36c30-42cf-4b40-af47-8adabe72537f/scratchpad/sdd-bc-thuong/t5/ (run-hrm.php, run-erp.php, cmp.php, pop-*.php; kết quả *.json).
