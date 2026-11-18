# -*- coding: utf-8 -*-
"""HDSD_Danh sách cần hạch toán chi phí vận chuyển nhanh (STT 181) — bản GỌN form quốc gia (khuôn màn mẫu 167).
Ảnh + icon: hdsd_shots/ (capture.js). Sơ đồ: uml/overview.png (gen_srs.py vẽ).
Chạy:  python gen_hdsd.py [--no-word]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..', '..', 'xuat-tai-lieu-chuyen-doi')))
import _lib_phieu as L  # noqa: E402

TEN = 'Danh sách cần hạch toán chi phí vận chuyển nhanh'
OUT = os.path.join(HERE, 'HDSD_%s.docx' % TEN)
PDF = os.path.join(HERE, 'out', 'HDSD_%s.pdf' % TEN)
VAO = 'Bước 1: Truy cập vào màn hình %s.' % TEN
NGAY = '18/11/2026'

H = {
    'ten': TEN,
    'thuat_ngu': [
        ['Dòng giao nhanh', 'Một khoản chi phí vận chuyển nhanh do khách hàng chịu, khai trên hợp đồng mua (nhân viên chịu phí, khách hàng, số tiền, hàng hoá).'],
        ['Chi phí KH', 'Chi phí theo khách hàng, tính bằng loại tiền của hợp đồng mua.'],
        ['Hạch toán', 'Lập phiếu kế toán ghi Nợ 35241 / Có 811 cho khoản chi phí.'],
        ['Chưa hạch toán / Đang tạo / Đã duyệt / Hủy', 'Trạng thái của dòng, theo phiếu kế toán gắn dòng (chưa có phiếu / phiếu lưu nháp / phiếu đã duyệt / phiếu bị hủy).'],
        ['Điều kiện lên danh sách', 'Hợp đồng mua đã duyệt và đã có phiếu nhập hàng hoàn thành có hàng của đúng khách hàng (hàng đã về kho).'],
    ],
    'phien_ban': [['1.0', NGAY, 'Đội phát triển phần mềm', 'Phát hành lần đầu']],
    'quyen': [
        'Mọi người dùng mở được màn hình. Không có quyền xem thì chỉ thấy các dòng mà mình là nhân viên chịu phí.',
        'Quyền "Xem hạch toán chi phí vận chuyển nhanh" quyết định phạm vi xem theo mức: Tổng công ty, Công ty, Phòng ban, Bộ phận (so với nhân viên chịu phí của dòng).',
        'Quyền "Hạch toán chi phí vận chuyển nhanh" cho phép tick dòng và bấm Tạo phiếu kế toán; lưu phiếu kế toán cần thêm quyền "Kế toán thanh toán".',
    ],
    'phan': [
        ('TRUY CẬP VÀ TÌM KIẾM', [
            ('step', 'Bước 1: Từ phân hệ Tài chính {icon:menu_phanhe}, tại menu Hàng hoá - Dịch vụ - Vận chuyển {icon:menu_nhom}, nhóm Nhập hàng, chọn Danh sách cần hạch toán chi phí vận chuyển nhanh {icon:menu_muc}'),
            ('img', '01_list', 'Màn hình Danh sách cần hạch toán chi phí vận chuyển nhanh'),
            ('step', 'Bước 2: Nhập số hợp đồng mua, mã phiếu nhập, mã hoặc tên khách hàng vào ô tìm kiếm nhanh {icon:o_timnhanh}'),
            ('step', 'Bước 3: Nhấn {icon:btn_timkiem}'),
            ('step', 'Bước 4: Bấm {icon:btn_timkiemnangcao} để mở các ô lọc:'),
            ('sub', 'Chọn {icon:o_congty}, {icon:o_phongban}, {icon:o_bophan}, {icon:o_nhanvien} để lọc theo nhân viên chịu phí (chỉ hiện theo quyền xem)'),
            ('sub', 'Hoặc chọn khoảng {icon:o_ngaynhap} để lọc theo ngày lập phiếu nhập'),
            ('sub', 'Hoặc chọn {icon:o_trangthai}: Chưa hạch toán, Đang tạo, Đã duyệt, Hủy'),
            ('sub', 'Hoặc gõ ít nhất 2 ký tự rồi chọn {icon:o_khachhang}'),
            ('sub', 'Hoặc nhập {icon:o_phieukt}, {icon:o_hopdong} rồi nhấn Enter'),
            ('sub', 'Hoặc chọn {icon:o_nguoiduyet} để lọc theo người duyệt phiếu kế toán'),
            ('img', '02_filter', 'Khu vực Tìm kiếm nâng cao'),
            ('step', 'Bước 5: Chọn {icon:btn_lammoi} để xóa giá trị đã lọc'),
            ('step', 'Bước 6: Bấm {icon:btn_caidatboloc} để chọn ô lọc hiển thị và thứ tự ô lọc, bấm Lưu để áp dụng.'),
        ]),
        ('XEM TRẠNG THÁI HẠCH TOÁN', [
            ('step', VAO),
            ('step', 'Bước 2: Kéo bảng sang phải để xem cột Phiếu kế toán, Hợp đồng mua, Người tạo, Người duyệt, Trạng thái.'),
            ('img', '03_states', 'Dòng Đã duyệt và dòng Đang tạo'),
            ('sub2', 'Chưa hạch toán: chưa có phiếu kế toán, ô Hạch toán còn tick được.'),
            ('sub2', 'Đang tạo: phiếu kế toán đã lưu nháp; Đã duyệt: phiếu đã duyệt, có Người duyệt; Hủy: phiếu bị hủy. Ba trạng thái này ô Hạch toán tích sẵn và khoá.'),
            ('sub2', 'Dòng có nhiều hàng hoá thì cột Hàng hóa tách từng dòng, các cột khác gộp ô.'),
        ]),
        ('HẠCH TOÁN (TẠO PHIẾU KẾ TOÁN)', [
            ('step', VAO),
            ('step', 'Bước 2: Mở Tìm kiếm nâng cao, chọn Trạng thái = Chưa hạch toán.'),
            ('step', 'Bước 3: Tick ô Hạch toán {icon:o_hachtoan} của các dòng cần hạch toán (chỉ trong trang đang xem; đổi trang hoặc lọc lại thì mất tick).'),
            ('img', '11_ticked', 'Đã tick 2 dòng cần hạch toán'),
            ('step', 'Bước 4: Bấm {icon:btn_taophieukt}'),
            ('sub2', 'Chưa tick dòng nào thì hệ thống báo "Vui lòng chọn ít nhất một mục để tạo phiếu kế toán".'),
            ('step', 'Bước 5: Hệ thống mở trang Tạo phiếu kế toán đã điền sẵn:'),
            ('sub2', 'Tự điền: Chi phí vận chuyển nhanh = số dòng đã chọn; Loại tiền theo hợp đồng mua; Tỷ giá theo danh mục tiền tệ; mỗi dòng giao nhanh 2 dòng định khoản Nợ 35241 / Có 811 cùng số tiền, mã khách hàng.'),
            ('sub2', 'Bắt buộc: Ngày hạch toán (mặc định hôm nay). Khi Lưu và duyệt: thêm Diễn giải, Diễn giải từng dòng định khoản.'),
            ('sub2', 'Tùy chọn: Đơn hàng/Hợp đồng ở dòng định khoản (chỉ ra hợp đồng bán của khách do nhân viên chịu phí lập), file đính kèm.'),
            ('img', '12_bill_form', 'Trang Tạo phiếu kế toán nạp sẵn các dòng đã chọn'),
            ('step', 'Bước 6: Bấm {icon:btn_luunhap} để lưu phiếu Đang tạo. Các dòng chuyển trạng thái Đang tạo, ô Hạch toán khoá.'),
            ('sub', 'Hoặc {icon:btn_luuduyet}, bấm Duyệt ở hộp xác nhận để lưu và duyệt luôn (ghi bút toán vào sổ cái; cần quyền Kế toán thanh toán).'),
            ('sub', 'Hoặc {icon:btn_luutieptuc} để lưu nháp rồi lập tiếp phiếu khác.'),
            ('sub', 'Hoặc {icon:btn_quaylai} để không lưu; các dòng vẫn Chưa hạch toán.'),
            ('sub2', 'Dòng vừa được người khác hạch toán thì hệ thống báo "Trạng thái đã bị thay đổi. Vui lòng load lại trang" và không lưu — tải lại danh sách rồi chọn lại.'),
            ('sub2', 'Xóa phiếu kế toán Đang tạo (màn Phiếu kế toán) thì các dòng trở về Chưa hạch toán.'),
        ]),
        ('XEM CHỨNG TỪ LIÊN KẾT', [
            ('step', VAO),
            ('step', 'Bước 2: Bấm mã ở cột Phiếu nhập để mở chi tiết phiếu nhập hàng ở tab mới.'),
            ('img', '15_pi_detail', 'Chi tiết Phiếu nhập hàng'),
            ('step', 'Bước 3: Bấm mã ở cột Phiếu kế toán để mở phiếu kế toán ở tab mới; bấm số ở cột Hợp đồng mua để xem hợp đồng mua.'),
        ]),
        ('XUẤT DANH SÁCH RA EXCEL', [
            ('step', 'Bước 1: Lọc danh sách theo đúng dữ liệu cần lấy (xem PHẦN 1).'),
            ('step', 'Bước 2: Bấm {icon:btn_xuatexcel}. Hệ thống mở cửa sổ "Chọn trường xuất Excel".'),
            ('img', '20_export', 'Cửa sổ Chọn trường xuất Excel'),
            ('step', 'Bước 3: Tích chọn, kéo biểu tượng ☰ để đổi vị trí các trường cần xuất.'),
            ('sub', 'Hoặc bấm {icon:btn_chontatca_x} / {icon:btn_bochonhet_x} để chọn / bỏ chọn nhanh.'),
            ('step', 'Bước 4: Bấm {icon:btn_xuatfile}'),
            ('step', 'Bước 5: Mở file Excel đã xuất (danh_sach_can_hach_toan_chi_phi_van_chuyen_nhanh.xlsx). Danh sách từ 2,000 dòng hàng hoá trở lên thì cần lọc hẹp lại.'),
        ]),
        ('TÙY CHỈNH CỘT HIỂN THỊ', [
            ('step', 'Bước 1: Ở màn danh sách, bấm biểu tượng {icon:btn_cauhinhcot}'),
            ('img', '25_colcfg', 'Cửa sổ Tùy chỉnh cột'),
            ('step', 'Bước 2: Tích để hiện cột, bỏ tích để ẩn cột (STT, Hàng hóa, Hạch toán luôn hiện).'),
            ('step', 'Bước 3: Bấm {icon:btn_chontatca} để hiện tất cả các cột.'),
            ('sub', 'Hoặc bấm {icon:btn_bochonhet} để ẩn tất cả các cột (trừ các cột bắt buộc).'),
            ('step', 'Bước 4: Kéo biểu tượng ba gạch ở cuối mỗi dòng để đổi thứ tự cột.'),
            ('step', 'Bước 5: Bấm Lưu để áp dụng, hoặc Đóng nếu muốn bỏ thay đổi.'),
        ]),
    ],
}

if __name__ == '__main__':
    scr = L.Screen(HERE)
    L.shorten_field_icons(scr)
    print('docx:', L.build_hdsd(scr, H, OUT))
    if '--no-word' not in sys.argv:
        L.finalize_and_check(OUT, PDF, extra_banned=('ERP', 'API'))
