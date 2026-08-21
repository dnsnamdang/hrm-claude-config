# Plan — Làm đẹp file Excel "Danh mục công việc / lỗi thiết bị"

Phụ trách: @khoipv
Màn: `customer-care/device-errors` → nút **Xuất Excel**
File BE: `hrm-api/Modules/CustomerCare/Exports/DeviceErrorExport.php`

## Phase 1 — Format file xuất

- [x] BE: thêm block tiêu đề (tên báo cáo + ngày xuất + tổng số bản ghi) phía trên bảng
- [x] BE: style dòng header (nền đậm, chữ trắng, in đậm, canh giữa, wrap, chiều cao dòng)
- [x] BE: set độ rộng từng cột theo nội dung (tên công việc / ghi chú rộng hẳn ra)
- [x] BE: bật wrap text cho cột dữ liệu dài (Tên công việc, Loại, Ghi chú)
- [x] BE: kẻ khung toàn bảng + zebra (nền xen kẽ) cho dễ dò dòng
- [x] BE: number format cột số (Định mức, Giá, Chiết khấu, Hệ số LN, VAT) + canh phải
- [x] BE fix: bỏ `#,##0.##` ở 4 cột số lẻ → `General` (Excel in thừa dấu `.` ở cuối số tròn: `1.`, `8.`)
- [x] BE: `WithStrictNullComparison` — giá trị 0 không còn bị ghi thành ô trống
- [x] BE: tô màu cột Trạng thái (Hoạt động xanh / Khóa đỏ)
- [x] BE: freeze pane + auto filter tại dòng header
- [x] BE: page setup in (ngang, A4, fit width, lặp header mỗi trang)
- [x] BE: chống formula injection cho cột text (=, +, -, @)
- [x] BE: nhánh danh sách rỗng — hiện "Không có dữ liệu", không kẻ khung dòng ma
- [x] Verify: `php -l` PASS + sinh file thật (5 dòng mẫu & 0 dòng) rồi đọc lại bằng PhpSpreadsheet

### Checkpoint — 2026-08-11
Vừa hoàn thành: viết lại `DeviceErrorExport` (BE) cho file xuất Excel của màn
`customer-care/device-errors`.

Thay đổi: export cũ chỉ có `FromCollection + WithHeadings + WithMapping` → file trần, 1 dòng
header không style, cột co theo mặc định nên tên công việc/ghi chú bị cắt. Nay thêm
`WithCustomStartCell` (bảng bắt đầu A4), `WithColumnWidths`, `WithEvents` (AfterSheet dựng style),
`WithTitle`, `WithStrictNullComparison`.

Layout mới: R1 tiêu đề merge A1:J1 → R2 ngày xuất + tổng số bản ghi → R3 dòng thở →
R4 header (nền `1F4E79`, chữ trắng, wrap, cao 32) → R5+ dữ liệu (khung mảnh `B7C3D0`,
zebra `F2F6FA`, wrap + chiều cao tự động, cột số canh phải có format nghìn, cột Trạng thái
xanh/đỏ), freeze A5 + auto filter A4:J{n}, in ngang A4 fit width lặp header.

⚠️ Lưu ý: danh mục này KHÔNG có route import nên thêm 3 dòng tiêu đề không phá luồng nào.
Nếu sau này làm import thì phải bỏ qua 4 dòng đầu (hoặc dùng file mẫu riêng).

Verify: lint PASS; sinh file thật bằng script scratchpad (5 dòng mẫu, có case chuỗi bắt đầu
bằng `=` và giá trị 0) rồi load lại bằng PhpSpreadsheet — merge/freeze/autofilter/width/format/
kiểu ô đều đúng; ô `=cmd|calc` lưu dạng TEXT (type `s`), không thành công thức.

Đang làm dở: không có.
Bước tiếp theo: user bấm **Xuất Excel** trên màn `customer-care/device-errors` với dữ liệu thật
để xác nhận độ rộng cột đã đủ.
Blocked: không có.
