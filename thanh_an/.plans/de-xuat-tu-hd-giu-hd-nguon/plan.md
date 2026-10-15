# Phiếu đề xuất lập từ HĐ đã kết xuất — giữ HĐ nguồn kể cả khi chưa chọn hàng

@khoipv — Bắt đầu 10/10/2026

## Bug
HĐ-182/2026 (dev) lập phiếu DXCU-2026-0059 từ màn "Hợp đồng đã kết xuất" nhưng cột "Phiếu đề xuất" trống.
Nguyên nhân: từ 30/09 (`de-xuat-tu-hd-khong-fill-hang`) bảng hàng để trống → phiếu gửi khi chưa chọn hàng bị
suy thành khách lẻ (type 3) → FE `buildPayload()` gửi `contract_id = null`, BE `store()/update()` cũng bỏ
`contract_id` với loại không bám HĐ → mất HĐ nguồn. Cột "Phiếu đề xuất" lại chỉ bám `supply_proposal_products.contract_id`.

## Phase 1 — BE
- [x] `SupplyProposalService::resolveType()`: thêm tham số HĐ nguồn — không có dòng hàng trong HĐ mà có HĐ nguồn → loại theo `contracts.type` của HĐ nguồn
- [x] `store()` / `update()`: truyền HĐ nguồn (`contract_id` request, update fallback `$model->contract_id`) vào `resolveType()`
- [x] `RenderedContractService`: `proposal_list` + `liveProposalSubquery()` nhận thêm phiếu có `sp.contract_id = contracts.id` (ngoài dòng hàng thuộc HĐ)

## Phase 2 — FE
- [x] `supply_proposals/add.vue` `effectiveType`: chưa có dòng hàng trong HĐ nhưng có HĐ nguồn → dùng `loadedType` (loại HĐ nguồn từ prefill / phiếu đã lưu)

## Phase 3 — Dữ liệu dev
- [ ] DXCU-2026-0059 không tự hiện lại (DB không lưu HĐ nguồn) — hỏi user có cập nhật tay `contract_id = 202` không

## Phase 4 — Verify
- [x] php -l các file BE
- [x] Test tinker (transaction + rollback): lưu phiếu từ HĐ không hàng → type theo HĐ, contract_id giữ; getList trả phiếu ở proposal_items

### Checkpoint — 10/10/2026
Vừa hoàn thành: sửa BE (resolveType nhận HĐ nguồn; proposal_list + liveProposalSubquery nhận sp.contract_id) + FE (effectiveType giữ loại HĐ nguồn khi chưa chọn hàng). Test script trên DB local (rollback): lập từ HĐ-191 không hàng → type=1, contract_id=216; sửa giữ HĐ nguồn; lập tay vẫn khách lẻ; cột Phiếu đề xuất + lọc Tiến độ + lọc mã phiếu đều ra phiếu mới.
Đang làm dở: —
Bước tiếp theo: user build client + test UI trên dev; quyết có cập nhật tay DXCU-2026-0059 → contract_id=202 không
Blocked:
