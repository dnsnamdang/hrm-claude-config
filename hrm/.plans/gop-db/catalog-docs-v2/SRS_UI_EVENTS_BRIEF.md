# Brief bổ sung "Mô tả chi tiết giao diện" + "Danh sách event và xử lý event" cho SRS (28/09/2026)

Tester báo: SRS các danh mục (trừ Quốc gia) thiếu 2 mục con này ở các chức năng Xem chi tiết / In, Xem lịch sử thay đổi, Import, Xuất Excel, Tùy chỉnh cột. Rà config thấy thiếu ở MỌI FR sau "Thêm mới" (cả Chỉnh sửa, Xóa, Khóa/Mở khóa…).

## Việc
Với mỗi slug được giao, sửa `configs/<slug>.py`: MỌI phần tử trong `CFG['srs']['fr']` phải có đủ `ui` (bảng, hàng đầu là tiêu đề cột) + `events` (list `[Event, Loại event, Xử lý event]`, builder tự thêm cột STT). FR đã có thì rà lại cho đúng code, không viết lại vô cớ. KHÔNG đụng key khác (tc, hdsd, capture…) trừ khi phát hiện sai rõ ràng liên quan.

## Khuôn — bám SRS Danh mục quốc gia
Bản trích text: `/private/tmp/claude-501/-Users-manhcuong-Desktop-dns-HRM/97975d78-0044-4d8d-903b-30099dcfa96c/scratchpad/qg_srs.txt` (dòng 137–356: Chỉnh sửa, Xóa, Khóa, Lịch sử, Import, Xuất). Tiêu đề cột bảng `ui` theo QG:
- Chỉnh sửa (form): `STT | Tên đối tượng | Loại | Trạng thái | Phạm vi | Bắt buộc | Giá trị ban đầu | Mô tả` (Giá trị ban đầu = "Dữ liệu hiện tại").
- Xóa, Khóa/Mở khóa: `STT | Tên đối tượng | Loại | Mô tả`.
- Lịch sử: `STT | Tên đối tượng | Loại | Giá trị ban đầu | Mô tả`.
- Import: `STT | Tên đối tượng | Loại | Trạng thái | Bắt buộc | Giá trị ban đầu | Mô tả`.
- Xuất Excel: `STT | Tên đối tượng | Loại | Trạng thái | Giá trị ban đầu | Mô tả`.
- Xem chi tiết (QG bỏ trống — mình PHẢI viết): `STT | Tên đối tượng | Loại | Trạng thái | Giá trị ban đầu | Mô tả` — liệt kê cách mở (bấm mã/tên ở cột…), tiêu đề cửa sổ/màn, từng trường hiển thị chỉ đọc (Read-only), khối lịch sử nhúng nếu có, các nút ở chân (Đóng / Sửa / In… đúng code, điều kiện hiện).
- Tùy chỉnh cột (QG bỏ trống — mình PHẢI viết): cùng cột như Xuất — nút mở (biểu tượng "Cấu hình cột hiển thị"), danh sách cột có checkbox, cột bị khoá không bỏ được (liệt kê đúng cột `locked` trong code), kéo thả đổi thứ tự nếu có, nút Mặc định/Áp dụng/Đóng… đúng code, lưu ở đâu (theo người dùng / trình duyệt).
- In (nếu màn có In): như Xuất.
Event: cột Xử lý event viết theo khung `Before:` / `During:` / `After:` với gạch `– ` (xuống dòng bằng `\n`), như QG.

## Quy tắc nội dung
- Đọc CODE THẬT (FE `/Users/manhcuong/Desktop/dns/HRM/worktrees/gop_db-client`, BE `/Users/manhcuong/Desktop/dns/HRM/worktrees/gop_db-api`), lấy nguyên văn chữ nút, tiêu đề, câu thông báo, tên file xuất, danh sách trường xuất, cột file mẫu import, câu lỗi validate import. Component dùng chung: `components/V2BaseImportModal*`, export field picker, column config (grep `Cấu hình cột hiển thị`), history modal (grep `Lịch sử thay đổi`).
- Code vừa đổi 28/09: xoá cứng khi chưa dùng (đã dùng → ẩn nút Xóa + BE 400), Khóa/Mở khóa, ô Trạng thái, bản ghi Khóa bị chặn 423 "Bản ghi đang bị khoá, vui lòng mở khoá trước khi cập nhật.". Nội dung phải khớp code hiện tại, và khớp phần HDSD/gioi_thieu đã có trong chính config (không mâu thuẫn).
- Không ghi URL/đường dẫn. Không ghi tên bảng DB — dùng tên nghiệp vụ. Số dạng `1,234.5`, ngày `dd/mm/yyyy`.
- Màn không có chức năng nào thì đừng bịa (không có FR thì thôi).

## Tự kiểm
```
cd /Users/manhcuong/Desktop/dns/HRM/.plans/gop-db/catalog-docs-v2
python3 -c "import sys; sys.path.insert(0,'../_catalog_docs_lib'); from catalog_v2 import load_cfg; c=load_cfg('<slug>'); print([f['ten'] for f in c['srs']['fr'] if not f.get('ui') or not f.get('events')])"   # phải in []
python3 -c "import sys; sys.path.insert(0,'../_catalog_docs_lib'); from catalog_v2 import build_srs; print(build_srs('<slug>'))"   # dựng thử, KHÔNG gọi finalize (finalize mở Word, nhiều agent chạy song song sẽ đụng nhau)
```
KHÔNG đẩy Drive, KHÔNG sửa Sheet, KHÔNG sửa code dự án, KHÔNG commit. Trả về: số FR đã bổ sung mỗi slug, chỗ code lệch tài liệu phát hiện được (ghi thêm vào `loi_code` nếu là lỗi code).
