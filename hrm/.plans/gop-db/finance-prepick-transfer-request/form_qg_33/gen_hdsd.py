# -*- coding: utf-8 -*-
"""HDSD bản GỌN — Yêu cầu điều chuyển hàng giữ (STT 33, form chuẩn Danh mục quốc gia, 28/10/2026).

Chạy: python gen_hdsd.py  → out/HDSD_Yêu cầu điều chuyển hàng giữ.docx (+ .pdf, render/ để soát)
Ảnh: hdsd_shots/ (capture.js, chụp trên dev-hrm); icon dùng chung form_qg_31/hdsd_shots/icons.
Phần dùng chung: ../../phieu-theo-form-quoc-gia/hdsd_phieu_lib.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'phieu-theo-form-quoc-gia'))
from hdsd_phieu_lib import PhieuHdsd, finalize_word, toc_lines, render_check  # noqa: E402

TEN = 'Yêu cầu điều chuyển hàng giữ'
SHOTS = os.path.join(HERE, 'hdsd_shots')
OUT = os.path.join(HERE, 'out', 'HDSD_%s.docx' % TEN)
ICONS = [os.path.join(SHOTS, 'icons'),
         os.path.join(HERE, '..', '..', 'finance-prepick-extend-request', 'form_qg_31', 'hdsd_shots', 'icons')]

THUAT_NGU = [
    ['Hàng giữ', 'Số lượng hàng hóa được giữ lại cho một khách hàng cụ thể, do một nhân viên kinh doanh đứng tên giữ.'],
    ['Lô hàng giữ', 'Một dòng hàng giữ cụ thể, gồm: người giữ – khách hàng – hàng hóa – hạn giữ – công ty.'],
    ['Điều chuyển hàng giữ', 'Chuyển một phần hoặc toàn bộ hàng đang giữ sang một nhân viên nhận và một khách hàng '
                             'nhận khác. Hạn giữ giữ nguyên theo lô nguồn.'],
    ['Người nhận', 'Nhân viên sẽ đứng tên giữ hàng sau khi phiếu được duyệt.'],
    ['Khách hàng nhận', 'Khách hàng mà hàng sẽ được giữ cho sau khi phiếu được duyệt.'],
    ['Từ xuất giữ', 'Lô hàng giữ nguồn được chọn để lấy hàng chuyển đi.'],
    ['Đang giữ', 'Số lượng còn lại của chính lô hàng giữ nguồn.'],
    ['Có thể giữ', 'Số lượng hàng còn trong kho có thể giữ tiếp. Đây là số tham khảo, khác với cột Đang giữ.'],
    ['TP / BGĐ / KT', 'Trưởng phòng / Ban giám đốc / Kế toán — ba cấp duyệt của phiếu.'],
    ['Trạng thái Chờ TP / BGĐ / KT duyệt', 'Phiếu đang chờ cấp tương ứng duyệt. Lập phiếu là vào thẳng Chờ TP duyệt '
                                           '(không có lưu nháp).'],
    ['Trạng thái Đã duyệt', 'Kế toán đã duyệt, hàng đã chuyển sang người nhận. Chỉ xem, in, xuất Excel.'],
    ['Trạng thái Không duyệt', 'Phiếu bị một cấp duyệt từ chối. Chỉ người lập thấy; được sửa rồi gửi lại, hoặc xóa.'],
]

PHIEN_BAN = [
    ['1.0', '05/09/2026', 'Ban hành lần đầu cho màn hình Yêu cầu điều chuyển hàng giữ trên phân hệ Tài chính.'],
    ['1.1', '28/10/2026', 'Chuyển sang form chuẩn'],
]

QUYEN = [
    ['Xem danh sách, xem chi tiết, in, xuất Excel',
     'Một trong các quyền: Xem phiếu hàng giữ theo tổng công ty / theo công ty / theo phòng ban. Phiếu do chính mình '
     'lập và phiếu đang chờ mình duyệt luôn xem được.'],
    ['Lập phiếu', 'Không cần quyền riêng.'],
    ['Sửa, xóa phiếu', 'Người lập phiếu, phiếu đang ở trạng thái Không duyệt.'],
    ['Duyệt, từ chối phiếu', 'Quyền Trưởng phòng duyệt hàng giữ (phiếu Chờ TP duyệt, người nhận thuộc phòng ban mình '
                             'quản lý) / Ban giám đốc duyệt hàng giữ (Chờ BGĐ duyệt) / Kế toán duyệt hàng giữ (Chờ KT '
                             'duyệt); cùng công ty với phiếu.'],
]


def build():
    d = PhieuHdsd(TEN, SHOTS, icon_dirs=ICONS)
    d.tong_quan(THUAT_NGU, PHIEN_BAN, QUYEN, os.path.join(HERE, 'uml', 'overview_srs.png'))

    # PHẦN 1
    d.truy_cap(
        menu=[('Tài chính', 'menu_phanhe'), ('Hàng hoá - Dịch vụ - Vận chuyển', 'menu_nhom'),
              ('Giữ hàng', 'menu_giuhang'), ('Phiếu Yêu cầu điều chuyển hàng giữ', 'menu_muc_33')],
        o_nhanh='mã phiếu',
        bo_loc=[('Công ty', 'o_congty'), ('Phòng ban', 'o_phongban'), ('Mã phiếu', 'o_maphieu'),
                ('Trạng thái', 'o_trangthai'), ('Người nhận', 'o_nguoinhan'), ('Khách nhận', 'o_khachnhan'),
                ('Người tạo', 'o_nguoitao'), ('Người duyệt', 'o_nguoiduyet'), ('Tên, mã hàng', 'o_tenmahang'),
                ('Số hợp đồng', 'o_sohopdong'), ('Ngày tạo', 'o_ngaytao')])

    # PHẦN 2 — Lập phiếu
    d.phan('LẬP PHIẾU YÊU CẦU ĐIỀU CHUYỂN')
    d.step(d.vao)
    d.step(['Bước 2: Bấm ', '@btn_taomoi'])
    d.step('Bước 3: Hệ thống mở màn “Thêm yêu cầu điều chuyển hàng giữ”.')
    d.img('10_create', 'Màn hình Thêm yêu cầu điều chuyển hàng giữ')
    d.step('Bước 4: Nhập thông tin chung:')
    d.sub('Người nhận (bắt buộc): chọn nhân viên sẽ đứng tên giữ hàng.')
    d.sub('Khách hàng nhận (bắt buộc): gõ tối thiểu 2 ký tự rồi chọn khách hàng.')
    d.sub('Ghi chú (tùy chọn): tối đa 255 ký tự.')
    d.sub(['File đính kèm (tùy chọn): bấm ', '@btn_themtailieu',
           ', chọn tệp PDF, ảnh, Word, Excel; mỗi tệp tối đa 13 MB.'])
    d.step(['Bước 5: Ở khối Chi tiết, bấm ', '@btn_themhanghoa', '. Hệ thống mở cửa sổ “Hàng bạn đang giữ”.'])
    d.img('11_stock', 'Cửa sổ Hàng bạn đang giữ')
    d.step(['Bước 6: Tích chọn ', '@o_tick', ' các hàng cần chuyển, bấm ', '@btn_chon'])
    d.sub(['Hoặc bấm ', '@btn_dong', ' để không chọn hàng.'])
    d.step('Bước 7: Nhập thông tin từng dòng hàng:')
    d.sub(['Từ xuất giữ (bắt buộc): bấm ', '@btn_chonlo', ', chọn lô hàng giữ nguồn còn hạn trong cửa sổ “Chọn lô '
           'hàng giữ”. Mỗi lô chỉ chọn ở một dòng.'])
    d.sub('Chuyển (bắt buộc): chỉ nhập số, lớn hơn 0 và không vượt số Đang giữ của lô.')
    d.sub(['Hợp đồng (tùy chọn): bấm ', '@btn_chonhopdong', ' để chọn đơn hàng / hợp đồng.'])
    d.sub(['Hoặc bấm ', '@btn_xoadong', ' để bỏ dòng hàng khỏi phiếu.'])
    d.step(['Bước 8: Bấm ', '@btn_guiduyet', ' để gửi duyệt (phiếu vào thẳng trạng thái Chờ TP duyệt, không có lưu '
            'nháp),'])
    d.sub(['Hoặc ', '@btn_luutieptuc', ' để gửi duyệt rồi lập tiếp phiếu khác.'])
    d.sub(['Hoặc ', '@btn_quaylai', ' để không lưu thông tin.'])

    # PHẦN 3 — Chỉnh sửa
    d.phan('CHỈNH SỬA')
    d.step(d.vao)
    d.step(['Bước 2: Bấm nút ', '@btn_sua_row', ' ở cột Hành động của phiếu Không duyệt do bạn lập.'])
    d.sub(['Hoặc bấm vào Mã phiếu để mở màn chi tiết, chọn ', '@btn_sua'])
    d.step('Bước 3: Hệ thống hiển thị màn hình “Sửa yêu cầu điều chuyển hàng giữ”.')
    d.img('12_edit', 'Màn hình Sửa yêu cầu điều chuyển hàng giữ')
    d.step('Bước 4: Sửa thông tin theo lý do bị trả về (quy tắc nhập như Lập phiếu ở PHẦN 2).')
    d.step(['Bước 5: Bấm ', '@btn_guiduyet', ' để gửi duyệt lại từ đầu (Chờ TP duyệt),'])
    d.sub(['Hoặc ', '@btn_quaylai', ' nếu muốn hủy.'])

    # PHẦN 4 — Xóa
    d.xoa('Xác nhận xóa', them_cach=['Hoặc bấm vào Mã phiếu để mở màn chi tiết, chọn ', '@btn_xoa'])

    # PHẦN 5 — Duyệt
    d.phan('DUYỆT PHIẾU')
    d.step(['Bước 1: Bấm ', '@btn_duyet_row', ' ở cột Hành động của phiếu đang chờ bạn duyệt để mở màn chi tiết.'])
    d.sub('Hoặc bấm vào Mã phiếu của phiếu đó.')
    d.step('Bước 2: Kiểm tra Người nhận, Khách hàng nhận và các dòng hàng.')
    d.step(['Bước 3: Bấm nút duyệt theo cấp của bạn (TP duyệt / BGĐ duyệt / KT duyệt), ví dụ ', '@btn_duyet'])
    d.step('Bước 4: Hệ thống hiện hộp xác nhận “Xác nhận duyệt”.')
    d.img('14_approve', 'Hộp xác nhận duyệt phiếu')
    d.step(['Bước 5: Bấm ', '@btn_confirm_duyet', ' để duyệt phiếu'])
    d.sub(['Hoặc bấm ', '@btn_huy_confirm', ' nếu bấm nhầm'])

    # PHẦN 6 — Từ chối
    d.phan('TỪ CHỐI PHIẾU')
    d.step('Bước 1: Mở màn chi tiết của phiếu đang chờ bạn duyệt (như Bước 1 PHẦN 5).')
    d.step(['Bước 2: Bấm ', '@btn_tuchoi', '. Hệ thống mở cửa sổ “Từ chối yêu cầu điều chuyển hàng giữ”.'])
    d.img('15_reject', 'Cửa sổ Từ chối yêu cầu điều chuyển hàng giữ')
    d.step('Bước 3: Nhập Lý do từ chối (bắt buộc, tối đa 255 ký tự).')
    d.step(['Bước 4: Bấm ', '@btn_confirm_tuchoi', ' để xác nhận. Phiếu chuyển sang trạng thái Không duyệt.'])
    d.sub(['Hoặc bấm ', '@btn_dong_reject', ' nếu muốn hủy.'])

    # PHẦN 7 — Lịch sử
    d.lich_su('Mã phiếu', img='16_history', cap='Cửa sổ Lịch sử yêu cầu điều chuyển hàng giữ')

    # PHẦN 8 — Xem chi tiết
    d.phan('XEM CHI TIẾT PHIẾU')
    d.step(d.vao)
    d.step('Bước 2: Bấm vào Mã phiếu. Hệ thống mở màn “Chi tiết yêu cầu điều chuyển hàng giữ”.')
    d.img('17_detail', 'Màn hình Chi tiết yêu cầu điều chuyển hàng giữ')
    d.step(['Bước 3: Bấm ', '@btn_quaylai', ' để về màn danh sách.'])

    # PHẦN 9 — In
    d.phan('IN PHIẾU VÀ IN DANH SÁCH')
    d.h2('1. In phiếu')
    d.step(['Bước 1: Ở cột Hành động, bấm ', '@btn_in_row'])
    d.sub(['Hoặc bấm ', '@btn_bacham_row', ' rồi chọn ', '@item_in'])
    d.sub(['Hoặc tại màn chi tiết phiếu, bấm ', '@btn_in'])
    d.step('Bước 2: Hệ thống mở cửa sổ xem trước bản in.')
    d.img('18_print', 'Bản xem trước phiếu yêu cầu điều chuyển hàng giữ')
    d.step(['Bước 3: Bấm ', '@btn_in_preview', ' để in.'])
    d.h2('2. In danh sách')
    d.step('Bước 1: Lọc danh sách theo đúng dữ liệu cần in (xem PHẦN 1).')
    d.step(['Bước 2: Bấm ', '@btn_in_list', '. Hệ thống mở cửa sổ xem trước danh sách.'])
    d.img('19_printlist', 'Bản xem trước danh sách yêu cầu điều chuyển hàng giữ')
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
