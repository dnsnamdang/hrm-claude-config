# Script kiểm Agent (chạy trong `websites/wt-tpe-agent/hrm-api`, bootstrap Laravel — mysql CLI không dùng được)
- `php -d memory_limit=1G <đường dẫn>/eval_nhom.php 178,179,180` — eval API THẬT một nhóm câu (theo số thứ tự questions.json).
- `hoi_that.php` — sửa mảng `$qs = [[NV, 'câu'], …]`, hỏi thật mỗi câu 1 hội thoại, in công cụ + câu trả lời, tự xoá lượt.
- `hoi_chuoi.php` — nhiều câu trong CÙNG 1 hội thoại (kiểm lịch sử / câu nối tiếp), tự xoá.
- `hr_smoke.php <NV> <ToolClass> '<json>'` — gọi thẳng 1 công cụ.
- `desc.php Tool1 Tool2` — in độ dài mô tả (≤ 1000).
- `gp_parity.php <NV>` — đối chiếu thong_ke_giai_phap với 2 báo cáo; `ct_parity.php <từ> <tới> <phòng>` — CT bảng công vs thong_ke_cong_tac.
