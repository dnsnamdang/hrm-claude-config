# -*- coding: utf-8 -*-
"""Sinh HDSD (Word) cho man 'Danh muc ngan hang' (/human/banks).

Bo cuc bam theo bo tai lieu mau cua team: .plans/gop-db/customer-docs/
(HDSD_Danh muc khach hang.docx + hdsd_noidung.py) — TONG QUAN gom ca bang quyen o muc 4,
cac PHAN chuc nang o giua, PHAN cuoi la "HUONG DAN THEO TUNG QUYEN" + cau hoi thuong gap.

⚠️ Tieu de dat la "TONG QUAN" (khong phai "TONG QUAN PHAN MEM") vi engine assert rang khong con
tieu de cua file khung trong output — file khung HDSD_MAU.docx dung dung chuoi "TONG QUAN PHAN MEM".

Anh chup that tren cong dev hrm-crm.eteksofts.com ngay 17/08/2026, 1440x900 -> banks_shots/
(thu muc anh CHI DE LOCAL, .gitignore da chan **/.plans/**/*_shots/).

Chay:  python .plans/gop-db/banks-cut-mysql2/gen_hdsd.py
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
    output=os.path.join(HERE, "HDSD_Danh muc ngan hang.docx"),
    shots_dir=os.path.join(HERE, "banks_shots"),
    cover_title="(Màn hình: Danh mục ngân hàng)",
    doc_title="HDSD - Danh mục ngân hàng",
)

# ============================================================================
b.h1("TỔNG QUAN")

b.h2("1. Thuật ngữ sử dụng trong tài liệu")
b.table([
    ["Thuật ngữ", "Giải thích"],
    ["Ngân hàng",
     "Một bản ghi trong danh mục, gồm mã, tên, tên viết tắt, tên giao dịch quốc tế, địa chỉ giao "
     "dịch và logo."],
    ["Chi nhánh",
     "Chi nhánh của một ngân hàng, gồm tên chi nhánh và tỉnh/thành phố. Chi nhánh luôn thuộc về "
     "đúng một ngân hàng, xem mục 9."],
    ["Trạng thái Hoạt động",
     "Ngân hàng đang dùng bình thường, sửa và xoá được."],
    ["Trạng thái Khóa",
     "Ngân hàng ngừng sử dụng nhưng vẫn giữ lại dữ liệu. Ngân hàng đang khóa không sửa và không "
     "xoá được, xem mục 7."],
    ["Tra cứu",
     "Chức năng lấy sẵn thông tin ngân hàng chuẩn (mã, tên, tên viết tắt, logo) để điền nhanh vào "
     "form, đỡ phải gõ tay."],
    ["Tuỳ chỉnh cột",
     "Chức năng cho mỗi người tự chọn cột nào hiện trên bảng và thứ tự các cột."],
    ["Lịch sử thay đổi",
     "Nhật ký ghi lại ai đã tạo, sửa, khóa, mở khóa hay xoá một ngân hàng."],
])

b.h2("2. Cập nhật tài liệu")
b.table([
    ["Phiên bản", "Ngày", "Người cập nhật", "Nội dung"],
    ["1.0", "07/08/2026", "@khoipv", "Bản đầu tiên của bộ tài liệu màn Danh mục ngân hàng."],
    ["2.0", "17/08/2026", "@khoipv",
     "Viết lại theo giao diện mới: cột Hành động chốt cuối bảng, nút Tuỳ chỉnh cột, popup Lịch sử "
     "thay đổi, cửa sổ Xem chi tiết. Chụp lại toàn bộ ảnh trên cổng dev."],
])

b.h2("3. Giới thiệu chung")
b.para("Danh mục ngân hàng là nơi khai báo và quản lý toàn bộ ngân hàng cùng chi nhánh của chúng, "
       "dùng chung cho cả hệ thống. Từ màn hình này, người dùng tra cứu ngân hàng, thêm ngân hàng "
       "mới, cập nhật thông tin, khóa những ngân hàng không còn giao dịch, quản lý danh sách chi "
       "nhánh và tra lại lịch sử thay đổi của từng ngân hàng.")
b.para("Dữ liệu khai báo ở đây sẽ xuất hiện tại các ô chọn Ngân hàng và Chi nhánh ở những màn khác, "
       "cụ thể:")
b.bullet("Hồ sơ nhân sự — phần tài khoản ngân hàng và tài khoản uỷ quyền của nhân viên.")
b.bullet("Danh mục tài khoản ngân hàng của công ty, phân hệ Tài chính.")
b.para("Vì vậy khai báo sai ở màn này sẽ kéo theo sai ở các màn kia. Đặc biệt lưu ý: mỗi ngân hàng "
       "chỉ nên khai báo MỘT LẦN — hệ thống không cho trùng mã và không cho trùng tên.")
b.para("Đường dẫn truy cập:")
b.bullet("Menu: Phân hệ Danh mục chung → Ngân hàng.")
b.bullet("Hoặc gõ thẳng đường dẫn /human/banks vào thanh địa chỉ trình duyệt.")

b.h2("4. Quyền và phạm vi dữ liệu")

b.h3("4.1 Bảng quyền của màn hình")
b.table([
    ["Tên quyền", "Cho phép làm gì", "Nút / cửa sổ tương ứng", "Ghi chú"],
    ["(Màn hình không có quyền riêng)",
     "Xem danh sách, tìm kiếm, tạo mới, sửa, xem chi tiết, khóa, mở khóa, xoá, quản lý chi nhánh, "
     "xem lịch sử.",
     "Toàn bộ nút trên màn hình.",
     "Chỉ cần đã đăng nhập hệ thống là dùng được đầy đủ."],
])
b.para("Đây là hiện trạng của phần mềm, không phải do tài khoản của bạn được cấp nhiều quyền: màn "
       "hình chưa khai báo quyền riêng nào, mục menu cũng không lọc theo quyền. Hướng dẫn chi tiết "
       "cho từng nhóm người dùng xem ở PHẦN 11.")

b.h3("4.2 Phạm vi dữ liệu")
b.bullet("Danh mục KHÔNG chia theo công ty, phòng ban hay bộ phận: mọi người nhìn thấy cùng một "
         "danh sách ngân hàng.")
b.bullet("Ngân hàng đang Khóa vẫn nằm trong danh sách với nhãn Khóa, không bị ẩn đi.")
b.bullet("Người chưa đăng nhập hoặc đã hết phiên bị đưa về màn Đăng nhập và không xem được dữ liệu "
         "nào.")

# ============================================================================
b.h1("PHẦN 1: TRUY CẬP VÀ BỐ CỤC MÀN HÌNH")

b.h2("1. Truy cập màn hình")
b.bullet("Bước 1: Đăng nhập hệ thống.")
b.bullet("Bước 2: Chọn phân hệ “Danh mục chung” ở góc trên bên trái.")
b.bullet("Bước 3: Trên menu bên trái, bấm mục “Ngân hàng”.")
b.para("Màn hình mở ra với tiêu đề “Danh mục ngân hàng”, danh sách hiển thị 10 dòng đầu tiên.")

b.image("01-danh-sach.png", "Màn hình Danh mục ngân hàng khi mới truy cập")

b.h2("2. Bố cục màn hình")
b.bullet("Khối trên — “Bộ lọc danh sách”: ô tìm nhanh, ô Tên giao dịch quốc tế, ô Trạng thái, nút "
         "Tìm kiếm và nút Làm mới. Ba ô lọc bày sẵn trên một hàng ngang nên màn này KHÔNG có nút "
         "“Tìm kiếm nâng cao”.")
b.bullet("Khối dưới — bảng “Danh mục ngân hàng”: góc phải phía trên có nút Tạo mới và nút Tuỳ chỉnh "
         "cột hiển thị; cuối bảng là dòng thống kê và phần phân trang.")

b.image("02-cot-hanh-dong.png", "Bảng danh sách khi thu gọn menu bên trái — thấy đủ cột Hành động")

b.h2("3. Các cột của bảng danh sách")
b.para("Bảng có 13 cột khả dụng, khi mới dùng hệ thống hiển thị sẵn 7 cột. Các cột còn lại bật thêm "
       "ở cửa sổ Tuỳ chỉnh cột, xem PHẦN 3.")
b.table([
    ["Cột", "Hiện sẵn", "Nội dung"],
    ["STT", "Có", "Số thứ tự tính theo trang đang xem. Trang 2 với 10 dòng/trang bắt đầu từ 11."],
    ["Mã ngân hàng", "Có", "Mã ngân hàng, hiển thị dạng đường dẫn. Bấm vào là mở cửa sổ Xem chi tiết."],
    ["Tên ngân hàng", "Có", "Tên đầy đủ của ngân hàng, tự xuống dòng khi dài."],
    ["Logo", "Không", "Ảnh logo ngân hàng. Chưa có logo thì hiện dấu gạch ngang."],
    ["Tên viết tắt", "Không", "Tên gọi tắt, ví dụ Vietcombank, ABBANK."],
    ["Tên giao dịch quốc tế", "Không", "Tên tiếng Anh dùng trong giao dịch quốc tế."],
    ["Địa chỉ giao dịch", "Không", "Địa chỉ giao dịch của ngân hàng."],
    ["Chi nhánh", "Không", "Số chi nhánh của ngân hàng. Bấm vào con số là mở ngay cửa sổ Chi nhánh."],
    ["Người tạo", "Có", "Người đã tạo bản ghi."],
    ["Ngày tạo", "Có", "Ngày giờ tạo bản ghi, dạng ngày/tháng/năm giờ:phút."],
    ["Người sửa", "Không", "Người sửa gần nhất. Bản ghi chưa từng sửa thì ô này để trống."],
    ["Ngày cập nhật", "Không", "Ngày giờ sửa gần nhất."],
    ["Trạng thái", "Có", "Nhãn Hoạt động màu xanh hoặc Khóa màu đỏ."],
    ["Hành động", "Có", "Các nút thao tác của dòng, luôn nằm ở cuối bảng."],
])
b.para("Ô nào chưa có dữ liệu sẽ hiển thị dấu gạch ngang (—). Đây là cách hiển thị bình thường, "
       "không phải lỗi.")

b.h2("4. Cột Hành động")
b.para("Cột Hành động hiển thị tối đa 2 nút chính, các thao tác còn lại nằm trong menu ba chấm (⋮). "
       "Nút nào không dùng được sẽ bị ẨN HẲN chứ không hiện rồi làm mờ — vì vậy hai dòng khác nhau "
       "có thể có số nút khác nhau, đó là bình thường.")

b.image("13-menu-hanh-dong.png", "Menu ba chấm trên cột Hành động, chứa thao tác Chi nhánh và Lịch sử")

b.table([
    ["Nút", "Khi nào hiển thị", "Công dụng"],
    ["Sửa (bút chì)", "Ngân hàng đang ở trạng thái Hoạt động.",
     "Mở cửa sổ Sửa ngân hàng, xem PHẦN 5."],
    ["Xóa (thùng rác đỏ)", "Ngân hàng đang Hoạt động VÀ chưa được sử dụng ở nơi nào khác.",
     "Xoá hẳn ngân hàng cùng toàn bộ chi nhánh, xem PHẦN 8."],
    ["Khóa (ổ khoá)", "Ngân hàng đang Hoạt động.",
     "Chuyển ngân hàng sang trạng thái Khóa, xem PHẦN 7."],
    ["Mở khóa (ổ khoá mở)", "Ngân hàng đang Khóa.",
     "Đưa ngân hàng trở lại Hoạt động, xem PHẦN 7."],
    ["Chi nhánh", "Luôn hiển thị, nằm trong menu ba chấm.",
     "Mở cửa sổ quản lý chi nhánh của ngân hàng, xem PHẦN 9."],
    ["Lịch sử", "Luôn hiển thị, nằm trong menu ba chấm.",
     "Mở cửa sổ Lịch sử thay đổi của ngân hàng, xem PHẦN 10."],
])
b.para("Ghi nhớ nhanh: ngân hàng đang KHÓA chỉ còn Mở khóa, Chi nhánh và Lịch sử. Ngân hàng đã được "
       "dùng ở hồ sơ nhân sự hoặc ở danh mục tài khoản ngân hàng công ty thì KHÔNG còn nút Xóa.")

b.h2("5. Phân trang")
b.bullet("Dòng bên trái phía dưới bảng ghi “Hiển thị 1–10 / 26”: đang xem dòng thứ 1 đến 10 trong "
         "tổng số 26 ngân hàng khớp bộ lọc.")
b.bullet("Ô “Số dòng/trang” cho chọn 5, 10, 20, 50 hoặc 100 dòng, mặc định là 10.")
b.bullet("Đổi số dòng/trang thì danh sách quay về trang 1.")
b.bullet("Các nút phân trang gồm: về trang đầu, trang trước, số trang, trang sau, trang cuối.")

# ============================================================================
b.h1("PHẦN 2: TÌM KIẾM VÀ LỌC DANH SÁCH")

b.image("03-tim-kiem.png", "Kết quả sau khi tìm nhanh theo từ khoá “Vietcom”")

b.h2("1. Tìm kiếm nhanh")
b.para("Ô đầu tiên có dòng gợi ý “Tìm theo mã, tên ngân hàng...”. Ô này quét đồng thời cả Mã ngân "
       "hàng và Tên ngân hàng.")
b.bullet("Gõ một phần chuỗi là đủ, kể cả phần nằm ở giữa: gõ “Sài Gòn” vẫn tìm được “Ngân hàng "
         "Thương mại Cổ phần Sài Gòn - Hà Nội”.")
b.bullet("Không phân biệt chữ hoa chữ thường.")
b.bullet("PHẢI bấm nút Tìm kiếm hoặc nhấn phím Enter thì danh sách mới lọc; chỉ gõ thôi thì danh "
         "sách chưa đổi.")
b.bullet("Bấm dấu x ở cuối ô để xoá nhanh từ khoá.")

b.h2("2. Lọc theo Tên giao dịch quốc tế")
b.para("Nhập một phần tên giao dịch quốc tế vào ô thứ hai. Chỉ những ngân hàng ĐÃ khai tên giao "
       "dịch quốc tế và chứa chuỗi vừa nhập mới hiện ra; ngân hàng bỏ trống trường này sẽ không "
       "xuất hiện.")

b.h2("3. Lọc theo Trạng thái")
b.para("Ô thứ ba cho chọn “Hoạt động” hoặc “Khóa”. Để trống là lấy tất cả, bấm dấu x trong ô để bỏ "
       "lựa chọn.")
b.para("Khác với ô tìm nhanh, hai ô Tên giao dịch quốc tế và Trạng thái tự lọc lại ngay khi bạn "
       "thay đổi, không cần bấm Tìm kiếm.")

b.h2("4. Kết hợp nhiều điều kiện")
b.para("Các điều kiện được kết hợp theo kiểu “và”: kết quả phải thoả mãn đồng thời tất cả ô đã "
       "nhập. Ví dụ gõ “trang” ở ô tìm nhanh và chọn Trạng thái = Khóa thì chỉ ra những ngân hàng "
       "vừa có chữ “trang” vừa đang bị khóa.")

b.h2("5. Nút Làm mới")
b.para("Bấm “Làm mới” để xoá sạch cả ba ô lọc và tải lại toàn bộ danh sách. Nên dùng nút này trước "
       "khi bắt đầu một việc mới, vì hệ thống có ghi nhớ bộ lọc, xem mục 6.")

b.h2("6. Hệ thống ghi nhớ bộ lọc trong 10 phút")
b.para("Nếu bạn đang lọc rồi chuyển sang màn khác và quay lại trong vòng 10 phút, hệ thống giữ "
       "nguyên điều kiện lọc cũ. Đây là chủ ý để bạn không phải nhập lại. Nếu thấy danh sách "
       "“thiếu” ngân hàng, hãy kiểm tra lại các ô lọc rồi bấm Làm mới.")

b.h2("7. Sắp xếp theo cột")
b.para("Các cột Mã ngân hàng, Tên ngân hàng, Ngày tạo và Ngày cập nhật có biểu tượng mũi tên ở "
       "tiêu đề để đổi thứ tự sắp xếp.")
b.para("Lưu ý: ở bản đang chạy, bấm vào mũi tên chỉ đổi biểu tượng mà thứ tự các dòng CHƯA đổi — "
       "danh sách luôn xếp theo bản ghi mới nhất trước. Bộ phận kỹ thuật đã ghi nhận và sẽ xử lý. "
       "Trong lúc chờ, hãy dùng ô tìm kiếm để thu hẹp danh sách thay vì dựa vào sắp xếp.")

# ============================================================================
b.h1("PHẦN 3: TUỲ CHỈNH CỘT HIỂN THỊ")

b.image("04-cau-hinh-cot.png", "Cửa sổ Tuỳ chỉnh cột — cột STT và Mã ngân hàng có biểu tượng ổ khoá")

b.h2("1. Mở cửa sổ tuỳ chỉnh cột")
b.para("Bấm nút biểu tượng cột nằm ngay bên phải nút Tạo mới. Cửa sổ “Tuỳ chỉnh cột” hiện ra, liệt "
       "kê đủ 13 cột; cột nào đang hiển thị thì được tích sẵn.")

b.h2("2. Bật và tắt cột")
b.bullet("Tích vào ô vuông đầu dòng để bật cột, bỏ tích để tắt.")
b.bullet("Ba cột STT, Mã ngân hàng và Hành động có biểu tượng ổ khoá, không tắt được vì đó là cột "
         "định danh và cột thao tác.")

b.h2("3. Đổi thứ tự cột")
b.para("Dùng chuột kéo biểu tượng ba gạch ở cuối mỗi dòng lên hoặc xuống để đổi vị trí cột trên "
       "bảng.")

b.h2("4. Lưu hoặc bỏ thay đổi")
b.bullet("Bấm “Lưu”: cửa sổ đóng, bảng vẽ lại theo lựa chọn mới. Cấu hình được ghi nhớ theo tài "
         "khoản của bạn, lần sau vào lại vẫn giữ nguyên và không ảnh hưởng tới người khác.")
b.bullet("Bấm “Đóng”: bỏ mọi thay đổi vừa chỉnh, bảng giữ nguyên như cũ.")

# ============================================================================
b.h1("PHẦN 4: TẠO MỚI NGÂN HÀNG")

b.h2("1. Mở cửa sổ Tạo mới")
b.para("Bấm nút “Tạo mới” ở góc phải phía trên bảng. Cửa sổ “Tạo ngân hàng” mở ra ngay trên màn "
       "hình danh sách.")

b.image("05-tao-moi.png", "Cửa sổ Tạo ngân hàng khi vừa mở — mọi ô còn trống")

b.h2("2. Các trường trong cửa sổ Tạo ngân hàng")
b.table([
    ["Trường", "Kiểu nhập", "Bắt buộc", "Giá trị điền sẵn", "Mô tả"],
    ["Gợi ý", "Ô nhập chữ", "Không", "Trống",
     "Từ khoá để tra cứu ngân hàng chuẩn. Nhập xong bấm nút Tra cứu bên cạnh, xem mục 4."],
    ["Mã ngân hàng", "Ô nhập chữ", "Có", "Trống",
     "Mã ngắn gọn, phải là duy nhất trong toàn hệ thống. Ví dụ: VCB, BIDV, ABB."],
    ["Tên ngân hàng", "Ô nhập chữ", "Có", "Trống",
     "Tên đầy đủ, phải là duy nhất trong toàn hệ thống."],
    ["Tên viết tắt", "Ô nhập chữ", "Có", "Trống",
     "Tên gọi tắt thường dùng, ví dụ Vietcombank. Không bắt buộc duy nhất."],
    ["Tên giao dịch quốc tế", "Ô nhập chữ", "Không", "Trống",
     "Tên tiếng Anh dùng khi giao dịch quốc tế."],
    ["Địa chỉ giao dịch", "Ô nhập chữ", "Không", "Trống",
     "Địa chỉ trụ sở hoặc địa chỉ giao dịch."],
    ["Logo", "Tải ảnh lên", "Không", "Chưa có logo",
     "Chỉ nhận ảnh .jpg, .jpeg, .png và tối đa 5 MB."],
])

b.h2("3. Giá trị điền sẵn khi tạo mới")
b.bullet("Tất cả các ô đều TRỐNG.")
b.bullet("Khung Logo hiện chữ “Chưa có logo”.")
b.bullet("KHÔNG có ô Trạng thái: ngân hàng mới tạo luôn ở trạng thái “Hoạt động”.")
b.bullet("Người tạo và Ngày tạo do hệ thống tự ghi theo người đang đăng nhập và thời điểm bấm Lưu, "
         "bạn không nhập được hai thông tin này.")

b.h2("4. Điền nhanh bằng chức năng Tra cứu")
b.para("Thay vì gõ tay, bạn có thể lấy sẵn thông tin ngân hàng chuẩn:")
b.bullet("Bước 1: Gõ một phần tên hoặc mã ngân hàng vào ô “Gợi ý”, ví dụ: vietcom.")
b.bullet("Bước 2: Bấm nút “Tra cứu”.")
b.bullet("Bước 3: Cửa sổ “Thông tin ngân hàng” mở ra với danh sách ngân hàng chuẩn đã lọc theo từ "
         "khoá.")
b.bullet("Bước 4: Bấm vào dòng mong muốn.")

b.image("08-tra-cuu.png", "Cửa sổ Thông tin ngân hàng — bấm vào một dòng để điền nhanh")

b.para("Sau khi bấm chọn, cửa sổ tra cứu đóng lại và bốn thông tin Mã ngân hàng, Tên ngân hàng, Tên "
       "viết tắt, Logo được điền sẵn vào form. Bạn vẫn phải bấm “Lưu” thì ngân hàng mới thực sự "
       "được tạo. Danh sách trong cửa sổ tra cứu là danh mục ngân hàng chuẩn bên ngoài, không phải "
       "danh mục của đơn vị bạn.")

b.h2("5. Tải logo lên")
b.bullet("Bấm nút “Tải ảnh lên”, chọn tệp ảnh trên máy.")
b.bullet("Ảnh hợp lệ sẽ hiện ngay trong khung xem trước, kèm nút “Xóa ảnh” để bỏ ảnh vừa chọn.")
b.bullet("Chọn tệp không phải ảnh: hệ thống báo đỏ “File không hợp lệ”.")
b.bullet("Chọn ảnh lớn hơn 5 MB: hệ thống báo đỏ “Dung lượng tối đa: 5MB”.")
b.bullet("Rê chuột vào biểu tượng chấm than cạnh nhãn Logo để xem lại quy định định dạng.")

b.h2("6. Lưu bản ghi")
b.table([
    ["Nút", "Kết quả"],
    ["Lưu", "Ghi ngân hàng mới, hiện thông báo “Đã lưu thành công!”, đóng cửa sổ và làm mới danh "
            "sách. Ngân hàng vừa tạo nằm ở đầu danh sách với trạng thái Hoạt động."],
    ["Lưu và tiếp tục", "Ghi ngân hàng mới nhưng GIỮ CỬA SỔ MỞ và xoá trắng các ô, để bạn nhập tiếp "
                        "ngân hàng kế theo mà không phải bấm Tạo mới lại."],
    ["Đóng", "Thoát khỏi cửa sổ, không ghi gì."],
])

b.h2("7. Các lỗi thường gặp khi lưu")

b.image("06-loi-bat-buoc.png", "Bấm Lưu khi chưa nhập gì — hệ thống chặn ngay tại ô Tên ngân hàng")

b.image("07-loi-trung-ma.png",
        "Thiếu Mã ngân hàng, thiếu Tên viết tắt và trùng Tên ngân hàng — lỗi hiện đỏ dưới từng ô")

b.table([
    ["Thông báo", "Nguyên nhân", "Cách xử lý"],
    ["Bắt buộc phải nhập (dưới ô Tên ngân hàng)", "Chưa nhập tên ngân hàng.",
     "Nhập tên ngân hàng rồi bấm Lưu lại."],
    ["Bắt buộc phải nhập (dưới ô Mã ngân hàng hoặc Tên viết tắt)",
     "Chưa nhập mã hoặc tên viết tắt.",
     "Nhập nốt ô còn thiếu. Lỗi này hiện sau khi hệ thống kiểm tra."],
    ["Mã ngân hàng này đã tồn tại", "Đã có ngân hàng khác dùng mã này.",
     "Đóng cửa sổ, tìm mã đó trên danh sách để kiểm tra. Nếu đã có rồi thì không tạo mới nữa."],
    ["Tên ngân hàng này đã tồn tại", "Đã có ngân hàng khác trùng tên.",
     "Kiểm tra lại danh sách, tránh tạo trùng."],
    ["Vui lòng kiểm tra lại thông tin",
     "Thông báo chung, luôn đi kèm ít nhất một lỗi đỏ ở ô nào đó.",
     "Cuộn trong cửa sổ để tìm ô có chữ đỏ."],
])
b.para("Khi có lỗi, cửa sổ KHÔNG đóng và dữ liệu bạn đã nhập vẫn còn nguyên — chỉ cần sửa ô báo đỏ "
       "rồi bấm Lưu lại.")

b.h2("8. Lưu ý khi đóng cửa sổ đang nhập dở")
b.para("Theo thiết kế, đóng cửa sổ khi đang nhập dở thì hệ thống phải hỏi lại “Thông tin chưa lưu”. "
       "Trên bản đang chạy, cửa sổ đóng thẳng và dữ liệu đang nhập bị mất. Bộ phận kỹ thuật đã ghi "
       "nhận. Vì vậy hãy cẩn thận với nút “Đóng” và dấu × khi đã nhập nhiều thông tin.")

# ============================================================================
b.h1("PHẦN 5: SỬA NGÂN HÀNG")

b.h2("1. Mở cửa sổ Sửa")
b.para("Bấm nút Sửa, biểu tượng bút chì, ở cột Hành động của dòng cần sửa. Nút này chỉ hiển thị với "
       "ngân hàng đang ở trạng thái Hoạt động; ngân hàng đang Khóa phải mở khóa trước, xem PHẦN 7.")

b.image("10-sua.png", "Cửa sổ Sửa ngân hàng với dữ liệu đã có sẵn")

b.h2("2. Điểm khác so với cửa sổ Tạo mới")
b.bullet("Tiêu đề là “Sửa ngân hàng”.")
b.bullet("Các ô đã điền sẵn thông tin hiện tại, khung Logo hiện logo đang dùng.")
b.bullet("Chân cửa sổ chỉ còn hai nút “Lưu” và “Đóng”, KHÔNG có “Lưu và tiếp tục”.")

b.h2("3. Các bước sửa")
b.bullet("Bước 1: Bấm nút Sửa ở dòng cần chỉnh.")
b.bullet("Bước 2: Sửa các ô cần thiết. Quy định bắt buộc và quy định không trùng giống hệt khi tạo "
         "mới.")
b.bullet("Bước 3: Muốn đổi logo thì bấm “Tải ảnh lên” và chọn ảnh mới, hoặc bấm “Xóa ảnh” để bỏ "
         "logo.")
b.bullet("Bước 4: Bấm “Lưu”. Hệ thống báo “Đã lưu thành công!”, đóng cửa sổ và làm mới danh sách.")

b.h2("4. Những điều nên biết")
b.bullet("Giữ nguyên mã và tên của chính ngân hàng đang sửa thì KHÔNG bị báo trùng.")
b.bullet("Sau khi lưu, cột Người sửa và Ngày cập nhật được cập nhật theo bạn và thời điểm lưu.")
b.bullet("Mọi thay đổi thông tin đều được ghi vào Lịch sử thay đổi kèm giá trị trước và sau, xem "
         "PHẦN 10. Riêng việc đổi logo KHÔNG được ghi lịch sử.")
b.bullet("Bấm Lưu mà không sửa gì thì vẫn báo thành công nhưng lịch sử không phát sinh mốc mới.")
b.bullet("Sửa mã hoặc tên ngân hàng ở đây sẽ ảnh hưởng tới mọi màn đang dùng ngân hàng đó, vì các "
         "màn kia lấy trực tiếp dữ liệu từ danh mục này.")

# ============================================================================
b.h1("PHẦN 6: XEM CHI TIẾT NGÂN HÀNG")

b.h2("1. Cách mở")
b.para("Bấm vào chính mã ngân hàng ở cột “Mã ngân hàng”, chữ có gạch chân. Cửa sổ “Xem ngân hàng” "
       "mở ra ngay, không chuyển sang trang khác. Cách này dùng được cả với ngân hàng đang Khóa.")

b.image("12-xem-lich-su.png", "Cửa sổ Xem ngân hàng, khối Lịch sử đã được mở")

b.h2("2. Nội dung cửa sổ Xem")
b.bullet("Toàn bộ ô thông tin ở chế độ chỉ đọc, không gõ sửa được.")
b.bullet("Có thêm ô “Trạng thái” hiển thị Hoạt động hoặc Khoá.")
b.bullet("Khung Logo chỉ để xem, không có nút Tải ảnh lên hay Xóa ảnh.")
b.bullet("Không có khối Gợi ý / Tra cứu và không có nút Lưu.")
b.bullet("Cuối cửa sổ là khối “Lịch sử” — bấm “Xem lịch sử” để mở ra ngay trong cửa sổ.")

b.h2("3. Khối Lịch sử trong cửa sổ Xem")
b.para("Nội dung khối này giống hệt cửa sổ Lịch sử thay đổi mô tả ở PHẦN 10. Khi mở ra có thêm nút "
       "“Làm mới” để tải lại và nút “Thu gọn” để đóng khối. Ngân hàng chưa từng bị thay đổi sẽ hiện "
       "dòng “Chưa có lịch sử thao tác nào.”.")

b.h2("4. Đóng cửa sổ")
b.para("Bấm “Đóng” hoặc dấu × ở góc phải. Sau khi đóng, bạn có thể bấm ngay nút Sửa của cùng dòng "
       "đó để chuyển sang chế độ chỉnh sửa.")

# ============================================================================
b.h1("PHẦN 7: KHÓA VÀ MỞ KHÓA NGÂN HÀNG")

b.h2("1. Khóa nghĩa là gì")
b.para("Khóa dùng khi đơn vị ngừng giao dịch với một ngân hàng nhưng vẫn muốn giữ lại dữ liệu cũ. "
       "Ngân hàng bị khóa vẫn nằm trong danh sách, vẫn xem được lịch sử và chi nhánh, nhưng không "
       "sửa và không xoá được.")

b.h2("2. Các bước khóa ngân hàng")
b.bullet("Bước 1: Ở dòng cần khóa, bấm nút Khóa, biểu tượng ổ khoá.")
b.bullet("Bước 2: Hộp thoại “Xác nhận khóa” hiện ra, nêu rõ tên ngân hàng.")
b.bullet("Bước 3: Bấm nút “Khóa” để đồng ý, hoặc “Hủy” để bỏ qua.")

b.image("18-xac-nhan-khoa.png", "Hộp xác nhận khóa ngân hàng")

b.para("Khóa xong hệ thống báo “Khoá thành công”; dòng đó chuyển sang nhãn Khóa màu đỏ và chỉ còn "
       "các nút Mở khóa, Chi nhánh, Lịch sử.")

b.h2("3. Mở khóa ngân hàng")
b.bullet("Bước 1: Ở dòng đang Khóa, bấm nút Mở khóa, biểu tượng ổ khoá mở.")
b.bullet("Bước 2: Hộp thoại “Xác nhận mở khóa” hiện ra.")
b.bullet("Bước 3: Bấm “Mở khóa”. Hệ thống báo “Mở khoá thành công”, dòng trở lại nhãn Hoạt động và "
         "hiện lại nút Sửa.")

b.h2("4. Lưu ý")
b.bullet("Khóa KHÔNG bị chặn dù ngân hàng đang được sử dụng ở hồ sơ nhân sự, khác với Xóa. Đây là "
         "chủ ý: khóa chỉ ngăn dùng tiếp, không làm mất dữ liệu đã ghi.")
b.bullet("Mọi lần khóa và mở khóa đều được ghi vào Lịch sử thay đổi kèm tên người thực hiện.")
b.bullet("Muốn xem nhanh các ngân hàng đang khóa: chọn ô Trạng thái = Khóa ở khối bộ lọc.")

# ============================================================================
b.h1("PHẦN 8: XÓA NGÂN HÀNG")

b.h2("1. Điều kiện được xoá")
b.para("Nút Xóa, biểu tượng thùng rác đỏ, chỉ hiển thị khi ngân hàng thoả mãn ĐỒNG THỜI hai điều "
       "kiện:")
b.bullet("Đang ở trạng thái Hoạt động; ngân hàng đang Khóa không có nút Xóa.")
b.bullet("Chưa được sử dụng ở nơi nào khác — tức chưa được chọn ở tài khoản ngân hàng hoặc tài "
         "khoản uỷ quyền của nhân viên nào, và chưa được dùng trong Danh mục tài khoản ngân hàng "
         "của công ty.")
b.para("Nếu không thấy nút Xóa ở một dòng, nghĩa là ngân hàng đó rơi vào một trong hai trường hợp "
       "trên chứ không phải bạn thiếu quyền.")

b.h2("2. Các bước xoá")
b.bullet("Bước 1: Bấm nút Xóa ở dòng cần xoá.")
b.bullet("Bước 2: Hộp thoại “Xác nhận xóa” hiện ra kèm tên ngân hàng.")
b.bullet("Bước 3: Bấm “Xóa” để đồng ý, hoặc “Hủy” để bỏ qua.")

b.image("19-xac-nhan-xoa.png", "Hộp xác nhận xoá ngân hàng")

b.para("Xoá xong hệ thống báo “Xoá ngân hàng thành công” và dòng đó biến mất khỏi danh sách.")

b.h2("3. Cảnh báo quan trọng")
b.bullet("Xoá ngân hàng sẽ xoá theo TOÀN BỘ chi nhánh của ngân hàng đó. Thao tác này không khôi "
         "phục lại được từ giao diện.")
b.bullet("Nếu chỉ muốn ngừng sử dụng, hãy dùng Khóa ở PHẦN 7 thay vì Xóa.")
b.bullet("Trường hợp ngân hàng đang được dùng ở nơi khác mà vẫn cố xoá, hệ thống từ chối và báo "
         "“Không thể xóa bản ghi, ngân hàng đang được sử dụng trên hệ thống”.")
b.bullet("Muốn xoá một ngân hàng đang được dùng: trước hết phải đổi ngân hàng ở các hồ sơ nhân sự "
         "và ở danh mục tài khoản ngân hàng công ty đang tham chiếu tới nó, sau đó quay lại màn này "
         "bấm Làm mới thì nút Xóa sẽ hiện ra.")

# ============================================================================
b.h1("PHẦN 9: QUẢN LÝ CHI NHÁNH NGÂN HÀNG")

b.h2("1. Mở cửa sổ Chi nhánh")
b.para("Có hai cách:")
b.bullet("Cách 1: Mở menu ba chấm ở cột Hành động của dòng, chọn “Chi nhánh”.")
b.bullet("Cách 2: Bật cột “Chi nhánh” ở cửa sổ Tuỳ chỉnh cột (PHẦN 3), rồi bấm thẳng vào con số ở "
         "cột đó.")

b.image("15-chi-nhanh.png", "Cửa sổ Chi nhánh ngân hàng của BIDV")

b.h2("2. Nội dung cửa sổ")
b.bullet("Hàng trên: ô lọc “Tỉnh/Thành phố”, ô lọc “Tên chi nhánh”, nút Tìm kiếm, nút Làm mới.")
b.bullet("Nút “Tạo mới” nằm bên phải, ngay trên bảng.")
b.bullet("Bảng gồm 4 cột: STT, Tên chi nhánh, Tỉnh/TP, Hành động. Danh sách dài thì cuộn trong "
         "khung, dòng tiêu đề luôn dính ở trên.")
b.bullet("Mỗi dòng có 2 nút: Sửa (bút chì) và Xóa (thùng rác).")

b.h2("3. Lọc danh sách chi nhánh")
b.bullet("Chọn Tỉnh/Thành phố để xem chi nhánh của một tỉnh.")
b.bullet("Gõ một phần tên vào ô Tên chi nhánh rồi bấm Tìm kiếm, hoặc nhấn Enter trong ô đó.")
b.bullet("Bấm “Làm mới” để xoá hai ô lọc và xem lại toàn bộ chi nhánh của ngân hàng.")

b.h2("4. Thêm chi nhánh")
b.para("Bấm nút “Tạo mới” trong cửa sổ Chi nhánh. Cửa sổ “Thêm chi nhánh ngân hàng” mở ra.")

b.image("16-them-chi-nhanh.png", "Cửa sổ Thêm chi nhánh ngân hàng")

b.table([
    ["Trường", "Kiểu nhập", "Bắt buộc", "Giá trị điền sẵn", "Mô tả"],
    ["Tên chi nhánh ngân hàng", "Ô nhập chữ", "Có", "Trống",
     "Tên chi nhánh, ví dụ “CN Tràng Tiền”. Không được trùng với chi nhánh khác CỦA CÙNG ngân hàng."],
    ["Tỉnh/Thành phố", "Ô chọn từ danh sách", "Có", "Trống",
     "Chọn tỉnh/thành nơi đặt chi nhánh. Có thể gõ để tìm nhanh trong danh sách."],
])
b.para("Chân cửa sổ có ba nút: “Lưu” ghi rồi đóng, “Lưu và tiếp tục” ghi rồi xoá trắng để nhập chi "
       "nhánh kế tiếp, và “Đóng”.")
b.para("Lưu xong hệ thống báo “Đã lưu thành công!”, danh sách chi nhánh cập nhật ngay và con số ở "
       "cột Chi nhánh ngoài danh sách tăng thêm 1.")

b.h2("5. Sửa chi nhánh")
b.bullet("Bấm nút Sửa, biểu tượng bút chì, ở dòng chi nhánh cần chỉnh.")
b.bullet("Cửa sổ “Sửa chi nhánh ngân hàng” mở ra với hai ô đã điền sẵn; chân cửa sổ chỉ có “Lưu” và "
         "“Đóng”.")
b.bullet("Đổi tên hoặc đổi tỉnh rồi bấm “Lưu”.")
b.bullet("Giữ nguyên tên của chính chi nhánh đó thì không bị báo trùng.")

b.h2("6. Xoá chi nhánh")
b.bullet("Bước 1: Bấm nút Xóa ở dòng chi nhánh.")
b.bullet("Bước 2: Hộp thoại “Xác nhận xóa” hiện ra, nêu tên chi nhánh.")
b.bullet("Bước 3: Bấm “Xóa” để đồng ý. Hệ thống báo “Xoá chi nhánh ngân hàng thành công”.")

b.image("17-xac-nhan-xoa-chi-nhanh.png",
        "Hộp xác nhận xoá chi nhánh; dòng đầu có nút xoá bị làm mờ vì chi nhánh đang được sử dụng")

b.para("Chi nhánh đang được dùng ở hồ sơ nhân sự thì nút Xóa bị làm mờ, không bấm được. Rê chuột "
       "vào nút sẽ thấy chú thích “Không thể xóa bản ghi, chi nhánh đang được sử dụng trên hệ "
       "thống”. Lưu ý điểm khác biệt: ở đây nút bị làm mờ, còn ngoài danh sách ngân hàng thì nút "
       "Xóa bị ẩn hẳn.")

b.h2("7. Các lỗi thường gặp")
b.table([
    ["Thông báo", "Nguyên nhân", "Cách xử lý"],
    ["Bắt buộc phải nhập", "Chưa nhập tên chi nhánh hoặc chưa chọn tỉnh/thành phố.",
     "Nhập hoặc chọn nốt ô báo đỏ rồi bấm Lưu lại."],
    ["Tên chi nhánh ngân hàng này đã tồn tại", "Ngân hàng này đã có chi nhánh trùng tên.",
     "Đặt tên khác, hoặc kiểm tra lại danh sách xem chi nhánh đó đã được khai chưa."],
])
b.para("Lưu ý: hai ngân hàng khác nhau ĐƯỢC PHÉP có chi nhánh trùng tên, ví dụ cả hai đều có “CN Hà "
       "Nội”. Ràng buộc không trùng chỉ áp dụng trong phạm vi một ngân hàng.")

b.h2("8. Vì sao con số ở cột Chi nhánh có thể lệch với danh sách")
b.para("Con số ở cột “Chi nhánh” ngoài danh sách đếm tất cả chi nhánh của ngân hàng, kể cả chi "
       "nhánh chưa gán Tỉnh/Thành phố. Trong khi đó danh sách bên trong cửa sổ chỉ hiện chi nhánh "
       "ĐÃ có tỉnh/thành. Vì vậy với dữ liệu cũ, hai con số có thể lệch nhau. Nếu gặp trường hợp "
       "này, hãy báo bộ phận kỹ thuật để bổ sung tỉnh/thành cho các chi nhánh còn thiếu.")

# ============================================================================
b.h1("PHẦN 10: XEM LỊCH SỬ THAY ĐỔI")

b.h2("1. Cách mở")
b.bullet("Cách 1: Mở menu ba chấm ở cột Hành động của dòng, chọn “Lịch sử”.")
b.bullet("Cách 2: Bấm mã ngân hàng để mở cửa sổ Xem, rồi bấm “Xem lịch sử” ở cuối cửa sổ.")

b.image("14-lich-su.png", "Cửa sổ Lịch sử thay đổi của một ngân hàng")

b.h2("2. Đọc một mốc lịch sử")
b.para("Mỗi mốc gồm bốn phần, xếp từ trên xuống:")
b.bullet("Ngày giờ thực hiện.")
b.bullet("Tên hành động, có màu riêng: Tạo mới, Thay đổi thông tin, Khóa, Mở khóa, Xóa.")
b.bullet("Người thực hiện, kèm mã nhân viên và phòng ban.")
b.bullet("Chi tiết thay đổi theo dạng “Tên trường: giá trị cũ → giá trị mới”.")
b.para("Các mốc xếp mới nhất ở trên cùng.")

b.h2("3. Lọc lịch sử")
b.para("Bấm nút “Bộ lọc” ở góc phải cửa sổ để lọc theo Loại hoạt động. Có đúng ba nhóm, dùng chung "
       "cho mọi màn danh mục của hệ thống:")
b.table([
    ["Nhóm", "Bao gồm những mốc nào"],
    ["Tạo mới", "Lần tạo bản ghi."],
    ["Thay đổi thông tin", "Các lần sửa nội dung: mã, tên, tên viết tắt, tên giao dịch quốc tế, "
                           "địa chỉ giao dịch."],
    ["Thay đổi trạng thái", "Các lần Khóa và Mở khóa."],
])

b.h2("4. Những gì KHÔNG có trong lịch sử")
b.bullet("Thao tác thêm, sửa, xoá chi nhánh — hiện chưa được ghi lịch sử.")
b.bullet("Việc thay đổi logo.")
b.bullet("Việc chỉ mở xem mà không sửa gì.")
b.para("Nếu bấm Lưu mà không đổi nội dung nào thì hệ thống cũng không sinh mốc mới — đây là chủ ý "
       "để lịch sử không bị loãng.")

# ============================================================================
b.h1("PHẦN 11: HƯỚNG DẪN THEO TỪNG QUYỀN")

b.h2("1. Người dùng đã đăng nhập")
b.para("Bạn nhìn thấy:")
b.bullet("Mục “Ngân hàng” trên menu của phân hệ Danh mục chung.")
b.bullet("Toàn bộ danh sách ngân hàng của hệ thống, không bị giới hạn theo công ty hay phòng ban.")
b.bullet("Nút Tạo mới, nút Tuỳ chỉnh cột và đầy đủ các nút thao tác trên từng dòng.")
b.para("Bạn làm được toàn bộ thao tác mô tả từ PHẦN 1 đến PHẦN 10 của tài liệu này: tìm kiếm, tạo "
       "mới, sửa, xem chi tiết, khóa, mở khóa, xoá, quản lý chi nhánh và xem lịch sử.")

b.h2("2. Người chưa đăng nhập hoặc đã hết phiên")
b.para("Gõ thẳng đường dẫn /human/banks khi chưa đăng nhập sẽ bị đưa về màn Đăng nhập, không xem "
       "được dữ liệu.")
b.para("Nếu đang mở màn hình mà phiên hết hạn, ví dụ đã đăng xuất ở tab khác, thao tác kế tiếp sẽ "
       "đưa bạn về màn Đăng nhập. Hãy đăng nhập lại rồi vào lại màn hình; dữ liệu đang nhập dở "
       "trong cửa sổ sẽ mất nên cần nhập lại.")

b.h2("3. Lưu ý cho người quản trị")
b.para("Vì mọi người dùng đều sửa và xoá được danh mục dùng chung này, nên trong thực tế cần thống "
       "nhất trong đơn vị: chỉ một nhóm nhỏ, thường là bộ phận nhân sự hoặc kế toán, chịu trách "
       "nhiệm khai báo. Khi có ngân hàng bị sửa sai, dùng cửa sổ Lịch sử thay đổi ở PHẦN 10 để biết "
       "ai đã sửa và giá trị trước đó là gì.")

b.h2("4. Câu hỏi thường gặp")

b.h3("4.1 Khai báo một ngân hàng mới cho nhân sự dùng thì làm thế nào")
b.bullet("Bước 1: Vào Danh mục chung → Ngân hàng, gõ tên ngân hàng vào ô tìm nhanh, bấm Tìm kiếm để "
         "chắc chắn chưa có.")
b.bullet("Bước 2: Bấm Tạo mới, gõ từ khoá vào ô Gợi ý rồi bấm Tra cứu, chọn đúng ngân hàng để điền "
         "sẵn mã, tên, tên viết tắt và logo.")
b.bullet("Bước 3: Bổ sung Tên giao dịch quốc tế và Địa chỉ giao dịch nếu cần, bấm Lưu.")
b.bullet("Bước 4: Mở menu ba chấm của dòng vừa tạo, chọn Chi nhánh, bấm Tạo mới để khai các chi "
         "nhánh mà nhân viên đang mở tài khoản.")
b.bullet("Bước 5: Vào hồ sơ nhân sự và chọn ngân hàng, chi nhánh vừa khai.")

b.h3("4.2 Không thấy nút Xóa ở một ngân hàng")
b.para("Kiểm tra theo thứ tự: một là ngân hàng đó có đang ở trạng thái Khóa không, nếu có thì mở "
       "khóa trước; hai là ngân hàng đó có đang được dùng ở hồ sơ nhân sự hoặc ở danh mục tài khoản "
       "ngân hàng của công ty không, nếu có thì phải gỡ ở đó trước. Đây không phải vấn đề phân "
       "quyền.")

b.h3("4.3 Danh sách thiếu ngân hàng so với lúc trước")
b.para("Thường do bộ lọc còn giữ điều kiện cũ, hệ thống ghi nhớ trong 10 phút. Bấm “Làm mới” ở khối "
       "bộ lọc để xem lại toàn bộ danh sách.")

b.h3("4.4 Tạo nhầm hoặc gõ sai tên ngân hàng")
b.para("Bấm Sửa ở dòng đó và chỉnh lại. Nếu bản ghi tạo nhầm hoàn toàn và chưa ai dùng thì xoá theo "
       "PHẦN 8. Mọi thay đổi đều được ghi lại trong Lịch sử thay đổi.")

b.h3("4.5 Không biết ai đã sửa dữ liệu")
b.para("Mở menu ba chấm của dòng đó rồi chọn Lịch sử. Cửa sổ liệt kê từng mốc kèm tên người thực "
       "hiện, thời điểm và giá trị trước - sau.")

b.h3("4.6 Bấm mũi tên sắp xếp mà danh sách không đổi thứ tự")
b.para("Đây là lỗi đã được ghi nhận ở bản đang chạy, xem PHẦN 2 mục 7. Hãy dùng ô tìm kiếm hoặc "
       "tăng số dòng/trang để tìm nhanh trong lúc chờ xử lý.")

b.finish()
