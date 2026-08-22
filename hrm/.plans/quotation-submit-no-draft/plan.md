# Báo giá — Gửi duyệt ở màn Tạo mới không sinh bản nháp

Bối cảnh: màn `/assign/quotations/create?project_id=...` bấm **Gửi duyệt** đang POST tạo báo giá TRƯỚC
rồi mới mở popup xác nhận. User đóng popup (hoặc popup báo lỗi Mỏ neo) ⇒ báo giá đã nằm dưới DB, màn kẹt
ở trạng thái "Làm giá: (Chưa tạo)" không sửa được (`isCreateMode` lật false vì `item.id` vừa được gán).

Chốt: **chỉ ghi DB khi user bấm "Xác nhận gửi"** trong popup.

## Phase 1 — Không tạo nháp khi bấm Gửi duyệt

### BE (`Modules/Assign`)
- [x] `QuotationService`: tách `assertSubmittable()` từ `submit()` (điều khoản TT, giai đoạn dự án, giá > 0, giá sàn cha, Mỏ neo)
- [x] `QuotationService::previewSubmit($data)`: create + assertSubmittable + calculateLevel trong transaction rồi ROLLBACK
- [x] `QuotationService::createAndSubmit($data, $selfApprove)`: create + submit (+ selfApprove cấp 1) trong CÙNG 1 transaction
- [x] `createAndSubmit`: BE tính ra cấp 1 mà popup không xin xác nhận tự duyệt ⇒ rollback + báo user bấm lại (tránh báo giá kẹt "Đang tạo" đã gán cấp 1)
- [x] `QuotationController`: tách `prepareStoreData()` (gate quyền + payload) dùng chung cho store / previewSubmit / createAndSubmit
- [x] Route `POST /assign/quotations/preview-submit` + `POST /assign/quotations/create-and-submit` (đặt trước `/{id}`)

### FE (`hrm-client`)
- [x] `_id/edit.vue`: `save()` thêm cờ `dryRun` — nhánh tạo mới chỉ validate + trả payload, không POST
- [x] `_id/edit.vue`: `openSubmit()` rẽ nhánh `openSubmitOnCreate()` → gọi preview-submit → mở popup
- [x] `_id/edit.vue`: modal mới hiện lý do BE chặn gửi duyệt (message nhiều dòng, `white-space: pre-line`)
- [x] `QuotationSubmitModal`: thêm props `preview` + `draftPayload`; chế độ nháp không gọi calculate-level, Xác nhận thì POST create-and-submit

### Checkpoint — 2026-08-19
Vừa hoàn thành: toàn bộ code BE + FE Phase 1.
Đang làm dở: chưa test thực tế (đợi user xác nhận có test không).
Bước tiếp theo: test luồng Tạo báo giá → Gửi duyệt → Huỷ popup (kỳ vọng: không sinh bản ghi) và → Xác nhận gửi.
Blocked:

## Đánh đổi đã chốt
- Preview dựng bản ghi tạm rồi rollback ⇒ id auto-increment vẫn bị tiêu, mã báo giá thật sau đó có thể
  nhảy số (BG-2026-00042 → 00044). Chấp nhận, đổi lấy số liệu/cấp duyệt chính xác 100% (tái dùng đúng
  `create()` + `calculateLevel()`) và không sinh báo giá nháp rác.
