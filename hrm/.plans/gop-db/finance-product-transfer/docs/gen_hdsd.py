# -*- coding: utf-8 -*-
"""HDSD_Phiếu điều chuyển hàng — bản GỌN form quốc gia (khuôn màn mẫu phiếu finance-declare-debt-beginning/docs/kh).
Ảnh + icon: hdsd_shots/ (capture.js). Sơ đồ: uml/overview.png (gen_srs.py vẽ).
Chạy:  python gen_hdsd.py [--no-word]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..', '..', 'xuat-tai-lieu-chuyen-doi')))
import _lib_phieu as L  # noqa: E402

TEN = 'Phiếu điều chuyển hàng'
OUT = os.path.join(HERE, 'HDSD_%s.docx' % TEN)
PDF = os.path.join(HERE, 'out', 'HDSD_%s.pdf' % TEN)
VAO = 'Bước 1: Truy cập vào màn hình %s.' % TEN
HUY = ('sub', 'Hoặc bấm {icon:btn_huy_confirm} nếu bấm nhầm.')

H = {
    'ten': TEN,
    'thuat_ngu': [
        ['Kho vật lý', 'Kho thực tế chứa hàng; mỗi kho vật lý có nhiều kho kế toán.'],
        ['Kho xuất / Kho nhập', 'Kho kế toán bị trừ tồn / được cộng tồn khi phiếu được duyệt (hạch toán). Cả hai phải thuộc cùng kho vật lý.'],
        ['Đang tạo', 'Phiếu đã lưu nháp, chưa tác động tồn kho; chỉ người lập nhìn thấy, còn sửa, xóa được.'],
        ['Đã hạch toán', 'Phiếu đã duyệt: đã chuyển tồn từ kho xuất sang kho nhập, đã ghi sổ Nợ 156 / Có 156; không sửa, không xóa được.'],
        ['SL tồn', 'Số lượng còn có thể chuyển ở kho xuất, tính theo đơn vị tính đang chọn.'],
    ],
    'phien_ban': [['1.0', L.NGAY, 'Đội phát triển phần mềm', 'Phát hành lần đầu']],
    'quyen': [
        'Người dùng có quyền "Kế toán kho" được lập phiếu, lưu nháp, lưu và duyệt (hạch toán); sửa, xóa phiếu Đang tạo do chính mình lập.',
        'Xem danh sách, chi tiết, lịch sử, in, xuất Excel theo phạm vi: "Xem phiếu điều chuyển hàng theo - tổng công ty" (mọi công ty), "… - công ty" (công ty mình); không có quyền xem nào thì chỉ thấy phiếu do mình lập.',
        'Phiếu Đang tạo chỉ người lập nhìn thấy. Phiếu đã duyệt không hủy được — muốn trả hàng về kho cũ thì lập phiếu điều chuyển ngược lại.',
    ],
    'phan': [
        ('TRUY CẬP VÀ TÌM KIẾM', [
            ('step', 'Bước 1: Từ phân hệ Tài chính {icon:menu_phanhe}, tại menu Hàng hoá - Dịch vụ - Vận chuyển {icon:menu_nhom}, nhóm Điều chuyển {icon:menu_nhom2}, chọn Phiếu điều chuyển hàng {icon:menu_muc}'),
            ('img', '01_list', 'Màn hình danh sách Phiếu điều chuyển hàng'),
            ('step', 'Bước 2: Nhập số phiếu vào ô tìm kiếm nhanh {icon:o_timnhanh}'),
            ('step', 'Bước 3: Nhấn {icon:btn_timkiem}'),
            ('step', 'Bước 4: Bấm {icon:btn_timkiemnangcao}, chọn kho vật lý ở {icon:o_khovatly}'),
            ('sub', 'Hoặc chọn {icon:o_khoxuat}, {icon:o_khonhap} để lọc theo kho kế toán'),
            ('sub', 'Hoặc chọn {icon:o_trangthai} để lọc Đang tạo / Đã hạch toán'),
            ('sub', 'Hoặc chọn {icon:o_nguoitao} để lọc theo người lập'),
            ('sub', 'Hoặc nhập {icon:o_mahang}, {icon:o_tenhang} rồi nhấn Enter để tìm phiếu có hàng hóa đó'),
            ('sub', 'Hoặc chọn khoảng ngày {icon:o_ngaytao}, {icon:o_ngayhachtoan}'),
            ('sub', 'Hoặc chọn Công ty / Phòng ban / Bộ phận của người lập phiếu'),
            ('img', '02_filter', 'Khu vực Tìm kiếm nâng cao'),
            ('step', 'Bước 5: Chọn {icon:btn_lammoi} để xóa giá trị đã lọc'),
            ('step', 'Bước 6: Bấm {icon:btn_caidatboloc} để chọn ô lọc hiển thị và thứ tự ô lọc, bấm Lưu để áp dụng.'),
        ]),
        ('LẬP PHIẾU ĐIỀU CHUYỂN HÀNG', [
            ('step', VAO),
            ('step', 'Bước 2: Bấm {icon:btn_taomoi} (chỉ có khi được cấp quyền Kế toán kho)'),
            ('img', '10_create', 'Trang Thêm phiếu điều chuyển hàng'),
            ('step', 'Bước 3: Nhập thông tin chung:'),
            ('sub2', 'Bắt buộc: Kho vật lý. Chọn xong thì ô Kho xuất, Kho nhập mới mở và chỉ hiện kho kế toán của kho vật lý đó.'),
            ('sub2', 'Bắt buộc khi duyệt: Kho xuất, Kho nhập (không được trùng nhau).'),
            ('sub2', 'Tùy chọn: Ghi chú; File đính kèm (bấm Thêm tài liệu, nhận pdf, png, jpg, jpeg, tối đa 20MB mỗi tệp).'),
            ('sub2', 'Tự điền: người lập và ngày giờ ở góc phải khối; Số phiếu hệ thống sinh khi lưu.'),
            ('sub2', 'Đổi Kho vật lý thì Kho xuất, Kho nhập và các dòng hàng đã chọn bị xóa.'),
            ('img', '10a_create_kho', 'Đã chọn đủ 3 kho, nút Thêm hàng hóa hiện ra'),
            ('step', 'Bước 4: Bấm {icon:btn_themhang}, tìm và tích các hàng cần chuyển rồi bấm "Thêm n hàng hoá".'),
            ('img', '14_picker', 'Cửa sổ Thêm hàng hoá'),
            ('sub2', 'Hàng đã có trong phiếu hoặc hàng ngoài danh mục (hàng tạm) sẽ không được thêm.'),
            ('step', 'Bước 5: Nhập từng dòng hàng:'),
            ('sub2', 'Bắt buộc khi duyệt: SL chuyển (lớn hơn 0, không vượt SL tồn), ĐVT (mặc định đơn vị cơ bản).'),
            ('sub2', 'Tự điền: Tên hàng hóa, Model, Mã hàng, SL tồn của kho xuất theo ĐVT đang chọn, TK nợ / TK có = 156.'),
            ('sub2', 'Nhập vượt tồn hệ thống báo đỏ dưới ô, giữ nguyên số đã nhập để bạn sửa lại.'),
            ('sub2', 'Bấm {icon:btn_xoadong} cuối dòng để bỏ dòng, xác nhận ở hộp "Xác nhận xóa hàng hóa".'),
            ('img', '10b_create_filled', 'Phiếu đã có 2 dòng hàng, dòng 2 nhập vượt tồn bị báo đỏ'),
            ('step', 'Bước 6: Bấm {icon:btn_luunhap} để lưu phiếu ở trạng thái Đang tạo và về danh sách. Lưu nháp CHƯA trừ / cộng tồn kho, phiếu vẫn sửa, xóa được.'),
            ('sub', 'Hoặc {icon:btn_luutieptuc} để lưu nháp rồi lập tiếp phiếu khác.'),
            ('sub', 'Hoặc {icon:btn_luuduyet} để lưu và hạch toán ngay (xem PHẦN LƯU VÀ DUYỆT PHIẾU).'),
            ('sub', 'Hoặc {icon:btn_quaylai} để không lưu.'),
        ]),
        ('LƯU VÀ DUYỆT PHIẾU', [
            ('step', 'Bước 1: Tại trang Thêm, hoặc trang Sửa của phiếu Đang tạo, nhập đủ Kho vật lý, Kho xuất, Kho nhập và ít nhất 1 dòng hàng có SL chuyển, ĐVT.'),
            ('step', 'Bước 2: Bấm {icon:btn_luuduyet}. Hệ thống hiện hộp "Xác nhận lưu và duyệt".'),
            ('img', '15b_approve_confirm', 'Hộp Xác nhận lưu và duyệt'),
            ('step', 'Bước 3: Bấm {icon:btn_xacnhan}. Hệ thống trừ tồn kho xuất, cộng tồn kho nhập, tính giá vốn từng dòng, ghi sổ Nợ 156 / Có 156; phiếu chuyển Đã hạch toán và không sửa, xóa được nữa.'),
            ('sub', 'Hoặc bấm Hủy để quay lại form, chưa lưu gì.'),
            ('sub2', 'Hàng đang kiểm kho hoặc vượt tồn thì hệ thống báo lỗi, không lưu, không hạch toán.'),
        ]),
        ('SỬA PHIẾU', [
            ('step', VAO),
            ('step', 'Bước 2: Bấm {icon:btn_sua} ở cột Hành động của phiếu Đang tạo do bạn lập (phiếu Đã hạch toán không có nút Sửa).'),
            ('img', '12_edit', 'Trang Sửa phiếu điều chuyển hàng'),
            ('step', 'Bước 3: Sửa kho, ghi chú, tệp đính kèm, dòng hàng (quy tắc nhập như khi lập).'),
            ('step', 'Bước 4: Bấm {icon:btn_luunhap} để lưu, hoặc {icon:btn_luuduyet} để lưu và hạch toán.'),
            ('sub', 'Hoặc {icon:btn_quaylai} nếu muốn hủy.'),
        ]),
        ('XEM CHI TIẾT PHIẾU', [
            ('step', VAO),
            ('step', 'Bước 2: Bấm vào Số phiếu. Hệ thống mở trang "Chi tiết phiếu điều chuyển hàng"; phiếu đã hạch toán có thêm Đơn giá vốn, Thành tiền vốn.'),
            ('img', '17_detail', 'Trang Chi tiết phiếu Đã hạch toán'),
            ('step', 'Bước 3: Bấm {icon:btn_inphieu_footer} để in, hoặc {icon:btn_sua_footer} / {icon:btn_xoa_footer} (chỉ có với phiếu Đang tạo do bạn lập), hoặc {icon:btn_quaylai} để về danh sách.'),
        ]),
        ('XÓA PHIẾU', [
            ('step', 'Bước 1: Bấm {icon:btn_xoa} ở cột Hành động (hoặc nút Xóa ở trang Chi tiết) của phiếu Đang tạo do bạn lập.'),
            ('step', 'Bước 2: Hệ thống hiện hộp "Xác nhận xóa"'),
            ('img', '13_delete', 'Hộp Xác nhận xóa phiếu'),
            ('step', 'Bước 3: Bấm {icon:btn_confirm_xoa} để xác nhận. Phiếu, các dòng hàng và tệp đính kèm bị xóa.'),
            HUY,
        ]),
        ('IN PHIẾU', [
            ('step', 'Bước 1: Ở cột Hành động bấm {icon:btn_inphieu} (với phiếu Đang tạo nút nằm trong {icon:btn_khac}), hoặc bấm In phiếu ở trang Chi tiết.'),
            ('img', '19b_printitem', 'Cửa sổ xem trước phiếu điều chuyển hàng'),
            ('step', 'Bước 2: Bấm {icon:btn_in} để in.'),
        ]),
        ('IN DANH SÁCH', [
            ('step', 'Bước 1: Lọc danh sách theo đúng dữ liệu cần in (xem PHẦN 1).'),
            ('step', 'Bước 2: Bấm {icon:btn_indanhsach}. Hệ thống mở cửa sổ xem trước "Danh sách phiếu điều chuyển hàng".'),
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
            ('step', 'Bước 5: Mở file Excel đã tải về (Danh-sach-phieu-dieu-chuyen-hang-<ngày>.xlsx).'),
        ]),
        ('XEM LỊCH SỬ THAY ĐỔI', [
            ('p', 'Cách 1: Xem từ màn danh sách:'),
            ('step', 'Ở cột Hành động, bấm {icon:btn_lichsu_row}'),
            ('img', '16_history', 'Cửa sổ Lịch sử thay đổi'),
            ('p', 'Cách 2: Xem từ màn chi tiết:'),
            ('step', 'Bước 1: Bấm vào số phiếu để mở trang Chi tiết'),
            ('step', 'Bước 2: Tại khối Lịch sử cuối trang, bấm {icon:btn_xemlichsu}'),
        ]),
        ('TÙY CHỈNH CỘT HIỂN THỊ', [
            ('step', 'Bước 1: Ở màn danh sách, bấm biểu tượng {icon:btn_cauhinhcot}'),
            ('img', '25_colcfg', 'Cửa sổ Tùy chỉnh cột'),
            ('step', 'Bước 2: Tích để hiện cột, bỏ tích để ẩn cột (STT, Số phiếu, Hành động luôn hiện).'),
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
