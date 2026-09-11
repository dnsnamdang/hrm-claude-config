# -*- coding: utf-8 -*-
"""Lop tuong thich macOS cho 2 engine tai lieu (srs_docx_lib / hdsd_engine).

Ca 2 engine trong `.claude/skills/` deu viet cho may Windows cua team:
  - font ve so do UML tro toi C:\\Windows\\Fonts\\segoeui*.ttf
  - cap nhat MUC LUC bang PowerShell + COM Word

Tren macOS 2 thu do khong ton tai. File nay va cham vao 2 diem do (chi trong
tien trinh dang chay, KHONG sua file skill dung chung cua team):
  - doi font sang bo Arial cua macOS (du dau tieng Viet)
  - goi Microsoft Word qua AppleScript de cap nhat that su muc luc + danh muc hinh

Cach dung o dau moi generator:

    import os, sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from _mac_docx import patch_srs, patch_hdsd     # tuy tai lieu dang lam

Chay tren Windows thi 2 ham nay tu bo qua, khong anh huong gi.
"""
import os
import subprocess
import sys

MAC_FONTS = {
    'F_REG': '/System/Library/Fonts/Supplemental/Arial.ttf',
    'F_BOLD': '/System/Library/Fonts/Supplemental/Arial Bold.ttf',
    'F_ITAL': '/System/Library/Fonts/Supplemental/Arial Italic.ttf',
}

_APPLESCRIPT = '''
tell application "Microsoft Word"
    set d to open file name POSIX file "%s"
    repeat with f in (get fields of d)
        update field f
    end repeat
    repeat with t in (get tables of contents of d)
        update table of contents t
    end repeat
    repeat with g in (get tables of figures of d)
        update table of figures g
    end repeat
    repaginate d
    save d
    close d saving no
end tell
'''


def _is_mac():
    return sys.platform == 'darwin'


def update_fields_by_word_mac(path):
    """Cap nhat muc luc / danh muc hinh anh bang Word tren macOS.

    Loi thi CANH BAO chu khong lam gay generator — dung dung nhu ban Windows.
    """
    try:
        res = subprocess.run(['osascript', '-e', _APPLESCRIPT % path],
                             capture_output=True, text=True, timeout=300)
        if res.returncode != 0:
            print('!!! Muc luc CHUA duoc Word cap nhat:', (res.stderr or '').strip()[:200])
            return False
    except Exception as exc:  # noqa: BLE001
        print('!!! Muc luc CHUA duoc Word cap nhat:', exc)
        return False
    return True


def patch_srs():
    """Va cham vao srs_docx_lib + srs_uml_render cho chay duoc tren macOS."""
    if not _is_mac():
        return
    import srs_uml_render
    import srs_docx_lib

    for name, path in MAC_FONTS.items():
        if os.path.exists(path):
            setattr(srs_uml_render, name, path)

    def _update(self):
        ok = update_fields_by_word_mac(self.out)
        self._word_pages = 'Pages=?(macOS)' if ok else ''

    srs_docx_lib.SrsDoc._update_fields_by_word = _update


def patch_hdsd():
    """Va cham vao hdsd_engine cho chay duoc tren macOS."""
    if not _is_mac():
        return
    import hdsd_engine

    def _update(self):
        ok = update_fields_by_word_mac(self.output)
        print('Cap nhat field bang Word:', 'OK' if ok else 'THAT BAI')

    hdsd_engine.HdsdBuilder._update_fields_by_word = _update


def renumber_figure_index(path):
    """Danh so lai muc "DANH MUC HINH ANH".

    Word tren macOS dung TOF (`TOC \\c "Hinh"`) van ghi ra "Hinh 1" cho MOI dong,
    trong khi chu thich duoi anh o than bai da danh so dung 1..N. Ban Windows khong
    dinh loi nay (file mau HDSD_MAU.docx danh so dung), nen day la buoc va cham
    rieng cho macOS: doc lai file sau khi Word da cap nhat field roi ghi de so thu tu.

    Chi sua PHAN SO o dau moi dong, giu nguyen chu va so trang Word tinh ra.
    """
    import re
    from docx import Document
    from docx.oxml.ns import qn

    doc = Document(path)
    n = 0
    for par in doc.paragraphs:
        if 'figure' not in par.style.name.lower():
            continue
        nodes = list(par._p.iter(qn('w:t')))
        if not nodes:
            continue
        m = re.match(r'^(Hình)\s+\d+(.*)$', nodes[0].text or '', re.S)
        if not m:
            continue
        n += 1
        nodes[0].text = '%s %d%s' % (m.group(1), n, m.group(2))
    doc.save(path)
    print('Da danh so lai %d dong danh muc hinh anh' % n)
    return n
