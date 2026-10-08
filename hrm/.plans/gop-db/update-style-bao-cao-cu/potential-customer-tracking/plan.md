# Báo cáo tổng hợp CSKH tiềm năng — theo kịp các quyết định khuôn sau 04/10 (07/10/2026)

Màn: `/assign/report/potential-customer-tracking` · nhánh `gop_db` · đây là MẪU CHUẨN của skill `report-styles` (chốt 04/10) —
việc là đưa nó theo các quyết định mới ở báo cáo thị trường – KH (đợt 1-10) và Kết quả TKT (đợt 1-5b).

## Hiện trạng đã khớp
Ô Công ty + can_change_company · ẩn chỉ tiêu 0 · ⓘ tiêu đề khối · bảng (th 1 dòng, ô chọn cấp xs, STT La Mã, TỔNG màu khuôn, phân
trang BE cấp 0, "Không thuộc bộ phận") · reportSeq/optionsSeq/drillSeq, reportParams, keepSelectedOptions · Excel link `?token=`,
tiền số thật · không đọc DB ERP cũ · tiến trình "6. Lập dự toán" (07/10).

## Chỗ lệch (rà 07/10)
| # | Chỗ lệch | Loại |
|---|---|---|
| 1 | In: `PrintOptionsModal` riêng (chưa `V2BaseReportPrintModal`), BE chưa `SUMMARY/DETAIL_COLUMNS` + `cols`, In danh sách popup in thẳng, tiêu đề in cố định, chưa dòng điều kiện / dòng "N · tổng giá trị", không gửi sort | Khuôn 4b |
| 2 | Bộ lọc: Khách hàng / Tiến trình / Lĩnh vực đang `col 6` (chưa đều col-md-3) | Hỏi (bố cục) |
| 3 | Khối tổng hợp: chưa ⓘ từng ô + dòng meta; tiền thiếu "VND"; chưa giá trị cạnh số lượng mỗi ô | Hỏi (giá trị mỗi ô, nội dung ⓘ) |
| 4 | Nhãn tiền chưa "(VND)" (bảng, in, Excel, popup) | Khuôn |
| 5 | Popup: FE lặp tải 500 dòng/lượt rồi lọc tại chỗ (CMD/TKT đã phân trang server); KPI/header không theo ô lọc/ô tìm; chưa header "N · Tổng giá trị … VND" | Khuôn |
| 6 | Nhãn "Sales phụ trách" (TKT dùng "Nhân viên chủ trì dự án") | Hỏi |
| 7 | Excel màn chính: STT "1.1" thành số (chưa `data-type="s"`); Excel popup chưa dòng TỔNG | Khuôn |

## Câu hỏi nghiệp vụ (hỏi lần lượt)
- [x] Q1 — bộ lọc chia đều col-md-3 (9 ô → 3 hàng, hàng cuối 1 ô).
- [x] Q2 — thêm giá trị CÙNG HÀNG số lượng ở mọi ô (nhu cầu = Giá trị nhu cầu, dự án = Ngân sách dự kiến); bỏ số tiền ở tiêu đề khối.
- [x] Q3 — giữ "Sales phụ trách".
- ⓘ nội dung user duyệt 07/10 (xem câu trả lời: dòng số liệu chung + từng ô + "Bấm vào số để mở danh sách").

## Tasks (user "Làm" 07/10/2026 — hrm-api + hrm-client gop_db, không migration/seeder/quyền/DB, chưa commit)
- [x] B1. `summary`: `value_soon`, `value_by_status` (Ngân sách dự kiến từng tiến trình).
- [x] B2. `popupRows()` dùng chung popup / In / Excel: `base` = ô số (danh mục ô lọc popup), `rows` = sau `p_type` / `p_sales_id`
      (0 = chưa có Sales) / `p_statuses` + `q` + `sort`/`dir` (ô trống cuối). `item-list` phân trang server + `meta.base_total`,
      `metrics`, `amount_total`, `filter_options`.
- [x] B3. PrintService: `SUMMARY_COLUMNS` (8) / `DETAIL_COLUMNS` (9, khoá = cột popup) + `cols`; `detailTitle()` theo ô số;
      `describeFilters()` (chỉ điều kiện đang lọc, gồm ô lọc popup + Tìm); `countLine()`. Blade tổng hợp dựng mỗi dòng = map ô theo
      khoá cột (lặp `$columns`); blade danh sách cột động. Blade nhận thiếu biến -> mặc định đủ cột (lời gọi cũ / unit test).
- [x] B4. Excel màn chính: STT `data-type="s"`, nhãn (VND). Excel popup: tiêu đề / điều kiện / dòng tổng như bản in, dòng TỔNG.
- [x] F1. index.vue: 9 ô lọc col-md-3; `V2BaseReportPrintModal` (`printModes` summary 8 cột / detail 9 cột, `drillPrint`), XOÁ
      `components/PrintOptionsModal.vue`; popup nhận `params` (phạm vi), bỏ vòng tải 500 dòng/lượt.
- [x] F2. TrackingSummary: "· x VND" cùng hàng mỗi ô (làm tròn), ⓘ 10/10 ô + dòng số liệu chung, bỏ số tiền ở tiêu đề khối, ô
      `min-width: max-content`.
- [x] F3. TrackingTable: "Giá trị nhu cầu (VND)" / "Ngân sách dự kiến (VND)", 2 cột 130 -> 185px, bảng min-width 1764px.
- [x] F4. ItemListModal tự tải trang (`seq` chống response cũ), ô lọc từ `filter_options`, ô tìm debounce 300ms, sắp ở BE, header
      "N nhu cầu · M dự án TKT · Tổng giá trị dự kiến … VND", "x / y dòng", In danh sách emit `columns`.
- [x] T. PHPUnit `PopupPrintStyleTest` 3 ca (RED 3/3 code cũ, GREEN 3/3) + Feature PCT 21/21 (sửa 2 assert nhãn VND) + Unit
      PartBudget 5/5. E2E: ca 1 (col-md-3), ca 2 (đọc số lượng phần tử đầu), ca 7 mới — biên dịch được, CHƯA chạy.

### Checkpoint — 2026-10-07
Vừa hoàn thành: B1-B4, F1-F4, T. ĐÃ COMMIT + PUSH gop_db (api `1ba6647bc`, client `de0d12263`, rebase trên 1 + 2 commit mới của remote, không đụng file báo cáo).
Đo MCP: bộ lọc 9 ô đều 253/274/413px (1280/1366/1920); khối tổng hợp 10/10 ô có ⓘ + "· x VND" cùng hàng, 0 ô cắt; khối Dự án
3 hàng ở 1280/1366 (2 hàng ở 1920) — khối tổng hợp cao 241px ở 1366 (trước ~131px); tiêu đề bảng 1 dòng 39px, 0 cắt. Popup "Dự án
đang triển khai": 20/281 dòng, header "281 dự án TKT · Tổng giá trị dự kiến 4,625,445,868,876 VND"; lọc "6. Lập dự toán" -> 47 /
281, 140,510,499,991 VND; ô tìm "công ty" (Nhu cầu) 43 / 152; In danh sách: chọn cột (không radio) = 9 cột popup, bỏ Nguồn -> bản
in 8 cột + tiêu đề / điều kiện / dòng tổng, popup vẫn mở; Excel popup tải được; In báo cáo bỏ 2 cột -> `cols` 6 khoá, bản in đúng.
Bước tiếp theo: chạy e2e potential-customer-tracking{,.api} khi user yêu cầu · deploy BE + FE (không migration).
Còn mở: skill report-styles mục 4 + template/ vẫn ghi "FE lặp đủ trang" cho popup — cập nhật khi user đồng ý sửa skill.
