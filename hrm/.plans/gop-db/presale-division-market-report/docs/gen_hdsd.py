# -*- coding: utf-8 -*-
"""HDSD_Báo cáo phân chia thị trường — bản GỌN (khuôn HDSD_MAU_GON.docx) + PHẦN "ĐỌC BÁO CÁO" (user chốt 02/11).
Khuôn: lookup-stock-companies/docs/gen_hdsd.py. Ảnh + icon: hdsd_shots/ (capture.js). Sơ đồ: uml/overview.png (gen_srs.py vẽ).
Chạy:  python gen_hdsd.py [--no-word]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
GOPDB = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(GOPDB, 'lookup-stock-companies', 'docs'))
import _lib_report as R  # noqa: E402
L = R.L

TEN = 'Báo cáo phân chia thị trường'
OUT = os.path.join(HERE, 'HDSD_%s.docx' % TEN)
PDF = os.path.join(HERE, 'out', 'HDSD_%s.pdf' % TEN)
VAO = 'Bước 1: Truy cập vào màn hình %s (xem PHẦN 1).' % TEN
BANNED = ('Danh mục quốc gia', 'danh mục quốc gia', 'Danh mục khu vực', 'http://', 'https://')

COT = [
    ['Cột', 'Ý nghĩa / lấy số từ đâu'],
    ['STT', 'Số thứ tự Tỉnh/TP (không phải số dòng), chạy liên tục qua các trang.'],
    ['Tỉnh/TP, Phường/Xã', 'Tỉnh/TP và phường/xã đã chia cho phòng trên phiếu phân chia thị trường theo phòng ban đã duyệt.'],
    ['Phòng phụ trách', 'Phòng được chia phường/xã đó (phiếu theo phòng ban đã duyệt).'],
    ['Nhân viên phụ trách', 'Nhân viên của phòng được giao phường/xã đó trên phiếu phân chia thị trường theo nhân viên đã duyệt, dạng "Mã phòng - Họ tên".'],
    ['Số điện thoại', 'Số điện thoại trong hồ sơ nhân viên hiện tại.'],
    ['Phụ trách tất cả các hãng', '"X" khi nhân viên phụ trách mọi hãng xe tại phường/xã đó.'],
    ['Hãng xe phụ trách', 'Các hãng xe được giao cho nhân viên tại phường/xã, cách nhau dấu phẩy.'],
    ['Dòng tóm tắt cạnh tiêu đề', 'Số Tỉnh/TP · số phường/xã · số dòng phụ trách của TOÀN BỘ kết quả lọc (mọi trang).'],
    ['Chân bảng "Hiển thị a–b / N"', 'Đếm theo PHƯỜNG/XÃ: mỗi trang 10 phường/xã (đổi được), N = tổng số phường/xã.'],
]

H = {
    'ten': TEN,
    'thuat_ngu': [
        ['Phiếu phân chia thị trường theo phòng ban', 'Phiếu giao Tỉnh/TP, phường/xã cho một phòng (hoặc bộ phận).'],
        ['Phiếu phân chia thị trường theo nhân viên', 'Phiếu giao phường/xã, hãng xe cho một nhân viên của phòng.'],
        ['Dòng phụ trách', 'Một dòng của bảng: một nhân viên phụ trách một phường/xã cho một phòng.'],
        ['Vùng', 'Nhóm các Tỉnh/TP theo địa lý.'],
    ],
    'phien_ban': [['1.0', '18/11/2026', 'Đội phát triển phần mềm', 'Phát hành lần đầu']],
    'quyen': [
        'Cần quyền "Xem báo cáo phân chia thị trường" (phân hệ CSKH trước bán). Không có quyền thì không thấy mục menu.',
        'Có quyền là xem được toàn bộ phân chia thị trường của mọi phòng, mọi công ty; xem, lọc, xuất Excel, in được.',
    ],
    'phan': [
        ('TRUY CẬP VÀ TÌM KIẾM', [
            ('step', 'Bước 1: Từ phân hệ CSKH trước bán {icon:menu_phanhe}, tại menu Báo cáo {icon:menu_nhom}, chọn nhóm Báo cáo thị trường {icon:menu_nhomcon}, chọn Báo cáo phân chia thị trường {icon:menu_muc}'),
            ('img', '01_report', 'Màn hình Báo cáo phân chia thị trường'),
            ('step', 'Bước 2: Nhập tên tỉnh/TP, phường/xã, phòng, nhân viên hoặc số điện thoại vào ô tìm kiếm nhanh {icon:o_timnhanh}'),
            ('step', 'Bước 3: Nhấn {icon:btn_timkiem}'),
            ('step', 'Bước 4: Chọn giá trị ở các ô lọc (khu vực ô lọc mở sẵn; bấm {icon:btn_timkiemnangcao} để ẩn / hiện). Bảng lọc ngay khi chọn.'),
            ('sub', 'Hoặc chọn {icon:o_quocgia} để lọc theo quốc gia (chọn Việt Nam = không lọc)'),
            ('sub', 'Hoặc chọn {icon:o_vung} để lọc theo vùng'),
            ('sub', 'Hoặc chọn {icon:o_tinh} để lọc theo tỉnh/thành phố'),
            ('sub', 'Hoặc chọn {icon:o_xa} để lọc theo phường/xã'),
            ('sub', 'Hoặc chọn {icon:o_phutrach} (Có / Không) để lọc nhân viên phụ trách tất cả các hãng'),
            ('sub', 'Hoặc chọn {icon:o_phong} để lọc theo phòng phụ trách'),
            ('sub', 'Hoặc chọn {icon:o_nhanvien} để lọc theo nhân viên phụ trách'),
            ('sub', 'Hoặc chọn {icon:o_hangxe} để lọc theo hãng xe'),
            ('img', '02_filter', 'Lọc Tỉnh Khánh Hòa, Phụ trách tất cả các hãng = Không'),
            ('step', 'Bước 5: Chọn {icon:btn_lammoi} để xóa giá trị đã lọc'),
            ('sub2', 'Muốn ẩn bớt ô lọc: bấm {icon:btn_caidatboloc}.'),
            ('sub2', 'Không lọc gì báo cáo tải khá lâu (khoảng 15–20 giây); nên chọn Tỉnh/TP hoặc Phòng trước.'),
        ]),
        ('ĐỌC BÁO CÁO', [
            ('step', 'Bước 1: Đọc dòng tóm tắt cạnh tiêu đề bảng: số Tỉnh/TP · số phường/xã · số dòng phụ trách.'),
            ('step', 'Bước 2: Đọc bảng từ trái sang phải: Tỉnh/TP › Phường/Xã › Phòng phụ trách › từng nhân viên. Ô Tỉnh/TP, Phường/Xã, Phòng được gộp cho các dòng bên dưới.'),
            ('img', '04_read', 'Tìm nhanh "Âu Lâu": 1 tỉnh/TP · 1 phường/xã · 18 dòng phụ trách'),
            ('step', 'Bước 3: Rê chuột vào {icon:ic_info} ở tiêu đề cột để xem giải thích của cột.'),
            ('table', COT, [2.0, 4.5]),
            ('pk', '**Ví dụ đọc từ ảnh trên:**'),
            ('sub2', 'Phường Âu Lâu (Tỉnh Lào Cai) do 4 phòng phụ trách: PHÒNG KINH DOANH THƯƠNG MẠI 5 nhân viên + PHÒNG THIẾT BỊ Ô TÔ 1 6 nhân viên + PHÒNG THIẾT BỊ Ô TÔ 3 5 nhân viên + PHÒNG THIẾT BỊ XE MÁY 2 nhân viên = 18 = số dòng phụ trách ở dòng tóm tắt.'),
            ('sub2', 'Có 6 dòng "X" ở cột Phụ trách tất cả các hãng (5 người PHÒNG THIẾT BỊ Ô TÔ 1 + Trần Văn Thắng).'),
            ('sub2', 'Bùi Hữu Hanh được giao thêm các hãng Acura, BMW, BYD; các dòng khác chưa giao hãng cụ thể nên cột Hãng xe phụ trách để trống.'),
            ('sub2', 'Chân bảng "Hiển thị 1–1 / 1" đếm theo phường/xã: kết quả chỉ có 1 phường/xã.'),
        ]),
        ('TÙY CHỈNH CỘT HIỂN THỊ', [
            ('step', 'Bước 1: Bấm biểu tượng {icon:btn_cauhinhcot}'),
            ('img', '09_colcfg', 'Cửa sổ Tuỳ chỉnh cột'),
            ('step', 'Bước 2: Tích để hiện cột, bỏ tích để ẩn cột, kéo biểu tượng ☰ để đổi vị trí (STT, Tỉnh/TP luôn hiện).'),
            ('step', 'Bước 3: Bấm {icon:btn_chontatca} để hiện tất cả các cột.'),
            ('sub', 'Hoặc bấm {icon:btn_bochonhet} để ẩn tất cả các cột (trừ các cột khóa).'),
            ('step', 'Bước 4: Bấm {icon:btn_luu} để áp dụng'),
            ('sub', 'Hoặc bấm {icon:btn_dong} nếu muốn bỏ thay đổi.'),
        ]),
        ('XUẤT BÁO CÁO RA EXCEL', [
            ('step', 'Bước 1: Lọc báo cáo theo đúng dữ liệu cần lấy (xem PHẦN 1).'),
            ('step', 'Bước 2: Bấm nút {icon:btn_xuatexcel}. Hệ thống mở cửa sổ "Chọn trường xuất Excel".'),
            ('img', '08_export', 'Cửa sổ Chọn trường xuất Excel'),
            ('step', 'Bước 3: Tích chọn, kéo biểu tượng ☰ để đổi vị trí các trường cần xuất.'),
            ('sub', 'Hoặc bấm {icon:btn_chontatca} / {icon:btn_bochonhet} để chọn / bỏ chọn nhanh.'),
            ('step', 'Bước 4: Bấm {icon:btn_xuatfile}'),
            ('step', 'Bước 5: Mở file bao_cao_phan_chia_thi_truong.xlsx vừa tải về.'),
            ('sub2', 'File gồm mọi dòng khớp bộ lọc (mọi trang), gộp ô như trên màn, có khối ký Người lập.'),
        ]),
        ('IN BÁO CÁO', [
            ('step', 'Bước 1: Lọc báo cáo theo đúng dữ liệu cần in (xem PHẦN 1).'),
            ('step', 'Bước 2: Bấm nút {icon:btn_in}. Hệ thống mở cửa sổ xem trước bản in.'),
            ('img', '10_print', 'Cửa sổ Xem trước báo cáo phân chia thị trường'),
            ('step', 'Bước 3: Bấm {icon:btn_in_popup} trong cửa sổ để in ra máy in.'),
            ('sub2', 'Chỉ in được tối đa 2,000 dòng. Nhiều hơn thì cửa sổ báo "vượt mức in tối đa 2,000 dòng" và không có nút In: thu hẹp bộ lọc hoặc dùng Xuất Excel.'),
        ]),
    ],
}

if __name__ == '__main__':
    scr = L.Screen(HERE)
    L.shorten_field_icons(scr)
    print('docx:', R.build_hdsd(scr, H, OUT))
    if '--no-word' not in sys.argv:
        print('Số trang:', L.word_finalize(OUT, PDF))
        L.check_docx(OUT, banned=BANNED)
