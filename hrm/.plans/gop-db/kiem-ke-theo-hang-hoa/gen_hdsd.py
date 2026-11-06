# -*- coding: utf-8 -*-
"""HDSD bản GỌN — Kiểm kê theo hàng hóa (phiếu kiểm kê theo hàng hóa, form chuẩn, 06/11/2026).

Chạy: python gen_hdsd.py  → HDSD_Kiem ke theo hang hoa.docx (PDF + ảnh soát ghi vào thư mục tạm)
Phần chung: ../phieu-theo-form-quoc-gia/hdsd_phieu_lib.py. Sơ đồ tổng quan dùng lại ảnh gen_srs.py sinh ra (kkhh_shots/uml/overview.png).
Khuôn cấu trúc: ../kiem-ke-theo-vi-tri/gen_hdsd.py (màn anh em).
Ảnh + icon: kkhh_shots (dev-hrm 06/11/2026, _capture/capture.js chặn mọi yêu cầu ghi). Ảnh Sửa / Xóa: phiếu 1090 giả Đang tạo
(sửa phản hồi trên trình duyệt). Ảnh lỗi Lưu: yêu cầu lưu bị chặn tại trình duyệt, trả lỗi kiểm tra giả đúng câu của máy chủ.
Cập nhật kết quả, Duyệt / Không duyệt, Xử lý, Chọn kế hoạch là trạng thái thật. Icon nút Lập phiếu lấy từ 2 màn Kế hoạch.
"""
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'phieu-theo-form-quoc-gia'))
from hdsd_phieu_lib import PhieuHdsd, finalize_word, toc_lines, render_check  # noqa: E402

TEN = 'Kiểm kê theo hàng hóa'
SHOTS = os.path.join(HERE, 'kkhh_shots')
KH_ICONS = os.path.join(HERE, '..', 'ke-hoach-kiem-ke-theo-hang-hoa', 'khkkhh_shots', 'icons')
OUT = os.path.join(HERE, 'HDSD_Kiem ke theo hang hoa.docx')
CHECK_DIR = os.path.join(tempfile.gettempdir(), 'hdsd_kkhh')

THUAT_NGU = [
    ['Phiếu kiểm kê theo hàng hóa', 'Phiếu <mã công ty>.KKK-NNNNN: danh sách hàng – vị trí – lô – tồn của các kho cần kiểm, kết quả '
                                    'thực kiểm, hàng thừa khác và hội đồng kiểm kê.'],
    ['Kế hoạch kiểm kê', 'Kế hoạch kiểm kê theo hàng hóa (Đang kiểm) hoặc Kế hoạch tổng kiểm kê hàng hóa (Đã duyệt) ở phân hệ Tài chính.'],
    ['Công ty thuê kho', 'Công ty có kho kế toán gắn với kho đã chọn.'],
    ['ĐVT kiểm kê', 'Đơn vị dùng để đếm từng lô; đổi sang đơn vị lớn thì lô tự tách dòng.'],
    ['Thực kiểm / Chênh lệch', 'Số đếm được / Thực kiểm trừ SL (âm là thiếu, dương là thừa).'],
    ['Hàng thừa khác', 'Hàng đếm được nhưng không có trong danh sách của phiếu.'],
    ['Đang tạo', 'Phiếu mới lưu; chỉ người tạo thấy, sửa, xóa.'],
    ['Đang kiểm', 'Phiếu đã gửi; người tạo cập nhật kết quả.'],
    ['Chờ KT duyệt', 'Đã gửi duyệt kết quả, chờ Ban kiểm soát.'],
    ['Không duyệt', 'Ban kiểm soát trả lại; người tạo cập nhật lại kết quả.'],
    ['Chờ xử lý / Đang xử lý', 'Đã duyệt, có chênh lệch cần lập phiếu xử lý / đã lập nhưng chưa xử lý hết.'],
    ['Hoàn thành', 'Phiếu đã xử lý xong.'],
]
PHIEN_BAN = [['1.0', '06/11/2026', 'Tạo mới tài liệu theo form chuẩn']]
QUYEN = [
    ['Tạo phiếu (lập tay), Thêm hàng hóa, Lưu và gửi', 'Mọi người dùng đã đăng nhập.'],
    ['Lập phiếu từ kế hoạch', 'Lập phiếu kiểm kê kho theo hàng hóa.'],
    ['Sửa, Xóa', 'Người tạo phiếu, khi phiếu Đang tạo.'],
    ['Cập nhật kết quả (Gửi duyệt)', 'Người tạo phiếu, khi phiếu Đang kiểm / Không duyệt.'],
    ['Duyệt kết quả, Không duyệt, lối chờ duyệt kết quả', 'Ban kiểm soát duyệt kết quả kiểm kê.'],
    ['Xử lý (tạo phiếu điều chuyển / nhập / xuất điều chỉnh)', 'Xử lý phiếu kiểm kê hàng hóa (nút nhập kho điều chuyển cần thêm Tạo phiếu nhập kho điều chỉnh kiểm kê).'],
    ['Xem phiếu của mọi công ty', 'Xem phiếu kiểm kê hàng hóa - theo tổng công ty.'],
    ['Xem phiếu của công ty mình', 'Xem phiếu kiểm kê hàng hóa - theo công ty (không có quyền: chỉ xem phiếu mình tạo).'],
    ['In, Xuất Excel, Xem lịch sử', 'Không cần quyền riêng (phiếu trong phạm vi xem).'],
]


def build():
    d = PhieuHdsd(TEN, SHOTS, icon_dirs=[os.path.join(SHOTS, 'icons'), KH_ICONS])
    d.tong_quan(THUAT_NGU, PHIEN_BAN, QUYEN, os.path.join(SHOTS, 'uml', 'overview.png'))

    d.phan('TRUY CẬP VÀ TÌM KIẾM')
    d.step(['Bước 1: Từ phân hệ Kho ', '@menu_phanhe', ', tại menu Kiểm kho ', '@menu_nhom', ', nhóm Theo vị trí ', '@menu_nhom2',
            ', chọn Kiểm kê theo hàng hóa ', '@menu_muc'])
    d.sub(['Hoặc (Ban kiểm soát) từ phân hệ Tài chính ', '@menu_phanhe_tc', ', tại menu Kiểm kê ', '@menu_nhom_tc', ', chọn ',
           '@menu_muc_tc', ' để chỉ xem phiếu chờ duyệt kết quả'])
    d.img('01_list', 'Màn hình Danh sách phiếu kiểm kê theo hàng hóa')
    d.step(['Bước 2: Nhập số phiếu vào ô tìm kiếm nhanh ', '@o_timnhanh'])
    d.step(['Bước 3: Nhấn ', '@btn_timkiem'])
    d.step(['Bước 4: Bấm ', '@btn_timkiemnangcao', ', chọn giá trị trong ', '@o_kho', ' để lọc theo Kho'])
    for lb, ic in [('Trạng thái', 'o_trangthai'), ('Người tạo', 'o_nguoitao'), ('Người duyệt', 'o_nguoiduyet'),
                   ('Mã hàng hóa', 'o_mahang'), ('Tên hàng hóa', 'o_tenhang'), ('Ngày tạo', 'o_ngaytao')]:
        d.sub(['Hoặc chọn / nhập giá trị ', '@' + ic, ' để lọc theo %s' % lb])
    d.step(['Bước 5: Chọn ', '@btn_lammoi', ' để xóa giá trị đã lọc'])

    d.phan('THÊM MỚI PHIẾU KIỂM KÊ')
    d.step('Bước 1: Truy cập vào màn hình Kiểm kê theo hàng hóa (PHẦN 1).')
    d.step(['Bước 2: Bấm ', '@btn_taomoi'])
    d.sub(['Hoặc ở màn Kế hoạch kiểm kê theo hàng hóa / Kế hoạch tổng kiểm kê hàng hóa, bấm ', '@btn_lapphieu_row',
           ' ở kế hoạch (phiếu nạp sẵn kế hoạch).'])
    d.step(['Bước 3: Chọn kế hoạch ở ô ', '@o_kehoach', ' (xem PHẦN 3) hoặc chọn Kho ', '@o_kho_form', ', kiểm tra Công ty thuê kho ',
            '@o_congtythue', ' và bấm ', '@btn_themhang', ' (xem PHẦN 4).'])
    d.img('10c_filled', 'Màn hình Tạo phiếu kiểm kê theo hàng hóa')
    d.step('Bước 4: Nhập / chọn đầy đủ thông tin bắt buộc: Kho, Công ty thuê kho, Hàng hóa (ĐVT kiểm kê từng lô), Thành viên, Chức vụ.')
    d.sub(['Hoặc nhập Ghi chú ', '@o_ghichu_form', '; bấm ', '@btn_themdong', ' để thêm thành viên hội đồng.'])
    d.step(['Bước 5: Bấm ', '@btn_luu', ' để lưu phiếu ở trạng thái Đang tạo, về màn danh sách'])
    d.sub(['Hoặc ', '@btn_luugui', ' để lưu và gửi luôn (xem PHẦN 5).'])
    d.sub(['Hoặc ', '@btn_luutieptuc', ' để lưu rồi tạo tiếp phiếu khác.'])
    d.sub(['Hoặc ', '@btn_quaylai_form', ' để không lưu, chọn ', '@btn_thoat', ' để rời màn hoặc ', '@btn_olai', ' để ở lại.'])

    d.phan('CHỌN KẾ HOẠCH KIỂM KÊ')
    d.step(['Bước 1: Ở màn Tạo phiếu, bấm vào ô Kế hoạch kiểm kê ', '@o_kehoach'])
    d.img('11_plan_picker', 'Popup Chọn kế hoạch kiểm kê hàng hóa')
    d.step(['Bước 2: Nhập mã phiếu / chọn người tạo, bấm ', '@btn_timkiem_popup'])
    d.sub(['Hoặc bấm ', '@btn_lammoi_popup', ' để xóa điều kiện tìm.'])
    d.step('Bước 3: Bấm vào dòng kế hoạch cần lập phiếu. Hệ thống nạp kho, công ty thuê kho, hàng hóa và hội đồng của kế hoạch.')
    d.step(['Bước 4: Muốn bỏ kế hoạch, bấm ', '@btn_xoa_kehoach', ' trong ô Kế hoạch kiểm kê.'])

    d.phan('THÊM HÀNG HÓA, LÀM MỚI SỐ LIỆU VÀ ĐVT KIỂM KÊ')
    d.step(['Bước 1: Ở màn Tạo, chọn Kho ', '@o_kho_form', ' (Công ty thuê kho tự chọn hết).'])
    d.step(['Bước 2: Bấm ', '@btn_themhang', ', tích các hàng cần kiểm rồi bấm chọn.'])
    d.img('10f_picker', 'Popup Thêm hàng hóa')
    d.sub(['Hoặc bấm ', '@btn_dong_picker', ' để đóng không chọn.'])
    d.step(['Bước 3: Ở cột ĐVT kiểm kê ', '@o_dvt', ', chọn đơn vị cần đếm; hệ thống tự tách dòng của lô.'])
    d.step(['Bước 4: Bấm ', '@btn_lammoisolieu', ' để cập nhật lại tồn theo lô.'])
    d.sub(['Hoặc bấm ', '@btn_xoa_hang', ' để bỏ một hàng.'])
    d.step('Bước 5: Đổi Kho khi đã có hàng: hệ thống hỏi “Đổi kho”.')
    d.sub(['Bấm ', '@btn_dongy_doikho', ' để đổi kho (xóa danh sách hàng) hoặc ', '@btn_huy_doikho', ' để giữ kho cũ.'])

    d.phan('LƯU VÀ GỬI PHIẾU')
    d.step('Bước 1: Ở màn Tạo hoặc Sửa phiếu, nhập đủ thông tin như PHẦN 2.')
    d.step(['Bước 2: Bấm ', '@btn_luugui', '. Phiếu chuyển trạng thái Đang kiểm ', '@badge_dangkiem'])
    d.img('10b_validate', 'Thiếu thông tin bắt buộc: hệ thống báo lỗi đỏ dưới từng ô')
    d.step('Bước 3: Nếu thiếu thông tin, nhập bổ sung các ô viền đỏ rồi bấm lại.')

    d.phan('CHỈNH SỬA')
    d.step('Bước 1: Truy cập vào màn hình Kiểm kê theo hàng hóa.')
    d.step(['Bước 2: Ở dòng phiếu Đang tạo ', '@badge_dangtao', ' của mình, bấm ', '@btn_sua_row', ' ở cột Hành động'])
    d.sub(['Hoặc tại màn chi tiết, bấm ', '@btn_sua'])
    d.step('Bước 3: Hệ thống mở màn “Sửa phiếu kiểm kê theo hàng hóa”.')
    d.img('12_edit', 'Màn hình Sửa phiếu kiểm kê theo hàng hóa')
    d.step('Bước 4: Sửa thông tin (quy tắc như Thêm mới).')
    d.step(['Bước 5: Bấm ', '@btn_luu'])
    d.sub(['Hoặc ', '@btn_luugui', ' để lưu và gửi.'])
    d.sub(['Hoặc ', '@btn_quaylai_form', ' để không lưu.'])

    d.phan('XÓA')
    d.step(['Bước 1: Ở dòng phiếu Đang tạo của mình, bấm ', '@btn_xoa_row', ' ở cột Hành động'])
    d.sub(['Hoặc tại màn chi tiết, bấm ', '@btn_xoa'])
    d.step('Bước 2: Hệ thống hiện hộp xác nhận “Xác nhận xóa”')
    d.img('13_delete', 'Hộp xác nhận xóa phiếu')
    d.step(['Bước 3: Bấm ', '@btn_confirm_xoa', ' để xác nhận xóa'])
    d.sub(['Hoặc bấm ', '@btn_huy_confirm', ' nếu bấm nhầm'])

    d.phan('CẬP NHẬT KẾT QUẢ KIỂM KÊ')
    d.step(['Bước 1: Ở dòng phiếu Đang kiểm ', '@badge_dangkiem', ' (hoặc Không duyệt ', '@badge_khongduyet', ') của mình, bấm ',
            '@btn_capnhatkq_row'])
    d.img('14_result', 'Màn chi tiết phiếu ở bước Cập nhật kết quả')
    d.step(['Bước 2: Nhập Thực kiểm ', '@o_thuckiem', ' cho từng dòng (bắt buộc), Ghi chú ', '@o_ghichu_kq', ' nếu cần.'])
    d.step(['Bước 3: Ở khối Hàng thừa khác, bấm ', '@btn_themdong_thua', ', nhập tên hàng hoặc bấm ', '@btn_chonhang_thua',
            ' để chọn hàng có mã; chọn Vị trí, nhập Thực kiểm.'])
    d.sub(['Hoặc bấm ', '@btn_themvitri_thua', ' để thêm vị trí cho hàng thừa.'])
    d.step(['Bước 4: Ở khối File đính kèm, bấm ', '@btn_themtailieu', ' để đính kèm file kết quả (bắt buộc nếu phiếu chưa có file).'])
    d.step(['Bước 5: Bấm ', '@btn_guiduyet', '. Phiếu chuyển Chờ KT duyệt ', '@badge_choduyet'])
    d.sub(['Hoặc ', '@btn_quaylai', ' để không lưu.'])

    d.phan('DUYỆT KẾT QUẢ')
    d.step(['Bước 1: (Ban kiểm soát) Ở dòng phiếu Chờ KT duyệt, bấm ', '@btn_duyet_row', ' hoặc bấm thông báo để mở chi tiết.'])
    d.step(['Bước 2: Bấm ', '@btn_duyet', ' ở chân màn chi tiết.'])
    d.img('15_approve', 'Popup Duyệt kết quả kiểm kê')
    d.step('Bước 3: Nhập Ghi chú duyệt (không bắt buộc).')
    d.step(['Bước 4: Bấm ', '@btn_duyet_popup'])
    d.sub(['Hoặc bấm ', '@btn_huy_popup', ' để không duyệt.'])

    d.phan('KHÔNG DUYỆT KẾT QUẢ')
    d.step(['Bước 1: (Ban kiểm soát) Mở chi tiết phiếu Chờ KT duyệt, bấm ', '@btn_khongduyet'])
    d.img('15b_reject', 'Popup Không duyệt kết quả kiểm kê')
    d.step('Bước 2: Nhập lý do vào Ghi chú duyệt (bắt buộc).')
    d.step(['Bước 3: Bấm ', '@btn_khongduyet_popup', '. Phiếu chuyển Không duyệt ', '@badge_khongduyet'])
    d.sub(['Hoặc bấm ', '@btn_huy_popup', ' để hủy thao tác.'])

    d.phan('XỬ LÝ PHIẾU')
    d.step(['Bước 1: (Người xử lý) Ở dòng phiếu Chờ xử lý ', '@badge_choxuly', ' hoặc Đang xử lý ', '@badge_dangxuly', ', bấm ',
            '@btn_xuly_row', ' hoặc bấm thông báo để mở chi tiết.'])
    d.img('16_handle', 'Màn chi tiết phiếu Chờ xử lý')
    d.step(['Bước 2: Bấm ', '@btn_nhapdc', ' để lập phiếu nhập kho điều chỉnh cho các dòng thừa.'])
    d.sub(['Hoặc bấm ', '@btn_xuatdc', ' để lập phiếu xuất kho điều chỉnh cho các dòng thiếu.'])
    d.sub('Hoặc bấm Tạo phiếu điều chuyển vị trí (khi hàng thiếu ở vị trí này, thừa ở vị trí khác).')
    d.step('Bước 3: Hoàn tất phiếu ở màn vừa mở; phiếu kiểm kê tự chuyển Đang xử lý / Hoàn thành.')

    d.phan('XEM LỊCH SỬ THAY ĐỔI')
    d.p('Cách 1: Xem lịch sử từ màn danh sách:')
    d.step(['Ở cột Hành động, bấm ', '@btn_lichsu_row'])
    d.sub(['Hoặc bấm ', '@btn_bacham_row', ' rồi chọn ', '@item_lichsu'])
    d.p('Cách 2: Xem lịch sử từ màn chi tiết:')
    d.step(['Bước 1: Bấm vào Số phiếu ', '@link_sophieu', ' để mở màn chi tiết'])
    d.step(['Bước 2: Ở khối Lịch sử, chọn nút ', '@btn_xemlichsu'])
    d.img('20_history', 'Cửa sổ Lịch sử thay đổi')
    d.step(['Bước 3: Bấm ', '@btn_boloc_ls', ' để lọc theo Loại hành động, Người thực hiện, Từ ngày, Đến ngày'])
    d.step(['Bước 4: Bấm ', '@btn_dong_ls', ' để đóng cửa sổ.'])

    d.phan('XEM CHI TIẾT')
    d.step('Bước 1: Truy cập vào màn hình Kiểm kê theo hàng hóa.')
    d.step(['Bước 2: Bấm vào Số phiếu ', '@link_sophieu', '. Hệ thống mở màn “Chi tiết phiếu kiểm kê theo hàng hóa”.'])
    d.img('17_detail', 'Màn hình Chi tiết phiếu kiểm kê theo hàng hóa')
    d.sub(['Bấm mã kế hoạch ', '@link_kehoach_ct', ' để mở kế hoạch ở tab mới.'])
    d.step(['Bước 3: Bấm ', '@btn_quaylai', ' để về màn danh sách.'])

    d.phan('IN PHIẾU')
    d.step(['Bước 1: Ở cột Hành động, bấm ', '@btn_in_row'])
    d.sub(['Hoặc tại màn chi tiết, bấm ', '@btn_in'])
    d.step('Bước 2: Hệ thống mở cửa sổ xem trước bản in.')
    d.img('18_print', 'Cửa sổ Xem trước phiếu kiểm kê theo hàng hóa')
    d.step(['Bước 3: Bấm ', '@btn_in_preview', ' để in.'])

    d.phan('IN DANH SÁCH')
    d.step('Bước 1: Lọc danh sách theo đúng dữ liệu cần in (xem PHẦN 1).')
    d.step(['Bước 2: Bấm ', '@btn_in_list', '. Hệ thống mở cửa sổ xem trước danh sách.'])
    d.img('19_printlist', 'Cửa sổ Xem trước danh sách phiếu kiểm kê theo hàng hóa')
    d.step(['Bước 3: Bấm ', '@btn_in_preview', ' để in.'])

    d.xuat_excel(img='21_export')
    d.phan('XUẤT EXCEL MỘT PHIẾU')
    d.step(['Bước 1: Ở cột Hành động, bấm ', '@btn_xuat_row'])
    d.sub(['Hoặc bấm ', '@btn_bacham_row', ' rồi chọn ', '@item_xuat'])
    d.sub(['Hoặc tại màn chi tiết, bấm ', '@btn_xuatexcel_detail'])
    d.img('03_rowmenu', 'Nút Xuất Excel trong menu Hành động khác')
    d.step('Bước 2: Mở file Excel phiếu đã tải về.')
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
