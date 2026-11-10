# YC hạch toán mua dịch vụ: chặn YC 0 đồng và vượt số lượng còn lại của HĐ (ERP) — @junfoke

## Ngày 07/11/2026 (@junfoke)
- [x] 06/11/2026 — Nhận lỗi (không có issue): màn YC hạch toán mua dịch vụ (`orders/buy-service-accounting-request`) gửi được nhiều YC hạch toán 0 đồng cho cùng 1 HĐ (QA nói 1 HĐ chỉ 1 YC). Code đang cho hạch toán TỪNG PHẦN theo số lượng.
- [x] 07/11/2026 — User chốt: giữ hạch toán từng phần, chỉ chặn 0đ + chặn vượt SL; làm nhánh fix riêng → develop_02 trước.
- [x] 07/11/2026 — Ẩn nút "Yêu cầu hạch toán dịch vụ" khi HĐ đã được yêu cầu hạch toán hết số lượng (`BuyServiceContract.php`); mở thẳng link tạo thì báo "Hợp đồng đã được yêu cầu hạch toán hết số lượng…" thay cho "Không có quyền".
- [x] 07/11/2026 — Kiểm lại lúc lưu, cả tạo lẫn sửa (`BuyServiceAccountingRequestController.php`): chặn tổng SL = 0; chặn dòng vượt SL còn lại (khi sửa không tính phần của chính YC đang sửa); khoá HĐ trong lúc lưu (2 tab gửi cùng lúc thì tab sau chờ rồi bị chặn). SL còn lại = SL HĐ − đã hạch toán − YC đang tạo/chờ duyệt/đang hạch toán (khớp cách tính cũ của màn).
- [x] 07/11/2026 — Kiểm local trên dữ liệu thật (transaction + rollback): gửi toàn 0 bị chặn, gửi đúng bằng SL còn lại hợp lệ, gửi vượt bị chặn; dựng lại ca HĐ 109 — YC đầu lấy hết SL thì nút ẩn, YC thứ hai bị chặn, sửa chính YC đó vẫn được.
- [x] 07/11/2026 — Commit `12e73d624d` nhánh `fix_yc_hach_toan_mdv_chan_0d` (đã push) → merge develop_02 `95e12277f6` + gop_db `822a4695ac` (đã push, tự gộp với thay đổi mã quyền trên gop_db).
- [ ] Prod còn YC **EG.YCHTMDV.2026000096** (0đ, Chờ duyệt) tạo trước bản sửa → kế toán bấm "Không duyệt".

## Ngày 09/11/2026 (@junfoke)
- [x] 09/11/2026 — Màn YC hạch toán mua dịch vụ thêm bộ lọc "Người tạo" (cùng commit lọc mẫu in `3f87275c4a`, develop_02 `79fb244c79`, gop_db `176739bc69`). Dev đã pull, QA kiểm được.
