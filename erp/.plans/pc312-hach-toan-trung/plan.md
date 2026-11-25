# Phiếu chi TPE.PC1125.00043 (id 312) hạch toán trùng — plan

Báo lỗi 25/11/2026: BC chi tiết công nợ NCC, NCC CÔNG TY CỔ PHẦN LIÊN KẾT VÀNG, HĐ FENGERDA 0925HP "Đã thanh toán" 4.470.876, thực tế 1 PC 1.490.292.

## Nguyên nhân
- PC312 đi qua bước duyệt (`BillPaymentController@update`, status=3) 2 lần cùng giây 11/11/2025 18:02:37 → lần 2 thêm dòng chi tiết trùng (1589) + hạch toán lại 2 dòng → Nợ 3311 = 3 × 1.490.292.
- `update` không khoá dòng phiếu; `canApprove()` chỉ kiểm status đã đọc → 2 request song song cùng qua.
- Rà toàn bộ phiếu chi đã duyệt (trừ loại 4 chi lương — hạch toán khác): chỉ PC312 lệch.

## Tasks
- [x] Sửa dữ liệu hrm_erp_gop (user duyệt 25/11): xoá account_detail_refs 278464/278466/278469, account_details 266973/266976/266978, bill_payment_details 1589. Kiểm lại: còn 266954 (Nợ 3311) + 266958 (Có 1111) = 1.490.292, chi tiết 1561.
- [x] BE: `update` dùng `lockForUpdate()`; chặn request lặp lại khi phiếu đã duyệt/đã hủy.
- [x] FE `show.blade.php`: `submit()` bỏ qua khi `loading.submit` đang bật.
- [x] ĐÃ push develop_02 `edab7ec8fd` (25/11).
