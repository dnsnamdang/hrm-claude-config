# -*- coding: utf-8 -*-
"""HDSD bản GỌN — Phiếu xuất giữ (STT 188, form chuẩn Danh mục quốc gia, 28/10/2026).

Chạy: python gen_hdsd.py  → out/HDSD_Phiếu xuất giữ.docx (+ .pdf, render/ để soát)
Phần dùng chung: ../../phieu-theo-form-quoc-gia/hdsd_phieu_lib.py — khuôn y hệt màn 27.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'phieu-theo-form-quoc-gia'))
from hdsd_phieu_lib import PhieuHdsd, finalize_word, toc_lines, render_check  # noqa: E402

TEN = 'Phiếu xuất giữ'
SHOTS = os.path.join(HERE, 'hdsd_shots')
OUT = os.path.join(HERE, 'out', 'HDSD_%s.docx' % TEN)

THUAT_NGU = [
    ['Hàng giữ', 'Số lượng hàng hóa trong kho được giữ lại cho một khách hàng, do một nhân viên kinh doanh đứng tên '
                 'giữ, tới một hạn nhất định.'],
    ['Lô hàng giữ', 'Một dòng tồn hàng giữ: người giữ – khách hàng – hàng hóa – hạn giữ – công ty.'],
    ['Yêu cầu xuất giữ', 'Phiếu đề nghị giữ hàng do nhân viên kinh doanh lập, mã PYCXG. Là phiếu nguồn của phiếu xuất '
                         'giữ.'],
    ['Phiếu xuất giữ', 'Phiếu do Kế toán lập từ một yêu cầu đã qua đủ các cấp duyệt, mã PXG. Đây là chứng từ DUY NHẤT '
                       'sinh ra lô hàng giữ.'],
    ['Người yêu cầu', 'Người lập yêu cầu xuất giữ — chính người này đứng tên giữ hàng, không phải Kế toán.'],
    ['SL có thể giữ', 'Số hàng còn trong kho có thể giữ được.'],
    ['SL yêu cầu', 'Số lượng người lập yêu cầu đã xin giữ, là mức trần của SL xuất giữ.'],
    ['SL xuất giữ', 'Số lượng Kế toán chốt thực xuất giữ.'],
    ['SL giữ (ĐV cơ bản)', 'Số lượng đã quy đổi về đơn vị cơ bản và cộng vào tồn hàng giữ; hiện ở màn chi tiết phiếu '
                           'đã duyệt.'],
    ['Trạng thái Đang tạo', 'Phiếu nháp, chưa ghi tồn hàng giữ. Người lập được sửa, xóa.'],
    ['Trạng thái Đã duyệt', 'Đã ghi tồn hàng giữ. Không sửa, không xóa được.'],
]

PHIEN_BAN = [
    ['1.0', '18/09/2026', 'Ban hành lần đầu cho màn hình Phiếu xuất giữ trên phân hệ Tài chính.'],
    ['1.1', '28/10/2026', 'Chuyển sang form chuẩn'],
]

QUYEN = [
    ['Xem danh sách, xem chi tiết, in, xuất Excel',
     'Một trong các quyền: Kế toán duyệt hàng giữ (xem mọi phiếu trong công ty), Xem phiếu hàng giữ theo tổng công '
     'ty / theo công ty / theo phòng ban. Phiếu do chính mình lập luôn xem được.'],
    ['Lập phiếu, Duyệt giữ hàng', 'Kế toán duyệt hàng giữ, cùng công ty với yêu cầu nguồn đang Chờ KT duyệt.'],
    ['Sửa, xóa phiếu', 'Người lập phiếu, phiếu đang ở trạng thái Đang tạo.'],
]


def build():
    d = PhieuHdsd(TEN, SHOTS)
    d.tong_quan(THUAT_NGU, PHIEN_BAN, QUYEN, os.path.join(HERE, 'uml', 'overview_srs.png'))

    d.truy_cap(
        menu=[('Tài chính', 'menu_phanhe'), ('Hàng hoá - Dịch vụ - Vận chuyển', 'menu_nhom'),
              ('Giữ hàng', 'menu_giuhang'), ('Phiếu xuất giữ', 'menu_muc')],
        o_nhanh='mã phiếu',
        bo_loc=[('Công ty', 'o_congty'), ('Phòng ban', 'o_phongban'), ('Mã phiếu', 'o_maphieu'),
                ('Yêu cầu xuất giữ', 'o_yeucau'), ('Trạng thái', 'o_trangthai'), ('Người tạo', 'o_nguoitao'),
                ('Người duyệt', 'o_nguoiduyet'), ('Người yêu cầu', 'o_nguoiyeucau'), ('Khách hàng', 'o_khachhang'),
                ('Tên, mã hàng', 'o_tenmahang'), ('Ngày tạo', 'o_ngaytao')])

    # PHẦN 2 — Lập phiếu
    d.phan('LẬP PHIẾU XUẤT GIỮ')
    d.step(['Bước 1: Bấm ', '@btn_laptuyc', '. Hệ thống chuyển sang màn Yêu cầu xuất giữ.'])
    d.step('Bước 2: Mở yêu cầu đang Chờ KT duyệt, bấm nút Lập phiếu xuất giữ (xem HDSD Yêu cầu xuất giữ). Hệ thống '
           'mở màn “Lập phiếu xuất giữ”, dữ liệu nạp sẵn từ yêu cầu.')
    d.img('10_create', 'Màn hình Lập phiếu xuất giữ')
    d.step('Bước 3: Kiểm tra và nhập thông tin:')
    d.sub('Giữ đến ngày (bắt buộc): điền sẵn theo yêu cầu, sửa được; là hạn ghi vào lô hàng giữ khi duyệt.')
    d.sub('Ghi chú (tùy chọn): tối đa 255 ký tự.')
    d.sub('File đính kèm (tùy chọn): bấm Thêm tài liệu rồi chọn tệp PDF, ảnh, Word, Excel (tối đa 13 MB mỗi tệp).')
    d.step(['Bước 4: Ở khối Chi tiết, bỏ tích ', '@o_tick', ' cột Cần xuất các dòng không xuất; nhập SL xuất giữ (bắt '
            'buộc, lớn hơn 0, không vượt SL yêu cầu).'])
    d.step(['Bước 5: Bấm ', '@btn_duyetgiuhang', ' để ghi tồn hàng giữ cho người yêu cầu (xem PHẦN 3),'])
    d.sub(['Hoặc ', '@btn_luunhap', ' để lưu nháp (chưa ghi tồn; yêu cầu nguồn chuyển sang Đang xuất giữ).'])
    d.sub(['Hoặc ', '@btn_khongduyet', ' — cũng chỉ lưu nháp như Lưu nháp, KHÔNG trả yêu cầu về người lập. Muốn trả '
           'về thì bấm Từ chối ở màn Yêu cầu xuất giữ.'])
    d.sub(['Hoặc ', '@btn_quaylai', ' để không lưu thông tin.'])

    # PHẦN 3 — Duyệt giữ hàng
    d.phan('DUYỆT GIỮ HÀNG')
    d.step('Bước 1: Ở màn Lập phiếu (PHẦN 2) hoặc màn Sửa phiếu (PHẦN 4), kiểm tra Người yêu cầu, Khách hàng, Giữ đến '
           'ngày và SL xuất giữ từng dòng.')
    d.step(['Bước 2: Bấm ', '@btn_duyetgiuhang', '. Hệ thống hiện hộp xác nhận “Xác nhận duyệt giữ hàng”.'])
    d.img('11_approve', 'Hộp xác nhận duyệt giữ hàng')
    d.step(['Bước 3: Bấm ', '@btn_confirm_duyetgiuhang', ' để xác nhận. Hệ thống ghi tồn hàng giữ, phiếu và yêu cầu '
            'nguồn chuyển sang Đã duyệt. Thao tác không hoàn tác được.'])
    d.sub(['Hoặc bấm ', '@btn_huy_confirm', ' nếu bấm nhầm'])

    # PHẦN 4 — Chỉnh sửa
    d.phan('CHỈNH SỬA')
    d.step(d.vao)
    d.step(['Bước 2: Bấm nút ', '@btn_sua_row', ' ở cột Hành động của phiếu Đang tạo.'])
    d.sub(['Hoặc bấm vào Mã phiếu để mở màn chi tiết, chọn ', '@btn_sua'])
    d.step('Bước 3: Hệ thống hiển thị màn hình “Sửa phiếu xuất giữ”.')
    d.img('12_edit', 'Màn hình Sửa phiếu xuất giữ')
    d.step('Bước 4: Nhập thông tin cần sửa (quy tắc nhập như PHẦN 2; không đổi được yêu cầu nguồn và hàng hóa).')
    d.step(['Bước 5: Bấm ', '@btn_luunhap', ' để lưu,'])
    d.sub(['Hoặc ', '@btn_duyetgiuhang', ' để duyệt giữ hàng (PHẦN 3).'])
    d.sub(['Hoặc ', '@btn_quaylai', ' nếu muốn hủy.'])

    # PHẦN 5 — Xóa
    d.xoa('Xác nhận xóa', them_cach=['Hoặc bấm vào Mã phiếu để mở màn chi tiết, chọn ', '@btn_xoa'])
    d.sub('Xóa phiếu nháp thì yêu cầu nguồn quay lại Chờ KT duyệt để lập lại.')

    # PHẦN 6 — Lịch sử
    d.lich_su('Mã phiếu', img='16_history', cap='Cửa sổ Lịch sử phiếu xuất giữ')

    # PHẦN 7 — Xem chi tiết
    d.phan('XEM CHI TIẾT PHIẾU')
    d.step(d.vao)
    d.step('Bước 2: Bấm vào Mã phiếu. Hệ thống mở màn “Chi tiết phiếu xuất giữ”; phiếu đã duyệt có thêm cột SL giữ (ĐV '
           'cơ bản).')
    d.img('17_detail', 'Màn hình Chi tiết phiếu xuất giữ')
    d.step(['Bước 3: Bấm ', '@btn_quaylai', ' để về màn danh sách.'])

    # PHẦN 8 — In
    d.phan('IN PHIẾU VÀ IN DANH SÁCH')
    d.h2('1. In phiếu')
    d.step(['Bước 1: Ở cột Hành động, bấm ', '@btn_in_row'])
    d.sub(['Hoặc bấm ', '@btn_bacham_row', ' rồi chọn ', '@item_in'])
    d.sub(['Hoặc tại màn chi tiết phiếu, bấm ', '@btn_in'])
    d.step('Bước 2: Hệ thống mở cửa sổ xem trước bản in.')
    d.img('18_print', 'Cửa sổ Xem trước phiếu xuất giữ')
    d.step(['Bước 3: Bấm ', '@btn_in_preview', ' để in.'])
    d.h2('2. In danh sách')
    d.step('Bước 1: Lọc danh sách theo đúng dữ liệu cần in (xem PHẦN 1).')
    d.step(['Bước 2: Bấm ', '@btn_in_list', '. Hệ thống mở cửa sổ xem trước danh sách.'])
    d.img('19_printlist', 'Cửa sổ Xem trước danh sách phiếu xuất giữ')
    d.step(['Bước 3: Bấm ', '@btn_in_preview', ' để in.'])

    d.xuat_excel()
    d.cai_dat_bo_loc()
    d.tuy_chinh_cot()
    return d.save(OUT)


if __name__ == '__main__':
    out = build()
    pdf = os.path.splitext(out)[0] + '.pdf'
    size = finalize_word(out, pdf)
    print('docx', out, size)
    print('TOC:')
    for line in toc_lines(out):
        print('  ', line)
    n, warn, sheets = render_check(pdf, os.path.join(HERE, 'out', 'render'))
    print('pages', n)
    for w_ in warn:
        print('WARN', w_)
    for s in sheets:
        print(s)
