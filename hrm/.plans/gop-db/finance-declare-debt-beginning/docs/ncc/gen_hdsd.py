# -*- coding: utf-8 -*-
"""HDSD_Khai báo đầu kỳ công nợ nhà cung cấp — bản GỌN form quốc gia, chép khuôn màn mẫu ../kh/gen_hdsd.py.
Ảnh + icon: hdsd_shots/ (capture.js). Sơ đồ: uml/overview.png (gen_srs.py vẽ).
Chạy:  python gen_hdsd.py [--no-word]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..', '..', '..', 'xuat-tai-lieu-chuyen-doi')))
import _lib_phieu as L  # noqa: E402

TEN = 'Khai báo đầu kỳ công nợ nhà cung cấp'
OUT = os.path.join(HERE, 'HDSD_%s.docx' % TEN)
PDF = os.path.join(HERE, 'out', 'HDSD_%s.pdf' % TEN)
VAO = 'Bước 1: Truy cập vào màn hình %s.' % TEN
HUY = ('sub', 'Hoặc bấm {icon:btn_huy_confirm} nếu bấm nhầm.')

H = {
    'ten': TEN,
    'thuat_ngu': [
        ['Khai báo đầu kỳ công nợ nhà cung cấp', 'Số dư công nợ của 1 nhà cung cấp trên 1 hợp đồng mua ở 1 tài khoản tại ngày khai báo đầu kỳ; mỗi khai báo có 1 mã phiếu.'],
        ['Dư nợ / Dư có', 'Ghi Nợ tài khoản (nhà cung cấp còn nợ công ty) / ghi Có tài khoản (công ty còn nợ nhà cung cấp).'],
        ['Công nợ / Tỷ giá / Quy đổi (VND)', 'Công nợ nhập theo loại tiền đã chọn (nguyên tệ); Quy đổi (VND) = Công nợ × Tỷ giá. VNĐ có tỷ giá 1.'],
        ['Ngày khai báo đầu kỳ', 'Mốc ngày khai ở Khai Quy chế – Cấu hình của công ty; mọi khai báo hạch toán vào ngày này.'],
        ['Chưa phát sinh chứng từ', 'Khai báo chưa có phiếu chi, ủy nhiệm chi, phiếu thu, phiếu báo có, phiếu kế toán nào trên cùng nhà cung cấp + hợp đồng + tài khoản — còn Sửa, Xóa được.'],
        ['Đã phát sinh chứng từ', 'Đã có chứng từ công nợ như trên — khai báo chỉ còn xem, không Sửa, không Xóa.'],
    ],
    'phien_ban': [['1.0', L.NGAY, 'Đội phát triển phần mềm', 'Phát hành lần đầu']],
    'quyen': [
        'Mọi người dùng đã đăng nhập đều vào được màn hình để xem, tìm kiếm, xem chi tiết, xem lịch sử, in danh sách, xuất Excel, tùy chỉnh cột.',
        'Quyền "Khai báo thêm công nợ đầu kỳ nhà cung cấp": Tạo mới, Import Excel. Quyền "Khai báo sửa công nợ đầu kỳ nhà cung cấp": Sửa. Quyền "Khai báo xoá công nợ đầu kỳ nhà cung cấp": Xóa.',
        'Dữ liệu được xem theo quyền phạm vi: "Xem tất cả công nợ đầu kỳ" (mọi công ty), "… của công ty", "… của phòng ban", "… của bộ phận"; không có quyền phạm vi nào thì chỉ thấy khai báo do mình tạo.',
        'Khai báo không qua bước duyệt: lưu xong là có hiệu lực và đã ghi vào sổ chi tiết công nợ.',
    ],
    'phan': [
        ('TRUY CẬP VÀ TÌM KIẾM', [
            ('step', 'Bước 1: Từ phân hệ Tài chính {icon:menu_phanhe}, tại menu Khai báo đầu kỳ {icon:menu_nhom}, chọn Khai báo đầu kỳ công nợ nhà cung cấp {icon:menu_muc}'),
            ('img', '01_list', 'Màn hình danh sách Khai báo đầu kỳ công nợ nhà cung cấp'),
            ('step', 'Bước 2: Nhập mã phiếu, số hợp đồng, mã hoặc tên nhà cung cấp vào ô tìm kiếm nhanh {icon:o_timnhanh}'),
            ('step', 'Bước 3: Nhấn {icon:btn_timkiem}'),
            ('step', 'Bước 4: Bấm {icon:btn_timkiemnangcao}, gõ ít nhất 2 ký tự rồi chọn nhà cung cấp ở {icon:o_ncc}'),
            ('sub', 'Hoặc chọn giá trị {icon:o_taikhoan} để lọc theo tài khoản'),
            ('sub', 'Hoặc nhập {icon:o_sohd} rồi nhấn Enter để lọc theo số hợp đồng'),
            ('sub', 'Hoặc chọn giá trị {icon:o_nguoilaphd} để lọc theo người lập hợp đồng'),
            ('sub', 'Hoặc chọn giá trị {icon:o_nguoitao}, {icon:o_nguoicapnhat}, khoảng ngày {icon:o_ngaytao}'),
            ('sub', 'Hoặc chọn Công ty / Phòng ban (chỉ hiện với người có quyền xem rộng)'),
            ('img', '02_filter', 'Khu vực Tìm kiếm nâng cao'),
            ('step', 'Bước 5: Chọn {icon:btn_lammoi} để xóa giá trị đã lọc'),
            ('step', 'Bước 6: Bấm {icon:btn_caidatboloc} để chọn ô lọc hiển thị và thứ tự ô lọc, bấm Lưu để áp dụng.'),
        ]),
        ('LẬP KHAI BÁO ĐẦU KỲ CÔNG NỢ NHÀ CUNG CẤP', [
            ('step', VAO),
            ('step', 'Bước 2: Bấm {icon:btn_taomoi} (chỉ có khi được cấp quyền thêm)'),
            ('img', '10_create', 'Trang Thêm khai báo đầu kỳ công nợ nhà cung cấp'),
            ('step', 'Bước 3: Chọn Nhà cung cấp (bắt buộc): gõ ít nhất 2 ký tự mã hoặc tên rồi chọn trong danh sách.'),
            ('sub2', 'Chưa chọn nhà cung cấp mà bấm Chọn hợp đồng, hệ thống báo đỏ "Chọn nhà cung cấp trước khi chọn hợp đồng".'),
            ('step', 'Bước 4: Bấm {icon:btn_chonhd}. Hệ thống mở cửa sổ "Chọn hợp đồng nhà cung cấp".'),
            ('img', '14_picker', 'Cửa sổ Chọn hợp đồng nhà cung cấp'),
            ('step', 'Bước 5: Bấm vào dòng hợp đồng cần khai báo — mỗi lần bấm thêm 1 dòng vào trang Thêm, cửa sổ vẫn mở để chọn tiếp; bấm Đóng khi chọn xong.'),
            ('sub2', 'Dòng ghi "Đã khai báo" (hợp đồng đã có khai báo của nhà cung cấp này) hoặc "Đã chọn" không chọn được.'),
            ('sub2', 'Có thể lọc theo Loại hợp đồng, Số hợp đồng; ô Phạm vi chọn "HĐ nhà cung cấp khác" để lấy hợp đồng của nhà cung cấp khác.'),
            ('step', 'Bước 6: Nhập thông tin từng dòng hợp đồng:'),
            ('sub2', 'Bắt buộc: Tài khoản (chọn ở 1 dòng thì các dòng chưa có tự điền theo), Loại tiền, Tỷ giá (khi khác VNĐ, lớn hơn 0), Loại dư (mặc định Dư nợ), Công nợ (số tiền theo loại tiền, lớn hơn 0).'),
            ('sub2', 'Tự điền: Loại hợp đồng, Số hợp đồng, Người lập hợp đồng theo hợp đồng; Loại tiền theo hợp đồng; Tỷ giá theo danh mục tiền tệ (VNĐ luôn 1, ô khóa); Quy đổi (VND) tự tính; Mã phiếu hệ thống sinh khi lưu.'),
            ('sub2', 'Bấm nút thùng rác cuối dòng để bỏ dòng; đổi Nhà cung cấp thì bảng hợp đồng bị xóa trắng.'),
            ('img', '10b_create_filled', 'Đã chọn 2 hợp đồng và nhập thông tin từng dòng'),
            ('step', 'Bước 7: Bấm {icon:btn_luu} để lưu và về danh sách. Mỗi dòng thành 1 khai báo có mã riêng và được ghi ngay vào sổ chi tiết công nợ.'),
            ('sub', 'Hoặc {icon:btn_luutieptuc} để lưu rồi lập tiếp khai báo khác.'),
            ('sub', 'Hoặc {icon:btn_quaylai} để không lưu; đã nhập dữ liệu thì bấm {icon:btn_thoat} để thoát hoặc {icon:btn_olai} để ở lại.'),
            ('sub2', 'Hợp đồng + tài khoản đã khai báo cho nhà cung cấp này thì hệ thống báo "Đã khai báo đầu kỳ cho tài khoản này" dưới ô Tài khoản, không lưu.'),
        ]),
        ('SỬA KHAI BÁO', [
            ('step', VAO),
            ('step', 'Bước 2: Bấm {icon:btn_sua} ở cột Hành động của khai báo Chưa phát sinh chứng từ (khai báo Đã phát sinh, hoặc khi chưa có quyền sửa, không có nút Sửa).'),
            ('img', '12_edit', 'Trang Sửa khai báo đầu kỳ công nợ nhà cung cấp'),
            ('step', 'Bước 3: Sửa Tài khoản, Loại tiền, Tỷ giá, Loại dư, Công nợ (quy tắc nhập như khi lập). Mã phiếu, Nhà cung cấp và hợp đồng không sửa được.'),
            ('step', 'Bước 4: Bấm {icon:btn_luu} để lưu; bút toán trong sổ chi tiết được cập nhật theo.'),
            ('sub', 'Hoặc {icon:btn_quaylai} nếu muốn hủy.'),
        ]),
        ('XEM CHI TIẾT KHAI BÁO', [
            ('step', VAO),
            ('step', 'Bước 2: Bấm vào Mã phiếu. Hệ thống mở trang "Chi tiết khai báo đầu kỳ công nợ nhà cung cấp".'),
            ('img', '17_detail', 'Trang Chi tiết khai báo'),
            ('step', 'Bước 3: Bấm {icon:btn_sua_footer} hoặc {icon:btn_xoa_footer} để thao tác (chỉ có khi khai báo Chưa phát sinh chứng từ và có quyền), hoặc {icon:btn_quaylai} để về danh sách.'),
        ]),
        ('XÓA KHAI BÁO', [
            ('step', 'Bước 1: Bấm {icon:btn_xoa} ở cột Hành động (hoặc nút Xóa ở trang Chi tiết) của khai báo Chưa phát sinh chứng từ.'),
            ('step', 'Bước 2: Hệ thống hiện hộp "Xác nhận xóa"'),
            ('img', '13_delete', 'Hộp Xác nhận xóa khai báo'),
            ('step', 'Bước 3: Bấm {icon:btn_confirm_xoa} để xác nhận. Khai báo và bút toán trong sổ chi tiết bị xóa.'),
            HUY,
        ]),
        ('IN DANH SÁCH', [
            ('step', 'Bước 1: Lọc danh sách theo đúng dữ liệu cần in (xem PHẦN 1).'),
            ('step', 'Bước 2: Bấm {icon:btn_indanhsach}. Hệ thống mở cửa sổ xem trước bản in "Khai báo công nợ đầu kỳ nhà cung cấp".'),
            ('img', '19_printlist', 'Cửa sổ xem trước bản in danh sách'),
            ('step', 'Bước 3: Bấm {icon:btn_in} để in. Danh sách quá 2,000 dòng thì cần lọc hẹp lại hoặc dùng Xuất Excel.'),
        ]),
        ('XUẤT DANH SÁCH RA EXCEL', [
            ('step', 'Bước 1: Lọc danh sách theo đúng dữ liệu cần lấy (xem PHẦN 1).'),
            ('step', 'Bước 2: Bấm {icon:btn_xuatexcel}. Hệ thống mở cửa sổ "Chọn trường xuất file".'),
            ('img', '20_export', 'Cửa sổ Chọn trường xuất file'),
            ('step', 'Bước 3: Tích chọn, kéo biểu tượng ☰ để đổi vị trí các trường cần xuất.'),
            ('sub', 'Hoặc bấm {icon:btn_chontatca} / {icon:btn_bochonhet} để chọn / bỏ chọn nhanh.'),
            ('step', 'Bước 4: Bấm {icon:btn_xuatfile}'),
            ('step', 'Bước 5: Mở file Excel đã xuất (khai_bao_dau_ky_cong_no_ncc.xlsx).'),
        ]),
        ('IMPORT KHAI BÁO TỪ FILE EXCEL', [
            ('step', 'Bước 1: Tại màn hình danh sách, bấm {icon:btn_import} (chỉ có khi được cấp quyền thêm). Hệ thống mở cửa sổ "Import khai báo đầu kỳ công nợ nhà cung cấp".'),
            ('img', '21_import_open', 'Cửa sổ Import khi vừa mở'),
            ('step', 'Bước 2: Bấm {icon:btn_taifilemau} để lấy file mẫu'),
            ('step', 'Bước 3: Điền dữ liệu vào file mẫu, mỗi dòng 1 khai báo, mỗi lần tối đa 500 dòng:'),
            ('sub2', 'Bắt buộc: Nhà cung cấp (mã), Mã hợp đồng mua, Loại hợp đồng mua (HDMNN, HDMN, HDMTN, HDMDK), Số tài khoản, Loại tiền (VNĐ, USD…), Công nợ (lớn hơn 0).'),
            ('sub2', 'Tùy chọn: Tỷ giá (bắt buộc khi loại tiền khác VNĐ), Loại dư (Dư nợ / Dư có, để trống = Dư nợ).'),
            ('step', 'Bước 4: Bấm {icon:btn_chonfile}, chọn file vừa điền'),
            ('step', 'Bước 5: Bấm {icon:btn_load}'),
            ('step', 'Bước 6: Bấm {icon:btn_validate} để hệ thống kiểm tra từng dòng.'),
            ('img', '23_import_validated', 'Kết quả kiểm tra — mỗi dòng lỗi nêu rõ lý do'),
            ('step', 'Bước 7:'),
            ('sub2', 'Sửa trực tiếp các dòng lỗi trên bảng rồi bấm Validate lại.'),
            ('sub2', 'Nếu không muốn nhập các dòng lỗi thì bấm {icon:btn_bodongloi}'),
            ('sub2', 'Muốn sửa lại những dòng đã khoá, bấm {icon:btn_xoavalidate}'),
            ('step', 'Bước 8: Bấm {icon:btn_import_modal} (chỉ bấm được khi không còn dòng lỗi). Hệ thống báo số dòng nhập thành công và tải lại danh sách.'),
        ]),
        ('XEM LỊCH SỬ THAY ĐỔI', [
            ('p', 'Cách 1: Xem từ màn danh sách:'),
            ('step', 'Ở cột Hành động, bấm {icon:btn_lichsu_row}'),
            ('img', '16_history', 'Cửa sổ Lịch sử thay đổi'),
            ('p', 'Cách 2: Xem từ màn chi tiết:'),
            ('step', 'Bước 1: Bấm vào mã phiếu để mở trang Chi tiết'),
            ('step', 'Bước 2: Tại khối Lịch sử cuối trang, bấm {icon:btn_xemlichsu}'),
        ]),
        ('TÙY CHỈNH CỘT HIỂN THỊ', [
            ('step', 'Bước 1: Ở màn danh sách, bấm biểu tượng {icon:btn_cauhinhcot}'),
            ('img', '25_colcfg', 'Cửa sổ Tùy chỉnh cột'),
            ('step', 'Bước 2: Tích để hiện cột, bỏ tích để ẩn cột (STT, Mã phiếu, Hành động luôn hiện).'),
            ('step', 'Bước 3: Bấm {icon:btn_chontatca} để hiện tất cả các cột.'),
            ('sub', 'Hoặc bấm {icon:btn_bochonhet} để ẩn tất cả các cột (trừ các cột bắt buộc).'),
            ('step', 'Bước 4: Kéo biểu tượng ba gạch ở cuối mỗi dòng để đổi thứ tự cột.'),
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
