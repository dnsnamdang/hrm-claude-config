# -*- coding: utf-8 -*-
"""HDSD_Phiếu huỷ hàng giữ kế toán — bản GỌN form quốc gia, chép khuôn màn mẫu finance-declare-debt-beginning/docs/kh/gen_hdsd.py.
Ảnh + icon: hdsd_shots/ (capture.js). Sơ đồ: uml/overview.png (gen_srs.py vẽ).
Chạy:  python gen_hdsd.py [--no-word]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..', '..', 'xuat-tai-lieu-chuyen-doi')))
import _lib_phieu as L  # noqa: E402

TEN = 'Phiếu huỷ hàng giữ kế toán'
OUT = os.path.join(HERE, 'HDSD_%s.docx' % TEN)
PDF = os.path.join(HERE, 'out', 'HDSD_%s.pdf' % TEN)
VAO = 'Bước 1: Truy cập vào màn hình %s.' % TEN

H = {
    'ten': TEN,
    'thuat_ngu': [
        ['Hàng giữ', 'Hàng hoá nhân viên kinh doanh đang giữ cho khách hàng, chia theo lô có hạn giữ.'],
        ['Phiếu huỷ hàng giữ kế toán', 'Phiếu kế toán lập để huỷ hàng đang giữ của 1 nhân viên, không cần phiếu yêu cầu; mã KTPHHG-xxxxx.'],
        ['Hủy của nhân viên', 'Nhân viên bị huỷ hàng giữ (khác Người tạo là kế toán lập phiếu).'],
        ['Có thể hủy', 'Số đang giữ cho 1 khách hàng, đã trừ phần đang chờ xuất kho, quy theo đơn vị tính đang chọn.'],
        ['Duyệt hủy', 'Số lượng huỷ nhập trên phiếu.'],
        ['ĐVT', 'Đơn vị tính.'],
    ],
    'phien_ban': [['1.0', L.NGAY, 'Đội phát triển phần mềm', 'Phát hành lần đầu']],
    'quyen': [
        'Người dùng có quyền "Quản lý giữ hàng" được dùng mọi chức năng của màn hình: xem, tìm kiếm, lập phiếu (Duyệt), xem chi tiết, xem lịch sử, in phiếu, in danh sách, xuất Excel, tùy chỉnh cột.',
        'Người dùng chỉ thấy phiếu do kế toán cùng công ty lập; tài khoản quản trị cao nhất thấy phiếu mọi công ty và có thêm ô lọc Công ty.',
        'Phiếu không có bước lưu nháp: bấm Duyệt là lưu phiếu và trừ hàng giữ của nhân viên ngay, sau đó không sửa, không xóa được.',
    ],
    'phan': [
        ('TRUY CẬP VÀ TÌM KIẾM', [
            ('step', 'Bước 1: Từ phân hệ Tài chính {icon:menu_phanhe}, tại menu Hàng hoá - Dịch vụ - Vận chuyển {icon:menu_nhom}, chọn nhóm Giữ hàng {icon:menu_nhom2}, chọn Phiếu huỷ hàng giữ kế toán {icon:menu_muc}'),
            ('img', '01_list', 'Màn hình danh sách Phiếu huỷ hàng giữ kế toán'),
            ('step', 'Bước 2: Nhập mã phiếu vào ô tìm kiếm nhanh {icon:o_timnhanh}'),
            ('step', 'Bước 3: Nhấn {icon:btn_timkiem}'),
            ('step', 'Bước 4: Bấm {icon:btn_timkiemnangcao}, chọn nhân viên bị huỷ hàng ở {icon:o_nhanvien}'),
            ('sub', 'Hoặc chọn {icon:o_nguoitao} để lọc theo kế toán lập phiếu'),
            ('sub', 'Hoặc nhập tên hoặc mã hàng ở {icon:o_hanghoa} để tìm phiếu có hàng đó'),
            ('sub', 'Hoặc chọn khoảng ngày {icon:o_ngaytao}'),
            ('sub', 'Hoặc chọn {icon:o_congty} (chỉ hiện với tài khoản quản trị cao nhất)'),
            ('img', '02_filter', 'Khu vực Tìm kiếm nâng cao'),
            ('step', 'Bước 5: Chọn {icon:btn_lammoi} để xóa giá trị đã lọc'),
            ('step', 'Bước 6: Bấm {icon:btn_caidatboloc} để chọn ô lọc hiển thị và thứ tự ô lọc, bấm Lưu để áp dụng.'),
        ]),
        ('LẬP PHIẾU HUỶ HÀNG GIỮ KẾ TOÁN', [
            ('step', VAO),
            ('step', 'Bước 2: Bấm {icon:btn_taomoi}'),
            ('img', '10_create', 'Trang Thêm phiếu hủy hàng giữ kế toán'),
            ('step', 'Bước 3: Chọn "Hủy của nhân viên" (bắt buộc) — nhân viên có hàng giữ cần huỷ. Nhập Ghi chú nếu cần (tùy chọn, tối đa 255 ký tự).'),
            ('step', 'Bước 4: Bấm {icon:btn_themhang}. Hệ thống mở cửa sổ "Hàng đang giữ của nhân viên".'),
            ('img', '14_picker', 'Cửa sổ Hàng đang giữ của nhân viên'),
            ('step', 'Bước 5: Tích các hàng cần huỷ (có thể lọc theo Mã / Tên hàng hóa), bấm {icon:btn_chon}'),
            ('sub2', 'Nhân viên không giữ hàng nào thì cửa sổ ghi "Nhân viên này hiện không giữ hàng hóa nào."'),
            ('sub2', 'Hàng đã có trên phiếu không hiện lại trong cửa sổ.'),
            ('step', 'Bước 6: Nhập thông tin từng dòng hàng hoá:'),
            ('sub2', 'Bắt buộc: Khách hàng (tự chọn sẵn khách đầu tiên), Duyệt hủy (số lớn hơn 0, không vượt cột Có thể hủy, tối đa 2 chữ số thập phân, dùng dấu chấm), Đơn vị tính (mặc định đơn vị cơ bản).'),
            ('sub2', 'Đổi Đơn vị tính thì cột Có thể hủy tự quy đổi theo đơn vị mới.'),
            ('sub2', 'Bấm {icon:link_themkhach} để huỷ thêm cho khách khác của cùng hàng; bấm {icon:btn_xoakhach} cạnh ô Khách hàng để bỏ khách, thùng rác cuối dòng để bỏ cả hàng hoá.'),
            ('sub2', 'Tự điền: Tên hàng hóa, Model, Mã hàng hóa, Thương hiệu, Có thể hủy; Mã phiếu hệ thống sinh khi duyệt; người lập và ngày giờ ở góc phải.'),
            ('img', '10b_create_filled', 'Đã chọn 2 hàng hoá, hàng 1 huỷ cho 2 khách, hàng 2 dùng đơn vị Túi'),
            ('sub2', 'Nhập vượt Có thể hủy thì ô báo đỏ "Vượt quá số có thể hủy (tối đa …)", cần sửa lại số.'),
            ('img', '10c_over', 'Báo đỏ khi nhập vượt số có thể hủy'),
            ('step', 'Bước 7: Bấm {icon:btn_duyet}. Hệ thống hiện hộp "Xác nhận duyệt".'),
            ('img', '13_confirm', 'Hộp Xác nhận duyệt'),
            ('step', 'Bước 8: Bấm {icon:btn_confirm_duyet} để lưu phiếu. Hàng giữ của nhân viên bị trừ ngay theo lô có hạn giữ sớm trước, nhân viên nhận thông báo; phiếu không sửa, không xóa được nữa.'),
            ('sub', 'Hoặc bấm {icon:btn_huy_confirm} để quay lại form.'),
            ('sub', 'Hoặc {icon:btn_luutieptuc} để duyệt phiếu này rồi lập tiếp phiếu khác.'),
            ('sub', 'Hoặc {icon:btn_quaylai} để không lưu; đã nhập dữ liệu thì bấm {icon:btn_thoat} để thoát hoặc {icon:btn_olai} để ở lại.'),
            ('sub2', 'Đổi nhân viên khi đã có hàng hoá thì hệ thống hỏi lại vì toàn bộ hàng hoá đã chọn sẽ bị xóa.'),
        ]),
        ('XEM CHI TIẾT PHIẾU', [
            ('step', VAO),
            ('step', 'Bước 2: Bấm vào Mã phiếu. Hệ thống mở trang "Chi tiết phiếu hủy hàng giữ kế toán".'),
            ('img', '17_detail', 'Trang Chi tiết phiếu'),
            ('step', 'Bước 3: Bấm {icon:btn_in_footer} để in phiếu, hoặc {icon:btn_quaylai} để về danh sách.'),
        ]),
        ('IN PHIẾU', [
            ('step', 'Bước 1: Ở cột Hành động bấm {icon:btn_in_row} (hoặc nút In ở trang Chi tiết). Hệ thống mở cửa sổ xem trước bản in.'),
            ('img', '19_print', 'Cửa sổ xem trước bản in phiếu'),
            ('step', 'Bước 2: Bấm {icon:btn_in} để in.'),
        ]),
        ('IN DANH SÁCH', [
            ('step', 'Bước 1: Lọc danh sách theo đúng dữ liệu cần in (xem PHẦN 1).'),
            ('step', 'Bước 2: Bấm {icon:btn_indanhsach} trên thanh công cụ. Hệ thống mở cửa sổ "Xem trước danh sách phiếu hủy hàng giữ kế toán".'),
            ('img', '19b_printlist', 'Cửa sổ xem trước bản in danh sách'),
            ('step', 'Bước 3: Bấm {icon:btn_in} để in.'),
        ]),
        ('XUẤT DANH SÁCH RA EXCEL', [
            ('step', 'Bước 1: Lọc danh sách theo đúng dữ liệu cần lấy (xem PHẦN 1).'),
            ('step', 'Bước 2: Bấm {icon:btn_xuatexcel}. Hệ thống mở cửa sổ "Chọn trường xuất Excel".'),
            ('img', '20_export', 'Cửa sổ Chọn trường xuất Excel'),
            ('step', 'Bước 3: Tích chọn, kéo biểu tượng ba gạch để đổi vị trí các trường cần xuất.'),
            ('sub', 'Hoặc bấm {icon:btn_chontatca} / {icon:btn_bochonhet} để chọn / bỏ chọn nhanh.'),
            ('step', 'Bước 4: Bấm {icon:btn_xuatfile}'),
            ('step', 'Bước 5: Mở file Excel đã xuất (danh_sach_huy_hang_giu_ke_toan.xlsx).'),
        ]),
        ('XEM LỊCH SỬ THAY ĐỔI', [
            ('p', 'Cách 1: Xem từ màn danh sách:'),
            ('step', 'Ở cột Hành động, bấm {icon:btn_lichsu_row}'),
            ('img', '16_history', 'Cửa sổ Lịch sử phiếu'),
            ('p', 'Cách 2: Xem từ màn chi tiết:'),
            ('step', 'Bước 1: Bấm vào mã phiếu để mở trang Chi tiết'),
            ('step', 'Bước 2: Tại khối Lịch sử thay đổi cuối trang, bấm {icon:btn_xemlichsu}'),
            ('sub2', 'Phiếu chỉ có mốc Tạo mới kèm số lô hàng giữ đã bị trừ; phiếu chuyển từ hệ thống cũ không có lịch sử.'),
        ]),
        ('TÙY CHỈNH CỘT HIỂN THỊ', [
            ('step', 'Bước 1: Ở màn danh sách, bấm biểu tượng {icon:btn_cauhinhcot}'),
            ('img', '25_colcfg', 'Cửa sổ Tùy chỉnh cột'),
            ('step', 'Bước 2: Tích để hiện cột, bỏ tích để ẩn cột (STT, Mã phiếu, Hành động luôn hiện; Ghi chú mặc định ẩn).'),
            ('step', 'Bước 3: Bấm {icon:btn_chontatca} để hiện tất cả các cột.'),
            ('sub', 'Hoặc bấm {icon:btn_bochonhet} để ẩn tất cả các cột (trừ các cột bắt buộc).'),
            ('step', 'Bước 4: Kéo biểu tượng ba gạch ở mỗi dòng để đổi thứ tự cột.'),
            ('step', 'Bước 5: Bấm Lưu để áp dụng, hoặc Đóng nếu muốn bỏ thay đổi.'),
        ]),
    ],
}

if __name__ == '__main__':
    scr = L.Screen(HERE)
    L.shorten_field_icons(scr)
    print('docx:', L.build_hdsd(scr, H, OUT))
    if '--no-word' not in sys.argv:
        L.finalize_and_check(OUT, PDF, extra_banned=('ERP', 'API'))
