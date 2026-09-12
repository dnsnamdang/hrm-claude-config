# Testcase — Danh mục Lĩnh vực Công ty kinh doanh

| Thông tin | Chi tiết |
|---|---|
| Module | Dự án & Giao việc (Assign) |
| Màn hình | Danh mục › Lĩnh vực Công ty kinh doanh (`/assign/internal-business-scopes`) |
| SRS | `docs/srs/linh-vuc-cong-ty-kinh-doanh.md` |
| File Excel | `docs/srs/linh-vuc-cong-ty-kinh-doanh-testcases.xlsx` |
| Sinh bởi | `docs/srs/generate_testcase_lvctkd.py` |
| Tổng số testcase | **201** |



## I. MENU & PHÂN QUYỀN

| TC ID | Chức năng | Ưu tiên | Tiền điều kiện | Bước thực hiện | Test Data | Kết quả mong đợi |
|---|---|:---:|---|---|---|---|
| LVCTKD_001.001 | Hiển thị mục menu với quyền Quản lý | P0 | User có quyền "Quản lý danh mục lĩnh vực Công ty kinh doanh" | 1. Đăng nhập<br>2. Mở menu trái<br>3. Vào nhóm "Danh mục" |  | Thấy mục "Lĩnh vực Công ty kinh doanh"<br>Mục nằm NGAY TRƯỚC mục "Nhóm ngành"<br>Click vào điều hướng tới /assign/internal-business-scopes |
| LVCTKD_001.002 | Hiển thị mục menu với quyền Xem | P0 | User CHỈ có quyền "Xem danh mục lĩnh vực Công ty kinh doanh" | 1. Đăng nhập<br>2. Mở nhóm "Danh mục" |  | Vẫn thấy mục "Lĩnh vực Công ty kinh doanh"<br>Vào được màn danh sách |
| LVCTKD_001.003 | Ẩn mục menu khi KHÔNG có quyền nào | P0 | User không có cả 2 quyền (dùng tài khoản fixture e2e_nocatalog@test.local) | 1. Đăng nhập<br>2. Mở nhóm "Danh mục" |  | KHÔNG thấy mục "Lĩnh vực Công ty kinh doanh" trong menu |
| LVCTKD_001.004 | Chặn truy cập trực tiếp URL khi không có quyền | P0 | User không có cả 2 quyền | 1. Gõ thẳng URL /assign/internal-business-scopes lên thanh địa chỉ<br>2. Enter |  | API danh sách trả 403<br>Bảng rỗng<br>KHÔNG hiện toast lỗi (tránh nhiễu) |
| LVCTKD_001.005 | Ẩn nút Tạo mới / Import với quyền Xem | P0 | User CHỈ có quyền Xem | 1. Vào màn danh sách<br>2. Quan sát khu vực nút phía trên bảng |  | KHÔNG có nút "Tạo mới"<br>KHÔNG có nút "Import Excel"<br>VẪN có nút "Xuất Excel"<br>Nút bị ẩn HẲN, không phải disable |
| LVCTKD_001.006 | Ẩn toàn bộ nút Hành động với quyền Xem | P0 | User CHỈ có quyền Xem, danh sách có ≥ 1 bản ghi Hoạt động | 1. Vào màn danh sách<br>2. Quan sát cột "Hành động" |  | Cột Hành động trống hoàn toàn: không có Sửa / Khoá / Mở khoá / Xoá |
| LVCTKD_001.007 | Quyền Xem vẫn mở được modal Xem chi tiết | P1 | User CHỈ có quyền Xem | 1. Vào màn danh sách<br>2. Click vào giá trị cột "Mã" |  | Mở modal "Xem chi tiết lĩnh vực Công ty kinh doanh"<br>Mọi ô chỉ đọc<br>Footer chỉ có nút Đóng |
| LVCTKD_001.008 | Cờ quyền fail-closed khi request quyền lỗi | P1 | Giả lập API quyền trả lỗi / chậm | 1. Vào màn danh sách khi store quyền chưa có dữ liệu<br>2. Quan sát nút |  | canManage = false → các nút quản lý bị ẩn<br>Không có trường hợp nút hiện nhầm rồi mất |
| LVCTKD_001.009 | Thu hồi quyền giữa chừng | P2 | User đang mở màn, admin gỡ quyền ở tab khác | 1. Ở màn danh sách<br>2. Admin gỡ quyền<br>3. Bấm Tìm kiếm để gọi lại API |  | API trả 403<br>Bảng rỗng<br>KHÔNG hiện toast lỗi |

## II. MÀN DANH SÁCH — HIỂN THỊ

| TC ID | Chức năng | Ưu tiên | Tiền điều kiện | Bước thực hiện | Test Data | Kết quả mong đợi |
|---|---|:---:|---|---|---|---|
| LVCTKD_002.001 | Hiển thị đủ 9 cột đúng thứ tự | P0 | User có quyền Quản lý, có ≥ 1 bản ghi | 1. Vào /assign/internal-business-scopes<br>2. Quan sát header bảng |  | Đúng 9 cột theo thứ tự: STT · Mã · Tên lĩnh vực Công ty kinh doanh · Người tạo · Ngày tạo · Người cập nhật · Ngày cập nhật · Trạng thái · Hành động<br>Cột Hành động ở CUỐI cùng |
| LVCTKD_002.002 | Tiêu đề trang & tiêu đề bảng | P1 | Đang ở màn danh sách | 1. Quan sát tiêu đề trang (tab trình duyệt) và tiêu đề bảng |  | Tab trình duyệt: "Danh sách lĩnh vực Công ty kinh doanh"<br>Tiêu đề bảng: "Danh sách lĩnh vực Công ty kinh doanh" |
| LVCTKD_002.003 | Cột Mã là link mở modal Xem | P0 | Có ≥ 1 bản ghi | 1. Click vào giá trị cột "Mã" của dòng bất kỳ | LVKDNB.OTO | Mở modal "Xem chi tiết lĩnh vực Công ty kinh doanh" đúng bản ghi vừa click<br>KHÔNG có nút "Xem" riêng ở cột Hành động |
| LVCTKD_002.004 | Badge trạng thái Hoạt động | P0 | Có bản ghi status = 1 | 1. Quan sát cột Trạng thái |  | Hiện badge "Hoạt động" (variant brand — màu chủ đạo) |
| LVCTKD_002.005 | Badge trạng thái Khoá | P0 | Có bản ghi status = 2 | 1. Quan sát cột Trạng thái |  | Hiện badge "Khoá" (variant required — màu đỏ) |
| LVCTKD_002.006 | Định dạng ngày KHÔNG có giây | P0 | Có ≥ 1 bản ghi | 1. Quan sát cột Ngày tạo, Ngày cập nhật |  | Hiển thị dạng dd/mm/yyyy HH:mm (VD 22/08/2026 14:30)<br>KHÔNG hiển thị giây |
| LVCTKD_002.007 | Cột Người tạo/Người cập nhật chỉ hiện TÊN | P0 | Có ≥ 1 bản ghi | 1. Quan sát cột Người tạo và Người cập nhật |  | Chỉ hiện họ tên nhân viên<br>KHÔNG kèm mã nhân viên, không kèm email |
| LVCTKD_002.008 | Ô trống hiển thị dấu gạch ngang | P1 | Bản ghi có updated_by = NULL (VD tạo bằng seeder) | 1. Quan sát cột Người cập nhật của bản ghi đó |  | Hiện ký tự "—" thay vì để trống |
| LVCTKD_002.009 | Chữ trong ô để thường, không in đậm | P2 | Có ≥ 1 bản ghi | 1. Quan sát cột Tên |  | Chữ hiển thị thường (font-weight normal), không bold |
| LVCTKD_002.010 | Bảng loading ngay khi vào màn | P1 | Mạng chậm (throttle Slow 3G) | 1. Vào màn danh sách<br>2. Quan sát ngay lập tức |  | Spinner hiện NGAY, không chờ request quyền xong<br>Request danh sách là request bắn ĐẦU TIÊN |
| LVCTKD_002.011 | Thông báo khi không có dữ liệu | P1 | Bộ lọc không khớp bản ghi nào | 1. Nhập từ khoá không tồn tại "zzzzzz"<br>2. Bấm Tìm kiếm | zzzzzz | Bảng hiện "Không có dữ liệu phù hợp bộ lọc."<br>Không có dòng dữ liệu nào |
| LVCTKD_002.012 | Toast khi API danh sách lỗi 500 | P2 | Giả lập API trả 500 | 1. Vào màn danh sách |  | Toast đỏ "Lỗi khi tải dữ liệu"<br>Bảng rỗng, spinner tắt |
| LVCTKD_002.013 | Sắp xếp mặc định id DESC | P0 | Có ≥ 3 bản ghi tạo ở các thời điểm khác nhau | 1. Vào màn danh sách (chưa lọc, chưa sort) |  | Bản ghi tạo MỚI NHẤT nằm ở dòng đầu tiên |

## III. TÌM KIẾM & LỌC

| TC ID | Chức năng | Ưu tiên | Tiền điều kiện | Bước thực hiện | Test Data | Kết quả mong đợi |
|---|---|:---:|---|---|---|---|
| LVCTKD_003.001 | Tìm nhanh theo Mã | P0 | Có bản ghi LVKDNB.OTO — Ô tô | 1. Nhập "OTO" vào ô tìm nhanh<br>2. Bấm Tìm kiếm | OTO | Danh sách chỉ còn bản ghi có mã chứa "OTO"<br>Về trang 1 |
| LVCTKD_003.002 | Tìm nhanh theo Tên | P0 | Có bản ghi tên "Ô tô" | 1. Nhập "Ô tô"<br>2. Bấm Tìm kiếm | Ô tô | Trả về bản ghi có tên chứa "Ô tô" |
| LVCTKD_003.003 | Tìm nhanh theo TÊN NGƯỜI TẠO | P0 | Bản ghi do "Nguyễn Văn A" tạo | 1. Nhập "Nguyễn Văn A"<br>2. Bấm Tìm kiếm | Nguyễn Văn A | Trả về các bản ghi do người đó tạo<br>(BE tìm qua employee_infos.fullname bằng EXISTS) |
| LVCTKD_003.004 | Placeholder ô tìm nhanh | P2 | Đang ở màn danh sách | 1. Quan sát ô tìm nhanh |  | Placeholder: "Tìm theo mã, tên lĩnh vực Công ty kinh doanh, người tạo" |
| LVCTKD_003.005 | Ô tìm nhanh KHÔNG auto-search | P1 | Đang ở màn danh sách | 1. Gõ ký tự vào ô tìm nhanh<br>2. Đợi 3 giây, KHÔNG bấm Tìm kiếm<br>3. Quan sát Network |  | KHÔNG có request danh sách nào được gọi<br>Danh sách giữ nguyên |
| LVCTKD_003.006 | Tìm kiếm bằng phím Enter | P1 | Đang ở màn danh sách | 1. Gõ từ khoá vào ô tìm nhanh<br>2. Nhấn Enter | OTO | Gọi API tìm kiếm, kết quả lọc đúng |
| LVCTKD_003.007 | Tìm không dấu vẫn khớp | P1 | Có bản ghi tên "Ô tô" | 1. Nhập "o to"<br>2. Bấm Tìm kiếm | o to | Vẫn khớp bản ghi "Ô tô" (collation _ci bỏ dấu) |
| LVCTKD_003.008 | Sắp theo độ khớp — khớp đúng dấu lên trước | P1 | Có 2 bản ghi: "Ô tô" và "Oto điện" | 1. Nhập "Ô tô"<br>2. Bấm Tìm kiếm<br>3. Quan sát thứ tự | Ô tô | Bản ghi khớp ĐÚNG DẤU xếp TRƯỚC bản ghi chỉ khớp nhờ bỏ dấu |
| LVCTKD_003.009 | Sắp theo độ khớp — trùng khít lên đầu | P1 | Có bản ghi "Ô tô" và "Ô tô điện" và "Phụ tùng Ô tô" | 1. Nhập "Ô tô"<br>2. Bấm Tìm kiếm | Ô tô | Thứ tự: trùng khít → bắt đầu bằng → khớp đầu từ → chỉ chứa<br>Cùng mức thì tên NGẮN hơn lên trước |
| LVCTKD_003.010 | Không sắp độ khớp khi từ khoá < 2 ký tự | P2 | Có nhiều bản ghi | 1. Nhập "O" (1 ký tự)<br>2. Bấm Tìm kiếm | O | Kết quả sắp theo id DESC (không áp thuật toán độ khớp) |
| LVCTKD_003.011 | Đã bấm sort cột thì KHÔNG sắp theo độ khớp | P2 | Có nhiều bản ghi | 1. Bấm sort cột Mã tăng dần<br>2. Nhập từ khoá<br>3. Bấm Tìm kiếm | OTO | Kết quả sắp theo cột Mã tăng dần, không theo độ khớp |
| LVCTKD_003.012 | Mở panel lọc nâng cao | P0 | Đang ở màn danh sách (panel mặc định thu gọn) | 1. Bấm nút mở rộng bộ lọc |  | Hiện đủ 7 ô: Mã · Tên lĩnh vực Công ty kinh doanh · Trạng thái · Người tạo · Người cập nhật · Cập nhật từ · Cập nhật đến |
| LVCTKD_003.013 | Lọc theo Mã (auto-search) | P0 | Panel nâng cao đang mở | 1. Nhập "LVKDNB.O" vào ô Mã<br>2. KHÔNG bấm nút nào | LVKDNB.O | Danh sách TỰ nạp lại (auto-search)<br>Về trang 1<br>Chỉ còn bản ghi có mã chứa chuỗi đó |
| LVCTKD_003.014 | Lọc theo Tên (auto-search) | P0 | Panel nâng cao đang mở | 1. Nhập "Ô tô" vào ô Tên | Ô tô | Danh sách tự lọc theo tên |
| LVCTKD_003.015 | Lọc theo Trạng thái = Hoạt động | P0 | Có cả bản ghi Hoạt động và Khoá | 1. Chọn Trạng thái = "Hoạt động" | Hoạt động | Chỉ hiện bản ghi status = 1 |
| LVCTKD_003.016 | Lọc theo Trạng thái = Khoá | P0 | Có cả bản ghi Hoạt động và Khoá | 1. Chọn Trạng thái = "Khoá" | Khoá | Chỉ hiện bản ghi status = 2 |
| LVCTKD_003.017 | Xoá điều kiện Trạng thái | P1 | Đang lọc Trạng thái = Khoá | 1. Bấm dấu X trên ô Trạng thái |  | Điều kiện được gỡ, danh sách nạp lại đầy đủ |
| LVCTKD_003.018 | Lọc theo Người tạo | P0 | Panel nâng cao đang mở | 1. Chọn 1 nhân viên ở ô Người tạo | Nguyễn Văn A | Chỉ hiện bản ghi do nhân viên đó tạo |
| LVCTKD_003.019 | Lọc theo Người cập nhật | P1 | Panel nâng cao đang mở | 1. Chọn 1 nhân viên ở ô Người cập nhật | Nguyễn Văn A | Chỉ hiện bản ghi do nhân viên đó cập nhật gần nhất |
| LVCTKD_003.020 | Lọc khoảng ngày cập nhật | P0 | Có bản ghi cập nhật ở nhiều ngày khác nhau | 1. Chọn "Cập nhật từ" = 01/08/2026<br>2. Chọn "Cập nhật đến" = 22/08/2026 | từ 01/08/2026 đến 22/08/2026 | Chỉ hiện bản ghi có updated_at nằm trong khoảng (so theo NGÀY, bao gồm 2 đầu mút) |
| LVCTKD_003.021 | Lọc chỉ có "Cập nhật từ" | P1 | Panel nâng cao đang mở | 1. Chọn "Cập nhật từ" = 22/08/2026, để trống ô đến |  | Hiện bản ghi cập nhật từ ngày đó trở về sau |
| LVCTKD_003.022 | Kết hợp nhiều điều kiện lọc | P0 | Panel nâng cao đang mở | 1. Nhập Tên = "Ô"<br>2. Chọn Trạng thái = Hoạt động<br>3. Chọn Người tạo |  | Các điều kiện áp ĐỒNG THỜI (AND), kết quả thoả cả 3 |
| LVCTKD_003.023 | Nút Làm mới xoá hết điều kiện VÀ nạp lại | P0 | Đang có từ khoá tìm nhanh + vài ô lọc nâng cao | 1. Bấm nút "Làm mới"<br>2. Quan sát Network + bảng |  | Mọi ô lọc + ô tìm nhanh về rỗng<br>Về trang 1<br>Gọi API danh sách ĐÚNG 1 LẦN (không 0 lần, không 2 lần)<br>Bảng hiện lại đầy đủ dữ liệu |
| LVCTKD_003.024 | Lọc xong về trang 1 | P1 | Đang ở trang 3 của danh sách | 1. Nhập điều kiện lọc bất kỳ |  | Danh sách nhảy về trang 1 |

## IV. SẮP XẾP & PHÂN TRANG

| TC ID | Chức năng | Ưu tiên | Tiền điều kiện | Bước thực hiện | Test Data | Kết quả mong đợi |
|---|---|:---:|---|---|---|---|
| LVCTKD_004.001 | Sort theo Mã tăng/giảm | P0 | Có ≥ 3 bản ghi | 1. Click header cột "Mã" (lần 1)<br>2. Click lần 2 |  | Lần 1: sắp tăng dần theo mã<br>Lần 2: sắp giảm dần<br>Icon sort đổi chiều tương ứng |
| LVCTKD_004.002 | Sort theo Tên | P0 | Có ≥ 3 bản ghi | 1. Click header cột "Tên lĩnh vực Công ty kinh doanh" |  | Danh sách sắp theo tên A→Z |
| LVCTKD_004.003 | Sort theo Ngày tạo | P1 | Có ≥ 3 bản ghi | 1. Click header cột "Ngày tạo" |  | Danh sách sắp theo created_at |
| LVCTKD_004.004 | Sort theo Ngày cập nhật | P1 | Có ≥ 3 bản ghi | 1. Click header cột "Ngày cập nhật" |  | Danh sách sắp theo updated_at |
| LVCTKD_004.005 | Các cột KHÔNG cho sort | P2 | Có ≥ 1 bản ghi | 1. Thử click header STT, Người tạo, Người cập nhật, Trạng thái, Hành động |  | Không có icon sort, click không đổi thứ tự |
| LVCTKD_004.006 | Sort bằng tham số ngoài whitelist | P1 | Có ≥ 2 bản ghi | 1. Gọi API với sort_by=abc (dùng Postman hoặc sửa URL) | sort_by=abc | Bỏ qua tham số lạ, kết quả rơi về id DESC, KHÔNG lỗi 500 |
| LVCTKD_004.007 | Đổi số dòng/trang | P0 | Có > 10 bản ghi | 1. Đổi page size từ 10 sang 25 | 25 | Bảng hiện tối đa 25 dòng<br>Về trang 1 |
| LVCTKD_004.008 | Chuyển trang | P0 | Có > 10 bản ghi | 1. Bấm sang trang 2 |  | Hiện tập bản ghi kế tiếp<br>Cột STT đánh số tiếp nối (11, 12, ...) |
| LVCTKD_004.009 | STT đánh số đúng theo trang | P1 | Có > 10 bản ghi, page size = 10 | 1. Sang trang 2<br>2. Quan sát cột STT dòng đầu |  | STT dòng đầu trang 2 = 11 (không reset về 1) |
| LVCTKD_004.010 | Race condition khi bấm nhanh 2 lượt lọc | P2 | Mạng chậm | 1. Nhập điều kiện A<br>2. Ngay lập tức nhập điều kiện B<br>3. Đợi cả 2 response về |  | Bảng hiển thị kết quả của lượt gọi CUỐI CÙNG (B)<br>Không bị response cũ ghi đè (loadSeq) |

## V. TẠO MỚI — VALIDATE Ô MÃ

| TC ID | Chức năng | Ưu tiên | Tiền điều kiện | Bước thực hiện | Test Data | Kết quả mong đợi |
|---|---|:---:|---|---|---|---|
| LVCTKD_005.001 | Mở modal Tạo mới | P0 | User có quyền Quản lý | 1. Bấm nút "Tạo mới" |  | Mở modal tiêu đề "Tạo mới lĩnh vực Công ty kinh doanh"<br>Ô Mã đã có sẵn tiền tố "LVKDNB."<br>Ô Tên rỗng<br>Trạng thái mặc định "Hoạt động"<br>Footer: Lưu · Lưu & Tiếp tục · Đóng |
| LVCTKD_005.002 | Bố cục 1 hàng đủ 12 cột | P2 | Modal Tạo mới đang mở | 1. Quan sát bố cục form |  | 1 hàng gồm 3 ô: Mã (3 cột) · Tên (6 cột) · Trạng thái (3 cột)<br>Không có ô nào nằm lẻ 1 dòng |
| LVCTKD_005.003 | Tiền tố LVKDNB. không xoá được | P0 | Modal Tạo mới đang mở | 1. Click vào ô Mã<br>2. Nhấn Backspace nhiều lần |  | Tiền tố "LVKDNB." luôn còn nguyên, không xoá được |
| LVCTKD_005.004 | Giới hạn hậu tố 4 ký tự trên UI | P0 | Modal Tạo mới đang mở | 1. Gõ "ABCDEFGH" vào phần hậu tố | ABCDEFGH | Ô chỉ nhận 4 ký tự đầu "ABCD" (maxlength = 4) |
| LVCTKD_005.005 | Để trống hậu tố → báo Bắt buộc phải nhập | P0 | Modal Tạo mới đang mở | 1. Để ô Mã chỉ có "LVKDNB."<br>2. Nhập Tên hợp lệ<br>3. Bấm Lưu | LVKDNB. | Lỗi dưới ô Mã: "Bắt buộc phải nhập."<br>Ô Mã viền đỏ<br>KHÔNG gọi API<br>KHÔNG hiện câu lỗi định dạng |
| LVCTKD_005.006 | Hậu tố có ký tự đặc biệt | P0 | Modal Tạo mới đang mở | 1. Nhập hậu tố "A@#"<br>2. Nhập Tên hợp lệ<br>3. Bấm Lưu | LVKDNB.A@# | Lỗi: "Hậu tố tối đa 4 ký tự, chỉ gồm chữ không dấu (A-Z), số (0-9) và dấu gạch dưới (_)." |
| LVCTKD_005.007 | Hậu tố có dấu tiếng Việt | P1 | Modal Tạo mới đang mở | 1. Nhập hậu tố "Ôtô"<br>2. Bấm Lưu | LVKDNB.Ôtô | Báo lỗi định dạng, không cho lưu |
| LVCTKD_005.008 | Hậu tố chấp nhận dấu gạch dưới | P1 | Modal Tạo mới đang mở | 1. Nhập hậu tố "A_1"<br>2. Nhập Tên hợp lệ<br>3. Bấm Lưu | LVKDNB.A_1 | Lưu thành công, mã trong danh sách là LVKDNB.A_1 |
| LVCTKD_005.009 | Hậu tố toàn số | P1 | Modal Tạo mới đang mở | 1. Nhập hậu tố "1234"<br>2. Nhập Tên hợp lệ<br>3. Bấm Lưu | LVKDNB.1234 | Lưu thành công |
| LVCTKD_005.010 | Hậu tố chữ thường tự viết HOA | P0 | Modal Tạo mới đang mở | 1. Nhập hậu tố "oto"<br>2. Nhập Tên "Ô tô test"<br>3. Bấm Lưu<br>4. Xem lại danh sách | oto | Bản ghi lưu với mã "LVKDNB.OTO" (viết HOA) |
| LVCTKD_005.011 | Hậu tố 1 ký tự (biên dưới) | P1 | Modal Tạo mới đang mở | 1. Nhập hậu tố "A"<br>2. Nhập Tên hợp lệ<br>3. Bấm Lưu | LVKDNB.A | Lưu thành công (1 ký tự là hợp lệ) |
| LVCTKD_005.012 | Hậu tố 4 ký tự (biên trên) | P1 | Modal Tạo mới đang mở | 1. Nhập hậu tố "ABCD"<br>2. Nhập Tên hợp lệ<br>3. Bấm Lưu | LVKDNB.ABCD | Lưu thành công |
| LVCTKD_005.013 | Mã trùng bản ghi đã có | P0 | Đã tồn tại LVKDNB.OTO | 1. Tạo mới với mã LVKDNB.OTO<br>2. Nhập Tên khác<br>3. Bấm Lưu | LVKDNB.OTO | API trả 422<br>Lỗi dưới ô Mã: "Mã lĩnh vực Công ty kinh doanh đã tồn tại"<br>Modal KHÔNG đóng<br>Toast đỏ "Bạn chưa nhập đầy đủ thông tin" |
| LVCTKD_005.014 | Mã trùng khác hoa thường | P1 | Đã tồn tại LVKDNB.OTO | 1. Tạo mới với hậu tố "oto"<br>2. Bấm Lưu | LVKDNB.oto | Vẫn báo trùng (do BE tự upper trước khi kiểm) |
| LVCTKD_005.015 | Khoảng trắng ngay sau dấu chấm bị loại | P2 | Modal Tạo mới đang mở (hoặc gọi API trực tiếp) | 1. Gửi code = "LVKDNB. OTO" | LVKDNB. OTO | BE chuẩn hoá thành LVKDNB.OTO trước khi validate |

## VI. TẠO MỚI — VALIDATE Ô TÊN

| TC ID | Chức năng | Ưu tiên | Tiền điều kiện | Bước thực hiện | Test Data | Kết quả mong đợi |
|---|---|:---:|---|---|---|---|
| LVCTKD_006.001 | Để trống Tên | P0 | Modal Tạo mới đang mở | 1. Nhập Mã hợp lệ<br>2. Để trống Tên<br>3. Bấm Lưu |  | Lỗi dưới ô Tên: "Bắt buộc phải nhập"<br>Ô Tên viền đỏ<br>KHÔNG gọi API |
| LVCTKD_006.002 | Tên chỉ gồm khoảng trắng | P1 | Modal Tạo mới đang mở | 1. Nhập Mã hợp lệ<br>2. Nhập Tên = "   " (3 dấu cách)<br>3. Bấm Lưu | "   " | BE trim → rỗng → báo "Bắt buộc phải nhập" |
| LVCTKD_006.003 | Tên 255 ký tự (biên trên) | P1 | Modal Tạo mới đang mở | 1. Nhập Tên đúng 255 ký tự<br>2. Bấm Lưu | Chuỗi 255 ký tự | Lưu thành công |
| LVCTKD_006.004 | Tên 256 ký tự (vượt biên) | P0 | Modal Tạo mới đang mở | 1. Nhập Tên 256 ký tự<br>2. Bấm Lưu | Chuỗi 256 ký tự | Lỗi: "Tên lĩnh vực Công ty kinh doanh tối đa 255 ký tự" |
| LVCTKD_006.005 | Tên chứa dấu phẩy | P0 | Modal Tạo mới đang mở | 1. Nhập Tên = "Ô tô, xe máy"<br>2. Bấm Lưu | Ô tô, xe máy | Lỗi: "Tên không được chứa ký tự dấu phẩy (,) và dấu hai chấm (:)" |
| LVCTKD_006.006 | Tên chứa dấu hai chấm | P0 | Modal Tạo mới đang mở | 1. Nhập Tên = "Ô tô: điện"<br>2. Bấm Lưu | Ô tô: điện | Lỗi: "Tên không được chứa ký tự dấu phẩy (,) và dấu hai chấm (:)" |
| LVCTKD_006.007 | Tên trùng bản ghi đã có | P0 | Đã tồn tại bản ghi tên "Ô tô" | 1. Tạo mới với Mã khác nhưng Tên = "Ô tô"<br>2. Bấm Lưu | Ô tô | API trả 422<br>Lỗi dưới ô Tên: "Tên lĩnh vực Công ty kinh doanh đã tồn tại"<br>Modal KHÔNG đóng |
| LVCTKD_006.008 | Tên trùng khác hoa thường | P1 | Đã tồn tại bản ghi tên "Ô tô" | 1. Tạo mới với Tên = "ô tô"<br>2. Bấm Lưu | ô tô | Vẫn báo trùng (MySQL collation _ci) |
| LVCTKD_006.009 | Tên có khoảng trắng đầu/cuối bị trim | P1 | Modal Tạo mới đang mở | 1. Nhập Tên = "  Ô tô mới  "<br>2. Bấm Lưu<br>3. Xem lại danh sách | "  Ô tô mới  " | Bản ghi lưu với tên "Ô tô mới" (đã trim 2 đầu) |
| LVCTKD_006.010 | Tên có ký tự Unicode / emoji | P2 | Modal Tạo mới đang mở | 1. Nhập Tên = "Ô tô 🚗"<br>2. Bấm Lưu | Ô tô 🚗 | Lưu được (không có rule cấm), hiển thị đúng ở danh sách |

## VII. TẠO MỚI — VALIDATE ĐỒNG THỜI & LƯU

| TC ID | Chức năng | Ưu tiên | Tiền điều kiện | Bước thực hiện | Test Data | Kết quả mong đợi |
|---|---|:---:|---|---|---|---|
| LVCTKD_007.001 | Bấm Lưu khi form TRỐNG → 2 lỗi đồng thời | P0 | Modal Tạo mới vừa mở, chưa nhập gì | 1. Bấm Lưu ngay |  | HIỆN CÙNG LÚC 2 lỗi:<br>- Dưới ô Mã: "Bắt buộc phải nhập."<br>- Dưới ô Tên: "Bắt buộc phải nhập"<br>CẢ 2 ô đều viền đỏ<br>Con trỏ focus vào ô Mã (ô lỗi đầu tiên)<br>KHÔNG gọi API |
| LVCTKD_007.002 | Sai cả Mã lẫn Tên → báo cùng lúc | P0 | Modal Tạo mới đang mở | 1. Nhập Mã = "LVKDNB.@@"<br>2. Nhập Tên = "Ô tô, xe"<br>3. Bấm Lưu | LVKDNB.@@ / Ô tô, xe | Hiện đồng thời lỗi định dạng Mã + lỗi ký tự cấm ở Tên<br>Không phải sửa xong ô này mới lòi lỗi ô kia |
| LVCTKD_007.003 | Focus ô lỗi đầu tiên khi chỉ Tên sai | P1 | Modal Tạo mới đang mở | 1. Nhập Mã hợp lệ<br>2. Để trống Tên<br>3. Bấm Lưu |  | Focus nhảy vào ô Tên |
| LVCTKD_007.004 | Lỗi BE 422 tự mất khi sửa lại ô đó | P0 | Vừa bị lỗi 422 "Tên đã tồn tại" | 1. Sửa lại ô Tên thành giá trị khác<br>2. Quan sát |  | Lỗi 422 cũ dưới ô Tên BIẾN MẤT ngay khi gõ<br>Không che mất validate realtime |
| LVCTKD_007.005 | Lỗi BE hiện đúng dưới từng ô | P0 | Đã có LVKDNB.OTO tên "Ô tô" | 1. Tạo mới với Mã = LVKDNB.OTO và Tên = "Ô tô"<br>2. Bấm Lưu | LVKDNB.OTO / Ô tô | Hiện ĐỒNG THỜI 2 lỗi 422: "Mã ... đã tồn tại" dưới ô Mã, "Tên ... đã tồn tại" dưới ô Tên |
| LVCTKD_007.006 | Lưu thành công | P0 | Modal Tạo mới đang mở, dữ liệu hợp lệ chưa trùng | 1. Nhập Mã = LVKDNB.TEST<br>2. Nhập Tên = "Lĩnh vực test"<br>3. Bấm Lưu | LVKDNB.TEST / Lĩnh vực test | Toast xanh "Thêm mới thành công"<br>Modal ĐÓNG<br>Danh sách nạp lại, bản ghi mới ở ĐẦU danh sách<br>Trạng thái = Hoạt động |
| LVCTKD_007.007 | Metadata tự ghi khi tạo | P0 | Vừa tạo bản ghi mới | 1. Quan sát cột Người tạo / Ngày tạo của bản ghi vừa tạo<br>2. Kiểm SQL: select code, created_by, updated_by from internal_business_scopes |  | Người tạo = tên tài khoản đang đăng nhập<br>Ngày tạo = thời điểm hiện tại, format dd/mm/yyyy HH:mm<br>created_by và updated_by KHÁC NULL |
| LVCTKD_007.008 | Chọn Trạng thái = Khoá khi tạo mới | P1 | Modal Tạo mới đang mở | 1. Nhập Mã, Tên hợp lệ<br>2. Đổi Trạng thái sang "Khoá"<br>3. Bấm Lưu | status = Khoá | Bản ghi tạo ra với trạng thái Khoá<br>Dòng đó chỉ còn nút "Mở khoá" |
| LVCTKD_007.009 | Lưu & Tiếp tục giữ modal mở | P0 | Modal Tạo mới đang mở, dữ liệu hợp lệ | 1. Nhập Mã + Tên<br>2. Bấm "Lưu & Tiếp tục" |  | Toast "Thêm mới thành công"<br>Modal VẪN MỞ<br>Form reset về trống (Mã chỉ còn tiền tố, Tên rỗng, Trạng thái Hoạt động)<br>Danh sách nền đã nạp lại |
| LVCTKD_007.010 | Nút Lưu & Tiếp tục chỉ có ở chế độ Tạo | P1 | Có bản ghi để sửa | 1. Mở modal Sửa<br>2. Quan sát footer |  | Footer chỉ có "Lưu" và "Đóng"<br>KHÔNG có "Lưu & Tiếp tục" |
| LVCTKD_007.011 | Đóng modal không lưu | P1 | Modal Tạo mới, đã nhập dữ liệu | 1. Bấm "Đóng"<br>2. Mở lại modal Tạo mới |  | Modal đóng, KHÔNG tạo bản ghi<br>Mở lại thì form đã reset sạch, không còn dữ liệu cũ và lỗi cũ |
| LVCTKD_007.012 | Đóng modal bằng dấu X | P2 | Modal Tạo mới đang mở | 1. Bấm dấu X góc phải header |  | Modal đóng, không tạo bản ghi, form được reset |
| LVCTKD_007.013 | Chặn double-submit | P1 | Modal Tạo mới, dữ liệu hợp lệ, mạng chậm | 1. Bấm Lưu<br>2. Bấm Lưu lần 2 ngay lập tức |  | Nút Lưu bị disable trong lúc đang gửi<br>Chỉ tạo ra ĐÚNG 1 bản ghi |

## VIII. SỬA

| TC ID | Chức năng | Ưu tiên | Tiền điều kiện | Bước thực hiện | Test Data | Kết quả mong đợi |
|---|---|:---:|---|---|---|---|
| LVCTKD_008.001 | Mở modal Sửa | P0 | Có bản ghi Hoạt động, user có quyền Quản lý | 1. Bấm biểu tượng Sửa trên dòng |  | Gọi GET /{id} nạp dữ liệu mới nhất<br>Modal tiêu đề "Sửa lĩnh vực Công ty kinh doanh"<br>Mã + Tên + Trạng thái điền đúng giá trị hiện tại |
| LVCTKD_008.002 | Header hiện chip người/ngày cập nhật | P1 | Bản ghi đã từng được cập nhật | 1. Mở modal Sửa<br>2. Quan sát header |  | Header hiện chip metadata: người cập nhật + ngày cập nhật gần nhất |
| LVCTKD_008.003 | Cuối body hiện Người tạo / Ngày tạo | P1 | Bản ghi bất kỳ | 1. Mở modal Sửa<br>2. Cuộn xuống cuối body |  | Hiện block metadata: Người tạo + Ngày tạo<br>KHÔNG có ô nhập cho 2 trường này |
| LVCTKD_008.004 | Sửa Tên thành công | P0 | Bản ghi Hoạt động | 1. Mở modal Sửa<br>2. Đổi Tên thành "Ô tô sửa"<br>3. Bấm Lưu | Ô tô sửa | Toast "Cập nhật thành công"<br>Modal đóng<br>Danh sách hiện tên mới |
| LVCTKD_008.005 | Sửa Mã thành công | P0 | Bản ghi Hoạt động | 1. Mở modal Sửa<br>2. Đổi hậu tố mã<br>3. Bấm Lưu | LVKDNB.NEW | Lưu thành công, danh sách hiện mã mới |
| LVCTKD_008.006 | Metadata cập nhật sau khi Sửa | P0 | Bản ghi do user A tạo, đăng nhập bằng user B có quyền Quản lý | 1. Sửa bản ghi<br>2. Về danh sách quan sát cột Người/Ngày cập nhật<br>3. Kiểm SQL updated_by |  | Người cập nhật = user B<br>Ngày cập nhật = thời điểm vừa sửa<br>Người tạo VẪN là user A (không đổi) |
| LVCTKD_008.007 | Không cho sửa trùng Mã bản ghi khác | P0 | Có 2 bản ghi A và B | 1. Mở Sửa bản ghi A<br>2. Đổi mã A thành mã của B<br>3. Bấm Lưu |  | 422 "Mã lĩnh vực Công ty kinh doanh đã tồn tại", modal không đóng |
| LVCTKD_008.008 | Không cho sửa trùng Tên bản ghi khác | P0 | Có 2 bản ghi A và B | 1. Mở Sửa A<br>2. Đổi tên A thành tên của B<br>3. Bấm Lưu |  | 422 "Tên lĩnh vực Công ty kinh doanh đã tồn tại" |
| LVCTKD_008.009 | Giữ nguyên Mã/Tên của CHÍNH bản ghi đó | P0 | Bản ghi A | 1. Mở Sửa A<br>2. KHÔNG đổi gì, bấm Lưu |  | Lưu thành công, KHÔNG báo trùng với chính nó (unique có loại trừ id) |
| LVCTKD_008.010 | Nút Sửa bị ẩn khi bản ghi đã Khoá | P0 | Có bản ghi status = 2 | 1. Quan sát cột Hành động của dòng đã Khoá |  | KHÔNG có nút Sửa (is_can_edit = false)<br>Chỉ còn nút "Mở khoá" |
| LVCTKD_008.011 | Ô Trạng thái bị disable khi bản ghi đang Khoá | P1 | Bản ghi đang Khoá — mở qua modal Xem | 1. Bấm vào Mã của dòng đã Khoá |  | Ô Trạng thái bị disable, không đổi được |
| LVCTKD_008.012 | Sửa bản ghi vừa bị người khác KHOÁ (2 tab) | P0 | 2 tab cùng mở danh sách | 1. Tab A: khoá bản ghi X<br>2. Tab B: bấm Sửa X (danh sách chưa refresh) rồi Lưu |  | API trả 423<br>Toast "Bản ghi đang bị khoá, vui lòng mở khoá trước khi cập nhật." |
| LVCTKD_008.013 | Sửa bản ghi vừa bị người khác XOÁ (2 tab) | P0 | 2 tab cùng mở danh sách | 1. Tab A: xoá bản ghi X<br>2. Tab B: bấm Sửa X |  | API trả 404<br>Toast "Dữ liệu đã thay đổi, vui lòng tải lại"<br>Modal đóng lại |

## IX. XEM CHI TIẾT

| TC ID | Chức năng | Ưu tiên | Tiền điều kiện | Bước thực hiện | Test Data | Kết quả mong đợi |
|---|---|:---:|---|---|---|---|
| LVCTKD_009.001 | Mở modal Xem bằng cách bấm Mã | P0 | Có ≥ 1 bản ghi | 1. Click vào giá trị cột Mã |  | Modal tiêu đề "Xem chi tiết lĩnh vực Công ty kinh doanh" |
| LVCTKD_009.002 | Mọi ô ở chế độ chỉ đọc | P0 | Modal Xem đang mở | 1. Thử gõ vào ô Mã, ô Tên<br>2. Thử đổi ô Trạng thái |  | Cả 3 ô đều disable, không sửa được giá trị |
| LVCTKD_009.003 | Footer chỉ có nút Đóng | P0 | Modal Xem đang mở | 1. Quan sát footer |  | Chỉ có nút "Đóng"<br>KHÔNG có Lưu, KHÔNG có Lưu & Tiếp tục |
| LVCTKD_009.004 | Không có dấu * bắt buộc ở chế độ Xem | P2 | Modal Xem đang mở | 1. Quan sát nhãn ô Mã và ô Tên |  | Không hiện dấu * đỏ (Required chỉ hiện khi không phải chế độ Xem) |
| LVCTKD_009.005 | Xem bản ghi đã Khoá | P1 | Có bản ghi status = 2 | 1. Bấm vào Mã của bản ghi đã Khoá |  | Modal mở bình thường, Trạng thái hiện "Khoá" |

## X. KHOÁ / MỞ KHOÁ

| TC ID | Chức năng | Ưu tiên | Tiền điều kiện | Bước thực hiện | Test Data | Kết quả mong đợi |
|---|---|:---:|---|---|---|---|
| LVCTKD_010.001 | Khoá bản ghi thành công | P0 | Bản ghi Hoạt động, KHÔNG có Nhóm ngành nào trỏ tới | 1. Bấm biểu tượng Khoá<br>2. Xác nhận trên modal |  | Modal xác nhận hiện đúng câu: "Bạn có chắc muốn khoá lĩnh vực Công ty kinh doanh '<tên>'?"<br>Toast "Khoá thành công"<br>Badge đổi sang "Khoá" (đỏ) |
| LVCTKD_010.002 | Nút Sửa/Xoá biến mất sau khi Khoá | P0 | Vừa khoá 1 bản ghi | 1. Quan sát cột Hành động của dòng đó |  | Chỉ còn nút "Mở khoá"<br>Không còn Sửa, không còn Xoá |
| LVCTKD_010.003 | Mở khoá thành công | P0 | Bản ghi đang Khoá | 1. Bấm "Mở khoá"<br>2. Xác nhận |  | Tiêu đề modal: "Xác nhận mở khoá"<br>Toast "Mở khoá thành công"<br>Badge về "Hoạt động"<br>Nút Sửa/Xoá hiện lại |
| LVCTKD_010.004 | Huỷ modal xác nhận Khoá | P1 | Bản ghi Hoạt động | 1. Bấm Khoá<br>2. Bấm "Hủy" |  | Modal đóng, trạng thái bản ghi KHÔNG đổi |
| LVCTKD_010.005 | Khoá ghi lại Người/Ngày cập nhật | P0 | Bản ghi Hoạt động | 1. Ghi lại giá trị Người/Ngày cập nhật<br>2. Khoá bản ghi<br>3. Quan sát lại |  | Người cập nhật = user đang đăng nhập<br>Ngày cập nhật = thời điểm khoá<br>(khoá cũng tính là 1 lần cập nhật) |
| LVCTKD_010.006 | ẨN nút Khoá khi còn Nhóm ngành ĐANG HOẠT ĐỘNG | P0 | Có Nhóm ngành đang Hoạt động trỏ tới lĩnh vực này | 1. Quan sát cột Hành động của lĩnh vực đó |  | KHÔNG có nút Khoá (is_can_lock_update = false)<br>Vẫn có nút Sửa |
| LVCTKD_010.007 | CHO PHÉP khoá khi Nhóm ngành liên quan đều đã Khoá | P1 | Lĩnh vực có 1 Nhóm ngành, Nhóm ngành đó đang ở trạng thái Khoá | 1. Quan sát nút Khoá<br>2. Bấm Khoá + xác nhận |  | Nút Khoá HIỆN<br>Khoá thành công |
| LVCTKD_010.008 | Gọi thẳng API lock khi đang bị chặn | P0 | Lĩnh vực có Nhóm ngành đang Hoạt động | 1. Dùng Postman gọi GET /assign/internal-business-scopes/{id}/lock |  | HTTP 400<br>Message "Dữ liệu đang được sử dụng, vui lòng tải lại"<br>Trạng thái KHÔNG đổi |
| LVCTKD_010.009 | Mở khoá luôn được phép | P1 | Lĩnh vực đang Khoá và có nhiều Nhóm ngành trỏ tới | 1. Bấm Mở khoá + xác nhận |  | Mở khoá thành công (không có điều kiện chặn nào) |

## XI. XOÁ

| TC ID | Chức năng | Ưu tiên | Tiền điều kiện | Bước thực hiện | Test Data | Kết quả mong đợi |
|---|---|:---:|---|---|---|---|
| LVCTKD_011.001 | Xoá bản ghi thành công | P0 | Bản ghi Hoạt động, KHÔNG có Nhóm ngành nào trỏ tới | 1. Bấm biểu tượng Xoá<br>2. Xác nhận |  | Modal xác nhận: "Bạn có chắc muốn xóa lĩnh vực Công ty kinh doanh '<tên>'?"<br>Toast "Xoá thành công"<br>Bản ghi biến mất khỏi danh sách |
| LVCTKD_011.002 | Huỷ modal xác nhận Xoá | P1 | Bản ghi Hoạt động | 1. Bấm Xoá<br>2. Bấm "Hủy" |  | Modal đóng, bản ghi VẪN CÒN |
| LVCTKD_011.003 | ẨN nút Xoá khi có Nhóm ngành trỏ tới | P0 | Lĩnh vực có ≥ 1 Nhóm ngành (bất kể trạng thái) trỏ tới | 1. Quan sát cột Hành động |  | KHÔNG có nút Xoá (is_can_delete = false) |
| LVCTKD_011.004 | ẨN nút Xoá khi bản ghi đang Khoá | P0 | Bản ghi status = 2 | 1. Quan sát cột Hành động |  | KHÔNG có nút Xoá |
| LVCTKD_011.005 | Gọi thẳng API delete khi đang được sử dụng | P0 | Lĩnh vực có Nhóm ngành trỏ tới | 1. Postman: DELETE /assign/internal-business-scopes/{id} |  | HTTP 400 "Dữ liệu đang được sử dụng, vui lòng tải lại"<br>Bản ghi KHÔNG bị xoá |
| LVCTKD_011.006 | Gọi thẳng API delete bản ghi đang Khoá | P0 | Bản ghi status = 2, không có Nhóm ngành | 1. Postman: DELETE /assign/internal-business-scopes/{id} |  | HTTP 423 "Bản ghi đang bị khoá, vui lòng mở khoá trước khi xoá." |
| LVCTKD_011.007 | Xoá bản ghi đã bị người khác xoá | P1 | 2 tab cùng mở danh sách | 1. Tab A: xoá bản ghi X<br>2. Tab B: xoá lại X |  | 404 → toast "Dữ liệu đã thay đổi, vui lòng tải lại" |
| LVCTKD_011.008 | Xoá xong danh sách nạp lại đúng | P1 | Đang ở trang 2, xoá dòng cuối cùng của trang | 1. Xoá bản ghi<br>2. Quan sát |  | Danh sách nạp lại, phân trang cập nhật đúng tổng số |

## XII. XUẤT EXCEL

| TC ID | Chức năng | Ưu tiên | Tiền điều kiện | Bước thực hiện | Test Data | Kết quả mong đợi |
|---|---|:---:|---|---|---|---|
| LVCTKD_012.001 | Xuất Excel không lọc | P0 | Có ≥ 3 bản ghi, user có quyền | 1. Bấm "Xuất Excel"<br>2. Mở file tải về |  | Tải được file tên "danh_sach_linh_vuc_cong_ty_kinh_doanh.xls"<br>File mở được bằng Excel |
| LVCTKD_012.002 | Đúng 8 cột theo thứ tự | P0 | Vừa tải file export | 1. Mở file, quan sát dòng header |  | STT · Mã · Tên lĩnh vực Công ty kinh doanh · Trạng thái · Người tạo · Ngày tạo · Người cập nhật · Ngày cập nhật |
| LVCTKD_012.003 | Tiêu đề trong file | P1 | Vừa tải file export | 1. Quan sát dòng tiêu đề phía trên bảng |  | Ghi "Danh sách lĩnh vực Công ty kinh doanh" |
| LVCTKD_012.004 | Export theo ĐÚNG bộ lọc đang áp | P0 | Có 10 bản ghi, đang lọc Trạng thái = Khoá (còn 3 bản ghi) | 1. Bấm Xuất Excel<br>2. Đếm số dòng trong file | status = Khoá | File chỉ chứa 3 bản ghi đang lọc, không phải toàn bộ 10 |
| LVCTKD_012.005 | Export KHÔNG bị giới hạn phân trang | P0 | Có 30 bản ghi, đang xem trang 1 với page size = 10 | 1. Bấm Xuất Excel<br>2. Đếm số dòng |  | File chứa đủ 30 bản ghi (không chỉ 10 dòng của trang hiện tại) |
| LVCTKD_012.006 | Export khi bộ lọc không ra dòng nào | P2 | Lọc bằng từ khoá không tồn tại | 1. Bấm Xuất Excel | zzzzzz | File tải về chỉ có phần header, không có dòng dữ liệu, không lỗi |
| LVCTKD_012.007 | Quyền Xem vẫn xuất được Excel | P0 | User CHỈ có quyền Xem | 1. Bấm Xuất Excel |  | Tải file thành công (route export nhận cả 2 quyền) |
| LVCTKD_012.008 | Tên file đúng trên Safari | P1 | Dùng trình duyệt Safari (hoặc webview iOS) | 1. Bấm Xuất Excel<br>2. Quan sát tên file trong thư mục Downloads |  | File có tên + đuôi .xls đúng<br>KHÔNG ra file UUID không đuôi (do tải trực tiếp qua ?token=, không dùng blob) |
| LVCTKD_012.009 | Định dạng ngày trong file export | P2 | Vừa tải file | 1. Quan sát cột Ngày tạo / Ngày cập nhật |  | Dạng dd/mm/yyyy HH:mm, không có giây |

## XIII. IMPORT EXCEL

| TC ID | Chức năng | Ưu tiên | Tiền điều kiện | Bước thực hiện | Test Data | Kết quả mong đợi |
|---|---|:---:|---|---|---|---|
| LVCTKD_013.001 | Mở modal Import | P0 | User có quyền Quản lý | 1. Bấm "Import Excel" |  | Mở modal tiêu đề "Import Lĩnh vực Công ty kinh doanh"<br>Phụ đề: "Chỉ nhập Mã và Tên • Validate xong dòng hợp lệ sẽ bị khoá" |
| LVCTKD_013.002 | Tải file mẫu | P0 | Modal Import đang mở | 1. Bấm "Tải file mẫu"<br>2. Mở file tải về |  | Tải được Mau_import_LinhVucKinhDoanhNoiBo.xlsx<br>Dòng 1 header: STT · Mã lĩnh vực Công ty kinh doanh · Tên lĩnh vực Công ty kinh doanh<br>Dòng 2 là dòng hướng dẫn<br>Dòng 3-4 là 2 dòng mẫu |
| LVCTKD_013.003 | Nạp file mẫu nguyên bản | P0 | Đã tải file mẫu | 1. Upload lại chính file mẫu<br>2. Bấm "Load lên bảng" | File mẫu gốc | Bảng nạp ĐÚNG 2 dòng (dòng hướng dẫn bị bỏ qua nhờ skipRows = 1) |
| LVCTKD_013.004 | File mẫu import được thật | P0 | Đã nạp 2 dòng mẫu, DB chưa có 2 mã đó | 1. Bấm Validate<br>2. Bấm Import |  | 2 dòng đều hợp lệ<br>Import thành công 2 bản ghi |
| LVCTKD_013.005 | Nhận file có header TÊN CŨ | P1 | File Excel dùng header "Mã lĩnh vực kinh doanh nội bộ" / "Tên lĩnh vực kinh doanh nội bộ" | 1. Upload file<br>2. Bấm Load lên bảng | File mẫu bản cũ | Vẫn khớp cột đúng nhờ aliases, nạp được dữ liệu |
| LVCTKD_013.006 | Báo lỗi khi file thiếu cột bắt buộc | P1 | File Excel chỉ có cột Mã, thiếu cột Tên | 1. Upload + Load lên bảng |  | Modal báo không khớp header / thiếu trường bắt buộc |
| LVCTKD_013.007 | Validate — dòng hợp lệ | P0 | Bảng đã nạp 1 dòng Mã + Tên hợp lệ, chưa trùng | 1. Bấm "Validate" | LVKDNB.IM1 / Lĩnh vực import 1 | Trả validCount = 1, invalidCount = 0<br>Dòng được đánh dấu hợp lệ và bị khoá lại (không sửa được nữa)<br>Toast "Validate thành công" |
| LVCTKD_013.008 | Validate — Mã sai định dạng | P0 | Bảng đã nạp dòng có mã sai | 1. Bấm Validate | ABC.123 | Dòng báo lỗi: "Mã phải có dạng LVKDNB. + tối đa 4 ký tự (A-Z, 0-9, _)" |
| LVCTKD_013.009 | Validate — Mã để trống | P0 | Bảng có dòng thiếu mã | 1. Bấm Validate | (trống) | Lỗi "Mã bắt buộc phải nhập" |
| LVCTKD_013.010 | Validate — Mã đã có trong DB | P0 | DB đã có LVKDNB.OTO | 1. Nạp dòng có mã LVKDNB.OTO<br>2. Bấm Validate | LVKDNB.OTO | Lỗi "Mã đã tồn tại trong hệ thống" |
| LVCTKD_013.011 | Validate — Mã trùng giữa 2 dòng trong file | P0 | File có dòng 1 và dòng 2 cùng mã | 1. Nạp + Validate | Dòng 1 và 2 đều LVKDNB.AA | Dòng 2 báo "Mã bị trùng với dòng 1 trong file"<br>Dòng 1 vẫn hợp lệ |
| LVCTKD_013.012 | Validate — Tên để trống | P0 | Dòng có mã hợp lệ nhưng thiếu tên | 1. Bấm Validate |  | Lỗi "Tên bắt buộc phải nhập" |
| LVCTKD_013.013 | Validate — Tên > 255 ký tự | P1 | Dòng có tên 256 ký tự | 1. Bấm Validate | Chuỗi 256 ký tự | Lỗi "Tên tối đa 255 ký tự" |
| LVCTKD_013.014 | Validate — Tên chứa dấu phẩy / hai chấm | P1 | Dòng có tên "Ô tô, xe" | 1. Bấm Validate | Ô tô, xe | Lỗi "Tên không được chứa dấu phẩy (,) và dấu hai chấm (:)" |
| LVCTKD_013.015 | Validate — Tên đã có trong DB | P0 | DB đã có bản ghi tên "Ô tô" | 1. Nạp dòng tên "ô tô" (khác hoa thường)<br>2. Validate | ô tô | Lỗi "Tên đã tồn tại trong hệ thống" (so không phân biệt hoa/thường) |
| LVCTKD_013.016 | Validate — Tên trùng giữa 2 dòng trong file | P0 | File có 2 dòng cùng tên | 1. Nạp + Validate |  | Dòng sau báo "Tên bị trùng với dòng N trong file" |
| LVCTKD_013.017 | Nút Import chỉ bật khi hết dòng lỗi | P0 | File có 1 dòng hợp lệ + 1 dòng lỗi, đã Validate | 1. Quan sát nút "Import" |  | Nút Import bị khoá/không bấm được khi còn dòng lỗi |
| LVCTKD_013.018 | Sửa dòng lỗi rồi validate lại | P0 | Đang có 1 dòng lỗi sau khi Validate | 1. Sửa lại giá trị dòng lỗi ngay trên bảng<br>2. Bấm Validate lại |  | Dòng chuyển sang hợp lệ<br>Nút Import bật lên |
| LVCTKD_013.019 | Import toàn bộ hợp lệ | P0 | Đã validate 3 dòng đều hợp lệ | 1. Bấm Import |  | Toast xanh "Import thành công 3 lĩnh vực Công ty kinh doanh"<br>Modal đóng<br>Danh sách có thêm 3 bản ghi, đều ở trạng thái Hoạt động |
| LVCTKD_013.020 | Import một phần (HTTP 207) | P0 | Gọi thẳng API import với 3 dòng: 2 hợp lệ + 1 lỗi | 1. Postman: POST /import với payload hỗn hợp |  | HTTP 207<br>Message "Import thành công 2/3 lĩnh vực Công ty kinh doanh. 1 lĩnh vực thất bại"<br>FE hiện toast màu cảnh báo |
| LVCTKD_013.021 | Import không có dòng nào hợp lệ | P0 | Payload toàn dòng lỗi | 1. Postman: POST /import |  | HTTP 400 "Không có dữ liệu hợp lệ để import"<br>KHÔNG ghi bản ghi nào |
| LVCTKD_013.022 | Import quá 1000 dòng | P1 | Payload 1001 phần tử | 1. Postman: POST /import | 1001 dòng | HTTP 422 "Import danh sách lĩnh vực Công ty kinh doanh tối đa 1000 phần tử" |
| LVCTKD_013.023 | Import mảng rỗng | P1 | Payload internal_business_scopes = [] | 1. Postman: POST /import | [] | HTTP 422 "Import danh sách lĩnh vực Công ty kinh doanh phải có ít nhất 1 phần tử" |
| LVCTKD_013.024 | Import thiếu key internal_business_scopes | P2 | Payload rỗng {} | 1. Postman: POST /import | {} | HTTP 422 "Danh sách lĩnh vực Công ty kinh doanh là bắt buộc" |
| LVCTKD_013.025 | Import với quyền Xem | P0 | User CHỈ có quyền Xem | 1. Postman: POST /import với token của user đó |  | HTTP 403, không ghi dữ liệu |
| LVCTKD_013.026 | Import ghi trong 1 transaction | P2 | Payload nhiều dòng, giả lập lỗi giữa chừng | 1. Gây lỗi ở dòng cuối<br>2. Kiểm DB |  | Không có bản ghi nào bị ghi dở dang (rollback) |

## XIV. API — KIỂM TRỰC TIẾP (Postman / curl)

| TC ID | Chức năng | Ưu tiên | Tiền điều kiện | Bước thực hiện | Test Data | Kết quả mong đợi |
|---|---|:---:|---|---|---|---|
| LVCTKD_014.001 | GET danh sách trả 200 + cấu trúc đúng | P0 | Token của user có quyền | 1. GET /api/v1/assign/internal-business-scopes |  | HTTP 200<br>Có data[] và meta (current_page, per_page, total, last_page, from, to) |
| LVCTKD_014.002 | Resource trả đủ field | P0 | Có ≥ 1 bản ghi | 1. GET danh sách<br>2. Kiểm 1 phần tử trong data |  | Có đủ: id, code, name, status, status_text, created_by_name, created_at, updated_by_name, updated_at, is_can_edit, is_can_delete, is_can_lock_update, scopes_count |
| LVCTKD_014.003 | GET danh sách KHÔNG token | P0 | Không gửi Authorization header | 1. GET /api/v1/assign/internal-business-scopes |  | HTTP 401 |
| LVCTKD_014.004 | GET danh sách với user KHÔNG quyền | P0 | Token của e2e_nocatalog@test.local | 1. GET danh sách |  | HTTP 403 |
| LVCTKD_014.005 | GET chi tiết id không tồn tại | P1 | Token hợp lệ | 1. GET /assign/internal-business-scopes/99999999 |  | HTTP 404 |
| LVCTKD_014.006 | POST tạo mới với user quyền Xem | P0 | Token quyền Xem | 1. POST / với payload hợp lệ |  | HTTP 403, không tạo bản ghi |
| LVCTKD_014.007 | PUT sửa với user quyền Xem | P0 | Token quyền Xem | 1. PUT /{id} |  | HTTP 403 |
| LVCTKD_014.008 | DELETE với user quyền Xem | P0 | Token quyền Xem | 1. DELETE /{id} |  | HTTP 403 |
| LVCTKD_014.009 | lock/unlock với user quyền Xem | P0 | Token quyền Xem | 1. GET /{id}/lock<br>2. GET /{id}/unlock |  | Cả 2 đều HTTP 403 |
| LVCTKD_014.010 | POST có id trong body → cập nhật | P1 | Bản ghi id = 12 đang Hoạt động | 1. POST / với body {id:12, code, name} |  | HTTP 200, bản ghi 12 được cập nhật (không tạo bản ghi mới) |
| LVCTKD_014.011 | POST có id KHÔNG tồn tại | P1 | Token hợp lệ | 1. POST / với body {id: 99999999, ...} |  | HTTP 404 "Dữ liệu đã thay đổi, vui lòng tải lại" |
| LVCTKD_014.012 | Lỗi 422 giữ nguyên (không bị nuốt thành 400) | P0 | Token hợp lệ | 1. POST / với code sai định dạng | code = "ABC" | HTTP 422 kèm object errors theo từng field<br>KHÔNG phải 400 |
| LVCTKD_014.013 | status ngoài 1/2 | P1 | Token hợp lệ | 1. POST / với status = 9 | status = 9 | HTTP 422 "Trạng thái không hợp lệ" |
| LVCTKD_014.014 | GET /getAll chỉ trả bản ghi Hoạt động | P0 | DB có cả bản ghi Hoạt động và Khoá | 1. GET /assign/internal-business-scopes/getAll |  | Chỉ trả bản ghi status = 1<br>Sắp theo name tăng dần<br>Mỗi phần tử có is_locked |
| LVCTKD_014.015 | GET /getAll với include_ids | P1 | Bản ghi id = 5 đang Khoá | 1. GET /getAll?include_ids[]=5 | include_ids = [5] | Trả cả bản ghi id = 5 dù đang Khoá, kèm is_locked = true<br>(để màn Sửa không mất giá trị đã chọn) |
| LVCTKD_014.016 | Phân trang per_page | P1 | Có > 5 bản ghi | 1. GET /?per_page=5&page=2 |  | Trả tối đa 5 phần tử, meta.current_page = 2 |

## XV. LIÊN KẾT VỚI NHÓM NGÀNH

| TC ID | Chức năng | Ưu tiên | Tiền điều kiện | Bước thực hiện | Test Data | Kết quả mong đợi |
|---|---|:---:|---|---|---|---|
| LVCTKD_015.001 | Ô chọn Lĩnh vực trong modal Nhóm ngành | P0 | Có ≥ 1 lĩnh vực đang Hoạt động | 1. Vào Danh mục › Nhóm ngành<br>2. Bấm Tạo mới |  | Có ô "Lĩnh vực Công ty kinh doanh" kèm dấu * bắt buộc<br>Placeholder "Chọn lĩnh vực Công ty kinh doanh"<br>Danh sách chọn chỉ có lĩnh vực đang Hoạt động |
| LVCTKD_015.002 | Bắt buộc chọn Lĩnh vực khi tạo Nhóm ngành | P0 | Modal Tạo Nhóm ngành đang mở | 1. Nhập Mã + Tên, KHÔNG chọn Lĩnh vực<br>2. Bấm Lưu |  | Báo lỗi "Bắt buộc phải chọn" dưới ô Lĩnh vực |
| LVCTKD_015.003 | Cột Lĩnh vực trong danh sách Nhóm ngành | P0 | Có Nhóm ngành đã gắn lĩnh vực | 1. Vào danh sách Nhóm ngành |  | Có cột "Lĩnh vực Công ty kinh doanh" hiện đúng tên lĩnh vực<br>Bản ghi chưa gắn hiện "—" |
| LVCTKD_015.004 | Bộ lọc Lĩnh vực ở màn Nhóm ngành | P1 | Danh sách Nhóm ngành có nhiều lĩnh vực khác nhau | 1. Mở lọc nâng cao<br>2. Chọn 1 Lĩnh vực |  | Chỉ hiện Nhóm ngành thuộc lĩnh vực đó |
| LVCTKD_015.005 | Không chọn được lĩnh vực đã Khoá | P0 | Có lĩnh vực đang Khoá | 1. Mở modal Tạo Nhóm ngành<br>2. Mở ô chọn Lĩnh vực |  | Lĩnh vực đang Khoá KHÔNG xuất hiện trong danh sách chọn |
| LVCTKD_015.006 | Sửa Nhóm ngành có lĩnh vực đã bị Khoá | P0 | Nhóm ngành X gắn lĩnh vực Y, sau đó Y bị Khoá | 1. Mở modal Sửa Nhóm ngành X |  | Ô Lĩnh vực VẪN hiện giá trị Y (nhờ include_ids), có dấu hiệu đã khoá<br>Không bị mất giá trị đang chọn |
| LVCTKD_015.007 | Gán lĩnh vực đã khoá qua API | P1 | Lĩnh vực Y đang Khoá | 1. Postman: tạo Nhóm ngành với internal_business_scope_id = Y |  | HTTP 422 "Lĩnh vực Công ty kinh doanh '<tên>' đã bị khoá, vui lòng chọn lĩnh vực khác" |
| LVCTKD_015.008 | Gán lĩnh vực không tồn tại | P1 | Token hợp lệ | 1. Postman: tạo Nhóm ngành với internal_business_scope_id = 99999999 |  | HTTP 422 "Lĩnh vực Công ty kinh doanh không tồn tại" |
| LVCTKD_015.009 | Import Nhóm ngành theo MÃ lĩnh vực | P0 | File mẫu Nhóm ngành có cột "Mã lĩnh vực Công ty kinh doanh *" | 1. Tải file mẫu Nhóm ngành<br>2. Điền mã LVKDNB.OTO<br>3. Validate + Import | LVKDNB.OTO | Import thành công, Nhóm ngành gắn đúng lĩnh vực |
| LVCTKD_015.010 | Import Nhóm ngành với mã lĩnh vực không tồn tại | P0 | Đang import Nhóm ngành | 1. Điền mã LVKDNB.XXX (không có trong DB)<br>2. Validate | LVKDNB.XXX | Dòng báo lỗi "Lĩnh vực Công ty kinh doanh 'LVKDNB.XXX' không tồn tại" |
| LVCTKD_015.011 | Import Nhóm ngành với mã lĩnh vực đã Khoá | P1 | Lĩnh vực LVKDNB.OLD đang Khoá | 1. Điền mã đó vào file import Nhóm ngành<br>2. Validate | LVKDNB.OLD | Dòng báo lỗi "Lĩnh vực Công ty kinh doanh 'LVKDNB.OLD' đã bị khoá" |
| LVCTKD_015.012 | scopes_count phản ánh đúng số Nhóm ngành | P1 | Lĩnh vực có 3 Nhóm ngành | 1. GET chi tiết lĩnh vực đó |  | scopes_count = 3<br>is_can_delete = false |

## XVI. GIAO DIỆN & E2E TỔNG HỢP

| TC ID | Chức năng | Ưu tiên | Tiền điều kiện | Bước thực hiện | Test Data | Kết quả mong đợi |
|---|---|:---:|---|---|---|---|
| LVCTKD_016.001 | Không còn chữ "nội bộ" trên giao diện | P0 | User có quyền Quản lý | 1. Rà toàn bộ màn: menu, tiêu đề bảng, nhãn cột, bộ lọc, modal, toast, modal Import |  | Mọi chỗ đều ghi "Lĩnh vực Công ty kinh doanh"<br>KHÔNG còn chuỗi "lĩnh vực kinh doanh nội bộ" ở bất kỳ đâu người dùng nhìn thấy |
| LVCTKD_016.002 | Tên quyền trong màn Phân quyền | P0 | Đăng nhập tài khoản admin | 1. Vào màn Phân quyền<br>2. Tìm nhóm "Danh mục" |  | Hiện 2 quyền: "Quản lý danh mục lĩnh vực Công ty kinh doanh" và "Xem danh mục lĩnh vực Công ty kinh doanh" |
| LVCTKD_016.003 | Đỏ chỉ dùng cho lỗi validate | P2 | Màn danh sách + modal | 1. Rà màu sắc toàn màn |  | Màu đỏ chỉ xuất hiện ở: dấu * bắt buộc, thông báo lỗi validate, badge Khoá, nút Xoá<br>Không dùng đỏ trang trí |
| LVCTKD_016.004 | Hiển thị trên màn hình nhỏ | P2 | Thu nhỏ cửa sổ còn 1366px | 1. Quan sát bảng |  | Cột STT và Mã dính (sticky) khi cuộn ngang<br>Bảng cuộn ngang được, không vỡ layout |
| LVCTKD_016.005 | E2E: Tạo → Sửa → Khoá → Mở khoá → Xoá | P0 | User có quyền Quản lý | 1. Tạo LVKDNB.E2E "Lĩnh vực E2E"<br>2. Sửa tên thành "Lĩnh vực E2E sửa"<br>3. Khoá<br>4. Mở khoá<br>5. Xoá | LVKDNB.E2E | Cả 5 bước đều thành công<br>Sau bước 2: Người/Ngày cập nhật đổi<br>Sau bước 3: chỉ còn nút Mở khoá<br>Sau bước 5: bản ghi biến mất |
| LVCTKD_016.006 | E2E: Tạo lĩnh vực → gắn Nhóm ngành → thử xoá/khoá | P0 | User có quyền Quản lý cả 2 danh mục | 1. Tạo lĩnh vực mới<br>2. Tạo Nhóm ngành gắn lĩnh vực đó<br>3. Quay lại màn Lĩnh vực, quan sát cột Hành động<br>4. Khoá Nhóm ngành<br>5. Quan sát lại |  | Bước 3: mất cả nút Xoá và nút Khoá<br>Bước 5: nút Khoá hiện lại (chỉ còn Nhóm ngành đã khoá), nút Xoá vẫn ẩn |
| LVCTKD_016.007 | E2E: Import → Xuất Excel đối chiếu | P1 | DB sạch | 1. Import 3 bản ghi từ file mẫu<br>2. Xuất Excel<br>3. Đối chiếu |  | File export có đủ 3 bản ghi vừa import, đúng Mã/Tên/Trạng thái Hoạt động |
| LVCTKD_016.008 | E2E: 2 user song song | P1 | 2 trình duyệt, 2 tài khoản đều có quyền Quản lý | 1. User A tạo bản ghi X<br>2. User B refresh, thấy X<br>3. User B sửa X<br>4. User A refresh |  | User A thấy Người cập nhật = User B<br>Dữ liệu nhất quán giữa 2 phiên |
| LVCTKD_016.009 | Dọn dữ liệu test sau khi chạy | P1 | Đã chạy xong bộ testcase | 1. Xoá toàn bộ bản ghi có mã bắt đầu LVKDNB.E2E / LVKDNB.TEST / LVKDNB.IM |  | DB trở lại trạng thái trước khi test |
