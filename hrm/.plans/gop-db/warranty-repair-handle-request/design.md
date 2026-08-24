# Phiếu xử lý yêu cầu (Warranty Repair Handle Request) — Design

> Người phụ trách: @namdangit · Nhánh: `gop_db` · Trạng thái: **đang brainstorm**

## Mục tiêu
Port màn "Phiếu xử lý yêu cầu" từ ERP sang HRM. Đây là **chứng từ thứ 2** của luồng dịch vụ,
lập từ Phiếu yêu cầu kiểm tra sửa chữa – bảo hành (chứng từ đã port xong ở
`.plans/gop-db/warranty-repair-request/`).

## Khảo sát ERP (đã làm)
- Code: `WarrantyRepairHandleRequestsController` (480 dòng), `Model/Customers/WarrantyRepairHandleRequest`
  (484 dòng), blade `customercare/warranty_repair_handle_requests/*`.
- Menu ERP: **CSKH → Kiểm tra bảo hành sửa chữa → Phiếu xử lý yêu cầu**.
- Bảng: `warranty_repair_handle_requests` (5.259 dòng trên DB gộp) · `warranty_repair_handle_request_products`
  · `warranty_repair_handle_request_product_manage_device_errors`.
- 6 trạng thái: Đang tạo · Chờ CCTT · Đã CCTT · Chờ CCTT bổ sung · Đang CCTT · Đã tư vấn điện thoại.
- 4 quyền: xem theo tổng công ty / công ty / phòng ban + "Tạo phiếu cung cấp thông tin".
- Luồng: mở từ phiếu yêu cầu (`?warranty_repair_request_id=`), chép sẵn khách hàng + thiết bị →
  mỗi dòng thiết bị chọn **lỗi thiết bị** (nhiều lỗi) và **hành động** (1 = Tư vấn điện thoại kèm
  nội dung xử lý · 2 = Cung cấp thông tin làm báo giá) → lưu.
  - MỌI dòng đều "Tư vấn điện thoại" → phiếu thành **Đã tư vấn điện thoại**, phiếu yêu cầu gốc
    cũng chuyển **Đã tư vấn điện thoại** (kết thúc luồng, không đi tiếp).
  - Có ít nhất 1 dòng "Cung cấp thông tin làm báo giá" → phiếu **Chờ CCTT**, thông báo cho những
    người có quyền "Tạo phiếu cung cấp thông tin" (**theo QUYỀN**, khác màn trước là theo phòng
    ban), phiếu yêu cầu gốc chuyển **Đã xử lý** + ghi Người xử lý / Ngày xử lý.

## Quyết định đã chốt (2026-08-20)
1. **Full parity ERP** — làm đủ danh sách, bộ lọc, lập/sửa/xem, Lưu, Lưu & Gửi duyệt, Không duyệt,
   In phiếu, In danh sách, Xuất Excel.
2. Nút **"Tạo phiếu cung cấp thông tin"** (chứng từ 3 chưa port) hiện đúng điều kiện nhưng bấm vào
   báo toast hướng dẫn xử lý tạm trên ERP — y như đã làm ở chứng từ 1.
3. Dữ liệu test: DB local, **tạo thoải mái, không cần dọn**; được đổi mật khẩu tài khoản để test.
4. (user tái xác nhận 2026-08-20) **Lưu nháp KHÔNG bắt đủ trường** (theo skill `form-validate`), khác ERP vốn bắt như nhau ở cả 2
   nút — giữ nhất quán với chứng từ 1.
5. (user tái xác nhận 2026-08-20) Bộ lọc theo tên hàng hóa / model làm **ĐÚNG**, không copy lỗi
   của ERP (ERP so nhầm mã dòng thiết bị với mã phiếu).
6. Trình bày theo skill: `V2Base*`, badge màu do BE trả, nút không đủ điều kiện thì ẩn hẳn, bảng
   cuộn 2 đầu, khung giấy ở màn in…

## Spec đầy đủ
`docs/superpowers/specs/gop-db/2026-08-20-warranty-repair-handle-request-design.md`

## Điểm KHÁC chứng từ 1 — dễ sai nhất
- Thông báo "Chờ CCTT" bắn **theo QUYỀN** ("Tạo phiếu cung cấp thông tin"), không theo phòng ban.
- Phạm vi quyền theo phòng ban **có cộng phòng đang công tác**, chứng từ 1 thì không.
- **Xóa phiếu xử lý phải trả phiếu yêu cầu gốc về "Chờ xử lý"** + xóa Người/Ngày xử lý.
- Mỗi thiết bị chọn **nhiều lỗi** (bảng nối riêng) và **1 hành động**; mọi dòng đều "Tư vấn điện
  thoại" thì phiếu tự thành "Đã tư vấn điện thoại" bất kể bấm nút nào.
