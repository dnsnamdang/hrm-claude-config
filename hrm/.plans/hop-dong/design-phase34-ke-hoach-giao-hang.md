# Phase 34 — Kế hoạch giao hàng + Cảnh báo giao hàng (HĐ bán HRM)

Nguồn: **yêu cầu khách hàng** 10/11/2026 — "Kế hoạch giao hàng: hàng nào giao khi nào, ngày đích danh hoặc từ ngày…đến ngày" (mục 10)
và "Cảnh báo giao hàng: nhập số ngày cần cảnh báo… nếu tới ngày đó chưa giao, cảnh báo trước bao nhiêu ngày" (mục 8).
Đợt 3 phần (b)+(c), làm sau Phase 33 (d), trước (a) tiến độ thanh toán (mốc "Giao hàng" của (a) lấy từ đây).

## 1. Đã chốt (12/11)

| # | Câu | Chốt |
|---|---|---|
| K1 | Mức chi tiết | **Theo đợt giao**: mỗi đợt = 1 ngày hoặc khoảng ngày + các dòng hàng kèm SL đợt đó; 1 dòng chia được nhiều đợt |
| K2 | Khi nhập | **Trong form HĐ, bắt buộc khi gửi duyệt** (mọi dòng hàng xếp đủ SL). Sau khi ký: nút "Cập nhật kế hoạch giao hàng" (người lập, có lịch sử cũ→mới, không duyệt lại) |
| K3 | "Đã giao" | Theo **Biên bản giao nhận hàng hoá** (màn `/sale/handover-product-records`, bảng ERP `handover_acceptance_product_records`) — BBGN **Đã duyệt** |
| K4 | BBGN ↔ đợt | **Cộng dồn theo thứ tự đợt**: SL đã bàn giao của mỗi mặt hàng đắp vào các đợt theo ngày kế hoạch (sớm trước). Đợt đủ mọi mặt hàng ⇒ Đã giao; ngày giao = ngày của BBGN làm đủ. Không sửa màn BBGN |
| K5 | Số ngày cảnh báo N | **Nhập trên từng HĐ, bắt buộc** khi gửi duyệt, số nguyên ≥ 0, điền sẵn 3; áp mọi đợt của HĐ |
| K6 | Bắn khi nào / cho ai | Đợt chưa giao đủ: "Sắp đến hạn" khi còn đúng N ngày + "Quá hạn" ngày hôm sau mốc. Mốc = ngày đợt (khoảng ngày ⇒ ngày cuối). Người nhận: **người lập HĐ** |

## 2. Hiện có liên quan

- **BBGN** (của dev khác, nhánh `develop` → đã vào nhánh tester `gop_db-xuat-hang-cha-con`, CHƯA có trên `gop_db`):
  người lập HĐ tạo cho HĐ HRM đã có YCXH loại 21 xuất kho; dòng = **dòng hàng cha** HĐ (`hrm_contract_product_prices.parent_id IS NULL`)
  gộp theo `product_id-unit_id`; `handover_qty`, `handover_date` (đầu + từng dòng), `attachments`; trạng thái 1 Đang tạo / 2 Đã duyệt (người lập lưu "Đã duyệt" là chốt).
  `ContractDeliveredQtyService::handedOver()` cộng SL MỌI trạng thái (y ERP) ⇒ Phase 34 tự cộng riêng chỉ status 2.
- Màn xem HĐ đã có tab **Xuất hàng** (Phase 30, SL HĐ / đã yêu cầu / đã xuất theo dòng) — kế hoạch giao hàng đặt cạnh.
- Khuôn nút + popup sau ký: Phase 32 (`ContractExecutionBaseModal`, lịch sử meta cũ→mới). Lệnh nhắc: Phase 33 (`assign:warn-expiring-contracts`, `ContractNotificationService`).

## 3. Dữ liệu (đề xuất)

- `hrm_contracts.delivery_warning_days` smallint unsigned NULL (bảng riêng HRM).
- `hrm_contract_delivery_batches`: id, contract_id, sort_order, date_from, date_to (NULL = ngày đích danh), note, timestamps, created_by, updated_by.
- `hrm_contract_delivery_batch_items`: id, batch_id, contract_product_price_id (dòng cha), product_id, unit_id, qty.
- Không cột "đã giao" lưu cứng — tính lúc đọc từ BBGN (đổi/huỷ BBGN tự đúng). Lệnh nhắc ghi nhật ký đã gửi để không lặp: dùng so đúng ngày như Phase 33.

## 4. Nghiệp vụ

- **Gửi duyệt** (thêm vào `executionTermsErrors` cùng 1 lần 422): thiếu kế hoạch / dòng hàng xếp thiếu hoặc thừa SL / đợt thiếu ngày / `date_to < date_from`
  / thiếu N ⇒ lỗi dưới đúng ô. Lưu nháp không bắt.
- **Trạng thái đợt** (tính): Đã giao (đủ) · Quá hạn (qua mốc, chưa đủ) · Sắp đến hạn (còn ≤ N ngày) · Chưa giao.
  Hiện ở màn xem HĐ (khối Kế hoạch giao hàng, cột Đã bàn giao / Còn thiếu theo dòng + badge trạng thái từng đợt, màu theo 9 mã chuẩn).
- **Cập nhật sau ký** (HĐ KH đã ký / Có hiệu lực / Đang thực hiện, người lập): sửa đợt chưa giao đủ; không giảm SL đợt dưới SL đã bàn giao; tổng vẫn phải đủ SL HĐ.
- **Lệnh nhắc** `assign:warn-delivery-batches` 08:00: `[HDB] Sắp đến hạn: <mã HĐ>. Giao hàng đợt 2 ngày 20/12/2026 (còn 3 ngày)` ·
  `[HDB] Quá hạn: <mã HĐ>. Giao hàng đợt 2 hạn 20/12/2026 chưa đủ`. HĐ ở Có hiệu lực / Đang thực hiện.
- Phụ lục HĐ / HĐ dịch vụ: ngoài phạm vi (HĐ bán HRM chưa có phụ lục).

## 5. Câu kỹ thuật còn mở (tự chốt khi lập plan, không cần user)

- **Nhánh:** BBGN chưa có trên `gop_db` ⇒ Phase 34 phải làm trên nhánh có BBGN. Đề xuất nhánh mới tách từ `origin/gop_db-xuat-hang-cha-con`
  (hoặc merge `develop` vào `gop_db-hd-dieu-kien-duyet`) — **hỏi user khi xin "làm"**.
- Dòng HĐ trùng `product_id-unit_id` ở 2 dòng cha: BBGN gộp chung ⇒ đắp theo thứ tự đợt rồi thứ tự dòng.
- Mockup khối Kế hoạch giao hàng (form Sửa + màn xem) làm trước khi code.
- Dòng **dịch vụ** (`hrm_contract_service_items`) KHÔNG vào kế hoạch giao hàng: BBGN chỉ có hàng hoá (dòng cha `hrm_contract_product_prices`). Ghi rõ ở mockup.
- Mockup bản 2 (12/11, góp ý user): popup Thêm/Sửa đợt có bảng chọn hàng (tick ⇒ tự điền SL còn lại, "Lấy hết phần còn lại"), kiểm SL ngay khi gõ
  (≤ còn lại, > 0), ngày / khoảng ngày (đến ≥ từ); ma trận sửa nhanh, vượt SL HĐ đỏ; Gửi duyệt báo mọi lỗi cùng lúc. `mockup-ke-hoach-giao-hang.html`.
- **Chốt 12/11 (user): giao hàng chỉ quan tâm HÀNG CHA** — kế hoạch, ma trận, đối chiếu BBGN chỉ dùng dòng cha (`hrm_contract_product_prices.parent_id IS NULL`);
  hàng con không hiện, không xếp đợt, không tính đã giao (đi theo cha). Khớp nguồn dòng của BBGN.
