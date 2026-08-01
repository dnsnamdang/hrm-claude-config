# Nhập 2 chiều Số tiền ↔ Tỷ lệ % — bảng "Thanh toán theo đợt"

**Người phụ trách:** @namdangit
**Ngày:** 2026-07-27
**Phạm vi:** Chỉ FE. Không migration (DB `contract_payment_installments` đã có sẵn cả 2 cột `percent` + `amount`).
**File:** `hrm-thanhan-client/pages/contract/contract/components/PaymentBlockCard.vue`

## Bối cảnh
Màn `contract/contract/{id}/edit` (vd 202) → tab "Điều khoản thanh toán" → mode "Thanh toán theo đợt".
Hiện tại cột "Số tiền" chỉ đọc (`amountOf` = % × tổng). User muốn nhập được số tiền → tự suy ra %.

## Quyết định thiết kế (user đã duyệt)
- **Số tiền là giá trị gốc được lưu**; % là giá trị suy ra để hiển thị/nhập nhanh.
- 2 chiều: gõ % → `amount = round(%/100 × tổng)`; gõ tiền → `percent = round(tiền/tổng × 100, 2 số lẻ)`.
- Tổng HĐ đổi → **giữ số tiền**, tính lại %.
- Giữ nguyên cảnh báo mềm "tổng % nên = 100%". **KHÔNG** thêm cảnh báo tổng tiền.
- Tổng HĐ = 0 → % = 0 (không chia 0).

## Task
- [x] 1. Đổi cột "Số tiền (VNĐ)" từ ô read-only → `currency-input` (format nghìn, canh phải, trả Number) — giống tab Hàng hóa.
- [x] 2. Thêm helper `calcAmount(percent)` + `calcPercent(amount)` (guard chia 0, làm tròn % 2 số lẻ).
- [x] 3. `onRowInput`: nhánh `percent` → set amount; nhánh `amount` → set percent.
- [x] 4. `buildRows` thêm field `amount` (đọc `r.amount`, fallback tính từ percent).
- [x] 5. `addInstallment` thêm `amount: null`; `emitUpdate` gửi `amount` = giá trị người dùng (không tính lại).
- [x] 6. Watch `baseTotal` → tính lại `percent` từ `amount` cho từng dòng (giữ tiền).
- [x] 7. `sumAmount` = tổng `row.amount`. Xóa `amountOf` cũ.
- [ ] 8. Verify: user E2E qua UI (dev server chưa chạy).

## Task bổ sung (2026-07-27) — ràng buộc chặn
- [x] 9. Ô nhập tiền dùng `currency-input` (format nghìn) như tab Hàng hóa.
- [x] 10. Clamp khi nhập: gõ % hoặc tiền vượt → tự cắt xuống mức còn lại (`otherAmount`/`maxAmount`), tổng không vượt 100% / giá trị HĐ.
- [x] 11. Cảnh báo đỏ đổi thành "phải bằng đúng 100% giá trị HĐ mới lưu được" (so theo `sumAmount !== roundedBase`).
- [x] 12. `GeneralComponent.validateInstallments()` — mỗi khối mode 'dot' phải có Σtiền = đúng giá trị khối (main + kpi nếu has_kpi). Trả mảng lỗi.
- [x] 13. Chặn lưu ở `add.vue` + `_id/edit.vue`: gọi validateInstallments trước dispatch, có lỗi → toast + return (chặn cả Lưu và Lưu-gửi).
- [x] 14. Cảnh báo tại bảng: đổi dòng text nhỏ → khung alert đỏ `.pbc-warning`, hiện cả khi chưa có đợt, ghi rõ còn thiếu/đang vượt bao nhiêu tiền (toast dễ trôi nên báo cố định ở bảng).
- [ ] 15. User E2E qua UI.

## Checkpoint — 2026-07-27 (đợt 2)
Vừa hoàn thành: Task 1–13.
- `PaymentBlockCard.vue`: currency-input + clamp 2 chiều (không cho vượt) + cảnh báo theo tiền + computed roundedBase.
- `GeneralComponent.vue`: method `validateInstallments()`.
- `add.vue` + `_id/edit.vue`: chặn lưu khi Σđợt ≠ đúng giá trị HĐ.
Đang làm dở: (không)
Bước tiếp theo: User chạy dev server test `contract/contract/202/edit`: (1) nhập vượt bị tự cắt; (2) tổng < 100% → bấm Lưu bị chặn + toast; (3) đủ đúng 100% → lưu OK; (4) khối KPI (nếu có) kiểm riêng.
Blocked: (không)

## Ghi chú kỹ thuật
- Khi tổng giá trị HĐ giảm sau khi đã nhập đợt (thay đổi ngoài input) → số tiền GIỮ NGUYÊN, chỉ % tính lại; nếu vượt thì cảnh báo đỏ + chặn lưu (không auto-cắt vì là thay đổi ngoài thao tác nhập). User tự chỉnh lại.
- Chưa áp cho màn phụ lục (`contract_annex_payment_terms`) — user chỉ yêu cầu màn HĐ. PaymentBlockCard dùng chung nên clamp tự có ở phụ lục, nhưng chặn-lưu ở submit phụ lục CHƯA wire.
