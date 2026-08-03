# Plan — Giữ bộ lọc khi rời trang

Phụ trách: @khoipv · 2026-07-04

## Recipe áp dụng cho mỗi màn (bám `plan/quotation`)
1. `import searchMixin from '@/utils/mixins/searchMixinPlugin.js'` + thêm vào `mixins`.
2. `data`: thêm `localStorageKey` + `pathsToKeep` (theo bảng design).
3. `mounted` (đầu hàm): `this.formFilter = { ...initialStateForm, ...this.loadFilterState().filter }`; chuẩn hoá `page`/`per_page`.
4. `watch.formFilter`: thêm `this.saveFilterState()` khi có thay đổi gọi API; **bỏ `immediate:true`** nếu có (gọi `getData()` tường minh cuối mounted).
5. `reset()`: thêm `this.clearFilterState()`.

## FE — 8 màn
- [x] 1. sale/assign-kpi (bỏ immediate:true, load state ở mounted, saveFilterState ở watch, clearFilterState ở reset)
- [x] 2. sale/register-kpi (tương tự #1, thêm mixins mới)
- [x] 3. sale/report-project-contract (currentPage computed proxy formFilter.page → khôi phục tự khớp; saveFilterState ở 3 method gọi API)
- [x] 4. sale/detail-report (không có initialStateForm → dùng {...this.formFilter}; saveFilterState trong getData)
- [x] 5. plan/detail-report (tương tự #4)
- [x] 6. bid_package/detail-report (tương tự #4)
- [x] 7. category/customer_handover (biến phân trang thật currentPage/perPage → đã sync trong mounted; resetSearch có clearFilterState)
- [x] 8. category/customer_handover/waiting-approve (đã bổ sung sync currentPage/perPage để không bị getData ghi đè trang)

## FE — Fix trùng key
- [x] 9. plan/project → `plan-project`
- [x] 10. bid_package/project → `bid-package-project`

## FE — Giữ lọc màn dashboard (plan/dashboard — 3 card chart)
Khác bản chất list: là dashboard chứa 3 card chart, mỗi card có `localFilter` riêng, mount lại là reset default. Hướng A: mỗi card tự lưu/khôi phục `localFilter` vào localStorage, key gắn theo `module` (tránh lẫn phân hệ khi tái dùng ở bid_package/contract...). Giữ CẢ địa bàn + trạng thái + nhân sự + từ/đến ngày.
- [x] 11. Tạo helper `utils/dashboard-chart-filter.js` (save/load/clear, hạn 10 phút giống searchMixin)
- [x] 12. FilterPieChartCard — key `dashboard-filter-pie-<module>`; khôi phục ở initializeFilterUI + reload ở finally; lưu ở watch localFilter (auto-apply) + apply; clear ở reset
- [x] 13. FilterLineChartCard — key `dashboard-filter-line-<module>`; khôi phục ở initializeComponent (loadLineChartData tự dùng localFilter); lưu ở apply; clear ở reset
- [x] 14. FilterColumnChartCard — key `dashboard-filter-column-<module>`; khôi phục ở initializeComponent (có saved → bỏ auto-match nhân sự, reload ở finally sau khi tắt isLoading); lưu ở apply; clear TRƯỚC khi init lại ở reset

### Checkpoint — 2026-07-04 (dashboard)
Vừa hoàn thành: giữ lọc 3 card chart màn plan/dashboard (Pie/Line/Column) qua helper dùng chung, key theo module.
Verify: `node --check` 3 component + helper → PASS.
Bước tiếp theo: user test tay trên browser (đổi lọc chart → sang trang khác → quay lại dashboard phải giữ nguyên); hoặc verify Playwright khi đăng nhập được.
Blocked: verify hành vi chờ đăng nhập.

## Verify
- [x] `node --check` cú pháp 8 file + 2 file project → PASS toàn bộ
- [x] Kiểm trùng localStorageKey toàn 4 phân hệ → tất cả duy nhất, hết trùng `sale-project-plan`
- [ ] Playwright hành vi (lọc → phân trang → chi tiết → back): CHƯA chạy được — dev server chạy (localhost:3000) nhưng route bảo vệ yêu cầu đăng nhập, không có credential. Chờ user đăng nhập hoặc test tay.

## Checkpoint — 2026-07-04
Vừa hoàn thành: 8 màn + 2 fix key, verify cú pháp + trùng key PASS.
Đang làm dở: (không)
Bước tiếp theo: user đăng nhập browser để verify hành vi bằng Playwright, hoặc user test tay.
Blocked: verify hành vi chờ đăng nhập.
