# -*- coding: utf-8 -*-
"""Phần dùng chung cho 3 SRS cụm Bàn giao công việc (handover / handover-add / handover-receiving)."""
import os
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = HERE
while not os.path.isdir(os.path.join(ROOT, '.claude', 'skills', 'srs-documenter')):
    ROOT = os.path.dirname(ROOT)
sys.path.insert(0, os.path.join(ROOT, '.claude', 'skills', 'srs-documenter', 'assets'))
from srs_docx_lib import SrsDoc  # noqa: E402,F401

NO_LOGIN = ('– Chưa đăng nhập hoặc phiên đăng nhập hết hạn → hệ thống yêu cầu đăng nhập lại và dừng xử lý.')

STATUS_TEXT = ('5 trạng thái phiếu: Nháp (xám), Chờ duyệt (cam), Đã duyệt (xanh dương), Từ chối (đỏ), '
               'Hoàn tất (xanh lá). Chữ và màu do hệ thống trả về.')

REASONS = 'Nghỉ việc · Chuyển phòng ban · Nghỉ thai sản · Nghỉ dài hạn · Khác'

TERMS = [
    ('Phiếu bàn giao', 'Chứng từ ghi danh sách nhiệm vụ / vấn đề người lập phiếu đang phụ trách cần chuyển cho '
     'người khác, kèm người nhận từng mục. Mã tự sinh dạng BG.<năm>.<4 số> (vd BG.2026.0001).'),
    ('Người lập phiếu', 'Người đang đăng nhập khi tạo phiếu; đồng thời là nhân viên bàn giao của phiếu.'),
    ('Công việc bàn giao', 'Một dòng trong phiếu: 1 nhiệm vụ hoặc 1 vấn đề đang giao cho người lập phiếu.'),
    ('Người nhận BG', 'Người được chỉ định nhận một công việc trong phiếu bàn giao.'),
    ('Trưởng phòng (TP)', 'Người có quyền “Duyệt bàn giao công việc”, duyệt hoặc không duyệt phiếu.'),
    ('Tiếp nhận / Từ chối tiếp nhận', 'Thao tác của người nhận trên từng công việc sau khi phiếu đã duyệt.'),
    ('Hoàn tất', 'Trạng thái phiếu khi mọi công việc trong phiếu đã được tiếp nhận hoặc từ chối.'),
]


def new_doc(here, ten_man, menu, prefix, icons):
    shots = os.path.join(here, 'shots')
    out = os.path.join(here, 'SRS - %s.docx' % ten_man)
    d = SrsDoc(out=out, menu=menu, route='', full_url='', img_prefix=prefix)
    d.set_menu_icons({k: os.path.join(shots, v) for k, v in icons.items()})
    d.title_block(ten_man)
    d.h2('Mục lục')
    d.toc()
    return d, (lambda n: os.path.join(shots, n))


def extra_menu(d, menu, note=None):
    """Dòng Menu thứ 2 (lối vào khác) — có icon."""
    d._menu_para(menu)
    if note:
        d.p(note)
