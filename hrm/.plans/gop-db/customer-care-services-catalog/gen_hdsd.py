# -*- coding: utf-8 -*-
"""Sinh HDSD (Word) cho man 'Danh muc goi bao duong' (/customer-care/services).

Bo cuc bam bo tai lieu mau cua team: .plans/gop-db/customer-docs/HDSD_Danh muc khach hang.docx
— TONG QUAN gom ca bang quyen o muc 4, cac PHAN chuc nang o giua, PHAN cuoi la
"HUONG DAN THEO TUNG QUYEN" + cau hoi thuong gap.

⚠️ Tieu de dat la "TONG QUAN" (khong phai "TONG QUAN PHAN MEM") vi engine assert khong con
tieu de cua file khung trong output — file khung HDSD_MAU.docx dung dung chuoi do.

Anh chup that tren cong dev hrm-crm.eteksofts.com ngay 17/08/2026, 1440x900 -> gbd_shots/
(CHI DE LOCAL, .gitignore da chan **/.plans/**/*_shots/).

Chay:  python .plans/gop-db/customer-care-services-catalog/gen_hdsd.py
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
    output=os.path.join(HERE, "HDSD_Danh muc goi bao duong.docx"),
    shots_dir=os.path.join(HERE, "gbd_shots"),
    cover_title="(Màn hình: Danh mục gói bảo dưỡng)",
    doc_title="HDSD - Danh mục gói bảo dưỡng",
)

# ============================================================================
b.h1("TỔNG QUAN")

b.h2("1. Thuật ngữ sử dụng trong tài liệu")
b.table([
    ["Thuật ngữ", "Giải thích"],
    ["Gói bảo dưỡng",
     "Một dòng trong danh mục, mô tả trọn gói công việc bảo dưỡng: làm những gì, theo cấp nào, "
     "giá bao nhiêu, áp dụng cho hàng hoá nào và kèm tài liệu gì."],
    ["Cấp bảo dưỡng",
     "Mức độ bảo dưỡng, lấy từ danh mục Cấp dịch vụ. Trong bảng nội dung kiểm tra, mỗi cấp là MỘT "
     "CỘT và có bộ thông số giá riêng."],
    ["Nội dung kiểm tra bảo dưỡng",
     "Một hạng mục phải làm khi bảo dưỡng, ví dụ “Kiểm tra dầu máy”. Mỗi hạng mục là MỘT DÒNG "
     "trong bảng, kèm đơn vị tính và số lượng."],
    ["Ghi chú kiểm tra",
     "Ký hiệu công việc phải làm tại ô giao giữa một nội dung kiểm tra và một cấp bảo dưỡng, ví dụ "
     "DK (định kỳ), VS (vệ sinh), CC (căn chỉnh)."],
    ["Định mức công", "Số công quy đổi cần cho một cấp bảo dưỡng, dùng để tính giá vốn."],
    ["Hệ số công nghệ", "Hệ số nhân thêm vào giá vốn theo độ phức tạp công nghệ của cấp đó."],
    ["Giá vốn",
     "Đơn giá công của công ty quản lý × Định mức công × Hệ số công nghệ. Hệ thống tự tính, xem "
     "PHẦN 4 mục 5."],
    ["Giá công thức", "Giá vốn × Hệ số giá bán của gói. Hệ thống tự tính."],
    ["Giá bán cơ sở",
     "Giá bán chuẩn của một cấp. Mặc định bằng Giá công thức nhưng bạn sửa tay được."],
    ["Hệ số giá bán theo công ty",
     "Hệ số riêng của từng công ty. Giá bán của công ty đó = Giá bán cơ sở × hệ số này."],
    ["Công ty quản lý gói bảo dưỡng",
     "Công ty mà hệ thống lấy đơn giá công để tính giá vốn cho gói. Chọn sai công ty là sai toàn bộ "
     "giá của gói."],
    ["Trạng thái Hoạt động", "Gói đang dùng bình thường, sửa và xoá được."],
    ["Trạng thái Khóa",
     "Gói ngừng sử dụng nhưng KHÔNG bị xoá. Đang khóa thì không sửa được, xem PHẦN 7."],
    ["Gói đã được sử dụng",
     "Gói đã gắn hàng hoá hoặc đã được chọn trong báo giá dịch vụ. Gói này KHÔNG xoá được, xem "
     "PHẦN 7."],
    ["Lịch sử thay đổi",
     "Nhật ký ghi lại ai đã tạo, sửa, khóa hay mở khóa một gói, xem PHẦN 9."],
])

b.h2("2. Cập nhật tài liệu")
b.table([
    ["Phiên bản", "Ngày", "Người cập nhật", "Nội dung"],
    ["1.0", "17/08/2026", "@khoipv",
     "Lập mới cho màn Danh mục gói bảo dưỡng sau khi chuyển màn từ phần mềm cũ sang phân hệ Chăm "
     "sóc khách hàng."],
])

b.h2("3. Giới thiệu chung")
b.para("Màn hình “Danh mục gói bảo dưỡng” là nơi khai báo các gói bảo dưỡng dùng chung cho toàn "
       "hệ thống: mỗi gói gồm thông tin chung, danh mục nội dung kiểm tra theo từng cấp bảo dưỡng, "
       "giá bán theo từng công ty, danh sách hàng hoá áp dụng và tài liệu PDF kèm theo.")
b.para("Gói bảo dưỡng khai ở đây được dùng lại khi lập báo giá dịch vụ và phiếu yêu cầu dịch vụ. "
       "Vì vậy khai sai giá hoặc sai nội dung kiểm tra ở màn này sẽ kéo theo sai ở chứng từ phía "
       "sau.")
b.para("Lưu ý phạm vi: danh sách hiển thị TẤT CẢ gói bảo dưỡng của hệ thống, không cắt theo công "
       "ty của bạn. Công ty của bạn chỉ được dùng để điền sẵn ô “Công ty quản lý gói bảo dưỡng” "
       "khi tạo mới.")
b.para("Đường dẫn truy cập:")
b.bullet("Menu: Phân hệ Chăm sóc khách hàng → Danh mục → Danh mục gói bảo dưỡng.")
b.bullet("Hoặc gõ thẳng đường dẫn /customer-care/services vào thanh địa chỉ trình duyệt.")

b.h2("4. Quyền và phạm vi dữ liệu")

b.h3("4.1 Bảng quyền của màn hình")
b.table([
    ["Tên quyền", "Cho phép làm gì", "Nút / cửa sổ tương ứng", "Ghi chú"],
    ["Thêm danh mục gói bảo dưỡng",
     "Tạo gói mới và nhân bản gói đang có.",
     "Nút Tạo mới; nút Nhân bản trong menu ba chấm và ở chân trang chi tiết.",
     "Thiếu quyền thì hai nút này bị ẩn."],
    ["Sửa danh mục gói bảo dưỡng",
     "Cập nhật gói đang Hoạt động và mở khoá gói đang Khóa.",
     "Nút Sửa (bút chì) và nút Mở khóa (ổ khoá mở) ở cột Hành động.",
     "Gói đang Khóa thì nút Sửa bị ẩn dù bạn có quyền."],
    ["Xóa danh mục gói bảo dưỡng",
     "Xoá gói chưa được sử dụng.",
     "Nút Xóa (thùng rác đỏ) ở cột Hành động.",
     "Gói đã được sử dụng thì nút Xóa bị ẩn, xem PHẦN 7."],
])
b.para("Ba quyền trên độc lập với nhau: bạn có thể chỉ có một trong ba.")

b.h3("4.2 Những việc KHÔNG cần quyền")
b.bullet("Xem danh sách gói bảo dưỡng: mọi tài khoản đã đăng nhập đều vào được.")
b.bullet("Xem chi tiết một gói.")
b.bullet("In phiếu Danh mục kiểm tra bảo dưỡng định kỳ.")
b.bullet("Xuất Excel danh sách gói bảo dưỡng.")
b.bullet("Xem lịch sử thay đổi của một gói.")
b.para("Đây là hiện trạng giữ nguyên theo phần mềm cũ. Nếu đơn vị bạn muốn siết chặt (ví dụ chỉ "
       "cho một nhóm người xem giá hoặc xuất file) thì cần đề nghị bổ sung quyền mới, chứ hiện tại "
       "hệ thống không chặn.")

b.h3("4.3 Phạm vi dữ liệu")
b.bullet("Danh sách hiển thị toàn bộ gói bảo dưỡng của hệ thống, không phân theo công ty, phòng "
         "ban hay bộ phận.")
b.bullet("Mọi người cùng nhìn chung một danh sách, nên khi sửa cần lưu ý gói có thể đang được đơn "
         "vị khác sử dụng.")
b.bullet("Ô “Công ty quản lý gói bảo dưỡng” được điền sẵn theo công ty của bạn khi tạo mới, nhưng "
         "bạn đổi sang công ty khác được.")

# ============================================================================
b.h1("PHẦN 1: TRUY CẬP VÀ BỐ CỤC MÀN HÌNH")

b.h2("1. Truy cập màn hình")
b.bullet("Bước 1: Đăng nhập hệ thống.")
b.bullet("Bước 2: Chọn phân hệ “Chăm sóc khách hàng” ở góc trên bên trái.")
b.bullet("Bước 3: Trên menu bên trái, mở nhóm “Danh mục”.")
b.bullet("Bước 4: Bấm mục “Danh mục gói bảo dưỡng”.")
b.para("Màn hình mở ra với tiêu đề “Danh mục gói bảo dưỡng”, danh sách hiển thị 10 dòng đầu tiên.")
b.image("01-danh-sach.png", "Màn hình Danh mục gói bảo dưỡng khi mới truy cập")

b.h2("2. Bố cục màn hình")
b.bullet("Trên cùng: tiêu đề màn hình.")
b.bullet("Khối “Bộ lọc danh sách”: ô tìm nhanh, ô Trạng thái, ô Người tạo và hai nút Tìm kiếm / "
         "Làm mới.")
b.bullet("Góc phải trên bảng: nút Tạo mới (nền xanh dương), nút Xuất Excel (nền xanh lá) và nút "
         "Cấu hình cột hiển thị (biểu tượng cột).")
b.bullet("Giữa màn hình: bảng danh sách gói bảo dưỡng.")
b.bullet("Dưới bảng: ô chọn số dòng mỗi trang, dòng “Hiển thị a–b / N” và các nút chuyển trang.")
b.para("Màn hình KHÔNG có nút Nhập Excel — dữ liệu chỉ khai bằng tay hoặc nhân bản từ gói có sẵn.")

b.h2("3. Các cột của bảng danh sách")
b.table([
    ["Cột", "Ý nghĩa", "Mặc định"],
    ["STT", "Số thứ tự theo trang đang xem.", "Luôn hiển thị, không tắt được"],
    ["Mã", "Mã gói bảo dưỡng. Bấm vào mã để mở màn chi tiết.", "Luôn hiển thị, không tắt được"],
    ["Tên gói bảo dưỡng",
     "Tên gói. Nếu gói đã khai cấp bảo dưỡng thì có thêm biểu tượng chữ i — rê chuột vào sẽ hiện "
     "giá bán của từng cấp.", "Hiển thị"],
    ["Công ty quản lý gói bảo dưỡng",
     "Công ty dùng để lấy đơn giá công tính giá vốn.", "Ẩn — bật ở Cấu hình cột"],
    ["Người tạo", "Người đã tạo gói.", "Hiển thị"],
    ["Ngày tạo", "Thời điểm tạo gói, dạng ngày/tháng/năm giờ:phút.", "Hiển thị"],
    ["Người sửa", "Người sửa gói gần nhất.", "Ẩn — bật ở Cấu hình cột"],
    ["Ngày sửa", "Thời điểm sửa gần nhất.", "Ẩn — bật ở Cấu hình cột"],
    ["Trạng thái", "Nhãn xanh “Hoạt động” hoặc nhãn đỏ “Khóa”.", "Hiển thị"],
    ["Hành động", "Các nút thao tác của dòng đó.", "Luôn hiển thị, chốt ở cuối bảng"],
])

b.h2("4. Cột Hành động")
b.para("Cột Hành động gồm các nút bấm nhanh và một menu ba chấm. Nút nào bạn không được phép dùng "
       "thì hệ thống ẩn hẳn chứ không làm mờ.")
b.image("02-menu-hanh-dong.png", "Menu ba chấm của một dòng — Nhân bản, In, Lịch sử")
b.table([
    ["Nút", "Khi nào hiện", "Bấm vào thì sao"],
    ["Sửa (bút chì)", "Có quyền Sửa và gói đang Hoạt động.", "Mở trang Sửa gói bảo dưỡng."],
    ["Xóa (thùng rác đỏ)",
     "Có quyền Xóa, gói đang Hoạt động và gói CHƯA được sử dụng.",
     "Mở hộp xác nhận trước khi xoá."],
    ["Mở khóa (ổ khoá mở)", "Có quyền Sửa và gói đang Khóa.",
     "Mở hộp xác nhận, đồng ý thì gói trở lại Hoạt động."],
    ["Nhân bản", "Có quyền Thêm.", "Mở trang Sao chép gói bảo dưỡng với dữ liệu điền sẵn."],
    ["In", "Luôn hiện.", "Mở tab mới với phiếu Danh mục kiểm tra bảo dưỡng định kỳ."],
    ["Lịch sử", "Luôn hiện.", "Mở cửa sổ Lịch sử thay đổi của gói đó."],
])

b.h2("5. Phân trang")
b.bullet("Mặc định 10 dòng mỗi trang.")
b.bullet("Ô “Số dòng/trang” có 5 mức: 5, 10, 20, 50, 100. Đổi số dòng thì danh sách quay về "
         "trang 1.")
b.bullet("Dòng “Hiển thị a–b / N” cho biết đang xem dòng nào và tổng cộng bao nhiêu gói khớp bộ "
         "lọc.")
b.bullet("Chuyển trang không làm mất bộ lọc và thứ tự sắp xếp đang có.")

b.h2("6. Sắp xếp theo cột")
b.bullet("Các cột sắp xếp được: Mã, Tên gói bảo dưỡng, Trạng thái, Ngày tạo, Ngày sửa.")
b.bullet("Bấm lần đầu xếp tăng dần, bấm lần nữa xếp giảm dần.")
b.bullet("Mặc định danh sách xếp theo Ngày tạo, gói mới nhất nằm trên cùng.")
b.bullet("Lưu ý: khi bạn đang tìm theo từ khoá, hệ thống tự xếp theo độ khớp; nếu bạn bấm sắp xếp "
         "theo cột thì thứ tự theo độ khớp sẽ bị bỏ qua.")

# ============================================================================
b.h1("PHẦN 2: TÌM KIẾM VÀ LỌC DANH SÁCH")

b.image("03-tim-kiem.png", "Kết quả sau khi tìm nhanh theo từ khoá “GBDT”")

b.h2("1. Tìm kiếm nhanh")
b.bullet("Bước 1: Gõ từ khoá vào ô “Tìm theo tên hoặc mã gói bảo dưỡng...”.")
b.bullet("Bước 2: Chờ khoảng nửa giây — hệ thống TỰ lọc, bạn không bắt buộc phải bấm Tìm kiếm.")
b.bullet("Muốn lọc ngay lập tức thì nhấn Enter hoặc bấm nút Tìm kiếm.")
b.para("Ô này quét đồng thời Tên gói và Mã gói, không phân biệt chữ hoa chữ thường. Kết quả được "
       "xếp theo độ khớp: bản ghi trùng khít đứng đầu, tiếp đến là bản ghi bắt đầu bằng từ khoá, "
       "cuối cùng mới tới bản ghi chỉ chứa từ khoá ở giữa.")
b.para("Nếu bạn chỉ gõ 1 ký tự thì hệ thống không xếp theo độ khớp mà trả về thứ tự mặc định — đây "
       "không phải lỗi.")

b.h2("2. Lọc theo trạng thái")
b.bullet("Chọn “Hoạt động” để chỉ xem gói đang dùng.")
b.bullet("Chọn “Khóa” để chỉ xem gói đã ngừng sử dụng.")
b.bullet("Để trống là xem tất cả. Danh sách tự tải lại ngay khi bạn chọn.")

b.h2("3. Lọc theo người tạo")
b.para("Chọn một nhân viên trong ô “Người tạo” để chỉ xem những gói do người đó tạo. Hữu ích khi "
       "cần rà lại phần mình vừa khai báo.")

b.h2("4. Kết hợp nhiều điều kiện")
b.para("Ba ô lọc hoạt động cùng lúc theo kiểu VÀ: kết quả phải thoả mãn đồng thời cả từ khoá, "
       "trạng thái và người tạo. Mỗi lần đổi điều kiện, danh sách quay về trang 1.")

b.h2("5. Nút Làm mới")
b.para("Bấm “Làm mới” để xoá sạch cả ba điều kiện lọc và tải lại toàn bộ danh sách từ trang 1. Khi "
       "thấy danh sách “thiếu” gói so với lúc trước, hãy bấm nút này đầu tiên.")

b.h2("6. Hệ thống ghi nhớ bộ lọc trong 10 phút")
b.para("Khi bạn rời sang màn khác rồi quay lại trong vòng 10 phút, bộ lọc cũ được khôi phục để bạn "
       "làm tiếp việc dở. Quá 10 phút thì bộ lọc tự xoá. Đây là lý do phổ biến nhất khiến danh "
       "sách trông như bị thiếu dữ liệu.")

# ============================================================================
b.h1("PHẦN 3: TUỲ CHỈNH CỘT HIỂN THỊ")

b.image("04-cau-hinh-cot.png", "Cửa sổ Tuỳ chỉnh cột — cột STT, Mã và Hành động có biểu tượng ổ khoá")

b.h2("1. Mở cửa sổ tuỳ chỉnh cột")
b.para("Bấm nút có biểu tượng cột nằm cạnh nút Xuất Excel. Cửa sổ “Tuỳ chỉnh cột” liệt kê đủ 10 "
       "cột của bảng kèm trạng thái bật/tắt hiện tại.")

b.h2("2. Bật và tắt cột")
b.bullet("Tích vào ô vuông trước tên cột để bật, bỏ tích để tắt.")
b.bullet("Ba cột STT, Mã và Hành động có biểu tượng ổ khoá — không tắt được vì đây là cột định "
         "danh và cột thao tác.")
b.bullet("Ba cột thường được bật thêm: Công ty quản lý gói bảo dưỡng, Người sửa, Ngày sửa.")

b.h2("3. Đổi thứ tự cột")
b.para("Giữ chuột vào tay nắm ở cuối mỗi dòng rồi kéo lên xuống để đổi vị trí cột trên bảng.")

b.h2("4. Lưu hoặc bỏ thay đổi")
b.bullet("Bấm “Lưu”: bảng vẽ lại theo cấu hình mới. Cấu hình lưu riêng cho tài khoản của bạn, tải "
         "lại trang vẫn giữ nguyên và không ảnh hưởng người khác.")
b.bullet("Bấm “Đóng”: bỏ toàn bộ thay đổi chưa lưu, bảng giữ nguyên như cũ.")

# ============================================================================
b.h1("PHẦN 4: TẠO MỚI GÓI BẢO DƯỠNG")

b.h2("1. Mở trang Thêm gói bảo dưỡng")
b.para("Bấm nút “Tạo mới” ở góc phải trên bảng. Khác nhiều màn danh mục khác, màn này mở một TRANG "
       "RIÊNG chứ không phải cửa sổ bật lên, vì lượng thông tin phải nhập rất lớn.")
b.para("Trang gồm 5 khối, xếp từ trên xuống:")
b.bullet("Thông tin chung.")
b.bullet("Danh mục kiểm tra bảo dưỡng định kỳ (bảng dạng ma trận).")
b.bullet("Giá vốn theo công ty.")
b.bullet("Áp dụng cho hàng hóa.")
b.bullet("File đính kèm (PDF).")
b.image("06-tao-moi-thong-tin-chung.png",
        "Trang Thêm gói bảo dưỡng — khối Thông tin chung và bảng nội dung kiểm tra")

b.h2("2. Các trường của khối Thông tin chung")
b.table([
    ["Trường", "Bắt buộc", "Cách nhập", "Lưu ý"],
    ["Tên gói bảo dưỡng", "Có", "Gõ tên gói, tối đa 255 ký tự.",
     "Không được trùng với gói khác. Khoảng trắng thừa ở đầu và cuối tự bị cắt."],
    ["Mã gói bảo dưỡng", "Có", "Gõ mã gói, tối đa 255 ký tự.",
     "Hệ thống tự chuyển thành CHỮ IN HOA khi lưu, nên “bdt001” và “BDT001” bị coi là trùng nhau."],
    ["Công ty quản lý gói bảo dưỡng", "Có", "Chọn trong danh sách công ty.",
     "Điền sẵn công ty của bạn. Công ty này quyết định đơn giá công dùng để tính giá vốn — chọn "
     "sai là sai toàn bộ giá của gói."],
    ["Định mức đàm phán giá (%)", "Không", "Gõ số từ 0 đến 99.",
     "Vượt 99 thì báo “Tối đa 99”."],
    ["VAT (%)", "Không", "Gõ số từ 0 đến 100.", "Vượt 100 thì báo “Tối đa 100”."],
    ["Hệ số giá bán gói bảo dưỡng", "Không", "Gõ số từ 1 đến 100.",
     "Nhỏ hơn 1 thì báo “Không được nhỏ hơn 1”. Dùng để tính Giá công thức."],
    ["Ghi chú", "Không", "Gõ nội dung, tối đa 255 ký tự.",
     "Nội dung này được in ở cuối phiếu kiểm tra bảo dưỡng."],
])
b.para("⚠ Các ô số ở màn này nhận DẤU PHẨY làm dấu thập phân: gõ 12,5 nghĩa là mười hai phẩy năm, "
       "không phải một trăm hai mươi lăm.")

b.h2("3. Giá trị điền sẵn khi tạo mới")
b.bullet("Công ty quản lý gói bảo dưỡng: điền sẵn công ty của bạn.")
b.bullet("Khối Giá vốn theo công ty: liệt kê sẵn các công ty với hệ số mặc định 1.")
b.bullet("Bảng nội dung kiểm tra: để trống, hiện dòng “Không có danh mục kiểm tra bảo dưỡng”.")
b.bullet("KHÔNG có ô Trạng thái — gói mới luôn được lưu ở trạng thái Hoạt động. Ô Trạng thái chỉ "
         "xuất hiện khi bạn Sửa gói.")

b.h2("4. Khai bảng Danh mục kiểm tra bảo dưỡng định kỳ")
b.para("Đây là phần quan trọng nhất và cũng dễ nhầm nhất. Hãy hình dung bảng như một ma trận:")
b.bullet("Mỗi DÒNG là một nội dung kiểm tra, ví dụ “Kiểm tra dầu máy”.")
b.bullet("Mỗi CỘT là một cấp bảo dưỡng, ví dụ “Bảo dưỡng máy làm sạch buồng đốt”.")
b.bullet("Ô giao giữa dòng và cột cho biết ở cấp đó phải làm gì với hạng mục đó.")
b.para("Các bước khai báo:")
b.bullet("Bước 1: Bấm “+ Thêm danh mục kiểm tra bảo dưỡng” để thêm một dòng.")
b.bullet("Bước 2: Nhập Nội dung kiểm tra, chọn Đơn vị tính và nhập Số lượng. Cả ba ô này đều bắt "
         "buộc.")
b.bullet("Bước 3: Bấm dấu + ở góc phải tiêu đề bảng để thêm một cột, rồi chọn Cấp bảo dưỡng cho "
         "cột đó.")
b.bullet("Bước 4: Bấm vào ô giao giữa dòng và cột, chọn một hoặc nhiều Ghi chú kiểm tra. Ô để "
         "trống thì khi Lưu sẽ báo lỗi.")
b.bullet("Bước 5: Lặp lại cho tới khi khai đủ các hạng mục và các cấp.")
b.para("⚠ Mỗi cấp bảo dưỡng chỉ được chọn MỘT lần trong bảng. Nếu chọn lại cấp đã dùng ở cột khác, "
       "hệ thống cảnh báo “Cấp bảo dưỡng này đã được chọn ở cột khác” và không nhận.")
b.para("Muốn bỏ một dòng thì bấm biểu tượng xoá ở cuối dòng; muốn bỏ một cột thì bấm biểu tượng "
       "xoá ở tiêu đề cột.")

b.h2("5. Nhập thông số giá của từng cấp")
b.para("Dưới bảng ma trận, mỗi cột cấp có thêm các dòng thông số:")
b.table([
    ["Dòng", "Bạn nhập hay hệ thống tự tính", "Ý nghĩa"],
    ["Định mức công", "Bạn nhập — BẮT BUỘC", "Số công quy đổi cần cho cấp đó."],
    ["Hệ số công nghệ", "Bạn nhập", "Hệ số nhân thêm theo độ phức tạp công nghệ."],
    ["Giá vốn", "Hệ thống tự tính",
     "Đơn giá công của công ty quản lý × Định mức công × Hệ số công nghệ, làm tròn xuống."],
    ["Giá công thức", "Hệ thống tự tính", "Giá vốn × Hệ số giá bán gói bảo dưỡng."],
    ["Giá bán cơ sở", "Hệ thống điền sẵn, bạn sửa được",
     "Mặc định bằng Giá công thức. Đây là căn cứ tính giá bán cho từng công ty."],
    ["Gợi ý hàng hoá", "Bạn chọn", "Hàng hoá gợi ý dùng kèm cho cấp bảo dưỡng đó."],
])
b.para("Ví dụ: công ty quản lý có đơn giá công 700.000; bạn nhập Định mức công = 2, Hệ số công "
       "nghệ = 2, Hệ số giá bán gói = 2. Khi đó Giá vốn = 700.000 × 2 × 2 = 2.800.000; Giá công "
       "thức = 2.800.000 × 2 = 5.600.000; Giá bán cơ sở điền sẵn 5.600.000 và bạn vẫn sửa tay "
       "được.")

b.h2("6. Khai Giá vốn theo công ty")
b.para("Khối này liệt kê các công ty trong hệ thống. Với mỗi công ty bạn nhập một Hệ số giá bán "
       "riêng; giá bán của công ty đó = Giá bán cơ sở × hệ số này.")
b.bullet("Hệ số mặc định là 1, nghĩa là bán đúng giá cơ sở.")
b.bullet("Để trống ô hệ số thì hệ thống hiểu là 1, KHÔNG phải 0.")
b.bullet("Hệ số tối đa 99.999.999,99. Nhập lớn hơn sẽ bị báo lỗi.")

b.h2("7. Chọn hàng hoá áp dụng và đính kèm file")
b.image("07-tao-moi-hang-hoa-file.png",
        "Khối Giá vốn theo công ty, Áp dụng cho hàng hóa và File đính kèm (PDF)")
b.para("Chọn hàng hoá:")
b.bullet("Bấm “Chọn hàng hóa” để mở cửa sổ tìm và tích chọn từng hàng hoá, rồi bấm nút thêm.")
b.bullet("Bấm “Chọn nhóm hàng” để thêm nhanh toàn bộ hàng hoá của một nhóm.")
b.bullet("Muốn bỏ một hàng hoá đã chọn thì bấm biểu tượng xoá ở dòng đó.")
b.image("14-chon-hang-hoa.png", "Cửa sổ Chọn hàng hóa áp dụng")
b.para("Đính kèm file:")
b.bullet("Bấm “+ Thêm file” ở khối File đính kèm (PDF) và chọn file từ máy.")
b.bullet("⚠ BẮT BUỘC có ít nhất 1 file PDF thì mới lưu được gói. Đây là quy định riêng của phần "
         "mềm mới, phần mềm cũ không bắt buộc.")
b.bullet("Chỉ nhận file định dạng PDF; chọn ảnh hoặc Word sẽ bị từ chối.")
b.bullet("Thêm được nhiều file cho một gói.")

b.h2("8. Lưu gói bảo dưỡng")
b.bullet("Bước 1: Kiểm tra lại các ô có dấu sao đỏ đã nhập đủ chưa.")
b.bullet("Bước 2: Bấm nút “Lưu” ở chân trang.")
b.bullet("Bước 3: Hệ thống báo “Tạo gói bảo dưỡng thành công” và quay về danh sách; gói mới nằm ở "
         "dòng đầu tiên với trạng thái Hoạt động.")
b.para("Mã gói hiển thị dạng in hoa dù bạn gõ chữ thường. Nếu bấm Lưu nhiều lần liên tiếp, hệ "
       "thống vẫn chỉ tạo đúng một gói.")
b.para("Muốn bỏ dở giữa chừng thì bấm “Quay lại”. Nếu đã nhập dở, hệ thống hỏi lại “Thông tin chưa "
       "lưu” — chọn ở lại thì dữ liệu còn nguyên, chọn rời đi thì mất toàn bộ.")

b.h2("9. Các lỗi thường gặp khi lưu")
b.image("08-loi-validate.png", "Bấm Lưu khi chưa nhập gì — lỗi đỏ hiện ngay tại ô bắt buộc")
b.table([
    ["Thông báo", "Nguyên nhân", "Cách xử lý"],
    ["Bắt buộc phải nhập", "Còn ô có dấu sao đỏ chưa nhập.",
     "Cuộn lên tìm ô có viền đỏ — có thể nằm trong bảng ma trận chứ không chỉ ở khối Thông tin "
     "chung."],
    ["Đã tồn tại (ở ô Tên hoặc Mã)", "Tên hoặc mã đã có gói khác dùng.",
     "Đổi sang tên/mã khác. Nhớ mã được so sánh sau khi in hoa nên “bdt001” trùng với “BDT001”."],
    ["Cấp bảo dưỡng này đã được chọn ở cột khác", "Chọn trùng cấp trong bảng ma trận.",
     "Chọn cấp khác, hoặc bỏ cột cũ nếu khai nhầm."],
    ["Bắt buộc phải đính kèm ít nhất 1 file PDF", "Chưa thêm file nào.",
     "Thêm ít nhất một file PDF rồi lưu lại."],
    ["Chỉ nhận file PDF", "Đính kèm file khác định dạng.", "Chuyển tài liệu sang PDF rồi thêm lại."],
    ["Tối đa 99 / Tối đa 100 / Không được nhỏ hơn 1", "Ô số nhập vượt giới hạn cho phép.",
     "Nhập lại trong khoảng cho phép, xem bảng ở mục 2."],
    ["Phải là số", "Gõ chữ vào ô số như VAT hoặc Số lượng.", "Xoá và nhập lại bằng số."],
])

# ============================================================================
b.h1("PHẦN 5: SỬA GÓI BẢO DƯỠNG")

b.h2("1. Mở trang Sửa")
b.bullet("Cách 1: Bấm nút Sửa (bút chì) ở cột Hành động của dòng cần sửa.")
b.bullet("Cách 2: Mở màn chi tiết của gói rồi bấm nút Sửa ở chân trang.")
b.para("Nếu không thấy nút Sửa: hoặc bạn chưa có quyền Sửa danh mục gói bảo dưỡng, hoặc gói đang "
       "ở trạng thái Khóa.")
b.image("13-sua.png", "Trang Sửa gói bảo dưỡng — dữ liệu hiện tại đã được nạp sẵn")

b.h2("2. Các bước sửa")
b.bullet("Bước 1: Mở trang Sửa, toàn bộ 5 khối đã nạp sẵn dữ liệu hiện tại.")
b.bullet("Bước 2: Sửa các khối cần thay đổi. Ràng buộc nhập liệu giống hệt màn Tạo mới.")
b.bullet("Bước 3: Bấm “Lưu”, hệ thống báo “Cập nhật gói bảo dưỡng thành công” và quay về danh "
         "sách.")
b.para("Cột Người sửa và Ngày sửa của dòng đó được cập nhật theo bạn và thời điểm vừa lưu.")

b.h2("3. Điểm khác so với màn Tạo mới")
b.bullet("Màn Sửa CÓ thêm ô Trạng thái với hai lựa chọn Hoạt động / Khóa. Đổi sang Khóa rồi Lưu là "
         "một cách để ngừng sử dụng gói.")
b.bullet("Giữ nguyên Tên và Mã cũ của chính gói đó thì không bị báo trùng.")
b.bullet("Bạn thêm hoặc bớt dòng nội dung kiểm tra, cột cấp, hàng hoá và file đính kèm như khi tạo "
         "mới.")

b.h2("4. Những điều nên biết")
b.bullet("⚠ Không bỏ được cột cấp đã phát sinh báo giá dịch vụ: khi Lưu, hệ thống chặn lại và giữ "
         "nguyên toàn bộ dữ liệu cũ của gói. Muốn bỏ cấp đó thì phải xử lý các báo giá liên quan "
         "trước.")
b.bullet("Nếu gói vừa bị người khác khóa trong lúc bạn đang sửa, khi bấm Lưu hệ thống sẽ báo phải "
         "mở khoá trước. Bấm Làm mới ở danh sách rồi thao tác lại.")
b.bullet("Lưu mà không sửa gì thì vẫn báo thành công nhưng không phát sinh mốc lịch sử mới.")
b.bullet("Lịch sử chỉ theo dõi các trường của khối Thông tin chung. Sửa bảng ma trận, hệ số theo "
         "công ty, hàng hoá hay file đính kèm sẽ KHÔNG xuất hiện trong lịch sử.")

# ============================================================================
b.h1("PHẦN 6: XEM CHI TIẾT VÀ NHÂN BẢN")

b.h2("1. Xem chi tiết một gói")
b.para("Bấm vào Mã gói ở danh sách. Hệ thống mở trang “Chi tiết gói bảo dưỡng: <mã gói>” ở chế độ "
       "chỉ đọc — mọi ô đều khoá, không gõ sửa được. Trang có đường dẫn riêng nên bạn mở được ở "
       "tab mới bằng chuột phải.")
b.image("09-chi-tiet.png", "Trang Chi tiết gói bảo dưỡng ở chế độ chỉ đọc")

b.h2("2. Nội dung trang chi tiết")
b.bullet("Thông tin chung: tên, mã, công ty quản lý, định mức đàm phán giá, VAT, hệ số giá bán, "
         "ghi chú, trạng thái.")
b.bullet("Danh mục kiểm tra bảo dưỡng định kỳ kèm các dòng Định mức công, Hệ số công nghệ, Giá "
         "vốn, Giá công thức, Giá bán cơ sở.")
b.bullet("Giá bán theo công ty.")
b.bullet("Áp dụng cho hàng hóa: hình ảnh, tên hàng, mã hàng.")
b.bullet("File đính kèm: bấm vào tên file để mở PDF ở tab mới.")
b.para("Chân trang có các nút Sửa, In, Nhân bản và Quay lại. Nút Sửa bị ẩn nếu gói đang Khóa hoặc "
       "bạn không có quyền Sửa; nút Nhân bản bị ẩn nếu bạn không có quyền Thêm.")

b.h2("3. Nhân bản gói bảo dưỡng")
b.para("Nhân bản dùng khi cần tạo một gói gần giống gói đã có, tránh phải khai lại toàn bộ ma "
       "trận nội dung kiểm tra.")
b.bullet("Bước 1: Mở menu ba chấm ở dòng cần sao chép và bấm “Nhân bản” (hoặc bấm Nhân bản ở chân "
         "trang chi tiết).")
b.bullet("Bước 2: Hệ thống mở trang “Sao chép gói bảo dưỡng” với toàn bộ dữ liệu của gói nguồn, kể "
         "cả hàng hoá áp dụng và file đính kèm.")
b.bullet("Bước 3: ⚠ Sửa lại Tên gói và Mã gói cho khác gói nguồn — hai trường này giữ nguyên nên "
         "nếu bấm Lưu ngay sẽ báo “Đã tồn tại”.")
b.bullet("Bước 4: Chỉnh các nội dung khác nếu cần rồi bấm Lưu.")
b.para("Gói nhân bản luôn được tạo ở trạng thái Hoạt động, kể cả khi nhân bản từ gói đang Khóa. "
       "Gói nguồn không bị thay đổi.")
b.para("Lưu ý: vì bản nhân bản mang theo danh sách hàng hoá của gói nguồn nên gói mới cũng bị coi "
       "là “đã được sử dụng” và sẽ không có nút Xóa.")

# ============================================================================
b.h1("PHẦN 7: XÓA, KHÓA VÀ MỞ KHÓA")

b.h2("1. Xóa và Khóa khác nhau thế nào")
b.bullet("Xóa: bản ghi biến mất hẳn khỏi danh mục cùng toàn bộ nội dung kiểm tra và các cấp của "
         "gói. Không khôi phục được.")
b.bullet("Khóa: bản ghi vẫn còn trong danh sách với nhãn đỏ “Khóa”, chỉ là không dùng và không sửa "
         "được nữa. Có thể mở khoá để dùng lại.")
b.para("⚠ Điểm dễ nhầm nhất của màn này: gói ĐÃ ĐƯỢC SỬ DỤNG thì hệ thống không xoá mà tự chuyển "
       "sang trạng thái Khóa, kèm thông báo “Gói bảo dưỡng đang được sử dụng nên đã được chuyển "
       "sang trạng thái Khóa”. Dữ liệu không bị mất.")
b.para("Một gói được coi là đã được sử dụng khi đã gắn hàng hoá, hoặc đã được chọn trong báo giá "
       "dịch vụ. Với những gói này, hệ thống ẩn luôn nút Xóa ngoài danh sách.")

b.h2("2. Các bước xóa một gói")
b.bullet("Bước 1: Tìm gói cần xoá trên danh sách.")
b.bullet("Bước 2: Bấm nút Xóa (thùng rác đỏ) ở cột Hành động. Nếu không thấy nút này thì gói đã "
         "được sử dụng, đang Khóa, hoặc bạn không có quyền Xóa.")
b.bullet("Bước 3: Đọc kỹ hộp thoại “Xác nhận xóa” — nội dung nêu rõ tên gói sắp xoá.")
b.bullet("Bước 4: Bấm “Xóa” để đồng ý, hoặc “Hủy” để dừng lại.")
b.image("11-xac-nhan-xoa.png", "Hộp thoại Xác nhận xóa gói bảo dưỡng")
b.para("Xoá thành công thì hệ thống báo “Xóa gói bảo dưỡng thành công”, dòng biến mất và tổng số "
       "bản ghi giảm đi 1.")

b.h2("3. Khóa một gói đang dùng")
b.para("Muốn ngừng sử dụng một gói mà vẫn giữ dữ liệu, hãy vào màn Sửa và đổi ô Trạng thái sang "
       "“Khóa” rồi Lưu. Sau khi khóa:")
b.bullet("Dòng đó mang nhãn đỏ “Khóa”.")
b.bullet("Nút Sửa và nút Xóa biến mất, chỉ còn Mở khóa, Nhân bản, In và Lịch sử.")
b.bullet("Gói vẫn xem chi tiết, in phiếu và nhân bản được bình thường.")

b.h2("4. Mở khóa gói")
b.bullet("Bước 1: Tìm gói đang có nhãn “Khóa”. Có thể lọc nhanh bằng ô Trạng thái = Khóa.")
b.bullet("Bước 2: Bấm nút Mở khóa (ổ khoá mở) ở cột Hành động.")
b.bullet("Bước 3: Bấm “Mở khóa” trong hộp xác nhận.")
b.para("Hệ thống báo “Mở khóa gói bảo dưỡng thành công”, dòng trở lại nhãn “Hoạt động” và hiện lại "
       "nút Sửa. Thao tác mở khóa cần quyền Sửa danh mục gói bảo dưỡng.")

b.h2("5. Lưu ý")
b.bullet("Không xoá được gói đang Khóa — muốn xoá thì mở khoá trước, và chỉ xoá được nếu gói chưa "
         "được sử dụng.")
b.bullet("Xoá dòng cuối cùng của trang cuối thì danh sách tự lùi về trang trước, không hiện trang "
         "trắng.")
b.bullet("Mọi lần khóa và mở khóa đều được ghi vào Lịch sử thay đổi kèm tên người thực hiện.")

# ============================================================================
b.h1("PHẦN 8: XUẤT EXCEL VÀ IN PHIẾU")

b.h2("1. Xuất Excel danh sách gói bảo dưỡng")
b.bullet("Bước 1: Bấm nút “Xuất Excel” (nền xanh lá) ở góc phải trên bảng.")
b.bullet("Bước 2: Cửa sổ “Chọn trường xuất file” mở ra với 6 trường: Mã, Tên gói bảo dưỡng, Công "
         "ty quản lý, Trạng thái, Người tạo, Ngày tạo. Mặc định chọn sẵn cả 6.")
b.bullet("Bước 3: Bỏ tích những trường không cần, hoặc bấm “Bỏ chọn hết” rồi chọn lại theo thứ tự "
         "mong muốn.")
b.bullet("Bước 4: Bấm “Xuất file”; trình duyệt tải về file Danh_sach_goi_bao_duong.xlsx.")
b.image("05-chon-truong-xuat.png", "Cửa sổ Chọn trường xuất file — mặc định chọn sẵn cả 6 trường")
b.para("Hai điểm cần nhớ:")
b.bullet("⚠ File xuất ra KHÔNG áp bộ lọc đang có trên màn hình. Dù bạn đang lọc còn vài dòng, file "
         "vẫn chứa toàn bộ gói bảo dưỡng của danh mục.")
b.bullet("⚠ Thứ tự cột trong file chạy theo THỨ TỰ BẠN CHỌN trong cửa sổ, không theo thứ tự cột "
         "trên bảng. Muốn cột nào đứng trước thì chọn cột đó trước.")
b.para("Bỏ chọn hết trường thì nút Xuất file không bấm được. Mã gói toàn số như “01” vẫn giữ "
       "nguyên số 0 ở đầu khi mở bằng Excel.")

b.h2("2. In phiếu Danh mục kiểm tra bảo dưỡng định kỳ")
b.bullet("Cách 1: Mở menu ba chấm ở dòng cần in và bấm “In”.")
b.bullet("Cách 2: Mở màn chi tiết của gói rồi bấm nút “In” ở chân trang.")
b.para("Phiếu mở ở TAB MỚI, danh sách ở tab cũ giữ nguyên bộ lọc và trang đang xem.")
b.image("10-in-phieu.png", "Màn In phiếu Danh mục kiểm tra bảo dưỡng định kỳ")

b.h2("3. Nội dung phiếu in")
b.bullet("Đầu phiếu: logo và thông tin công ty.")
b.bullet("Tiêu đề “DANH MỤC KIỂM TRA BẢO DƯỠNG ĐỊNH KỲ” và dòng “TÊN DỊCH VỤ: <tên gói in hoa>”.")
b.bullet("Bảng gồm STT, Nội dung kiểm tra bảo dưỡng, SL, các cột cấp bảo dưỡng, cột Kiểm tra "
         "(Có/Không) và cột Ghi chú để kỹ thuật viên điền tay ngoài hiện trường.")
b.bullet("Cuối phiếu: phần Ghi chú của gói và bảng giải thích các ký hiệu như KTBM, DK, CC, VS.")
b.para("Bấm nút “In” ở góc trái phía trên để mở hộp thoại in của trình duyệt. Bản in tự ẩn menu "
       "bên trái và ẩn chính nút In.")
b.para("Gói chưa khai nội dung kiểm tra vẫn in được, chỉ là bảng nội dung để trống.")

# ============================================================================
b.h1("PHẦN 9: XEM LỊCH SỬ THAY ĐỔI")

b.h2("1. Cách mở")
b.para("Mở menu ba chấm ở dòng cần xem rồi bấm “Lịch sử”. Cửa sổ “Lịch sử thay đổi” hiện ra kèm "
       "dòng phụ “Gói bảo dưỡng: <mã> - <tên>”. Chức năng này không đòi quyền riêng.")
b.image("12-lich-su.png", "Cửa sổ Lịch sử thay đổi của một gói bảo dưỡng")

b.h2("2. Đọc một mốc lịch sử")
b.bullet("Ngày giờ thực hiện.")
b.bullet("Nhãn hành động: Tạo mới, Thay đổi thông tin, Khóa hoặc Mở khóa.")
b.bullet("Tên người thực hiện kèm phòng ban.")
b.bullet("Chi tiết thay đổi dạng “Tên trường: giá trị cũ → giá trị mới”, ví dụ “Trạng thái: Khóa → "
         "Hoạt động”.")
b.para("Các mốc xếp mới nhất trước.")

b.h2("3. Những trường được theo dõi")
b.table([
    ["Trường", "Có ghi lịch sử không"],
    ["Mã gói bảo dưỡng", "Có"],
    ["Tên gói bảo dưỡng", "Có"],
    ["Định mức đàm phán giá", "Có"],
    ["VAT", "Có"],
    ["Ghi chú", "Có"],
    ["Trạng thái", "Có"],
    ["Nội dung kiểm tra, cấp bảo dưỡng, định mức công, giá", "KHÔNG"],
    ["Hệ số giá bán theo công ty", "KHÔNG"],
    ["Hàng hoá áp dụng, file đính kèm", "KHÔNG"],
])
b.para("Vì vậy nếu bạn chỉ sửa bảng ma trận hoặc hệ số theo công ty thì lịch sử sẽ không có mốc "
       "mới — đây là thiết kế hiện tại, không phải mất dữ liệu.")

b.h2("4. Lọc lịch sử")
b.para("Bấm nút “Bộ lọc” trong cửa sổ để lọc theo loại hoạt động. Có 3 nhóm dùng chung cho mọi màn "
       "danh mục:")
b.bullet("Tạo mới.")
b.bullet("Thay đổi thông tin.")
b.bullet("Thay đổi trạng thái (gồm Khóa và Mở khóa).")
b.para("Gói chưa phát sinh thao tác nào thì cửa sổ hiện “Chưa có lịch sử thao tác nào.”.")

# ============================================================================
b.h1("PHẦN 10: HƯỚNG DẪN THEO TỪNG QUYỀN")

b.h2("1. Người dùng KHÔNG có quyền nào của màn")
b.para("Bạn vẫn vào được màn hình và vẫn thấy đủ danh sách gói bảo dưỡng. Bạn làm được:")
b.bullet("Tìm kiếm, lọc, sắp xếp, tuỳ chỉnh cột hiển thị.")
b.bullet("Xem chi tiết một gói và mở file đính kèm.")
b.bullet("In phiếu Danh mục kiểm tra bảo dưỡng định kỳ.")
b.bullet("Xuất Excel danh sách.")
b.bullet("Xem lịch sử thay đổi.")
b.para("Bạn KHÔNG thấy nút Tạo mới; trên từng dòng chỉ còn In và Lịch sử. Cần thao tác thêm thì đề "
       "nghị quản trị cấp quyền tương ứng.")

b.h2("2. Người dùng có quyền “Thêm danh mục gói bảo dưỡng”")
b.bullet("Có nút Tạo mới ở góc phải trên bảng.")
b.bullet("Có nút Nhân bản trong menu ba chấm và ở chân trang chi tiết.")
b.bullet("Không có nút Sửa và nút Xóa — muốn sửa lại gói vừa tạo thì cần thêm quyền Sửa.")

b.h2("3. Người dùng có quyền “Sửa danh mục gói bảo dưỡng”")
b.bullet("Dòng đang Hoạt động: có nút Sửa.")
b.bullet("Dòng đang Khóa: có nút Mở khóa.")
b.bullet("Không có nút Tạo mới, Nhân bản và Xóa.")

b.h2("4. Người dùng có quyền “Xóa danh mục gói bảo dưỡng”")
b.bullet("Có nút Xóa ở những gói đang Hoạt động và chưa được sử dụng.")
b.bullet("Gói đã gắn hàng hoá hoặc đã dùng ở báo giá dịch vụ thì vẫn không có nút Xóa — đây là "
         "ràng buộc dữ liệu, không phải thiếu quyền.")

b.h2("5. Câu hỏi thường gặp")

b.h3("5.1 Khai một gói bảo dưỡng mới thì làm thế nào")
b.bullet("Bước 1: Gõ tên hoặc mã dự kiến vào ô tìm nhanh để chắc chắn chưa có gói trùng.")
b.bullet("Bước 2: Bấm Tạo mới, nhập Tên, Mã và kiểm tra ô Công ty quản lý gói bảo dưỡng.")
b.bullet("Bước 3: Thêm các dòng nội dung kiểm tra, thêm cột cấp bảo dưỡng và chọn ghi chú kiểm tra "
         "ở các ô giao nhau.")
b.bullet("Bước 4: Nhập Định mức công cho từng cấp, kiểm tra lại Giá vốn và Giá bán cơ sở hệ thống "
         "tính ra.")
b.bullet("Bước 5: Chọn hàng hoá áp dụng, đính kèm ít nhất 1 file PDF rồi bấm Lưu.")

b.h3("5.2 Giá bán hiện ra không đúng như mong đợi")
b.para("Kiểm tra theo thứ tự: ô Công ty quản lý gói bảo dưỡng (quyết định đơn giá công), Định mức "
       "công, Hệ số công nghệ, Hệ số giá bán gói, rồi mới tới hệ số của từng công ty. Công thức "
       "đầy đủ ghi ở PHẦN 4 mục 5.")

b.h3("5.3 Vì sao không thấy nút Xóa ở gói cần bỏ")
b.para("Ba khả năng: bạn chưa có quyền Xóa; gói đang ở trạng thái Khóa; hoặc gói đã được sử dụng "
       "(đã gắn hàng hoá hoặc đã dùng ở báo giá dịch vụ). Trường hợp cuối thì cách xử lý đúng là "
       "chuyển gói sang trạng thái Khóa chứ không xoá.")

b.h3("5.4 Không sửa được một gói")
b.para("Kiểm tra trạng thái: gói đang Khóa thì nút Sửa bị ẩn, phải Mở khóa trước. Nếu vẫn thấy nút "
       "Sửa mà bấm Lưu báo lỗi, nghĩa là gói vừa bị người khác khóa — bấm Làm mới rồi thao tác "
       "lại.")

b.h3("5.5 Không bỏ được một cột cấp bảo dưỡng")
b.para("Cấp đó đã được dùng trong báo giá dịch vụ nên hệ thống chặn để không phá dữ liệu chứng từ "
       "cũ. Hãy xử lý các báo giá liên quan trước, hoặc giữ nguyên cấp đó.")

b.h3("5.6 File Excel xuất ra nhiều dòng hơn danh sách đang xem")
b.para("Đúng như thiết kế hiện tại: file xuất luôn lấy toàn bộ danh mục, không áp bộ lọc trên màn "
       "hình. Nếu chỉ cần phần đang lọc, hãy lọc lại trong Excel sau khi tải về.")

b.h3("5.7 Nhập 12,5 vào ô VAT có bị hiểu thành 125 không")
b.para("Không. Các ô số ở màn này nhận dấu phẩy làm dấu thập phân, nên 12,5 được hiểu là mười hai "
       "phẩy năm. Mở lại màn Sửa sẽ thấy đúng giá trị đã nhập.")

b.h3("5.8 Danh sách thiếu gói so với lúc trước")
b.para("Thường do bộ lọc còn giữ điều kiện cũ, hệ thống ghi nhớ trong 10 phút. Bấm “Làm mới” ở "
       "khối bộ lọc để xem lại toàn bộ danh sách.")

b.h3("5.9 Không biết ai đã sửa dữ liệu")
b.para("Mở menu ba chấm ở dòng đó và bấm Lịch sử. Cửa sổ liệt kê từng mốc kèm tên người thực hiện, "
       "thời điểm và giá trị trước - sau. Lưu ý lịch sử chỉ theo dõi các trường của khối Thông tin "
       "chung.")

b.finish()
