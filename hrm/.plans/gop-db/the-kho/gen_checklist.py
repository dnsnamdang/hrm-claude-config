# -*- coding: utf-8 -*-
"""Đối chiếu tài liệu màn "Thẻ kho" (phân hệ Kho › Báo cáo kho) với checklist của tester (06/11/2026).

Chạy: python gen_checklist.py  -> "Đối chiếu checklist.xlsx" (chạy sau gen_testcase.py và gen_srs.py).
Checklist chuẩn (chốt 03/11/2026): .claude/skills/testcase-documenter/assets/CHECKLIST_TC_SRS.xlsx (tab Testcase + tab SRS);
hàm ghi dùng chung checklist_doi_chieu.write() đọc bản JSON (324 case + 163 mục SRS) — _assert_checklist_moi() dừng nếu 2 bản lệch.
TC_MAP : dựng từ CK của gen_testcase.py + N/A + ghi chú lệch. SRS_MAP: stt checklist SRS -> mục trong SRS.
Màn BÁO CÁO CHỈ ĐỌC: không có Thêm mới, Chỉnh sửa, Xóa, Khóa / Mở khóa, Lịch sử thay đổi, Tùy chỉnh cột, Import Excel, Duyệt, Không duyệt.
"Xem chi tiết" của checklist = bung lô / vị trí + mở chứng từ nguồn (nhóm IV testcase, SRS 2.5).
SRS có 7 chức năng: 2.1 Xem thẻ kho · 2.2 Tìm kiếm và lọc · 2.3 Chọn hàng hóa · 2.4 Cài đặt bộ lọc · 2.5 Xem chi tiết chứng từ và
lô / vị trí · 2.6 In thẻ kho (UC) · 2.7 Xuất Excel (UC).
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
        assert len(a) == len(b) and not lech, '%s: checklist mới khác bản JSON, lệch ở stt %s' % (name, lech[:20])
        print('Checklist mới khớp bản JSON: %s %d dòng' % (name, len(a)))


RO = 'màn báo cáo chỉ đọc'
NA_CREATE = 'N/A: %s, không có chức năng Thêm mới (TC_07.001, TC_08.008 kiểm không có nút)' % RO
NA_EDIT = 'N/A: %s, không có chức năng Chỉnh sửa (số liệu đổi qua chứng từ nguồn — TC_07.004)' % RO
NA_DEL = 'N/A: %s, không có chức năng Xóa' % RO
NA_LOCK = 'N/A: %s, không có chức năng Khóa / Mở khóa (dòng thẻ kho không có trạng thái)' % RO
NA_HIS = 'N/A: %s, không có chức năng Lịch sử thay đổi (không ghi dữ liệu)' % RO
NA_COL = 'N/A: màn không có Tùy chỉnh cột (khuôn báo cáo bỏ Cấu hình cột, người dùng chốt 22/10/2026 — TC_01.005)'
NA_IMPORT = 'N/A: %s, không có chức năng Import Excel' % RO
NA_APPROVE = 'N/A: %s, không có Duyệt phiếu' % RO
NA_REJECT = 'N/A: %s, không có Không duyệt phiếu' % RO

NOTE = {
    5: 'màn không có cột ẩn / cấu hình cột',
    7: 'dòng thẻ kho không có trạng thái',
    17: 'lệch: chỉ về trang 1 khi đổi hàng hóa / số dòng; đổi ô lọc khác giữ trang (về trang cuối nếu vượt) — đúng theo code',
    20: 'bảng không sắp xếp theo cột — thứ tự cố định theo thời điểm ghi tồn', 21: 'bảng không sắp xếp theo cột',
    22: 'không có cột ngày tạo / cập nhật; thứ tự theo ngày ghi tồn', 23: 'mọi cột đều không sắp xếp',
    24: 'thứ tự cố định theo thời gian', 25: 'không đổi sắp xếp được — kiểm thứ tự liên tục giữa trang',
    29: 'lệch: so khớp có dấu (gõ không dấu không ra) — đúng theo code', 33: 'lệch: không giới hạn số ký tự — đúng theo code',
    45: 'lệch: rời màn thì xóa bộ lọc ghi tạm — đúng theo code', 48: 'lệch: bộ lọc ghi tạm theo trình duyệt, không theo tài khoản',
    186: 'chi tiết = bung lô / vị trí trong bảng + mở chứng từ nguồn ở tab mới (không phải popup)',
    187: 'tiêu đề là màn chứng từ nguồn', 194: 'N/A: dòng thẻ kho không có trạng thái Khóa',
    195: 'không có khu vực lịch sử (màn không ghi lịch sử)', 196: 'không có popup — thu dòng lô',
    218: 'Excel không có bước chọn trường (luôn đủ cột của kiểu Đầy đủ / Rút gọn)',
    213: 'popup chọn KIỂU xuất (Đầy đủ / Rút gọn), không chọn trường', 214: 'mặc định kiểu Đầy đủ',
    222: 'lệch: kỳ rỗng vẫn tải file (chỉ 5 dòng tổng hợp) — đúng theo code',
    293: 'không có Import; Xuất Excel theo quyền Thủ kho', 296: 'menu luôn hiện, mở thẳng màn khi thiếu quyền thì máy chủ từ chối',
}

TC_MAP = {}
for _stt, _ids in CK.items():
    TC_MAP[_stt] = ', '.join(sorted(set(_ids)))
for _stt in range(49, 103):
    TC_MAP.setdefault(_stt, NA_CREATE)
for _stt in range(103, 130):
    TC_MAP.setdefault(_stt, NA_EDIT)
for _stt in range(130, 142):
    TC_MAP.setdefault(_stt, NA_DEL)
for _stt in range(142, 162):
    TC_MAP.setdefault(_stt, NA_LOCK)
for _stt in range(162, 186):
    TC_MAP.setdefault(_stt, NA_HIS)
for _stt in range(198, 212):
    TC_MAP.setdefault(_stt, NA_COL)
for _stt in range(231, 268):
    TC_MAP.setdefault(_stt, NA_IMPORT)
for _stt in range(300, 313):
    TC_MAP.setdefault(_stt, NA_APPROVE)
for _stt in range(313, 325):
    TC_MAP.setdefault(_stt, NA_REJECT)
TC_MAP.setdefault(194, 'N/A: dòng thẻ kho không có trạng thái Khóa')
TC_MAP.setdefault(271, NA_LOCK)
TC_MAP.setdefault(273, NA_LOCK)
TC_MAP.setdefault(275, NA_IMPORT)
TC_MAP.setdefault(277, NA_LOCK)
for _stt, _note in NOTE.items():
    if _stt in TC_MAP and not TC_MAP[_stt].startswith('N/A') and '(' not in TC_MAP[_stt]:
        TC_MAP[_stt] += ' (%s)' % _note
_miss = [s for s in range(1, 325) if s not in TC_MAP]
assert not _miss, 'Thiếu dòng checklist Testcase: %s' % _miss

SRS_INTRO = '2.1.1; 2.2.1; 2.3.1; 2.4.1; 2.5.1; 2.6.2; 2.7.2'
SRS_MAP = {
    1: 'Phần 1', 2: 'Phần 1', 3: 'Phần 1', 4: 'Phần 1', 5: 'Phần 1', 6: 'Phần 1 (dòng thẻ kho không có trạng thái riêng)',
    7: 'Phần 1', 8: 'Phần 1',
    9: 'Phần 2', 10: 'Phần 2', 11: 'Phần 2', 12: 'Phần 2',
    13: 'Phần 2 (màn không có Thêm, Sửa, Xóa, Khóa / Mở khóa — ghi rõ dưới ma trận)',
    14: 'Phần 2 (không có Import, Lịch sử; In / Xuất Excel theo quyền Thủ kho)', 15: 'Phần 2', 16: 'Phần 2',
    17: 'Phần 3; 2.6.1; 2.7.1',
    18: SRS_INTRO, 19: SRS_INTRO, 20: SRS_INTRO, 21: SRS_INTRO, 22: '2.1.1; 2.2.1; 2.3.1; 2.4.1; 2.6.2; 2.7.2',
    23: SRS_INTRO + ' (đoạn "Quy tắc chung" có liên kết đầu mỗi mục Giới thiệu)',
    24: '2.1.2; 2.2.2; 2.3.2; 2.4.2; 2.5.2; 2.6.3; 2.7.3', 25: '2.1.2; 2.2.2; 2.3.2; 2.4.2; 2.5.2; 2.6.3; 2.7.3',
    26: '2.1.3; 2.2.3; 2.3.3; 2.4.3; 2.5.3; 2.6.4; 2.7.4', 27: '2.1.3; 2.2.3; 2.3.3; 2.4.3; 2.5.3; 2.6.4; 2.7.4',
    28: '2.1.3; 2.2.3; 2.3.3; 2.4.3; 2.5.3; 2.6.4; 2.7.4', 29: '2.1.4; 2.2.4; 2.3.4; 2.4.4; 2.5.4; 2.6.5; 2.7.5',
    30: '2.1.4; 2.2.4; 2.3.4; 2.4.4; 2.5.4; 2.6.5; 2.7.5',
    31: '2.1.1; 2.1.2', 32: '2.1.3; 2.1.5', 33: '2.1.1; 2.1.3 (không có cột ẩn / cấu hình cột)', 34: '2.1.3; Phần 2',
    35: '2.1.1; 2.1.5 (không sắp xếp theo cột — thứ tự theo thời điểm ghi tồn)', 36: '2.1.1; 2.1.3', 37: '2.1.3; 2.1.5',
    38: '2.1.1; 2.1.3', 39: '2.1.1; 2.1.4', 40: '2.1.4',
    41: '2.2.1; 2.2.3; 2.2.5', 42: '2.2.1', 43: '2.2.1; 2.2.3 (không giới hạn số ký tự — đúng theo code)', 44: '2.2.3; 2.2.5',
    45: '2.2.3', 46: '2.2.1', 47: '2.2.1; 2.2.4', 48: '2.2.3; 2.2.4', 49: '2.2.1; 2.2.3', 50: '2.1.3; 2.2.1', 51: '2.2.4',
    83: 'Phần 1 (Thuật ngữ — dòng thẻ kho không có trạng thái Khóa / Hoạt động)',
    120: '2.7.1; 2.7.2; 2.7.3', 121: '2.7.4', 122: '2.7.4 (popup chọn kiểu xuất, mặc định Đầy đủ)',
    123: 'N/A: Excel không có bước chọn trường nên không có Chọn tất cả / Bỏ chọn hết (bản In có "Chọn tất cả" — 2.6.4)',
    124: '2.7.4; 2.7.5', 125: '2.7.2', 126: '2.7.2 (kỳ rỗng vẫn tải file 5 dòng tổng hợp — đúng theo code)', 127: '2.7.2; 2.7.4',
    128: '2.7.2; 2.7.4', 129: '2.7.5',
    130: '2.5.1', 131: '2.5.2', 132: '2.5.3; 2.5.5', 133: '2.5.1; 2.5.3',
    134: 'N/A: dòng thẻ kho không có trạng thái Khóa',
    135: 'N/A: không có khối lịch sử (màn chỉ đọc, không ghi lịch sử — Phần 4 BR-13)',
    136: 'N/A: không có khối lịch sử nên không có bộ lọc lịch sử',
    137: '2.5.1; 2.5.4', 138: '2.5.4',
    147: 'Phần 4 — BR-13 (thẻ kho không có trường duy nhất; gom theo phiếu + loại — BR-04)', 148: 'Phần 4 — BR-06; BR-09',
    149: 'N/A: không có Khóa và không nhập dữ liệu nên không có trường hợp trùng với bản ghi đã khóa',
    150: 'Phần 4 — BR-02; BR-04', 151: 'Phần 4 — BR-13 (màn không có Xóa; dữ liệu đổi qua chứng từ nguồn)',
    152: 'N/A: màn không có chức năng Khóa / Mở khóa',
    153: 'Phần 4 — BR-01; BR-11; Phần 5', 154: 'Phần 4 — BR-13', 155: 'Phần 4 — BR-01 đến BR-14',
    156: 'Phần 5', 157: 'Phần 5', 158: 'Phần 5', 159: 'Phần 5', 160: 'Phần 5',
    161: 'N/A: màn không có chức năng Khóa / Mở khóa (Phần 5 theo khuôn Drive 4 cột STT | Nhóm | Màn hình | Đường dẫn)',
    162: 'Phần 5', 163: 'Phần 5 (Kho > Nhà > Dãy > Khoang > Vị trí; chứng từ > lô — Phần 1 Thuật ngữ)',
}
for _stt in range(52, 63):
    SRS_MAP[_stt] = 'N/A: %s, không có chức năng Thêm mới (ghi rõ ở Phần 1 Phạm vi chức năng)' % RO
for _stt in range(63, 74):
    SRS_MAP[_stt] = 'N/A: %s, không có chức năng Chỉnh sửa (ghi rõ ở Phần 1)' % RO
for _stt in range(74, 83):
    SRS_MAP[_stt] = 'N/A: %s, không có chức năng Xóa (ghi rõ ở Phần 1 và dưới ma trận Phần 2)' % RO
for _stt in range(84, 94):
    SRS_MAP[_stt] = 'N/A: %s, không có chức năng Khóa / Mở khóa (ghi rõ ở Phần 1)' % RO
for _stt in range(94, 102):
    SRS_MAP[_stt] = 'N/A: %s, không có chức năng Lịch sử thay đổi (Phần 1, Phần 4 — BR-13)' % RO
for _stt in range(102, 120):
    SRS_MAP[_stt] = 'N/A: %s, không có chức năng Import Excel (ghi rõ ở Phần 1)' % RO
for _stt in range(139, 147):
    SRS_MAP[_stt] = 'N/A: màn không có Tùy chỉnh cột (khuôn báo cáo bỏ Cấu hình cột 22/10/2026 — Phần 1, 2.1.1)'
_miss = [s for s in range(1, 164) if s not in SRS_MAP]
assert not _miss, 'Thiếu dòng checklist SRS: %s' % _miss

if __name__ == '__main__':
    _assert_checklist_moi()
    write(HERE, TC_MAP, SRS_MAP)
    tc_na = sum(1 for v in TC_MAP.values() if v.startswith('N/A'))
    srs_na = sum(1 for v in SRS_MAP.values() if v.startswith('N/A'))
    print('Testcase: %d có TC / %d N/A; SRS: %d có mục / %d N/A' % (len(TC_MAP) - tc_na, tc_na, len(SRS_MAP) - srs_na, srs_na))
