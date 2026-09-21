# Plan — #10841 phản hồi tester: đưa LÝ DO HỦY vào mục Lịch sử (Yêu cầu làm giải pháp)

Phụ trách: @cuong61n · Nhánh: `tpe` · Ngày: 2026-09-16

Phản hồi #13 (Nguyễn Minh Hằng): *"Phần lý do hủy cho vào mục lịch sử đi"*.

## Hiện trạng trước khi sửa
- `RequestSolutionService::cancel()` chỉ ghi cột `cancel_reason` / `cancelled_by` / `cancelled_at`, KHÔNG sinh dòng lịch sử.
- Yêu cầu làm giải pháp chưa có bảng log riêng; `SystemLogService::requestSolutionLogs()` chỉ dựng từ cột audit (Tạo mới / Chỉnh sửa gần nhất) ⇒ mở Lịch sử không thấy vì sao phiếu bị hủy.
- Lỗi cùng loại ở thao tác **Từ chối** (`reject_reason` cũng không hiện).

## Đã làm
- [x] `SystemLogService::requestSolutionLogs()` ghép thêm 2 dòng dựng từ cột trên bảng chính, theo đúng khuôn mục "Đóng dự án" của dự án TKT: **Hủy yêu cầu làm giải pháp** (ghi chú = `cancel_reason`) và **Từ chối** (ghi chú = `reject_reason`), xếp trước các dòng audit.
- [x] Không tạo bảng log mới, không migration — lý do đã lưu sẵn trên bảng chính (skill entity-history §4.1).
- [x] Nhóm bộ lọc: `cancelled` rơi vào nhóm mặc định *Thay đổi trạng thái*, `rejected` đã có sẵn trong `ACTION_GROUP_MAP` — bộ lọc vẫn đúng 3 nhóm chuẩn.

## Kiểm thử (script bootstrap Laravel, mỗi ca bọc transaction rồi rollback)
- [x] CA1 chưa hủy/từ chối → chỉ 2 dòng audit, không sinh dòng rác
- [x] CA2 đã hủy có lý do → dòng "Hủy yêu cầu làm giải pháp" + ghi chú đúng nội dung
- [x] CA3 đã từ chối có lý do → dòng "Từ chối" + ghi chú
- [x] CA4 vừa từ chối vừa hủy → 2 dòng, xếp MỚI → CŨ đúng thứ tự
- [x] CA5 hủy không có lý do (dữ liệu cũ) → vẫn có dòng, ghi chú trống, không lỗi
- [x] Giao diện màn chi tiết `/assign/request-solution/24`: khối Lịch sử hiện dòng "Hủy yêu cầu làm giải pháp" kèm lý do trong khối ghi chú
- [x] Dữ liệu thử đã khôi phục nguyên trạng

## Nâng cấp theo yêu cầu: LỊCH SỬ CHI TIẾT (2026-09-16)
User yêu cầu làm đúng skill `entity-history` chứ không chỉ hiện lý do hủy ⇒ dựng lịch sử subset-diff đầy đủ cho Yêu cầu làm giải pháp.

- [x] Migration `request_solution_history` (mẫu `meeting_history`): action / old_value / new_value / note / changed_by / changed_at
- [x] Entity `RequestSolutionHistory`
- [x] `RequestSolutionHistoryService`: snapshot 18 trường theo GIÁ TRỊ HIỂN THỊ, `log()`, `logStatus()`, `diff()`, `normalize()` (chống log rác `5.00` vs `5`, `''` vs null)
- [x] Gắn vào `RequestSolutionService`: store → `create`; update → `update` + dòng riêng `change_status`; receive → `change_status` + nội dung; reject/cancel → `change_status` kèm LÝ DO (skill §3a, §4.1)
- [x] `SystemLogService::requestSolutionLogs()` đọc bảng mới (dùng lại `MeetingHistoryService::changesFrom`), phiếu CŨ chưa có log vẫn fallback dựng từ cột audit + cột lý do
- [x] Nhóm bộ lọc: create / update / change_status → đúng 3 nhóm chuẩn

### Trường được theo dõi (18)
Tiêu đề · Dự án tiền khả thi · Giai đoạn dự án · Phòng tiếp nhận · Nhóm ngành · Nhóm giải pháp ·
Ngày KH cần giải pháp · Ngày KH cần báo giá · Ngày nội bộ cần giải pháp · Ngày chốt giải pháp ·
Ghi chú · Người phụ trách (PM) · SĐT PM · Ghi chú PM · Người tiếp nhận · Ngày gửi tiếp nhận ·
Hạn tiếp nhận · Tệp đính kèm. Trạng thái KHÔNG nằm trong snapshot (đi dòng riêng).

### Kết quả test — script `test_history_fields.php` (30 ca, mỗi ca transaction + rollback)
- A. 17 ca đổi ĐÚNG MỘT trường → mỗi ca đúng 1 dòng log, đúng tên trường, đúng giá trị cũ → mới
- B. không sửa gì / lưu lại y nguyên / `5.00` vs `5` / `''` vs null → KHÔNG ghi log rác; đổi 3 trường → 1 dòng 3 khoá; xoá trắng → "giá trị → (trống)"
- B2. thêm 1 tệp → 1 dòng "đã thêm"; xoá 1 tệp → 1 dòng "đã xoá" (giữ nguyên đường dẫn)
- C. hủy/từ chối → dòng `change_status` riêng + ghi chú lý do, đọc qua `getLogs()` ra nhãn "Đổi trạng thái", nhóm lọc `status`; trạng thái không đổi & không lý do → không ghi
- D. sắp xếp MỚI → CŨ; phiếu cũ chưa có log vẫn dựng được từ cột audit
- **30 ĐẠT / 0 HỎNG**, không để lại dòng log rác

### Kiểm trên giao diện (Playwright, phiếu TPE.YCP.TC.26.0021)
Sửa Tiêu đề + Giai đoạn + Ghi chú rồi Hủy kèm lý do → khối Lịch sử hiện 2 mục: "Đổi trạng thái"
(Nháp → Đã hủy + ghi chú lý do) và "Chỉnh sửa" (3 dòng cũ→mới, đỏ→xanh). Ảnh: `HRM/lichsu-yclgp-chitiet.png`.
Dữ liệu demo đã khôi phục nguyên trạng, bảng log đã dọn sạch.

## Còn lại
- [ ] Commit + push (chờ user)
- [ ] Trả lời tester trên Redmine #10841
