# -*- coding: utf-8 -*-
"""HDSD bản GỌN — Phiếu chuyển hàng nhập thẳng (form chuẩn Danh mục quốc gia, 28/10/2026).

Chạy: python gen_hdsd.py  → out/HDSD_Phiếu chuyển hàng nhập thẳng.docx (+ .pdf, render/ để soát)
Phần dùng chung: ../../phieu-theo-form-quoc-gia/hdsd_phieu_lib.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'phieu-theo-form-quoc-gia'))
from hdsd_phieu_lib import PhieuHdsd, finalize_word, toc_lines, render_check  # noqa: E402

TEN = 'Phiếu chuyển hàng nhập thẳng'
SHOTS = os.path.join(HERE, 'hdsd_shots')
OUT = os.path.join(HERE, 'out', 'HDSD_%s.docx' % TEN)

THUAT_NGU = [
    ['Hàng nhập thẳng', 'Hàng được nhà cung cấp giao thẳng cho nhân viên, không nhập qua kho. Tồn của loại hàng này '
                        'được ghi nhận theo từng nhân viên đang giữ hàng.'],
    ['Phiếu chuyển hàng nhập thẳng', 'Chứng từ để nhân viên đang giữ hàng nhập thẳng chuyển số hàng đó sang một nhân '
                                     'viên khác cùng công ty.'],
    ['Người lập phiếu', 'Người tạo phiếu, cũng chính là người đang giữ hàng và sẽ bị trừ tồn.'],
    ['Người nhận', 'Nhân viên được nhận hàng; sau khi phiếu được duyệt sẽ có tồn tương ứng.'],
    ['Kế toán kho', 'Người duyệt hoặc từ chối phiếu.'],
    ['Tồn hàng nhập thẳng', 'Số hàng nhập thẳng người lập phiếu đang giữ, là nguồn để chọn hàng vào phiếu.'],
    ['ĐVT', 'Đơn vị tính của hàng hóa (Cái, Bộ, Thùng…).'],
    ['SL theo ĐV cơ bản', 'Số lượng quy về đơn vị nhỏ nhất của hàng hóa, là con số hệ thống dùng để trừ tồn.'],
    ['Trạng thái Đang tạo', 'Phiếu lưu nháp, chưa gửi duyệt. Người lập được sửa, xóa.'],
    ['Trạng thái Chờ duyệt', 'Phiếu đã gửi, đang chờ Kế toán kho duyệt. Không sửa, không xóa được.'],
    ['Trạng thái Đã duyệt', 'Tồn đã được chuyển sang người nhận. Chỉ xem, in, xuất Excel.'],
    ['Trạng thái Không duyệt', 'Phiếu bị từ chối, có ghi lý do. Người lập được sửa rồi gửi lại, hoặc xóa.'],
]

PHIEN_BAN = [
    ['1.0', '28/08/2026', 'Ban hành lần đầu cho bản chạy trên hệ thống HRM.'],
    ['1.1', '28/10/2026', 'Chuyển sang form chuẩn'],
]

QUYEN = [
    ['Xem danh sách, xem chi tiết, in, xuất Excel',
     'Một trong các quyền: Xem phiếu chuyển hàng nhập thẳng theo tổng công ty / theo công ty / theo phòng ban / '
     'theo bộ phận. Phiếu do chính mình lập luôn xem được.'],
    ['Lập phiếu', 'Không cần quyền riêng.'],
    ['Sửa, xóa phiếu', 'Người lập phiếu, phiếu đang ở trạng thái Đang tạo hoặc Không duyệt.'],
    ['Duyệt, từ chối phiếu', 'Quyền Kế toán kho, cùng công ty với phiếu, phiếu đang ở trạng thái Chờ duyệt.'],
]


def build():
    d = PhieuHdsd(TEN, SHOTS)
    d.tong_quan(THUAT_NGU, PHIEN_BAN, QUYEN, os.path.join(HERE, 'uml', 'overview_srs.png'))

    # PHẦN 1
    d.truy_cap(
        menu=[('Tài chính', 'menu_phanhe'), ('Hàng hoá - Dịch vụ - Vận chuyển', 'menu_nhom'),
              ('Điều chuyển', 'menu_dieuchuyen'), ('Phiếu chuyển hàng nhập thẳng', 'menu_muc')],
        o_nhanh='số phiếu hoặc tên người tạo',
        bo_loc=[('Công ty', 'o_congty'), ('Phòng ban', 'o_phongban'), ('Số phiếu', 'o_sophieu'),
                ('Trạng thái', 'o_trangthai'), ('Tên/mã hàng hóa', 'o_tenmahang'), ('Người nhận', 'o_nguoinhan'),
                ('Người tạo', 'o_nguoitao'), ('Ngày tạo', 'o_ngaytao')])

    # PHẦN 2 — Lập phiếu
    d.phan('LẬP PHIẾU CHUYỂN HÀNG NHẬP THẲNG')
    d.step(d.vao)
    d.step(['Bước 2: Bấm ', '@btn_taomoi'])
    d.img('10_create', 'Màn hình Thêm phiếu chuyển hàng nhập thẳng')
    d.step('Bước 3: Nhập thông tin chung:')
    d.sub('Người nhận (bắt buộc): chọn nhân viên trong danh sách. Phòng ban tự điền theo người nhận.')
    d.sub('Ghi chú (tùy chọn): nhập chữ, tối đa 255 ký tự.')
    d.step(['Bước 4: Ở khối Chi tiết, bấm ', '@btn_themhanghoa',
            '. Hệ thống mở cửa sổ “Tồn hàng nhập thẳng của nhân viên”.'])
    d.img('11_stock', 'Cửa sổ Tồn hàng nhập thẳng của nhân viên')
    d.step(['Bước 5: Tích chọn ', '@o_tick', ' các hàng cần chuyển, bấm ', '@btn_chon'])
    d.sub(['Hoặc bấm ', '@btn_dong', ' để không chọn hàng.'])
    d.step('Bước 6: Nhập thông tin từng dòng hàng (bắt buộc):')
    d.sub('ĐVT: chọn đơn vị tính trong danh sách.')
    d.sub('Số lượng: chỉ nhập số, lớn hơn 0 và không vượt Tồn hiện có; dấu phẩy ngăn hàng nghìn, '
          'dấu chấm ngăn phần thập phân (ví dụ 1,200.5).')
    d.sub(['Hoặc bấm ', '@btn_xoadong', ' để bỏ dòng hàng khỏi phiếu.'])
    d.step(['Bước 7: Bấm ', '@btn_luuguiduyet', ', chọn ', '@btn_confirm_xacnhan', ' để gửi Kế toán kho duyệt,'])
    d.sub(['Hoặc ', '@btn_luunhap', ' để lưu nháp (chỉ cần chọn Người nhận).'])
    d.sub(['Hoặc ', '@btn_luutieptuc', ' để lưu nháp rồi lập tiếp phiếu khác.'])
    d.sub(['Hoặc ', '@btn_quaylai', ' để không lưu thông tin.'])

    # PHẦN 3 — Chỉnh sửa
    d.phan('CHỈNH SỬA')
    d.step(d.vao)
    d.step(['Bước 2: Bấm nút ', '@btn_sua_row', ' ở cột Hành động của phiếu Đang tạo hoặc Không duyệt.'])
    d.sub(['Hoặc bấm vào Số phiếu để mở màn chi tiết, chọn ', '@btn_sua'])
    d.step('Bước 3: Hệ thống hiển thị màn hình “Sửa phiếu chuyển hàng nhập thẳng”.')
    d.img('12_edit', 'Màn hình Sửa phiếu chuyển hàng nhập thẳng')
    d.step('Bước 4: Nhập thông tin cần sửa (quy tắc nhập như Lập phiếu ở PHẦN 2).')
    d.step(['Bước 5: Bấm ', '@btn_luuguiduyet', ' để lưu và gửi duyệt,'])
    d.sub(['Hoặc ', '@btn_luunhap', ' để lưu nháp.'])
    d.sub(['Hoặc ', '@btn_quaylai', ' nếu muốn hủy.'])

    # PHẦN 4 — Xóa
    d.xoa('Xác nhận xóa', them_cach=['Hoặc bấm vào Số phiếu để mở màn chi tiết, chọn ', '@btn_xoa'])

    # PHẦN 5 — Duyệt
    d.phan('DUYỆT PHIẾU')
    d.step(['Bước 1: Bấm ', '@btn_duyet_row', ' ở cột Hành động của phiếu Chờ duyệt để mở màn chi tiết.'])
    d.sub('Hoặc bấm vào Số phiếu của phiếu Chờ duyệt.')
    d.step('Bước 2: Kiểm tra Người nhận và các dòng hàng hóa.')
    d.step(['Bước 3: Bấm ', '@btn_duyet'])
    d.step('Bước 4: Hệ thống hiện hộp xác nhận “Xác nhận duyệt”.')
    d.img('14_approve', 'Hộp xác nhận duyệt phiếu')
    d.step(['Bước 5: Bấm ', '@btn_confirm_xacnhan', ' để duyệt phiếu'])
    d.sub(['Hoặc bấm ', '@btn_huy_confirm', ' nếu bấm nhầm'])

    # PHẦN 6 — Từ chối
    d.phan('TỪ CHỐI PHIẾU')
    d.step('Bước 1: Mở màn chi tiết của phiếu Chờ duyệt (như Bước 1 PHẦN 5).')
    d.step(['Bước 2: Bấm ', '@btn_tuchoi', '. Hệ thống mở cửa sổ “Từ chối phiếu”.'])
    d.img('15_reject', 'Cửa sổ Từ chối phiếu')
    d.step('Bước 3: Nhập Lý do từ chối (bắt buộc).')
    d.step(['Bước 4: Bấm ', '@btn_confirm_tuchoi', ' để xác nhận'])
    d.sub(['Hoặc bấm ', '@btn_dong_reject', ' nếu muốn hủy.'])

    # PHẦN 7 — Lịch sử
    d.lich_su('Số phiếu', img='16_history', cap='Cửa sổ Lịch sử thay đổi của phiếu')

    # PHẦN 8 — Xem chi tiết
    d.phan('XEM CHI TIẾT PHIẾU')
    d.step(d.vao)
    d.step('Bước 2: Bấm vào Số phiếu. Hệ thống mở màn “Chi tiết phiếu chuyển hàng nhập thẳng”.')
    d.img('17_detail', 'Màn hình Chi tiết phiếu chuyển hàng nhập thẳng')
    d.step(['Bước 3: Bấm ', '@btn_quaylai', ' để về màn danh sách.'])

    # PHẦN 9 — In
    d.phan('IN PHIẾU VÀ IN DANH SÁCH')
    d.h2('1. In phiếu')
    d.step(['Bước 1: Ở cột Hành động, bấm ', '@btn_in_row'])
    d.sub(['Hoặc bấm ', '@btn_bacham_row', ' rồi chọn ', '@item_in'])
    d.sub(['Hoặc tại màn chi tiết phiếu, bấm ', '@btn_in'])
    d.step('Bước 2: Hệ thống mở cửa sổ xem trước bản in.')
    d.img('18_print', 'Cửa sổ Xem trước phiếu chuyển hàng nhập thẳng')
    d.step(['Bước 3: Bấm ', '@btn_in_preview', ' để in.'])
    d.h2('2. In danh sách')
    d.step('Bước 1: Lọc danh sách theo đúng dữ liệu cần in (xem PHẦN 1).')
    d.step(['Bước 2: Bấm ', '@btn_in_list', '. Hệ thống mở cửa sổ xem trước danh sách.'])
    d.img('19_printlist', 'Cửa sổ Xem trước danh sách phiếu chuyển hàng nhập thẳng')
    d.step(['Bước 3: Bấm ', '@btn_in_preview', ' để in.'])

    # PHẦN 10..12
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
