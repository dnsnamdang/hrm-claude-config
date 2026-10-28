# Design — Meeting web: tab "Dự án TKT" chỉ xem + tab "Nhân sự tham gia"

Phụ trách: @dnsnamdang · Nhánh `gop_db` (hrm-api + hrm-client) · Spec đầy đủ:
`docs/superpowers/specs/gop-db/2026-10-14-meeting-tab-du-an-nhan-su-design.md`

## Mục tiêu
1. Tab "Dự án tiền khả thi" → **"Dự án TKT"**, chỉ hiện khi meeting đã chọn ≥ 1 dự án; bỏ tạo / xoá dự án trong tab;
   thông tin dự án chỉ xem; phiếu thu thập thông tin vẫn nhập + lưu.
2. Tab "Điểm danh" → **"Nhân sự tham gia"**: gộp Thành phần (đang ở cột phải tab Thông tin) + Điểm danh thành 1 bảng.

## Quyết định đã chốt (14/10/2026)
| # | Nội dung |
|---|---|
| Q1 | Lưu meeting chỉ lưu LIÊN KẾT meeting–dự án (không ghi đè trường dự án, không tạo dự án, bỏ rule trường dự án) |
| Q2 | Phiếu thu thập thông tin vẫn nhập + Lưu phiếu từ meeting |
| Q3 | Nhân sự tham gia: 1 bảng, nhóm theo phía (Công ty trước, Khách hàng sau), kéo thả trong từng nhóm |
| Q4 | Cột điểm danh ẩn khi chưa Chốt lịch |
| Q5 | Đổi tên tab → "Dự án TKT" |
| Q6 | Không đổi cách lưu `meeting_employees` → báo cáo không bị ảnh hưởng |

| U1 | 14/10 user "làm" theo đề xuất: sửa luôn lỗi bỏ dự án không xoá liên kết — sync đúng danh sách, chỉ xoá dòng liên kết, GIỮ câu trả lời phiếu |
| — | 14/10 user cho phép code toàn bộ 4 phase (hrm-api + hrm-client + e2e, nhánh gop_db, không migration, không commit) |
