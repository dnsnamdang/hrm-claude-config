# -*- coding: utf-8 -*-
"""Sinh "SRS - Cấu hình duyệt giá.docx" theo FORM CHUẨN (2026-09-24).

Chạy:  python3 .plans/gop-db/cau-hinh-giao-viec-docs/gen_srs_duyet_gia.py
Nguồn đối chiếu code (nhánh gop_db):
  FE  pages/assign/settings/price-approval/index.vue · components/subsystem-menu/{sale-hub,sale}.js
  BE  Modules/Assign/Routes/api.php (bom-price-approval-configs) · BomPriceApprovalConfigController
      Services/BomPriceApprovalConfigService (calculateApprovalLevel / findLevel)
      Modules/Timesheet GeneralRegulationController (profit_margin_threshold, FIELD_PERMISSIONS)
  Quyền: PermissionsTableSeeder id 211 "Cấu hình phân hệ giao việc/ công tác" + "Thiết lập thông số"
"""
from _common import new_doc, shot, MENU_B, A_CH, NO_PERM

TEN_MAN = 'Cấu hình duyệt giá'
d = new_doc(TEN_MAN, MENU_B, '/assign/settings/price-approval', 'duyetgia_')

# ========================================================= PHAN 1
d.h1('Phần 1. Giới thiệu')
d.h2('1 Mục đích')
d.p('Tài liệu này đặc tả yêu cầu phần mềm cho màn Cấu hình duyệt giá, nhằm:')
d.bullets([
    'Là căn cứ nghiệm thu chức năng và phân quyền của màn Cấu hình duyệt giá.',
    'Làm rõ cách hệ thống xác định cấp duyệt của báo giá từ 3 điều kiện: giá trị đơn hàng, tỷ suất '
    'lợi nhuận, tỷ suất lợi nhuận dòng hàng tạm.',
    'Làm rõ cách các ngưỡng tự nối tiếp nhau giữa các cấp và ý nghĩa của tỷ suất lợi nhuận mức sàn.',
])

d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('Cấp duyệt', 'Cấp 1 = Người làm giá tự duyệt; Cấp 2 = Trưởng phòng; Cấp 3 = Ban giám đốc.'),
    ('V', 'Tổng giá trị đơn hàng trước thuế của báo giá (VNĐ).'),
    ('M', 'Tỷ suất lợi nhuận (%) = (Tổng bán trước thuế − Tổng nhập trước thuế) / Tổng nhập trước thuế × 100%.'),
    ('Hàng tạm', 'Dòng hàng chưa có trong danh mục hàng hóa, được thêm tạm vào báo giá.'),
    ('Tỷ suất lợi nhuận mức sàn', 'Ngưỡng tỷ suất lợi nhuận tối thiểu; báo giá dưới mức này hiện cảnh báo đỏ.'),
    ('Công ty đang làm việc', 'Công ty người dùng đang chọn ở góc trên bên phải màn hình.'),
], widths=[1.8, 4.2])

# ========================================================= PHAN 2
d.h1('Phần 2. Phân quyền')
d.h2('1 Danh sách quyền')
d.p('Nhóm quyền thao tác:')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('Q1', 'Cấu hình phân hệ giao việc/ công tác',
     'Hiển thị menu “Cấu hình duyệt giá” của phân hệ Bán hàng; được xem, lưu mọi cấu hình trên màn và xem '
     'lịch sử thay đổi.'),
    ('Q2', 'Thiết lập thông số',
     'Quyền của màn Quy định chung — được lưu riêng ô “Tỷ suất lợi nhuận mức sàn” (cùng dữ liệu với '
     'màn Quy định chung). Không làm hiện menu Cấu hình duyệt giá.'),
], widths=[0.8, 2.0, 3.2])
d.p('Màn cấu hình không phân quyền theo cấp dữ liệu (công ty/phòng ban/bộ phận). Phạm vi dữ liệu do '
    'loại cấu hình quyết định — xem quy tắc BR-01.')

d.h2('2 Ma trận phân quyền')
d.table(['Chức năng', 'Q1', 'Q2', 'Không có quyền nào'], [
    ('FR-01 Xem cấu hình duyệt giá', '✅', '❌', '❌'),
    ('FR-02 Cấu hình tỷ suất lợi nhuận mức sàn', '✅', '✅ (lưu được, không có menu vào màn)', '❌'),
    ('FR-03 Cấu hình duyệt theo giá trị đơn hàng', '✅', '❌', '❌'),
    ('FR-04 Cấu hình duyệt theo tỷ suất lợi nhuận', '✅', '❌', '❌'),
    ('FR-05 Cấu hình duyệt theo tỷ suất LN dòng hàng tạm', '✅', '❌', '❌'),
    ('FR-06 Xem lịch sử thay đổi cấu hình duyệt giá', '✅', '❌', '❌'),
], widths=[2.9, 0.6, 1.4, 1.1])

# ========================================================= PHAN 3
d.h1('Phần 3. Đặc tả chi tiết theo từng chức năng')
d.h2('1 Sơ đồ UML tổng quan')
d.overview_figure2(
    [(A_CH, [0, 1, 2, 3, 4])],
    [('FR-01', 'Xem cấu hình duyệt giá', 'view'),
     ('FR-02', 'Cấu hình tỷ suất LN mức sàn', 'crud'),
     ('FR-03', 'Duyệt theo giá trị đơn hàng', 'crud'),
     ('FR-04', 'Duyệt theo tỷ suất lợi nhuận', 'crud'),
     ('FR-05', 'Duyệt theo tỷ suất LN hàng tạm', 'crud')],
    [('FR-06', 'Xem lịch sử thay đổi', 'view', 'extend', [0], None)],
    'Sơ đồ Use Case tổng quan màn %s' % TEN_MAN)

d.h2('2 Đặc tả chi tiết từng chức năng')

# ------------------------------------------------------------------ 2.9 Duyet gia
d.h3('2.1 Xem cấu hình duyệt giá')
d.p('2.1.1 Giới thiệu')
d.rule_ref('- Màn Danh sách và UI/UX. Chỉ bổ sung các quy tắc riêng của màn Cấu hình duyệt giá tại phần '
           'mô tả chi tiết.', anchor='list')
d.intro_table(
    ten='Xem cấu hình duyệt giá',
    mota='Hiển thị trên 1 màn: Tỷ suất lợi nhuận mức sàn, 3 bảng ngưỡng cấp duyệt (theo giá trị đơn hàng, '
         'theo tỷ suất lợi nhuận, theo tỷ suất LN dòng hàng tạm) và Lịch sử thay đổi.',
    tacnhan='Người quản trị cấu hình; Người dùng đã đăng nhập',
    dieukien='Người dùng có quyền Q1.',
    chinh='1. Người dùng vào menu Cấu hình duyệt giá.\n'
          '2. Hệ thống nạp đồng thời: cấu hình 3 bảng cấp duyệt, 10 dòng lịch sử mới nhất, tỷ suất mức sàn '
          'của công ty đang làm việc.\n'
          '3. Màn hiển thị 5 khối từ trên xuống.',
    phu='• Không tải được cấu hình → “Lỗi tải cấu hình”.\n'
        '• Không tải được tỷ suất mức sàn → hiển thị 0.')
d.p('2.1.2 Layout màn hình')
d.layout(menu=MENU_B, shot=shot('08a-duyet-gia-view.png'),
         shot_caption='Màn Cấu hình duyệt giá lúc mới mở')
d.p('2.1.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề trang', 'Label', 'Hiển thị', '–', 'Cấu hình duyệt giá', '–'),
    ('Khối Tỷ suất lợi nhuận mức sàn', 'Card', 'Hiển thị', '–', 'Hiển thị', 'Xem FR-02.'),
    ('Khối Theo giá trị đơn hàng (VNĐ) trước thuế', 'Card', 'Hiển thị', '–', 'Hiển thị', 'Xem FR-03.'),
    ('Khối Theo tỷ suất lợi nhuận (%)', 'Card', 'Hiển thị', '–', 'Hiển thị', 'Xem FR-04.'),
    ('Khối Theo tỷ suất LN dòng hàng tạm (%)', 'Card', 'Hiển thị', '–', 'Hiển thị',
     'Xem FR-05; cuối khối có ghi chú “Cấp duyệt thực tế của báo giá = cấp cao nhất trong cả 3 điều kiện trên.”'),
    ('Khối Lịch sử thay đổi', 'Card', 'Hiển thị', '–', '10 dòng mới nhất', 'Xem FR-06.'),
    ('Cột chung của 3 bảng', 'Table/Grid', 'Read-only', '–', 'Cấp 1 → Cấp 3',
     'Cấp duyệt · Từ · Đến · Người duyệt · Mô tả. Người duyệt: Cấp 1 “Người làm giá (tự duyệt)”, '
     'Cấp 2 “Trưởng phòng”, Cấp 3 “Ban giám đốc”.'),
    ('Số tiền', 'Text', 'Read-only', '–', 'Theo dữ liệu', 'Định dạng 1,000,000,000.'),
], required=False)
d.p('2.1.4 Danh sách event và xử lý event')
d.event_table([
    ('Mở màn hình', 'System',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     'After:\n– Nạp 3 nhóm dữ liệu song song và hiển thị 5 khối.'),
])

# ------------------------------------------------------------------ 2.10
d.h3('2.2 Cấu hình tỷ suất lợi nhuận mức sàn')
d.p('2.2.1 Biểu đồ Usecase')
d.uc_figure('FR-02', 'Cấu hình tỷ suất LN mức sàn', 'crud', actor=A_CH)
d.p('2.2.2 Giới thiệu')
d.rule_ref('- Validate dữ liệu, Thông báo và UI/UX. Logic ghi lịch sử áp dụng theo SRS Các quy tắc chung '
           '- Quy tắc ghi lịch sử.', anchor='create')
d.intro_table(
    ten='Cấu hình tỷ suất lợi nhuận mức sàn',
    mota='Đặt ngưỡng tỷ suất lợi nhuận tối thiểu của công ty đang làm việc; báo giá dưới ngưỡng hiện cảnh báo đỏ.',
    tacnhan='Người quản trị cấu hình',
    dieukien='Người dùng có quyền Q1 hoặc Q2.',
    chinh='1. Người dùng nhập “Tỷ suất lợi nhuận mức sàn (%)”.\n'
          '2. Người dùng bấm “Lưu cấu hình” của khối.\n'
          '3. Hệ thống kiểm tra trong khoảng 0–100 và lưu.\n'
          '4. Hệ thống báo “Đã lưu mức sàn <X>%”.',
    phu='• Ngoài khoảng 0–100 → “Tỷ suất phải trong khoảng 0-100%”, không lưu.\n'
        '• Không có quyền Q1 lẫn Q2 → “Bạn không có quyền thực hiện chức năng này”.\n'
        '• Lỗi khác → hiển thị nội dung lỗi hoặc “Lưu thất bại”.',
    dacbiet='Cùng dữ liệu với ô Tỷ suất lợi nhuận mức sàn ở màn Quy định chung; lịch sử ghi ở lịch sử Quy định '
            'chung, không hiện ở khối Lịch sử thay đổi của màn này.')
d.p('2.2.3 Layout màn hình')
d.layout(menu=MENU_B + ' => Lưu cấu hình', shot=shot('09-san.png'),
         shot_caption='Khối Tỷ suất lợi nhuận mức sàn')
d.p('2.2.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Biểu tượng ⓘ', 'Icon', 'Hiển thị', '–', '–', 'Hiển thị',
     'Rê chuột: “Cài đặt tỷ suất lợi nhuận sàn chung cho từng hàng hóa/dịch vụ. Công thức: (M %) = (Thành tiền '
     'bán - Thành tiền nhập) / Thành tiền nhập × 100%”.'),
    ('Tỷ suất lợi nhuận mức sàn (%)', 'Number', 'Enable', '0 – 100, 2 chữ số thập phân', 'Có', 'Theo dữ liệu',
     'Gợi ý “VD: 15”. Chú thích bên cạnh: “Dưới mức này, báo giá sẽ hiện cảnh báo đỏ.”'),
    ('Nút Lưu cấu hình', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Hiện trạng thái đang xử lý khi lưu.'),
])
d.p('2.2.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Lưu cấu hình (khối mức sàn)', 'Click',
     'Before:\n– Kiểm tra quyền Q1 hoặc Q2.\n' + NO_PERM + '\n'
     'During:\n– Không phải số, < 0 hoặc > 100 → “Tỷ suất phải trong khoảng 0-100%”, dừng.\n'
     'After:\n– Lưu mức sàn cho công ty đang làm việc; báo giá mở sau đó dùng mức mới.\n'
     '– Hiển thị “Đã lưu mức sàn <X>%”.'),
])


def bang_cap(fr, so, ten, menu_shot, caption, mota, chinh, phu, dacbiet, ui, ev):
    d.h3('2.%d %s' % (so, ten))
    d.p('2.%d.1 Biểu đồ Usecase' % so)
    d.uc_figure(fr, ten, 'crud', actor=A_CH)
    d.p('2.%d.2 Giới thiệu' % so)
    d.rule_ref('- Validate dữ liệu, Thông báo và UI/UX. Logic ghi lịch sử áp dụng theo SRS Các quy tắc chung '
               '- Quy tắc ghi lịch sử.', anchor='create')
    d.intro_table(ten=ten, mota=mota, tacnhan='Người quản trị cấu hình',
                  dieukien='Người dùng có quyền Q1.', chinh=chinh, phu=phu, dacbiet=dacbiet)
    d.p('2.%d.3 Layout màn hình' % so)
    d.layout(menu=MENU_B + ' => Lưu cấu hình', shot=shot(menu_shot), shot_caption=caption)
    d.p('2.%d.4 Mô tả chi tiết giao diện' % so)
    d.ui_table(ui)
    d.p('2.%d.5 Danh sách event và xử lý event' % so)
    d.event_table(ev)


SAVE_AFTER = ('After:\n– Tự sinh lại cột Mô tả của từng cấp rồi lưu lần lượt Cấp 1 → Cấp 3.\n'
              '– Mỗi cấp có giá trị thay đổi được ghi 1 dòng lịch sử (giá trị cũ → mới).\n'
              '– Hiển thị “Lưu cấu hình thành công”, xóa thông báo lỗi của khối, nạp lại khối Lịch sử thay đổi.\n'
              '– Lỗi khi lưu → hiển thị nội dung lỗi hoặc “Lỗi khi lưu cấu hình”.')

bang_cap(
    'FR-03', 3, 'Cấu hình duyệt theo giá trị đơn hàng', '10-gia-tri.png',
    'Khối Theo giá trị đơn hàng (VNĐ) trước thuế',
    'Khai ngưỡng giá trị đơn hàng trước thuế (V) cho 3 cấp duyệt. Cấp càng cao ứng với giá trị càng lớn.',
    '1. Người dùng nhập ô “Đến (VNĐ)” của Cấp 1 và Cấp 2.\n'
    '2. Hệ thống tự gán “Từ” của cấp sau bằng “Đến” của cấp trước và sinh lại cột Mô tả.\n'
    '3. Người dùng bấm “Lưu cấu hình” của khối.\n'
    '4. Hệ thống kiểm tra thứ tự ngưỡng, lưu và báo “Lưu cấu hình thành công”.',
    '• Ngưỡng không tăng dần → hiển thị thông báo lỗi đỏ ở đầu khối, không lưu.',
    'Ngưỡng nối tiếp: V ≤ Đến cấp 1 → Cấp 1; Đến cấp 1 < V ≤ Đến cấp 2 → Cấp 2; V > Đến cấp 2 → Cấp 3.',
    [('Cấp duyệt', 'Label', 'Read-only', 'Cấp 1 – 3', '–', 'Theo dữ liệu', '–'),
     ('Từ (VNĐ) – Cấp 1', 'Number', 'Disable', '–', '–', '0', 'Luôn bắt đầu từ 0, không sửa được.'),
     ('Từ (VNĐ) – Cấp 2, 3', 'Text', 'Read-only', '–', '–', 'Bằng “Đến” cấp trước', 'Tự cập nhật.'),
     ('Đến (VNĐ) – Cấp 1, 2', 'Number', 'Enable', '> Từ cùng cấp', 'Có', 'Theo dữ liệu',
      'Ô tiền, ngăn cách hàng nghìn bằng dấu phẩy.'),
     ('Đến (VNĐ) – Cấp 3', 'Text', 'Read-only', '–', '–', 'Không giới hạn', '–'),
     ('Người duyệt', 'Text', 'Read-only', '–', '–', 'Theo cấp', '–'),
     ('Mô tả', 'Text', 'Read-only', '–', '–', 'Tự sinh',
      'Vd “Người làm giá (tự duyệt) (V ≤ 1,000,000,000)”, “Trưởng phòng (1,000,000,000 < V ≤ 20,000,000,000)”, '
      '“Ban giám đốc (V > 20,000,000,000)”.'),
     ('Thông báo lỗi đầu khối', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', 'Khung đỏ phía trên bảng.'),
     ('Nút Lưu cấu hình', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Lưu cả 3 cấp của khối.')],
    [('Sửa ô Đến (VNĐ)', 'Change',
      'After:\n– Gán “Từ” cấp sau = “Đến” cấp trước; sinh lại Mô tả; xóa thông báo lỗi của khối.'),
     ('Bấm Lưu cấu hình (khối giá trị đơn hàng)', 'Click',
      'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
      'During:\n– Cấp có Từ ≥ Đến → “Cấp <n>: Giá trị \"Từ\" (<a>) phải nhỏ hơn \"Đến\" (<b>).”\n'
      '– Đến cấp sau ≤ Đến cấp trước → “Cấp <n>: Giá trị \"Đến\" (<x>) phải lớn hơn cấp <m> (<y>).”\n'
      '– Nếu có lỗi → không thực hiện bước After.\n' + SAVE_AFTER)])

TS_UI = [
    ('Cấp duyệt', 'Label', 'Read-only', 'Cấp 1 – 3', '–', 'Theo dữ liệu', '–'),
    ('Từ (%) – Cấp 1, 2', 'Number', 'Enable', 'Số thập phân 2 chữ số', 'Có', 'Theo dữ liệu',
     'Ô trống được hiểu là 0.'),
    ('Từ (%) – Cấp 3', 'Text', 'Read-only', '–', '–', 'Không giới hạn', 'Bao gồm cả tỷ suất âm.'),
    ('Đến (%) – Cấp 1', 'Text', 'Read-only', '–', '–', 'Không giới hạn', '–'),
    ('Đến (%) – Cấp 2, 3', 'Text', 'Read-only', '–', '–', 'Bằng “Từ” cấp trước', 'Tự cập nhật.'),
    ('Người duyệt', 'Text', 'Read-only', '–', '–', 'Theo cấp', '–'),
    ('Mô tả', 'Text', 'Read-only', '–', '–', 'Tự sinh',
     'Vd “Người làm giá (tự duyệt) (M ≥ 35%)”, “Trưởng phòng (20% ≤ M < 35%)”, “Ban giám đốc (M < 20%)”.'),
    ('Biểu tượng ⓘ', 'Icon', 'Hiển thị', '–', '–', 'Hiển thị', 'Rê chuột hiện công thức tính.'),
    ('Thông báo lỗi đầu khối', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', 'Khung đỏ phía trên bảng.'),
    ('Nút Lưu cấu hình', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Lưu cả 3 cấp của khối.'),
]


def ts_ev(ten_khoi):
    return [('Sửa ô Từ (%)', 'Change',
             'After:\n– Gán “Đến” cấp sau = “Từ” cấp trước; Cấp 3 “Từ” = Không giới hạn; sinh lại Mô tả; '
             'xóa thông báo lỗi của khối.'),
            ('Bấm Lưu cấu hình (%s)' % ten_khoi, 'Click',
             'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
             'During:\n– Cấp có Từ ≥ Đến → “Cấp <n>: Giá trị \"Từ\" (<a>) phải nhỏ hơn \"Đến\" (<b>).”\n'
             '– Từ cấp sau ≥ Từ cấp trước → “Cấp <n>: Giá trị \"Từ\" (<x>%) phải nhỏ hơn cấp <m> (<y>%).”\n'
             '– Nếu có lỗi → không thực hiện bước After.\n' + SAVE_AFTER)]


bang_cap(
    'FR-04', 4, 'Cấu hình duyệt theo tỷ suất lợi nhuận', '11-ty-suat.png', 'Khối Theo tỷ suất lợi nhuận (%)',
    'Khai ngưỡng tỷ suất lợi nhuận tổng (M) của báo giá cho 3 cấp duyệt. Ngược với giá trị đơn hàng: tỷ suất '
    'càng cao càng dễ duyệt.',
    '1. Người dùng nhập ô “Từ (%)” của Cấp 1 và Cấp 2.\n'
    '2. Hệ thống tự gán “Đến” của cấp sau bằng “Từ” của cấp trước và sinh lại Mô tả.\n'
    '3. Người dùng bấm “Lưu cấu hình” của khối.\n'
    '4. Hệ thống kiểm tra thứ tự ngưỡng, lưu và báo “Lưu cấu hình thành công”.',
    '• Ngưỡng không giảm dần theo cấp → thông báo lỗi đỏ ở đầu khối, không lưu.\n'
    '• Rê chuột ⓘ → “Áp dụng tỷ suất lợi nhuận cho tổng giá trị đơn hàng trước thuế. Công thức: M (%) = '
    '(Tổng bán trước thuế - Tổng nhập trước thuế) / Tổng nhập trước thuế × 100%”.',
    'M ≥ Từ cấp 1 → Cấp 1; Từ cấp 2 ≤ M < Từ cấp 1 → Cấp 2; M < Từ cấp 2 → Cấp 3.',
    TS_UI, ts_ev('khối tỷ suất lợi nhuận'))

bang_cap(
    'FR-05', 5, 'Cấu hình duyệt theo tỷ suất LN dòng hàng tạm', '12-hang-tam.png',
    'Khối Theo tỷ suất LN dòng hàng tạm (%)',
    'Khai ngưỡng tỷ suất lợi nhuận của DÒNG hàng tạm trong báo giá cho 3 cấp duyệt; cách nhập giống khối '
    'tỷ suất lợi nhuận.',
    '1. Người dùng nhập ô “Từ (%)” của Cấp 1 và Cấp 2.\n'
    '2. Hệ thống tự gán “Đến” của cấp sau và sinh lại Mô tả.\n'
    '3. Người dùng bấm “Lưu cấu hình” của khối.\n'
    '4. Hệ thống kiểm tra, lưu và báo “Lưu cấu hình thành công”.',
    '• Ngưỡng không giảm dần theo cấp → thông báo lỗi đỏ ở đầu khối, không lưu.\n'
    '• Rê chuột ⓘ → giải thích: áp cho từng dòng hàng tạm, M (%) = (Giá bán - Giá nhập) / Giá nhập × 100%; '
    'nhiều hàng tạm thì lấy dòng có tỷ suất thấp nhất; dòng chưa nhập giá vốn tính là 0%.',
    'Báo giá không có hàng tạm thì bỏ qua điều kiện này (không bị đẩy lên Cấp 3).',
    TS_UI, ts_ev('khối hàng tạm'))

# ------------------------------------------------------------------ 2.14
d.h3('2.6 Xem lịch sử thay đổi cấu hình duyệt giá')
d.p('2.6.1 Giới thiệu')
d.rule_ref('- Quy tắc ghi lịch sử. Chỉ bổ sung các quy tắc riêng tại phần mô tả chi tiết.', anchor='history')
d.intro_table(
    ten='Xem lịch sử thay đổi cấu hình duyệt giá',
    mota='Khối cuối màn liệt kê các lần thay đổi ngưỡng của 3 bảng cấp duyệt, mới nhất ở trên.',
    tacnhan='Người quản trị cấu hình; Người dùng đã đăng nhập',
    dieukien='Người dùng có quyền Q1.',
    chinh='1. Hệ thống hiển thị 10 dòng lịch sử mới nhất khi mở màn.\n'
          '2. Mỗi dòng: thời điểm (dd/mm/yyyy hh:mm), người thay đổi, nhóm cấu hình, cấp, giá trị cũ → giá trị mới.\n'
          '3. Người dùng bấm “Xem thêm” để nạp tiếp 10 dòng cũ hơn.',
    phu='• Chưa có thay đổi → “Chưa có lịch sử thay đổi”.\n'
        '• Đã hết trang → nút “Xem thêm” ẩn.\n'
        '• Lưu xong 1 bảng cấp duyệt → khối tự nạp lại từ trang đầu.')
d.p('2.6.2 Layout màn hình')
d.layout(menu=MENU_B, shot=shot('13-lich-su.png'), shot_caption='Khối Lịch sử thay đổi của màn Cấu hình duyệt giá')
d.p('2.6.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề khối', 'Label', 'Hiển thị', '–', 'Lịch sử thay đổi', '–'),
    ('Thời điểm', 'Text', 'Read-only', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu', '–'),
    ('Người thay đổi', 'Text', 'Read-only', '–', 'Theo dữ liệu', 'Kèm chữ “thay đổi cấu hình”.'),
    ('Nhóm cấu hình', 'Badge', 'Read-only', '3 giá trị', 'Theo dữ liệu',
     '“Giá trị ĐH” / “Tỷ suất LN” / “Tỷ suất LN hàng tạm”.'),
    ('Cấp', 'Text', 'Read-only', 'Cấp 1 – 3', 'Theo dữ liệu', '–'),
    ('Giá trị cũ → mới', 'Text', 'Read-only', '–', 'Theo dữ liệu',
     '“Từ: a, Đến: b → Từ: c, Đến: d”; không giới hạn hiện “∞”. Giá trị cũ màu đỏ, mới màu xanh.'),
    ('Nút Xem thêm', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi chỉ có 1 trang', 'Nạp thêm 10 dòng.'),
    ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn', '“Chưa có lịch sử thay đổi”.'),
], required=False)
d.p('2.6.4 Danh sách event và xử lý event')
d.event_table([
    ('Mở màn / sau khi lưu bảng cấp duyệt', 'System', 'After:\n– Nạp trang 1 (10 dòng mới nhất).'),
    ('Bấm Xem thêm', 'Click', 'After:\n– Nạp trang kế tiếp, nối vào cuối danh sách.'),
])


# ==================================================== PHAN 4
d.h1('Phần 4. Quy tắc nghiệp vụ')
d.rule_ref('. Phần này chỉ ghi các quy tắc đặc thù của màn Cấu hình duyệt giá; không lặp lại các quy tắc đã '
           'có trong SRS quy tắc chung.', anchor='list', head='Quy tắc áp dụng',
           lead='Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ')
d.rule_table([
    ('BR-01', 'Phạm vi áp dụng cấu hình', [
        '– 3 bảng cấp duyệt (giá trị đơn hàng, tỷ suất lợi nhuận, tỷ suất LN dòng hàng tạm) DÙNG CHUNG toàn hệ '
        'thống, không tách theo công ty.',
        '– Tỷ suất lợi nhuận mức sàn áp dụng theo CÔNG TY ĐANG LÀM VIỆC.',
    ], 'Toàn màn hình'),
    ('BR-02', 'Xác định cấp duyệt báo giá', [
        '– Cấp duyệt = cấp CAO NHẤT trong 3 điều kiện: giá trị đơn hàng trước thuế (V), tỷ suất lợi nhuận tổng (M), '
        'tỷ suất LN dòng hàng tạm thấp nhất.',
        '– Mỗi cấp so theo Từ ≤ giá trị < Đến (riêng giá trị đơn hàng: Từ < V ≤ Đến); không khớp cấp nào → Cấp 3.',
        '– Báo giá không có hàng tạm → bỏ qua điều kiện hàng tạm. Dòng hàng tạm chưa có giá vốn tính là 0%.',
    ], ['Duyệt giá báo giá', 'Cấu hình duyệt giá']),
    ('BR-03', 'Ngưỡng các cấp nối tiếp nhau', [
        '– Giá trị đơn hàng: Cấp 1 bắt đầu từ 0, Cấp 3 không giới hạn trên; “Từ” cấp sau tự bằng “Đến” cấp trước; '
        '“Đến” phải tăng dần theo cấp.',
        '– Tỷ suất: Cấp 1 không giới hạn trên, Cấp 3 không giới hạn dưới (kể cả âm); “Đến” cấp sau tự bằng “Từ” '
        'cấp trước; “Từ” phải giảm dần theo cấp.',
        '– Cột Mô tả do hệ thống tự sinh khi lưu.',
    ], ['Duyệt theo giá trị đơn hàng', 'Duyệt theo tỷ suất', 'Duyệt theo hàng tạm']),
    ('BR-04', 'Tỷ suất lợi nhuận mức sàn', [
        '– Giá trị 0–100%. Báo giá có tỷ suất dưới mức sàn hiện cảnh báo đỏ. Lưu được bằng quyền Q1 hoặc Q2.',
    ], 'Cấu hình tỷ suất LN mức sàn'),
    ('BR-05', 'Chỉ ghi lịch sử khi giá trị thực sự đổi', [
        '– Mỗi cấp chỉ ghi 1 dòng lịch sử khi giá trị Từ / Đến / Mô tả thay đổi; lưu mà không đổi thì không phát sinh.',
        '– Lịch sử cấu hình duyệt giá là chung toàn hệ thống; thay đổi mức sàn ghi ở lịch sử Quy định chung.',
    ], 'Lịch sử thay đổi'),
])

d.save()
