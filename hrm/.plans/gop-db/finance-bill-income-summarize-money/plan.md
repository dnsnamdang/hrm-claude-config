# Tổng hợp tiền về ngân hàng — Plan tài liệu

> @khoipv · Feature gốc: `.plans/gop-db/finance-bill-income-report/`

## Tài liệu SRS / HDSD / Testcase (03/11/2026) @khoipv

Khuôn: `../lookup-product-arrived-notifies/` + `../finance-addition-accounting-request/` + checklist "Mẫu tài liệu.xlsx".

- [x] Đọc code màn + plan feature gốc (`summarize-money.vue`, V2Base dùng chung, `BillIncomeReportSummarizeService`, `searchSummarizeCustomers`, `BillIncomeReportSummarizeExport`, controller; màn đích `BillAdjustDeptRequestForm` + `billIncomeReportDetails`; quyền xem `BillIncomeReportAccess`)
- [x] Chụp ảnh (dev, chỉ đọc) — `thtv_shots/_capture/capture.js`, DNS Admin: danh sách, dòng Đã điều chỉnh hết, khối lọc, 2 trạng thái tích chọn + thông báo chặn 2 phiếu, màn Tạo phiếu yêu cầu điều chỉnh công nợ (thoát bằng Quay lại, không hỏi vì chưa nhập), chi tiết phiếu báo có, Xuất Excel, Tùy chỉnh cột, Cài đặt bộ lọc; 40 icon (trim_icon `--dry` 0/40). Không bật cờ giả, không bấm Lưu / Gửi duyệt. Tải 4 file Excel (GET) về scratchpad để soát cấu trúc.
- [x] gen_srs.py → SRS - Tổng hợp tiền về ngân hàng.docx: 7 chức năng (Xem danh sách 3 lối vào menu, Tìm kiếm và lọc, Cài đặt bộ lọc, Tùy chỉnh cột, Xuất Excel, Xem phiếu báo có, Tạo mới điều chỉnh công nợ), Phần 4 BR-01..BR-13, Phần 5 (2 bảng). Selfcheck khớp mẫu, 58 trang. Metrics: ui=13.7 ev=5.4 evch=1457 intro=2050, noBefore/noDuring=0.
- [x] gen_hdsd.py → HDSD_Tong hop tien ve ngan hang.docx: 6 PHẦN, 13 trang.
- [x] gen_testcase.py → testcase.xlsx: 146 TC, P0 65 (45%), 8 nhóm (I Hiển thị · II Tìm kiếm và lọc + Cài đặt bộ lọc · III Xem chi tiết · IV Tùy chỉnh cột · V Xuất Excel · VI Ảnh hưởng màn khác · VII Phân quyền (duy nhất) · VIII Chọn dòng và tạo mới điều chỉnh công nợ); tc_engine sạch.
- [x] gen_checklist.py → Đối chiếu checklist.xlsx: Testcase 115 có TC / 209 N/A (Thêm mới, Chỉnh sửa, Xóa, Khóa/Mở khóa, Lịch sử, Import, Duyệt, Không duyệt + vài dòng ràng buộc); SRS 92 có mục / 71 N/A.
- Lệch checklist / nghi lỗi ghi nhận (không sửa code): bộ lọc không được ghi nhớ (rời màn, F5 đều mất — `pathsToKeep` chỉ khớp `/summarize-money/<số>` không tồn tại); cửa sổ Xuất Excel luôn tích cả 10 trường (màn truyền `visibleExportFields` nhưng không dùng `exportFieldsMixin`); nút Quay lại ở Chi tiết phiếu báo có về danh sách Phiếu báo có, không về màn này; người không có quyền xem phiếu báo có vẫn thấy dòng nhưng bấm Số báo có báo "Không tải được phiếu báo có"; ký tự % _ là ký tự đại diện; chặn chọn 2 phiếu báo có chỉ ở giao diện; dev: cột Khách hàng trống ở cả 8043 dòng.

### Checkpoint — 2026-11-03 11:30
Vừa hoàn thành: bộ tài liệu SRS + HDSD + testcase + đối chiếu checklist màn Tổng hợp tiền về ngân hàng (chạy sạch 4 script).
Đang làm dở: không.
Bước tiếp theo: user xem lại tài liệu, quyết định có đẩy Drive không; quyết định có sửa các điểm lệch (ghi nhớ bộ lọc, trường xuất mặc định, Quay lại từ chi tiết).
Blocked:

### Sửa Phần 5 SRS theo khuôn Drive (03/11/2026) @khoipv
- [x] Phần 5 đổi về khuôn SRS "Khai báo tồn kho đầu kỳ" trên Drive (user chỉ định 04/11): tiêu đề "Phần 5. Bảng danh sách các màn hình tham chiếu dữ liệu", câu dẫn có dẫn chiếu BR, 1 bảng 4 cột STT | Nhóm | Màn hình | Đường dẫn (giải thích ngắn trong ngoặc, đường dẫn "Phân hệ => … => Tên màn"); bỏ bảng 7 cột + bảng 2
- [x] gen_checklist: dòng 161 → N/A (màn không có Khóa / Mở khóa), dòng 163 ghi chú lại; sinh lại SRS (selfcheck khớp bản mẫu) + Đối chiếu checklist
- [x] (04/11) Sửa Phần 5 trên bản SRS ở Drive (folder SRS chuyển đổi), giữ nguyên phần người khác đã sửa + nhận xét: 4 file sửa TRỰC TIẾP trong Google Docs (xoá nội dung cũ sau tiêu đề Phần 5, dán câu dẫn + bảng 4 cột); riêng Báo cáo hạn mức công nợ KH đã tải phiên bản mới lên (dựng từ bản Drive 09:07 có sửa "Tùy chỉnh cột" của người khác; file không có nhận xét nào). Tải về kiểm: Phần 1–4 không đổi, số ảnh không đổi, tiêu đề Heading 1, dòng tiêu đề bảng in đậm
- [x] (04/11) Theo file mẫu SRS "Yêu cầu kiểm tra sửa chữa – bảo hành" (user chỉ định): đường dẫn Phần 5 đổi sang "Phân hệ -> Nhóm menu" (không ghi tên màn); gen_srs thêm ngắt trang trước Mục lục + căn giữa chữ "Mục lục"; sinh lại SRS (selfcheck khớp). Drive: 4 file sửa đường dẫn bằng Tìm & thay thế trên Google Docs; Báo cáo hạn mức KH (0 nhận xét, bản Drive thiếu chữ 21 ô) tải phiên bản mới từ bản đầy đủ, giữ sửa "Tùy chỉnh cột" của người khác; 2 file khổ ngang (Báo cáo hạn mức KH, YC hạch toán MDV) chuyển khổ đứng trên Docs. Giữ các mục riêng của màn báo cáo (skill bắt buộc, user chốt)
