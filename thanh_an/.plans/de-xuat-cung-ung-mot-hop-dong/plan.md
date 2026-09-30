# 1 phiếu đề xuất chỉ bám 1 hợp đồng — PLAN

**Người phụ trách:** @khoipv · **Ngày tạo:** 23/09/2026
**Design:** [design.md](design.md) · **Spec:** [../../docs/superpowers/specs/2026-09-23-de-xuat-cung-ung-mot-hop-dong-design.md](../../docs/superpowers/specs/2026-09-23-de-xuat-cung-ung-mot-hop-dong-design.md)

## Trạng thái: đã chốt yêu cầu — đang code

## Phase 0 — Chốt yêu cầu
- [x] Áp dụng cho các loại bám HĐ: 1 (cho KH), 4 (đặt/mượn), 5 (trao tặng), 6 (nguyên tắc)
- [x] Hàng NGOÀI hợp đồng vẫn chọn thoải mái, không giới hạn
- [x] Cách chặn: **khóa mềm theo hàng đã chọn** — chưa có hàng trong HĐ thì popup hiện tất cả;
      khi phiếu (hoặc lần tick hiện tại) đã dính HĐ A thì dòng của HĐ khác bị làm mờ + nhãn
      "HĐ khác", không tick được. Xóa hết hàng của HĐ A → mở lại.
- [x] `supply_proposals.contract_id` (cấp phiếu) tự suy từ hàng đã chọn khi lưu
- [x] Dữ liệu cũ: stag chỉ có `DXCU-2026-0023` dính 2 HĐ, status 9 (Đã xử lý) → không sửa được nữa,
      không cần migration

## Phase 1 — FE
- [x] `GoodsPickerModal.vue`: prop `lockedContractId`, computed `activeContractId`
      (HĐ của phiếu → nếu chưa có thì HĐ của dòng đầu tiên vừa tick), `isOtherContract()`
- [x] `GoodsPickerModal.vue`: disable checkbox + làm mờ dòng + nhãn "HĐ khác"; `selectable` /
      `selectableAll` loại dòng bị khóa; "Chọn tất cả" chỉ ăn HĐ gặp đầu tiên + hàng ngoài HĐ
- [x] `add.vue`: computed `lockedContractId` (từ `products`, fallback `formSubmit.contract_id`),
      truyền xuống popup
- [x] `add.vue`: `onPickConfirm` chặn thêm lần nữa (phòng khi lọt), toast báo tên hàng bị bỏ
- [x] `add.vue`: `buildPayload` gửi `contract_id` suy từ hàng đã chọn (KHÔNG set vào `formSubmit`
      vì `isFromContract` đang phụ thuộc field này → set vào sẽ khóa nhầm ô Loại/Khách hàng)

## Phase 2 — BE (chốt chặn cuối)
- [x] `SupplyProposalService::resolveContractId($items, $fallback)`: gom `contract_id` distinct của
      các dòng `in_contract`; >1 → throw "Mỗi phiếu đề xuất chỉ được chọn hàng hóa của 1 hợp đồng."
- [x] `store()` / `update()`: dùng hàm trên thay cho `$request->input('contract_id')`

## Phase 3 — Verify
- [x] `php -l` file BE sửa
- [x] compile template FE sửa
- [ ] User build client + test tay

## Phase 4 — Phiếu có HĐ nguồn thì ẩn hẳn hàng HĐ khác (23/09/2026)
- [x] Chốt: `supply_proposals.contract_id` = **HĐ NGUỒN** (phiếu lập từ màn Kết xuất hợp đồng),
      KHÔNG suy từ hàng đã chọn → revert phần suy ở Phase 1/2 (suy vào sẽ bật nhầm `isFromContract`
      bên FE khi mở sửa phiếu lập tay: khóa ô Loại đề xuất / Khách hàng + chạy thừa
      `assertContractHasRemaining`)
- [x] BE: `resolveContractId()` → đổi thành `assertSingleContract($items)` chỉ validate (throw khi
      hàng dính ≥ 2 HĐ); `store()`/`update()` gọi assert rồi lưu `contract_id` như cũ
- [x] FE `add.vue`: computed `sourceContractId`, `buildPayload` trả lại `formSubmit.contract_id`
- [x] FE `GoodsPickerModal.vue`: prop `sourceContractId` → `filtered` ẩn hẳn dòng của HĐ khác,
      bộ lọc HĐ chỉ còn HĐ nguồn, banner đổi chữ "chỉ hiện hàng của hợp đồng này và hàng trong danh mục"
- [x] `php -l` + compile template lại

### Checkpoint — 23/09/2026
Vừa hoàn thành: Phase 1 (FE) + Phase 2 (BE) + Phase 3 verify + Phase 4 (HĐ nguồn ẩn hẳn hàng HĐ khác).
Đang làm dở: không.
Bước tiếp theo: user build lại client + hard refresh, lập 1 phiếu loại bám HĐ cho khách có >= 2 HĐ:
tick hàng HĐ A → dòng HĐ B phải mờ + nhãn "HĐ khác"; hàng ngoài HĐ vẫn tick được; xóa hết hàng HĐ A
→ mở lại HĐ B; bấm "Chọn tất cả" chỉ ăn 1 HĐ. Thêm: vào từ màn Kết xuất hợp đồng → popup KHÔNG
còn dòng của HĐ khác (không phải chỉ mờ).
Blocked: (trống)
