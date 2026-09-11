# Kết xuất hợp đồng sang cung ứng — Design (tóm tắt)

- Phụ trách: @khoipv · Bắt đầu 2026-08-26
- **Spec đầy đủ:** `docs/superpowers/specs/2026-08-26-contract-render-supply-design.md`

## Mục tiêu

Nối phân hệ Hợp đồng (bán) sang Cung ứng: HĐ bán đã duyệt được "kết xuất" sang một màn danh
sách mới bên Cung ứng, từ đó lập Phiếu đề xuất cung ứng với dữ liệu điền sẵn từ HĐ.

## Luồng

HĐ đã duyệt → nút **Kết xuất** ở dòng danh sách HĐ → màn `/contract/contract/{id}/render`
(mở sửa **Kết quả** + **Điều khoản thanh toán**, validate bắt buộc) → HĐ hiện ở
`/supply/contract_render` "Hợp đồng đã kết xuất" → **Tạo phiếu đề xuất**
(`/supply/supply_proposals/add?contract_id=X`, prefill KH + toàn bộ hàng HĐ) → lưu phiếu thì
HĐ ẩn khỏi danh sách; xóa phiếu thì HĐ hiện lại.

## Quyết định lớn

1. **Lưu cờ trên `contracts`** (`supply_rendered_at`, `supply_rendered_by`) + `supply_proposals.contract_id`,
   không bảng nối. "Ẩn khi đã có phiếu" tính bằng `NOT EXISTS` trên `supply_proposals` chưa xóa mềm
   → xóa phiếu là HĐ tự hiện lại, không phải đồng bộ cờ.
2. **Điều kiện kết xuất:** `status = 3` (đã duyệt) + `record_type = 2` (Hợp đồng) + chưa kết xuất.
3. **Bắt buộc trước khi kết xuất:** Kết quả = *Thực hiện* (chặn "Không thực hiện") và có Điều khoản
   thanh toán cho khối main (+ khối KPI nếu `has_kpi = 1`). Cho sửa ngay tại màn kết xuất rồi lưu vào HĐ.
4. **1 HĐ ↔ 1 phiếu đề xuất còn sống**, BE chặn lập phiếu thứ 2 (400).
5. **Chưa gắn phân quyền** (user bổ sung sau) — không seed quyền, không phân quyền theo cấp.
6. Menu Cung ứng: mục phẳng "Hợp đồng đã kết xuất" ngay trước "Phiếu đề xuất cung ứng".
7. Trên dòng chỉ có 2 hành động: Tạo phiếu đề xuất · Xem chi tiết HĐ (không có trả kết xuất).

## Phạm vi kỹ thuật

- **DB:** 2 migration, chỉ index (không khóa ngoại).
- **BE Category:** route + `ContractController::renderSupply` + `ContractService::renderSupply`
  (tái dùng `updatePaymentTermsAfterApprove`) + Request mới + `ContractResource` thêm `can_render_supply`.
- **BE Supply:** `RenderedContractController/Service/Resource` mới (list + prefill);
  `SupplyProposalService` nhận `contract_id` + guard trùng phiếu; tách `contractProductRows()` dùng chung với `goodsPool()`.
- **FE:** menu · nút Kết xuất ở list HĐ · màn `_id/render.vue` mới · prop `isRender` cho
  `GeneralComponent` HĐ · màn `supply/contract_render/index.vue` mới · prefill ở `supply_proposals/add.vue`.

## Ngoài phạm vi

Phân quyền, trả kết xuất, lịch sử nhiều phiếu/HĐ, trừ SL đã đề xuất trên HĐ, kết xuất hàng loạt.
