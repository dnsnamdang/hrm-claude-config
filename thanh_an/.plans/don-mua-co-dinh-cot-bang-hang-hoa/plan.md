# Plan — Cố định 3 cột đầu + xuống dòng tên hàng hóa (Bảng hàng hóa — Đơn mua hàng)

**Phụ trách:** @khoipv
**Màn:** `supply/purchase_orders` — tab "Hàng hóa" (dùng chung cho Lập mới / Sửa / Xem chi tiết)
**File:** `hrm-thanhan-client/pages/supply/purchase_orders/components/ProductsTab.vue`
**Ngày:** 2026-09-08

## Mục tiêu
1. Cuộn ngang bảng hàng hóa thì **3 cột đầu (STT / Mã hàng / Tên hàng hóa) đứng yên**.
2. Cột **Tên hàng hóa dài thì xuống dòng**, không kéo dài bảng như hiện tại (`white-space: nowrap`).

## Quyết định
- Dùng đúng pattern sticky-left đã có trong repo (`contract/contract/components/ProductComponent.vue`):
  `position: sticky` + `left` cộng dồn theo bề rộng cột.
- Bề rộng chốt: STT **42px** · Mã hàng **96px** · Tên hàng hóa **240px** → `left`: 0 / 42 / 138.
- Nền ô đông cứng phải **đục** (đè nội dung cuộn phía dưới) và giữ đúng màu theo trạng thái dòng:
  thường `#fff` · dòng cảnh báo `#fcefec` · dòng TỔNG CỘNG `#eef4f3`.
- `z-index`: header vừa sticky-top vừa sticky-left → **3**; ô body sticky-left → **1**;
  header thường giữ **2** (đã có sẵn).
- Dòng TỔNG CỘNG đang là `td colspan=6` phủ qua vùng đông cứng → tách thành
  `colspan=3` (sticky, chứa chữ "TỔNG CỘNG") + `colspan=3` (trống) để chữ luôn nhìn thấy khi cuộn.
  Tổng số ô vẫn = 20, không lệch cột.

## Task

### FE — `ProductsTab.vue`
- [x] Thêm class `col-freeze col-stt` / `col-freeze col-code` / `col-freeze col-name col-freeze-last`
      cho 3 `th` đầu + 3 `td` đầu của dòng dữ liệu
- [x] Tách `td colspan=6` của dòng TỔNG CỘNG thành `colspan=3` (sticky) + `colspan=3` (trống)
- [x] CSS: `.col-freeze` sticky + nền đục theo trạng thái dòng, `left` cộng dồn, `z-index` phân tầng
- [x] CSS: `.cell-name` bỏ `nowrap` → `white-space: normal` + `word-break: break-word`, khóa
      `width/min/max = 240px`; header vẫn nowrap (rule `thead.thead-sticky th` đặc hiệu hơn)
- [x] Viền phải cột thứ 3 (`col-freeze-last`) có đổ bóng nhẹ làm mốc phân cách vùng đông cứng
- [x] `vue-template-compiler` check sạch

## Kiểm thử tay (chờ @khoipv)
- [ ] Cuộn ngang bảng → 3 cột đầu đứng yên, không lộ nội dung cuộn phía dưới
- [ ] Dòng cảnh báo (SL mua lệch SL đề xuất) → 3 ô đầu vẫn màu hồng, không trắng
- [ ] Dòng TỔNG CỘNG → chữ "TỔNG CỘNG" luôn thấy khi cuộn, các cột số vẫn thẳng hàng
- [ ] Tên hàng hóa dài → xuống dòng trong 240px, tên thương mại (dòng `.sub`) vẫn đúng
- [ ] Cuộn dọc → header vẫn dính trên và không bị 3 cột đầu đè lên

### Checkpoint — 2026-09-08
Vừa hoàn thành: sửa xong `ProductsTab.vue` (template + SCSS), compile sạch
Đang làm dở: không
Bước tiếp theo: @khoipv build lại client + hard refresh, xem mắt theo checklist kiểm thử tay
Blocked:
