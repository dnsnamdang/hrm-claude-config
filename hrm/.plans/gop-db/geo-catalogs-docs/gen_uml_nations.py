# -*- coding: utf-8 -*-
"""Sinh RIENG bo anh Use Case man 'Danh muc quoc gia' theo note cua BA.

Dot 1 (24/08/2026):
  1. Bo chu "He thong HRM -"; them Import file va Xuat Excel; bo text
     "«extend» An ban ghi da Khoa" o so do tong quan.
  2..5. FR-03 / FR-04 / FR-05 / FR-06: bo include va extend o so do rieng.
  6. Them so do cho Import file va Xuat Excel.

Dot 2 (24/08/2026):
  7. Ten so do: "Use Case Diagram – Quan ly danh muc quoc gia".
  8. So do tong quan PHAI the hien quan he giua cac use case
     (vd: Tim kiem va loc, Tuy chinh cot  --«extend»-->  Xem danh sach).
     KHONG ve «include» cho kiem tra trung / hop xac nhan — do la hanh vi ngam cua he thong.
  9. "Lich su thay doi" -> "Xem lich su thay doi".
  10. Thieu UC Xem chi tiet -> them FR-10 Xem chi tiet quoc gia.
  11. Ten use case LUON la CUM DONG TU (the hien hanh dong).

Chi sinh ANH, KHONG dung toi file SRS .docx.
Chay:  python .plans/gop-db/geo-catalogs-docs/gen_uml_nations.py
"""
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", ".claude", "skills",
                                "srs-documenter", "assets"))
import srs_uml_render as uml  # noqa: E402

OUT = os.path.join(HERE, "uml_nations")
os.makedirs(OUT, exist_ok=True)

ACTOR = 'Người dùng đã đăng nhập'
TITLE = 'Use Case Diagram – Quản lý danh mục quốc gia'


def png(name):
    return os.path.join(OUT, name + '.png')


# ---------------------------------------------------------------- tong quan
# Moi nhan deu la CUM DONG TU. Cot 'main' = actor noi thang vao;
# cot 'side' = use case duoc include / use case mo rong.
NODES = [
    ('fr01', 'FR-01  Xem danh sách quốc gia',          'view',   'main'),
    ('fr03', 'FR-03  Thêm mới quốc gia',               'crud',   'main'),
    ('fr04', 'FR-04  Chỉnh sửa quốc gia',              'crud',   'main'),
    ('fr05', 'FR-05  Xóa quốc gia',                    'action', 'main'),
    ('fr06', 'FR-06  Khóa / Mở khóa quốc gia',         'action', 'main'),
    ('fr08', 'FR-08  Import file danh sách quốc gia',  'io',     'main'),
    ('fr09', 'FR-09  Xuất danh sách quốc gia ra Excel', 'io',    'main'),

    ('fr02', 'FR-02  Tìm kiếm và lọc quốc gia',        'view',   'side'),
    ('fr10', 'FR-10  Xem chi tiết quốc gia',           'view',   'side'),
    ('fr11', 'FR-11  Tùy chỉnh cột hiển thị',          'view',   'side'),
    ('fr07', 'FR-07  Xem lịch sử thay đổi',            'view',   'side'),
]

# (nguon, dich, kieu) — nguon la dau mui ten di RA.
#   extend : use case mo rong --> use case me
# CHI VE «extend». Da BO «include» (user chot 24/08/2026): kiem tra trung ten/ma va
# hop xac nhan la HANH VI NGAM cua he thong, khong phai use case -> khong dua vao so do.
RELS = [
    ('fr02', 'fr01', 'extend'),
    ('fr10', 'fr01', 'extend'),
    ('fr11', 'fr01', 'extend'),
    ('fr07', 'fr01', 'extend'),
]

uml.draw_overview_rel(png('nations_overview'), TITLE, ACTOR, NODES, RELS)

# ------------------------------------------------- so do tung chuc nang
# Note dot 1 (2..5): so do rieng KHONG ve include/extend.
UC_FIGS = [
    ('FR-03', 'Thêm mới quốc gia',                'crud'),
    ('FR-04', 'Chỉnh sửa quốc gia',               'crud'),
    ('FR-05', 'Xóa quốc gia',                     'action'),
    ('FR-06', 'Khóa / Mở khóa quốc gia',          'action'),
    ('FR-08', 'Import file danh sách quốc gia',   'io'),
    ('FR-09', 'Xuất danh sách quốc gia ra Excel', 'io'),
    ('FR-10', 'Xem chi tiết quốc gia',            'view'),
]

for code, name, group in UC_FIGS:
    uml.draw_usecase(png('nations_uc_%s' % code.lower().replace('-', '')),
                     ACTOR, code, name, group, relations=())

for f in sorted(os.listdir(OUT)):
    print(f)
