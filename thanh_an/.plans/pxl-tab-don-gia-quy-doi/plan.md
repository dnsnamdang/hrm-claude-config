# Plan — PXL tab "Đơn giá quy đổi"

> @khoipv — Bắt đầu 02/10/2026
> Design: [design.md](design.md) · Spec: [docs/superpowers/specs/2026-10-02-pxl-tab-don-gia-quy-doi-design.md](../../docs/superpowers/specs/2026-10-02-pxl-tab-don-gia-quy-doi-design.md)

## Phase 0 — Brainstorming
- [x] Khảo sát nguồn giá (PLT, đơn mua/HĐ mua, báo giá, giá vốn, quy đổi ĐVT)
- [x] Chốt thiết kế (user: báo giá lấy `price`, HĐ mua trước CK, thiếu thì giá vốn, chụp lúc lưu, 1→nhiều so từng cặp + cộng khối)
- [x] Viết spec + design.md

## Phase 1 — BE
- [x] Migration 4 cột `swap_origin_price`, `swap_origin_price_source`, `swap_price`, `swap_price_source` (không FK) + chạy migrate
- [x] Service mới `SwapValuePriceService::priceMap(items)` — chuỗi nguồn NK/PPL + quy đổi ĐVT + nhãn nguồn
- [x] `SupplyHandlingService::syncProducts()` — chụp giá dòng đổi, giữ snapshot cũ khi cặp không đổi
- [x] Endpoint `POST supply-handlings/swap-prices` (route + controller)
- [x] `DetailSupplyHandlingResource` trả 4 cột snapshot
- [x] Test script trên DB stag (bọc transaction + rollback)

## Phase 2 — FE
- [x] `SwapValueTab.vue` — 3 ô tổng + bảng cặp/khối, màu chênh lệch, đơn giá quy đổi
- [x] `HandlingSummaryTabs.vue` — thêm tab, `v-if` có dòng đổi
- [x] `add.vue` — gọi API xem trước (tạo/sửa + phiếu cũ chưa snapshot), map snapshot trong `mapHandlingItem`
- [x] Compile check (vue-template-compiler + babel)

## Phase 2b — Chỉnh theo góp ý
- [x] Bỏ dòng mô tả nguồn giá đầu tab
- [x] Bỏ dòng chú thích công thức + màu cuối tab
- [x] Bỏ cột "Đơn giá quy đổi"
- [x] Fix: chuyển tab rồi quay lại bị tải lại giá (bỏ `lazy` ở b-tab — lazy hủy component khi rời tab)

## Phase 3 — Test UI (user)
- [ ] Đổi 1→1: giá A/B, nguồn, chênh lệch đúng màu
- [ ] Đổi 1→nhiều: từng cặp + dòng Cộng khối + đơn giá quy đổi
- [ ] Thiếu giá 1 hàng: khối "—", không cộng vào tổng
- [ ] Lưu phiếu → mở lại giá giữ nguyên dù có đơn mua mới; đổi hàng B khác → giá B tính lại
- [ ] Phiếu cũ trước tính năng: hiện giá tham khảo + nhãn
- [ ] Phiếu không đổi hàng: không có tab

### Checkpoint — 02/10/2026
Vừa hoàn thành: Phase 1 BE + Phase 2 FE (`SwapValueTab.vue`, tab trong `HandlingSummaryTabs`, `swapPairKey` ở `constants.js`, map snapshot + `swap_price_pair` trong `add.vue::mapHandlingItem`), compile check OK
Đang làm dở: —
Bước tiếp theo: user build lại client + hard refresh, test UI Phase 3 rồi góp ý chỉnh
Blocked:
