# Xuất DS hàng hóa kèm Hóa chất sử dụng — Plan

> Người phụ trách: @khoipv · Bắt đầu: 06/10/2026
> Spec: [docs/superpowers/specs/2026-10-06-xuat-hang-hoa-hoa-chat-thiet-bi-design.md](../../docs/superpowers/specs/2026-10-06-xuat-hang-hoa-hoa-chat-thiet-bi-design.md)

## Phase 0 — Brainstorming
- [x] Khảo sát code màn danh sách hàng hóa + cách lưu Hóa chất / Thiết bị sử dụng
- [x] Chốt yêu cầu với user (xếp dọc, STT 1 / 1.1)
- [x] Viết spec + design tóm tắt

## Phase 1 — BE (`hrm-thanhan-api/Modules/Category`)
- [x] Route `GET products/export-related` (đặt trước `/{product}`)
- [x] `ProductController::exportRelated()` — validate `relation`, dùng `productService->index()` + `whereHas` + eager load, map JSON
- [x] Verify bằng tinker / gọi API

## Phase 2 — FE (`hrm-thanhan-client`)
- [x] Helper `utils/exportProductRelated.js` dựng workbook xếp dọc (STT 1 / 1.1)
- [x] `pages/category/product/index.vue`: nút Xuất excel → dropdown 3 mục + method `exportRelated()`
- [x] Kiểm tra compile

## Phase 3 — Đổi bộ cột theo yêu cầu user (06/10/2026)
Cột: STT · Tên · Mã hàng hóa · Chủng loại · Quy cách · Mã nội bộ · Hãng, nước SX (bỏ ĐVT; cả 2 file đều lấy nước SX)
- [x] BE: trả thêm `specification`; dòng con lấy Tên/Mã/Model/Quy cách/Mã nội bộ/nước SX từ hàng hóa liên kết (`object_id`), fallback bản sao trong bảng con
- [x] FE helper: đổi bộ cột + thứ tự
- [x] Verify lại + cập nhật spec

## Phase 4 — Bỏ chức năng xuất kèm Thiết bị sử dụng (user yêu cầu 06/10/2026)
- [x] BE: route `export-related` → `export-chemicals`, bỏ tham số `relation`, chỉ xử lý `chemicals`
- [x] FE: bỏ mục dropdown "DS hàng hóa kèm Thiết bị sử dụng", `exportRelated()` → `exportChemicals()`, helper bỏ cấu hình devices
- [x] Verify lại + cập nhật spec / design / STATUS

### Checkpoint — 2026-10-06 15:15
Vừa hoàn thành: BE API `GET category/products/export-related` + FE dropdown Xuất excel 3 mục + helper `utils/exportProductRelated.js`
Đang làm dở: —
Bước tiếp theo: user build client (`npm run build` / dev) + hard refresh, test tay theo mục 9 của spec
Blocked:

**Verify đã chạy:** script PHP bootstrap Laravel trên DB `thanhan_stag_07052026` — chemicals 6 hàng / 209 dòng con (khớp `whereHas` đối chiếu = 6), devices 190 hàng / 200 dòng con, relation sai → 422, lọc status=2 OK. Helper FE chạy bằng Node 14 với dữ liệu thật, đọc lại xlsx: số dòng khớp (217 / 392), STT 1 / 1.1, dòng cha đậm, STT `3.10` giữ dạng text. Template `index.vue` compile 0 lỗi.

### Checkpoint — 2026-10-06 15:20
Vừa hoàn thành: Phase 3 — đổi bộ cột (Tên · Mã hàng hóa · Chủng loại · Quy cách · Mã nội bộ · Hãng, nước SX), dòng con lấy từ hàng hóa liên kết
Đang làm dở: —
Bước tiếp theo: user build client + hard refresh, test tay
Blocked:

**Verify:** chemicals 6 hàng / 209 con, devices 190 / 200 con (200/200 con có quy cách + nước SX), xlsx 217 / 392 dòng khớp.

### Checkpoint — 2026-10-06 15:32
Vừa hoàn thành: Phase 4 — bỏ chức năng xuất kèm Thiết bị; API đổi thành `GET category/products/export-chemicals` (`exportChemicals()`), helper đổi thành `utils/exportProductChemicals.js`, dropdown còn 2 mục
Đang làm dở: —
Bước tiếp theo: user build client + hard refresh, test tay theo mục 9 spec
Blocked:

**Verify:** 6 hàng / 209 dòng con (khớp đối chiếu), lọc status=2 OK; xlsx 217 dòng khớp; template `index.vue` compile 0 lỗi; không còn tham chiếu `exportRelated` / `export-related`.
