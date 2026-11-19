# -*- coding: utf-8 -*-
"""HDSD bản GỌN — Phiếu yêu cầu chuyển hàng (STT 26, form chuẩn Danh mục quốc gia, 28/10/2026).

Chạy: python gen_hdsd.py  → out/HDSD_Phiếu yêu cầu chuyển hàng.docx (+ .pdf, render/ để soát)
Ảnh: capture.js (DEV) → hdsd_shots/. Phần dùng chung: ../../phieu-theo-form-quoc-gia/hdsd_phieu_lib.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'phieu-theo-form-quoc-gia'))
from hdsd_phieu_lib import PhieuHdsd, finalize_word, toc_lines, render_check  # noqa: E402

TEN = 'Phiếu yêu cầu chuyển hàng'
SHOTS = os.path.join(HERE, 'hdsd_shots')
OUT = os.path.join(HERE, 'out', 'HDSD_%s.docx' % TEN)

THUAT_NGU = [
    ['Phiếu yêu cầu chuyển hàng', 'Chứng từ do người kinh doanh lập để đề nghị bộ phận kho chuyển hàng về phục vụ '
                                  'khách hàng. Mã phiếu tự sinh dạng PYCCH kèm 5 chữ số.'],
    ['Dòng hàng hoá', 'Một dòng trong bảng Danh sách hàng hóa, ứng với một mã hàng. Mỗi mã hàng chỉ có một dòng.'],
    ['Dòng khách hàng', 'Dòng con trong cột Khách hàng của một dòng hàng hoá: khách hàng, số lượng, ngày cần, ghi '
                        'chú. Mỗi dòng hàng hoá có ít nhất một dòng khách hàng.'],
    ['ĐVT', 'Đơn vị tính của hàng hoá. Đơn vị có hệ số quy đổi khác 1 hiển thị kèm hệ số, ví dụ “Thùng (x10)”.'],
    ['Giá niêm yết / SL tồn', 'Thông tin tham khảo theo đơn vị tính và kho đang chọn; không lưu vào phiếu, không chặn '
                              'khi số lượng vượt tồn.'],
    ['Người tiếp nhận', 'Người của bộ phận kho đã xử lý phiếu (Không duyệt hoặc tiếp nhận).'],
    ['Trạng thái Đang tạo', 'Phiếu lưu nháp. Chỉ người lập thấy, sửa, xóa được.'],
    ['Trạng thái Chờ duyệt', 'Phiếu đã gửi, chờ Kế toán kho xử lý (Không duyệt hoặc Tổng hợp).'],
    ['Trạng thái Đã tiếp nhận … Đã phân bổ', 'Các bước do chuỗi nghiệp vụ kho cập nhật; màn này chỉ hiển thị.'],
    ['Không duyệt', 'Kế toán kho trả phiếu Chờ duyệt về Đang tạo kèm Ghi chú duyệt để người lập sửa và gửi lại. '
                    'Không phải hủy phiếu.'],
    ['Tổng hợp', 'Chuyển sang màn Tạo yêu cầu xuất hàng, nạp sẵn phiếu đang xem. Không đổi trạng thái phiếu.'],
]

PHIEN_BAN = [
    ['1.0', '03/09/2026', 'Ban hành lần đầu cho màn Phiếu yêu cầu chuyển hàng (phân hệ Tài chính, nhóm Hàng hoá - '
                          'Dịch vụ - Vận chuyển).'],
    ['1.1', '28/10/2026', 'Chuyển sang form chuẩn'],
]

QUYEN = [
    ['Xem danh sách, xuất Excel', 'Một trong các quyền Xem yêu cầu chuyển hàng theo tổng công ty / theo công ty / theo '
                                  'phòng ban / theo bộ phận. Không có quyền nào thì chỉ thấy phiếu do mình lập.'],
    ['Lập phiếu', 'Không cần quyền riêng.'],
    ['Sửa, xóa phiếu', 'Người lập phiếu, phiếu đang ở trạng thái Đang tạo.'],
    ['Xem chi tiết, in, xem lịch sử', 'Người lập phiếu; hoặc quyền Kế toán kho cùng công ty với phiếu.'],
    ['Không duyệt, Tổng hợp', 'Quyền Kế toán kho, cùng công ty với phiếu, phiếu đang ở trạng thái Chờ duyệt.'],
]


def build():
    d = PhieuHdsd(TEN, SHOTS)
    d.tong_quan(THUAT_NGU, PHIEN_BAN, QUYEN, os.path.join(HERE, 'uml', 'overview_srs.png'))

    # PHẦN 1
    d.truy_cap(
        menu=[('Tài chính', 'menu_phanhe'), ('Hàng hoá - Dịch vụ - Vận chuyển', 'menu_nhom'),
              ('Xuất hàng', 'menu_xuathang'), ('Phiếu yêu cầu chuyển hàng', 'menu_muc')],
        o_nhanh='mã yêu cầu hoặc tên người tạo',
        bo_loc=[('Trạng thái', 'o_trangthai'), ('Tên/mã hàng hóa', 'o_tenmahang'), ('Người tạo', 'o_nguoitao'),
                ('Người tiếp nhận', 'o_nguoitiepnhan'), ('Ngày tạo', 'o_ngaytao')])
    d.p('Hoặc vào từ phân hệ Bán hàng: nhóm Yêu cầu, mục Hàng hóa, chọn YC chuyển hàng.')

    # PHẦN 2 — Tạo mới
    d.phan('TẠO MỚI PHIẾU YÊU CẦU CHUYỂN HÀNG')
    d.step(d.vao)
    d.step(['Bước 2: Bấm ', '@btn_taomoi'])
    d.step('Bước 3: Nhập Ghi chú (tùy chọn, tối đa 255 ký tự). Ngày tạo, Người tạo tự điền, không sửa được.')
    d.step('Bước 4: Chọn kho ở ô “Xem tồn theo kho” (tùy chọn) để xem cột SL tồn.')
    d.step(['Bước 5: Bấm ', '@btn_themhanghoa', ' ở tiêu đề bảng Danh sách hàng hóa. Hệ thống mở cửa sổ “Thêm hàng hoá”.'])
    d.img('11_product', 'Cửa sổ Thêm hàng hoá')
    d.step(['Bước 6: Tích chọn các hàng cần thêm, bấm ', '@btn_themsp', ' rồi bấm ', '@btn_dong_sp'])
    d.step('Bước 7: Chọn ĐVT của từng dòng hàng (bắt buộc).')
    d.step(['Bước 8: Bấm ô ', '@o_khachhang', ' để chọn khách hàng (bắt buộc). Hệ thống mở cửa sổ “Chọn khách hàng”.'])
    d.img('11b_customer', 'Cửa sổ Chọn khách hàng')
    d.step('Bước 9: Tìm theo Tên / Mã khách hàng, Mã số thuế hoặc Số điện thoại, bấm vào dòng khách hàng cần chọn.')
    d.step('Bước 10: Nhập thông tin dòng khách hàng (bắt buộc):')
    d.sub('Số lượng: số nguyên từ 1 đến 999,999,999.')
    d.sub('Ngày cần: ngày sau hôm nay (dd/mm/yyyy).')
    d.sub('Ghi chú: tối đa 255 ký tự.')
    d.sub(['Bấm ', '@btn_themkhachhang', ' để thêm khách hàng khác cho cùng hàng hóa; bấm ', '@btn_xoadong',
           ' để xóa dòng khách hàng.'])
    d.sub(['Bấm ', '@btn_xoahang', ' để xóa cả dòng hàng hóa.'])
    d.step(['Bước 11: Ở khối File đính kèm, bấm ', '@btn_themtailieu',
            ' và chọn tệp PDF (bắt buộc ít nhất 1 tệp, tối đa 20 MB mỗi tệp).'])
    d.img('10_create', 'Màn hình Thêm phiếu yêu cầu chuyển hàng')
    d.step(['Bước 12: Bấm ', '@btn_luuguiduyet', ', chọn ', '@btn_confirm_xacnhan', ' để gửi Kế toán kho xử lý,'])
    d.sub(['Hoặc ', '@btn_luunhap', ' để lưu nháp (trạng thái Đang tạo).'])
    d.sub(['Hoặc ', '@btn_luutieptuc', ' để lưu nháp rồi lập tiếp phiếu khác.'])
    d.sub(['Hoặc ', '@btn_quaylai', ' để không lưu thông tin.'])

    # PHẦN 3 — Chỉnh sửa
    d.phan('CHỈNH SỬA')
    d.step(d.vao)
    d.step(['Bước 2: Bấm nút ', '@btn_sua_row', ' ở cột Hành động của phiếu Đang tạo do mình lập.'])
    d.sub(['Hoặc bấm vào Mã yêu cầu để mở màn chi tiết, chọn ', '@btn_sua'])
    d.step('Bước 3: Hệ thống hiển thị màn hình “Sửa phiếu yêu cầu chuyển hàng”.')
    d.img('12_edit', 'Màn hình Sửa phiếu yêu cầu chuyển hàng')
    d.step('Bước 4: Nhập thông tin cần sửa (quy tắc nhập như Tạo mới ở PHẦN 2; tệp đính kèm không bắt buộc thêm).')
    d.step(['Bước 5: Bấm ', '@btn_luuguiduyet', ' để lưu và gửi duyệt,'])
    d.sub(['Hoặc ', '@btn_luunhap', ' để lưu nháp.'])
    d.sub(['Hoặc ', '@btn_quaylai', ' nếu muốn hủy.'])

    # PHẦN 4 — Xóa
    d.xoa('Xác nhận xóa')

    # PHẦN 5 — Không duyệt
    d.phan('KHÔNG DUYỆT PHIẾU')
    d.step('Bước 1: Bấm vào Mã yêu cầu của phiếu Chờ duyệt để mở màn chi tiết.')
    d.step('Bước 2: Kiểm tra các dòng hàng hóa và khách hàng.')
    d.step(['Bước 3: Bấm ', '@btn_khongduyet', '. Hệ thống hiện hộp “Xác nhận không duyệt”.'])
    d.img('15_reject', 'Hộp xác nhận không duyệt')
    d.step('Bước 4: Nhập Ghi chú duyệt (bắt buộc).')
    d.step(['Bước 5: Bấm ', '@btn_confirm_khongduyet', ' để xác nhận, phiếu về trạng thái Đang tạo'])
    d.sub(['Hoặc bấm ', '@btn_huy_confirm', ' nếu bấm nhầm'])

    # PHẦN 6 — Tổng hợp
    d.phan('TỔNG HỢP SANG YÊU CẦU XUẤT HÀNG')
    d.step(['Bước 1: Bấm ', '@btn_tonghop_row', ' ở cột Hành động của phiếu Chờ duyệt'])
    d.sub(['Hoặc tại màn chi tiết phiếu, bấm ', '@btn_tonghop'])
    d.step('Bước 2: Hệ thống mở màn “Tạo yêu cầu xuất hàng”, chọn sẵn loại Xuất điều chuyển kho chi nhánh và nạp sẵn '
           'phiếu đang xem.')
    d.img('19_summary', 'Màn hình Tạo yêu cầu xuất hàng mở từ nút Tổng hợp')
    d.step('Bước 3: Nhập tiếp thông tin và lưu yêu cầu xuất hàng tại màn này.')

    # PHẦN 7 — Lịch sử
    d.lich_su('Mã yêu cầu', xem_o_chi_tiet='@khoi_lichsu', img='16_history', cap='Cửa sổ Lịch sử thay đổi của phiếu')

    # PHẦN 8 — Xem chi tiết
    d.phan('XEM CHI TIẾT PHIẾU')
    d.step(d.vao)
    d.step('Bước 2: Bấm vào Mã yêu cầu. Hệ thống mở màn “Chi tiết phiếu yêu cầu chuyển hàng”.')
    d.img('17_detail', 'Màn hình Chi tiết phiếu yêu cầu chuyển hàng')
    d.step(['Bước 3: Bấm ', '@btn_quaylai', ' để về màn danh sách.'])

    # PHẦN 9 — In
    d.phan('IN PHIẾU')
    d.step(['Bước 1: Ở cột Hành động, bấm ', '@btn_in_row'])
    d.sub(['Hoặc bấm ', '@btn_bacham_row', ' rồi chọn ', '@item_in'])
    d.sub(['Hoặc tại màn chi tiết phiếu, bấm ', '@btn_in'])
    d.step('Bước 2: Hệ thống mở cửa sổ xem trước bản in.')
    d.img('18_print', 'Cửa sổ Xem trước phiếu yêu cầu chuyển hàng')
    d.step(['Bước 3: Bấm ', '@btn_in_preview', ' để in.'])

    # PHẦN 10..12
    d.xuat_excel(cua_so='Chọn trường xuất file')
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
