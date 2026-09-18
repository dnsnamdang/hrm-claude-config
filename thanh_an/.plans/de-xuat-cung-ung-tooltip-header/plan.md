# Plan — Bỏ chú thích dưới header, thay bằng tooltip (i) — @khoipv

Màn: `supply/supply_proposals/add` (phiếu đề xuất cung ứng) + `supply/supply_handlings/add` (phiếu xử lý cung ứng).

Yêu cầu: các header bảng đang hiện dòng chú thích nhỏ bên dưới (vd *Tên thương mại* → "dữ liệu phần mềm")
→ bỏ dòng chú thích, thay bằng icon **i** đặt cạnh tiêu đề, rê chuột mới hiện tooltip.

## Phase 1 — FE

- [x] `components/GoodsTable.vue` — bỏ `.col-sub` ở header "Tên thương mại" + các cột "Số liệu nguồn" (`s.sub`), thay bằng icon `i` + `v-b-tooltip`
- [x] `components/ProductInfoTab.vue` — bỏ `.th-sub` ở 4 header (Tên thương mại HĐ / Tên thương mại phần mềm / Giá dealer / Giá dealer không service), thay bằng icon `i` + tooltip
- [x] Dọn CSS `.col-sub` / `.th-sub` → `.th-tip`
- [x] Giữ nguyên `sub` trong `constants.js` vì export Excel (`add.vue:880`) vẫn dùng `label (sub)`

## Phase 2 — FE màn Xử lý cung ứng (`supply/supply_handlings/add`)

- [x] `components/HandlingGoodsTable.vue` — bỏ `.col-sub` ở "Tên thương mại", cột "Số liệu nguồn" (`s.sub`) và nhóm cột "Xử lý cung ứng" (`allocSub(key)`), thay bằng icon `i` + tooltip
- [x] `components/HandlingSummaryTabs.vue` — bỏ `.th-sub` ở 4 header (Tên thương mại HĐ x2 / Tên thương mại phần mềm / Đơn giá báo giá – gồm VAT)
- [x] Dọn CSS `.col-sub` / `.th-sub` → `.th-tip`
- [x] Giữ nguyên `allocColSub()` + `buildHandlingSrcCols()` trong `constants.js` vì export Excel (`add.vue:461`) vẫn dùng

## Sửa bổ sung

- [x] `cursor: help` → `cursor: pointer` (con trỏ Windows đang hiện dấu `?` khi rê vào icon)

## Không đụng

- `constants.js` của cả 2 màn (field `sub` / `allocColSub()` dùng chung cho export Excel)
- `.hd-sub` ở `supply_handlings/add.vue` (Dư nợ → "Tổng nợ") — là thẻ thông tin đầu phiếu, không phải header bảng
- Logic BE, các màn khác

### Checkpoint — 2026-09-17
Vừa hoàn thành: 4 component đổi sang tooltip — GoodsTable, ProductInfoTab (đề xuất) + HandlingGoodsTable, HandlingSummaryTabs (xử lý)
Đang làm dở: (không có)
Bước tiếp theo: build lại client, user hard refresh kiểm tra
Blocked:
