# -*- coding: utf-8 -*-
"""HDSD_Danh sách đăng ký khách hàng toàn công ty — bản GỌN (khuôn HDSD_MAU_GON.docx) + PHẦN "ĐỌC BÁO CÁO" (khuôn
lookup-stock-companies/docs/gen_hdsd.py đã duyệt). Ảnh + icon: hdsd_shots/ (capture.js). Sơ đồ: uml/overview.png (gen_srs.py vẽ).
Chạy:  python gen_hdsd.py [--no-word]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import _lib_report as R  # noqa: E402
L = R.L

NGAY = '18/11/2026'
TEN = 'Danh sách đăng ký khách hàng toàn công ty'
OUT = os.path.join(HERE, 'HDSD_%s.docx' % TEN)
PDF = os.path.join(HERE, 'out', 'HDSD_%s.pdf' % TEN)

COT = [
    ['Cột', 'Ý nghĩa / lấy số từ đâu'],
    ['STT', 'Số thứ tự, đánh liên tục qua các trang.'],
    ['Khách hàng đăng ký', 'Dòng trên: tên khách hàng. Dòng dưới chữ nghiêng: người liên hệ được đăng ký (khách là tổ chức).'],
    ['Ngày đăng ký', 'Thời điểm nhân viên bấm Đăng ký khách hàng trên báo giá hãng (ngày giờ).'],
    ['Thời hạn đăng ký', 'Ngày hết hạn giữ khách. Từ hôm nay trở đi là Còn hạn, trước hôm nay là Hết hạn.'],
    ['Người đăng ký', 'Mã phòng ban - Họ tên của nhân viên đăng ký (theo hồ sơ hiện tại).'],
    ['Số báo giá', 'Báo giá sinh ra đăng ký. Bấm để mở báo giá ở tab mới.'],
    ['Ghi chú', 'Ghi chú nhân viên nhập khi đăng ký; rê chuột để đọc đủ.'],
    ['Chân bảng', '"Hiển thị a–b / N": N là tổng số đăng ký khớp bộ lọc.'],
]

H = {
    'ten': TEN,
    'thuat_ngu': [
        ['Đăng ký khách hàng', 'Nhân viên kinh doanh đăng ký giữ một khách hàng / người liên hệ trong một thời hạn để người khác không chen vào.'],
        ['Thời hạn đăng ký', 'Ngày hết hạn giữ khách.'],
        ['Còn hạn / Hết hạn', 'Thời hạn đăng ký từ hôm nay trở đi / trước hôm nay.'],
        ['Người liên hệ', 'Người thuộc khách hàng tổ chức mà nhân viên làm việc cùng.'],
        ['Báo giá hãng', 'Báo giá nơi có nút Đăng ký khách hàng (lập trên hệ thống ERP).'],
    ],
    'phien_ban': [['1.0', NGAY, 'Đội phát triển phần mềm', 'Phát hành lần đầu']],
    'quyen': [
        'Cần quyền "Xem danh sách khách hàng đã đăng ký". Có quyền là xem được đăng ký của toàn công ty, lọc và xuất Excel.',
        'Không có quyền thì không thấy mục menu.',
        'Màn hình chỉ để xem: đăng ký / hủy đăng ký làm trên báo giá hãng.',
    ],
    'phan': [
        ('TRUY CẬP VÀ TÌM KIẾM', [
            ('step', 'Bước 1: Từ phân hệ CSKH trước bán {icon:menu_phanhe}, tại menu Báo cáo {icon:menu_nhom}, chọn nhóm Báo cáo thị trường {icon:menu_nhomcon} rồi chọn Danh sách đăng ký khách hàng toàn công ty {icon:menu_muc}'),
            ('img', '01_list', 'Màn hình Danh sách đăng ký khách hàng toàn công ty'),
            ('step', 'Bước 2: Nhập tên / mã khách hàng, người liên hệ, người đăng ký hoặc số báo giá vào ô tìm kiếm nhanh {icon:o_timnhanh}'),
            ('step', 'Bước 3: Nhấn {icon:btn_timkiem}'),
            ('step', 'Bước 4: Bấm {icon:btn_timkiemnangcao} để lọc thêm'),
            ('img', '02_filter', 'Khu vực Tìm kiếm nâng cao'),
            ('sub', 'Hoặc nhập {icon:o_khachhang} rồi bấm Tìm kiếm để lọc theo tên khách hàng'),
            ('sub', 'Hoặc chọn {icon:o_thoihan} Còn hạn / Hết hạn'),
            ('sub', 'Hoặc chọn {icon:o_nguoidk} để xem đăng ký của một nhân viên'),
            ('sub', 'Hoặc nhập {icon:o_sobaogia} rồi bấm Tìm kiếm'),
            ('step', 'Bước 5: Chọn {icon:btn_lammoi} để xóa giá trị đã lọc'),
            ('sub2', 'Bấm tiêu đề cột Ngày đăng ký / Thời hạn đăng ký để sắp tăng / giảm dần.'),
            ('sub2', 'Muốn ẩn bớt ô lọc: bấm {icon:btn_caidatboloc}.'),
        ]),
        ('ĐỌC BÁO CÁO', [
            ('step', 'Bước 1: Mỗi dòng là một lượt đăng ký. Đăng ký mới nhất nằm trên cùng.'),
            ('img', '05_read', 'Bảng danh sách đăng ký (trang 1)'),
            ('step', 'Bước 2: Bấm số báo giá {icon:link_sobaogia} để mở báo giá ở tab mới.'),
            ('table', COT, [2.0, 4.5]),
            ('img', '03_conhan', 'Lọc Thời hạn đăng ký = Còn hạn ngày 18/11/2026: 3 đăng ký'),
            ('pk', '**Ví dụ đọc từ ảnh trên:**'),
            ('sub2', 'Dòng 1: nhân viên HN_KD2 - Lại Quốc Vương đăng ký người liên hệ NGUYỄN THÙY LINH của CÔNG TY TNHH LINH NAM lúc 19/10/2026 16:00, giữ đến hết 18/11/2026, từ báo giá BGBH_TPE_HN_KD2_26_5641.'),
            ('sub2', 'Ngày 18/11/2026 lọc Thời hạn đăng ký = Còn hạn ra 3 dòng (3 đăng ký hết hạn đúng 18/11/2026, vẫn còn hạn tới hết ngày); lọc Hết hạn ra 2,131 dòng; 3 + 2,131 = 2,134 = tổng khi không lọc.'),
        ]),
        ('XUẤT DANH SÁCH RA EXCEL', [
            ('step', 'Bước 1: Lọc danh sách theo đúng dữ liệu cần lấy (xem PHẦN 1).'),
            ('step', 'Bước 2: Bấm nút {icon:btn_xuatexcel}. Hệ thống mở cửa sổ "Chọn trường xuất file".'),
            ('img', '08_export', 'Cửa sổ Chọn trường xuất file'),
            ('step', 'Bước 3: Tích chọn, kéo biểu tượng ☰ để đổi vị trí các trường cần xuất (tích thêm Người liên hệ nếu cần).'),
            ('sub', 'Hoặc bấm {icon:btn_chontatca} / {icon:btn_bochonhet} để chọn / bỏ chọn nhanh.'),
            ('step', 'Bước 4: Bấm {icon:btn_xuatfile}'),
            ('step', 'Bước 5: Mở file danh_sach_dang_ky_khach_hang.xlsx vừa tải về.'),
            ('sub2', 'File gồm mọi dòng khớp bộ lọc (không chỉ trang đang xem).'),
        ]),
        ('TÙY CHỈNH CỘT HIỂN THỊ', [
            ('step', 'Bước 1: Bấm biểu tượng {icon:btn_cauhinhcot}'),
            ('img', '09_colcfg', 'Cửa sổ Tuỳ chỉnh cột'),
            ('step', 'Bước 2: Tích để hiện cột, bỏ tích để ẩn cột, kéo ☰ để đổi thứ tự (cột có biểu tượng khóa luôn hiện).'),
            ('step', 'Bước 3: Bấm {icon:btn_chontatca} để hiện tất cả các cột.'),
            ('sub', 'Hoặc bấm {icon:btn_bochonhet} để ẩn tất cả các cột (trừ các cột khóa).'),
            ('step', 'Bước 4: Bấm {icon:btn_luu} để áp dụng'),
            ('sub', 'Hoặc bấm {icon:btn_dong} nếu muốn bỏ thay đổi.'),
        ]),
    ],
}

if __name__ == '__main__':
    scr = L.Screen(HERE)
    L.shorten_field_icons(scr)
    print('docx:', R.build_hdsd(scr, H, OUT))
    if '--no-word' not in sys.argv:
        print('Số trang:', L.word_finalize(OUT, PDF))
        L.check_docx(OUT)
