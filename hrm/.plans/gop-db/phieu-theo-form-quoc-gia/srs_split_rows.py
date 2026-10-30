# -*- coding: utf-8 -*-
"""Tách dòng gộp trong bảng "Mô tả chi tiết giao diện" của SRS: mỗi đối tượng 1 hàng (user yêu cầu 30/10/2026).

Dòng gộp kiểu ('Cột Người tạo / Phòng ban / Người duyệt', ...) → 3 hàng 'Cột Người tạo', 'Cột Phòng ban', 'Cột Người duyệt'.
Phần sau chưa có tiền tố ('Phòng ban') tự nhận tiền tố của phần đầu ('Cột', 'Nút', 'Ô').

    rows = split_ui_rows(rows, over={...}, explicit={...}, keep={...})

over     : mô tả riêng cho hàng sau khi tách. Khoá là tên mới, hoặc (tên dòng gộp, tên mới) khi cùng tên mới xuất hiện ở
           nhiều dòng gộp với nghĩa khác nhau. Giá trị là chuỗi / list (thay cột Mô tả) hoặc dict
           {'desc':…, 'scope':…, 'init':…, 'type':…, 'state':…}.
explicit : {tên dòng gộp: [hàng đầy đủ, …]} — dòng gộp không tách được theo dấu '/' (vd "Các ô thông tin …").
keep     : tên KHÔNG tách vì là 1 đối tượng (nhãn có sẵn dấu '/': 'Khách hàng / Nhà cung cấp', 'Cột KH / NCC').
"""

KEEP_DEFAULT = {'Khách hàng / Nhà cung cấp', 'Cột KH / NCC', 'Tên / Mã khách hàng'}
PREFIXES = ('Cột ', 'Nút ', 'Ô ', 'Mục ')

# Mô tả mặc định cho nút chung khi dòng gộp chỉ ghi '–' (chép đúng hành vi các cửa sổ dùng chung).
BTN_DESC = {
    'Nút Tìm kiếm': 'Áp dụng điều kiện tìm kiếm, về trang 1.',
    'Nút Làm mới': 'Xóa điều kiện tìm kiếm / lọc, nạp lại từ trang 1.',
    'Nút Tìm kiếm nâng cao': 'Mở / đóng khối ô lọc nâng cao.',
    'Nút Cài đặt bộ lọc': 'Mở cửa sổ Cài đặt bộ lọc.',
    'Nút Lưu': 'Lưu cấu hình theo người dùng, đóng cửa sổ.',
    'Nút Khôi phục mặc định': 'Trả danh sách và thứ tự về cấu hình ban đầu.',
    'Nút Đóng': 'Đóng cửa sổ; thay đổi chưa lưu bị bỏ.',
    'Nút Chọn tất cả': 'Tích mọi mục (trừ mục bị khóa).',
    'Nút Bỏ chọn hết': 'Bỏ tích mọi mục (trừ mục bị khóa).',
    'Nút Xuất file': 'Tải file Excel gồm các trường đã tích, đúng thứ tự trong danh sách.',
    'Nút Hủy': 'Đóng hộp / cửa sổ, không thực hiện thao tác.',
    'Nút Bộ lọc': 'Lọc các mốc theo loại hành động, người thực hiện, từ ngày, đến ngày.',
    'Nút Quay lại': 'Về màn danh sách.',
}


def _parts(name):
    parts = [p.strip() for p in name.split(' / ')]
    pre = next((p for p in PREFIXES if parts[0].startswith(p)), '')
    return [parts[0]] + [(p if (not pre or p.startswith(PREFIXES)) else pre + p) for p in parts[1:]]


def _idx(row):
    """Vị trí cột theo số ô của hàng: 7 ô (8 cột) · 6 ô (7 cột, bỏ Bắt buộc) · 5 ô (6 cột, bỏ Bắt buộc + Phạm vi)."""
    n = len(row)
    if n == 7:
        return {'type': 1, 'state': 2, 'scope': 3, 'req': 4, 'init': 5, 'desc': 6}
    if n == 6:
        return {'type': 1, 'state': 2, 'scope': 3, 'init': 4, 'desc': 5}
    return {'type': 1, 'state': 2, 'init': 3, 'desc': 4}


def _apply(row, o):
    if o is None:
        return row
    row = list(row)
    idx = _idx(row)
    if isinstance(o, dict):
        for k, v in o.items():
            if k in idx:
                row[idx[k]] = v
    else:
        row[idx['desc']] = o
    return tuple(row)


def split_ui_rows(rows, over=None, explicit=None, keep=()):
    over, explicit = over or {}, explicit or {}
    keep = set(keep) | KEEP_DEFAULT
    out = []
    for r in rows:
        name = r[0]
        if name in explicit:
            out.extend(explicit[name])
            continue
        if ' / ' not in name or name in keep or name.startswith('Dòng “Hiển thị'):
            out.append(r)
            continue
        for p in _parts(name):
            row = (p,) + tuple(r[1:])
            idx = _idx(row)
            o = over.get((name, p), over.get(p))
            if o is None and p in BTN_DESC and str(row[idx['desc']]).strip() in ('–', '-', ''):
                o = BTN_DESC[p]
            out.append(_apply(row, o))
    bad = [x[0] for x in out if ' / ' in x[0] and x[0] not in keep and not x[0].startswith('Dòng “Hiển thị')]
    assert not bad, 'Còn dòng gộp chưa tách: %s' % bad
    return out
