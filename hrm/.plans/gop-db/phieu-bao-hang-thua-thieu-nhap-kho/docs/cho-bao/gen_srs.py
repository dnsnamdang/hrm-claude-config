# -*- coding: utf-8 -*-
"""SRS - Phiếu nhập kho chờ báo thừa, thiếu (STT 288) — khuôn PHIẾU đợt 3 (màn mẫu finance-declare-debt-beginning/docs/kh).

Màn là DANH SÁCH VIỆC CẦN LÀM (hàng chờ lập phiếu báo) — không có Thêm / Sửa / Xóa / Duyệt riêng; thao tác duy nhất
"Báo hàng thừa thiếu" mở trang Tạo phiếu báo của màn 289 (../phieu/).
Nguồn (code HRM develop, 18/11/2026):
  FE hrm-client/pages/warehouse/import-discrepancies/index.vue, pages/warehouse/exc-shortage-imports/components/constants.js,
     components/subsystem-menu/warehouse.js
  BE Modules/Finance: ExcShortageController@queue/queueFilterOptions/queueExportRows,
     Services/ExcShortage/ExcShortageService (queueQuery, applyQueueScope, applyQueueFilters, queueRows),
     Entities/ExcShortage/ExcShortageWarehouseImport (quyền); WarehouseImportService::listRows (cột Loại, Người đề nghị…)
Chạy:  python gen_srs.py [--no-word]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..', '..', '..', 'xuat-tai-lieu-chuyen-doi')))
import _lib_phieu as L  # noqa: E402
from _lib_phieu import ui, UI4, UI4W, UI6, UI6W, UI7, UI7W, UI8, UI8W, TRUOC_LUU  # noqa: E402,F401

TEN = 'Phiếu nhập kho chờ báo thừa, thiếu'
OUT = os.path.join(HERE, 'SRS - %s.docx' % TEN)
PDF = os.path.join(HERE, 'out', 'SRS - %s.pdf' % TEN)
Q_XEM = 'Xem xử lý thừa thiếu nhập kho'
Q_TAO = 'Tạo phiếu báo hàng thừa, thiếu nhập kho'
PB = 'Phiếu báo hàng thừa, thiếu nhập kho'
TN = 'Người dùng đăng nhập hệ thống (dữ liệu theo phạm vi xem — Phần 2)'
DK = '1. Người dùng đăng nhập thành công.'
LOAI = ('Nhập hàng mua trong nước; Nhập hàng mua trong nước (HĐNT); Nhập hàng mua trong nước (TỰ DO + HÃNG); '
        'Nhập hàng mua nước ngoài; Nhập hàng mua nước ngoài (mới); Nhập hàng mua ngoài')

P5 = [
    ('Kho', PB + ' (nút "Báo hàng thừa thiếu" mở trang Tạo phiếu báo đã chọn sẵn phiếu nhập kho; cửa sổ "Chọn phiếu nhập kho" của trang Tạo dùng đúng danh sách này)',
     'Kho => Nhập kho => ' + PB),
    ('Kho', 'Phiếu nhập kho (nguồn dữ liệu: phiếu Đã hạch toán, dòng hàng SL đề nghị / SL thực nhập; cột Mã phiếu mở chi tiết)',
     'Kho => Nhập kho => Phiếu nhập kho (hoặc Tài chính => Nhập hàng => Phiếu nhập kho)'),
    ('Kho', 'Phiếu đề nghị nhập kho (cột Phiếu ĐNNK mở chi tiết; Người đề nghị = người lập đề nghị)',
     'Kho => Nhập kho => Phiếu đề nghị nhập kho'),
    ('Tài chính', 'Yêu cầu nhập hàng (cột Người yêu cầu = người lập yêu cầu nhập hàng)', 'Tài chính => Nhập hàng => Yêu cầu nhập hàng'),
]

FR = []

FR.append({
    'ten': 'Xem danh sách phiếu nhập kho chờ báo thừa, thiếu',
    'qtc': 'Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xem danh sách phiếu nhập kho chờ báo thừa, thiếu'],
        ['Mô tả', 'Hiển thị các phiếu nhập kho đã hạch toán có hàng thực nhập lệch số lượng đề nghị và chưa có phiếu báo (BR-01), trong phạm vi xem của người dùng; mỗi dòng có nút "Báo hàng thừa thiếu".'],
        ['Tác nhân', TN],
        ['Điều kiện ban đầu', DK],
        ['Dòng sự kiện chính', '1. Người dùng mở màn theo đường dẫn menu.\n2. Hệ thống tải trang đầu (10 dòng), phiếu nhập kho tạo gần nhất ở trên cùng.\n3. Bảng hiển thị dữ liệu, chân bảng ghi "Hiển thị a–b / N".'],
        ['Dòng sự kiện phụ', '• Không có phiếu nào → bảng hiện "Không có phiếu nhập kho nào chờ báo thừa, thiếu."\n• Phiếu nhập lại (nhập lại cho phiếu khác) ghi thêm dòng phụ "Nhập lại cho phiếu <mã>" dưới mã phiếu.\n• Nút "Báo hàng thừa thiếu" chỉ hiện với người có quyền "%s".' % Q_TAO],
    ],
    'anh': [('01_list', 'Màn danh sách Phiếu nhập kho chờ báo thừa, thiếu lúc mới truy cập'),
            ('01b_list_actions', 'Cột Hành động với nút Báo hàng thừa thiếu')],
    'ui': ui(UI6, [
        ['Tiêu đề bảng', 'Label', 'Hiển thị', 'Danh sách phiếu nhập kho chờ báo thừa, thiếu', 'Tiêu đề trang: "Phiếu nhập kho chờ báo thừa, thiếu". Màn không có nút Tạo mới.'],
        ['Nút Xuất Excel', 'Button', 'Enable', 'Hiển thị', 'Mở cửa sổ "Chọn trường xuất Excel" (mục 2.5); trong lúc xuất cạnh nút hiện tiến độ.'],
        ['Nút Cấu hình cột hiển thị', 'Button', 'Enable', 'Hiển thị', 'Mở cửa sổ "Tuỳ chỉnh cột" (mục 2.3).'],
        ['Cột STT', 'Table/Grid', 'Read-only', 'Hiển thị', 'Số thứ tự liên tục qua các trang. Cột khóa.'],
        ['Cột Mã phiếu', 'Table/Grid', 'Read-only', 'Hiển thị', '- Mã phiếu nhập kho; liên kết mở chi tiết phiếu nhập kho ở tab mới. Sắp xếp được. Cột khóa.\n- Phiếu nhập lại: dòng phụ in nghiêng "Nhập lại cho phiếu <mã phiếu gốc>" (mã gốc cũng là liên kết).'],
        ['Cột Loại', 'Table/Grid', 'Read-only', 'Hiển thị', 'Loại phiếu nhập kho (6 loại nhập hàng mua — BR-01).'],
        ['Cột Nhà cung cấp', 'Table/Grid', 'Read-only', 'Hiển thị', 'Không có thì để trống.'],
        ['Cột Ngày tạo', 'Table/Grid', 'Read-only', 'Hiển thị', 'Ngày tạo phiếu nhập kho dd/mm/yyyy hh:mm. Sắp xếp được.'],
        ['Cột Phiếu ĐNNK', 'Table/Grid', 'Read-only', 'Hiển thị', 'Mã phiếu đề nghị nhập kho; liên kết mở chi tiết ở tab mới.'],
        ['Cột Người đề nghị', 'Table/Grid', 'Read-only', 'Hiển thị', '"Họ tên - Mã phòng ban" người lập phiếu đề nghị nhập kho.'],
        ['Cột Người yêu cầu', 'Table/Grid', 'Read-only', 'Hiển thị', '"Họ tên - Mã phòng ban" người lập yêu cầu nhập hàng.'],
        ['Cột Người tạo', 'Table/Grid', 'Read-only', 'Hiển thị', '"Họ tên - Mã phòng ban" người lập phiếu nhập kho.'],
        ['Cột Hành động', 'Table/Grid', 'Read-only', 'Hiển thị', 'Nút "Báo hàng thừa thiếu" (biểu tượng chấm than) — chỉ khi có quyền "%s"; không có quyền thì cột trống. Cột khóa.' % Q_TAO],
        ['Phân trang', 'Table/Grid', 'Enable', '10 dòng/trang', 'Chọn số dòng/trang, chuyển trang; chân bảng "Hiển thị a–b / N".'],
    ]),
    'ui_widths': UI6W,
    'events': [
        ['Mở màn hình', 'System', 'Before:\n– Mục menu hiện với mọi người dùng; dữ liệu giới hạn theo phạm vi xem (BR-02).\nAfter:\n– Tải trang 1, mới nhất trên cùng; khôi phục bộ lọc đã ghi nhớ (nếu còn trong 10 phút).'],
        ['Bấm tiêu đề cột Mã phiếu / Ngày tạo', 'Click', 'After:\n– Đổi chiều sắp xếp tăng / giảm, tải lại từ trang 1.'],
        ['Chuyển trang / đổi số dòng', 'Click', 'After:\n– Giữ bộ lọc, thứ tự; đổi số dòng thì về trang 1.'],
        ['Bấm Mã phiếu / Phiếu ĐNNK', 'Click', 'After:\n– Mở chi tiết chứng từ ở tab mới.'],
    ],
})

FR.append({
    'ten': 'Tìm kiếm và lọc danh sách',
    'qtc': 'Kịch bản tìm kiếm, Bộ lọc, Dropdown và Phân trang.',
    'gioi_thieu': [
        ['Tên chức năng', 'Tìm kiếm và lọc danh sách'],
        ['Mô tả', 'Thu hẹp danh sách bằng ô tìm kiếm nhanh và các ô lọc ở khu vực Tìm kiếm nâng cao.'],
        ['Tác nhân', TN],
        ['Điều kiện ban đầu', DK + '\n2. Đang ở màn danh sách.'],
        ['Dòng sự kiện chính', '1. Người dùng nhập mã phiếu nhập kho rồi bấm Tìm kiếm hoặc Enter; hoặc bấm Tìm kiếm nâng cao và chọn / nhập giá trị ở các ô lọc.\n2. Hệ thống áp đồng thời mọi điều kiện, tải lại danh sách từ trang 1.'],
        ['Dòng sự kiện phụ', '• Ô gõ chữ (tìm nhanh, Hàng hóa, Phiếu ĐNNK) chỉ lọc khi bấm Tìm kiếm / Enter; ô chọn lọc ngay khi chọn.\n• Bấm Làm mới → xoá mọi điều kiện.\n• Ô Công ty chỉ hiện với người xem mức Tổng công ty.\n• Ghi nhớ bộ lọc 10 phút.'],
    ],
    'anh': [('02_filter', 'Khu vực Tìm kiếm nâng cao ở trạng thái mở')],
    'ui': ui(UI7, [
        ['Ô tìm kiếm nhanh', 'Textbox', 'Enable', '0–255 ký tự', 'Trống', 'Placeholder "Tìm theo mã phiếu nhập kho"; tìm gần đúng.'],
        ['Nút Tìm kiếm / Làm mới', 'Button', 'Enable', '–', '–', 'Áp dụng / xoá mọi điều kiện.'],
        ['Nút Tìm kiếm nâng cao', 'Button', 'Enable', '–', 'Thu gọn', 'Mở / đóng khu vực ô lọc.'],
        ['Nút Cài đặt bộ lọc', 'Button', 'Enable', '–', '–', 'Mở cửa sổ "Cài đặt bộ lọc" (mục 2.3).'],
        ['Ô Hàng hóa', 'Textbox', 'Enable', '0–255 ký tự', 'Trống', 'Placeholder "Mã hoặc tên hàng"; phiếu có ít nhất 1 dòng hàng khớp.'],
        ['Ô Kho hàng', 'Dropdown', 'Enable', 'Kho có trên phiếu trong phạm vi', 'Trống', '"Mã - Tên kho"; kho đã khóa kèm biểu tượng khóa.'],
        ['Ô Phiếu ĐNNK', 'Textbox', 'Enable', '0–255 ký tự', 'Trống', 'Placeholder "Mã phiếu đề nghị nhập kho"; tìm gần đúng.'],
        ['Ô Loại', 'Dropdown', 'Enable', '6 loại', 'Trống', LOAI + '.'],
        ['Ô Nhà cung cấp', 'Dropdown', 'Enable', 'Nhà cung cấp có trên phiếu', 'Trống', 'Nhà cung cấp đã khóa kèm biểu tượng khóa.'],
        ['Ô Người đề nghị', 'Dropdown', 'Enable', 'Người lập đề nghị nhập kho', 'Trống', '"Mã phòng ban - Họ tên".'],
        ['Ô Ngày tạo', 'Datepicker', 'Enable', 'dd/mm/yyyy, Từ → Đến', 'Trống', 'Lọc theo ngày tạo phiếu nhập kho, tính cả 2 đầu mút.'],
        ['Ô Công ty', 'Dropdown', 'Enable / Ẩn', 'Công ty đang hoạt động', 'Trống', 'Chỉ hiện với người xem mức Tổng công ty.'],
    ]),
    'ui_widths': UI7W,
    'events': [
        ['Bấm Tìm kiếm / Enter', 'Click', 'After:\n– Áp đồng thời từ khóa và ô lọc, tải lại từ trang 1.'],
        ['Chọn giá trị ở ô chọn', 'Change', 'After:\n– Tải lại bảng từ trang 1 ngay.'],
        ['Bấm Làm mới', 'Click', 'After:\n– Xoá mọi điều kiện, tải lại danh sách đầy đủ.'],
    ],
})

FR.append({
    'ten': 'Cài đặt bộ lọc và tuỳ chỉnh cột',
    'qtc': 'Bộ lọc, Cấu hình cột và lưu cấu hình theo người dùng.',
    'gioi_thieu': [
        ['Tên chức năng', 'Cài đặt bộ lọc và tuỳ chỉnh cột'],
        ['Mô tả', 'Chọn ô lọc / cột nào hiển thị và thứ tự; lưu theo từng người dùng, từng màn.'],
        ['Tác nhân', TN],
        ['Điều kiện ban đầu', DK + '\n2. Đang ở màn danh sách.'],
        ['Dòng sự kiện chính', '1. Bấm "Cài đặt bộ lọc" (hoặc Cấu hình cột hiển thị).\n2. Tích / bỏ tích, kéo đổi thứ tự.\n3. Bấm Lưu: áp dụng ngay.'],
        ['Dòng sự kiện phụ', '• Bấm Đóng: bỏ thay đổi.\n• Cài đặt bộ lọc có "Khôi phục mặc định".\n• Cột STT, Mã phiếu, Hành động không bỏ được.'],
    ],
    'menu_them': ' => Cài đặt bộ lọc {icon:btn_caidatboloc} / Cấu hình cột hiển thị {icon:btn_cauhinhcot}',
    'ghi_chu_layout': 'Modal Cài đặt bộ lọc và Modal Tuỳ chỉnh cột được mở ngay trên màn hình danh sách theo đường dẫn ở trên.',
    'anh': [('26_filtercfg', 'Cửa sổ Cài đặt bộ lọc'), ('25_colcfg', 'Cửa sổ Tuỳ chỉnh cột')],
    'ui': ui(UI6, [
        ['Danh sách ô lọc', 'Checkbox', 'Enable', '8 ô (7 nếu không có Công ty)', 'Tích ô muốn hiện, kéo đổi thứ tự.'],
        ['Nút Khôi phục mặc định', 'Button', 'Enable', '–', 'Đưa cấu hình ô lọc về mặc định.'],
        ['Danh sách cột', 'Checkbox', 'Enable', '10/10 cột', 'STT, Mã phiếu, Hành động bị khóa. Dòng đếm "Đang chọn x/10 cột".'],
        ['Nút Chọn tất cả / Bỏ chọn hết', 'Button', 'Enable', '–', 'Chọn / bỏ nhanh (trừ cột khóa).'],
        ['Nút Lưu / Đóng', 'Button', 'Enable', '–', 'Lưu áp dụng ngay / đóng không lưu.'],
    ]),
    'ui_widths': UI6W,
    'events': [
        ['Bấm Lưu', 'Click', 'After:\n– Lưu cấu hình theo người dùng, vẽ lại bảng / khu vực lọc.'],
        ['Bấm Đóng / (x)', 'Click', 'After:\n– Đóng cửa sổ, không lưu.'],
    ],
})

FR.append({
    'ten': 'Báo hàng thừa thiếu', 'uc': 'uc_bao', 'uc_ten': 'FR-04 Báo hàng thừa thiếu cho phiếu nhập kho',
    'qtc': 'Liên kết màn hình và Màn Thêm mới.',
    'gioi_thieu': [
        ['Tên chức năng', 'Báo hàng thừa thiếu'],
        ['Mô tả', 'Từ 1 dòng của hàng chờ, mở trang "Tạo phiếu báo hàng thừa, thiếu nhập kho" với ô Phiếu nhập kho đã chọn sẵn; việc lập phiếu theo SRS màn %s (mục Lập phiếu báo). Phiếu báo lưu xong (Đang tạo hoặc Chờ xử lý) thì phiếu nhập kho rời khỏi hàng chờ.' % PB],
        ['Tác nhân', 'Người dùng có quyền "%s"' % Q_TAO],
        ['Điều kiện ban đầu', DK + '\n2. Người dùng có quyền "%s".' % Q_TAO],
        ['Dòng sự kiện chính', '1. Bấm "Báo hàng thừa thiếu" ở cột Hành động.\n2. Hệ thống mở trang Tạo phiếu báo, nạp Phiếu nhập kho, Yêu cầu nhập, Số hợp đồng, Nhà cung cấp và bảng Chi tiết (các dòng lệch SL).\n3. Người dùng nhập Diễn giải, đính kèm file, bấm Lưu / Lưu và gửi.\n4. Hệ thống tạo phiếu báo, về màn danh sách %s; phiếu nhập kho không còn ở hàng chờ.' % PB],
        ['Dòng sự kiện phụ', '• Phiếu nhập kho vừa được người khác báo / không còn đủ điều kiện → toast "Phiếu nhập kho không còn chờ báo thừa, thiếu hoặc bạn không có quyền.", ô Phiếu nhập kho để trống.\n• Bấm Quay lại ở trang Tạo → về danh sách %s (không về hàng chờ); đã nhập thì hỏi "Thông tin chưa lưu".\n• Bấm "Lưu và tiếp tục" → lưu rồi mở trang Tạo trống (không còn chọn sẵn).' % PB],
    ],
    'menu_them': ' => Báo hàng thừa thiếu {icon:btn_baohang}',
    'ghi_chu_layout': 'Trang Tạo phiếu báo hàng thừa, thiếu nhập kho mở thay trang hiện tại.',
    'anh': [('10_create_from_queue', 'Trang Tạo phiếu báo mở từ nút Báo hàng thừa thiếu: phiếu nhập kho và bảng Chi tiết đã điền sẵn')],
    'ui': ui(UI4, [
        ['Nút Báo hàng thừa thiếu', 'Button', 'Biểu tượng chấm than trong vòng tròn ở cột Hành động; ẩn khi không có quyền Tạo.'],
        ['Trang Tạo phiếu báo', 'Page', 'Như SRS %s: Phiếu nhập kho (chọn sẵn, bỏ chọn được), Yêu cầu nhập, Số hợp đồng, Nhà cung cấp, Diễn giải (bắt buộc), File đính kèm (bắt buộc), bảng Chi tiết; nút Lưu, Lưu và gửi, Lưu và tiếp tục, Quay lại.' % PB],
    ]),
    'ui_widths': UI4W,
    'events': [
        ['Bấm Báo hàng thừa thiếu', 'Click', 'Before:\n– Nút chỉ hiện khi có quyền "%s".\nAfter:\n– Mở trang Tạo phiếu báo; hệ thống kiểm phiếu nhập kho còn chờ báo và thuộc phạm vi rồi nạp dữ liệu.' % Q_TAO],
        ['Lưu phiếu báo ở trang Tạo', 'Click', 'After:\n– Theo SRS %s; phiếu nhập kho rời hàng chờ. Xóa phiếu báo sau này thì phiếu nhập kho quay lại hàng chờ.' % PB],
    ],
})

FR.append({
    'ten': 'Xuất Excel danh sách', 'uc': 'uc_xuat', 'uc_ten': 'FR-05 Xuất Excel danh sách chờ báo thừa, thiếu',
    'qtc': 'Quy tắc Excel và Cấu hình cột.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xuất danh sách ra Excel'],
        ['Mô tả', 'Xuất mọi dòng khớp bộ lọc (mọi trang) ra file danh_sach_phieu_nhap_kho_cho_bao_thua_thieu.xlsx, tiêu đề "DANH SÁCH PHIẾU NHẬP KHO CHỜ BÁO THỪA, THIẾU".'],
        ['Tác nhân', TN],
        ['Điều kiện ban đầu', DK],
        ['Dòng sự kiện chính', '1. Bấm Xuất Excel.\n2. Hệ thống mở cửa sổ "Chọn trường xuất Excel", tích sẵn các trường ứng với cột đang hiện trên bảng.\n3. Người dùng tích / bỏ, kéo đổi thứ tự, bấm Xuất file.\n4. Hệ thống tải dữ liệu theo lô, dựng file và tải về; báo "Xuất Excel thành công".'],
        ['Dòng sự kiện phụ', '• Không có dòng nào → "Không có dữ liệu để xuất", không tải file.\n• Lỗi → "Lỗi khi xuất Excel".'],
    ],
    'menu_them': ' => Xuất Excel {icon:btn_xuatexcel}',
    'ghi_chu_layout': 'Modal Chọn trường xuất Excel được mở ngay trên màn hình danh sách theo đường dẫn ở trên.',
    'anh': [('20_export', 'Cửa sổ Chọn trường xuất Excel')],
    'ui': ui(UI8, [
        ['Danh sách trường', 'Checkbox', 'Enable', '8 trường', 'Có (≥ 1)', 'Các cột đang hiện', 'Mã phiếu, Loại, Nhà cung cấp, Ngày tạo, Phiếu ĐNNK, Người đề nghị, Người yêu cầu, Người tạo. File luôn có cột STT đầu.'],
        ['Nút Chọn tất cả / Bỏ chọn hết', 'Button', 'Enable', '–', '–', '–', 'Chọn / bỏ nhanh.'],
        ['Dòng đếm', 'Label', 'Read-only', '–', '–', '–', '"Đang chọn x/8 trường".'],
        ['Nút Xuất file / Đóng', 'Button', 'Enable', '–', '–', '–', 'Xuất file / đóng không xuất.'],
    ]),
    'ui_widths': UI8W,
    'events': [
        ['Bấm Xuất file', 'Click', 'After:\n– Tải dữ liệu theo bộ lọc + phạm vi, dựng file, tải về; báo kết quả.'],
        ['Bấm Đóng / (x)', 'Click', 'After:\n– Đóng cửa sổ.'],
    ],
})

FR_NAMES = ['FR-%02d %s' % (i + 1, f['ten']) for i, f in enumerate(FR)]

S = {
    'ten': TEN, 'ten_ngan': 'phiếu nhập kho chờ báo thừa, thiếu', 'phan_he': 'Kho',
    'menu': [('Kho', 'menu_phanhe'), ('Nhập kho', 'menu_nhom'), (TEN, 'menu_muc')],
    'muc_dich': [
        'Thống nhất yêu cầu cho HÀNG CHỜ BÁO THỪA / THIẾU: danh sách phiếu nhập kho đã hạch toán có hàng thực nhập khác số lượng đề nghị mà chưa được lập phiếu báo — để thủ kho / người phụ trách lập phiếu báo hàng thừa, thiếu.',
        'Là căn cứ nghiệm thu điều kiện vào / ra hàng chờ, phạm vi dữ liệu và lối sang màn ' + PB + '.',
        'Màn chỉ xem và chuyển tiếp: không thêm / sửa / xóa phiếu nhập kho, không ghi tồn kho, không sinh bút toán.',
    ],
    'thuat_ngu': [
        ['Phiếu nhập kho chờ báo thừa, thiếu', 'Phiếu nhập kho thỏa đủ điều kiện BR-01, chưa có phiếu báo.'],
        ['Phiếu báo hàng thừa, thiếu nhập kho (phiếu báo)', 'Chứng từ lập từ 1 phiếu nhập kho để báo các dòng hàng lệch số lượng (màn STT 289).'],
        ['Dòng hàng lệch', 'Dòng hàng của phiếu nhập kho có SL thực nhập khác SL đề nghị nhập (so phần nguyên).'],
        ['Phiếu ĐNNK', 'Phiếu đề nghị nhập kho — chứng từ nguồn của phiếu nhập kho.'],
        ['Người đề nghị / Người yêu cầu / Người tạo', 'Người lập phiếu đề nghị nhập kho / người lập yêu cầu nhập hàng / người lập phiếu nhập kho.'],
    ],
    'trang_thai': {
        'cau_dan': 'Màn KHÔNG có trạng thái riêng và không có bước duyệt. Một phiếu nhập kho có mặt trong hàng chờ hay không do hệ thống '
                   'tự xác định theo việc đã có phiếu báo hay chưa.',
        'rows': [
            ['Chờ báo thừa, thiếu', 'Phiếu nhập kho thỏa BR-01, chưa có phiếu báo — hiện trên màn.', 'Xem, Báo hàng thừa thiếu, Xuất Excel', 'Người có quyền "%s" (Báo); mọi người trong phạm vi (Xem)' % Q_TAO],
            ['Đã có phiếu báo', 'Đã lập phiếu báo (mọi trạng thái của phiếu báo) — không còn trên màn.', 'Xem ở màn ' + PB, 'Tự chuyển khi phiếu báo được lưu'],
        ],
        'anh': 'state_flow',
        'ghi_chu': ['Xóa phiếu báo (chỉ khi phiếu báo Đang tạo / Không duyệt) thì phiếu nhập kho quay lại hàng chờ.'],
    },
    'quyen_truoc': ['Mục menu và màn hình mở được với mọi người dùng đã đăng nhập; quyền quyết định phạm vi dữ liệu và nút "Báo hàng thừa thiếu". '
                    'Các quyền thuộc phân hệ Kho, nhóm Nhập kho; Super Admin có mọi quyền.'],
    'quyen_rows': [
        [Q_XEM + ' (mức: Công ty / Tổng công ty)', 'Mở rộng phạm vi xem danh sách và xuất Excel (bảng bên dưới); dùng chung với màn ' + PB + '.'],
        [Q_TAO, 'Thấy nút "Báo hàng thừa thiếu" trên từng dòng và lập được phiếu báo.'],
    ],
    'pham_vi_truoc': ['Phạm vi dữ liệu (xét theo thứ tự, gặp mức nào trước thì áp mức đó):'],
    'pham_vi_rows': [
        ['1', Q_XEM + ' — mức Tổng công ty', 'Phiếu nhập kho của mọi công ty; khu vực lọc có ô Công ty.'],
        ['2', Q_XEM + ' — mức Công ty', 'Phiếu nhập kho thuộc công ty đang làm việc của người dùng.'],
        ['3', '(không có quyền xem)', 'Chỉ phiếu nhập kho do chính người dùng lập.'],
    ],
    'pham_vi_sau': ['Công ty của dòng = công ty của phiếu nhập kho. Phạm vi áp như nhau cho danh sách, xuất Excel, cửa sổ chọn phiếu nhập kho '
                    'và khi mở trang Tạo phiếu báo từ dòng.'],
    'ma_tran': [['Chức năng', 'Không có quyền', Q_XEM, Q_TAO]] + [
        [FR_NAMES[i]] + (['Không', 'Không', 'Có'] if i == 3 else ['Có (theo phạm vi)'] * 3) for i in range(len(FR))],
    'ma_tran_widths': [2.4, 1.2, 1.4, 1.4],
    'quyen_sau': ['"Có (theo phạm vi)": thao tác trên các phiếu nhập kho thuộc phạm vi ở bảng trên.'],
    'fr': FR,
    'quy_tac': [
        ('BR-01', 'Điều kiện vào hàng chờ', ['– Phiếu nhập kho ở trạng thái Đã hạch toán.', '– Loại: ' + LOAI + '.', '– Có ít nhất 1 dòng hàng SL thực nhập khác SL đề nghị nhập, so phần nguyên (lệch phần thập phân không tính).', '– Chưa có phiếu báo nào (mọi trạng thái).'], ['Xem danh sách', 'Báo hàng thừa thiếu']),
        ('BR-02', 'Phạm vi dữ liệu', ['– Tổng công ty → mọi phiếu; Công ty → phiếu nhập kho của công ty đang làm việc; còn lại → phiếu nhập kho do mình lập.', '– Quyền Duyệt phiếu báo KHÔNG mở rộng phạm vi màn này.'], ['Mọi chức năng']),
        ('BR-03', 'Ra / vào lại hàng chờ', ['– Lưu phiếu báo (Lưu hoặc Lưu và gửi) → phiếu nhập kho rời hàng chờ.', '– Xóa phiếu báo → phiếu nhập kho quay lại hàng chờ.', '– Một phiếu nhập kho chỉ có 1 phiếu báo: 2 người cùng lập thì người lưu sau bị từ chối.'], ['Báo hàng thừa thiếu']),
        ('BR-04', 'Thứ tự mặc định', ['– Ngày tạo phiếu nhập kho giảm dần; sắp xếp được theo Mã phiếu, Ngày tạo.'], ['Xem danh sách']),
        ('BR-05', 'Không tác động số liệu', ['– Màn không ghi tồn kho, không sinh bút toán, không sửa phiếu nhập kho.'], ['Mọi chức năng']),
        ('BR-06', 'Xuất Excel', ['– Theo đúng bộ lọc và phạm vi (mọi trang); không có dữ liệu thì không tải file.'], ['Xuất Excel']),
    ],
    'phan5': {'cau_dan': 'Các màn hình dưới đây cung cấp dữ liệu cho hàng chờ hoặc dùng dữ liệu của hàng chờ.', 'rows': P5},
}

UML = {
    'actor': 'Người dùng (theo quyền)',
    'mains': [('FR-01', 'Xem danh sách chờ báo thừa, thiếu', 'view'), ('FR-04', 'Báo hàng thừa thiếu', 'crud'),
              ('FR-05', 'Xuất Excel danh sách', 'io')],
    'subs': [('FR-02', 'Tìm kiếm và lọc danh sách', 'view'), ('FR-03', 'Cài đặt bộ lọc, tuỳ chỉnh cột', 'view')],
    'rieng': [('FR-04', 'Báo hàng thừa thiếu', 'crud', 'uc_bao'), ('FR-05', 'Xuất Excel danh sách', 'io', 'uc_xuat')],
}

STATES = [('start', '', None), ('cho', 'Chờ báo thừa, thiếu', '#fef3c7'), ('da', 'Đã có phiếu báo', '#dcfce7')]
TRANS = [('start', 'cho', 'Phiếu nhập kho hạch toán, có hàng lệch'), ('cho', 'da', 'Lưu phiếu báo'),
         ('da', 'cho', 'Xóa phiếu báo')]

if __name__ == '__main__':
    scr = L.Screen(HERE)
    print(L.draw_uml(scr, UML['actor'], UML['mains'], UML['subs'], UML['rieng']))
    L.draw_state_flow(os.path.join(scr.uml, 'state_flow.png'), STATES, TRANS)
    print('docx:', L.build_srs(scr, S, OUT))
    if '--no-word' not in sys.argv:
        L.finalize_and_check(OUT, PDF, extra_banned=('ERP', 'API'))
