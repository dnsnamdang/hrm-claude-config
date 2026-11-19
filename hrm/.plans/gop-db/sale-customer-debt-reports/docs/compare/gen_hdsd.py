# -*- coding: utf-8 -*-
"""HDSD_Bảng đối chiếu công nợ 1 khách hàng — bản GỌN (khuôn HDSD_MAU_GON.docx, mẫu danh-muc-kho/docs/warehouses)
+ PHẦN "ĐỌC BÁO CÁO" (user chốt 02/11/2026: ảnh bảng có số + bảng Cột | Ý nghĩa + ví dụ cộng số đọc từ chính ảnh).
`_lib_win.build_hdsd` chưa có loại mục "bảng" nên hàm dựng chép sang đây (`build_hdsd_report`), không sửa lib dùng chung.
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

TEN = 'Bảng đối chiếu công nợ 1 khách hàng'
OUT = os.path.join(HERE, 'HDSD_%s.docx' % TEN)
PDF = os.path.join(HERE, 'out', 'HDSD_%s.pdf' % TEN)
VAO = 'Bước 1: Truy cập màn hình %s, chọn Thời gian và Khách hàng để bảng có số liệu (xem PHẦN 1).' % TEN

COT = [
    ['Cột', 'Ý nghĩa / lấy số từ đâu'],
    ['Tổng cộng (dòng đầu bảng)', 'Tổng công nợ của khách hàng theo bộ lọc, gồm cả chứng từ chưa gắn hợp đồng. Không đổi khi chuyển trang hoặc khi dùng ô tìm nhanh. Số 0 vẫn in "0".'],
    ['STT', 'Dòng chữ đậm là hợp đồng (1, 2, 3…); các dòng bên dưới là chứng từ của hợp đồng đó (1.1, 1.2…).'],
    ['Ngày chứng từ', 'Ngày hạch toán (ghi sổ) của chứng từ. Báo cáo xếp kỳ theo ngày này.'],
    ['Số chứng từ', 'Dòng đậm: số hợp đồng (bấm mở hợp đồng ở tab mới). Dòng chứng từ: số phiếu, phiếu xuất kèm số phiếu yêu cầu trong ngoặc; bấm số phiếu xuất để xem hàng hóa (PHẦN 3), bấm chứng từ khác để mở phiếu ở tab mới.'],
    ['Diễn giải', 'Ghi chú của chứng từ (phiếu thu, phiếu chi, ủy nhiệm chi, phiếu điều chỉnh công nợ lấy ghi chú của dòng ứng với hợp đồng này).'],
    ['Số dư đầu kỳ', 'Chỉ có ở dòng Tổng cộng: công nợ khách còn phải trả TRƯỚC Từ ngày.'],
    ['Hàng hóa/Dịch vụ', 'Giá trị bán trong kỳ: phiếu xuất hàng, phiếu xuất bán hàng mượn, hạch toán dịch vụ, biên bản thanh lý, hạch toán dịch vụ bảo hành - sửa chữa, khai báo công nợ đầu kỳ.'],
    ['Điều chỉnh công nợ (tăng)', 'Phiếu điều chỉnh công nợ ghi tăng trong kỳ.'],
    ['Nhập trả lại', 'Phiếu nhập hàng khách trả lại trong kỳ.'],
    ['Đã thanh toán', 'Phiếu thu, phiếu báo có, khai báo công nợ đầu kỳ (phần đã trả) trong kỳ.'],
    ['Điều chỉnh công nợ (giảm)', 'Phiếu điều chỉnh công nợ ghi giảm trong kỳ.'],
    ['Trả lại tiền thừa', 'Phiếu chi, ủy nhiệm chi trả lại tiền thừa cho khách; làm TĂNG số dư cuối kỳ.'],
    ['Số dư cuối kỳ', 'Dòng Tổng cộng: Số dư đầu kỳ + Hàng hóa/Dịch vụ + Điều chỉnh tăng − Nhập trả lại − Đã thanh toán − Điều chỉnh giảm + Trả lại tiền thừa. Dòng hợp đồng và dòng chứng từ KHÔNG tính số dư đầu kỳ và 2 cột Điều chỉnh công nợ; dòng chứng từ là số dư cộng dồn từ chứng từ đầu của hợp đồng.'],
]

H = {
    'ten': TEN,
    'thuat_ngu': [
        ['Công nợ phải thu', 'Số tiền khách hàng còn phải trả công ty.'],
        ['Kỳ', 'Từ ngày đến hết Đến ngày của ô Thời gian, tính theo ngày hạch toán của chứng từ.'],
        ['Số dư đầu kỳ / cuối kỳ', 'Công nợ còn phải thu trước Từ ngày / đến hết Đến ngày.'],
        ['Phát sinh tăng / giảm', 'Các khoản làm tăng / giảm công nợ trong kỳ.'],
        ['Dòng hợp đồng', 'Dòng chữ đậm, mỗi hợp đồng có phát sinh trong kỳ một dòng.'],
        ['Dòng chứng từ', 'Dòng 1.1, 1.2… dưới dòng hợp đồng, mỗi chứng từ một dòng.'],
    ],
    'phien_ban': [['1.0', L.NGAY, 'Đội phát triển phần mềm', 'Phát hành lần đầu']],
    'quyen': [
        'Mọi người dùng đăng nhập đều mở được màn hình và dùng mọi chức năng: xem, tìm kiếm, xem hàng hóa của phiếu xuất, in, xuất Excel.',
        'Số liệu được xem tùy quyền: quyền "Xem báo cáo đối soát công nợ khách hàng theo tổng công ty" xem mọi công ty; "… theo công ty" xem công ty đang làm việc; "… theo phòng ban" / "… theo bộ phận" xem phòng ban / bộ phận mình quản lý. Mọi cấp đều thấy thêm hợp đồng do chính mình tạo; không có quyền nào thì chỉ thấy hợp đồng do mình tạo.',
    ],
    'phan': [
        ('TRUY CẬP VÀ TÌM KIẾM', [
            ('step', 'Bước 1: Từ phân hệ Bán hàng {icon:menu_phanhe}, tại menu Báo cáo {icon:menu_nhom}, chọn nhóm Báo cáo công nợ {icon:menu_nhomcon} rồi chọn Đối chiếu công nợ 1 KH {icon:menu_muc}'),
            ('img', '01_empty', 'Màn hình Bảng đối chiếu công nợ 1 khách hàng khi mới mở'),
            ('step', 'Bước 2: Chọn Từ ngày, Đến ngày ở ô {icon:o_thoigian} (bắt buộc).'),
            ('step', 'Bước 3: Gõ từ 2 ký tự mã hoặc tên khách hàng vào ô {icon:o_khachhang} rồi chọn khách hàng (bắt buộc, chọn được nhiều khách). Đủ 2 ô này bảng tự hiện số liệu.'),
            ('sub', 'Thiếu một trong 2 ô mà bấm Tìm kiếm thì dưới ô hiện chữ đỏ "Vui lòng chọn thời gian" / "Vui lòng chọn khách hàng".'),
            ('step', 'Bước 4: Lọc thêm (tùy chọn):'),
            ('sub', 'Nhập số hợp đồng vào ô {icon:o_sohopdong} rồi bấm {icon:btn_timkiem}: lọc gần đúng theo số hợp đồng, dòng Tổng cộng tính lại theo số hợp đồng.'),
            ('sub', 'Hoặc nhập số hợp đồng / số chứng từ vào ô tìm nhanh {icon:o_timnhanh} rồi bấm {icon:btn_timkiem}: chỉ thu hẹp danh sách hợp đồng, dòng Tổng cộng giữ nguyên.'),
            ('sub', 'Hoặc chọn {icon:o_congty}, {icon:o_phongban}, {icon:o_bophan}, {icon:o_nhanvien} để lọc hợp đồng theo người tạo (ô nào hiện tùy quyền xem).'),
            ('step', 'Bước 5: Chọn {icon:btn_lammoi} để xóa mọi giá trị đã lọc.'),
        ]),
        ('ĐỌC BÁO CÁO', [
            ('p', 'Bảng gồm dòng Tổng cộng ở đầu, sau đó mỗi hợp đồng là một dòng chữ đậm, dưới nó là các chứng từ phát sinh trong kỳ của hợp đồng. Rê chuột vào biểu tượng ⓘ ở tiêu đề cột để xem cách tính.'),
            ('img', '03_report', 'Bảng đối chiếu của CÔNG TY CỔ PHẦN BÁCH LIÊN, kỳ 01/01/2026 – 30/06/2026'),
            ('table', COT, [1.6, 4.9]),
            ('img', '12_read_zoom', 'Phóng to cột STT và 8 cột số của dòng Tổng cộng, hợp đồng 1, 2 (cắt từ ảnh Hình 3)'),
            ('p', '**Ví dụ đọc số từ ảnh phóng to:**'),
            ('sub2', 'Hợp đồng 2 (HĐ_TPE_HN_KD2_26_0267_236): cột Hàng hóa/Dịch vụ 663,120 = 259,200 (dòng 2.1) + 403,920 (dòng 2.2).'),
            ('sub2', 'Số dư cuối kỳ cộng dồn của hợp đồng 2: dòng 2.1 là 259,200; dòng 2.2 là 259,200 + 403,920 = 663,120; dòng 2.3 là phiếu điều chỉnh giảm 663,120 nhưng số dư vẫn 663,120 vì dòng chứng từ không tính cột Điều chỉnh công nợ.'),
            ('sub2', 'Dòng Tổng cộng, cột Số dư cuối kỳ: −2,251,800 + 16,173,540 + 0 − 0 − 0 − 9,601,740 + 0 = 4,320,000.'),
            ('p', 'Lưu ý: cột Số dư cuối kỳ của dòng hợp đồng không trừ điều chỉnh công nợ giảm, nên cộng các dòng hợp đồng sẽ KHÁC số dư cuối kỳ của dòng Tổng cộng; khi đối chiếu tổng công nợ với khách hãy dùng dòng Tổng cộng.'),
        ]),
        ('XEM HÀNG HÓA CỦA PHIẾU XUẤT', [
            ('step', VAO),
            ('step', 'Bước 2: Ở cột Số chứng từ, bấm số phiếu xuất hàng (PXH-…) hoặc phiếu xuất bán hàng mượn (PXBHM-…), ví dụ {icon:lnk_phieuxuat}'),
            ('step', 'Bước 3: Hệ thống mở cửa sổ "Danh sách hàng hóa" liệt kê các mặt hàng của phiếu.'),
            ('img', '06_products', 'Cửa sổ Danh sách hàng hóa của phiếu xuất hàng'),
            ('sub', 'Thành tiền bán là giá chưa thuế nên có thể nhỏ hơn số ở cột Hàng hóa/Dịch vụ của phiếu trên báo cáo.'),
            ('step', 'Bước 4: Bấm {icon:btn_xemchitietphieu} để mở phiếu ở tab mới,'),
            ('sub', 'Hoặc bấm {icon:btn_dong} để quay về bảng báo cáo.'),
        ]),
        ('IN BÁO CÁO', [
            ('step', VAO),
            ('step', 'Bước 2: Bấm {icon:btn_in}. Hệ thống mở cửa sổ "Xem trước bảng đối chiếu công nợ khách hàng" gồm mọi trang theo bộ lọc.'),
            ('img', '10_print', 'Cửa sổ xem trước bản in'),
            ('step', 'Bước 3: Bấm nút In trong cửa sổ để in ra máy in.'),
            ('sub', 'Báo cáo quá 2.000 dòng thì không in được, hãy thu hẹp kỳ hoặc dùng Xuất Excel.'),
        ]),
        ('XUẤT EXCEL', [
            ('step', VAO),
            ('step', 'Bước 2: Bấm {icon:btn_xuatexcel}. Hệ thống mở cửa sổ "Chọn trường xuất Excel".'),
            ('img', '09_export', 'Cửa sổ Chọn trường xuất Excel'),
            ('step', 'Bước 3: Tích chọn, kéo biểu tượng ☰ để đổi vị trí các trường cần xuất.'),
            ('sub', 'Hoặc bấm {icon:btn_chontatca} / {icon:btn_bochonhet} để chọn / bỏ chọn nhanh.'),
            ('step', 'Bước 4: Bấm {icon:btn_xuatfile}. File bang_doi_chieu_cong_no_1_khach_hang.xlsx được tải về, gồm mọi trang theo bộ lọc.'),
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
