# -*- coding: utf-8 -*-
"""Sinh 6 file HDSD cho nhom danh muc dia ly.

Chay:  python .plans/gop-db/geo-catalogs-docs/gen_hdsd.py
"""
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", ".claude", "skills",
                                "hdsd-documenter", "assets"))
sys.path.insert(0, HERE)
from hdsd_engine import HdsdBuilder  # noqa: E402
from srs_geo_config import SCREENS  # noqa: E402

SHOTS = os.path.join(HERE, "geo_shots")


def build(cfg):
    ten, dt, co_khoa = cfg['ten'], cfg['doi_tuong'], cfg['co_khoa']
    S = cfg['shots']
    ten_file = ten.replace('/', '-')

    b = HdsdBuilder(
        output=os.path.join(HERE, 'HDSD_%s.docx' % ten_file),
        shots_dir=SHOTS,
        cover_title='(Màn hình: %s)' % ten,
        doc_title='HDSD - %s' % ten)

    # ============================================================ TỔNG QUAN
    b.h1("TỔNG QUAN")

    b.h2("1. Thuật ngữ sử dụng trong tài liệu")
    b.table([["Thuật ngữ", "Giải thích"]] + [[t[0], t[1]] for t in cfg['thuat_ngu']
                                             if t[0] != 'SRS'])

    b.h2("2. Cập nhật tài liệu")
    b.table([
        ["Phiên bản", "Ngày", "Người cập nhật", "Nội dung"],
        ["1.0", "17/08/2026", "Tri Lee", "Lập mới cho màn %s." % ten],
    ])

    b.h2("3. Giới thiệu chung")
    b.para("%s là nơi khai báo và quản lý danh sách %s dùng chung cho toàn hệ thống. "
           "Dữ liệu của màn này là nguồn cho các ô địa chỉ ở mọi màn nghiệp vụ khác, "
           "nên mỗi thay đổi ở đây đều ảnh hưởng tới nhiều nơi." % (ten, dt))
    b.para("Đường dẫn truy cập:")
    b.bullet("Menu: Danh mục chung → Địa lý → %s" % ten.replace('Danh mục ', ''))
    b.bullet("Hoặc gõ thẳng đường dẫn %s vào thanh địa chỉ trình duyệt" % cfg['route'])

    b.h2("4. Quyền sử dụng")
    b.para("Màn hình này hiện KHÔNG yêu cầu quyền riêng. Mọi người dùng đã đăng nhập đều mở "
           "được màn hình và thực hiện được đầy đủ các thao tác: Thêm mới, Chỉnh sửa, Xóa%s "
           "và Xem lịch sử." % (", Khóa / Mở khóa" if co_khoa else ""))
    b.para("Vì vậy anh/chị sẽ KHÔNG thấy nút nào bị ẩn hay làm mờ vì lý do phân quyền. "
           "Đây là hiện trạng hiện tại của phần mềm; bộ phận quản trị đang xem xét bổ sung "
           "quyền cho nhóm danh mục địa lý.")
    b.para("Lưu ý: vì ai cũng sửa được, anh/chị hãy cân nhắc kỹ trước khi đổi hoặc xóa một "
           "bản ghi — dữ liệu này đang được nhiều màn khác sử dụng.")

    # ============================================================ PHẦN 1
    b.h1("PHẦN 1: TRUY CẬP VÀ BỐ CỤC MÀN HÌNH")

    b.h2("1. Truy cập màn hình")
    b.para("Đăng nhập hệ thống, vào menu Danh mục chung → Địa lý → %s. Hệ thống hiển thị danh "
           "sách %s hiện có." % (ten.replace('Danh mục ', ''), dt))
    b.image(S['danhsach'], "Màn hình %s khi mới truy cập" % ten)

    b.h2("2. Bố cục màn hình")
    b.para("Màn hình chia làm ba khu vực từ trên xuống:")
    b.bullet("Khu vực tìm kiếm và lọc — ô tìm kiếm nhanh, các ô lọc, nút Tìm kiếm và Làm mới.")
    b.bullet("Thanh công cụ — nút Tạo mới.")
    b.bullet("Bảng danh sách — các cột thông tin, cột Hành động ở cuối, và phân trang bên dưới.")

    b.h2("3. Các cột của bảng danh sách")
    b.table([["Cột", "Nội dung"]] + [[c[0], c[1]] for c in cfg['cot']])

    b.h2("4. Cột Hành động")
    if co_khoa:
        b.para("Trên mỗi dòng, cột Hành động có ba phần:")
        b.bullet("Biểu tượng bút chì — mở cửa sổ chỉnh sửa.")
        b.bullet("Biểu tượng thùng rác — xóa bản ghi.")
        b.bullet("Nút ba chấm “Hành động khác” — chứa hai mục Khóa (hoặc Mở khóa) và Lịch sử.")
        if 'menu' in S:
            b.image(S['menu'], "Nút ba chấm chứa hai thao tác Khóa và Lịch sử")
        b.para("Lưu ý quan trọng: với bản ghi ĐÃ KHÓA, hai nút Sửa và Xóa sẽ BIẾN MẤT, chỉ còn "
               "Mở khóa và Lịch sử. Muốn sửa lại, anh/chị phải Mở khóa trước.")
    else:
        b.para("Trên mỗi dòng, cột Hành động có ba nút: biểu tượng bút chì để sửa, biểu tượng "
               "thùng rác để xóa, và biểu tượng đồng hồ để xem Lịch sử thay đổi.")
        b.para("Màn hình này không có thao tác Khóa / Mở khóa.")

    b.h2("5. Phân trang và sắp xếp")
    b.para("Cuối bảng có ô hiển thị tổng số bản ghi. Con số này là tổng số %s khớp bộ lọc đang "
           "áp dụng, không phải tổng toàn danh mục." % dt)
    b.para("Bấm vào tiêu đề cột có mũi tên để sắp xếp. Bấm lần thứ hai để đảo chiều. Thứ tự sắp "
           "xếp được giữ nguyên khi chuyển trang.")
    b.para("Anh/chị đổi được số dòng mỗi trang. Sau khi đổi, hệ thống tự quay về trang 1.")

    # ============================================================ PHẦN 2
    b.h1("PHẦN 2: TÌM KIẾM VÀ LỌC DANH SÁCH")

    b.h2("1. Các ô tìm kiếm và lọc")
    b.table([["Ô", "Cách dùng"]] + [[f[0], f[4]] for f in cfg['loc']])

    b.h2("2. Cách áp dụng")
    b.para("Nhập hoặc chọn xong các tiêu chí, bấm Tìm kiếm. Các tiêu chí kết hợp với nhau theo "
           "kiểu VÀ — chỉ bản ghi thỏa đồng thời tất cả các tiêu chí mới hiện ra.")
    b.para("Bấm Làm mới để xóa toàn bộ tiêu chí; danh sách nạp lại đầy đủ ngay lập tức.")
    if cfg['key'] in ('districts', 'wards'):
        b.para("Lưu ý: ô Quốc gia và ô Tỉnh/TP phụ thuộc nhau. Đổi Quốc gia thì ô Tỉnh/TP bị xóa "
               "trắng và nạp lại danh sách tỉnh thành của quốc gia mới.")
    if cfg['key'] == 'hamlets':
        b.para("Lưu ý: ô Tỉnh/TP và ô Phường/xã phụ thuộc nhau. Đổi Tỉnh/TP thì ô Phường/xã bị "
               "xóa trắng và nạp lại theo tỉnh mới.")
    if co_khoa:
        b.para("Ô lọc Trạng thái để trống nghĩa là hiện CẢ bản ghi Hoạt động lẫn bản ghi đã "
               "Khóa. Đây là mặc định khi vào màn hình.")

    # ============================================================ PHẦN 3
    b.h1("PHẦN 3: THÊM MỚI %s" % dt.upper())

    b.h2("1. Mở cửa sổ thêm mới")
    b.para("Bấm nút Tạo mới trên thanh công cụ. Hệ thống mở cửa sổ nhập liệu với mọi ô để trống.")
    b.image(S['taomoi'], "Cửa sổ Tạo %s" % dt)

    b.h2("2. Các trường cần nhập")
    b.table([["Trường", "Kiểu nhập", "Bắt buộc", "Giá trị ban đầu", "Ghi chú"]] +
            [[t[0], t[1], t[3], t[4], t[5]] for t in cfg['truong']])
    b.para("Giá trị điền sẵn khi thêm mới: mọi ô đều để trống%s."
           % (", riêng ô Quốc gia mặc định là Việt Nam" if cfg['key'] == 'hamlets' else ""))

    if cfg['key'] == 'hamlets':
        b.h2("3. Quy tắc riêng khi chọn Quốc gia")
        b.para("Ô Quốc gia quyết định form có mấy ô:")
        b.bullet("Chọn Việt Nam — ô Quận/Huyện/Thị xã bị ẨN, không phải nhập. Địa chỉ đi thẳng "
                 "từ Tỉnh/TP xuống Phường/xã.")
        b.bullet("Chọn quốc gia khác — ô Quận/Huyện/Thị xã HIỆN RA và bắt buộc phải chọn.")
        b.image(S['khac_vn'], "Cửa sổ Tạo đường/phố khi chọn quốc gia khác Việt Nam")
        b.para("Đây là thiết kế cố ý, không phải lỗi hiển thị.")
        so = 4
    else:
        so = 3

    b.h2("%d. Ba nút lưu và đóng" % so)
    b.table([
        ["Nút", "Tác dụng"],
        ["Lưu", "Ghi bản ghi rồi đóng cửa sổ, quay về danh sách."],
        ["Lưu và tiếp tục", "Ghi bản ghi nhưng GIỮ cửa sổ mở và xóa trắng các ô, để anh/chị "
                            "nhập tiếp bản ghi kế theo. Rất tiện khi cần thêm nhiều bản ghi "
                            "liên tiếp."],
        ["Đóng", "Hủy bỏ, không ghi gì."],
    ])

    b.h2("%d. Các lỗi thường gặp" % (so + 1))
    b.para("Nếu còn thiếu sót, hệ thống báo lỗi đỏ ngay dưới ô tương ứng. Cửa sổ KHÔNG đóng và "
           "dữ liệu đã nhập vẫn còn nguyên — anh/chị chỉ cần sửa chỗ báo đỏ rồi bấm Lưu lại.")
    if 'validate' in S:
        b.image(S['validate'], "Hệ thống báo lỗi đỏ ngay dưới ô còn thiếu")
    loi = [["Thông báo", "Nguyên nhân và cách xử lý"],
           ["Bắt buộc phải nhập",
            "Chưa nhập một trong các ô bắt buộc: %s."
            % ', '.join(t[0] for t in cfg['truong'] if t[3].startswith('Có'))],
           [cfg['loi_trung_ten'],
            "Đã có %s khác cùng tên %s. Hãy kiểm tra lại danh sách trước khi thêm."
            % (dt, cfg['pham_vi_trung'])]]
    if any('chữ số' in t[2] for t in cfg['truong']):
        loi.append(["Phải là số",
                    "Ô chỉ nhận chữ số nhưng anh/chị đã nhập chữ cái hoặc ký tự khác."])
        loi.append(["Chỉ được nhập chữ số, từ … đến … chữ số",
                    "Số chữ số vượt quá giới hạn cho phép của ô đó."])
    b.table(loi)
    if cfg['key'] == 'provinces':
        b.para("Lưu ý: thông báo trùng tên của màn này hiện chữ “Tên khu vực này đã tồn tại”. "
               "Đây là lỗi chữ đã được ghi nhận — nội dung đúng phải là “Tên tỉnh/TP này đã tồn "
               "tại”. Anh/chị hiểu là tên Tỉnh/TP bị trùng.")

    # ============================================================ PHẦN 4
    b.h1("PHẦN 4: CHỈNH SỬA VÀ XÓA")

    b.h2("1. Chỉnh sửa")
    b.para("Bấm biểu tượng bút chì ở dòng cần sửa. Cửa sổ mở ra giống hệt cửa sổ thêm mới, "
           "nhưng mọi ô đã điền sẵn dữ liệu hiện tại.")
    b.para("Các quy tắc bắt buộc và thông báo lỗi giống hệt phần thêm mới. Có một điểm khác: "
           "nếu anh/chị giữ nguyên tên cũ của chính bản ghi đó thì hệ thống KHÔNG báo trùng. "
           "Chỉ khi đổi sang tên đã có của bản ghi khác mới bị chặn.")
    b.para("Sửa xong bấm Lưu. Mọi thay đổi đều được ghi vào Lịch sử kèm tên anh/chị và thời điểm.")
    if co_khoa:
        b.para("Lưu ý: bản ghi đang ở trạng thái Khóa sẽ KHÔNG có nút bút chì. Muốn sửa, "
               "anh/chị phải Mở khóa trước.")

    b.h2("2. Xóa")
    b.para("Bấm biểu tượng thùng rác ở dòng cần xóa. Hệ thống hiện hộp xác nhận nêu rõ tên bản "
           "ghi — hãy đọc kỹ để chắc chắn không bấm nhầm dòng.")
    b.image(S.get('xoa', S['danhsach']), "Hộp xác nhận xóa %s" % dt)
    b.bullet("Bấm Xóa để xác nhận. Bản ghi biến mất khỏi danh sách.")
    b.bullet("Bấm Hủy nếu bấm nhầm. Không có gì thay đổi.")
    b.para("Nếu bản ghi đang được cấp địa chỉ bên dưới hoặc dữ liệu nghiệp vụ khác sử dụng, "
           "hệ thống sẽ từ chối xóa và nêu lý do. Khi đó anh/chị cần xử lý dữ liệu liên quan "
           "trước.")
    if not co_khoa:
        b.para("Lưu ý về cách xóa của màn này: bản ghi bị xóa được chuyển sang trạng thái ngừng "
               "sử dụng chứ không bị xóa hẳn khỏi hệ thống. Bản ghi biến mất khỏi danh sách và "
               "không chọn được ở lần nhập mới, nhưng các chứng từ cũ đang tham chiếu tới nó "
               "vẫn hiển thị đúng tên.")
    else:
        b.para("Lưu ý: bản ghi đang ở trạng thái Khóa sẽ KHÔNG có nút thùng rác.")

    # ============================================================ PHẦN 5
    if co_khoa:
        b.h1("PHẦN 5: KHÓA VÀ MỞ KHÓA")

        b.h2("1. Khóa nghĩa là gì")
        b.para("Khi một %s không còn dùng nữa nhưng anh/chị không muốn xóa hẳn (vì dữ liệu cũ "
               "vẫn đang tham chiếu tới nó), hãy dùng thao tác Khóa. Sau khi khóa:" % dt)
        b.bullet("Bản ghi VẪN nằm trong danh sách, cột Trạng thái hiện chữ Khóa.")
        b.bullet("Vẫn xem được lịch sử thay đổi của bản ghi.")
        b.bullet("Điểm khác biệt: bản ghi không còn xuất hiện ở ô chọn %s của các màn nghiệp vụ "
                 "khác." % dt)
        b.bullet("Hai nút Sửa và Xóa của dòng đó biến mất.")

        b.h2("2. Các bước khóa")
        b.para("Bấm nút ba chấm “Hành động khác” ở dòng cần khóa, chọn Khóa. Hệ thống hiện hộp "
               "xác nhận nêu rõ tên bản ghi.")
        b.image(S['khoa'], "Hộp xác nhận khóa %s" % dt)
        b.bullet("Bấm Khóa để xác nhận. Cột Trạng thái đổi ngay thành Khóa.")
        b.bullet("Bấm Hủy nếu bấm nhầm.")

        b.h2("3. Mở khóa")
        b.para("Với bản ghi đang Khóa, bấm nút ba chấm rồi chọn Mở khóa và xác nhận. Bản ghi trở "
               "về trạng thái Hoạt động, hai nút Sửa và Xóa hiện trở lại, và bản ghi lại chọn "
               "được ở các màn nghiệp vụ khác.")
        b.para("Nếu bản ghi vừa bị người khác thao tác trước đó, hệ thống báo dữ liệu đã thay "
               "đổi. Anh/chị chỉ cần tải lại danh sách rồi thử lại.")
        phan_ls = 6
    else:
        phan_ls = 5

    # ============================================================ LỊCH SỬ
    b.h1("PHẦN %d: XEM LỊCH SỬ THAY ĐỔI" % phan_ls)
    b.para("Mở lịch sử của một bản ghi từ cột Hành động%s."
           % (" (trong nút ba chấm)" if co_khoa else ""))
    b.image(S['lichsu'], "Cửa sổ Lịch sử thay đổi của %s" % dt)
    b.para("Cửa sổ liệt kê mọi lần thay đổi của bản ghi đó, MỚI NHẤT Ở TRÊN CÙNG. Mỗi dòng cho "
           "biết:")
    b.bullet("Thời điểm thay đổi.")
    b.bullet("Loại thay đổi — ví dụ Thay đổi thông tin, Khóa, Mở khóa.")
    b.bullet("Người thực hiện, kèm mã nhân viên và phòng ban.")
    b.bullet("Trường nào đã đổi, giá trị cũ và giá trị mới.")
    b.para("Cửa sổ có bộ lọc riêng để thu hẹp danh sách khi bản ghi có nhiều lần thay đổi.")
    b.para("Bản ghi vừa được tạo, chưa sửa lần nào thì cửa sổ hiện “Chưa có lịch sử thao tác "
           "nào.” — đây là bình thường, không phải lỗi.")
    if cfg['key'] == 'areas':
        b.para("Lưu ý: hiện tại dòng thay đổi Quốc gia đang hiển thị nhãn “nation_name” thay vì "
               "“Quốc gia”. Đây là lỗi chữ đã được ghi nhận, không ảnh hưởng tới dữ liệu.")
    if cfg['key'] in ('districts', 'hamlets'):
        ref = 'Tỉnh/TP' if cfg['key'] == 'districts' else 'Phường/xã'
        b.para("Lưu ý: hiện tại dòng thay đổi %s đang hiển thị số định danh nội bộ thay vì tên. "
               "Đây là lỗi hiển thị đã được ghi nhận, không ảnh hưởng tới dữ liệu." % ref)

    # ============================================================ CÂU HỎI
    b.h1("PHẦN %d: CÂU HỎI THƯỜNG GẶP" % (phan_ls + 1))
    faq = [["Tình huống", "Giải thích"],
           ["Tôi không sửa được một bản ghi vì không thấy nút bút chì",
            ("Bản ghi đó đang ở trạng thái Khóa. Hãy Mở khóa trước rồi sửa."
             if co_khoa else
             "Hãy tải lại trang. Nếu vẫn không thấy, liên hệ quản trị hệ thống.")],
           ["Tôi bấm Làm mới nhưng danh sách vẫn như cũ",
            "Kiểm tra lại ô tìm kiếm nhanh — có thể vẫn còn từ khóa trong đó."],
           ["Hệ thống báo trùng tên nhưng tôi tìm không thấy bản ghi nào cùng tên",
            "Trùng tên xét %s. Hãy kiểm tra đúng phạm vi đó, và nhớ rằng bản ghi đã "
            "khóa hoặc đã ngừng sử dụng vẫn tính là trùng." % cfg['pham_vi_trung']],
           ["Tôi xóa nhầm một bản ghi",
            "Liên hệ quản trị hệ thống. Lịch sử thay đổi ghi lại người thực hiện và thời điểm "
            "nên có thể tra cứu được."],
           ["Tôi cần thêm nhiều bản ghi liên tiếp cho nhanh",
            "Dùng nút “Lưu và tiếp tục” — cửa sổ giữ nguyên và tự xóa trắng các ô sau mỗi lần "
            "lưu."]]
    if cfg['key'] == 'hamlets':
        faq.append(["Tôi không thấy ô Quận/Huyện khi thêm đường/phố",
                    "Ô này chỉ hiện khi Quốc gia KHÁC Việt Nam. Với địa chỉ Việt Nam, hệ thống "
                    "đi thẳng từ Tỉnh/TP xuống Phường/xã."])
    faq.append(["Vì sao ai cũng sửa được danh mục này?",
                "Màn hình hiện chưa gắn quyền riêng. Bộ phận quản trị đang xem xét bổ sung. "
                "Trong lúc đó, anh/chị hãy cân nhắc kỹ trước khi đổi hoặc xóa dữ liệu."])
    b.table(faq)

    b.finish()


if __name__ == '__main__':
    for cfg in SCREENS:
        build(cfg)
