# -*- coding: utf-8 -*-
"""Đối chiếu tài liệu màn "Báo cáo tồn kho tổng hợp theo mặt hàng" với checklist "Mẫu tài liệu.xlsx" của tester (07/11/2026).

Chạy: python gen_checklist.py  -> "Đối chiếu checklist.xlsx" (chạy sau gen_testcase.py và gen_srs.py).
TC_MAP : stt checklist Testcase (1..324) -> TC ID (lấy từ tham số ck của gen_testcase.py), hoặc 'N/A: <lý do>'.
SRS_MAP: stt checklist SRS (1..163)      -> mục trong SRS (2.x / 2.x.y / Phần n), hoặc 'N/A: <lý do>'.
Màn BÁO CÁO CHỈ ĐỌC: không có Thêm mới, Chỉnh sửa, Xóa, Khóa/Mở khóa, Lịch sử thay đổi, Import Excel, Duyệt, Không duyệt, Tùy chỉnh cột.
"Xem chi tiết" của checklist = nhóm cột Chi tiết theo công ty thuê kho + đổi ĐVT ngay trong bảng (SRS 2.5, testcase nhóm IV).
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
import gen_testcase  # noqa: E402

RO = 'N/A: màn báo cáo chỉ đọc, không có chức năng %s'
NA_CREATE = RO % 'Thêm mới'
NA_EDIT = RO % 'Chỉnh sửa'
NA_DEL = RO % 'Xóa'
NA_LOCK = RO % 'Khóa / Mở khóa (dòng báo cáo không có trạng thái)'
NA_HIS = RO % 'Lịch sử thay đổi'
NA_IMPORT = RO % 'Import Excel'
NA_COL = 'N/A: bảng cố định 7 cột + nhóm Chi tiết, không có Tùy chỉnh cột (chọn cột chỉ có ở bản in — TC_06.005)'
NA_APPROVE = RO % 'Duyệt phiếu'
NA_REJECT = RO % 'Không duyệt phiếu'

NOTE_TC = {
    20: '(lệch: không sắp xếp theo cột, luôn theo tên hàng — đúng theo code)',
    21: '(lệch: không sắp xếp theo cột)', 22: '(màn không có cột ngày tạo / cập nhật; không sắp xếp theo cột)',
    26: '(màn không có ô tìm nhanh — tìm theo mã hợp đồng ở ô Hợp đồng)',
    29: '(hệ thống phân biệt Đ và D)', 31: '(lệch: % và _ được hiểu là ký tự đại diện — đúng theo code)',
    33: '(lệch: ô Hợp đồng không giới hạn ký tự)', 48: '(bộ lọc ghi tạm không tách theo tài khoản)', 37: '(dev 07/11: TC_02.039 lỗi 403 ở cửa sổ Chọn hàng hóa khi khác công ty đăng nhập)',
    186: '(chi tiết = nhóm cột Chi tiết theo công ty thuê kho + ô ĐVT ngay trong bảng, không phải cửa sổ)',
    222: '(rỗng vẫn tạo file có dòng Không có dữ liệu — đúng theo code)', 218: '(Excel không có bước chọn trường; bản in bắt chọn ≥ 1 cột)',
}

TC_MAP = {}
for i in range(1, 325):
    ids = sorted(set(gen_testcase.CK.get(i, [])))
    if ids:
        TC_MAP[i] = ', '.join(ids) + ((' ' + NOTE_TC[i]) if i in NOTE_TC else '')
for i in range(49, 103):
    TC_MAP.setdefault(i, NA_CREATE)
for i in range(103, 130):
    TC_MAP.setdefault(i, NA_EDIT)
for i in range(130, 142):
    TC_MAP.setdefault(i, NA_DEL)
for i in range(142, 162):
    TC_MAP.setdefault(i, NA_LOCK)
for i in range(162, 186):
    TC_MAP.setdefault(i, NA_HIS)
for i in range(198, 212):
    TC_MAP.setdefault(i, NA_COL)
for i in range(231, 268):
    TC_MAP.setdefault(i, NA_IMPORT)
for i in range(300, 313):
    TC_MAP.setdefault(i, NA_APPROVE)
for i in range(313, 325):
    TC_MAP.setdefault(i, NA_REJECT)
TC_MAP.setdefault(297, 'TC_08.005, TC_08.006 (máy chủ tự kiểm quyền + phạm vi kho; testcase không viết case gọi thẳng chức năng theo chuẩn 03/11)')
TC_MAP.setdefault(25, 'N/A: màn không có sắp xếp theo cột (luôn theo tên hàng — TC_01.018)')
TC_MAP.setdefault(194, 'N/A: dòng báo cáo không có trạng thái Khóa')
TC_MAP.setdefault(195, 'N/A: chi tiết không có khu vực lịch sử (màn chỉ đọc, không ghi lịch sử)')
TC_MAP.setdefault(269, 'N/A: màn báo cáo không tạo bản ghi cấp cha / con')
TC_MAP.setdefault(271, NA_LOCK)
TC_MAP.setdefault(273, NA_LOCK)
TC_MAP.setdefault(275, NA_IMPORT)
TC_MAP.setdefault(277, NA_LOCK)

SRS_MAP = {
    1: 'Phần 1', 2: 'Phần 1', 3: 'Phần 1', 4: 'Phần 1', 5: 'Phần 1', 6: 'Phần 1 (dòng báo cáo không có trạng thái — thuật ngữ Trạng thái bản ghi)',
    7: 'Phần 1', 8: 'Phần 1',
    9: 'Phần 2', 10: 'Phần 2', 11: 'Phần 2', 12: 'Phần 2', 13: 'Phần 2 (chỉ có quyền xem; không có thêm / sửa / xóa / khóa)',
    14: 'Phần 2 (In, Xuất Excel theo cùng quyền xem; không có import / lịch sử)', 15: 'Phần 2', 16: 'Phần 2',
    17: '2.6.1; 2.7.1 (chức năng chỉ đọc bỏ biểu đồ Use Case theo skill)', 18: '2.1.1; 2.2.1; 2.5.1', 19: '2.1.1', 20: '2.1.1; 2.6.2',
    21: '2.1.1; 2.2.1', 22: '2.1.1; 2.6.2; 2.7.2', 23: '2.1.1', 24: '2.1.2', 25: '2.1.2; 2.2.2; 2.4.2; 2.6.3',
    26: '2.1.3', 27: '2.2.3', 28: '2.1.3; 2.5.3', 29: '2.1.4', 30: '2.1.4; 2.6.5',
    31: '2.1.1; 2.1.2', 32: '2.1.3', 33: '2.1.1 (bảng cố định 7 cột + nhóm Chi tiết, không có cột ẩn)', 34: '2.1.3; Phần 2',
    35: '2.1.1 (lệch: không sắp xếp theo cột, luôn theo tên hàng)', 36: '2.1.3', 37: '2.1.3; 2.1.5', 38: '2.1.1; 2.1.3', 39: '2.1.1; 2.1.4',
    40: '2.1.4',
    41: '2.2.1 (không có ô tìm nhanh; tìm theo mã hợp đồng)', 42: '2.2.1', 43: '2.2.3', 44: '2.2.3; 2.2.5', 45: '2.2.3', 46: '2.2.1',
    47: '2.2.4', 48: '2.2.3', 49: '2.2.1', 50: '2.1.5; 2.2.1', 51: '2.2.4',
    120: '2.7.2', 121: '2.7.4', 122: '2.7.4',
    123: '2.6.4 (lệch: Excel không chọn trường, chỉ chọn kiểu; Chọn tất cả cột ở cửa sổ In)', 124: '2.7.4; 2.7.5', 125: '2.7.2',
    126: '2.7.2', 127: '2.7.2', 128: '2.7.5', 129: '2.7.5',
    130: '2.5.1', 131: '2.5.2', 132: '2.5.3; 2.5.5', 133: '2.5.1', 134: NA_LOCK,
    135: 'N/A: chi tiết không có khối lịch sử (màn chỉ đọc)', 136: 'N/A: chi tiết không có khối lịch sử', 137: '2.5.1', 138: '2.5.4',
    147: 'Phần 4', 148: 'Phần 4', 149: NA_LOCK, 150: 'Phần 4', 151: NA_DEL, 152: NA_LOCK, 153: 'Phần 5', 154: 'Phần 4', 155: 'Phần 4',
    156: 'Phần 5', 157: 'Phần 5', 158: 'Phần 5', 159: 'Phần 5', 160: 'Phần 5',
    161: 'N/A: màn không có chức năng Khóa / Mở khóa (Phần 5 theo khuôn Drive 4 cột STT | Nhóm | Màn hình | Đường dẫn)',
    162: 'N/A: báo cáo không lưu tham chiếu tới bản ghi nào nên không chặn xóa ở màn khác', 163: 'Phần 4; Phần 5',
}
for i in range(52, 63):
    SRS_MAP[i] = NA_CREATE
for i in range(63, 74):
    SRS_MAP[i] = NA_EDIT
for i in range(74, 83):
    SRS_MAP[i] = NA_DEL
for i in range(83, 94):
    SRS_MAP[i] = NA_LOCK
for i in range(94, 102):
    SRS_MAP[i] = NA_HIS
for i in range(102, 120):
    SRS_MAP[i] = NA_IMPORT
for i in range(139, 147):
    SRS_MAP[i] = NA_COL

if __name__ == '__main__':
    missing = [i for i in range(1, 325) if i not in TC_MAP]
    assert not missing, 'Thiếu TC_MAP: %s' % missing
    write(HERE, TC_MAP, SRS_MAP)
    na_tc = sum(1 for v in TC_MAP.values() if v.startswith('N/A'))
    na_srs = sum(1 for v in SRS_MAP.values() if v.startswith('N/A'))
    print('Testcase: %d có TC / %d N/A | SRS: %d có mục / %d N/A' % (324 - na_tc, na_tc, 163 - na_srs, na_srs))
