# Đề xuất: Agent liệt kê danh sách meeting — 11/11/2026 (user chọn "làm 1+2", CHƯA CODE)

## Bối cảnh
User hỏi "xem các meeting ở Hà Nội", "chi tiết các meeting của Tô Duy Nhân", "danh sách meeting của Phòng KDTM trong tháng" ⇒ Agent chỉ ra thống kê hoặc "chưa hỗ trợ" (lượt 9173–9175). Hiện có: `lich_meeting` (chỉ của người hỏi, cố ý từ chối người khác), `meeting_theo_thi_truong` (chỉ thống kê bars), `chi_tiet_meeting` / `bien_ban_va_viec_giao` (1 cuộc theo mã).

## (2) Mở rộng `meeting_theo_thi_truong` — liệt kê các cuộc đứng sau con số thống kê
- Thêm `liet_ke: true` ⇒ trả DANH SÁCH meeting (tối đa 20, mới nhất trước) thay cho nhóm; cùng mọi bộ lọc hiện có (pham_vi, phong_ban_id, tinh, tu_ngay/den_ngay) + MỚI `nhan_vien_id` (người chủ trì = `COALESCE(host_employee_id, created_by)`, như cột "theo người chủ trì").
- Phạm vi quyền GIỮ NGUYÊN: báo cáo "Kết quả meeting theo thị trường" (`MeetingMarketScope::base()` = `MeetingByMarketService::applyPermissionFilter`) ⇒ danh sách luôn khớp đúng con số thống kê vừa hiện. Panel meeting mở được vì `Meeting::canViewByReportScope(MeetingByMarketService)` đã có.
- Thẻ: `meetings` có sẵn (ngày, giờ · trạng thái, tên, chủ trì · KH · tỉnh) + `link` ⇒ bấm mở panel meeting (đã làm 11/11). `data` gửi model: total + 20 dòng gọn (code, ngày, tên, trạng thái, KH, chủ trì).
- Câu đi qua đường này: "xem các meeting ở Hà Nội" (sau thống kê), "liệt kê các cuộc Hoàng Phương Đông chủ trì tháng này ở Hà Nội".

## (1) Công cụ MỚI `meeting_cua_phong` — danh sách meeting theo phạm vi màn Danh sách meeting
- Phạm vi quyền: `MeetingGuard::listQuery()` (= `MeetingCriteria`, màn Danh sách meeting — mã `meeting.danh_sach_meeting.view` theo cấp + người tạo / chủ trì / thành phần) ∩ công ty đang làm. Không cần quyền báo cáo; meeting nội bộ (không KH) cũng có. Panel mở được (đã kiểm 11/11: `MeetingCriteria` ⊆ `Meeting::canView`).
- Tham số: `pham_vi` (phong — mặc định phòng người hỏi / `phong_ban_id`; cong_ty; nguoi — `nhan_vien_id` qua `tim_nhan_vien`), `tu_ngay`/`den_ngay` theo ngày họp (mặc định tháng này), `trang_thai` (len_lich / chot_lich / hoan_thanh / huy), `khach_hang_id` (qua `tim_khach_hang`), `tinh`, `co_khach_hang` (chỉ meeting với KH / chỉ nội bộ), `chua_co_bien_ban`.
- "Phòng" = phòng của NGƯỜI CHỦ TRÌ (`COALESCE(host_employee_id, created_by)` thuộc phòng) — khớp thống kê thị trường; đo 11/11: 2,868/2,877 meeting có KH (99.7%) phòng ghi trên meeting trùng phòng người chủ trì.
- Trả: total, đếm theo trạng thái, tối đa 20 dòng (mới nhất trước) — thẻ `meetings`, bấm mở panel.
- `lich_meeting` giữ nguyên (lịch CỦA TÔI); mô tả công cụ trỏ câu "của phòng / của anh X" sang `meeting_cua_phong`. Sửa kỳ vọng eval các câu trước đây chấm `na` (lịch họp người khác / cả phòng).

## Kiểm
PHPUnit: mỗi phạm vi có / không quyền, người ngoài phạm vi không lọt, liệt kê khớp tổng thống kê (2), nhan_vien_id ngoài phạm vi không lộ. Eval thêm ~8 câu. Playwright: thẻ meetings + bấm mở panel. Hỏi thật vài câu trên DB local.

## Câu hỏi chốt (hỏi lần lượt)
1. ✅ (11/11) "Meeting của anh X" = cuộc X CHỦ TRÌ (`COALESCE(host_employee_id, created_by)`) **+** cuộc X là THÀNH PHẦN phía công ty (`meeting_employees.type = 1`); mỗi dòng ghi vai trò "Chủ trì" / "Tham dự". Áp cho `meeting_cua_phong` pham_vi=nguoi. Riêng `meeting_theo_thi_truong` liet_ke + nhan_vien_id vẫn theo NGƯỜI CHỦ TRÌ (khớp cột thống kê "theo người chủ trì").
