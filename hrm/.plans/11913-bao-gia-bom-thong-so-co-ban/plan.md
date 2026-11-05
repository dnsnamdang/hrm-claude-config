# Báo giá / BOM giải pháp: Xem thêm cột Thông số kỹ thuật + cột Thông số cơ bản (#11913) — @cuong61n

Nhánh `develop` (hrm-api + hrm-client). Trạng thái: **CODE XONG + TEST TRÌNH DUYỆT LOCAL + ĐÃ PUSH `develop` + ĐÃ DEPLOY DEV (05/11/2026)** — hrm-api `317cd30d4` · hrm-client `09e469980` (build_tpe.sh trên hrm-dev, route cache + FE build đã có code mới).

**Quyết định đã chốt (tự chọn, chờ user xác nhận):** "Thông số cơ bản" = bảng thuộc tính của sản phẩm
(`attribute_products`: Tên: giá trị đơn vị, mỗi dòng 1 thuộc tính) — mục "Thông số cơ bản" ở màn sản phẩm; "Đặc điểm"
đã là cột Thông số kỹ thuật nên không lặp. Đọc trực tiếp từ sản phẩm theo `erp_product_id` (không lưu trên dòng
báo giá/BOM, không migration); hàng tạm → trống.

## Phase 1 — BE
- [x] 05/11 `AdminData::basicSpecs(ids)` — 1 query gom chuỗi thuộc tính theo sản phẩm (test local ok)
- [x] 05/11 `DetailQuotationResource` + `DetailBomListResource` trả `basic_spec` mỗi dòng
- [x] 05/11 Endpoint `POST assign/quotations/basic-specs` — nạp bù cho hàng vừa thêm/nhân bản
- [x] 05/11 Excel báo giá: cột tuỳ chọn "Thông số cơ bản" (cạnh Hình ảnh/Bảo hành), `with_basic_spec=0` để ẩn; import đọc theo tên header nên tự bỏ qua
- [x] 05/11 Excel BOM: `with_basic_spec=1` chèn cột sau "Số lượng*", trước 2 cột ẩn; import bỏ qua cột thừa

## Phase 2 — FE
- [x] 05/11 Component dùng chung `components/assign/SpecExpandCell.vue` — rút gọn 80px + "Xem thêm"/"Thu gọn"
- [x] 05/11 Báo giá (xem + sửa): cột TSKT rộng 260px dùng SpecExpandCell, thêm cột Thông số cơ bản, sửa colspan 10→11, nạp bù hàng mới
- [x] 05/11 BOM (lưới + Chọn cột hiển thị `basicSpec`): tương tự báo giá
- [x] 05/11 Cấu hình in Báo giá + BOM: "Thông số cơ bản" nằm trong danh sách "Chọn cột hiển thị" (không tách ô riêng) + cột trên bản in
- [x] 05/11 Xuất Excel báo giá (xem + sửa): popup chuẩn `ExportFieldsModal` (tích chọn + kéo thả thứ tự cột như danh sách); BE `fields=a|b|c` + `withColumnOrder()`, cột bắt buộc bị bỏ tích vẫn được giữ cuối bảng để nạp lại được; util `utils/assign/quotationExportColumns.js`
- [x] 05/11 Xuất Excel BOM: popup chuẩn `ExportFieldsModal` (tích chọn + kéo thả), giữ ô "Xuất hàng hoá cấp con"; BE `fields=` + `withColumnOrder()`, blade xuất theo TÊN cột; "Thông số cơ bản" ngay sau TSKT

## Đã kiểm
- php -l các file BE; compile template 10 file Vue ok; render view Excel BOM (có header + dữ liệu) và Excel báo giá local ok.
- [x] 05/11 Test trình duyệt (Playwright MCP, local, tk namdangit — không lưu dữ liệu nào):
  · Báo giá BG-00218: xem / sửa / tạo mới có cột; Xem thêm–Thu gọn; thêm hàng ERP từ popup → nạp bù 1 request; popup in (cột trong danh sách, tích/bỏ tích); xuất Excel kéo thả thứ tự → file đúng; nhập lại file đó: 140/140 Hợp lệ
  · BOM-00006 (sửa): cột + Xem thêm; thêm hàng ERP → nạp bù đúng; thêm hàng tạm → để trống, không gọi API; in; xuất Excel kéo thả
  · BOM-00030: xuất Excel đổi thứ tự rồi nhập lại → 3/3 Hợp lệ, 0 lỗi; BOM-00006 nhập: header đủ, cột thừa bỏ qua (Validate bị chặn "chỉ người tạo BOM" — không liên quan task)
  · Ghi chú: popup "Chọn cột hiển thị" của BOM không có nút mở (sẵn từ trước); `e2e/` trống trên máy này nên chưa có spec lưu lại.

## Còn mở
- Báo giá tổng hợp (`summary-quotations`) chưa làm cột này (ngoài phạm vi task).
