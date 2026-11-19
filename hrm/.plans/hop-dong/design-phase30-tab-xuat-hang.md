# Phase 30 — Tab "Xuất hàng" trên màn xem hợp đồng bán (thiết kế 10/11/2026)

Mockup: `mockup-tab-xuat-hang.html` (cùng thư mục). Chưa code. **User duyệt thiết kế 10/11 ("ok").**

## 1. Mục đích & người dùng

- Người dùng chính: **kinh doanh phụ trách HĐ** (người lập HĐ). Tab nằm trên form xem HĐ.
- Mục đích (user chốt 10/11): **thấy toàn cảnh việc thực hiện xuất hàng của HĐ** trong một lần nhìn — tổng thể đi được bao xa,
  từng mặt hàng đang ở khâu nào, đã giao mấy đợt, đợt nào đang kẹt.
- Không phải màn nghiệp vụ kho / kế toán: KHÔNG hiện tài khoản (1541/155/632/1561), kho lắp ráp, phiếu nhập cha tự động
  dưới dạng chứng từ kế toán.

### Mục tiêu
- Một tab "Xuất hàng" trên `pages/assign/contracts/_id/index.vue`. Hiện khi HĐ ở trạng thái từ Có hiệu lực trở đi
  (6, 19, 20, 21, 22, 12, 11, 10). Đóng (18) chỉ đóng được từ "Chờ KH ký" (ContractService::close) ⇒ không bao giờ có YCXH ⇒
  chỉ cần trạng thái, KHÔNG truy vấn (kiểm code 10/11).
- Số liệu theo **dòng HĐ** (dữ liệu Phase 29 đã gắn `hrm_contract_product_id` suốt chuỗi).
- Từ tab lập được YCXH (nút chuyển vào đây).

### Không làm (non-goals)
- Không sửa / lập phiếu kho ngay trong tab (chỉ link sang màn phiếu).
- Không hiện bút toán, không báo cáo công nợ / thu tiền (đã ở tab Điều khoản thanh toán).
- Không đổi quy tắc "còn lại" / giới hạn xuất đã chốt ở Phase 29.

### Anti-goal (hỏng dù chạy đúng)
- Số trên tab lệch với số mà màn Tạo YCXH dùng để chặn ("còn lại" khác nhau ⇒ kinh doanh mất tin).
- Kinh doanh thấy chứng từ kế toán nội bộ (phiếu nhập cha, PXH tự động, kho LRHD) như việc họ phải xử lý.

## 2. Bố cục (mockup)

### 2.1 Dải tổng quan (trên cùng, 1 hàng thẻ)
- **Tiến độ chung**: thanh % đã xuất **theo giá trị HĐ** (Σ SL Hoàn tất × đơn giá / tổng giá trị hàng). Ẩn thẻ này với người
  bị ẩn giá — dùng đúng luật ẩn giá đang chặn bản in phụ lục (403) ở Phase 28.
- 4 thẻ đếm **số dòng hàng** theo trạng thái: Chưa yêu cầu · Đang xử lý · Đã xuất kho · Hoàn tất. Bấm thẻ ⇒ lọc bảng (bấm lại bỏ lọc).
- Thẻ **Trả lại** (chỉ hiện khi có).
- Nút **"Yêu cầu xuất hàng"** góc phải dải — giữ cờ BE hiện có (người lập HĐ + HĐ đủ điều kiện xuất), tắt khi
  `hasLinesLeftToRequest() = false`. Nút cũ ở thanh hành động: gỡ hay giữ ⇒ xem mục 6.

### 2.2 Bảng theo hàng hoá (thân tab)
Cây cha–con như tab Chi tiết HĐ. Cột:

| Cột | Ý nghĩa |
|---|---|
| Hàng hoá (mã · tên) | như tab Chi tiết; dòng cha lắp từ con có nhãn "Đã lắp x/y bộ" |
| ĐVT | |
| SL HĐ | |
| Đã yêu cầu | Σ SL trên YCXH chưa huỷ (gồm nháp) — lấy từ `contractRemainingByLine` (đọc `product_export_request_tab_products.contract_product_id`) |
| Đã xuất kho | Σ SL PXK đã trừ tồn (hàng rời kho) |
| Đã hạch toán | Σ SL trên PXH ĐÃ DUYỆT (status 1 = bước duyệt chốt, ghi sổ; + quyết toán 12/13; nháp/chờ duyệt 3 không tính). User đổi tên 10/11 (trước: "Hoàn tất") — thẻ trạng thái, chú thích, bước cuối dòng thời gian cũng đổi |
| Trả lại | Σ SL phiếu nhập hàng bán trả lại đã hoàn tất (user chốt: cột riêng, không trừ vào cột khác) |
| Còn lại | = `remaining_qty` của `contractRemainingByLine` — KHÔNG tự tính SL HĐ − Đã yêu cầu (dòng con lấy min với giới hạn theo dòng cha, công thức tay sẽ lệch) |
| Tiến độ | thanh nhỏ chia màu 3 khúc: yêu cầu / xuất kho / hoàn tất |

- Bấm một con số (Đã yêu cầu / Đã xuất kho / Hoàn tất / Trả lại) ⇒ popup danh sách phiếu tạo nên số đó:
  mã phiếu · ngày · SL · trạng thái · link mở màn phiếu (tab mới).
- Trạng thái dòng — xét theo thứ tự, dòng rơi vào ô ĐẦU TIÊN khớp (phủ mọi ca, tổng 4 thẻ = số dòng đếm):
  1. Hoàn tất: Hoàn tất ≥ SL HĐ · 2. Chưa yêu cầu: Đã yêu cầu = 0 · 3. Đang xử lý: Đã xuất kho < Đã yêu cầu ·
  4. Đã xuất kho: còn lại (kể cả ca "yêu cầu 5/10, 5 đã hoàn tất" — cột Còn lại cho thấy phần chưa yêu cầu).
- Thẻ đếm **chỉ dòng cấp 1** (dòng cha + dòng thường); dòng con không đếm nhưng vẫn lọc theo dòng cha của nó (Claude chốt).
- Dòng con: cột Hoàn tất hiện SL PXH loại 20 đã hạch toán (chỉ số lượng, không bút toán).

### 2.3 Dòng thời gian các đợt xuất (dưới bảng, thu gọn được)
Mỗi YCXH của HĐ = 1 mốc: ngày lập · mã YCXH · loại (Xuất bán / Xuất sản xuất) · số dòng · **khâu hiện tại** gọi theo
việc thật: Đã yêu cầu → Kho đang soạn → Đã xuất khỏi kho → Hoàn tất (hoặc Đã huỷ, mờ). Bấm mã ⇒ mở YCXH.
Thay cho chế độ "Theo phiếu" — không dùng nút gạt 2 chế độ.

## 3. Quy tắc số liệu

1. Mọi số gom theo `hrm_contract_product_id` (5 bảng đã có cột từ Phase 29: `product_export_request_details`,
   `warehouse_export_request_details`, `warehouse_export_lots`, `product_export_details`, `product_import_details`).
2. Phiếu đã huỷ không vào cột nào (popup vẫn có thể hiện mờ — để builder quyết).
3. **Dòng cha lắp từ con** (có dòng con trong HĐ):
   - Đã yêu cầu = YCXH loại 21 tay của dòng + số bộ quy đổi từ YCXH con (đúng luật giới hạn chung Phase 29).
   - Đã xuất kho = số bộ đã lắp (phiếu nhập cha tự động Hoàn tất) + PXK loại 21 tay.
   - Hoàn tất = PXH loại 21 (tay + tự động) đã hạch toán.
   - Nhãn "Đã lắp x/y bộ": x = số bộ lắp, y = SL HĐ.
4. **Dòng con**: chỉ số lượng xuất sản xuất (YCXH/PXK/PXH loại 20); không hiện hạch toán.
5. **Trả lại**: phiếu nhập hàng bán trả lại lập từ PXH loại 21 của HĐ. Dòng trả lại trỏ về
   `product_export_request_detail_id` ⇒ lấy `hrm_contract_product_id` qua dòng đó. ⚠ Builder kiểm lại đường nối này
   trước khi viết query (chưa lần tới bảng chi tiết phiếu nhập trả lại).
6. "Còn lại" không cộng lại hàng trả lại (Claude tự chốt: xuất bù là việc của phụ lục HĐ). User muốn khác ⇒ đổi.

## 4. API (gợi ý cho builder)
- 1 endpoint đọc: `GET assign/contracts/{id}/export-progress` ⇒ `{summary, lines[], timeline[]}`; quyền = quyền xem HĐ;
  ẩn giá ⇒ không trả giá trị tiền (BE quyết, không chỉ ẩn FE).
- Popup phiếu: `GET assign/contracts/{id}/export-progress/documents?line_id=&column=` (lazy, chỉ gọi khi bấm số).
- Tái dùng `ProductExportRequestService::contractRemainingByLine` cho "Đã yêu cầu/Còn lại" — không viết công thức thứ 2.

## 4b. Hiệu năng — mở HĐ không được chậm thêm (user yêu cầu 10/11)
Đo 10/11 trên rehearsal (44k YCXH, 239k dòng tab_products, 282k dòng request_details): API xem HĐ HIỆN ĐÃ chạy
`contractRemainingByLine` mỗi lần mở (cờ `is_can_create_export_request` → `hasLinesLeftToRequest`) ≈ **111 ms** (HĐ 3443).
1. **Tải lười**: KHÔNG thêm gì vào `GET assign/contracts/{id}`. Dữ liệu tab chỉ gọi khi bấm tab "Xuất hàng" lần đầu
   (khuôn `loadPrintDoc` của tab Mẫu in Phase 28), giữ lại khi đổi tab qua lại; có nút tải lại. Popup phiếu gọi riêng khi bấm số.
2. **Hiện tab không tốn truy vấn**: quyết bằng `status` có sẵn trong payload HĐ. Ca Đóng (18) có YCXH: dùng
   `is_can_create_export_request`/cờ sẵn có hoặc 1 `exists` — KHÔNG đếm số lên nhãn tab (đếm = truy vấn mỗi lần mở).
3. **Endpoint tab** gom bằng vài truy vấn `GROUP BY hrm_contract_product_id` (5 bảng đã có index `idx_*_hrm_cpp` từ Phase 29),
   không N+1 theo dòng; tái dùng 1 lần `contractRemainingByLine` trong request. Mục tiêu < 300 ms với HĐ lớn; đo bằng HĐ nhiều dòng nhất trên rehearsal.
4. ⚠ Index thiếu: `product_export_requests.emplement_contract_id`, `product_exports.emplement_contract_id`,
   `product_export_request_tab_products.contract_product_id` chưa có index (SHOW INDEX 10/11). Lọc phiếu theo HĐ đang quét bảng.
   Đề xuất migration thêm index (cũng làm nhanh luôn phần 111 ms đang có khi mở HĐ) — **hỏi user riêng** khi lập kế hoạch (bảng ERP dùng chung, chạy trên prod lớn).
5. Không tính trước / không cache bảng tổng hợp ở giai đoạn này — số phải khớp tức thời với màn Tạo YCXH.

## 5. Kiểm
- PHPUnit cho service tổng hợp: HĐ cha–con (lắp đủ / lắp dở), 2 dòng cha trùng mã, có phiếu huỷ, có trả lại, ẩn giá.
- Playwright: đo DOM số ô, khớp số với màn Tạo YCXH ("Còn lại" = số picker cho phép), thẻ lọc, popup, ẩn giá, HĐ chưa có
  hiệu lực ⇒ không có tab. Bổ sung ca e2e vào bộ hợp đồng.

## 6. Các điểm Claude tự chốt (user soát)
1. "Hoàn tất" = PXH đã hạch toán; cha lắp từ con tính theo PXH cha tự động.
2. Dòng con không hiện hạch toán / kho lắp ráp.
3. Phiếu huỷ không tính.
4. "Còn lại" không cộng hàng trả lại.
5. Tiến độ chung tính theo giá trị, CHỈ trên dòng cấp 1 (như tổng HĐ ở `ContractService`, không cộng trùng con); ẩn giá dùng cờ `hide_price` có sẵn ở ContractController.
6. "Đã yêu cầu" tính cả YCXH nháp — để khớp đúng số chặn của màn Tạo YCXH.
7. Nút "Yêu cầu xuất hàng" CHỈ ở thanh hành động dưới đáy (sửa 10/11 khi code: 8 tab + nút chữ trên hàng tab tràn mép phải 34px ở 1200px ⇒ hàng tab chỉ còn nút icon Tải lại).

8. Thẻ trạng thái chỉ đếm dòng cấp 1; luật xếp trạng thái theo thứ tự ở mục 2.2.
9. Điều kiện hiện tab ở mục 1.

## 7. Builder check 10/11 (subagent, Claude đã tự kiểm lại trong code)
- Đã sửa: Còn lại = `remaining_qty`; nguồn Đã yêu cầu; luật trạng thái phủ hết ca; thẻ chỉ đếm dòng cấp 1; điều kiện hiện tab.
- **Trả lại hàng cha lắp tự động** (user "ok" 10/11 không chọn rõ ⇒ Claude áp phương án 1: Phase 30 chấp nhận hiện trạng, cột Trả lại chỉ tính
  hàng cha mua sẵn + hàng thường; việc cho trả lại cha lắp tự động ghi vào danh sách vấn đề ngoài luồng, làm riêng nếu user muốn): PXH cha tự động sinh với `product_export_request_id = null`
  (`ContractParentImportService.php` ~288) ⇒ luồng "bán trả lại" (lấy dòng từ YCXH của PXH) không có dòng nào để trả
  ⇒ HIỆN KHÔNG trả lại được hàng cha lắp từ con. Phiếu trả lại nối về YCXH qua
  `product_import_request_details.product_export_request_detail_id` (ERP lập).
