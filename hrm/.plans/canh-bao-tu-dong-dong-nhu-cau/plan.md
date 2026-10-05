# Plan — Cảnh báo & tự động đóng nhu cầu khách hàng (#11377)

Người phụ trách: @junfoke · Nhánh: `task_11377` → đã merge vào `tpe-develop-assign` (cả `hrm-api` và
`hrm-client`). Thiết kế: [design.md](design.md).

## Phase 1 — Hạ tầng + luồng tự động (BE) — ĐÃ XONG

- [x] **B1.** Migration: `internal_business_scopes.demand_due_days` (N, mặc định 0) ·
      `general_regulations.demand_warning_days` (M, mặc định 3) · `meetings.completed_at` (mốc T,
      backfill = `end_date`) · `meeting_investment_demands.expiry_warned_at`.
- [x] **B2.** Ghi mốc T bằng hook `saving()` của `Meeting` — chỉ ghi lần đầu chuyển Hoàn thành.
- [x] **B3.** `MeetingInvestmentDemand::dueDate()` tính hạn tại chỗ (không lưu cứng).
- [x] **B4.** Viết lại cron `assign:close-expired-customer-demands` (01:20 hằng ngày): luồng cảnh báo
      (T+N−M, chỉ khi N > M, một lần/nhu cầu) + luồng đóng (T+N, `closed_at` = đúng ngày hết hạn).
- [x] **B5.** Thông báo "Sắp đến hạn" gửi người chủ trì cuộc họp (không có thì người tạo), dựng nội
      dung qua helper chuẩn của skill `notification-convention`.
- [x] **B6.** Chặn lập Dự án TKT từ nhu cầu đã đóng ở `ProspectiveProjectService` — đúng câu yêu cầu.
- [x] **B7.** Validate N (bắt buộc, số nguyên 0–3650) + trả `demand_due_days` ra danh sách/chi tiết
      danh mục; M vào nhóm trường track Lịch sử cấu hình hạn.
- [x] **B8.** API danh sách nhu cầu trả hạn + cờ sắp hết hạn + số ngày còn lại.

## Phase 2 — Giao diện (FE) — ĐÃ XONG

- [x] **F1.** Danh mục Lĩnh vực: ô N ở popup Tạo/Sửa/Xem (kèm icon ⓘ) + cột "Thời gian hiệu lực
      (ngày)"; N = 0 hiện "Không thời hạn".
- [x] **F2.** Cấu hình chung: ô M "Cảnh báo trước khi đóng nhu cầu" + nhãn trong popup Lịch sử cấu hình.
- [x] **F3.** Màn Nhu cầu khách hàng: cột "Thời gian hết hạn nhu cầu" tô cam + ghi chú
      `(còn X ngày)` / `(hết hạn hôm nay)` / `(quá hạn X ngày)`.
- [x] **F4.** 2 lỗi tự bắt khi soi trình duyệt: ô N để trống không báo lỗi (thiếu validate realtime) và
      nhu cầu quá hạn hiện "(còn -3 ngày)".

## Phase 3 — Tài liệu (2026-09-15)

- [x] **D1.** `design.md` — tóm tắt cơ chế + 7 quyết định kỹ thuật + 3 điểm lệch so với yêu cầu gốc.
- [x] **D2.** `testcase.xlsx` — **88 ca / 10 nhóm + nhóm phân quyền**, P0 62%, form chuẩn team (17 cột,
      9 mục mô tả, 2 khối summary DNS/TP). Script sinh: `gen_testcase.py`.

### Checkpoint — 2026-09-15

Vừa hoàn thành: Phase 3 (tài liệu + testcase). Code Phase 1/2 do đợt trước, đã merge vào
`tpe-develop-assign`.

Đang làm dở: không.

Bước tiếp theo:
- QA chạy testcase. Nhóm V/VI cần kỹ thuật chạy tay `assign:close-expired-customer-demands`
  (có `--dry-run` để liệt kê mà không ghi dữ liệu).
- Chốt lại với người viết yêu cầu 3 điểm lệch ghi ở cuối `design.md` (nhãn "Đóng" vs "Đã đóng",
  ẩn nút vs làm mờ, M theo công ty vs toàn cục).

Blocked: không.
