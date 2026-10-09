# Bỏ cột '% Lũy tiến' — báo cáo tổng hợp thu nhập bán hàng (quyết toán quý)

## Yêu cầu
Bỏ cột '% Lũy tiến' (progressive_approval_percent) khỏi report commission-settlement-quarter.

## Ảnh hưởng (đã kiểm)
- Không vào tính tổng nào (total_income không có). Chỉ hiển thị.
- Xuất hiện: màn hình report blade + bản in (2 bảng). Không có ở export Excel.

## Tasks
- [x] Report blade: bỏ header + ô % Lũy tiến (4 dòng: header/tổng/phòng/NV) — verify 13/13/13/13 ô khớp
- [x] Print (CommissionSettlementQuarterPrint): bỏ ở getTable (tổng hợp) + getTable4Excel (export) — php -l sạch, cột khớp
- [ ] User test màn hình report + in + export Excel

## Ghi chú
- Giữ `progressive_approval_percent` dòng 497 (data cho print-detail popup từng NV) — không phải cột report.
- Service `CommissionSettlementQuarterReportService` để nguyên (field thừa vô hại).

## Branch: master

### Checkpoint — 2026-07-02
Vừa hoàn thành: Bỏ cột "% Lũy tiến" — report blade + print (getTable + getTable4Excel).
Đang làm dở: (không)
Bước tiếp theo: User test màn hình + in + export.
Blocked:
