# Checklist sửa SRS/HDSD theo form "Danh mục quốc gia" (TPE Pass)

Nguồn: 2 file mẫu trong `mau/` + toàn bộ góp ý TPE trên SRS/HDSD quốc gia (đọc ngày 28/10/2026).
Áp cho 16 màn "DNS đang fix" ở sheet theo dõi (tab ERP->HRM).

## SRS

**Khung**
- Phần 1 Giới thiệu (Mục đích, Thuật ngữ) · Phần 2 Phân quyền (Danh sách quyền, Ma trận) ·
  Phần 3 (Sơ đồ UML tổng quan + đặc tả 2.x) · Phần 4 Quy tắc nghiệp vụ · **Phần 5 Bảng màn hình tham chiếu dữ liệu**.
- Sơ đồ UML tổng quan: KHÔNG ghi "Hệ thống HRM - ...", tên hệ thống ghi chung.
- Use Case riêng chỉ cho chức năng thao tác. Không vẽ cho Xem DS / Tìm-lọc / Lịch sử / Tùy chỉnh cột / Cài đặt bộ lọc.
  Kiểm tra trùng tên/mã là business rule, KHÔNG phải UC. Xem chi tiết CÓ sơ đồ.

**Mỗi chức năng 2.x**
- Dòng đầu: "Quy tắc chung: Áp dụng SRS Các quy tắc chung [link] - <mục>. Chỉ bổ sung quy tắc riêng của <màn>".
  Mục nào đã có trong quy tắc chung (khóa, xóa, lịch sử, phân trang, bộ lọc mặc định) thì gắn link, KHÔNG viết lại.
- Bảng Mục | Nội dung: Tác nhân = "Người dùng có quyền thực hiện chức năng" (ghi quyền), không ghi "Người dùng đã đăng nhập".
  Điều kiện ban đầu: 1. đăng nhập thành công 2. có quyền (+ trạng thái bản ghi).
  Dòng sự kiện chính có bước "Ghi nhận ... trong lịch sử" khi tạo/sửa/đổi trạng thái/import.
- Popup nhập liệu: sự kiện phụ "Bấm Đóng / (x) / click ra ngoài: chưa đổi gì thì đóng; đã nhập thì hỏi xác nhận".
- Layout: "Đường dẫn màn hình: Menu: Phân hệ X => ... (=> thao tác)", không URL. Popup thêm câu
  "Modal ... được mở ngay trên màn hình <danh sách/chi tiết/tạo mới> theo đường dẫn ở trên." (ghi ĐÚNG màn mở popup).
  Ảnh chụp đủ trường (kể cả Người/Ngày cập nhật, bộ lọc), hộp xác nhận chụp có nội dung.
- Mô tả giao diện: đủ nút Tìm / Làm mới / Tùy chỉnh cột; ghi cột nào sắp xếp được; cột Trạng thái trên lưới là
  Table/Grid (không phải Dropdown). Phạm vi ghi rõ "1–255 ký tự", ký tự cho phép.
  Loại phải đúng bản chất đối tượng (TPE bắt "Sai loại"): cột trên lưới = Table/Grid, ô nhập = Textbox, ô chọn ngày =
  Datepicker, ô nhiều dòng = Textarea. Bỏ các loại không phải đối tượng: "Number" (cột số → Table/Grid, ô số → Textbox),
  "Loading", "Modal" (dòng trong popup → đúng loại của dòng), "Text" → Label.
  Màn đơn giản không cần mô tả lại bộ lọc mặc định; màn có bộ lọc riêng thì mô tả.
- Event: Before / During / After. During có câu "Nếu có lỗi kiểm tra → gửi thông báo lỗi theo quy tắc thông báo
  chung [link], không thực hiện bước After". Loại event: Click / Change / System / Drag (không Keypress, Blur).
- Import: bảng cột file mẫu; đính kèm link file mẫu; ghi rõ Tổng/Hợp lệ/Lỗi hiện gì khi nào; Import chỉ chạy khi
  KHÔNG còn dòng lỗi; nút Làm mới và Đóng tách 2 dòng.
- Xuất Excel: chọn trường + thứ tự; kết quả rỗng vẫn xuất (logo + tên cột); giới hạn dòng.
- Lịch sử: Tạo/Import cũng ghi lịch sử (không có câu "chưa từng sửa → chưa có lịch sử").

**Phần 4**: câu dẫn "chỉ ghi quy tắc đặc thù, không lặp quy tắc chung"; bảng STT | Mã quy tắc | Tên | Mô tả | Phạm vi áp dụng.
Mã BR-01, BR-02... liên tục.

## HDSD

- Bìa Tân Phát "(Màn hình: X)" · MỤC LỤC (không DANH MỤC HÌNH ẢNH).
- TỔNG QUAN: 1. Thuật ngữ sử dụng trong tài liệu · 2. Cập nhật tài liệu (Phiên bản | Ngày | Người cập nhật | Nội dung) ·
  3. Quyền sử dụng (ngắn) · 4. Sơ đồ chức năng tổng quan (Hình 1).
- PHẦN 1: TRUY CẬP VÀ TÌM KIẾM; sau đó mỗi thao tác 1 PHẦN.
- Nội dung: "Bước n: ..." ngắn + icon nút inline + ảnh "Hình n: ..."; "Hoặc ..." cho lựa chọn phụ; "Cách 1/Cách 2".
- Không URL, không văn xuôi giải thích, không bảng mô tả trường, không phần "theo vai trò"/"lỗi thường gặp"/"lưu ý".
- Góp ý TPE trên HDSD mẫu: Thêm mới phải nói rõ trường bắt buộc / tùy chọn và định dạng; Import có bảng cột, dữ liệu mẫu,
  quy tắc trùng, cách xác nhận nhập thành công.
