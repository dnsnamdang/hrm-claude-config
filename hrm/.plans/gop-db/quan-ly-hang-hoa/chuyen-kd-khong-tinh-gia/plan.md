# Chuyển kinh doanh không tính giá — Plan

**Design:** `design.md` · **Tồn:** `ton.md` · @namdangit · nhánh `gop_db` (checkout chính 2 repo HRM) · không migration / seeder / quyền mới.
✅ User cho "làm" 23/10/2026 (2 repo HRM, gop_db, không migration). Commit 24/10: hrm-api `17f76d1f9`, hrm-client `3940e0c1b` (chưa push).

## Task 1 — BE (hrm-api)
- [x] `Product::tradableWithoutPriceAt()`
- [x] `ProductLifecycleService::tradeWithoutPrice()` (khuôn `restore()`: cap 100, transaction + lockForUpdate, skipped kèm lý do; `ensureProductSet` → status 3 → `logStatus` ghi chú "Không bắt buộc tính giá")
- [x] Controller + route `POST master-data/products/trade-without-price` (1652 + dueConfig)
- [x] `ProductListResource`: `can_trade_without_price`
- [x] PHPUnit `ProductTradeWithoutPriceApiTest` (ca ở design §5) + chạy lại Lifecycle / Restore / Take

## Task 1b — Luật khôi phục (Đ2, design §2b)
- [x] `ProductRestoreRule::readySql()` + `readyBindings()`; `reasons()` bỏ qua hàng khoá theo công ty
- [x] Đổi 3 chỗ gọi (ProductService ×2, ProductLifecycleService ×1)
- [x] Test RestoreRule / RestoreApi: ca mới + sửa ca cũ; Playwright màn Hàng hoá đang khoá (cột Khôi phục về; ô lọc chỉ kiểm bằng PHPUnit `ProductLockedScreenTest`)
- [x] Ghi đổi K2/K3 vào `hang-hoa-dang-khoa/design.md`

## Task 2 — FE (hrm-client)
- [x] `utils/product-list-screens.js`: cờ `tradeWithoutPrice` cho `entering`
- [x] `utils/productLifecycle.js`: `tradeWithoutPrice()` (confirm + toast)
- [x] `ProductListPage.vue`: computed gate · mục menu dòng · nút thanh hàng loạt · lọc dòng có cờ, trần 100

## Task 3 — Kiểm
- [x] Playwright MCP trên local `hrm_erp_21_10_prod` (đo DOM, có / không quyền) — thao tác thật sẽ ghi DB local (đổi trạng thái hàng thử, trả lại sau)
- [x] Viết spec e2e (chưa chạy tới khi user yêu cầu)
- [x] Cập nhật `viec-con-lai.md` + `SO-CHOT-VA-TON.md`

## Phát sinh lúc code (23/10)
- [x] Footer chi tiết có nút (user chốt) — `ProductDetailResource` + `pages/master-data/products/_id/index.vue`
- [x] Màn *Dữ liệu hàng hoá công ty* bật cùng action (khớp chi tiết) — `product-list-screens.js`
- [x] Sửa test cũ theo Đ2: `ProductLifecycleApiTest` (2 ca), `ProductLockedScreenTest` (1 ca), `ProductRestoreApiTest` (+2 ca mới, 3 ca sửa), `ProductRestoreRuleTest` (+1)
- [x] Sửa spec e2e cũ: `products-lifecycle-ui` (helper đọc cả menu "…", D1, D8, D10 so tập, N1 thêm cờ mới), chú thích `products-lifecycle.api`, `product-history-ui`

## Kết quả kiểm (23/10)
- PHPUnit MasterData 658 ca: 4 đỏ ⇒ 1 do Đ2 (`ProductLockedScreenTest`, đã sửa, xanh) + 3 KHÔNG liên quan: `ExpectedPriceApplyTest::chot_chan…` + `TempProductVisibilityTest::catalog_tab…` (đỏ sẵn đã ghi) + `PriceReaderWhitelistTest` bắt `Modules/Finance/Services/InventoryAuditReportService.php` (commit `538a477a3` của đồng đội 21/10 — màn Biên bản kiểm kê, chưa khai price-readers).
- Playwright MCP (NV 13, local `hrm_erp_21_10_prod`): menu dòng + popup + POST thật TDHFUJI-MOCCAU ⇒ rời màn Nhập thông tin, có ở Đang KD; khoá ⇒ màn đang khoá "Khôi phục về: Đang kinh doanh" ⇒ khôi phục về 3; thanh hàng loạt + footer chi tiết đo bằng route giả (payload, câu hỏi, toast, về màn `from`); nút thanh cách 12px; màn Dữ liệu công ty: dòng 1 có icon, dòng 3 không. Đã trả TDHFUJI-MOCCAU về status 1 + xoá 3 dòng lịch sử thử.
- E2E 24/10 (user yêu cầu, `--workers=1`, node 20): `products-trade-without-price-ui` + `products-lifecycle-ui` **15 passed, 2 skipped**.
  - Lượt 1 đỏ 3 ⇒ sửa: `utils/productFixture.ts` dọn thiếu `product_company_units` (FK chặn xoá `product_units`) · D9 footer thêm nút mới.
  - Skip (dữ liệu, không do code): D5 không có mã Cty 4 chưa dùng · N1 tài khoản `e2e_cmd_noperm@test.local` không có ở DB gộp (login 422). Ca không quyền đã có ở PHPUnit (403 + cờ false).
  - `products-lifecycle.api` chặn ngay beforeAll: cần mã ERP Cty 1 chưa có dòng hệ số — DB gộp 27.244/27.244 mã đã có dòng ⇒ cả file không chạy (đỏ sẵn, ngoài luồng).

### Checkpoint — 23/10/2026
Vừa hoàn thành: code BE + FE + test, kiểm Playwright MCP (23/10 tối).
Đang làm dở: —
Bước tiếp theo: user soát ⇒ commit (user tự báo) · lên prod cùng đợt deploy kế.
Blocked: —
