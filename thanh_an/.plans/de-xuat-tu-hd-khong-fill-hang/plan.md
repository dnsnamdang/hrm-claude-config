# Phiếu đề xuất lập từ HĐ đã kết xuất — không tự fill hàng hóa

@khoipv — Bắt đầu 30/09/2026

## Yêu cầu
- Lập phiếu đề xuất từ màn "Hợp đồng đã kết xuất" (`/supply/supply_proposals/add?contract_id=...`) KHÔNG tự điền toàn bộ hàng của HĐ nữa — bảng hàng hóa để trống, người dùng tự bấm chọn trong popup.
- Popup chọn hàng chỉ hiện hàng của HĐ nguồn + hàng trong danh mục, không hiện hàng HĐ khác của cùng khách.

## Phase 1 — FE
- [x] `add.vue` `loadContractPrefill()`: bỏ gán `formSubmit.products = d.products`, giữ loại/khách/HĐ nguồn; bỏ `loadProductInfo()` ở đây
- [x] Popup: xác nhận đã lọc ẩn hàng HĐ khác theo `sourceContractId` (có sẵn từ 23/09 — `GoodsPickerModal.filtered` + `contractOptions`), không cần sửa

## Phase 2 — BE
- [x] Giữ nguyên API `rendered-contracts/{id}/prefill` (vẫn dùng để chặn HĐ đã đề xuất đủ + lấy khách/loại/HĐ); FE chỉ không dùng `products`

### Checkpoint — 30/09/2026
Vừa hoàn thành: bỏ tự fill hàng ở loadContractPrefill
Đang làm dở: —
Bước tiếp theo: test UI — mở phiếu từ HĐ kết xuất, bảng trống, popup chỉ có hàng HĐ đó + danh mục
Blocked:
