# -*- coding: utf-8 -*-
"""Noi dung HDSD man Danh muc khach hang."""


def build(b):
    # ============================================================ TỔNG QUAN
    b.h1("TỔNG QUAN")

    b.h2("1. Thuật ngữ sử dụng trong tài liệu")
    b.table([
        ["Thuật ngữ", "Giải thích"],
        ["Khách hàng cá nhân",
         "Khách hàng có Loại hình tổ chức là “Cá nhân”. Nhóm này có quy tắc hiển thị riêng, "
         "xem mục 4.3."],
        ["Khách hàng tổ chức",
         "Khách hàng thuộc một trong bốn loại: Doanh nghiệp tư nhân, Doanh nghiệp nước ngoài, "
         "Tổ chức phi chính phủ, Cơ quan nhà nước."],
        ["Công ty mẹ",
         "Một khách hàng khác được chọn làm đơn vị chủ quản, dùng cho chi nhánh hoặc đơn vị "
         "trực thuộc."],
        ["Người đại diện",
         "Người đại diện pháp luật của khách hàng tổ chức."],
        ["Người liên hệ",
         "Đầu mối làm việc thực tế. Một khách hàng tổ chức có thể có nhiều người liên hệ."],
        ["Khóa khách hàng",
         "Chuyển khách hàng sang trạng thái Khóa. Khách hàng KHÔNG bị xóa, vẫn nằm trong danh "
         "sách, chỉ không chọn được ở các màn nghiệp vụ khác."],
        ["Loại hình hoạt động – Lĩnh vực kinh doanh",
         "Cặp phân loại ngành nghề của khách hàng. Luôn khai theo cặp, lĩnh vực phải thuộc đúng "
         "loại hình đã chọn."],
    ])

    b.h2("2. Cập nhật tài liệu")
    b.table([
        ["Phiên bản", "Ngày", "Người cập nhật", "Nội dung"],
        ["1.0", "15/08/2026", "Tri Lee", "Lập mới cho màn Danh mục khách hàng sau khi gộp dữ liệu "
                                        "khách hàng của hai phần mềm cũ."],
    ])

    b.h2("3. Giới thiệu chung")
    b.para("Danh mục khách hàng là nơi quản lý tập trung toàn bộ khách hàng của công ty. Từ màn "
           "hình này, người dùng tra cứu thông tin khách hàng, thêm khách hàng mới, cập nhật "
           "thông tin, khóa những khách hàng không còn giao dịch, nhập hàng loạt từ file Excel, "
           "xuất danh sách ra file và mở màn Quản lý khách hàng để xem toàn bộ lịch sử giao dịch "
           "của một khách hàng.")
    b.para("Đường dẫn truy cập:")
    b.bullet("Menu: Phân hệ Giao việc → Danh mục chung → Danh mục khách hàng")
    b.bullet("Hoặc gõ thẳng đường dẫn /assign/customers vào thanh địa chỉ trình duyệt")

    b.h2("4. Quyền và phạm vi dữ liệu")

    b.h3("4.1 Bảng quyền của màn hình")
    b.table([
        ["Tên quyền", "Cho phép làm gì", "Nút / thẻ tương ứng", "Ghi chú"],
        ["Xem khách hàng",
         "Mở màn Quản lý khách hàng và xem các thẻ nghiệp vụ",
         "Menu ba chấm → Quản lý; các thẻ Báo giá, Hợp đồng, Danh sách trang thiết bị",
         "Thiếu quyền thì các thẻ này báo không có quyền."],
        ["Thêm khách hàng",
         "Thêm khách hàng mới và nhập hàng loạt từ file Excel",
         "Nút Tạo mới, nút Import Excel",
         "Thiếu quyền thì hai nút này không hiển thị."],
        ["Sửa khách hàng",
         "Cập nhật thông tin khách hàng; thêm / sửa / xóa trang thiết bị; tải ảnh và tài liệu",
         "Biểu tượng bút chì trên cột Hành động; các nút thao tác ở thẻ Danh sách trang thiết bị "
         "và thẻ Thông tin khác",
         "Thiếu quyền thì nút bị làm mờ chứ không bị ẩn."],
        ["Xóa khách hàng",
         "Khóa và Mở khóa khách hàng",
         "Biểu tượng ổ khóa trên cột Hành động",
         "Không có quyền riêng mang tên Khóa; hai thao tác này dùng chung quyền Xóa khách hàng."],
        ["Xuất dữ liệu khách hàng",
         "Xuất danh sách ra file",
         "Nút Xuất CSV, Xuất Excel, Xuất PDF",
         "Thiếu quyền thì ba nút này không dùng được."],
    ])

    b.h3("4.2 Bốn cấp phạm vi dữ liệu")
    b.para("Ngoài các quyền thao tác ở trên, hệ thống còn có bốn quyền quyết định NHÌN THẤY BAO "
           "NHIÊU khách hàng. Hệ thống xét từ trên xuống, ai có cấp nào trước thì áp cấp đó:")
    b.table([
        ["Tên quyền", "Nhìn thấy"],
        ["Xem tất cả khách hàng", "Toàn bộ khách hàng của hệ thống."],
        ["Xem tất cả khách hàng của công ty",
         "Khách hàng đã phát sinh báo giá thuộc công ty của mình."],
        ["Xem tất cả khách hàng của phòng ban", "Giới hạn theo phòng ban của mình."],
        ["Xem tất cả khách hàng của bộ phận", "Giới hạn theo bộ phận của mình."],
        ["(không có quyền nào ở trên)",
         "Chỉ khách hàng do chính mình tạo, cộng khách hàng mình đang đăng ký còn hạn hoặc đã "
         "từng làm việc."],
    ])
    b.para("Lưu ý quan trọng: bản thân việc MỞ màn hình này không cần quyền. Ai đăng nhập cũng vào "
           "được, chỉ khác nhau ở số lượng khách hàng nhìn thấy. Nếu anh/chị thấy danh sách ít hơn "
           "đồng nghiệp, đó là do cấp phạm vi dữ liệu khác nhau, không phải lỗi hệ thống.")
    b.para("Dù ở cấp nào, anh/chị LUÔN nhìn thấy những khách hàng do chính mình tạo ra.")

    b.h3("4.3 Quy tắc riêng với khách hàng cá nhân")
    b.para("Khách hàng cá nhân được bảo vệ thêm một lớp để tránh tình trạng tranh giành khách. "
           "Một khách hàng cá nhân chỉ hiện trong danh sách khi thỏa ít nhất một điều kiện sau:")
    b.bullet("Do chính mình tạo ra")
    b.bullet("Mình đang đăng ký khách hàng đó và còn trong thời hạn")
    b.bullet("Đang có người khác đăng ký khách hàng đó và còn trong thời hạn")
    b.bullet("Khách hàng đó đã phát sinh báo giá, cuộc họp hoặc dự án tiềm năng — của bất kỳ ai")
    b.para("Khách hàng cá nhân không thỏa điều kiện nào ở trên được gọi là khách hàng tự do và "
           "KHÔNG hiện trong danh sách. Muốn tìm khách hàng tự do, anh/chị phải gõ ĐÚNG TRỌN VẸN "
           "số điện thoại của họ vào ô tìm kiếm. Gõ thiếu một chữ số sẽ không ra kết quả — đây là "
           "quy tắc cố ý, không phải lỗi tìm kiếm.")
    b.para("Khách hàng tổ chức không chịu quy tắc này.")

    # ============================================================ PHẦN 1
    b.h1("PHẦN 1: TRUY CẬP VÀ BỐ CỤC MÀN HÌNH")

    b.h2("1. Truy cập màn hình")
    b.para("Đăng nhập hệ thống, vào menu Phân hệ Giao việc → Danh mục chung → Danh mục khách hàng. "
           "Hệ thống hiển thị danh sách khách hàng nằm trong phạm vi dữ liệu của anh/chị.")
    b.image("kh_01_danhsach.png", "Màn hình Danh mục khách hàng khi mới truy cập")

    b.h2("2. Bố cục màn hình")
    b.para("Màn hình chia làm ba khu vực từ trên xuống:")
    b.bullet("Khu vực tìm kiếm và bộ lọc — ô tìm kiếm nhanh, nút Tìm kiếm nâng cao, nút Làm mới "
             "và nút Cài đặt bộ lọc.")
    b.bullet("Thanh công cụ — các nút Tạo mới, Import Excel, Xuất CSV, Xuất Excel, Xuất PDF và "
             "biểu tượng tuỳ chỉnh cột ở góc phải.")
    b.bullet("Bảng danh sách — các cột thông tin khách hàng, cột Hành động ở cuối, phân trang và "
             "ô hiển thị tổng số bản ghi ở dưới cùng.")

    b.h2("3. Các cột của bảng danh sách")
    b.table([
        ["Cột", "Nội dung"],
        ["STT", "Số thứ tự, chạy liên tục qua các trang. Luôn hiển thị, không tắt được."],
        ["Mã KH", "Mã khách hàng do hệ thống sinh tự động. Bấm vào mở màn chi tiết. Luôn hiển thị."],
        ["Tên khách hàng", "Tên đầy đủ của khách hàng."],
        ["Tên viết tắt", "Tên gọi tắt, dùng cho các mẫu in ngắn gọn."],
        ["Loại", "Một trong năm loại hình tổ chức."],
        ["MST", "Mã số thuế."],
        ["SĐT", "Các số điện thoại, ngăn nhau bằng dấu phẩy."],
        ["Email", "Địa chỉ thư điện tử."],
        ["Nhóm KH", "Các nhóm khách hàng, ngăn nhau bằng dấu phẩy."],
        ["Địa chỉ, Tỉnh/TP", "Địa chỉ liên hệ chính."],
        ["Tên đơn vị", "Tên gara hoặc đơn vị công tác, thường dùng với khách hàng cá nhân."],
        ["Địa chỉ xuất hóa đơn", "Địa chỉ ghi trên hóa đơn."],
        ["Công ty mẹ, Hãng xe, Người tạo, Người sửa (gần nhất)",
         "Bốn cột này MẶC ĐỊNH ẨN. Bật lên ở cửa sổ tuỳ chỉnh cột. Lưu ý: bật bốn cột này làm "
         "bảng nạp chậm hơn."],
        ["Trạng thái", "Hoạt động hoặc Khóa."],
        ["Hành động", "Biểu tượng bút chì (Sửa), ổ khóa (Khóa / Mở khóa) và menu ba chấm."],
    ])

    b.h2("4. Cột Hành động")
    b.para("Trên mỗi dòng, cột Hành động có ba phần:")
    b.bullet("Biểu tượng bút chì — mở màn Chỉnh sửa. Yêu cầu quyền Sửa khách hàng.",
             bold_prefix=None)
    b.bullet("Biểu tượng ổ khóa — Khóa hoặc Mở khóa khách hàng. Yêu cầu quyền Xóa khách hàng.")
    b.bullet("Menu ba chấm — chứa hai mục Quản lý và Lịch sử.")
    b.image("kh_05_menu_hanhdong.png", "Menu ba chấm trên cột Hành động")
    b.para("Nếu thiếu quyền, nút tương ứng bị làm mờ chứ không bị ẩn đi, để anh/chị biết chức năng "
           "có tồn tại và cần đề nghị cấp quyền.")

    b.h2("5. Phân trang")
    b.para("Cuối bảng có ô “Hiển thị a–b / N”. Con số N là TỔNG số khách hàng khớp bộ lọc đang áp "
           "dụng, không phải tổng số khách hàng của toàn hệ thống. Đổi bộ lọc thì con số này đổi "
           "theo.")
    b.para("Anh/chị đổi được số dòng mỗi trang. Sau khi đổi, hệ thống tự quay về trang 1.")

    # ============================================================ PHẦN 2
    b.h1("PHẦN 2: TÌM KIẾM VÀ LỌC DANH SÁCH")

    b.h2("1. Tìm kiếm nhanh")
    b.para("Gõ từ khóa vào ô tìm kiếm ở đầu màn hình. Hệ thống tìm đồng thời trên tên khách hàng, "
           "mã khách hàng, mã số thuế và số điện thoại. Không phân biệt chữ hoa chữ thường.")
    b.para("Xóa hết từ khóa thì danh sách quay về đầy đủ và về trang 1.")

    b.h2("2. Bộ lọc nâng cao")
    b.para("Bấm nút Tìm kiếm nâng cao để mở panel bộ lọc. Con số hiển thị trên nút là SỐ TIÊU CHÍ "
           "đang có giá trị, không phải số bản ghi.")
    b.image("kh_02_boloc_nangcao.png", "Panel Bộ lọc nâng cao với đầy đủ tiêu chí")

    b.h3("2.1 Danh sách tiêu chí lọc")
    b.table([
        ["Tiêu chí", "Cách dùng"],
        ["Công ty – Phòng ban – Bộ phận – Nhân viên",
         "Chọn theo cây đơn vị, chọn được tới cấp nhân viên."],
        ["Quốc gia", "Chọn quốc gia. Quyết định danh sách của ô Tỉnh/Thành phố bên dưới."],
        ["Tỉnh/Thành phố",
         "Chỉ hiện tỉnh thành thuộc quốc gia đã chọn. Đổi quốc gia thì ô này bị xóa trắng."],
        ["Mã khách hàng", "Nhập một phần mã, hệ thống tìm mọi mã có chứa đoạn đó."],
        ["MST/SĐT",
         "Nhập mã số thuế hoặc số điện thoại. Tìm được cả khi số cần tìm nằm ở vị trí thứ hai, "
         "thứ ba trong danh sách nhiều số."],
        ["Tên khách hàng", "Nhập một phần tên."],
        ["Số CCCD", "Dùng cho khách hàng cá nhân."],
        ["Tên đơn vị", "Tên gara hoặc đơn vị công tác."],
        ["Loại hình tổ chức", "Chọn một trong năm loại."],
        ["Trạng thái", "Hoạt động hoặc Khóa. Bỏ trống thì hiện cả hai."],
        ["Loại hình hoạt động – Lĩnh vực kinh doanh",
         "Chọn theo CẶP, không chọn rời từng vế."],
        ["Người sửa gần nhất", "Chọn nhân viên đã sửa khách hàng gần nhất."],
        ["Khách hàng hãng", "Có hoặc Không."],
        ["Hãng xe", "Chọn hãng xe cụ thể."],
        ["Cấp đại lý", "Chọn cấp đại lý."],
    ])

    b.h3("2.2 Cách áp dụng và xóa bộ lọc")
    b.para("Chọn xong các tiêu chí, bấm Tìm kiếm. Các tiêu chí kết hợp với nhau theo kiểu VÀ — "
           "chỉ khách hàng thỏa đồng thời tất cả các tiêu chí mới hiện ra.")
    b.para("Bấm Làm mới để xóa toàn bộ tiêu chí. Danh sách nạp lại ngay lập tức, tổng số bản ghi "
           "quay về đầy đủ.")
    b.para("Nếu đóng panel bộ lọc mà chưa bấm Tìm kiếm thì kết quả trên bảng không thay đổi.")
    b.para("Ô tìm kiếm nhanh và bộ lọc nâng cao dùng được cùng lúc, cái này không xóa cái kia.")

    b.h2("3. Cài đặt bộ lọc")
    b.para("Nếu anh/chị chỉ dùng vài tiêu chí quen thuộc, có thể ẩn bớt các ô lọc không cần. "
           "Bấm nút Cài đặt bộ lọc trong panel bộ lọc.")
    b.image("kh_03_caidat_boloc.png", "Cửa sổ Cài đặt bộ lọc")
    b.para("Trong cửa sổ này:")
    b.bullet("Bỏ tích một ô lọc để ẩn nó khỏi panel bộ lọc.")
    b.bullet("Dùng tay nắm bên trái để kéo đổi thứ tự các ô lọc.")
    b.bullet("Bấm Lưu để ghi nhận. Cấu hình này lưu riêng cho tài khoản của anh/chị, không ảnh "
             "hưởng người khác, và còn nguyên sau khi đăng nhập lại.")
    b.para("Lưu ý: ẩn một ô lọc chỉ ẩn trên giao diện. Nếu ô lọc đó đang có giá trị thì giá trị "
           "vẫn còn tác dụng lên kết quả cho tới khi anh/chị bấm Làm mới.")

    b.h2("4. Tuỳ chỉnh cột hiển thị")
    b.para("Bấm biểu tượng tuỳ chỉnh cột ở góc phải thanh công cụ.")
    b.image("kh_04_cauhinh_cot.png", "Cửa sổ tuỳ chỉnh cột hiển thị")
    b.bullet("Tích hoặc bỏ tích để hiện / ẩn từng cột.")
    b.bullet("Kéo để đổi thứ tự cột.")
    b.bullet("Cột STT và Mã KH bị khóa, luôn hiển thị, không bỏ tích được.")
    b.bullet("Bấm Lưu để ghi nhận. Cấu hình lưu riêng theo tài khoản.")
    b.para("Bốn cột Công ty mẹ, Hãng xe, Người tạo và Người sửa (gần nhất) mặc định ẩn vì làm bảng "
           "nạp chậm hơn. Chỉ nên bật khi thực sự cần.")

    # ============================================================ PHẦN 3
    b.h1("PHẦN 3: THÊM MỚI KHÁCH HÀNG")
    b.para("Yêu cầu quyền: Thêm khách hàng. Nếu không có quyền này, nút Tạo mới sẽ không hiển thị; "
           "trường hợp truy cập trực tiếp bằng đường dẫn, hệ thống báo lỗi không có quyền.")

    b.h2("1. Mở màn thêm mới")
    b.para("Bấm nút Tạo mới trên thanh công cụ. Hệ thống mở màn Tạo khách hàng mới. Ban đầu chỉ "
           "hiện khối Thông tin khách hàng; các khối còn lại hiện ra sau khi anh/chị chọn Loại "
           "hình tổ chức.")

    b.h2("2. Chọn Loại hình tổ chức trước tiên")
    b.para("Ô Loại hình tổ chức quyết định các khối nhập liệu bên dưới:")
    b.table([
        ["Chọn", "Các khối hiện ra"],
        ["Cá nhân", "Thông tin khách hàng + Thông tin cá nhân"],
        ["Doanh nghiệp tư nhân / Doanh nghiệp nước ngoài / Tổ chức phi chính phủ / "
         "Cơ quan nhà nước",
         "Thông tin khách hàng + Thông tin tổ chức + Người liên hệ"],
    ])
    b.para("Lưu ý: nếu đổi Loại hình tổ chức sau khi đã nhập, các khối cũ sẽ biến mất và dữ liệu "
           "đã gõ ở đó không được mang sang khối mới. Nên chọn loại hình trước rồi mới nhập.")
    b.para("Khối Địa chỉ giao hàng KHÔNG hiện ở màn thêm mới. Khối này chỉ xuất hiện khi anh/chị "
           "sửa một khách hàng đã có.")

    b.h2("3. Thêm mới khách hàng cá nhân")
    b.image("kh_08_taomoi_canhan.png", "Màn thêm mới khi chọn Loại hình tổ chức là Cá nhân")
    b.table([
        ["Trường", "Kiểu nhập", "Bắt buộc", "Giá trị ban đầu", "Ghi chú"],
        ["Tên khách hàng", "Ô nhập chữ", "Có", "Trống",
         "Bỏ trống sẽ báo “Bắt buộc phải nhập”."],
        ["Loại hình tổ chức", "Danh sách chọn", "Có", "Trống", "Chọn Cá nhân."],
        ["Tên viết tắt", "Ô nhập chữ", "Không", "Trống", ""],
        ["Là nhà cung cấp", "Ô tích", "Không", "Không tích",
         "Tích khi đối tác vừa là khách hàng vừa là nhà cung cấp."],
        ["Là khách hãng", "Ô tích", "Không", "Không tích",
         "Tích thì bắt buộc phải chọn Hãng xe."],
        ["Hãng xe", "Danh sách chọn", "Có khi tích Là khách hãng", "Trống",
         "Bỏ trống sẽ báo “Bắt buộc khi là khách hãng”."],
        ["Nhóm khách hàng", "Danh sách chọn nhiều", "Không", "Trống", ""],
        ["Loại hình hoạt động – Lĩnh vực kinh doanh", "Danh sách chọn", "Không", "Trống",
         "Khai theo cặp; thêm được nhiều cặp."],
        ["Email", "Ô nhập chữ", "Không", "Trống",
         "Phải đúng định dạng thư điện tử và chưa ai dùng. Trùng sẽ báo “Email đã tồn tại”."],
        ["Số điện thoại", "Ô nhập chữ", "Có", "Trống",
         "Ít nhất một số. Phải bắt đầu bằng chữ số 0 và dài từ 10 đến 12 chữ số. "
         "Thêm được nhiều số."],
        ["Số CMND/CCCD", "Ô nhập chữ", "Không", "Trống",
         "Không được trùng với khách hàng khác."],
        ["Ngày sinh", "Chọn ngày", "Không", "Trống", "Không được chọn ngày ở tương lai."],
        ["Ngày cấp, Nơi cấp", "Chọn ngày / Ô nhập chữ", "Không", "Trống",
         "Ngày cấp không được ở tương lai."],
        ["Tên đơn vị", "Ô nhập chữ", "Không", "Trống", "Tên gara hoặc nơi công tác."],
        ["Quốc gia", "Danh sách chọn", "Có", "Trống", ""],
        ["Tỉnh/Thành phố", "Danh sách chọn", "Có", "Trống", "Phụ thuộc Quốc gia."],
        ["Quận/Huyện", "Danh sách chọn", "Không", "Trống", "Phụ thuộc Tỉnh/Thành phố."],
        ["Phường/Xã", "Danh sách chọn", "Có", "Trống", "Phụ thuộc Quận/Huyện."],
        ["Thôn/Xóm, Số nhà – đường", "Danh sách chọn / Ô nhập chữ", "Không", "Trống", ""],
        ["Số tài khoản, Chủ tài khoản, Ngân hàng, Tỉnh/TP ngân hàng, Chi nhánh",
         "Ô nhập chữ / Danh sách chọn", "Không", "Trống",
         "Ô Chi nhánh chỉ hiện chi nhánh của ngân hàng và tỉnh thành đã chọn."],
    ])
    b.para("Giá trị điền sẵn khi thêm mới: mọi ô đều để trống. Mã khách hàng do hệ thống sinh tự "
           "động sau khi lưu, anh/chị không phải nhập. Trạng thái của khách hàng mới luôn là "
           "Hoạt động.")

    b.h2("4. Thêm mới khách hàng tổ chức")
    b.image("kh_09_taomoi_tochuc.png", "Màn thêm mới khi chọn loại hình tổ chức")
    b.para("Khách hàng tổ chức dùng chung khối Thông tin khách hàng và khối địa chỉ như khách hàng "
           "cá nhân. Khác biệt nằm ở hai khối sau:")

    b.h3("4.1 Khối Thông tin tổ chức")
    b.table([
        ["Trường", "Kiểu nhập", "Bắt buộc", "Giá trị ban đầu", "Ghi chú"],
        ["Mã số thuế", "Ô nhập chữ", "Có khi KHÔNG chọn Công ty mẹ", "Trống",
         "Chỉ gồm chữ số và dấu gạch ngang, tối đa 14 ký tự. Không được trùng."],
        ["Công ty mẹ", "Danh sách chọn", "Không", "Trống",
         "Chọn khách hàng khác làm đơn vị chủ quản. CHỌN CÔNG TY MẸ THÌ MÃ SỐ THUẾ KHÔNG CÒN "
         "BẮT BUỘC, vì chi nhánh dùng chung mã số thuế của công ty mẹ."],
        ["Người đại diện", "Ô nhập chữ", "Có", "Trống",
         "Ít nhất một người. Phải có đủ cả tên và chức vụ."],
        ["Chức vụ người đại diện", "Ô nhập chữ", "Có", "Trống", ""],
        ["Địa chỉ xuất hoá đơn", "Ô nhập nhiều dòng", "Có", "Trống",
         "Bỏ trống sẽ báo “Bắt buộc nhập”."],
        ["Fax, Số điện thoại bàn", "Ô nhập chữ", "Không", "Trống", ""],
    ])

    b.h3("4.2 Khối Người liên hệ")
    b.table([
        ["Trường", "Kiểu nhập", "Bắt buộc", "Giá trị ban đầu", "Ghi chú"],
        ["Người liên hệ", "Ô nhập chữ", "Có", "Trống",
         "Phải có ít nhất một người liên hệ."],
        ["Chức vụ người liên hệ", "Ô nhập chữ", "Có", "Trống", ""],
        ["SĐT người liên hệ", "Ô nhập chữ", "Có", "Trống",
         "Mỗi người liên hệ phải có ít nhất một số điện thoại."],
        ["Số CMND/CCCD, Ngày sinh, Email của người liên hệ",
         "Ô nhập chữ / Chọn ngày", "Không", "Trống",
         "Ngày sinh không được ở tương lai."],
        ["Tài khoản ngân hàng của người liên hệ", "Ô nhập chữ", "Không", "Trống", ""],
    ])
    b.para("Bấm nút Thêm người liên hệ để khai thêm người liên hệ thứ hai, thứ ba.")

    b.h2("5. Lưu và các lỗi thường gặp")
    b.para("Nhập xong bấm nút Lưu ở cuối màn hình. Nếu dữ liệu hợp lệ, hệ thống báo thêm mới thành "
           "công và quay về danh sách; khách hàng mới nằm trong danh sách với mã tự sinh và trạng "
           "thái Hoạt động.")
    b.para("Nếu còn thiếu sót, hệ thống báo lỗi đỏ ngay dưới ô tương ứng. Màn hình KHÔNG đóng và "
           "dữ liệu đã nhập vẫn còn nguyên — anh/chị chỉ cần sửa chỗ báo đỏ rồi bấm Lưu lại.")
    b.image("kh_10_validate.png", "Hệ thống báo lỗi đỏ ngay dưới ô còn thiếu")
    b.table([
        ["Thông báo", "Nguyên nhân và cách xử lý"],
        ["Bắt buộc phải nhập", "Chưa nhập Tên khách hàng."],
        ["Bắt buộc nhập", "Chưa chọn Loại hình tổ chức, hoặc chưa nhập Địa chỉ xuất hoá đơn, "
                          "hoặc chưa nhập Mã số thuế khi không chọn Công ty mẹ."],
        ["Bắt buộc phải nhập số điện thoại", "Khách hàng cá nhân chưa có số điện thoại nào."],
        ["Số điện thoại không đúng định dạng",
         "Số phải bắt đầu bằng chữ số 0 và dài từ 10 đến 12 chữ số."],
        ["Phải có ít nhất 1 người đại diện", "Khách hàng tổ chức chưa khai người đại diện."],
        ["Phải có ít nhất 1 liên hệ", "Khách hàng tổ chức chưa khai người liên hệ."],
        ["Mã số thuế không đúng định dạng",
         "Mã số thuế chỉ được gồm chữ số và dấu gạch ngang, tối đa 14 ký tự."],
        ["Mã số thuế đã tồn tại", "Đã có khách hàng khác dùng mã số thuế này."],
        ["Email đã tồn tại", "Đã có khách hàng khác dùng địa chỉ thư điện tử này."],
        ["Số CMND/CCCD đã tồn tại", "Đã có khách hàng khác dùng số giấy tờ này."],
        ["Không được lớn hơn ngày hiện tại", "Ngày sinh hoặc ngày cấp đang là ngày ở tương lai."],
        ["Lĩnh vực không thuộc loại hình đã chọn, vui lòng chọn lại",
         "Cặp Loại hình hoạt động – Lĩnh vực kinh doanh không khớp nhau."],
        ["Bắt buộc chọn quốc gia / tỉnh–thành phố / phường–xã",
         "Ba ô địa chỉ này bắt buộc. Riêng Quận/Huyện và Thôn/Xóm thì không bắt buộc."],
        ["Bắt buộc khi là khách hãng", "Đã tích Là khách hãng nhưng chưa chọn Hãng xe."],
    ])
    b.para("Nếu anh/chị bấm Quay lại khi đã nhập dở, hệ thống hỏi xác nhận rời khỏi trang. Chọn ở "
           "lại thì dữ liệu còn nguyên; chọn rời đi thì mọi thứ vừa nhập sẽ mất.")

    # ============================================================ PHẦN 4
    b.h1("PHẦN 4: CHỈNH SỬA VÀ XEM CHI TIẾT")

    b.h2("1. Chỉnh sửa khách hàng")
    b.para("Yêu cầu quyền: Sửa khách hàng. Nếu không có quyền này, biểu tượng bút chì sẽ bị làm "
           "mờ; trường hợp truy cập trực tiếp bằng đường dẫn, hệ thống báo lỗi không có quyền.")
    b.para("Bấm biểu tượng bút chì trên cột Hành động của dòng cần sửa. Hệ thống mở màn Chỉnh sửa "
           "khách hàng với đầy đủ dữ liệu hiện tại.")
    b.image("kh_16_sua.png", "Màn Chỉnh sửa khách hàng")
    b.para("Các trường và quy tắc bắt buộc giống hệt màn thêm mới. Có ba điểm khác cần lưu ý:")
    b.bullet("Màn sửa có thêm khối Địa chỉ giao hàng — khối này không có ở màn thêm mới.")
    b.bullet("Mã khách hàng không sửa được và không thay đổi sau khi lưu.")
    b.bullet("Giữ nguyên mã số thuế của chính khách hàng đó thì lưu bình thường, hệ thống không "
             "báo trùng. Chỉ khi đổi sang mã số thuế của khách hàng khác mới bị chặn.")
    b.para("Sửa xong bấm Lưu. Hệ thống báo cập nhật thành công và quay về danh sách. Mọi thay đổi "
           "đều được ghi vào Lịch sử.")

    b.h2("2. Xem chi tiết khách hàng")
    b.para("Bấm vào Mã KH trên bảng danh sách để mở màn chi tiết. Mọi thông tin ở chế độ chỉ đọc, "
           "không sửa được và không có nút Lưu.")
    b.image("kh_13_chitiet.png", "Màn Chi tiết khách hàng ở chế độ chỉ đọc")

    # ============================================================ PHẦN 5
    b.h1("PHẦN 5: KHÓA VÀ MỞ KHÓA KHÁCH HÀNG")
    b.para("Yêu cầu quyền: Xóa khách hàng. Nếu không có quyền này, biểu tượng ổ khóa sẽ bị làm mờ; "
           "trường hợp truy cập trực tiếp bằng đường dẫn, hệ thống báo lỗi không có quyền.")

    b.h2("1. Khóa nghĩa là gì")
    b.para("Hệ thống KHÔNG có chức năng xóa vĩnh viễn khách hàng. Khi một khách hàng không còn "
           "giao dịch, anh/chị dùng thao tác Khóa. Sau khi khóa:")
    b.bullet("Khách hàng VẪN nằm trong danh sách, cột Trạng thái hiện chữ Khóa.")
    b.bullet("Vẫn xem được chi tiết, lịch sử và vẫn xuất ra file bình thường.")
    b.bullet("Mọi báo giá, hợp đồng, trang thiết bị của khách hàng đó vẫn còn nguyên.")
    b.bullet("Điểm khác biệt duy nhất: khách hàng đó không còn xuất hiện ở ô chọn khách hàng của "
             "các màn nghiệp vụ khác (lập báo giá, hợp đồng…).")

    b.h2("2. Các bước khóa khách hàng")
    b.para("Bấm biểu tượng ổ khóa trên cột Hành động của dòng cần khóa. Hệ thống hiện hộp xác nhận "
           "nêu rõ mã và tên khách hàng — hãy đọc kỹ để chắc chắn không bấm nhầm dòng.")
    b.image("kh_17_xacnhan_khoa.png", "Hộp xác nhận khóa khách hàng")
    b.bullet("Bấm Khóa để xác nhận. Hệ thống báo thành công, cột Trạng thái đổi ngay thành Khóa.")
    b.bullet("Bấm Hủy nếu bấm nhầm. Hộp đóng lại, trạng thái không đổi.")

    b.h2("3. Mở khóa khách hàng")
    b.para("Với khách hàng đang ở trạng thái Khóa, bấm lại biểu tượng ổ khóa trên dòng đó rồi xác "
           "nhận. Khách hàng trở về trạng thái Hoạt động và chọn lại được ở các màn nghiệp vụ.")
    b.para("Nếu khách hàng vừa bị người khác thao tác trước đó, hệ thống báo dữ liệu đã thay đổi. "
           "Anh/chị chỉ cần tải lại danh sách rồi thử lại.")

    # ============================================================ PHẦN 6
    b.h1("PHẦN 6: XEM LỊCH SỬ THAY ĐỔI")
    b.para("Bấm menu ba chấm trên cột Hành động rồi chọn Lịch sử.")
    b.image("kh_06_lichsu.png", "Cửa sổ Lịch sử khách hàng")
    b.para("Cửa sổ liệt kê mọi lần thay đổi của khách hàng đó, MỚI NHẤT Ở TRÊN CÙNG. Mỗi dòng cho "
           "biết:")
    b.bullet("Loại thay đổi: Thêm mới, Sửa hoặc đổi trạng thái.")
    b.bullet("Trường nào đã đổi, giá trị cũ và giá trị mới.")
    b.bullet("Ai thực hiện và vào lúc nào.")
    b.para("Khách hàng vừa được tạo, chưa sửa lần nào thì chỉ có một dòng Thêm mới — đây là bình "
           "thường, không phải lỗi. Thay đổi ở người liên hệ và thao tác Khóa / Mở khóa cũng được "
           "ghi lại thành dòng riêng.")

    # ============================================================ PHẦN 7
    b.h1("PHẦN 7: NHẬP KHÁCH HÀNG TỪ FILE EXCEL")
    b.para("Yêu cầu quyền: Thêm khách hàng. Nếu không có quyền này, nút Import Excel sẽ không hiển "
           "thị; trường hợp truy cập trực tiếp bằng đường dẫn, hệ thống báo lỗi không có quyền.")

    b.h2("1. Mở cửa sổ nhập dữ liệu")
    b.para("Bấm nút Import Excel trên thanh công cụ.")
    b.image("kh_11_import_excel.png", "Cửa sổ Import khách hàng")

    b.h2("2. Chuẩn bị file")
    b.para("Bấm nút Tải file mẫu để tải file về máy. File mẫu gồm ba trang: một trang để nhập liệu "
           "và các trang danh mục tra cứu (nhóm khách hàng, lĩnh vực, địa chỉ…) được sinh từ dữ "
           "liệu thật của hệ thống — anh/chị tra ở đây để điền cho đúng.")
    b.para("Ba điều bắt buộc phải nhớ khi điền file:")
    b.bullet("Dòng 1 là tiêu đề cột. DỮ LIỆU BẮT ĐẦU TỪ DÒNG 3. Điền vào dòng 2 sẽ bị bỏ qua.")
    b.bullet("Không đổi tên và không xóa các cột tiêu đề. Xóa cột bắt buộc thì hệ thống báo lỗi "
             "thiếu cột và không xử lý được.")
    b.bullet("Mỗi lần nhập tối đa 1.000 dòng. Danh sách dài hơn thì chia thành nhiều file.")
    b.para("Mẹo khai nhiều người liên hệ cho cùng một khách hàng: điền khách hàng ở dòng đầu, sau "
           "đó ở các dòng tiếp theo BỎ TRỐNG ô Tên khách hàng và chỉ điền thông tin người liên hệ. "
           "Hệ thống hiểu các dòng đó là người liên hệ của khách hàng ở dòng ngay trên. Lưu ý dòng "
           "bỏ trống Tên khách hàng KHÔNG được đứng đầu file.")

    b.h2("3. Ba bước nhập dữ liệu")
    b.table([
        ["Bước", "Nút bấm", "Việc hệ thống làm"],
        ["1", "Chọn file Excel rồi bấm Load lên bảng",
         "Đọc file và hiển thị dữ liệu lên bảng xem trước. Anh/chị sửa trực tiếp trên bảng được."],
        ["2", "Validate",
         "Kiểm tra từng dòng và báo lỗi kèm số dòng. CHƯA có khách hàng nào được ghi vào hệ thống "
         "ở bước này. Các dòng hợp lệ sẽ bị khóa lại không cho sửa tiếp."],
        ["3", "Import",
         "Ghi các dòng hợp lệ thành khách hàng mới và báo kết quả."],
    ])
    b.para("Tích ô Chỉ dòng lỗi để bảng chỉ hiện những dòng đang có lỗi, tiện cho việc sửa nhanh.")

    b.h2("4. Đọc kết quả nhập")
    b.para("Sau khi bấm Import, hệ thống báo ba con số: tổng số dòng đọc được, số dòng thêm thành "
           "công và số dòng lỗi. Ba con số này luôn cộng khớp với nhau. Có ba tình huống:")
    b.bullet("Tất cả dòng hợp lệ — hệ thống báo nhập thành công, toàn bộ khách hàng được thêm.")
    b.bullet("Một phần dòng lỗi — hệ thống báo nhập một phần thành công. Các dòng hợp lệ ĐÃ được "
             "thêm; các dòng lỗi thì không. Anh/chị sửa các dòng lỗi rồi nhập lại riêng chúng.")
    b.bullet("Toàn bộ dòng lỗi — hệ thống báo thất bại, không có khách hàng nào được thêm.")
    b.para("Các lỗi thường gặp trong file: thiếu tên khách hàng, số điện thoại sai định dạng, mã "
           "số thuế trùng (trùng với dữ liệu đã có hoặc trùng giữa hai dòng trong cùng file), mã "
           "danh mục không tồn tại, cặp loại hình – lĩnh vực không khớp nhau.")
    b.para("Khách hàng nhập từ file ghi nhận người tạo là chính anh/chị.")

    # ============================================================ PHẦN 8
    b.h1("PHẦN 8: XUẤT DANH SÁCH RA FILE")
    b.para("Yêu cầu quyền: Xuất dữ liệu khách hàng. Nếu không có quyền này, ba nút xuất file sẽ "
           "không dùng được; trường hợp truy cập trực tiếp bằng đường dẫn, hệ thống báo lỗi không "
           "có quyền.")

    b.h2("1. Ba định dạng xuất")
    b.para("Thanh công cụ có ba nút: Xuất CSV, Xuất Excel và Xuất PDF. Cả ba đều xuất theo ĐÚNG bộ "
           "lọc đang áp dụng.")
    b.para("Lưu ý: file chứa TOÀN BỘ kết quả lọc, không phải chỉ những dòng của trang đang xem. "
           "Nếu bộ lọc cho ra 320 khách hàng và anh/chị đang ở trang 5, file vẫn có đủ 320 dòng.")
    b.para("Khách hàng nằm ngoài phạm vi dữ liệu của anh/chị sẽ không có trong file. Khách hàng đã "
           "Khóa vẫn được xuất, cột Trạng thái ghi rõ là Khóa.")

    b.h2("2. Chọn trường và thứ tự cột")
    b.para("Bấm nút xuất, hệ thống mở cửa sổ chọn trường.")
    b.image("kh_12_chon_truong_xuat.png", "Cửa sổ Chọn trường xuất Excel")
    b.para("Mặc định toàn bộ 20 trường đều được chọn: Mã KH, Tên KH, MST/SĐT, Đối tượng, Nhóm "
           "khách, Địa chỉ, Tỉnh/TP, Tên đơn vị, Tên viết tắt, Địa chỉ xuất hóa đơn, Hãng xe, "
           "Công ty mẹ, Cấp đại lý, Người đại diện, Tên liên hệ, SĐT liên hệ, Chức vụ liên hệ, "
           "Người tạo, Người sửa (gần nhất), Trạng thái.")
    b.para("Bấm dấu x bên cạnh một trường để bỏ trường đó khỏi file. Phải giữ lại ít nhất một "
           "trường mới xuất được.")
    b.para("Điểm cần nhớ: THỨ TỰ CỘT TRONG FILE CHẠY THEO THỨ TỰ ANH/CHỊ CHỌN. Muốn đổi vị trí "
           "một cột, hãy bỏ chọn rồi chọn lại theo trình tự mong muốn — cửa sổ này không kéo thả "
           "để sắp xếp được.")
    b.para("Chọn xong bấm Xuất, file sẽ được tải về máy.")

    # ============================================================ PHẦN 9
    b.h1("PHẦN 9: MÀN QUẢN LÝ KHÁCH HÀNG")
    b.para("Yêu cầu quyền: Xem khách hàng để mở các thẻ nghiệp vụ; thêm quyền Sửa khách hàng nếu "
           "muốn cập nhật trang thiết bị và tài liệu đính kèm. Nếu không có quyền Xem khách hàng, "
           "các thẻ Báo giá, Hợp đồng và Danh sách trang thiết bị sẽ báo lỗi không có quyền.")

    b.h2("1. Mở màn Quản lý khách hàng")
    b.para("Bấm menu ba chấm trên cột Hành động rồi chọn Quản lý.")
    b.image("kh_14_quanly_kh.png", "Màn Quản lý khách hàng với sáu thẻ nghiệp vụ")
    b.para("Màn hình có sáu thẻ, thẻ Thông tin chung được chọn sẵn:")
    b.table([
        ["Thẻ", "Nội dung"],
        ["Thông tin chung", "Thông tin cơ bản, người đại diện, địa chỉ của khách hàng."],
        ["Thông tin liên hệ", "Danh sách người liên hệ."],
        ["Báo giá", "Các báo giá đã lập cho khách hàng này."],
        ["Hợp đồng", "Các hợp đồng đã ký với khách hàng này."],
        ["Danh sách trang thiết bị",
         "Thiết bị đã bán qua hệ thống và thiết bị khai thêm từ ngoài."],
        ["Thông tin khác", "Ảnh, tài liệu, video đính kèm."],
    ])

    b.h2("2. Thẻ Báo giá và Hợp đồng")
    b.para("Hai thẻ này chỉ hiển thị chứng từ của đúng khách hàng đang xem. Anh/chị xuất file hoặc "
           "in danh sách trực tiếp từ đây; bản in có sẵn tiêu đề đầu trang của công ty.")

    b.h2("3. Thẻ Danh sách trang thiết bị")
    b.image("kh_15_tab_thietbi.png", "Thẻ Danh sách trang thiết bị")
    b.para("Thẻ này gộp hai nhóm thiết bị và phân biệt rõ: thiết bị khách hàng đã mua qua hệ thống, "
           "và thiết bị khách hàng đang dùng nhưng mua từ nơi khác (khai thêm bằng tay).")
    b.para("Với nhóm khai thêm, người có quyền Sửa khách hàng thực hiện được các thao tác sau:")
    b.table([
        ["Thao tác", "Cách làm", "Lưu ý"],
        ["Thêm thiết bị", "Bấm nút thêm thiết bị, nhập tên thiết bị, số lượng và thông tin kèm "
                          "theo rồi bấm Lưu.", ""],
        ["Sửa thiết bị", "Bấm nút sửa ở dòng thiết bị, chỉnh thông tin rồi bấm Lưu.", ""],
        ["Xóa thiết bị", "Bấm nút xóa ở dòng thiết bị rồi xác nhận.", ""],
        ["Tăng số lượng", "Bấm chức năng tăng số lượng, nhập số cần thêm.",
         "Số nhập vào được CỘNG DỒN vào số lượng hiện có, không thay thế. Thiết bị đang có 5, "
         "nhập thêm 3 thì kết quả là 8."],
        ["Thêm số máy", "Bấm thêm số máy, nhập số máy rồi bấm Lưu.",
         "Số máy phải chưa tồn tại trong hệ thống. Nếu trùng, hệ thống cảnh báo và cho biết số "
         "máy đó đang thuộc thiết bị nào."],
    ])
    b.para("Nếu không có quyền Sửa khách hàng, anh/chị vẫn xem được danh sách thiết bị nhưng các "
           "nút thao tác sẽ bị làm mờ.")

    b.h2("4. Thẻ Thông tin khác")
    b.para("Nơi lưu ảnh, tài liệu và video liên quan tới khách hàng. Người có quyền Sửa khách hàng "
           "tải file lên hoặc xóa file đã tải. Bấm vào ảnh để xem ảnh phóng to.")

    # ============================================================ PHẦN 10
    b.h1("PHẦN 10: HƯỚNG DẪN THEO TỪNG QUYỀN")
    b.para("Phần này tóm tắt lại: với quyền anh/chị đang có, màn hình sẽ trông như thế nào và làm "
           "được những gì. Hãy đọc mục tương ứng với quyền của mình.")

    b.h2("1. Người dùng không có quyền khách hàng nào")
    b.para("Anh/chị VẪN mở được màn Danh mục khách hàng. Danh sách chỉ hiện những khách hàng do "
           "chính anh/chị tạo ra, cộng những khách hàng anh/chị đang đăng ký còn hạn hoặc đã từng "
           "làm việc.")
    b.para("Thanh công cụ không có nút Tạo mới, Import Excel và ba nút xuất file. Trên cột Hành "
           "động, biểu tượng bút chì và ổ khóa bị làm mờ. Anh/chị tra cứu và xem chi tiết bình "
           "thường, chỉ không thay đổi được dữ liệu.")

    b.h2("2. Người dùng có quyền Xem khách hàng")
    b.para("Ngoài việc tra cứu danh sách, anh/chị mở được màn Quản lý khách hàng qua menu ba chấm "
           "và xem đầy đủ các thẻ Báo giá, Hợp đồng, Danh sách trang thiết bị của từng khách hàng. "
           "Các nút thao tác trên các thẻ này vẫn bị làm mờ nếu chưa có quyền Sửa khách hàng.")

    b.h2("3. Người dùng có quyền Thêm khách hàng")
    b.para("Thanh công cụ hiện thêm hai nút Tạo mới và Import Excel. Anh/chị thêm được khách hàng "
           "lẻ theo Phần 3, hoặc nhập hàng loạt theo Phần 7.")
    b.para("Lưu ý: có quyền Thêm không đồng nghĩa với quyền Sửa. Sau khi tạo xong, nếu chưa được "
           "cấp quyền Sửa khách hàng thì anh/chị không chỉnh lại được — hãy kiểm tra kỹ trước khi "
           "bấm Lưu.")

    b.h2("4. Người dùng có quyền Sửa khách hàng")
    b.para("Biểu tượng bút chì trên cột Hành động sáng lên và bấm được. Anh/chị cập nhật được mọi "
           "thông tin của khách hàng theo Phần 4, kể cả khối Địa chỉ giao hàng.")
    b.para("Quyền này cũng cho phép thêm / sửa / xóa trang thiết bị khai ngoài và tải ảnh, tài "
           "liệu ở màn Quản lý khách hàng.")
    b.para("Mọi thay đổi đều được ghi lại trong Lịch sử kèm tên anh/chị và thời điểm thực hiện.")

    b.h2("5. Người dùng có quyền Xóa khách hàng")
    b.para("Biểu tượng ổ khóa trên cột Hành động sáng lên. Anh/chị khóa và mở khóa khách hàng theo "
           "Phần 5. Nhắc lại: thao tác này KHÔNG xóa dữ liệu, chỉ đổi trạng thái.")

    b.h2("6. Người dùng có quyền Xuất dữ liệu khách hàng")
    b.para("Ba nút Xuất CSV, Xuất Excel và Xuất PDF dùng được. Anh/chị lọc danh sách cần lấy rồi "
           "xuất theo Phần 8. File chỉ chứa những khách hàng anh/chị nhìn thấy được trên màn hình.")

    b.h2("7. Câu hỏi thường gặp")
    b.table([
        ["Tình huống", "Giải thích"],
        ["Tôi tìm tên khách hàng nhưng không ra kết quả",
         "Có thể khách hàng đó nằm ngoài phạm vi dữ liệu của anh/chị, hoặc là khách hàng cá nhân "
         "tự do. Với khách hàng cá nhân, hãy thử gõ đúng trọn vẹn số điện thoại."],
        ["Đồng nghiệp thấy nhiều khách hàng hơn tôi",
         "Do cấp phạm vi dữ liệu khác nhau, xem mục 4.2 phần Tổng quan. Liên hệ quản trị nếu cần "
         "mở rộng."],
        ["Tôi bấm Làm mới nhưng danh sách vẫn như cũ",
         "Kiểm tra ô tìm kiếm nhanh — nút Làm mới trong panel bộ lọc chỉ xóa các tiêu chí nâng cao."],
        ["Tôi ẩn một ô lọc nhưng kết quả không đổi",
         "Ẩn ô lọc chỉ ẩn trên giao diện. Giá trị đã lọc vẫn còn tác dụng cho tới khi bấm Làm mới."],
        ["Không nhập được mã số thuế vì báo đã tồn tại",
         "Mã số thuế là duy nhất. Hãy tìm trong danh sách xem khách hàng đó đã được tạo chưa. "
         "Nếu là chi nhánh, hãy chọn Công ty mẹ, khi đó mã số thuế không còn bắt buộc."],
        ["Khách hàng đã khóa nhưng vẫn thấy trong danh sách",
         "Đúng như thiết kế. Khóa không xóa dữ liệu; khách hàng vẫn ở đây với trạng thái Khóa, "
         "chỉ không chọn được ở màn nghiệp vụ khác."],
        ["File nhập báo lỗi hết các dòng",
         "Kiểm tra dữ liệu có bắt đầu từ dòng 3 không, và các cột tiêu đề có bị đổi tên hay xóa "
         "mất không."],
        ["Thứ tự cột trong file xuất không như mong muốn",
         "Thứ tự cột chạy theo thứ tự anh/chị chọn trong cửa sổ chọn trường. Bỏ chọn hết rồi chọn "
         "lại theo đúng trình tự mong muốn."],
    ])
