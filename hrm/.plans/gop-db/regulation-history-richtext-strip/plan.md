# Fix lịch sử "Điều khoản báo giá" hiển thị HTML thô — Plan

Xem `design.md`. Nhánh `gop_db`. Chỉ sửa BE `hrm-api` (tầng hiển thị lịch sử). FE không đổi.

## Phase 1 — Test đỏ trước (TDD)
- [x] `RegulationHistoryTest::rich_text_field_history_strips_html_tags` — baogia field
      `quotation_footer` + dieukhoan field `quotation_footer_company`, old/new là HTML (`<p>/<ul>`) →
      dòng lịch sử phải là chữ SẠCH. Chạy trước fix: ĐỎ (còn `<p>…</p>` trong chuỗi). ĐÚNG bug.
      Lưu ý: cả 2 field text đều ghi vào `RegulationConfigHistory` (diff json) → chung `formatDiffList`;
      `company_regulation_histories` chỉ chứa field SỐ (cột decimal) nên KHÔNG dính rich.

## Phase 2 — Registry đánh dấu field rich
- [x] `RegulationTabRegistry.php`: thêm `'rich' => true` cho `quotation_footer`,
      `service_quotation_footer` (baogia) và `quotation_footer_company`, `payment_term_company`
      (dieukhoan). Giữ nguyên `type => 'string'` (không đụng rule validate).

## Phase 3 — Service strip HTML khi format lịch sử
- [x] Thêm `richToPlainText(string $html)`: `<[^>]+>`→space → html_entity_decode → gộp `\s+` → trim.
- [x] `formatHistoryValue($raw, $type, bool $rich = false)`: rich+string → strip trước.
- [x] `formatDiffList`: truyền `!empty($fields[$key]['rich'])`.
- [x] `historyCompanyRegulation`: GIỮ NGUYÊN (bảng số, không rich) — chỉ thêm comment giải thích.
- [x] `php -l` sạch.

## Phase 4 — Verify
- [x] PHPUnit `RegulationHistoryTest`: 7 test / 41 assertions PASS. SchemaTest + ScalarTabsTest PASS.
- [x] Regression: 5 errors + 2 failures của `RegulationCongnoVersioningTest` là **PRE-EXISTING**
      (fail y hệt khi `git stash` bỏ thay đổi của tôi — drift do việc congno khác trên gop_db,
      KHÔNG liên quan fix này). Thay đổi của tôi = 0 regression.
- [x] E2E DB thật (chèn tạm 1 dòng baogia rich → gọi `getHistory()` → `CONTENT=[… Giá cũ đã gồm VAT.
      → Giá mới đã gồm VAT. Hiệu lực 30 ngày.]`, `HAS_TAG=NO` → xoá dòng tạm, DB nguyên trạng).
      (Không dùng Playwright: workspace không có `e2e/` storageState, MCP mất phiên đăng nhập.)

## Checkpoint — 2026-09-23
Vừa hoàn thành: fix BE + test PASS + verify E2E DB thật. 3 file đổi (RegulationTabRegistry,
RegulationConfigService, RegulationHistoryTest) — tất cả trong `hrm-api`, FE không đổi.
Bước tiếp theo: chờ user duyệt commit (chưa commit theo ràng buộc CLAUDE.md).
Theo dõi riêng (chưa gộp): hàng đợi "Phiên bản đã hẹn" render `diff_snapshot.old/new` bằng `{{ }}`
trên FE — nếu HẸN sửa 1 field rich thì cũng hiện HTML thô; cùng root cause, khác khu vực UI,
chưa có báo lỗi.
