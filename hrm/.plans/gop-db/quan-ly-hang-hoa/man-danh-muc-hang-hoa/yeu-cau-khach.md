# DANH MỤC HÀNG HÓA — yêu cầu khách (nguyên văn, user đưa 21/09/2026)

## Tab 1: Thông tin chung
- Tên hàng hóa
- Model
- Tên hàng thường gọi
- Tên tiếng anh
- Tính chất hàng hóa: Hiển thị theo loại sản phầm
- Nhóm chức năng: Hiển thị theo loại sản phẩm
- Nhóm sản phẩm: Hiển thị theo loại sản phẩm
- Loại sản phẩm: Bắt buộc chọn
- Đặc tính sản phẩm
- Barcode
- Định mực công lắp đặt
- Ghi chú
- Tài liệu kỹ thuật
- Thông số cơ bản
- Đơn vị tính
- Thương hiệu
- Xuất xứ
- Hãng sản xuất
- Code đặt hàng
- Công ty quản lý
- Hình ảnh
- Video

## Tab 2: Thông số kỹ thuật
- Phụ kiện tiêu chuẩn
- Đặc điểm
- Phụ kiện tùy chọn mua thêm
- Vật tư phục vụ sửa chữa – bảo hành
- Vật tư phục vụ lắp đặt
- Công thức lắp ráp
- Hãng xe
- Loại xe
- Model xe
- Đời xe

## Tab 3: Kỹ thuật
- Hệ số công nghệ
- Bảo hành

## Tab 4: Mua hàng
- Tên khai báo hải quan
- HS code
- % VAT
- Thuế nhập khẩu (không có CO)
- Thuế nhập khẩu (Có CO)
- Thuế chống bán phá giá
- SL tối thiểu nhập mua
- Hệ số tính thuế bảo vệ môi trường

## Tab 5: Dữ liệu quản trị
Mỗi công ty sẽ có thông tin khác nhau
- Nhà cung cấp
- Chính sách kinh doanh
- SL tồn kho tối thiếu

## Tab 6: Giá bán
- Quản lý thông tin giá cả của hàng hóa tại từng công ty theo thời gian. Các trường thông tin bao gồm:
- Đơn vị tính, giá vốn, giá mua ngoài. Loại giá, Hệ số, Giá công thức, Giá bán, Định mức đàm phán giá, Ngày hiệu lực. Hệ số giá theo công ty

---

## Ghi chú đọc hiểu (không có trong bản gốc)

- **Cây phân loại đi NGƯỢC**: người dùng chọn **Loại sản phẩm** (lá, bắt buộc), còn Tính chất hàng
  hóa / Nhóm chức năng / Nhóm sản phẩm chỉ **hiển thị suy ra** từ nó — không phải cascade 4 cấp
  từ trên xuống.
- "Loại **sản phẩm**" (cây Phase 0) ≠ "Loại **hàng hóa**" (`products.product_cate` enum cũ).
- Tab 3 "Kỹ thuật" chỉ có 2 trường, tên gần trùng tab 2 "Thông số kỹ thuật" — cần xác nhận lại với
  khách khi dựng mockup.
- Tab 5 và tab 6 đều ghi rõ **theo từng công ty** → đã chốt tách sang Phase 3 (xem `design.md`).

---

# LOGIC XÂY DỰNG HÀNG HOÁ — yêu cầu khách (nguyên văn, user đưa 23/09/2026)

Logic xây dựng hàng hoá như sau:

**Bước 1: Nhập thông tin hàng hoá.**
- Màn hình "Hàng hoá đang nhập thông tin"
- Quyền "Nhập thông tin hàng hoá (?)"
- Nhập đầy đủ thông tin các tab như Mockup
- Nếu lưu nháp =>> hàng hoá trạng thái "Đang nhập thông tin"
- Nếu Lưu =>> hàng hoá chuyển sang trạng thái "Chờ tính giá bán"
=>> hàng hoá ở trạng thái này sẽ chuyển sang màn hình "Hàng hoá chờ tính giá"

**Bước 2: Tính giá hàng hoá**
- Màn hình "Hàng hoá chờ tính giá".
- Quyền "Tính giá bán hàng hoá".
- Màn hình sẽ lấy hàng hoá ở trạng thái "Chờ tính giá"
- Nhập đầy đủ thông tin giá =>> lưu tạm =>> hàng hoá chuyển trạng thái "Đang tính giá"
                =>> Lưu & duyệt giá bán =>> trạng thái "Đang kinh doanh"
=>> hàng hoá "Đang kinh doanh" Sẽ vào màn "Danh mục hàng hoá kinh doanh" và các popup tìm kiếm hàng hoá trên báo giá/hợp đồng/..

=>> **Lưu ý quan trọng:**
- Hàng hoá của Công ty nào thì do người có quyền của công ty đó xây dựng/cập nhật

**Logic chia sẻ hàng hoá giữa các Công ty trên hệ thống phần mềm ERP:**

- Các Công ty ty có thể lấy hàng hoá của nhau về =>> nhập thêm các thông tin quản trị theo công ty =>> tính giá bán
- Trạng thái của hàng hoá cũng quản lý theo Công ty: 1 mã hàng Công ty TPE có trạng thái "Đang kinh doanh" nhưng Power có thể ở trạng thái "Đang nhập thông tin".
- Màn "Hàng hoá đang nhập thông tin" có button "Xem hàng hoá Công ty khác" =>> Logic chi tiết như sau:
    + Quyền sử dụng button này vẫn lấy "Nhập thông tin hàng hoá"
    + Khi click button Mở popup hiển thị hàng hoá của các công ty khác tạo ra mà hiện tại công ty của user chưa sử dụng (chưa có trong 3 màn hình quản lý hàng hoá theo công ty như nêu ở trên).
    + Có đầy đủ bộ lọc hàng hoá theo công ty quản lý hàng hoá (cty tạo ra), danh mục phân loại hàng hoá
    + Có checkbox lựa chọn các hàng hoá =>> khi click Chọn =>> hàng hoá chuyển vào màn hình "Hàng hoá đang nhập thông tin" sau đó tiếp tục theo logic xây dựng hàng hoá của 1 Công ty.

**Các phần cần sửa database để quản lý theo Công ty:**

- Dữ liệu quản trị theo công ty trên hàng hoá: Tab dữ liệu quản trị
- Bộ trạng thái hàng hoá
- Giá bán, giá vốn
- update toàn bộ các luồng sử dụng tới 3 phần trên để chuyển sang lấy số liệu ở bảng dữ liệu theo công ty

**Tổng hợp các công việc xử lý phần hàng hoá cần hoàn thành:**

- Chuyển toàn bộ danh mục liên quan hàng hoá sang Phân hệ "Danh mục dùng chung"
- Chuyển các danh mục phân loại xe
- Xây dựng các chức năng xâu dựng hàng hoá như phân tích ở trên
- Chuyển quản lý hàng tạm tương ứng (có thể xử lý sau khi xong các việc trên)
- Xử lý các ảnh hưởng liên quan việc thay đổi database và logic quản lý (Phần này khó nhất).

**Việc còn đang tính toán lại:**

- Logic mới này khi nhập xong thông tin hàng hoá =>> mã hàng chuyển sang màn hình chờ tính giá =>> Như vậy có bị trùng với luồng hỏi giá hay không?
