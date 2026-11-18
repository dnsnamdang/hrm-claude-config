# -*- coding: utf-8 -*-
"""HDSD_Sổ chi tiết công nợ nhân viên — bản GỌN (khuôn HDSD_MAU_GON.docx) + PHẦN "ĐỌC BÁO CÁO"
(user chốt 02/11/2026: ảnh bảng có số + bảng Cột | Ý nghĩa + ví dụ cộng số đọc từ chính ảnh).
Chép khuôn sale-customer-debt-reports/docs/compare/gen_hdsd.py (mẫu đã duyệt). Ảnh + icon: hdsd_shots/ (capture.js,
make_zoom.py). Sơ đồ: uml/overview.png (gen_srs.py vẽ).
Chạy:  python gen_hdsd.py [--no-word]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
GOPDB = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(GOPDB, 'danh-muc-kho', 'docs'))
import _lib_win as L  # noqa: E402
from _lib_win import QgWriter, HDSD_ROLES, HDSD_TPL, h1_trang_moi  # noqa: E402

TEN = 'Sổ chi tiết công nợ nhân viên'
NGAY = '18/11/2026'
OUT = os.path.join(HERE, 'HDSD_%s.docx' % TEN)
PDF = os.path.join(HERE, 'out', 'HDSD_%s.pdf' % TEN)
VAO = 'Bước 1: Truy cập màn hình %s, chọn Tài khoản và Thời gian để bảng có số liệu (xem PHẦN 1).' % TEN

COT = [
    ['Cột / dòng', 'Ý nghĩa / lấy số từ đâu'],
    ['Số dư đầu kỳ (dòng tổng 1)', 'Công nợ còn lại TRƯỚC Từ ngày = Nợ − Có của các bút toán trước kỳ, chỉ tính bút toán có gắn nhân viên. Dư Nợ ghi cột Phát sinh nợ, dư Có ghi cột Phát sinh có.'],
    ['Tổng phát sinh (dòng tổng 2)', 'Tổng Nợ, tổng Có của MỌI bút toán trong kỳ theo bộ lọc (cộng cả các trang). Mẫu Ngoại tệ: mỗi loại tiền một dòng.'],
    ['Số dư cuối kỳ (dòng tổng 3)', 'Số dư đầu kỳ + Tổng Nợ − Tổng Có.'],
    ['STT', 'Thứ tự bút toán, đánh liên tục qua các trang.'],
    ['Đơn hàng/Hợp đồng', 'Số hợp đồng gắn với bút toán (nếu có); chữ xanh thì bấm để mở hợp đồng.'],
    ['Ngày hạch toán', 'Ngày chứng từ được ghi sổ; bảng xếp theo ngày này.'],
    ['Số chứng từ', 'Chứng từ sinh ra bút toán; chữ xanh thì bấm để mở chứng từ ở tab mới.'],
    ['Nhân viên / Phòng ban', 'Nhân viên và phòng ban ghi trên bút toán.'],
    ['Ghi chú', 'Ghi chú của phiếu xuất hàng, phiếu nhập hàng, phiếu thu, phiếu ủy nhiệm chi, phiếu báo có (loại khác để trống).'],
    ['Phát sinh nợ / Phát sinh có', 'Số tiền VNĐ của bút toán, nằm ở cột Nợ hoặc Có theo chiều ghi sổ.'],
    ['Tài khoản đối ứng', 'Số hiệu và tên tài khoản phía bên kia của bút toán.'],
    ['Mẫu Ngoại tệ', 'Thêm cột Loại tiền, Số phát sinh ngoại tệ (Nợ, Có — chỉ bút toán khác VNĐ), Tỷ giá; 2 cột tiền VNĐ đổi tên thành Số phát sinh VNĐ (Nợ, Có).'],
]

H = {
    'ten': TEN,
    'thuat_ngu': [
        ['Bút toán', 'Một dòng ghi Nợ hoặc ghi Có vào sổ tài khoản do một chứng từ sinh ra.'],
        ['Tài khoản', 'Tài khoản kế toán theo dõi công nợ (vd 141 Tạm ứng). Sổ lấy cả các tài khoản con trực tiếp (vd 1411, 1412).'],
        ['Kỳ', 'Từ ngày đến hết Đến ngày của ô Thời gian, tính theo ngày hạch toán.'],
        ['Số dư đầu kỳ / cuối kỳ', 'Công nợ còn lại trước Từ ngày / đến hết Đến ngày.'],
        ['Dư Nợ / dư Có', 'Số dư dương ghi ở cột Nợ, số dư âm ghi ở cột Có.'],
        ['Mẫu', 'Cách bày cột: VNĐ hoặc Ngoại tệ.'],
    ],
    'phien_ban': [['1.0', NGAY, 'Đội phát triển phần mềm', 'Phát hành lần đầu']],
    'quyen': [
        'Cần quyền "Xem sổ chi tiết công nợ nhân viên". Mức Tổng công ty: xem sổ của mọi công ty. Mức Công ty: xem bút toán của nhân viên thuộc công ty đang làm việc và của chính mình.',
        'Không có quyền: vẫn thấy mục menu nhưng mở màn sẽ báo "Bạn không có quyền thực hiện thao tác này" và không xem được số liệu.',
    ],
    'phan': [
        ('TRUY CẬP VÀ TÌM KIẾM', [
            ('step', 'Bước 1: Từ phân hệ Tài chính {icon:menu_phanhe}, tại menu Kế toán công nợ {icon:menu_nhom}, chọn nhóm Nhân viên {icon:menu_nhomcon} rồi chọn Sổ chi tiết công nợ nhân viên {icon:menu_muc}'),
            ('img', '01_empty', 'Màn hình Sổ chi tiết công nợ nhân viên khi mới mở'),
            ('step', 'Bước 2: Chọn tài khoản ở ô {icon:o_taikhoan} (bắt buộc).'),
            ('step', 'Bước 3: Chọn Từ ngày, Đến ngày ở ô {icon:o_thoigian} (bắt buộc). Đủ 2 ô này bảng tự hiện số liệu.'),
            ('sub', 'Thiếu một trong 2 ô mà bấm Tìm kiếm thì dưới ô hiện chữ đỏ "Vui lòng chọn tài khoản" / "Vui lòng chọn thời gian".'),
            ('step', 'Bước 4: Lọc thêm (tùy chọn):'),
            ('sub', 'Chọn {icon:o_congty}, {icon:o_phongban}, {icon:o_bophan}, {icon:o_nhanvien} để xem sổ của một đơn vị / một nhân viên (ô Công ty chỉ hiện với quyền mức Tổng công ty).'),
            ('sub', 'Chọn {icon:o_tkdoiung}, {icon:o_loaichungtu}, {icon:o_loaitien}, {icon:o_khachhang}, {icon:o_chitieu}, {icon:o_mavuviec}: bảng tải lại ngay.'),
            ('sub', 'Nhập {icon:o_hopdong}, {icon:o_sochungtu}, {icon:o_ghichu}, {icon:o_sotien} hoặc ô tìm nhanh {icon:o_timnhanh} rồi bấm {icon:btn_timkiem} (hoặc Enter).'),
            ('sub', 'Chọn {icon:o_mau} là VNĐ hoặc Ngoại tệ để đổi cách bày cột (số liệu không đổi).'),
            ('step', 'Bước 5: Chọn {icon:btn_lammoi} để xóa mọi giá trị đã lọc.'),
        ]),
        ('ĐỌC BÁO CÁO', [
            ('p', 'Đầu bảng là 3 dòng tổng: Số dư đầu kỳ, Tổng phát sinh, Số dư cuối kỳ. Bên dưới, mỗi bút toán trong kỳ là một dòng, xếp theo ngày hạch toán. Chân bảng ghi tổng số bút toán.'),
            ('img', '04b_employee_table', 'Sổ chi tiết tài khoản 141 - Tạm ứng của nhân viên Võ Cát Hào, kỳ 01/01/2026 – 31/10/2026'),
            ('table', COT, [1.8, 4.7]),
            ('img', '12_read_zoom', 'Phóng to cột STT – Số chứng từ và cột Ghi chú – Phát sinh có của ảnh trên'),
            ('p', '**Ví dụ đọc số từ ảnh phóng to:**'),
            ('sub2', 'Số dư đầu kỳ 14,582,880 nằm ở cột Phát sinh có: trước 01/01/2026 nhân viên đang dư Có 14,582,880.'),
            ('sub2', 'Tổng phát sinh có 33,798,960 là tổng của cả 116 bút toán (12 trang), không phải chỉ trang đang xem: 10 dòng trang 1 cộng lại mới được 236,340 + 313,560 + 439,920 + 383,760 + 325,260 + 423,540 + 500,760 + 299,520 + 353,340 + 145,080 = 3,421,080.'),
            ('sub2', 'Số dư cuối kỳ = 14,582,880 (dư Có) + 33,798,960 (phát sinh Có) = 48,381,840, nằm ở cột Phát sinh có.'),
            ('p', 'Lưu ý: Số dư đầu kỳ chỉ cộng các bút toán có gắn nhân viên, còn các dòng và Tổng phát sinh lấy mọi bút toán của tài khoản. Khi xem sổ không chọn nhân viên mà tài khoản có bút toán không gắn nhân viên (cột Nhân viên trống), số dư cuối kỳ kỳ này sẽ khác số dư đầu kỳ của kỳ sau.'),
            ('img', '05b_foreign_table', 'Mẫu Ngoại tệ — tài khoản 131, loại tiền USD'),
            ('sub2', 'Ở mẫu Ngoại tệ, dòng Tổng phát sinh ghi theo từng loại tiền: USD dư Có 37,639,432.17 USD, quy đổi 976,381,619,156 VNĐ.'),
        ]),
        ('IN SỔ CHI TIẾT', [
            ('step', VAO),
            ('step', 'Bước 2: Bấm {icon:btn_in}. Hệ thống mở cửa sổ "Xem trước sổ chi tiết công nợ nhân viên" gồm mọi bút toán theo bộ lọc.'),
            ('img', '08_print', 'Cửa sổ xem trước bản in'),
            ('step', 'Bước 3: Bấm nút In trong cửa sổ để in ra máy in.'),
            ('sub', 'Sổ quá 2.000 bút toán thì không in được, hãy thu hẹp bộ lọc hoặc dùng Xuất Excel.'),
        ]),
        ('XUẤT EXCEL', [
            ('step', VAO),
            ('step', 'Bước 2: Bấm {icon:btn_xuatexcel}. Cạnh nút hiện tiến độ tải dữ liệu.'),
            ('step', 'Bước 3: File so_chi_tiet_cong_no_nhan_vien.xlsx được tải về, gồm 3 dòng tổng và mọi bút toán theo bộ lọc, cột theo Mẫu đang chọn; hệ thống báo "Xuất Excel thành công".'),
            ('img', '07_export', 'Xuất Excel thành công'),
        ]),
    ],
}


def build_hdsd_report(scr, H, out):
    w = QgWriter(HDSD_TPL, HDSD_ROLES, body_from=19, cover_replace={'Danh mục khu vực': H['ten']})
    h1_trang_moi(w, 'TỔNG QUAN')
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
        h1_trang_moi(w, 'PHẦN %d: %s' % (i, title))
        for it in items:
            kind = it[0]
            if kind == 'img':
                w.image(scr.shot(it[1]), width=L._fit_width(scr.shot(it[1]), 6.0), caption=it[2])
                L._keep_next(w)
            elif kind == 'table':
                w.table(it[1], widths=it[2])
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
