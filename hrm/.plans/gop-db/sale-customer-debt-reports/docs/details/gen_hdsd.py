# -*- coding: utf-8 -*-
"""HDSD_BC chi tiết công nợ KH — bản GỌN (khuôn HDSD_MAU_GON.docx) + PHẦN "ĐỌC BÁO CÁO" (user chốt 02/11/2026).
Ảnh + icon: hdsd_shots/ (capture.js). Sơ đồ: uml/overview.png (gen_srs.py vẽ).
Số ví dụ đọc từ ảnh 04_customer / 05b_table_right (dev 02/11/2026, kỳ 01/10/2026 - 31/10/2026, KH 89THUPTR-62).
Chạy:  python gen_hdsd.py [--no-word]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import _report_lib as R  # noqa: E402
L = R.L

TEN = 'BC chi tiết công nợ KH'
OUT = os.path.join(HERE, 'HDSD_%s.docx' % TEN)
PDF = os.path.join(HERE, 'out', 'HDSD_%s.pdf' % TEN)
VAO = 'Bước 1: Truy cập vào màn hình Báo cáo chi tiết công nợ khách hàng và chọn Thời gian (xem PHẦN 1).'

DOC = [
    ['Cột', 'Ý nghĩa / lấy số từ đâu'],
    ['STT', 'Dòng khách hàng đánh 1, 2, 3…; hợp đồng của khách đánh 1.1, 1.2…'],
    ['Đơn hàng/hợp đồng', 'Dòng đậm: mã - tên khách hàng. Dòng thường: số hợp đồng (bấm để mở hợp đồng ở tab mới); ô trống là chứng từ không gắn hợp đồng.'],
    ['Phòng ban, Bộ phận, NVKD', 'Của người tạo hợp đồng, theo hồ sơ hiện tại.'],
    ['Số dư đầu kỳ', 'Khách còn nợ trước "Từ ngày" = Nợ − Có của chứng từ hạch toán trước Từ ngày. Số âm: khách trả thừa.'],
    ['Hàng hóa/Dịch vụ', 'Hàng, dịch vụ bán trong kỳ: phiếu xuất hàng, xuất bán hàng mượn, hạch toán dịch vụ, thanh lý, hạch toán dịch vụ bảo hành - sửa chữa, khai báo công nợ đầu kỳ.'],
    ['Điều chỉnh công nợ (nhóm tăng)', 'Phiếu kế toán ghi tăng công nợ trong kỳ.'],
    ['Cộng (nhóm tăng)', 'Hàng hóa/Dịch vụ + Điều chỉnh công nợ tăng.'],
    ['Nhập trả lại', 'Hàng khách trả lại trong kỳ (phiếu nhập hàng).'],
    ['Đã thanh toán', 'Tiền khách trả trong kỳ: phiếu thu, phiếu báo có, khai báo công nợ đầu kỳ.'],
    ['Điều chỉnh công nợ (nhóm giảm)', 'Phiếu kế toán ghi giảm công nợ trong kỳ.'],
    ['Cộng (nhóm giảm)', 'Nhập trả lại + Đã thanh toán + Điều chỉnh công nợ giảm.'],
    ['Trả lại tiền thừa', 'Tiền chi trả lại khách: phiếu chi, phiếu ủy nhiệm chi. Làm TĂNG số dư cuối kỳ.'],
    ['Số dư cuối kỳ', 'Đầu kỳ + Cộng tăng − Cộng giảm + Trả lại tiền thừa. Dương: khách còn nợ; âm: khách trả thừa.'],
    ['Dòng khách hàng (đậm)', 'Cộng mọi hợp đồng của khách, kể cả hợp đồng ở trang khác.'],
    ['Dòng Tổng cộng', 'Tổng toàn bộ theo bộ lọc. Không áp ô tìm nhanh và lọc Số dư cuối kỳ, nên khi dùng 2 ô này có thể khác tổng các dòng.'],
]

H = {
    'ten': TEN,
    'thuat_ngu': [
        ['Công nợ phải thu', 'Số tiền khách hàng còn phải trả công ty.'],
        ['Kỳ báo cáo', 'Khoảng Từ ngày → Đến ngày ở ô Thời gian, tính theo ngày hạch toán của chứng từ.'],
        ['Dư nợ / Dư có', 'Số dư cuối kỳ dương (khách còn nợ) / âm (khách trả thừa, trả trước).'],
        ['NVKD', 'Nhân viên kinh doanh — người tạo hợp đồng.'],
        ['Chứng từ', 'Phiếu ghi vào công nợ: phiếu xuất hàng, phiếu nhập hàng, phiếu thu, phiếu chi, phiếu báo có, ủy nhiệm chi, phiếu kế toán, khai báo công nợ đầu kỳ…'],
    ],
    'phien_ban': [['1.0', L.NGAY, 'Đội phát triển phần mềm', 'Phát hành lần đầu']],
    'quyen': [
        'Mọi người dùng đều mở được báo cáo. Số liệu thấy được tùy quyền:',
        '- "Xem báo cáo chi tiết công nợ khách hàng theo tổng công ty": toàn bộ.',
        '- "… theo công ty" / "… theo phòng ban" / "… theo bộ phận": công nợ của công ty / phòng ban / bộ phận mình quản lý, cộng hợp đồng do mình tạo.',
        '- Không có quyền nào: chỉ hợp đồng do mình tạo.',
    ],
    'phan': [
        ('TRUY CẬP VÀ TÌM KIẾM', [
            ('step', 'Bước 1: Từ phân hệ Bán hàng {icon:menu_phanhe}, chọn Báo cáo {icon:menu_nhom}, chọn nhóm Báo cáo công nợ {icon:menu_nhomcon}, chọn Chi tiết công nợ KH {icon:menu_muc}'),
            ('img', '01_open', 'Màn hình Báo cáo chi tiết công nợ khách hàng khi mới mở'),
            ('step', 'Bước 2: Chọn khoảng ngày ở ô {icon:o_thoigian} (bắt buộc). Báo cáo tự tải.'),
            ('step', 'Bước 3: Chọn thêm điều kiện nếu cần:'),
            ('sub', 'Chọn khách hàng ở ô {icon:o_khachhang} (gõ ít nhất 2 ký tự mã hoặc tên)'),
            ('sub', 'Hoặc nhập đúng đủ số hợp đồng ở ô {icon:o_sohopdong} rồi nhấn Enter'),
            ('sub', 'Hoặc chọn Tất cả / Dư nợ / Dư có ở ô {icon:o_soducuoiky}'),
            ('sub', 'Hoặc chọn {icon:o_congty}, {icon:o_phongban}, {icon:o_bophan}, {icon:o_nhanvien} (chỉ hiện khi có quyền xem rộng)'),
            ('step', 'Bước 4: Nhập số hợp đồng, mã hoặc tên khách hàng vào ô tìm nhanh {icon:o_timnhanh} rồi nhấn {icon:btn_timkiem}'),
            ('step', 'Bước 5: Chọn {icon:btn_lammoi} để xóa giá trị đã lọc'),
            ('sub', 'Bấm {icon:btn_antimkiemnangcao} để thu gọn các ô lọc; {icon:btn_caidatboloc} để chọn ô lọc hiển thị'),
        ]),
        ('ĐỌC BÁO CÁO', [
            ('step', 'Bước 1: Lọc báo cáo (xem PHẦN 1). Ví dụ dưới đây: Thời gian 01/10/2026 → 31/10/2026, khách hàng 89THUPTR-62.'),
            ('img', '04_customer', 'Báo cáo của 1 khách hàng: dòng Tổng cộng, dòng khách hàng (đậm) và 3 hợp đồng'),
            ('img', '05b_table_right', 'Phần bên phải bảng: Phát sinh giảm, Trả lại tiền thừa, Số dư cuối kỳ'),
            ('step', 'Bước 2: Đọc từng cột theo bảng sau. Rê chuột vào {icon:ic_info} ở đầu cột để xem chú thích ngay trên màn.'),
            ('table', DOC, [1.9, 4.6]),
            ('step', 'Bước 3: Kiểm tra số trên ảnh:'),
            ('sub2', 'Số dư đầu kỳ dòng khách hàng = 831,664,501 + 12,024,720 + 4,838,400 = 848,527,621.'),
            ('sub2', 'Hợp đồng 1.2: 12,024,720 + 1,380,623,222 − 453,829,501 = 938,818,441 (Số dư cuối kỳ).'),
            ('sub2', 'Số dư cuối kỳ dòng khách hàng = 0 + 938,818,441 + 4,838,400 = 943,656,841.'),
            ('sub2', 'Đang lọc 1 khách hàng nên dòng Tổng cộng bằng dòng khách hàng.'),
            ('step', 'Bước 4: Bấm vào số tiền có gạch chân để xem các chứng từ tạo nên số đó (PHẦN 3).'),
        ]),
        ('XEM CHI TIẾT CHỨNG TỪ CỦA SỐ LIỆU', [
            ('step', VAO),
            ('step', 'Bước 2: Bấm vào số tiền có gạch chân ở dòng hợp đồng hoặc dòng khách hàng.'),
            ('step', 'Bước 3: Hệ thống mở cửa sổ "Chi tiết chứng từ".'),
            ('img', '07_popup_hanghoa', 'Chi tiết chứng từ của ô Hàng hóa/Dịch vụ — tổng 215,035,000 bằng số đã bấm'),
            ('step', 'Bước 4: Bấm mã phiếu để mở chứng từ ở tab mới.'),
            ('step', 'Bước 5: Bấm {icon:btn_dong} để quay lại báo cáo.'),
        ]),
        ('XUẤT BÁO CÁO RA EXCEL', [
            ('step', VAO),
            ('step', 'Bước 2: Bấm nút {icon:btn_xuatexcel}. Hệ thống mở cửa sổ "Chọn trường xuất Excel".'),
            ('img', '11_export', 'Cửa sổ Chọn trường xuất Excel'),
            ('step', 'Bước 3: Tích chọn, kéo biểu tượng ☰ để đổi vị trí các trường cần xuất.'),
            ('sub', 'Hoặc bấm {icon:btn_chontatca} / {icon:btn_bochonhet} để chọn / bỏ chọn nhanh.'),
            ('step', 'Bước 4: Bấm {icon:btn_xuatfile}'),
            ('step', 'Bước 5: Mở file bao_cao_chi_tiet_cong_no_khach_hang.xlsx đã tải về.'),
        ]),
    ],
}

if __name__ == '__main__':
    scr = L.Screen(HERE)
    L.shorten_field_icons(scr)
    print('docx:', R.build_hdsd(scr, H, OUT))
    if '--no-word' not in sys.argv:
        print('Số trang:', L.word_finalize(OUT, PDF))
        L.check_docx(OUT)
