# Serial vượt SL thiết bị lọt qua báo giá/HĐ + gắn nhầm serial KH khác — plan

Báo 26/11/2026 (SG): PNKQ TPSG.PNKQ.2026009973 (id 9973) duyệt KQ báo "PULI-KPL-U-D45:03 SL serial > SL thiết bị",
nhưng BGDV 11991 → HĐDV 7983 vẫn lập được. SG tăng SL thiết bị ngoài (external_equipments 2772) lên 2 để duyệt.

## Nguyên nhân (đã kiểm trên hrm_erp_gop)
1. Kiểm "SL serial > SL thiết bị" ở báo giá CHỈ có FE (`checkValidateSerialProducts`); BE lưu báo giá / HĐDV / PLBS
   không kiểm. Chỉ bước nhập/duyệt KQ có BE (`SerialValidationTrait::checkValidateSerial`).
   (Chưa xác định được SL thiết bị ngày lập BG 26/09 — không có lịch sử external_equipments.)
2. `Serial::insertSerial()` tìm serial ĐANG SỬ DỤNG chỉ theo TÊN toàn hệ thống → serial nhập mới "Tam1"/"Tam4"
   bị gắn vào serial 3317 (KH 7672, hàng 10328) / 3350 (KH 19687, hàng 27224). KH 17068 không có serial nào.
   Hệ thống đang coi tên serial là duy nhất (0 tên serial đang dùng trùng giữa các KH; danh mục serial chặn
   "Hệ thống đã tồn tại serial này") → KHÔNG tạo serial trùng tên, mà CHẶN ở validate.

## Phát hiện thêm 26/11 — phạm vi lớn
Quét HĐDV: 2.558 dòng sửa chữa (1.839 HĐ) + 477 dòng bảo dưỡng (194 HĐ) đang trỏ serial_id của KH KHÁC,
từ 08/2025 tới nay. Chủ yếu serial "giữ chỗ": '' (508), 'tạm' (484), 'Tam1' (370), '123', '1', 'Tạm 1', 'Tam2'...
Riêng 26/11 serial 3317 "Tam1" (KH 7672) bị gắn cho 5 HĐ của 4 KH khác (7983, 8924, 9034, 9099, 12947-bảo dưỡng).
→ User chốt 26/11: SG CẦN gõ serial giữ chỗ (không biết serial thật) → KHÔNG chặn trùng tên; `insertSerial` chỉ dùng lại
  serial cùng KH + cùng hàng, khác thì tạo serial mới cho KH đó (chấp nhận trùng tên giữa các KH).

## Tasks
- [x] ~~Chặn trùng tên serial KH khác~~ — đã gỡ theo user chốt
- [x] `Serial::insertSerial()`: dùng lại serial chỉ khi cùng `customer_id` + `product_id`; `WrAssignTask` 2 chỗ `$exist_serial`
      (đổi serial) cùng phạm vi. Test transaction+rollback: Tam1 cho KH 17068 → tạo mới 28154, gọi lại → dùng lại; KH 7672 → 3317
- [ ] (ngoài phạm vi, để nguyên) Request lắp đặt `WrImportResultRequest`/`AppRequest`/`WrApproveResultsStoreRequest` vẫn
      chặn "Serial đã tồn tại cho sản phẩm khác" theo tên toàn hệ thống
- [x] Trait: thêm `checkValidateSerialForDocument($request, $customer_id = null)` (gộp thiết bị cùng hàng, cộng SL)
- [x] Gọi ở BE: BGDV store/update, HĐDV store/update, PLBS store/update (chưa commit)
- [x] Script hrm_erp_gop: BG 11991 bị chặn "Tam1 đang dùng cho … TOYOTA BÌNH PHƯỚC"; 3 serial mới/thiết bị SL 2 bị chặn; 2 serial mới → qua
- [ ] Quét hồi quy BG gần đây (bỏ dở — getListProductOfCustomer chậm, >10 phút)
- [ ] Kiểm màn thật (BGDV/HĐDV/duyệt KQ)
- [x] Sửa dữ liệu hrm_erp_gop (= DB prod) 26/11: tạo serial 28157 Tam1 / 28158 Tam4 cho KH 17068 hàng 33890, trỏ lại
      HĐ 7983 (11512,11515), PDKQ 20441 (17833,17836), PNKQ 9973 (29150,29153). 4 HĐ khác cùng ngày + ~3.000 dòng cũ: CHƯA sửa (user chọn chỉ chuỗi 9973)
- [x] Commit/push develop_02 `ca55430d44` + gop_db `5c97d860f2` (26/11; gop_db chưa có chặn phường khoá → chỉ giữ phần serial)

### Checkpoint — 2026-11-26 (wrap up cuối ngày)
Vừa hoàn thành: chặn SL serial ở BE (BGDV/HĐDV/PLBS) + `insertSerial()` chỉ dùng lại serial cùng KH + cùng hàng; sửa data chuỗi PNKQ 9973 trên hrm_erp_gop; push develop_02 `ca55430d44` + gop_db `5c97d860f2`.
Đang làm dở: quét hồi quy BG gần đây (bỏ dở, query chậm >10 phút).
Bước tiếp theo: kiểm màn thật (BGDV/HĐDV/duyệt KQ); quyết có sửa 4 HĐ 8924/9034/9099/12947 + ~3.000 dòng cũ (2.558 sửa chữa / 477 bảo dưỡng) không; màn lắp đặt (HĐ hãng) vẫn chặn "Serial đã tồn tại cho sản phẩm khác" — để ngoài phạm vi.
Blocked: chờ user quyết phạm vi sửa dữ liệu cũ.
