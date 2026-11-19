# Plan — Sửa tỷ lệ đề xuất %DS cho phòng hỗ trợ (Hỗ trợ hạch toán HĐ phối hợp)

## Tasks
- [x] T1 (FE): `departments-support.blade.php` — thêm `<input>` cho `commission_sale_percent`
      phòng hỗ trợ khi `!isPreview && !$last`; giữ text read-only khi `isPreview || $last`.
- [x] T2 (FE): `FirmSupportAccounting.blade.php` — viết lại `onChangeCommissionSalePercent()`
      tính phòng hỗ trợ cuối = 100 − (chính + các hỗ trợ còn lại), kẹp ≥ 0.
      (+ thêm helper `totalCommissionSalePercent(data)`)
- [x] T3 (FE): `FirmSupportAccounting.blade.php` `isInvalidData()` — chặn submit khi tổng %DS ≠ 100.
- [x] T4 (BE): `FirmContractApproveRequest.php` — `withValidator` tổng %DS các phòng = 100
      (chỉ khi có approver_id/status).
- [x] T5: `php -l` sạch; logic auto-tính verify bằng node (5 ca OK). Playwright KHÔNG chạy được:
      app local fatal ở controller khác (`ProductExportRequest::CHO_DUYET_NHAP`) chặn load route,
      và submit-path không chạy vì DB trỏ prod `hrm_erp_gop`.

## Checkpoint — 2026-10-01
Vừa hoàn thành: T1–T5 (3 FE + 1 BE validate + verify). php -l sạch, node check 5 ca đúng.
Đang làm dở: (không)
Bước tiếp theo: user kiểm thực tế trên môi trường có HĐ phối hợp ở trạng thái CHỜ DUYỆT (≥2 phòng hỗ trợ);
nếu cần tôi đẩy `commission_sale_percent` vào `getKeysChanged` (ép chuyển duyệt khi đổi %DS) thì gộp sau.
Blocked: Playwright verify (app local lỗi route không liên quan + DB prod không submit được).
ĐÃ COMMIT + PUSH: gop_db `4e6332e709` (c97fd91ef3..4e6332e709), user chốt giữ hướng A 2026-10-01.
