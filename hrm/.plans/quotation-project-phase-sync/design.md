# Design — Đồng bộ Giai đoạn dự án từ Báo giá / Yêu cầu giải pháp (Redmine #11016)

## Spec gốc
Báo giá dự án và Yêu cầu làm giải pháp đều có trường bắt buộc "Giai đoạn dự án"; khi lưu thì đồng bộ
giá trị đó về dự án gốc. Dự án luôn hiển thị giai đoạn của chứng từ cập nhật gần nhất.

## Phản hồi QA (#5, #6) — kiểm chứng 2026-09-16 trên nhánh tpe

### #6 "Lưu nháp báo giá nhưng giai đoạn bên dự án TKT cũng bị đổi theo" — CÓ THẬT
Spec ghi "khi lưu" nên code gọi `syncProjectPhase()` ở **mọi** đường lưu, kể cả lưu nháp. QA chốt lại
nghiệp vụ: **bản nháp chưa được phép đổi giai đoạn của dự án**.

Chốt: chỉ đồng bộ khi chứng từ đã RỜI trạng thái nháp.

| Chỗ gọi | Trước | Sau |
| --- | --- | --- |
| `QuotationService::create()` | luôn sync | bỏ — báo giá mới luôn ở Đang tạo |
| `QuotationService::update()` | luôn sync | bỏ — `ensureEditableByCreator()` chỉ cho sửa khi Đang tạo, nên mọi lần vào đây đều là lưu nháp |
| `QuotationService::submit()` | không sync | **thêm sync**, đặt trước nhánh cấp 1 (return sớm) để báo giá tự duyệt cũng đồng bộ |
| `RequestSolutionService::create()` / `update()` | luôn sync | thêm guard `status !== STATUS_TAO_NHAP` — bấm Gửi (status 2) vẫn đồng bộ |

Lưu ý khi đọc code: guard ở `Quotation::update()` sẽ là **code chết** nếu viết dạng `if (status !== DANG_TAO)`,
vì hàm đó không bao giờ chạy với trạng thái khác. Đã thay bằng comment giải thích.

### #5 "Báo giá: khoá giai đoạn -> Sửa -> vẫn thấy danh mục đã khoá trong dropdown" — KHÔNG tái hiện
Thử 2 kịch bản với giai đoạn bị khoá thật trong DB:
- Giai đoạn khoá mà báo giá KHÔNG dùng → không xuất hiện trong dropdown.
- Báo giá ĐANG dùng giai đoạn khoá → hiện kèm 🔒 (đúng quy tắc "không được mất dữ liệu"); đổi sang
  giai đoạn khác thì option khoá biến mất ngay khỏi DOM.

Xử lý nằm ở `filterUnusedLockedOptions` (`utils/select2LockedOption.js`) + `projectPhaseOptionsMixin`,
vào nhánh tpe ngày 2026-08-20 (commit `d1dc896c5`). Xem `.claude/skills/select-and-input-state/SKILL.md` mục 1.
