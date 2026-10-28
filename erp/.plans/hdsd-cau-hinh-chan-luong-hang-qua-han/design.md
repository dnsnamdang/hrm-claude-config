# HDSD màn "Cấu hình chặn luồng hàng quá hạn" (ERP, nhánh gop_db)

- **Output:** `HDSD_CauHinhChanLuongHangQuaHan.docx` (cùng thư mục này), 15 trang.
- **Generator:** `gen_hdsd.py` — khuôn chi tiết `HdsdBuilder` (hrm/.claude/skills/hdsd-documenter/assets/hdsd_engine.py),
  bám file mẫu user đưa `HDSD_YeuCauXuatHang.docx` (14/10/2026).
- **Không chèn ảnh** (như mẫu) → các ô "[Vị trí chèn ảnh] …".

## Nguồn khảo sát
- ERP: `routes/web.php` :6945-6949, `Common/DueConfigsController.php`,
  `Middleware/CheckDueConfigs.php` (tab 1), `Middleware/CheckDueConfigsManager.php` +
  `Services/DueConfig/DueConfigBlockService.php` (tab 2), `Api/DueConfigController.php`,
  views `common/due_configs/{edit,overdue-modal}.blade.php`, `layouts/topmenubar.blade.php` :2001.
- HRM: `hrm-api/app/Http/Middleware/CheckDueConfigsManager.php`, `Modules/Finance` CheckDueConfig,
  các route có chặn ở Timesheet / Assign / PaymentBusinessRequest / PaymentProfile / SettlementContract.

## Cách dựng lại (Windows, cần Microsoft Word để cập nhật mục lục)
```bash
python gen_hdsd.py
```
Dùng `finish_win()` thay `finish()` của engine: engine báo nhầm vì tiêu đề "TỔNG QUAN PHẦN MỀM"
trùng với tiêu đề của khung mẫu.

## Cấu trúc
Bìa → Mục lục → Danh mục hình → TỔNG QUAN (thuật ngữ, lịch sử, giới thiệu + đường dẫn, quyền)
→ PHẦN 1 Truy cập & bố cục → PHẦN 2 Chặn nhân viên (tab 1) → PHẦN 3 Chặn trưởng phòng duyệt (tab 2)
→ PHẦN 4 Thao tác cấu hình & Lưu → PHẦN 5 Lịch sử chỉnh sửa → PHẦN 6 FAQ.

Hành vi nghi lỗi (quyền "Cấu hình hệ thống" không tồn tại, ô 37 lệch tên phía ERP, ô 39/52 phía HRM…)
KHÔNG ghi vào HDSD — đã báo riêng, xem testcase `../cau-hinh-chan-luong-hang-qua-han/`.
