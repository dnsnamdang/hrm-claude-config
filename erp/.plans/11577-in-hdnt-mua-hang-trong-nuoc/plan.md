# Plan — #11577 HĐNT mua hàng trong nước theo hãng: thêm chức năng In (@junfoke)

Redmine: http://quanly.dnsmedia.vn/issues/11577 — màn `/admin/orders/rule_inland_buy_contracts`.

## Ngày 13/11/2026 (@junfoke)
- [x] 13/11/2026 — Lỗi #11577: hiện trạng nút "In hợp đồng" ở danh sách bị comment, màn chi tiết không có nút In.
  - Nút In ở danh sách (màn HĐNT + màn Chờ duyệt) và màn chi tiết; phụ lục không có (DM mẫu in chưa có loại mẫu phụ lục).
  - Popup In theo ảnh QA: Nhà cung cấp (NCC hoạt động, mặc định NCC của HĐ, không bắt buộc); Mẫu (*) loại "HĐNT mua hàng" ở DM mẫu in mới — có NCC thì chỉ mẫu gắn NCC đó, trống NCC thì chỉ mẫu không gắn NCC; thiếu mẫu báo đỏ dưới ô.
  - In theo mẫu đã chọn ở tab mới; đường in cũ (mẫu lưu trên HĐ) giữ nguyên. HĐ chưa có người duyệt trước bị lỗi 500, nay in được.
  - Bảng biến loại "HĐNT mua hàng" ở màn Mẫu in đang copy nhầm từ HĐ dịch vụ (`KHACH_HANG`, `DON_VI`…) trong khi mẫu thật dùng `NHA_CUNG_CAP`, `DIA_CHI_NCC` ⇒ điền cả 2 bộ biến bằng dữ liệu NCC. Bảng biến hiển thị ở màn Mẫu in chưa sửa.
- [x] 13/11/2026 — Kiểm ERP local (xem ảnh): popup ở danh sách + chi tiết đúng; NCC 11851 lọc ra mẫu 103; in HĐ `HDNTDHTN-00051` với mẫu 103 không còn biến `{{…}}`; HĐ đang tạo in được.
- [x] 13/11/2026 — Commit `cae17d9c57` trên `task_11577` (tách từ `gop_db`) → merge `develop_02` (`9b1c632b92`), push cả 2 nhánh. Bản merge chỉ `php -l`, chưa chạy lại trình duyệt.

### Checkpoint — 13/11/2026 15:18
Vừa hoàn thành: đã lên `origin/develop_02` để user check trên dev.
Đang làm dở: —
Bước tiếp theo: check trên dev (dev cần có mẫu "HĐNT mua hàng" gắn NCC, không thì ô Mẫu trống); đạt thì merge `gop_db` (hỏi user).
Blocked:
