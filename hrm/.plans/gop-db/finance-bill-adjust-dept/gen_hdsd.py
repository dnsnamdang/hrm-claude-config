# -*- coding: utf-8 -*-
"""HDSD bản GỌN — Phiếu kế toán (form chuẩn Danh mục quốc gia, 04/11/2026).

Chạy: python gen_hdsd.py  → HDSD_Phieu ke toan.docx (PDF + ảnh soát ghi vào thư mục tạm)
Phần chung: ../phieu-theo-form-quoc-gia/hdsd_phieu_lib.py. Sơ đồ tổng quan dùng lại ảnh gen_srs.py sinh ra (pkt_shots/uml/overview.png).
Khuôn cấu trúc: ../buy-service-accounting/gen_hdsd.py. Ảnh + icon: pkt_shots (dev-hrm 04/11/2026, script pkt_shots/_capture/capture.js).
"""
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'phieu-theo-form-quoc-gia'))
from hdsd_phieu_lib import PhieuHdsd, finalize_word, toc_lines, render_check  # noqa: E402

TEN = 'Phiếu kế toán'
SHOTS = os.path.join(HERE, 'pkt_shots')
OUT = os.path.join(HERE, 'HDSD_Phieu ke toan.docx')
CHECK_DIR = os.path.join(tempfile.gettempdir(), 'hdsd_pkt')

THUAT_NGU = [
    ['Phiếu kế toán', 'Chứng từ ghi bút toán Nợ / Có vào sổ cái, mã phiếu dạng TPE.PKT1126.00001.'],
    ['Phiếu nguồn', 'Phiếu yêu cầu điều chỉnh công nợ, Phiếu yêu cầu hạch toán bổ sung hoặc các dòng chi phí vận chuyển nhanh mà '
                    'phiếu kế toán được lập từ đó.'],
    ['Dòng định khoản', 'Một dòng của bảng Chi tiết: Số tài khoản, khách hàng, Phát sinh nợ hoặc Phát sinh có, Diễn giải, hợp đồng…'],
    ['Nhóm định khoản', 'Số gom các dòng thành 1 bút toán; trong 1 nhóm Tổng Nợ phải bằng Tổng Có.'],
    ['Đang tạo', 'Phiếu lưu nháp, chưa ghi sổ; người tạo sửa / xóa / duyệt được.'],
    ['Đã duyệt', 'Phiếu đã Lưu và duyệt: ghi bút toán vào sổ cái; không sửa, không xóa được.'],
]
PHIEN_BAN = [['1.0', '04/11/2026', 'Tạo mới tài liệu theo form chuẩn']]
QUYEN = [
    ['Xem danh sách, xem chi tiết, in, xuất Excel, xem lịch sử',
     'Phiếu do mình tạo luôn xem được. Xem rộng hơn cần quyền Xem tất cả phiếu kế toán của tổng công ty hoặc Xem tất cả phiếu kế '
     'toán của công ty.'],
    ['Lập phiếu, Lưu và duyệt', 'Quyền Kế toán thanh toán.'],
    ['Sửa, xóa', 'Quyền Kế toán thanh toán, là người tạo phiếu; phiếu Đang tạo.'],
]


def build():
    d = PhieuHdsd(TEN, SHOTS)
    d.tong_quan(THUAT_NGU, PHIEN_BAN, QUYEN, os.path.join(SHOTS, 'uml', 'overview.png'))

    d.phan('TRUY CẬP VÀ TÌM KIẾM')
    d.step(['Bước 1: Từ phân hệ Tài chính ', '@menu_phanhe', ', tại menu Sổ tổng hợp ', '@menu_sotonghop', ', nhóm Sổ tổng hợp ',
            '@menu_nhom_sotonghop', ', chọn Phiếu kế toán ', '@menu_muc'])
    d.img('01_list', 'Màn hình Phiếu kế toán')
    d.step(['Bước 2: Nhập mã phiếu vào ô tìm kiếm nhanh ', '@o_timnhanh'])
    d.step(['Bước 3: Nhấn ', '@btn_timkiem'])
    d.step(['Bước 4: Bấm ', '@btn_timkiemnangcao', ', chọn giá trị trong ', '@o_trangthai', ' để lọc theo Trạng thái'])
    for lb, ic in [('Công ty', 'o_congty'), ('Phòng ban', 'o_phongban'), ('Người tạo', 'o_nguoitao'), ('Khách hàng', 'o_khachhang'),
                   ('NVKD', 'o_nvkd'), ('Ngày tạo', 'o_ngaytao')]:
        d.sub(['Hoặc chọn giá trị ', '@' + ic, ' để lọc theo %s' % lb])
    d.sub(['Hoặc gõ vào ', '@o_maycdc', ' / ', '@o_taikhoan', ' / ', '@o_hopdong', ' / ', '@o_nganhang', ' / ', '@o_stk',
           ' rồi nhấn Tìm kiếm để lọc theo Mã phiếu YCĐC / Tài khoản / Đơn hàng, Hợp đồng / Ngân hàng / STK ngân hàng'])
    d.sub(['Hoặc nhập khoảng ', '@o_sotien', ' rồi nhấn Tìm kiếm để lọc theo Tổng phát sinh'])
    d.step(['Bước 5: Chọn ', '@btn_lammoi', ' để xóa giá trị đã lọc'])

    d.phan('LẬP PHIẾU KẾ TOÁN')
    d.p('Cách 1: Nhập tay từ màn Phiếu kế toán:')
    d.step('Bước 1: Truy cập vào màn hình Phiếu kế toán (PHẦN 1).')
    d.step(['Bước 2: Bấm ', '@btn_taomoi', ' (chỉ hiện với người có quyền Kế toán thanh toán)'])
    d.img('10_create', 'Màn hình Tạo phiếu kế toán')
    d.step(['Bước 3: (Không bắt buộc) bấm ô Phiếu yêu cầu điều chỉnh công nợ ', '@o_phieuycdc', ', bấm vào dòng phiếu cần lập (xem '
            'PHẦN 3). Hệ thống điền sẵn Diễn giải, Ngày hạch toán, Loại tiền, bảng Chi tiết.'])
    d.step(['Bước 4: Chọn Ngày hạch toán ', '@o_ngayht', ' (bắt buộc, mặc định hôm nay), Loại tiền ', '@o_loaitien',
            ' (mặc định VNĐ), Tỷ giá ', '@o_tygia', ' (ngoại tệ); nhập Diễn giải ', '@o_diengiai',
            '. Loại tiền, Tỷ giá, Diễn giải bắt buộc khi Lưu và duyệt.'])
    d.step(['Bước 5: Bấm ', '@btn_themtailieu', ' để đính kèm file (không bắt buộc, mỗi file tối đa 20MB).'])
    d.step(['Bước 6: Bấm ', '@btn_themdong', ', chọn Số tài khoản; bấm ô Mã khách ', '@o_makhach', ' để chọn đối tượng, ô Đơn '
            'hàng/Hợp đồng ', '@o_hopdong_row', ' để chọn hợp đồng (xem PHẦN 3); nhập Phát sinh nợ hoặc Phát sinh có, Diễn giải; chọn '
            'Mã phí, Mã vụ việc, Ngân hàng, STK ngân hàng, Nhóm định khoản nếu cần.'])
    d.step(['Bước 7: Bấm ', '@btn_luunhap', ' để lưu nháp (chỉ cần Ngày hạch toán)'])
    d.sub(['Hoặc ', '@btn_luutieptuc', ' để lưu nháp rồi lập tiếp phiếu khác.'])
    d.sub(['Hoặc ', '@btn_luuduyet', ' để ghi sổ (xem PHẦN 4).'])
    d.sub(['Hoặc ', '@btn_quaylai_form', ' để không lưu, chọn ', '@btn_thoat', ' để rời màn hoặc ', '@btn_olai', ' để ở lại.'])
    d.p('Cách 2: Từ phiếu nguồn:')
    d.step(['Bước 1: Ở màn Phiếu yêu cầu điều chỉnh công nợ, dòng phiếu Chờ tạo phiếu kế toán, bấm ', '@btn_taopkt_ycdc'])
    d.sub(['Hoặc ở màn Phiếu yêu cầu hạch toán bổ sung, dòng phiếu Chờ duyệt, bấm ', '@btn_lappkt_htbs'])
    d.step('Bước 2: Hệ thống mở màn Tạo phiếu kế toán với phiếu nguồn và bảng Chi tiết điền sẵn.')
    d.img('21_from_request', 'Màn Tạo phiếu kế toán mở từ Phiếu yêu cầu điều chỉnh công nợ')
    d.step('Bước 3: Kiểm tra, bổ sung thông tin (như Cách 1, Bước 4–6) rồi lưu như Bước 7.')

    d.phan('CHỌN PHIẾU YÊU CẦU, ĐỐI TƯỢNG VÀ HỢP ĐỒNG')
    d.p('Cách 1: Chọn phiếu yêu cầu điều chỉnh công nợ:')
    d.step(['Bước 1: Ở màn Tạo phiếu, bấm ô ', '@o_phieuycdc'])
    d.img('11_request_picker', 'Cửa sổ Chọn phiếu yêu cầu điều chỉnh công nợ')
    d.step(['Bước 2: Nhập Mã phiếu yêu cầu hoặc chọn Người tạo, bấm ', '@btn_timkiem_popup', ' (bấm ', '@btn_lammoi_popup',
            ' để xóa điều kiện)'])
    d.step('Bước 3: Bấm vào dòng phiếu cần chọn. Hệ thống báo “Thêm phiếu thành công”.')
    d.sub(['Hoặc bấm ', '@btn_dong_popup', ' để đóng cửa sổ.'])
    d.p('Cách 2: Chọn đối tượng và hợp đồng cho dòng định khoản:')
    d.step(['Bước 1: Bấm ô Mã khách ', '@o_makhach', ' của dòng, lọc theo Mã, Tên, Loại rồi bấm dòng đối tượng.'])
    d.img('12_object_picker', 'Cửa sổ Chọn đối tượng')
    d.step(['Bước 2: Bấm ô Đơn hàng/Hợp đồng ', '@o_hopdong_row', ', bấm dòng hợp đồng cần chọn.'])
    d.sub(['Hoặc bấm ', '@btn_dong_obj', ' để đóng cửa sổ.'])

    d.phan('LƯU VÀ DUYỆT (GHI SỔ CÁI)')
    d.step('Bước 1: Ở màn Tạo hoặc màn Sửa phiếu Đang tạo, nhập đủ thông tin (PHẦN 2).')
    d.step(['Bước 2: Bấm ', '@btn_luuduyet', '. Hệ thống hiện hộp “Xác nhận duyệt phiếu kế toán”.'])
    d.img('14_approve_confirm', 'Hộp Xác nhận duyệt phiếu kế toán')
    d.step(['Bước 3: Bấm ', '@btn_duyet_confirm', ' để ghi sổ. Thiếu thông tin thì hệ thống báo đỏ dưới ô; nhóm định khoản lệch Nợ / Có '
            'thì báo lỗi.'])
    d.sub(['Hoặc bấm ', '@btn_huy_duyet', ' để quay lại form.'])
    d.step('Bước 4: Nếu hiện khối “Hợp đồng có số dư lẻ”: tích hợp đồng cần điều chỉnh, bấm “Áp dụng vào bảng định khoản”, rồi bấm lại '
           'Lưu và duyệt.')

    d.phan('CHỈNH SỬA')
    d.step('Bước 1: Truy cập vào màn hình Phiếu kế toán.')
    d.step(['Bước 2: Bấm ', '@btn_sua_row', ' ở cột Hành động của phiếu Đang tạo do mình tạo.'])
    d.sub(['Hoặc bấm vào Mã phiếu ', '@link_sophieu', ' để mở màn chi tiết, chọn ', '@btn_sua'])
    d.step('Bước 3: Hệ thống hiển thị màn hình “Sửa phiếu kế toán: <mã phiếu>”.')
    d.img('19_edit', 'Màn hình Sửa phiếu kế toán')
    d.step('Bước 4: Nhập thông tin cần sửa (quy tắc như PHẦN 2).')
    d.step(['Bước 5: Bấm ', '@btn_luunhap', ' để lưu'])
    d.sub(['Hoặc ', '@btn_luuduyet', ' để ghi sổ.'])
    d.sub(['Hoặc ', '@btn_quaylai_form', ' nếu muốn hủy.'])

    d.phan('XÓA')
    d.step(['Bước 1: Bấm ', '@btn_xoa_row', ' ở cột Hành động của phiếu Đang tạo do mình tạo'])
    d.sub(['Hoặc tại màn chi tiết phiếu, bấm ', '@btn_xoa'])
    d.step('Bước 2: Hệ thống hiện hộp xác nhận “Xác nhận xóa”.')
    d.img('13_delete', 'Hộp xác nhận xóa phiếu')
    d.step(['Bước 3: Bấm ', '@btn_confirm_xoa', ' để xác nhận xóa. Phiếu nguồn trở lại trạng thái chờ lập phiếu.'])
    d.sub(['Hoặc bấm ', '@btn_huy_confirm', ' nếu bấm nhầm'])

    d.phan('XEM LỊCH SỬ THAY ĐỔI')
    d.p('Cách 1: Xem lịch sử từ màn danh sách:')
    d.step(['Ở cột Hành động, bấm ', '@btn_lichsu_row'])
    d.sub(['Hoặc bấm ', '@btn_bacham_row', ' rồi chọn ', '@item_lichsu'])
    d.p('Cách 2: Xem lịch sử từ màn chi tiết:')
    d.step(['Bước 1: Bấm vào Mã phiếu ', '@link_sophieu', ' để mở màn chi tiết'])
    d.step(['Bước 2: Ở khối Lịch sử, chọn nút ', '@btn_xemlichsu'])
    d.img('16_history', 'Cửa sổ Lịch sử thay đổi của phiếu')
    d.step(['Bước 3: Bấm ', '@btn_boloc_ls', ' để lọc theo Loại hành động, Người thực hiện, Từ ngày, Đến ngày'])
    d.step(['Bước 4: Bấm ', '@btn_dong_ls', ' để đóng cửa sổ.'])

    d.phan('XEM CHI TIẾT')
    d.step('Bước 1: Truy cập vào màn hình Phiếu kế toán.')
    d.step(['Bước 2: Bấm vào Mã phiếu ', '@link_sophieu', '. Hệ thống mở màn “Chi tiết phiếu kế toán”.'])
    d.sub(['Bấm mã phiếu nguồn ', '@link_phieunguon_detail', ' để mở phiếu nguồn ở tab mới.'])
    d.img('17_detail', 'Màn hình Chi tiết phiếu kế toán')
    d.step(['Bước 3: Bấm ', '@btn_quaylai', ' để về màn danh sách.'])

    d.phan('XUẤT EXCEL')
    d.p('Cách 1: Xuất danh sách:')
    d.step('Bước 1: Lọc danh sách theo đúng dữ liệu cần lấy (xem PHẦN 1).')
    d.step(['Bước 2: Bấm ', '@btn_xuatexcel', '. Hệ thống mở cửa sổ “Chọn trường xuất file”.'])
    d.img('20_export', 'Cửa sổ Chọn trường xuất file')
    d.step('Bước 3: Tích chọn, kéo biểu tượng ☰ để đổi vị trí các trường cần xuất.')
    d.sub(['Hoặc bấm ', '@btn_chontatca', ' / ', '@btn_bochonhet'])
    d.step(['Bước 4: Bấm ', '@btn_xuatfile'])
    d.sub(['Hoặc bấm ', '@btn_dong_export', ' để không xuất'])
    d.step('Bước 5: Mở file Excel đã tải.')
    d.p('Cách 2: Xuất một phiếu:')
    d.step(['Bước 1: Ở cột Hành động, bấm ', '@btn_xuat_row'])
    d.sub(['Hoặc bấm ', '@btn_bacham_row', ' rồi chọn ', '@item_xuat'])
    d.sub(['Hoặc tại màn chi tiết phiếu, bấm ', '@btn_xuat_detail'])
    d.step('Bước 2: Mở file Excel chi tiết phiếu đã tải.')

    d.tuy_chinh_cot()

    d.phan('IN PHIẾU')
    d.step(['Bước 1: Ở cột Hành động, bấm ', '@btn_in_row'])
    d.sub(['Hoặc bấm ', '@btn_bacham_row', ' rồi chọn ', '@item_in'])
    d.sub(['Hoặc tại màn chi tiết phiếu, bấm ', '@btn_in'])
    d.step('Bước 2: Hệ thống mở cửa sổ xem trước bản in khổ ngang.')
    d.img('18_print', 'Cửa sổ Xem trước phiếu kế toán')
    d.step(['Bước 3: Bấm ', '@btn_in_preview', ' để in.'])

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
