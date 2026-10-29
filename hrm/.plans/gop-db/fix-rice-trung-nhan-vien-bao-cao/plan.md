# Báo cáo cơm chi tiết hiện trùng nhân viên (PROD) — @cuong61n

Không có số Redmine. User gửi ảnh ngày 29/10/2026: màn Báo cáo → Báo cáo cơm chi tiết (hrm.eteksofts.com), phòng HN_NSHC có 2 dòng "Nguyễn Thị Huế" (1 dòng có MCC 12510963, 1 dòng "MCC: —").

## Điều tra (29/10/2026)
- [x] Nghiệp vụ: báo cáo đọc danh sách nhân viên của phân hệ Cơm (`rice_employee_infos`), không đọc hồ sơ nhân sự. Hồ sơ chỉ có 1 chị Huế (employee 1090 / info 1517); bảng cơm có 2 dòng: 1659 (đúng) + 1661 (thừa, không mã cơm, không employee_id) — 29/10/2026
- [x] Quét toàn bộ bảng cơm (DB chung hrm_erp_gop + DB riêng hrm_toyota), so trong CÙNG công ty cơm (công ty cơm 3/4 đánh employee_info_id theo DB etekpower/etek riêng → ~490 "trùng" là báo động giả). Có 5 người bị nhân bản, 36 dòng thừa: Huế (1), Phạm Vũ Bích Liên – Etek Green (14), Nguyễn Bảo Hà – Etekpower (10), Nguyễn Huy Hoàng – TP Sài Gòn (9), Nguyễn Anh Tuấn – Toyota (2) — 29/10/2026
- [x] Nguyên nhân: hook `EmployeeInfo::saved` tạo dòng cơm qua connection riêng `mysql_tpe`, ngoài transaction lưu hồ sơ → lưu nhân viên lỗi bị rollback vẫn để lại dòng cơm, mỗi lần bấm Lưu lại thêm 1 dòng (dòng thừa trỏ tới employee_info_id không còn tồn tại, tạo cách nhau vài chục giây). Đã được fix từ 08/09/2026 (commit 07b0bf8fe — `EmployeeInfoController::store` mở transaction trên cả 2 connection, xem `.plans/fix-employee-rice-ssn-orphan`); mọi ca trùng ở tpe/etek/etekgreen/etekpower đều trước ngày đó — 29/10/2026
- [x] Toyota PROD vẫn chạy code nhánh tpe kéo về 28/08/2026 (chưa có fix) → giải thích ca trùng 28/09/2026 — 29/10/2026

## Dọn dữ liệu PROD (29/10/2026)
- [x] Sao lưu các dòng xoá ra file TSV ở máy local (scratchpad phiên 29/10) — 29/10/2026
- [x] hrm_erp_gop: xoá 34 dòng `rice_employee_infos` (1661, 1912–1914, 1917–1927, 1955–1964, 1854–1862) + 23 liên kết máy nhận diện `rice_employee_info_conn_infos`; điều kiện chặn: rice_ssn NULL, employee_id NULL, không có đăng ký cơm/hỗ trợ. Đã kiểm 7 bảng tham chiếu: không có lượt đăng ký nào; máy nhận người theo rice_ssn nên không để lại rác trên máy — 29/10/2026
- [x] hrm_toyota: xoá 2 dòng 150, 151 (Nguyễn Anh Tuấn 12600502, chưa có hồ sơ nhân sự thật) — 29/10/2026
- [x] Kiểm lại: không còn trùng mã / employee_info_id trong cùng công ty cơm; 4 dòng đúng (1659, 1864, 1928, 1966) giữ nguyên — 29/10/2026
- Để nguyên (không làm báo cáo hiện trùng): DNS Admin (636, TK test Etek Green), Vũ Ngọc Sơn Etek (1585 có 85 lượt đăng ký, dòng 2021 đã khoá)

## Sửa code
- [x] Thử bọc hook đồng bộ cơm trong `DB::afterCommit` → test local: chặn được dòng mồ côi khi rollback NHƯNG gây hồi quy: `store()` cần dòng cơm có sẵn trong transaction để hook `Employee::saved` điền rice_ssn + đẩy khuôn mặt lên máy cơm → BỎ, không commit (nguyên nhân gốc đã fix từ 08/09) — 29/10/2026
- [x] Toyota PROD: KHÔNG deploy theo quyết định user (29/10/2026) — vẫn chạy code 28/08, có thể tái diễn dòng cơm trùng khi lưu hồ sơ lỗi
- [ ] (Đề xuất, chưa làm) Các đường lưu hồ sơ khác ngoài `store()` (EmployeeController, HumanService, duyệt yêu cầu cập nhật hồ sơ) vẫn chỉ mở transaction trên mysql — rủi ro thấp vì chủ yếu là sửa, không tạo dòng cơm mới

### Checkpoint — 2026-10-29
Vừa hoàn thành: dọn 36 dòng cơm trùng trên PROD, xác định nguyên nhân đã fix từ 08/09
Đang làm dở: —
Bước tiếp theo: — (đóng việc; Toyota để nguyên theo user)
Blocked:
