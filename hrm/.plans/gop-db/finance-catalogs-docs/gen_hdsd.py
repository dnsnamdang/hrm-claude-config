# -*- coding: utf-8 -*-
"""Sinh 3 file HDSD cho nhom danh muc Tai chinh.

Chay:  python .plans/gop-db/finance-catalogs-docs/gen_hdsd.py
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
from fin_config import SCREENS  # noqa: E402

SHOTS = os.path.join(HERE, "fin_shots")


def build(cfg):
    ten, dt, quyen = cfg['ten'], cfg['doi_tuong'], cfg['quyen']
    S = cfg['shots']
    ma = 'mã' if cfg['co_ma'] else 'tên'

    b = HdsdBuilder(
        output=os.path.join(HERE, 'HDSD_%s.docx' % ten.replace('/', '-')),
        shots_dir=SHOTS,
        cover_title='(Màn hình: %s)' % ten,
        doc_title='HDSD - %s' % ten)

    # ============================================================ TỔNG QUAN
    b.h1("TỔNG QUAN")

    b.h2("1. Thuật ngữ sử dụng trong tài liệu")
    b.table([["Thuật ngữ", "Giải thích"]] + [[t[0], t[1]] for t in cfg['thuat_ngu']])

    b.h2("2. Cập nhật tài liệu")
    b.table([
        ["Phiên bản", "Ngày", "Người cập nhật", "Nội dung"],
        ["1.0", "17/08/2026", "Tri Lee", "Lập mới cho màn %s." % ten],
    ])

    b.h2("3. Giới thiệu chung")
    b.para("%s là nơi khai báo danh sách %s dùng cho nghiệp vụ kế toán. Dữ liệu của màn này "
           "được chọn khi lập bút toán, nên mỗi thay đổi ở đây đều ảnh hưởng tới sổ sách."
           % (ten, dt))
    b.para("Đường dẫn truy cập:")
    b.bullet("Menu: Tài chính → Danh mục → %s" % ten.replace('Danh mục ', ''))
    b.bullet("Hoặc gõ thẳng đường dẫn %s vào thanh địa chỉ trình duyệt" % cfg['route'])

    b.h2("4. Quyền sử dụng")
    b.table([
        ["Tên quyền", "Cho phép làm gì", "Ghi chú"],
        [quyen,
         "Mở màn hình và thực hiện đầy đủ: Thêm mới, Chỉnh sửa, Xóa, Xem lịch sử.",
         "Màn hình chỉ có MỘT quyền cho cả xem lẫn sửa, không tách quyền xem riêng."],
    ])
    b.para("Nếu không có quyền này, mục menu %s sẽ không hiển thị; trường hợp truy cập trực tiếp "
           "bằng đường dẫn, hệ thống báo lỗi không có quyền." % ten)

    # ============================================================ PHẦN 1
    b.h1("PHẦN 1: TRUY CẬP VÀ BỐ CỤC MÀN HÌNH")

    b.h2("1. Truy cập màn hình")
    b.para("Đăng nhập hệ thống, vào menu Tài chính → Danh mục → %s."
           % ten.replace('Danh mục ', ''))
    b.image(S['danhsach'], "Màn hình %s khi mới truy cập" % ten)

    b.h2("2. Các cột của bảng danh sách")
    b.table([["Cột", "Nội dung"]] + [[c[0], c[1]] for c in cfg['cot']])

    b.h2("3. Cột Hành động")
    if cfg['dieu_kien_xoa']:
        b.para("Trên mỗi dòng, cột Hành động có ba nút: bút chì để sửa, thùng rác để xóa, và "
               "biểu tượng đồng hồ để xem Lịch sử thay đổi.")
        b.para("Lưu ý quan trọng: nút thùng rác CHỈ hiện với %s %s. Nếu %s đã được dùng trong "
               "bút toán kế toán, nút này biến mất — đây là thiết kế nhằm giữ toàn vẹn số liệu "
               "đã ghi sổ, không phải lỗi." % (dt, cfg['dieu_kien_xoa'], dt))
        b.para("Muốn ngừng sử dụng một %s đã phát sinh bút toán, anh/chị mở cửa sổ Sửa rồi "
               "chuyển ô Trạng thái sang Khóa." % dt)
    else:
        b.para("Trên mỗi dòng, cột Hành động có ba nút: bút chì để sửa, thùng rác để xóa, và "
               "biểu tượng đồng hồ để xem Lịch sử thay đổi.")

    b.h2("4. Phân trang và sắp xếp")
    b.para("Cuối bảng có ô hiển thị tổng số bản ghi khớp bộ lọc đang áp dụng. Bấm vào tiêu đề "
           "cột có mũi tên để sắp xếp, bấm lần thứ hai để đảo chiều. Thứ tự sắp xếp giữ nguyên "
           "khi chuyển trang.")

    # ============================================================ PHẦN 2
    b.h1("PHẦN 2: TÌM KIẾM VÀ LỌC DANH SÁCH")

    b.h2("1. Các ô tìm kiếm và lọc")
    b.table([["Ô", "Cách dùng"]] + [[f[0], f[4]] for f in cfg['loc']])
    if len(cfg['loc']) > 1:
        b.image(S['boloc'], "Khu vực Tìm kiếm nâng cao của màn %s" % ten)
        b.para("Bấm nút Tìm kiếm nâng cao để mở panel chứa các ô lọc. Chọn xong bấm Tìm kiếm. "
               "Các tiêu chí kết hợp với nhau theo kiểu VÀ.")
    else:
        b.para("Màn hình này chỉ có ô tìm kiếm nhanh, không có bộ lọc nâng cao.")
    b.para("Bấm Làm mới để xóa toàn bộ tiêu chí; danh sách nạp lại đầy đủ ngay lập tức.")

    # ============================================================ PHẦN 3
    b.h1("PHẦN 3: THÊM MỚI %s" % dt.upper())
    b.para("Yêu cầu quyền: %s." % quyen)

    b.h2("1. Mở cửa sổ thêm mới")
    b.para("Bấm nút Tạo mới trên thanh công cụ.")
    b.image(S['taomoi'], "Cửa sổ Tạo %s" % dt)

    b.h2("2. Các trường cần nhập")
    b.table([["Trường", "Kiểu nhập", "Bắt buộc", "Giá trị ban đầu", "Ghi chú"]] +
            [[t[0], t[1], t[3], t[4], t[5]] for t in cfg['truong']])
    if cfg['co_trangthai']:
        b.para("Giá trị điền sẵn khi thêm mới: các ô nhập đều để trống, riêng ô Trạng thái đặt "
               "sẵn là Hoạt động. Anh/chị đổi sang Khóa nếu muốn khai trước nhưng chưa dùng ngay.")
    else:
        b.para("Màn hình này chỉ có đúng một ô nhập. Giá trị ban đầu là trống.")

    b.h2("3. Hai nút lưu và đóng")
    b.table([
        ["Nút", "Tác dụng"],
        ["Lưu", "Ghi bản ghi rồi đóng cửa sổ, quay về danh sách."],
        ["Đóng", "Hủy bỏ, không ghi gì."],
    ])
    b.para("Lưu ý: màn hình này KHÔNG có nút “Lưu và tiếp tục” như nhóm danh mục địa lý. Mỗi lần "
           "thêm xong cửa sổ sẽ đóng lại.")

    b.h2("4. Các lỗi thường gặp")
    b.para("Nếu còn thiếu sót, hệ thống báo lỗi đỏ ngay dưới ô tương ứng. Cửa sổ KHÔNG đóng và "
           "dữ liệu đã nhập vẫn còn nguyên.")
    if 'validate' in S:
        b.image(S['validate'], "Hệ thống báo lỗi đỏ ngay dưới ô còn thiếu")
    b.table([
        ["Thông báo", "Nguyên nhân và cách xử lý"],
        ["Bắt buộc phải nhập",
         "Chưa nhập một trong các ô bắt buộc: %s."
         % ', '.join(t[0] for t in cfg['truong'] if t[3] == 'Có')],
        [cfg['loi_trung'],
         "Đã có %s khác dùng %s này. Hãy tra lại danh sách trước khi thêm." % (dt, ma)],
    ])
    if cfg['co_ma']:
        b.para("Lưu ý: ràng buộc không được trùng CHỈ áp cho ô %s. Hai bản ghi khác %s hoàn toàn "
               "được phép trùng tên." % (cfg['truong'][0][0], ma))

    # ============================================================ PHẦN 4
    b.h1("PHẦN 4: CHỈNH SỬA VÀ XÓA")
    b.para("Yêu cầu quyền: %s." % quyen)

    b.h2("1. Chỉnh sửa")
    b.para("Bấm biểu tượng bút chì ở dòng cần sửa. Cửa sổ mở ra giống hệt cửa sổ thêm mới, "
           "nhưng mọi ô đã điền sẵn dữ liệu hiện tại.")
    b.para("Các quy tắc bắt buộc và thông báo lỗi giống hệt phần thêm mới. Có một điểm khác: "
           "nếu anh/chị giữ nguyên %s cũ của chính bản ghi đó thì hệ thống KHÔNG báo trùng. "
           "Chỉ khi đổi sang %s đã có của bản ghi khác mới bị chặn." % (ma, ma))
    b.para("Sửa xong bấm Lưu. Mọi thay đổi đều được ghi vào Lịch sử kèm tên anh/chị và thời điểm.")

    if cfg['co_trangthai']:
        b.h2("2. Ngừng sử dụng bằng cách chuyển Trạng thái sang Khóa")
        b.para("Khi một %s không còn dùng nữa nhưng đã phát sinh bút toán (nên không xóa được), "
               "anh/chị mở cửa sổ Sửa rồi đổi ô Trạng thái sang Khóa." % dt)
        b.bullet("Bản ghi VẪN nằm trong danh mục với trạng thái Khóa.")
        b.bullet("Các bút toán cũ đã dùng bản ghi này giữ nguyên, không bị ảnh hưởng.")
        b.bullet("Bản ghi không còn xuất hiện khi lập bút toán mới.")
        b.para("Màn hình này KHÔNG có nút Khóa riêng trên cột Hành động — mọi thay đổi trạng "
               "thái đều làm trong cửa sổ Sửa.")
        so_xoa = 3
    else:
        so_xoa = 2

    b.h2("%d. Xóa" % so_xoa)
    b.para("Bấm biểu tượng thùng rác ở dòng cần xóa. Hệ thống hiện hộp xác nhận nêu rõ tên bản "
           "ghi — hãy đọc kỹ để chắc chắn không bấm nhầm dòng.")
    b.image(S['xoa'], "Hộp xác nhận xóa %s" % dt)
    b.bullet("Bấm Xóa để xác nhận. Bản ghi biến mất khỏi danh sách.")
    b.bullet("Bấm Hủy nếu bấm nhầm. Không có gì thay đổi.")
    if cfg['dieu_kien_xoa']:
        b.para("Nhắc lại: nút thùng rác chỉ hiện với %s %s. Không thấy nút này nghĩa là bản ghi "
               "đã được dùng trong bút toán kế toán — hãy dùng cách chuyển Trạng thái sang Khóa."
               % (dt, cfg['dieu_kien_xoa']))
    if cfg['xoa_mem']:
        b.para("Lưu ý về cách xóa của màn này: bản ghi bị xóa được chuyển sang trạng thái ngừng "
               "sử dụng chứ không xóa hẳn khỏi hệ thống. Bản ghi biến mất khỏi danh sách và "
               "không chọn được ở lần nhập mới, nhưng các chứng từ cũ đang tham chiếu tới nó "
               "vẫn hiển thị đúng tên.")

    # ============================================================ PHẦN 5
    b.h1("PHẦN 5: XEM LỊCH SỬ THAY ĐỔI")
    b.para("Bấm biểu tượng đồng hồ ở dòng cần xem.")
    b.image(S['lichsu'], "Cửa sổ Lịch sử thay đổi của %s" % dt)
    b.para("Cửa sổ liệt kê mọi lần thay đổi của bản ghi đó, MỚI NHẤT Ở TRÊN CÙNG. Mỗi dòng cho "
           "biết:")
    b.bullet("Thời điểm thay đổi.")
    b.bullet("Loại thay đổi.")
    b.bullet("Người thực hiện, kèm mã nhân viên và phòng ban.")
    b.bullet("Trường nào đã đổi, giá trị cũ và giá trị mới.")
    b.para("Bản ghi vừa được tạo, chưa sửa lần nào thì cửa sổ hiện “Chưa có lịch sử thao tác "
           "nào.” — đây là bình thường, không phải lỗi.")

    # ============================================================ PHẦN 6
    b.h1("PHẦN 6: CÂU HỎI THƯỜNG GẶP")
    faq = [["Tình huống", "Giải thích"],
           ["Tôi không thấy mục menu của màn này",
            "Anh/chị chưa được gán quyền “%s”. Liên hệ quản trị hệ thống." % quyen]]
    if cfg['dieu_kien_xoa']:
        faq.append(["Dòng này không có nút xóa",
                    "%s đó đã được dùng trong bút toán kế toán nên không xóa được. Hãy mở cửa sổ "
                    "Sửa và chuyển Trạng thái sang Khóa." % dt.capitalize()])
        faq.append(["Tôi không tìm thấy nút Khóa trên cột Hành động",
                    "Màn này không có nút Khóa riêng. Đổi trạng thái làm trong cửa sổ Sửa."])
        faq.append(["Hệ thống báo trùng nhưng tôi thấy tên khác nhau",
                    "Ràng buộc trùng áp cho ô %s, không phải tên. Hãy kiểm tra lại ô %s."
                    % (cfg['truong'][0][0], cfg['truong'][0][0])])
    faq.append(["Tôi bấm Làm mới nhưng danh sách vẫn như cũ",
                "Kiểm tra lại ô tìm kiếm nhanh — có thể vẫn còn từ khóa trong đó."])
    faq.append(["Tôi xóa nhầm một bản ghi",
                "Liên hệ quản trị hệ thống. Lịch sử thay đổi ghi lại người thực hiện và thời "
                "điểm nên tra cứu được."])
    if cfg['xoa_mem']:
        faq.append(["Xóa rồi thì chứng từ cũ có mất tên nguồn vốn không?",
                    "Không. Bản ghi chỉ chuyển sang ngừng sử dụng, chứng từ cũ vẫn hiển thị "
                    "đúng tên."])
    b.table(faq)

    b.finish()


if __name__ == '__main__':
    for cfg in SCREENS:
        build(cfg)
