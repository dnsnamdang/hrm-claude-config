# -*- coding: utf-8 -*-
"""Sinh "SRS - Cấu hình phân hệ giao việc - Quản lý dự án.docx" theo FORM CHUẨN (2026-09-24).

Chạy:  python3 .plans/gop-db/cau-hinh-giao-viec-docs/gen_srs_quan_ly_du_an.py
Nguồn đối chiếu code (nhánh gop_db):
  FE  pages/assign/settings/index.vue (tab "Quản lý dự án": 3 tab con) · components/modal/SettingHistoryModal.vue
      components/menu-sidebar.js (nhóm Thiết lập)
  BE  Modules/Assign/Routes/api.php (priority-levels, my-job/deadline-config, project-close-configs)
      PriorityLevelStoreRequest · ProjectCloseConfigUpdateRequest · Entities/PriorityLevel
      Services/{PriorityLevelService, MyJobService, ProjectCloseConfigService}
      app/Services/SettingHistory/Adapters/{PriorityLevel,DeadlineConfig,ProjectCloseConfig}Adapter
  Quyền: PermissionsTableSeeder id 211 "Cấu hình phân hệ giao việc/ công tác"
"""
from _common import new_doc, shot, MENU_A, A_CH, NO_PERM

TEN_MAN = 'Cấu hình phân hệ giao việc - Quản lý dự án'
d = new_doc(TEN_MAN, MENU_A, '/assign/settings', 'chqlda_')

# ========================================================= PHAN 1
d.h1('Phần 1. Giới thiệu')
d.h2('1 Mục đích')
d.p('Tài liệu này đặc tả yêu cầu phần mềm cho tab “Quản lý dự án” của màn Cấu hình phân hệ giao việc, nhằm:')
d.bullets([
    'Là căn cứ nghiệm thu chức năng và phân quyền của 3 tab con: Cấu hình mức độ ưu tiên, Cấu hình hạn, '
    'Đóng dự án tự động.',
    'Làm rõ các tham số đang điều khiển hành vi tự động của hệ thống: mức độ ưu tiên làm giải pháp, '
    'mốc cảnh báo sắp tới hạn, hạn biên bản meeting, cơ chế tự đóng dự án và phân cấp duyệt gia hạn dự án.',
    'Làm rõ phạm vi áp dụng của từng nhóm cấu hình: theo công ty đang làm việc hay dùng chung toàn hệ thống.',
])

d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('Mức độ ưu tiên', 'Mức ưu tiên làm giải pháp (Khẩn cấp, Cao, Trung bình, Thấp…) kèm thời gian phản '
     'hồi và màu hiển thị. Được gán cho giai đoạn dự án.'),
    ('Công ty đang làm việc', 'Công ty người dùng đang chọn ở góc trên bên phải màn hình. Các cấu hình '
     '“theo công ty” chỉ đọc/ghi dữ liệu của công ty này.'),
    ('Hạn đóng dự án', 'Ngày mà sau đó dự án TKT bị hệ thống tự chuyển sang đóng nếu không được gia hạn.'),
    ('Báo giá được duyệt', 'Báo giá của dự án đã qua đủ cấp duyệt giá.'),
    ('Thời gian ân hạn', 'Số ngày dự án đã quá hạn đóng vẫn được để mở trước khi hệ thống tự đóng.'),
], widths=[1.8, 4.2])

# ========================================================= PHAN 2
d.h1('Phần 2. Phân quyền')
d.h2('1 Danh sách quyền')
d.p('Nhóm quyền thao tác:')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('Q1', 'Cấu hình phân hệ giao việc/ công tác',
     'Hiển thị menu “Cấu hình chung (Quy chế thu nhập kỹ thuật - công nghệ)” của phân hệ Công việc; được xem, '
     'thêm, sửa, xóa, đổi thứ tự, lưu mọi cấu hình của tab Quản lý dự án và xem lịch sử thay đổi.'),
], widths=[0.8, 2.0, 3.2])
d.p('Màn cấu hình không phân quyền theo cấp dữ liệu (công ty/phòng ban/bộ phận). Phạm vi dữ liệu do '
    'loại cấu hình quyết định — xem quy tắc BR-01.')

d.h2('2 Ma trận phân quyền')
d.table(['Chức năng', 'Q1', 'Không có quyền nào'], [
    ('FR-01 Xem cấu hình mức độ ưu tiên', '✅', '❌'),
    ('FR-02 Thêm mức độ ưu tiên', '✅', '❌'),
    ('FR-03 Sửa mức độ ưu tiên', '✅', '❌'),
    ('FR-04 Xóa mức độ ưu tiên', '✅', '❌'),
    ('FR-05 Đổi thứ tự mức độ ưu tiên', '✅', '❌'),
    ('FR-06 Cấu hình hạn', '✅', '❌'),
    ('FR-07 Cấu hình đóng dự án tự động', '✅', '❌'),
    ('FR-08 Xem lịch sử thay đổi', '✅', '❌'),
], widths=[3.6, 1.0, 1.4])

# ========================================================= PHAN 3
d.h1('Phần 3. Đặc tả chi tiết theo từng chức năng')
d.h2('1 Sơ đồ UML tổng quan')
d.overview_figure2(
    [(A_CH, [0, 1, 2, 3, 4, 5, 6])],
    [('FR-01', 'Xem cấu hình mức độ ưu tiên', 'view'),
     ('FR-02', 'Thêm mức độ ưu tiên', 'crud'),
     ('FR-03', 'Sửa mức độ ưu tiên', 'crud'),
     ('FR-04', 'Xóa mức độ ưu tiên', 'action'),
     ('FR-05', 'Đổi thứ tự mức độ ưu tiên', 'action'),
     ('FR-06', 'Cấu hình hạn', 'crud'),
     ('FR-07', 'Cấu hình đóng dự án tự động', 'crud')],
    [('FR-08', 'Xem lịch sử thay đổi', 'view', 'extend', [0], None)],
    'Sơ đồ Use Case tổng quan màn %s' % TEN_MAN)

d.h2('2 Đặc tả chi tiết từng chức năng')

# ------------------------------------------------------------------ 2.1
d.h3('2.1 Xem cấu hình mức độ ưu tiên')
d.p('2.1.1 Giới thiệu')
d.rule_ref('- Màn Danh sách và UI/UX. Chỉ bổ sung các quy tắc riêng của tab Cấu hình mức độ ưu tiên '
           'tại phần mô tả chi tiết.', anchor='list')
d.intro_table(
    ten='Xem cấu hình mức độ ưu tiên làm giải pháp',
    mota='Hiển thị bảng các mức độ ưu tiên của công ty đang làm việc theo thứ tự STT, ở chế độ chỉ xem.',
    tacnhan='Người quản trị cấu hình; Người dùng đã đăng nhập',
    dieukien='Người dùng có quyền Q1.',
    chinh='1. Người dùng mở màn Cấu hình phân hệ giao việc, chọn tab “Quản lý dự án”.\n'
          '2. Hệ thống mở sẵn tab con “Cấu hình mức độ ưu tiên”.\n'
          '3. Hệ thống nạp các mức độ ưu tiên của công ty đang làm việc, sắp theo STT.\n'
          '4. Bảng hiển thị từng dòng ở chế độ chỉ xem; chân bảng hiện tổng số dòng.',
    phu='• Công ty chưa có mức độ ưu tiên nào → bảng hiện “Không có dữ liệu.”.\n'
        '• Bảng rộng hơn khung → xuất hiện thanh cuộn ngang để xem cột Mã màu và Hành động.')
d.p('2.1.2 Layout màn hình')
d.layout(menu=MENU_A + ' => Cấu hình mức độ ưu tiên', shot=shot('01-uu-tien.png'),
         shot_caption='Tab Cấu hình mức độ ưu tiên lúc mới mở')
d.p('2.1.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề trang', 'Label', 'Hiển thị', '–', 'Cấu hình phân hệ giao việc', 'Tiêu đề trên thanh đầu trang.'),
    ('Tab “Quản lý dự án”', 'Tab', 'Enable', '–', 'Hiển thị',
     'Tab cấp 1 cạnh “Thông tin chung”, “Giới hạn khoảng cách tính công tác phí”.'),
    ('Tab con “Cấu hình mức độ ưu tiên” / “Cấu hình hạn” / “Đóng dự án tự động”', 'Tab', 'Enable', '–',
     'Mở sẵn “Cấu hình mức độ ưu tiên”', 'Chuyển giữa 3 nhóm cấu hình.'),
    ('Nhãn “Mức độ ưu tiên làm giải pháp”', 'Label', 'Hiển thị', '–', 'Hiển thị',
     'Kèm dòng hướng dẫn “Kéo thả bằng icon để đổi STT. Mặc định chỉ xem, bấm Sửa để sửa từng dòng.”'),
    ('Nút Lịch sử thay đổi', 'Button', 'Enable', '–', 'Hiển thị', 'Mở popup lịch sử (FR-08).'),
    ('Nút Thêm dòng', 'Button', 'Enable', '–', 'Hiển thị', 'Thêm dòng mới cuối bảng (FR-02).'),
    ('Cột STT', 'Table/Grid', 'Read-only', '–', 'Theo thứ tự', 'Icon kéo thả + số thứ tự 1, 2, 3…'),
    ('Cột Tên mức độ ưu tiên', 'Textbox', 'Read-only', '0–20 ký tự', 'Theo dữ liệu',
     'Kèm bộ đếm ký tự “n/20” bên dưới.'),
    ('Cột Số ngày phản hồi', 'Number', 'Read-only', '≥ 0', 'Theo dữ liệu', '–'),
    ('Cột Số giờ phản hồi', 'Number', 'Read-only', '0 – 23', 'Theo dữ liệu', '–'),
    ('Cột Mã màu', 'Text', 'Read-only', '#RRGGBB', 'Theo dữ liệu',
     'Ô màu xem trước + ô chọn màu + ô mã màu.'),
    ('Cột Hành động', 'Button', 'Enable', '–', 'Sửa, Xóa', 'Nút Sửa (FR-03) và nút Xóa (FR-04).'),
    ('Chân bảng', 'Label', 'Hiển thị', '–', '“n dòng”', 'Tổng số mức độ ưu tiên đang có.'),
    ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn', '“Không có dữ liệu.” khi chưa có dòng nào.'),
], required=False)
d.p('2.1.4 Danh sách event và xử lý event')
d.event_table([
    ('Mở tab Quản lý dự án', 'System',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     'During:\n– Nạp mức độ ưu tiên, cấu hình hạn, cấu hình đóng dự án của công ty đang làm việc.\n'
     'After:\n– Hiển thị bảng mức độ ưu tiên ở chế độ chỉ xem, các ô nhập bị khóa.'),
    ('Đổi công ty đang làm việc', 'Change',
     'After:\n– Nạp lại dữ liệu theo công ty mới.'),
])

# ------------------------------------------------------------------ 2.2
d.h3('2.2 Thêm mức độ ưu tiên')
d.p('2.2.1 Biểu đồ Usecase')
d.uc_figure('FR-02', 'Thêm mức độ ưu tiên', 'crud', actor=A_CH)
d.p('2.2.2 Giới thiệu')
d.rule_ref('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX. Logic ghi lịch sử áp dụng theo SRS '
           'Các quy tắc chung - Quy tắc ghi lịch sử.', anchor='create')
d.intro_table(
    ten='Thêm mức độ ưu tiên',
    mota='Thêm một mức độ ưu tiên mới cho công ty đang làm việc, nhập trực tiếp trên dòng mới của bảng.',
    tacnhan='Người quản trị cấu hình',
    dieukien='Người dùng có quyền Q1 và đang ở tab Cấu hình mức độ ưu tiên.',
    chinh='1. Người dùng bấm “Thêm dòng”.\n'
          '2. Hệ thống thêm 1 dòng cuối bảng ở chế độ nhập, điền sẵn giá trị mặc định, hiện “Chưa lưu”.\n'
          '3. Người dùng nhập Tên, Số ngày phản hồi, Số giờ phản hồi, chọn Mã màu.\n'
          '4. Người dùng bấm “Lưu” trên dòng.\n'
          '5. Hệ thống kiểm tra dữ liệu, ghi mức độ ưu tiên với STT bằng vị trí dòng.\n'
          '6. Hệ thống báo “Thêm mới thành công!” và nạp lại bảng ở chế độ chỉ xem.',
    phu='• Dữ liệu không hợp lệ → báo lỗi đỏ dưới từng ô, hiện thông báo “Chưa hợp lệ – Sửa các trường '
        'đang báo lỗi rồi lưu lại.”, không lưu.\n'
        '• Tên đã có trong công ty → báo “Đã tồn tại trên hệ thống” dưới ô Tên.\n'
        '• Bấm Xóa trên dòng chưa lưu → hỏi xác nhận rồi bỏ dòng khỏi bảng, không ghi dữ liệu.',
    dacbiet='Tên mức độ ưu tiên chỉ cần duy nhất trong cùng công ty; công ty khác được đặt trùng tên.')
d.p('2.2.3 Layout màn hình')
d.layout(menu=MENU_A + ' => Cấu hình mức độ ưu tiên => Thêm dòng', shot=shot('02-them-dong.png'),
         shot_caption='Dòng mới sau khi bấm Thêm dòng (cuộn bảng sang phải)')
d.p('2.2.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tên mức độ ưu tiên', 'Textbox', 'Enable', '1–20 ký tự', 'Có', 'Trống',
     'Gợi ý “VD: Khẩn cấp”; không gõ quá 20 ký tự; bộ đếm “n/20”.'),
    ('Số ngày phản hồi', 'Number', 'Enable', '≥ 0', 'Có', '0', 'Gợi ý “VD: 2”.'),
    ('Số giờ phản hồi', 'Number', 'Enable', '0 – 23', 'Không', '0', 'Bỏ trống được lưu là 0.'),
    ('Ô chọn màu', 'Color picker', 'Enable', '–', 'Có', '#16a34a', 'Chọn màu thì ô Mã màu cập nhật theo.'),
    ('Ô Mã màu', 'Textbox', 'Enable', '#RRGGBB', 'Có', '#16a34a', 'Gõ tay mã màu 6 ký tự hexa.'),
    ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Chỉ hiện trên dòng mới.'),
    ('Nút Xóa', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', 'Bỏ dòng chưa lưu (có hỏi xác nhận).'),
    ('Nhãn “Chưa lưu”', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', 'Nhắc dòng còn thay đổi chưa lưu.'),
    ('Thông báo lỗi dưới ô', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', 'Chữ đỏ dưới ô bị lỗi.'),
])
d.p('2.2.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Thêm dòng', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     'After:\n– Thêm dòng cuối bảng: Tên trống, Số ngày 0, Số giờ 0, Mã màu #16a34a.\n'
     '– Hiển thị thông báo “Thêm dòng thành công” (dòng chưa được lưu).'),
    ('Bấm Lưu trên dòng mới', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     'During:\n– Tên trống → “Bắt buộc.”; Tên quá 20 ký tự → “Tối đa 20 ký tự.”\n'
     '– Số ngày phản hồi trống → “Bắt buộc.”; nhỏ hơn 0 → “Phải >= 0.”\n'
     '– Số giờ phản hồi nhỏ hơn 0 → “Phải >= 0.”; lớn hơn 23 → “Tối đa 23.”\n'
     '– Mã màu trống → “Bắt buộc.”; sai định dạng → “Sai định dạng (#RRGGBB).”\n'
     '– Tên trùng trong công ty → “Đã tồn tại trên hệ thống”.\n'
     '– Nếu có lỗi validate → hiện thông báo “Chưa hợp lệ”, không thực hiện bước After.\n'
     'After:\n– Bỏ khoảng trắng đầu/cuối của Tên và Mã màu, ghi mức độ ưu tiên cho công ty đang làm việc.\n'
     '– Ghi lịch sử “Thêm mức độ ưu tiên”.\n'
     '– Hiển thị “Thêm mới thành công!” và nạp lại bảng.'),
])

# ------------------------------------------------------------------ 2.3
d.h3('2.3 Sửa mức độ ưu tiên')
d.p('2.3.1 Biểu đồ Usecase')
d.uc_figure('FR-03', 'Sửa mức độ ưu tiên', 'crud', actor=A_CH)
d.p('2.3.2 Giới thiệu')
d.rule_ref('- Màn Chỉnh sửa, Validate dữ liệu, Thông báo và UI/UX. Logic ghi lịch sử áp dụng theo SRS '
           'Các quy tắc chung - Quy tắc ghi lịch sử.', anchor='create')
d.intro_table(
    ten='Sửa mức độ ưu tiên',
    mota='Sửa trực tiếp trên từng dòng của bảng: bấm Sửa để mở khóa dòng, nhập lại rồi Lưu hoặc Huỷ.',
    tacnhan='Người quản trị cấu hình',
    dieukien='Người dùng có quyền Q1; dòng đang ở chế độ chỉ xem.',
    chinh='1. Người dùng bấm “Sửa” trên dòng cần sửa.\n'
          '2. Hệ thống mở khóa các ô của dòng đó, nút đổi thành “Lưu” và “Huỷ”.\n'
          '3. Người dùng sửa thông tin và bấm “Lưu”.\n'
          '4. Hệ thống kiểm tra dữ liệu và cập nhật.\n'
          '5. Hệ thống báo “Cập nhật thành công!” và nạp lại bảng.',
    phu='• Bấm “Huỷ” → trả các ô về giá trị trước khi sửa, dòng về chế độ chỉ xem.\n'
        '• Dữ liệu không hợp lệ / tên trùng → báo lỗi như chức năng Thêm, không lưu.',
    dacbiet='Có thể mở nhiều dòng ở chế độ sửa cùng lúc; mỗi dòng lưu độc lập.')
d.p('2.3.3 Layout màn hình')
d.layout(menu=MENU_A + ' => Cấu hình mức độ ưu tiên => Sửa', shot=shot('03-sua.png'),
         shot_caption='Dòng “Khẩn cấp” đang ở chế độ sửa')
d.p('2.3.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tên mức độ ưu tiên', 'Textbox', 'Enable', '1–20 ký tự', 'Có', 'Theo dữ liệu', 'Như chức năng Thêm.'),
    ('Số ngày phản hồi', 'Number', 'Enable', '≥ 0', 'Có', 'Theo dữ liệu', '–'),
    ('Số giờ phản hồi', 'Number', 'Enable', '0 – 23', 'Không', 'Theo dữ liệu', '–'),
    ('Ô chọn màu / Ô Mã màu', 'Color picker / Textbox', 'Enable', '#RRGGBB', 'Có', 'Theo dữ liệu', '–'),
    ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Hiện khi dòng ở chế độ sửa.'),
    ('Nút Huỷ', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Hiện khi dòng ở chế độ sửa.'),
    ('Nút Xóa', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', 'Vẫn hiện khi đang sửa (FR-04).'),
    ('Nhãn “Chưa lưu”', 'Label', 'Hiển thị', '–', '–', 'Ẩn', 'Hiện khi đã thay đổi ô mà chưa lưu.'),
])
d.p('2.3.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Sửa', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     'After:\n– Ghi nhớ giá trị hiện tại của dòng, mở khóa các ô, hiện nút Lưu và Huỷ.'),
    ('Bấm Huỷ', 'Click', 'After:\n– Trả các ô về giá trị đã ghi nhớ, dòng về chế độ chỉ xem, xóa lỗi.'),
    ('Bấm Lưu', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     'During:\n– Kiểm tra như chức năng Thêm (Bắt buộc / Tối đa 20 ký tự / Phải >= 0 / Tối đa 23 / '
     'Sai định dạng (#RRGGBB) / Đã tồn tại trên hệ thống).\n'
     '– Mức độ ưu tiên không thuộc công ty đang làm việc → “Không tìm thấy dữ liệu”.\n'
     '– Nếu có lỗi validate → không thực hiện bước After.\n'
     'After:\n– Cập nhật mức độ ưu tiên.\n– Ghi lịch sử “Cập nhật mức độ ưu tiên” (giá trị cũ → mới).\n'
     '– Hiển thị “Cập nhật thành công!” và nạp lại bảng.'),
])

# ------------------------------------------------------------------ 2.4
d.h3('2.4 Xóa mức độ ưu tiên')
d.p('2.4.1 Biểu đồ Usecase')
d.uc_figure('FR-04', 'Xóa mức độ ưu tiên', 'action', actor=A_CH)
d.p('2.4.2 Giới thiệu')
d.rule_ref('- Quy tắc Xóa và Thông báo. Logic ghi lịch sử áp dụng theo SRS Các quy tắc chung - Quy tắc '
           'ghi lịch sử.', anchor='delete')
d.intro_table(
    ten='Xóa mức độ ưu tiên',
    mota='Xóa hẳn một mức độ ưu tiên chưa được giai đoạn dự án nào sử dụng.',
    tacnhan='Người quản trị cấu hình',
    dieukien='Người dùng có quyền Q1.',
    chinh='1. Người dùng bấm nút Xóa (biểu tượng thùng rác) trên dòng.\n'
          '2. Hệ thống hiện hộp “Xác nhận xóa”: “Bạn có chắc muốn xóa mức độ ưu tiên ‘<Tên>’?”.\n'
          '3. Người dùng bấm “Xóa”.\n'
          '4. Hệ thống xóa mức độ ưu tiên, đánh lại STT các dòng còn lại.\n'
          '5. Hệ thống báo “Xóa mức độ ưu tiên thành công!”.',
    phu='• Bấm “Hủy” → đóng hộp, không xóa.\n'
        '• Mức độ ưu tiên đang được gán cho giai đoạn dự án → báo “Dữ liệu đang được sử dụng, vui lòng tải lại”, '
        'không xóa.\n'
        '• Dòng chưa lưu → chỉ bỏ khỏi bảng, không ghi dữ liệu.',
    dacbiet='Xóa là xóa hẳn khỏi hệ thống (không xóa mềm).')
d.p('2.4.3 Layout màn hình')
d.layout(menu=MENU_A + ' => Cấu hình mức độ ưu tiên => Xóa', shot=shot('04-xoa.png'),
         shot_caption='Hộp xác nhận xóa mức độ ưu tiên')
d.p('2.4.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề hộp', 'Label', 'Hiển thị', 'Xác nhận xóa', 'Biểu tượng cảnh báo đỏ.'),
    ('Nội dung', 'Label', 'Hiển thị', 'Theo dòng', '“Bạn có chắc muốn xóa mức độ ưu tiên ‘<Tên>’?”'),
    ('Nút Xóa', 'Button', 'Enable', 'Hiển thị', 'Màu đỏ, xác nhận xóa.'),
    ('Nút Hủy', 'Button', 'Enable', 'Hiển thị', 'Đóng hộp, không xóa.'),
], required=False, scope=False)
d.p('2.4.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Xóa trên dòng', 'Click', 'After:\n– Mở hộp Xác nhận xóa.'),
    ('Bấm Xóa trong hộp xác nhận', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     'During:\n– Mức độ ưu tiên không thuộc công ty đang làm việc → “Không tìm thấy dữ liệu”.\n'
     '– Đang được giai đoạn dự án sử dụng → “Dữ liệu đang được sử dụng, vui lòng tải lại”, dừng xử lý.\n'
     'After:\n– Xóa mức độ ưu tiên; ghi lịch sử “Xóa mức độ ưu tiên”.\n'
     '– Đánh lại STT các dòng còn lại theo thứ tự trên bảng.\n'
     '– Hiển thị “Xóa mức độ ưu tiên thành công!”.'),
    ('Bấm Hủy', 'Click', 'After:\n– Đóng hộp, giữ nguyên dữ liệu.'),
])

# ------------------------------------------------------------------ 2.5
d.h3('2.5 Đổi thứ tự mức độ ưu tiên')
d.p('2.5.1 Biểu đồ Usecase')
d.uc_figure('FR-05', 'Đổi thứ tự mức độ ưu tiên', 'action', actor=A_CH)
d.p('2.5.2 Giới thiệu')
d.rule_ref('- Thông báo và UI/UX. Logic ghi lịch sử áp dụng theo SRS Các quy tắc chung - Quy tắc ghi '
           'lịch sử.', anchor='history')
d.intro_table(
    ten='Đổi thứ tự (STT) mức độ ưu tiên bằng kéo thả',
    mota='Kéo biểu tượng ở cột STT để đổi vị trí dòng; hệ thống lưu ngay thứ tự mới.',
    tacnhan='Người quản trị cấu hình',
    dieukien='Người dùng có quyền Q1; bảng có từ 2 dòng.',
    chinh='1. Người dùng giữ biểu tượng kéo thả ở cột STT của một dòng.\n'
          '2. Người dùng kéo tới vị trí mới rồi thả.\n'
          '3. Hệ thống đánh lại STT 1, 2, 3… theo thứ tự mới và lưu ngay.\n'
          '4. Hệ thống hiện thông báo “Đã đổi STT – Thứ tự đã được cập nhật.”',
    phu='• Dòng chưa lưu được đổi chỗ trên giao diện nhưng chỉ dòng đã lưu mới được ghi thứ tự.\n'
        '• Thứ tự không đổi so với trước → không ghi lịch sử.',
    dacbiet='Không cần bấm Lưu; thả chuột là lưu.')
d.p('2.5.3 Layout màn hình')
d.layout(menu=MENU_A + ' => Cấu hình mức độ ưu tiên', shot=shot('01-uu-tien.png'),
         shot_caption='Biểu tượng kéo thả ở cột STT')
d.p('2.5.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Biểu tượng kéo thả', 'Icon Button', 'Enable', '–', '–', 'Hiển thị',
     'Rê chuột hiện “Giữ và kéo để đổi STT”.'),
    ('Số STT', 'Label', 'Read-only', '1 – n', '–', 'Theo vị trí', 'Tự đánh lại sau khi thả.'),
    ('Thông báo góc màn hình', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
     '“Đã đổi STT – Thứ tự đã được cập nhật.”, tự ẩn sau khoảng 2 giây.'),
])
d.p('2.5.5 Danh sách event và xử lý event')
d.event_table([
    ('Thả dòng ở vị trí mới', 'Drag & drop',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     'During:\n– Chỉ đánh lại thứ tự các mức của công ty đang làm việc; mức không thuộc công ty → từ chối.\n'
     'After:\n– Lưu STT mới cho các dòng đã lưu.\n– Nếu thứ tự thay đổi → ghi lịch sử “Đổi thứ tự ưu tiên”.\n'
     '– Hiện thông báo “Đã đổi STT”.'),
])

# ------------------------------------------------------------------ 2.6
d.h3('2.6 Cấu hình hạn')
d.p('2.6.1 Biểu đồ Usecase')
d.uc_figure('FR-06', 'Cấu hình hạn', 'crud', actor=A_CH)
d.p('2.6.2 Giới thiệu')
d.rule_ref('- Validate dữ liệu, Thông báo và UI/UX. Logic ghi lịch sử áp dụng theo SRS Các quy tắc chung '
           '- Quy tắc ghi lịch sử.', anchor='create')
d.intro_table(
    ten='Cấu hình hạn',
    mota='Khai các mốc thời gian để hệ thống cảnh báo sắp tới hạn (nhiệm vụ, Issue, meeting, giải pháp), '
         'hạn nhập biên bản meeting, cảnh báo trước khi đóng nhu cầu và ngưỡng “nhiều nhiệm vụ trễ”. '
         'Áp dụng cho công ty đang làm việc.',
    tacnhan='Người quản trị cấu hình',
    dieukien='Người dùng có quyền Q1.',
    chinh='1. Người dùng chọn tab con “Cấu hình hạn”.\n'
          '2. Hệ thống hiển thị 9 tham số với giá trị đang lưu của công ty (chưa có thì giá trị mặc định).\n'
          '3. Người dùng sửa các tham số và bấm “Lưu cấu hình”.\n'
          '4. Hệ thống kiểm tra, lưu và báo “Cập nhật thành công!”.',
    phu='• Ô “Cảnh báo trước khi đóng nhu cầu” trống / âm / số lẻ / lớn hơn 365 → báo lỗi đỏ dưới ô, '
        'thông báo “Bạn chưa nhập đầy đủ thông tin”, không lưu.\n'
        '• Lỗi khi lưu → “Có lỗi xảy ra khi cập nhật cấu hình!”.\n'
        '• Không tải được cấu hình → “Không thể tải cấu hình hạn!”.',
    dacbiet='“Hạn nhập biên bản meeting sau” và “Cảnh báo trước khi tự hủy meeting” để trống hoặc ≤ 0 '
            'thì hệ thống lưu về mặc định 1 ngày / 3 giờ (0 nghĩa là hủy cuộc họp ngay khi họp xong).')
d.p('2.6.3 Layout màn hình')
d.layout(menu=MENU_A + ' => Cấu hình hạn', shot=shot('06-cau-hinh-han.png'),
         shot_caption='Tab Cấu hình hạn')
d.p('2.6.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Cảnh báo sớm nhiệm vụ trước', 'Number', 'Enable', '≥ 0 (ngày)', 'Không', '0',
     'Nhiệm vụ còn ≤ số ngày này thì gửi thông báo và đưa vào danh sách “Sắp tới hạn”.'),
    ('Cảnh báo sớm Issue trước', 'Number', 'Enable', '≥ 0 (ngày)', 'Không', '0', 'Tương tự cho Issue.'),
    ('Meeting sắp tới lịch trước', 'Number', 'Enable', '≥ 0 (ngày)', 'Không', '0',
     'Mốc meeting sắp tới lịch.'),
    ('Hạn nhập biên bản meeting sau', 'Number', 'Enable', '≥ 1 (ngày)', 'Không', '1',
     'Số ngày sau khi họp xong để người tạo cập nhật biên bản và Hoàn thành; quá hạn hệ thống tự hủy cuộc họp.'),
    ('Cảnh báo trước khi tự hủy meeting', 'Number', 'Enable', '≥ 1 (giờ)', 'Không', '3',
     'Gửi nhắc người tạo meeting trước thời điểm tự hủy bao nhiêu giờ.'),
    ('Cảnh báo trước khi đóng nhu cầu', 'Number', 'Enable', '0 – 365 (ngày, số nguyên)', 'Có', '3',
     'Gửi nhắc trước khi nhu cầu khách hàng bị tự đóng. Để 0 nếu không muốn cảnh báo.'),
    ('Giải pháp sắp tới hạn trước', 'Number', 'Enable', '≥ 0 (ngày)', 'Không', '0', 'Mốc giải pháp sắp tới hạn.'),
    ('Hạng mục nhiều nhiệm vụ trễ khi có từ', 'Number', 'Enable', '≥ 0 (nhiệm vụ trễ)', 'Không', '0',
     'Ngưỡng đánh dấu hạng mục có nhiều nhiệm vụ trễ.'),
    ('Nhân sự nhiều nhiệm vụ trễ khi có từ', 'Number', 'Enable', '≥ 0 (nhiệm vụ trễ)', 'Không', '0',
     'Ngưỡng đánh dấu nhân sự có nhiều nhiệm vụ trễ.'),
    ('Nút Lịch sử thay đổi', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Mở popup lịch sử (FR-08).'),
    ('Nút Lưu cấu hình', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Lưu toàn bộ 9 tham số.'),
    ('Thông báo lỗi dưới ô', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
     'Chỉ áp cho ô Cảnh báo trước khi đóng nhu cầu.'),
])
d.p('2.6.5 Danh sách event và xử lý event')
d.event_table([
    ('Nhập ô Cảnh báo trước khi đóng nhu cầu', 'Change / Blur',
     'During:\n– Trống → “Bắt buộc phải nhập”.\n– Âm hoặc số lẻ → “Bắt buộc nhập, kiểu số nguyên dương >= 0”.\n'
     '– Lớn hơn 365 → “Giá trị nhập vào không được vượt quá 365.”'),
    ('Bấm Lưu cấu hình', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     'During:\n– Kiểm tra ô Cảnh báo trước khi đóng nhu cầu; lỗi → “Bạn chưa nhập đầy đủ thông tin”, dừng.\n'
     'After:\n– Lưu 9 tham số cho công ty đang làm việc (chưa có bản ghi thì tạo mới).\n'
     '– Hạn nhập biên bản / Cảnh báo trước khi tự hủy meeting trống hoặc ≤ 0 → lưu mặc định 1 ngày / 3 giờ.\n'
     '– Ghi lịch sử “Cập nhật cấu hình hạn” cho các tham số thực sự đổi.\n'
     '– Hiển thị “Cập nhật thành công!” và hiển thị lại giá trị đã lưu.'),
])

# ------------------------------------------------------------------ 2.7
d.h3('2.7 Cấu hình đóng dự án tự động')
d.p('2.7.1 Biểu đồ Usecase')
d.uc_figure('FR-07', 'Cấu hình đóng dự án tự động', 'crud', actor=A_CH)
d.p('2.7.2 Giới thiệu')
d.rule_ref('- Validate dữ liệu, Thông báo và UI/UX. Logic ghi lịch sử áp dụng theo SRS Các quy tắc chung '
           '- Quy tắc ghi lịch sử.', anchor='create')
d.intro_table(
    ten='Cấu hình đóng dự án tự động',
    mota='Khai thời hạn đóng dự án TKT khi chưa có báo giá, thời hạn theo từng giai đoạn khi đã có báo '
         'giá được duyệt, số ngày nhắc trước hạn, thời gian ân hạn và ngưỡng Trưởng phòng được duyệt gia hạn.',
    tacnhan='Người quản trị cấu hình',
    dieukien='Người dùng có quyền Q1.',
    chinh='1. Người dùng chọn tab con “Đóng dự án tự động”.\n'
          '2. Hệ thống nạp lại cấu hình mới nhất mỗi lần mở tab: 4 tham số chung và bảng Thời hạn theo giai đoạn.\n'
          '3. Người dùng sửa các ô và bấm “Lưu cấu hình”.\n'
          '4. Hệ thống kiểm tra, lưu và báo “Đã lưu cấu hình đóng dự án tự động”.',
    phu='• Ô không hợp lệ → báo lỗi đỏ ngay dưới ô, thông báo “Vui lòng kiểm tra lại các ô được báo đỏ”, không lưu.\n'
        '• Lỗi khác khi lưu → hiển thị nội dung lỗi hoặc “Lưu cấu hình thất bại”.\n'
        '• Rê chuột vào biểu tượng ⓘ cạnh từng tham số → hiện giải thích cách tính.',
    dacbiet='4 tham số chung áp dụng cho công ty đang làm việc; bảng Thời hạn theo giai đoạn dùng chung '
            'cho mọi công ty. Thay đổi áp dụng cả cho dự án đang chạy.')
d.p('2.7.3 Layout màn hình')
d.layout(menu=MENU_A + ' => Đóng dự án tự động', shot=shot('07-dong-du-an.png'),
         shot_caption='Tab Đóng dự án tự động')
d.p('2.7.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Hạn đóng khi dự án chưa có báo giá', 'Number', 'Enable', '0 – 120 (tháng)', 'Có', '3',
     'Hạn đóng = ngày tạo dự án + số tháng này; chỉ áp khi dự án chưa có báo giá nào được duyệt.'),
    ('Nhắc trước hạn đóng', 'Number', 'Enable', '0 – 365 (ngày)', 'Có', '7',
     'Trước hạn bao nhiêu ngày thì nhắc nhân viên kinh doanh chính của dự án; 0 = không nhắc.'),
    ('Quá hạn bao lâu thì tự đóng', 'Number', 'Enable', '0 – 365 (ngày)', 'Có', '0',
     'Thời gian ân hạn sau hạn đóng; 0 = đóng ở lần chạy tự động kế tiếp (01:30 hằng ngày).'),
    ('Trưởng phòng được duyệt gia hạn tối đa', 'Number', 'Enable', '0 – 3650 (ngày)', 'Có', '30',
     'Ngưỡng phân cấp duyệt đề xuất gia hạn.'),
    ('Biểu tượng ⓘ', 'Icon', 'Hiển thị', '–', '–', 'Hiển thị', 'Rê chuột hiện giải thích của từng tham số.'),
    ('Bảng Thời hạn theo giai đoạn', 'Table/Grid', 'Enable', '–', '–', 'Mọi giai đoạn dự án',
     'Cột STT, Giai đoạn dự án (chỉ đọc), Thời hạn (tháng). Giai đoạn sắp theo tên (số thứ tự đầu tên '
     'được so như số).'),
    ('Thời hạn (tháng) của giai đoạn', 'Number', 'Enable', '0 – 120 hoặc trống', 'Không', 'Theo dữ liệu',
     'Gợi ý “Không tự đóng”; bỏ trống = giai đoạn đó không bao giờ tự đóng.'),
    ('Nút Lịch sử thay đổi', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Mở popup lịch sử (FR-08).'),
    ('Nút Lưu cấu hình', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
     'Trong lúc lưu đổi chữ thành “Đang lưu...” và không bấm lại được.'),
    ('Thông báo lỗi dưới ô', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', 'Chữ đỏ dưới ô bị lỗi.'),
])
d.p('2.7.5 Danh sách event và xử lý event')
d.event_table([
    ('Mở tab Đóng dự án tự động', 'Click',
     'After:\n– Nạp lại cấu hình mới nhất (tránh ghi đè giá trị người khác vừa sửa).\n'
     '– Giai đoạn dự án mới thêm chưa có cấu hình → hiện dòng trống (không tự đóng).'),
    ('Bấm Lưu cấu hình', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     'During:\n– 4 tham số chung trống → “Bắt buộc phải nhập”.\n'
     '– Không phải số nguyên → “Phải là số nguyên”; âm → “Không được nhỏ hơn 0”.\n'
     '– Vượt trần → “Không được lớn hơn <trần>” (120 tháng / 365 ngày / 365 ngày / 3650 ngày; '
     'giai đoạn: 120 tháng).\n'
     '– Ô thời hạn giai đoạn được để trống.\n'
     '– Nếu có lỗi → thông báo “Vui lòng kiểm tra lại các ô được báo đỏ”, không thực hiện bước After.\n'
     'After:\n– Lưu 4 tham số chung cho công ty đang làm việc; lưu thời hạn từng giai đoạn (trống lưu là '
     '“không tự đóng”, không ép về 0).\n'
     '– Chỉ ghi lịch sử những ô thực sự đổi giá trị.\n'
     '– Hiển thị “Đã lưu cấu hình đóng dự án tự động” và hiển thị lại dữ liệu đã lưu.'),
    ('Rê chuột vào ⓘ', 'Hover', 'After:\n– Hiện popover giải thích tham số tương ứng.'),
])

# ------------------------------------------------------------------ 2.8
d.h3('2.8 Xem lịch sử thay đổi')
d.p('2.8.1 Giới thiệu')
d.rule_ref('- Quy tắc ghi lịch sử và Màn Xem chi tiết. Chỉ bổ sung các quy tắc riêng tại phần mô tả chi tiết.',
           anchor='history')
d.intro_table(
    ten='Xem lịch sử thay đổi cấu hình',
    mota='Popup lịch sử dùng chung cho 3 tab con: mỗi tab mở đúng lịch sử của nhóm cấu hình đó, '
         'thuộc công ty đang làm việc.',
    tacnhan='Người quản trị cấu hình; Người dùng đã đăng nhập',
    dieukien='Người dùng có quyền Q1.',
    chinh='1. Người dùng bấm “Lịch sử thay đổi” ở tab con đang mở.\n'
          '2. Hệ thống mở popup “Lịch sử thay đổi: <tên tab>”.\n'
          '3. Hệ thống hiển thị các lần thay đổi từ mới đến cũ: thời điểm, người thực hiện, loại hành động, '
          'trường thay đổi với giá trị cũ → giá trị mới.\n'
          '4. Người dùng lọc theo Loại hành động, Người thực hiện, Từ ngày / Đến ngày nếu cần.',
    phu='• Chưa có lịch sử → popup hiện “Chưa có lịch sử thao tác nào.”.\n'
        '• Không có quyền → từ chối hiển thị.')
d.p('2.8.2 Layout màn hình')
d.layout(menu=MENU_A + ' => Cấu hình hạn => Lịch sử thay đổi', shot=shot('06b-lich-su-han.png'),
         shot_caption='Popup Lịch sử thay đổi: Cấu hình hạn')
d.p('2.8.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề popup', 'Label', 'Hiển thị', '–', 'Lịch sử thay đổi: <tên tab>',
     '“Cấu hình mức độ ưu tiên” / “Cấu hình hạn” / “Đóng dự án tự động”.'),
    ('Bộ lọc Loại hành động', 'Dropdown', 'Enable', 'Danh sách', 'Trống',
     'Mức độ ưu tiên: Thêm / Cập nhật / Xóa mức độ ưu tiên, Đổi thứ tự ưu tiên; Cấu hình hạn: Cập nhật cấu hình hạn.'),
    ('Bộ lọc Người thực hiện', 'Dropdown', 'Enable', 'Danh sách', 'Trống', 'Người đã từng thay đổi.'),
    ('Từ ngày / Đến ngày', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Trống', 'Lọc theo thời điểm thay đổi.'),
    ('Dòng thời gian', 'Table/Grid', 'Read-only', '–', 'Mới → cũ',
     'Mỗi mục: thời điểm, người thực hiện, hành động, danh sách trường đổi (cũ → mới). Nhãn trường khớp nhãn '
     'trên form kèm đơn vị, vd “Nhắc trước hạn đóng (ngày)”; giai đoạn trống hiện “Không tự đóng”.'),
    ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn', '“Chưa có lịch sử thao tác nào.”'),
    ('Nút Đóng', 'Button', 'Enable', '–', 'Hiển thị', 'Đóng popup.'),
], required=False)
d.p('2.8.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Lịch sử thay đổi', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     'During:\n– Chỉ lấy lịch sử của nhóm cấu hình tương ứng thuộc công ty đang làm việc.\n'
     'After:\n– Mở popup, hiển thị dòng thời gian.'),
    ('Đổi bộ lọc', 'Change', 'After:\n– Nạp lại dòng thời gian theo bộ lọc.'),
    ('Bấm Đóng', 'Click', 'After:\n– Đóng popup; lần mở sau luôn tải lại.'),
])


# ==================================================== PHAN 4
d.h1('Phần 4. Quy tắc nghiệp vụ')
d.rule_ref('. Phần này chỉ ghi các quy tắc đặc thù của tab Quản lý dự án; không lặp lại các quy tắc đã có '
           'trong SRS quy tắc chung.', anchor='list', head='Quy tắc áp dụng',
           lead='Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ')
d.rule_table([
    ('BR-01', 'Phạm vi áp dụng cấu hình', [
        '– Theo CÔNG TY ĐANG LÀM VIỆC: mức độ ưu tiên, 9 tham số Cấu hình hạn, 4 tham số chung của Đóng dự án '
        'tự động.',
        '– DÙNG CHUNG mọi công ty: bảng Thời hạn theo giai đoạn của Đóng dự án tự động.',
        '– Công ty chưa lưu cấu hình thì dùng giá trị mặc định (Cấu hình hạn: 0 / 1 ngày / 3 giờ / 3 ngày; '
        'Đóng dự án: 3 tháng / 7 / 0 / 30 ngày).',
    ], 'Toàn màn hình'),
    ('BR-02', 'Tên mức độ ưu tiên duy nhất trong công ty', [
        '– Tên bắt buộc, tối đa 20 ký tự, không trùng trong cùng công ty; công ty khác được trùng.',
        '– Mức độ ưu tiên đang gán cho giai đoạn dự án thì không xóa được.',
    ], ['Thêm', 'Sửa', 'Xóa mức độ ưu tiên']),
    ('BR-03', 'STT mức độ ưu tiên', [
        '– STT = vị trí dòng trên bảng; kéo thả là lưu ngay, xóa dòng thì đánh lại STT các dòng còn lại.',
    ], ['Đổi thứ tự', 'Xóa mức độ ưu tiên']),
    ('BR-04', 'Hạn biên bản meeting không nhận 0', [
        '– “Hạn nhập biên bản meeting sau” và “Cảnh báo trước khi tự hủy meeting” trống hoặc ≤ 0 → lưu mặc '
        'định 1 ngày / 3 giờ, vì 0 làm cuộc họp bị hủy ngay khi kết thúc.',
        '– Quá hạn nhập biên bản, hệ thống tự hủy cuộc họp; nhắc người tạo trước thời điểm hủy theo số giờ cấu hình.',
    ], 'Cấu hình hạn'),
    ('BR-05', 'Cách tính hạn đóng dự án TKT', [
        '– Chưa có báo giá được duyệt: Hạn đóng = ngày tạo dự án + “Hạn đóng khi dự án chưa có báo giá” (tháng).',
        '– Đã có báo giá được duyệt: Hạn đóng = ngày duyệt của báo giá được duyệt gần nhất + số tháng của giai '
        'đoạn dự án đang đứng + tổng số ngày đã được duyệt gia hạn.',
        '– Giai đoạn để trống thời hạn = không bao giờ tự đóng. Đổi giai đoạn / có báo giá mới được duyệt thì '
        'hạn tự tính lại; sửa cấu hình áp dụng cả dự án đang chạy.',
    ], 'Đóng dự án tự động'),
    ('BR-06', 'Nhắc, ân hạn và tự đóng', [
        '– Trước hạn “Nhắc trước hạn đóng” ngày, gửi thông báo cho nhân viên kinh doanh chính của dự án; mỗi mốc '
        'hạn nhắc 1 lần, gia hạn thì nhắc lại theo mốc mới; 0 = không nhắc.',
        '– Dự án tự đóng sau khi quá hạn “Quá hạn bao lâu thì tự đóng” ngày, tại lần chạy tự động 01:30 hằng ngày.',
        '– Dự án đã quá hạn không gửi được đề xuất gia hạn.',
    ], 'Đóng dự án tự động'),
    ('BR-07', 'Phân cấp duyệt gia hạn dự án', [
        '– Xin gia hạn ≤ “Trưởng phòng được duyệt gia hạn tối đa” ngày → Trưởng phòng duyệt là đủ.',
        '– Xin nhiều hơn → Trưởng phòng duyệt trước, chuyển tiếp Ban giám đốc duyệt mới có hiệu lực.',
    ], 'Đóng dự án tự động'),
    ('BR-08', 'Chỉ ghi lịch sử khi giá trị thực sự đổi', [
        '– Bấm Lưu mà không đổi giá trị nào thì không phát sinh dòng lịch sử.',
        '– Lịch sử xem theo công ty đang làm việc, mỗi tab con một luồng lịch sử riêng.',
    ], 'Lịch sử thay đổi'),
])

d.save()
