# Dữ liệu tạo cho SRS Yêu cầu làm giải pháp (05/10/2026, DB local_hrm_erp)

Không sửa / xoá dữ liệu có sẵn (YCGP 21–34, dự án 145–154 chỉ mở để chụp, không lưu).

## prospective_projects (SQL — `clone_projects.py`, nhân bản từ id 152, created_by=13, status=2, implementation_type=3, bỏ phiếu thu thập)
- id **155** `HN_KD3.UD.0100.2026.DA094` "Cung cấp thiết bị chẩn đoán và cân chỉnh góc lái cho xưởng dịch vụ Toyota Hải Dương"
- id **156** `HN_KD3.UD.0100.2026.DA095` "Cung cấp cầu nâng và thiết bị bảo dưỡng nhanh cho xưởng dịch vụ Mazda Thái Bình"

## request_solutions
- id **36** `TPE.YCP.TC.26.0914` (dự án 155) — tạo qua giao diện, **Lưu nháp**, phòng tiếp nhận 51 (PHÒNG KỸ THUẬT CÔNG NGHỆ). Sau khi chụp Sửa / Xóa / Hủy: **Hủy** qua giao diện (lý do "Khách hàng tạm dừng đầu tư…") → Đã hủy; dự án 155 về Thu thập thông tin dự án.
- id **37** `TPE.YCP.TC.26.0915` (dự án 156) — tạo qua giao diện từ lối vào Dự án TKT, **Lưu và gửi** → Chờ tiếp nhận; sau đó **Tiếp nhận qua API** (PUT receive, PM = DNS Admin, ngày dự kiến 20/11/2026) → Đã tiếp nhận, receive_id=13 (để chụp nút "Làm giải pháp").
- Kèm theo: các dòng `request_solution_history` của 36, 37 do hệ thống tự ghi; dự án 156 chuyển trạng thái theo luồng gửi yêu cầu.

## Thao tác chỉ mở để chụp (không lưu)
- id 25 (Yêu cầu bổ sung): mở màn Sửa + Chi tiết.
- id 34 (Chờ tiếp nhận): mở các tab, cửa sổ Tiếp nhận (Esc) và Xác nhận từ chối (Không).
- Hộp Xác nhận xóa (Hủy), cửa sổ Hủy bấm Đồng ý khi trống (máy chủ trả lỗi, không đổi dữ liệu).

Ghi chú: id 35 (dự án 161) là của agent khác tạo cùng thời điểm, không phải của SRS này.
