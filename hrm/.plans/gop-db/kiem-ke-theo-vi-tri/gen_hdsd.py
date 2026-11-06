# -*- coding: utf-8 -*-
"""HDSD bản GỌN — Kiểm kê theo vị trí (phiếu kiểm kê theo vị trí, form chuẩn Danh mục quốc gia, 06/11/2026).

Chạy: python gen_hdsd.py  → HDSD_Kiem ke theo vi tri.docx (PDF + ảnh soát ghi vào thư mục tạm)
Phần chung: ../phieu-theo-form-quoc-gia/hdsd_phieu_lib.py. Sơ đồ tổng quan dùng lại ảnh gen_srs.py sinh ra (kkvt_shots/uml/overview.png).
Khuôn cấu trúc: ../ke-hoach-kiem-ke-theo-vi-tri/gen_hdsd.py (màn anh em).
Ảnh + icon: kkvt_shots (dev-hrm 06/11/2026, _capture/capture.js chặn mọi yêu cầu ghi). Ảnh Sửa / Xóa (giả Đang tạo), Duyệt / Không
duyệt (giả Chờ duyệt kết quả), Hoàn thành (giả không còn dòng cần điều chuyển), Chọn kế hoạch (giả 1 dòng) chụp bằng cách sửa phản hồi
trên trình duyệt; Nhập kết quả, Tạo phiếu điều chuyển vị trí là trạng thái thật. Icon Lập phiếu kiểm kê lấy từ khkkvt_shots.
"""
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'phieu-theo-form-quoc-gia'))
from hdsd_phieu_lib import PhieuHdsd, finalize_word, toc_lines, render_check  # noqa: E402

TEN = 'Kiểm kê theo vị trí'
SHOTS = os.path.join(HERE, 'kkvt_shots')
KH_ICONS = os.path.join(HERE, '..', 'ke-hoach-kiem-ke-theo-vi-tri', 'khkkvt_shots', 'icons')
OUT = os.path.join(HERE, 'HDSD_Kiem ke theo vi tri.docx')
CHECK_DIR = os.path.join(tempfile.gettempdir(), 'hdsd_kkvt')

THUAT_NGU = [
    ['Phiếu kiểm kê theo vị trí', 'Phiếu <mã công ty>-KKVT-NNNNN: hàng – lô – số tồn tại các vị trí cần kiểm, kết quả thực kiểm và '
                                  'hội đồng kiểm kê của một kho vật lý.'],
    ['Kế hoạch kiểm kê', 'Kế hoạch lập ở phân hệ Tài chính; phiếu có thể lập từ kế hoạch Đang kiểm.'],
    ['ĐVT kiểm kê', 'Đơn vị dùng để đếm từng lô; đổi sang đơn vị lớn thì lô tự tách dòng.'],
    ['Thực kiểm / Chênh lệch', 'Số đếm được / Thực kiểm trừ SL (âm là thiếu).'],
    ['Tổng kiểm kê', 'Ô tick ở dòng có chênh lệch: dòng thiếu được tick thì không cần điều chuyển.'],
    ['Đang tạo', 'Phiếu mới lưu; chỉ người tạo thấy, sửa, xóa.'],
    ['Đang kiểm', 'Phiếu đã gửi; người tạo nhập kết quả.'],
    ['Chờ duyệt kết quả', 'Đã lưu kết quả, chờ Ban kiểm soát.'],
    ['Chờ xử lý', 'Đã duyệt, còn chênh lệch thiếu cần xử lý.'],
    ['Hoàn thành', 'Phiếu đã xử lý xong.'],
]
PHIEN_BAN = [['1.0', '06/11/2026', 'Tạo mới tài liệu theo form chuẩn']]
QUYEN = [
    ['Tạo phiếu, chọn kế hoạch', 'Lập phiếu kiểm kê kho theo vị trí.'],
    ['Sửa, Xóa', 'Người tạo phiếu, khi phiếu Đang tạo.'],
    ['Nhập kết quả', 'Người tạo phiếu, khi phiếu Đang kiểm.'],
    ['Duyệt kết quả, Không duyệt', 'Ban kiểm soát duyệt kết quả kiểm kê.'],
    ['Xử lý (Tổng kiểm kê, Tạo phiếu điều chuyển vị trí, Hoàn thành)', 'Xử lý phiếu kiểm kê vị trí.'],
    ['Xem phiếu của mọi công ty', 'Xem phiếu kiểm kê vị trí - theo tổng công ty.'],
    ['Xem phiếu của công ty mình', 'Xem phiếu kiểm kê vị trí - theo công ty (không có quyền: chỉ xem phiếu mình tạo).'],
    ['In, Xuất Excel, Xem lịch sử', 'Không cần quyền riêng (phiếu trong phạm vi xem).'],
]


def build():
    d = PhieuHdsd(TEN, SHOTS, icon_dirs=[os.path.join(SHOTS, 'icons'), KH_ICONS])
    d.tong_quan(THUAT_NGU, PHIEN_BAN, QUYEN, os.path.join(SHOTS, 'uml', 'overview.png'))

    d.phan('TRUY CẬP VÀ TÌM KIẾM')
    d.step(['Bước 1: Từ phân hệ Kho ', '@menu_phanhe', ', tại menu Kiểm kho ', '@menu_nhom', ', nhóm Theo vị trí ', '@menu_nhom2',
            ', chọn Kiểm kê theo vị trí ', '@menu_muc'])
    d.img('01_list', 'Màn hình Kiểm kê theo vị trí')
    d.step(['Bước 2: Nhập số phiếu vào ô tìm kiếm nhanh ', '@o_timnhanh'])
    d.step(['Bước 3: Nhấn ', '@btn_timkiem'])
    d.step(['Bước 4: Bấm ', '@btn_timkiemnangcao', ', chọn giá trị trong ', '@o_trangthai', ' để lọc theo Trạng thái'])
    for lb, ic in [('Người tạo', 'o_nguoitao'), ('Người duyệt', 'o_nguoiduyet'), ('Hàng hóa (mã hoặc tên)', 'o_hanghoa'),
                   ('Ngày kiểm kê', 'o_ngaykiemke'), ('Kho', 'o_kho'), ('Nhà', 'o_nha'), ('Dãy', 'o_day'), ('Khoang', 'o_khoang'),
                   ('Vị trí', 'o_vitri'), ('Công ty', 'o_congty'), ('Phòng ban', 'o_phongban')]:
        d.sub(['Hoặc chọn / nhập giá trị ', '@' + ic, ' để lọc theo %s' % lb])
    d.step(['Bước 5: Chọn ', '@btn_lammoi', ' để xóa giá trị đã lọc'])

    d.phan('THÊM MỚI PHIẾU KIỂM KÊ')
    d.step('Bước 1: Truy cập vào màn hình Kiểm kê theo vị trí (PHẦN 1).')
    d.step(['Bước 2: Bấm ', '@btn_taomoi'])
    d.sub(['Hoặc ở màn Kế hoạch kiểm kê theo vị trí, bấm ', '@btn_lapphieu_row', ' ở kế hoạch Đang kiểm (phiếu nạp sẵn kế hoạch).'])
    d.step(['Bước 3: Chọn kế hoạch ở ô ', '@o_kehoach', ' (xem PHẦN 3) hoặc chọn Kho vật lý ', '@o_kho_form', ', tick phạm vi và bấm ',
            '@btn_layvitri', ' (xem PHẦN 4).'])
    d.img('10c_filled', 'Màn hình Tạo phiếu kiểm kê theo vị trí')
    d.step('Bước 4: Nhập / chọn đầy đủ thông tin bắt buộc: Kho vật lý, Vị trí, Chi tiết (ĐVT kiểm kê từng lô), Nhân viên, Chức vụ.')
    d.sub(['Hoặc bấm ', '@btn_themdong', ' để thêm thành viên hội đồng.'])
    d.step(['Bước 5: Bấm ', '@btn_luu', ' để lưu phiếu ở trạng thái Đang tạo, về màn danh sách'])
    d.sub(['Hoặc ', '@btn_luugui', ' để lưu và gửi luôn (xem PHẦN 5).'])
    d.sub(['Hoặc ', '@btn_luutieptuc', ' để lưu rồi tạo tiếp phiếu khác.'])
    d.sub(['Hoặc ', '@btn_quaylai_form', ' để không lưu, chọn ', '@btn_thoat', ' để rời màn hoặc ', '@btn_olai', ' để ở lại.'])

    d.phan('CHỌN KẾ HOẠCH KIỂM KÊ')
    d.step(['Bước 1: Ở màn Tạo phiếu, bấm vào ô Kế hoạch kiểm kê ', '@o_kehoach'])
    d.img('11_plan_picker', 'Popup Chọn kế hoạch kiểm kê theo vị trí')
    d.step(['Bước 2: Nhập mã kế hoạch, bấm ', '@btn_timkiem_popup'])
    d.sub(['Hoặc bấm ', '@btn_lammoi_popup', ' để xóa điều kiện tìm.'])
    d.step('Bước 3: Bấm vào dòng kế hoạch cần lập phiếu. Hệ thống nạp kho, phạm vi, chi tiết và hội đồng của kế hoạch.')
    d.step(['Bước 4: Muốn bỏ kế hoạch, bấm ', '@btn_xoa_kehoach', ' trong ô Kế hoạch kiểm kê.'])

    d.phan('CHỌN PHẠM VI, LẤY VỊ TRÍ VÀ ĐVT KIỂM KÊ')
    d.step(['Bước 1: Ở màn Tạo (không chọn kế hoạch), chọn Kho vật lý ', '@o_kho_form'])
    d.step('Bước 2: Tick Nhà → Dãy → Khoang → Vị trí cần kiểm (gồm nhóm Vị trí tự do).')
    d.img('10d_scope', 'Khối Phạm vi kiểm kê')
    d.sub('Hoặc gõ vào ô tìm của cột để tìm theo mã / tên, tick Chọn hết để chọn mọi mục đang hiện.')
    d.step(['Bước 3: Bấm ', '@btn_layvitri', '. Hệ thống đổ hàng tồn theo từng lô vào bảng Chi tiết.'])
    d.step(['Bước 4: Ở cột ĐVT kiểm kê ', '@o_dvt', ', chọn đơn vị cần đếm; hệ thống tự tách dòng của lô.'])
    d.step('Bước 5: Đổi Kho vật lý khi bảng Chi tiết đã có dữ liệu: hệ thống hỏi “Đổi kho vật lý”.')
    d.sub(['Bấm ', '@btn_doikho', ' để đổi kho hoặc ', '@btn_huy_doikho', ' để giữ kho cũ.'])

    d.phan('LƯU VÀ GỬI PHIẾU')
    d.step('Bước 1: Ở màn Tạo hoặc Sửa phiếu, nhập đủ thông tin như PHẦN 2.')
    d.step(['Bước 2: Bấm ', '@btn_luugui', '. Phiếu chuyển trạng thái Đang kiểm ', '@badge_dangkiem'])
    d.img('10b_validate', 'Thiếu thông tin bắt buộc: hệ thống báo lỗi đỏ dưới từng ô')
    d.step('Bước 3: Nếu thiếu thông tin, nhập bổ sung các ô viền đỏ rồi bấm lại.')

    d.phan('CHỈNH SỬA')
    d.step('Bước 1: Truy cập vào màn hình Kiểm kê theo vị trí.')
    d.step(['Bước 2: Ở dòng phiếu Đang tạo ', '@badge_dangtao', ' của mình, bấm ', '@btn_sua_row', ' ở cột Hành động'])
    d.sub(['Hoặc tại màn chi tiết, bấm ', '@btn_sua'])
    d.step('Bước 3: Hệ thống mở màn “Sửa phiếu kiểm kê theo vị trí”.')
    d.img('12_edit', 'Màn hình Sửa phiếu kiểm kê theo vị trí')
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

    d.phan('NHẬP KẾT QUẢ KIỂM KÊ')
    d.step(['Bước 1: Ở dòng phiếu Đang kiểm ', '@badge_dangkiem', ' của mình, bấm ', '@btn_nhapkq_row'])
    d.img('14_result', 'Màn chi tiết phiếu ở bước Nhập kết quả')
    d.step(['Bước 2: Nhập Thực kiểm ', '@o_thuckiem', ' cho từng dòng (bắt buộc).'])
    d.step(['Bước 3: Dòng có Chênh lệch khác 0: nhập Ghi chú ', '@o_ghichu_kq', ' (bắt buộc), tick Tổng kiểm kê ', '@o_tongkiemke',
            ' nếu cần.'])
    d.step('Bước 4: Ở khối File đính kèm, bấm Thêm tài liệu để đính kèm biên bản (bắt buộc nếu phiếu chưa có file).')
    d.step(['Bước 5: Bấm ', '@btn_luukq', '. Phiếu chuyển Chờ duyệt kết quả ', '@badge_choduyet'])
    d.sub(['Hoặc ', '@btn_quaylai', ' để không lưu.'])

    d.phan('DUYỆT KẾT QUẢ')
    d.step(['Bước 1: (Ban kiểm soát) Ở dòng phiếu Chờ duyệt kết quả, bấm ', '@btn_duyet_row', ' hoặc bấm thông báo để mở chi tiết.'])
    d.step(['Bước 2: Bấm ', '@btn_duyet', ' ở chân màn chi tiết.'])
    d.img('15_approve', 'Popup Duyệt kết quả kiểm kê')
    d.step('Bước 3: Nhập Ghi chú duyệt (không bắt buộc).')
    d.step(['Bước 4: Bấm ', '@btn_duyet_popup'])
    d.sub(['Hoặc bấm ', '@btn_huy_popup', ' để không duyệt.'])

    d.phan('KHÔNG DUYỆT KẾT QUẢ')
    d.step(['Bước 1: (Ban kiểm soát) Mở chi tiết phiếu Chờ duyệt kết quả, bấm ', '@btn_khongduyet'])
    d.img('15b_reject', 'Popup Không duyệt kết quả kiểm kê')
    d.step('Bước 2: Nhập lý do vào Ghi chú duyệt (bắt buộc).')
    d.step(['Bước 3: Bấm ', '@btn_khongduyet_popup', '. Phiếu trả về Đang kiểm.'])
    d.sub(['Hoặc bấm ', '@btn_huy_popup', ' để hủy thao tác.'])

    d.phan('XỬ LÝ PHIẾU')
    d.step(['Bước 1: (Người xử lý) Ở dòng phiếu Chờ xử lý ', '@badge_choxuly', ', bấm ', '@btn_dieuchuyen_row',
            ' hoặc bấm thông báo để mở chi tiết.'])
    d.img('16_handle', 'Màn chi tiết phiếu Chờ xử lý')
    d.step(['Bước 2: Tick Tổng kiểm kê ', '@o_tongkiemke', ' ở dòng thiếu không cần điều chuyển (lưu ngay).'])
    d.step(['Bước 3: Bấm ', '@btn_dieuchuyen', ' để lập phiếu điều chuyển vị trí cho các dòng thiếu còn lại.'])
    d.step(['Bước 4: Khi không còn dòng cần điều chuyển, bấm ', '@btn_hoanthanh', ', rồi bấm ', '@btn_confirm_hoanthanh', ' để xác nhận.'])
    d.sub(['Hoặc bấm ', '@btn_huy_confirm', ' để hủy.'])

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
    d.step('Bước 1: Truy cập vào màn hình Kiểm kê theo vị trí.')
    d.step(['Bước 2: Bấm vào Số phiếu ', '@link_sophieu', '. Hệ thống mở màn “Chi tiết phiếu kiểm kê theo vị trí”.'])
    d.img('17_detail', 'Màn hình Chi tiết phiếu kiểm kê theo vị trí')
    d.sub(['Bấm mã kế hoạch ', '@link_kehoach', ' để mở kế hoạch ở tab mới.'])
    d.step(['Bước 3: Bấm ', '@btn_quaylai', ' để về màn danh sách.'])

    d.phan('IN PHIẾU')
    d.step(['Bước 1: Ở cột Hành động, bấm ', '@btn_in_row'])
    d.sub(['Hoặc tại màn chi tiết, bấm ', '@btn_in'])
    d.step('Bước 2: Hệ thống mở cửa sổ xem trước bản in.')
    d.img('18_print', 'Cửa sổ Xem trước phiếu kiểm kê theo vị trí')
    d.step(['Bước 3: Bấm ', '@btn_in_preview', ' để in.'])

    d.phan('IN DANH SÁCH')
    d.step('Bước 1: Lọc danh sách theo đúng dữ liệu cần in (xem PHẦN 1).')
    d.step(['Bước 2: Bấm ', '@btn_in_list', '. Hệ thống mở cửa sổ xem trước danh sách.'])
    d.img('19_printlist', 'Cửa sổ Xem trước danh sách kiểm kê theo vị trí')
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
