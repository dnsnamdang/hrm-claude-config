# plan.md — customer-date-no-future

**Người phụ trách:** @khoipv · **Nhánh:** `gop_db` · Tạo 2026-08-13

## Phase 1 — FE: xám ngày tương lai trong lịch

- [x] T1. Thêm method `disableFutureDate(date)` vào `CustomerForm.vue` (đầu khối `methods`, dòng ~1812)
- [x] T2. Truyền `:disabled-date="disableFutureDate"` cho ô **Ngày cấp** (`grant_date`, dòng 369)
- [x] T3. Truyền `:disabled-date="disableFutureDate"` cho ô **Sinh nhật KH** (`date_of_birth`, dòng 466)
- [x] T4. Truyền `:disabled-date="disableFutureDate"` cho ô **Sinh nhật người liên hệ**
      (`contacts[].date_of_birth`, dòng 1203)

## Phase 2 — BE: validate lưới an toàn (gõ tay không lọt)

- [x] T5. `SaveCustomerRequest.php`: thêm `before_or_equal:today` cho `grant_date`,
      `date_of_birth`, `contacts.*.date_of_birth` + 6 message tiếng Việt
- [x] T6. `UpdateCustomerRequest.php`: y hệt T5

## Phase 3 — Verify

- [x] T7. `vue-template-compiler` compile template + `@babel/parser` parse script → OK,
      đếm đúng **3** binding `disabled-date`, method có thật
- [x] T8. `php -l` 2 file Request → no syntax errors
- [x] T9. Chạy thật `disableFutureDate`: hôm qua `false` · hôm nay `false` · ngày mai `true`
- [x] T10. Chạy thật Laravel Validator với bộ rule mới: hôm nay **PASS** · `null` **PASS** ·
      ngày mai **FAIL** đúng 3 trường, message ra đúng tiếng Việt
      ("Ngày cấp không được lớn hơn ngày hiện tại" / "Sinh nhật không được lớn hơn ngày hiện tại")
- [x] T11. **User test trình duyệt** — user xác nhận xong 2026-08-13

## Phase 4 — Tài liệu (wrap up)

- [x] T12. `.plans/gop-db/customer-date-no-future/design.md` — tóm tắt
- [x] T13. `docs/superpowers/specs/gop-db/2026-08-13-customer-date-no-future-design.md` — spec đầy đủ
- [x] T14. Cập nhật `.plans/gop-db/STATUS.md` (mục Đang làm)

## Checkpoint — 2026-08-13

Vừa hoàn thành: **TOÀN BỘ feature** — Phase 1-4, verify tự động (T1–T10), tài liệu (T12–T14),
user test trình duyệt xong (T11). Feature đã chuyển sang mục "Hoàn thành" ở `.plans/gop-db/STATUS.md`.
Đang làm dở: không.
Bước tiếp theo: chưa commit — commit/merge về `gop_db` khi anh yêu cầu.
Blocked:
