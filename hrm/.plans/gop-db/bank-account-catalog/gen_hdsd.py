# -*- coding: utf-8 -*-
"""Sinh HDSD (Word) cho man 'Danh muc tai khoan ngan hang' (/finance/account-banks).

Bo cuc bam bo tai lieu mau cua team: .plans/gop-db/customer-docs/HDSD_Danh muc khach hang.docx
— TONG QUAN gom ca bang quyen o muc 4, cac PHAN chuc nang o giua, PHAN cuoi la
"HUONG DAN THEO TUNG QUYEN" + cau hoi thuong gap.

⚠️ Tieu de dat la "TONG QUAN" (khong phai "TONG QUAN PHAN MEM") vi engine assert khong con
tieu de cua file khung trong output — file khung HDSD_MAU.docx dung dung chuoi do.

Anh chup that tren cong dev hrm-crm.eteksofts.com ngay 17/08/2026, 1440x900 -> tknh_shots/
(CHI DE LOCAL, .gitignore da chan **/.plans/**/*_shots/).

Chay:  python .plans/gop-db/bank-account-catalog/gen_hdsd.py
"""
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..", "..", "..", ".claude", "skills", "hdsd-documenter", "assets"))

from hdsd_engine import HdsdBuilder  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))

b = HdsdBuilder(
    output=os.path.join(HERE, "HDSD_Danh muc tai khoan ngan hang.docx"),
    shots_dir=os.path.join(HERE, "tknh_shots"),
    cover_title="(Màn hình: Danh mục tài khoản ngân hàng)",
    doc_title="HDSD - Danh mục tài khoản ngân hàng",
)

# ============================================================================
b.h1("TỔNG QUAN")

b.h2("1. Thuật ngữ sử dụng trong tài liệu")
b.table([
    ["Thuật ngữ", "Giải thích"],
    ["Tài khoản ngân hàng của công ty",
     "Một dòng trong danh mục: số tài khoản, chủ tài khoản, ngân hàng, chi nhánh và loại tiền tệ. "
     "Đây là tài khoản của CÔNG TY, không phải tài khoản cá nhân của nhân viên."],
    ["Chủ tài khoản",
     "Tên chủ tài khoản in trên sổ hoặc thẻ ngân hàng. Hệ thống tự chuyển thành CHỮ IN HOA khi lưu."],
    ["Ngân hàng",
     "Lấy từ màn Danh mục ngân hàng của phân hệ Danh mục chung. Chỉ ngân hàng đang Hoạt động mới "
     "chọn được."],
    ["Chi nhánh",
     "Chi nhánh của ngân hàng đã chọn. Danh sách chi nhánh luôn lọc theo đúng ngân hàng, xem "
     "mục 4 của PHẦN 4."],
    ["Loại tiền tệ",
     "Lấy từ màn Danh mục tiền tệ của phân hệ Tài chính. Chỉ loại tiền tệ đang Hoạt động mới chọn "
     "được."],
    ["Trạng thái Hoạt động", "Tài khoản đang dùng bình thường, sửa được."],
    ["Trạng thái Khóa",
     "Tài khoản ngừng sử dụng nhưng KHÔNG bị xoá; khi đang khóa thì không sửa được, xem PHẦN 7."],
    ["Lịch sử thay đổi",
     "Nhật ký ghi lại ai đã tạo, sửa, khóa hay mở khóa một tài khoản, xem PHẦN 8."],
])

b.h2("2. Cập nhật tài liệu")
b.table([
    ["Phiên bản", "Ngày", "Người cập nhật", "Nội dung"],
    ["1.0", "17/08/2026", "@khoipv",
     "Lập mới cho màn Danh mục tài khoản ngân hàng sau khi chuyển màn từ phần mềm cũ sang phân hệ "
     "Tài chính."],
])

b.h2("3. Giới thiệu chung")
b.para("Màn hình “Danh mục tài khoản ngân hàng” là nơi khai báo và quản lý các tài khoản ngân hàng "
       "CỦA CÔNG TY: số tài khoản, chủ tài khoản, ngân hàng, chi nhánh và loại tiền tệ.")
b.para("Dữ liệu khai báo ở đây được dùng lại ở các nghiệp vụ thu chi, đề nghị thanh toán và các "
       "chứng từ cần chọn tài khoản nhận hoặc chuyển tiền của công ty. Vì vậy khai báo sai ở màn "
       "này sẽ kéo theo sai ở chứng từ.")
b.para("Lưu ý phạm vi: mỗi người chỉ nhìn thấy tài khoản ngân hàng của CÔNG TY MÌNH. Tài khoản của "
       "công ty khác không hiển thị và cũng không tìm ra được.")
b.para("Đường dẫn truy cập:")
b.bullet("Menu: Phân hệ Tài chính → Danh mục → Danh mục tài khoản ngân hàng.")
b.bullet("Hoặc gõ thẳng đường dẫn /finance/account-banks vào thanh địa chỉ trình duyệt.")

b.h2("4. Quyền và phạm vi dữ liệu")

b.h3("4.1 Bảng quyền của màn hình")
b.table([
    ["Tên quyền", "Cho phép làm gì", "Nút / cửa sổ tương ứng", "Ghi chú"],
    ["Quản lý danh mục tài khoản ngân hàng",
     "Mở màn hình, xem danh sách, tạo mới, sửa, khóa / mở khóa, xem chi tiết và xem lịch sử.",
     "Toàn bộ nút trên màn hình: Tạo mới, Sửa, Khóa / Mở khóa, Lịch sử.",
     "Đây là quyền DUY NHẤT của màn. Thiếu quyền thì mục menu bị ẩn và gõ thẳng đường dẫn cũng bị "
     "chặn."],
])
b.para("Khác với một số màn danh mục khác, quyền này gắn cho CẢ chức năng xem danh sách, không chỉ "
       "các thao tác thêm - sửa. Không có quyền thì không xem được gì.")

b.h3("4.2 Phạm vi dữ liệu theo công ty")
b.bullet("Bạn chỉ thấy tài khoản ngân hàng thuộc công ty ghi trong hồ sơ nhân sự của bạn.")
b.bullet("Tài khoản của công ty khác: không hiển thị, tìm kiếm cũng không ra.")
b.bullet("Tài khoản mới tạo tự động thuộc công ty của bạn — không có ô chọn công ty trên form.")
b.bullet("Nếu hồ sơ nhân sự của bạn CHƯA gắn công ty: danh sách trống hoàn toàn và khi bấm Lưu hệ "
         "thống báo “Tài khoản đăng nhập chưa gắn công ty, không thể thao tác”. Hãy báo bộ phận "
         "nhân sự bổ sung công ty cho hồ sơ.")
b.bullet("Màn hình không chia nhỏ theo phòng ban hay bộ phận: mọi người cùng công ty thấy chung "
         "một danh sách.")

# ============================================================================
b.h1("PHẦN 1: TRUY CẬP VÀ BỐ CỤC MÀN HÌNH")

b.h2("1. Truy cập màn hình")
b.bullet("Bước 1: Đăng nhập hệ thống.")
b.bullet("Bước 2: Chọn phân hệ “Tài chính” ở góc trên bên trái.")
b.bullet("Bước 3: Trên menu bên trái, mở nhóm “Danh mục”.")
b.bullet("Bước 4: Bấm mục “Danh mục tài khoản ngân hàng”.")
b.para("Màn hình mở ra với tiêu đề “Danh mục tài khoản ngân hàng”, danh sách hiển thị 10 dòng đầu "
       "tiên của công ty bạn.")

b.image("01-danh-sach.png", "Màn hình Danh mục tài khoản ngân hàng khi mới truy cập")

b.h2("2. Bố cục màn hình")
b.bullet("Khối trên — “Bộ lọc danh sách”: ô tìm nhanh, ô Chi nhánh, ô Trạng thái, nút Tìm kiếm và "
         "nút Làm mới. Ba ô lọc bày sẵn trên một hàng ngang nên màn này KHÔNG có nút “Tìm kiếm "
         "nâng cao”.")
b.bullet("Khối dưới — bảng “Danh sách tài khoản ngân hàng”: góc phải phía trên có nút Tạo mới và "
         "nút Cấu hình cột hiển thị; cuối bảng là dòng thống kê và phần phân trang.")

b.image("02-cot-hanh-dong.png", "Bảng danh sách khi thu gọn menu bên trái — thấy đủ cột Hành động")

b.h2("3. Các cột của bảng danh sách")
b.para("Bảng có 12 cột khả dụng, khi mới dùng hệ thống hiển thị sẵn 8 cột. Bốn cột còn lại bật "
       "thêm ở cửa sổ Tuỳ chỉnh cột, xem PHẦN 3.")
b.table([
    ["Cột", "Hiện sẵn", "Nội dung"],
    ["STT", "Có", "Số thứ tự tính theo trang đang xem. Trang 2 với 10 dòng/trang bắt đầu từ 11."],
    ["Số tài khoản", "Có",
     "Số tài khoản ngân hàng, hiển thị dạng đường dẫn. Bấm vào là mở cửa sổ Xem chi tiết."],
    ["Chủ tài khoản", "Có", "Tên chủ tài khoản, luôn hiển thị dạng CHỮ IN HOA."],
    ["Ngân hàng", "Có", "Tên ngân hàng của tài khoản."],
    ["Loại tiền tệ", "Không", "Mã loại tiền tệ, ví dụ VNĐ, AUD, CHF. Dòng chưa khai hiện dấu gạch "
                             "ngang."],
    ["Chi nhánh", "Không", "Tên chi nhánh ngân hàng."],
    ["Người cập nhật", "Không", "Người sửa gần nhất."],
    ["Ngày cập nhật", "Không", "Ngày giờ sửa gần nhất."],
    ["Người tạo", "Có", "Người đã tạo bản ghi."],
    ["Ngày tạo", "Có", "Ngày giờ tạo bản ghi. Danh sách mặc định xếp theo cột này, mới nhất trước."],
    ["Trạng thái", "Có", "Nhãn Hoạt động màu xanh hoặc Khóa màu đỏ."],
    ["Hành động", "Có", "Các nút thao tác của dòng, luôn nằm ở cuối bảng."],
])

b.h2("4. Cột Hành động")
b.para("Màn hình có đúng 3 thao tác trên từng dòng nên cả 3 nút hiện thẳng ra, không có menu ba "
       "chấm. Nút nào không dùng được sẽ bị ẨN HẲN chứ không hiện rồi làm mờ.")
b.table([
    ["Nút", "Khi nào hiển thị", "Công dụng"],
    ["Sửa (bút chì)", "Tài khoản đang Hoạt động và bạn có quyền quản lý.",
     "Mở cửa sổ Sửa tài khoản ngân hàng, xem PHẦN 5."],
    ["Khóa (ổ khoá)", "Tài khoản đang Hoạt động và bạn có quyền quản lý.",
     "Chuyển tài khoản sang trạng thái Khóa, xem PHẦN 7."],
    ["Mở khóa (ổ khoá mở)", "Tài khoản đang Khóa và bạn có quyền quản lý.",
     "Đưa tài khoản trở lại Hoạt động, xem PHẦN 7."],
    ["Lịch sử (đồng hồ)", "Luôn hiển thị.",
     "Mở cửa sổ Lịch sử thay đổi của tài khoản, xem PHẦN 8."],
])
b.para("Ghi nhớ nhanh: tài khoản đang KHÓA chỉ còn Mở khóa và Lịch sử. Màn hình KHÔNG có nút Xóa — "
       "tài khoản không dùng nữa thì Khóa lại.")

b.h2("5. Phân trang")
b.bullet("Dòng bên trái phía dưới bảng ghi “Hiển thị 1–10 / N”: đang xem dòng 1 đến 10 trong tổng "
         "số N tài khoản khớp bộ lọc.")
b.bullet("Ô “Số dòng/trang” cho chọn 5, 10, 20, 50 hoặc 100 dòng, mặc định là 10.")
b.bullet("Đổi số dòng/trang thì danh sách quay về trang 1.")
b.bullet("Danh sách mặc định xếp theo Ngày tạo, mới nhất ở trên cùng.")

b.h2("6. Sắp xếp theo cột")
b.para("Bốn cột có biểu tượng mũi tên ở tiêu đề để đổi thứ tự sắp xếp: Số tài khoản, Chủ tài "
       "khoản, Ngày tạo và Ngày cập nhật.")
b.bullet("Bấm lần 1: xếp tăng dần. Bấm lần 2: xếp giảm dần.")
b.bullet("Mỗi lần chỉ sắp xếp theo một cột; bấm cột khác thì bỏ tiêu chí cũ.")
b.bullet("Các cột còn lại (Ngân hàng, Chi nhánh, Loại tiền tệ, Trạng thái) không có chức năng sắp "
         "xếp, bấm vào không xảy ra gì.")

# ============================================================================
b.h1("PHẦN 2: TÌM KIẾM VÀ LỌC DANH SÁCH")

b.image("03-tim-kiem.png", "Kết quả sau khi tìm nhanh theo từ khoá “TRANG TEST”")

b.h2("1. Tìm kiếm nhanh")
b.para("Ô đầu tiên có dòng gợi ý “Tìm theo số tài khoản, chủ tài khoản, ngân hàng”. Ô này quét "
       "đồng thời cả ba trường đó.")
b.bullet("Gõ một phần chuỗi là đủ, kể cả phần nằm ở giữa.")
b.bullet("Không phân biệt chữ hoa chữ thường.")
b.bullet("PHẢI bấm nút Tìm kiếm hoặc nhấn phím Enter thì danh sách mới lọc; chỉ gõ thôi thì danh "
         "sách chưa đổi.")
b.bullet("Bấm dấu x ở cuối ô để xoá nhanh từ khoá.")

b.h2("2. Lọc theo chi nhánh")
b.para("Nhập một phần tên chi nhánh vào ô thứ hai, ví dụ “Bắc” hoặc “Cầu Giấy”. Hệ thống lọc theo "
       "tên chi nhánh đang lưu trên từng tài khoản.")

b.h2("3. Lọc theo trạng thái")
b.para("Ô thứ ba cho chọn “Hoạt động” hoặc “Khóa”. Để trống là lấy tất cả, bấm dấu x trong ô để bỏ "
       "lựa chọn.")
b.para("Khác với ô tìm nhanh, hai ô Chi nhánh và Trạng thái tự lọc lại ngay khi bạn thay đổi, "
       "không cần bấm Tìm kiếm.")

b.h2("4. Kết hợp nhiều điều kiện")
b.para("Các điều kiện được kết hợp theo kiểu “và”: kết quả phải thoả mãn đồng thời tất cả ô đã "
       "nhập. Ví dụ gõ “TRANG TEST” ở ô tìm nhanh và chọn Trạng thái = Khóa thì chỉ ra những tài "
       "khoản vừa khớp từ khoá vừa đang bị khóa.")

b.h2("5. Nút Làm mới")
b.para("Bấm “Làm mới” để xoá sạch cả ba ô lọc và tải lại toàn bộ danh sách. Nên dùng nút này trước "
       "khi bắt đầu một việc mới, vì hệ thống có ghi nhớ bộ lọc (xem mục 6).")

b.h2("6. Hệ thống ghi nhớ bộ lọc trong 10 phút")
b.para("Nếu bạn đang lọc rồi chuyển sang màn khác và quay lại trong vòng 10 phút, hệ thống giữ "
       "nguyên điều kiện lọc cũ. Đây là chủ ý để bạn không phải nhập lại. Nếu thấy danh sách "
       "“thiếu” tài khoản, hãy kiểm tra lại các ô lọc rồi bấm Làm mới.")

# ============================================================================
b.h1("PHẦN 3: TUỲ CHỈNH CỘT HIỂN THỊ")

b.image("04-cau-hinh-cot.png", "Cửa sổ Tuỳ chỉnh cột — cột STT và Số tài khoản có biểu tượng ổ khoá")

b.h2("1. Mở cửa sổ tuỳ chỉnh cột")
b.para("Bấm nút biểu tượng cột nằm ngay bên phải nút Tạo mới. Cửa sổ “Tuỳ chỉnh cột” hiện ra, liệt "
       "kê đủ 12 cột; cột nào đang hiển thị thì được tích sẵn.")

b.h2("2. Bật và tắt cột")
b.bullet("Tích vào ô vuông đầu dòng để bật cột, bỏ tích để tắt.")
b.bullet("Ba cột STT, Số tài khoản và Hành động có biểu tượng ổ khoá — không tắt được, vì Số tài "
         "khoản là lối vào cửa sổ Xem chi tiết.")
b.bullet("Bốn cột mặc định tắt nên bật thêm khi cần: Loại tiền tệ, Chi nhánh, Người cập nhật, "
         "Ngày cập nhật.")

b.h2("3. Đổi thứ tự cột")
b.para("Dùng chuột kéo biểu tượng ba gạch ở cuối mỗi dòng lên hoặc xuống để đổi vị trí cột trên "
       "bảng.")

b.h2("4. Lưu hoặc bỏ thay đổi")
b.bullet("Bấm “Lưu”: cửa sổ đóng, bảng vẽ lại theo lựa chọn mới. Cấu hình được ghi nhớ theo tài "
         "khoản của bạn, lần sau vào lại vẫn giữ nguyên và không ảnh hưởng tới người khác.")
b.bullet("Bấm “Đóng”: bỏ mọi thay đổi vừa chỉnh, bảng giữ nguyên như cũ.")

# ============================================================================
b.h1("PHẦN 4: TẠO MỚI TÀI KHOẢN NGÂN HÀNG")

b.h2("1. Mở cửa sổ Tạo mới")
b.para("Bấm nút “Tạo mới” ở góc phải phía trên bảng. Cửa sổ “Tạo tài khoản ngân hàng” mở ra ngay "
       "trên màn hình danh sách.")

b.image("05-tao-moi.png", "Cửa sổ Tạo tài khoản ngân hàng khi vừa mở")

b.h2("2. Các trường trong cửa sổ Tạo mới")
b.table([
    ["Trường", "Kiểu nhập", "Bắt buộc", "Giá trị điền sẵn", "Mô tả"],
    ["Số tài khoản", "Ô nhập chữ", "Có", "Trống",
     "Số tài khoản ngân hàng. Không được trùng với bất kỳ tài khoản nào trong hệ thống."],
    ["Loại tiền tệ", "Ô chọn từ danh sách", "Có", "Trống",
     "Chọn loại tiền tệ của tài khoản. Danh sách hiển thị dạng “Mã — Tên”, ví dụ “VNĐ — "
     "VietNamDong”. Chỉ có loại tiền tệ đang Hoạt động."],
    ["Chủ tài khoản", "Ô nhập chữ", "Có", "Trống",
     "Tên chủ tài khoản. Hệ thống tự chuyển thành CHỮ IN HOA khi lưu, gõ chữ thường vẫn đúng."],
    ["Ngân hàng", "Ô chọn từ danh sách", "Có", "Trống",
     "Chọn ngân hàng. Chỉ có ngân hàng đang Hoạt động; ngân hàng đã khóa không xuất hiện."],
    ["Chi nhánh", "Ô chọn từ danh sách", "Có", "Trống",
     "Bị khoá cho tới khi chọn Ngân hàng. Danh sách chỉ gồm chi nhánh của ngân hàng vừa chọn."],
    ["Trạng thái", "Ô chọn từ danh sách", "Có", "Hoạt động",
     "Chọn Hoạt động hoặc Khóa. Không xoá trắng được ô này."],
])

b.h2("3. Giá trị điền sẵn khi tạo mới")
b.bullet("Năm ô bắt buộc đều TRỐNG.")
b.bullet("Ô Trạng thái điền sẵn “Hoạt động” — đổi được ngay lúc tạo nếu muốn khai sẵn tài khoản "
         "chưa dùng tới.")
b.bullet("Ô Chi nhánh bị khoá cho tới khi bạn chọn Ngân hàng.")
b.bullet("Công ty, Người tạo và Ngày tạo do hệ thống tự ghi, không có ô nhập.")

b.h2("4. Thứ tự chọn Ngân hàng rồi tới Chi nhánh")
b.bullet("Bước 1: Chọn Ngân hàng trước. Trước đó ô Chi nhánh không mở được.")
b.bullet("Bước 2: Mở ô Chi nhánh — danh sách chỉ gồm chi nhánh của ngân hàng vừa chọn.")
b.bullet("Nếu sau đó bạn ĐỔI ngân hàng, ô Chi nhánh sẽ tự xoá trắng và phải chọn lại. Đây là chủ "
         "ý để tránh gán nhầm chi nhánh của ngân hàng khác.")

b.h2("5. Lưu bản ghi")
b.table([
    ["Nút", "Kết quả"],
    ["Lưu", "Ghi tài khoản mới, hiện thông báo “Thêm mới thành công”, đóng cửa sổ và làm mới danh "
            "sách. Tài khoản vừa tạo nằm ở đầu danh sách."],
    ["Đóng", "Thoát khỏi cửa sổ, không ghi gì."],
])
b.para("Sau khi lưu, Chủ tài khoản và tên ngân hàng hiển thị dạng CHỮ IN HOA — đây là quy ước của "
       "hệ thống, không phải lỗi nhập liệu.")

b.h2("6. Các lỗi thường gặp khi lưu")

b.image("06-loi-validate.png", "Bấm Lưu khi chưa nhập gì — hệ thống chặn ngay tại ô Chủ tài khoản")

b.image("07-loi-bat-buoc-be.png",
        "Bốn ô còn lại báo lỗi đỏ sau khi hệ thống kiểm tra dữ liệu")

b.table([
    ["Thông báo", "Nguyên nhân", "Cách xử lý"],
    ["Bắt buộc phải nhập (dưới ô Chủ tài khoản)", "Chưa nhập chủ tài khoản.",
     "Nhập chủ tài khoản rồi bấm Lưu lại. Ô này bị chặn ngay, chưa gửi dữ liệu đi."],
    ["Bắt buộc phải nhập (dưới ô Số tài khoản / Loại tiền tệ / Ngân hàng / Chi nhánh)",
     "Còn ô bắt buộc chưa nhập.",
     "Nhập hoặc chọn nốt ô báo đỏ. Bốn lỗi này hiện sau khi hệ thống kiểm tra."],
    ["Số tài khoản đã tồn tại", "Đã có tài khoản khác dùng số này.",
     "Kiểm tra lại danh sách. Lưu ý: số tài khoản không được trùng trên toàn hệ thống, kể cả với "
     "tài khoản của công ty khác mà bạn không nhìn thấy."],
    ["Ngân hàng không tồn tại hoặc đã bị khóa", "Ngân hàng vừa bị khóa ở Danh mục ngân hàng.",
     "Chọn ngân hàng khác, hoặc đề nghị mở khóa ngân hàng đó."],
    ["Chi nhánh không thuộc ngân hàng đã chọn", "Chi nhánh và ngân hàng không khớp nhau.",
     "Chọn lại Ngân hàng rồi chọn Chi nhánh trong danh sách vừa lọc."],
    ["Loại tiền tệ không tồn tại hoặc đã bị khóa", "Loại tiền tệ vừa bị khóa ở Danh mục tiền tệ.",
     "Chọn loại tiền tệ khác."],
    ["Tài khoản đăng nhập chưa gắn công ty, không thể thao tác",
     "Hồ sơ nhân sự của bạn chưa gắn công ty.",
     "Báo bộ phận nhân sự bổ sung công ty cho hồ sơ, sau đó đăng nhập lại."],
])
b.para("Khi có lỗi, cửa sổ KHÔNG đóng và dữ liệu bạn đã nhập vẫn còn nguyên — chỉ cần sửa ô báo đỏ "
       "rồi bấm Lưu lại.")

# ============================================================================
b.h1("PHẦN 5: SỬA TÀI KHOẢN NGÂN HÀNG")

b.h2("1. Mở cửa sổ Sửa")
b.para("Bấm nút Sửa, biểu tượng bút chì, ở cột Hành động của dòng cần sửa. Nút này chỉ hiển thị "
       "với tài khoản đang ở trạng thái Hoạt động; tài khoản đang Khóa phải Mở khóa trước, xem "
       "PHẦN 7.")

b.image("09-sua.png",
        "Cửa sổ Sửa tài khoản ngân hàng — ô Ngân hàng trống vì ngân hàng của bản ghi đã bị khóa")

b.h2("2. Các bước sửa")
b.bullet("Bước 1: Bấm nút Sửa ở dòng cần chỉnh.")
b.bullet("Bước 2: Sửa các ô cần thiết. Quy định bắt buộc và quy định không trùng giống hệt khi tạo "
         "mới.")
b.bullet("Bước 3: Bấm “Lưu”. Hệ thống báo “Cập nhật thành công”, đóng cửa sổ và làm mới danh sách.")

b.h2("3. Khi ngân hàng hoặc loại tiền tệ của tài khoản đã bị khóa")
b.para("Nếu ngân hàng gắn với tài khoản đã bị khóa ở Danh mục ngân hàng, khi mở cửa sổ Sửa bạn sẽ "
       "thấy:")
b.bullet("Ô Ngân hàng bị XOÁ TRẮNG kèm thông báo “Ngân hàng của tài khoản này đã bị khóa, vui lòng "
         "chọn ngân hàng khác”.")
b.bullet("Ô Chi nhánh cũng trống theo vì chi nhánh phụ thuộc ngân hàng.")
b.para("Loại tiền tệ bị khóa cũng xử lý tương tự, kèm thông báo “Loại tiền tệ của tài khoản này đã "
       "bị khóa, vui lòng chọn loại tiền tệ khác”.")
b.para("Đây là hành vi ĐÚNG, không phải mất dữ liệu: hệ thống bắt bạn chọn lại giá trị còn hiệu "
       "lực trước khi lưu. Nếu chỉ muốn xem thông tin cũ, hãy dùng cửa sổ Xem chi tiết (PHẦN 6) — "
       "ở đó tên ngân hàng cũ vẫn hiển thị đầy đủ.")

b.h2("4. Những điều nên biết")
b.bullet("Giữ nguyên số tài khoản của chính bản ghi đang sửa thì KHÔNG bị báo trùng.")
b.bullet("Sau khi lưu, cột Người cập nhật và Ngày cập nhật đổi theo bạn và thời điểm lưu.")
b.bullet("Đổi ô Trạng thái sang Khóa ngay trong cửa sổ Sửa cũng có tác dụng như bấm nút Khóa ngoài "
         "danh sách.")
b.bullet("Mọi thay đổi đều được ghi vào Lịch sử thay đổi kèm giá trị trước và sau, xem PHẦN 8. Bấm "
         "Lưu mà không sửa gì thì không phát sinh mốc lịch sử mới.")
b.bullet("Tài khoản đang Khóa không sửa được: nút Sửa bị ẩn, và nếu dữ liệu trên màn đã cũ (tài "
         "khoản vừa bị người khác khóa) thì hệ thống báo “Tài khoản ngân hàng đang bị khóa, không "
         "thể sửa”.")

# ============================================================================
b.h1("PHẦN 6: XEM CHI TIẾT TÀI KHOẢN NGÂN HÀNG")

b.h2("1. Cách mở")
b.para("Bấm vào chính số tài khoản ở cột “Số tài khoản” (chữ có gạch chân). Cửa sổ “Xem tài khoản "
       "ngân hàng” mở ra ngay, không chuyển sang trang khác. Cách này dùng được cả với tài khoản "
       "đang Khóa.")

b.image("10-xem-lich-su.png", "Cửa sổ Xem tài khoản ngân hàng, khối Lịch sử đã được mở")

b.h2("2. Nội dung cửa sổ Xem")
b.bullet("Toàn bộ ô thông tin ở chế độ chỉ đọc, không gõ sửa được.")
b.bullet("Ô Trạng thái hiển thị Hoạt động hoặc Khóa.")
b.bullet("Không có nút Lưu; chân cửa sổ chỉ có nút Đóng.")
b.bullet("Cuối cửa sổ là khối “Lịch sử” — bấm “Xem lịch sử” để mở ra ngay trong cửa sổ.")

b.h2("3. Điểm khác với cửa sổ Sửa")
b.para("Nếu ngân hàng của tài khoản đã bị khóa, cửa sổ Xem VẪN hiển thị đúng tên ngân hàng đó, còn "
       "cửa sổ Sửa thì để trống và bắt chọn lại. Lý do: tên ngân hàng được lưu kèm ngay trên bản "
       "ghi từ lúc tạo, nên tra cứu vẫn thấy; còn khi sửa thì hệ thống chỉ cho chọn danh mục đang "
       "còn hiệu lực.")

# ============================================================================
b.h1("PHẦN 7: KHÓA VÀ MỞ KHÓA TÀI KHOẢN")

b.h2("1. Khóa nghĩa là gì")
b.para("Màn hình này KHÔNG có chức năng xóa. Tài khoản ngân hàng không dùng nữa thì chuyển sang "
       "trạng thái Khóa: bản ghi vẫn nằm trong danh sách, vẫn xem được chi tiết và lịch sử, nhưng "
       "không sửa được và không nên dùng cho chứng từ mới.")

b.h2("2. Các bước khóa tài khoản")
b.bullet("Bước 1: Ở dòng cần khóa, bấm nút Khóa (biểu tượng ổ khoá).")
b.bullet("Bước 2: Hộp thoại “Xác nhận khóa” hiện ra, nêu rõ số tài khoản.")
b.bullet("Bước 3: Bấm nút “Khóa” để đồng ý, hoặc “Hủy” để bỏ qua.")

b.image("12-xac-nhan-khoa.png", "Hộp xác nhận khóa tài khoản ngân hàng")

b.para("Khóa xong hệ thống báo “Khóa thành công”; dòng đó chuyển sang nhãn Khóa màu đỏ và nút Sửa "
       "biến mất.")

b.h2("3. Mở khóa tài khoản")
b.bullet("Bước 1: Ở dòng đang Khóa, bấm nút Mở khóa (ổ khoá mở).")
b.bullet("Bước 2: Hộp thoại “Xác nhận mở khóa” hiện ra.")
b.bullet("Bước 3: Bấm “Mở khóa”. Hệ thống báo “Mở khóa thành công”, dòng trở lại nhãn Hoạt động và "
         "hiện lại nút Sửa.")

b.h2("4. Lưu ý")
b.bullet("Có hai cách đổi trạng thái cho cùng một kết quả: nút Khóa / Mở khóa ngoài danh sách, "
         "hoặc ô Trạng thái trong cửa sổ Sửa.")
b.bullet("Mọi lần khóa và mở khóa đều được ghi vào Lịch sử thay đổi kèm tên người thực hiện.")
b.bullet("Muốn xem nhanh các tài khoản đang khóa: chọn ô Trạng thái = Khóa ở khối bộ lọc.")
b.bullet("Nếu bấm Khóa mà hệ thống báo “Dữ liệu đã thay đổi, vui lòng tải lại” thì bản ghi vừa bị "
         "người khác thay đổi — hãy bấm Làm mới rồi thao tác lại.")

# ============================================================================
b.h1("PHẦN 8: XEM LỊCH SỬ THAY ĐỔI")

b.h2("1. Cách mở")
b.bullet("Cách 1: Bấm nút Lịch sử (biểu tượng đồng hồ) ở cột Hành động của dòng.")
b.bullet("Cách 2: Bấm số tài khoản để mở cửa sổ Xem, rồi bấm “Xem lịch sử” ở cuối cửa sổ.")

b.image("11-lich-su.png", "Cửa sổ Lịch sử thay đổi của một tài khoản ngân hàng")

b.h2("2. Đọc một mốc lịch sử")
b.para("Mỗi mốc gồm bốn phần, xếp từ trên xuống:")
b.bullet("Ngày giờ thực hiện.")
b.bullet("Tên hành động, có màu riêng: Tạo mới, Thay đổi thông tin, Khóa, Mở khóa.")
b.bullet("Người thực hiện, kèm mã nhân viên và phòng ban.")
b.bullet("Chi tiết thay đổi theo dạng “Tên trường: giá trị cũ → giá trị mới”.")
b.para("Các mốc xếp mới nhất ở trên cùng. Tài khoản chưa từng bị thay đổi sẽ hiện dòng “Chưa có "
       "lịch sử thao tác nào.”.")

b.h2("3. Những trường được theo dõi")
b.table([
    ["Trường", "Ghi chú"],
    ["Số tài khoản", "Ghi lại giá trị cũ và mới."],
    ["Chủ tài khoản", "Ghi theo giá trị đã in hoa."],
    ["Ngân hàng", "Ghi theo TÊN ngân hàng."],
    ["Chi nhánh", "Ghi theo tên chi nhánh."],
    ["Loại tiền tệ", "Ghi theo TÊN loại tiền tệ, không phải mã số — đổi tên danh mục sau này cũng "
                     "không làm sai lịch sử cũ."],
    ["Trạng thái", "Ghi bằng chữ: Hoạt động hoặc Khóa."],
])

b.h2("4. Lọc lịch sử")
b.para("Bấm nút “Bộ lọc” ở góc phải cửa sổ để lọc theo Loại hoạt động. Có đúng ba nhóm, dùng chung "
       "cho mọi màn danh mục của hệ thống:")
b.table([
    ["Nhóm", "Bao gồm những mốc nào"],
    ["Tạo mới", "Lần tạo bản ghi."],
    ["Thay đổi thông tin",
     "Các lần sửa: số tài khoản, chủ tài khoản, ngân hàng, chi nhánh, loại tiền tệ."],
    ["Thay đổi trạng thái", "Các lần Khóa và Mở khóa."],
])

# ============================================================================
b.h1("PHẦN 9: HƯỚNG DẪN THEO TỪNG QUYỀN")

b.h2("1. Người dùng có quyền “Quản lý danh mục tài khoản ngân hàng”")
b.para("Bạn nhìn thấy:")
b.bullet("Mục “Danh mục tài khoản ngân hàng” trong nhóm Danh mục của phân hệ Tài chính.")
b.bullet("Danh sách tài khoản ngân hàng của CÔNG TY MÌNH.")
b.bullet("Nút Tạo mới, nút Cấu hình cột và đầy đủ các nút Sửa / Khóa / Mở khóa / Lịch sử trên từng "
         "dòng.")
b.para("Bạn làm được toàn bộ thao tác mô tả từ PHẦN 1 đến PHẦN 8: tìm kiếm, tạo mới, sửa, xem chi "
       "tiết, khóa, mở khóa và xem lịch sử.")

b.h2("2. Người dùng KHÔNG có quyền này")
b.bullet("Mục menu Danh mục tài khoản ngân hàng không hiển thị.")
b.bullet("Gõ thẳng đường dẫn /finance/account-banks thì hệ thống từ chối, không xem được dữ liệu "
         "nào.")
b.para("Nếu công việc của bạn cần tra cứu tài khoản ngân hàng của công ty, hãy đề nghị quản trị "
       "cấp quyền “Quản lý danh mục tài khoản ngân hàng”. Lưu ý màn này chỉ có MỘT quyền, cấp "
       "quyền là cấp cả xem lẫn sửa — chưa tách riêng quyền chỉ xem.")

b.h2("3. Người dùng chưa được gắn công ty")
b.para("Có quyền nhưng hồ sơ nhân sự chưa gắn công ty thì danh sách hiện trống và khi bấm Lưu hệ "
       "thống báo “Tài khoản đăng nhập chưa gắn công ty, không thể thao tác”. Hãy báo bộ phận nhân "
       "sự bổ sung công ty cho hồ sơ rồi đăng nhập lại.")

b.h2("4. Câu hỏi thường gặp")

b.h3("4.1 Khai báo một tài khoản ngân hàng mới thì làm thế nào")
b.bullet("Bước 1: Vào Tài chính → Danh mục → Danh mục tài khoản ngân hàng, gõ số tài khoản vào ô "
         "tìm nhanh để chắc chắn chưa có.")
b.bullet("Bước 2: Bấm Tạo mới, nhập Số tài khoản, chọn Loại tiền tệ, nhập Chủ tài khoản.")
b.bullet("Bước 3: Chọn Ngân hàng rồi chọn Chi nhánh của ngân hàng đó.")
b.bullet("Bước 4: Để Trạng thái là Hoạt động rồi bấm Lưu.")

b.h3("4.2 Không thấy ngân hàng cần chọn trong danh sách")
b.para("Ngân hàng đó đang bị khóa ở màn Danh mục ngân hàng, hoặc chưa được khai báo. Hãy sang màn "
       "Danh mục chung → Ngân hàng để kiểm tra: nếu đang khóa thì mở khóa, nếu chưa có thì khai "
       "báo mới rồi quay lại.")

b.h3("4.3 Không thấy chi nhánh cần chọn")
b.para("Ô Chi nhánh chỉ liệt kê chi nhánh của ngân hàng đang chọn. Nếu danh sách trống, nghĩa là "
       "ngân hàng đó chưa khai chi nhánh nào — sang màn Danh mục ngân hàng, mở cửa sổ Chi nhánh "
       "của ngân hàng và thêm chi nhánh trước.")

b.h3("4.4 Hệ thống báo số tài khoản đã tồn tại nhưng tìm không thấy")
b.para("Số tài khoản không được trùng trên toàn hệ thống. Bản ghi trùng có thể thuộc CÔNG TY KHÁC "
       "nên bạn không nhìn thấy trong danh sách. Hãy kiểm tra lại số tài khoản, nếu chắc chắn đúng "
       "thì báo quản trị kiểm tra giúp.")

b.h3("4.5 Không sửa được một tài khoản")
b.para("Kiểm tra trạng thái của tài khoản đó: đang Khóa thì nút Sửa bị ẩn, phải Mở khóa trước. Nếu "
       "vẫn thấy nút Sửa mà bấm vào báo lỗi, nghĩa là tài khoản vừa bị người khác khóa — bấm Làm "
       "mới rồi thao tác lại.")

b.h3("4.6 Muốn xoá một tài khoản nhập nhầm")
b.para("Màn hình không có chức năng xóa. Cách xử lý: sửa lại cho đúng nếu tài khoản còn dùng, hoặc "
       "Khóa lại nếu không dùng nữa. Trường hợp bắt buộc phải xoá hẳn thì báo bộ phận kỹ thuật.")

b.h3("4.7 Danh sách thiếu tài khoản so với lúc trước")
b.para("Thường do bộ lọc còn giữ điều kiện cũ, hệ thống ghi nhớ trong 10 phút. Bấm “Làm mới” ở "
       "khối bộ lọc để xem lại toàn bộ danh sách.")

b.h3("4.8 Không biết ai đã sửa dữ liệu")
b.para("Bấm nút Lịch sử ở dòng đó. Cửa sổ liệt kê từng mốc kèm tên người thực hiện, thời điểm và "
       "giá trị trước - sau.")

b.finish()
