# BC thưởng theo quý — UI (#12203 + #12205)

Màn `/sale/bonus-quarter-report` (client `pages/sale/bonus-quarter-report/`, api `Modules/Finance/.../BonusQuarter*`).
Chỉ làm đúng các mục trong 2 vé, KHÔNG thêm ngoài vé. Khuôn: `pages/sale/bonus-month-report` (#12201 vừa làm).

## Mục vé

| Vé | Mục | Cách làm |
|----|-----|----------|
| 12203 | Icon và chữ tiêu đề lệch nhau | Bỏ thẻ tiêu đề riêng (`tp-card` + `ri-medal-line` + h5), tiêu đề nằm trên panel lọc như các báo cáo mới |
| 12203 | Ghi rõ "Kỳ quyết toán" | Nhãn `Kỳ` → `Kỳ quyết toán` |
| 12203 | Ghi rõ "Số hợp đồng" | Nhãn `Số HĐ` → `Số hợp đồng` |
| 12203 | Thiếu bộ lọc Tháng | Thêm ô **Tháng** (Tháng 1…12), chỉ cho chọn khi đã có Năm (xem bên dưới) |
| 12203 | Công ty / Phòng ban / Bộ phận / Nhân viên lên hàng đầu | Ô `org` đặt đầu danh sách field |
| 12203 | In, Xuất Excel ngang hàng Cài đặt bộ lọc | Chuyển vào slot `#header-actions` của panel |
| 12205 | Tùy chỉnh cột | `columnCustomizationMixin` + `ColumnCustomizationModal` (khoá STT, Phòng ban/NV/HĐ) |
| 12205 | Làm lại theo UI phân cấp báo cáo mới | Khối thống kê `.rsum` + bảng cây `rsum-tb` (caret, ô chọn cấp ở tiêu đề cột) như #12201 |
| 12205 | Lệch số với ERP | ĐÃ xong ở api `ebb3eaaad` (cắt trang theo dòng HĐ như ERP) |

## Quyết định

- **Tháng** (ERP có ô Tháng nhưng gửi khoảng ngày rỗng nên không lọc được): HRM hiểu Năm + Tháng = khoảng ngày
  từ 01 đến ngày cuối tháng đó, tự điền 2 ô ngày và khoá lại, giống cách chọn Kỳ. Tháng và Kỳ chọn cái này thì xoá cái kia.
  Đổi/bỏ Năm thì xoá cả Tháng, Kỳ và 2 ô ngày như hiện tại. BE không đổi, vẫn nhận `start_date` và `end_date`.
- Thứ tự ô lọc: Công ty/Phòng ban/Bộ phận/Nhân viên · Năm · Tháng · Kỳ quyết toán · Thời gian · Số hợp đồng · Khách hàng.
- Ô chọn cấp (Chỉ phòng ban / Đến nhân viên / Đến hợp đồng, mặc định "Đến hợp đồng" như ô "Hiện chi tiết HĐ" cũ)
  thay cho checkbox "Hiện chi tiết HĐ". In và Xuất Excel theo cấp đang chọn: cấp 3 có thêm dòng HĐ (`expand`).
- Phân trang: vẫn theo DÒNG HĐ như ERP (#12205, ý đồ ERP). STT phòng ban (I, II…) đánh trong trang.
- Khối thống kê: QUY MÔ (phòng ban · nhân viên · dòng hợp đồng) + GIÁ TRỊ (6 cột tiền). Tính trên toàn bộ
  kết quả lọc; BE thêm `summary` = `total` + đếm. Ô chỉ hiển thị.
- Bấm tên NV hoặc số ở dòng NV mở popup chi tiết NV hiện có (`BonusQuarterDetailModal`). Số HĐ ở dòng HĐ là link tab mới.
- Xuất Excel: popup chọn trường (`ExportFieldsModal`, mặc định = cột đang hiện) + loading ngay khi bấm Đồng ý.

## Kiểm tra

- phpunit `Modules/Finance/Tests/Feature/BonusQuarter*`.
- Playwright 127.0.0.1:3000: thứ tự lọc, nhãn, Tháng điền/khoá ngày, nút trên panel, Tùy chỉnh cột, đổi cấp, In, Excel.
