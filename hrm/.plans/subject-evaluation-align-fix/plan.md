# Plan — subject-evaluation-align-fix

Người phụ trách: @junfoke

## Bối cảnh

Màn Cập nhật khoá học → tab "Cấu hình đánh giá" (`/training/subjects`, component `TabEvaluation.vue`).
User báo: ô input "Rule đạt khoá" và "Ngưỡng đạt (% tổng trọng số)" lệch nhau (không thẳng hàng ngang).

## Root cause

Trong `.cfg-body`, các cột `col-md-4` có khối label CAO KHÁC NHAU:

- "Rule đạt khoá" / "Tỷ lệ yêu cầu (%)" / "Cách tính %": chỉ có `<V2BaseLabel class="mb-1">` → cao ~19px.
- "Ngưỡng đạt (% tổng trọng số)": bọc thêm `<div class="d-flex">` chứa label + `<span class="info-ico">`.
  `.info-ico` bị ép `width/height: 28px` (`scss/_index.scss:630-633`) → khối label cao 28px + mb-1.

Chênh ~13px → input bên dưới của 2 cột bắt đầu ở toạ độ Y khác nhau.

## Phase 1 — Đồng nhất chiều cao khối label trong cfg-body

- [x] T1. Thêm class dùng chung `.fld-head` (scoped, chỉ trong TabEvaluation): `display:flex; align-items:center; gap:6px; min-height:28px; margin-bottom:4px`
- [x] T2. Áp `.fld-head` cho cả 4 khối label trong `.cfg-body` (Rule đạt khoá, Tỷ lệ yêu cầu, Cách tính %, Ngưỡng đạt) — phải áp HẾT vì "Rule đạt khoá" hiển thị đồng thời với cả nhánh `percent` lẫn nhánh `weighted`
- [x] T3. Đổi `V2BaseLabel` trong các khối này từ `class="mb-1"` → `class="mb-0"` (margin đã do `.fld-head` lo)

## Phase 2 — Đồng nhất chiều cao control (user báo bổ sung: hàng trên 3 ô cũng lệch)

Root cause KHÁC Phase 1 (không phải label, mà là chiều cao ô):

- `V2BaseSelect` size="sm" → `updateHeight()` set **inline** `height: 32px !important` lên
  `.select2-selection--single` (heightMap.sm), sau `setTimeout` 100ms.
- `V2BaseInput` size="sm" → render `<input class="v2-input v2-input--sm">`, **không set height**,
  chỉ `padding: 6px 10px` + `font-size: 12px` → cao ~29px.
- → Select 32px vs Input ~29px, đứng cạnh nhau trong `form-row` là lệch mép (~3px).

Ghi chú: rule `.form-control.form-control-sm { height: 34px }` ở `_index.scss:47` KHÔNG liên quan —
V2BaseInput/V2BaseSelect không dùng class `.form-control`.

- [x] T4. Thêm `.v2-input--sm { height: 32px }` trong `.subject-builder-root` (`scss/_index.scss`)
      → input khớp đúng 32px của select. Không cần `!important` (specificity 0,2,0 > 0,1,0).

Hướng đã loại: ép ngược select về 34px là BẤT KHẢ THI bằng CSS — inline `!important` do JS set luôn thắng stylesheet.

## Ràng buộc

- Phase 1: chỉ sửa `TabEvaluation.vue` (template + scoped style).
- Phase 2: sửa `scss/_index.scss` — file này nạp UNSCOPED ở `SubjectBuilderForm.vue:716` và bọc trong
  `.subject-builder-root` → chỉ ảnh hưởng màn Subject Builder (4 tab + modal), KHÔNG lan ra hệ thống.
- KHÔNG đổi `.info-ico` (28px là chuẩn chung toàn màn).
- KHÔNG sửa `V2BaseInput.vue` / `V2BaseSelect.vue` (component dùng chung toàn app — theo CLAUDE.md
  phải hỏi trước). Xem mục "Nợ kỹ thuật" bên dưới.
- KHÔNG migration / permission / BE / git.
- hrm-client không cấu hình eslint (package.json chỉ có nuxt scripts) → không có lint để chạy.

## Nợ kỹ thuật (CẦN HỎI USER — chưa làm)

`V2BaseInput` size="sm" (~29px) vs `V2BaseSelect` size="sm" (32px) lệch nhau ở **TOÀN BỘ app**,
không riêng màn này. Fix đúng gốc = set `height: 32px` cho `.v2-input--sm` trong `V2BaseInput.vue`.
Nhưng đó là component dùng chung → phải xin ý kiến trước. Hiện đang vá cục bộ ở `_index.scss`.

## Verify

- [ ] Hàng trên: "Hình thức đánh giá" (select) / "Số lần thi" (input) / "Quy tắc lấy điểm" (select) thẳng mép
- [ ] Nhánh "Theo trọng số": "Rule đạt khoá" + "Ngưỡng đạt (% tổng trọng số)" thẳng hàng
- [ ] Nhánh "Hoàn thành theo %": 3 ô (Rule / Tỷ lệ / Cách tính) thẳng hàng
- [ ] Nhánh "Hoàn thành 100% bài bắt buộc": chỉ 1 ô, không vỡ layout
- [ ] Tab Thông tin / Người học / Chứng chỉ: input không bị vỡ do rule `.v2-input--sm` mới

### Checkpoint — 2026-07-15

Vừa hoàn thành: T1-T3 (label đồng cao trong cfg-body) + T4 (input sm = 32px khớp select sm).
Đang làm dở: không.
Bước tiếp theo: user tự verify mắt (user chốt không cần Playwright). Nếu OK → hỏi có fix gốc V2BaseInput không.
Blocked: không
