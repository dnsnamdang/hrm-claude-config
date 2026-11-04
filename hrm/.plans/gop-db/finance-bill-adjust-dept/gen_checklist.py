# -*- coding: utf-8 -*-
"""Đối chiếu tài liệu màn "Phiếu kế toán" với checklist của tester (04/11/2026).

Chạy: python gen_checklist.py  -> "Đối chiếu checklist.xlsx" (chạy sau gen_testcase.py và gen_srs.py).
Checklist chuẩn (chốt 03/11/2026): .claude/skills/testcase-documenter/assets/CHECKLIST_TC_SRS.xlsx (tab Testcase + tab SRS).
Hàm ghi dùng chung checklist_doi_chieu.write() đọc bản JSON cũ (checklist_mau_tai_lieu.json, 324 case + 163 mục SRS);
_assert_checklist_moi() bên dưới so từng dòng (Nhóm / Phân nhóm / Nội dung) của file xlsx mới với bản JSON đó và DỪNG nếu
lệch — nên bảng đối chiếu luôn phản ánh đúng checklist mới. (04/11/2026: 2 bản trùng khớp 324/324 + 163/163; file mới đánh
STT 299 cho cả 25 dòng Duyệt / Không duyệt phiếu — bảng đối chiếu giữ STT liên tục 300..324 như bản JSON.)
TC_MAP : dựng từ CK của gen_testcase.py (mỗi TC khai stt checklist nó phủ) + N/A + ghi chú lệch.
SRS_MAP: stt checklist SRS (1..163) -> mục trong SRS (2.x / 2.x.y / Phần n), hoặc 'N/A: <lý do>'.
Khuôn: ../buy-service-accounting/gen_checklist.py (cùng kiểu màn Lưu nháp / Lưu và duyệt ghi sổ), số mục SRS dời theo 14 chức năng của màn.
"""
import os
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..', 'phieu-theo-form-quoc-gia'))
from checklist_doi_chieu import write  # noqa: E402
from gen_testcase import CK  # noqa: E402

CHECKLIST_MOI = os.path.join(HERE, '..', '..', '..', '.claude', 'skills', 'testcase-documenter', 'assets', 'CHECKLIST_TC_SRS.xlsx')
CHECKLIST_JSON = os.path.join(HERE, '..', 'phieu-theo-form-quoc-gia', 'checklist_mau_tai_lieu.json')


def _doc_checklist_moi(path):
    """Đọc 2 tab của CHECKLIST_TC_SRS.xlsx thành [(nhóm, phân nhóm, nội dung)] — ô Nhóm / Phân nhóm gộp thì lấy giá trị trên."""
    import openpyxl
    wb = openpyxl.load_workbook(path, read_only=True)
    out = {}
    for name in ('Testcase', 'SRS'):
        rows, nhom, phan = [], None, None
        for r in wb[name].iter_rows(min_row=2, values_only=True):
            if len(r) < 4 or not str(r[3] or '').strip():
                continue
            nhom = r[1] or nhom
            phan = r[2] or phan
            rows.append((nhom, phan, r[3]))
        out[name] = rows
    return out


def _assert_checklist_moi():
    import io
    import json
    moi = _doc_checklist_moi(CHECKLIST_MOI)
    cu = json.load(io.open(CHECKLIST_JSON, encoding='utf-8'))
    for name in ('Testcase', 'SRS'):
        a = moi[name]
        b = [(it['nhom'], it['phan'], it['noi_dung']) for it in cu[name]]
        lech = [i + 1 for i, (x, y) in enumerate(zip(a, b)) if x != y]
        assert len(a) == len(b) and not lech, ('%s: checklist mới (%d dòng) khác bản JSON (%d dòng), lệch ở stt %s — cần dựng '
                                               'bảng đối chiếu riêng theo file mới' % (name, len(a), len(b), lech[:20]))
        print('Checklist mới khớp bản JSON: %s %d dòng' % (name, len(a)))

NA_LOCK = 'N/A: màn không có chức năng Khóa / Mở khóa (phiếu chỉ có 2 trạng thái Đang tạo, Đã duyệt)'
NA_IMPORT = 'N/A: màn không có chức năng Import Excel'
NA_REJECT = ('N/A: màn không có chức năng Không duyệt — phiếu chỉ có Lưu nháp / Lưu và duyệt; trả phiếu về làm ở màn phiếu nguồn '
             '(Phiếu yêu cầu điều chỉnh công nợ / hạch toán bổ sung có Từ chối)')

NOTE = {
    16: 'tổng số ở dòng "Hiển thị a–b / N" hiện số thô 15410 — chưa có dấu ngăn nghìn',
    29: 'so khớp có dấu / không dấu theo cách so sánh chữ của cơ sở dữ liệu — chưa xác minh trên dev',
    31: 'lệch: ký tự % và _ được hiểu là ký tự đại diện — đúng theo code',
    32: 'chưa xác minh bằng code việc bỏ khoảng trắng đầu / cuối của ô tìm nhanh',
    33: 'lệch: ô tìm nhanh không giới hạn số ký tự — đúng theo code',
    45: 'bộ lọc chỉ nhớ 10 phút khi đi vào màn chi tiết / sửa / tạo của chính màn',
    46: 'F5 đưa bộ lọc về trống — đúng theo code',
    48: 'lệch: bộ lọc nhớ theo trình duyệt, không theo tài khoản',
    54: 'màn Tạo là trang: nút Lưu nháp / Lưu và duyệt / Lưu và tiếp tục / Quay lại',
    64: 'Diễn giải không có độ dài tối thiểu',
    66: 'Diễn giải dòng tối đa 255 ký tự (máy chủ chặn); Diễn giải phiếu 65.535',
    67: 'phiếu không có trường nhập duy nhất, mã phiếu tự sinh',
    76: 'màn Tạo là trang, không phải popup — kiểm vẫn ở màn Tạo',
    83: 'màn là trang: sau Lưu nháp chuyển về danh sách',
    86: 'màn không có "Lưu và gửi duyệt": nút tương ứng là Lưu và duyệt (ghi sổ cái)',
    87: 'nút tương ứng: Lưu và duyệt', 88: 'nút tương ứng: Lưu và duyệt',
    89: 'nút tương ứng: Lưu và duyệt — không có ràng buộc trùng giữa các phiếu',
    90: 'màn là trang: sau Lưu và duyệt chuyển về danh sách',
    95: 'màn là trang, không có nút X — kiểm rời màn bằng menu',
    102: 'lưu nháp đồng thời 2 tab từ cùng phiếu YCĐC: máy chủ chưa chặn trùng — cần xác minh trên dev',
    103: 'màn Sửa là trang, không phải popup',
    116: 'phiếu không có trường duy nhất nên không thể trùng phiếu khác',
    126: 'màn không có trạng thái Khóa; trường hợp gần nhất: phiếu Đã duyệt không sửa được',
    127: 'câu lỗi "không tìm thấy bản ghi" là lỗi chung của máy chủ — chưa xác minh nguyên văn trên dev',
    138: 'câu lỗi "không tìm thấy bản ghi" là lỗi chung của máy chủ — chưa xác minh nguyên văn trên dev',
    186: 'màn chi tiết là trang, không phải popup',
    194: 'màn không có trạng thái Khóa; phiếu Đã duyệt (trạng thái cuối, chỉ xem)',
    196: 'màn chi tiết là trang: "đóng" là nút Quay lại',
    297: 'skill chốt 03/11 không viết case gọi thẳng API — kiểm việc máy chủ chặn qua thao tác trên giao diện của tài khoản đã bị gỡ quyền',
    222: 'lệch: danh sách rỗng không tải file, báo "Không có dữ liệu để xuất" — đúng theo code',
    278: 'phiếu không có trường Tên — kiểm sửa Diễn giải đồng bộ',
    279: 'mã phiếu tự sinh, không sửa được — kiểm liên kết với phiếu nguồn',
    300: 'màn không có nút "Duyệt" riêng: Lưu và duyệt chính là duyệt',
    308: 'thông báo chỉ gửi người lập phiếu nguồn (YCĐC, hạch toán bổ sung); phiếu nhập tay không gửi',
}

TC_MAP = {}
for _stt, _ids in CK.items():
    _ref = ', '.join(dict.fromkeys(_ids))
    TC_MAP[_stt] = _ref + (' (%s)' % NOTE[_stt] if _stt in NOTE else '')
TC_MAP[137] = 'N/A: màn không có trạng thái Khóa; phiếu Đã duyệt không xóa được (TC_05.007)'
for _stt in (179, 180, 271, 273, 276, 277):
    TC_MAP[_stt] = NA_LOCK
for _stt in (181, 275):
    TC_MAP[_stt] = NA_IMPORT
for _stt in range(142, 162):
    TC_MAP[_stt] = NA_LOCK
for _stt in range(231, 268):
    TC_MAP[_stt] = NA_IMPORT
for _stt in range(313, 325):
    TC_MAP[_stt] = NA_REJECT

SRS_INTRO = '2.1.1; 2.2.1; 2.5.2; 2.8.2; 2.11.2; 2.14.1'
SRS_MAP = {
    1: 'Phần 1', 2: 'Phần 1', 3: 'Phần 1', 4: 'Phần 1', 5: 'Phần 1', 6: 'Phần 1', 7: 'Phần 1', 8: 'Phần 1',
    9: 'Phần 2', 10: 'Phần 2', 11: 'Phần 2', 12: 'Phần 2',
    13: 'Phần 2 (màn không có Khóa / Mở khóa — ghi rõ dưới ma trận)',
    14: 'Phần 2 (không có Import; In, Xuất Excel, Lịch sử không gắn quyền riêng)',
    15: 'Phần 2', 16: 'Phần 2',
    17: 'Phần 3; 2.5.1; 2.6.1; 2.7.1; 2.8.1; 2.9.1; 2.10.1; 2.11.1; 2.12.1; 2.13.1',
    18: SRS_INTRO, 19: SRS_INTRO, 20: SRS_INTRO, 21: SRS_INTRO,
    22: '2.1.1; 2.2.1; 2.4.1; 2.5.2; 2.11.2; 2.13.2',
    23: '2.1.1; 2.2.1; 2.5.2; 2.14.1 (đoạn "Quy tắc chung" có liên kết đầu mỗi mục Giới thiệu)',
    24: '2.1.2; 2.5.3; 2.11.3', 25: '2.1.2; 2.5.3; 2.9.3; 2.10.3; 2.12.3; 2.14.2',
    26: '2.1.3; 2.5.4', 27: '2.1.3; 2.5.4', 28: '2.1.3; 2.5.4', 29: '2.1.4; 2.5.5', 30: '2.1.4; 2.5.5',
    31: '2.1.1; 2.1.2', 32: '2.1.3', 33: '2.1.1; 2.1.3; 2.4.1', 34: '2.1.3', 35: '2.1.3; 2.1.4', 36: '2.1.3', 37: '2.1.3',
    38: '2.1.1; 2.1.3', 39: '2.1.1', 40: '2.1.4',
    41: '2.2.1; 2.2.3', 42: '2.2.1', 43: '2.2.1; 2.2.3 (không giới hạn số ký tự — đúng theo code)', 44: '2.2.3', 45: '2.2.3',
    46: '2.2.1', 47: '2.2.1; 2.2.4', 48: '2.2.3; 2.2.4', 49: '2.2.1; 2.2.3', 50: '2.1.3; 2.2.1', 51: '2.2.4',
    52: '2.5.2; 2.1.3', 53: '2.5.4', 54: '2.5.4', 55: '2.5.2; Phần 4 — BR-03, BR-06', 56: '2.5.4; 2.5.5', 57: '2.5.5',
    58: '2.5.4; 2.5.5', 59: '2.5.2 (màn Tạo là trang: không có (x) / click ngoài — ghi rõ cách rời màn)', 60: '2.5.2; 2.5.5',
    61: '2.5.2; 2.5.5', 62: '2.5.5',
    63: '2.8.2; 2.1.3', 64: '2.8.2; 2.8.5', 65: '2.8.2; 2.8.4', 66: '2.8.4; 2.8.5', 67: '2.8.2; Phần 4 — BR-01',
    68: '2.8.2 (phiếu không có trường nhập duy nhất nên không trùng chính phiếu / phiếu khác)', 69: '2.8.2; 2.8.5', 70: '2.8.2; 2.8.5',
    71: '2.8.2 (không có Khóa; phiếu Đã duyệt coi như khóa sửa)', 72: '2.8.2; 2.14.1', 73: '2.8.5',
    74: '2.9.2; 2.9.4', 75: '2.9.2', 76: '2.9.2', 77: '2.9.2 (không có Khóa)', 78: '2.9.3; 2.9.4', 79: '2.9.4',
    80: '2.9.2; 2.9.4', 81: '2.9.2', 82: '2.9.5',
    83: 'Phần 1; Phần 4 — BR-04 (không có Khóa / Mở khóa; 2 trạng thái phiếu mô tả ở Thuật ngữ và BR-04)',
    94: '2.14.1; 2.14.2', 95: '2.14.3', 96: '2.14.3', 97: '2.14.1; 2.14.3', 98: '2.14.1; 2.14.3', 99: '2.14.1',
    100: '2.14.1', 101: '2.14.4',
    120: '2.13.2; 2.13.3', 121: '2.13.4', 122: '2.13.2; 2.13.4', 123: '2.13.4', 124: '2.13.4; 2.13.5', 125: '2.13.2',
    126: '2.13.2', 127: '2.13.2', 128: '2.13.2; 2.13.4', 129: '2.13.5',
    130: '2.10.2', 131: '2.10.3', 132: '2.10.4', 133: '2.10.2; 2.10.4',
    134: '2.10.2 (không có Khóa; phiếu Đã duyệt chỉ xem, chân màn chỉ In, Xuất Excel, Quay lại)',
    135: '2.10.4; 2.10.5', 136: '2.10.4; 2.14.3', 137: '2.10.2', 138: '2.10.5',
    139: '2.4.1; 2.4.2', 140: '2.4.3', 141: '2.4.1; 2.4.3', 142: '2.4.3; 2.4.4', 143: '2.4.1; 2.4.4', 144: '2.4.1',
    145: '2.4.1', 146: '2.4.4',
    147: 'Phần 4 — BR-01', 148: 'Phần 4 — BR-03, BR-06',
    149: 'N/A: không có Khóa và không có trường nhập duy nhất nên không có trường hợp trùng với bản ghi đã khóa',
    150: 'Phần 4 — BR-08', 151: 'Phần 4 — BR-04, BR-12; 2.9.2',
    152: 'N/A: màn không có chức năng Khóa / Mở khóa',
    153: 'Phần 4 — BR-11, BR-13; Phần 5', 154: 'Phần 4 — BR-14', 155: 'Phần 4 — BR-01 đến BR-15',
    156: 'Phần 5', 157: 'Phần 5', 158: 'Phần 5', 159: 'Phần 5', 160: 'Phần 5',
    161: 'N/A: màn không có chức năng Khóa / Mở khóa (Phần 5 theo khuôn Drive 4 cột STT | Nhóm | Màn hình | Đường dẫn)',
    162: 'Phần 5', 163: 'Phần 5 (quan hệ chứng từ nguồn – chứng từ dùng lại ghi trong cột Màn hình)',
}
for _stt in range(84, 94):
    SRS_MAP[_stt] = 'N/A: màn không có chức năng Khóa / Mở khóa (ghi rõ ở Phần 1 Phạm vi chức năng và dưới ma trận Phần 2)'
for _stt in range(102, 120):
    SRS_MAP[_stt] = 'N/A: màn không có chức năng Import Excel (ghi rõ ở Phần 1 Phạm vi chức năng)'

if __name__ == '__main__':
    _assert_checklist_moi()
    write(HERE, TC_MAP, SRS_MAP)
