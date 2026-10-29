# Plan — Sửa cột "Thưởng thêm" cộng Có trừ Nợ

## Tasks
- [x] T1: `CommissionSettlementQuarterReportService.php` dòng 54 (nhánh FirmContract) —
      `commission_bonus_quarter` thêm vế `- SUM(... type=1 ...)`.
- [x] T2: cùng file dòng 214 (nhánh WrServiceContract) — sửa y hệt T1.
- [x] T3: `php -l` sạch; print/export (`CommissionSettlementQuaterDetailPrint` +
      `CommissionSettlementQuarterPrint`) KHÔNG có SQL riêng (grep rỗng) → không phải sửa.

- [x] T4 (popup chi tiết): xác minh logic popup "Chi tiết" (`ReportController@commissionSettlementQuarterGetDetail`)
      KHÔNG có SQL `commission_bonus_quarter` riêng. Popup gọi `getData($request, $permissions, 'detail')`;
      ở chế độ `'detail'` method bỏ qua block re-aggregate (dòng 347-428) và trả thẳng dòng union từ
      `getDataFirm`(dòng 55)/`getDataWr`(dòng 216) → DÙNG LẠI đúng cột đã sửa ở T1/T2. Controller chỉ
      `->sum('commission_bonus_quarter')` cộng lại các giá trị đã-sửa. grep toàn repo: chỉ 3 chỗ tính bằng
      CASE WHEN = Service:55, Service:216 (báo cáo này, đã Có−Nợ) + `AccountDetail.php:3951` (báo cáo KHÁC,
      vốn đã Có−Nợ). → popup chi tiết đã đúng theo T1/T2, KHÔNG cần sửa thêm.

## Checkpoint — 2026-10-03
Vừa hoàn thành: T1–T4. Sửa 2 dòng DB::raw (replace_all) → cột "Thưởng thêm" = SUM Có(type2) − SUM Nợ(type1),
work_id=TT, account 117, giữ nguyên whereNotIn loại trừ BillPayment/BillPaymentAuthorization/ClosingEntry.
Dòng 354 (SUM union ngoài) giữ nguyên. Popup chi tiết dùng chung getDataFirm/getDataWr nên đã đúng (T4). php -l sạch.
Đang làm dở: (không)
Bước tiếp theo: user kiểm trên môi trường có bút toán Nợ TK3351/work TT để thấy cả bảng tổng LẪN popup chi tiết giảm đúng.
Blocked: không test submit/data được vì DB trỏ PROD (chỉ sửa code).
CHƯA commit/push (chờ yêu cầu).
