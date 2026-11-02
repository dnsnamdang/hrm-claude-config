# -*- coding: utf-8 -*-
"""HDSD_Danh mục vị trí — bản GỌN (skill hdsd-documenter, khuôn HDSD_MAU_GON.docx). Chép khuôn màn mẫu
docs/warehouses/gen_hdsd.py. Ảnh + icon: hdsd_shots/ (capture.js). Sơ đồ: uml/overview.png (gen_srs.py vẽ).
Chạy:  python gen_hdsd.py [--no-word]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
import _lib_win as L  # noqa: E402

TEN = 'Danh mục vị trí'
OUT = os.path.join(HERE, 'HDSD_%s.docx' % TEN)
PDF = os.path.join(HERE, 'out', 'HDSD_%s.pdf' % TEN)
VAO = 'Bước 1: Truy cập vào màn hình %s.' % TEN
HUY = ('sub', 'Hoặc bấm {icon:btn_huy_confirm} nếu bấm nhầm.')

H = {
    'ten': TEN,
    'thuat_ngu': [
        ['Vị trí', 'Cấp cuối của cây kho: Kho vật lý → Nhà kho → Dãy → Khoang → Vị trí; nơi xếp hàng cụ thể.'],
        ['Vị trí Thuộc khoang', 'Vị trí nằm trong một khoang; nhà kho, dãy, kho lấy theo khoang.'],
        ['Vị trí Tự do', 'Vị trí gắn thẳng vào kho, không qua nhà kho / dãy / khoang (ví dụ vị trí tách ghép hàng "<Mã kho>-TACH-GHEP").'],
        ['Trạng thái Hoạt động', 'Vị trí dùng được ở các màn nghiệp vụ (phiếu nhập, xuất, điều chuyển, kiểm kê…).'],
        ['Trạng thái Khóa', 'Vị trí vẫn nằm trong danh mục, xem được lịch sử nhưng không còn chọn được ở các màn nghiệp vụ.'],
    ],
    'phien_ban': [['1.0', L.NGAY, 'Đội phát triển phần mềm', 'Phát hành lần đầu']],
    'quyen': [
        'Người dùng có quyền "Quản lý kho" được dùng mọi chức năng của màn hình: xem, tìm kiếm, thêm mới, chỉnh sửa, xóa, khóa / mở khóa, xem lịch sử, xem chi tiết, xuất Excel, import Excel, tùy chỉnh cột.',
        'Người dùng thường chỉ thấy vị trí thuộc kho của công ty mình; Super admin thấy vị trí của mọi công ty và lọc được theo Công ty.',
    ],
    'phan': [
        ('TRUY CẬP VÀ TÌM KIẾM', [
            ('step', 'Bước 1: Từ phân hệ Kho {icon:menu_phanhe}, tại menu Danh mục {icon:menu_nhom}, chọn Vị trí {icon:menu_muc}'),
            ('img', '01_list', 'Màn hình Danh mục vị trí'),
            ('step', 'Bước 2: Nhập mã hoặc tên vị trí vào ô tìm kiếm nhanh {icon:o_timnhanh}'),
            ('step', 'Bước 3: Nhấn {icon:btn_timkiem}'),
            ('step', 'Bước 4: Bấm {icon:btn_timkiemnangcao}, chọn giá trị trong {icon:o_kho} để lọc theo kho (bấm biểu tượng ổ khóa cạnh chữ Kho để hiện cả kho đã khóa)'),
            ('sub', 'Hoặc chọn giá trị {icon:o_trangthai} để lọc theo trạng thái'),
            ('sub', 'Hoặc chọn giá trị {icon:o_nguoitao} để lọc theo người tạo'),
            ('sub', 'Hoặc chọn khoảng ngày {icon:o_ngaytao} để lọc theo ngày tạo'),
            ('sub', 'Hoặc chọn giá trị {icon:o_congty} để lọc theo công ty (chỉ Super admin)'),
            ('step', 'Bước 5: Chọn {icon:btn_lammoi} để xóa giá trị đã lọc'),
        ]),
        ('THÊM MỚI VỊ TRÍ', [
            ('step', VAO),
            ('step', 'Bước 2: Bấm {icon:btn_taomoi}'),
            ('img', '10_create', 'Cửa sổ Tạo mới vị trí — loại Thuộc khoang'),
            ('step', 'Bước 3: Chọn Loại vị trí rồi nhập/ chọn đầy đủ thông tin bắt buộc:'),
            ('sub2', 'Thuộc khoang: chọn lần lượt Kho, Nhà kho, Dãy, Khoang (ô sau chỉ chọn được khi đã chọn ô trước).'),
            ('sub2', 'Tự do: chỉ chọn Kho; 3 ô Nhà kho, Dãy, Khoang được ẩn đi.'),
            ('img', '10b_create_free', 'Cửa sổ Tạo mới vị trí — loại Tự do'),
            ('sub2', 'Mã vị trí: chữ không dấu, số, dấu - và _, tối đa 50 ký tự, không trùng vị trí khác trong cùng kho.'),
            ('sub2', 'Tên vị trí: tối đa 255 ký tự, không trùng vị trí khác trong cùng khoang (vị trí Tự do: trong cùng kho).'),
            ('sub2', 'Tùy chọn: Trạng thái (mặc định Hoạt động), Mô tả (tối đa 500 ký tự).'),
            ('step', 'Bước 4: Bấm {icon:btn_luu} để lưu và đóng cửa sổ,'),
            ('sub', 'Hoặc {icon:btn_luutieptuc} để lưu rồi nhập tiếp vị trí khác.'),
            ('sub', 'Hoặc {icon:btn_dong} để không lưu thông tin; đã nhập dữ liệu thì bấm {icon:btn_thoat} để thoát hoặc {icon:btn_olai} để ở lại.'),
        ]),
        ('CHỈNH SỬA', [
            ('step', VAO),
            ('step', 'Bước 2: Bấm nút {icon:btn_sua} ở cột Hành động.'),
            ('step', 'Bước 3: Hệ thống hiển thị cửa sổ "Sửa vị trí".'),
            ('img', '12_edit', 'Cửa sổ Sửa vị trí'),
            ('step', 'Bước 4: Sửa Mã vị trí, Tên vị trí, Trạng thái hoặc Mô tả (quy tắc nhập như Thêm mới). Loại vị trí, Kho, Nhà kho, Dãy, Khoang không sửa được.'),
            ('step', 'Bước 5: Bấm {icon:btn_luu} để xác nhận thay đổi'),
            ('sub', 'Hoặc {icon:btn_dong} nếu muốn hủy.'),
        ]),
        ('XÓA', [
            ('step', 'Bước 1: Bấm {icon:btn_xoa} ở cột Hành động của vị trí chưa được dùng ở đâu (nút chỉ hiện với vị trí xóa được).'),
            ('step', 'Bước 2: Hệ thống hiện hộp xác nhận "Xác nhận xóa"'),
            ('img', '13_delete', 'Hộp xác nhận xóa vị trí'),
            ('step', 'Bước 3: Bấm {icon:btn_confirm_xoa} để xác nhận xóa'),
            HUY,
        ]),
        ('KHÓA', [
            ('step', 'Bước 1: Chọn Khóa {icon:btn_khoa_row} hoặc {icon:btn_bacham_row} {icon:item_khoa} ở cột Hành động của vị trí đang Hoạt động.'),
            ('step', 'Bước 2: Hệ thống hiện hộp xác nhận "Xác nhận khóa"'),
            ('img', '14_lock', 'Hộp xác nhận khóa vị trí'),
            ('step', 'Bước 3: Bấm {icon:btn_confirm_khoa} để xác nhận'),
            HUY,
        ]),
        ('MỞ KHÓA', [
            ('step', 'Bước 1: Bấm {icon:btn_mokhoa_row} ở cột Hành động của vị trí đang Khóa (khoang, hoặc kho với vị trí Tự do, phải đang Hoạt động).'),
            ('step', 'Bước 2: Hệ thống hiện hộp xác nhận "Xác nhận mở khóa"'),
            ('img', '15_unlock', 'Hộp xác nhận mở khóa vị trí'),
            ('step', 'Bước 3: Bấm {icon:btn_confirm_mokhoa} để xác nhận'),
            HUY,
        ]),
        ('XEM LỊCH SỬ THAY ĐỔI', [
            ('p', 'Cách 1: Xem từ màn danh sách:'),
            ('step', 'Ở cột Hành động, bấm {icon:btn_lichsu_row}'),
            ('sub', 'Hoặc bấm {icon:btn_bacham_row} rồi chọn {icon:item_lichsu}'),
            ('p', 'Cách 2: Xem từ màn chi tiết:'),
            ('step', 'Bước 1: Bấm vào mã vị trí để mở cửa sổ xem chi tiết'),
            ('step', 'Bước 2: Chọn nút {icon:btn_xemlichsu}'),
            ('img', '16_history', 'Cửa sổ Lịch sử thay đổi'),
        ]),
        ('XEM CHI TIẾT VỊ TRÍ', [
            ('step', VAO),
            ('step', 'Bước 2: Bấm vào mã vị trí. Hệ thống mở cửa sổ "Xem chi tiết vị trí".'),
            ('img', '17_detail', 'Xem chi tiết vị trí ở chế độ chỉ đọc'),
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
        ('IMPORT VỊ TRÍ TỪ FILE EXCEL', [
            ('step', 'Bước 1: Tại màn hình danh sách, bấm {icon:btn_import}. Hệ thống mở cửa sổ "Import vị trí".'),
            ('img', '21_import_open', 'Cửa sổ Import vị trí khi vừa mở'),
            ('step', 'Bước 2: Bấm {icon:btn_taifilemau} để lấy file mẫu'),
            ('step', 'Bước 3: Điền dữ liệu vào file mẫu: Loại vị trí, Mã kho, Mã vị trí, Tên vị trí là bắt buộc; Mã nhà kho, Mã dãy, Mã khoang bắt buộc khi Loại vị trí là Thuộc khoang; Trạng thái, Mô tả tùy chọn. Mỗi lần tối đa 500 dòng.'),
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
