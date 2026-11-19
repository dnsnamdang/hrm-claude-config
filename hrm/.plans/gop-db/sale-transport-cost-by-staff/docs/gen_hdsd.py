# -*- coding: utf-8 -*-
"""HDSD_BC chi phí vận chuyển theo NV kinh doanh — bản GỌN (khuôn HDSD_MAU_GON.docx như 7 danh mục kho) + PHẦN
"ĐỌC BÁO CÁO" (user chốt 02/11/2026: ảnh bảng có số liệu + bảng Cột | Ý nghĩa + ví dụ cộng số đọc từ chính ảnh).
_lib_win.build_hdsd không có mục bảng -> build_hdsd_report ở đây (chép khuôn, thêm loại mục 'table').
Ảnh + icon: hdsd_shots/ (capture.js). Sơ đồ: uml/overview.png (gen_srs.py vẽ).
Chạy:  python gen_hdsd.py [--no-word]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'danh-muc-kho', 'docs'))
import _lib_win as L  # noqa: E402

TEN = 'BC chi phí vận chuyển theo NV kinh doanh'
TEN_MAN = 'Báo cáo chi phí vận chuyển theo nhân viên kinh doanh'
OUT = os.path.join(HERE, 'HDSD_%s.docx' % TEN)
PDF = os.path.join(HERE, 'out', 'HDSD_%s.pdf' % TEN)
VAO = 'Bước 1: Truy cập màn hình %s và chọn Thời gian (xem PHẦN 1).' % TEN_MAN

COT = [
    ['Cột', 'Ý nghĩa / lấy số từ đâu'],
    ['Tổng cộng', 'Tổng cước của mọi phòng ban khớp bộ lọc, kể cả phòng ở các trang sau. Không có cước thì ghi 0.'],
    ['STT', 'Phòng ban 1, 2, 3…; nhân viên 1.1, 1.2…; chuyến xe 1.1.1…'],
    ['Mã NVKD', 'Mã nhân viên kinh doanh chịu cước, tên ở ô bên cạnh. Phòng ban và nhân viên lấy theo thông tin ghi trên phiếu hạch toán chuyến xe lúc hạch toán.'],
    ['Thời gian', 'Ngày hạch toán của phiếu hạch toán chuyến xe. Ô Thời gian trên bộ lọc lọc theo ngày này.'],
    ['Tải trọng tính cước, Dòng xe tính cước', 'Tải trọng, dòng xe khai trên chuyến xe.'],
    ['Xe chạy thực tế', 'Biển số - Tải trọng - Dòng xe của xe chạy chuyến.'],
    ['Tuyến đường', 'Tuyến của chuyến; chuyến xe khác không chọn tuyến thì ghi Điểm đi - Điểm đến.'],
    ['Cước vận chuyển', 'Dòng chuyến xe: số tiền trên phiếu hạch toán chuyến xe (chuyến chở hàng và chuyến xe khác) ghi cho nhân viên đó. '
                        'Không tính tiền công lái xe, xăng xe, vé cầu đường, công tác phí, chi phí khác.\n'
                        'Dòng nhân viên = cộng các chuyến; dòng phòng ban = cộng các nhân viên.'],
    ['Yêu cầu xuất hàng, Hợp đồng', 'Yêu cầu xuất hàng chở trên chuyến và hợp đồng của yêu cầu đó. Bấm mã để mở ở tab mới.'],
    ['Số chuyến xe', 'Số phiếu hạch toán chuyến xe. Bấm để mở phiếu ở tab mới.'],
]

H = {
    'ten': TEN_MAN,
    'thuat_ngu': [
        ['NVKD', 'Nhân viên kinh doanh — người chịu cước vận chuyển được ghi trên phiếu hạch toán chuyến xe.'],
        ['Phiếu hạch toán chuyến xe', 'Chứng từ kế toán ghi chi phí của một chuyến xe chở hàng hoặc chuyến xe khác; là nguồn số của báo cáo.'],
        ['Cước vận chuyển', 'Số tiền vận chuyển tính cho nhân viên kinh doanh (quy ra VND).'],
        ['YCXH', 'Yêu cầu xuất hàng — hàng được chở trên chuyến xe.'],
        ['Đối tượng chịu phí', 'Nhân viên chịu hoặc Công ty chịu, đánh dấu trên từng yêu cầu xuất hàng của chuyến.'],
    ],
    'phien_ban': [['1.0', L.NGAY, 'Đội phát triển phần mềm', 'Phát hành lần đầu']],
    'quyen': [
        'Mọi người dùng đều mở được báo cáo. Số liệu thấy được tùy quyền:',
        '- Quyền xem theo tổng công ty: cước của mọi công ty, lọc được Công ty, Phòng ban, Nhân viên KD.',
        '- Quyền xem theo công ty: cước của công ty đang làm việc, lọc được Phòng ban, Nhân viên KD.',
        '- Quyền xem theo phòng ban: cước của các phòng mình quản lý và phòng của mình, lọc được Nhân viên KD.',
        '- Không có quyền: chỉ cước của chính mình.',
    ],
    'phan': [
        ('TRUY CẬP VÀ TÌM KIẾM', [
            ('step', 'Bước 1: Từ phân hệ Bán hàng {icon:menu_phanhe}, tại menu Báo cáo {icon:menu_nhom}, chọn nhóm {icon:menu_nhom2}, chọn {icon:menu_muc}'),
            ('sub', 'Hoặc từ phân hệ Vận chuyển {icon:menu2_phanhe}, tại menu {icon:menu2_nhom}, chọn {icon:menu2_muc}'),
            ('img', '01_open', 'Màn hình báo cáo khi mới mở'),
            ('step', 'Bước 2: Chọn Từ ngày → Đến ngày ở ô {icon:o_thoigian} (bắt buộc). Báo cáo tự tải.'),
            ('sub', 'Chưa chọn Thời gian mà bấm Tìm kiếm thì ô báo đỏ "Vui lòng chọn thời gian".'),
            ('img', '02_required', 'Ô Thời gian báo đỏ khi chưa chọn'),
            ('step', 'Bước 3: Nhập mã / tên nhân viên KD, phòng ban hoặc số chuyến xe vào ô {icon:o_timnhanh}'),
            ('step', 'Bước 4: Nhấn {icon:btn_timkiem} hoặc phím Enter'),
            ('img', '02_filter', 'Kết quả tìm theo từ khóa "Vinh"'),
            ('step', 'Bước 5: Chọn giá trị {icon:o_congty} để lọc theo công ty'),
            ('sub', 'Hoặc chọn giá trị {icon:o_phongban} để lọc theo phòng ban'),
            ('sub', 'Hoặc chọn giá trị {icon:o_nhanvien} để lọc theo nhân viên kinh doanh'),
            ('sub', 'Hoặc nhập {icon:o_sochuyen}, {icon:o_hopdong}, {icon:o_ycxh} rồi nhấn Enter'),
            ('sub', 'Hoặc chọn {icon:o_doituong} (Nhân viên chịu / Công ty chịu)'),
            ('step', 'Bước 6: Chọn {icon:btn_lammoi} để xóa giá trị đã lọc'),
        ]),
        ('ĐỌC BÁO CÁO', [
            ('p', 'Báo cáo có 3 cấp: phòng ban (chữ đậm, nền xám) → nhân viên kinh doanh → chuyến xe (khi tích Xem chi tiết chuyến xe). Dòng Tổng cộng nằm trên cùng.'),
            ('img', '04_detail', 'Báo cáo kỳ 01/10/2026 – 02/11/2026, đã tích Xem chi tiết chuyến xe'),
            ('table', COT),
            ('p', 'Ví dụ đọc số ở Hình 5:'),
            ('sub2', 'Dòng Tổng cộng 6,156,920 = 379,012 + 436,800 + 1,627,313 + 3,713,795 (4 dòng phòng ban 1, 2, 3, 4).'),
            ('sub2', 'Phòng 1 "Kinh doanh CN Vinh" 379,012 = dòng nhân viên 1.1 Nguyễn Đình Huỳnh 379,012 = chuyến 1.1.1 ngày 08/10/2026 379,012.'),
            ('img', '03_report', 'Báo cáo kỳ 01/01/2026 – 02/11/2026, chưa tích Xem chi tiết chuyến xe'),
            ('sub2', 'Ở Hình 6, phòng 2 "Kinh doanh CN Vinh" 23,879,782 = 1,245,648 + 847,237 + 11,147,097 + 10,639,800 (4 nhân viên 2.1 → 2.4).'),
            ('step', 'Chân bảng ghi "Hiển thị 1–10 / 21" là 21 phòng ban có cước; chọn số phòng ban mỗi trang ở ô "Số dòng/trang" và chuyển trang ở {icon:pagination}'),
            ('img', '03c_footer', 'Chân bảng: số phòng ban và phân trang'),
            ('step', 'Rê chuột vào biểu tượng ⓘ cạnh tên cột để xem cách tính của cột.'),
            ('img', '05_tip', 'Chú thích cách tính cột Cước vận chuyển'),
        ]),
        ('XEM CHI TIẾT CHUYẾN XE', [
            ('step', VAO),
            ('step', 'Bước 2: Tích {icon:chk_chitiet}. Dưới mỗi nhân viên hiện từng chuyến xe, mới nhất ở trên.'),
            ('img', '04b_detail_right', 'Các cột Yêu cầu xuất hàng, Hợp đồng, Số chuyến xe của dòng chuyến xe'),
            ('step', 'Bước 3: Bấm mã yêu cầu xuất hàng {icon:link_ycxh} để mở yêu cầu ở tab mới'),
            ('sub', 'Hoặc bấm mã hợp đồng {icon:link_hopdong} để mở hợp đồng ở tab mới'),
            ('sub', 'Hoặc bấm số chuyến xe {icon:link_sochuyen} để mở phiếu hạch toán chuyến xe ở tab mới'),
            ('step', 'Bước 4: Bỏ tích {icon:chk_chitiet} để ẩn các dòng chuyến xe.'),
        ]),
        ('XUẤT BÁO CÁO RA EXCEL', [
            ('step', VAO),
            ('step', 'Bước 2: Tích {icon:chk_chitiet} nếu muốn file có từng chuyến xe; không tích thì file chỉ có phòng ban và nhân viên.'),
            ('step', 'Bước 3: Bấm nút {icon:btn_xuatexcel}. Hệ thống mở cửa sổ "Chọn trường xuất Excel".'),
            ('img', '06_export', 'Cửa sổ Chọn trường xuất Excel'),
            ('step', 'Bước 4: Tích chọn, kéo biểu tượng ☰ để đổi vị trí các trường cần xuất.'),
            ('sub', 'Hoặc bấm {icon:btn_chontatca} / {icon:btn_bochonhet} để chọn / bỏ chọn nhanh.'),
            ('step', 'Bước 5: Bấm {icon:btn_xuatfile}'),
            ('sub', 'Hoặc {icon:btn_dong} nếu không muốn xuất.'),
            ('step', 'Bước 6: Mở file Excel đã tải về.'),
        ]),
    ],
}


def build_hdsd_report(scr, H, out):
    from qg_writer import QgWriter
    w = QgWriter(L.HDSD_TPL, L.HDSD_ROLES, body_from=19, cover_replace={'Danh mục khu vực': H['ten']})
    L.h1_trang_moi(w, 'TỔNG QUAN')
    w.h2('1. Thuật ngữ sử dụng trong tài liệu')
    w.table([['Thuật ngữ', 'Giải thích']] + H['thuat_ngu'], widths=[2.0, 4.5])
    w.h2('2. Cập nhật tài liệu')
    w.table([['Phiên bản', 'Ngày', 'Người cập nhật', 'Nội dung']] + H['phien_ban'], widths=[0.9, 1.1, 1.5, 3.0])
    w.h2('3. Quyền sử dụng')
    for s in H['quyen']:
        w.p(s)
    w.h2('4. Sơ đồ chức năng tổng quan')
    w.image(os.path.join(scr.uml, 'overview.png'), caption='Sơ đồ chức năng tổng quan màn ' + H['ten'])
    L._keep_next(w)
    for i, (title, items) in enumerate(H['phan'], 1):
        L.h1_trang_moi(w, 'PHẦN %d: %s' % (i, title))
        for it in items:
            kind = it[0]
            if kind == 'img':
                w.image(scr.shot(it[1]), width=L._fit_width(scr.shot(it[1]), 6.0), caption=it[2])
                L._keep_next(w)
            elif kind == 'table':
                w.table(it[1], widths=[1.9, 4.6])
            elif kind == 'p':
                w.p(scr.segs(it[1]))
            else:
                w.raw(kind, scr.segs(it[1]))
    w.rebuild_toc(levels=(1, 2))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    L._table_runs_13(w)
    w.save(out)
    L.force_times_new_roman(out)
    return out


if __name__ == '__main__':
    scr = L.Screen(HERE)
    L.shorten_field_icons(scr)
    print('docx:', build_hdsd_report(scr, H, OUT))
    if '--no-word' not in sys.argv:
        print('Số trang:', L.word_finalize(OUT, PDF))
        L.check_docx(OUT)
