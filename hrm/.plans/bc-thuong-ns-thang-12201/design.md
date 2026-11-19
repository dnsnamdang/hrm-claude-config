# #12201 — Báo cáo thưởng năng suất tháng: làm lại UI theo khuôn rsum

Màn: `/sale/bonus-month-report` (`hrm-client/pages/sale/bonus-month-report/`), API `finance/bonus-month-report`.
Mockup: `mockup.html` (cùng thư mục, dựng từ DOM + CSS thật của màn mẫu, số liệu minh hoạ).
Màn mẫu bám theo: `pages/customer-care/report/install-delivery-repair` (#12170) + skill `report-styles`.

## Yêu cầu vé (QA)
1. Ô Từ ngày – Đến ngày gộp thành 1 ô (như `/sale/customer-debt-by-employee`). Ảnh 16299: ô "Từ ngày" báo đỏ "Bắt buộc phải nhập".
2. Có Tùy chỉnh cột.
3. In + Xuất Excel nằm cùng hàng nút "Cài đặt bộ lọc".
4. Ẩn ô "Show chi tiết".
5. UI phân cấp như các báo cáo mới: khối thống kê, màu, bấm số mở chi tiết, tooltip công thức ở cột số.
6. Excel cho chọn trường.
7. Bấm Xuất Excel phải hiện loading ngay (hiện đơ ~3s).
8. Sửa lệch tiêu đề + icon (tiêu đề card "Báo cáo thưởng năng suất tháng" có icon lệch).

## Thiết kế (đề xuất — chờ duyệt)

### 1. Bộ lọc (`V2BaseSmartFilterPanel floating`)
- Ô tìm nhanh: `Tìm theo số hợp đồng, mã/tên khách hàng` (thay ô "Số hợp đồng" gõ khớp tuyệt đối hiện nay).
- Các ô: **Thời gian\*** (1 ô `type: 'date-range'`, key `date_range`, mặc định = tháng hiện tại, bắt buộc) · Công ty · Phòng ban · Bộ phận · Nhân viên (`V2BaseCompanyDepartmentFilter` như cũ) · Khách hàng.
- **Bỏ ô Năm + Tháng** — 1 ô Thời gian đã đủ (chọn tháng = chọn 01→cuối tháng). BE vẫn giữ nhận `year/month` để không gãy link/test cũ; FE chỉ gửi `date_from/date_to`.
- Bỏ ô "Show chi tiết" — thay bằng ô chọn cấp bung trong tiêu đề cột (mục 3).
- `header-actions` (cùng hàng Cài đặt bộ lọc, đúng thứ tự màn mẫu): Cấu hình cột hiển thị · In báo cáo · Xuất Excel.
- Bỏ card tiêu đề riêng "Báo cáo thưởng năng suất tháng" + icon lệch (tiêu đề đã có ở topbar, như màn mẫu) ⇒ hết lỗi lệch (yêu cầu 8). Ô ⓘ cạnh "Bộ lọc danh sách" ghi mục đích báo cáo.

### 2. Khối thống kê `.rsum` (đề xuất theo cột của báo cáo)
Dòng đầu: `Số liệu tại <giờ bấm Tìm>` ⓘ · `Kỳ dd/mm/yyyy – dd/mm/yyyy · N phòng ban · M nhân viên` · nút Thu gọn.

| Cụm | Ô | Công thức (tooltip) |
|---|---|---|
| QUY MÔ | Phòng ban | số phòng trong cây đã lọc |
| | Nhân viên có thưởng | số NV trong cây |
| | Hợp đồng phát sinh thưởng | số HĐ khác nhau (1 HĐ nhiều NV tính 1) |
| GIÁ TRỊ | DS tiêu chuẩn tính thưởng NS tháng | Σ DSTC các dòng HĐ |
| | Thưởng năng suất tháng | Σ (Có − Nợ) TK 3351, work TNST, trong kỳ |
| | Tỷ lệ thưởng / DSTC | Thưởng ÷ DSTC × 100 (DSTC = 0 ⇒ `—`) |

Số tính trên TOÀN BỘ kết quả lọc (không chỉ trang đang xem) ⇒ BE trả thêm `summary` trong `GET /`.
Ô thống kê chỉ hiển thị, không bấm (drill nằm ở bảng).

### 3. Bảng cây `rsum-tb`: Phòng ban ▸ Nhân viên ▸ Hợp đồng
- Cột: STT · Phòng ban / Nhân viên / Hợp đồng · Khách hàng · Số HĐ · DS tiêu chuẩn tính thưởng NS tháng · Thưởng năng suất tháng · **Tỷ lệ** (cột mới, đề xuất).
  Tiêu đề cột 1 dòng, cột số có ⓘ công thức (`ReportInfoTip`).
- Dòng TỔNG nền `#fdf1ea` đầu bảng; dòng phòng (d0) đánh I, II…; NV (d1) đánh 1, 2…; HĐ (d2) không số. Thụt 30/52/74px.
- Ô chọn cấp bung trong tiêu đề cột: **Chỉ phòng ban / Đến nhân viên (mặc định) / Đến hợp đồng**; caret từng dòng bung/thu riêng.
- Tên NV hiển thị `Tên - Mã phòng - Mã NV` (utils/employeeOptionText); số HĐ là link mở HĐ tab mới.
- Bấm số (`.rsum-drill`, gạch chân đứt):
  - Dòng NV — Số HĐ / Thưởng NS ⇒ popup chi tiết NV hiện có (`BonusMonthDetailModal`, HĐ ▸ phiếu ▸ mặt hàng).
  - Dòng HĐ — Thưởng NS ⇒ cùng popup, lọc sẵn HĐ đó (BE `detail` nhận thêm `contractable_type` + `contractable_id`).
  - Dòng phòng / TỔNG — Số HĐ ⇒ không drill ở đợt này (popup danh sách HĐ của phòng là việc thêm, chỉ làm nếu user muốn).
- Phân trang theo phòng ban, mặc định 20, chọn [10, 20, 50, 100] (hiện tại 10).

### 4. Cấu hình cột
`ColumnCustomizationModal` như màn mẫu; cột "Phòng ban / Nhân viên / Hợp đồng" khoá không ẩn được; lưu theo user (cùng cơ chế màn mẫu).

### 5. In
Giữ `print-list-data`; tham số `expand` lấy từ ô chọn cấp (Đến hợp đồng ⇒ 1). In theo cột đang hiện.

### 6. Xuất Excel
- Bấm ⇒ mở `export-fields-modal` chọn trường (mặc định = cột đang hiện), Đồng ý ⇒ nút chuyển trạng thái loading NGAY rồi mới gọi `export-rows` (hết đơ 3s).
- File: letterhead công ty (`fetchCompanyLetterhead`), cây phòng ▸ NV ▸ HĐ theo cấp đang chọn, ô số là số thật `#,##0`.

## Phạm vi code
**FE** (`hrm-client/pages/sale/bonus-month-report/`): viết lại `index.vue` theo khuôn màn mẫu; `components/export-excel.js` (chọn trường + cấp + letterhead); `detail-modal.vue` nhận thêm lọc HĐ. Không sửa component dùng chung.
**BE** (`Modules/Finance`, nhỏ):
- `BonusMonthReportService::search()` trả thêm `summary` {departments, employees, contracts, doanh_so_tieu_chuan, commission_month}.
- `contractRows()` nhận `keyword` (LIKE số HĐ / mã KH / tên KH) — giữ `contract_code` cũ.
- `detail()` nhận thêm `contractable_type` + `contractable_id`.
- Test thêm vào `BonusMonthReportServiceTest` / `BonusMonthApiTest`.
Không đổi số liệu/công thức — chỉ đổi trình bày.

## Cần user chốt
1. Bỏ hẳn ô Năm/Tháng, chỉ còn 1 ô Thời gian (mặc định tháng hiện tại)? — đề xuất **Có**.
2. Thêm cột **Tỷ lệ** (Thưởng ÷ DSTC)? — đề xuất Có (cấu hình cột ẩn được).
3. Số HĐ ở dòng phòng/TỔNG có cần bấm mở danh sách HĐ không? — đề xuất **Không** ở đợt này.

## Quyết định đã chốt (user 19/11: làm đúng phạm vi vé)
1. GIỮ ô Năm + Tháng; chỉ gộp Từ ngày – Đến ngày thành 1 ô `date-range` (bỏ lỗi đỏ "Bắt buộc" của ô lẻ).
2. KHÔNG thêm cột Tỷ lệ (bỏ luôn ô "Tỷ lệ thưởng / DSTC" ở khối thống kê).
3. Drill chỉ ở dòng NV và dòng HĐ; dòng phòng ban / TỔNG không bấm.
4. Không thêm gì ngoài vé.
- Lệch skill `report-styles` (không có popup chọn trường Excel): vé QA yêu cầu "chọn trường xuất Excel" → dùng `ExportFieldsModal` chung. Lý do: nghiệp vụ do vé quyết.
- Tiêu đề cột 2 bản in đổi "Nhân viên" → "Phòng ban / Nhân viên / Hợp đồng" cho khớp màn + Excel.

## Kết quả kiểm (Playwright 19/11)
- Năm 2026: 22 phòng / 164 NV / 7,135 HĐ; cây 3 cấp, select cấp hiển thị hoạt động.
- Drill dòng HĐ → popup tiêu đề "… — HĐ <mã>"; Tháng ↔ Thời gian xoá lẫn nhau.
- Xuất Excel: popup chọn trường 5/5, loading hiện < 120ms, file 14,753 dòng (TỔNG + 1 / 1.1 / 1.1.1), ô số thật.
- In: vượt 2,000 dòng thì báo thu hẹp lọc; Tháng 07/2026 in đúng cây.
- BE: 59 test Finance/BonusMonth* OK.
