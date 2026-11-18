# -*- coding: utf-8 -*-
"""Phần DÙNG CHUNG cho bộ tài liệu 2 báo cáo bốc xếp (STT 309 theo nhà cung cấp · STT 310 theo nhân viên).

Hai màn dùng chung 1 thân trang (hrm-client `pages/transport/arrange-reports/components/*`) và 1 service BE
(hrm-api `Modules/Finance/Services/ArrangeReport/*`, `ArrangeReportController`), khác nhau ở `kind` = supplier | employee.
Mọi nội dung riêng của từng màn rẽ nhánh bằng `K['ncc']`.

Khuôn: sale-customer-debt-reports/docs/compare/{gen_srs,gen_hdsd}.py (hàm dựng chép sang đây — không sửa lib chung
`danh-muc-kho/docs/_lib_win.py`). Testcase: skill testcase-documenter `assets/tc_chuan.build_chuan(loai='bao_cao')`.
Code đọc: nhánh origin/develop ngày 18/11/2026. Ảnh: dev-hrm 18/11/2026 (capture.js).
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
GOPDB = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
HRM_CFG = os.path.abspath(os.path.join(GOPDB, '..', '..'))
sys.path.insert(0, os.path.join(GOPDB, 'danh-muc-kho', 'docs'))
sys.path.insert(0, os.path.join(HRM_CFG, '.claude', 'skills', 'testcase-documenter', 'assets'))
import _lib_win as L  # noqa: E402
from _lib_win import QgWriter, SRS_ROLES, QTC_LINK, HDSD_ROLES, HDSD_TPL, h1_trang_moi  # noqa: E402

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

NGAY = '18/11/2026'
QUYEN = 'Xem báo cáo bốc xếp'


def kind(k):
    ncc = k == 'ncc'
    K = {
        'ncc': ncc,
        'ten': 'Báo cáo cẩu hàng bốc xếp theo nhà cung cấp' if ncc else 'Báo cáo cẩu hàng bốc xếp theo nhân viên',
        'muc': 'Báo cáo cẩu hàng bốc xếp theo nhà cung cấp' if ncc else 'Báo cáo cẩu hàng bốc xếp theo nhân viên',
        'dv': 'nhà cung cấp' if ncc else 'nhân viên',
        'Dv': 'Nhà cung cấp' if ncc else 'Nhân viên',
        'cot_cay': 'Nhà cung cấp / Phiếu hạch toán' if ncc else 'Nhân viên',
        'tien': 'Số tiền (sau VAT)' if ncc else 'Số tiền',
        'o_dt': 'o_ncc' if ncc else 'o_nhanvien',
        'file': 'bao_cao_cau_hang_boc_xep_theo_nha_cung_cap.xlsx' if ncc else 'bao_cao_cau_hang_boc_xep_theo_nhan_vien.xlsx',
        'tieu_de_in': 'BÁO CÁO CẨU HÀNG BỐC XẾP THEO NHÀ CUNG CẤP' if ncc else 'BÁO CÁO CẨU HÀNG BỐC XẾP THEO NHÂN VIÊN',
        'tieu_de_ds': 'DANH SÁCH LƯỢT BỐC XẾP THUÊ NGOÀI' if ncc else 'DANH SÁCH LƯỢT BỐC XẾP THEO NHÂN VIÊN',
        'xem_truoc': 'Xem trước báo cáo cẩu hàng bốc xếp theo nhà cung cấp' if ncc else 'Xem trước báo cáo cẩu hàng bốc xếp theo nhân viên',
        'cong_ty_hint': ('Công ty của Phiếu nhập hàng / Phiếu xuất hàng chứa lượt bốc xếp.' if ncc
                         else 'Công ty nơi nhân viên bốc xếp đang làm việc.'),
        'pham_vi_cty': ('lượt bốc xếp trên Phiếu nhập hàng / Phiếu xuất hàng thuộc công ty đang làm việc' if ncc
                        else 'lượt bốc xếp của nhân viên thuộc công ty đang làm việc'),
        'pham_vi_minh': ('lượt bốc xếp trên Phiếu nhập hàng / Phiếu xuất hàng do chính mình lập' if ncc
                         else 'lượt bốc xếp mà chính mình là người bốc xếp'),
        'muc_dich': (['Tổng hợp chi phí bốc xếp THUÊ NGOÀI theo từng nhà cung cấp trong kỳ',
                      'Nguồn: dòng bốc xếp trên Phiếu nhập hàng / Phiếu xuất hàng có loại thuê "Thuê ngoài"',
                      'Kỳ lọc theo ngày hạch toán của phiếu'] if ncc else
                     ['Tổng hợp tiền công bốc xếp của từng nhân viên trong kỳ',
                      'Nguồn: người bốc xếp ghi trên dòng bốc xếp của Phiếu nhập hàng / Phiếu xuất hàng',
                      'Kỳ lọc theo ngày hạch toán của phiếu — khớp báo cáo chi tiết theo nhân viên']),
        'tip_ten': (['Mỗi nhóm là 1 nhà cung cấp bốc xếp thuê ngoài; mỗi dòng con là 1 lượt bốc xếp',
                     'Dòng con ghi Phiếu nhập hàng / Phiếu xuất hàng chứa lượt đó — bấm để mở phiếu',
                     'Dòng TỔNG tính trên toàn bộ dữ liệu đã lọc, không theo trang'] if ncc else
                    ['Mỗi dòng là 1 nhân viên tham gia bốc xếp trong kỳ',
                     'Bấm số lượt để xem từng lượt bốc xếp của nhân viên',
                     'Dòng TỔNG tính trên toàn bộ dữ liệu đã lọc, không theo trang']),
        'tip_tien': (['Thành tiền bốc xếp × (1 + VAT%)', 'Dòng nhóm / TỔNG cộng đúng các dòng con'] if ncc
                     else ['Tiền công bốc xếp của nhân viên ghi trên từng lượt']),
        'tien_note': 'Số tiền = thành tiền × (1 + VAT%)' if ncc else 'Số tiền = tiền công của từng người bốc xếp',
        'cot_so': (['Số lượt', 'Ngày hạch toán', 'Phiếu nhập/xuất kho', 'Nhập/Xuất', 'Loại bốc xếp', 'Khối lượng (tấn)',
                    'Số tiền (sau VAT)'] if ncc else ['Số lượt', 'Khối lượng (tấn)', 'Số tiền']),
        'loc': (['Kỳ', 'Công ty', 'Nhà cung cấp', 'Loại bốc xếp', 'Phiếu hạch toán'] if ncc else ['Kỳ', 'Công ty', 'Nhân viên']),
    }
    K['tip_trang'] = '. '.join(K['muc_dich']) + '.'
    K['tip_khoi_luot'] = ['Mỗi lượt là 1 dòng bốc xếp trên Phiếu nhập hàng / Phiếu xuất hàng có ngày hạch toán trong kỳ',
                          K['tien_note'], 'Bấm vào con số để mở danh sách lượt']
    K['tip_khoi_loai'] = ['Số lượt của từng loại bốc xếp (danh mục Bốc xếp của từng công ty)', 'Số nhỏ bên cạnh là số tiền',
                          'Loại không có lượt nào thì không hiện']
    K['menu_txt'] = 'Vào phân hệ Vận chuyển > nhóm Báo cáo bốc xếp > bấm "%s"' % K['muc']
    return K


def tip(head, lines):
    return '%s • %s' % (head, ' • '.join(lines))


def ui(header, rows):
    return [header] + [[str(i + 1)] + r for i, r in enumerate(rows)]


UI6 = ['STT', 'Tên đối tượng', 'Loại', 'Trạng thái', 'Giá trị ban đầu', 'Mô tả']
UI6W = [0.5, 1.35, 0.85, 0.8, 0.95, 2.75]
UI7 = ['STT', 'Tên đối tượng', 'Loại', 'Trạng thái', 'Phạm vi', 'Giá trị ban đầu', 'Mô tả']
UI7W = [0.45, 1.2, 0.85, 0.8, 1.0, 0.85, 2.6]
NUM = '- Số theo định dạng 1,234,567; khối lượng có tối đa 2 chữ số lẻ (vd 1,403.1).'


# =============================================================================================== SRS
def srs(K):
    ncc, ten, dv, Dv, T = K['ncc'], K['ten'], K['dv'], K['Dv'], K['tien']
    Q = 'Người dùng đã đăng nhập (mọi người dùng; quyền chỉ quyết định phạm vi dữ liệu)'
    DK = '1. Người dùng đăng nhập thành công.\n2. Không cần quyền để mở màn; phạm vi dữ liệu theo BR-02.'
    FR = []

    # ------------------------------------------------------------------ 2.1 Xem báo cáo
    cot = [
        ['Tiêu đề trang', 'Label', 'Hiển thị', ten, ['- Ở thanh trên cùng, kèm icon ⓘ.', '- Icon ⓘ: "%s"' % K['tip_trang']]],
        ['Khối bộ lọc', 'Panel', 'Hiển thị', 'Mở', ['- Tiêu đề "Bộ lọc %s%s", kèm icon ⓘ "MỤC ĐÍCH BÁO CÁO".' % (ten[0].lower(), ten[1:]),
                                                    '- Các ô lọc, nút Tìm kiếm, Xóa lọc: mục 2.2.']],
        ['Nút Cấu hình cột hiển thị', 'Button', 'Enable', 'Hiển thị', ['- Nút biểu tượng cột, đứng đầu cụm nút trên khối bộ lọc.', '- Mở cửa sổ "Tuỳ chỉnh cột" (mục 2.4).']],
        ['Nút In báo cáo', 'Button', 'Enable', 'Hiển thị', ['- Mở cửa sổ "In báo cáo" (mục 2.5).', '- Báo cáo chưa tải xong: báo "Báo cáo chưa tải xong, vui lòng thử lại."']],
        ['Nút Xuất Excel', 'Button', 'Enable', 'Hiển thị', ['- Nền xanh lá. Mở cửa sổ "Xuất Excel" (mục 2.6).', '- Báo cáo chưa tải xong: báo "Báo cáo chưa tải xong, vui lòng thử lại."']],
        ['Dòng kỳ của khối tổng hợp', 'Label', 'Read-only', 'Kỳ tháng hiện tại', [
            '- "Kỳ <nhãn kỳ> (theo ngày hạch toán)" kèm icon ⓘ "MỤC ĐÍCH BÁO CÁO", rồi "· N lượt · N %s · Khối lượng X tấn".' % dv,
            '- Nhãn kỳ: "tuần này", "tháng mm/yyyy", "năm yyyy", "từ dd/mm/yyyy đến dd/mm/yyyy".']],
        ['Nút Thu gọn / Mở rộng', 'Button', 'Enable', 'Thu gọn', ['- Ẩn / hiện 2 khối số liệu bên dưới; chữ đổi "Thu gọn" ↔ "Mở rộng".']],
        ['Khối LƯỢT BỐC XẾP', 'Panel', 'Read-only', 'Theo dữ liệu', [
            '- Góc phải: "Số tiền <tổng số tiền>".',
            '- Ô "Lượt bốc xếp" (luôn hiện), "Lượt nhập hàng", "Lượt xuất hàng" (ô = 0 thì ẩn); mỗi ô: số lượt + chữ "lượt".',
            '- Icon ⓘ: "%s"' % tip('LƯỢT BỐC XẾP', K['tip_khoi_luot']),
            '- Con số khác 0 bấm được → mở popup danh sách lượt (mục 2.3); số 0 không bấm được.']],
        ['Khối THEO LOẠI BỐC XẾP', 'Panel', 'Read-only', 'Ẩn khi không có lượt', [
            '- Góc phải: "N loại". Mỗi loại bốc xếp có lượt trong kỳ 1 ô: tên loại, số lượt (bấm được), số tiền nhỏ bên cạnh.',
            '- Xếp theo số tiền giảm dần.', '- Icon ⓘ: "%s"' % tip('THEO LOẠI BỐC XẾP', K['tip_khoi_loai'])]],
        ['Bảng báo cáo', 'Table/Grid', 'Read-only', 'Theo dữ liệu', [
            '- Cột: STT | %s | %s (mỗi cột mô tả 1 dòng bên dưới).' % (K['cot_cay'], ' | '.join(K['cot_so'])),
            '- Thứ tự dòng: dòng TỔNG → dòng %s (STT La Mã I, II…)%s.' % (dv, ' → các dòng lượt bốc xếp của nhà cung cấp đó (STT 1, 2…)' if ncc else ''),
            '- Tiêu đề cột dính khi cuộn dọc trong khung bảng; bảng rộng hơn màn thì có thanh cuộn ngang.',
            '- Đang tải lại: số liệu cũ mờ đi, không xoá trắng màn.',
            '- Không có lượt nào: dòng TỔNG hiện số 0 và dòng "Không có lượt bốc xếp nào khớp bộ lọc."']],
        ['Dòng TỔNG', 'Table/Grid', 'Read-only', 'Theo dữ liệu', [
            '- Nền cam nhạt, ô STT ghi "TỔNG", ô thứ 2 ghi "%s" chữ hoa kèm icon ⓘ.' % K['cot_cay'].upper(),
            '- Icon ⓘ: "%s"' % tip(K['cot_cay'].upper(), K['tip_ten']),
            '- Số lượt (bấm được → popup "Tất cả lượt bốc xếp"), Khối lượng, %s: cộng trên TOÀN BỘ dữ liệu đã lọc, không theo trang; bằng 0 vẫn in "0".' % T]],
        ['Cột STT', 'Table/Grid', 'Read-only', 'Hiển thị', ['- Dòng %s: số La Mã I, II, III… liên tục qua các trang.' % dv]
            + (['- Dòng lượt: 1, 2, 3… đánh lại trong từng nhà cung cấp.'] if ncc else [])],
    ]
    if ncc:
        cot += [
            ['Cột Nhà cung cấp / Phiếu hạch toán', 'Table/Grid', 'Read-only', 'Hiển thị', [
                '- Tiêu đề kèm ô chọn cấp (mục dưới).',
                '- Dòng nhà cung cấp: mũi tên bung / thu, tên nhà cung cấp, mã chữ nhỏ màu xám bên cạnh; tên dài bị cắt "…", rê chuột hiện đủ "Tên - Mã".',
                '- Nhà cung cấp không còn trong danh mục: hiện "Nhà cung cấp #<số>".',
                '- Dòng lượt: số Phiếu xuất hàng (PXH-…) / Phiếu nhập hàng (PNH-…) chứa lượt, chữ liên kết → mở phiếu ở tab mới.']],
            ['Ô chọn cấp', 'Dropdown', 'Enable', 'Đến từng lượt bốc xếp', [
                '- Lựa chọn: "Chỉ nhà cung cấp", "Đến từng lượt bốc xếp".', '- Chỉ đổi cách xem (bung / thu mọi nhóm), không tải lại dữ liệu; chuyển trang vẫn giữ cấp đang chọn.']],
            ['Mũi tên bung / thu', 'Button', 'Enable', 'Mở (theo ô chọn cấp)', ['- Bung / thu riêng 1 nhà cung cấp; rê chuột: "Hiện các lượt bốc xếp" / "Ẩn các lượt bốc xếp".']],
            ['Cột Số lượt', 'Table/Grid', 'Read-only', 'Hiển thị', ['- Dòng TỔNG, dòng nhà cung cấp: số lượt, gạch chân đứt, bấm → popup danh sách lượt (mục 2.3).', '- Dòng lượt: để trống.']],
            ['Cột Ngày hạch toán', 'Table/Grid', 'Read-only', 'Hiển thị', ['- Chỉ ở dòng lượt, dạng dd/mm/yyyy HH:mm, căn giữa.',
                                                                              '- Icon ⓘ: "%s"' % tip('NGÀY HẠCH TOÁN', ['Ngày hạch toán của Phiếu nhập hàng / Phiếu xuất hàng chứa lượt bốc xếp', 'Kỳ báo cáo lọc theo ngày này'])]],
            ['Cột Phiếu nhập/xuất kho', 'Table/Grid', 'Read-only', 'Hiển thị', ['- Chỉ ở dòng lượt: số Phiếu xuất kho (PXK-…) / Phiếu nhập kho (PNK-…) đi kèm, chữ liên kết → mở phiếu ở tab mới.']],
            ['Cột Nhập/Xuất', 'Table/Grid', 'Read-only', 'Hiển thị', ['- Chỉ ở dòng lượt: "Nhập" (lượt của Phiếu nhập hàng) / "Xuất" (lượt của Phiếu xuất hàng).']],
            ['Cột Loại bốc xếp', 'Table/Grid', 'Read-only', 'Hiển thị', ['- Chỉ ở dòng lượt: tên loại bốc xếp ghi trên lượt; dài thì xuống dòng.']],
        ]
    else:
        cot += [
            ['Cột Nhân viên', 'Table/Grid', 'Read-only', 'Hiển thị', ['- Tên nhân viên bốc xếp, mã nhân viên chữ nhỏ màu xám bên cạnh.', '- Bảng 1 cấp: không có mũi tên bung / thu, không có ô chọn cấp.']],
            ['Cột Số lượt', 'Table/Grid', 'Read-only', 'Hiển thị', ['- Số lượt bốc xếp nhân viên tham gia trong kỳ; gạch chân đứt, bấm → popup danh sách lượt của nhân viên (mục 2.3).']],
        ]
    cot += [
        ['Cột Khối lượng (tấn)', 'Table/Grid', 'Read-only', 'Hiển thị', ['- Khối lượng ghi trên lượt bốc xếp; dòng nhóm / TỔNG là tổng.', NUM]],
        ['Cột ' + T, 'Table/Grid', 'Read-only', 'Hiển thị', ['- ' + ('Thành tiền bốc xếp × (1 + VAT%) của lượt; dòng nhóm / TỔNG là tổng.' if ncc else 'Tiền công của nhân viên trên từng lượt; dòng nhân viên / TỔNG là tổng.'),
                                                             NUM, '- Icon ⓘ: "%s"' % tip(T.upper(), K['tip_tien'])]],
        ['Chân bảng', 'Label', 'Hiển thị', 'Hiển thị', ['- "Hiển thị a–b / N %s": N = số %s có lượt trong kỳ; phân trang theo %s, không cắt rời các lượt của 1 %s.' % (dv, dv, dv, dv)]],
        ['Ô Số dòng/trang', 'Dropdown', 'Enable', '10', ['- Lựa chọn 10, 20, 50, 100 %s / trang; đổi số dòng → về trang 1.' % dv]],
        ['Phân trang', 'Button', 'Enable', 'Trang 1', ['- Nút «, ‹, số trang, ›, »; nút không dùng được thì mờ. Chuyển trang giữ bộ lọc và dòng TỔNG.']],
    ]
    if ncc:
        data_rows = [
            ('Tập dữ liệu / thời điểm số liệu', 'Lượt bốc xếp ghi trên Phiếu nhập hàng / Phiếu xuất hàng có loại thuê "Thuê ngoài" và có nhà cung cấp, sau khi áp phạm vi quyền (BR-02) và bộ lọc. Phiếu phải đã hạch toán và có ngày hạch toán nằm trong kỳ. Số liệu tính tại thời điểm tải báo cáo.', '—'),
            ('Ngày hạch toán', 'Ngày hạch toán SỚM NHẤT trong các bút toán của Phiếu nhập hàng / Phiếu xuất hàng chứa lượt (có giờ).', 'Ngày hạch toán của Phiếu nhập hàng / Phiếu xuất hàng chứa lượt bốc xếp • Kỳ báo cáo lọc theo ngày này'),
            ('Số lượt', 'Đếm số lượt bốc xếp (mỗi dòng bốc xếp trên phiếu là 1 lượt).', '—'),
            ('Khối lượng (tấn)', 'Khối lượng ghi trên lượt bốc xếp; nhóm / TỔNG = tổng các lượt.', '—'),
            ('Số tiền (sau VAT)', 'Thành tiền bốc xếp của lượt × (1 + VAT% của lượt), làm tròn 2 chữ số lẻ; nhóm / TỔNG = tổng các lượt (cộng SAU VAT).', tip('SỐ TIỀN (SAU VAT)', K['tip_tien'])),
            ('Phiếu nhập/xuất kho, Nhập/Xuất', 'Lượt của Phiếu xuất hàng → "Xuất" + Phiếu xuất kho của phiếu; lượt của Phiếu nhập hàng → "Nhập" + Phiếu nhập kho của phiếu.', '—'),
            ('Thứ tự dòng', 'Nhà cung cấp xếp theo Số tiền giảm dần, bằng nhau thì theo tên; lượt trong nhóm xếp theo ngày hạch toán tăng dần.', '—'),
            ('Khối LƯỢT BỐC XẾP', 'Lượt bốc xếp = tổng số lượt; Lượt nhập hàng / Lượt xuất hàng = số lượt của Phiếu nhập hàng / Phiếu xuất hàng; Số tiền = tổng Số tiền.', tip('LƯỢT BỐC XẾP', K['tip_khoi_luot'])),
            ('Khối THEO LOẠI BỐC XẾP', 'Gom theo loại bốc xếp của lượt: số lượt + tổng số tiền; xếp theo số tiền giảm dần.', tip('THEO LOẠI BỐC XẾP', K['tip_khoi_loai'])),
            ('Ràng buộc khớp số', '- TỔNG = tổng các dòng nhà cung cấp (mọi trang) = tổng các dòng lượt.\n- Lượt bốc xếp = Lượt nhập hàng + Lượt xuất hàng = tổng số lượt các loại bốc xếp.\n- Số lượt của 1 ô = số dòng của popup mở từ ô đó.', '—'),
        ]
    else:
        data_rows = [
            ('Tập dữ liệu / thời điểm số liệu', 'Người bốc xếp ghi trên lượt bốc xếp của Phiếu nhập hàng / Phiếu xuất hàng (mọi loại thuê), sau khi áp phạm vi quyền (BR-02) và bộ lọc. 1 lượt có nhiều người bốc xếp thì mỗi người tính 1 dòng. Phiếu phải đã hạch toán và có ngày hạch toán nằm trong kỳ.', '—'),
            ('Số lượt', 'Đếm số lượt nhân viên tham gia. Dòng TỔNG = tổng số lượt của mọi nhân viên (1 lượt có 3 người bốc xếp được đếm 3).', '—'),
            ('Khối lượng (tấn)', 'Khối lượng ghi trên lượt bốc xếp, tính ĐỦ cho từng người tham gia lượt đó; nhân viên / TỔNG = tổng các lượt.', '—'),
            ('Số tiền', 'Tiền công của nhân viên ghi trên lượt bốc xếp; nhân viên / TỔNG = tổng.', tip('SỐ TIỀN', K['tip_tien'])),
            ('Thứ tự dòng', 'Nhân viên xếp theo Số tiền giảm dần, bằng nhau thì theo tên.', '—'),
            ('Khối LƯỢT BỐC XẾP', 'Như Số lượt: Lượt bốc xếp = tổng; Lượt nhập hàng / Lượt xuất hàng theo loại phiếu; Số tiền = tổng tiền công.', tip('LƯỢT BỐC XẾP', K['tip_khoi_luot'])),
            ('Khối THEO LOẠI BỐC XẾP', 'Gom theo loại bốc xếp của lượt: số lượt + tổng tiền công; xếp theo số tiền giảm dần.', tip('THEO LOẠI BỐC XẾP', K['tip_khoi_loai'])),
            ('Ràng buộc khớp số', '- TỔNG = tổng các dòng nhân viên (mọi trang).\n- Lượt bốc xếp = Lượt nhập hàng + Lượt xuất hàng.\n- Số lượt / Số tiền của 1 nhân viên = số dòng / tổng Số tiền của popup mở từ dòng đó, và khớp dòng nhân viên đó ở "Báo cáo chi tiết cẩu hàng bốc xếp theo nhân viên" cùng kỳ.', '—'),
        ]
    popup_rows = [
        ('Số lượt ở dòng TỔNG / ô "Lượt bốc xếp" của khối tổng hợp', 'Danh sách lượt bốc xếp — "Tất cả lượt bốc xếp"', 'Xem từng lượt tạo nên tổng của báo cáo', 'Mọi lượt theo bộ lọc đang áp'),
        ('Số lượt ở dòng %s' % dv, 'Danh sách lượt bốc xếp — "<Tên> - <Mã>"', 'Xem các lượt của 1 %s' % dv, 'Lượt của %s đó' % dv),
        ('Ô "Lượt nhập hàng" / "Lượt xuất hàng"', 'Danh sách lượt bốc xếp — "Lượt nhập hàng" / "Lượt xuất hàng"', 'Tách lượt theo hàng nhập / hàng xuất', 'Lượt của Phiếu nhập hàng / Phiếu xuất hàng'),
        ('Số lượt của 1 loại ở khối THEO LOẠI BỐC XẾP', 'Danh sách lượt bốc xếp — "Loại bốc xếp: <tên loại>"', 'Xem các lượt của 1 loại', 'Lượt có loại bốc xếp đó'),
    ]
    if ncc:
        popup_rows.append(('Số phiếu ở cột Nhà cung cấp / Phiếu hạch toán, Phiếu nhập/xuất kho', 'Không phải popup — mở phiếu ở tab mới', 'Kiểm tra chứng từ gốc của lượt', 'Đúng phiếu của dòng'))
    popup_rows.append(('Ô Khối lượng, Số tiền', 'Không bấm được', '—', '—'))

    FR.append({
        'ten': 'Xem báo cáo',
        'qtc': 'Màn Báo cáo, Phân trang, Định dạng số.',
        'gioi_thieu': [
            ['Tên chức năng', 'Xem %s' % (ten[0].lower() + ten[1:])],
            ['Mô tả', ('Hiển thị chi phí bốc xếp thuê ngoài trong kỳ theo từng nhà cung cấp và từng lượt bốc xếp: khối tổng hợp, dòng TỔNG, dòng nhà cung cấp, dòng lượt. Màn chỉ đọc.' if ncc
                       else 'Hiển thị tiền công bốc xếp trong kỳ của từng nhân viên: khối tổng hợp, dòng TỔNG, mỗi nhân viên 1 dòng (số lượt, khối lượng, số tiền). Màn chỉ đọc.')],
            ['Tác nhân', Q],
            ['Điều kiện ban đầu', DK],
            ['Dòng sự kiện chính', '1. Người dùng mở màn theo đường dẫn menu.\n2. Hệ thống tải báo cáo kỳ mặc định "Tháng này" theo phạm vi quyền: khối tổng hợp, dòng TỔNG, trang 1 gồm 10 %s%s.\n3. Chân bảng ghi "Hiển thị a–b / N %s".' % (dv, ', bung sẵn đến từng lượt bốc xếp' if ncc else '', dv)],
            ['Dòng sự kiện phụ', '• Không có lượt nào → TỔNG = 0, "Không có lượt bốc xếp nào khớp bộ lọc.", khối THEO LOẠI BỐC XẾP ẩn.\n• Lỗi khi tải → báo "Không tải được báo cáo. Vui lòng thử lại." (hoặc câu lỗi của hệ thống), giữ số liệu đang hiển thị.\n• Đổi bộ lọc liên tục: chỉ kết quả lần lọc cuối được hiển thị.\n• Phiên đăng nhập hết hạn → hệ thống đưa về màn đăng nhập.'],
            ['Yêu cầu đặc biệt', 'Mở màn và tải kỳ mặc định trên môi trường thử nghiệm khoảng 7–8 giây (đo 18/11/2026, gồm tải trang); kỳ "Năm nay" vẫn tải trong vài giây.'],
        ],
        'anh': [('01_report', 'Màn %s khi mở (kỳ Tháng này)' % ten), ('02_summary', 'Khối tổng hợp đầu báo cáo')]
               + ([('07_level1', 'Ô chọn cấp "Chỉ nhà cung cấp" — chỉ còn dòng nhà cung cấp')] if ncc else [('07_paging', 'Báo cáo kỳ Năm nay — 18 nhân viên, 2 trang')])
               + [('06_tip_amount', 'Icon ⓘ của cột %s' % T), ('08_empty', 'Báo cáo không có lượt nào khớp bộ lọc')],
        'ui': ui(UI6, cot), 'ui_widths': UI6W,
        'events': [
            ['Mở màn hình', 'System', 'Before:\n– Không kiểm quyền vào màn; đọc phạm vi của người dùng (BR-02), khoá / mở ô Công ty.\nAfter:\n– Bộ lọc về mặc định (Kỳ = Tháng này); tải khối tổng hợp + bảng trang 1.'],
            ['Đổi ô lọc / bấm Tìm kiếm', 'Change / Click', 'Xem mục 2.2.'],
            ['Chuyển trang / đổi Số dòng/trang', 'Click / Change', 'After:\n– Tải lại các dòng %s của trang mới, giữ bộ lọc và dòng TỔNG; đổi số dòng thì về trang 1.' % dv],
            ['Bấm con số (khối tổng hợp, dòng TỔNG, dòng %s)' % dv, 'Click', 'After:\n– Mở popup danh sách lượt của đúng ô đã bấm (mục 2.3).'],
        ] + ([['Đổi ô chọn cấp / bấm mũi tên', 'Change / Click', 'After:\n– Bung / thu dòng lượt tại chỗ, không tải lại dữ liệu.'],
              ['Bấm số phiếu ở dòng lượt', 'Click', 'After:\n– Mở Phiếu xuất hàng / Phiếu nhập hàng / Phiếu xuất kho / Phiếu nhập kho ở tab mới; báo cáo giữ nguyên.']] if ncc else []) + [
            ['Bấm Thu gọn / Mở rộng', 'Click', 'After:\n– Ẩn / hiện 2 khối số liệu.'],
            ['Rê chuột vào icon ⓘ', 'Hover', 'After:\n– Hiện chú thích (nội dung ở bảng 2.1.5 / 2.1.6).'],
        ],
        'them': [
            ('Cách lấy dữ liệu và giải thích chỉ tiêu', [
                ('p', 'Bảng dưới mô tả cách hệ thống lấy từng chỉ tiêu, cột số liệu và nội dung icon ⓘ (nguyên văn trên giao diện).'),
                ('data', data_rows)]),
            ('Danh sách popup mở từ số liệu', [('popup', popup_rows)]),
        ],
    })

    # ------------------------------------------------------------------ 2.2 Tìm kiếm và lọc
    loc_rows = [
        ['Ô Kỳ', 'Dropdown', 'Enable', 'Tuần này, Tháng này, Tháng trước, Năm nay, Tuỳ chọn', 'Tháng này', [
            '- Không xoá trống được. Icon ⓘ: "Lọc theo NGÀY HẠCH TOÁN của Phiếu nhập hàng / Phiếu xuất hàng chứa lượt bốc xếp."',
            '- Đổi kỳ → tải lại ngay.', '- Chọn "Tuỳ chọn" → hiện ô Thời gian ngay sau ô Kỳ; đổi sang kỳ khác → ô Thời gian biến mất và bị xoá.']],
        ['Ô Thời gian', 'Datepicker', 'Enable / Ẩn', 'Khoảng ngày dd/mm/yyyy', 'Trống', [
            '- Chỉ hiện khi Kỳ = Tuỳ chọn; gồm ngày bắt đầu → ngày kết thúc, tính cả 2 đầu mút.',
            '- Chọn đủ 2 ngày → tải lại; chưa đủ thì chưa tải; bấm Tìm kiếm khi chưa đủ: "Chọn đủ ngày bắt đầu và ngày kết thúc của kỳ Tuỳ chọn."',
            '- Ngày kết thúc trước ngày bắt đầu: hệ thống báo "Ngày kết thúc phải sau hoặc bằng ngày bắt đầu".']],
        ['Ô Công ty', 'Dropdown', 'Enable / Disable', 'Danh sách công ty đang hoạt động', 'Trống (quyền tổng công ty) / công ty của mình', [
            '- Icon ⓘ: "%s"' % K['cong_ty_hint'],
            '- Có quyền mức Tổng công ty: chọn 1 công ty hoặc để trống = mọi công ty.',
            '- Không có mức Tổng công ty: ô khoá ở công ty của mình, không đổi được.',
            '- Đổi công ty → xoá %s, tải lại ngay.' % ('ô Loại bốc xếp (giữ Nhà cung cấp)' if ncc else 'ô Nhân viên')]],
    ]
    if ncc:
        loc_rows += [
            ['Ô Nhà cung cấp', 'Dropdown', 'Enable', 'Toàn bộ danh mục khách hàng / nhà cung cấp, chọn nhiều', 'Trống', [
                '- Gõ tìm trong ô tìm của danh sách theo tên, số điện thoại hoặc mã; gợi ý "Tên, SĐT hoặc mã KH/NCC".',
                '- Hiển thị "Mã - Tên"; mới tạo đứng trước; gõ dưới 3 ký tự chỉ lấy 20 kết quả.',
                '- Chọn / bỏ → tải lại ngay. Để trống = mọi nhà cung cấp.']],
            ['Ô Loại bốc xếp', 'Dropdown', 'Enable', 'Các loại bốc xếp có lượt trong phạm vi + công ty đang chọn, chọn nhiều', 'Trống', ['- Chọn / bỏ → tải lại ngay.']],
            ['Ô Phiếu hạch toán', 'Textbox', 'Enable', 'Chữ tự do', 'Trống', [
                '- Gợi ý "Mã phiếu hạch toán (PNH / PXH)".', '- Lọc gần đúng theo số Phiếu nhập hàng / Phiếu xuất hàng, không phân biệt hoa thường; bỏ khoảng trắng đầu / cuối.',
                '- Chỉ áp khi nhấn Enter hoặc bấm Tìm kiếm.']],
        ]
    else:
        loc_rows += [
            ['Ô Nhân viên', 'Dropdown', 'Enable', 'Nhân viên có lượt bốc xếp trong phạm vi + công ty đang chọn (mọi kỳ)', 'Trống', [
                '- Hiển thị "Mã NV - Tên"; có ô tìm; chọn 1 người. Chọn / bỏ → tải lại ngay.']],
        ]
    loc_rows += [
        ['Nút Tìm kiếm', 'Button', 'Enable', '–', '–', ['- Tải lại báo cáo từ trang 1 với mọi điều kiện đang nhập.']],
        ['Nút Xóa lọc', 'Button', 'Enable', '–', '–', ['- Mọi ô về mặc định (Kỳ = Tháng này); không có mức Tổng công ty thì giữ công ty bị khoá; tải lại.']],
    ]
    if ncc:
        loc_rows += [
            ['Nút Ẩn / Tìm kiếm nâng cao', 'Button', 'Enable', '–', 'Mở', ['- Thu gọn / mở các ô lọc.']],
            ['Nút Cài đặt bộ lọc', 'Button', 'Enable', '–', '–', ['- Cửa sổ "Cài đặt bộ lọc": tích chọn ô lọc hiển thị, kéo đổi thứ tự; Lưu / Khôi phục mặc định / Đóng; lưu theo từng màn.']],
        ]
    else:
        loc_rows += [
            ['Nút Ẩn / Tìm kiếm nâng cao, Cài đặt bộ lọc', 'Button', 'Ẩn', '–', 'Ẩn', ['- Màn chỉ có 3 ô lọc nên bày 1 hàng, không có 2 nút này; chọn Kỳ = Tuỳ chọn (thêm ô Thời gian) thì 2 nút hiện ra.']],
        ]
    FR.append({
        'ten': 'Tìm kiếm và lọc',
        'qtc': 'Kịch bản tìm kiếm, Bộ lọc, Dropdown.',
        'gioi_thieu': [
            ['Tên chức năng', 'Tìm kiếm và lọc báo cáo'],
            ['Mô tả', 'Chọn kỳ (theo ngày hạch toán) và thu hẹp số liệu bằng %s.' % ', '.join(K['loc'][1:])],
            ['Tác nhân', Q],
            ['Điều kiện ban đầu', DK + '\n3. Đang ở màn %s.' % ten],
            ['Dòng sự kiện chính', '1. Người dùng đổi Kỳ hoặc ô chọn%s → hệ thống tải lại ngay từ trang 1.\n%s3. Khối tổng hợp, dòng TỔNG và bảng tính lại theo bộ lọc.' % (
                '' if ncc else '', '2. Người dùng nhập Phiếu hạch toán rồi nhấn Enter / bấm Tìm kiếm.\n' if ncc else '2. Người dùng bấm Tìm kiếm để tải lại khi cần.\n')],
            ['Dòng sự kiện phụ', '• Kỳ = Tuỳ chọn chưa đủ 2 ngày: chưa tải; bấm Tìm kiếm báo "Chọn đủ ngày bắt đầu và ngày kết thúc của kỳ Tuỳ chọn."\n• Bấm Xóa lọc → mọi ô về mặc định.\n• Rời màn rồi quay lại, F5, mở tab mới: bộ lọc về mặc định (màn không ghi nhớ bộ lọc).'],
        ],
        'anh': [('03_custom', 'Kỳ Tuỳ chọn — hiện ô Thời gian'), ('03b_custom_toast', 'Bấm Tìm kiếm khi chưa chọn đủ 2 ngày'),
                ('04_ncc_dropdown' if ncc else '04_nv_dropdown', 'Ô %s — danh sách chọn' % Dv)]
               + ([('14_filtercfg', 'Cửa sổ Cài đặt bộ lọc')] if ncc else []),
        'ui': ui(UI7, loc_rows), 'ui_widths': UI7W,
        'events': [
            ['Đổi Kỳ / ô chọn', 'Change', 'Before:\n– Kỳ = Tuỳ chọn mà chưa đủ 2 ngày: dừng, chưa tải.\nAfter:\n– Tải lại báo cáo + danh mục ô lọc từ trang 1.'],
        ] + ([['Gõ ô Phiếu hạch toán', 'Keypress', 'After:\n– Chưa lọc; chờ Enter hoặc nút Tìm kiếm.']] if ncc else []) + [
            ['Bấm Tìm kiếm / Enter', 'Click', 'Before:\n– Kỳ = Tuỳ chọn chưa đủ 2 ngày → "Chọn đủ ngày bắt đầu và ngày kết thúc của kỳ Tuỳ chọn.", dừng.\nAfter:\n– Tải lại từ trang 1.'],
            ['Bấm Xóa lọc', 'Click', 'After:\n– Mọi ô về mặc định, tải lại.'],
        ],
    })

    # ------------------------------------------------------------------ 2.3 Popup danh sách lượt
    pop = [
        ['Tiêu đề popup', 'Label', 'Hiển thị', 'Theo ô đã bấm', ['- "Tất cả lượt bốc xếp" / "<Tên> - <Mã>" / "Lượt nhập hàng" / "Lượt xuất hàng" / "Loại bốc xếp: <tên>".',
                                                              '- Dòng phụ: "N lượt · %s: X · Kỳ <nhãn kỳ>" (đếm trên toàn bộ dòng của ô đã bấm).' % T]],
        ['Nút phóng to / ×', 'Button', 'Enable', 'Hiển thị', ['- Phóng to popup toàn màn / đóng popup.']],
        ['Ô tìm', 'Textbox', 'Enable', 'Trống', ['- Gợi ý "Tìm phiếu hạch toán / phiếu nhập xuất kho…"; lọc tại chỗ theo số phiếu hạch toán và số phiếu nhập / xuất kho, không phân biệt hoa thường, không dấu; có nút × xoá.']],
        ['Ô Chọn %s' % dv, 'Dropdown', 'Enable / Ẩn', 'Trống', ['- Lựa chọn rút từ các dòng của popup; ẩn khi popup mở từ dòng 1 %s.' % dv]],
        ['Ô Chọn nhập / xuất', 'Dropdown', 'Enable / Ẩn', 'Trống', ['- "Nhập" / "Xuất"; ẩn khi mở từ ô Lượt nhập hàng / Lượt xuất hàng.']],
        ['Ô Chọn loại bốc xếp', 'Dropdown', 'Enable / Ẩn', 'Trống', ['- Ẩn khi mở từ 1 loại ở khối THEO LOẠI BỐC XẾP.']],
        ['Nút Xoá lọc (biểu tượng làm mới)', 'Button', 'Ẩn / Enable', 'Ẩn', ['- Chỉ hiện khi đang có ô lọc / từ khoá; bấm → bỏ hết lọc của popup.']],
        ['Dòng đếm', 'Label', 'Hiển thị', 'b / b lượt', ['- "a / b lượt": a = số dòng sau lọc, b = tổng dòng của ô đã bấm.']],
        ['Bảng lượt', 'Table/Grid', 'Read-only', 'Theo dữ liệu', ['- Cột: STT | %s (tên + mã chữ nhỏ) | Ngày hạch toán | Phiếu hạch toán (liên kết) | Ngày bốc xếp | Phiếu nhập/xuất kho (liên kết) | Nhập/Xuất | Loại bốc xếp | Khối lượng (tấn) | %s.' % (Dv, T),
                                                                 '- Ngày hạch toán, Ngày bốc xếp dạng dd/mm/yyyy HH:mm; Ngày bốc xếp = ngày giờ lập Phiếu nhập hàng / Phiếu xuất hàng.',
                                                                 '- Bấm tiêu đề cột để sắp xếp tăng / giảm (ô trống xuống cuối).',
                                                                 '- Không có dòng: "Không có lượt bốc xếp nào khớp bộ lọc."']],
        ['Phân trang popup', 'Button', 'Enable', '10 dòng/trang', ['- "Hiển thị a–b / N lượt", Số dòng/trang 10 / 20 / 50 / 100.']],
        ['Nút In danh sách', 'Button', 'Enable', 'Hiển thị', ['- Mở cửa sổ "In danh sách" chọn cột (các cột đang hiện trên popup) rồi xem trước bản in danh sách đúng ô đã bấm + ô lọc của popup.']],
        ['Nút Xuất Excel danh sách', 'Button', 'Enable', 'Hiển thị', ['- Mở cửa sổ "Xuất Excel danh sách" chọn cột rồi tải file danh_sach_luot_boc_xep_<yyyymmdd>.xlsx.']],
        ['Nút Đóng', 'Button', 'Enable', 'Hiển thị', ['- Đóng popup, về báo cáo (giữ trang, bộ lọc). Mở lại = trạng thái sạch (không giữ lọc / sắp xếp cũ).']],
    ]
    FR.append({
        'ten': 'Xem danh sách lượt bốc xếp', 'uc': 'uc_popup',
        'qtc': 'Popup, Định dạng số.',
        'gioi_thieu': [
            ['Tên chức năng', 'Xem danh sách lượt bốc xếp của một con số'],
            ['Mô tả', 'Popup liệt kê từng lượt bốc xếp tạo nên con số đã bấm (khối tổng hợp, dòng TỔNG, dòng %s), lọc / tìm / sắp xếp tại chỗ, in và xuất Excel danh sách.' % dv],
            ['Tác nhân', Q],
            ['Điều kiện ban đầu', DK + '\n3. Báo cáo đã tải, con số bấm khác 0.'],
            ['Dòng sự kiện chính', '1. Người dùng bấm một con số gạch chân.\n2. Hệ thống mở popup, tải ĐỦ mọi lượt của ô đó theo bộ lọc báo cáo đang hiển thị.\n3. Người dùng lọc / tìm / sắp xếp, mở phiếu, In danh sách, Xuất Excel danh sách hoặc Đóng.'],
            ['Dòng sự kiện phụ', '• Số 0: không bấm được.\n• Lỗi tải: báo lỗi, popup trống.\n• Không dòng nào khớp lọc: "Không có lượt bốc xếp nào khớp bộ lọc."'],
        ],
        'menu_them': ' => Bấm con số Số lượt / ô ở khối tổng hợp',
        'ghi_chu_layout': 'Popup được mở ngay trên màn báo cáo theo đường dẫn ở trên.',
        'anh': [('09_popup', 'Popup danh sách lượt bốc xếp — "%s"' % ('Tất cả lượt bốc xếp' if ncc else 'Lê Văn Chiến - 12110292')),
                ('09b_popup_print', 'Cửa sổ In danh sách của popup (chọn cột)')],
        'ui': ui(UI6, pop), 'ui_widths': UI6W,
        'events': [
            ['Bấm con số', 'Click', 'After:\n– Mở popup trạng thái sạch, tải đủ mọi lượt của ô (bộ lọc báo cáo + phạm vi ô).'],
            ['Gõ ô tìm / chọn ô lọc', 'Keypress / Change', 'After:\n– Lọc tại chỗ, về trang 1, cập nhật dòng đếm "a / b lượt".'],
            ['Bấm tiêu đề cột', 'Click', 'After:\n– Sắp xếp tăng / giảm theo cột trên tập đã lọc.'],
            ['Bấm In danh sách / Xuất Excel danh sách', 'Click', 'After:\n– Mở cửa sổ chọn cột; In → xem trước; Xuất Excel → tải file (ô đã bấm + ô lọc + từ khoá của popup).'],
            ['Bấm Đóng / ×', 'Click', 'After:\n– Đóng popup.'],
        ],
        'them': [
            ('Mục đích thiết kế popup', [
                ('bullet', 'Trả lời "con số này gồm những lượt bốc xếp nào, của phiếu nào, khối lượng và tiền bao nhiêu".'),
                ('bullet', 'Là popup để giữ nguyên báo cáo, bộ lọc và trang đang xem.'),
                ('bullet', 'Ràng buộc khớp số: số dòng popup = con số đã bấm; tổng %s trên dòng phụ = %s của dòng / ô tương ứng.' % (T, T)),
            ]),
            ('Các biến thể theo con số bấm', [('variant', [
                ('Số lượt dòng TỔNG / ô Lượt bốc xếp', 'Mọi lượt theo bộ lọc', 'Tất cả lượt bốc xếp', 'Không ẩn ô nào'),
                ('Số lượt dòng %s' % dv, 'Lượt của %s đó' % dv, '<Tên> - <Mã>', 'Ẩn ô Chọn %s' % dv),
                ('Ô Lượt nhập hàng / Lượt xuất hàng', 'Lượt của Phiếu nhập hàng / Phiếu xuất hàng', 'Lượt nhập hàng / Lượt xuất hàng', 'Ẩn ô Chọn nhập / xuất'),
                ('Số lượt 1 loại bốc xếp', 'Lượt có loại đó', 'Loại bốc xếp: <tên>', 'Ẩn ô Chọn loại bốc xếp'),
            ])]),
        ],
    })

    # ------------------------------------------------------------------ 2.4 Tùy chỉnh cột
    FR.append({
        'ten': 'Tùy chỉnh cột', 'uc': 'uc_cot',
        'qtc': 'Tùy chỉnh cột.',
        'gioi_thieu': [
            ['Tên chức năng', 'Tùy chỉnh cột hiển thị của bảng báo cáo'],
            ['Mô tả', 'Bật / tắt và đổi thứ tự các cột số liệu của bảng; cấu hình lưu theo người dùng và theo màn.'],
            ['Tác nhân', Q], ['Điều kiện ban đầu', DK],
            ['Dòng sự kiện chính', '1. Người dùng bấm nút Cấu hình cột hiển thị.\n2. Hệ thống mở cửa sổ "Tuỳ chỉnh cột".\n3. Người dùng tích / bỏ tích, kéo ☰ đổi thứ tự, bấm Lưu.\n4. Bảng hiển thị theo cấu hình mới.'],
            ['Dòng sự kiện phụ', '• Bấm Đóng: không lưu.\n• Cột STT và cột %s luôn hiện, đứng đầu, không bỏ tích / kéo được.\n• Cấu hình cột không áp vào In / Xuất Excel (2 chức năng này có bước chọn cột riêng).' % K['cot_cay']],
        ],
        'menu_them': ' => Cấu hình cột hiển thị {icon:btn_cauhinhcot}',
        'ghi_chu_layout': 'Cửa sổ Tuỳ chỉnh cột được mở ngay trên màn báo cáo.',
        'anh': [('13_colcfg', 'Cửa sổ Tuỳ chỉnh cột')],
        'ui': ui(UI6, [
            ['Dòng hướng dẫn', 'Label', 'Hiển thị', '–', ['- "Tích chọn cột cần hiển thị, kéo ☰ để đổi thứ tự cột trên bảng."']],
            ['Danh sách cột', 'Checkbox', 'Enable', 'Tích tất cả', ['- STT, %s (khoá), %s.' % (K['cot_cay'], ', '.join(K['cot_so']))]],
            ['Nút Chọn tất cả / Bỏ chọn hết', 'Button', 'Enable', '–', ['- Tích / bỏ tích mọi cột không khoá.']],
            ['Dòng đếm', 'Label', 'Hiển thị', 'Đang chọn %d/%d cột' % (len(K['cot_so']) + 2, len(K['cot_so']) + 2), ['- Cập nhật theo số cột đang tích.']],
            ['Nút Lưu', 'Button', 'Enable', '–', ['- Lưu cấu hình cho tài khoản + màn này, đóng cửa sổ, bảng vẽ lại.']],
            ['Nút Đóng / ×', 'Button', 'Enable', '–', ['- Đóng, không lưu.']],
        ]), 'ui_widths': UI6W,
        'events': [
            ['Bấm Cấu hình cột hiển thị', 'Click', 'After:\n– Mở cửa sổ với cấu hình đang lưu.'],
            ['Tích / kéo ☰', 'Change / Drag', 'After:\n– Đổi cột / thứ tự sẽ lưu.'],
            ['Bấm Lưu', 'Click', 'After:\n– Lưu, đóng cửa sổ, bảng hiển thị theo cấu hình; giữ sau F5 / đăng nhập lại.'],
            ['Bấm Đóng', 'Click', 'After:\n– Đóng, không đổi.'],
        ],
    })

    # ------------------------------------------------------------------ 2.5 In
    in_cot = ', '.join(K['cot_so'])
    FR.append({
        'ten': 'In báo cáo', 'uc': 'uc_in',
        'qtc': 'In.',
        'gioi_thieu': [
            ['Tên chức năng', 'In báo cáo'],
            ['Mô tả', 'Chọn bản in (bảng tổng hợp / danh sách lượt bốc xếp) và cột in, xem trước rồi in. Lấy MỌI trang theo bộ lọc đang hiển thị.'],
            ['Tác nhân', Q], ['Điều kiện ban đầu', DK + '\n3. Báo cáo đã tải xong.'],
            ['Dòng sự kiện chính', '1. Người dùng bấm In báo cáo.\n2. Hệ thống mở cửa sổ "In báo cáo": 2 bản in, khối "Chọn cột in" (tích sẵn hết).\n3. Người dùng chọn bản, chọn cột, bấm In.\n4. Hệ thống mở cửa sổ xem trước; người dùng bấm In để in ra máy in.'],
            ['Dòng sự kiện phụ', '• Bỏ hết cột rồi bấm In: chữ đỏ "Vui lòng chọn ít nhất 1 cột để in", cửa sổ không đóng.\n• Vượt 2.000 dòng: bản xem trước chỉ hiện "Danh sách có N dòng, vượt mức in tối đa 2,000 dòng nên chưa in được. Vui lòng thu hẹp bộ lọc (khoảng thời gian, trạng thái…) rồi in lại, hoặc dùng Xuất Excel cho danh sách dài."\n• Không có dữ liệu: "Không có dữ liệu để in".'],
        ],
        'menu_them': ' => In báo cáo {icon:btn_inbaocao}',
        'ghi_chu_layout': 'Cửa sổ chọn bản in và cửa sổ xem trước được mở ngay trên màn báo cáo.',
        'anh': [('10_print_opt', 'Cửa sổ In báo cáo'), ('11_print_preview', 'Xem trước bản in bảng tổng hợp'), ('11b_print_preview_detail', 'Xem trước bản in danh sách lượt bốc xếp')],
        'ui': ui(UI6, [
            ['Tiêu đề cửa sổ', 'Label', 'Hiển thị', 'In báo cáo', ['- Nút × đóng.']],
            ['Bản "In bảng tổng hợp"', 'Radio', 'Enable', 'Chọn', ['- "Đúng bảng đang xem, đủ mọi trang%s, kèm dòng TỔNG."' % (' và mọi lượt' if ncc else ''), '- Cột: %s; cột STT và %s luôn được in.' % (in_cot, K['cot_cay'])]],
            ['Bản "In danh sách lượt bốc xếp"', 'Radio', 'Enable', '–', ['- "Mỗi dòng 1 lượt bốc xếp, đúng bộ lọc báo cáo hiện tại."', '- Cột: %s, Ngày hạch toán, Phiếu hạch toán, Ngày bốc xếp, Phiếu nhập/xuất kho, Nhập/Xuất, Loại bốc xếp, Khối lượng (tấn), %s.' % (Dv, T)]],
            ['Khối Chọn cột in', 'Checkbox', 'Enable', 'Tích tất cả', ['- Đổi bản in → danh sách cột đổi, tích lại hết. Icon ⓘ ghi cột luôn được in. Ô "Chọn tất cả".']],
            ['Nút In / Hủy', 'Button', 'Enable', '–', ['- In: mở xem trước. Hủy: đóng cửa sổ.']],
            ['Cửa sổ xem trước', 'Label', 'Read-only', 'Theo dữ liệu', [
                '- Tiêu đề "%s" (bản danh sách: "Xem trước danh sách lượt bốc xếp"), nút In, nút ×.' % K['xem_truoc'],
                '- Bản in: tiêu đề công ty, "%s" (bản danh sách: "%s"), dòng điều kiện "Kỳ <nhãn> (theo ngày hạch toán)" + các ô đang lọc; bảng; "Ngày dd Tháng mm Năm yyyy", "Người lập (Ký, họ tên)".' % (K['tieu_de_in'], K['tieu_de_ds'])]],
        ]), 'ui_widths': UI6W,
        'events': [
            ['Bấm In báo cáo', 'Click', 'Before:\n– Báo cáo chưa tải xong → "Báo cáo chưa tải xong, vui lòng thử lại.", dừng.\nAfter:\n– Mở cửa sổ chọn bản + cột.'],
            ['Bấm In (cửa sổ chọn)', 'Click', 'Before:\n– Không tích cột nào → chữ đỏ, dừng.\nAfter:\n– Lấy mọi dòng theo bộ lọc, dựng bản in theo cột đã chọn, mở xem trước.'],
            ['Bấm In (xem trước)', 'Click', 'After:\n– In ra máy in, không mở tab mới.'],
            ['Bấm Hủy / ×', 'Click', 'After:\n– Đóng cửa sổ.'],
        ],
    })

    # ------------------------------------------------------------------ 2.6 Xuất Excel
    FR.append({
        'ten': 'Xuất Excel', 'uc': 'uc_xuat',
        'qtc': 'Xuất Excel.',
        'gioi_thieu': [
            ['Tên chức năng', 'Xuất báo cáo ra Excel'],
            ['Mô tả', 'Chọn bản xuất (bảng tổng hợp / danh sách lượt bốc xếp) và cột, tải file Excel gồm MỌI trang theo bộ lọc đang hiển thị.'],
            ['Tác nhân', Q], ['Điều kiện ban đầu', DK + '\n3. Báo cáo đã tải xong.'],
            ['Dòng sự kiện chính', '1. Người dùng bấm Xuất Excel.\n2. Hệ thống mở cửa sổ "Xuất Excel": "Xuất bảng tổng hợp", "Xuất danh sách lượt bốc xếp", khối "Chọn cột xuất".\n3. Người dùng chọn bản + cột, bấm Xuất Excel.\n4. Trình duyệt tải file: bảng tổng hợp "%s", danh sách "danh_sach_luot_boc_xep_<yyyymmdd>.xlsx".' % K['file']],
            ['Dòng sự kiện phụ', '• Bỏ hết cột: chữ đỏ "Vui lòng chọn ít nhất 1 cột để xuất".\n• Lỗi: "Lỗi khi xuất Excel".'],
        ],
        'menu_them': ' => Xuất Excel {icon:btn_xuatexcel}',
        'ghi_chu_layout': 'Cửa sổ Xuất Excel được mở ngay trên màn báo cáo.',
        'anh': [('12_export_opt', 'Cửa sổ Xuất Excel')],
        'ui': ui(UI6, [
            ['Bản "Xuất bảng tổng hợp" / "Xuất danh sách lượt bốc xếp"', 'Radio', 'Enable', 'Bảng tổng hợp', ['- Cùng bản + cột như In báo cáo, chỉ đổi chữ.']],
            ['Khối Chọn cột xuất', 'Checkbox', 'Enable', 'Tích tất cả', ['- Cột STT luôn được xuất.']],
            ['Nút Xuất Excel / Hủy', 'Button', 'Enable', '–', ['- Xuất Excel (xanh lá): tải file, đóng cửa sổ. Hủy: đóng.']],
            ['File bảng tổng hợp', 'File', '–', '–', ['- Dòng 1 logo công ty; dòng 2 "%s"; dòng 3 "Kỳ <nhãn> (theo ngày hạch toán)" + điều kiện lọc; hàng tiêu đề cột; dòng TỔNG, dòng %s (STT La Mã)%s; cuối "Ngày dd Tháng mm Năm yyyy", "Người lập".' % (K['tieu_de_in'], dv, ', dòng lượt' if ncc else ''),
                                                         '- Ô số là kiểu số, định dạng 1,234,567 (khối lượng lẻ giữ 2 chữ số).']],
            ['File danh sách', 'File', '–', '–', ['- Dòng 2 "%s"; dòng kỳ; dòng "N lượt · Khối lượng: X tấn · Số tiền: Y VND"; mỗi lượt 1 dòng; dòng TỔNG cuối (Khối lượng, %s).' % (K['tieu_de_ds'], T)]],
        ]), 'ui_widths': UI6W,
        'events': [
            ['Bấm Xuất Excel', 'Click', 'Before:\n– Báo cáo chưa tải xong → "Báo cáo chưa tải xong, vui lòng thử lại.".\nAfter:\n– Mở cửa sổ chọn bản + cột.'],
            ['Bấm Xuất Excel (cửa sổ)', 'Click', 'Before:\n– Không tích cột → chữ đỏ, dừng.\nAfter:\n– Lấy mọi dòng theo bộ lọc, dựng file theo bản + cột, tải về.'],
            ['Bấm Hủy / ×', 'Click', 'After:\n– Đóng cửa sổ.'],
        ],
    })

    PERMS = [
        ('%s — mức Tổng công ty' % QUYEN, 'Thấy lượt bốc xếp của mọi công ty; ô Công ty mở (để trống = mọi công ty).'),
        ('%s — mức Công ty' % QUYEN, 'Chỉ thấy %s; ô Công ty khoá.' % K['pham_vi_cty']),
        ('(Không có quyền)', 'Vẫn mở được màn và dùng mọi chức năng; chỉ thấy %s; ô Công ty khoá ở công ty của mình.' % K['pham_vi_minh']),
    ]
    FUNCS = ['FR-01 Xem báo cáo', 'FR-02 Tìm kiếm và lọc', 'FR-03 Xem danh sách lượt bốc xếp', 'FR-04 Tùy chỉnh cột', 'FR-05 In báo cáo', 'FR-06 Xuất Excel']
    br = [
        ('BR-01', 'Kỳ báo cáo', ['– Lọc theo NGÀY HẠCH TOÁN (sớm nhất) của Phiếu nhập hàng / Phiếu xuất hàng chứa lượt; phiếu chưa hạch toán không lên báo cáo.',
                                 '– Tuần này / Tháng này (mặc định) / Tháng trước / Năm nay theo ngày hiện tại; Tuỳ chọn: từ đầu ngày bắt đầu đến hết ngày kết thúc.',
                                 '– Tuỳ chọn phải đủ 2 ngày, ngày kết thúc không trước ngày bắt đầu.'], ['Xem báo cáo', 'Tìm kiếm và lọc']),
        ('BR-02', 'Phạm vi dữ liệu', ['– Mức Tổng công ty: mọi công ty, lọc được theo Công ty.',
                                      '– Mức Công ty: %s.' % K['pham_vi_cty'],
                                      '– Không có quyền: %s.' % K['pham_vi_minh'],
                                      '– Người có nhiều Vai trò: áp mức lớn nhất. Phạm vi áp cho mọi con số: khối tổng hợp, bảng, popup, bản in, file Excel.'], ['Mọi chức năng']),
    ]
    if ncc:
        br += [
            ('BR-03', 'Lượt được tính', ['– Chỉ lượt có loại thuê "Thuê ngoài" và có nhà cung cấp; lượt do công ty tự bốc xếp không lên báo cáo.',
                                         '– Nhà cung cấp không còn trong danh mục vẫn giữ nhóm, hiện "Nhà cung cấp #<số>".'], ['Xem báo cáo']),
            ('BR-04', 'Số tiền sau VAT', ['– Số tiền lượt = thành tiền × (1 + VAT%), làm tròn 2 chữ số lẻ.', '– Dòng nhà cung cấp / TỔNG cộng SAU VAT (bằng tổng các dòng lượt).'], ['Xem báo cáo', 'In', 'Xuất Excel']),
            ('BR-05', 'Lọc Công ty', ['– Theo công ty của Phiếu nhập hàng / Phiếu xuất hàng chứa lượt.', '– Chỉ có tác dụng với người có mức Tổng công ty.'], ['Tìm kiếm và lọc']),
            ('BR-06', 'Ô Nhà cung cấp', ['– Tìm trên toàn danh mục khách hàng / nhà cung cấp (tên, số điện thoại, mã), chọn nhiều; gõ dưới 3 ký tự chỉ 20 kết quả.',
                                         '– Đổi Công ty không xoá Nhà cung cấp đã chọn; xoá Loại bốc xếp.'], ['Tìm kiếm và lọc']),
        ]
    else:
        br += [
            ('BR-03', 'Lượt được tính', ['– Mọi lượt bốc xếp có người bốc xếp, cả lượt công ty tự bốc lẫn thuê ngoài.',
                                         '– 1 lượt có nhiều người: mỗi người 1 dòng tính riêng; Số lượt và Khối lượng của lượt đó được tính cho TỪNG người, nên dòng TỔNG đếm / cộng lặp lượt nhiều người.'], ['Xem báo cáo']),
            ('BR-04', 'Số tiền', ['– Số tiền = tiền công của nhân viên ghi trên lượt (không cộng VAT).'], ['Xem báo cáo', 'In', 'Xuất Excel']),
            ('BR-05', 'Lọc Công ty', ['– Theo công ty nơi nhân viên bốc xếp đang làm việc (hồ sơ hiện tại), không theo công ty của phiếu.', '– Chỉ có tác dụng với người có mức Tổng công ty.'], ['Tìm kiếm và lọc']),
            ('BR-06', 'Ô Nhân viên', ['– Danh sách = nhân viên có lượt bốc xếp trong phạm vi quyền + công ty đang chọn (mọi kỳ, không theo kỳ đang xem); chọn 1 người.',
                                      '– Đổi Công ty → xoá Nhân viên đã chọn.'], ['Tìm kiếm và lọc']),
        ]
    br += [
        ('BR-07', 'Áp dụng bộ lọc', ['– Ô chọn (Kỳ, Công ty, %s) đổi là tải lại ngay; %s.' % (', '.join(K['loc'][2:]) if ncc else 'Nhân viên', 'ô Phiếu hạch toán chỉ áp khi Enter / Tìm kiếm' if ncc else 'nút Tìm kiếm tải lại với điều kiện hiện tại'),
                                     '– Mọi lần lọc / đổi số dòng đưa về trang 1.', '– Màn không ghi nhớ bộ lọc: mở lại, F5, tab mới đều về mặc định.'], ['Tìm kiếm và lọc']),
        ('BR-08', 'Bảng, dòng TỔNG và phân trang', ['– Dòng TỔNG và khối tổng hợp tính trên toàn bộ dữ liệu đã lọc, không theo trang.',
                                                     '– Phân trang theo %s (mặc định 10), STT La Mã liên tục qua trang; %s xếp theo Số tiền giảm dần.' % (dv, dv),
                                                     '– Ô số ở dòng nhóm / TỔNG bằng 0 vẫn in "0"; ô khối tổng hợp = 0 thì ẩn (trừ ô Lượt bốc xếp).'], ['Xem báo cáo']),
        ('BR-09', 'Định dạng', ['– Số dạng 1,234,567, khối lượng tối đa 2 chữ số lẻ.', '– Ngày hạch toán, Ngày bốc xếp dạng dd/mm/yyyy HH:mm.'], ['Xem báo cáo', 'Popup', 'In', 'Xuất Excel']),
        ('BR-10', 'In / Xuất Excel', ['– Lấy MỌI dòng (mọi trang) theo bộ lọc của báo cáo đang hiển thị; chọn bản + cột trước khi in / xuất; phải chọn ít nhất 1 cột.',
                                       '– In tối đa 2.000 dòng; vượt thì không in, gợi ý Xuất Excel.', '– Cấu hình Tùy chỉnh cột không áp vào In / Xuất Excel.'], ['In', 'Xuất Excel']),
        ('BR-11', 'Popup danh sách lượt', ['– Tải đủ mọi lượt của ô đã bấm; lọc, tìm, sắp xếp, phân trang tại chỗ; ô lọc đã cố định bởi ô bấm thì ẩn.', '– Số 0 không bấm được.'], ['Xem danh sách lượt bốc xếp']),
    ]
    P5 = [
        ('Vận chuyển', ('Báo cáo cẩu hàng bốc xếp theo nhân viên' if ncc else 'Báo cáo cẩu hàng bốc xếp theo nhà cung cấp') + ' (cùng nguồn lượt bốc xếp, cùng kỳ / quyền)', 'Vận chuyển => Báo cáo bốc xếp'),
        ('Vận chuyển', 'Báo cáo chi tiết cẩu hàng bốc xếp theo nhân viên (cùng nguồn; %s)' % ('khớp số từng nhân viên với báo cáo này' if not ncc else 'theo người bốc xếp'), 'Vận chuyển => Báo cáo bốc xếp'),
        ('Tài chính', 'Phiếu nhập hàng (chứng từ chứa lượt bốc xếp hàng nhập, ngày hạch toán; mở từ cột Phiếu hạch toán)', 'Tài chính => Hàng hoá - Dịch vụ - Vận chuyển => Nhập hàng'),
        ('Tài chính', 'Phiếu xuất hàng (tab Bốc xếp: loại thuê, nhà cung cấp, loại bốc xếp; ngày hạch toán; mở từ cột Phiếu hạch toán)', 'Tài chính => Hàng hoá - Dịch vụ - Vận chuyển => Xuất hàng'),
        ('Tài chính / Kho', 'Phiếu nhập kho (thao tác Phiếu xếp hàng; mở từ cột Phiếu nhập/xuất kho)', 'Tài chính => Hàng hoá - Dịch vụ - Vận chuyển => Nhập hàng; hoặc Kho => Nhập kho'),
        ('Tài chính', 'Phiếu xuất kho (mở từ cột Phiếu nhập/xuất kho)', 'Tài chính => Hàng hoá - Dịch vụ - Vận chuyển => Xuất hàng'),
    ]
    S = {
        'ten': ten,
        'menu': [('Vận chuyển', 'menu_phanhe'), ('Báo cáo bốc xếp', 'menu_nhom'), (K['muc'], 'menu_muc')],
        'muc_dich': ['Là căn cứ nghiệm thu màn báo cáo.',
                     'Làm rõ nguồn số liệu (lượt bốc xếp trên Phiếu nhập hàng / Phiếu xuất hàng), cách tính từng cột, kỳ theo ngày hạch toán, phạm vi dữ liệu theo quyền "%s" và các chức năng xem chi tiết, in, xuất Excel.' % QUYEN],
        'thuat_ngu': [
            ['Lượt bốc xếp', 'Một dòng bốc xếp ghi trên Phiếu nhập hàng hoặc Phiếu xuất hàng (loại bốc xếp, khối lượng, tiền).'],
            ['Phiếu hạch toán', 'Phiếu nhập hàng (PNH-…) / Phiếu xuất hàng (PXH-…) chứa lượt bốc xếp.'],
            ['Ngày hạch toán', 'Ngày ghi sổ sớm nhất của Phiếu nhập hàng / Phiếu xuất hàng; dùng để xếp kỳ.'],
            ['Ngày bốc xếp', 'Ngày giờ lập Phiếu nhập hàng / Phiếu xuất hàng chứa lượt.'],
        ] + ([['Thuê ngoài', 'Loại thuê của lượt: bốc xếp do nhà cung cấp bên ngoài thực hiện (khác "Công ty" tự bốc).'],
              ['Số tiền (sau VAT)', 'Thành tiền bốc xếp × (1 + VAT%).']] if ncc else
             [['Người bốc xếp', 'Nhân viên ghi trên lượt bốc xếp; 1 lượt có thể nhiều người, mỗi người có tiền công riêng.'],
              ['Số tiền', 'Tiền công bốc xếp của nhân viên trên lượt.']]) + [
            ['Phạm vi dữ liệu', 'Phần số liệu người dùng được xem theo mức quyền (Tổng công ty / Công ty / của mình).'],
        ],
        'quyen_truoc': ['Màn KHÔNG chặn quyền vào: mọi người dùng đăng nhập đều thấy mục menu, mở được màn và dùng mọi chức năng. Quyền "%s" (gán qua Vai trò, mức Tổng công ty hoặc Công ty) chỉ mở rộng PHẠM VI DỮ LIỆU. Màn không có nút nào cần quyền riêng.' % QUYEN],
        'quyen_rows': [list(p) for p in PERMS],
        'ma_tran': [['Chức năng', 'Tổng công ty', 'Công ty', 'Không quyền']] + [[f, 'Có', 'Có', 'Có'] for f in FUNCS],
        'ma_tran_widths': [3.0, 1.1, 1.1, 1.1],
        'quyen_sau': ['Mọi chức năng dùng được với mọi mức; khác nhau ở phạm vi số liệu (BR-02). "Công ty đang làm việc" = công ty người dùng đang chọn khi đăng nhập; đổi công ty làm việc thì phạm vi tính lại theo công ty mới.'],
        'fr': FR,
        'quy_tac': br,
        'phan5': {'cau_dan': 'Các màn dưới đây là chứng từ nguồn sinh ra lượt bốc xếp (mở được từ báo cáo) hoặc báo cáo dùng chung dữ liệu lượt bốc xếp.', 'rows': P5},
    }
    UML = {
        'actor': 'Người dùng đã đăng nhập',
        'mains': [('FR-01', 'Xem báo cáo', 'view'), ('FR-05', 'In báo cáo', 'io'), ('FR-06', 'Xuất Excel', 'io')],
        'subs': [('FR-02', 'Tìm kiếm và lọc', 'view'), ('FR-03', 'Xem danh sách lượt bốc xếp', 'view'), ('FR-04', 'Tùy chỉnh cột', 'view')],
        'rieng': [('FR-03', 'Xem danh sách lượt bốc xếp', 'view', 'uc_popup'), ('FR-04', 'Tùy chỉnh cột', 'view', 'uc_cot'),
                  ('FR-05', 'In báo cáo', 'io', 'uc_in'), ('FR-06', 'Xuất Excel', 'io', 'uc_xuat')],
    }
    return S, UML


def build_srs_report(scr, S, out):
    """Chép nguyên `sale-customer-debt-reports/docs/compare/gen_srs.build_srs_report` (khuôn đã duyệt)."""
    w = QgWriter(L.SRS_TPL, SRS_ROLES, body_from=10, cover_replace={'Danh mục quốc gia': S['ten']})

    def img(path, cap, width=6.2):
        w.image(path, width=width, caption=cap)
        L._keep_next(w)

    def sub(text):
        w.raw('sub', text)
        L._keep_with_next(w)

    menu = []
    for i, (text, icon) in enumerate(S['menu']):
        menu.append(('Phân hệ ' if i == 0 else ' => ') + text + ' ')
        if icon:
            menu.append(scr.ic(icon, 0.24))

    h1_trang_moi(w, 'Phần 1. Giới thiệu')
    w.h2('1 Mục đích')
    w.p('Tài liệu này đặc tả yêu cầu phần mềm cho màn hình %s, nhằm:' % S['ten'])
    for b in S['muc_dich']:
        w.bullet(b)
    w.h2('2 Thuật ngữ và viết tắt')
    w.table([['Thuật ngữ', 'Mô tả']] + S['thuat_ngu'], widths=[1.3, 3])

    h1_trang_moi(w, 'Phần 2. Phân quyền')
    w.h2('1 Danh sách quyền')
    for p in S['quyen_truoc']:
        w.p(p)
    w.table([['Tên quyền', 'Phạm vi dữ liệu trên màn hình']] + S['quyen_rows'], widths=[2.0, 3])
    w.h2('2 Ma trận phân quyền')
    w.table(S['ma_tran'], widths=S.get('ma_tran_widths'))
    for p in S.get('quyen_sau', []):
        w.p(p)

    h1_trang_moi(w, 'Phần 3. Đặc tả chi tiết theo từng chức năng')
    w.h2('1 Sơ đồ UML tổng quan')
    img(os.path.join(scr.uml, 'overview.png'), 'Sơ đồ Use Case tổng quan màn %s' % S['ten'], 6.3)
    w.h2('2 Đặc tả chi tiết từng chức năng')
    for i, fr in enumerate(S['fr']):
        assert fr.get('ui') and fr.get('events'), fr['ten']
        n = '2.%d' % (i + 1)
        w.h3('%s %s' % (n, fr['ten']))
        k = 0
        if fr.get('uc'):
            k += 1
            sub('%s.%d Biểu đồ Usecase' % (n, k))
            img(os.path.join(scr.uml, fr['uc'] + '.png'), 'Biểu đồ Use Case — %s' % fr['ten'], 6.2)
        k += 1
        sub('%s.%d Giới thiệu' % (n, k))
        w.clone_texts('qtc', ['Quy tắc chung: ', 'Áp dụng SRS Các quy tắc chung ', QTC_LINK,
                              ' - %s Chỉ bổ sung quy tắc riêng của %s.' % (fr['qtc'], S['ten'])])
        w.table([['Mục', 'Nội dung']] + fr['gioi_thieu'], widths=[1, 3.2])
        k += 1
        sub('%s.%d Layout màn hình' % (n, k))
        w.p('Đường dẫn màn hình:')
        extra = scr.segs(fr['menu_them']) if fr.get('menu_them') else []
        w.raw('menu_b', 'Menu: ')
        w.raw('menu', menu + extra)
        if fr.get('ghi_chu_layout'):
            w.p(fr['ghi_chu_layout'])
        for name, cap in fr.get('anh', []):
            img(scr.shot(name), cap, L._fit_width(scr.shot(name)))
        k += 1
        sub('%s.%d Mô tả chi tiết giao diện' % (n, k))
        w.table(fr['ui'], widths=fr.get('ui_widths'))
        k += 1
        sub('%s.%d Danh sách event và xử lý event' % (n, k))
        w.table([['STT', 'Event', 'Loại event', 'Xử lý event']] +
                [[str(j + 1)] + e for j, e in enumerate(fr['events'])], widths=[0.5, 1.4, 0.8, 3.5])
        for title, items in fr.get('them', []):
            k += 1
            sub('%s.%d %s' % (n, k, title))
            for it in items:
                kd = it[0]
                if kd == 'p':
                    w.p(it[1])
                elif kd == 'bullet':
                    w.bullet(it[1])
                elif kd == 'data':
                    w.table([['STT', 'Chỉ tiêu / Cột', 'Cách lấy dữ liệu', 'Nội dung icon ⓘ']] +
                            [[str(j + 1)] + list(r) for j, r in enumerate(it[1])], widths=[0.55, 1.3, 2.9, 2.0])
                elif kd == 'popup':
                    w.table([['STT', 'Bấm vào', 'Popup mở ra', 'Mục đích thiết kế', 'Dữ liệu hiển thị']] +
                            [[str(j + 1)] + list(r) for j, r in enumerate(it[1])], widths=[0.55, 1.55, 1.4, 1.6, 1.65])
                elif kd == 'variant':
                    w.table([['STT', 'Con số / vị trí bấm', 'Tập dòng hiển thị', 'Tiêu đề popup', 'Ô lọc ẩn / cố định']] +
                            [[str(j + 1)] + list(r) for j, r in enumerate(it[1])], widths=[0.55, 1.4, 1.5, 1.6, 1.7])

    h1_trang_moi(w, 'Phần 4. Quy tắc nghiệp vụ')
    w.p('**Quy tắc áp dụng:** Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung '
        'SRS_Các quy tắc chung_VN_1.0. Phần này chỉ ghi các quy tắc đặc thù của %s; không lặp lại các quy tắc '
        'đã có trong SRS quy tắc chung.' % S['ten'])
    j = lambda v: '\n'.join(v) if isinstance(v, (list, tuple)) else v  # noqa: E731
    rows = [['STT', 'Mã quy tắc', 'Tên quy tắc', 'Mô tả', 'Phạm vi áp dụng']]
    for i, q in enumerate(S['quy_tac'], 1):
        assert q[0] == 'BR-%02d' % i, q[0]
        rows.append([str(i), q[0], q[1], j(q[2]), j(q[3])])
    w.table(rows, widths=[0.5, 0.85, 1.3, 2.75, 1.2])

    p5 = S['phan5']
    h1_trang_moi(w, 'Phần 5. Bảng danh sách các màn hình dùng chung / tham chiếu dữ liệu')
    w.p(p5['cau_dan'])
    w.table([['STT', 'Nhóm', 'Màn hình', 'Đường dẫn']] +
            [[str(i + 1)] + list(r) for i, r in enumerate(p5['rows'])], widths=[0.5, 1.0, 2.6, 2.3])

    w.rebuild_toc(levels=(1, 2, 3))
    L._exclude_toc_heading(w)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    L._table_runs_13(w)
    w.save(out)
    L.force_times_new_roman(out)
    return out


def run_srs(here, k):
    K = kind(k)
    S, UML = srs(K)
    scr = L.Screen(here)
    out = os.path.join(here, 'SRS - %s.docx' % K['ten'])
    pdf = os.path.join(here, 'out', 'SRS - %s.pdf' % K['ten'])
    print(L.draw_uml(scr, UML['actor'], UML['mains'], UML['subs'], UML['rieng']))
    print('docx:', build_srs_report(scr, S, out))
    if '--no-word' not in sys.argv:
        print('Số trang:', L.word_finalize(out, pdf))
        L.check_docx(out)


# =============================================================================================== HDSD
def hdsd(K):
    ncc, ten, dv, Dv, T = K['ncc'], K['ten'], K['dv'], K['Dv'], K['tien']
    VAO = 'Bước 1: Truy cập màn hình %s (xem PHẦN 1).' % ten
    cot = [['Cột', 'Ý nghĩa / lấy số từ đâu'],
           ['TỔNG (dòng đầu bảng)', 'Tổng của TOÀN BỘ dữ liệu đã lọc (mọi trang): số lượt, khối lượng, %s. Bấm số lượt để xem từng lượt.' % ('số tiền (sau VAT)' if ncc else 'số tiền')]]
    if ncc:
        cot += [
            ['STT', 'Dòng nhà cung cấp đánh I, II, III…; các dòng lượt bên dưới đánh 1, 2, 3…'],
            ['Nhà cung cấp / Phiếu hạch toán', 'Dòng nhóm: tên + mã nhà cung cấp thuê ngoài. Dòng lượt: số Phiếu xuất hàng / Phiếu nhập hàng chứa lượt (bấm mở phiếu ở tab mới).'],
            ['Số lượt', 'Số lượt bốc xếp thuê ngoài của nhà cung cấp trong kỳ.'],
            ['Ngày hạch toán', 'Ngày giờ hạch toán của phiếu; báo cáo xếp kỳ theo ngày này.'],
            ['Phiếu nhập/xuất kho', 'Phiếu xuất kho / Phiếu nhập kho đi kèm phiếu (bấm mở ở tab mới).'],
            ['Nhập/Xuất', '"Nhập" nếu lượt nằm trên Phiếu nhập hàng, "Xuất" nếu trên Phiếu xuất hàng.'],
            ['Loại bốc xếp', 'Loại bốc xếp chọn trên lượt (vd Xe cẩu, Bốc xếp hàng…).'],
            ['Khối lượng (tấn)', 'Khối lượng ghi trên lượt; dòng nhóm là tổng các lượt.'],
            ['Số tiền (sau VAT)', 'Thành tiền bốc xếp × (1 + VAT%); dòng nhóm, dòng TỔNG cộng các lượt.'],
        ]
    else:
        cot += [
            ['STT', 'Mỗi nhân viên 1 dòng, đánh I, II, III… liên tục qua các trang.'],
            ['Nhân viên', 'Tên và mã nhân viên được ghi là người bốc xếp trên lượt.'],
            ['Số lượt', 'Số lượt nhân viên tham gia trong kỳ (bấm để xem từng lượt).'],
            ['Khối lượng (tấn)', 'Tổng khối lượng các lượt nhân viên tham gia (lượt nhiều người thì mỗi người đều được tính đủ khối lượng lượt đó).'],
            ['Số tiền', 'Tổng tiền công bốc xếp của nhân viên ghi trên các lượt.'],
        ]
    if ncc:
        doc = [
            ('p', 'Đầu báo cáo là khối tổng hợp, bên dưới là bảng: dòng TỔNG, mỗi nhà cung cấp một dòng nhóm, dưới nó là từng lượt bốc xếp. Rê chuột vào biểu tượng ⓘ để xem cách tính.'),
            ('img', '05b_read_summary', 'Khối tổng hợp kỳ tháng 11/2026'),
            ('img', '05_read', 'Bảng báo cáo kỳ tháng 11/2026'),
            ('img', '05c_read_zoom', 'Phóng to cột STT, tên và 2 cột số của ảnh trên'),
            ('table', cot, [1.8, 4.7]),
            ('p', '**Ví dụ đọc số từ 2 ảnh trên:**'),
            ('sub2', 'Dòng TỔNG cột Số tiền (sau VAT) 445,400 = 275,400 (CÔNG TY CỔ PHẦN GIẢI PHÁP ETEK GREEN) + 170,000 (BEIJING FSW TECHNOLOGY CO., LTD).'),
            ('sub2', 'Dòng TỔNG cột Khối lượng (tấn) 5 = 3 + 2; Số lượt 2 = 1 + 1.'),
            ('sub2', 'Khối LƯỢT BỐC XẾP: Lượt bốc xếp 2 = Lượt nhập hàng 1 (PNH-15777) + Lượt xuất hàng 1 (PXH-43237).'),
            ('p', 'Lưu ý: báo cáo chỉ gồm lượt THUÊ NGOÀI đã hạch toán; tiền là tiền SAU VAT.'),
        ]
    else:
        doc = [
            ('p', 'Đầu báo cáo là khối tổng hợp, bên dưới là bảng: dòng TỔNG rồi mỗi nhân viên một dòng, xếp theo số tiền giảm dần. Rê chuột vào biểu tượng ⓘ để xem cách tính.'),
            ('img', '05b_read_summary', 'Khối tổng hợp kỳ tháng 10/2026'),
            ('img', '05_read', 'Bảng báo cáo kỳ tháng 10/2026 (trang 1 / 2)'),
            ('img', '05c_read_zoom', 'Phóng to cột STT, Nhân viên và 3 cột số của ảnh trên'),
            ('table', cot, [1.8, 4.7]),
            ('p', '**Ví dụ đọc số từ 2 ảnh trên:**'),
            ('sub2', 'Khối LƯỢT BỐC XẾP: Lượt bốc xếp 133 = Lượt nhập hàng 51 + Lượt xuất hàng 82; Số tiền 10,245,700 bằng số tiền dòng TỔNG.'),
            ('sub2', 'Dòng I Lê Văn Chiến: 24 lượt, 54.1 tấn, 1,546,900 — bấm số 24 mở popup đúng 24 lượt, dòng phụ "24 lượt · Số tiền: 1,546,900".'),
            ('sub2', 'Dòng IV đến X: 7 nhân viên cùng 7 lượt, cùng 180.2 tấn — đây là các lượt cả nhóm cùng bốc, mỗi người được tính đủ khối lượng lượt.'),
            ('p', 'Lưu ý: dòng TỔNG cộng khối lượng của từng người nên lượt nhiều người được cộng nhiều lần; khi cần tổng khối lượng hàng thực bốc hãy xem báo cáo theo nhà cung cấp / phiếu.'),
        ]
    tk = [
        ('step', 'Bước 1: Từ phân hệ Vận chuyển {icon:menu_phanhe}, chọn nhóm Báo cáo bốc xếp {icon:menu_nhom} rồi chọn {icon:menu_muc}'),
        ('img', '00_menu', 'Menu vào màn %s' % ten),
        ('img', '01_report', 'Màn %s khi mở (kỳ Tháng này)' % ten),
        ('step', 'Bước 2: Chọn kỳ ở ô {icon:o_ky} (mặc định Tháng này). Chọn "Tuỳ chọn" thì chọn thêm ngày bắt đầu, ngày kết thúc ở ô {icon:o_thoigian}.'),
        ('sub', 'Chưa chọn đủ 2 ngày mà bấm Tìm kiếm: hệ thống báo "Chọn đủ ngày bắt đầu và ngày kết thúc của kỳ Tuỳ chọn."'),
        ('step', 'Bước 3: Lọc thêm (tùy chọn):'),
        ('sub', 'Chọn công ty ở ô {icon:o_congty} (chỉ chọn được khi có quyền xem theo tổng công ty).'),
    ]
    if ncc:
        tk += [
            ('sub', 'Bấm ô {icon:o_ncc}, gõ tên, số điện thoại hoặc mã rồi chọn một hoặc nhiều nhà cung cấp.'),
            ('sub', 'Chọn một hoặc nhiều loại ở ô {icon:o_loai}.'),
            ('sub', 'Nhập số phiếu nhập hàng / xuất hàng vào ô {icon:o_phieuht} rồi nhấn Enter hoặc bấm {icon:btn_timkiem}.'),
        ]
    else:
        tk += [('sub', 'Chọn một nhân viên ở ô {icon:o_nhanvien}.')]
    tk += [
        ('sub', 'Đổi ô chọn là báo cáo tự tải lại, không cần bấm Tìm kiếm.'),
        ('step', 'Bước 4: Bấm {icon:btn_xoaloc} để đưa mọi ô về mặc định.'),
    ]
    phan = [('TRUY CẬP VÀ TÌM KIẾM', tk), ('ĐỌC BÁO CÁO', doc)]
    xem = [('step', VAO)]
    if ncc:
        xem += [('step', 'Bước 2: Ở ô chọn cấp {icon:o_cap} chọn "Chỉ nhà cung cấp" để chỉ xem dòng nhà cung cấp, hoặc "Đến từng lượt bốc xếp" để bung hết.'),
                ('sub', 'Hoặc bấm mũi tên {icon:btn_caret} trước tên để bung / thu riêng một nhà cung cấp.'),
                ('step', 'Bước 3: Bấm số phiếu ở dòng lượt, ví dụ {icon:lnk_phieu}, để mở phiếu ở tab mới.'),
                ('step', 'Bước 4: Bấm con số gạch chân ở cột Số lượt, ví dụ {icon:lnk_soluot}, hoặc ở khối tổng hợp để mở danh sách lượt.')]
    else:
        xem += [('step', 'Bước 2: Bấm con số gạch chân ở cột Số lượt của nhân viên, ví dụ {icon:lnk_soluot}, hoặc ở khối tổng hợp để mở danh sách lượt.')]
    xem += [
        ('img', '09_popup', 'Cửa sổ danh sách lượt bốc xếp'),
        ('step', 'Bước %d: Gõ số phiếu vào ô {icon:o_timpopup} hoặc chọn các ô lọc trong cửa sổ; bấm tiêu đề cột để sắp xếp.' % (5 if ncc else 3)),
        ('step', 'Bước %d: Bấm {icon:btn_indanhsach} hoặc {icon:btn_xuatexceldanhsach} để in / xuất đúng danh sách đang xem (chọn cột rồi bấm In / Xuất Excel),' % (6 if ncc else 4)),
        ('sub', 'Hoặc bấm {icon:btn_dong} để quay về báo cáo.'),
    ]
    phan.append(('XEM DANH SÁCH LƯỢT BỐC XẾP', xem))
    phan.append(('TÙY CHỈNH CỘT', [
        ('step', VAO),
        ('step', 'Bước 2: Bấm {icon:btn_cauhinhcot}. Hệ thống mở cửa sổ "Tuỳ chỉnh cột".'),
        ('img', '13_colcfg', 'Cửa sổ Tuỳ chỉnh cột'),
        ('step', 'Bước 3: Tích / bỏ tích cột, kéo biểu tượng ☰ để đổi thứ tự (cột STT và %s luôn hiện).' % K['cot_cay']),
        ('step', 'Bước 4: Bấm {icon:btn_luu}. Bảng hiển thị theo cấu hình mới, lần sau mở màn vẫn giữ.'),
    ]))
    phan.append(('IN BÁO CÁO', [
        ('step', VAO),
        ('step', 'Bước 2: Bấm {icon:btn_inbaocao}. Hệ thống mở cửa sổ "In báo cáo".'),
        ('img', '10_print_opt', 'Cửa sổ In báo cáo'),
        ('step', 'Bước 3: Chọn "In bảng tổng hợp" hoặc "In danh sách lượt bốc xếp", tích các cột cần in.'),
        ('step', 'Bước 4: Bấm {icon:btn_in}. Hệ thống mở bản xem trước gồm mọi trang theo bộ lọc.'),
        ('img', '11_print_preview', 'Bản xem trước'),
        ('step', 'Bước 5: Bấm nút In trên bản xem trước để in ra máy in.'),
        ('sub', 'Danh sách quá 2.000 dòng thì không in được, hãy thu hẹp kỳ hoặc dùng Xuất Excel.'),
    ]))
    phan.append(('XUẤT EXCEL', [
        ('step', VAO),
        ('step', 'Bước 2: Bấm {icon:btn_xuatexcel}. Hệ thống mở cửa sổ "Xuất Excel".'),
        ('img', '12_export_opt', 'Cửa sổ Xuất Excel'),
        ('step', 'Bước 3: Chọn "Xuất bảng tổng hợp" hoặc "Xuất danh sách lượt bốc xếp", tích các cột cần xuất.'),
        ('step', 'Bước 4: Bấm {icon:btn_xuatexcel_popup}. File %s (hoặc danh_sach_luot_boc_xep_<ngày>.xlsx) được tải về, gồm mọi trang theo bộ lọc.' % K['file']),
    ]))
    H = {
        'ten': ten,
        'thuat_ngu': [
            ['Lượt bốc xếp', 'Một dòng bốc xếp ghi trên Phiếu nhập hàng / Phiếu xuất hàng.'],
            ['Phiếu hạch toán', 'Phiếu nhập hàng (PNH-…) / Phiếu xuất hàng (PXH-…) chứa lượt bốc xếp.'],
            ['Kỳ', 'Khoảng thời gian lọc báo cáo, tính theo ngày hạch toán của phiếu.'],
        ] + ([['Thuê ngoài', 'Lượt bốc xếp do nhà cung cấp bên ngoài làm; chỉ lượt này lên báo cáo.']] if ncc
             else [['Người bốc xếp', 'Nhân viên được ghi trên lượt bốc xếp, kèm tiền công.']]),
        'phien_ban': [['1.0', NGAY, 'Đội phát triển phần mềm', 'Phát hành lần đầu']],
        'quyen': [
            'Mọi người dùng đăng nhập đều mở được màn hình và dùng mọi chức năng: xem, tìm kiếm, xem danh sách lượt, tùy chỉnh cột, in, xuất Excel.',
            'Số liệu được xem tùy quyền "%s": mức Tổng công ty xem mọi công ty; mức Công ty xem %s; không có quyền chỉ xem %s.' % (QUYEN, K['pham_vi_cty'], K['pham_vi_minh']),
        ],
        'phan': phan,
    }
    return H


def build_hdsd_report(scr, H, out):
    """Chép nguyên `sale-customer-debt-reports/docs/compare/gen_hdsd.build_hdsd_report` (khuôn đã duyệt)."""
    w = QgWriter(HDSD_TPL, HDSD_ROLES, body_from=19, cover_replace={'Danh mục khu vực': H['ten']})
    h1_trang_moi(w, 'TỔNG QUAN')
    w.h2('1. Thuật ngữ sử dụng trong tài liệu')
    w.table([['Thuật ngữ', 'Giải thích']] + H['thuat_ngu'], widths=[2.0, 4.5])
    w.h2('2. Cập nhật tài liệu')
    w.table([['Phiên bản', 'Ngày', 'Người cập nhật', 'Nội dung']] + H['phien_ban'], widths=[0.9, 1.1, 1.5, 3.0])
    w.h2('3. Quyền sử dụng')
    for s in H['quyen']:
        w.p(s)
    w.h2('4. Sơ đồ chức năng tổng quan')
    w.image(os.path.join(scr.uml, 'overview.png'), caption='Sơ đồ chức năng tổng quan màn ' + H['ten'])
    L._keep_next(w)
    for i, (title, items) in enumerate(H['phan'], 1):
        h1_trang_moi(w, 'PHẦN %d: %s' % (i, title))
        for it in items:
            kd = it[0]
            if kd == 'img':
                w.image(scr.shot(it[1]), width=L._fit_width(scr.shot(it[1]), 6.0), caption=it[2])
                L._keep_next(w)
            elif kd == 'table':
                w.table(it[1], widths=it[2])
            elif kd == 'p':
                w.p(scr.segs(it[1]))
            else:
                w.raw(kd, scr.segs(it[1]))
    w.rebuild_toc(levels=(1, 2))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    L._table_runs_13(w)
    w.save(out)
    L.force_times_new_roman(out)
    return out


def run_hdsd(here, k):
    K = kind(k)
    H = hdsd(K)
    scr = L.Screen(here)
    L.shorten_field_icons(scr)
    out = os.path.join(here, 'HDSD_%s.docx' % K['ten'])
    pdf = os.path.join(here, 'out', 'HDSD_%s.pdf' % K['ten'])
    print('docx:', build_hdsd_report(scr, H, out))
    if '--no-word' not in sys.argv:
        print('Số trang:', L.word_finalize(out, pdf))
        L.check_docx(out)
