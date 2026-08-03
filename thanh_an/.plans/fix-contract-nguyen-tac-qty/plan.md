# Fix: HĐ Nguyên tắc bị tính giá trị hợp đồng (SL lọt = 1)

**Người phụ trách:** @namdangit
**Ngày:** 2026-07-22

## Bối cảnh / Root cause

HĐ loại **Nguyên tắc (type=5)** là HĐ khung — chỉ chốt đơn giá, KHÔNG cam kết số lượng → giá trị hợp đồng phải = 0 (Σ qty×price với qty=0).

Phát hiện thực tế ở HĐ 371 (`https://demothanhan.dnsmedia.vn/contract/contract/371`): giá trị hiển thị **4.181.000** = tổng thành tiền của **7 dòng nhóm I** (`product_id` 1097–1103) bị `qty = 1`. Truy nguồn: **báo giá gốc BG-472 đã có sẵn 7 dòng qty=1**; khi tạo HĐ nguyên tắc, qty bị bê nguyên sang, không nơi nào ép về 0.

3 điểm để lọt:
1. BE `ContractService::syncGroups` (`Modules/Category/Services/ContractService.php:474-476`) — `$product['qty'] = $product['qty'] ?? 0` là **no-op** khi qty≠null. `amount` không đụng tới. → **chốt chặn cuối, mọi đường ghi contract_products đều qua đây.**
2. FE `GeneralComponent::onQuotationChange` (`pages/contract/contract/components/GeneralComponent.vue` ~2363) — spread `...product` bê `qty` từ báo giá.
3. FE `ProductComponent::handleImportSuccess` (`pages/contract/contract/components/ProductComponent.vue` ~2291, ~2342) — import Excel set qty/amount từ file, không ép 0 cho type 5.

## Task

- [x] BE: `syncGroups` — với type 5, hard-set `qty = 0` và `amount = 0` (thay `?? 0`) — `ContractService.php:474-480`
- [x] FE: `onQuotationChange` — với type 5, set `qty: 0` khi build product từ báo giá — `GeneralComponent.vue:2383`
- [x] FE: `handleImportSuccess` — với type 5, ép `qty: 0`, `amount: 0` (normalize 1 chỗ sau build, bao cả 2 nhánh) — `ProductComponent.vue:2424`
- [ ] Verify: tạo/sửa HĐ nguyên tắc → giá trị = 0; kiểm HĐ 371 sau khi mở-lưu lại (CẦN Nuxt dev + tài khoản test)
- [ ] (Tùy chọn) Dọn data 7 dòng HĐ 371 hiện tại: mở HĐ bấm Lưu (nay syncGroups tự ép 0)

## Ghi chú
- Không đụng type 3/4 (Cho/Tặng, Đặt/Mượn) — field giá trị đã ẩn sẵn, không có triệu chứng. Có cùng pattern `?? 0` latent nhưng để ngoài scope.
- Migration: không.

### Checkpoint — 2026-07-22
Vừa hoàn thành: sửa xong 3 điểm code (BE syncGroups + FE onQuotationChange + FE handleImportSuccess), php -l BE PASS
Đang làm dở: —
Bước tiếp theo: user bật Nuxt dev → verify UI (tạo HĐ nguyên tắc từ báo giá có qty → giá trị = 0; mở-lưu lại HĐ 371 → hết 4.181.000)
Blocked: cần Nuxt dev + tài khoản test để E2E
