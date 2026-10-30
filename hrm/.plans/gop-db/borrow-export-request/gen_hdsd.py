# -*- coding: utf-8 -*-
"""HDSD bản GỌN — Yêu cầu xuất hàng mượn (form chuẩn Danh mục quốc gia, 30/10/2026).

Chạy: python gen_hdsd.py  → HDSD_Yeu cau xuat hang muon.docx (PDF + ảnh soát ghi vào thư mục tạm)
Khuôn: ../finance-bill-income-request/form_qg_48/gen_hdsd.py; phần chung ở
../phieu-theo-form-quoc-gia/hdsd_phieu_lib.py. Sơ đồ tổng quan dùng lại ảnh gen_srs.py sinh ra (pycxhm_shots/uml/overview.png).
"""
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'phieu-theo-form-quoc-gia'))
from hdsd_phieu_lib import PhieuHdsd, finalize_word, toc_lines, render_check  # noqa: E402

TEN = 'Yêu cầu xuất hàng mượn'
SHOTS = os.path.join(HERE, 'pycxhm_shots')
OUT = os.path.join(HERE, 'HDSD_Yeu cau xuat hang muon.docx')
CHECK_DIR = os.path.join(tempfile.gettempdir(), 'hdsd_pycxhm')   # PDF + ảnh soát, không để trong repo

THUAT_NGU = [
    ['Phiếu yêu cầu xuất hàng mượn', 'Phiếu PYCXHM-NNNNN: đề nghị Kế toán kho xuất hẳn phần hàng đang mượn, '
                                     'không trả lại nữa.'],
    ['Phiếu xuất mượn', 'Phiếu yêu cầu xuất hàng loại Xuất mượn (PYCXH-…) đã xuất kho, đang ở trạng thái Đã mượn.'],
    ['Đang mượn', 'Số lượng hàng còn được phép xuất trên một phiếu mượn.'],
    ['Phiếu xuất hàng mượn', 'Chứng từ PXHM-NNNNN Kế toán kho lập để duyệt phiếu yêu cầu.'],
    ['Chờ duyệt', 'Phiếu đã gửi, chờ Kế toán kho xử lý.'],
    ['Đã duyệt', 'Kế toán kho đã lập Phiếu xuất hàng mượn từ phiếu.'],
    ['Không duyệt', 'Kế toán kho đã từ chối phiếu; phiếu dừng hẳn, không sửa được.'],
]
PHIEN_BAN = [['1.0', '30/10/2026', 'Tạo mới tài liệu theo form chuẩn']]
QUYEN = [
    ['Xem danh sách, xem chi tiết, in, xuất Excel, xem lịch sử',
     'Phiếu do chính mình lập luôn xem được. Xem rộng hơn cần một trong các quyền: Kế toán kho; Xem phiếu hàng '
     'mượn theo tổng công ty / theo công ty / theo phòng ban.'],
    ['Lập phiếu', 'Không cần quyền riêng; chỉ chọn được phiếu xuất mượn do chính mình lập.'],
    ['Từ chối, Tạo phiếu xuất hàng mượn (duyệt)', 'Quyền Kế toán kho; phiếu đang ở trạng thái Chờ duyệt.'],
]


def build():
    d = PhieuHdsd(TEN, SHOTS)
    d.tong_quan(THUAT_NGU, PHIEN_BAN, QUYEN, os.path.join(SHOTS, 'uml', 'overview.png'))

    # PHẦN 1 — 2 lối vào
    d.phan('TRUY CẬP VÀ TÌM KIẾM')
    d.p('Cách 1: Lối vào chung (người lập phiếu):')
    d.step(['Bước 1: Từ phân hệ Bán hàng ', '@menu_phanhe_banhang', ', tại menu Yêu cầu ', '@menu_yeucau',
            ', nhóm Hàng hóa ', '@menu_hanghoa', ', chọn YC xuất hàng mượn ', '@menu_muc_sale'])
    d.p('Cách 2: Lối vào của Kế toán kho:')
    d.step(['Bước 1: Từ phân hệ Tài chính ', '@menu_phanhe', ', tại menu Hàng hoá - Dịch vụ - Vận chuyển ',
            '@menu_nhom', ', nhóm Mượn hàng ', '@menu_muonhang', ', chọn Yêu cầu xuất hàng mượn ', '@menu_muc'])
    d.img('01_list', 'Màn hình Yêu cầu xuất hàng mượn')
    d.step(['Bước 2: Nhập mã phiếu vào ô tìm kiếm nhanh ', '@o_timnhanh'])
    d.step(['Bước 3: Nhấn ', '@btn_timkiem'])
    d.step(['Bước 4: Bấm ', '@btn_timkiemnangcao', ', chọn giá trị trong ', '@o_trangthai', ' để lọc theo Trạng thái'])
    for lb, ic in [('Công ty', 'o_congty'), ('Phòng ban', 'o_phongban'), ('Mã phiếu', 'o_maphieu'),
                   ('Người tạo', 'o_nguoitao'), ('Người duyệt', 'o_nguoiduyet'), ('Mã hàng hóa', 'o_mahang'),
                   ('Tên hàng hóa', 'o_tenhang'), ('Ngày tạo', 'o_ngaytao')]:
        d.sub(['Hoặc chọn giá trị ', '@' + ic, ' để lọc theo %s' % lb])
    d.step(['Bước 5: Chọn ', '@btn_lammoi', ' để xóa giá trị đã lọc'])

    # PHẦN 2 — Lập phiếu
    d.phan('LẬP PHIẾU YÊU CẦU XUẤT HÀNG MƯỢN')
    d.step('Bước 1: Truy cập vào màn hình Yêu cầu xuất hàng mượn (Cách 1, PHẦN 1).')
    d.step(['Bước 2: Bấm ', '@btn_taomoi'])
    d.img('10c_filled', 'Màn hình Thêm yêu cầu xuất hàng mượn')
    d.step(['Bước 3: Bấm ', '@btn_themphieu', ', bấm vào từng phiếu xuất mượn cần đưa vào phiếu (bắt buộc ít nhất '
            '1 phiếu), rồi bấm ', '@btn_dong_picker'])
    d.sub(['Hoặc bấm ', '@btn_bophieu', ' trên thẻ mã để bỏ phiếu đã chọn.'])
    d.step('Bước 4: Nhập Ghi chú (bắt buộc, tối đa 255 ký tự).')
    d.step(['Bước 5: Bấm ', '@btn_themtailieu', ' và chọn file đính kèm (bắt buộc ít nhất 1 file, chỉ PDF, tối đa '
            '20 MB).'])
    d.step(['Bước 6: Ở bảng Chi tiết, bấm ', '@btn_themhang', ', tích hàng hóa cần xuất, bấm ', '@btn_them_hang_modal',
            ' rồi ', '@btn_dong_product'])
    d.step('Bước 7: Với mỗi hàng, chọn Đơn vị tính và nhập số Xuất theo từng phiếu mượn (số nguyên, không vượt '
           'cột Đang mượn).')
    d.sub(['Hoặc bấm ', '@btn_xoadong', ' để bỏ dòng hàng.'])
    d.sub('Dòng ghi “Chưa có phiếu mượn” là hàng không có trên phiếu mượn đã chọn: không nhập được và không được gửi.')
    d.step(['Bước 8: Bấm ', '@btn_guiduyet', ', chọn Gửi duyệt ở hộp “Xác nhận gửi duyệt” để gửi Kế toán kho'])
    d.sub(['Hoặc ', '@btn_luutieptuc', ' để gửi duyệt rồi lập tiếp phiếu khác.'])
    d.sub(['Hoặc ', '@btn_quaylai_form', ' để không lưu thông tin.'])

    # PHẦN 3 — Xem chi tiết
    d.phan('XEM CHI TIẾT PHIẾU')
    d.step('Bước 1: Truy cập vào màn hình Yêu cầu xuất hàng mượn.')
    d.step('Bước 2: Bấm vào Mã phiếu. Hệ thống mở màn “Chi tiết yêu cầu xuất hàng mượn”.')
    d.img('17_detail', 'Màn hình Chi tiết yêu cầu xuất hàng mượn')
    d.step(['Bước 3: Bấm ', '@btn_quaylai', ' để về màn danh sách.'])

    # PHẦN 4 — Tạo phiếu xuất hàng mượn (duyệt)
    d.phan('DUYỆT PHIẾU (TẠO PHIẾU XUẤT HÀNG MƯỢN)')
    d.step('Bước 1: Truy cập vào màn hình Yêu cầu xuất hàng mượn (Cách 2, PHẦN 1), lọc Trạng thái Chờ duyệt.')
    d.step(['Bước 2: Bấm ', '@btn_duyet_row', ' ở cột Hành động (hoặc bấm Mã phiếu) để mở màn chi tiết.'])
    d.step(['Bước 3: Bấm ', '@btn_taophieuxuat', '. Hệ thống mở màn “Lập phiếu xuất hàng mượn” với phiếu yêu cầu '
            'điền sẵn.'])
    d.img('21_borrow_export_create', 'Màn hình Lập phiếu xuất hàng mượn')
    d.step('Bước 4: Kiểm tra, sửa số Xuất được duyệt nếu cần.')
    d.step(['Bước 5: Bấm ', '@btn_luuvaduyet', '. Phiếu yêu cầu chuyển sang Đã duyệt.'])

    # PHẦN 5 — Từ chối
    d.phan('TỪ CHỐI PHIẾU')
    d.step('Bước 1: Mở màn chi tiết của phiếu Chờ duyệt (Bước 1, 2 PHẦN 4).')
    d.step(['Bước 2: Bấm ', '@btn_tuchoi', '. Hệ thống mở cửa sổ “Từ chối yêu cầu xuất hàng mượn”.'])
    d.img('15_reject', 'Cửa sổ Từ chối yêu cầu xuất hàng mượn')
    d.step('Bước 3: Nhập Lý do từ chối (bắt buộc, tối đa 255 ký tự).')
    d.step(['Bước 4: Bấm ', '@btn_confirm_tuchoi', ' để xác nhận'])
    d.sub(['Hoặc bấm ', '@btn_dong_reject', ' nếu muốn hủy.'])

    # PHẦN 6 — In phiếu
    d.phan('IN PHIẾU')
    d.step(['Bước 1: Ở cột Hành động, bấm ', '@btn_in_row'])
    d.sub(['Hoặc tại màn chi tiết phiếu, bấm ', '@btn_in'])
    d.step('Bước 2: Hệ thống mở cửa sổ xem trước bản in.')
    d.img('18_print', 'Cửa sổ Xem trước phiếu yêu cầu xuất hàng mượn')
    d.step(['Bước 3: Bấm ', '@btn_in_preview', ' để in.'])

    # PHẦN 7 — In danh sách
    d.phan('IN DANH SÁCH')
    d.step('Bước 1: Lọc danh sách theo đúng dữ liệu cần in (xem PHẦN 1).')
    d.step(['Bước 2: Bấm ', '@btn_in_list', '. Hệ thống mở cửa sổ xem trước danh sách.'])
    d.img('19_printlist', 'Cửa sổ Xem trước danh sách yêu cầu xuất hàng mượn')
    d.step(['Bước 3: Bấm ', '@btn_in_preview', ' để in.'])

    # PHẦN 8 — Lịch sử (nút Lịch sử hiện thẳng trên dòng, không có ba chấm)
    d.phan('XEM LỊCH SỬ THAY ĐỔI')
    d.p('Cách 1: Xem lịch sử từ màn danh sách:')
    d.step(['Ở cột Hành động, bấm ', '@btn_lichsu_row'])
    d.p('Cách 2: Xem lịch sử từ màn chi tiết:')
    d.step('Bước 1: Bấm vào Mã phiếu để mở màn chi tiết')
    d.step(['Bước 2: Ở khối Lịch sử, chọn nút ', '@btn_xemlichsu'])
    d.img('16_history', 'Cửa sổ Lịch sử thay đổi của phiếu')
    d.step(['Bước 3: Bấm ', '@btn_boloc_ls', ' để lọc theo Loại hành động, Người thực hiện, Từ ngày, Đến ngày'])
    d.step(['Bước 4: Bấm ', '@btn_dong_ls', ' để đóng cửa sổ.'])

    # PHẦN 9..11
    d.xuat_excel()
    d.cai_dat_bo_loc()
    d.tuy_chinh_cot()
    return d.save(OUT)


if __name__ == '__main__':
    out = build()
    os.makedirs(CHECK_DIR, exist_ok=True)
    pdf = os.path.join(CHECK_DIR, 'HDSD.pdf')
    size = finalize_word(out, pdf)
    print('docx', out, size)
    print('TOC:')
    for line in toc_lines(out):
        print('  ', line)
    n, warn, sheets = render_check(pdf, os.path.join(CHECK_DIR, 'render'))
    print('pages', n)
    for w_ in warn:
        print('WARN', w_)
    for s in sheets:
        print(s)
