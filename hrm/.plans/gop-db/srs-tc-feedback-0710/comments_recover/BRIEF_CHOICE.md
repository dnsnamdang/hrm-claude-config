# Chọn đúng vị trí gốc cho nhận xét bị mất (SRS danh mục)

Thư mục: /Users/manhcuong/Desktop/dns/HRM/.plans/gop-db/srs-tc-feedback-0710/comments_recover/
Đầu vào: `need_choice.json` — mỗi phần tử là 1 nhận xét người duyệt đã viết trên SRS:
- `anchor`: đoạn chữ người duyệt bôi đen khi nhận xét (lấy từ email, có thể chỉ là vài chữ).
- `thread`: nội dung nhận xét + các trả lời.
- `candidates`: các chỗ đoạn `anchor` xuất hiện trong BẢN CŨ của tài liệu (lúc người duyệt nhận xét): mục (heading),
  dòng bảng (row = 2 ô đầu), đoạn văn (para), toàn ô (cell).

Nhiệm vụ: với mỗi nhận xét, đọc kỹ NỘI DUNG nhận xét để suy ra người duyệt đang nói về chỗ nào, rồi chọn đúng 1 candidate
(`old_i`). Ví dụ nhận xét "Hiển thị theo định dạng tên nhân viên - mã phòng" với anchor "Người" → chọn candidate ở dòng
"Người tạo"/"Người cập nhật" trong bảng mô tả giao diện, không chọn chỗ "Người dùng…" ở phần phân quyền. Nhận xét "ghi rõ tên
quyền" với anchor "Quản lý" → chọn chỗ nói về quyền. Các nhận xét cùng người viết liên tiếp vài phút thường nằm gần nhau
trong tài liệu (đọc theo thứ tự thời gian) — dùng làm gợi ý phụ.

Nhận xét KHÔNG có candidate (11 cái): mở `cur_units/<id>.json` (bản HIỆN TẠI: u = số thứ tự đoạn, heading, row, text) — id
lấy từ `ids.json` theo tên file — và chọn trực tiếp đoạn hiện tại phù hợp nhất (`cur_u`), dựa vào anchor + nội dung nhận xét.

Đầu ra: ghi `choices.json` = danh sách `{"n": <n>, "old_i": <số hoặc null>, "cur_u": <số hoặc null>, "confidence": "cao|vừa|thấp", "why": "<1 câu>"}`
cho ĐỦ mọi phần tử của need_choice.json. Không sửa file nào khác, không dùng trình duyệt, không gọi mạng.
Trả lời cuối: số cao/vừa/thấp và liệt kê các nhận xét độ tin cậy thấp (n + lý do ngắn).
