# Màn ẩn đặt lại quyết định / HĐLĐ về "Đang tạo" (không có số Redmine) — @cuong61n

Việc hay phải làm tay: đưa quyết định về "Đang tạo". Làm màn chỉ vào bằng URL (không menu), dán đường dẫn quyết định → hệ thống đổi trạng thái.

## Phase 1
- [x] BE: `DecisionResetStatusService` — đọc URL (`/decision/<loại>/<id>`, `/regulations/general|salary/<id>`), 20 loại quyết định + hợp đồng lao động; xem trước + đặt lại (05/11/2026)
  - Quyết định: `decisions.status = 1`, xoá dấu vết xem xét/duyệt, GIỮ số quyết định, KHÔNG ghi lịch sử (user chốt)
  - HĐLĐ (bảng riêng): `decision_labor_contracts.status = 1`
  - KHÔNG hoàn tác dữ liệu phát sinh lúc duyệt (lịch sử lương, thông tin NV, ngày kết thúc HĐ cũ)
- [x] BE: `DecisionResetStatusController` + route `GET decision/reset-status/preview`, `POST decision/reset-status` — chủ ý KHÔNG gắn quyền (user gửi URL riêng cho người dùng) (05/11/2026)
- [x] FE: `pages/decision/reset-status.vue` → `/decision/reset-status` (không menu): dán URL → Kiểm tra → xác nhận → Đặt về Đang tạo (05/11/2026)
- [x] Kiểm: parser URL 5 mẫu; trên DB local reset HĐLĐ #702 và 1 quyết định tiếp nhận (đã rollback) → trạng thái về 1, có dòng lịch sử (05/11/2026)
- [ ] Chưa test giao diện FE trên trình duyệt; chưa push/deploy (chờ user)
