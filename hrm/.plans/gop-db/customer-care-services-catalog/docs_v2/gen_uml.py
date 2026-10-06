# -*- coding: utf-8 -*-
"""Sơ đồ Use Case màn Danh mục gói bảo dưỡng — cùng quy ước với bộ Quốc gia (gen_uml_nations.py):
tên use case là CỤM ĐỘNG TỪ, sơ đồ tổng quan chỉ vẽ «extend», sơ đồ riêng không vẽ include/extend."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', '..', '.claude', 'skills', 'srs-documenter', 'assets'))
import srs_uml_render as uml  # noqa: E402
from _mac_docx import MAC_FONTS  # noqa: E402
for k, v in MAC_FONTS.items():
    if os.path.exists(v):
        setattr(uml, k, v)

OUT = os.path.join(HERE, 'uml'); os.makedirs(OUT, exist_ok=True)
ACTOR = 'Người dùng đã đăng nhập'
TITLE = 'Use Case Diagram – Quản lý danh mục gói bảo dưỡng'
png = lambda n: os.path.join(OUT, n + '.png')

MAINS = [
    ('FR-01', 'Xem danh sách gói bảo dưỡng', 'view'),
    ('FR-03', 'Thêm mới gói bảo dưỡng', 'crud'),
    ('FR-04', 'Chỉnh sửa gói bảo dưỡng', 'crud'),
    ('FR-05', 'Xóa gói bảo dưỡng', 'action'),
    ('FR-06', 'Khóa / Mở khóa gói bảo dưỡng', 'action'),
    ('FR-08', 'Import file gói bảo dưỡng', 'io'),
    ('FR-09', 'Xuất danh sách ra Excel', 'io'),
    ('FR-12', 'Nhân bản gói bảo dưỡng', 'crud'),
    ('FR-13', 'In phiếu kiểm tra bảo dưỡng', 'io'),
]
SUBS = [
    ('FR-02', 'Tìm kiếm và lọc gói bảo dưỡng', 'view', 'extend', [0], None),
    ('FR-10', 'Xem chi tiết gói bảo dưỡng', 'view', 'extend', [0], None),
    ('FR-11', 'Tùy chỉnh cột hiển thị', 'view', 'extend', [0], None),
    ('FR-07', 'Xem lịch sử thay đổi', 'view', 'extend', [0], None),
]
uml.draw_overview2(png('overview'), [(ACTOR, list(range(len(MAINS))))], MAINS, SUBS)
for code, name, group in MAINS[1:] + [('FR-10', 'Xem chi tiết gói bảo dưỡng', 'view')]:
    uml.draw_usecase(png('uc_' + code.lower().replace('-', '')), ACTOR, code, name, group, relations=())
print(sorted(os.listdir(OUT)))
