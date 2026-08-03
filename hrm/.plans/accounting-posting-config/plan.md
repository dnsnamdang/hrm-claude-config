# Plan: Cấu hình hạch toán cho các phiếu

> Design: `.plans/accounting-posting-config/design.md` · Spec: `docs/superpowers/specs/2026-07-07-accounting-posting-config-design.md`
> Phụ trách: @dnsnamdang · Phạm vi: UI/UX màn hình

## Trạng thái
- Bắt đầu: 2026-07-07
- Giai đoạn: **UI CODE DONE (6/6 task, FE mock data) trên nhánh tpe-develop-accounting — chờ user test trực quan + quyết định push/merge. Chưa push.**

## Tasks (UI-only, FE, mock data)
> Plan chi tiết từng step: `docs/superpowers/plans/2026-07-07-accounting-posting-config-ui.md`

- [x] Task 1: Mock data + route page `/accounting/posting-config` + menu sidebar
- [x] Task 2: Panel trái `VoucherTypeList` (search + nhóm ERP/HRM + dot trạng thái + chọn)
- [x] Task 3: Panel phải `PostingEntryTable` (dòng bút toán cơ bản + thêm/xoá + empty state)
- [x] Task 4: Dòng phụ Điều kiện (⚙) + kéo-thả sắp thứ tự (vuedraggable)
- [x] Task 5: Validation inline + Lưu/Huỷ + cảnh báo chưa lưu (dirty)
- [x] Task 6: Modal "Xem thử bút toán"

### Checkpoint — 2026-07-07
Vừa hoàn thành: Brainstorming feature (9 quyết định) + viết spec UI/UX đầy đủ (`docs/superpowers/specs/2026-07-07-accounting-posting-config-design.md`) + design.md tóm tắt.
Đang làm dở: (không)
Bước tiếp theo: user review spec → nếu OK, chạy writing-plans để lên plan implement UI (FE-only, không đụng data theo phạm vi).
Blocked: (không) — lưu ý cần chốt branch (Modules/Accounting chưa merge vào tpe-develop-assign).


### Checkpoint — 2026-07-07 (UI hoàn tất qua subagent-driven)
Vừa hoàn thành: 6/6 task UI (mock data) trên nhánh `tpe-develop-accounting` (hrm-client), mỗi task 1 implementer + 1 reviewer. 8 commit `4f63af86..cd7fb13a`. 2 vòng fix trong task (Task 3 immutable edits, Task 6 reactive preview) + final whole-branch review (opus): 0 Critical, 2 Important đã fix (validation inline đạt convention HRM: viền đỏ select2 qua ::v-deep + invalid-feedback; cảnh báo TK Nợ trùng TK Có) + 2 Minor fix (dot theo trạng thái đã lưu; guard click lại phiếu đang chọn).
Đang làm dở: (không)
Bước tiếp theo: user chạy `npm run dev` test trực quan `/accounting/posting-config`; quyết định push/merge (chưa push). Follow-up Minor + scope kế tiếp (DB/API/engine sinh bút toán) ghi trong ledger + spec.
Blocked: (không)
Trạng thái wrap-up (2026-07-08): **TẠM DỪNG theo yêu cầu user để check ý tưởng.** Code UI local trên `tpe-develop-accounting` (chưa push), không có tiến trình nền. Chờ user quyết: chỉnh UI / push-merge / brainstorm scope data-API-engine.
Follow-up Minor (chưa fix, đã ghi ledger): gap-2 cosmetic; double-emit drag vô hại; validate current-voucher; showCondition đánh dirty; preview không reset sampleValues khi đổi phiếu; factor rỗng→1; chưa có route-leave guard cấp trang.
