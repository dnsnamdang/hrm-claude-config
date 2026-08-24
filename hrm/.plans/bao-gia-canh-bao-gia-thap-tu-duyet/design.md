# Báo giá — Cảnh báo đơn giá ≤ 1.000 & tự động duyệt (Redmine #10797)

@dnsnamdang · nhánh `tpe-develop-assign` · 2026-08-17

## Mục tiêu

1. Khi bấm **Trình duyệt**: rà đơn giá bán từng dòng hàng hoá; dòng nào ≤ 1.000 đ thì tô nền cam +
   hiện popup cảnh báo liệt kê mã/tên hàng, cho user chọn *Quay lại chỉnh sửa* hoặc *Tiếp tục trình duyệt*.
2. Đổi logic phê duyệt: báo giá "sạch" thì **tự động duyệt**, còn lại giữ luồng duyệt phân cấp cũ.

## Quyết định đã chốt (user xác nhận 2026-08-17)

1. **Không có khái niệm "hàng khuyến mại" trong hệ thống** (bảng `discount_types` chỉ có 1 loại
   "Giảm giá tổng đơn") → **cảnh báo TẤT CẢ** dòng hàng hoá có đơn giá bán ≤ 1.000, không trừ dòng nào.
2. **TH1 ĐÈ cấp duyệt**: thoả điều kiện là tự duyệt ngay, kể cả báo giá vốn thuộc cấp 2 (TP) hay
   cấp 3 (TP + BGĐ).
3. **Chữ/màu/icon nút theo `button-convention`, KHÔNG theo nguyên văn spec** (user chốt 2026-08-17):
   spec ghi "Tiếp tục trình duyệt" / "Quay lại chỉnh sửa" → thực tế đặt **"Tiếp tục gửi duyệt"**
   (`primary status="warning"`, icon `ri-send-plane-line` — nhóm Gửi duyệt = cam) và **"Quay lại"**
   (`tertiary`, `fas fa-arrow-left`). Bảng text chuẩn cấm chữ "Trình duyệt"; nút ở footer màn cũng
   đang ghi "Gửi duyệt" nên để "Trình duyệt" là lệch ngay trong cùng 1 màn.
4. Cảnh báo **không chặn** trình duyệt — user vẫn bấm "Tiếp tục trình duyệt" được (spec).

## Điều kiện tự động duyệt (TH1)

Tất cả các mệnh đề sau đúng (`QuotationService::isAutoApprovable()`):

- `discount_method = null` **và** `total_discount = 0` **và** không có dòng `quotation_discounts`;
- Mọi dòng hàng hoá có `erp_product_id` (không hàng tạm);
- Mọi dòng dịch vụ có `cost_id` (không dịch vụ tạm);
- Mọi đơn giá bán (hàng hoá lẫn dịch vụ) **> 1.000 đ**;
- Báo giá không rỗng.

Không thoả → **TH2**: giữ nguyên `calculateApprovalLevel()` theo giá trị đơn + tỷ suất LN như cũ.

## Thay đổi

| Lớp | File | Nội dung |
| --- | --- | --- |
| BE | `Modules/Assign/Services/QuotationService.php` | `LOW_PRICE_THRESHOLD = 1000`; `isAutoApprovable()`; `calculateLevel()` ép `level = 1` và trả thêm `auto_approve` khi thoả TH1 |
| FE | `components/assign/quotation/QuotationLowPriceWarningModal.vue` (mới) | Popup cảnh báo: header icon cam, số lượng vi phạm, bảng Mã / Tên / Đơn giá bán, 2 nút *Tiếp tục gửi duyệt* + *Quay lại*, footer ghim đáy |
| FE | `pages/assign/quotations/_id/edit.vue` | computed `lowPriceItems` / `lowPriceKeySet`, method `isLowPriceRow`, class `.low-price-row` (nền `#ffedd5`); `openSubmit()` chèn bước cảnh báo trước khi mở popup gửi duyệt |
| FE | `components/assign/quotation/QuotationSubmitModal.vue` | Đọc `auto_approve`, hiển thị "Tự động duyệt" thay cho "Cấp N" + câu giải thích |

## Luồng Trình duyệt sau thay đổi

```
Bấm Trình duyệt → Lưu (strict) → kiểm Mỏ neo
   └─ có dòng ≤ 1.000 → tô nền cam + popup cảnh báo
          ├─ Quay lại → đóng popup, giữ nguyên màn (dòng vi phạm vẫn nền cam)
          └─ Tiếp tục gửi duyệt → popup gửi duyệt
   └─ không có → popup gửi duyệt
Popup gửi duyệt → calculate-level (đã gồm auto_approve)
   ├─ auto_approve / cấp 1 → submit + self-approve → Đã duyệt
   └─ cấp 2/3 → submit → Chờ TP duyệt
```

## Lưu ý

- BE **không chặn** báo giá có dòng ≤ 1.000 — chỉ FE cảnh báo; nhưng những báo giá đó **không bao giờ
  tự duyệt** (điều kiện TH1 loại chúng ra), nên vẫn đi qua TP/BGĐ.
- Dòng con của combo cũng được tính (đơn giá con = 0 chính là ca "chưa cập nhật giá bán" cần bắt);
  `ensureAllPricesPositive()` hiện chỉ chặn dòng cha nên dòng con vẫn có thể = 0.

## Điều kiện nghiệm thu (theo Redmine)

- AC1 — báo giá toàn hàng ERP, không GG → không cảnh báo, tự động duyệt ✅
- AC2 — có hàng ≤ 1.000 → highlight cam + popup có Mã/Tên ✅
- AC3 — "Quay lại" (spec gọi "Quay lại chỉnh sửa") → đóng popup, giữ nguyên màn ✅
- AC4 — "Tiếp tục gửi duyệt" (spec gọi "Tiếp tục trình duyệt") → sang popup phê duyệt ✅
- AC5 — có hàng tạm / dịch vụ tạm / GG → đi luồng duyệt phân cấp ✅
