# -*- coding: utf-8 -*-
"""HDSD bản GỌN — Phiếu báo có + Tổng hợp tiền về ngân hàng (form chuẩn Danh mục quốc gia, 28/10/2026).

Chạy: python gen_hdsd.py  → out/HDSD_Phiếu báo có.docx (+ .pdf, out/render/ để soát)
Khuôn: finance-product-import-direct-transfer/form_qg/gen_hdsd.py (màn 27).
Phần dùng chung: ../../phieu-theo-form-quoc-gia/hdsd_phieu_lib.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'phieu-theo-form-quoc-gia'))
from hdsd_phieu_lib import PhieuHdsd, finalize_word, toc_lines, render_check  # noqa: E402

TEN = 'Phiếu báo có'
SHOTS = os.path.join(HERE, 'hdsd_shots')
OUT = os.path.join(HERE, 'out', 'HDSD_%s.docx' % TEN)

THUAT_NGU = [  # giữ theo bản Drive
    ['Phiếu báo có', 'Chứng từ ghi nhận tiền về tài khoản ngân hàng của công ty theo sao kê, gắn khoản tiền đó với '
                     'khách hàng / nhà cung cấp / hợp đồng.'],
    ['Đang tạo', 'Phiếu mới lập, còn là bản nháp. Người lập còn sửa và xóa được; chưa ghi vào sổ kế toán.'],
    ['Đã duyệt', 'Phiếu đã được duyệt, hệ thống đã ghi bút toán vào sổ kế toán. Phiếu không sửa, không xóa được nữa.'],
    ['Ghi bút toán vào sổ cái', 'Hệ thống tự sinh các dòng hạch toán Nợ / Có của phiếu vào sổ kế toán chung. Đây là '
                                'số liệu kế toán thật, không hoàn tác được.'],
    ['Loại thu', 'Ba loại: Thu bán hàng, Thu nhà cung cấp, Thu khác. Loại thu quyết định bảng Chi tiết có những cột '
                 'nào.'],
    ['KHÁCH KHÔNG RÕ', 'Khách hàng mặc định hệ thống điền sẵn khi chưa biết tiền của ai. Sau đó dùng màn Tổng hợp '
                       'tiền về ngân hàng để gán lại đúng khách.'],
    ['Không báo tiền về', 'Đánh dấu một dòng chi tiết là không cần đối chiếu công nợ. Dòng đã đánh dấu sẽ không xuất '
                          'hiện ở màn Tổng hợp tiền về ngân hàng.'],
    ['Số tiền chưa điều chỉnh', 'Phần tiền của một dòng chưa được xử lý bằng phiếu yêu cầu điều chỉnh công nợ.'],
    ['Hợp đồng nguyên tắc', 'Loại hợp đồng bán mà mỗi lần thu tiền phải gắn với một phiếu yêu cầu xuất hàng cụ thể, '
                            'hoặc phải đánh dấu là thu số dư nợ đầu kì.'],
    ['Phiếu YC xuất hàng', 'Phiếu yêu cầu xuất hàng.'],
]

PHIEN_BAN = [
    ['1.0', '05/09/2026', 'Ban hành lần đầu cho màn Phiếu báo có và màn Tổng hợp tiền về ngân hàng.'],
    ['1.1', '28/10/2026', 'Chuyển sang form chuẩn'],
]

QUYEN = [
    ['Xem danh sách, xem chi tiết, xem lịch sử',
     'Một trong các quyền: Xem tất cả phiếu báo có của tổng công ty / của công ty. Phiếu do chính mình lập luôn xem '
     'được.'],
    ['Tạo mới, Import Excel, Duyệt, Đánh dấu không báo tiền về', 'Quyền Quản lý phiếu báo có.'],
    ['Sửa, Xóa', 'Quyền Quản lý phiếu báo có, là người lập, phiếu đang ở trạng thái Đang tạo.'],
    ['Tổng hợp tiền về ngân hàng (xem, xuất Excel, tạo phiếu yêu cầu điều chỉnh công nợ)',
     'Không cần quyền riêng; chỉ thấy dữ liệu của công ty mình.'],
]

IMPORT_COLS = [
    ['Số tiền *', 'Bắt buộc. Số lớn hơn 0. Ví dụ: 1,000,000'],
    ['Diễn giải', 'Tùy chọn. Ví dụ: Cong ty A thanh toan HD 123'],
    ['Ngày hạch toán *', 'Bắt buộc. dd/mm/yyyy hoặc yyyy-mm-dd, ngày có thật. Ví dụ: 28/10/2026'],
    ['Mã ngân hàng *', 'Bắt buộc. Mã có trong danh mục Ngân hàng. Ví dụ: VIETINBANK'],
    ['Số tài khoản *', 'Bắt buộc. Số tài khoản ngân hàng của công ty. Ví dụ: 116000142872'],
    ['Tên chi nhánh *', 'Bắt buộc. Tên chi nhánh có trong danh mục. Ví dụ: CN Ha Noi'],
    ['Loại tiền *', 'Bắt buộc. Mã loại tiền trong danh mục. Ví dụ: VNĐ'],
    ['Tỷ giá', 'Tùy chọn. Số lớn hơn 0; bỏ trống thì lấy tỷ giá của loại tiền. Ví dụ: 1'],
]


def build():
    d = PhieuHdsd(TEN, SHOTS)
    d.tong_quan(THUAT_NGU, PHIEN_BAN, QUYEN, os.path.join(HERE, 'uml', 'overview_srs.png'))

    # PHẦN 1
    d.truy_cap(
        menu=[('Tài chính', 'menu_phanhe'), ('Quản lý tiền', 'menu_nhom'),
              ('Thanh toán tiền mặt', 'menu_thanhtoan'), ('Phiếu báo có', 'menu_muc')],
        o_nhanh='mã phiếu',
        bo_loc=[('Công ty – Phòng ban – Bộ phận', 'o_congty'), ('Loại thu', 'o_loaithu'),
                ('Trạng thái', 'o_trangthai'), ('Người tạo', 'o_nguoitao'), ('Ngân hàng', 'o_nganhang'),
                ('Tài khoản ngân hàng', 'o_taikhoan'), ('Khách hàng', 'o_khachhang'),
                ('Tên khách hàng (gõ tay)', 'o_tenkhach'), ('Ghi chú', 'o_ghichu'),
                ('Không báo tiền về', 'o_khongbao'), ('Ngày hạch toán', 'o_ngayhachtoan'), ('Ngày tạo', 'o_ngaytao')])

    # PHẦN 2 — Tạo mới
    d.phan('TẠO MỚI PHIẾU BÁO CÓ')
    d.step(d.vao)
    d.step(['Bước 2: Bấm ', '@btn_taomoi'])
    d.img('10_create', 'Màn hình Thêm phiếu báo có')
    d.step('Bước 3: Nhập khối Thông tin chung:')
    d.sub('Loại thu (bắt buộc): Thu bán hàng (mặc định), Thu nhà cung cấp hoặc Thu khác.')
    d.sub('Tài khoản nợ (bắt buộc): mặc định 1121 - Tiền Việt Nam.')
    d.sub('Loại tiền (bắt buộc): mặc định VNĐ. Chọn ngoại tệ thì nhập Tỷ giá (bắt buộc, số lớn hơn 0).')
    d.sub('Ngày hạch toán (bắt buộc): dd/mm/yyyy, mặc định ngày hiện tại.')
    d.sub('Ngân hàng (bắt buộc), rồi Tài khoản (bắt buộc). Chi nhánh tự điền.')
    d.sub('Diễn giải (tùy chọn): tối đa 500 ký tự.')
    d.step(['Bước 4: Ở khối Chi tiết, nhập từng dòng tiền về (bấm ', '@btn_themdong', ' để thêm dòng):'])
    d.sub('Số tài khoản có (bắt buộc): mặc định 1311 với Thu bán hàng, 3311 với Thu nhà cung cấp.')
    d.sub('Khách hàng: bấm vào ô để mở cửa sổ “Chọn khách hàng”; bắt buộc với Thu bán hàng, tùy chọn với Thu khác. '
          'Mặc định KHÁCH KHÔNG RÕ.')
    d.sub('Số đơn hàng/Hợp đồng: bấm vào ô để chọn; bắt buộc khi đã chọn khách cụ thể và tài khoản có là công nợ.')
    d.sub('Phiếu YC xuất hàng: bắt buộc khi hợp đồng là hợp đồng nguyên tắc, trừ khi tích Số dư nợ đầu kì.')
    d.sub('Thu nhà cung cấp: Nhà cung cấp (bắt buộc), Phiếu xuất hàng (tùy chọn).')
    d.sub('Số tiền (bắt buộc): lớn hơn 0. Diễn giải (bắt buộc): tối đa 500 ký tự.')
    d.sub('Không báo tiền về (tùy chọn): tích nếu dòng không cần đối chiếu công nợ.')
    d.sub(['Hoặc bấm ', '@btn_xoadong', ' để bỏ dòng.'])
    d.img('11_customer', 'Cửa sổ Chọn khách hàng')
    d.step(['Bước 5: Trong cửa sổ, nhập Tên / Mã khách hàng, Mã số thuế hoặc Số điện thoại, bấm ', '@btn_timkiem',
            ', rồi bấm vào dòng khách hàng cần chọn.'])
    d.step(['Bước 6: Bấm ', '@btn_luu', ' để lưu nháp (trạng thái Đang tạo).'])
    d.sub(['Hoặc ', '@btn_luuduyet', ', chọn ', '@btn_confirm_xacnhan',
           ' để lưu và duyệt ngay (ghi bút toán vào sổ cái, sau đó không sửa, không xóa được).'])
    d.sub(['Hoặc ', '@btn_luutieptuc', ' để lưu nháp rồi lập tiếp phiếu khác.'])
    d.sub(['Hoặc ', '@btn_quaylai', ' để không lưu thông tin.'])

    # PHẦN 3 — Chỉnh sửa
    d.phan('CHỈNH SỬA')
    d.step(d.vao)
    d.step(['Bước 2: Bấm nút ', '@btn_sua_row', ' ở cột Hành động của phiếu Đang tạo do mình lập.'])
    d.sub(['Hoặc bấm vào Mã phiếu để mở màn chi tiết, chọn ', '@btn_sua'])
    d.img('12_edit', 'Màn hình Sửa phiếu báo có')
    d.step('Bước 3: Nhập thông tin cần sửa (quy tắc nhập như Tạo mới ở PHẦN 2). Mã phiếu, Người lập, Phòng ban '
           'không sửa được.')
    d.step(['Bước 4: Bấm ', '@btn_luu', ' để lưu,'])
    d.sub(['Hoặc ', '@btn_luuduyet', ' để lưu và duyệt ngay.'])
    d.sub(['Hoặc ', '@btn_quaylai', ' nếu muốn hủy.'])

    # PHẦN 4 — Xóa
    d.xoa('Xác nhận xóa', them_cach=['Hoặc bấm vào Mã phiếu để mở màn chi tiết, chọn ', '@btn_xoa'])

    # PHẦN 5 — Duyệt
    d.phan('DUYỆT PHIẾU')
    d.step(['Bước 1: Ở dòng phiếu Đang tạo, bấm ', '@btn_bacham_row', ' rồi chọn ', '@item_duyet'])
    d.sub(['Hoặc bấm vào Mã phiếu để mở màn chi tiết, chọn ', '@btn_duyet'])
    d.step('Bước 2: Hệ thống hiện hộp xác nhận “Xác nhận duyệt”.')
    d.img('14_approve', 'Hộp xác nhận duyệt phiếu báo có')
    d.step(['Bước 3: Bấm ', '@btn_confirm_duyet', ' để duyệt phiếu và ghi bút toán vào sổ cái.'])
    d.sub(['Hoặc bấm ', '@btn_huy_confirm', ' nếu bấm nhầm'])

    # PHẦN 6 — Xem chi tiết
    d.phan('XEM CHI TIẾT PHIẾU')
    d.step(d.vao)
    d.step('Bước 2: Bấm vào Mã phiếu. Hệ thống mở màn “Chi tiết phiếu báo có”.')
    d.img('17_detail', 'Màn hình Chi tiết phiếu báo có')
    d.step(['Bước 3: Bấm ', '@btn_quaylai', ' để về màn danh sách.'])

    # PHẦN 7 — Không báo tiền về
    d.phan('ĐÁNH DẤU KHÔNG BÁO TIỀN VỀ')
    d.step('Bước 1: Mở màn chi tiết phiếu (phiếu Thu bán hàng hoặc Thu khác).')
    d.step(['Bước 2: Ở khối “Đánh dấu không báo tiền về”, tích ', '@o_tick', ' ở dòng cần đánh dấu.'])
    d.img('18_notreport', 'Khối Đánh dấu không báo tiền về')
    d.step('Bước 3: Hệ thống lưu ngay và báo “Cập nhật thành công.”')
    d.sub('Hoặc bỏ tích để bỏ đánh dấu.')

    # PHẦN 8 — Lịch sử
    d.lich_su('Mã phiếu', img='16_history', cap='Cửa sổ Lịch sử thay đổi của phiếu', bo_loc=False)

    # PHẦN 9 — Import
    d.phan('IMPORT EXCEL SAO KÊ NGÂN HÀNG')
    d.step(['Bước 1: Ở màn danh sách, bấm ', '@btn_import'])
    d.img('30b_import_open', 'Cửa sổ Import phiếu báo có lúc vừa mở')
    d.step(['Bước 2: Bấm ', '@btn_taifilemau', ', điền file theo các cột:'])
    d.w.table([['Tên cột', 'Cách nhập']] + IMPORT_COLS, widths=[1.8, 4.7])
    d.step(['Bước 3: Bấm ', '@btn_chonfile', ' chọn file đã điền, rồi bấm ', '@btn_loadbang'])
    d.img('31_import_loaded', 'Dữ liệu sau khi Load lên bảng')
    d.step(['Bước 4: Bấm ', '@btn_validate', '. Hệ thống hiện số dòng Tổng / Hợp lệ / Lỗi và lý do lỗi dưới từng '
            'dòng.'])
    d.img('32_import_validated', 'Kết quả sau khi Validate')
    d.step('Bước 5: Sửa dòng lỗi ngay trên bảng rồi bấm Validate lại,')
    d.sub(['Hoặc bấm ', '@btn_bodongloi', ' để bỏ các dòng lỗi.'])
    d.step(['Bước 6: Khi Lỗi = 0, bấm ', '@btn_import_do',
            '. Mỗi dòng tạo một phiếu Đã duyệt và ghi sổ cái ngay; hệ thống không kiểm tra trùng.'])
    d.sub(['Hoặc bấm ', '@btn_dong_import', ' để không import.'])
    d.step('Bước 7: Hệ thống báo “Import thành công …”, phiếu mới hiện đầu danh sách với trạng thái Đã duyệt.')

    # PHẦN 10 — Tổng hợp tiền về ngân hàng
    d.phan('TỔNG HỢP TIỀN VỀ NGÂN HÀNG')
    d.step(['Bước 1: Từ phân hệ Tài chính ', '@menu_phanhe', ', tại menu Quản lý tiền ', '@menu_nhom',
            ', nhóm Thanh toán tiền mặt ', '@menu_thanhtoan', ', chọn Tổng hợp tiền về ngân hàng ', '@menu_tonghop'])
    d.img('40_summary', 'Màn hình Tổng hợp tiền về ngân hàng')
    d.step(['Bước 2: Nhập số báo có vào ô tìm kiếm nhanh ', '@o_timnhanh_sum', ', nhấn ', '@btn_timkiem'])
    d.step(['Bước 3: Bấm ', '@btn_timkiemnangcao', ' để lọc theo Khách hàng, Diễn giải, Ngân hàng, STK ngân hàng, '
            'Người tạo, Trạng thái, Số tiền, Ngày hạch toán.'])
    d.step(['Bước 4: Chọn ', '@btn_lammoi', ' để xóa giá trị đã lọc'])

    # PHẦN 11 — Tạo phiếu yêu cầu điều chỉnh công nợ
    d.phan('TẠO PHIẾU YÊU CẦU ĐIỀU CHỈNH CÔNG NỢ')
    d.step(['Bước 1: Ở màn Tổng hợp tiền về ngân hàng, tích ', '@o_tick',
            ' ở cột Điều chỉnh công nợ của các dòng cần điều chỉnh (các dòng phải cùng một phiếu báo có).'])
    d.img('40b_summary_right', 'Cột Điều chỉnh công nợ trên màn Tổng hợp')
    d.step(['Bước 2: Bấm ', '@btn_taomoidc'])
    d.sub(['Hoặc tại màn chi tiết phiếu báo có, bấm ', '@btn_taophieudc'])
    d.step('Bước 3: Hệ thống mở màn tạo Phiếu yêu cầu điều chỉnh công nợ với các dòng đã chọn; nhập tiếp theo màn đó.')

    # PHẦN 12 — Xuất Excel
    d.phan('XUẤT EXCEL TỔNG HỢP TIỀN VỀ NGÂN HÀNG')
    d.step('Bước 1: Lọc danh sách Tổng hợp tiền về ngân hàng theo đúng dữ liệu cần lấy (xem PHẦN 10).')
    d.step(['Bước 2: Bấm nút ', '@btn_xuatexcel', '. Hệ thống mở cửa sổ “Chọn trường xuất file”.'])
    d.img('42_export', 'Cửa sổ Chọn trường xuất file')
    d.step('Bước 3: Tích chọn, kéo biểu tượng ☰ để đổi vị trí các trường cần xuất.')
    d.sub(['Hoặc bấm ', '@btn_chontatca_x', ' để tích tất cả các trường'])
    d.sub(['Hoặc bấm ', '@btn_bochonhet_x', ' để bỏ tích tất cả các trường'])
    d.step(['Bước 4: Bấm ', '@btn_xuatfile'])
    d.sub(['Hoặc bấm ', '@btn_dong_export', ' để không xuất'])
    d.step('Bước 5: Mở file Excel đã xuất.')

    # PHẦN 13..14
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
