# Redmine đào tạo-đánh giá 21/11/2026 — 5 vé mới + 3 vé phản hồi

Người làm: @nguyentrancu97 · Nhánh: hrm-api / hrm-client `develop` · Bản gốc vé: scratchpad phiên (rm/<id>/issue.txt + ảnh).

## Nhóm A — Phiếu yêu cầu hỏi giá (YCHG) `/sale/price-asking-requests`

| Vé | Mục |
|---|---|
| #12238 Tạo mới | 1. Ẩn ô Người tạo, đưa Ghi chú lên ngang hàng ô Công ty · 2. Thông báo "Bỏ N hàng không lập YCHG được" chỉ liệt kê mã hàng lỗi (không kèm lý do dài) · 3. Cố định (sticky) cột Mã hàng trong bảng hàng |
| #12239 Danh sách | 1. Đồng bộ icon Tùy chỉnh cột · 2. Cột Ngày tạo có giờ · 3. Thêm cột Ngày cập nhật, Người cập nhật · 4. Dòng con (NCC/hãng) không lùi dòng, thẳng hàng Số phiếu · 5. Nút Ghi lịch sử ngoài danh sách |
| #12240 In | Ẩn dòng Trạng thái |
| #12241 Chi tiết | 1. Lịch sử đổi trạng thái gom vào nhóm "Thay đổi trạng thái" như màn khác · 2. Bỏ ô Người tạo · 3. Bỏ cột thừa (ô "Chờ … duyệt" ở cột Giá bán lẻ hiện hành) · 4. "Từ Báo giá…: BG-…" thành link sang báo giá |

## Nhóm B — Báo cáo (khuôn report-styles)

| Vé | Phản hồi còn lại |
|---|---|
| #12203 BC thưởng theo quý `/sale/bonus-quarter-report` | Tiêu đề và icon ⓘ lệch nhau · popup chi tiết (bấm số trong bảng) theo chuẩn `V2BaseReportModal` · số ở khối thống kê bấm được mở popup |
| #12201 BC thưởng NS tháng | Bug 8 tiêu đề/icon lệch · số ở khối thống kê bấm được mở popup |
| #12164 BC theo dõi thực hiện HĐ | Popup chi tiết khi bấm số ở khối thống kê theo chuẩn · tooltip ý nghĩa cột Thực thu trong kỳ, Giá trị HĐ |

## Nhóm C — #12243 BC chi tiết DSTC theo 1 HĐ, popup chọn hợp đồng

Ẩn nút Cài đặt bộ lọc + Ẩn tìm kiếm nâng cao, các ô tìm kiếm lên 1 dòng · thêm nút 🔒 ở Công ty/Phòng ban để xem bản ghi đã khoá.

## Tiến độ
- 21/11: chuyển 8 vé sang "Đang tiến hành", bắt đầu sửa.
- 21/11: sửa xong cả 3 nhóm, kiểm Playwright local (YCHG: danh sách/lịch sử/in/form + ghim cột Mã hàng; 3 BC: popup tổng khớp thẻ thống kê — quý K2/2026 27,235,295 · NS tháng 06/2026 2,349,277 · theo dõi HĐ Q2 thực thu 1,417,725,837; ⓘ thẳng tiêu đề; popup #12243 1 hàng + 🔒).
- 21/11: ĐÃ push develop (hash sau rebase): api `5b6f19bc2` (YCHG) `c2f34b301` (#12203 export flat) · client `435e4b2af` (YCHG) `b96a90a8a` (#12203) `49866fc09` (#12201) `fe2e8ebe8` (#12164) `691ec5450` (#12243) `ddf9cea1b` (gỡ vá ⓘ cục bộ).
- Icon ⓘ lệch: user duyệt sửa layout chung; Tri Lee đã sửa tận gốc ở client `3b79eb4f0` (bỏ lề 10px của h5 tiêu đề + bỏ `mt-2` icon) → mình bỏ phần sửa SidebarMenu, chỉ gỡ 2 bản vá cục bộ. Đo Playwright: tâm icon = tâm chữ tiêu đề.
- 21/11: 8 vé chuyển "Code xong chờ test" kèm hash. Chưa gop_db.
