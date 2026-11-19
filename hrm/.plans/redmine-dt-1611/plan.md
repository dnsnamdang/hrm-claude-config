# Redmine fix-bug-dao-tao-danh-gia — Mới + Phản hồi 16/11/2026

Worktree: `HRM/wt-<vé>-api`, `HRM/wt-<vé>-client` (nhánh `fix/<vé>` từ origin/develop).

## #12144 Phản hồi — BC chi tiết DSTC theo 1 HĐ (`/sale/revenue-standard-contract`)
- [x] Popup chọn hợp đồng: thêm lọc Công ty, Phòng ban, Loại hợp đồng; sort theo Số HĐ, Giá trị HĐ
- [x] Dòng "Giảm vượt định mức", "Chi phí dự phòng" chữ đỏ như ERP
- [x] Bỏ lựa chọn "Đến nhóm" ở select cấp hiển thị
- [x] In: nới 2 cột hệ số cho tiêu đề không xuống dòng nhiều

## #12164 Mới — BC theo dõi thực hiện HĐ
- [x] UI theo form báo cáo mới (khuôn `/warehouse/self-inventory-report`)
  - Nút In / Xuất Excel lên đầu khối lọc (`#header-actions`), tiêu đề + ⓘ mục đích, nút "Xóa lọc"
  - Bảng cây mới `components/MonitorContractTable.vue` (Phòng → NV → HĐ, chọn cấp bung, dòng TỔNG, tiêu đề 1 dòng, phân trang theo HĐ)
  - Dòng kỳ báo cáo `.rsum`; đang tải lại thì làm mờ báo cáo cũ
- [x] Thời gian: chỉ cần nhập 1 trong 2 (từ / đến) là lọc được
  - BE `required_without_all:contract_code,<ngày kia>`; `after_or_equal` chỉ khi đủ 2 ngày
  - FE tự gắn lỗi ô Thời gian (không dùng helper chung vì helper bắt đủ 2 đầu); dòng kỳ / bản in chỉ ghi đầu đã nhập
- [x] Lọc thời gian báo "Lỗi khi tải dữ liệu" → sửa
  - Nguyên nhân: kỳ dài ~19k HĐ, truy vấn gộp 3 nguồn 15–100s → quá thời gian chờ máy chủ (504, không có JSON message)
  - `set_time_limit(300)` cho index / export-rows / print; FE báo rõ "máy chủ xử lý quá lâu…" trong bảng, giữ báo cáo cũ
- [x] Cùng bộ lọc: danh sách rỗng nhưng In ra 23 nghìn dòng, Xuất Excel lỗi → In/Excel phải dùng đúng bộ lọc như danh sách
  - BE `reusedRows()`: In + Excel dùng chung bộ nhớ đệm với danh sách (khóa bỏ tham số rỗng) → cùng tập dòng, không chạy lại truy vấn
  - FE In / Xuất chỉ dùng bộ lọc của lần tải THÀNH CÔNG (`reportParams`); chưa có báo cáo thì Tìm kiếm trước
  - Bản in đếm "N dòng" = số HĐ có phòng, khớp tổng của danh sách

## #12167 Mới — Phiếu hạch toán dịch vụ HĐBH: Tạo mới
- [x] Thêm nút "Lưu và tiếp tục" ở màn tạo mới (`/finance/service-accounting/create`)
  - client e96b04a04 (nhánh fix/12167): Lưu nháp + remount form, bỏ query YC — copy pattern `pages/finance/service-accounting-requests/create.vue` + saveAndContinueMixin
