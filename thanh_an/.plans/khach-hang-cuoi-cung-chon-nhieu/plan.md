# Plan — Khách hàng sử dụng cuối cùng chọn nhiều

> Plan chi tiết (7 task): [`docs/superpowers/plans/2026-07-07-khach-hang-cuoi-cung-chon-nhieu.md`](../../docs/superpowers/plans/2026-07-07-khach-hang-cuoi-cung-chon-nhieu.md)

## Phase 1 — BE
- [x] Migration ×3 (add cột JSON + backfill) — đã migrate + tinker verify
- [x] Entity ×3 (fillable + cast json + **mutator** tự đồng bộ name/id) — tinker `A, B | 1`
- [x] StoreRequest ×3 (rule array)
- [x] Detail Resource ×3 (trả mảng)
- ~~Controller store/update~~ — KHÔNG cần: mutator lo denormalize ở cả store lẫn update (đều `fill()`)

## Phase 2 — FE
- [x] Quotation: GeneralComponent (chip UI + handler + addProject auto) + add + edit (init + map + payload)
- [x] Contract: GeneralComponent (addNegotiation merge + concentrated-bid reset) + add + edit
- [x] Bid_package: GeneralComponent (addQuotation merge + addProject auto + defaultForm) + add + edit

## Phase 3 — Verify
- [ ] **(CHỜ USER)** Test UI tạo/sửa 3 module: chọn nhiều, xóa, auto từ dự toán, dedupe
- [ ] **(CHỜ USER)** Kiểm tra report/list hiển thị chuỗi nhiều tên nối `", "`

### Checkpoint — 2026-07-07
Vừa hoàn thành: toàn bộ 6 task code (BE + FE 3 module). BE verify tinker PASS.
Đang làm dở: chờ user verify UI (không tự chạy Nuxt server được).
Bước tiếp theo: user chạy UI 3 màn add/edit để xác nhận; nếu OK → move sang Hoàn thành.
Blocked: (không)
