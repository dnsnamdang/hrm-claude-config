# -*- coding: utf-8 -*-
"""HDSD_Danh mục kho vật lý — bản GỌN (skill hdsd-documenter, khuôn HDSD_MAU_GON.docx). MÀN MẪU cho 7 danh mục kho.
Ảnh + icon: hdsd_shots/ (capture.js). Sơ đồ: uml/overview.png (gen_srs.py vẽ).
Chạy:  python gen_hdsd.py [--no-word]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
import _lib_win as L  # noqa: E402

TEN = 'Danh mục kho vật lý'
OUT = os.path.join(HERE, 'HDSD_%s.docx' % TEN)
PDF = os.path.join(HERE, 'out', 'HDSD_%s.pdf' % TEN)
VAO = 'Bước 1: Truy cập vào màn hình %s.' % TEN
HUY = ('sub', 'Hoặc bấm {icon:btn_huy_confirm} nếu bấm nhầm.')

H = {
    'ten': TEN,
    'thuat_ngu': [
        ['Kho vật lý', 'Kho hàng thực tế, cấp gốc của cây kho: Kho vật lý → Nhà kho → Dãy → Khoang → Vị trí.'],
        ['Nhà kho', 'Cấp con của kho vật lý; khi tạo kho hệ thống tự tạo "Nhà 1"… "Nhà N" (mã N1…NN).'],
        ['Vị trí tách ghép hàng', 'Vị trí "<Mã kho>-TACH-GHEP" hệ thống tự tạo cho mỗi kho, dùng khi tách / ghép hàng.'],
        ['Thủ kho', 'Nhân viên phụ trách kho; một kho có một hoặc nhiều thủ kho.'],
        ['Trạng thái Hoạt động', 'Kho dùng được ở các màn nghiệp vụ (phiếu nhập, xuất, kiểm kê…).'],
        ['Trạng thái Khóa', 'Kho vẫn nằm trong danh mục, xem được lịch sử nhưng không còn chọn được ở các màn nghiệp vụ.'],
    ],
    'phien_ban': [['1.0', L.NGAY, 'Đội phát triển phần mềm', 'Phát hành lần đầu']],
    'quyen': [
        'Người dùng có quyền "Quản lý kho" được dùng mọi chức năng của màn hình: xem, tìm kiếm, thêm mới, chỉnh sửa, xóa, khóa / mở khóa, xem lịch sử, xem chi tiết, xuất Excel, import Excel, tùy chỉnh cột.',
        'Người dùng thường chỉ thấy kho của công ty mình; Super admin thấy kho của mọi công ty và lọc được theo Công ty.',
    ],
    'phan': [
        ('TRUY CẬP VÀ TÌM KIẾM', [
            ('step', 'Bước 1: Từ phân hệ Kho {icon:menu_phanhe}, tại menu Danh mục {icon:menu_nhom}, chọn Kho vật lý {icon:menu_muc}'),
            ('img', '01_list', 'Màn hình Danh mục kho vật lý'),
            ('step', 'Bước 2: Nhập mã kho, tên kho hoặc tên người tạo vào ô tìm kiếm nhanh {icon:o_timnhanh}'),
            ('step', 'Bước 3: Nhấn {icon:btn_timkiem}'),
            ('step', 'Bước 4: Bấm {icon:btn_timkiemnangcao}, chọn giá trị trong {icon:o_thukho} để lọc theo thủ kho'),
            ('sub', 'Hoặc chọn giá trị {icon:o_nhom} để lọc theo nhóm kho'),
            ('sub', 'Hoặc chọn giá trị {icon:o_trangthai} để lọc theo trạng thái'),
            ('sub', 'Hoặc chọn giá trị {icon:o_nguoitao} để lọc theo người tạo'),
            ('sub', 'Hoặc chọn khoảng ngày {icon:o_ngaytao} để lọc theo ngày tạo'),
            ('sub', 'Hoặc chọn giá trị {icon:o_congty} để lọc theo công ty (chỉ Super admin)'),
            ('step', 'Bước 5: Chọn {icon:btn_lammoi} để xóa giá trị đã lọc'),
        ]),
        ('THÊM MỚI KHO VẬT LÝ', [
            ('step', VAO),
            ('step', 'Bước 2: Bấm {icon:btn_taomoi}'),
            ('img', '10_create', 'Cửa sổ Tạo mới kho vật lý'),
            ('step', 'Bước 3: Nhập/ chọn đầy đủ thông tin bắt buộc: Mã kho, Tên kho, Địa chỉ, Thủ kho, Số nhà kho.'),
            ('sub2', 'Mã kho: chữ không dấu, số, dấu - và _, tối đa 50 ký tự, không trùng kho khác.'),
            ('sub2', 'Tên kho, Địa chỉ: tối đa 255 ký tự; Tên kho không trùng kho khác.'),
            ('sub2', 'Thủ kho: chọn một hoặc nhiều nhân viên.'),
            ('sub2', 'Số nhà kho: số nguyên từ 1 đến 999; hệ thống tự tạo các nhà "Nhà 1", "Nhà 2"… và vị trí tách ghép hàng.'),
            ('sub2', 'Tùy chọn: Trạng thái (mặc định Hoạt động), Mô tả (tối đa 500 ký tự).'),
            ('step', 'Bước 4: Bấm {icon:btn_luu} để lưu và đóng cửa sổ,'),
            ('sub', 'Hoặc {icon:btn_luutieptuc} để lưu rồi nhập tiếp kho khác.'),
            ('sub', 'Hoặc {icon:btn_dong} để không lưu thông tin; đã nhập dữ liệu thì bấm {icon:btn_thoat} để thoát hoặc {icon:btn_olai} để ở lại.'),
        ]),
        ('CHỈNH SỬA', [
            ('step', VAO),
            ('step', 'Bước 2: Bấm nút {icon:btn_sua} ở cột Hành động.'),
            ('step', 'Bước 3: Hệ thống hiển thị cửa sổ "Sửa kho vật lý".'),
            ('img', '12_edit', 'Cửa sổ Sửa kho vật lý'),
            ('step', 'Bước 4: Nhập thông tin cần sửa (quy tắc nhập như Thêm mới). Số nhà kho chỉ được tăng để thêm nhà kho mới.'),
            ('step', 'Bước 5: Bấm {icon:btn_luu} để xác nhận thay đổi'),
            ('sub', 'Hoặc {icon:btn_dong} nếu muốn hủy.'),
        ]),
        ('XÓA', [
            ('step', 'Bước 1: Bấm {icon:btn_xoa} ở cột Hành động của kho chưa từng phát sinh tồn kho.'),
            ('step', 'Bước 2: Hệ thống hiện hộp xác nhận "Xác nhận xóa"'),
            ('img', '13_delete', 'Hộp xác nhận xóa kho vật lý'),
            ('step', 'Bước 3: Bấm {icon:btn_confirm_xoa} để xác nhận xóa'),
            HUY,
        ]),
        ('KHÓA', [
            ('step', 'Bước 1: Chọn Khóa {icon:btn_khoa_row} hoặc {icon:btn_bacham_row} {icon:item_khoa} ở cột Hành động của kho không còn tồn.'),
            ('step', 'Bước 2: Hệ thống hiện hộp xác nhận "Xác nhận khóa"'),
            ('img', '14_lock', 'Hộp xác nhận khóa kho vật lý'),
            ('step', 'Bước 3: Bấm {icon:btn_confirm_khoa} để xác nhận'),
            HUY,
        ]),
        ('MỞ KHÓA', [
            ('step', 'Bước 1: Bấm {icon:btn_mokhoa_row} ở cột Hành động của kho đang Khóa.'),
            ('step', 'Bước 2: Hệ thống hiện hộp xác nhận "Xác nhận mở khóa"'),
            ('img', '15_unlock', 'Hộp xác nhận mở khóa kho vật lý'),
            ('step', 'Bước 3: Bấm {icon:btn_confirm_mokhoa} để xác nhận'),
            HUY,
        ]),
        ('XEM LỊCH SỬ THAY ĐỔI', [
            ('p', 'Cách 1: Xem từ màn danh sách:'),
            ('step', 'Ở cột Hành động, bấm {icon:btn_lichsu_row}'),
            ('sub', 'Hoặc bấm {icon:btn_bacham_row} rồi chọn {icon:item_lichsu}'),
            ('p', 'Cách 2: Xem từ màn chi tiết:'),
            ('step', 'Bước 1: Bấm vào mã kho để mở cửa sổ xem chi tiết'),
            ('step', 'Bước 2: Chọn nút {icon:btn_xemlichsu}'),
            ('img', '16_history', 'Cửa sổ Lịch sử thay đổi'),
        ]),
        ('XEM CHI TIẾT KHO VẬT LÝ', [
            ('step', VAO),
            ('step', 'Bước 2: Bấm vào mã kho. Hệ thống mở cửa sổ "Xem chi tiết kho vật lý".'),
            ('img', '17_detail', 'Xem chi tiết kho vật lý ở chế độ chỉ đọc'),
        ]),
        ('XUẤT DANH SÁCH RA EXCEL', [
            ('step', 'Bước 1: Lọc danh sách theo đúng dữ liệu cần lấy (xem PHẦN 1).'),
            ('step', 'Bước 2: Bấm nút {icon:btn_xuatexcel}. Hệ thống mở cửa sổ "Chọn trường xuất file".'),
            ('img', '20_export', 'Cửa sổ Chọn trường xuất file'),
            ('step', 'Bước 3: Tích chọn, kéo biểu tượng ☰ để đổi vị trí các trường cần xuất.'),
            ('sub', 'Hoặc bấm {icon:btn_chontatca} / {icon:btn_bochonhet} để chọn / bỏ chọn nhanh.'),
            ('step', 'Bước 4: Bấm {icon:btn_xuatfile}'),
            ('step', 'Bước 5: Mở file Excel đã xuất.'),
        ]),
        ('IMPORT KHO VẬT LÝ TỪ FILE EXCEL', [
            ('step', 'Bước 1: Tại màn hình danh sách, bấm {icon:btn_import}. Hệ thống mở cửa sổ "Import kho vật lý".'),
            ('img', '21_import_open', 'Cửa sổ Import kho vật lý khi vừa mở'),
            ('step', 'Bước 2: Bấm {icon:btn_taifilemau} để lấy file mẫu'),
            ('step', 'Bước 3: Điền dữ liệu vào file mẫu: Mã kho, Tên kho, Địa chỉ, Mã thủ kho (nhiều người cách nhau dấu phẩy), Số nhà kho là bắt buộc; Trạng thái, Mô tả tùy chọn. Mỗi lần tối đa 500 dòng.'),
            ('step', 'Bước 4: Bấm {icon:btn_chonfile}, chọn file vừa điền'),
            ('step', 'Bước 5: Bấm {icon:btn_load}'),
            ('img', '22_import_loaded', 'Dữ liệu đã được load lên bảng xem trước'),
            ('step', 'Bước 6: Bấm {icon:btn_validate} để hệ thống kiểm tra từng dòng.'),
            ('img', '23_import_validated', 'Kết quả kiểm tra — mỗi dòng lỗi nêu rõ lý do'),
            ('step', 'Bước 7:'),
            ('sub2', 'Sửa trực tiếp các dòng lỗi trên bảng rồi bấm Validate lại.'),
            ('sub2', 'Nếu không muốn nhập các dòng lỗi thì bấm {icon:btn_bodongloi}'),
            ('sub2', 'Muốn sửa lại những dòng đã khoá, bấm {icon:btn_xoavalidate}'),
            ('step', 'Bước 8: Bấm {icon:btn_import_modal} (chỉ bấm được khi không còn dòng lỗi).'),
        ]),
        ('TÙY CHỈNH CỘT HIỂN THỊ', [
            ('step', 'Bước 1: Ở màn danh sách, bấm biểu tượng {icon:btn_cauhinhcot}'),
            ('img', '25_colcfg', 'Cửa sổ Tùy chỉnh cột'),
            ('step', 'Bước 2: Tích để hiện cột, bỏ tích để ẩn cột.'),
            ('step', 'Bước 3: Bấm {icon:btn_chontatca} để hiện tất cả các cột.'),
            ('sub', 'Hoặc bấm {icon:btn_bochonhet} để ẩn tất cả các cột (trừ các cột bắt buộc).'),
            ('step', 'Bước 4: Kéo biểu tượng ba gạch ở cuối mỗi dòng để đổi thứ tự cột.'),
            ('step', 'Bước 5: Bấm {icon:btn_luu} để áp dụng'),
            ('sub', 'Hoặc bấm {icon:btn_dong} nếu muốn bỏ thay đổi.'),
        ]),
    ],
}

if __name__ == '__main__':
    scr = L.Screen(HERE)
    L.shorten_field_icons(scr)
    print('docx:', L.build_hdsd(scr, H, OUT))
    if '--no-word' not in sys.argv:
        print('Số trang:', L.word_finalize(OUT, PDF))
        L.check_docx(OUT)
