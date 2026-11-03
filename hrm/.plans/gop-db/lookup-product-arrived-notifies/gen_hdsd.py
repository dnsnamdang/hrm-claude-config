# -*- coding: utf-8 -*-
"""HDSD bản GỌN — Phiếu báo hàng về (phân hệ Thông báo, 3 tab) — form chuẩn Danh mục quốc gia (03/11/2026).

Chạy: python gen_hdsd.py  → HDSD_Phieu bao hang ve.docx (PDF + ảnh soát ghi vào thư mục tạm)
Phần chung: ../phieu-theo-form-quoc-gia/hdsd_phieu_lib.py. Sơ đồ tổng quan dùng lại ảnh gen_srs.py sinh ra (chạy gen_srs.py trước).
Ảnh: ./pbhv_shots (dev-hrm 03/11/2026, script pbhv_shots/_capture/capture.js).
"""
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'phieu-theo-form-quoc-gia'))
from hdsd_phieu_lib import PhieuHdsd, finalize_word, toc_lines, render_check  # noqa: E402

TEN = 'Phiếu báo hàng về'
SHOTS = os.path.join(HERE, 'pbhv_shots')
OUT = os.path.join(HERE, 'HDSD_Phieu bao hang ve.docx')
CHECK_DIR = os.path.join(tempfile.gettempdir(), 'hdsd_pbhv')   # PDF + ảnh soát, không để trong repo

THUAT_NGU = [
    ['Phiếu báo hàng về', 'Phiếu thông báo hàng mua sắp về kho, mã dạng PBHV-00667. Phiếu được lập ở hệ thống ERP, màn này để tra '
                          'cứu và thao tác tiếp.'],
    ['Nhập khẩu / Trong nước / Mua ngoài', '3 tab của màn: hàng mua nước ngoài theo invoice; hàng mua trong nước theo hợp đồng '
                                           'mới; hàng mua ngoài theo hợp đồng / phụ lục hợp đồng mua trong nước.'],
    ['Đã gửi', 'Phiếu đã báo, chưa lập chứng từ tiếp theo (nhãn vàng). Người tạo phiếu xóa được (tab Nhập khẩu) và lập phân bổ '
               'chi phí / yêu cầu nhập hàng được.'],
    ['Đã yêu cầu nhập hàng', 'Đã lập phiếu yêu cầu nhập hàng / phân bổ chi phí từ phiếu (nhãn xanh lá).'],
    ['Hệ thống ERP', 'Hệ thống quản trị cũ; mã invoice, hợp đồng, đơn đặt hàng mở màn của hệ thống này ở tab mới.'],
]
PHIEN_BAN = [['1.0', '03/11/2026', 'Tạo mới tài liệu theo form chuẩn']]
QUYEN = [
    ['Xem danh sách, tìm kiếm, xuất Excel, xem chi tiết, in, xuất Excel một phiếu',
     'Mọi người dùng vào được phân hệ Thông báo. Tab Nhập khẩu chỉ hiện phiếu trong phạm vi quyền Xem phiếu báo hàng về mua '
     'nhập khẩu theo tổng công ty / theo công ty / theo phòng ban; không có quyền nào thì phiếu mình tạo và phiếu có hàng '
     'thuộc thương hiệu mình phụ trách mua.'],
    ['Xóa, Tạo phân bổ chi phí, Tạo (phiếu) yêu cầu nhập hàng', 'Người tạo phiếu; phiếu ở trạng thái Đã gửi.'],
]


def build():
    d = PhieuHdsd(TEN, SHOTS)
    d.tong_quan(THUAT_NGU, PHIEN_BAN, QUYEN, os.path.join(SHOTS, 'uml', 'overview.png'))

    d.phan('TRUY CẬP VÀ TÌM KIẾM')
    d.step(['Bước 1: Từ phân hệ Thông báo ', '@menu_phanhe', ', tại menu Thông báo ', '@menu_thongbao',
            ', chọn Phiếu báo hàng về ', '@menu_muc'])
    d.img('01_list', 'Màn hình Phiếu báo hàng về — tab Nhập khẩu')
    d.step(['Bước 2: Chọn tab ', '@tab_nhapkhau', ' (mặc định)'])
    d.sub(['Hoặc chọn tab ', '@tab_trongnuoc', ' để xem phiếu trong nước'])
    d.sub(['Hoặc chọn tab ', '@tab_muangoai', ' để xem phiếu mua ngoài'])
    d.step(['Bước 3: Nhập mã phiếu vào ô tìm kiếm nhanh ', '@o_timnhanh'])
    d.step(['Bước 4: Nhấn ', '@btn_timkiem'])
    d.step(['Bước 5: Bấm ', '@btn_timkiemnangcao', ', chọn giá trị trong ', '@o_trangthai', ' để lọc theo Trạng thái'])
    for lb, ic in [('Nhà cung cấp (gõ mã hoặc tên rồi chọn)', 'o_ncc'), ('Invoice (tab Nhập khẩu)', 'o_invoice'),
                   ('Hợp đồng', 'o_hopdong'), ('Tên, mã hàng (tab Nhập khẩu, Mua ngoài)', 'o_hang'),
                   ('Tên hàng (tab Trong nước)', 'o_tenhang'), ('Mã hàng (tab Trong nước)', 'o_mahang'), ('Kho', 'o_kho'),
                   ('Model (tab Nhập khẩu)', 'o_model'), ('Barcode (tab Nhập khẩu)', 'o_barcode'),
                   ('Người tạo (tab Nhập khẩu)', 'o_nguoitao'), ('Công ty (tab Mua ngoài)', 'o_congty'),
                   ('Phòng ban (tab Mua ngoài)', 'o_phongban'), ('Bộ phận (tab Mua ngoài)', 'o_bophan'),
                   ('Ngày tạo (từ ngày → đến ngày)', 'o_ngaytao')]:
        d.sub(['Hoặc chọn / nhập giá trị ', '@' + ic, ' để lọc theo %s' % lb])
    d.step(['Bước 6: Ô nhập chữ (Invoice, Hợp đồng, Tên, mã hàng, Model, Barcode…) bấm ', '@btn_timkiem', ' để áp dụng'])
    d.step(['Bước 7: Chọn ', '@btn_lammoi', ' để xóa giá trị đã lọc'])

    d.phan('XEM CHI TIẾT PHIẾU')
    d.step('Bước 1: Truy cập vào màn hình Phiếu báo hàng về, chọn tab của phiếu (PHẦN 1).')
    d.step(['Bước 2: Bấm vào mã phiếu ', '@link_ma', '. Hệ thống mở màn “Chi tiết phiếu báo hàng về: <mã phiếu>”.'])
    d.img('17_detail_import', 'Màn hình Chi tiết phiếu báo hàng về nhập khẩu')
    d.step(['Bước 3: Tích ', '@chk_chitiet', ' để xem thêm Tên khách, Ngày cần, Ghi chú của từng dòng khách'])
    d.step(['Bước 4: Phiếu nhập khẩu: bấm ', '@tab_khuyenmai', ' / ', '@tab_baohanh', ' / ', '@tab_thuathieu',
            ' để xem hàng khuyến mại, bảo hành, thừa thiếu của invoice'])
    d.sub(['Hoặc bấm ', '@tab_hanghoa', ' để quay lại bảng hàng hóa'])
    d.step('Bước 5: Bấm mã invoice / hợp đồng / đơn đặt hàng để mở màn tương ứng của hệ thống ERP ở tab mới.')
    d.step(['Bước 6: Bấm ', '@btn_quaylai', ' để về màn danh sách'])

    d.phan('XÓA PHIẾU NHẬP KHẨU')
    d.step(['Bước 1: Ở tab Nhập khẩu, bấm ', '@btn_xoa_row', ' ở cột Hành động của phiếu Đã gửi do mình tạo'])
    d.sub(['Hoặc tại màn chi tiết phiếu, bấm ', '@btn_xoa'])
    d.step('Bước 2: Hệ thống hiện hộp xác nhận “Xác nhận xóa”')
    d.img('13_delete', 'Hộp xác nhận xóa phiếu')
    d.step(['Bước 3: Bấm ', '@btn_confirm_xoa', ' để xác nhận xóa'])
    d.sub(['Hoặc bấm ', '@btn_huy_confirm', ' nếu bấm nhầm'])

    d.phan('IN PHIẾU NHẬP KHẨU')
    d.step(['Bước 1: Ở tab Nhập khẩu, bấm ', '@btn_in_row', ' ở cột Hành động'])
    d.sub(['Hoặc tại màn chi tiết phiếu, bấm ', '@btn_in'])
    d.step('Bước 2: Hệ thống mở cửa sổ “Xem trước phiếu báo hàng về”.')
    d.img('18_print', 'Cửa sổ Xem trước phiếu báo hàng về')
    d.step(['Bước 3: Bấm ', '@btn_in_preview', ' để in.'])

    d.phan('XUẤT EXCEL')
    d.p('Cách 1: Xuất danh sách:')
    d.step('Bước 1: Chọn tab và lọc danh sách theo đúng dữ liệu cần lấy (xem PHẦN 1).')
    d.step(['Bước 2: Bấm ', '@btn_xuatexcel', '. Hệ thống mở cửa sổ “Chọn trường xuất file”.'])
    d.img('20_export', 'Cửa sổ Chọn trường xuất file')
    d.step('Bước 3: Tích chọn, kéo biểu tượng ≡ để đổi vị trí các trường cần xuất.')
    d.sub(['Hoặc bấm ', '@btn_chontatca_x', ' / ', '@btn_bochonhet_x'])
    d.step(['Bước 4: Bấm ', '@btn_xuatfile'])
    d.sub(['Hoặc bấm ', '@btn_dong_export', ' để không xuất'])
    d.p('Cách 2: Xuất một phiếu nhập khẩu:')
    d.step(['Bước 1: Ở tab Nhập khẩu, bấm ', '@btn_xuat_row', ' ở cột Hành động'])
    d.sub(['Hoặc tại màn chi tiết phiếu, bấm ', '@btn_xuat'])
    d.step('Bước 2: Mở file Excel đã tải.')

    d.phan('TẠO PHÂN BỔ CHI PHÍ')
    d.step('Bước 1: Ở tab Nhập khẩu, bấm mã phiếu Đã gửi do mình tạo để mở màn chi tiết.')
    d.img('17b_detail_import_owner', 'Màn chi tiết phiếu nhập khẩu của người tạo phiếu')
    d.step(['Bước 2: Bấm ', '@btn_phanbo', '. Hệ thống mở form tạo phân bổ chi phí của hệ thống ERP ở tab mới.'])
    d.step('Bước 3: Nhập và lưu phân bổ chi phí trên hệ thống ERP.')

    d.phan('TẠO PHIẾU YÊU CẦU NHẬP HÀNG')
    d.p('Cách 1: Từ phiếu mua ngoài:')
    d.step('Bước 1: Ở tab Mua ngoài, bấm mã phiếu Đã gửi do mình tạo để mở màn chi tiết.')
    d.step(['Bước 2: Bấm ', '@btn_taoycnh', '. Hệ thống mở màn “Thêm phiếu yêu cầu nhập hàng”.'])
    d.img('21_ycnh_create', 'Màn Thêm phiếu yêu cầu nhập hàng (loại Nhập hàng mua ngoài, phiếu báo hàng về chọn sẵn)')
    d.step('Bước 3: Kiểm tra Loại yêu cầu (Nhập hàng mua ngoài), Phiếu báo hàng về, Hợp đồng, Nhà cung cấp, Hàng hoá đã điền sẵn.')
    d.step('Bước 4: Chọn Kho nhập và Vận chuyển (bắt buộc), nhập Ghi chú, đính kèm file nếu cần.')
    d.step('Bước 5: Bấm Lưu và gửi duyệt hoặc Lưu nháp. Phiếu báo hàng về chuyển sang Đã yêu cầu nhập hàng.')
    d.p('Cách 2: Từ phiếu trong nước:')
    d.step(['Bước 1: Ở màn chi tiết phiếu trong nước Đã gửi do mình tạo, bấm ', '@btn_taoycnh_inland'])
    d.step('Bước 2: Lập yêu cầu nhập hàng trên form của hệ thống ERP mở ở tab mới.')

    d.cai_dat_bo_loc()
    d.tuy_chinh_cot()
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
