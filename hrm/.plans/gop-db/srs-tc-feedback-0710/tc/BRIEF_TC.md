# Nhiệm vụ: soạn testcase BỔ SUNG + sửa 2 loại dòng cũ theo feedback tester 07/10/2026

Thư mục làm việc: `/Users/manhcuong/Desktop/dns/HRM/.plans/gop-db/srs-tc-feedback-0710/tc/`
Dump từng tab: `dumps_cd/NN.txt` (workbook "Testcase chuyển đổi") và `dumps_qlda/NN.txt` (workbook "Testcase _Quản lý dự án").
`NN` = vị trí tab trong workbook. Dòng `R<số>:` = số hàng THẬT trên sheet. `C=` `D=`… là cột. Cột: A Module · B Nhóm chức năng ·
C TC ID · D Chức năng · E Priority · F Tiền điều kiện · G Bước thực hiện · H Test Data · I Expected Result · J KQ thực tế ·
K/L/M DNS check lần 1/2/3 · N Ghi chú. (Kiểm lại hàng header của từng tab — tab QLDA header ở R6 hoặc R16, nhãn cột có thể khác.)
Hàng tiêu đề nhóm: tab chuyển đổi dạng `C=I. HIỂN THỊ TRANG & TRUY CẬP`; tab QLDA dạng `C=KBKT_ Xem danh sách` hoặc `C=II. BỘ LỌC…`.
Tab QLDA có TC ID là CÔNG THỨC (vd `="TC-ROLE-"&ROW()-ROW($A$7)`) — case mới chèn vào khối đó thì cột id ghi đúng công thức
của dòng ngay trên (công thức tự tính theo hàng); khối dùng mã chữ (`TC_04.016`) thì đánh số tiếp.

## Code căn cứ (CHỈ ĐỌC, không sửa gì)
Nhánh develop mới nhất: FE `/private/tmp/claude-501/-Users-manhcuong-Desktop-dns-HRM/d4eb21da-a9be-45c4-92d7-751f1e0faae1/scratchpad/dev-client`
(pages/, components/, utils/), BE `/private/tmp/claude-501/-Users-manhcuong-Desktop-dns-HRM/d4eb21da-a9be-45c4-92d7-751f1e0faae1/scratchpad/dev-api` (Modules/, app/,
`resources/lang/vi/validation.php`). FE locale `locales/vi.json`. Mọi chữ nút, câu thông báo, giới hạn độ dài, số dòng/trang,
thứ tự sắp xếp mặc định, điều kiện hiện nút… PHẢI lấy từ code. Không chắc → ghi `questions`, KHÔNG bịa.
Hành vi dùng chung đã biết (vẫn phải kiểm màn cụ thể có truyền prop khác không):
- Phân trang `components/V2BasePagination.vue` / `V2BaseDataTable.vue`: mặc định 10 dòng/trang, lựa chọn 5/10/20/50/100, dòng
  tổng "Hiển thị {từ}–{đến} / {tổng} bản ghi" (kiểm `itemLabel` màn truyền vào và tổng có định dạng nghìn hay không).
  Thứ tự mặc định: đọc BE service index (orderBy) của màn.
- Nhớ bộ lọc: `utils/mixins/filterStateMixin.js` — lưu trên trình duyệt, hết hạn 10 phút (`expirationTime`), CHỈ lưu khi rời
  màn để vào trang con khớp `pathsToKeep` (vd trang chi tiết `/…/{id}`), rời sang màn khác thì XOÁ; khoá lưu theo màn chứ
  KHÔNG theo tài khoản; trình duyệt dùng chung giữa các tab. Đọc thêm `V2BaseSmartFilterPanel.vue` / `V2BaseFilterPanel.vue`
  xem có cơ chế nhớ riêng (vd nhớ trạng thái mở "Tìm kiếm nâng cao", "Cài đặt bộ lọc" theo người dùng) không.
- Import danh mục (Redmine #11588, develop): `utils/mixins/CatalogImportMixin.js` + `utils/import-error-helper.js`
  (`markRejectedImportRows`) + BE controller `import()` của màn: bấm Import mà có dòng không còn hợp lệ so với lúc Validate
  (vd mã/tên vừa được tạo ở tab/người khác) → KHÔNG import dòng nào, popup giữ nguyên, dòng lỗi tô đỏ kèm lý do, câu báo
  "Chưa import dòng nào: n dòng không còn hợp lệ — …". Các màn module Giao việc (pages/assign/*) KHÔNG dùng mixin này và
  BE chưa có chặn #11588 → vẫn viết case theo hành vi YÊU CẦU (giữ popup, tô đỏ dòng lỗi) nhưng ghi màn đó vào `code_gaps`.

## Feedback cần áp
A. THÊM case mới (KHÔNG sửa case cũ; ý nào tab đã có case tương đương → bỏ, ghi `skipped` kèm TC ID đã có):
 1. "Lưu và tiếp tục" khi có dữ liệu lỗi (bỏ trống bắt buộc / sai định dạng / trùng) → báo lỗi, không lưu, popup giữ dữ liệu.
    Chỉ màn có nút đó (đọc đúng chữ trên nút trong code). Không có → skipped.
 2. Ô chọn cha–con phụ thuộc nhau (form Tạo/Sửa và bộ lọc, vd Quốc gia → Khu vực → Tỉnh/TP): chưa chọn cha thì ô con
    ra sao (khoá / trống / hiện tất cả — theo code), chọn cha thì ô con chỉ còn con của cha đó; "ngược lại" = chọn con trước
    thì ô cha có tự điền không / đổi cha thì ô con đã chọn bị xoá không — viết đúng hành vi code. Màn không có cặp cha–con → skipped.
 5. Nhớ bộ lọc: giữ trong bao nhiêu phút (vào trang con rồi quay lại trước/sau 10 phút), rời sang màn khác rồi quay lại,
    đăng xuất đổi tài khoản khác trên cùng trình duyệt, mở màn trong tab trình duyệt mới. Expected theo code; hành vi nào
    trông như lỗi (vd bộ lọc của tài khoản A hiện cho tài khoản B) thì expected viết hành vi ĐÚNG mong đợi và ghi `questions`.
 6. Kết hợp tiêu chí lọc: từ khoá + 1 bộ lọc, 2 bộ lọc với nhau, cả 3 tiêu chí (lấy đúng các ô lọc của màn — tester lấy
    ví dụ màn Tỉnh/TP: từ khoá + Quốc gia, Quốc gia + Trạng thái, cả 3); kiểm tra giới hạn độ dài ô tìm kiếm (có maxlength
    không, dán chuỗi rất dài thì sao — theo code).
 7. Mở khoá bản ghi đã bị người khác XOÁ, và bản ghi đã bị người khác đổi trạng thái (đã Mở khoá trước) — 2 tab/2 người.
    Expected theo câu thông báo thật của BE/FE. Màn không có Khoá/Mở khoá → skipped.
 8. Import (#11588): đã Validate hợp lệ, tab khác tạo trước bản ghi trùng mã/tên với 1 dòng trong file, quay lại bấm Import
    → không dòng nào được ghi, popup giữ nguyên, dòng đó tô đỏ kèm lý do trùng, câu báo; sửa/bỏ dòng lỗi rồi Import lại
    thành công. Thêm 1 case: toàn bộ dòng hợp lệ → import thành công, đóng popup, danh sách nạp lại. Màn không có Import → skipped.
B. SỬA dòng cũ (được user cho phép, CHỈ 2 loại này):
 3. Case "Mở màn hình từ menu" (hoặc tương đương đầu nhóm hiển thị): viết lại cột I (Expected) cho rõ: mặc định bao nhiêu
    bản ghi 1 trang, sắp xếp bản ghi tạo mới nhất → cũ nhất (đúng theo code), dòng tổng số bản ghi hiển thị theo định dạng
    nào (chép đúng khuôn chữ), được chọn bao nhiêu bản ghi 1 trang. GIỮ nguyên các ý Expected cũ còn đúng, chỉ bổ sung/viết rõ.
    Tab chưa có case nào như vậy → thêm case mới (mục A).
 4. Case tìm kiếm/lọc mà ô lọc đó chỉ hiện sau khi bấm "Tìm kiếm nâng cao" (kiểm code: ô nào nằm ở thanh gọn, ô nào ở
    khối nâng cao): viết lại cột G (Bước) chèn bước "Bấm Tìm kiếm nâng cao" vào đúng chỗ, đánh số lại các bước.
    Ô lọc hiện sẵn không cần bấm → không sửa.

## Quy tắc viết
- Văn phong y hệt case đang có trong tab (đọc vài case cùng nhóm): ngôn ngữ nghiệp vụ, KHÔNG thuật ngữ code (bảng/cột/hàm,
  API, HTTP, mã 422/403/423, localStorage, BE/FE, mixin, prop…), KHÔNG URL/đường dẫn tương đối — chỉ đường bấm menu + tên nút.
  Bước đánh số `1. …\n2. …`. Expected chi tiết, kiểm chứng được, chép đúng chữ thông báo. Dùng `\n` xuống dòng trong ô.
- Case mới đặt vào CUỐI đúng nhóm đang có (6 → nhóm Tìm kiếm/Lọc; 5 → nhóm Tìm kiếm/Lọc hoặc Hiển thị; 2,1 → Thêm mới/Sửa;
  7 → Khoá/Mở khoá; 8 → Import). Chưa có nhóm phù hợp → nhóm mới đặt sau nhóm case cuối cùng của tab (trước ghi chú tester).
- TC ID: tiếp nối số lớn nhất trong nhóm (TC_04.016 → TC_04.017…). Nhóm mới: số nhóm = max + 1, `.001`. Khối id công thức → công thức.
- Priority theo thang tab đang dùng. KHÔNG điền cột J/K/L/M.
- Cột A/B của case mới: ghi đúng giá trị Module / Nhóm chức năng của nhóm đó (dùng khi nhóm không gộp ô).

## Đầu ra: `plans_<cd|qlda>/NN.json` cho MỖI tab được giao (UTF-8, ensure_ascii=False)
```json
{
  "book": "cd|qlda", "nn": "16", "tab": "<tên tab đúng như dòng TAB:>",
  "module": "<cột A>",
  "edits": [
    {"row": 19, "col": "I", "old_prefix": "<40 ký tự đầu nội dung HIỆN TẠI của ô>", "new": "<toàn văn mới>", "feedback": 3}
  ],
  "inserts": [
    {"group_title": "<cột C hàng tiêu đề nhóm>", "group_name": "<cột B dòng đầu nhóm>", "new_group": false,
     "after_row": <hàng của case CUỐI CÙNG trong nhóm (new_group: hàng case cuối cùng của tab)>,
     "cases": [{"id":"TC_02.015","func":"...","priority":"P1","pre":"...","steps":"1. ...\n2. ...","data":"...","expected":"...","feedback":6}]}
  ],
  "skipped": [{"feedback": 1, "reason": "..."}],
  "questions": ["..."],
  "code_gaps": ["<hành vi tester yêu cầu mà code chưa có>"],
  "code_refs": ["file:dòng căn cứ chính"]
}
```
`inserts` sắp theo `after_row` TĂNG dần; `edits` chỉ cột G hoặc I. Tự kiểm trước khi xong: JSON parse được; không có chữ cấm
(`BE`, `FE`, `API`, `HTTP`, `422`, `403`, `423`, `localStorage`, `/api`, `http`, `mixin`); mọi `after_row` đúng là hàng có TC ID
trong dump (và là case cuối nhóm); `old_prefix` khớp đúng dump.
Trả lời cuối cùng NGẮN GỌN: mỗi tab — số case thêm (theo ý), số dòng sửa, skipped, questions, code_gaps.
