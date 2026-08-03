# Thanh lý HĐ — Giá trị thực tế & chặn thanh lý — Design (tóm tắt)

- **Người phụ trách:** @khoipv
- **Ngày:** 2026-07-01
- **Spec chi tiết:** `docs/superpowers/specs/2026-07-01-contract-liquidation-actual-value-design.md`

## Mục tiêu
Thêm ô **"Giá trị thực tế"** (bắt buộc) vào biên bản thanh lý (`contract/contract_liquidation`). So sánh với **số tiền đã nghiệm thu lũy kế** (`summary.total_performed`):
- Chưa có BBNT đã duyệt (`bbnt_list.length = 0`) → bỏ qua so sánh, cho lập.
- Đã có ≥1 BBNT → nếu `total_performed < actual_value` thì **chặn** lập/lưu thanh lý.

## Quyết định lớn
- Lưu cột mới `actual_value` (decimal 18,2) trên `contract_liquidations`, hiển thị lại ở chi tiết/duyệt.
- Chặn ở **mọi nút lưu** (nháp + gửi/duyệt); enforce cả FE lẫn BE (BE là nguồn chân lý — guard trong `ContractLiquidationService`).
- Ô đặt ở **Bước 2**, **luôn bắt buộc** nhập.
- So sánh **strict less-than** ("nhỏ hơn").

## File thay đổi
BE: migration (mới), `ContractLiquidation.php`, `StoreContractLiquidationRequest.php`, `ContractLiquidationService.php`, `ContractLiquidationDetailResource.php`.
FE: `pages/contract/contract_liquidation/components/ContractLiquidationForm.vue`.

## Không đụng
`updateSupplement` / luồng bổ sung, logic tổng hợp BBNT, snapshot hóa đơn/hàng hóa, phân quyền.
