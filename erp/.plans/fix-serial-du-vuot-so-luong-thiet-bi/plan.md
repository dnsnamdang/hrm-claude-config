# Plan — Fix serial dư vượt số lượng thiết bị

Owner: @junfoke — Bắt đầu 2026-08-24

## Phase 1 — Bật lại chốt kiểm tra serial ở Duyệt kết quả (BE)
- [x] Điều tra nguồn serial dư (query prod) → xác định 2 luồng: nhập tay màn Serial (17) + nhập kết quả PGV (10); loại BBGN & phiếu xuất
- [x] Truy lịch sử git: xác nhận `checkValidateSerial` bị comment tắt qua 3 commit (2024-07 → 2025-07 → 2026-01)
- [x] Viết lại thân `checkValidateSerial` cho chuẩn TH1/TH2, clamp `free_slots`, chỉ đếm serial thêm mới thật sự
- [x] Bật lại lời gọi ở `store()` và `update()`
- [x] `php -l` sạch, giữ nguyên CRLF, `git diff --stat` gọn (1 file, 51+/36-)

## Phase 2 — Kiểm thử (chưa làm)
- [ ] Test TH1.1: thiết bị đủ serial, ĐỔI serial (có serial_id) → lưu được, serial cũ → ngừng
- [ ] Test TH1.2: thiết bị đủ serial, nhập serial MỚI (không serial_id) → bị chặn, báo "đã đủ…"
- [ ] Test TH2.1/2.2: còn chỗ trống, thêm serial mới trong hạn mức → lưu được
- [ ] Test regression: phiếu không đụng serial vẫn lưu/duyệt bình thường (kể cả thiết bị đang dư serial)
- [ ] Test ca bypass 5598 vẫn không bị chốt serial chặn sai

## Phase 3 — Dọn data & vá nguồn (chưa làm, cần team duyệt)
- [ ] Soạn query liệt kê mọi (product+customer) có serial active > exported_qty
- [ ] Soạn script tắt serial dư về status=2 (giữ serial gắn phiếu xuất) — KHÔNG tự chạy
- [ ] Đề xuất gom 1 helper chung kiểm serial ≤ qty cho `SerialController::addSerial` + `WrAssignTask::syncProduct`

### Checkpoint — 2026-08-24
Vừa hoàn thành: Phase 1 — bật lại + viết chuẩn `checkValidateSerial` cho TH1/TH2, bật 2 nơi gọi (store/update), lint sạch, giữ CRLF.
Đang làm dở: (không)
Bước tiếp theo: Phase 2 — user test 4 tình huống trên môi trường thật; sau đó bàn Phase 3 (dọn data).
Blocked: Cần team quyết có dọn data prod ngay không (bật chốt nhưng data cũ vẫn dư — chỉ chặn khi thêm serial mới, không kẹt phiếu).
