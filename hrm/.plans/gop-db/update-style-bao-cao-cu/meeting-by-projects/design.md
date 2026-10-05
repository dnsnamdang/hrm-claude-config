# Update style — Báo cáo thời gian meeting theo dự án (tóm tắt)

**Route:** `/assign/report/meeting-by-projects` · **Folder lớn:** `../design.md` · Mở: 04/10/2026 · @namdangit
**Mockup:** `mockup.html` (ĐÃ DUYỆT 04/10) · **Khuôn:** skill `report-styles`
**Trạng thái:** ĐÃ MERGE gop_db 05/10/2026 (api 8de764f79, client 2f04d1dfb).

## Hiện trạng (đọc code 04/10/2026)

- FE `hrm-client/pages/assign/report/meeting-by-projects/`: bộ lọc (Xem theo thời gian Tháng/Năm/Tuỳ chọn + Tháng +
  Năm, Công ty qua `V2BaseCompanyDepartmentFilter`, NV tạo dự án, Khách hàng tự dựng dropdown, Dự án, Hình thức, Loại,
  Giai đoạn) · biểu đồ Top 5 (`TopProjectsChart`) · bảng 12 cột tiêu đề 2 tầng, chip bấm mở 4 popup `b-modal`
  (theo trạng thái / hình thức / loại / người tham gia) · In mở `print.vue` tab riêng · Excel.
- BE `Modules/Assign/Services/Report/MeetingByProjectsService.php`: `getData()` **cắt trang theo meeting** rồi mới
  gom dự án → 1 dự án bị tách 2 trang, số tổng dòng dự án chỉ của trang đó. Quyền 3 cấp trong
  `applyPermissionFilter()` (tổng công ty / công ty / dự án mình tạo hoặc là NVKD). Chỉ tính meeting
  `Meeting::REPORT_STATUSES` = Chốt lịch + Hoàn thành. Drill `meetings-by-status|type` có đoạn lọc công ty bị
  comment — cần rà khi viết `item-list`.

## Quyết định đã chốt (04/10/2026)

| # | Vấn đề | Chốt |
|---|---|---|
| 1 | Mức độ | Đổi cả bố cục theo khuôn report-styles, có sửa BE |
| 2 | Biểu đồ Top 5 | Bỏ hẳn (component + endpoint `chart-data`) |
| 3 | Cấp cây | Dự án ▸ Meeting (2 cấp). Ô chọn cấp: Chỉ dự án (mặc định) / Đến meeting. Phân trang theo dự án |
| 4 | Khối tổng hợp | PHẠM VI: Dự án · Meeting · Khách hàng · Người tham gia · Tổng thời lượng (không bấm) — TRẠNG THÁI & HÌNH THỨC: Chốt lịch · Hoàn thành · Trực tiếp · Online (ô 0 ẩn) |
| 5 | Cột | 14 cột: STT · Dự án / Meeting · Khách hàng · Người tạo dự án · Tiến trình · Giai đoạn · **Số meeting** · **Trạng thái** · Thời gian · Thời lượng (phút) · Loại meeting · Hình thức · Người tham gia · Biên bản |
| 6 | Popup người tham gia | 1 danh sách, cột Phía + ô lọc Phía (thay 2 tab); các popup meeting gộp làm 1 |
| 7 | Ô thời gian | "Kỳ theo dõi" của khuôn: Tuần này · Tháng này · Năm nay (mặc định) · Năm trước · Tuỳ chọn |
| 8 | Meeting được tính | CHỈ meeting khớp TOÀN BỘ bộ lọc: trạng thái Chốt lịch/Hoàn thành + ngày họp trong kỳ + loại + hình thức. Dự án hiện khi còn ≥ 1 meeting khớp. Tổng hợp = TỔNG = Σ dòng dự án = số dòng popup. (Cũ: lọc ở cấp dự án rồi hiện MỌI meeting của dự án, kể cả Đang tạo/Lên lịch/Hủy — local 29 meeting) → số sẽ khác báo cáo cũ |
| 10 | Xem meeting từ báo cáo | Nới `Meeting::canView()` khớp ĐÚNG phạm vi báo cáo (user chốt 05/10): 1060 → mọi meeting gắn dự án TKT · 1061 → dự án thuộc công ty hiện tại HOẶC dự án mình tạo · không quyền → dự án mình tạo / mình là NVKD. Dùng chung `MeetingByProjectsReportService::applyProjectScope()`. Chỉ quyền XEM, không lọc trạng thái |
| 9 | Gộp người tham gia phía KH | Theo họ tên + SĐT (chuẩn hoá: bỏ khoảng trắng thừa, không phân biệt hoa thường). Cũ: mỗi lượt có mặt = 1 người (local 741 lượt → 642 người). Phía công ty giữ gộp theo employee_id |

Điểm UI tự chốt: xem comment đầu `mockup.html` (mục a → h).

## Phạm vi dự kiến khi code (chốt lại ở plan.md)

- **BE** (`hrm-api`, Modules/Assign): `index` trả `{ summary, groups (trang dự án), meta }` phân trang theo dự án;
  `filter-options` (+ `can_change_company`); `item-list` (meeting) + `participant-list`; `export`, `item-list/export`,
  `print-list-data`; tham số `period` + `from/to`. Bỏ `chart-data` + 4 endpoint drill cũ khi FE không còn gọi.
  Không migration, không quyền mới (giữ 2 quyền "Xem báo cáo meeting theo dự án theo tổng công ty / theo công ty").
- **FE** (`hrm-client`): viết lại `index.vue` + `components/` theo `template/` của skill; xoá `print.vue`,
  `TopProjectsChart`, 4 popup cũ nếu không còn chỗ nào import.
- **Kiểm:** Playwright đo DOM (skill mục 6), PHPUnit phân trang theo dự án + quyền có/không, e2e spec mới
  (chỉ chạy khi user yêu cầu, `--workers=1`).
