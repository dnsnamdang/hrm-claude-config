# -*- coding: utf-8 -*-
"""Đối chiếu tài liệu màn "Theo dõi theo kho" với checklist "Mẫu tài liệu.xlsx" của tester (10/11/2026).

Chạy: python gen_checklist.py  -> "Đối chiếu checklist.xlsx" (chạy sau gen_testcase.py và gen_srs.py).
TC_MAP : stt checklist Testcase (1..324) -> TC ID (lấy từ tham số ck của gen_testcase.py), hoặc 'N/A: <lý do>'.
SRS_MAP: stt checklist SRS (1..163)      -> mục trong SRS (2.x / 2.x.y / Phần n), hoặc 'N/A: <lý do>'.
Màn THEO DÕI CHỈ ĐỌC 2 trang: không có Thêm mới, Chỉnh sửa, Xóa, Khóa/Mở khóa, Lịch sử thay đổi, Import Excel, Duyệt, Không duyệt, In.
"Xem chi tiết" của checklist = trang hoạt động nhập/xuất của 1 kho (mở ở tab mới từ Mã / Tên kho) + mở màn chi tiết phiếu đề nghị
(SRS 2.3, 2.5; testcase nhóm IV). Phân trang kiểm ở trang 1 (trang 2 không phân trang).
Mục SRS: 2.1 Xem danh sách kho (2.1.1 Giới thiệu · 2.1.2 Layout · 2.1.3 Giao diện · 2.1.4 Event · 2.1.5 Cách lấy dữ liệu · 2.1.6 vị trí
bấm được); 2.2 Tìm kiếm và lọc (2.2.1–2.2.4); 2.3 Xem hoạt động của kho (2.3.1–2.3.6); 2.4 Tìm theo mã phiếu; 2.5 Mở phiếu đề nghị;
2.6 Tùy chỉnh cột (2.6.1–2.6.4); 2.7 Xuất Excel danh sách kho (2.7.1 Use Case · 2.7.2–2.7.5); 2.8 Xuất Excel hoạt động kho (như 2.7).
Khuôn: ../hoat-dong-kho/gen_checklist.py.
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

RO = 'N/A: màn theo dõi chỉ đọc, không có chức năng %s'
NA_CREATE = RO % 'Thêm mới'
NA_EDIT = RO % 'Chỉnh sửa'
NA_DEL = RO % 'Xóa'
NA_LOCK = RO % 'Khóa / Mở khóa (khóa kho làm ở danh mục Kho vật lý)'
NA_HIS = RO % 'Lịch sử thay đổi'
NA_IMPORT = RO % 'Import Excel'
NA_APPROVE = RO % 'Duyệt phiếu (duyệt làm ở màn Phiếu đề nghị / Phiếu xuất, nhập kho)'
NA_REJECT = RO % 'Không duyệt phiếu'

NOTE_TC = {
    17: '(trang 1)', 10: '(trang 1; trang 2 không phân trang — TC_04.002)',
    22: '(màn không có cột ngày tạo / cập nhật: kiểm sắp xếp Tên; thứ tự mặc định theo ngày tạo kho — TC_01.018)',
    29: '(mã / tên kho có dấu)', 31: '(% và _ hiểu theo nghĩa đen)', 33: '(ô tìm không giới hạn ký tự)',
    47: '(ghi tạm trên trình duyệt, chung các tab)', 48: '(ghi tạm theo trình duyệt, không theo tài khoản)',
    186: '(chi tiết = trang hoạt động của kho / màn phiếu, mở ở tab mới)',
    214: '(trang 1 tích theo cột đang hiện; lệch: trang 2 luôn tích đủ 10 trường — đúng theo code)',
    222: '(trang 1 rỗng không tạo file; lệch: trang 2 rỗng vẫn tạo file — đúng theo code)',
}

TC_MAP = {}
for i in range(1, 325):
    ids = sorted(set(gen_testcase.CK.get(i, [])))
    if ids:
        TC_MAP[i] = ', '.join(ids) + ((' ' + NOTE_TC[i]) if NOTE_TC.get(i) else '')
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
for i in range(231, 268):
    TC_MAP.setdefault(i, NA_IMPORT)
for i in range(300, 313):
    TC_MAP.setdefault(i, NA_APPROVE)
for i in range(313, 325):
    TC_MAP.setdefault(i, NA_REJECT)
TC_MAP.setdefault(194, 'TC_01.007 (kho đang Khóa vẫn mở được trang hoạt động)')
TC_MAP.setdefault(195, 'N/A: màn không có khu vực lịch sử (lịch sử kho / phiếu xem ở màn nguồn)')
TC_MAP.setdefault(268, 'N/A: màn theo dõi không tạo bản ghi cấp cha / con')
TC_MAP.setdefault(269, 'N/A: màn theo dõi không tạo bản ghi cấp cha / con')
TC_MAP.setdefault(270, 'N/A: màn không có chức năng Xóa (xóa kho ở Kho vật lý → TC_07.004)')
TC_MAP.setdefault(271, NA_LOCK)
TC_MAP.setdefault(275, NA_IMPORT)
TC_MAP.setdefault(276, 'N/A: màn không có ô chọn kho để chọn mới (kho Khóa vẫn liệt kê — TC_07.003)')
TC_MAP.setdefault(277, 'N/A: màn không có ô chọn kho (kho Khóa / mở khóa đều liệt kê)')
TC_MAP.setdefault(297, 'N/A: testcase theo góc nhìn người dùng (không viết case gọi thẳng hệ thống); máy chủ chặn bằng quyền Quản lý kho '
                       '— kiểm qua mở thẳng địa chỉ TC_08.005, TC_08.006 và gỡ quyền TC_08.011')

SRS_MAP = {
    1: 'Phần 1', 2: 'Phần 1', 3: 'Phần 1', 4: 'Phần 1', 5: 'Phần 1 (Thuật ngữ)',
    6: 'Phần 1 (Thuật ngữ: Trạng thái trên bảng, Trạng thái phiếu)', 7: 'Phần 1 (Thời gian nhận / lấy-xếp hàng / hoàn thành, Tổng thời gian xử lý)',
    8: 'Phần 1 (Cấu trúc phân cấp: không có, 2 bảng phẳng)',
    9: 'Phần 2 (Quản lý kho; Xem danh mục kho của tất cả công ty)', 10: 'Phần 2', 11: 'Phần 2 (P1 / P2)', 12: 'Phần 2 (ma trận 8 FR)',
    13: 'Phần 2 (chỉ có xem; không có thêm / sửa / xóa / khóa)', 14: 'Phần 2 (Xuất Excel theo phạm vi; không có import / lịch sử)',
    15: 'Phần 2', 16: 'Phần 2',
    17: '2.7.1; 2.8.1 (chức năng chỉ đọc bỏ biểu đồ Use Case theo skill)',
    18: '2.1.1; 2.2.1; 2.3.1; 2.4.1; 2.5.1; 2.6.1; 2.7.2; 2.8.2', 19: '2.1.1; 2.3.1; 2.7.2', 20: '2.1.1; 2.3.1; 2.7.2',
    21: '2.1.1; 2.2.1; 2.3.1; 2.7.2', 22: '2.1.1; 2.3.1; 2.6.1; 2.7.2', 23: '2.1.1',
    24: '2.1.2; 2.3.2', 25: '2.1.2; 2.2.2; 2.3.2; 2.4.2; 2.5.2; 2.6.2; 2.7.3; 2.8.3', 26: '2.1.3; 2.3.3', 27: '2.2.3; 2.4.3; 2.6.3; 2.7.4',
    28: '2.1.3; 2.3.3', 29: '2.1.4; 2.3.4', 30: '2.1.4; 2.7.5; 2.8.5',
    31: '2.1.1; 2.1.2', 32: '2.1.3; 2.1.5', 33: '2.1.1 (Yêu cầu đặc biệt: đủ 5 cột, 2 cột khóa)', 34: '2.1.3; Phần 2',
    35: '2.1.1; 2.1.5; Phần 4 BR-08', 36: '2.1.1; 2.1.3 (trang 1 phân trang; trang 2 không — 2.3.1)', 37: '2.1.3; 2.1.5',
    38: '2.1.1; 2.1.3', 39: '2.1.1', 40: '2.1.4',
    41: '2.2.1; 2.4.1', 42: '2.2.1 (Yêu cầu đặc biệt)', 43: '2.2.3', 44: '2.2.3 (ô Nhóm, ô Công ty)', 45: '2.2.3',
    46: '2.2.1 (điều kiện VÀ)', 47: '2.2.1; 2.2.4 (ô chọn áp ngay, ô tìm áp khi Tìm kiếm)', 48: '2.2.3', 49: '2.2.1', 50: '2.2.3',
    51: '2.2.4; 2.4.4',
    120: '2.7.2; 2.8.2', 121: '2.7.4; 2.8.4', 122: '2.7.4 (theo cột đang hiện); 2.8.4 (luôn đủ 10 trường)', 123: '2.7.4; 2.8.4',
    124: '2.7.4; 2.7.5', 125: '2.7.2 (mọi trang theo bộ lọc); 2.8.2',
    126: '2.7.2 (rỗng: “Không có dữ liệu để xuất”); 2.8.2 (lệch: rỗng vẫn tạo file — đúng theo code)', 127: '2.7.4; 2.8.4',
    128: '2.7.5; 2.8.5', 129: '2.7.5; 2.8.5',
    130: '2.3.1; 2.5.1', 131: '2.3.2; 2.5.2', 132: '2.3.3; 2.5.1', 133: '2.3.1 (trang chỉ đọc); 2.5.1',
    134: '2.3.1 (kho đang Khóa vẫn xem được); Phần 4 BR-03', 135: 'N/A: màn không có khối lịch sử (xem ở màn nguồn)',
    136: 'N/A: màn không có khối lịch sử', 137: '2.3.3 (nút Quay lại giữ bộ lọc); 2.5.1', 138: '2.3.4; 2.5.4',
    139: '2.6.1', 140: '2.6.3', 141: '2.6.3', 142: '2.6.3; 2.6.4', 143: '2.6.1; 2.6.4', 144: '2.6.1', 145: '2.6.1', 146: '2.6.4',
    147: 'Phần 4 (không có trường duy nhất: mã kho / mã phiếu sinh ở màn nguồn)', 148: 'Phần 4 BR-10', 149: NA_LOCK,
    150: 'Phần 4 BR-05 (không có cấp cha / con)', 151: NA_DEL, 152: NA_LOCK, 153: 'Phần 5', 154: 'Phần 4 BR-11', 155: 'Phần 4',
    156: 'Phần 5', 157: 'Phần 5', 158: 'Phần 5', 159: 'Phần 5', 160: 'Phần 5',
    161: 'N/A: màn không có chức năng Khóa / Mở khóa (Phần 5 theo khuôn Drive 4 cột STT | Nhóm | Màn hình | Đường dẫn)',
    162: 'N/A: màn theo dõi không lưu tham chiếu tới bản ghi nào nên không chặn xóa ở màn khác', 163: 'Phần 4; Phần 5',
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

if __name__ == '__main__':
    missing = [i for i in range(1, 325) if i not in TC_MAP]
    assert not missing, 'Thiếu TC_MAP: %s' % missing
    missing = [i for i in range(1, 164) if i not in SRS_MAP]
    assert not missing, 'Thiếu SRS_MAP: %s' % missing
    write(HERE, TC_MAP, SRS_MAP)
    na_tc = sum(1 for v in TC_MAP.values() if v.startswith('N/A'))
    na_srs = sum(1 for v in SRS_MAP.values() if v.startswith('N/A'))
    print('Testcase: %d có TC / %d N/A | SRS: %d có mục / %d N/A' % (324 - na_tc, na_tc, 163 - na_srs, na_srs))
