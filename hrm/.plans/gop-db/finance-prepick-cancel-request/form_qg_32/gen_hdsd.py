# -*- coding: utf-8 -*-
"""HDSD bản GỌN — Yêu cầu hủy hàng giữ (STT 32, form chuẩn Danh mục quốc gia, 28/10/2026).

Chạy: python gen_hdsd.py  → out/HDSD_Yêu cầu hủy hàng giữ.docx (+ .pdf, render/ để soát)
Khuôn chép từ màn 27 (finance-product-import-direct-transfer/form_qg/gen_hdsd.py).
Phần dùng chung: ../../phieu-theo-form-quoc-gia/hdsd_phieu_lib.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'phieu-theo-form-quoc-gia'))
from hdsd_phieu_lib import PhieuHdsd, finalize_word, toc_lines, render_check  # noqa: E402

TEN = 'Yêu cầu hủy hàng giữ'
SHOTS = os.path.join(HERE, 'hdsd_shots')
OUT = os.path.join(HERE, 'out', 'HDSD_%s.docx' % TEN)

THUAT_NGU = [
    ['Hàng giữ', 'Số lượng hàng hóa được giữ lại cho một khách hàng cụ thể, do một nhân viên kinh doanh đứng tên giữ.'],
    ['Yêu cầu hủy hàng giữ', 'Phiếu đề nghị trả lại kho phần hàng đang giữ mà khách không lấy nữa. Mã phiếu dạng '
                             'PYCHHG-NNNNN.'],
    ['Phiếu hủy hàng giữ', 'Chứng từ người duyệt lập từ phiếu yêu cầu. Mã phiếu dạng PHHG-NNNNN. Lưu phiếu này thì hàng '
                           'giữ mới bị trừ.'],
    ['Có thể hủy', 'Số lượng còn có thể hủy của hàng hóa, đã trừ phần đang nằm trong đề nghị xuất kho chưa xong.'],
    ['Yêu cầu hủy', 'Số lượng người lập đề nghị hủy giữ.'],
    ['Duyệt hủy', 'Số lượng người duyệt thực sự cho hủy, có thể khác số đề nghị.'],
    ['Có thể giữ', 'Tồn kho khả dụng tại thời điểm mở phiếu, chỉ để tham khảo.'],
    ['Trạng thái Đang tạo', 'Phiếu lưu nháp hoặc bị Không duyệt trả về. Người lập được sửa, xóa.'],
    ['Trạng thái Chờ duyệt', 'Phiếu đã gửi, chờ người có quyền Quản lý giữ hàng xử lý.'],
    ['Trạng thái Đã duyệt', 'Đã lập Phiếu hủy hàng giữ, hàng giữ đã bị trừ. Chỉ xem, in, xuất Excel.'],
]

PHIEN_BAN = [
    ['1.0', '05/09/2026', 'Ban hành lần đầu cho màn hình Yêu cầu hủy hàng giữ trên phân hệ Tài chính.'],
    ['1.1', '28/10/2026', 'Chuyển sang form chuẩn'],
]

QUYEN = [
    ['Xem danh sách, xem chi tiết, in, xuất Excel, xem lịch sử',
     'Không cần quyền riêng. Phạm vi theo quyền Xem phiếu hàng giữ theo tổng công ty / theo công ty / theo phòng ban; '
     'quyền Quản lý giữ hàng xem được mọi phiếu khác Đang tạo. Không có quyền nào thì chỉ thấy phiếu của mình.'],
    ['Tạo mới', 'Không cần quyền riêng; người lập phải đang giữ hàng cho ít nhất một khách hàng.'],
    ['Sửa, xóa', 'Người lập phiếu, phiếu đang ở trạng thái Đang tạo.'],
    ['Duyệt (Tạo phiếu hủy hàng giữ), Không duyệt', 'Quyền Quản lý giữ hàng, phiếu đang ở trạng thái Chờ duyệt.'],
]


def build():
    d = PhieuHdsd(TEN, SHOTS)
    d.tong_quan(THUAT_NGU, PHIEN_BAN, QUYEN, os.path.join(HERE, 'uml', 'overview_drive.png'))

    # PHẦN 1
    d.truy_cap(
        menu=[('Tài chính', 'menu_phanhe'), ('Hàng hoá - Dịch vụ - Vận chuyển', 'menu_nhom'),
              ('Giữ hàng', 'menu_giuhang'), ('Yêu cầu hủy hàng giữ', 'menu_muc')],
        o_nhanh='mã phiếu',
        bo_loc=[('Công ty', 'o_congty'), ('Phòng ban', 'o_phongban'), ('Mã phiếu', 'o_maphieu'),
                ('Trạng thái', 'o_trangthai'), ('Người tạo', 'o_nguoitao'), ('Người duyệt', 'o_nguoiduyet'),
                ('Tên hàng hóa', 'o_tenhang'), ('Mã hàng hóa', 'o_mahang'), ('Ngày tạo', 'o_ngaytao')])

    # PHẦN 2 — Tạo mới
    d.phan('TẠO MỚI PHIẾU YÊU CẦU HỦY HÀNG GIỮ')
    d.step(d.vao)
    d.step(['Bước 2: Bấm ', '@btn_taomoi'])
    d.step('Bước 3: Nhập thông tin chung:')
    d.sub('Khách hàng (bắt buộc): chọn trong danh sách. Danh sách chỉ gồm khách hàng bạn đang giữ hàng.')
    d.sub('Ghi chú (tùy chọn): nhập chữ, tối đa 255 ký tự.')
    d.step(['Bước 4: Ở khối Chi tiết, bấm ', '@btn_themhanghoa',
            '. Hệ thống mở cửa sổ “Hàng đang giữ cho khách hàng”.'])
    d.img('11_stock', 'Cửa sổ Hàng đang giữ cho khách hàng')
    d.step(['Bước 5: Tích chọn ', '@o_tick', ' các hàng cần hủy giữ, bấm ', '@btn_chon'])
    d.sub(['Hoặc bấm ', '@btn_dong', ' để không chọn hàng.'])
    d.step('Bước 6: Nhập Yêu cầu hủy cho từng dòng (bắt buộc): chỉ nhập số, lớn hơn 0 và không vượt cột Có thể hủy; '
           'dấu phẩy ngăn hàng nghìn, dấu chấm ngăn phần thập phân (ví dụ 1,200.5).')
    d.img('10_create', 'Màn hình Thêm yêu cầu hủy hàng giữ')
    d.sub('Bỏ tích ô Cần hủy nếu không muốn hủy dòng đó.')
    d.sub(['Hoặc bấm ', '@btn_xoadong', ' để bỏ dòng hàng khỏi phiếu.'])
    d.step(['Bước 7: Bấm ', '@btn_luuguiduyet', ', chọn ', '@btn_confirm_xacnhan',
            ' để gửi người có quyền Quản lý giữ hàng duyệt,'])
    d.sub(['Hoặc ', '@btn_luunhap', ' để lưu nháp (chỉ cần chọn Khách hàng, chưa cần dòng hàng).'])
    d.sub(['Hoặc ', '@btn_luutieptuc', ' để lưu nháp rồi lập tiếp phiếu khác.'])
    d.sub(['Hoặc ', '@btn_quaylai', ' để không lưu thông tin.'])

    # PHẦN 3 — Chỉnh sửa
    d.phan('CHỈNH SỬA')
    d.step(d.vao)
    d.step(['Bước 2: Bấm nút ', '@btn_sua_row', ' ở cột Hành động của phiếu Đang tạo do bạn lập.'])
    d.sub(['Hoặc bấm vào Mã phiếu để mở màn chi tiết, chọn ', '@btn_sua'])
    d.step('Bước 3: Hệ thống hiển thị màn hình “Sửa yêu cầu hủy hàng giữ”.')
    d.img('12_edit', 'Màn hình Sửa yêu cầu hủy hàng giữ')
    d.step('Bước 4: Sửa Ghi chú, dòng hàng, số Yêu cầu hủy (quy tắc nhập như PHẦN 2). Ô Khách hàng không đổi được.')
    d.step(['Bước 5: Bấm ', '@btn_luuguiduyet', ', chọn ', '@btn_confirm_xacnhan', ' để lưu và gửi duyệt,'])
    d.sub(['Hoặc ', '@btn_luunhap', ' để lưu nháp.'])
    d.sub(['Hoặc ', '@btn_quaylai', ' nếu muốn hủy.'])

    # PHẦN 4 — Xóa
    d.xoa('Xác nhận xóa', them_cach=['Hoặc bấm vào Mã phiếu để mở màn chi tiết, chọn ', '@btn_xoa'])

    # PHẦN 5 — Duyệt = Tạo phiếu hủy hàng giữ
    d.phan('DUYỆT PHIẾU (TẠO PHIẾU HỦY HÀNG GIỮ)')
    d.step(['Bước 1: Bấm ', '@btn_duyet_row', ' ở cột Hành động của phiếu Chờ duyệt.'])
    d.sub(['Hoặc bấm vào Mã phiếu để mở màn chi tiết, chọn ', '@btn_taophieuhuy'])
    d.step('Bước 2: Hệ thống mở màn “Lập phiếu hủy hàng giữ” điền sẵn phiếu yêu cầu và các dòng hàng.')
    d.img('14_approve', 'Màn hình Lập phiếu hủy hàng giữ mở từ phiếu yêu cầu')
    d.step('Bước 3: Kiểm tra số Duyệt hủy từng dòng (bắt buộc, lớn hơn 0, không vượt cột Có thể hủy); bỏ tích Cần hủy ở '
           'dòng không đồng ý.')
    d.step(['Bước 4: Bấm ', '@btn_duyet', '. Hệ thống hiện hộp xác nhận “Xác nhận duyệt”.'])
    d.img('14_approve_confirm', 'Hộp xác nhận duyệt — lập phiếu hủy sẽ trừ hàng giữ ngay')
    d.step(['Bước 5: Bấm ', '@btn_confirm_duyet', ' để duyệt. Hàng giữ bị trừ, phiếu yêu cầu chuyển sang Đã duyệt.'])
    d.sub(['Hoặc bấm ', '@btn_huy_confirm', ' nếu bấm nhầm'])
    d.sub(['Hoặc bấm ', '@btn_quaylai', ' để về danh sách mà không duyệt.'])

    # PHẦN 6 — Không duyệt
    d.phan('KHÔNG DUYỆT PHIẾU')
    d.step('Bước 1: Bấm vào Mã phiếu của phiếu Chờ duyệt để mở màn chi tiết.')
    d.step(['Bước 2: Bấm ', '@btn_khongduyet', '. Hệ thống mở cửa sổ “Không duyệt yêu cầu hủy hàng giữ”.'])
    d.img('15_reject', 'Cửa sổ Không duyệt yêu cầu hủy hàng giữ')
    d.step('Bước 3: Nhập Lý do không duyệt (bắt buộc, tối đa 255 ký tự).')
    d.step(['Bước 4: Bấm ', '@btn_confirm_khongduyet', '. Phiếu quay về trạng thái Đang tạo để người lập sửa và gửi lại.'])
    d.sub(['Hoặc bấm ', '@btn_dong_reject', ' nếu muốn hủy.'])

    # PHẦN 7 — Lịch sử
    # (cột Hành động hiện thẳng biểu tượng Lịch sử, không có menu ba chấm -> không dùng d.lich_su())
    d.phan('XEM LỊCH SỬ THAY ĐỔI')
    d.p('Cách 1: Xem lịch sử từ màn danh sách:')
    d.step(['Ở cột Hành động, bấm ', '@btn_lichsu_row'])
    d.p('Cách 2: Xem lịch sử từ màn chi tiết:')
    d.step('Bước 1: Bấm vào Mã phiếu để mở màn chi tiết')
    d.step(['Bước 2: Ở khối Lịch sử thay đổi, chọn nút ', '@btn_xemlichsu'])
    d.img('16_history', 'Cửa sổ Lịch sử yêu cầu hủy hàng giữ')
    d.step(['Bước 3: Bấm ', '@btn_dong_ls', ' để đóng cửa sổ.'])

    # PHẦN 8 — Xem chi tiết
    d.phan('XEM CHI TIẾT PHIẾU')
    d.step(d.vao)
    d.step('Bước 2: Bấm vào Mã phiếu. Hệ thống mở màn “Chi tiết yêu cầu hủy hàng giữ”.')
    d.img('17_detail_approved', 'Màn hình Chi tiết yêu cầu hủy hàng giữ (phiếu Đã duyệt)')
    d.step('Bước 3: Bấm mã ở ô Phiếu hủy hàng giữ để mở phiếu hủy đã lập (phiếu Đã duyệt).')
    d.step(['Bước 4: Bấm ', '@btn_quaylai', ' để về màn danh sách.'])

    # PHẦN 9 — In phiếu (nút In danh sách đã gỡ theo Redmine #11149)
    d.phan('IN PHIẾU')
    d.step(['Bước 1: Ở cột Hành động, bấm ', '@btn_in_row'])
    d.sub(['Hoặc tại màn chi tiết phiếu, bấm ', '@btn_in'])
    d.step('Bước 2: Hệ thống mở cửa sổ xem trước bản in.')
    d.img('18_print', 'Cửa sổ Xem trước bản in phiếu yêu cầu hủy hàng giữ')
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
