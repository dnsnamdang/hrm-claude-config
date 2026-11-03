# -*- coding: utf-8 -*-
"""Testcase màn "Báo cáo hạn mức công nợ khách hàng" (phân hệ Tài chính) — skill testcase-documenter (tc_engine).

Chạy: python gen_testcase.py -> testcase.xlsx
03/11/2026: bản đầu theo checklist "Mẫu tài liệu.xlsx" (../phieu-theo-form-quoc-gia/checklist_mau_tai_lieu.json): section
  xếp theo thứ tự nhóm của checklist, BỎ nhóm màn không có (Thêm mới, Chỉnh sửa, Xóa, Khóa/Mở khóa, Lịch sử thay đổi,
  Import Excel, Duyệt, Không duyệt), đánh số liền. Một nhóm Phân quyền duy nhất (role_tcs=[]); case Cài đặt bộ lọc nằm
  trong nhóm Tìm kiếm và lọc. Đối chiếu ở gen_checklist.py.
Nguồn hành vi (đọc 03/11/2026, nhánh develop cả 2 repo): pages/finance/report-limit-debts/{index.vue,
  components/DebtByEmployeeModal.vue}, V2BaseSmartFilterPanel, V2BaseDataTable, export-fields-modal (+ exportFieldsMixin),
  column-customization-modal, filterStateMixin, utils/export/listExportFile.js; BE ReportLimitDebtService,
  ReportLimitDebtController, CustomerDebtAggregator.
  Số liệu dev-hrm 03/11/2026 (DNS Admin): 8 khách hàng có hạn mức; Chỉ tiêu "Trong hạn mức tính lãi" = 3, 3 chỉ tiêu còn lại = 0.
"""
import os
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', '.claude', 'skills', 'testcase-documenter', 'assets'))
sys.path.insert(0, os.path.join(HERE, '..', 'phieu-theo-form-quoc-gia'))
from tc_engine import build  # noqa: E402
from tc_phieu_bosung import check_no_dash_pre  # noqa: E402

OUT = os.path.join(HERE, 'testcase.xlsx')
MENU = ('Vào phân hệ Tài chính > menu "Kế toán công nợ" > nhóm "Khách hàng" > bấm "Báo cáo hạn mức công nợ khách hàng".')
ADV = 'Bấm Tìm kiếm nâng cao.'
EMPTY = '"Không có dữ liệu phù hợp."'
FOOT0 = '"Không có khách hàng nào."'
POP = 'cửa sổ "Chi tiết hạn mức dư nợ khách hàng 29TPHPTH-1 - CÔNG TY CỔ PHẦN GIẢI PHÁP ETEK GREEN theo NVKD"'

PRE = ('Tài khoản DNS Admin; công ty của tài khoản có 8 khách hàng được khai hạn mức (thứ tự khai): 29TPHPNG-26, 29TPHPKI-151, '
       '29TPHPBO-85, 29TPHKBA-3, 29TPHXNA-27, 43TPHDKH, 29TPHPTH-1, 29TPHPBA-01.')
K6 = ('Khách 43TPHDKH "NGUYEN VAN TEST": Cá nhân, SĐT 0987656789, Hạn mức tính lãi 120,000, Hạn mức được nợ 120,000, chưa có '
      'người liên hệ, không có bút toán công nợ.')
K7 = ('Khách 29TPHPTH-1 "CÔNG TY CỔ PHẦN GIẢI PHÁP ETEK GREEN": Doanh nghiệp tư nhân, SĐT 02436864866, Hạn mức tính lãi '
      '2,147,483,647, Hạn mức được nợ để trống; công nợ sổ 131 của 8 NVKD, tổng 1,380,934,878.')
K1 = 'Khách 29TPHPNG-26: Hạn mức tính lãi để trống, Hạn mức được nợ 500,000,000; người liên hệ "Chị Hương", "TRẦN MINH HƯƠNG".'
ACC_A = 'Tài khoản A: kế toán cùng công ty với DNS Admin, không được gán quyền nào ở phân hệ Tài chính.'
ACC_B = 'Tài khoản B: nhân viên công ty 2 (khác công ty DNS Admin); công ty 2 có 2 khách hàng được khai hạn mức.'
ACC_C = 'Tài khoản C: chưa được gắn công ty làm việc.'
P5 = 'Đổi Số dòng/trang = 5.'


def T(no, func, prio, pre, steps, td, exp):
    if isinstance(pre, (list, tuple)):
        pre = '\n'.join(pre)
    if isinstance(td, (list, tuple)):
        td = '\n'.join(td)
    st = '\n'.join('%d. %s' % (i + 1, s) for i, s in enumerate(steps))
    ex = '\n'.join(x if x.startswith('- ') else '- ' + x for x in exp)
    return ('%03d' % no, func, prio, pre, st, td, ex)


def renum(cases):
    return [('%03d' % (i + 1),) + tuple(c[1:]) for i, c in enumerate(cases)]


DESCRIPTION_BLOCK = [
    ('1. Mục đích tính năng',
     'Báo cáo liệt kê các khách hàng được khai hạn mức công nợ cho công ty của người xem (hạn mức tính lãi, hạn mức được nợ), '
     'kèm thông tin liên hệ và số dư nợ hiện tại. Bấm Mã khách hàng mở cửa sổ công nợ của khách tách theo NVKD. Màn chỉ đọc; '
     'có Xuất Excel chọn trường, Tùy chỉnh cột, Cài đặt bộ lọc.'),
    ('2. Đối tượng được tính / hiển thị',
     '- Dòng khai hạn mức của khách cho công ty = công ty người đăng nhập.\n'
     '- Có hạn mức tính lãi > 0 hoặc hạn mức được nợ > 0.'),
    ('3. Đối tượng bị ẩn / không tính',
     '- Dòng hạn mức của công ty khác; dòng có cả 2 hạn mức bằng 0 / trống.\n'
     '- Màn KHÔNG có Thêm mới, Chỉnh sửa, Xóa, Duyệt / Không duyệt, Khóa / Mở khóa, Import Excel, In, Lịch sử thay đổi.'),
    ('4. Bộ lọc thời gian áp dụng cho',
     'Ô Thời gian KHÔNG lọc bảng chính; chỉ làm mốc tính công nợ ở cửa sổ theo NVKD (Từ ngày chia dư đầu kỳ, Đến ngày chặn '
     'bút toán sau ngày đó).'),
    ('5. Cấu trúc dữ liệu / cây phân cấp',
     '- Khách hàng > dòng hạn mức theo công ty > công nợ theo NVKD. Báo cáo hiện dòng hạn mức của công ty mình; cửa sổ NVKD hiện '
     'công nợ theo nhân viên.'),
    ('6. Quy tắc cộng dồn / deduplicate',
     '- Số dư nợ hiện tại LUÔN 0 (giữ y ERP, chốt 22/10/2026).\n'
     '- Chỉ tiêu: chỉ "Trong hạn mức tính lãi" ra dòng (hạn mức tính lãi > 0); 3 chỉ tiêu còn lại luôn rỗng.\n'
     '- Cửa sổ NVKD: công nợ = dư cuối kỳ sổ 131 theo từng NVKD; Tổng công nợ = tổng các dòng đang hiện.'),
    ('7. Phân quyền cấp',
     '- Màn không gắn quyền: ai vào được phân hệ Tài chính đều dùng được mọi chức năng.\n'
     '- Dữ liệu theo công ty của người đăng nhập; chưa gắn công ty thì rỗng.'),
    ('8. Cách tính các ô thống kê',
     'Dòng "Hiển thị a–b / N": N là số khách hàng có hạn mức khớp bộ lọc trong phạm vi công ty. Cửa sổ NVKD có dòng '
     '"Tổng công nợ".'),
    ('9. Ghi chú đọc bảng',
     '- Tài khoản dùng trong file: DNS Admin, A (cùng công ty, không quyền), B (công ty 2), C (chưa gắn công ty).\n'
     '- Lưu ý: bộ lọc giữ khi tải lại trang (10 phút), mất khi rời sang màn khác.\n'
     '- Lưu ý: số tiền phân cách hàng nghìn bằng dấu phẩy.\n'
     '- Các case "dùng công cụ kiểm thử API" dành cho tester kỹ thuật.'),
]

# ============================================================== I. HIỂN THỊ DANH SÁCH VÀ TRUY CẬP
S1 = [
    T(1, 'Mở màn từ menu', 'P0', PRE, ['Đăng nhập.', MENU], '—',
      ['Mở màn "Báo cáo hạn mức công nợ khách hàng".', 'Bảng hiện 8 dòng, dòng 1 là 29TPHPNG-26.', 'Dưới bảng "Hiển thị 1–8 / 8".']),
    T(2, 'Tiêu đề màn hình', 'P0', PRE, [MENU, 'Quan sát thanh trên cùng, tab trình duyệt và tiêu đề bảng.'], '—',
      ['Thanh trên cùng và tab trình duyệt: "Báo cáo hạn mức công nợ khách hàng".', 'Tiêu đề bảng: "Báo cáo hạn mức công nợ khách hàng".']),
    T(3, 'Các nút chức năng được hiển thị', 'P0', PRE, [MENU, 'Quan sát khối bộ lọc và thanh công cụ của bảng.'], '—',
      ['Khối bộ lọc: ô "Tìm theo mã, tên khách hàng", nút Tìm kiếm, Làm mới, Tìm kiếm nâng cao, Cài đặt bộ lọc.',
       'Thanh công cụ: Xuất Excel, nút biểu tượng cột (Cấu hình cột hiển thị).',
       'KHÔNG có nút Thêm mới, Import Excel, Sửa, Xóa, In, Lịch sử.']),
    T(4, 'Các cột mặc định hiển thị', 'P0', [PRE, 'Tài khoản chưa từng lưu cấu hình cột.'], [MENU, 'Đọc tiêu đề cột từ trái sang phải.'], '—',
      ['Đúng 9 cột: STT, Mã khách hàng, Tên khách hàng, Địa chỉ, Người liên hệ, Số điện thoại, Hạn mức tính lãi, Hạn mức được nợ, '
       'Số dư nợ hiện tại.', 'STT và Mã khách hàng ghim bên trái khi cuộn ngang.']),
    T(5, 'Không có cột mặc định ẩn', 'P2', [PRE, 'Tài khoản chưa từng lưu cấu hình cột.'], [MENU, 'Bấm nút biểu tượng cột.'], '—',
      ['Cửa sổ "Tuỳ chỉnh cột" tích đủ 9/9 cột, không cột nào ẩn sẵn.']),
    T(6, 'Dữ liệu dòng khớp màn Khai báo hạn mức', 'P0', [PRE, K6],
      [MENU, 'Đối chiếu dòng 43TPHDKH với màn Khai báo hạn mức công nợ khách hàng (dòng công ty mình).'], '—',
      ['Mã "43TPHDKH" (chữ xanh gạch chân), Tên "NGUYEN VAN TEST".', 'Địa chỉ "Đặc khu Hoàng Sa, Thành phố Đà Nẵng, Việt Nam".',
       'Người liên hệ trống; Số điện thoại "0987656789".', 'Hạn mức tính lãi "120,000", Hạn mức được nợ "120,000" căn phải; Số dư nợ hiện tại "0".']),
    T(7, 'Hạn mức trống hiện 0 và người liên hệ nhiều dòng', 'P0', [PRE, K1], [MENU, 'Quan sát dòng 29TPHPNG-26.'], '—',
      ['Hạn mức tính lãi hiện "0" (không để trống).', 'Người liên hệ hiện 2 dòng "Chị Hương" và "TRẦN MINH HƯƠNG", tên trùng chỉ 1 lần.',
       'Dòng báo cáo không có cột / nhãn trạng thái (không Khóa / Hoạt động).']),
    T(8, 'Số dư nợ hiện tại luôn bằng 0', 'P0', [PRE, K7], [MENU, 'Quan sát cột Số dư nợ hiện tại của cả 8 dòng.'], '—',
      ['Cả 8 dòng đều "0", kể cả 29TPHPTH-1 đang có công nợ 1,380,934,878 ở cửa sổ NVKD.',
       'Lưu ý: giữ y hệt ERP theo quyết định 22/10/2026 (#11777) — không phải lỗi.']),
    T(9, 'Danh sách chưa có dữ liệu', 'P1', ACC_C, ['Đăng nhập C.', MENU], '—',
      ['Bảng hiện ' + EMPTY, 'Dưới bảng ' + FOOT0, 'Không báo lỗi.']),
    T(10, 'Không có dữ liệu phù hợp bộ lọc', 'P1', PRE, [MENU, 'Nhập "ZZZ999" vào ô tìm nhanh, bấm Tìm kiếm.'], 'Ô tìm nhanh: ZZZ999',
      ['Bảng hiện ' + EMPTY, 'Dưới bảng ' + FOOT0]),
    T(11, 'Số dòng mặc định / trang', 'P1', PRE, [MENU, 'Quan sát ô Số dòng/trang.'], '—',
      ['Mặc định 10; ô có 5, 10, 20, 50, 100.']),
    T(12, 'Thay đổi số dòng / trang', 'P0', PRE, [MENU, P5], 'Số dòng/trang: 5',
      ['Bảng hiện 5 dòng (29TPHPNG-26 … 29TPHXNA-27).', 'Tự quay về trang 1, "Hiển thị 1–5 / 8"; có 2 trang.']),
    T(13, 'Trang trước / trang tiếp theo', 'P0', PRE, [MENU, P5, 'Bấm nút ›.', 'Bấm nút ‹.'], '—',
      ['Bước 3: trang 2 có 43TPHDKH, 29TPHPTH-1, 29TPHPBA-01; "Hiển thị 6–8 / 8".', 'Bước 4: về trang 1, "Hiển thị 1–5 / 8".']),
    T(14, 'Trang đầu / trang cuối', 'P1', PRE, [MENU, P5, 'Bấm nút ».', 'Bấm nút «.'], '—',
      ['Bước 3: trang 2 (trang cuối), 3 dòng.', 'Bước 4: về trang 1.']),
    T(15, 'Trạng thái nút phân trang ở trang đầu / cuối', 'P2', PRE, [MENU, P5, 'Ở trang 1 quan sát « và ‹.', 'Về trang cuối, quan sát › và ».'], '—',
      ['Trang 1: « và ‹ mờ, bấm không tác dụng.', 'Trang cuối: › và » mờ, bấm không tác dụng.']),
    T(16, 'STT liên tục giữa các trang', 'P0', PRE, [MENU, P5, 'Sang trang 2.'], '—', ['Trang 2: STT 6, 7, 8.']),
    T(17, 'Tổng số bản ghi', 'P0', PRE, [MENU, 'Đọc dòng dưới bảng.', ADV, 'Chọn Chỉ tiêu vượt hạn mức = Trong hạn mức tính lãi.'], '—',
      ['Bước 2: "Hiển thị 1–8 / 8".', 'Bước 4: "Hiển thị 1–3 / 3" (43TPHDKH, 29TPHPTH-1, 29TPHPBA-01).']),
    T(18, 'Về trang 1 khi thay đổi bộ lọc', 'P0', PRE, [MENU, P5, 'Sang trang 2.', ADV, 'Chọn Loại hình tổ chức = Doanh nghiệp tư nhân.'], '—',
      ['Danh sách tự nạp lại ở trang 1.', 'Dòng tổng "Hiển thị 1–5 / 7".']),
    T(19, 'Về trang 1 khi thay đổi số dòng', 'P1', PRE, [MENU, P5, 'Sang trang 2.', 'Đổi Số dòng/trang = 10.'], '—',
      ['Quay về trang 1, "Hiển thị 1–8 / 8".']),
    T(20, 'Sắp xếp mặc định', 'P1', PRE, [MENU, 'Quan sát thứ tự dòng, chưa bấm tiêu đề cột nào.'], '—',
      ['Thứ tự khai hạn mức: 29TPHPNG-26, 29TPHPKI-151, 29TPHPBO-85, 29TPHKBA-3, 29TPHXNA-27, 43TPHDKH, 29TPHPTH-1, 29TPHPBA-01.',
       'Không cột nào có mũi tên sắp xếp đang bật.']),
    T(21, 'Sắp xếp tăng dần theo Hạn mức được nợ', 'P0', PRE, [MENU, 'Bấm tiêu đề cột Hạn mức được nợ.'], '—',
      ['Mũi tên lên; thứ tự 29TPHPTH-1 (0), 43TPHDKH (120,000), 29TPHPBA-01 (3,000,000), 29TPHPKI-151, 29TPHPBO-85 (50,000,000), '
       '29TPHKBA-3, 29TPHXNA-27, 29TPHPNG-26 (500,000,000).', 'Hai dòng bằng nhau xếp theo thứ tự khai.']),
    T(22, 'Sắp xếp giảm dần', 'P0', PRE, [MENU, 'Bấm tiêu đề Hạn mức tính lãi 2 lần.', 'Bấm tiêu đề Tên khách hàng 2 lần.'], '—',
      ['Bước 2: dòng đầu 29TPHPTH-1 (2,147,483,647), rồi 29TPHPBA-01, 43TPHDKH.',
       'Bước 3: tên giảm dần, dòng đầu 43TPHDKH "NGUYEN VAN TEST", dòng cuối 29TPHPTH-1 "CÔNG TY CỔ PHẦN GIẢI PHÁP ETEK GREEN".']),
    T(23, 'Sắp xếp theo Mã khách hàng và Số dư nợ hiện tại', 'P1', PRE,
      [MENU, 'Bấm tiêu đề Mã khách hàng.', 'Bấm tiêu đề Số dư nợ hiện tại.'], '—',
      ['Bước 2: tăng dần 29TPHKBA-3, 29TPHPBA-01, 29TPHPBO-85, 29TPHPKI-151, 29TPHPNG-26, 29TPHPTH-1, 29TPHXNA-27, 43TPHDKH.',
       'Bước 3: mọi dòng bằng 0 nên thứ tự về thứ tự khai hạn mức.', 'Màn không có cột Ngày tạo / Ngày cập nhật.']),
    T(24, 'Cột không hỗ trợ sắp xếp', 'P2', PRE, [MENU, 'Bấm tiêu đề STT, Địa chỉ, Người liên hệ, Số điện thoại.'], '—',
      ['Các tiêu đề này không có biểu tượng sắp xếp.', 'Bấm không đổi thứ tự, không nạp lại.']),
    T(25, 'Giữ sắp xếp khi chuyển trang', 'P1', PRE, [MENU, P5, 'Bấm tiêu đề Mã khách hàng (tăng dần).', 'Sang trang 2.'], '—',
      ['Trang 2: 29TPHPTH-1, 29TPHXNA-27, 43TPHDKH (tiếp thứ tự tăng dần).', 'Mũi tên sắp xếp vẫn ở cột Mã khách hàng.']),
    T(26, 'Về trang 1 khi đổi sắp xếp', 'P1', PRE, [MENU, P5, 'Sang trang 2.', 'Bấm tiêu đề Tên khách hàng.'], '—',
      ['Danh sách quay về trang 1, sắp theo Tên khách hàng tăng dần.']),
    T(27, 'Không có dòng của công ty khác hoặc hạn mức bằng 0', 'P0',
      [PRE, 'Khách 29TPHPBA "MR HOANG A" chỉ có hạn mức khai cho công ty 2; khách X có dòng công ty mình với cả 2 hạn mức = 0.'],
      [MENU, 'Tìm "29TPHPBA".', 'Tìm theo mã khách X.'], '—',
      ['Bước 2: chỉ ra 29TPHPBA-01, không có 29TPHPBA.', 'Bước 3: ' + EMPTY]),
    T(28, 'Phiên đăng nhập hết hạn khi đang ở báo cáo', 'P2', [PRE, 'Phiên đăng nhập đã hết hạn (đăng xuất ở tab khác).'],
      [MENU, P5, 'Bấm sang trang 2.'], '—', ['Báo "Phiên đăng nhập đã hết hạn".', 'Tự chuyển về màn đăng nhập, không hiện dữ liệu.']),
]

# ============================================================== II. TÌM KIẾM VÀ LỌC
S2 = [
    T(1, 'Tìm theo mã khách hàng chính xác', 'P0', [PRE, K6], [MENU, 'Nhập "43TPHDKH", bấm Tìm kiếm.'], 'Ô tìm nhanh: 43TPHDKH',
      ['Chỉ còn 1 dòng 43TPHDKH: "Hiển thị 1–1 / 1".']),
    T(2, 'Tìm theo một phần mã / tên', 'P0', PRE, [MENU, 'Nhập "29tphp", bấm Tìm kiếm.', 'Đổi thành "ETEK", bấm Tìm kiếm.'],
      ['Ô tìm nhanh: 29tphp', 'Ô tìm nhanh: ETEK'],
      ['Bước 2: 5 dòng 29TPHPNG-26, 29TPHPKI-151, 29TPHPBO-85, 29TPHPTH-1, 29TPHPBA-01.', 'Bước 3: 1 dòng 29TPHPTH-1 (khớp tên).']),
    T(3, 'Không phân biệt hoa / thường', 'P0', PRE, [MENU, 'Nhập "etek green", bấm Tìm kiếm.'], 'Ô tìm nhanh: etek green',
      ['Ra 29TPHPTH-1 như khi gõ chữ hoa.']),
    T(4, 'Có dấu / không dấu', 'P1', PRE, [MENU, 'Nhập "công ty", bấm Tìm kiếm.', 'Nhập "cong ty", bấm Tìm kiếm.'],
      ['Ô tìm nhanh: công ty', 'Ô tìm nhanh: cong ty'],
      ['Cả 2 lần ra cùng 6 dòng có tên bắt đầu "CÔNG TY".']),
    T(5, 'Không tìm theo số điện thoại; từ khóa không tồn tại', 'P1', [PRE, K6], [MENU, 'Nhập "0987656789", bấm Tìm kiếm.'],
      'Ô tìm nhanh: 0987656789', ['Bảng hiện ' + EMPTY + ' (ô tìm nhanh chỉ theo mã, tên — #11766).']),
    T(6, 'Ký tự đặc biệt trong ô tìm nhanh', 'P2', PRE, [MENU, 'Nhập "@#$<>", bấm Tìm kiếm.', 'Nhập "%", rồi "_", bấm Tìm kiếm.'],
      ['Ô tìm nhanh: @#$<>', 'Ô tìm nhanh: %', 'Ô tìm nhanh: _'],
      ['Không lỗi, không treo; cả 3 lần ' + EMPTY, 'Ký tự % và _ được hiểu là ký tự thường (không ra toàn bộ dòng).']),
    T(7, 'Khoảng trắng đầu / cuối từ khóa', 'P1', PRE, [MENU, 'Nhập "  43TPHDKH  ", bấm Tìm kiếm.'], 'Ô tìm nhanh: "  43TPHDKH  "',
      ['Hệ thống bỏ khoảng trắng đầu / cuối, ra 1 dòng 43TPHDKH.']),
    T(8, 'Độ dài ô tìm nhanh', 'P2', PRE, [MENU, 'Dán chuỗi 300 ký tự vào ô tìm nhanh, bấm Tìm kiếm.'], 'Chuỗi 300 ký tự chữ và số',
      ['Ô nhận hết chuỗi, không lỗi, không treo.', 'Bảng ' + EMPTY, 'Lưu ý: ô chưa giới hạn số ký tự.']),
    T(9, 'Xóa từ khóa', 'P1', 'Đang tìm "ETEK", bảng còn 1 dòng.', ['Bấm nút × trong ô tìm nhanh.', 'Bấm Tìm kiếm.'], '—',
      ['Sau bước 1 bảng chưa đổi (ô tìm nhanh chỉ áp khi bấm Tìm kiếm).', 'Sau bước 2 hiện lại đủ 8 dòng.']),
    T(10, 'Áp từ khóa bằng Enter hoặc nút Tìm kiếm', 'P0', PRE, [MENU, 'Nhập "29tphp", nhấn Enter.', 'Làm mới, nhập lại "29tphp", bấm Tìm kiếm.'],
      'Ô tìm nhanh: 29tphp', ['Cả 2 cách đều ra 5 dòng, về trang 1.']),
    T(11, 'Giá trị mặc định của bộ lọc', 'P1', PRE, [MENU, ADV], '—',
      ['Ô tìm nhanh trống; Thời gian, Khách hàng, Loại hình tổ chức, Chỉ tiêu vượt hạn mức đều trống.', 'Báo cáo đủ 8 dòng.']),
    T(12, 'Lọc Loại hình tổ chức', 'P0', PRE, [MENU, ADV, 'Mở ô Loại hình tổ chức.', 'Chọn "Cá nhân".', 'Đổi sang "Cơ quan nhà nước".'], '—',
      ['Ô có 5 lựa chọn: Cá nhân, Doanh nghiệp tư nhân, Doanh nghiệp nước ngoài, Tổ chức phi chính phủ, Cơ quan nhà nước.',
       'Bước 4: lọc ngay, còn 1 dòng 43TPHDKH.', 'Bước 5: ' + EMPTY]),
    T(13, 'Lọc Chỉ tiêu "Trong hạn mức tính lãi"', 'P0', PRE, [MENU, ADV, 'Mở ô Chỉ tiêu vượt hạn mức.', 'Chọn "Trong hạn mức tính lãi".'], '—',
      ['Ô có 4 lựa chọn: Trong hạn mức tính lãi, Trong hạn mức được nợ, Vượt hạn mức tính lãi, Vượt hạn mức công nợ.',
       'Còn 3 dòng có Hạn mức tính lãi > 0: 43TPHDKH, 29TPHPTH-1, 29TPHPBA-01.']),
    T(14, 'Lọc 3 chỉ tiêu còn lại luôn rỗng', 'P0', PRE,
      [MENU, ADV, 'Chọn lần lượt "Trong hạn mức được nợ", "Vượt hạn mức tính lãi", "Vượt hạn mức công nợ".'], '—',
      ['Cả 3 lần bảng ' + EMPTY + ' dù có 7 khách có Hạn mức được nợ > 0.',
       'Lưu ý: giữ y hệt ERP (số dư luôn 0, chốt 22/10/2026 #11777) — không phải lỗi.']),
    T(15, 'Lọc Khách hàng', 'P0', [PRE, K7], [MENU, ADV, 'Gõ "2" vào ô Khách hàng.', 'Gõ tiếp "9TPHPTH-1", chọn "29TPHPTH-1 - CÔNG TY CỔ PHẦN GIẢI PHÁP ETEK GREEN".'],
      'Khách hàng: 29TPHPTH-1',
      ['Bước 3: gõ 1 ký tự chưa hiện gợi ý (cần tối thiểu 2 ký tự).',
       'Bước 4: gợi ý dạng "Mã - Tên" gồm 29TPHPTH-120, 29TPHPTH-12, 29TPHPTH-1 (khách tạo gần nhất trước).',
       'Chọn xong lọc ngay: còn đúng 1 dòng 29TPHPTH-1.']),
    T(16, 'Ô Khách hàng tìm toàn bộ danh mục và giới hạn số gợi ý', 'P1', PRE,
      [MENU, ADV, 'Gõ "ab" vào ô Khách hàng.', 'Gõ "CÔNG TY".', 'Gõ "0987656789".', 'Gõ "BÔNG", chọn "15TPHXNA-28 - CÔNG TY TNHH BỒNG NGUYÊN VIỆT NAM".'], '—',
      ['Bước 3: tối đa 20 gợi ý (dưới 3 ký tự).', 'Bước 4: tối đa 50 gợi ý.', 'Bước 5: ra "43TPHDKH - NGUYEN VAN TEST" (tìm theo SĐT).',
       'Bước 6: khách không có hạn mức của công ty mình: bảng ' + EMPTY]),
    T(17, 'Lọc Thời gian không đổi bảng chính', 'P0', PRE,
      [MENU, ADV, 'Chọn Thời gian Từ ngày 01/01/2026.', 'Chọn Đến ngày 31/01/2026.'], 'Thời gian: 01/01/2026 – 31/01/2026',
      ['Bước 3: chưa nạp lại (mới chọn 1 đầu).', 'Bước 4: nạp lại nhưng vẫn đủ 8 dòng, Số dư nợ hiện tại vẫn 0.',
       'Lịch Đến ngày không cho chọn trước 01/01/2026.']),
    T(18, 'Kết hợp từ khóa với 1 ô lọc', 'P0', PRE, [MENU, 'Nhập "ETEK", bấm Tìm kiếm.', ADV, 'Chọn Chỉ tiêu = Trong hạn mức tính lãi.'],
      ['Từ khóa: ETEK', 'Chỉ tiêu: Trong hạn mức tính lãi'], ['Còn 1 dòng 29TPHPTH-1.']),
    T(19, 'Kết hợp 2 ô lọc với nhau', 'P0', PRE, [MENU, ADV, 'Chọn Loại hình tổ chức = Doanh nghiệp tư nhân.', 'Chọn Chỉ tiêu = Trong hạn mức tính lãi.'],
      ['Loại hình: Doanh nghiệp tư nhân', 'Chỉ tiêu: Trong hạn mức tính lãi'],
      ['Bước 3: 7 dòng.', 'Bước 4: còn 2 dòng 29TPHPTH-1, 29TPHPBA-01 thỏa CẢ HAI điều kiện.']),
    T(20, 'Kết hợp cả 3 tiêu chí', 'P1', PRE,
      [MENU, 'Nhập "29tphp", bấm Tìm kiếm.', ADV, 'Chọn Loại hình = Doanh nghiệp tư nhân.', 'Chọn Chỉ tiêu = Trong hạn mức tính lãi.'],
      ['Từ khóa: 29tphp', 'Loại hình: Doanh nghiệp tư nhân', 'Chỉ tiêu: Trong hạn mức tính lãi'],
      ['Còn 2 dòng 29TPHPTH-1, 29TPHPBA-01.', 'Bấm Làm mới xóa cả 3 tiêu chí.']),
    T(21, 'Kết hợp tìm kiếm không có kết quả', 'P1', PRE, [MENU, 'Nhập "ETEK", bấm Tìm kiếm.', ADV, 'Chọn Loại hình = Cá nhân.'], '—',
      ['Bảng ' + EMPTY, 'Dưới bảng ' + FOOT0]),
    T(22, 'Tổng số và phân trang sau lọc', 'P0', PRE, [MENU, P5, ADV, 'Chọn Loại hình = Doanh nghiệp tư nhân.', 'Bấm trang cuối.'], '—',
      ['"Hiển thị 1–5 / 7"; có 2 trang.', 'Trang cuối "Hiển thị 6–7 / 7", 2 dòng.']),
    T(23, 'Sắp xếp sau lọc', 'P1', 'Đang lọc Chỉ tiêu = Trong hạn mức tính lãi.', ['Bấm tiêu đề Hạn mức tính lãi 2 lần.'], '—',
      ['Chỉ 3 dòng được sắp giảm dần: 29TPHPTH-1, 29TPHPBA-01, 43TPHDKH; bộ lọc giữ nguyên.']),
    T(24, 'Làm mới xóa toàn bộ điều kiện', 'P0', 'Đang tìm "29tphp", lọc Loại hình, Chỉ tiêu, Thời gian, sắp theo Tên, ở trang 2.',
      ['Bấm Làm mới.'], '—', ['Mọi ô kể cả ô tìm nhanh về trống; bỏ sắp xếp.', 'Nạp lại từ trang 1, đủ 8 dòng.']),
    T(25, 'Chuyển màn rồi quay lại', 'P1', 'Đang lọc Chỉ tiêu = Trong hạn mức tính lãi (3 dòng).',
      ['Vào màn Khai báo hạn mức công nợ KH bằng menu.', 'Quay lại màn báo cáo bằng menu.'], '—',
      ['Bộ lọc về trống, hiện đủ 8 dòng.', 'Lưu ý: màn không giữ bộ lọc khi rời sang màn khác — ghi nhận nếu nghiệp vụ yêu cầu giữ.']),
    T(26, 'Tải lại trang (F5) khi đang lọc', 'P1', 'Đang lọc Chỉ tiêu = Trong hạn mức tính lãi, khối Tìm kiếm nâng cao đang mở.',
      ['Nhấn F5 trong vòng 10 phút.', 'Đợi quá 10 phút không thao tác, nhấn F5.'], '—',
      ['Bước 1: màn mở lại vẫn giữ Chỉ tiêu = Trong hạn mức tính lãi (3 dòng), khối nâng cao vẫn mở.', 'Bước 2: bộ lọc về trống, 8 dòng.']),
    T(27, 'Mở màn trong tab trình duyệt mới', 'P2', 'Đang lọc Loại hình = Cá nhân ở tab 1 (vừa lọc dưới 10 phút).',
      ['Mở màn Báo cáo hạn mức công nợ khách hàng ở tab mới.'], '—',
      ['Tab mới khôi phục bộ lọc ghi tạm của trình duyệt (Loại hình = Cá nhân, 1 dòng).',
       'Lưu ý: bộ lọc ghi tạm dùng chung giữa các tab cùng trình duyệt.']),
    T(28, 'Đổi tài khoản trên cùng trình duyệt', 'P1', 'Tài khoản DNS Admin đang lọc Loại hình = Cá nhân.',
      ['Đăng xuất.', 'Đăng nhập tài khoản A trên cùng trình duyệt.', MENU], '—',
      ['Rời màn để đăng xuất làm xóa bộ lọc: A thấy bộ lọc trống, 8 dòng của công ty.']),
    T(29, 'Khoảng ngày sai khi gọi thẳng', 'P2', PRE,
      ['Dùng công cụ kiểm thử API gọi chức năng lấy báo cáo với Từ ngày 10/10/2026, Đến ngày 01/10/2026.'], '—',
      ['Bị từ chối với thông báo "Đến ngày phải lớn hơn hoặc bằng Từ ngày.".', 'Trên giao diện lịch đã chặn chọn ngày sai.']),
    T(30, 'Cài đặt bộ lọc: ẩn một tiêu chí', 'P1', PRE, [MENU, 'Bấm Cài đặt bộ lọc, bỏ tích Thời gian, bấm Lưu.', ADV], '—',
      ['Báo "Cập nhật thành công".', 'Khối Tìm kiếm nâng cao không còn ô Thời gian; ô tìm nhanh + 3 ô còn lại bày trên 1 hàng nếu tối đa 3 ô.']),
    T(31, 'Cài đặt bộ lọc: danh sách tiêu chí', 'P2', PRE, [MENU, 'Bấm Cài đặt bộ lọc.'], '—',
      ['Cửa sổ "Cài đặt bộ lọc" có 4 tiêu chí: Thời gian, Khách hàng, Loại hình tổ chức, Chỉ tiêu vượt hạn mức; đánh số 1–4.',
       'Có nút Lưu, Khôi phục mặc định, Đóng, (x).']),
    T(32, 'Cài đặt bộ lọc: Khôi phục mặc định và đóng không lưu', 'P2', 'Đã ẩn ô Thời gian ở case trên.',
      ['Bấm Cài đặt bộ lọc, bấm Khôi phục mặc định, bấm Đóng.', 'Mở lại, bấm Khôi phục mặc định, bấm Lưu.'], '—',
      ['Bước 1: đóng không lưu, ô Thời gian vẫn ẩn.', 'Bước 2: tích lại đủ 4 tiêu chí, ô Thời gian hiện lại.']),
    T(33, 'Cài đặt bộ lọc: kéo đổi thứ tự tiêu chí', 'P2', PRE, [MENU, 'Bấm Cài đặt bộ lọc, kéo Chỉ tiêu vượt hạn mức lên đầu, bấm Lưu.', ADV], '—',
      ['Ô Chỉ tiêu vượt hạn mức đứng đầu khối Tìm kiếm nâng cao.']),
    T(34, 'Cài đặt bộ lọc: ẩn tiêu chí đang có giá trị', 'P2', 'Đang lọc Loại hình = Cá nhân (1 dòng).',
      ['Bấm Cài đặt bộ lọc, bỏ tích Loại hình tổ chức, bấm Lưu.'], '—', ['Ô Loại hình biến mất, giá trị bị bỏ, báo cáo về 8 dòng.']),
]

# ============================================================== III. XEM CHI TIẾT (CỬA SỔ THEO NVKD)
S3 = [
    T(1, 'Mở cửa sổ chi tiết theo NVKD', 'P0', [PRE, K7], [MENU, 'Bấm mã "29TPHPTH-1".'], '—',
      ['Mở ' + POP + ' ngay trên báo cáo (cửa sổ nổi).', 'Ô Chọn nhân viên trống; bảng chưa sắp theo cột nào.']),
    T(2, 'Tiêu đề cửa sổ', 'P1', [PRE, K6], [MENU, 'Bấm mã "43TPHDKH".'], '—',
      ['Tiêu đề "Chi tiết hạn mức dư nợ khách hàng 43TPHDKH - NGUYEN VAN TEST theo NVKD".', 'Góc phải tiêu đề có nút (x).']),
    T(3, 'Đầy đủ trường', 'P0', [PRE, K7], [MENU, 'Bấm "29TPHPTH-1".'], '—',
      ['Ô Chọn nhân viên; bảng cột STT, Mã nhân viên, Tên nhân viên, Bộ phận, Phòng ban, Công nợ.',
       'Dòng "Tổng công nợ: 1,380,934,878" dưới bảng; nút Đóng ở chân cửa sổ.']),
    T(4, 'Khớp dữ liệu công nợ', 'P0', [PRE, K7], [MENU, 'Bấm "29TPHPTH-1".', 'Đối chiếu với Báo cáo chi tiết công nợ khách hàng của 29TPHPTH-1.'], '—',
      ['8 dòng: 10510016 Cao Xuân Khang 0; 12310449 Đào Phúc Sơn 44,064,000; 22010683 Lê Thị Thanh Vy 0; 12410479 Vũ Quang Minh '
       '42,266,880; 22210702 Nguyễn Văn Nam 1,277,053,998; 12510548 Vũ Quang Hưng 0; 21710650 Vương Thị Thùy 10,125,000; DNS01 DNS Admin 7,425,000.',
       'Tổng công nợ = tổng 8 dòng = số dư cuối kỳ của khách trên sổ công nợ phải thu.']),
    T(5, 'Khớp với dòng trên báo cáo', 'P0', [PRE, K7], [MENU, 'Bấm "29TPHPTH-1".'], '—',
      ['Tiêu đề đúng mã, tên của dòng đã bấm.',
       'Tổng công nợ 1,380,934,878 KHÁC cột Số dư nợ hiện tại (0) — Lưu ý: cột báo cáo giữ y ERP luôn 0, cửa sổ tính công nợ thật.']),
    T(6, 'Trường chỉ đọc', 'P1', [PRE, K7], ['Mở cửa sổ 29TPHPTH-1.', 'Thử bấm / gõ vào các ô của bảng.'], '—',
      ['Không ô nào sửa được; chỉ ô Chọn nhân viên và tiêu đề Công nợ thao tác được.']),
    T(7, 'Không có nút Lưu', 'P1', [PRE, K7], ['Mở cửa sổ 29TPHPTH-1.', 'Quan sát chân cửa sổ.'], '—',
      ['Chỉ có nút Đóng; không có Lưu, Sửa, Xuất Excel, In.']),
    T(8, 'Lọc theo nhân viên', 'P0', [PRE, K7], ['Mở cửa sổ 29TPHPTH-1.', 'Mở ô Chọn nhân viên.', 'Chọn "12310449 - Đào Phúc Sơn".', 'Bấm × bỏ chọn.'], '—',
      ['Bước 2: 8 lựa chọn dạng "Mã - Tên".', 'Bước 3: còn 1 dòng Đào Phúc Sơn, "Tổng công nợ: 44,064,000".',
       'Bước 4: hiện lại đủ 8 dòng, tổng 1,380,934,878.']),
    T(9, 'Sắp xếp cột Công nợ', 'P1', [PRE, K7], ['Mở cửa sổ 29TPHPTH-1.', 'Bấm tiêu đề Công nợ.', 'Bấm lại.'], '—',
      ['Bước 2: tăng dần, các dòng 0 lên đầu, Nguyễn Văn Nam cuối.', 'Bước 3: giảm dần, dòng đầu Nguyễn Văn Nam 1,277,053,998.',
       'Các cột khác không sắp xếp được.']),
    T(10, 'Mốc Thời gian áp vào cửa sổ', 'P0', [PRE, K7],
      [MENU, ADV, 'Chọn Thời gian 01/01/2025 – 31/12/2025.', 'Bấm "29TPHPTH-1".'], 'Thời gian: 01/01/2025 – 31/12/2025',
      ['Cửa sổ chỉ tính bút toán tới 31/12/2025: còn 6 nhân viên, "Tổng công nợ: 1,353,014,667".',
       'Công nợ có thể âm (Cao Xuân Khang -30,852).']),
    T(11, 'Khách hàng chưa có công nợ', 'P1', [PRE, K6], [MENU, 'Bấm "43TPHDKH".'], '—',
      ['Bảng ' + EMPTY, 'Không hiện dòng Tổng công nợ; ô Chọn nhân viên không có lựa chọn.']),
    T(12, 'Đóng cửa sổ', 'P0', [PRE, K7], ['Mở cửa sổ 29TPHPTH-1, chọn nhân viên Đào Phúc Sơn.', 'Bấm Đóng.',
                                          'Mở lại, bấm (x).', 'Mở lại, click ra ngoài cửa sổ.'], '—',
      ['Mỗi lần cửa sổ đóng ngay, không hỏi xác nhận.', 'Lần mở sau ô Chọn nhân viên trống, bảng chưa sắp.']),
    T(13, 'Giữ trang và bộ lọc khi đóng cửa sổ', 'P1', 'Đang ở trang 2 (5 dòng/trang), sắp theo Mã khách hàng.',
      ['Bấm "29TPHPTH-1" ở trang 2.', 'Bấm Đóng.'], '—', ['Báo cáo vẫn ở trang 2, giữ sắp xếp và bộ lọc.']),
]

# ============================================================== IV. TÙY CHỈNH CỘT
COL = [MENU, 'Bấm nút biểu tượng cột (Cấu hình cột hiển thị).']
COL_PRE = [PRE, 'Tài khoản chưa từng lưu cấu hình cột.']
S4 = [
    T(1, 'Mở cửa sổ tùy chỉnh cột', 'P1', COL_PRE, COL, '—', ['Mở cửa sổ "Tuỳ chỉnh cột" có nút (x), dòng hướng dẫn.']),
    T(2, 'Danh sách cột', 'P1', COL_PRE, COL, '—',
      ['Đủ 9 cột: STT, Mã khách hàng, Tên khách hàng, Địa chỉ, Người liên hệ, Số điện thoại, Hạn mức tính lãi, Hạn mức được nợ, Số dư nợ hiện tại.']),
    T(3, 'Cột được chọn mặc định', 'P1', COL_PRE, COL, '—', ['Cả 9 cột tích; dòng đếm "Đang chọn 9/9 cột".']),
    T(4, 'Hiện cột đang ẩn', 'P0', [PRE, 'Đã ẩn cột Địa chỉ.'], COL + ['Tích Địa chỉ, bấm Lưu.'], '—',
      ['Báo "Cập nhật thành công".', 'Bảng có lại cột Địa chỉ.']),
    T(5, 'Ẩn cột', 'P0', COL_PRE, COL + ['Bỏ tích Địa chỉ, bấm Lưu.'], '—', ['Báo "Cập nhật thành công".', 'Bảng không còn cột Địa chỉ.']),
    T(6, 'Cột bắt buộc không ẩn được', 'P0', COL_PRE, COL + ['Thử bỏ tích STT, Mã khách hàng; di chuột lên biểu tượng cuối dòng.'], '—',
      ['STT, Mã khách hàng: ô tích xám, biểu tượng ổ khóa, gợi ý "Cột bắt buộc — không thể ẩn hoặc đổi vị trí".']),
    T(7, 'Kéo thả đổi thứ tự cột', 'P1', COL_PRE, COL + ['Kéo Số dư nợ hiện tại lên ngay sau Tên khách hàng, bấm Lưu.'], '—',
      ['Cột Số dư nợ hiện tại đứng ngay sau Tên khách hàng trên bảng.']),
    T(8, 'Cột cố định', 'P2', COL_PRE, COL + ['Thử kéo STT, Mã khách hàng.', 'Đóng cửa sổ, cuộn bảng sang phải.'], '—',
      ['STT, Mã khách hàng không kéo được.', 'STT, Mã khách hàng ghim trái khi cuộn ngang.']),
    T(9, 'Lưu cấu hình với Chọn tất cả / Bỏ chọn hết', 'P1', COL_PRE, COL + ['Bấm Bỏ chọn hết, bấm Lưu.', 'Mở lại, bấm Chọn tất cả, bấm Lưu.'], '—',
      ['Bước 3: bảng chỉ còn STT, Mã khách hàng.', 'Bước 4: bảng đủ 9 cột.']),
    T(10, 'Đóng không lưu', 'P1', COL_PRE, COL + ['Bỏ tích Người liên hệ.', 'Bấm Đóng (hoặc (x) / click ra ngoài).', 'Mở lại cửa sổ.'], '—',
      ['Bảng vẫn có cột Người liên hệ.', 'Mở lại thấy Người liên hệ vẫn tích.']),
    T(11, 'Ghi nhớ sau khi tải lại', 'P0', 'Đã lưu cấu hình ẩn Địa chỉ ở TC_04.005.', ['Nhấn F5.'], '—', ['Bảng vẫn không có cột Địa chỉ.']),
    T(12, 'Cấu hình theo tài khoản', 'P1', 'DNS Admin đã ẩn cột Địa chỉ.', ['Đăng nhập A trên cùng trình duyệt, mở màn.',
                                                                           'Đăng nhập DNS Admin ở trình duyệt khác, mở màn.'], '—',
      ['A vẫn thấy cột Địa chỉ.', 'DNS Admin ở trình duyệt khác vẫn không có cột Địa chỉ (lưu theo tài khoản).']),
    T(13, 'Không ảnh hưởng dữ liệu', 'P1', COL_PRE, COL + ['Ẩn 4 cột, bấm Lưu.'], '—', ['Dòng tổng vẫn "Hiển thị 1–8 / 8".']),
    T(14, 'Không ảnh hưởng lọc', 'P1', [PRE, 'Đang lọc Loại hình = Cá nhân.'], COL + ['Ẩn cột Số điện thoại, bấm Lưu.'], '—',
      ['Bộ lọc giữ nguyên, vẫn 1 dòng 43TPHDKH.']),
]

# ============================================================== V. XUẤT EXCEL
EXP = [MENU, 'Bấm Xuất Excel trên thanh công cụ.']
FILE = '"bao-cao-han-muc-cong-no-khach-hang.xlsx"'
S5 = [
    T(1, 'Mở cửa sổ chọn trường', 'P1', PRE, EXP, '—', ['Mở cửa sổ "Chọn trường xuất file", chưa tải file ngay.']),
    T(2, 'Danh sách trường', 'P0', PRE, EXP, '—',
      ['8 trường: Mã khách hàng, Tên khách hàng, Địa chỉ, Người liên hệ, Số điện thoại, Hạn mức tính lãi, Hạn mức được nợ, Số dư nợ '
       'hiện tại.', 'STT không nằm trong danh sách (luôn có trong file).']),
    T(3, 'Trường chọn mặc định theo cột đang hiện', 'P1', [PRE, 'Đã ẩn cột Địa chỉ bằng Tùy chỉnh cột.'], EXP, '—',
      ['7 trường tích sẵn theo thứ tự cột trên bảng, Địa chỉ xếp cuối và không tích; "Đang chọn 7/8 trường".']),
    T(4, 'Xuất với trường mặc định', 'P0', PRE, EXP + ['Bấm Xuất file.'], '—',
      ['Cửa sổ đóng, cạnh nút Xuất Excel hiện tiến độ, tải file ' + FILE + ', báo "Xuất Excel thành công.".',
       'File có STT + 8 cột, 8 dòng dữ liệu.']),
    T(5, 'Xuất tất cả trường', 'P1', [PRE, 'Đã ẩn cột Địa chỉ.'], EXP + ['Bấm Chọn tất cả.', 'Bấm Xuất file.'], '—',
      ['"Đang chọn 8/8 trường".', 'File có STT + 8 cột (gồm Địa chỉ).']),
    T(6, 'Xuất một số trường', 'P0', PRE, EXP + ['Bấm Bỏ chọn hết, tích Mã khách hàng, Hạn mức được nợ.', 'Bấm Xuất file.'], '—',
      ['File đúng STT + 2 cột Mã khách hàng, Hạn mức được nợ.']),
    T(7, 'Không chọn trường nào', 'P1', PRE, EXP + ['Bấm Bỏ chọn hết.'], '—', ['"Đang chọn 0/8 trường"; nút Xuất file bị khóa.']),
    T(8, 'Xuất theo từ khóa tìm kiếm', 'P1', PRE, [MENU, 'Tìm "29tphp".', 'Bấm Xuất Excel, Xuất file.'], '—',
      ['File chỉ gồm 5 dòng 29TPHPNG-26, 29TPHPKI-151, 29TPHPBO-85, 29TPHPTH-1, 29TPHPBA-01.']),
    T(9, 'Xuất theo bộ lọc', 'P0', PRE, [MENU, ADV, 'Chọn Chỉ tiêu = Trong hạn mức tính lãi.', 'Xuất Excel, Xuất file.'], '—',
      ['File đúng 3 dòng 43TPHDKH, 29TPHPTH-1, 29TPHPBA-01.', 'File không có dòng ghi điều kiện lọc / khoảng ngày.']),
    T(10, 'Xuất nhiều trang', 'P0', PRE, [MENU, P5, 'Đang ở trang 1.', 'Xuất Excel, Xuất file.'], '—',
      ['File có đủ 8 dòng (không chỉ 5 dòng trang đang xem).']),
    T(11, 'Xuất danh sách rỗng', 'P0', PRE, [MENU, 'Tìm "ZZZ999".', 'Xuất Excel, Xuất file.'], '—',
      ['KHÔNG tải file; báo "Không có dữ liệu để xuất".',
       'Lưu ý: khác checklist (rỗng vẫn ra file có tiêu đề) — đúng theo thiết kế hiện tại, ghi nhận nếu cần đổi.']),
    T(12, 'Tên file', 'P2', PRE, EXP + ['Bấm Xuất file.'], '—', ['Tên file ' + FILE + '.']),
    T(13, 'Định dạng và bố cục file', 'P1', PRE, EXP + ['Xuất file, mở bằng Excel.'], '—',
      ['Mở được, đuôi .xlsx, sheet "Han muc cong no KH".',
       'Dòng 1 letterhead công ty người đăng nhập rộng bằng bảng; dòng 2 tiêu đề "BÁO CÁO HẠN MỨC CÔNG NỢ KHÁCH HÀNG"; dòng 3 hàng tên cột in đậm có nút lọc.',
       'Bảng có viền; cuối file khối "Ngày ..., tháng ..., năm ...", "Người lập", "(Ký, họ tên)".']),
    T(14, 'Tiêu đề cột trong file', 'P1', PRE, EXP + ['Xuất file.'], '—',
      ['Hàng tên cột: STT, Mã khách hàng, Tên khách hàng, Địa chỉ, Người liên hệ, Số điện thoại, Hạn mức tính lãi, Hạn mức được nợ, Số dư nợ hiện tại.']),
    T(15, 'Thứ tự cột theo kéo thả', 'P1', PRE, EXP + ['Bỏ chọn hết; tích Mã khách hàng, Tên khách hàng, Hạn mức được nợ; kéo Hạn mức được nợ lên đầu.', 'Xuất file.'], '—',
      ['File: STT, Hạn mức được nợ, Mã khách hàng, Tên khách hàng (đúng thứ tự kéo).']),
    T(16, 'Số lượng bản ghi', 'P0', PRE, [MENU, ADV, 'Chọn Loại hình = Doanh nghiệp tư nhân.', 'Xuất file.'], '—',
      ['File đúng 7 dòng dữ liệu, STT 1–7 (khớp dòng tổng trên màn).']),
    T(17, 'Dữ liệu khớp danh sách', 'P0', [PRE, K6], [MENU, 'Tìm "43TPHDKH".', 'Xuất file.'], '—',
      ['Dòng 1: 43TPHDKH, NGUYEN VAN TEST, Đặc khu Hoàng Sa, Thành phố Đà Nẵng, Việt Nam, (trống), 0987656789, 120,000, 120,000, 0.',
       'Giá trị từng ô trùng dòng trên bảng.']),
    T(18, 'Định dạng ngày / số / chữ', 'P1', PRE, EXP + ['Xuất file, mở Excel, chọn các ô Hạn mức được nợ rồi xem thanh trạng thái.'], '—',
      ['Hạn mức tính lãi, Hạn mức được nợ, Số dư nợ hiện tại là ô SỐ định dạng #,##0, Excel cộng SUM được (tổng Hạn mức được nợ 923,120,000).',
       'Hạn mức trống ra 0; Số điện thoại giữ số 0 đầu (02436864866); file không có cột ngày.']),
    T(19, 'Tiếng Việt và ký tự đặc biệt', 'P2', PRE, EXP + ['Xuất file.'], '—',
      ['Tên "CÔNG TY CỔ PHẦN GIẢI PHÁP ETEK GREEN", "TRẦN MINH HƯƠNG" đúng dấu.', 'Người liên hệ nhiều tên xuống dòng trong cùng ô; địa chỉ có "/" giữ nguyên.']),
    T(20, 'Đóng cửa sổ không xuất', 'P2', PRE, EXP + ['Bấm Đóng (hoặc (x) / click ra ngoài).'], '—', ['Cửa sổ đóng, không tải file.']),
]

# ============================================================== VI. ẢNH HƯỞNG CÁC MÀN HÌNH SỬ DỤNG DỮ LIỆU
DECL = 'Vào phân hệ Tài chính > menu "Kế toán công nợ" > nhóm "Khách hàng" > bấm "Khai báo hạn mức công nợ KH".'
S6 = [
    T(1, 'Khai hạn mức mới xuất hiện trên báo cáo', 'P0',
      [PRE, 'Tài khoản E có quyền Quản lý khai báo hạn mức công nợ khách hàng; khách Y chưa có hạn mức của công ty mình.'],
      ['Đăng nhập E.', DECL, 'Nhập Hạn mức công nợ xuất hàng 10,000,000 cho dòng công ty mình của khách Y, bấm Lưu.', MENU, 'Tìm theo mã khách Y.'],
      'Hạn mức công nợ xuất hàng: 10,000,000',
      ['Báo cáo có dòng khách Y: Hạn mức tính lãi 0, Hạn mức được nợ 10,000,000, Số dư nợ hiện tại 0.', 'Tổng số dòng tăng 1 (9).']),
    T(2, 'Sửa hạn mức cập nhật trên báo cáo', 'P0', [PRE, K6, 'Tài khoản E như trên.'],
      [DECL, 'Đổi Hạn mức công nợ tính lãi của 43TPHDKH (công ty mình) thành 200,000, bấm Lưu.', MENU, 'Tìm "43TPHDKH".'], '—',
      ['Hạn mức tính lãi hiện 200,000; các cột khác giữ nguyên.']),
    T(3, 'Đặt hạn mức về 0 thì dòng rời báo cáo', 'P0', [PRE, 'Tài khoản E như trên; khách Y ở case 1.'],
      [DECL, 'Đổi cả 2 hạn mức của khách Y về 0, bấm Lưu.', MENU, 'Tìm theo mã khách Y.'], '—',
      [EMPTY + '; tổng số dòng về 8.']),
    T(4, 'Hạn mức của công ty khác không lên báo cáo', 'P1', [PRE, ACC_B],
      ['Đăng nhập B, khai hạn mức cho khách 43TPHDKH ở dòng công ty 2.', 'Đăng nhập DNS Admin, mở báo cáo, tìm "43TPHDKH".'], '—',
      ['DNS Admin vẫn thấy 1 dòng 43TPHDKH với hạn mức của công ty mình (120,000), không thấy số của công ty 2.']),
    T(5, 'Công nợ theo NVKD cập nhật theo chứng từ', 'P0', [PRE, K7, 'Kế toán vừa duyệt phiếu thu 5,000,000 của khách 29TPHPTH-1 thuộc hợp đồng NVKD Đào Phúc Sơn.'],
      [MENU, 'Bấm "29TPHPTH-1".'], '—',
      ['Dòng Đào Phúc Sơn giảm 5,000,000 (39,064,000); Tổng công nợ giảm tương ứng.', 'Cột Số dư nợ hiện tại trên báo cáo vẫn 0.']),
    T(6, 'Bộ lọc màn liên quan cập nhật', 'P1', [PRE, K6, 'Tài khoản E như trên.'],
      [DECL, 'Đổi Hạn mức công nợ tính lãi của 43TPHDKH về 0 (giữ Hạn mức xuất hàng 120,000), bấm Lưu.', MENU, ADV,
       'Chọn Chỉ tiêu = Trong hạn mức tính lãi.'], '—',
      ['Còn 2 dòng (29TPHPTH-1, 29TPHPBA-01); 43TPHDKH không còn trong chỉ tiêu này.', 'Bỏ lọc thì 43TPHDKH vẫn có (Hạn mức được nợ > 0).']),
    T(7, 'Không xóa được dữ liệu từ báo cáo', 'P1', PRE, [MENU, 'Quan sát từng dòng và thanh công cụ.'], '—',
      ['Không có nút Xóa; dữ liệu khai hạn mức chỉ đổi ở màn Khai báo hạn mức công nợ khách hàng.']),
    T(8, 'Cấp con đúng cấp cha', 'P1', [PRE, K7], [MENU, 'Bấm "29TPHPTH-1".'], '—',
      ['Cửa sổ chỉ có công nợ của đúng khách 29TPHPTH-1, các NVKD đều có bút toán với khách này.']),
    T(9, 'Tham chiếu không mất khi đổi trạng thái', 'P1', [PRE, 'Khách 29TPHPKI-151 vừa được đổi trạng thái ở danh mục khách hàng.'],
      [MENU, 'Tìm "29TPHPKI-151".'], '—', ['Dòng vẫn hiện đủ Mã, Tên, Địa chỉ, Người liên hệ, hạn mức (báo cáo không lọc theo trạng thái khách).']),
    T(10, 'Đổi tên khách hàng đồng bộ', 'P2', [PRE, 'Tên khách 29TPHPBA-01 vừa được sửa ở danh mục khách hàng.'], [MENU, 'Tìm "29TPHPBA-01".'], '—',
      ['Cột Tên khách hàng hiện tên mới; hạn mức giữ nguyên.']),
    T(11, 'Không có bản ghi mồ côi', 'P2', [PRE, 'Dòng hạn mức của khách Y đã bị xóa khỏi màn Khai báo.'], [MENU, 'Tìm theo mã khách Y.'], '—',
      [EMPTY + '; mở cửa sổ NVKD của khách Y bằng công cụ kiểm thử API báo "Lỗi khi tải dữ liệu".']),
    T(12, 'Không có dữ liệu trùng', 'P2', PRE, [MENU, P5, 'So 2 trang khi sắp theo Mã khách hàng.'], '—',
      ['Không dòng nào lặp lại giữa 2 trang; mỗi khách chỉ 1 dòng.', 'Người liên hệ trùng tên chỉ hiện 1 lần trong ô.']),
]

# ============================================================== VII. PHÂN QUYỀN
S7 = renum([
    T(1, 'Xem báo cáo không cần quyền riêng', 'P0', ACC_A, ['Đăng nhập A.', MENU], '—',
      ['A mở được màn, thấy đủ 8 dòng của công ty như DNS Admin.']),
    T(2, 'Phạm vi dữ liệu theo công ty', 'P0', ACC_B, ['Đăng nhập B.', MENU, 'Tìm "29TPHPTH-1".'], '—',
      ['B chỉ thấy 2 dòng của công ty 2.', 'Tìm "29TPHPTH-1" (chỉ có hạn mức của công ty DNS Admin): ' + EMPTY]),
    T(3, 'Chưa gắn công ty', 'P1', ACC_C, ['Đăng nhập C.', MENU, 'Xuất Excel, Xuất file.'], '—',
      ['Bảng ' + EMPTY, 'Xuất báo "Không có dữ liệu để xuất", không tạo file.']),
    T(4, 'Xem chi tiết theo NVKD không cần quyền', 'P0', [ACC_A, K7], ['Đăng nhập A.', MENU, 'Bấm "29TPHPTH-1".'], '—',
      ['A mở được cửa sổ, Tổng công nợ 1,380,934,878 như DNS Admin.']),
    T(5, 'Không có chức năng Thêm mới / Sửa / Xóa / Khóa / Import / Lịch sử', 'P1', 'Tài khoản DNS Admin (quyền cao nhất).',
      [MENU, 'Quan sát thanh công cụ và từng dòng.'], '—',
      ['Không có nút Thêm mới, Sửa, Xóa, Khóa / Mở khóa, Import Excel, In, Lịch sử ở màn.']),
    T(6, 'Xuất Excel trong phạm vi', 'P1', ACC_B, ['Đăng nhập B.', MENU, 'Xuất Excel, Xuất file.'], '—',
      ['File chỉ có 2 dòng của công ty 2; letterhead công ty 2.']),
    T(7, 'Gọi thẳng chức năng bỏ qua giao diện', 'P0', [ACC_B, K7],
      ['Dùng công cụ kiểm thử API, đăng nhập B, gọi chức năng lấy báo cáo với từ khóa "29TPHPTH-1".',
       'Gọi chức năng lấy dữ liệu xuất Excel không kèm bộ lọc.', 'Gọi chức năng mở cửa sổ NVKD của khách 29TPHPTH-1.'], '—',
      ['Bước 1: tổng 0.', 'Bước 2: chỉ 2 dòng của công ty 2.', 'Bước 3: "Không tìm thấy dữ liệu" (trên giao diện hiện "Lỗi khi tải dữ liệu").']),
    T(8, 'Nút luôn hiện, không phụ thuộc quyền', 'P0', ACC_A, ['Đăng nhập A.', MENU], '—',
      ['Nút Xuất Excel, Cấu hình cột hiển thị, Cài đặt bộ lọc, liên kết Mã khách hàng đều hiện và dùng được.']),
    T(9, 'Mở thẳng đường dẫn màn', 'P1', ACC_A, ['Đăng nhập A.', 'Dán đường dẫn màn báo cáo vào thanh địa chỉ.'], '—',
      ['Mở được màn bình thường (màn không gắn quyền).']),
    T(10, 'Đổi công ty làm việc giữa lúc thao tác', 'P2', 'Tài khoản A đang mở màn.',
      ['Quản trị chuyển A sang công ty 2.', 'A bấm sang trang khác hoặc tải lại trang.'], '—', ['A chỉ còn thấy 2 dòng của công ty 2.']),
    T(11, 'Mục menu bị tắt', 'P2', 'Mục "Báo cáo hạn mức công nợ khách hàng" của phân hệ Tài chính bị tắt ở màn Cài đặt phân hệ.',
      ['Đăng nhập tài khoản thường.', 'Mở phân hệ Tài chính > Kế toán công nợ > Khách hàng.'], '—',
      ['Không thấy mục menu Báo cáo hạn mức công nợ khách hàng.']),
])

SECTIONS = [
    ('I', 'HIỂN THỊ DANH SÁCH VÀ TRUY CẬP', S1),
    ('II', 'TÌM KIẾM VÀ LỌC', S2),
    ('III', 'XEM CHI TIẾT', S3),
    ('IV', 'TÙY CHỈNH CỘT', S4),
    ('V', 'XUẤT EXCEL', S5),
    ('VI', 'ẢNH HƯỞNG CÁC MÀN HÌNH SỬ DỤNG DỮ LIỆU', S6),
    ('VII', 'PHÂN QUYỀN', S7),
]
check_no_dash_pre(SECTIONS, [])

if __name__ == '__main__':
    n = sum(len(s[2]) for s in SECTIONS)
    p0 = sum(1 for s in SECTIONS for c in s[2] if c[2] == 'P0')
    print('TC', n, 'P0', p0, '%.0f%%' % (100.0 * p0 / n))
    build(output_file=OUT, sheet_name='Trang tính1',
          feature_name='Báo cáo hạn mức công nợ khách hàng - Cập nhật ngày 03/11/2026',
          module_name='Báo cáo hạn mức công nợ khách hàng', description_block=DESCRIPTION_BLOCK, role_tcs=[], sections=SECTIONS)
