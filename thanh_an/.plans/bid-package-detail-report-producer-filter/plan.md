# Plan: Lọc Hãng/nước SX — màn bid_package/detail-report

**@khoipv · 2026-08-28**

> Ô nhập **text** (LIKE), giống cách đã làm ở `plan/detail-report`
> (xem `.plans/detail-report-producer-country-filter/`).

## Phase 1 — Backend
- [x] `BidPackageController::applyBidPackageSummaryReportFilters`: filter `producer_country` LIKE (whereExists trên `bid_package_products`)

## Phase 2 — Frontend (`pages/bid_package/detail-report/index.vue`)
- [x] `formFilter.producer_country` (data + reset)
- [x] Ô `b-form-input` "Hãng, nước sản xuất" sau ô "Mã hàng hóa"

## Phase 3 — Verify
- [x] PHP lint BE PASS
- [ ] User verify trên UI (lọc danh sách + thống kê + export Excel hưởng filter)

---
### Checkpoint — 2026-08-28
Vừa hoàn thành: BE `applyBidPackageSummaryReportFilters` + FE ô text "Hãng, nước sản xuất" (template + data + reset). PHP lint PASS.
Đang làm dở: không
Bước tiếp theo: user verify trên UI (lọc + thống kê + export)
Blocked:

## Phase 4 — Fix: lọc trượt do dữ liệu dính xuống dòng
**Triệu chứng:** lọc "LaCAR MDx" không ra gói GT-558 dù gói có hàng của hãng đó.

**Root cause:** `bid_package_products.producer_country` nhập từ Excel, nhiều bản ghi
có ký tự `\n` ngay giữa tên hãng (`LaCAR\nMDx Technologies S.A./Bỉ`). HTML render
`\n` thành khoảng trắng nên nhìn vẫn là "LaCAR MDx", nhưng `LIKE '%LaCAR MDx%'`
so nguyên văn nên trượt. Tái hiện được trên DB local: GT-48 (dấu cách) khớp,
GT-274 (xuống dòng) không khớp.

- [x] Thêm `stripWhitespace()` + `sqlStripWhitespace()` (private, BidPackageController)
- [x] `applyBidPackageSummaryReportFilters`: so khớp sau khi bỏ whitespace ở CẢ 2 vế
      (space, tab, CR, LF, NBSP) → chịu được xuống dòng + người dùng gõ thừa khoảng trắng
- [x] Guard: từ khóa toàn khoảng trắng → bỏ qua filter (tránh `LIKE '%%'` ra hết)
- [x] PHP lint PASS
- [x] Test 6 case trên DB thật: TẤT CẢ PASS (GT-274 nay đã khớp "LaCAR MDx")

## Còn lại
- [ ] Deploy lên demo (demothanhan.dnsmedia.vn) rồi user verify — thay đổi hiện chỉ có ở local
- [ ] Cân nhắc áp dụng cùng cách chuẩn hóa cho filter `producer_country` ở màn
      `plan/detail-report` (QuotationController) — dính đúng lỗi dữ liệu này

---
### Checkpoint — 2026-08-28 (2)
Vừa hoàn thành: fix root cause lọc Hãng/nước SX trượt do `\n` trong dữ liệu; test 6 case PASS
Đang làm dở: không
Bước tiếp theo: deploy demo + user verify; hỏi user có áp dụng cho màn plan/detail-report không
Blocked: không verify được trực tiếp trên demothanhan.dnsmedia.vn (server remote, không có quyền truy cập)

## Phase 5 — Áp dụng cùng cách chuẩn hóa cho màn báo giá (user duyệt)
- [x] Tách helper dùng chung `Modules/Category/Helpers/SearchHelper.php`
      (`stripWhitespace()` + `sqlStripWhitespace()`) — file mới, không sửa hàm dùng chung sẵn có
- [x] `BidPackageController` chuyển sang dùng SearchHelper (bỏ 2 private method tạm)
- [x] `QuotationController::applyDetailReportFilters` — chuẩn hóa whitespace
- [x] `QuotationController::applySummaryReportFilters` — chuẩn hóa whitespace
- [x] PHP lint 3 file PASS
- [x] Test lại trên DB thật: TẤT CẢ PASS.
      Báo giá lọc "LaCAR MDx": TRƯỚC 0 kết quả → SAU 3 kết quả (21 dòng sp dính xuống dòng)

---
### Checkpoint — 2026-08-28 (3)
Vừa hoàn thành: helper chung SearchHelper + áp dụng cho cả gói thầu và báo giá; test PASS
Đang làm dở: không
Bước tiếp theo: deploy lên demo rồi user verify GT-558
Blocked: không verify được trực tiếp trên demothanhan.dnsmedia.vn (server remote)
