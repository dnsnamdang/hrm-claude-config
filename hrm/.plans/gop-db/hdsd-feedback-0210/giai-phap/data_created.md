# Dữ liệu tạo/sửa cho HDSD Giải pháp (02/10/2026, DB local_hrm_erp)

- prospective_projects id=152 `HN_KD3.UD.0100.2026.DA090` "Cung cấp thiết bị xưởng dịch vụ 3S Hyundai Bắc Ninh" — INSERT bằng SQL (nhân bản từ id 142, đổi mã/tên, implementation_type=3, created_by/main_sale=13).
- request_solutions id=33 `TPE.YCP.TC.26.0911` — tạo qua API, tiếp nhận qua API (receive_dept=55), sau đó SQL đổi pm_id=970.
- solutions id=955 `HN_KD3.UD.0100.2026.DA090_GP01` "Giải pháp thiết bị xưởng dịch vụ 3S Hyundai Bắc Ninh" — tạo qua API (created_by=13 DNS Admin = vai Trưởng phòng GP), 2 hạng mục 955/956. SQL: pm_id 13→970, leader 13→781, thành viên HM01 781→835, HM02 835→1142 (vì admin không có trong danh sách chọn nhân sự).
- Đổi mật khẩu local (test) = `HdsdGp@2026`: employees 970 (hungvq.da@tanphat.com – PM), 781 (sondp.da@tanphat.com – Leader).
- Luồng chạy qua giao diện: PM 970 bấm "Giao cho Leader" (GP 955 → Chờ Leader duyệt), Leader 781 bấm "Lưu và duyệt" (→ Đang triển khai).
- tasks id 963, 964 (gắn GP 955, hạng mục 955/956) và issues id 1 `ISS-202610-0001` — tạo qua API bằng tài khoản PM 970.
- tasks id 965 (Nháp, để có nút Xoá) — API bằng PM 970.
- solution_progress: Phân bổ % hạng mục HM01=60, HM02=40 — nhập trên giao diện (tab Tiến độ) bằng PM 970.
- bom_lists id=28 `BOM-2026-00028` "BOM tổng hợp giải pháp xưởng dịch vụ 3S Hyundai Bắc Ninh" — INSERT SQL (nhân bản đầu phiếu BOM 27, không chép dòng hàng), status Hoàn thành, gắn solution_version 955 — vì hồ sơ trình duyệt bắt buộc có BOM tổng hợp Hoàn thành.
- Sau khi Trưởng phòng Từ chối hồ sơ 19 (giao diện), BOM 28 bị chuyển trạng thái → SQL đặt lại status=2 (Hoàn thành) để PM trình lại (thay cho bước sửa BOM).
- SQL solutions 955 department_id → 55 (PHÒNG DỰ ÁN) — giả lập Trưởng phòng GP thuộc phòng Dự án (tài khoản admin thuộc phòng khác nên danh sách 'PM mới' rỗng).
- issues id 2 `ISS-202610-0002` (trạng thái Mới, để có nút Xoá) — API PM 970. Version mới V2 (solution_versions 957) tạo qua giao diện bằng PM 970; GP 955 về Đang triển khai.
