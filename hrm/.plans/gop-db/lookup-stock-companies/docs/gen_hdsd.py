# -*- coding: utf-8 -*-
"""HDSD_Báo cáo hàng có thể bán theo công ty — bản GỌN (khuôn HDSD_MAU_GON.docx) + PHẦN "ĐỌC BÁO CÁO" (user chốt 02/11).
Ảnh + icon: hdsd_shots/ (capture.js). Sơ đồ: uml/overview.png (gen_srs.py vẽ).
Chạy:  python gen_hdsd.py [--no-word]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import _lib_report as R  # noqa: E402
L = R.L

TEN = 'Báo cáo hàng có thể bán theo công ty'
OUT = os.path.join(HERE, 'HDSD_%s.docx' % TEN)
PDF = os.path.join(HERE, 'out', 'HDSD_%s.pdf' % TEN)
VAO = 'Bước 1: Truy cập vào màn hình %s (xem PHẦN 1).' % TEN

COT = [
    ['Cột', 'Ý nghĩa / lấy số từ đâu'],
    ['SL tồn có thể bán', 'Số còn bán được = Tổng tồn − SL KM − Tổng gửi − Tổng giữ − Tổng đang xuất (Hàng bán). Âm thì ghi 0.'],
    ['SL KM có thể xuất', 'Hàng khuyến mại còn xuất được = SL KM − Tổng đang xuất (Hàng KM). Âm thì ghi 0.'],
    ['Tổng tồn', 'Tồn kho kế toán của công ty tại các kho đang lọc, gồm cả kho khuyến mại.'],
    ['Hàng đang về – KD đặt', 'Hàng kinh doanh đã đặt trên đơn đặt hàng nhập khẩu / trong nước đã duyệt và yêu cầu nhập hàng mua trong nước chưa hạch toán. Tính trên toàn hệ thống, không theo công ty, kho.'],
    ['Hàng đang về – Tồn kho', 'Hàng đang về trên đơn đặt hàng, tổng hợp đặt hàng và chứng từ nhập kho chưa hoàn tất (từ 01/07/2024). Toàn hệ thống. Bấm số để xem từng chứng từ.'],
    ['SL KM', 'Tồn ở kho khuyến mại của công ty tại các kho đang lọc.'],
    ['Tổng gửi', 'Hàng khách gửi tại các kho đang lọc (từ phiếu nhập hàng gửi).'],
    ['Tổng giữ', 'Hàng đang giữ của công ty trên MỌI kho, không theo ô Kho.'],
    ['Tổng đang xuất – Hàng bán / Hàng KM', 'Hàng trên đề nghị xuất kho chưa hoàn tất tại các kho đang lọc; Hàng KM là phần xuất khuyến mại (HĐ hãng), Hàng bán là phần còn lại (đã trừ phần xuất từ hàng giữ, hàng gửi).'],
    ['Nhóm cột theo kho (vd PTT)', 'Số riêng của từng kho: SL tồn, SL KM, SL gửi, Đang xuất Hàng bán / Hàng KM. Chỉ hiện kho có số liệu.'],
    ['Dòng Tổng', 'Cộng từng cột của MỌI mặt hàng khớp bộ lọc (mọi trang), theo đơn vị tính cơ bản.'],
]

H = {
    'ten': TEN,
    'thuat_ngu': [
        ['SL tồn có thể bán', 'Số lượng hàng công ty còn bán được tại các kho đang xem.'],
        ['Tồn kho kế toán', 'Số lượng hàng đang có theo sổ kho của công ty.'],
        ['Hàng gửi', 'Hàng khách gửi lại kho.'],
        ['Hàng giữ', 'Hàng đã giữ cho nhân viên / hợp đồng, chưa xuất bán.'],
        ['Hàng đang về', 'Hàng đã đặt mua hoặc đang chờ nhập kho.'],
        ['KD / KM', 'Kinh doanh / Khuyến mại.'],
        ['ĐVT cơ bản', 'Đơn vị tính gốc của mặt hàng (hệ số 1).'],
    ],
    'phien_ban': [['1.0', L.NGAY, 'Đội phát triển phần mềm', 'Phát hành lần đầu']],
    'quyen': [
        'Màn hình chỉ để xem, không cần quyền riêng: mọi người dùng đã đăng nhập đều xem, lọc, xuất Excel được.',
        'Người dùng chọn được mọi công ty ở ô Tồn theo công ty; mặc định là công ty đang làm việc của mình.',
    ],
    'phan': [
        ('TRUY CẬP VÀ TÌM KIẾM', [
            ('step', 'Bước 1: Từ phân hệ Thông báo {icon:menu_phanhe}, tại menu Tra cứu tồn kho {icon:menu_nhom}, chọn Hàng có thể bán theo công ty {icon:menu_muc}'),
            ('img', '01_report', 'Màn hình Báo cáo hàng có thể bán theo công ty'),
            ('step', 'Bước 2: Nhập tên, mã hoặc model hàng vào ô tìm kiếm nhanh {icon:o_timnhanh}'),
            ('step', 'Bước 3: Nhấn {icon:btn_timkiem}'),
            ('step', 'Bước 4: Bấm {icon:btn_timkiemnangcao}, chọn công ty ở ô {icon:o_congty} (bắt buộc, mặc định công ty của bạn)'),
            ('sub', 'Hoặc chọn {icon:o_kho} để xem riêng một số kho (bỏ trống = mọi kho của công ty)'),
            ('sub', 'Hoặc chọn {icon:o_nhom} để lọc theo nhóm hàng hóa'),
            ('sub', 'Hoặc chọn {icon:o_tinhchat} để lọc theo tính chất hàng hóa'),
            ('sub', 'Hoặc chọn {icon:o_loai} để lọc theo loại hàng hóa'),
            ('sub', 'Hoặc chọn {icon:o_thuonghieu} để lọc theo thương hiệu'),
            ('sub', 'Hoặc chọn {icon:o_hang} để lọc theo hãng sản xuất'),
            ('sub', 'Hoặc nhập {icon:o_model} rồi bấm Tìm kiếm để lọc theo model'),
            ('sub', 'Hoặc gõ ít nhất 2 ký tự vào {icon:o_hanghoa} để chọn một mặt hàng'),
            ('step', 'Bước 5: Chọn {icon:btn_lammoi} để xóa giá trị đã lọc, về công ty của bạn'),
            ('sub2', 'Để trống ô công ty rồi bấm Tìm kiếm: hệ thống báo đỏ "Vui lòng chọn tồn theo công ty".'),
            ('sub2', 'Muốn ẩn bớt ô lọc: bấm {icon:btn_caidatboloc}.'),
        ]),
        ('ĐỌC BÁO CÁO', [
            ('step', 'Bước 1: Đọc phần bên trái bảng: tên hàng, ĐVT, SL tồn có thể bán, SL KM có thể xuất, Tổng tồn. Dòng Tổng đứng ngay dưới tiêu đề.'),
            ('img', '04a_read_left', 'Phần trái bảng (tìm nhanh "ENEO-AO": 5 mặt hàng)'),
            ('step', 'Bước 2: Kéo thanh cuộn ngang sang phải để xem Hàng đang về, SL KM, Tổng gửi, Tổng giữ, Tổng đang xuất và nhóm cột theo từng kho.'),
            ('img', '04c_read_right', 'Phần phải bảng: Hàng đang về, Tổng đang xuất, nhóm cột kho PTT'),
            ('step', 'Bước 3: Rê chuột vào {icon:ic_info} ở tiêu đề cột để xem cách tính của cột.'),
            ('table', COT, [2.0, 4.5]),
            ('pk', '**Ví dụ đọc từ ảnh trên:**'),
            ('sub2', 'Dòng Áo phông ENEOS: Tổng tồn 805 − SL KM 581 − Tổng gửi 71 − Tổng giữ 0 − Hàng bán đang xuất 50 = 103 = SL tồn có thể bán.'),
            ('sub2', 'Cùng dòng: SL KM 581 − Hàng KM đang xuất 86 = 495 = SL KM có thể xuất.'),
            ('sub2', 'Dòng Tổng cột SL tồn có thể bán: 59 + 38 + 105 + 15 + 103 = 320.'),
            ('sub2', 'Dòng Tổng cột Tổng tồn: 130 + 646 + 150 + 15 + 805 = 1,746 = SL tồn của kho PTT (cả 5 mặt hàng chỉ có ở kho PTT).'),
            ('sub2', 'Số 0 để trống; ô Hàng bán đang xuất và các cột theo kho chỉ hiện số dương.'),
        ]),
        ('ĐỔI ĐƠN VỊ TÍNH TRÊN DÒNG', [
            ('step', VAO),
            ('step', 'Bước 2: Ở dòng mặt hàng, chọn đơn vị khác trong ô ĐVT {icon:o_dvt}'),
            ('step', 'Bước 3: Mọi số trên dòng đổi theo đơn vị mới (chia cho hệ số, làm tròn 2 chữ số thập phân).'),
            ('img', '06_unit_card', 'TATE-TZ-03 đổi sang Hộp (x100): 13,375 Cái thành 133.75 Hộp; dòng Tổng giữ nguyên'),
            ('sub2', 'Dòng Tổng, popup Hàng đang về và file Excel luôn theo đơn vị cơ bản.'),
            ('sub2', 'Tìm kiếm lại, chuyển trang hoặc sắp xếp thì mọi dòng về đơn vị cơ bản.'),
        ]),
        ('XEM CHỨNG TỪ HÀNG ĐANG VỀ', [
            ('step', VAO),
            ('step', 'Bước 2: Bấm số ở cột Hàng đang về – Tồn kho {icon:link_tonkho} của dòng cần xem.'),
            ('step', 'Bước 3: Hệ thống mở cửa sổ "Hàng đang về" liệt kê từng chứng từ, chân cửa sổ ghi Tổng SL bằng số vừa bấm.'),
            ('img', '07_incoming', 'Cửa sổ Hàng đang về: 6 chứng từ, Tổng SL 726'),
            ('step', 'Bước 4: Bấm số phiếu hoặc số hợp đồng để mở chứng từ ở tab mới.'),
            ('step', 'Bước 5: Bấm {icon:btn_dong_popup} để đóng cửa sổ.'),
        ]),
        ('XUẤT BÁO CÁO RA EXCEL', [
            ('step', 'Bước 1: Lọc báo cáo theo đúng dữ liệu cần lấy (xem PHẦN 1).'),
            ('step', 'Bước 2: Bấm nút {icon:btn_xuatexcel}. Hệ thống mở cửa sổ "Chọn trường xuất Excel".'),
            ('img', '08_export', 'Cửa sổ Chọn trường xuất Excel'),
            ('step', 'Bước 3: Tích chọn, kéo biểu tượng ☰ để đổi vị trí các trường cần xuất.'),
            ('sub', 'Hoặc bấm {icon:btn_chontatca} / {icon:btn_bochonhet} để chọn / bỏ chọn nhanh.'),
            ('step', 'Bước 4: Bấm {icon:btn_xuatfile}'),
            ('step', 'Bước 5: Mở file bao_cao_hang_co_the_ban_theo_cong_ty.xlsx vừa tải về.'),
            ('sub2', 'File gồm mọi mặt hàng khớp bộ lọc, số theo đơn vị cơ bản, có dòng Tổng cộng và khối ký Người lập.'),
        ]),
        ('TÙY CHỈNH CỘT HIỂN THỊ', [
            ('step', 'Bước 1: Bấm biểu tượng {icon:btn_cauhinhcot}'),
            ('img', '09_colcfg', 'Cửa sổ Tuỳ chỉnh cột'),
            ('step', 'Bước 2: Tích để hiện cột, bỏ tích để ẩn cột (các cột có biểu tượng khóa luôn hiện).'),
            ('step', 'Bước 3: Bấm {icon:btn_chontatca} để hiện tất cả các cột.'),
            ('sub', 'Hoặc bấm {icon:btn_bochonhet} để ẩn tất cả các cột (trừ các cột khóa).'),
            ('step', 'Bước 4: Bấm {icon:btn_luu} để áp dụng'),
            ('sub', 'Hoặc bấm {icon:btn_dong} nếu muốn bỏ thay đổi.'),
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
