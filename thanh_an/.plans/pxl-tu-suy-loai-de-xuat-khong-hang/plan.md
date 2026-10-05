# PXL tự suy loại khi đề xuất KH chưa có hàng hóa

@khoipv — Bắt đầu 01/10/2026 · Design: [design.md](design.md)

## Phase 1 — BE
- [x] `SupplyProposal::handlingResolvesType()` — đề xuất khách lẻ + không có dòng hàng
- [x] `SupplyHandlingService`: `resolveType()` + dùng ở `store()` (type + submitStatus)
- [x] `SupplyHandlingService::update()`: phiếu thuộc diện tự suy → cập nhật lại `type` theo hàng
- [x] `DetailSupplyHandlingResource`: thêm `type_from_goods`

## Phase 2 — FE `pages/supply/supply_handlings/add.vue`
- [x] Cờ `typeFromGoods` (add: tính từ đề xuất; edit/show: từ BE) + `loadedType`
- [x] `resolvedType` + watcher cập nhật `formSubmit.type`, reset `don_gia` khi rời khách lẻ, nạp lại product-info
- [x] `loadGoodsPool`: diện tự suy gửi `group` + `customer_id`
- [x] Popup: không truyền `type` khi tự suy; `mapPoolItem` giữ `contract_type`
- [x] Header "Loại": chưa có hàng → "Chưa xác định", có ghi chú "Tự xác định theo hàng hóa chọn"

## Phase 3 — Kiểm tra
- [ ] Đề xuất KH chỉ chọn khách → PXL chọn hàng HĐ trong thầu → loại "Cung ứng cho KH", lưu đúng type 1
- [ ] Chọn hàng HĐ đặt/mượn → type 4; chỉ hàng ngoài HĐ → type 3 (cột khách lẻ)
- [ ] Đề xuất có hàng / nội bộ: PXL giữ nguyên như cũ

### Checkpoint — 01/10/2026
Vừa hoàn thành: BE (`handlingResolvesType`, `SupplyHandlingService::resolveType` dùng ở store/update, cờ `type_from_goods`) + FE add.vue (pool theo group, `resolvedType` + watcher, popup không truyền type, header "Loại"). php -l OK; template/script compile OK; script thử: DXCU-2026-0038 (khách lẻ không hàng) resolves=true, DXCU-2026-0024 (có hàng) false; HĐ trong thầu → 1, HĐ nguyên tắc → 6, ngoài HĐ/không hàng → 3
Đang làm dở: —
Bước tiếp theo: test UI Phase 3 trên DXCU-2026-0038
Blocked:
