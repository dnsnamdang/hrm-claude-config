# -*- coding: utf-8 -*-
"""HDSD bản GỌN — Phiếu hủy hàng giữ (STT 191, form chuẩn Danh mục quốc gia, 28/10/2026).

Chạy: python gen_hdsd.py  → out/HDSD_Phiếu hủy hàng giữ.docx (+ .pdf, render/ để soát)
Khuôn chép từ màn 27 (finance-product-import-direct-transfer/form_qg/gen_hdsd.py).
Màn KHÔNG có Sửa / Xóa; lập phiếu = duyệt phiếu yêu cầu, có 2 lối vào màn lập phiếu.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'phieu-theo-form-quoc-gia'))
from hdsd_phieu_lib import PhieuHdsd, finalize_word, toc_lines, render_check  # noqa: E402

TEN = 'Phiếu hủy hàng giữ'
SHOTS = os.path.join(HERE, 'hdsd_shots')
OUT = os.path.join(HERE, 'out', 'HDSD_%s.docx' % TEN)

THUAT_NGU = [
    ['Hàng giữ', 'Số lượng hàng hóa được giữ lại cho một khách hàng cụ thể, do một nhân viên kinh doanh đứng tên giữ.'],
    ['Lô hàng giữ', 'Một phần hàng giữ có cùng hạn giữ. Một hàng hóa có thể nằm trên nhiều lô.'],
    ['Yêu cầu hủy hàng giữ', 'Phiếu nhân viên lập để đề nghị trả lại kho phần hàng đang giữ. Mã dạng PYCHHG-NNNNN. '
                             'Phiếu này chưa trừ hàng giữ.'],
    ['Phiếu hủy hàng giữ', 'Chứng từ lập từ một phiếu yêu cầu đang chờ duyệt. Mã dạng PHHG-NNNNN. Lưu phiếu này là '
                           'duyệt phiếu yêu cầu và trừ hàng giữ ngay.'],
    ['Có thể hủy', 'Số hàng giữ còn lại của người lập phiếu yêu cầu, tính lại lúc mở phiếu. Là trần của Duyệt hủy.'],
    ['Yêu cầu hủy', 'Số lượng người lập phiếu yêu cầu đã đề nghị. Chỉ để tham khảo.'],
    ['Duyệt hủy', 'Số lượng thực sự cho hủy, là số bị trừ khỏi hàng giữ.'],
    ['Trạng thái Đã đề nghị', 'Trạng thái duy nhất của phiếu hủy. Phiếu lập xong không sửa, không xóa được.'],
]

PHIEN_BAN = [
    ['1.0', '09/09/2026', 'Ban hành lần đầu cho màn hình Phiếu hủy hàng giữ trên phân hệ Tài chính.'],
    ['1.1', '28/10/2026', 'Chuyển sang form chuẩn'],
]

QUYEN = [
    ['Xem danh sách, xem chi tiết, in, xuất Excel, xem lịch sử',
     'Không cần quyền riêng. Phạm vi theo quyền Xem phiếu hàng giữ theo tổng công ty / theo công ty; quyền Quản lý giữ '
     'hàng xem phiếu thuộc công ty mình. Không có quyền nào thì chỉ thấy phiếu do mình lập hoặc sinh ra từ phiếu yêu '
     'cầu do mình lập.'],
    ['Lập phiếu hủy (duyệt phiếu yêu cầu)', 'Quyền Quản lý giữ hàng. Thiếu quyền thì cửa sổ chọn phiếu yêu cầu luôn '
                                            'rỗng.'],
    ['Sửa, xóa', 'Không có. Phiếu lập xong là chốt.'],
]


def build():
    d = PhieuHdsd(TEN, SHOTS)
    d.tong_quan(THUAT_NGU, PHIEN_BAN, QUYEN, os.path.join(HERE, 'uml', 'overview_drive.png'))

    # PHẦN 1
    d.truy_cap(
        menu=[('Tài chính', 'menu_phanhe'), ('Hàng hoá - Dịch vụ - Vận chuyển', 'menu_nhom'),
              ('Giữ hàng', 'menu_giuhang'), ('Phiếu hủy hàng giữ', 'menu_muc')],
        o_nhanh='mã phiếu hoặc mã phiếu yêu cầu',
        bo_loc=[('Trạng thái', 'o_trangthai'), ('Mã phiếu yêu cầu', 'o_maphieuyc'),
                ('Người yêu cầu', 'o_nguoiyeucau'), ('Người tạo', 'o_nguoitao'),
                ('Tên/mã hàng hóa', 'o_tenmahang'), ('Ngày tạo', 'o_ngaytao')])

    # PHẦN 2 — Lập phiếu hủy = duyệt phiếu yêu cầu
    d.phan('LẬP PHIẾU HỦY HÀNG GIỮ (DUYỆT PHIẾU YÊU CẦU)')
    d.p('Cách 1: Lập từ màn Phiếu hủy hàng giữ:')
    d.step(d.vao)
    d.step(['Bước 2: Bấm ', '@btn_taomoi'])
    d.img('10_create_empty', 'Màn hình Lập phiếu hủy hàng giữ khi chưa chọn phiếu yêu cầu')
    d.step(['Bước 3: Bấm ', '@btn_tracuu', ' cạnh ô Phiếu yêu cầu hủy hàng giữ. Hệ thống mở cửa sổ “Phiếu yêu cầu hủy '
            'hàng giữ chờ duyệt”.'])
    d.img('11_request', 'Cửa sổ Phiếu yêu cầu hủy hàng giữ chờ duyệt')
    d.step(['Bước 4: Nhập Mã phiếu hoặc chọn Người tạo, bấm ', '@btn_timkiem', ' để tìm phiếu.'])
    d.step('Bước 5: Bấm vào dòng (hoặc Mã phiếu) cần duyệt để chọn.')
    d.sub(['Hoặc bấm ', '@btn_dong', ' để không chọn phiếu.'])
    d.p('Cách 2: Lập từ màn Yêu cầu hủy hàng giữ:')
    d.step(['Bước 1: Ở màn Yêu cầu hủy hàng giữ, bấm ', '@btn_duyet_row', ' ở cột Hành động của phiếu Chờ duyệt.'])
    d.sub(['Hoặc bấm vào Mã phiếu yêu cầu để mở màn chi tiết, chọn ', '@btn_taophieuhuy'])
    d.step('Bước 2: Màn lập phiếu mở ra với phiếu yêu cầu đã chọn sẵn.')
    d.p('Sau khi đã chọn phiếu yêu cầu (cả 2 cách):')
    d.step('Bước 1: Kiểm tra Người yêu cầu, Phòng ban yêu cầu, Khách hàng và các dòng hàng (hệ thống điền sẵn).')
    d.img('10_create', 'Màn hình Lập phiếu hủy hàng giữ sau khi đã chọn phiếu yêu cầu')
    d.step('Bước 2: Nhập thông tin:')
    d.sub('Duyệt hủy (bắt buộc với dòng đang tích Cần hủy): chỉ nhập số, lớn hơn 0, không vượt cột Có thể hủy. Điền sẵn '
          'bằng số Yêu cầu hủy.')
    d.sub('Cần hủy: bỏ tích ở dòng không đồng ý hủy.')
    d.sub('Ghi chú (tùy chọn): tối đa 255 ký tự.')
    d.step(['Bước 3: Bấm ', '@btn_duyet', '. Hệ thống hiện hộp xác nhận “Xác nhận duyệt”.'])
    d.img('14_confirm', 'Hộp xác nhận duyệt — lập phiếu hủy sẽ trừ hàng giữ ngay')
    d.step(['Bước 4: Bấm ', '@btn_confirm_duyet', ' để lập phiếu. Hàng giữ bị trừ, phiếu yêu cầu chuyển sang Đã duyệt.'])
    d.sub(['Hoặc bấm ', '@btn_huy_confirm', ' nếu bấm nhầm'])
    d.sub(['Hoặc bấm ', '@btn_duyettieptuc', ' (chỉ có ở Cách 1) để duyệt rồi lập tiếp phiếu khác.'])
    d.sub(['Hoặc bấm ', '@btn_quaylai', ' để không lập phiếu.'])

    # PHẦN 3 — Xem chi tiết
    d.phan('XEM CHI TIẾT PHIẾU')
    d.step(d.vao)
    d.step('Bước 2: Bấm vào Mã phiếu. Hệ thống mở màn “Chi tiết phiếu hủy hàng giữ”.')
    d.img('17_detail', 'Màn hình Chi tiết phiếu hủy hàng giữ')
    d.step(['Bước 3: Bấm ', '@btn_quaylai', ' để về màn danh sách.'])

    # PHẦN 4 — Lịch sử (biểu tượng Lịch sử hiện thẳng ở cột Hành động)
    d.phan('XEM LỊCH SỬ THAY ĐỔI')
    d.p('Cách 1: Xem lịch sử từ màn danh sách:')
    d.step(['Ở cột Hành động, bấm ', '@btn_lichsu_row'])
    d.p('Cách 2: Xem lịch sử từ màn chi tiết:')
    d.step('Bước 1: Bấm vào Mã phiếu để mở màn chi tiết')
    d.step(['Bước 2: Ở khối Lịch sử thay đổi, chọn nút ', '@btn_xemlichsu'])
    d.img('16_history', 'Cửa sổ Lịch sử phiếu hủy hàng giữ')
    d.step(['Bước 3: Bấm ', '@btn_dong_ls', ' để đóng cửa sổ.'])

    # PHẦN 5 — In phiếu
    d.phan('IN PHIẾU')
    d.step(['Bước 1: Ở cột Hành động, bấm ', '@btn_in_row'])
    d.sub(['Hoặc tại màn chi tiết phiếu, bấm ', '@btn_in'])
    d.step('Bước 2: Hệ thống mở cửa sổ xem trước bản in.')
    d.img('18_print', 'Cửa sổ Xem trước phiếu hủy hàng giữ')
    d.step(['Bước 3: Bấm ', '@btn_in_preview', ' để in.'])

    # PHẦN 6..8
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
