# Hỗ trợ: phiếu nhập không cộng tồn, huỷ báo không đủ tồn — GPP sphquocnam5723 (không có số Redmine) — @cuong61n

Yêu cầu từ hỗ trợ (Tuấn Kiệt), 07/11/2026: GPP `sphquocnam5723` (Nhà thuốc Tây Quốc Nam, cơ sở 1832),
thuốc DQG00062116 Aurozapine OD 15, lô MPA26039C — phiếu nhập không cộng tồn, khách nhập thêm phiếu khác,
huỷ phiếu thì báo không đủ tồn.

## Task

- [x] (07/11/2026) Điều tra trên prod GPP
  - Nghiệp vụ: **cả hai** phiếu PN652685 (nhập 02/11) và PN653279 (nhập 04/11), mỗi phiếu 70 hộp = 2.100 viên,
    đều KHÔNG được tính vào tồn. Thứ tự thật ngược với mô tả: PN652685 lỗi trước, 04/11 khách nhập lại
    PN653279 (cùng số HĐ NCC 00015880) và cũng lỗi. Tồn hiện 818 viên = kiểm kho 29/10 (870) − bán sau đó (52).
    Huỷ 1 phiếu phải trừ 2.100 viên từ 818 → báo không đủ tồn.
  - Nguyên nhân: sau mỗi lần nhập/bán, API gọi `InvoiceService::recalculateStockFromReport` tính lại tồn =
    tồn kiểm + nhập − xuất **có `invoice.created_at` > thời điểm kiểm kho**. `invoice.created_at` là *ngày nhập
    hàng người dùng chọn* (29/10 00:00), còn phiếu kiểm KP224007 lập 29/10 16:24 → hai phiếu bị coi là trước
    kiểm kho và bị loại. Hàm nhập (f_create_invoice_iv2_iv7_warehousing) đã cộng đúng 2.100, nhưng ngay sau
    đó bước tính lại ghi đè về 870/860. Bằng chứng: `new_warehouse_logs` wh_id 11149280 — 02/11 07:59:54
    2970→870, 04/11 07:59:22 2960→860, desc "Nhập sau kiểm=0".
  - Phạm vi: quét toàn prod từ 01/09/2026 có thêm 2 ca cùng điều kiện: cơ sở 1007 PN638463 (10), cơ sở 2797
    PN646326 (60).
  - Đã kiểm: invoice/invoice_detail/warehouse/warehouse_agency/t_stock/check_detail/vouchers_check,
    logging.invoice_warehouse, new_warehouse_logs, nginx access log + laravel.log 2 server API.
  - Trạng thái: chờ quyết định sửa code (so mốc kiểm kho theo `invoice_detail.created_at` = thời điểm nhập
    thật) và sửa dữ liệu lô MPA26039C. Chưa sửa gì trên prod.

- [x] (07/11/2026) Sửa dữ liệu prod lô MPA26039C cơ sở 1832 (anh Cường duyệt)
  - Nghiệp vụ: giữ PN652685, để khách tự huỷ phiếu trùng PN653279 trên màn hình. Đổi ngày nhập PN652685
    29/10 → 30/10 để bước tính lại tồn không loại nó nữa; tồn đặt về 5.004 viên (= 870 kiểm kho + 2×2.100 − 66 đã
    bán) → huỷ PN653279 xong còn 2.904, khớp với số tính lại (870 + 2.100 − 66).
  - Kỹ thuật: 1 transaction, khoá warehouse/warehouse_agency, tự kiểm tồn hiện tại = 870 − bán trước khi ghi.
    Update invoice 3557933.created_at; warehouse (is_check=false) + warehouse_agency agency 2957, 3 đơn vị.
    Backup: `stockfix.bk_20261107_1832_mpa26039c_{invoice,wh,wha}`.
  - Kết quả: Viên 5004 / Vỉ 834 / Hộp 166.8 ở cả 2 bảng. Chờ khách huỷ PN653279.
  - Đã kiểm: chạy `php artisan stock:recalculate-report 1832 --drug_code=DQG00062116 --number=MPA26039C --agency=2957`
    (không --apply) trên api-01 → Tồn kiểm 870, Nhập sau kiểm 2.100 (PN652685), Bán 66, Tồn cuối 2.904 = đúng số
    sau khi huỷ PN653279. Code prod trùng md5 với local.
- [x] (07/11/2026) Huỷ PN653279 thay khách (anh Cường bảo làm)
  - Gọi đúng API màn Hoá đơn nhập hàng `POST /api/v2/invoice/update-status {id:3561722,status:cancel}` bằng tài
    khoản sphquocnam5723 (hỗ trợ cung cấp) → phiếu quỹ 2029678 tự chuyển cancel, bước tính lại tồn chạy.
  - Kết quả: PN653279 = cancel, PN652685 vẫn done. Tồn lô MPA26039C = 2.904 viên / 484 vỉ / 96,8 hộp ở cả
    warehouse và warehouse_agency; new_warehouse_logs ghi "Nhập sau kiểm=2100, Bán 66, Tồn cuối=2904" → khớp.
- [ ] Sửa code `recalculateStockFromReport` so mốc kiểm kho theo `invoice_detail.created_at` (chưa làm, chờ duyệt);
      còn 2 ca cùng lỗi: cơ sở 1007 PN638463, 2797 PN646326.
