"""Sinh nhóm testcase XUẤT EXCEL / IMPORT cho tab testcase của 1 danh mục, từ config (configs/<slug>.py).

Dùng: from tc_gen import export_cases, import_cases
Mỗi case = (Chức năng, Priority, Tiền điều kiện, Bước, Test data, Expected).
Override theo danh mục ở CFG['tc']:
  export_theo_loc: False nếu file xuất KHÔNG theo bộ lọc (lỗi/thiết kế) — ghi đúng hiện trạng
  export_extra / import_extra: list case thêm
  import_rows_dung: mô tả file hợp lệ để Load (vd 'File mẫu điền 4 khu vực hợp lệ')
  import_loi_data: {thông báo lỗi: test data} — test data cho từng case lỗi
"""


def _file_xuat(cfg):
    for b in cfg['xuat']['buoc']:
        if 'tải về file' in b:
            return b.split('tải về file')[1].split()[0]
    return ''


def export_cases(cfg):
    x, t, ten = cfg['xuat'], cfg.get('tc', {}), cfg['doi_tuong']
    truong = x['truong'].replace('Chọn nhiều trường: ', '').rstrip('.')
    f = _file_xuat(cfg)
    rows = [
        ('Mở cửa sổ Chọn trường xuất file', 'P0', 'Đang ở màn danh sách, chưa chỉnh cấu hình cột.',
         '1. Bấm nút Xuất Excel\n2. Đọc danh sách trường trong cửa sổ',
         '', '- Mở cửa sổ “Chọn trường xuất file”\n- Có đủ các trường: %s\n- Tích sẵn đúng các cột đang hiển thị trên bảng\n- Dòng cuối ghi “Đang chọn a/b trường”' % truong),
        ('Xuất file với các trường mặc định', 'P0', 'Đang mở cửa sổ Chọn trường xuất file.',
         '1. Giữ nguyên các trường đã tích\n2. Bấm Xuất file\n3. Mở file vừa tải',
         '', '- Tải về file %s, báo “Xuất Excel thành công”\n- File có đúng các cột đã tích, dữ liệu khớp với bảng trên màn hình' % f),
    ]
    if t.get('export_theo_loc', True):
        rows.append(('File xuất chạy theo bộ lọc đang áp dụng', 'P0', 'Đang lọc danh sách còn vài %s.' % ten,
                     '1. Áp dụng bộ lọc\n2. Bấm Xuất Excel → Xuất file\n3. Đếm số dòng trong file',
                     '', '- File chỉ chứa các %s khớp bộ lọc\n- Số dòng bằng tổng số bản ghi ở cuối bảng' % ten))
    rows += [
        ('Xuất toàn bộ kết quả, không chỉ trang đang xem', 'P1', 'Kết quả có nhiều hơn 1 trang (10 dòng/trang).',
         '1. Đứng ở trang 1\n2. Bấm Xuất Excel → Xuất file',
         '', '- File chứa TOÀN BỘ kết quả (tối đa 10,000 dòng), không chỉ 10 dòng của trang 1'),
        ('Bỏ tích một trường', 'P1', 'Đang mở cửa sổ Chọn trường xuất file.',
         '1. Bỏ tích một trường bất kỳ\n2. Bấm Xuất file',
         '', '- File KHÔNG có cột vừa bỏ tích, các cột còn lại giữ nguyên'),
        ('Đổi thứ tự cột bằng kéo biểu tượng ba gạch', 'P2', 'Đang mở cửa sổ Chọn trường xuất file.',
         '1. Kéo biểu tượng ba gạch của trường cuối lên đầu danh sách\n2. Bấm Xuất file',
         '', '- Trong file, cột đó đứng đầu, đúng thứ tự vừa kéo'),
        ('Chọn tất cả / Bỏ chọn hết', 'P2', 'Đang mở cửa sổ Chọn trường xuất file.',
         '1. Bấm Bỏ chọn hết\n2. Quan sát nút Xuất file\n3. Bấm Chọn tất cả',
         '', '- Bỏ chọn hết: không trường nào được tích, nút Xuất file không bấm được\n- Chọn tất cả: tích đủ mọi trường'),
        ('Trường đang ẩn trên bảng thì không tích sẵn', 'P2', 'Đã ẩn 1 cột bằng Cấu hình cột hiển thị.',
         '1. Bấm Xuất Excel\n2. Tìm trường tương ứng cột đã ẩn',
         '', '- Trường đó KHÔNG được tích sẵn; tích lại thì vẫn xuất được'),
        ('Bấm Đóng thì không xuất', 'P2', 'Đang mở cửa sổ Chọn trường xuất file.',
         '1. Bấm Đóng', '', '- Cửa sổ đóng, không tải file nào'),
    ]
    return rows + [tuple(r) for r in t.get('export_extra', [])]


def import_cases(cfg):
    im, t, ten = cfg['import'], cfg.get('tc', {}), cfg['doi_tuong']
    dung = t.get('import_rows_dung', 'File mẫu điền 3 %s hợp lệ' % ten)
    rows = [
        ('Mở cửa sổ Import', 'P0', 'Đang ở màn danh sách.',
         '1. Bấm nút Import Excel\n2. Quan sát cửa sổ',
         '', '- Mở cửa sổ “%s”\n- Có nút Chọn file Excel, Tải file mẫu, Load lên bảng, Validate, Import, Đóng, Làm mới\n- Ô Tổng / Hợp lệ / Lỗi hiện 0' % im['tieu_de']),
        ('Tải file mẫu', 'P0', 'Đang mở cửa sổ Import.',
         '1. Bấm Tải file mẫu\n2. Mở file vừa tải',
         '', '- Tải về %s\n- Có các cột: %s\n- Hàng 1 tiêu đề, hàng 2 mô tả in nghiêng, từ hàng 3 là dòng ví dụ' % (im['file'], im['cot_text'])),
        ('Chọn file không phải Excel', 'P1', 'Đang mở cửa sổ Import.',
         '1. Bấm Chọn file Excel\n2. Chọn file .pdf',
         'File: tai_lieu.pdf', '- Báo “Vui lòng chọn file .xlsx hoặc .xls”, không nạp dữ liệu'),
        ('Load file đúng mẫu lên bảng', 'P0', dung + '.',
         '1. Bấm Chọn file Excel, chọn file\n2. Bấm Load lên bảng',
         '', '- Dữ liệu hiện lên bảng xem trước, đúng số dòng trong file\n- Ô Tổng bằng số dòng, chưa có dòng nào bị khoá'),
        ('Validate file hợp lệ', 'P0', 'Đã Load file hợp lệ.',
         '1. Bấm Validate',
         '', '- Báo “%s”\n' % t.get('import_ok_msg', 'Validate xong: N hợp lệ, 0 không hợp lệ') + '- Dòng hợp lệ bị khoá, không sửa được\n- Validate CHƯA ghi dữ liệu vào danh mục'),
    ]
    data = t.get('import_loi_data', {})
    for msg, why in im['loi']:
        rows.append(('Validate báo lỗi: ' + msg, 'P1', 'Đã Load file có dòng lỗi như Test data.',
                     '1. Bấm Validate\n2. Đọc thông báo dưới dòng lỗi',
                     data.get(msg, ''), '- Dòng lỗi tô nền đỏ, báo “%s” (%s)\n- Ô Lỗi tăng tương ứng' % (msg, why.rstrip('.').lower()[:1] + why.rstrip('.')[1:])))
    rows += [
        ('Còn dòng lỗi thì không Import được', 'P0', 'Đã Validate, còn ít nhất 1 dòng lỗi.',
         '1. Quan sát nút Import', '', '- Nút Import không bấm được'),
        ('Sửa dòng lỗi rồi Validate lại', 'P1', 'Đã Validate, còn dòng lỗi.',
         '1. Sửa trực tiếp giá trị sai trên bảng\n2. Bấm Validate',
         '', '- Dòng vừa sửa hết lỗi và bị khoá như các dòng hợp lệ'),
        ('Bỏ dòng lỗi', 'P0', 'Đã Validate, có vài dòng lỗi.',
         '1. Bấm Bỏ dòng lỗi\n2. Bấm Validate',
         '', '- Các dòng lỗi bị loại khỏi bảng\n- Validate lại: toàn bộ dòng còn lại hợp lệ, nút Import bấm được'),
        ('Xoá trạng thái validate', 'P2', 'Đã Validate.',
         '1. Bấm Xoá trạng thái validate',
         '', '- Dòng hợp lệ được mở khoá để sửa, thông báo lỗi biến mất'),
        ('Import thành công', 'P0', 'Đã Validate, tất cả dòng hợp lệ.',
         '1. Bấm Import\n2. Xem danh sách',
         '', '- Báo “%s”\n- Cửa sổ đóng, danh sách nạp lại có %s mới%s' % (im['toast'], ten, '' if t.get('khong_trang_thai') else ' ở trạng thái Hoạt động')),
        ('Người tạo của bản ghi import', 'P1', 'Vừa import thành công.',
         '1. Đọc cột Người tạo / Ngày tạo của bản ghi mới\n2. Mở Lịch sử của bản ghi đó',
         '', '- Người tạo là tài khoản thực hiện import, Ngày tạo là thời điểm import\n- Lịch sử có mốc Tạo mới'),
        ('File vượt quá 500 dòng', 'P2', 'File có 501 dòng dữ liệu.',
         '1. Chọn file\n2. Bấm Load lên bảng',
         '', '- Báo “File có 501 dòng dữ liệu, vượt quá giới hạn 500 dòng mỗi lần import. Vui lòng tách file và import nhiều lần.”'),
        ('Làm mới cửa sổ Import', 'P2', 'Đã Load dữ liệu.',
         '1. Bấm Làm mới', '', '- Bảng xem trước và file đã chọn bị xoá, ô Tổng / Hợp lệ / Lỗi về 0'),
    ]
    return rows + [tuple(r) for r in t.get('import_extra', [])]


def tsv_cell(v):
    v = '' if v is None else str(v)
    if any(c in v for c in '\n\t"'):
        return '"' + v.replace('"', '""') + '"'
    return v


def group_rows(module, grp_no, grp_title, grp_idx, cases):
    """Trả list dòng (list 9 ô A..I): dòng tiêu đề nhóm + các case. TC ID = TC_<grp_idx>.<nnn>."""
    out = [['', '', '%s. %s' % (grp_no, grp_title)] + [''] * 6]
    for i, c in enumerate(cases, 1):
        name, pr, pre, steps, data, exp = c
        out.append([module if i == 1 else '', grp_title if i == 1 else '', 'TC_%02d.%03d' % (grp_idx, i),
                    name, pr, pre, steps, data, exp])
    return out


def to_tsv(rows):
    return '\n'.join('\t'.join(tsv_cell(v) for v in r) for r in rows)
