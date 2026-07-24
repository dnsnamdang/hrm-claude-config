# Design tóm tắt — Nhóm hàng 2 cấp + kéo-thả cho BÁO GIÁ (Quotation)

> Spec đầy đủ: `docs/superpowers/specs/2026-07-17-baogia-multilevel-groups-design.md`

## Mục tiêu
Áp mô hình "nhóm hàng 2 cấp (cây) + kéo-thả + đồng bộ Import/Export/In" đã làm cho BOM (`bom-multilevel-groups`) sang màn Báo giá `/assign/quotations`, theo task gốc.

## Bối cảnh cốt lõi
- Báo giá 2 chế độ: **Tự nhập** (tự dựng nhóm) + **Từ BOM** (copy khung từ 1 BOM rồi điền giá).
- Cây 2 cấp ở báo giá HIỆN đã có ở tầng **SẢN PHẨM** (`quotation_product_prices.parent_id`); tầng **NHÓM** (`quotation_groups`) vẫn phẳng → feature này thêm 2 cấp cho NHÓM.

## 6 quyết định chốt
1. Đúng 2 cấp nhóm.
2. Cả 2 chế độ (Từ BOM: bổ sung copy `parent_id` khi materialize).
3. Import 26 cột theo template Google Sheet (tách Nhóm cha/con + Mã hàng cha, giữ cột giá + logic GG).
4. Cha-con SẢN PHẨM nối bằng `Mã hàng cha` (nearest-above cùng nhóm lá); STT giữ làm toạ độ/thứ tự.
5. Phân cấp thể hiện ở Export round-trip (blade riêng) + In ấn (`QuotationPrintPreview`, client-side). KHÔNG đụng Export trình bày khách (blade chung BOM).
6. KHÔNG làm subtotal theo nhóm.

## Thay đổi chính
- **DB**: 1 migration thêm `quotation_groups.parent_id` (nullable, không FK/transaction).
- **BE**: `syncDirectGroups()` 2 pass; `materializeBomGroupsIntoQuotation()` copy `parent_id`; Import 26 cột + `resolveImportParentLinks()`; Export round-trip 26 cột (blade riêng).
- **FE**: `edit/create.vue` render cây 2 cấp + kéo-thả header nhóm (`.q-drag-group`); `QuotationImportModal` 26 cột; `QuotationPrintPreview` render 2 cấp.

## AC
AC1 tạo nhóm con · AC2 export round-trip + in 2 cấp · AC3 import nhóm cha-con · AC4 kéo-thả · AC5 Từ BOM giữ 2 cấp.

## Ngoài scope
Subtotal theo nhóm · nhóm 3+ cấp · export trình bày khách 2 cấp · sửa logic tính tiền · đụng BOM.
