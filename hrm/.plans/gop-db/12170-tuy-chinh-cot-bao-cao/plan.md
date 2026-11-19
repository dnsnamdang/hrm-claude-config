# Plan — #12170 Báo cáo - Tùy chỉnh cột

## Phase 1 (FE hrm-client)
- [x] Khảo sát 11 màn: 3 màn hạn mức công nợ đã có tuỳ chỉnh cột, 8 màn rsum-tb chưa có
- [x] Tồn kho tổng hợp theo mặt hàng (`warehouse/stock-general-product`) — làm khuôn: bảng `columnDefs` + prop `visibleKeys`, trang dùng columnCustomizationMixin; nhóm "Chi tiết" chỉ có khi `meta.show_detail`
- [x] Tồn kho chi tiết theo mặt hàng (`warehouse/stock-detail-by-product`) — khoá STT + cột cây; popup: Mã hàng, Model, Thương hiệu, ĐVT, Hợp đồng, SL tồn
- [x] Tồn kho theo vị trí (`warehouse/stock-location-product`) — khoá STT + cột cây; popup: Nhà kho, Mã hàng, Model, Thương hiệu, ĐVT, SL tồn, SL, Cộng
- [x] Tồn theo kho (`warehouse/stock-warehouse-product`) — khoá STT + Tên hàng; nhóm "Chi tiết theo kho" 1 mục, chỉ có khi `meta.show_detail`
- [x] Tổng hợp xuất nhập tồn (`warehouse/change-summary-report`) — khoá STT + Tên hàng; mỗi cột 1 mục
- [x] Hàng thừa thiếu sau tổng kiểm kê (`warehouse/self-inventory-report`) — khoá STT + cột cây; ô tên dòng cha chỉ gộp sang Model/Mã hàng khi 2 cột đó đứng liền sau (`nameSpan`)
- [x] BC theo dõi lắp đặt - bàn giao - SC - BD (`customer-care/report/install-delivery-repair`) — key mới `cc_report_install_delivery_repair`; bỏ min-width cứng, tính theo cột đang hiện
- [x] BC theo dõi chi tiết lắp đặt - bàn giao - SC - BD (`customer-care/report/install-delivery-repair-detail`) — key `cc_report_install_delivery_repair_detail`, 1 cấu hình chung 3 tab
- [x] Kiểm: compile template + babel parse 16 file OK (chưa mở trình duyệt)

## Phản hồi QA 17/11 — "Chuyển nút ra ngoài cùng"
Ảnh QA chụp màn BC bốc xếp (transport, #12169 — Tri Lee) mũi tên chỉ nút cột sang trái, trước "In báo cáo".
- [x] Chuyển nút "Cấu hình cột hiển thị" lên ĐẦU nhóm `#header-actions` (trước In / Xuất Excel) ở 8 màn
- [x] Kiểm compile template 8 file — OK (chưa mở trình duyệt)
- [x] User yêu cầu sửa cả: chuyển nút lên đầu ở 3 màn transport (`ArrangeReportPage`, `TransportReportPage`,
  `DriverCostReportPage` — #12169 Tri Lee) + `finance/import-direct-stocks` — compile OK

### Checkpoint — 16/11/2026
Vừa hoàn thành: nút Tuỳ chỉnh cột cho 8 màn báo cáo rsum-tb (3 màn hạn mức công nợ đã có sẵn); 16 file hrm-client, biên dịch OK
Đang làm dở: —
Bước tiếp theo: user mở trình duyệt kiểm ẩn/hiện + kéo thứ tự cột ở 8 màn; In/Xuất Excel chưa theo cột đang hiện (ngoài phạm vi)
Blocked:
