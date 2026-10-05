# Thêm 3 loại đề xuất cung ứng theo loại hợp đồng — PLAN

**Người phụ trách:** @khoipv · **Ngày tạo:** 22/09/2026

## Trạng thái: đã chốt yêu cầu — đang code

## Phase 0 — Chốt yêu cầu
- [x] Q1: Loại 1 "Cung ứng cho KH" → **thu hẹp** còn HĐ trong thầu (1) + ngoài thầu (2)
- [x] Q2: Popup 3 loại mới = hàng trong HĐ đúng loại **+ toàn bộ danh mục** (giống loại 1)
- [x] Q3: 3 loại mới **cần BGĐ duyệt** (gửi → Chờ BGĐ duyệt, giống nội bộ / khách lẻ)
- [x] Q4: Ô khách hàng của 3 loại mới = **toàn bộ KH đang hoạt động** (giống khách lẻ)
- [x] Mapping: đặt/mượn = `contracts.type = 4`, trao tặng = `3` (Cho/Tặng), nguyên tắc = `5`
- [x] PXL sinh từ 3 loại mới: phải duyệt như nội bộ / khách lẻ (đã đúng sẵn, không cần sửa)
- [x] Màn Kết xuất hợp đồng: tự set loại đề xuất theo loại HĐ (bỏ hardcode loại 1)
- [x] Scope: **chỉ làm phiếu đề xuất**, phiếu xử lý (cột phân bổ) làm sau

## Phase 1 — BE
- [x] `SupplyProposal`: thêm `TYPE_HD_DAT_MUON=4`, `TYPE_HD_TRAO_TANG=5`, `TYPE_HD_NGUYEN_TAC=6` + `TYPES`
- [x] `SupplyProposal`: helper `contractTypes()`, `isContractBased()`, `typeFromContractType()`, `typeNeedsBoardApproval()`
- [x] `SupplyProposal::needsBoardApproval()` gọi helper (gồm 2,3,4,5,6)
- [x] `SupplyProposalService::customers()`: loại 3/4/5/6 → danh mục KH; loại 1 → HĐ trong+ngoài thầu; type rỗng → giữ nguyên toàn bộ HĐ (màn kết xuất HĐ đang dùng)
- [x] `SupplyProposalService::goodsPool()`: loại bám HĐ lọc `contracts.type` theo mapping, vẫn merge danh mục
- [x] `SupplyProposalService::store()/update()`: `contract_id` + `needApprove` dùng helper
- [x] `RenderedContractService::prefill()`: trả thêm `type` suy từ `contracts.type`

## Phase 2 — FE
- [x] `constants.js`: TYPE + TYPE_OPTIONS 6 loại, `isContractType()` gồm 1/4/5/6
- [x] `add.vue`: thay so sánh cứng `TYPE.KHACH` bằng `isContractType` (tab tham chiếu HĐ, onTypeChange, loadGoodsPool, openPicker)
- [x] `add.vue`: prefill kết xuất HĐ set type theo `d.type` trả về từ BE + gọi lại `loadCustomers()`
- [x] `GoodsPickerModal.vue`, `ProductInfoTab.vue` dùng `isContractType()` dùng chung
- [x] `purchase_orders/.../SupplyDocDetailModal.vue` + `reports/purchase-demand/index.vue`: bỏ map cứng 2 loại, dùng `typeText()`
- [x] `StoreSupplyProposalRequest`: rule `type` sinh từ `SupplyProposal::TYPES`, `customer_id` bắt buộc mọi loại trừ nội bộ

## Phase 3 — Verify
- [x] `php -l` các file BE sửa
- [x] tinker: `customers()` / `goodsPool()` cho từng loại mới
- [x] `vue-template-compiler` check template `add.vue`
- [ ] User build client + test tay (chưa có HĐ đặt/mượn - trao tặng - nguyên tắc đã duyệt trên stag → cần tạo data test)

## Ghi chú / nợ kỹ thuật
- `SupplyHandling::COLS_BY_TYPE` chưa có entry cho loại 3/4/5/6 → bảng phân bổ PXL sẽ trống. Đã chốt "phiếu xử lý làm sau".

### Checkpoint — 22/09/2026
Vừa hoàn thành: toàn bộ Phase 1 (BE) + Phase 2 (FE) + Phase 3 verify tự động.
Đang làm dở: không.
Bước tiếp theo: user build lại client + hard refresh, tạo 1 HĐ loại đặt/mượn (hoặc trao tặng / nguyên tắc) đã duyệt trên stag rồi test popup chọn hàng + luồng gửi (phải ra trạng thái "Chờ BGĐ duyệt").
Blocked: stag chưa có HĐ đã duyệt loại 3/4/5 nên chưa test tay được.

## Phase 4 — Bảng hàng hóa của loại 4/5/6 giống khách lẻ (23/09/2026)
Chốt: phần hàng hóa của 3 loại HĐ đặt/mượn - trao tặng - nguyên tắc trình bày GIỐNG khách lẻ
(không có số liệu theo HĐ), nhưng vẫn giữ bám HĐ ở phần thông tin phiếu (chọn HĐ, lọc pool theo
`contracts.type`) → KHÔNG tái dùng `isContractType()` cho phần hàng hóa.

- [x] `constants.js`: thêm `hasContractGoodsCols()` (chỉ loại 1) + `isRetailGoodsType()` (3/4/5/6)
- [x] `constants.js`: `buildProposalSrcCols()` dùng `hasContractGoodsCols()` → 4/5/6 còn 2 cột nguồn
      (kéo theo Export Excel vì dùng chung helper) và mất cảnh báo "vượt SL còn lại theo HĐ"
- [x] ~~`add.vue`: tab "Tham chiếu hợp đồng bán" chỉ hiện với loại 1~~ → 23/09 user chốt lại:
      3 loại 4/5/6 VẪN phải có tab tham chiếu HĐ → giữ nguyên `isContractType` (1/4/5/6)
- [x] `GoodsPickerModal.vue`: bỏ bộ lọc HĐ + checkbox "Chỉ hiện hàng còn SL theo HĐ" với 4/5/6
- [x] `ProductInfoTab.vue`: bỏ cột "Tên thương mại (dữ liệu HĐ chuyển sang)" với 4/5/6;
      hiện 2 cột Giá dealer / Giá dealer không service cho cả 3/4/5/6
- [x] BE `SupplyProposal::typeShowsDealerPrice()` + `SupplyProposalController::productInfo()`:
      trả 2 cột giá dealer cho cả 4/5/6 (trước đó chỉ khách lẻ → 2 cột mới sẽ trống)
- [x] Verify: `php -l` 2 file BE, compile template 4 file FE, parse `constants.js`

### Checkpoint — 23/09/2026
Vừa hoàn thành: Phase 4 — phần hàng hóa của loại 4/5/6 trình bày giống khách lẻ (4 file FE + 2 file BE).
Đang làm dở: không.
Bước tiếp theo: build lại client + hard refresh, mở 1 phiếu loại đặt/mượn (hoặc trao tặng / nguyên tắc)
kiểm tra: bảng chỉ còn 2 cột nguồn, vẫn còn tab "Tham chiếu hợp đồng bán", popup chọn hàng không còn
bộ lọc HĐ, tab "Thông tin hàng hóa" có 2 cột giá dealer và không còn cột tên thương mại theo HĐ.
Blocked: stag chưa có HĐ đã duyệt loại 3/4/5 nên chưa test tay được (giữ nguyên từ Phase 3).
