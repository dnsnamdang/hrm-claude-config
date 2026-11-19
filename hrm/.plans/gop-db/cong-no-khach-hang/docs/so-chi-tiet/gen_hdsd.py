# -*- coding: utf-8 -*-
"""HDSD_Sổ chi tiết công nợ phải thu khách hàng — bản GỌN (khuôn HDSD_MAU_GON.docx) + PHẦN "ĐỌC BÁO CÁO"
(khuôn sale-customer-debt-reports/docs/compare/gen_hdsd.py đã duyệt; hàm dựng chép sang đây, không sửa lib dùng chung).
Ảnh + icon: hdsd_shots/ (capture.js). Sơ đồ: uml/overview.png (gen_srs.py vẽ).
Chạy:  python gen_hdsd.py [--no-word]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
GOPDB = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, os.path.join(GOPDB, 'danh-muc-kho', 'docs'))
import _lib_win as L  # noqa: E402
from _lib_win import QgWriter, HDSD_ROLES, HDSD_TPL, h1_trang_moi  # noqa: E402

TEN = 'Sổ chi tiết công nợ phải thu khách hàng'
NGAY = '18/11/2026'
OUT = os.path.join(HERE, 'HDSD_%s.docx' % TEN)
PDF = os.path.join(HERE, 'out', 'HDSD_%s.pdf' % TEN)
VAO = 'Bước 1: Truy cập màn hình %s, chọn Tài khoản, Khách hàng và Thời gian để bảng có số liệu (xem PHẦN 1).' % TEN

COT = [
    ['Cột / dòng', 'Ý nghĩa / lấy số từ đâu'],
    ['Số dư đầu kỳ (dòng tổng)', 'Công nợ của khách hàng trên tài khoản đã chọn TRƯỚC Từ ngày = tổng ghi Nợ − tổng ghi Có. Dư dương ghi ở cột Phát sinh nợ, dư âm ghi ở cột Phát sinh có.'],
    ['Tổng phát sinh (dòng tổng)', 'Tổng ghi Nợ và tổng ghi Có trong kỳ của mọi trang (không bù trừ).'],
    ['Số dư cuối kỳ (dòng tổng)', 'Số dư đầu kỳ + Tổng phát sinh nợ − Tổng phát sinh có.'],
    ['STT', 'Thứ tự bút toán, liên tục qua các trang.'],
    ['Đơn hàng/Hợp đồng', 'Hợp đồng của bút toán; bấm để mở hợp đồng ở tab mới.'],
    ['Ngày hạch toán', 'Ngày chứng từ được ghi sổ. Sổ xếp theo ngày này.'],
    ['Số chứng từ', 'Chứng từ sinh ra bút toán (phiếu xuất hàng, phiếu kế toán, phiếu thu…); bấm để mở chứng từ ở tab mới. Một chứng từ có thể có nhiều dòng.'],
    ['NVKD / Phòng ban', 'Người tạo hợp đồng và phòng ban hiện tại của người đó.'],
    ['Ghi chú', 'Ghi chú của phiếu xuất hàng, phiếu nhập hàng, phiếu thu, phiếu ủy nhiệm chi, phiếu báo có.'],
    ['Phát sinh nợ / Phát sinh có', 'Số tiền VNĐ của bút toán ghi Nợ (làm tăng công nợ) hoặc ghi Có (làm giảm công nợ).'],
    ['Tài khoản đối ứng', 'Số hiệu và tên các tài khoản ghi bên kia của bút toán (vd 5111 doanh thu bán hàng, 1311 bù trừ công nợ).'],
]

H = {
    'ten': TEN,
    'thuat_ngu': [
        ['Công nợ phải thu', 'Số tiền khách hàng còn phải trả công ty.'],
        ['Bút toán', 'Một dòng ghi Nợ hoặc ghi Có vào sổ công nợ do một chứng từ sinh ra.'],
        ['Kỳ', 'Từ ngày đến hết Đến ngày của ô Thời gian, tính theo ngày hạch toán.'],
        ['Số dư đầu kỳ / cuối kỳ', 'Công nợ còn lại trước Từ ngày / đến hết Đến ngày.'],
        ['Tài khoản đối ứng', 'Tài khoản ghi bên kia của bút toán.'],
        ['NVKD', 'Nhân viên kinh doanh — người tạo hợp đồng.'],
    ],
    'phien_ban': [['1.0', NGAY, 'Đội phát triển phần mềm', 'Phát hành lần đầu']],
    'quyen': [
        'Cần quyền "Xem sổ chi tiết công nợ phải thu khách hàng". Mức Tổng công ty xem sổ của mọi công ty; mức Công ty xem sổ của công ty đang làm việc và các hợp đồng do mình tạo.',
        'Không có quyền thì không thấy mục menu và không xem, in, xuất được sổ.',
    ],
    'phan': [
        ('TRUY CẬP VÀ TÌM KIẾM', [
            ('step', 'Bước 1: Từ phân hệ Tài chính {icon:menu_phanhe}, tại menu Kế toán công nợ {icon:menu_nhom}, chọn nhóm Khách hàng {icon:menu_nhomcon} rồi chọn Sổ chi tiết công nợ phải thu khách hàng {icon:menu_muc}'),
            ('sub', 'Hoặc tại màn Bảng cân đối phát sinh công nợ khách hàng, bấm mã khách hàng: sổ chi tiết mở ở tab mới, đã điền sẵn bộ lọc và hiện số liệu.'),
            ('img', '01_empty', 'Màn hình Sổ chi tiết công nợ phải thu khách hàng khi mới mở'),
            ('step', 'Bước 2: Chọn tài khoản ở ô {icon:o_taikhoan} (bắt buộc), ví dụ 131 - Phải thu của khách hàng.'),
            ('step', 'Bước 3: Gõ từ 2 ký tự mã, tên hoặc số điện thoại khách hàng vào ô {icon:o_khachhang} rồi chọn khách hàng (bắt buộc).'),
            ('step', 'Bước 4: Chọn Từ ngày, Đến ngày ở ô {icon:o_thoigian} (bắt buộc). Đủ 3 ô này bảng tự hiện số liệu.'),
            ('sub', 'Thiếu ô nào mà bấm Tìm kiếm thì dưới ô hiện chữ đỏ "Vui lòng chọn tài khoản" / "Vui lòng chọn khách hàng" / "Vui lòng chọn thời gian".'),
            ('step', 'Bước 5: Lọc thêm (tùy chọn):'),
            ('sub', 'Chọn {icon:o_loaitien}: VNĐ (mặc định) hoặc Ngoại tệ để xem bút toán ngoại tệ kèm tỷ giá.'),
            ('sub', 'Nhập số chứng từ / số hợp đồng vào ô tìm nhanh {icon:o_timnhanh}, hoặc ô {icon:o_hopdong}, {icon:o_sochungtu}, {icon:o_sotien} rồi bấm {icon:btn_timkiem}.'),
            ('sub', 'Hoặc chọn {icon:o_tkdoiung}, {icon:o_congty}, {icon:o_phongban}, {icon:o_bophan}, {icon:o_nhanvien} (ô Công ty chỉ hiện với quyền mức Tổng công ty).'),
            ('sub', 'Lưu ý: khi lọc thêm, các dòng Số dư đầu kỳ / Tổng phát sinh / Số dư cuối kỳ cũng chỉ tính phần bút toán khớp điều kiện.'),
            ('step', 'Bước 6: Chọn {icon:btn_lammoi} để xóa mọi giá trị đã lọc.'),
        ]),
        ('ĐỌC BÁO CÁO', [
            ('p', 'Bảng gồm 3 dòng tổng ở đầu (Số dư đầu kỳ, Tổng phát sinh, Số dư cuối kỳ), sau đó mỗi bút toán trong kỳ là một dòng, xếp theo ngày hạch toán.'),
            ('img', '03_report', 'Sổ chi tiết TK 131 của khách hàng 14TQUPCA-2, kỳ 01/01/2026 – 31/10/2026'),
            ('table', COT, [1.8, 4.7]),
            ('img', '12_read_zoom', 'Phóng to cột STT, Số chứng từ, Phát sinh nợ, Phát sinh có của 3 dòng tổng và 3 bút toán đầu (cắt từ ảnh trên)'),
            ('p', '**Ví dụ đọc số từ ảnh phóng to:**'),
            ('sub2', 'Số dư cuối kỳ = 167,583,599 (đầu kỳ) + 686,725,656 (tổng phát sinh nợ) − 632,677,254 (tổng phát sinh có) = 221,632,001.'),
            ('sub2', 'Phiếu xuất hàng PXH-16319 có 2 dòng: dòng 1 ghi nợ 96,184,800 (doanh thu + thuế), dòng 2 ghi có 4,809,240 (giảm giá hàng bán + thuế) — công nợ thực tăng 91,375,560.'),
            ('p', 'Mẫu Ngoại tệ: mỗi loại tiền có riêng 3 dòng tổng; bảng có thêm cột Loại tiền, Số phát sinh ngoại tệ (Nợ, Có), Tỷ giá và Số phát sinh VNĐ.'),
            ('img', '06_foreign', 'Sổ chi tiết mẫu Ngoại tệ (bút toán USD)'),
        ]),
        ('IN BÁO CÁO', [
            ('step', VAO),
            ('step', 'Bước 2: Bấm {icon:btn_in}. Hệ thống mở cửa sổ "Xem trước sổ chi tiết công nợ phải thu khách hàng" gồm mọi bút toán theo bộ lọc.'),
            ('img', '08_print', 'Cửa sổ xem trước bản in'),
            ('step', 'Bước 3: Bấm nút In trong cửa sổ để in ra máy in.'),
            ('sub', 'Sổ quá 2.000 bút toán thì không in được, hãy thu hẹp kỳ hoặc dùng Xuất Excel.'),
        ]),
        ('XUẤT EXCEL', [
            ('step', VAO),
            ('step', 'Bước 2: Bấm {icon:btn_xuatexcel}. Cạnh nút hiện tiến độ; xong hệ thống báo "Xuất Excel thành công" và tải về file so_chi_tiet_cong_no_kh.xlsx gồm 3 dòng tổng và mọi bút toán theo bộ lọc.'),
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
