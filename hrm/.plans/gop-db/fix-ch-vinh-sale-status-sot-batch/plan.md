# Fix CH Vinh (cty 3) sót trạng thái giá sau gộp DB — hàng ETGN-EG-IE010010061 (43782)

**Loại:** Data-fix trên production `hrm_erp_gop` (hrm.eteksofts.com). KHÔNG đổi code.

## Hiện tượng (user báo 2026-11-02)
Màn `master-data/products/entering` tại CH Vinh (cty 3) hiện hàng **ETGN-EG-IE010010061**
vẫn "Chờ tính giá bán" (status 2), trong khi mong đợi "Đang kinh doanh".

## Nguyên nhân gốc
Hàng 43782, công ty quản lý = cty 9 (ETEK GREEN). Giá đã tính ở cty 1 (chuỗi
PYCHG-00373 → PTG). Batch **gộp DB** lúc `2026-10-22 05:09:49` set status **3 (Đang kinh
doanh)** + điền `min_stock_qty=0/guarantee=0/guarantee_type='thang'/info_entered_at` cho
cty 1,2,4,8,9 (coefficient=1.0 ⇒ kế thừa giá cty quản lý). **Cty 3 bị sót** vì hôm trước
(2026-10-21) user 407 đã tạo dòng cty 3 + gửi YCHG **PYCHG-04693** → đẩy status sang 2, nên
batch quét theo trạng thái mặc định không trúng.

Hệ quả phụ: PYCHG-04693 thành phiếu treo — header status 10 (Đang hỏi giá), nhóm duy nhất
4417 status 1 (Chờ lập YCTG) nhưng **rỗng** (hàng đã bị gỡ khỏi nhóm). Hàng 43782 không còn
nằm trong YCHG cty 3 nào ⇒ không hủy phiếu để revert được, không thêm vào YCHG mới được
(picker chặn status 2), không lập YCTG được (nhóm rỗng). ⇒ kẹt, phải chạm dữ liệu.

## Hướng xử lý — Hướng A (user chốt 2026-11-02): CH Vinh KẾ THỪA giá như cty 2/4/8
Không lập phiếu mới. Đưa dòng cty 3 về đúng chuẩn batch gộp DB + dọn phiếu treo.

- [x] **T1 — Lật trạng thái + điền default cho dòng cty 3** (`product_company_coefficients`
      id 117530): status 2→3, min_stock_qty=0, guarantee=0, guarantee_type='thang',
      info_entered_at='2026-10-22 05:09:49', updated_by=407, updated_at=now.
- [x] **T2 — Ghi lịch sử hàng hoá** (`catalog_histories`): action `change_status`,
      old `{"c3|Trạng thái":"Chờ tính giá bán"}` → new `{"c3|Trạng thái":"Đang kinh doanh"}`,
      note "Khớp batch gộp DB — kế thừa giá công ty quản lý (sót cty 3)", changed_by=407.
- [x] **T3 — Dọn phiếu treo PYCHG-04693** theo đúng luồng `xnkCancel`:
      group 4417 → status 6 (CANCELLED) + close_reason/closed_by=407/closed_at;
      header 4693 → status 9 (Không có giá) (refreshHead: mọi nhóm đóng, không nhóm nào
      có giá); +1 dòng `price_asking_request_approve_histories` type='Huỷ duyệt'.
- [x] **T4 — Verify**: pcc cty3 = status 3 giống 5 cty kia; PYCHG-04693 không còn ở danh
      sách "Đang hỏi giá"; màn `products/entering` CH Vinh hiện "Đang kinh doanh".

## Ghi chú an toàn
Chạy trong 1 transaction, mỗi UPDATE có WHERE khoá cứng id + điều kiện trạng thái hiện tại
(idempotent, không đụng dòng đã đúng). Actor = 407 (chính người tạo dòng + phiếu).

## Lượt 2 (2026-11-02) — 3 hàng cùng CH Vinh, CÙNG root cause (PYCHG-04693)
Lịch sử xác nhận cả 3 bị PYCHG-04693 đẩy cty3→status 2 (15:05:27). Phiếu PYCHG-04693 đã dọn
ở lượt 1 nên 3 hàng này đều **mồ côi** (không còn dòng YCHG cty 3) ⇒ chỉ cần lật status, KHÔNG
dọn phiếu. 47902 còn 2 dòng YCHG của cty 1 (PYCHG-03241/04697, đã PRICED) — không đụng.

- [x] 37545 `ETGN-EG-EQ9233-1` — cty3 2→3 + default + history (cty4 coef 1.073 giữ nguyên).
- [x] 43622 `ETGN-EG-IE010010025` — cty3 2→3 + default + history.
- [x] 47902 `ETGN-EG-IE010010060:01` — cty3 2→3 + default + history (KHÁC id 43781
      `ETGN-EG-IE010010060` đã sẵn status 3).
- [x] Verify 3 hàng cty3 = status 3; rời màn entering sang màn Đang kinh doanh.

## Lượt 3 (2026-11-02) — GIÁ cty3 vẫn = 0 dù status 3 (user phản hồi)
User báo EG (cty 9) đã có giá nhưng CH Vinh (cty 3) hiện **toàn 0** dù badge "Kế thừa - EG".

**Nguyên nhân:** kế thừa giá là chép VẬT LÝ vào `product_unit_prices` theo từng cty (mỗi cty 6 dòng
giá / ĐVT). Màn "Cập nhật giá bán" đọc đúng dòng cty đang xem, KHÔNG fallback → cty3 có dòng nhưng
toàn 0 nên hiện 0. Lượt 1+2 mới lật status, CHƯA chép giá. cty3 không có `inherited_price_factors`
⇒ k=1 ⇒ phải chép verbatim giá cty9 (bằng siblings cty 2/4/8).

Đã dựng sẵn SQL mô phỏng `InheritedPriceSync::updatePrices` (UPDATE 24 dòng + INSERT 1 dòng
`product_expected_prices` cho 47902) nhưng **KHÔNG CHẠY**.

- [x] **User tự sửa xong GIÁ cty3 qua giao diện** (2026-11-02) — không cần data-fix SQL. Đóng việc.
