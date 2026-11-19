# #10685 — [App Quản lý dự án] Chi tiết task hiển thị sai Mã-Tên GP — @cuong61n

Nguyên nhân: app đọc object `solution` (BE `DetailTaskResource` không trả) → rơi xuống nhánh dự phòng lấy mã-tên DỰ ÁN cho ô "Mã-Tên giải pháp". BE đã trả sẵn trường phẳng `solution_code/_name`, `project_code/_name`, `solution_module_code/_name`.
- [x] App `ui/task/task_detail_page.dart`: 3 dòng khối "Giải pháp & Dự án" dùng trường phẳng, ghép "Mã - Tên" (`_codeName`); bỏ việc lấy dự án đắp vào ô giải pháp; Dự án + Hạng mục/Module hiện cả mã và tên theo yêu cầu (19/10/2026)
- [x] Test simulator: task không gắn GP/DA → 3 dòng "-" ✓; task gắn DA 152/GP 955/HM 956 (dựng tạm trên 986, đã trả lại) → "…DA090_GP01 - Giải pháp…", "…DA090 - Cung cấp…", "…GP01_HM02 - Ốp bản vẽ móng máy" ✓
