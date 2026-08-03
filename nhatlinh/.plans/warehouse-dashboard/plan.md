# Plan — Dashboard Kho

- Spec: `docs/superpowers/specs/2026-07-02-warehouse-dashboard-design.md`
- Plan chi tiết (bite-sized, cho executor): `docs/superpowers/plans/2026-07-02-warehouse-dashboard.md`
- Design tóm tắt: `.plans/warehouse-dashboard/design.md`

## Phase 1 — Schema min_stock + Danh mục hàng hoá
- [x] T1: Migration `min_stock` vào `products` + Product entity fillable (review clean)
- [x] T2: ProductRequest rule + ProductResource + DetailProductResource + ProductForm.vue (review clean)

## Phase 2 — Backend Dashboard
- [x] T3: Permission `1138 Xem dashboard kho` (seeder) + seed/gán role dev
- [x] T4: `WhDashboardService` (review clean; fix bug pluck-CONCAT trong plan; Minor: eager-load ĐVT không filter query, Carbon string-unit — để final review)
- [x] T5: `DashboardRequest` + `DashboardController@index` + route `/v1/warehouse/dashboard` (review clean; dùng BaseRequest/ApiController/responseJson đúng convention)

## Phase 3 — Frontend Dashboard
- [x] T6: store `warehouse-dashboard.js` (review clean; dùng apiGetMethod + query string, page tự unwrap .data)
- [x] T7: `pages/warehouse/dashboard/index.vue` (6 khối: 2 hàng KPI + chart nhập/xuất + 2 top + 2 bảng) — verify tĩnh (template compile OK qua vue-template-compiler, script parse OK qua @babel/core); chưa test trình duyệt thực tế
- [x] T8: menu "Tổng quan" đầu sidebar kho (self-verify: đầu mảng, permission khớp)
  (T7 Minor: icon Remix chưa verify hiển thị; stretched-link trong __body giống pattern sale — để user test trình duyệt)

## Bug fix ngoài plan
- [x] BUG: `/warehouse/category` không hiện sidebar — trang thiếu `layout: 'default-sidebar'` (sót khi move từ `/category/warehouses` sang phân hệ kho 2026-06-29; các trang kho khác đều có) → thêm 1 dòng layout vào `pages/warehouse/category/index.vue`
- [x] Entry phân hệ kho mặc định vào Dashboard: đổi `/warehouse/receipt` → `/warehouse/dashboard` ở 3 chỗ — `pages/index.vue` (màn chọn phân hệ), `layouts/default-sidebar.vue` (urlLogo), `components/BasicSubsystem.vue` (popup phân hệ topbar)

## Checkpoint
### Checkpoint — 2026-07-02 (CODE HOÀN THÀNH 8/8 task + FINAL REVIEW PASS)
Vừa hoàn thành: Toàn bộ 8 task (subagent-driven, mỗi task qua review riêng) + final review opus.
- Phase 1: migration min_stock (products), ProductRequest/Resource/DetailResource/ProductForm.
- Phase 2: permission 1138, WhDashboardService (6 khối), DashboardRequest/Controller/route.
- Phase 3: store warehouse-dashboard, trang dashboard 6 khối, menu "Tổng quan".
- **Final review: 1 Critical (C1) ĐÃ FIX** — ProductService bỏ sót lưu min_stock (2 mảng create/update dòng 136/188) → nếu không fix, khối cảnh báo tồn thấp luôn rỗng; đã thêm + verify tinker lưu OK ('15.00').
- Minor T4b (Carbon string-unit) ĐÃ đồng bộ sang subWeeks/subMonths/subQuarters/subYears. Minor còn lại (icon Remix chưa verify hiển thị; stretched-link trong __body giống pattern sale) → chấp nhận, user test trình duyệt.
Bước tiếp theo (user): (1) migrate min_stock; (2) seed + gán quyền 1138; (3) test trình duyệt (lưu min_stock hàng hoá → thấy ở cảnh báo tồn thấp; 6 KPI; toggle Tuần/Tháng/Quý/Năm; datepicker Top; 403 khi không quyền; icon render); (4) commit khi có yêu cầu.
Blocked:
