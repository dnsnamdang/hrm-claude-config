# Plan — Demo "Phiếu giao hàng" (từ Đơn mua hàng → Bộ phận giao hàng)

> Người phụ trách: @khoipv · Bắt đầu: 27/10/2026
> Design: `.plans/demo-phieu-giao-hang/design.md`
> Spec: `docs/superpowers/specs/2026-10-27-demo-phieu-giao-hang-design.md`

## Phase 1 — Khảo sát & thiết kế
- [x] 1. Đọc luồng hiện tại: `PurchaseOrder` (status, ship_method, dest), `PurchaseDeliveryPoint` / `PurchaseDeliveryCost`, `ShipTab.vue`, màn chi tiết đơn (`Xác nhận đã nhận` / `Xác nhận đã giao` bấm tay)
- [x] 2. Chốt luồng demo 5 bước: Đơn mua đã duyệt → Lập phiếu giao hàng → BP giao hàng tiếp nhận & phân công → Tài xế thực hiện → Kết quả cập nhật về đơn mua
- [x] 3. Viết spec + design tóm tắt

## Phase 2 — Demo HTML
- [x] 4. Code `demos/demo-phieu-giao-hang.html` (style V2Base, vanilla JS, mở trực tiếp)
- [x] 5. Cập nhật `demos/README.md`
- [x] 6. User xem demo + phản hồi (28/10/2026): bỏ bước Cung ứng lập phiếu chi tiết + điều phối phân công tài xế. Đơn mua gửi thẳng BP giao hàng → **ai phụ trách tự vào Tiếp nhận** → người phụ trách cập nhật tiến độ, **chi phí**, **chứng từ**

## Phase 3 — Làm lại demo theo phản hồi 28/10
- [x] 7. Đơn mua: nút "Gửi bộ phận giao hàng" (modal: lấy hàng từ, hạn giao, ưu tiên, ghi chú) — gửi toàn bộ SL còn phải lấy; bị trả lại → "Sửa & gửi lại"
- [x] 8. BP giao hàng: danh sách tab (Chờ tiếp nhận / Đang xử lý / Của tôi / Hoàn thành / Bị trả lại), đổi người đăng nhập trong bộ phận; Tiếp nhận = thành người phụ trách; Trả lại (bắt buộc lý do); trưởng BP / người phụ trách chuyển người phụ trách
- [x] 9. Màn xử lý phiếu (người phụ trách): tab Tiến độ (phương tiện, lấy hàng NCC, giao từng điểm) · Chi phí (khoản chi, số tiền, trả cho, hóa đơn) · Chứng từ (bắt buộc / tùy chọn, file, bản gốc) · Lịch sử; khối Điều kiện hoàn thành
- [x] 10. Kết quả về đơn mua: điểm giao, chi phí thực tế vs dự kiến, chứng từ, gửi phần còn lại
- [x] 11. Cập nhật spec + design + README

### Checkpoint — 2026-10-27 (bản 1, đã thay)
Vừa hoàn thành: demo `demos/demo-phieu-giao-hang.html` + spec + design + README + STATUS (đã kiểm cú pháp JS, chưa mở trình duyệt — user tự test)
Đang làm dở: —
Bước tiếp theo: user mở demo, chốt các câu hỏi mở ở spec §9
Blocked:

## Phase 4 — Mọi hình thức vận chuyển đều gửi BP giao hàng (phản hồi 28/10)
- [x] 12. Bỏ chặn gửi theo phương thức: NCC giao về kho / NCC giao thẳng KH / Cty tự lấy đều gửi được BP giao hàng
- [x] 13. Phiếu loại NCC giao: không có bước lấy hàng tại NCC; khối "Vận chuyển của NCC" (xe / nhà xe, tài xế); xác nhận thực nhận từng điểm (≤ SL yêu cầu, thiếu → lý do), kho = thủ kho ký
- [x] 14. Chi phí dự kiến theo phương thức (tự lấy: tự chi · NCC giao: cước NCC thu thêm); checklist / kết quả / danh sách hiển thị đúng theo phương thức
- [x] 15. Cập nhật spec + design + README + STATUS

### Checkpoint — 2026-10-28
Vừa hoàn thành: viết lại `demos/demo-phieu-giao-hang.html` bản 2 (gửi BP giao hàng → tự tiếp nhận → người phụ trách cập nhật tiến độ / chi phí / chứng từ → hoàn thành về đơn mua). Đã kiểm cú pháp JS + chạy thử luồng bằng node (cả về kho / giao KH, trả lại / gửi lại), chưa mở trình duyệt — user tự test. Đã cập nhật spec, design, README, STATUS.
Đang làm dở: —
Bước tiếp theo: user mở demo, chốt câu hỏi mở ở spec §9 (nhất là: tự tiếp nhận hay trưởng BP giao người; chứng từ bắt buộc; hoàn ứng chi phí tự chi)
Blocked:
- [x] 16. Đơn mua: bỏ khối "Phiếu giao hàng của đơn" (phản hồi 28/10)
- [x] 17. Popup Gửi bộ phận giao hàng: bỏ ô "Gửi tới" (phản hồi 28/10)
- [x] 18. Màn cập nhật phiếu đơn giản (phản hồi 28/10): bỏ Yêu cầu (lạnh / dễ vỡ), panel Người phụ trách (+ chuyển người), Điều kiện hoàn thành, tab Chứng từ, Hàng hóa & lộ trình, Lịch sử → 1 trang Tiến độ · Chi phí · Chứng từ (danh sách file, không bắt buộc) · Hoàn thành
- [x] 19. Bỏ hẳn Chứng từ (mục chứng từ trên phiếu, biên bản ở từng điểm, KPI / bảng chứng từ ở kết quả); chỉ còn file hóa đơn theo từng khoản chi phí
- [x] 20. Bỏ khối Phương tiện & người đi giao (cả Vận chuyển của NCC) + cảnh báo thuê xe ở Chi phí
- [x] 21. Tạm bỏ bước 4 "Hoàn thành → về đơn mua" (màn Kết quả); hoàn thành xong ở lại phiếu chỉ xem
- [x] 22. Chú thích luồng trên đơn mua ("Mọi phương thức đều gửi…") chuyển vào tooltip ⓘ cạnh tiêu đề Giao nhận & vận chuyển
- [x] 23. Bỏ khối "Câu hỏi cần chốt" khỏi màn Quy tắc của demo (câu hỏi vẫn giữ ở spec §9)
- [x] 24. Đổi "Số dòng" / "N dòng" (hàng hóa) → "Số mặt hàng" / "N mặt hàng" (popup gửi, thông tin phiếu, lấy thiếu)
- [x] 25. Điểm về kho: "Thủ kho ký nhận" đổi từ ô nhập tay sang chọn nhân viên (mặc định thủ kho); điểm khách hàng vẫn nhập tay
- [x] 26. Bỏ ghi chú "Chi phí dự kiến trên đơn mua…" ở đầu mục Chi phí (dòng Tổng vẫn so với dự kiến)
- [x] 27. Thêm nút Trả lại cung ứng ngay trên dòng phiếu Chờ tiếp nhận ở danh sách BP giao hàng (trước chỉ có trong màn chi tiết)
- [x] 28. Popup Gửi bộ phận giao hàng: bỏ "Lấy hàng từ" (ngày + giờ) và "Hạn giao xong", chỉ còn **Ngày lấy hàng** (bắt buộc); danh sách BP giao hàng gộp còn cột Ngày lấy hàng, bỏ cột Hạn giao
- [x] 29. Popup Gửi bộ phận giao hàng: bỏ bảng "Gửi kèm (toàn bộ SL còn phải gửi)" (phiếu vẫn tự kèm toàn bộ SL còn phải gửi)
- [x] 30. Tiến độ giao hàng — điểm về kho: bỏ ô "Thủ kho ký nhận" (form, dòng tóm tắt, validate, lịch sử, quy tắc), chỉ còn Thời gian nhận / giao; điểm khách hàng giữ "Người ký nhận"

### Checkpoint — 2026-10-28 (Phase 4)
Vừa hoàn thành: mọi hình thức vận chuyển đều gửi BP giao hàng. NCC giao (về kho / thẳng KH): không có bước lấy hàng, khối "Vận chuyển của NCC" (xe / tài xế NCC, người đi cùng), xác nhận SL thực nhận từng điểm ngay sau tiếp nhận (≤ yêu cầu, thiếu → lý do), chi phí dự kiến = cước NCC thu thêm (mặc định trả NCC), checklist / kết quả / danh sách theo phương thức. Đã kiểm cú pháp + chạy thử luồng bằng node cho cả 4 phương thức (gồm trả lại / gửi lại), chưa mở trình duyệt — user tự test. Đã cập nhật spec, design, README, STATUS.
Đang làm dở: —
Bước tiếp theo: user mở demo, thử 4 phương thức; chốt câu hỏi mở ở spec §9 (thêm: cước NCC có hóa đơn riêng không, NCC giao bù → phiếu mới hay mở lại phiếu cũ)
Blocked:

### Checkpoint — 2026-10-28 (đơn giản hóa)
Vừa hoàn thành: bỏ khối "Phiếu giao hàng của đơn" trên đơn mua, bỏ ô "Gửi tới" trong popup gửi, màn cập nhật phiếu còn 1 trang Tiến độ → Chi phí → Chứng từ → Hoàn thành (bỏ tab, panel phải, lịch sử, lộ trình, yêu cầu bảo quản, chứng từ bắt buộc). Đã kiểm cú pháp + chạy thử 4 phương thức bằng node, chưa mở trình duyệt.
Đang làm dở: —
Bước tiếp theo: user mở demo xem màn cập nhật mới; chốt câu hỏi mở spec §9
Blocked:

### Checkpoint — 2026-10-28 (bỏ chứng từ + phương tiện + bước 4)
Vừa hoàn thành: màn cập nhật phiếu còn Tiến độ giao hàng → Chi phí → Hoàn thành; bỏ chứng từ (phiếu + biên bản điểm + kết quả) và khối Phương tiện & người đi giao / Vận chuyển của NCC; tạm bỏ bước 4 về đơn mua; chú thích đơn mua vào tooltip. Đã kiểm cú pháp + chạy thử 4 phương thức bằng node, chưa mở trình duyệt.
Đang làm dở: —
Bước tiếp theo: user mở demo xem lại; chốt câu hỏi mở spec §9
Blocked:
