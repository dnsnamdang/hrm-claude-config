# -*- coding: utf-8 -*-
"""Sinh "SRS - Tổng hợp meeting.docx" theo FORM CHUẨN (2026-09-24).

Chạy:  SRS_NO_WORD=1 /opt/homebrew/bin/python3 gen_srs.py
Nguồn đối chiếu code (nhánh gop_db):
  FE  pages/assign/meeting/{index.vue, create.vue, _id/show.vue, _id/edit.vue}
      pages/assign/meeting/components/{MeetingForm, GeneralInfo, MeetingAttendance, MeetingReport,
      CancelMeetingModal, MeetingHistoryModal, PopupStaff}.vue
      components/assign/MeetingAttendanceConfirm.vue · components/assign/meeting/{MeetingPartsConfigModal,
      MeetingPrintPreview}.vue · components/V2Footer.vue · components/subsystem-menu/meeting.js
  BE  Modules/Assign/Routes/Meeting/api.php · Http/Controllers/Api/V1/MeetingController.php
      Http/Requests/Meeting/{MeetingCreateApiRequest, MeetingUpdateApiRequest}.php
      Entities/Meeting/Meeting.php · Repositories/Criteria/MeetingCriteria.php · Services/MeetingService.php
      app/Console/Commands/Assign/MeetingReportDeadlineCommand.php
  Quyền: PermissionsTableSeeder id 1095–1098 (nhóm "Quản lý meeting")
Ảnh: shots/ (chụp thật 1440x900 trên client gop_db; ảnh HDSD vòng đời meeting dùng lại).
"""
import os
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = '/Users/manhcuong/Desktop/dns/HRM'
sys.path.insert(0, os.path.join(ROOT, '.claude', 'skills', 'srs-documenter', 'assets'))
from srs_docx_lib import SrsDoc  # noqa: E402

SHOTS = os.path.join(HERE, 'shots')


def shot(name):
    return os.path.join(SHOTS, name)


TEN_MAN = 'Tổng hợp meeting'
OUT = os.path.join(HERE, 'SRS - %s.docx' % TEN_MAN)
MENU = 'Phân hệ Meeting => Tổng hợp meeting'

d = SrsDoc(out=OUT, menu=MENU, route='', full_url='', img_prefix='meeting_')
d.set_menu_icons({k: shot(v) for k, v in {
    'Phân hệ Meeting': 'icon_n_phanhe.png',
    'Tổng hợp meeting': 'icon_n_menu.png',
    'Tìm kiếm nâng cao': 'icon_n_timkiemnc.png',
    'Cài đặt bộ lọc': 'icon_n_caidat.png',
    'Tùy chỉnh cột': 'icon_n_cot.png',
    'Xuất Excel': 'icon_n_xuatexcel.png',
    'Tạo mới': 'icon_n_taomoi.png',
    'Sửa': 'icon_n_sua.png',
    'Xóa': 'icon_n_xoa.png',
    'Mã meeting': 'icon_n_ma.png',
    'Lưu nháp': 'icon_btn_luunhap.png',
    'Lưu và Lên lịch': 'icon_btn_luulenlich.png',
    'Lưu và Chốt lịch': 'icon_btn_luuchotlich.png',
    'Lưu': 'icon_btn_luu.png',
    'Hoàn thành': 'icon_btn_hoanthanh.png',
    'Hủy': 'icon_btn_huy_footer.png',
    'Điểm danh': 'icon_tab_diemdanh.png',
    'Biên bản': 'icon_tab_bienban.png',
    'Có mặt': 'icon_btn_comat.png',
    'Vắng có lý do': 'icon_btn_vangcolydo.png',
    'Giao nhiệm vụ': 'icon_n_giaonv.png',
    'In biên bản': 'icon_n_inbienban.png',
    'In': 'icon_btn_in_footer.png',
    'Excel': 'icon_n_excel_bb.png',
    'Đăng ký phòng họp': 'icon_n_dkphong.png',
    'Hành động khác': 'icon_n_bacham.png',
    'Tạo phiếu công tác khác': 'icon_n_taophieu.png',
    'Lịch sử': 'icon_n_lichsu.png',
}.items()})

d.title_block(TEN_MAN)
d.h2('Mục lục')
d.toc()

A_NV = 'Nhân viên (người dùng đã đăng nhập)'
A_TAO = 'Người tạo meeting'
A_CT = 'Người chủ trì'
A_TV = 'Thành viên nội bộ'

NO_EDIT = ('– Không phải người tạo hoặc người chủ trì → hiển thị “Bạn không có quyền sửa meeting này!” '
           'và dừng xử lý.')
LOCKED = ('– Meeting đã Hoàn thành / Hủy → hiển thị “Thao tác không thành công. Dữ liệu đã được thay đổi '
          'hoặc chuyển trạng thái bởi người dùng khác. Vui lòng tải lại trang để cập nhật thông tin mới nhất.”')
OVERDUE = ('– Đã quá hạn nhập biên bản → hiển thị “Đã quá hạn nhập biên bản cuộc họp (<giờ ngày hạn>). Cuộc '
           'họp sẽ bị hủy, không thể cập nhật biên bản.”')


def lay(menus, shots):
    """Mục Layout: 'Đường dẫn màn hình:' + từng dòng Menu (kèm icon) + ảnh chụp thật."""
    d.p('Đường dẫn màn hình:')
    for m in menus:
        if m.startswith('Menu') or ' => ' in m:
            d._menu_para(m)
        else:
            d.p(m)
    for path, cap in shots:
        if not os.path.exists(shot(path)):
            raise IOError('Thiếu ảnh %s' % path)
        d.figure(shot(path), cap, width_in=6.2)


def fr(idx, code, name, group, actor, rule, intro, menus, shots, ui, kind, ev, uc=True):
    if not ui or not ev:
        raise RuntimeError('%s thiếu bảng giao diện hoặc bảng event' % code)
    d.h3('2.%d %s' % (idx, name))
    n = 1
    if uc:
        d.p('2.%d.%d Biểu đồ Usecase' % (idx, n))
        d.uc_figure(code, name, group, actor=actor)
        n += 1
    d.p('2.%d.%d Giới thiệu' % (idx, n)); n += 1
    d.rule_ref(rule[0], anchor=rule[1])
    d.intro_table(**intro)
    d.p('2.%d.%d Layout màn hình' % (idx, n)); n += 1
    lay(menus, shots)
    d.p('2.%d.%d Mô tả chi tiết giao diện' % (idx, n)); n += 1
    if kind == 'input':
        d.ui_table(ui)
    elif kind == 'read':
        d.ui_table(ui, required=False)
    else:
        d.ui_table(ui, required=False, scope=False)
    d.p('2.%d.%d Danh sách event và xử lý event' % (idx, n))
    d.event_table(ev)


# ============================================================== PHẦN 1
d.h1('Phần 1. Giới thiệu')
d.h2('1 Mục đích')
d.p('Tài liệu này đặc tả yêu cầu phần mềm cho màn hình “Tổng hợp meeting” (Danh sách meeting) của phân hệ '
    'Meeting — nơi tổng hợp các cuộc họp nội bộ và họp với đối tác/khách hàng của mọi phân hệ, nhằm:')
d.bullets([
    'Là căn cứ nghiệm thu đầy đủ các chức năng: xem danh sách, tìm kiếm/lọc, cài đặt bộ lọc, tùy chỉnh cột, '
    'xuất Excel, tạo mới, chỉnh sửa, xem chi tiết, xóa, lên lịch/chốt lịch, xác nhận tham dự, điểm danh, lập '
    'biên bản, giao nhiệm vụ từ biên bản, hoàn thành, hủy, in biên bản, xuất Excel biên bản, đăng ký phòng '
    'họp, tạo phiếu công tác khác và xem lịch sử.',
    'Làm rõ vòng đời trạng thái của một cuộc họp: Đang tạo → Lên lịch → Chốt lịch → Hoàn thành, hoặc Hủy; '
    'kèm cơ chế tự động hủy khi quá hạn nhập biên bản.',
    'Làm rõ ai được làm gì: thao tác trên cuộc họp phụ thuộc VAI TRÒ của người dùng trong cuộc họp (người '
    'tạo, người chủ trì, thành viên nội bộ); quyền hệ thống chỉ quyết định phạm vi dữ liệu được xem.',
])

d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('Meeting / Cuộc họp', 'Một buổi họp nội bộ hoặc họp với đối tác/khách hàng, được quản lý từ lúc soạn '
     'tới khi có biên bản.'),
    ('Mã meeting', 'Mã tự sinh theo dạng <Mã công ty>.MET.<KH|NB>.<2 số cuối năm>.<STT 4 chữ số>, '
     'ví dụ TPE.MET.NB.26.0067. KH = loại meeting có khách hàng, NB = nội bộ.'),
    ('Phân loại họp', 'Họp đối tác (loại meeting có khách hàng) hoặc Họp nội bộ.'),
    ('Người tạo', 'Nhân viên lập cuộc họp. Là người duy nhất được Hủy và Xóa cuộc họp.'),
    ('Người chủ trì', 'Nhân viên chủ trì cuộc họp, mặc định là người tạo; luôn nằm trong Thành phần — Phía '
     'Công ty. Được sửa, lên lịch, chốt lịch, điểm danh, lập biên bản, hoàn thành.'),
    ('Thành phần — Phía Công ty', 'Danh sách nhân viên nội bộ được mời họp (thành viên nội bộ).'),
    ('Thành phần — Phía Khách hàng', 'Danh sách người tham dự phía khách hàng (chỉ có ở Họp đối tác).'),
    ('Biên bản', 'Nội dung trao đổi, phương án xử lý, người đề xuất, người thực hiện, hạn dự kiến, tài liệu '
     'đính kèm và kết luận của cuộc họp.'),
    ('Hạn nhập biên bản', 'Thời gian kết thúc cuộc họp + số ngày cấu hình (mặc định 1 ngày). Quá hạn mà chưa '
     'Hoàn thành thì cuộc họp bị hệ thống tự động Hủy.'),
    ('Dự án TKT', 'Dự án tiền khả thi gắn với cuộc họp (khi tích “Meeting theo dự án”).'),
    ('Trạng thái', 'Đang tạo (Lưu nháp) · Lên lịch · Chốt lịch · Hoàn thành · Hủy.'),
], widths=[1.8, 4.2])

# ============================================================== PHẦN 2
d.h1('Phần 2. Phân quyền')
d.h2('1 Danh sách quyền')
d.p('Nhóm quyền thao tác:')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('Q1', 'Không gắn quyền riêng — mọi nhân viên đã đăng nhập',
     'Thấy menu “Tổng hợp meeting”; xem danh sách (trong phạm vi ở bảng dưới), tìm kiếm/lọc, cài đặt bộ lọc, '
     'tùy chỉnh cột, xuất Excel danh sách, tạo meeting mới.'),
    ('R1', 'Vai trò: Người tạo meeting',
     'Mọi thao tác trên cuộc họp của mình: sửa, lên lịch, chốt lịch, điểm danh, lập biên bản, hoàn thành, '
     'hủy, xóa (khi đang Lưu nháp), đăng ký phòng họp.'),
    ('R2', 'Vai trò: Người chủ trì',
     'Như người tạo nhưng KHÔNG được Hủy và KHÔNG được Xóa cuộc họp.'),
    ('R3', 'Vai trò: Thành viên nội bộ (có tên trong Thành phần — Phía Công ty)',
     'Xem chi tiết, tự xác nhận tham dự (Có mặt / Vắng có lý do), in biên bản, xuất Excel biên bản, giao '
     'nhiệm vụ từ biên bản, tạo phiếu công tác khác, xem lịch sử.'),
], widths=[0.8, 2.1, 3.1])
d.p('Thao tác trên từng cuộc họp KHÔNG gắn quyền hệ thống mà do vai trò R1–R3 quyết định. Quyền xem theo cấp '
    '(V1–V4) chỉ mở rộng phạm vi XEM, không cho phép sửa/hủy/xóa cuộc họp của người khác.')
d.p('Nhóm quyền quyết định phạm vi dữ liệu:')
d.table(['Ký hiệu', 'Tên quyền', 'Phạm vi dữ liệu'], [
    ('V1', 'Xem danh sách meeting theo tổng công ty', 'Toàn bộ cuộc họp của mọi công ty.'),
    ('V2', 'Xem danh sách meeting theo công ty', 'Cuộc họp thuộc công ty người xem đang làm việc.'),
    ('V3', 'Xem danh sách meeting theo phòng ban', 'Cuộc họp thuộc các phòng ban / bộ phận người xem quản lý.'),
    ('V4', 'Xem danh sách meeting theo bộ phận', 'Cuộc họp thuộc các bộ phận người xem quản lý.'),
    ('–', 'Không có quyền nào', 'Chỉ cuộc họp mình tạo, mình chủ trì hoặc mình có tên trong Thành phần — '
     'Phía Công ty.'),
], widths=[0.8, 2.6, 2.6])
d.p('Cuộc họp đang Lưu nháp chỉ người tạo và người chủ trì nhìn thấy, bất kể quyền V1–V4. Cấp tổ chức của cuộc '
    'họp (công ty / phòng ban / bộ phận) lấy theo người tạo tại thời điểm tạo.')

d.h2('2 Ma trận phân quyền')
Y, N = '✅', '❌'
d.table(['Chức năng', 'R1', 'R2', 'R3', 'V1–V4', 'Không có quyền nào'], [
    ('FR-01 Xem danh sách meeting', Y, Y, Y, Y, Y),
    ('FR-02 Tìm kiếm và lọc', Y, Y, Y, Y, Y),
    ('FR-03 Cài đặt bộ lọc', Y, Y, Y, Y, Y),
    ('FR-04 Tùy chỉnh cột', Y, Y, Y, Y, Y),
    ('FR-05 Xuất Excel danh sách', Y, Y, Y, Y, Y),
    ('FR-06 Tạo mới meeting', Y, Y, Y, Y, Y),
    ('FR-07 Chỉnh sửa meeting', Y, Y, N, N, N),
    ('FR-08 Xem chi tiết meeting', Y, Y, Y, Y, N),
    ('FR-09 Xóa meeting', Y, N, N, N, N),
    ('FR-10 Lên lịch và chốt lịch', Y, Y, N, N, N),
    ('FR-11 Xác nhận tham dự', 'Khi có tên trong thành phần', 'Khi có tên trong thành phần', Y, N, N),
    ('FR-12 Điểm danh', Y, Y, N, N, N),
    ('FR-13 Lập biên bản', Y, Y, N, N, N),
    ('FR-14 Giao nhiệm vụ từ biên bản', Y, Y, Y, Y, N),
    ('FR-15 Hoàn thành meeting', Y, Y, N, N, N),
    ('FR-16 Hủy meeting', Y, N, N, N, N),
    ('FR-17 In biên bản', Y, Y, Y, Y, N),
    ('FR-18 Xuất Excel biên bản', Y, Y, Y, Y, N),
    ('FR-19 Đăng ký phòng họp', Y, Y, N, N, N),
    ('FR-20 Tạo phiếu công tác khác', Y, Y, Y, Y, N),
    ('FR-21 Xem lịch sử thay đổi', Y, Y, Y, Y, N),
], widths=[2.4, 0.6, 0.6, 0.8, 0.7, 0.9])
d.p('Ghi chú: “Không có quyền nào” = người dùng không có vai trò trong cuộc họp đang xét và không có quyền '
    'V1–V4; người đó vẫn xem được danh sách cuộc họp của chính mình và tạo cuộc họp mới.')

# ============================================================== PHẦN 3
d.h1('Phần 3. Đặc tả chi tiết theo từng chức năng')
d.h2('1 Sơ đồ UML tổng quan')
d.overview_figure2(
    [(A_NV, [0, 1, 2]),
     (A_TAO, [3, 4, 5, 7, 8, 9, 10, 11, 12, 13, 14, 15]),
     (A_CT, [3, 5, 7, 8, 9, 10, 12, 13, 14, 15]),
     (A_TV, [6, 9, 12, 13, 15])],
    [('FR-01', 'Xem danh sách meeting', 'view'),
     ('FR-05', 'Xuất Excel danh sách', 'io'),
     ('FR-06', 'Tạo mới meeting', 'crud'),
     ('FR-07', 'Chỉnh sửa meeting', 'crud'),
     ('FR-09', 'Xóa meeting', 'action'),
     ('FR-10', 'Lên lịch và chốt lịch', 'action'),
     ('FR-11', 'Xác nhận tham dự', 'action'),
     ('FR-12', 'Điểm danh', 'action'),
     ('FR-13', 'Lập biên bản', 'crud'),
     ('FR-14', 'Giao nhiệm vụ từ biên bản', 'action'),
     ('FR-15', 'Hoàn thành meeting', 'action'),
     ('FR-16', 'Hủy meeting', 'action'),
     ('FR-17', 'In biên bản', 'io'),
     ('FR-18', 'Xuất Excel biên bản', 'io'),
     ('FR-19', 'Đăng ký phòng họp', 'action'),
     ('FR-20', 'Tạo phiếu công tác khác', 'action')],
    [('FR-02', 'Tìm kiếm và lọc', 'view', 'extend', [0], None),
     ('FR-03', 'Cài đặt bộ lọc', 'view', 'extend', [0], None),
     ('FR-04', 'Tùy chỉnh cột', 'view', 'extend', [0], None),
     ('FR-08', 'Xem chi tiết meeting', 'view', 'extend', [0], None),
     ('FR-21', 'Xem lịch sử thay đổi', 'view', 'extend', [0], None)],
    'Sơ đồ Use Case tổng quan màn %s' % TEN_MAN)

d.h2('2 Đặc tả chi tiết từng chức năng')

# ---------------------------------------------------------------- 2.1 Xem danh sách
fr(1, 'FR-01', 'Xem danh sách meeting', 'view', A_NV,
   ('- Màn Danh sách, Phân trang và UI/UX. Chỉ bổ sung các quy tắc riêng của màn Tổng hợp meeting tại phần '
    'mô tả chi tiết.', 'list'),
   dict(ten='Xem danh sách meeting',
        mota='Hiển thị các cuộc họp người dùng được phép xem, mới tạo nhất ở trên, phân trang 10 dòng/trang. '
             'Mỗi dòng có mã (bấm để xem chi tiết), thông tin họp, thành phần, trạng thái, biên bản và các nút '
             'thao tác theo vai trò.',
        tacnhan='Nhân viên; Người dùng đã đăng nhập',
        dieukien='Người dùng đã đăng nhập.',
        chinh='1. Người dùng chọn phân hệ Meeting, bấm menu “Tổng hợp meeting”.\n'
              '2. Hệ thống khôi phục bộ lọc đã dùng trong vòng 10 phút gần nhất (nếu có).\n'
              '3. Hệ thống nạp danh sách theo phạm vi xem (BR-02) và bộ lọc, sắp theo Ngày tạo giảm dần.\n'
              '4. Bảng hiển thị dữ liệu; chân bảng hiện “Hiển thị a–b / tổng” và phân trang.',
        phu='• Không có bản ghi phù hợp → bảng hiện “Không có dữ liệu phù hợp bộ lọc.”.\n'
            '• Lỗi khi tải → thông báo “Lỗi khi tải dữ liệu”, bảng rỗng.\n'
            '• Bấm tiêu đề cột Mã meeting / Tên meeting / Ngày họp / Ngày tạo / Ngày cập nhật → sắp xếp tăng/giảm.\n'
            '• Bấm link ở cột Biên bản → mở luồng In biên bản (FR-17).'),
   [MENU],
   [('n01_list.png', 'Màn hình Danh sách meeting')],
   [
       ('Tiêu đề trang', 'Label', 'Hiển thị', '–', 'Danh sách meeting', 'Tiêu đề trên thanh đầu trang.'),
       ('Khối “Bộ lọc danh sách”', 'Label', 'Hiển thị', '–', 'Thu gọn', 'Ô tìm nhanh + nút Tìm kiếm, Làm mới, '
        'Cài đặt bộ lọc, Tìm kiếm nâng cao (FR-02, FR-03).'),
       ('Nút Tạo mới', 'Button', 'Enable', '–', 'Hiển thị', 'Mở màn Tạo meeting (FR-06).'),
       ('Nút Đăng ký phòng họp', 'Button', 'Enable', '–', 'Hiển thị', 'Mở popup đăng ký phòng (FR-19).'),
       ('Nút Xuất Excel', 'Button', 'Enable / Disable', '–', 'Hiển thị', 'Mở popup chọn trường xuất (FR-05); '
        'khóa trong lúc đang xuất.'),
       ('Nút Tùy chỉnh cột (biểu tượng cột)', 'Icon Button', 'Enable', '–', 'Hiển thị',
        'Rê chuột hiện “Cấu hình cột hiển thị”; mở FR-04.'),
       ('Cột STT', 'Table/Grid', 'Read-only', '–', 'Theo trang', 'Cố định bên trái khi cuộn ngang.'),
       ('Cột Mã meeting', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', 'Link mở Chi tiết meeting (FR-08); '
        'cố định bên trái; sắp xếp được.'),
       ('Cột Tên meeting', 'Table/Grid', 'Read-only', '0–255 ký tự', 'Theo dữ liệu', 'Tối đa 2 dòng; sắp xếp được.'),
       ('Cột Ngày họp', 'Table/Grid', 'Read-only', 'dd/mm/yyyy', 'Theo dữ liệu',
        'Ngày bắt đầu, dòng phụ “giờ bắt đầu – giờ kết thúc”; sắp xếp được.'),
       ('Cột Thời lượng', 'Table/Grid', 'Read-only', '≥ 0', 'Theo dữ liệu', '“n phút”.'),
       ('Cột Loại meeting', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', 'Tên loại meeting.'),
       ('Cột Hình thức', 'Badge', 'Read-only', 'Trực tiếp / Online', 'Theo dữ liệu', 'Badge phân loại.'),
       ('Cột Khách hàng', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
        '“Mã - Tên khách hàng”, dòng phụ “Người liên hệ: Tên • SĐT”.'),
       ('Cột Dự án tiền khả thi', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', 'Mỗi dự án TKT 1 dòng.'),
       ('Cột Địa điểm', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', 'Địa điểm nhập tay / chọn từ bản đồ.'),
       ('Cột Phòng họp', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', 'Phòng nội bộ đã đăng ký, chưa có hiện “-”.'),
       ('Cột Thành phần tham dự', 'Table/Grid', 'Read-only', '≥ 0', 'Theo dữ liệu',
        '“Phía công ty: n người” và “Phía khách hàng: n người”.'),
       ('Cột Trạng thái', 'Badge', 'Read-only', 'Danh sách 5 giá trị', 'Theo dữ liệu',
        'Đang tạo (xám) · Lên lịch (xanh da trời) · Chốt lịch (xanh dương) · Hoàn thành (xanh lá) · Hủy (xám).'),
       ('Cột Biên bản', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
        'Có biên bản: link “Biên bản cuộc họp_<mã>” mở In biên bản; chưa có: badge “Chưa lập biên bản”.'),
       ('Cột Người tạo / Ngày tạo / Người cập nhật / Ngày cập nhật', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm',
        'Theo dữ liệu', 'Ngày tạo, Ngày cập nhật sắp xếp được.'),
       ('Cột Hành động', 'Icon Button', 'Enable / Ẩn', '–', 'Theo vai trò & trạng thái',
        'Tối đa 3 nút hiện thành biểu tượng; nhiều hơn thì 2 nút đầu là biểu tượng, còn lại vào menu “Hành động khác” (⋮): Sửa, Xóa, In biên bản, Tạo '
        'phiếu công tác khác, Lịch sử, Đăng ký / Đổi phòng họp. Nút không dùng được thì ẩn hẳn (BR-03).'),
       ('Phân trang', 'Pagination', 'Enable', '5 / 10 / 20 / 50 / 100', '10 dòng/trang', 'Số dòng/trang + chuyển trang.'),
       ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn', '“Không có dữ liệu phù hợp bộ lọc.”'),
   ], 'read',
   [
       ('Mở màn hình', 'System',
        'Before:\n– Kiểm tra người dùng đã đăng nhập.\n'
        'During:\n– Khôi phục bộ lọc đã lưu (hết hạn sau 10 phút).\n– Lấy cuộc họp theo phạm vi xem (BR-02).\n'
        'After:\n– Hiển thị bảng; lỗi → “Lỗi khi tải dữ liệu”.'),
       ('Bấm tiêu đề cột sắp xếp', 'Click', 'After:\n– Đảo chiều sắp xếp, về trang 1 và nạp lại danh sách.'),
       ('Đổi trang / số dòng mỗi trang', 'Click / Change', 'After:\n– Nạp lại dữ liệu trang tương ứng.'),
       ('Bấm Mã meeting', 'Click', 'After:\n– Mở màn Chi tiết meeting (FR-08); chuột phải mở được tab mới.'),
       ('Bấm link ở cột Biên bản', 'Click', 'After:\n– Mở luồng In biên bản (FR-17).'),
   ], uc=False)

# ---------------------------------------------------------------- 2.2 Tìm kiếm và lọc
fr(2, 'FR-02', 'Tìm kiếm và lọc', 'view', A_NV,
   ('- Kịch bản tìm kiếm, Bộ lọc, Dropdown. Chỉ bổ sung các quy tắc riêng tại phần mô tả chi tiết.', 'search'),
   dict(ten='Tìm kiếm và lọc danh sách meeting',
        mota='Tìm nhanh theo mã / tên meeting và lọc nâng cao theo 13 điều kiện. Đổi giá trị ô chọn là danh '
             'sách tự lọc lại, ô gõ chữ lọc khi bấm Tìm kiếm.',
        tacnhan='Nhân viên; Người dùng đã đăng nhập',
        dieukien='Người dùng đang ở màn Danh sách meeting.',
        chinh='1. Người dùng nhập từ khóa vào ô “Tìm theo mã meeting, tên meeting”.\n'
              '2. Người dùng bấm “Tìm kiếm nâng cao” để mở khối lọc.\n'
              '3. Người dùng chọn các điều kiện lọc.\n'
              '4. Hệ thống lọc lại danh sách, về trang 1.',
        phu='• Bấm “Làm mới” → xóa mọi điều kiện, nạp lại danh sách đúng 1 lần.\n'
            '• Chọn “Ngày họp từ” thì ô “Ngày họp đến” không cho chọn ngày nhỏ hơn và ngược lại.\n'
            '• Loại meeting đang lọc đã bị khóa vẫn hiện trong ô lọc (kèm biểu tượng khóa).\n'
            '• Điều kiện lọc và khách hàng đang lọc được nhớ trong 10 phút khi rời màn rồi quay lại.'),
   [MENU + ' => Tìm kiếm nâng cao'],
   [('n04_filter.png', 'Khối Tìm kiếm nâng cao đang mở')],
   [
       ('Ô tìm nhanh', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống',
        'Gợi ý “Tìm theo mã meeting, tên meeting”; tìm gần đúng theo mã hoặc tên.'),
       ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Áp dụng điều kiện.'),
       ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Xóa toàn bộ điều kiện lọc.'),
       ('Nút Tìm kiếm nâng cao / Ẩn tìm kiếm nâng cao', 'Button', 'Enable', '–', '–', 'Thu gọn',
        'Mở / đóng khối lọc nâng cao.'),
       ('Công ty / Phòng ban / Bộ phận', 'Dropdown', 'Enable / Disable', 'Danh sách', 'Không', 'Trống',
        '3 ô phụ thuộc nhau; chỉ mở theo quyền V1–V4 của người xem (thiếu quyền thì khóa, có biểu tượng khóa).'),
       ('Loại meeting', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống', 'Loại meeting đang hoạt động.'),
       ('Dự án tiền khả thi', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống', 'Dự án TKT đã gắn cuộc họp.'),
       ('Khách hàng', 'Dropdown', 'Enable', 'Gõ để tìm, tối đa 30 kết quả', 'Không', 'Trống',
        'Chỉ khách hàng tổ chức; tìm khi gõ, không nạp sẵn cả danh sách.'),
       ('Hình thức', 'Dropdown', 'Enable', 'Trực tiếp / Online', 'Không', 'Trống', '–'),
       ('Trạng thái', 'Dropdown', 'Enable', 'Danh sách 5 giá trị', 'Không', 'Trống',
        'Đang tạo, Lên lịch, Chốt lịch, Hoàn thành, Hủy.'),
       ('Biên bản', 'Dropdown', 'Enable', 'Đã lập biên bản / Chưa lập biên bản', 'Không', 'Trống', '–'),
       ('Người tạo / Người cập nhật', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Không', 'Trống', '–'),
       ('Ngày họp từ', 'Datepicker', 'Enable', 'dd/mm/yyyy, ≤ Ngày họp đến', 'Không', 'Trống',
        'Lấy cuộc họp có giờ bắt đầu từ ngày này.'),
       ('Ngày họp đến', 'Datepicker', 'Enable', 'dd/mm/yyyy, ≥ Ngày họp từ', 'Không', 'Trống',
        'Lấy cuộc họp có giờ kết thúc tới ngày này.'),
   ], 'input',
   [
       ('Gõ ô tìm nhanh rồi bấm Tìm kiếm / Enter', 'Click / Keypress',
        'After:\n– Lọc theo mã hoặc tên có chứa từ khóa, về trang 1.'),
       ('Đổi giá trị ô chọn / ô ngày', 'Change',
        'After:\n– Tự lọc lại danh sách, về trang 1 (không cần bấm Tìm kiếm).'),
       ('Gõ tên khách hàng', 'Keypress',
        'After:\n– Tìm khách hàng tổ chức theo từ khóa, hiện tối đa 30 kết quả.'),
       ('Bấm Làm mới', 'Click', 'After:\n– Xóa mọi điều kiện, nạp lại danh sách 1 lần.'),
   ])

# ---------------------------------------------------------------- 2.3 Cài đặt bộ lọc
fr(3, 'FR-03', 'Cài đặt bộ lọc', 'view', A_NV,
   ('- Kịch bản tìm kiếm, Bộ lọc. Chỉ bổ sung các quy tắc riêng tại phần mô tả chi tiết.', 'search'),
   dict(ten='Cài đặt bộ lọc',
        mota='Cho người dùng chọn các trường lọc muốn hiện ở khối Tìm kiếm nâng cao và sắp xếp thứ tự bằng kéo '
             'thả. Cấu hình lưu riêng theo từng người dùng cho màn này.',
        tacnhan='Nhân viên; Người dùng đã đăng nhập',
        dieukien='Người dùng đang ở màn Danh sách meeting.',
        chinh='1. Người dùng bấm “Cài đặt bộ lọc”.\n'
              '2. Hệ thống mở cửa sổ “Cài đặt bộ lọc” với 11 trường lọc.\n'
              '3. Người dùng tích / bỏ tích, kéo thả để đổi thứ tự.\n'
              '4. Người dùng bấm “Lưu”.\n'
              '5. Hệ thống lưu cấu hình, báo “Cập nhật thành công”, khối lọc hiển thị theo cấu hình mới.',
        phu='• Bấm “Khôi phục mặc định” → trả về đủ 11 trường theo thứ tự gốc (chưa lưu cho tới khi bấm Lưu).\n'
            '• Bấm “Đóng” → không lưu.\n'
            '• Lưu lỗi → “Thao tác thất bại”.'),
   [MENU + ' => Cài đặt bộ lọc'],
   [('n05_filter_setting.png', 'Cửa sổ Cài đặt bộ lọc')],
   [
       ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Cài đặt bộ lọc',
        'Dòng hướng dẫn “Tích chọn trường lọc muốn hiển thị; kéo để sắp xếp thứ tự…”.'),
       ('Danh sách trường lọc', 'Checkbox', 'Enable', '11 trường', 'Không', 'Theo cấu hình đã lưu',
        'Công ty – Phòng ban – Bộ phận, Loại meeting, Dự án tiền khả thi, Khách hàng, Hình thức, Trạng thái, '
        'Biên bản, Người tạo, Người cập nhật, Ngày họp từ, Ngày họp đến.'),
       ('Biểu tượng kéo thả', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', 'Kéo để đổi thứ tự.'),
       ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Lưu cấu hình.'),
       ('Nút Khôi phục mặc định', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Trả về cấu hình gốc.'),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng, không lưu.'),
   ], 'input',
   [
       ('Bấm Cài đặt bộ lọc', 'Click', 'After:\n– Mở cửa sổ với cấu hình đang áp dụng.'),
       ('Bấm Lưu', 'Click',
        'After:\n– Lưu cấu hình theo người dùng + màn; hiển thị “Cập nhật thành công”.\n'
        '– Lỗi → “Thao tác thất bại”.'),
       ('Bấm Khôi phục mặc định', 'Click', 'After:\n– Tích lại đủ trường theo thứ tự gốc.'),
       ('Bấm Đóng', 'Click', 'After:\n– Đóng cửa sổ, giữ cấu hình cũ.'),
   ])

# ---------------------------------------------------------------- 2.4 Tùy chỉnh cột
fr(4, 'FR-04', 'Tùy chỉnh cột', 'view', A_NV,
   ('- Quy tắc Excel và Cấu hình cột. Chỉ bổ sung các quy tắc riêng tại phần mô tả chi tiết.', 'excel'),
   dict(ten='Tùy chỉnh cột hiển thị',
        mota='Ẩn / hiện và sắp xếp thứ tự các cột của bảng danh sách. Mặc định hiện hết cột.',
        tacnhan='Nhân viên; Người dùng đã đăng nhập',
        dieukien='Người dùng đang ở màn Danh sách meeting.',
        chinh='1. Người dùng bấm nút Tùy chỉnh cột (biểu tượng cột, cạnh nút Xuất Excel).\n'
              '2. Hệ thống mở cửa sổ “Tuỳ chỉnh cột” liệt kê đủ 19 cột.\n'
              '3. Người dùng tích / bỏ tích, kéo thả biểu tượng ≡ để đổi vị trí.\n'
              '4. Người dùng bấm “Lưu”, hệ thống báo “Cập nhật thành công” và vẽ lại bảng.',
        phu='• Cột STT, Mã meeting, Hành động bị khóa: luôn hiện, không bỏ tích, không kéo được (biểu tượng ổ khóa).\n'
            '• Bấm “Đóng” → trả danh sách về cấu hình đang áp dụng.\n'
            '• Lưu lỗi → “Thao tác thất bại”.'),
   [MENU + ' => Tùy chỉnh cột'],
   [('n06_columns.png', 'Cửa sổ Tuỳ chỉnh cột')],
   [
       ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Tuỳ chỉnh cột', '–'),
       ('Danh sách cột', 'Checkbox', 'Enable', '19 cột', 'Không', 'Hiện hết',
        'STT, Mã meeting, Tên meeting, Ngày họp, Thời lượng, Loại meeting, Hình thức, Khách hàng, Dự án tiền '
        'khả thi, Địa điểm, Phòng họp, Thành phần tham dự, Trạng thái, Biên bản, Người tạo, Ngày tạo, Người cập '
        'nhật, Ngày cập nhật, Hành động.'),
       ('Cột bị khóa', 'Checkbox', 'Disable', 'STT, Mã meeting, Hành động', '–', 'Tích sẵn',
        'Rê chuột hiện “Cột bắt buộc — không thể ẩn hoặc đổi vị trí”.'),
       ('Biểu tượng ≡', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', 'Kéo thả đổi thứ tự cột.'),
       ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Lưu cấu hình cột theo người dùng.'),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng, không lưu.'),
   ], 'input',
   [
       ('Bấm nút Tùy chỉnh cột', 'Click', 'After:\n– Mở cửa sổ với cấu hình đang áp dụng.'),
       ('Bấm Lưu', 'Click',
        'After:\n– Lưu cấu hình; hiển thị “Cập nhật thành công”, bảng hiển thị theo cấu hình mới.\n'
        '– Lỗi → “Thao tác thất bại”.'),
       ('Bấm Đóng', 'Click', 'After:\n– Bỏ các thay đổi chưa lưu.'),
   ])

# ---------------------------------------------------------------- 2.5 Xuất Excel danh sách
fr(5, 'FR-05', 'Xuất Excel danh sách', 'io', A_NV,
   ('- Quy tắc Excel và Cấu hình cột, Thông báo. Chỉ bổ sung các quy tắc riêng tại phần mô tả chi tiết.', 'excel'),
   dict(ten='Xuất Excel danh sách meeting',
        mota='Xuất file Excel “danh_sach_cuoc_hop.xlsx” gồm TOÀN BỘ cuộc họp khớp bộ lọc đang áp dụng (không '
             'chỉ trang đang xem), với các cột người dùng chọn.',
        tacnhan='Nhân viên; Người dùng đã đăng nhập',
        dieukien='Người dùng đang ở màn Danh sách meeting.',
        chinh='1. Người dùng bấm “Xuất Excel”.\n'
              '2. Hệ thống mở cửa sổ “Chọn trường xuất file”, tích sẵn đúng các cột đang hiện trên bảng.\n'
              '3. Người dùng chọn / bỏ chọn, kéo thả đổi thứ tự cột trong file.\n'
              '4. Người dùng bấm “Xuất file”.\n'
              '5. Hệ thống tải file về máy và báo “Xuất Excel thành công”.',
        phu='• Lỗi khi xuất → “Lỗi khi xuất Excel”.\n'
            '• Trong lúc đang xuất, nút Xuất Excel bị khóa để tránh bấm lặp.\n'
            '• Bấm “Đóng” → không xuất.'),
   [MENU + ' => Xuất Excel'],
   [('n07_export.png', 'Cửa sổ Chọn trường xuất file')],
   [
       ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Chọn trường xuất file',
        'Dòng hướng dẫn “Tích chọn trường cần xuất, kéo ≡ để đổi thứ tự cột trong file.”'),
       ('Danh sách trường', 'Checkbox', 'Enable', '22 trường', 'Có (≥ 1)', 'Các cột đang hiện trên bảng',
        'Mã meeting, Tên meeting, Loại meeting, Hình thức, Ngày họp, Giờ bắt đầu, Giờ kết thúc, Thời lượng '
        '(phút), Địa điểm, Phòng họp, Link họp online, Mã khách hàng, Tên khách hàng, Người liên hệ KH, SĐT '
        'người liên hệ, Số người phía công ty, Số người phía khách hàng, Trạng thái, Người tạo, Ngày tạo, Người '
        'cập nhật, Ngày cập nhật.'),
       ('Nút Chọn tất cả / Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', '–'),
       ('Dòng đếm', 'Label', 'Hiển thị', '–', '–', '“Đang chọn n/22 trường”', '–'),
       ('Nút Xuất file', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị', 'Khóa trong lúc đang xuất.'),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng, không xuất.'),
   ], 'input',
   [
       ('Bấm Xuất Excel', 'Click', 'After:\n– Mở cửa sổ chọn trường, tích sẵn các cột đang hiện.'),
       ('Bấm Xuất file', 'Click',
        'Before:\n– Người dùng đã đăng nhập.\n'
        'During:\n– Lấy toàn bộ cuộc họp theo bộ lọc + phạm vi xem (BR-02), đúng thứ tự sắp xếp đang dùng.\n'
        'After:\n– Tải file “danh_sach_cuoc_hop.xlsx” (sheet “Danh sách meeting”) với các cột đã chọn theo '
        'thứ tự đã chọn.\n– Hiển thị “Xuất Excel thành công”; lỗi → “Lỗi khi xuất Excel”.'),
   ])

# ---------------------------------------------------------------- 2.6 Tạo mới
fr(6, 'FR-06', 'Tạo mới meeting', 'crud', A_NV,
   ('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX. Logic ghi lịch sử áp dụng theo SRS Các quy tắc '
    'chung - Quy tắc ghi lịch sử.', 'create'),
   dict(ten='Tạo mới meeting',
        mota='Lập một cuộc họp mới gồm thông tin chung, phòng/địa điểm, thời gian, người chủ trì, khách hàng & '
             'người liên hệ (Họp đối tác), dự án TKT (Meeting theo dự án), mục tiêu/nội dung, tài liệu chuẩn bị và '
             'thành phần tham dự. Lưu ở 1 trong 3 trạng thái: Lưu nháp, Lên lịch hoặc Chốt lịch.',
        tacnhan='Nhân viên; Người dùng đã đăng nhập',
        dieukien='Người dùng đã đăng nhập.',
        chinh='1. Người dùng bấm “Tạo mới” trên màn Danh sách meeting.\n'
              '2. Hệ thống mở màn “Tạo meeting”, tab Thông tin; điền sẵn Người chủ trì = người đang đăng nhập và thêm '
              'chính người đó vào Thành phần — Phía Công ty.\n'
              '3. Người dùng nhập Tên meeting, chọn Phân loại họp, Loại meeting, Hình thức, Bắt đầu, Kết thúc…\n'
              '4. Với Họp đối tác: chọn Khách hàng và Người liên hệ, thêm Thành phần — Phía Khách hàng.\n'
              '5. Người dùng bấm dấu + ở Thành phần — Phía Công ty để chọn thêm nhân viên.\n'
              '6. Người dùng bấm “Lưu nháp”, “Lưu và Lên lịch” hoặc “Lưu và Chốt lịch”.\n'
              '7. Hệ thống kiểm tra, sinh mã meeting, lưu, ghi lịch sử “Tạo mới”, báo “Thêm mới thành công” và quay '
              'về màn Danh sách meeting.',
        phu='• Lưu và Lên lịch / Lưu và Chốt lịch → gửi thông báo lịch họp cho toàn bộ Thành phần — Phía Công ty (BR-15).\n'
            '• Tích “Meeting theo dự án” → hiện ô Dự án TKT (bắt buộc) và thêm tab “Dự án tiền khả thi”.\n'
            '• Dữ liệu không hợp lệ → báo lỗi đỏ dưới từng ô, tab chứa lỗi hiện cờ đỏ và tự chuyển tới ô lỗi đầu tiên.\n'
            '• Loại meeting vừa bị khóa → “Loại meeting "<tên>" đã bị khoá. Vui lòng chọn Loại meeting khác.”\n'
            '• Rời màn khi chưa lưu → hỏi xác nhận thoát (cảnh báo thông tin chưa lưu).\n'
            '• Bấm “Quay lại” → về màn Danh sách meeting (hoặc màn nguồn khi mở từ màn khác).',
        dacbiet='Phòng họp chưa đăng ký được ở bước tạo mới — phải lưu và Lên lịch trước (FR-19). Tab Điểm danh và '
                'Biên bản hiện nhưng chỉ dùng được ở các bước sau.'),
   [MENU + ' => Tạo mới'],
   [('02_create.png', 'Màn hình Tạo meeting — Họp nội bộ'),
    ('n15_create_partner.png', 'Màn hình Tạo meeting — Họp đối tác: khối Khách hàng & Người liên hệ'),
    ('n16_create_project.png', 'Tích “Meeting theo dự án”: ô Dự án TKT và tab Dự án tiền khả thi'),
    ('03_pick_staff.png', 'Cửa sổ Chọn nhân viên phía công ty')],
   [
       ('Thanh trạng thái meeting', 'Label', 'Read-only', '–', '–', 'Lưu nháp',
        'Các bước Lên lịch → Đã chốt → Hoàn thành → Huỷ; bước đạt tới tô xanh, Hủy tô đỏ.'),
       ('Tab Thông tin / Điểm danh / Biên bản / Dự án tiền khả thi', 'Tab', 'Enable', '–', '–', 'Thông tin',
        'Tab Dự án tiền khả thi chỉ hiện khi tích Meeting theo dự án; tab có lỗi hiện cờ đỏ.'),
       ('Tên meeting', 'Textbox', 'Enable', '1–255 ký tự', 'Có', 'Trống',
        'Gợi ý “[Đấu thầu] Thương thảo hợp đồng và Chốt phương án cung cấp - Xưởng 3S VinFast”.'),
       ('Phân loại họp', 'Radio', 'Enable', 'Họp đối tác / Họp nội bộ', 'Không', 'Họp đối tác',
        'Lọc danh sách Loại meeting theo có/không có khách hàng; đổi phân loại thì xóa Loại meeting đã chọn nếu không khớp.'),
       ('Loại meeting', 'Dropdown', 'Enable', 'Danh sách', 'Có', 'Trống',
        'Loại đang hoạt động, kèm biểu tượng ⓘ mô tả loại.'),
       ('Hình thức', 'Dropdown', 'Enable', 'Trực tiếp / Trực tuyến (Online)', 'Không', 'Trống', '–'),
       ('Link họp (nếu Online)', 'Textbox', 'Enable / Ẩn', 'Đường dẫn hợp lệ', 'Không', 'Ẩn',
        'Chỉ hiện khi Hình thức = Online.'),
       ('Phòng họp', 'Label', 'Read-only', '–', '–', 'Chưa đăng ký phòng',
        'Ở bước tạo mới hiện “Lưu cuộc họp trước rồi mới đăng ký phòng được.”'),
       ('Địa điểm meeting', 'Radio + Textbox', 'Enable / Ẩn', '0–255 ký tự', 'Có khi Trực tiếp, từ Chốt lịch, '
        'chưa có phòng', 'Nhập', '2 cách: Nhập (gợi ý “VD: Phòng 302, Trụ sở Hà Nội”) hoặc Chọn từ bản đồ. Ẩn khi '
        'đã có phòng họp. Ghi chú cam: khi nhập thủ công, lúc làm phiếu giao đi công tác phải chọn lại địa điểm.'),
       ('Bắt đầu / Kết thúc', 'Datepicker', 'Enable', 'dd/mm/yyyy hh:mm, ≥ hiện tại', 'Có', 'Trống',
        'Không chọn được ngày quá khứ; Kết thúc phải sau Bắt đầu.'),
       ('Người chủ trì', 'Dropdown', 'Enable', 'Nhân viên đang làm việc', 'Có', 'Người đang đăng nhập',
        'Đổi người chủ trì thì người mới được đưa vào Thành phần — Phía Công ty.'),
       ('Meeting theo dự án', 'Checkbox', 'Enable', '–', 'Không', 'Bỏ tích', 'Tích → hiện ô Dự án TKT.'),
       ('Dự án TKT', 'Dropdown (chọn nhiều)', 'Enable / Ẩn', 'Danh sách', 'Có khi tích Meeting theo dự án', 'Trống',
        'Tìm theo mã / tên; mỗi dự án có thể chọn Giải pháp, Hạng mục/Module.'),
       ('Khách hàng', 'Popup chọn', 'Enable / Ẩn', '–', 'Có khi loại meeting có khách hàng', 'Trống',
        '“Nhấn vào đây để chọn thông tin khách hàng”; kèm nút “Thêm nhanh khách hàng”, “Lịch sử meeting”; hiện khối '
        'Mã KH, MST, SĐT, Họ tên, Địa chỉ.'),
       ('Người liên hệ', 'Dropdown', 'Enable / Ẩn', 'Danh sách', 'Có với khách hàng doanh nghiệp', 'Trống',
        'Gõ SĐT đầy đủ để tìm liên hệ khác; nút + thêm nhanh liên hệ (Họ tên, Chức vụ, SĐT bắt buộc). Tên / Chức '
        'vụ / SĐT người liên hệ tự điền, chỉ đọc.'),
       ('Mục tiêu / Nội dung', 'Textarea (soạn thảo)', 'Enable', '–', 'Không', 'Trống', 'Trình soạn thảo văn bản.'),
       ('Tài liệu chuẩn bị cho buổi họp', 'Table/Grid', 'Enable', 'Tên ≤ 255 ký tự', 'Tên: Có', 'Trống',
        'Bảng tài liệu: Tên tài liệu + Chọn tệp; tải lên ngay khi chọn.'),
       ('Thành phần — Phía Công ty', 'Table/Grid', 'Enable', '≥ 1 người', 'Có', 'Người đang đăng nhập',
        'Nút + mở “Chọn nhân viên phía công ty”; kéo thả đổi thứ tự; người chủ trì có nhãn “Người chủ trì” và '
        'không xóa được.'),
       ('Thành phần — Phía Khách hàng', 'Table/Grid', 'Enable / Ẩn', 'Họ tên ≤ 255; SĐT 0 + 9–11 số', 'Họ tên: Có',
        'Trống', 'Chỉ có ở Họp đối tác; nút + thêm dòng Họ tên / Chức vụ / SĐT.'),
       ('Nút Lưu nháp', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Lưu trạng thái Đang tạo.'),
       ('Nút Lưu và Lên lịch', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Lưu trạng thái Lên lịch + gửi thông báo.'),
       ('Nút Lưu và Chốt lịch', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Lưu trạng thái Chốt lịch + gửi thông báo.'),
       ('Nút Quay lại', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Về màn nguồn.'),
       ('Thông báo lỗi dưới ô', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', 'Chữ đỏ dưới ô bị lỗi.'),
   ], 'input',
   [
       ('Bấm dấu + ở Thành phần — Phía Công ty', 'Click',
        'After:\n– Mở “Chọn nhân viên phía công ty”: tìm theo tên/mã, tích chọn, bấm “Thêm thành viên”.'),
       ('Chọn Phân loại họp / Loại meeting', 'Change',
        'After:\n– Loại có khách hàng → hiện khối Khách hàng & Người liên hệ và Thành phần — Phía Khách hàng.'),
       ('Bấm Lưu nháp / Lưu và Lên lịch / Lưu và Chốt lịch', 'Click',
        'Before:\n– Người dùng đã đăng nhập (không cần quyền riêng).\n'
        'During:\n– Tên meeting trống → “Bắt buộc phải nhập”; quá 255 ký tự → “Vui lòng nhập tối đa 255 ký tự.”\n'
        '– Loại meeting trống → “Bắt buộc phải nhập”; loại đã bị khóa → “Loại meeting "<tên>" đã bị khoá. Vui '
        'lòng chọn Loại meeting khác.”\n'
        '– Bắt đầu / Kết thúc trống → “Bắt buộc phải nhập”; nhỏ hơn hiện tại → “Ngày giờ bắt đầu phải lớn hơn hoặc '
        'bằng thời điểm hiện tại.” / “Ngày giờ kết thúc phải lớn hơn hoặc bằng thời điểm hiện tại.”; Kết thúc ≤ Bắt '
        'đầu → “Ngày giờ kết thúc phải lớn hơn ngày giờ bắt đầu.”\n'
        '– Người chủ trì trống → “Vui lòng chọn Người chủ trì.”; không hợp lệ → “Người chủ trì không hợp lệ.”\n'
        '– Lưu và Chốt lịch, Hình thức Trực tiếp, chưa có phòng mà Địa điểm trống → “Bắt buộc phải nhập”.\n'
        '– Link họp sai định dạng → “Không hợp lệ”.\n'
        '– Loại meeting có khách hàng: Khách hàng trống → “Bắt buộc phải nhập”; khách hàng doanh nghiệp thiếu Tên / '
        'SĐT người liên hệ → “Bắt buộc phải nhập”; SĐT sai dạng → “Không hợp lệ”; khách hàng cá nhân / người liên '
        'hệ đang được nhân viên kinh doanh khác đăng ký còn hạn → chặn kèm thông báo khóa sở hữu.\n'
        '– Dự án TKT thiếu Tên / Ứng dụng / Loại hình / Lĩnh vực… → “Vui lòng nhập Tên dự án TKT.”, “Vui lòng chọn '
        'Ứng dụng.”, “Vui lòng chọn Loại hình hoạt động khách hàng.”…; Ứng dụng đã khóa → “Ứng dụng "<tên>" đã '
        'bị khoá. Vui lòng chọn Ứng dụng khác cho dự án.”\n'
        '– Thành phần phía công ty/khách hàng thiếu Họ tên → “Bắt buộc phải nhập”; SĐT sai → “Không hợp lệ”.\n'
        '– Tài liệu thiếu tên → “Bắt buộc phải nhập”.\n'
        '– Còn lỗi → toast nêu câu lỗi đầu tiên, chuyển tới tab/ô lỗi; không thực hiện bước After.\n'
        'After:\n– Sinh mã meeting (BR-04); gán công ty / phòng ban / bộ phận theo người tạo.\n'
        '– Lưu cuộc họp + thành phần + tài liệu + dự án TKT; bảo đảm người chủ trì nằm trong Thành phần — Phía Công ty.\n'
        '– Ghi lịch sử “Tạo mới”.\n– Lên lịch / Chốt lịch → gửi thông báo cho thành phần nội bộ.\n'
        '– Hiển thị “Thêm mới thành công” và quay về màn Danh sách meeting.\n'
        '– Lỗi khác → “Bạn chưa nhập đầy đủ thông tin” / “Có lỗi xảy ra”.'),
       ('Bấm Quay lại / rời màn khi chưa lưu', 'Click', 'After:\n– Hỏi xác nhận thoát; đồng ý → bỏ dữ liệu đang nhập.'),
   ])

# ---------------------------------------------------------------- 2.7 Chỉnh sửa
fr(7, 'FR-07', 'Chỉnh sửa meeting', 'crud', A_TAO,
   ('- Màn Chỉnh sửa, Validate dữ liệu, Thông báo và UI/UX. Logic ghi lịch sử áp dụng theo SRS Các quy tắc '
    'chung - Quy tắc ghi lịch sử.', 'create'),
   dict(ten='Chỉnh sửa meeting',
        mota='Sửa thông tin cuộc họp chưa Hoàn thành / Hủy. Bộ nút ở chân màn đổi theo trạng thái hiện tại.',
        tacnhan='Người tạo meeting, Người chủ trì; Người dùng đã đăng nhập',
        dieukien='Người dùng là người tạo hoặc người chủ trì; cuộc họp ở trạng thái Đang tạo, Lên lịch hoặc Chốt lịch '
                 'và chưa quá hạn nhập biên bản.',
        chinh='1. Người dùng bấm biểu tượng Sửa ở cột Hành động (hoặc nút Sửa ở màn chi tiết).\n'
              '2. Hệ thống mở màn “Sửa meeting” với dữ liệu hiện tại.\n'
              '3. Người dùng sửa thông tin (quy tắc nhập như Tạo mới).\n'
              '4. Người dùng bấm nút lưu tương ứng trạng thái: Đang tạo → “Lưu nháp”; Lên lịch / Chốt lịch → “Lưu”.\n'
              '5. Hệ thống kiểm tra, cập nhật, ghi lịch sử “Chỉnh sửa”, báo thành công và quay về màn nguồn.',
        phu='• Cuộc họp đã Chốt lịch mà đổi giờ → hộp “Xác nhận thay đổi thời gian”: “Thời gian cuộc họp đã thay đổi so '
            'với lịch đã chốt trước đó. Việc lưu sẽ gửi lịch họp mới đến tất cả thành viên tham dự. Bạn có xác nhận gửi '
            'lịch họp mới không?” — bấm “Xác nhận gửi lịch” mới lưu.\n'
            '• Lưu khi đã Lên lịch / Chốt lịch: đổi giờ → báo toàn bộ thành viên nội bộ; thêm/bớt người → chỉ báo người '
            'liên quan.\n'
            '• Người chỉ tham gia mở màn Sửa bằng đường dẫn trực tiếp → tự chuyển sang màn Chi tiết.\n'
            '• Tải dữ liệu lỗi → “Có lỗi xảy ra khi tải dữ liệu”.',
        dacbiet='Bộ nút chân màn: Đang tạo = Lưu nháp, Lưu và Lên lịch, Lưu và Chốt lịch, Quay lại · Lên lịch = Lưu, '
                'Lưu và Lên lịch, Lưu và Chốt lịch, Hủy, Quay lại · Chốt lịch = Lưu, Hoàn thành, Hủy, Quay lại. Người '
                'chủ trì (không phải người tạo) không có nút Hủy.'),
   [MENU + ' => Sửa'],
   [('04_edit.png', 'Màn hình Sửa meeting')],
   [
       ('Các trường của tab Thông tin', 'Textbox / Dropdown / Datepicker', 'Enable', 'Như FR-06', 'Như FR-06',
        'Theo dữ liệu', 'Ràng buộc như Tạo mới, riêng thời gian xem BR-05.'),
       ('Phòng họp', 'Label + Button', 'Enable / Ẩn', '–', 'Không', 'Theo dữ liệu',
        'Từ Lên lịch: nút “Đăng ký phòng” / “Đổi phòng”, “Hủy đăng ký” (FR-19); badge trạng thái phiếu đặt phòng.'),
       ('Bắt đầu', 'Datepicker', 'Enable', 'Lên lịch: ≥ hiện tại; khác: ≥ thời điểm tạo meeting', 'Có',
        'Theo dữ liệu', '–'),
       ('Kết thúc', 'Datepicker', 'Enable', '≥ Bắt đầu', 'Có', 'Theo dữ liệu', '–'),
       ('Nút Lưu nháp', 'Button', 'Enable / Ẩn', '–', '–', 'Hiện khi Đang tạo', 'Giữ trạng thái Đang tạo.'),
       ('Nút Lưu', 'Button', 'Enable / Ẩn', '–', '–', 'Hiện khi Lên lịch / Chốt lịch',
        'Lưu thay đổi, giữ nguyên trạng thái.'),
       ('Nút Lưu và Lên lịch / Lưu và Chốt lịch', 'Button', 'Enable / Ẩn', '–', '–',
        'Hiện khi Đang tạo / Lên lịch', 'Xem FR-10.'),
       ('Nút Hoàn thành', 'Button', 'Enable / Disable / Ẩn', '–', '–', 'Hiện khi Chốt lịch', 'Xem FR-15.'),
       ('Nút Hủy', 'Button', 'Enable / Disable / Ẩn', '–', '–', 'Hiện khi Lên lịch / Chốt lịch, chỉ người tạo',
        'Xem FR-16.'),
       ('Nút Quay lại', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Về màn nguồn (danh sách, Công việc của tôi, '
        'quản lý giải pháp / hạng mục).'),
       ('Hộp Xác nhận thay đổi thời gian', 'Modal', 'Hiển thị', '–', '–', 'Ẩn',
        'Nút “Xác nhận gửi lịch” và “Hủy”.'),
   ], 'input',
   [
       ('Mở màn Sửa', 'System',
        'Before:\n– Tải dữ liệu cuộc họp; không xem được → “Bạn không có quyền xem meeting này!”.\n'
        'After:\n– Người không phải người tạo / chủ trì → chuyển sang màn Chi tiết.'),
       ('Bấm Lưu nháp / Lưu', 'Click',
        'Before:\n– Kiểm tra vai trò người tạo hoặc người chủ trì.\n' + NO_EDIT + '\n' + LOCKED + '\n' + OVERDUE + '\n'
        'During:\n– Kiểm tra như FR-06; Bắt đầu sai mốc → “Phải sau hoặc bằng thời gian hiện tại” (Lên lịch) hoặc '
        '“Phải sau hoặc bằng thời gian tạo meeting”; Kết thúc < Bắt đầu → “Phải sau hoặc bằng thời gian bắt đầu”.\n'
        '– Chốt lịch và đổi giờ → hỏi xác nhận thay đổi thời gian trước khi lưu.\n'
        '– Nếu có lỗi validate → không thực hiện bước After.\n'
        'After:\n– Cập nhật cuộc họp và bảng con; ghi lịch sử “Chỉnh sửa” (giá trị cũ → mới).\n'
        '– Gửi thông báo cho người bị ảnh hưởng (BR-15).\n'
        '– Hiển thị “Cập nhật thành công” và quay về màn nguồn.'),
       ('Bấm Xác nhận gửi lịch', 'Click', 'After:\n– Lưu với giờ mới, gửi lịch họp mới cho toàn bộ thành viên nội bộ.'),
   ])

# ---------------------------------------------------------------- 2.8 Xem chi tiết
fr(8, 'FR-08', 'Xem chi tiết meeting', 'view', A_TV,
   ('- Màn Xem chi tiết và Phân quyền. Chỉ bổ sung các quy tắc riêng tại phần mô tả chi tiết.', 'detail'),
   dict(ten='Xem chi tiết meeting',
        mota='Hiển thị toàn bộ cuộc họp ở chế độ chỉ đọc: thanh trạng thái, xác nhận tham dự của chính người xem, lý do '
             'hủy (nếu đã hủy), các tab Thông tin / Điểm danh / Biên bản / Nhiệm vụ / Dự án tiền khả thi và khối Lịch '
             'sử ở cuối màn.',
        tacnhan='Người tạo meeting, Người chủ trì, Thành viên nội bộ, Người có quyền V1–V4; Người dùng đã đăng nhập',
        dieukien='Người dùng xem được cuộc họp (BR-02).',
        chinh='1. Người dùng bấm Mã meeting ở màn Danh sách meeting.\n'
              '2. Hệ thống mở màn “Chi tiết meeting: <mã>”.\n'
              '3. Người dùng chuyển giữa các tab để xem thông tin.\n'
              '4. Người dùng bấm các nút ở chân màn tùy vai trò và trạng thái.',
        phu='• Không có quyền xem → hệ thống chuyển sang trang không tìm thấy.\n'
            '• Cuộc họp đã Hủy → hiện khối đỏ “Lý do hủy”: “<Tên lý do> — <ghi chú>”, “Hủy lúc <giờ> bởi <người>”.\n'
            '• Tab Nhiệm vụ: danh sách nhiệm vụ gắn với cuộc họp (lọc, tạo mới nhiệm vụ theo quy tắc chức năng Nhiệm vụ).\n'
            '• Khối Lịch sử thu gọn mặc định, bấm “Xem lịch sử” mới tải (FR-21).\n'
            '• Ngoài menu, màn này còn được mở từ thông báo chuông, Công việc của tôi, Nhu cầu khách hàng, Đăng ký phòng họp '
            'và tab Meeting của Giải pháp / Hạng mục.'),
   [MENU + ' => Mã meeting'],
   [('09_complete.png', 'Màn hình Chi tiết meeting — tab Thông tin'),
    ('n13_tasks_tab.png', 'Tab Nhiệm vụ và khối Lịch sử ở cuối màn chi tiết')],
   [
       ('Tiêu đề trang', 'Label', 'Hiển thị', '–', 'Chi tiết meeting: <mã>', '–'),
       ('Thanh trạng thái meeting', 'Label', 'Read-only', '–', 'Theo dữ liệu',
        'Lưu nháp / Lên lịch hẹn / Đã chốt lịch / Đã hoàn thành / Huỷ.'),
       ('Khối Xác nhận tham dự', 'Badge + Button', 'Enable / Ẩn', '–', 'Chỉ hiện với thành viên nội bộ', 'Xem FR-11.'),
       ('Khối Lý do hủy', 'Label', 'Read-only', '–', 'Chỉ hiện khi Hủy', 'Tên lý do — ghi chú, thời điểm và người hủy.'),
       ('Tab Thông tin / Điểm danh / Biên bản', 'Tab', 'Enable', '–', 'Thông tin', 'Mọi ô ở chế độ chỉ đọc.'),
       ('Tab Nhiệm vụ', 'Tab', 'Enable', '–', 'Hiển thị', 'Danh sách nhiệm vụ gắn với cuộc họp.'),
       ('Tab Dự án tiền khả thi', 'Tab', 'Enable / Ẩn', '–', 'Hiện khi Meeting theo dự án', '–'),
       ('Khối Lịch sử', 'Table/Grid', 'Read-only', '–', 'Thu gọn', 'Nút “Xem lịch sử” (FR-21).'),
       ('Nút In', 'Button', 'Enable', '–', 'Hiển thị', 'In biên bản (FR-17).'),
       ('Nút Sửa', 'Button', 'Enable / Ẩn', '–', 'Hiện khi chưa Hoàn thành / Hủy và là người tạo / chủ trì', 'FR-07.'),
       ('Nút Xóa', 'Button', 'Enable / Ẩn', '–', 'Hiện khi Đang tạo và là người tạo', 'FR-09.'),
       ('Nút Hủy', 'Button', 'Enable / Disable / Ẩn', '–', 'Hiện khi Lên lịch / Chốt lịch và là người tạo', 'FR-16.'),
       ('Nút Tạo phiếu công tác khác', 'Button', 'Enable / Ẩn', '–', 'Hiện khi chưa Hoàn thành / Hủy', 'FR-20.'),
       ('Nút Quay lại', 'Button', 'Enable', '–', 'Hiển thị', 'Về màn nguồn.'),
   ], 'read',
   [
       ('Mở màn Chi tiết', 'System',
        'Before:\n– Kiểm tra người xem là người tạo, người chủ trì, thành viên nội bộ hoặc có quyền V1–V4 phù hợp.\n'
        '– Không đủ điều kiện → “Bạn không có quyền xem meeting này!”, chuyển sang trang không tìm thấy.\n'
        'After:\n– Hiển thị dữ liệu chỉ đọc và bộ nút theo vai trò, trạng thái.'),
       ('Chuyển tab', 'Click', 'After:\n– Hiển thị nội dung tab tương ứng.'),
       ('Bấm Quay lại', 'Click', 'After:\n– Về màn nguồn (mặc định màn Danh sách meeting).'),
   ], uc=False)

# ---------------------------------------------------------------- 2.9 Xóa
fr(9, 'FR-09', 'Xóa meeting', 'action', A_TAO,
   ('- Quy tắc Xóa và Thông báo.', 'delete'),
   dict(ten='Xóa meeting',
        mota='Xóa hẳn cuộc họp đang Lưu nháp cùng thành phần, biên bản, tài liệu và liên kết dự án TKT.',
        tacnhan='Người tạo meeting',
        dieukien='Người dùng là người tạo; cuộc họp ở trạng thái Đang tạo.',
        chinh='1. Người dùng bấm biểu tượng Xóa ở cột Hành động (hoặc nút Xóa ở màn chi tiết).\n'
              '2. Hệ thống hiện hộp “Xác nhận xóa”.\n'
              '3. Người dùng bấm “Xóa”.\n'
              '4. Hệ thống xóa cuộc họp, báo “Xóa thành công” và nạp lại danh sách (từ màn chi tiết thì quay về màn nguồn).',
        phu='• Bấm “Hủy” → đóng hộp, không xóa.\n'
            '• Cuộc họp đã đổi trạng thái → “Thao tác không thành công. Dữ liệu đã được thay đổi hoặc chuyển trạng thái '
            'bởi người dùng khác. Vui lòng tải lại trang để cập nhật thông tin mới nhất.”\n'
            '• Cuộc họp không còn tồn tại → “Dữ liệu đã thay đổi, vui lòng tải lại”.',
        dacbiet='Xóa là xóa hẳn (không xóa mềm); file tài liệu trên kho lưu trữ được xóa theo.'),
   [MENU + ' => Xóa'],
   [('14_delete.png', 'Hộp xác nhận xóa meeting')],
   [
       ('Tiêu đề hộp', 'Label', 'Hiển thị', 'Xác nhận xóa', 'Biểu tượng cảnh báo.'),
       ('Nội dung', 'Label', 'Hiển thị', 'Theo dòng', 'Ở danh sách: “Bạn có chắc muốn xóa meeting ‘<tên>’?”; ở chi tiết: '
        '“Bạn có chắc chắn muốn xóa meeting này?”'),
       ('Nút Xóa', 'Button', 'Enable', 'Hiển thị', 'Màu đỏ, xác nhận xóa.'),
       ('Nút Hủy', 'Button', 'Enable', 'Hiển thị', 'Đóng hộp, không xóa.'),
   ], 'confirm',
   [
       ('Bấm Xóa trên dòng / chân màn chi tiết', 'Click', 'After:\n– Mở hộp Xác nhận xóa.'),
       ('Bấm Xóa trong hộp xác nhận', 'Click',
        'Before:\n– Kiểm tra người dùng là người tạo.\n– Không phải → “Bạn không có quyền xoá meeting này!” và dừng xử lý.\n'
        'During:\n– Cuộc họp không còn ở Đang tạo → “Thao tác không thành công. Dữ liệu đã được thay đổi hoặc chuyển '
        'trạng thái bởi người dùng khác. Vui lòng tải lại trang để cập nhật thông tin mới nhất.”\n'
        'After:\n– Xóa câu trả lời biểu mẫu & liên kết dự án TKT, thành phần, người thực hiện biên bản, biên bản, tài liệu '
        '(cả file), phiếu đặt phòng liên quan, rồi xóa cuộc họp.\n'
        '– Hiển thị “Xóa thành công”; lỗi → nội dung lỗi hoặc “Xoá thất bại” / “Xóa thất bại”.'),
       ('Bấm Hủy', 'Click', 'After:\n– Đóng hộp, giữ nguyên dữ liệu.'),
   ])

# ---------------------------------------------------------------- 2.10 Lên lịch và chốt lịch
fr(10, 'FR-10', 'Lên lịch và chốt lịch', 'action', A_TAO,
   ('- Validate dữ liệu, Thông báo và UI/UX. Logic ghi lịch sử áp dụng theo SRS Các quy tắc chung - Quy tắc ghi '
    'lịch sử.', 'create'),
   dict(ten='Lên lịch và chốt lịch meeting',
        mota='Chuyển cuộc họp sang Lên lịch (gửi lịch hẹn cho thành viên) rồi Chốt lịch (đã thống nhất thời gian, địa '
             'điểm, thành phần). Hai thao tác là nút lưu kèm đổi trạng thái ở màn Tạo / Sửa.',
        tacnhan='Người tạo meeting, Người chủ trì',
        dieukien='Cuộc họp ở trạng thái Đang tạo (lên lịch / chốt lịch) hoặc Lên lịch (lên lịch lại / chốt lịch).',
        chinh='1. Người dùng mở màn Sửa của cuộc họp.\n'
              '2. Người dùng bấm “Lưu và Lên lịch” → cuộc họp chuyển Lên lịch, hệ thống gửi thông báo lịch họp.\n'
              '3. Khi đã thống nhất, người dùng bấm “Lưu và Chốt lịch” → cuộc họp chuyển Chốt lịch, hệ thống gửi thông '
              'báo chốt lịch.\n'
              '4. Hệ thống ghi lịch sử “Đổi trạng thái”, báo “Cập nhật thành công” và quay về màn nguồn.',
        phu='• Đang Lên lịch mà bấm lại “Lưu và Lên lịch” → giữ trạng thái và gửi lại thông báo lịch họp.\n'
            '• Chốt lịch với hình thức Trực tiếp, chưa có phòng họp → bắt buộc nhập Địa điểm meeting.\n'
            '• Từ Lên lịch trở đi mới đăng ký được phòng họp (FR-19).',
        dacbiet='Thông báo: “[MET]: <Tên meeting>. Thời gian dự kiến (<giờ>) Địa điểm: … Hình thức: …” khi Lên lịch; '
                '“[MET]: <Tên meeting>. Thời gian (<giờ>) …” khi Chốt lịch; gửi cho toàn bộ Thành phần — Phía Công ty.'),
   [MENU + ' => Sửa => Lưu và Lên lịch / Lưu và Chốt lịch'],
   [('05_schedule_edit.png', 'Màn hình Sửa meeting ở trạng thái Lên lịch')],
   [
       ('Nút Lưu và Lên lịch', 'Button', 'Enable / Ẩn', '–', '–', 'Hiện khi Tạo mới / Đang tạo / Lên lịch',
        'Lưu với trạng thái Lên lịch, gửi thông báo.'),
       ('Nút Lưu và Chốt lịch', 'Button', 'Enable / Ẩn', '–', '–', 'Hiện khi Tạo mới / Đang tạo / Lên lịch',
        'Lưu với trạng thái Chốt lịch, gửi thông báo.'),
       ('Địa điểm meeting', 'Textbox', 'Enable', '0–255 ký tự', 'Có khi Chốt lịch + Trực tiếp + chưa có phòng',
        'Theo dữ liệu', 'Dấu * chỉ hiện từ bước Chốt lịch.'),
       ('Thanh trạng thái', 'Label', 'Read-only', '–', '–', 'Theo dữ liệu', 'Bước Lên lịch / Đã chốt tô xanh.'),
   ], 'input',
   [
       ('Bấm Lưu và Lên lịch', 'Click',
        'Before:\n– Kiểm tra vai trò người tạo hoặc người chủ trì.\n' + NO_EDIT + '\n' + LOCKED + '\n'
        'During:\n– Kiểm tra dữ liệu như FR-06 / FR-07.\n– Nếu có lỗi validate → không thực hiện bước After.\n'
        'After:\n– Lưu trạng thái Lên lịch; ghi lịch sử “Đổi trạng thái”.\n'
        '– Gửi thông báo lịch họp cho toàn bộ thành viên nội bộ.\n– Hiển thị “Cập nhật thành công” / “Thêm mới thành công”.'),
       ('Bấm Lưu và Chốt lịch', 'Click',
        'Before:\n– Như trên.\n'
        'During:\n– Hình thức Trực tiếp, chưa có phòng, Địa điểm trống → “Bắt buộc phải nhập”.\n'
        'After:\n– Lưu trạng thái Chốt lịch; ghi lịch sử “Đổi trạng thái”.\n'
        '– Gửi thông báo chốt lịch cho toàn bộ thành viên nội bộ; hiển thị “Cập nhật thành công”.'),
   ])

# ---------------------------------------------------------------- 2.11 Xác nhận tham dự
fr(11, 'FR-11', 'Xác nhận tham dự', 'action', A_TV,
   ('- Thông báo và UI/UX. Chỉ bổ sung các quy tắc riêng tại phần mô tả chi tiết.', 'notice'),
   dict(ten='Xác nhận tham dự trước cuộc họp',
        mota='Thành viên nội bộ tự xác nhận Có mặt hoặc báo Vắng có lý do trước giờ họp, ngay trên màn chi tiết hoặc '
             'trên dòng thông báo ở chuông.',
        tacnhan='Thành viên nội bộ',
        dieukien='Người dùng có tên trong Thành phần — Phía Công ty; cuộc họp Lên lịch / Chốt lịch; chưa tới giờ bắt đầu.',
        chinh='1. Người dùng mở chi tiết cuộc họp (bấm Mã meeting hoặc thông báo chuông).\n'
              '2. Hệ thống hiện dòng “Xác nhận tham dự” kèm badge trạng thái hiện tại.\n'
              '3. Người dùng bấm “Có mặt”, hoặc “Vắng có lý do” rồi nhập lý do và bấm “Xác nhận”.\n'
              '4. Hệ thống ghi nhận vào cột điểm danh của chính người đó, báo “Xác nhận tham dự thành công” / “Đã báo '
              'vắng mặt”.',
        phu='• Lựa chọn đang áp dụng thì ẩn nút của chính nó; vẫn đổi lại được trước giờ họp.\n'
            '• Đang “Vắng có lý do” → có nút bút chì “Sửa lý do vắng mặt” (mở lại hộp, điền sẵn lý do cũ).\n'
            '• Hết điều kiện → ẩn nút, hiện lý do khóa, vd “Cuộc họp đã đến giờ bắt đầu, việc chốt điểm danh thuộc về '
            'người chủ trì.”'),
   [MENU + ' => Mã meeting => Có mặt / Vắng có lý do'],
   [('06_confirm_attend.png', 'Dòng Xác nhận tham dự trên màn hình Chi tiết meeting')],
   [
       ('Nhãn “Xác nhận tham dự”', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', 'Chỉ hiện với thành viên nội bộ.'),
       ('Badge trạng thái', 'Badge', 'Read-only', '4 giá trị', '–', 'Chưa phản hồi',
        'Đã xác nhận: Có mặt · Đã báo: Vắng có lý do - <lý do> · Vắng không lý do · Chưa phản hồi.'),
       ('Nút Có mặt', 'Button', 'Enable / Ẩn', '–', '–', 'Hiển thị', 'Ẩn khi đang là Có mặt.'),
       ('Nút Vắng có lý do', 'Button', 'Enable / Ẩn', '–', '–', 'Hiển thị', 'Ẩn khi đang là Vắng có lý do.'),
       ('Hộp “Báo vắng mặt cuộc họp”', 'Modal', 'Hiển thị', '–', '–', 'Ẩn',
        '“Bạn báo vắng mặt cuộc họp này. Vui lòng nhập lý do để người chủ trì nắm được.” + nút Xác nhận / Hủy.'),
       ('Ghi chú / Lý do', 'Textarea', 'Enable', '–', 'Có', 'Lý do cũ', 'Gợi ý “Nhập lý do vắng mặt”.'),
       ('Dòng lý do khóa', 'Label', 'Hiển thị', '–', '–', 'Ẩn', 'Biểu tượng ổ khóa + lý do không xác nhận được.'),
   ], 'input',
   [
       ('Bấm Có mặt', 'Click',
        'Before:\n– Kiểm tra người dùng có tên trong Thành phần — Phía Công ty; không có → “Bạn không nằm trong Thành phần '
        'tham gia nội bộ của cuộc họp này.”\n'
        'During:\n– Cuộc họp không ở Lên lịch / Chốt lịch → “Cuộc họp không ở trạng thái Lên lịch / Chốt lịch nên không xác '
        'nhận tham dự được.”\n– Đã tới giờ bắt đầu → “Cuộc họp đã đến giờ bắt đầu, việc chốt điểm danh thuộc về người chủ trì.”\n'
        'After:\n– Ghi điểm danh Có mặt cho dòng của chính người dùng; hiển thị “Xác nhận tham dự thành công”.'),
       ('Bấm Vắng có lý do → Xác nhận', 'Click',
        'During:\n– Lý do trống → “Vui lòng nhập lý do vắng mặt”.\n– Các điều kiện như trên.\n'
        'After:\n– Ghi Vắng có lý do + lý do; hiển thị “Đã báo vắng mặt”; cập nhật luôn tab Điểm danh.'),
   ])

# ---------------------------------------------------------------- 2.12 Điểm danh
fr(12, 'FR-12', 'Điểm danh', 'action', A_CT,
   ('- Validate dữ liệu, Thông báo và UI/UX. Logic ghi lịch sử áp dụng theo SRS Các quy tắc chung - Quy tắc ghi '
    'lịch sử.', 'create'),
   dict(ten='Điểm danh thành viên',
        mota='Người tạo / người chủ trì chốt trạng thái tham dự từng thành viên (nội bộ và khách hàng) ở tab Điểm danh.',
        tacnhan='Người tạo meeting, Người chủ trì',
        dieukien='Cuộc họp ở trạng thái Chốt lịch, đang mở màn Sửa.',
        chinh='1. Người dùng mở màn Sửa cuộc họp đã Chốt lịch, chọn tab “Điểm danh”.\n'
              '2. Người dùng bấm “Điểm danh nhanh: Tất cả có mặt” hoặc chọn trạng thái cho từng người.\n'
              '3. Người dùng nhập Ghi chú / Lý do nếu vắng.\n'
              '4. Người dùng bấm “Lưu” (hoặc “Hoàn thành”).\n'
              '5. Hệ thống lưu điểm danh, ghi lịch sử “Chỉnh sửa”, báo “Cập nhật thành công”.',
        phu='• Trạng thái khác Chốt lịch hoặc đang ở màn chi tiết → tab chỉ đọc, hiện “Có mặt / Vắng có lý do / Vắng không '
            'lý do / Chưa điểm danh”.\n'
            '• Họp nội bộ → không liệt kê thành viên phía khách hàng.\n'
            '• Chưa có thành viên → “Chưa có thành viên nào để điểm danh”.\n'
            '• Lựa chọn thành viên tự xác nhận trước giờ họp (FR-11) hiện sẵn ở đây.'),
   [MENU + ' => Sửa => Điểm danh'],
   [('07_attendance.png', 'Tab Điểm danh')],
   [
       ('Nút Điểm danh nhanh: Tất cả có mặt', 'Button', 'Enable / Ẩn', '–', '–', 'Hiện khi sửa được',
        'Đặt mọi thành viên = Có mặt.'),
       ('Cột STT / Họ và tên / Chức vụ / Phòng ban', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu', '–'),
       ('Cột Thành phần', 'Badge', 'Read-only', 'Nội bộ / Khách hàng', '–', 'Theo dữ liệu', '–'),
       ('Cột Trạng thái điểm danh', 'Radio (chip)', 'Enable', 'Có mặt / Vắng có lý do / Vắng không lý do', 'Có khi Hoàn thành',
        'Chưa điểm danh', 'Chọn 1 trong 3.'),
       ('Cột Ghi chú / Lý do', 'Textbox', 'Enable', '–', 'Không', 'Trống', 'Gợi ý “Nhập text tại đây...”; lý do dài cắt “...”, '
        'rê chuột xem đủ.'),
       ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Lưu điểm danh cùng toàn bộ form.'),
   ], 'input',
   [
       ('Bấm Điểm danh nhanh', 'Click', 'After:\n– Đặt mọi dòng = Có mặt (chưa lưu).'),
       ('Chọn trạng thái từng người', 'Click', 'After:\n– Đổi trạng thái dòng tương ứng (chưa lưu).'),
       ('Bấm Lưu', 'Click',
        'Before:\n– Kiểm tra vai trò người tạo hoặc người chủ trì.\n' + NO_EDIT + '\n' + LOCKED + '\n' + OVERDUE + '\n'
        'After:\n– Lưu trạng thái điểm danh và ghi chú; ghi lịch sử “Chỉnh sửa”.\n– Hiển thị “Cập nhật thành công”.'),
   ])

# ---------------------------------------------------------------- 2.13 Lập biên bản
fr(13, 'FR-13', 'Lập biên bản', 'crud', A_CT,
   ('- Validate dữ liệu, Thông báo và UI/UX. Logic ghi lịch sử áp dụng theo SRS Các quy tắc chung - Quy tắc ghi '
    'lịch sử.', 'create'),
   dict(ten='Lập biên bản cuộc họp',
        mota='Nhập nội dung biên bản ở tab Biên bản: các nội dung trao đổi (người đề xuất, người thực hiện, hạn), tài '
             'liệu đính kèm, kết luận; với loại “Họp tìm hiểu & Giới thiệu sản phẩm” có thêm khối Khảo sát nhu cầu '
             'khách hàng. Mục I–III do hệ thống tự thêm khi in.',
        tacnhan='Người tạo meeting, Người chủ trì',
        dieukien='Người dùng là người tạo / người chủ trì; cuộc họp chưa Hoàn thành / Hủy, chưa quá hạn nhập biên bản.',
        chinh='1. Người dùng mở màn Sửa, chọn tab “Biên bản”.\n'
              '2. Tại “Các nội dung khác”, bấm “Thêm dòng”, nhập Nội dung / Vấn đề trao đổi, Phương án xử lý, chọn Người đề '
              'xuất, Người thực hiện, Hạn dự kiến.\n'
              '3. Tại “Tài liệu đính kèm”, bấm “Thêm tài liệu”, nhập tên, bấm “Chọn tệp”.\n'
              '4. Nhập “Kết luận”.\n'
              '5. Bấm “Lưu” (hoặc “Hoàn thành”). Hệ thống lưu, ghi lịch sử, báo “Cập nhật thành công”.',
        phu='• Cuộc họp đã kết thúc và đang chờ biên bản → banner vàng “Hạn nhập biên bản: <hạn>” / “Vui lòng cập nhật biên '
            'bản và bấm Hoàn thành trước hạn. Quá hạn, cuộc họp sẽ tự động chuyển sang trạng thái Hủy và không tính vào KPI.”; '
            'quá hạn → banner đỏ “Đã quá hạn nhập biên bản”.\n'
            '• Bấm “Xoá hết” → bỏ toàn bộ dòng nội dung (chưa lưu).\n'
            '• Tệp đã tải lên: xem trước (ảnh/PDF), tải xuống, thay đổi, xóa.',
        dacbiet='Tệp nhận .jpg, .jpeg, .png, .doc, .docx, .xls, .xlsx, .pdf; được tải lên ngay khi chọn.'),
   [MENU + ' => Sửa => Biên bản'],
   [('08_report.png', 'Tab Biên bản ở màn Sửa meeting'),
    ('13_deadline_banner.png', 'Banner hạn nhập biên bản')],
   [
       ('Banner hạn nhập biên bản', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        'Chỉ hiện khi đã qua giờ kết thúc và cuộc họp còn Lên lịch / Chốt lịch.'),
       ('Nút In / Excel', 'Button', 'Enable', '–', '–', 'Hiện khi đã lưu', 'FR-17 / FR-18.'),
       ('Mục I/ Thông tin cuộc họp, II/ Thời gian, III/ Thành phần tham gia', 'Label', 'Read-only', '–', '–', 'Hiển thị',
        '“(Phần mềm tự động thêm khi in)”.'),
       ('Khối Khảo sát nhu cầu khách hàng', 'Radio / Dropdown / Number / Datepicker', 'Enable / Ẩn', '–',
        'Có khi Hoàn thành', 'Ẩn', 'Chỉ với loại meeting “Họp tìm hiểu & Giới thiệu sản phẩm”: nhu cầu đầu tư, lĩnh vực, '
        'nhóm ngành, mức đầu tư dự kiến, thời gian dự kiến bắt đầu, nhu cầu sửa chữa/bảo trì.'),
       ('Nút Thêm dòng / Xoá hết', 'Button', 'Enable / Ẩn', '–', '–', 'Hiện khi sửa', '–'),
       ('Nội dung / Vấn đề trao đổi', 'Textarea', 'Enable', '1–1000 ký tự', 'Có', 'Trống', 'Gợi ý “Nội dung trao đổi...”.'),
       ('Phương án xử lý', 'Textarea', 'Enable', '0–2000 ký tự', 'Không', 'Trống', '–'),
       ('Người đề xuất', 'Popup chọn', 'Enable', '1 người', 'Không', 'Trống', 'Chọn 1 người.'),
       ('Người thực hiện', 'Popup chọn', 'Enable', '≥ 1 người', 'Có', 'Trống', 'Chọn nhiều người.'),
       ('Hạn dự kiến', 'Datepicker', 'Enable', 'dd/mm/yyyy, ≥ hôm nay', 'Có', 'Trống', '–'),
       ('Nút Thêm tài liệu', 'Button', 'Enable / Ẩn', '–', '–', 'Hiện khi sửa', '–'),
       ('Tên tài liệu', 'Textbox', 'Enable', '1–255 ký tự', 'Có', 'Trống', 'Gợi ý “Nhập tên tài liệu...”.'),
       ('Upload / File', 'File', 'Enable', '.jpg .jpeg .png .doc .docx .xls .xlsx .pdf', 'Có khi Hoàn thành', 'Trống',
        'Nút “Chọn tệp”; đang tải hiện “Đang tải lên...”.'),
       ('Dung lượng', 'Text', 'Read-only', '–', '–', 'Theo tệp', '–'),
       ('V/ Kết luận', 'Textarea (soạn thảo)', 'Enable', '–', 'Có khi Hoàn thành', 'Trống',
        'Ghi chú cam “Bắt buộc nhập kết luận cuộc họp khi hoàn thành”.'),
   ], 'input',
   [
       ('Bấm Thêm dòng / Thêm tài liệu', 'Click', 'After:\n– Thêm 1 dòng trống cuối bảng.'),
       ('Chọn tệp', 'Change', 'After:\n– Tải tệp lên kho lưu trữ, hiện tên tệp và dung lượng; lỗi → thông báo lỗi.'),
       ('Bấm Lưu', 'Click',
        'Before:\n– Kiểm tra vai trò người tạo hoặc người chủ trì.\n' + NO_EDIT + '\n' + LOCKED + '\n' + OVERDUE + '\n'
        'During:\n– Nội dung trống → “Bắt buộc phải nhập”; quá 1000 ký tự → “Vui lòng nhập tối đa 1000 ký tự.”\n'
        '– Người thực hiện trống → “Bắt buộc phải nhập”.\n– Hạn dự kiến trống → “Bắt buộc phải nhập”; nhỏ hơn hôm nay (khi '
        'cuộc họp đang Lên lịch) → “Phải lớn hơn hoặc bằng ngày hiện tại.”\n– Tên tài liệu trống → “Bắt buộc phải nhập”.\n'
        '– Nếu có lỗi validate → không thực hiện bước After.\n'
        'After:\n– Lưu biên bản, tài liệu, kết luận; ghi lịch sử “Chỉnh sửa”.\n– Hiển thị “Cập nhật thành công”.'),
   ])

# ---------------------------------------------------------------- 2.14 Giao nhiệm vụ
fr(14, 'FR-14', 'Giao nhiệm vụ từ biên bản', 'action', A_CT,
   ('- Màn Thêm mới, Thông báo. Chỉ bổ sung các quy tắc riêng tại phần mô tả chi tiết.', 'create'),
   dict(ten='Giao nhiệm vụ từ dòng biên bản',
        mota='Tạo nhiệm vụ từ một dòng “Các nội dung khác” của biên bản đã lưu, kế thừa sẵn tên, người thực hiện, hạn và '
             'cuộc họp; dòng hiện số nhiệm vụ đã giao.',
        tacnhan='Người xem được cuộc họp (theo quy tắc của chức năng Nhiệm vụ)',
        dieukien='Đang ở màn Chi tiết meeting, tab Biên bản; dòng biên bản đã được lưu.',
        chinh='1. Người dùng bấm biểu tượng “Giao nhiệm vụ” ở cột Thao tác của dòng biên bản.\n'
              '2. Hệ thống mở cửa sổ “Thêm mới nhiệm vụ” điền sẵn: Tên công việc = Phương án xử lý (trống thì lấy Nội dung), '
              'Người thực hiện = những người thực hiện là nhân viên, Hạn hoàn thành = Hạn dự kiến, Meeting = cuộc họp hiện tại.\n'
              '3. Người dùng bổ sung thông tin và lưu nhiệm vụ.\n'
              '4. Dòng biên bản hiện “Đã giao n nhiệm vụ”.',
        phu='• 1 người thực hiện → Nhiệm vụ cụ thể; nhiều người → Nhiệm vụ chung (mỗi người 1 bản ghi).\n'
            '• Người thực hiện ngoài công ty bị bỏ qua.\n'
            '• Bấm “Đã giao n nhiệm vụ” → mở danh sách nhiệm vụ đã giao, bấm 1 dòng để xem nhiệm vụ.'),
   [MENU + ' => Mã meeting => Biên bản => Giao nhiệm vụ'],
   [('n10b_report_show_row.png', 'Tab Biên bản ở màn chi tiết — cột Thao tác có nút Giao nhiệm vụ'),
    ('n12_assign_task.png', 'Cửa sổ Thêm mới nhiệm vụ được điền sẵn từ dòng biên bản')],
   [
       ('Nút Giao nhiệm vụ', 'Icon Button', 'Enable / Ẩn', '–', '–', 'Hiện với dòng đã lưu', 'Ở cột Thao tác (chỉ màn chi tiết).'),
       ('Nhãn “Đã giao n nhiệm vụ”', 'Badge', 'Enable / Ẩn', '≥ 1', '–', 'Ẩn khi chưa giao', 'Bấm mở danh sách nhiệm vụ đã giao.'),
       ('Loại nhiệm vụ', 'Dropdown', 'Enable', 'Nhiệm vụ cụ thể / chung', 'Có', 'Theo số người thực hiện', '–'),
       ('Tên công việc', 'Textbox', 'Enable', '–', 'Có', 'Phương án xử lý / Nội dung', '–'),
       ('Meeting', 'Text', 'Read-only', '–', '–', '<Tên meeting> (<mã>)', '–'),
       ('Người thực hiện', 'Dropdown', 'Enable', 'Nhân viên', 'Có', 'Người thực hiện của dòng', '–'),
       ('Hạn hoàn thành / Giờ hạn', 'Datepicker', 'Enable', 'dd/mm/yyyy hh:mm', 'Có', 'Hạn dự kiến', '–'),
       ('Nút Lưu / Lưu & Tiếp tục / Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Theo chức năng Nhiệm vụ.'),
   ], 'input',
   [
       ('Bấm Giao nhiệm vụ', 'Click', 'After:\n– Mở cửa sổ Thêm mới nhiệm vụ với giá trị kế thừa từ dòng biên bản.'),
       ('Lưu nhiệm vụ', 'Click',
        'Before / During:\n– Kiểm tra quyền và dữ liệu theo quy tắc của chức năng Nhiệm vụ.\n'
        'After:\n– Tạo nhiệm vụ gắn cuộc họp + dòng biên bản; dòng hiện “Đã giao n nhiệm vụ”.'),
       ('Bấm Đã giao n nhiệm vụ', 'Click', 'After:\n– Mở danh sách nhiệm vụ đã giao từ dòng đó.'),
   ])

# ---------------------------------------------------------------- 2.15 Hoàn thành
fr(15, 'FR-15', 'Hoàn thành meeting', 'action', A_CT,
   ('- Validate dữ liệu, Thông báo. Logic ghi lịch sử áp dụng theo SRS Các quy tắc chung - Quy tắc ghi lịch sử.', 'history'),
   dict(ten='Hoàn thành meeting',
        mota='Chốt biên bản và chuyển cuộc họp sang Hoàn thành; sau đó cuộc họp không sửa được nữa và người được giao '
             'việc trong biên bản nhận thông báo.',
        tacnhan='Người tạo meeting, Người chủ trì',
        dieukien='Cuộc họp Chốt lịch; đã tới giờ bắt đầu; đang mở màn Sửa.',
        chinh='1. Người dùng điểm danh đủ thành viên (FR-12) và nhập biên bản, kết luận (FR-13).\n'
              '2. Người dùng bấm “Hoàn thành”.\n'
              '3. Hệ thống kiểm tra đủ các mục bắt buộc.\n'
              '4. Hệ thống lưu trạng thái Hoàn thành, ghi lịch sử “Đổi trạng thái”, gửi thông báo cho người thực hiện trong '
              'biên bản, báo “Cập nhật thành công” và quay về màn nguồn.',
        phu='• Còn thiếu → thông báo “Vui lòng nhập đầy đủ:” liệt kê từng mục (mỗi mục 1 dòng), tự chuyển tới tab chứa mục '
            'thiếu đầu tiên. Các mục: “Điểm danh (còn n thành viên chưa điểm danh)”, “Khảo sát nhu cầu khách hàng - …”, “Các '
            'nội dung khác (thêm ít nhất 1 dòng)”, “Các nội dung khác dòng n - Nội dung / Vấn đề trao đổi, Người thực hiện, Hạn '
            'dự kiến”, “Tài liệu đính kèm dòng n - Tên tài liệu, Upload / File”, “Kết luận”.\n'
            '• Chưa tới giờ bắt đầu → nút Hoàn thành mờ, rê chuột hiện “Chỉ được xác nhận hoàn thành khi cuộc họp đã bắt đầu”.'),
   [MENU + ' => Sửa => Hoàn thành'],
   [('09_complete.png', 'Cuộc họp ở trạng thái Đã hoàn thành')],
   [
       ('Nút Hoàn thành', 'Button', 'Enable / Disable / Ẩn', '–', '–', 'Hiện khi Chốt lịch',
        'Mờ kèm chú thích khi chưa tới giờ bắt đầu.'),
       ('Thông báo “Vui lòng nhập đầy đủ:”', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        'Liệt kê mọi mục còn thiếu, hiện 5–15 giây tùy số mục.'),
       ('Điểm danh mọi thành viên', 'Radio (chip)', 'Enable', '3 giá trị', 'Có', 'Theo dữ liệu', 'Nội bộ + khách hàng (Họp đối tác).'),
       ('Biên bản ≥ 1 dòng đủ Nội dung, Người thực hiện, Hạn dự kiến', 'Table/Grid', 'Enable', '–', 'Có', 'Theo dữ liệu', '–'),
       ('Tài liệu đính kèm đủ Tên + File', 'Table/Grid', 'Enable', '–', 'Có với dòng đã thêm', 'Theo dữ liệu', '–'),
       ('Kết luận', 'Textarea', 'Enable', '–', 'Có', 'Theo dữ liệu', '–'),
       ('Khảo sát nhu cầu khách hàng', 'Radio / Dropdown', 'Enable / Ẩn', '–', 'Có với loại Họp tìm hiểu & Giới thiệu sản phẩm',
        'Theo dữ liệu', '–'),
   ], 'input',
   [
       ('Bấm Hoàn thành', 'Click',
        'Before:\n– Kiểm tra vai trò người tạo hoặc người chủ trì.\n' + NO_EDIT + '\n' + LOCKED + '\n' + OVERDUE + '\n'
        'During:\n– Thiếu mục bắt buộc → “Vui lòng nhập đầy đủ:” + danh sách mục, dừng.\n'
        '– Chưa tới giờ bắt đầu → “Chỉ được xác nhận hoàn thành khi cuộc họp đã bắt đầu”.\n'
        '– Còn thành viên chưa điểm danh → “Vui lòng hoàn thành điểm danh cho tất cả thành viên trước khi chốt biên bản và '
        'hoàn thành cuộc họp.”\n– Kết luận trống → “Bắt buộc phải nhập”.\n'
        '– Khảo sát: “Vui lòng trả lời câu hỏi về nhu cầu đầu tư của khách hàng.”, “Vui lòng trả lời câu hỏi về nhu cầu dịch '
        'vụ sửa chữa, bảo dưỡng/bảo trì.”, “Vui lòng chọn ít nhất một lĩnh vực.”, “Vui lòng chọn ít nhất một nhóm ngành.”, '
        '“Vui lòng nhập mức đầu tư dự kiến.”, “Vui lòng chọn thời gian dự kiến bắt đầu.”\n'
        'After:\n– Lưu trạng thái Hoàn thành; ghi lịch sử “Đổi trạng thái”.\n'
        '– Gửi thông báo giao việc cho từng người thực hiện là nhân viên trong biên bản.\n'
        '– Hiển thị “Cập nhật thành công”, quay về màn nguồn.'),
   ])

# ---------------------------------------------------------------- 2.16 Hủy
fr(16, 'FR-16', 'Hủy meeting', 'action', A_TAO,
   ('- Thông báo. Logic ghi lịch sử áp dụng theo SRS Các quy tắc chung - Quy tắc ghi lịch sử.', 'history'),
   dict(ten='Hủy meeting',
        mota='Người tạo hủy cuộc họp đã Lên lịch / Chốt lịch trước giờ bắt đầu, bắt buộc chọn lý do từ danh mục “Lý do hủy '
             'cuộc họp”, ghi chú tùy chọn.',
        tacnhan='Người tạo meeting',
        dieukien='Người dùng là người tạo; cuộc họp Lên lịch / Chốt lịch; chưa tới giờ bắt đầu.',
        chinh='1. Người dùng bấm “Hủy” ở chân màn Chi tiết hoặc Sửa.\n'
              '2. Hệ thống mở cửa sổ “Xác nhận hủy cuộc họp” (dòng mô tả “Cuộc họp: <mã> - <tên>”).\n'
              '3. Người dùng chọn Lý do hủy cuộc họp, nhập Ghi chú (nếu có).\n'
              '4. Người dùng bấm “Xác nhận hủy”.\n'
              '5. Hệ thống chuyển Hủy, ghi lý do, người và thời điểm hủy, ghi lịch sử, gửi thông báo cho thành viên, báo '
              '“Cập nhật thành công” và quay về màn nguồn.',
        phu='• Chưa chọn lý do → “Vui lòng chọn lý do hủy cuộc họp” dưới ô.\n'
            '• Lý do vừa bị khóa → “Lý do hủy đã bị khóa hoặc không còn tồn tại, vui lòng chọn lại.”, giữ cửa sổ mở để chọn lại.\n'
            '• Đã tới giờ bắt đầu → nút Hủy mờ, rê chuột hiện “Cuộc họp đã đến giờ bắt đầu, không hủy được nữa”.\n'
            '• Bấm “Đóng” → không hủy.'),
   [MENU + ' => Mã meeting => Hủy', MENU + ' => Sửa => Hủy'],
   [('12_cancel.png', 'Cửa sổ Xác nhận hủy cuộc họp')],
   [
       ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Xác nhận hủy cuộc họp', 'Dòng mô tả “Cuộc họp: <mã> - <tên>”.'),
       ('Cảnh báo', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '“Bạn có chắc chắn muốn hủy cuộc họp này không?”'),
       ('Lý do hủy cuộc họp', 'Dropdown', 'Enable', 'Danh mục đang hoạt động', 'Có', 'Trống',
        'Gợi ý “Chọn lý do hủy cuộc họp”.'),
       ('Ghi chú', 'Textarea', 'Enable', '0–1000 ký tự', 'Không', 'Trống',
        'Gợi ý “Nhập thêm chi tiết lý do hủy (không bắt buộc)”.'),
       ('Nút Xác nhận hủy', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị', 'Màu đỏ; khóa trong lúc gửi.'),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng, không hủy.'),
   ], 'input',
   [
       ('Bấm Hủy', 'Click', 'After:\n– Mở cửa sổ, nạp danh mục lý do đang hoạt động; lỗi → “Lỗi khi tải danh mục lý do hủy '
        'cuộc họp”.'),
       ('Bấm Xác nhận hủy', 'Click',
        'Before:\n– Kiểm tra người dùng là người tạo; không phải → “Bạn không có quyền thay đổi trạng thái meeting này!”.\n'
        'During:\n– Chưa chọn lý do → “Vui lòng chọn lý do hủy cuộc họp”.\n'
        '– Cuộc họp không ở Lên lịch / Chốt lịch → “Cuộc họp không ở trạng thái cho phép hủy.”\n'
        '– Đã tới giờ bắt đầu → “Cuộc họp đã đến giờ bắt đầu, không hủy được nữa”.\n'
        '– Lý do khóa / không tồn tại → “Lý do hủy đã bị khóa hoặc không còn tồn tại, vui lòng chọn lại.”\n'
        'After:\n– Lưu trạng thái Hủy, lý do, ghi chú, thời điểm và người hủy; nhả phiếu đặt phòng.\n'
        '– Ghi lịch sử “Đổi trạng thái” kèm lý do hủy.\n– Gửi thông báo hủy (kèm lý do) cho thành viên nội bộ.\n'
        '– Hiển thị “Cập nhật thành công”, quay về màn nguồn; lỗi → nội dung lỗi hoặc “Cập nhật thất bại”.'),
       ('Bấm Đóng', 'Click', 'After:\n– Đóng cửa sổ.'),
   ])

# ---------------------------------------------------------------- 2.17 In biên bản
fr(17, 'FR-17', 'In biên bản', 'io', A_TV,
   ('- Thông báo và UI/UX. Chỉ bổ sung các quy tắc riêng tại phần mô tả chi tiết.', 'notice'),
   dict(ten='In biên bản cuộc họp',
        mota='In “BIÊN BẢN CUỘC HỌP (MEETING RECORD)” theo 2 bước: chọn phần cần in → xem trước → In. Dùng chung ở danh '
             'sách, màn chi tiết và tab Biên bản.',
        tacnhan='Người xem được cuộc họp',
        dieukien='Cuộc họp đã được lưu; người dùng xem được cuộc họp.',
        chinh='1. Người dùng bấm “In biên bản” ở cột Hành động (hoặc link ở cột Biên bản, nút In ở màn chi tiết / tab Biên bản).\n'
              '2. Hệ thống mở cửa sổ “Cấu hình in biên bản”, tích sẵn mọi phần có dữ liệu.\n'
              '3. Người dùng chọn phần cần in, tích “Chỉ in người điểm danh có mặt” nếu cần, bấm “Xem trước”.\n'
              '4. Hệ thống mở “Xem trước biên bản cuộc họp” (Số biên bản, Ngày lập biên bản, các mục I–V).\n'
              '5. Người dùng bấm “In” để in.',
        phu='• Chưa tích phần nào → “Vui lòng chọn ít nhất 1 phần để xuất”.\n'
            '• Không tải được dữ liệu → “Không thể tải biên bản” / “Lỗi khi tải biên bản”.\n'
            '• Phần Dự án / Thành phần tham dự không có dữ liệu thì không có trong danh sách chọn; Khảo sát chỉ có với loại '
            '“Họp tìm hiểu & Giới thiệu sản phẩm”.'),
   [MENU + ' => Hành động khác => In biên bản', MENU + ' => Mã meeting => In'],
   [('10_print_config.png', 'Cửa sổ Cấu hình in biên bản'),
    ('11_print_preview.png', 'Cửa sổ Xem trước biên bản cuộc họp')],
   [
       ('Tiêu đề cửa sổ bước 1', 'Label', 'Hiển thị', '–', '–', 'Cấu hình in biên bản', '–'),
       ('Chọn tất cả', 'Checkbox', 'Enable', '–', '–', 'Tích', 'Tích / bỏ toàn bộ, gồm cả tùy chọn con.'),
       ('Danh sách phần', 'Checkbox', 'Enable', 'Tối đa 8 phần', 'Có (≥ 1)', 'Tích hết',
        'Thông tin chung cuộc họp, Tài liệu chuẩn bị cho buổi họp, Dự án, Thành phần tham dự, Biên bản cuộc họp, Tài liệu '
        'đính kèm, Khảo sát nhu cầu khách hàng, Kết luận cuộc họp.'),
       ('Chỉ in người điểm danh có mặt', 'Checkbox', 'Enable / Disable', '–', 'Không', 'Tích',
        'Tùy chọn con của Thành phần tham dự; khóa khi bỏ tích phần cha.'),
       ('Nút Xem trước / Huỷ', 'Button', 'Enable', '–', '–', 'Hiển thị', '–'),
       ('Cửa sổ Xem trước biên bản cuộc họp', 'Modal', 'Read-only', '–', '–', 'Ẩn',
        'Tiêu đề, Số biên bản, Ngày lập biên bản, các mục đã chọn; nút “In” ở tiêu đề.'),
   ], 'input',
   [
       ('Bấm In biên bản', 'Click',
        'After:\n– Tải dữ liệu chi tiết cuộc họp; mở bước 1; lỗi → “Không thể tải biên bản” / “Lỗi khi tải biên bản”.'),
       ('Bấm Xem trước', 'Click',
        'During:\n– Không phần nào được tích → “Vui lòng chọn ít nhất 1 phần để xuất”.\n'
        'After:\n– Đóng bước 1, mở cửa sổ xem trước với đúng các phần đã chọn.'),
       ('Bấm In', 'Click', 'After:\n– Mở hộp thoại in của trình duyệt với nội dung biên bản.'),
   ])

# ---------------------------------------------------------------- 2.18 Xuất Excel biên bản
fr(18, 'FR-18', 'Xuất Excel biên bản', 'io', A_TV,
   ('- Quy tắc Excel và Cấu hình cột. Chỉ bổ sung các quy tắc riêng tại phần mô tả chi tiết.', 'excel'),
   dict(ten='Xuất Excel biên bản cuộc họp',
        mota='Xuất biên bản của 1 cuộc họp ra file “Bien_ban_cuoc_hop_<mã>.xlsx” (sheet “Biên bản cuộc họp”) với các phần '
             'người dùng chọn.',
        tacnhan='Người xem được cuộc họp',
        dieukien='Đang ở tab Biên bản của cuộc họp đã lưu.',
        chinh='1. Người dùng bấm “Excel” ở tab Biên bản.\n'
              '2. Hệ thống mở cửa sổ “Cấu hình xuất Excel biên bản”.\n'
              '3. Người dùng chọn phần cần xuất, bấm “Xuất Excel”.\n'
              '4. Hệ thống tạo file và tải về máy.',
        phu='• Chưa tích phần nào → “Vui lòng chọn ít nhất 1 phần để xuất”.\n'
            '• Lỗi → “Lỗi khi xuất Excel biên bản”.\n• Bấm “Huỷ” → không xuất.'),
   [MENU + ' => Mã meeting => Biên bản => Excel'],
   [('n11_excel_config.png', 'Cửa sổ Cấu hình xuất Excel biên bản')],
   [
       ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Cấu hình xuất Excel biên bản', 'Nhãn “Chọn phần cần xuất”.'),
       ('Chọn tất cả', 'Checkbox', 'Enable', '–', '–', 'Tích', '–'),
       ('Danh sách phần', 'Checkbox', 'Enable', 'Như FR-17 (không có “Chỉ in người điểm danh có mặt”)', 'Có (≥ 1)',
        'Tích hết', '–'),
       ('Nút Xuất Excel / Huỷ', 'Button', 'Enable', '–', '–', 'Hiển thị', '–'),
   ], 'input',
   [
       ('Bấm Excel', 'Click', 'After:\n– Mở cửa sổ cấu hình.'),
       ('Bấm Xuất Excel', 'Click',
        'During:\n– Không phần nào được tích → “Vui lòng chọn ít nhất 1 phần để xuất”.\n'
        'After:\n– Dựng file trên trình duyệt từ dữ liệu đang hiển thị, tải “Bien_ban_cuoc_hop_<mã>.xlsx”.\n'
        '– Lỗi → “Lỗi khi xuất Excel biên bản”.'),
   ])

# ---------------------------------------------------------------- 2.19 Đăng ký phòng họp
fr(19, 'FR-19', 'Đăng ký phòng họp', 'action', A_TAO,
   ('- Màn Thêm mới, Validate dữ liệu, Thông báo. Chỉ bổ sung các quy tắc riêng tại phần mô tả chi tiết.', 'create'),
   dict(ten='Đăng ký / đổi / hủy đăng ký phòng họp cho cuộc họp',
        mota='Giữ phòng họp nội bộ cho cuộc họp bằng popup “Đăng ký phòng họp” dùng chung với màn Đăng ký phòng họp. Mở từ '
             'nút trên thanh công cụ (tự chọn cuộc họp), từ menu dòng (“Đăng ký phòng họp” / “Đổi phòng họp”, cuộc họp '
             'đặt sẵn) hoặc từ khối Phòng họp ở màn Sửa.',
        tacnhan='Người tạo meeting, Người chủ trì',
        dieukien='Cuộc họp đã lưu, ở trạng thái Lên lịch / Chốt lịch; người dùng là người tạo hoặc người chủ trì.',
        chinh='1. Người dùng bấm “Đăng ký phòng họp” trên thanh công cụ (hoặc trên menu dòng / nút “Đăng ký phòng” ở màn Sửa).\n'
              '2. Hệ thống mở popup, hướng đăng ký “Gắn với cuộc họp”.\n'
              '3. Người dùng chọn Cuộc họp (nếu chưa đặt sẵn), lọc nhanh theo sức chứa / tiện nghi, chọn Phòng họp.\n'
              '4. Người dùng bấm “Lưu đăng ký” (hoặc “Lưu và gửi duyệt” với phòng cần duyệt).\n'
              '5. Hệ thống tạo phiếu, báo “Đăng ký phòng thành công”, nạp lại danh sách để cột Phòng họp hiện phòng vừa giữ.',
        phu='• Ở màn Sửa có thêm nút “Hủy đăng ký” → hộp “Hủy đăng ký phòng”, xong báo “Đã hủy đăng ký phòng”.\n'
            '• Không đủ điều kiện → khối Phòng họp hiện lý do: “Lưu cuộc họp trước rồi mới đăng ký phòng được.”, “Lên lịch '
            'xong mới đăng ký phòng được (bản nháp còn đổi giờ).”, “Cuộc họp đã hoàn thành.”, “Cuộc họp đã hủy.”, “Chỉ người '
            'tạo cuộc họp hoặc người chủ trì mới đăng ký được phòng.”\n'
            '• Phiếu bị từ chối → “Lý do từ chối: <lý do>. Vui lòng đăng ký phòng khác.”\n'
            '• Lỗi → nội dung lỗi hoặc “Đăng ký phòng thất bại”.',
        dacbiet='Chi tiết luật trống/bận phòng, duyệt phiếu áp dụng theo SRS màn Đăng ký phòng họp.'),
   [MENU + ' => Đăng ký phòng họp'],
   [('n08_booking.png', 'Popup Đăng ký phòng họp mở từ thanh công cụ')],
   [
       ('Hướng đăng ký', 'Radio', 'Enable / Disable', 'Gắn với cuộc họp / Nhu cầu khác', 'Có', 'Gắn với cuộc họp',
        'Khóa khi mở cho 1 cuộc họp cụ thể.'),
       ('Cuộc họp', 'Dropdown', 'Enable / Disable', 'Danh sách', 'Có', 'Trống / cuộc họp đặt sẵn',
        'Gợi ý “Chọn cuộc họp cần đặt phòng”.'),
       ('Sức chứa tối thiểu / Tiện nghi cần có', 'Number / Dropdown', 'Enable', '≥ 0', 'Không', 'Trống',
        'Lọc nhanh danh sách phòng, không lưu vào phiếu.'),
       ('Phòng họp', 'Dropdown', 'Enable', 'Danh sách', 'Có', 'Trống', 'Gợi ý “Chọn phòng họp”.'),
       ('Thời gian (theo cuộc họp)', 'Text', 'Read-only', '–', '–', 'Theo cuộc họp', '“Chọn cuộc họp để xem thời gian”.'),
       ('Thông tin phòng / Giờ bận – giờ rảnh trong ngày', 'Label', 'Read-only', '–', '–', 'Theo phòng', '–'),
       ('Nút Lưu đăng ký / Lưu và gửi duyệt', 'Button', 'Enable', '–', '–', 'Hiển thị', '–'),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '–'),
   ], 'input',
   [
       ('Bấm Đăng ký phòng họp / Đổi phòng họp', 'Click', 'After:\n– Mở popup (đặt sẵn cuộc họp nếu mở từ dòng).'),
       ('Bấm Lưu đăng ký', 'Click',
        'Before:\n– Chỉ người tạo / người chủ trì cuộc họp; cuộc họp từ Lên lịch, chưa Hoàn thành / Hủy.\n'
        'During:\n– Kiểm tra phòng trống, khung giờ, sức chứa theo quy tắc Đăng ký phòng họp.\n'
        'After:\n– Tạo phiếu đặt phòng; hiển thị “Đăng ký phòng thành công”; nạp lại danh sách.'),
       ('Bấm Hủy đăng ký (màn Sửa)', 'Click', 'After:\n– Xác nhận rồi hủy phiếu; “Đã hủy đăng ký phòng” / “Hủy đăng ký phòng thất bại”.'),
   ])

# ---------------------------------------------------------------- 2.20 Tạo phiếu công tác khác
fr(20, 'FR-20', 'Tạo phiếu công tác khác', 'action', A_TV,
   ('- Màn Thêm mới. Chỉ bổ sung các quy tắc riêng tại phần mô tả chi tiết.', 'create'),
   dict(ten='Tạo phiếu công tác khác từ cuộc họp',
        mota='Mở màn tạo phiếu giao công tác ở TAB MỚI, gắn sẵn cuộc họp (và địa điểm họp nếu bấm từ màn chi tiết) để '
             'lập phiếu đi công tác cho buổi họp.',
        tacnhan='Người xem được cuộc họp',
        dieukien='Cuộc họp chưa Hoàn thành / Hủy.',
        chinh='1. Người dùng bấm “Hành động khác” (⋮) ở dòng, chọn “Tạo phiếu công tác khác” (hoặc nút cùng tên ở màn chi tiết).\n'
              '2. Hệ thống mở tab mới: màn tạo phiếu giao công tác, điền sẵn cuộc họp.\n'
              '3. Người dùng hoàn tất phiếu theo quy tắc của chức năng Giao công tác.',
        phu='• Mở từ màn chi tiết → truyền thêm địa điểm và tọa độ cuộc họp; địa điểm nhập tay thì phải chọn lại địa điểm đến.\n'
            '• Cuộc họp Hoàn thành / Hủy → không có lựa chọn này.'),
   [MENU + ' => Hành động khác => Tạo phiếu công tác khác'],
   [('n02_row_menu.png', 'Menu Hành động khác của một dòng meeting')],
   [
       ('Nút Hành động khác (⋮)', 'Icon Button', 'Enable / Ẩn', '–', '–', 'Hiện khi dòng có từ 4 hành động', 'Mở menu.'),
       ('Mục Tạo phiếu công tác khác', 'Button', 'Enable / Ẩn', '–', '–', 'Hiện khi chưa Hoàn thành / Hủy', 'Mở tab mới.'),
       ('Nút Tạo phiếu công tác khác (chi tiết)', 'Button', 'Enable / Ẩn', '–', '–', 'Hiện khi chưa Hoàn thành / Hủy', '–'),
   ], 'input',
   [
       ('Bấm Tạo phiếu công tác khác', 'Click',
        'After:\n– Mở tab mới màn tạo phiếu giao công tác, gắn sẵn cuộc họp (kèm địa điểm khi bấm ở màn chi tiết).'),
   ])

# ---------------------------------------------------------------- 2.21 Lịch sử
fr(21, 'FR-21', 'Xem lịch sử thay đổi', 'view', A_TV,
   ('- Quy tắc ghi lịch sử và Màn Xem chi tiết. Chỉ bổ sung các quy tắc riêng tại phần mô tả chi tiết.', 'history'),
   dict(ten='Xem lịch sử thay đổi meeting',
        mota='Xem dòng thời gian các lần tạo / chỉnh sửa / đổi trạng thái của 1 cuộc họp: thời điểm, người thực hiện, '
             'trường thay đổi (giá trị cũ → mới), lý do hủy. Mở ở popup “Lịch sử lịch meeting” từ danh sách hoặc khối Lịch '
             'sử ở cuối màn chi tiết (cùng nội dung).',
        tacnhan='Người xem được cuộc họp; Người dùng đã đăng nhập',
        dieukien='Người dùng xem được cuộc họp.',
        chinh='1. Người dùng bấm “Lịch sử” ở cột Hành động (hoặc “Xem lịch sử” ở màn chi tiết).\n'
              '2. Hệ thống mở popup “Lịch sử lịch meeting”, dòng “Lịch meeting: <tên>”.\n'
              '3. Hệ thống hiển thị các lần thay đổi từ mới đến cũ.\n'
              '4. Người dùng bấm “Bộ lọc” để lọc theo loại hành động, người thực hiện, từ ngày / đến ngày.',
        phu='• Chưa có lịch sử → “Chưa có lịch sử thao tác nào.”\n• Nội dung dài → “Xem thêm”.'),
   [MENU + ' => Hành động khác => Lịch sử'],
   [('n03_history.png', 'Popup Lịch sử lịch meeting')],
   [
       ('Tiêu đề popup', 'Label', 'Hiển thị', '–', 'Lịch sử lịch meeting', 'Dòng xám “Lịch meeting: <tên>”.'),
       ('Nút Bộ lọc', 'Button', 'Enable', '–', 'Thu gọn', 'Mở các ô lọc.'),
       ('Loại hành động', 'Dropdown', 'Enable', 'Tạo mới / Chỉnh sửa / Đổi trạng thái', 'Trống', 'Gợi ý “Chọn loại hành động”.'),
       ('Người thực hiện', 'Dropdown', 'Enable', 'Danh sách', 'Trống', 'Gợi ý “Chọn người thực hiện”.'),
       ('Từ ngày / Đến ngày', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Trống', '–'),
       ('Dòng thời gian', 'Table/Grid', 'Read-only', '–', 'Mới → cũ',
        'Thời điểm, hành động (màu theo nhóm), người thực hiện — phòng ban, danh sách trường đổi (cũ đỏ → mới xanh), thành '
        'phần / biên bản / tệp thêm mới, sửa, xóa.'),
       ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn', '“Chưa có lịch sử thao tác nào.”'),
       ('Nút đóng (×)', 'Icon Button', 'Enable', '–', 'Hiển thị', 'Đóng popup; lần mở sau tải lại.'),
   ], 'read',
   [
       ('Bấm Lịch sử', 'Click', 'After:\n– Mở popup, tải lịch sử của đúng cuộc họp.'),
       ('Đổi bộ lọc', 'Change', 'After:\n– Lọc lại dòng thời gian.'),
       ('Đóng popup', 'Click', 'After:\n– Xóa dữ liệu tạm, lần mở sau tải lại.'),
   ], uc=False)

# ============================================================== PHẦN 4
d.h1('Phần 4. Quy tắc nghiệp vụ')
d.rule_ref('. Phần này chỉ ghi các quy tắc đặc thù của màn Tổng hợp meeting; không lặp lại các quy tắc đã có trong '
           'SRS quy tắc chung.', anchor='list', head='Quy tắc áp dụng',
           lead='Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ')
d.rule_table([
    ('BR-01', 'Vòng đời trạng thái', [
        '– Đang tạo (Lưu nháp) → Lên lịch → Chốt lịch → Hoàn thành; Lên lịch / Chốt lịch có thể chuyển Hủy.',
        '– Có thể lưu thẳng Lên lịch hoặc Chốt lịch ngay khi tạo; Hoàn thành chỉ từ Chốt lịch trên giao diện.',
        '– Hoàn thành và Hủy là trạng thái cuối: không sửa, không điểm danh, không lập biên bản được nữa.',
        '– Màu badge: Đang tạo #64748B · Lên lịch #0EA5E9 · Chốt lịch #2563EB · Hoàn thành #16A34A · Hủy #6B7280.',
    ], 'Toàn màn hình'),
    ('BR-02', 'Phạm vi xem cuộc họp', [
        '– Luôn xem được cuộc họp mình tạo, mình chủ trì hoặc có tên trong Thành phần — Phía Công ty.',
        '– Ngoài ra theo quyền V1–V4 (tổng công ty / công ty / phòng ban / bộ phận theo cấp tổ chức của người tạo).',
        '– Cuộc họp Đang tạo chỉ người tạo và người chủ trì thấy.',
    ], ['Xem danh sách', 'Xem chi tiết', 'Xuất Excel']),
    ('BR-03', 'Thao tác theo vai trò', [
        '– Sửa, Lên lịch, Chốt lịch, Điểm danh, Lập biên bản, Hoàn thành, Đăng ký phòng: người tạo hoặc người chủ trì.',
        '– Hủy, Xóa: chỉ người tạo. Quyền xem cấp cao không cho phép thao tác trên cuộc họp của người khác.',
        '– Nút không dùng được thì ẩn hẳn; người chỉ tham gia mở màn Sửa sẽ được chuyển sang màn Chi tiết.',
    ], 'Toàn màn hình'),
    ('BR-04', 'Sinh mã meeting', [
        '– <Mã công ty>.MET.<KH|NB>.<YY>.<NNNN>: KH khi loại meeting có khách hàng, NB khi nội bộ.',
        '– STT 4 chữ số tăng dần theo năm và công ty của người tạo (không tách KH/NB); qua năm hoặc công ty khác đếm lại.',
    ], 'Tạo mới'),
    ('BR-05', 'Ràng buộc thời gian', [
        '– Tạo mới: Bắt đầu, Kết thúc ≥ thời điểm hiện tại; Kết thúc > Bắt đầu.',
        '– Sửa: cuộc họp đang Lên lịch thì Bắt đầu ≥ hiện tại; trạng thái khác thì Bắt đầu ≥ thời điểm tạo meeting; Kết thúc ≥ Bắt đầu.',
        '– Hạn dự kiến dòng biên bản ≥ hôm nay khi cuộc họp còn Lên lịch.',
    ], ['Tạo mới', 'Chỉnh sửa', 'Lập biên bản']),
    ('BR-06', 'Địa điểm và phòng họp', [
        '– Địa điểm meeting bắt buộc từ bước Chốt lịch khi Hình thức Trực tiếp và chưa có phòng họp.',
        '– Đã có phòng họp thì ẩn ô Địa điểm (phòng chính là địa điểm); giá trị địa điểm cũ được giữ nguyên.',
        '– Đăng ký phòng chỉ từ Lên lịch, chưa Hoàn thành / Hủy, do người tạo hoặc người chủ trì; hủy / xóa cuộc họp thì nhả phòng.',
    ], ['Tạo mới', 'Chỉnh sửa', 'Đăng ký phòng họp']),
    ('BR-07', 'Khách hàng và người liên hệ', [
        '– Loại meeting có khách hàng: bắt buộc Khách hàng; khách hàng doanh nghiệp bắt buộc Tên + SĐT người liên hệ.',
        '– SĐT người liên hệ / thành phần: bắt đầu bằng 0, 10–12 chữ số.',
        '– Khách hàng cá nhân hoặc người liên hệ đang được nhân viên kinh doanh khác đăng ký còn hạn thì không chọn mới được '
        '(giữ nguyên giá trị cũ khi sửa thì không chặn).',
    ], ['Tạo mới', 'Chỉnh sửa']),
    ('BR-08', 'Người chủ trì và thành phần', [
        '– Người chủ trì mặc định là người tạo, luôn được đưa vào Thành phần — Phía Công ty và không xóa được khỏi danh sách.',
        '– Thành phần — Phía Công ty bắt buộc ≥ 1 người; thứ tự kéo thả được dùng chung cho tab Điểm danh và bản in.',
    ], ['Tạo mới', 'Chỉnh sửa']),
    ('BR-09', 'Xác nhận tham dự và điểm danh', [
        '– Thành viên nội bộ tự xác nhận khi cuộc họp Lên lịch / Chốt lịch và trước giờ bắt đầu; Vắng có lý do bắt buộc lý do.',
        '– Từ giờ bắt đầu, việc chốt điểm danh thuộc về người tạo / người chủ trì ở tab Điểm danh (chỉ khi Chốt lịch).',
        '– Họp nội bộ không điểm danh thành viên phía khách hàng.',
    ], ['Xác nhận tham dự', 'Điểm danh']),
    ('BR-10', 'Điều kiện Hoàn thành', [
        '– Đã tới giờ bắt đầu; mọi thành viên đã điểm danh (Có mặt / Vắng có lý do / Vắng không lý do).',
        '– Biên bản ≥ 1 dòng đủ Nội dung, Người thực hiện, Hạn dự kiến; tài liệu đã thêm phải đủ tên + file; có Kết luận.',
        '– Loại “Họp tìm hiểu & Giới thiệu sản phẩm”: trả lời đủ khảo sát nhu cầu (lĩnh vực, nhóm ngành, mức đầu tư, thời gian).',
        '– Sau khi Hoàn thành, mỗi người thực hiện là nhân viên trong biên bản nhận thông báo giao việc.',
    ], 'Hoàn thành meeting'),
    ('BR-11', 'Điều kiện Hủy', [
        '– Chỉ người tạo; chỉ khi Lên lịch / Chốt lịch và trước giờ bắt đầu — không có ngoại lệ theo quyền.',
        '– Bắt buộc chọn lý do từ danh mục “Lý do hủy cuộc họp” đang hoạt động; ghi chú tùy chọn (≤ 1000 ký tự).',
        '– Hiển thị lý do dạng “<Tên lý do> — <ghi chú>”, kèm người và thời điểm hủy.',
    ], 'Hủy meeting'),
    ('BR-12', 'Hạn nhập biên bản và tự động hủy', [
        '– Hạn = giờ kết thúc + số ngày cấu hình của công ty sở hữu cuộc họp (mặc định 1 ngày).',
        '– Trước hạn số giờ cấu hình (mặc định 3 giờ), hệ thống nhắc người tạo meeting.',
        '– Quá hạn mà cuộc họp còn Lên lịch / Chốt lịch: chặn mọi cập nhật; tác vụ tự động chuyển cuộc họp sang Hủy và báo '
        'người tạo cùng thành viên nội bộ.',
    ], ['Lập biên bản', 'Hoàn thành meeting']),
    ('BR-13', 'Xóa cuộc họp', [
        '– Chỉ cuộc họp Đang tạo, chỉ người tạo; xóa hẳn kèm thành phần, biên bản, người thực hiện, tài liệu (cả file), liên '
        'kết và câu trả lời biểu mẫu dự án TKT.',
    ], 'Xóa meeting'),
    ('BR-14', 'Thông báo', [
        '– Lên lịch / Chốt lịch / Hủy: báo toàn bộ Thành phần — Phía Công ty, tiền tố [MET].',
        '– Bấm Lưu khi đã Lên lịch / Chốt lịch: đổi giờ → báo mọi thành viên nội bộ; thêm / bớt người → chỉ báo người liên quan.',
        '– Cuộc họp Chốt lịch đổi giờ phải xác nhận “Xác nhận gửi lịch” trước khi lưu.',
    ], ['Tạo mới', 'Chỉnh sửa', 'Lên lịch và chốt lịch', 'Hủy meeting']),
    ('BR-15', 'Danh mục bị khóa', [
        '– Loại meeting / Ứng dụng đã khóa không chọn mới được; cuộc họp đang dùng giá trị đã khóa vẫn hiển thị và lưu lại '
        'bình thường (trừ khi cuộc họp còn Đang tạo).',
    ], ['Tạo mới', 'Chỉnh sửa', 'Tìm kiếm và lọc']),
    ('BR-16', 'Ghi lịch sử', [
        '– Ghi mọi lần Tạo mới, Chỉnh sửa (giá trị cũ → mới, cả thành phần, biên bản, tệp) và Đổi trạng thái (kèm lý do hủy).',
        '– Ai xem được cuộc họp thì xem được lịch sử; không gắn quyền riêng.',
    ], 'Xem lịch sử thay đổi'),
])

d.save(update_fields=os.environ.get('SRS_NO_WORD') != '1')
