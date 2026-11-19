# -*- coding: utf-8 -*-
"""HDSD_BC tổng hợp công nợ KH theo nhân viên — bản GỌN (khuôn danh mục kho) + PHẦN "ĐỌC BÁO CÁO" (user chốt 02/11/2026).
Ảnh + icon: hdsd_shots/ (capture.js, dev-hrm; ảnh file Excel dựng từ file tải về thật bằng render_excel.py/.js).
Sơ đồ: uml/overview.png (gen_srs.py vẽ).
Số ví dụ ở PHẦN 2 đọc từ CHÍNH ảnh 05_table_a / 05_table_b (Thời gian 01/10/2026 – 31/10/2026, NV 12010262 - Vương Văn Duy,
Số dư cuối kỳ = Dư nợ, chụp ngày 02/11/2026).
Chạy:  python gen_hdsd.py [--no-word]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import _lib_bc as B  # noqa: E402

L = B.L
TEN_FILE = 'BC tổng hợp công nợ KH theo nhân viên'
TEN = 'Báo cáo tổng hợp công nợ khách hàng theo nhân viên'
OUT = os.path.join(HERE, 'HDSD_%s.docx' % TEN_FILE)
PDF = os.path.join(HERE, 'out', 'HDSD_%s.pdf' % TEN_FILE)
VAO = 'Bước 1: Truy cập màn hình %s và chọn Thời gian (xem PHẦN 1).' % TEN

H = {
    'ten': TEN,
    'thuat_ngu': [
        ['Công nợ phải thu', 'Số tiền khách hàng còn phải trả cho công ty.'],
        ['Ngày hạch toán', 'Ngày kế toán ghi chứng từ vào sổ công nợ. Báo cáo lấy số theo ngày này, không theo ngày lập phiếu.'],
        ['Nhân viên tạo hợp đồng', 'Người lập hợp đồng; báo cáo gom công nợ theo người này.'],
        ['Dư nợ / Dư có', 'Số dư cuối kỳ dương: khách còn nợ. Số âm: khách trả thừa / trả trước.'],
        ['Ngày nghiệm thu', 'Mốc bàn giao của hợp đồng, dùng để tính Số ngày nợ.'],
        ['Số ngày nợ', 'Số ngày khách đã nợ tính tới hôm nay, sau 6 ngày kể từ Ngày nghiệm thu.'],
    ],
    'phien_ban': [['1.0', L.NGAY, 'Đội phát triển phần mềm', 'Phát hành lần đầu']],
    'quyen': [
        'Mọi người dùng đều mở được màn hình. Số liệu hiển thị theo quyền xem:',
        '- "Xem báo cáo tổng hợp công nợ khách hàng theo nhân viên - tổng công ty": thấy mọi công ty.',
        '- "... - công ty" / "... - phòng ban" / "... - bộ phận": thấy công ty đang làm việc / phòng ban, bộ phận mình quản lý và đang thuộc, cộng hợp đồng do mình tạo.',
        '- Không có quyền nào: chỉ thấy hợp đồng do mình tạo; không có ô lọc Công ty / Phòng ban / Bộ phận / Nhân viên.',
    ],
    'phan': [
        ('TRUY CẬP VÀ TÌM KIẾM', [
            ('step', 'Bước 1: Từ phân hệ Bán hàng {icon:menu_phanhe}, chọn Báo cáo {icon:menu_rail}, nhóm Báo cáo công nợ {icon:menu_nhom}, chọn Tổng hợp công nợ theo NV {icon:menu_muc}'),
            ('img', '00b_empty', 'Màn hình lúc mới mở, chưa chọn Thời gian'),
            ('step', 'Bước 2: Chọn Từ ngày và Đến ngày ở ô {icon:o_thoigian} (bắt buộc). Bảng tự tải số liệu.'),
            ('img', '01_report', 'Báo cáo sau khi chọn Thời gian 01/10/2026 – 31/10/2026'),
            ('step', 'Bước 3: Nhập số hợp đồng, mã hoặc tên khách hàng vào ô tìm kiếm nhanh {icon:o_timnhanh}'),
            ('step', 'Bước 4: Nhấn {icon:btn_timkiem}'),
            ('step', 'Bước 5: Chọn giá trị {icon:o_khachhang} để lọc theo khách hàng (gõ ít nhất 2 ký tự)'),
            ('sub', 'Hoặc nhập đủ số hợp đồng vào {icon:o_sohopdong} rồi nhấn {icon:btn_timkiem}'),
            ('sub', 'Hoặc chọn {icon:o_soducuoiky}: Dư nợ (khách còn nợ) / Dư có (khách trả thừa)'),
            ('sub', 'Hoặc chọn ngày ở {icon:o_ngaynghiemthu} để xem hợp đồng nghiệm thu đúng ngày đó'),
            ('sub', 'Hoặc chọn {icon:o_congty} {icon:o_phongban} {icon:o_bophan} {icon:o_nhanvien} (hiện theo quyền xem)'),
            ('step', 'Bước 6: Chọn {icon:btn_lammoi} để xóa giá trị đã lọc'),
            ('sub', 'Hoặc bấm {icon:btn_antimkiem} để thu gọn khu vực bộ lọc.'),
        ]),
        ('ĐỌC BÁO CÁO', [
            ('p', 'Ví dụ dưới lọc Thời gian 01/10/2026 – 31/10/2026, Nhân viên 12010262 - Vương Văn Duy, Số dư cuối kỳ = Dư nợ.'),
            ('img', '05_table_a', 'Bảng báo cáo – nửa trái (STT đến Phát sinh giảm)', 6.2),
            ('img', '05_table_b', 'Bảng báo cáo – nửa phải (cuộn ngang: Phát sinh tăng đến Số ngày nợ)', 6.2),
            ('p', 'Bảng có 3 loại dòng: dòng Tổng cộng (trên cùng), dòng nhân viên in đậm (mã - tên người tạo hợp đồng), các dòng hợp đồng bên dưới.'),
            ('table', ['Cột', 'Ý nghĩa / lấy số từ đâu'], [
                ['Đơn hàng/hợp đồng', 'Số hợp đồng; bấm vào mở hợp đồng ở tab mới. Ô trống: chứng từ không gắn hợp đồng.'],
                ['Khách hàng', 'Mã - tên khách của hợp đồng.'],
                ['Số dư đầu kỳ', 'Công nợ còn lại trước Từ ngày.'],
                ['Hàng hóa/Dịch vụ', 'Phiếu xuất kho, xuất bán hàng mượn, hạch toán dịch vụ, biên bản thanh lý, khai báo công nợ đầu kỳ hạch toán trong kỳ.'],
                ['Điều chỉnh công nợ (nhóm tăng)', 'Phiếu kế toán điều chỉnh tăng công nợ.'],
                ['Cộng (nhóm tăng)', 'Hàng hóa/Dịch vụ + Điều chỉnh công nợ.'],
                ['Nhập trả lại', 'Phiếu nhập hàng khách trả lại.'],
                ['Đã thanh toán', 'Phiếu thu, phiếu báo có, khai báo công nợ đầu kỳ (phần đã thu).'],
                ['Điều chỉnh công nợ (nhóm giảm)', 'Phiếu kế toán điều chỉnh giảm công nợ.'],
                ['Cộng (nhóm giảm)', 'Nhập trả lại + Đã thanh toán + Điều chỉnh công nợ.'],
                ['Trả lại tiền thừa', 'Phiếu chi, phiếu ủy nhiệm chi trả tiền lại cho khách; làm số dư TĂNG.'],
                ['Số dư cuối kỳ', 'Đầu kỳ + Cộng tăng − Cộng giảm + Trả lại tiền thừa. Số âm: khách trả thừa.'],
                ['Ngày nghiệm thu', 'Ngày biên bản nghiệm thu (hợp đồng cần lắp đặt) hoặc ngày xuất hàng / hạch toán dịch vụ muộn nhất.'],
                ['Số ngày nợ (Ngày)', 'Hôm nay − (Ngày nghiệm thu + 6 ngày); chỉ hiện khi hợp đồng còn nợ.'],
                ['Dòng nhân viên', 'Cộng mọi hợp đồng của nhân viên theo bộ lọc, kể cả hợp đồng ở trang sau.'],
                ['Dòng Tổng cộng', 'Các cột phát sinh: cộng mọi dòng. Số dư đầu kỳ: mọi chứng từ trước Từ ngày, không theo ô Số dư cuối kỳ.'],
            ], [1.9, 4.6]),
            ('p', 'Ví dụ cộng số đọc từ ảnh trên:'),
            ('sub2', 'Số dư đầu kỳ dòng nhân viên 60,698,500 = 27,940,000 + 7,528,680 + 25,229,820 (dòng 1.1, 1.2, 1.3).'),
            ('sub2', 'Hàng hóa/Dịch vụ dòng nhân viên 7,767,360 = 7,192,800 + 574,560 (dòng 1.4, 1.5).'),
            ('sub2', 'Số dư cuối kỳ dòng 1.1: 27,940,000 − 10,000,000 (Đã thanh toán) = 17,940,000.'),
            ('sub2', 'Số dư cuối kỳ dòng nhân viên: 60,698,500 + 7,767,360 − 10,000,000 = 58,465,860.'),
            ('sub2', 'Số ngày nợ dòng 1.1 = 50: nghiệm thu 07/09/2026, cộng 6 ngày là 13/09/2026, tới ngày xem 02/11/2026 là 50 ngày.'),
            ('sub2', 'Dòng Tổng cộng có Số dư đầu kỳ 60,624,980, khác dòng nhân viên vì đang lọc Dư nợ: Tổng cộng vẫn tính cả hợp đồng dư có đã bị ẩn. Số dư cuối kỳ Tổng cộng 58,392,340 = 60,624,980 + 7,767,360 − 10,000,000.'),
            ('step', 'Rê chuột vào icon ⓘ cạnh tên cột để xem cách tính của cột đó.'),
            ('img', '06_tip_crop', 'Chú thích cột Số dư cuối kỳ khi rê chuột vào icon ⓘ', 5.0),
        ]),
        ('CÀI ĐẶT BỘ LỌC', [
            ('step', 'Bước 1: Bấm {icon:btn_caidatboloc}'),
            ('img', '04_settings', 'Cửa sổ Cài đặt bộ lọc'),
            ('step', 'Bước 2: Tích để hiện ô lọc, bỏ tích để ẩn; kéo biểu tượng ở cuối dòng để đổi thứ tự.'),
            ('step', 'Bước 3: Bấm Lưu để áp dụng'),
            ('sub', 'Hoặc bấm Khôi phục mặc định để trả về như ban đầu, hoặc Đóng để bỏ thay đổi.'),
        ]),
        ('XUẤT EXCEL', [
            ('step', VAO),
            ('step', 'Bước 2: Bấm nút {icon:btn_xuatexcel}. Hệ thống mở cửa sổ "Chọn trường xuất Excel".'),
            ('img', '03_export', 'Cửa sổ Chọn trường xuất Excel'),
            ('step', 'Bước 3: Tích chọn, kéo biểu tượng ☰ để đổi vị trí các trường cần xuất.'),
            ('sub', 'Hoặc bấm {icon:btn_chontatca} / {icon:btn_bochonhet} để chọn / bỏ chọn nhanh.'),
            ('step', 'Bước 4: Bấm {icon:btn_xuatfile}'),
            ('step', 'Bước 5: Mở file Excel đã tải về (gồm mọi trang theo bộ lọc).'),
            ('img', '03c_excel', 'File Excel tải về'),
        ]),
        ('XUẤT EXCEL MẪU IN', [
            ('step', VAO),
            ('step', 'Bước 2: Bấm nút {icon:btn_xuatexcelmauin}. File tải về ngay, không cần chọn trường.'),
            ('step', 'Bước 3: Mở file, điền tay các cột Ngày xuất hóa đơn, Giải trình lý do chưa thu nợ, Kế hoạch ngày thu hồi công nợ, Xác nhận công nợ.'),
            ('img', '07_mauin', 'File Excel mẫu in tải về'),
        ]),
    ],
}

if __name__ == '__main__':
    scr = L.Screen(HERE)
    L.shorten_field_icons(scr)
    print('docx:', B.build_hdsd(scr, H, OUT))
    if '--no-word' not in sys.argv:
        print('Số trang:', L.word_finalize(OUT, PDF))
        L.check_docx(OUT)
