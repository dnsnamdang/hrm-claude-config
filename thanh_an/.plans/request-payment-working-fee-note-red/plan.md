# Ghi chú phiếu công tác hiển thị chữ đỏ — @khoipv

Màn: `timesheet/request-payment-working-fee/:id` (Phiếu đề nghị thanh toán công tác phí)

## Task
- [x] FE: Đổi màu nội dung ô "Ghi chú" (`item.note_status_done`) trong mục I — Phiếu công tác (đứng sau "Nội dung công việc") thành chữ đỏ
  - File: `hrm-thanhan-client/pages/timesheet/request-payment-working-fee/components/RequestPaymentWorkingFeeForm.vue`
  - Thêm class `note-status-done` cho `b-form-textarea` + style scoped `color: #f46a6a !important` (kèm `:disabled` vì textarea luôn disabled)

## Checkpoint — 2026-09-12
Vừa hoàn thành: đổi màu chữ ghi chú phiếu công tác sang đỏ
Đang làm dở: không
Bước tiếp theo: user reload màn /timesheet/request-payment-working-fee/94 kiểm tra hiển thị
Blocked:
