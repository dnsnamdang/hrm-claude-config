# Nhiệm vụ: soạn nội dung bổ sung mục IMPORT trong SRS danh mục (feedback tester 07/10/2026)

Thư mục: `/Users/manhcuong/Desktop/dns/HRM/.plans/gop-db/srs-tc-feedback-0710/`
- `srs_list.json`: danh sách SRS (id Drive, tên màn). File SRS hiện tại trên Drive: `drive/<id>.docx` (chỉ ĐỌC để hiểu mục
  Import đang viết gì — đọc bằng python-docx). Một số file có thể chưa tải xong → đọc code là đủ.
- Code căn cứ (CHỈ ĐỌC): FE `/private/tmp/claude-501/-Users-manhcuong-Desktop-dns-HRM/d4eb21da-a9be-45c4-92d7-751f1e0faae1/scratchpad/dev-client`,
  BE `/private/tmp/claude-501/-Users-manhcuong-Desktop-dns-HRM/d4eb21da-a9be-45c4-92d7-751f1e0faae1/scratchpad/dev-api` (nhánh develop mới nhất),
  lang BE `resources/lang/vi/validation.php`, FE `locales/vi.json`.

## Feedback tester cần đáp ứng (chỉ phần Import)
- Ý 2: "Với chức năng import, cần bổ sung các cột trong file import, mô tả đầy đủ các cột" — áp TẤT CẢ danh mục.
- Ý 5: "Import file: Dòng sự kiện chính thêm ghi lịch sử tạo mới".
- (Ý 1 — luồng giữ cửa sổ Import tô đỏ dòng lỗi — mình tự viết chung, KHÔNG cần soạn, nhưng ghi `gaps` nếu màn đó code chưa có:
  màn có luồng này = FE dùng `utils/mixins/CatalogImportMixin.js` VÀ controller BE `import()` trả kết quả validate khi có dòng
  không còn hợp lệ (comment "Redmine #11588").)

## Cần làm cho TỪNG SRS được giao
1. Tìm đúng màn trong code (theo menu/tên màn), đọc: cột import FE (`importColumns` / cấu hình cột của `V2BaseImportModal`,
   hàm `mapImportRow`, hàm tải file mẫu `buildImportTemplate` — tên file mẫu), BE `validateImportData()` / `import()` /
   request rules của import (bắt buộc, độ dài, trùng, phải tồn tại trong danh mục nào, phải đang Hoạt động không, giá trị
   hợp lệ của cột chọn, giá trị mặc định khi bỏ trống, tự viết hoa mã…), và câu báo lỗi thật.
2. Kiểm import có GHI LỊCH SỬ Tạo mới cho từng bản ghi không (service import có gọi ghi history / dùng cùng hàm store với
   Thêm mới không) → `history_on_import`: true/false + căn cứ file:dòng. Nếu true thì viết câu `history_sentence` mô tả
   giống cách SRS đó tả lịch sử ở mục Thêm mới (vd "Hệ thống ghi lịch sử Tạo mới cho từng bản ghi được import: người
   thực hiện là người đang import, thời điểm import."). Nếu false → vẫn viết câu theo yêu cầu tester nhưng ghi `gaps`.
3. Liệt kê ĐẦY ĐỦ các cột của file mẫu theo đúng thứ tự trong file (gồm cả cột STT nếu file có), mỗi cột:
   `name` (đúng chữ tiêu đề cột trong file mẫu, bỏ dấu *), `required` ("Có"/"Không"/"Có điều kiện"), `desc` = mô tả đầy đủ:
   ý nghĩa, định dạng/kiểu, độ dài tối đa, ràng buộc trùng (phạm vi trùng), phải chọn từ danh mục nào (và có phải đang Hoạt
   động), giá trị hợp lệ của cột chọn, bỏ trống thì hệ thống lấy gì, câu lỗi tiêu biểu khi sai. Văn phong nghiệp vụ, 1–3 câu.
4. Đọc mục Import hiện có trong SRS (`drive/<id>.docx`) để: biết tiêu đề mục Import (`import_heading`), và chỉ ra câu nào
   trong mục đó đang SAI so với code (vd "file mẫu không có cột Trạng thái" trong khi develop đã thêm) → `wrong_sentences`
   (trích nguyên văn + đề xuất sửa). Không tự sửa file.

## Quy tắc viết
- Ngôn ngữ nghiệp vụ; CẤM thuật ngữ code (bảng/cột DB, hàm, API, HTTP, mã 422, BE/FE, localStorage, mixin) và CẤM URL/đường dẫn.
- Chép đúng chữ hiển thị (tiêu đề cột, câu lỗi). Số theo chuẩn `1,234`.
- Không chắc → `questions`, không bịa.

## Đầu ra: `specs/<id>.json` (UTF-8, ensure_ascii=False) cho mỗi SRS
```json
{"id":"...","name":"<tên màn>","has_import":true,"import_heading":"2.8 Import file tỉnh/TP",
 "template_file":"Mau_import_tinh_tp.xlsx",
 "columns":[{"name":"STT","required":"Không","desc":"..."},{"name":"Tên Tỉnh/TP","required":"Có","desc":"..."}],
 "history_on_import":true,"history_sentence":"...",
 "has_rejected_flow":true,
 "wrong_sentences":[{"old":"...","new":"..."}],
 "gaps":["..."],"questions":["..."],"code_refs":["file:dòng"]}
```
Màn không có Import → `has_import:false` và lý do trong `gaps`. Cuối cùng trả lời NGẮN: mỗi SRS số cột, history_on_import,
has_rejected_flow, gaps, questions.
