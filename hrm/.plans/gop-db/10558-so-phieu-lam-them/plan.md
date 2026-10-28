# #10558 — Đăng ký / phân công làm thêm: số phiếu, người nộp, ngày nộp (App + Web) — @cuong61n

hrm-api / hrm-client / TPE_APP nhánh `develop`. Phần chính đã làm từ 05/06/2026 (commit "Lỗi #10558" của Trí): mã PLT-/PCLT-, cột + lọc mã trên web, người nộp đơn + mã phân công ở màn chi tiết web.
Phản hồi 3 tháng trước (Lê Huyền Trang): "Ngày nộp đơn" của đơn tự sinh từ phân công không hiện ngày tạo phiếu phân công.

## Phase 1 — BE
- [x] Nguyên nhân: `OvertimeAssignmentDetailResource` lùi về `created_at` nhưng trả nguyên Carbon → JSON ISO UTC (`…T03:28:05.000000Z`); ô ngày web (value-type `YYYY-MM-DD H:mm:ss`) không đọc được → trống; app parse lỗi → tự lấy giờ hiện tại (sai ngày). 518/518 phiếu phân công local không có application_date
- [x] Sửa: format `created_at` theo giờ VN `Y-m-d H:i:s` như application_date. API: PCLT-5532 → `2026-09-30 10:28:05` (khớp DB), PLT-5531 giữ nguyên

## Phase 2 — Web
- [x] Playwright màn chi tiết: PCLT-5532 hiện Người nộp đơn / PCLT-5532 / Ngày nộp 30/09/2026 10:28; PLT-5531 không đổi (không phải sửa FE)

## Phase 3 — App (task ghi APP+WEB, app còn thiếu)
- [x] Model/entity/mapper đọc `code`; danh sách hiện "Số phiếu: PLT-…" thay "ID: …"
- [x] Chi tiết: nhãn "Phiếu yêu cầu / phân công làm thêm", không có phiếu yêu cầu thì hiện số phiếu của đơn (PCLT-…) — như web
- [x] Danh sách Đăng ký trên app ép `assignment_type: 0` → không bao giờ thấy phiếu phân công (web thì có). User chốt "Hiện giống web": chỉ gửi `assignment_type=0` ở màn Phê duyệt
- [x] Test simulator: danh sách có PCLT-5532 (người nộp, ngày nộp 30/09/2026 10:28:05) + PLT-4538…; chi tiết PCLT-5532 hiện Vũ Thị Phương Linh / PCLT-5532 / 30/09/2026 10:28:05
