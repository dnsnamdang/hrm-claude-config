# -*- coding: utf-8 -*-
"""HDSD bản GỌN — Phiếu xuất hàng mượn (form chuẩn Danh mục quốc gia, 05/11/2026).

Chạy: python gen_hdsd.py  → HDSD_Phieu xuat hang muon.docx (PDF + ảnh soát ghi vào thư mục tạm)
Phần chung: ../phieu-theo-form-quoc-gia/hdsd_phieu_lib.py. Sơ đồ tổng quan dùng lại ảnh gen_srs.py sinh ra (pxhm_shots/uml/overview.png).
Khuôn cấu trúc: ../finance-bill-adjust-dept/gen_hdsd.py + ../borrow-export-request/gen_hdsd.py.
Ảnh + icon: pxhm_shots (dev-hrm 05/11/2026 _capture/capture.js; ảnh cần phiếu yêu cầu Chờ duyệt / lịch sử chụp local
_capture/capture_local.js).
"""
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'phieu-theo-form-quoc-gia'))
from hdsd_phieu_lib import PhieuHdsd, finalize_word, toc_lines, render_check  # noqa: E402

TEN = 'Phiếu xuất hàng mượn'
SHOTS = os.path.join(HERE, 'pxhm_shots')
OUT = os.path.join(HERE, 'HDSD_Phieu xuat hang muon.docx')
CHECK_DIR = os.path.join(tempfile.gettempdir(), 'hdsd_pxhm')

THUAT_NGU = [
    ['Phiếu xuất hàng mượn', 'Chứng từ PXHM-NNNNN Kế toán kho lập để duyệt một phiếu yêu cầu xuất hàng mượn.'],
    ['Phiếu yêu cầu xuất hàng mượn', 'Phiếu PYCXHM-NNNNN người mượn lập, xin xuất hẳn phần hàng đang mượn không trả lại.'],
    ['Phiếu xuất mượn', 'Phiếu yêu cầu xuất hàng loại Xuất mượn (PYCXH-…) đã giao hàng cho người mượn.'],
    ['Đang mượn', 'Số lượng hàng còn được phép xuất trên một phiếu mượn.'],
    ['Xuất', 'Số lượng Kế toán kho chấp nhận xuất hẳn trên từng phiếu mượn (lớn hơn 0, không vượt Đang mượn).'],
    ['Đã duyệt', 'Trạng thái duy nhất của phiếu: phiếu lưu xong là Đã duyệt, không sửa, không xóa.'],
]
PHIEN_BAN = [['1.0', '05/11/2026', 'Tạo mới tài liệu theo form chuẩn']]
QUYEN = [
    ['Mọi chức năng của màn (xem, lập phiếu, in, xuất Excel, xem lịch sử)', 'Quyền Kế toán kho.'],
    ['Xem cột Đơn giá vốn (màn chi tiết, bản in phiếu)', 'Thêm quyền Xem giá vốn hàng hoá.'],
]


def build():
    d = PhieuHdsd(TEN, SHOTS)
    d.tong_quan(THUAT_NGU, PHIEN_BAN, QUYEN, os.path.join(SHOTS, 'uml', 'overview.png'))

    d.phan('TRUY CẬP VÀ TÌM KIẾM')
    d.step(['Bước 1: Từ phân hệ Tài chính ', '@menu_phanhe', ', tại menu Hàng hoá - Dịch vụ - Vận chuyển ', '@menu_nhom',
            ', nhóm Mượn hàng ', '@menu_muonhang', ', chọn Phiếu xuất hàng mượn ', '@menu_muc'])
    d.img('01_list', 'Màn hình Phiếu xuất hàng mượn')
    d.step(['Bước 2: Nhập mã phiếu hoặc mã phiếu yêu cầu vào ô tìm kiếm nhanh ', '@o_timnhanh'])
    d.step(['Bước 3: Nhấn ', '@btn_timkiem'])
    d.step(['Bước 4: Bấm ', '@btn_timkiemnangcao', ', nhập ', '@o_maphieu', ' để lọc theo Mã phiếu'])
    for lb, ic in [('Mã phiếu yêu cầu', 'o_maphieuyc'), ('Người yêu cầu', 'o_nguoiyeucau'), ('Người tạo', 'o_nguoitao'),
                   ('Hàng hóa (tên hoặc mã)', 'o_hanghoa'), ('Trạng thái', 'o_trangthai'), ('Ngày tạo', 'o_ngaytao')]:
        d.sub(['Hoặc chọn / nhập giá trị ', '@' + ic, ' để lọc theo %s' % lb])
    d.step(['Bước 5: Chọn ', '@btn_lammoi', ' để xóa giá trị đã lọc'])

    d.phan('LẬP PHIẾU XUẤT HÀNG MƯỢN')
    d.p('Cách 1: Từ màn Phiếu xuất hàng mượn:')
    d.step('Bước 1: Truy cập vào màn hình Phiếu xuất hàng mượn (PHẦN 1).')
    d.step(['Bước 2: Bấm ', '@btn_taomoi'])
    d.step(['Bước 3: Bấm ô Phiếu yêu cầu xuất hàng mượn ', '@o_phieuyc', ' (bắt buộc), chọn phiếu ở cửa sổ chọn (xem PHẦN 3). '
            'Hệ thống điền Người lập phiếu yêu cầu, Phòng ban, Phiếu xuất mượn và bảng Chi tiết.'])
    d.img('10c_filled', 'Màn hình Lập phiếu xuất hàng mượn')
    d.sub(['Hoặc bấm ', '@btn_xoa_phieuyc', ' trong ô để bỏ phiếu đã chọn.'])
    d.step('Bước 4: Ở bảng Chi tiết, kiểm tra số Xuất của từng phiếu mượn (điền sẵn số đề nghị; bắt buộc, lớn hơn 0, không vượt '
           'cột Đang mượn).')
    d.step(['Bước 5: Nhập Ghi chú ', '@o_ghichu', ' (không bắt buộc, tối đa 255 ký tự).'])
    d.step(['Bước 6: Bấm ', '@btn_luuduyet', ' để lưu phiếu và duyệt phiếu yêu cầu, về màn danh sách'])
    d.sub(['Hoặc ', '@btn_luutieptuc', ' để lưu rồi lập tiếp phiếu khác.'])
    d.sub(['Hoặc ', '@btn_quaylai_form', ' để không lưu, chọn ', '@btn_thoat', ' để rời màn hoặc ', '@btn_olai', ' để ở lại.'])
    d.p('Cách 2: Từ phiếu yêu cầu xuất hàng mượn:')
    d.step('Bước 1: Ở màn Yêu cầu xuất hàng mượn, mở chi tiết phiếu đang Chờ duyệt.')
    d.step(['Bước 2: Bấm ', '@btn_taophieuxuat', '. Hệ thống mở màn Lập phiếu xuất hàng mượn với phiếu yêu cầu chọn sẵn.'])
    d.img('21_from_request', 'Màn Lập phiếu xuất hàng mượn mở từ phiếu yêu cầu')
    d.step('Bước 3: Kiểm tra số Xuất, nhập Ghi chú rồi lưu như Cách 1, Bước 6.')

    d.phan('CHỌN PHIẾU YÊU CẦU XUẤT HÀNG MƯỢN')
    d.step(['Bước 1: Ở màn Lập phiếu, bấm ô ', '@o_phieuyc'])
    d.img('11_picker', 'Cửa sổ Chọn phiếu yêu cầu xuất hàng mượn')
    d.step(['Bước 2: Nhập Mã phiếu hoặc chọn Người tạo, bấm ', '@btn_timkiem_picker'])
    d.sub(['Hoặc bấm ', '@btn_lammoi_picker', ' để xóa điều kiện tìm.'])
    d.step('Bước 3: Bấm vào dòng phiếu cần chọn. Cửa sổ tự đóng, form điền dữ liệu của phiếu.')
    d.sub(['Hoặc bấm ', '@btn_dong_picker', ' để đóng cửa sổ.'])

    d.phan('XEM LỊCH SỬ THAY ĐỔI')
    d.p('Cách 1: Xem lịch sử từ màn danh sách:')
    d.step(['Ở cột Hành động, bấm ', '@btn_lichsu_row'])
    d.p('Cách 2: Xem lịch sử từ màn chi tiết:')
    d.step(['Bước 1: Bấm vào Mã phiếu ', '@link_sophieu', ' để mở màn chi tiết'])
    d.step(['Bước 2: Ở khối Lịch sử, chọn nút ', '@btn_xemlichsu'])
    d.img('16_history', 'Cửa sổ Lịch sử thay đổi của phiếu')
    d.step(['Bước 3: Bấm ', '@btn_boloc_ls', ' để lọc theo Loại hành động, Người thực hiện, Từ ngày, Đến ngày'])
    d.step(['Bước 4: Bấm ', '@btn_dong_ls', ' để đóng cửa sổ.'])

    d.phan('XEM CHI TIẾT')
    d.step('Bước 1: Truy cập vào màn hình Phiếu xuất hàng mượn.')
    d.step(['Bước 2: Bấm vào Mã phiếu ', '@link_sophieu', '. Hệ thống mở màn “Chi tiết phiếu xuất hàng mượn”.'])
    d.sub(['Bấm mã phiếu yêu cầu ', '@link_phieuyc_detail', ' để mở phiếu yêu cầu.'])
    d.img('17_detail', 'Màn hình Chi tiết phiếu xuất hàng mượn')
    d.step(['Bước 3: Bấm ', '@btn_quaylai', ' để về màn danh sách.'])

    d.phan('IN PHIẾU')
    d.step(['Bước 1: Ở cột Hành động, bấm ', '@btn_in_row'])
    d.sub(['Hoặc tại màn chi tiết phiếu, bấm ', '@btn_in'])
    d.step('Bước 2: Hệ thống mở cửa sổ xem trước bản in.')
    d.img('18_print', 'Cửa sổ Xem trước phiếu xuất hàng mượn')
    d.step(['Bước 3: Bấm ', '@btn_in_preview', ' để in.'])

    d.phan('IN DANH SÁCH')
    d.step('Bước 1: Lọc danh sách theo đúng dữ liệu cần in (xem PHẦN 1).')
    d.step(['Bước 2: Bấm ', '@btn_in_list', '. Hệ thống mở cửa sổ xem trước danh sách.'])
    d.img('19_printlist', 'Cửa sổ Xem trước danh sách phiếu xuất hàng mượn')
    d.step(['Bước 3: Bấm ', '@btn_in_preview', ' để in.'])

    d.xuat_excel()
    d.tuy_chinh_cot()
    d.cai_dat_bo_loc()
    return d.save(OUT)


if __name__ == '__main__':
    out = build()
    os.makedirs(CHECK_DIR, exist_ok=True)
    pdf = os.path.join(CHECK_DIR, 'HDSD.pdf')
    size = finalize_word(out, pdf)
    print('docx', out, size)
    for line in toc_lines(out):
        print('  ', line)
    n, warn, sheets = render_check(pdf, os.path.join(CHECK_DIR, 'render'))
    print('pages', n)
    for w_ in warn:
        print('WARN', w_)
    for s in sheets:
        print(s)
