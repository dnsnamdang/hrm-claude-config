# Dữ liệu tạo/sửa cho HDSD Phê duyệt — Yêu cầu giải pháp (02/10/2026, DB local_hrm_erp)

- form_templates id=4 `PTT-2026-00004` "Phiếu khảo sát thiết bị thực hành cơ điện tử – khí nén" (Đã ban hành, ứng dụng 130 "Đào tạo ngành cơ điện tử") + 1 section + 4 câu hỏi — INSERT bằng SQL.
- prospective_projects id=153 `HN_DA.UD.0130.2026.DA093` "Cung cấp bàn thực hành cơ điện tử – PLC khí nén cho Trường CĐ Công nghiệp Hà Nội" — SQL nhân bản từ id 150 (đổi mã/tên/ứng dụng 130, status=2, created_by=13). Snapshot phiếu id=8 sinh bằng tinker `handleFormTemplateSnapshot`.
- (Đã hoàn tác) lỡ sinh snapshot phiếu id=7 cho dự án 150 (của agent khác) → đã xoá snapshot 7 + lịch sử phiếu id=3, trả `form_template_snapshot_id` của 150 về NULL (cột updated_at của 150 bị đổi thành 15:40:20).
- prospective_projects 153: SQL đặt industry_id=368 (Khí nén - thủy lực), scope_id=2 cho khớp ứng dụng 130.
- request_solutions id=34 `TPE.YCP.TC.26.0912` "Yêu cầu làm giải pháp bàn thực hành cơ điện tử – PLC khí nén Trường CĐ Công nghiệp Hà Nội" — tạo qua giao diện (Lưu nháp) bởi DNS Admin, dự án 153.
- id=34: sửa bằng giao diện (Lưu và gửi → Chờ tiếp nhận); SQL tạm đặt status=1 để chụp màn Sửa rồi trả lại status=2.
- id=34: tại màn chi tiết (tab Phiếu thu thập thông tin) gửi "Yêu cầu bổ sung" 1 câu hỏi "Vui lòng bổ sung bản vẽ mặt bằng phòng thực hành và vị trí cấp khí nén…" → trạng thái Yêu cầu bổ sung; dự án 153: trả lời câu hỏi bổ sung + 4 câu trả lời phiếu (Lưu phiếu); sau đó Sửa id=34 → Lưu và gửi → về lại Chờ tiếp nhận (hạn tiếp nhận tính lại).
- Không bấm "Xác nhận tiếp nhận"; các hộp Xóa/Tiếp nhận chỉ mở để chụp rồi Hủy/Đóng.
