# Update style — Báo cáo meeting nhân viên theo thời gian (tóm tắt)

**Route:** `/assign/report/meeting-by-employees` · **Folder lớn:** `../design.md` · Mở: 05/10/2026 · @namdangit
**Khuôn:** skill `report-styles` · **Tham chiếu gần nhất:** báo cáo 1 `../meeting-by-projects/` (đã merge gop_db 05/10)
**Trạng thái:** CODE XONG 05/10/2026 — 10 task + final review sạch; PHPUnit 40 + 97 xanh; e2e đã viết (10 api + 11 ui) CHƯA chạy. Nhánh `gop_db-update-style-meeting-by-employees` (api 5b7934f3e · client b442bc862) ĐÃ PUSH + ĐÃ MERGE gop_db 05/10 (api 9696baa26 · client 6c0b509de). Ledger: `sdd-ledger.md`.

## Hiện trạng (đọc `origin/gop_db` 05/10/2026: api 8de764f79, client 2f04d1dfb)

**FE** `hrm-client/pages/assign/report/meeting-by-employees/` (index 1080 dòng + 8 component + `print.vue`):
- Bộ lọc: Xem theo thời gian (Tháng/Năm/Tuỳ chọn) + Tháng + Năm / khoảng ngày · Công ty–Phòng–Bộ phận–Nhân viên
  (`V2BaseCompanyDepartmentFilter` + `permissions`) · Khách hàng (dropdown tự dựng) · Dự án (lọc theo KH) · Loại · Hình thức.
- Biểu đồ `TopDepartmentsChart` (Top phòng ban, 2 trục Số meeting / Tổng phút, sắp theo count|minutes) — endpoint `chart-data`.
- Bảng cây 4 cấp **Công ty ▸ Phòng ban ▸ Nhân viên ▸ Meeting**, tiêu đề 2 tầng, 14 cột: STT · Tên · Chức vụ · Mã NV ·
  Thời gian · Thời lượng · Loại meeting · Hình thức · Số người tham gia · Dự án · Khách hàng · Biên bản · Nội dung · Kết luận.
- Popup `b-modal`: theo trạng thái / hình thức / loại / người tham gia theo phía / người tham gia 1 meeting.
  `MeetingsByStatusModal` gọi route `meeting-by-employees/meetings-by-status` **không tồn tại** (popup chết sẵn).
- In: `MeetingByEmployeesPrintConfigModal` (cấu hình in #11145 AC5) + `print.vue`. Excel: `export`.

**BE** `Modules/Assign/Services/Report/MeetingByEmployeesService.php` (1527 dòng), route trong `ReportController`:
- **Meeting được tính (Redmine #11145):** đã qua giờ bắt đầu → Hoàn thành + **Hủy**; chưa tới giờ → Chốt lịch; thiếu
  giờ bắt đầu → Hoàn thành/Hủy. Hủy được ĐẾM buổi nhưng **0 phút**. (Khác báo cáo 1: chỉ Chốt lịch + Hoàn thành.)
- Gom theo NV tham gia phía công ty (`company_members.employee_id`), đơn vị lấy từ hồ sơ NV **hiện tại**.
  Chỉ NV khớp bộ lọc công ty/phòng/bộ phận/NV mới hiện. 1 meeting có NV 2 phòng → hiện dưới cả 2 phòng; cấp phòng/công ty
  đếm meeting không trùng.
- **Bộ lọc Khách hàng + Dự án CHẾT ở BE**: FE gửi `customer_id`/`project_id`, `getFilteredQuery` không đọc → lọc im lặng không ăn.
- Người tham gia: phía công ty gộp theo employee_id; phía KH đếm theo `customer_members.id` (mỗi lượt = 1 người).
- Dự án/KH của meeting: chỉ lấy dự án ĐẦU TIÊN gắn meeting.
- Phân trang: **cắt theo số meeting** (30/trang) xuyên qua nhân viên → 1 NV có thể bị tách 2 trang.
- Quyền 4 mức: "…theo tổng công ty" · "…theo công ty" (công ty hiện tại) · "…theo phòng ban" (phòng/bộ phận mình quản lý)
  · không quyền → chỉ dòng của chính mình.

## Quyết định (điền dần khi hỏi)

| # | Vấn đề | Chốt |
|---|---|---|
| 1 | Mức độ | Đổi cả bố cục theo khuôn report-styles + sửa BE (như báo cáo 1). Sửa luôn lọc KH/Dự án chết + popup trạng thái hỏng |
| 2 | Meeting được tính | GIỮ quy tắc #11145: đã qua giờ → Hoàn thành + Hủy · chưa tới giờ → Chốt lịch · thiếu giờ → Hoàn thành/Hủy. Hủy đếm buổi, 0 phút. Lấy CẢ meeting không gắn dự án (ô Dự án/KH trống) |
| 3 | Biểu đồ Top phòng ban | Bỏ hẳn (`TopDepartmentsChart` + endpoint `chart-data`) |
| 4 | Cây + phân trang | 4 cấp Công ty ▸ Phòng ban ▸ Nhân viên ▸ Meeting. Phân trang theo NHÂN VIÊN (20/trang, không cắt ngang NV); dòng Công ty/Phòng lặp ở trang sau, số trên đó luôn là tổng ĐỦ. Mặc định bung tới Nhân viên |
| 5 | Khối tổng hợp | PHẠM VI: Nhân viên · Meeting · Người tham gia · Tổng thời lượng (không bấm) — TRẠNG THÁI & HÌNH THỨC: Chốt lịch · Hoàn thành · Đã hủy · Trực tiếp · Online · Chưa xác định (ô 0 ẩn) |
| 6 | Cột | 13 cột (Mã NV cũ thành mã phụ sau tên): STT · Công ty / Phòng / NV / Meeting (mã NV = mã phụ) · Chức vụ (HỒ SƠ NV; dòng meeting hiện vai trò trong meeting nếu có) · Số meeting · Trạng thái · Thời gian · Thời lượng (phút) · Loại · Người tham gia · Dự án · Khách hàng · Nội dung · Biên bản. BỎ Hình thức + Kết luận (Hình thức vẫn còn ở khối tổng hợp + bộ lọc) |
| 7 | Người tham gia | Theo báo cáo 1: KH gộp họ tên + SĐT chuẩn hoá, công ty theo employee_id — dùng lại `MeetingParticipantCounter`. Popup 1 danh sách có cột Phía |
| 8 | Bộ lọc | Kỳ theo dõi (Tuần này · Tháng này · Năm nay mặc định · Năm trước · Tuỳ chọn) · Công ty (`can_change_company`) · Phòng ban · Bộ phận · Nhân viên · Khách hàng · Dự án · Loại · Hình thức. KH/Dự án: chỉ meeting gắn KH/dự án đó. Danh mục từ `filter-options` theo quyền |
| 9 | Xem meeting từ báo cáo | Nới `Meeting::canView()` theo đúng phạm vi báo cáo (dùng chung 1 hàm scope): tổng công ty → meeting có NV tham gia · công ty → có NV công ty hiện tại · phòng ban → có NV phòng/bộ phận mình quản lý. Chỉ quyền XEM |
| 10 | In | PrintOptionsModal (Tổng hợp/Chi tiết) + GIỮ tick chọn cột (#11145 AC5; STT + cột Đối tượng luôn in) |
| 11 | Đơn vị NV | Đơn vị HIỆN TẠI trong hồ sơ (như cũ), quyền phòng ban cũng xét theo đơn vị hiện tại |

| 12 | Thời lượng dòng cha / TỔNG / khối tổng hợp | PHÚT-NGƯỜI: cộng dồn dòng NV (1 meeting 60' có 3 NV cùng phòng → phòng 180'). Σ con = cha. Tổng thời lượng ≠ tổng phút popup danh sách meeting (ghi chú ⓘ) |
| 13 | Bấm số Nhân viên ở tổng hợp | Popup danh sách NV riêng: STT · NV (mã) · Công ty · Phòng ban · Chức vụ · Số meeting · Thời lượng (phút); số dòng = số NV |
| 14 | Cột NV tham gia trong popup meeting | Liệt kê TẤT CẢ NV công ty của meeting, NV thuộc phạm vi đang xem in đậm (lộ tên NV ngoài quyền — chỉ tên) |
| 15 | Bản in | Tick chọn cột áp cho CẢ 2 bản. Bản Chi tiết: mỗi dòng = 1 NV × 1 meeting (có cột Công ty, Phòng, NV) |

| 16 | Nguồn Khách hàng | Cột + lọc KH theo `meetings.customer_id`, thiếu thì KH dự án (sửa chữ #2: meeting không dự án vẫn hiện KH) |
| 17 | Xuất Excel (bộ lọc) | Tải ngay cây đủ 13 cột như báo cáo 1, không popup chọn |
| 18 | Danh mục ô Phòng/Bộ phận/NV | Chỉ đơn vị/NV có meeting trong kỳ, trong quyền (giữ mục đang chọn khi đổi kỳ) |
| 19 | Quyền 1059 (phòng ban) | Giữ như cũ: chỉ NV phòng/bộ phận mình quản lý, không tự cộng chính mình |
| 20 | Lọc Trạng thái (bổ sung 05/10) | Ô lọc chọn 1: Hoàn thành / Đã hủy (không có Chốt lịch); trống = mọi trạng thái được tính. FE gửi `status` (BE có sẵn). Nhánh `gop_db-mbe-loc-trang-thai` (client), bộ lọc chia lại 2 hàng × 12 cột |

Điểm UI tự chốt (05/10): đúng 13 cột · Loại meeting dòng cha "n Loại · n Loại" bấm được (như báo cáo 1) · vai trò meeting hiện nguyên chữ đã nhập.

Ghi chú: meeting có NV ở 2 phòng hiện dưới cả 2 phòng; dòng Phòng/Công ty/TỔNG đếm meeting không trùng → Số MEETING Σ dòng con có thể > dòng cha (như ruling báo cáo 1); riêng thời lượng là phút-người nên Σ con = cha (#12).
