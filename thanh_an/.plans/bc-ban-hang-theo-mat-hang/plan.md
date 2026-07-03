# Báo cáo bán hàng theo mặt hàng — Plan

> @khoipv · Plan chi tiết: `docs/superpowers/plans/2026-07-02-bc-ban-hang-theo-mat-hang.md`
> Spec: `docs/superpowers/specs/2026-07-02-bc-ban-hang-theo-mat-hang-design.md`

## Phase 0 — Brainstorming ✅
- [x] Chốt scope (A1 Thực xuất để trống, A2 1 quyền, A3 Excel, không lọc cấp, loại HĐ hủy)
- [x] Viết spec chi tiết
- [x] User review spec + duyệt ("cứ làm đi")
- [x] Lập plan triển khai

## Phase 1 — Backend
- [x] Task 1 — Quyền `Xem báo cáo bán hàng theo mặt hàng` (seeder tổng id=511 + seeder idempotent, đã chạy & verify OK)
- [x] Task 2 — Endpoint `ProjectController@saleProductReport` + route + helper dựng cây (show-once BG/Thầu). Verify: 1442 dòng→707 MH, KPI đúng, tree JSON hợp lệ

## Phase 2 — Frontend
- [x] Task 3 — Trang khung + KPI + bộ lọc
- [x] Task 4 — Bảng cây flatten + collapse (2 tầng header, Thực xuất `–`)
- [x] Task 5 — Drill-down modal (mở thẳng chi tiết DT/BG/GT/HĐ, tái dùng endpoint)
- [x] Task 6 — Xuất Excel (ExcelJS)
- [x] Task 7 — Gắn `isShow` menu

## Đã dùng thực tế (khác plan gốc)
- Dùng snapshot info trên `contract_products` (product_code/name/unit_id/array/group/producer) thay vì join product master → chính xác hơn.
- HĐ hủy = `status = 5` (Contract::HUY), không phải 18.
- Endpoint thực tế: `category/projects/reports/sale-product` (route nằm trong group /projects).
- Drill-down mở thẳng modal chi tiết (không qua bước list) vì flow đã có sẵn id.

## Bổ sung sau (2026-07-02)
- [x] Phân trang client-side ở cấp mặt hàng (giống UI `plan/detail-report`: chọn số dòng/trang + `b-pagination` + "Tổng số mặt hàng"). KPI/Tổng cộng vẫn tính trên toàn bộ; Excel vẫn xuất tất cả trang. Tách `buildRows` (lọc + reset trang) và `renderRows` (dựng dòng theo trang), thêm computed `pagedItems`/`totalRows`/`currentPage`, `onPageChange`, watcher `per_page`.

## Còn lại (cần user chạy/kiểm)
- [ ] Chạy `npm run dev` client, mở `/contract/reports/sale-product` kiểm thị giao diện + collapse + drill-down + Excel.
- [ ] Gán quyền `Xem báo cáo bán hàng theo mặt hàng` cho role qua UI phân quyền.
- v1 chỉ hiển thị luồng HĐ đã ký (pipeline hoãn).

### Checkpoint — 2026-07-02
Vừa hoàn thành: toàn bộ Task 1–7 (BE verify qua tinker/reflection; FE viết theo pattern report-project-contract)
Đang làm dở: chưa chạy nuxt dev để xác nhận render (Node 14, cần user chạy)
Bước tiếp theo: user chạy client + gán quyền cho role + đối chiếu số liệu
Blocked: 
