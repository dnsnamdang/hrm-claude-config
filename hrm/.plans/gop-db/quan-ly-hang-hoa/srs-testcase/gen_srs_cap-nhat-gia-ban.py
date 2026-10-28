# -*- coding: utf-8 -*-
"""Sinh SRS - Cap nhat gia ban (luong Chuyen doi hang hoa) — form chuan 2026-09-24.

Pham vi: man "Cap nhat gia ban" (Tai chinh > Quan ly gia - CTKM > Gia ban, quyen 1657) — xem danh sach bo gia
theo cong ty, tim kiem va loc, nhap gia + luu tung khoi (hang x DVT), giá hieu luc, gui duyet gia ban (cong ty
bat duyet gia), popup Lich su gia, popup Cong thuc lap rap. Tap trung cac quy tac GIA BAN (phep tinh T1-T11,
gia theo cong ty, trang thai hang trong luong tinh gia, co cho duyet / khong duyet).

Nguon doi chieu code: worktree wt-chuyen-doi-hang-hoa nhanh feat/chuyen-doi-hang-hoa
(hrm-api 39c4a91fe, hrm-client 5c14659e8) — doc ngay 16/10/2026.
  BE: Modules/MasterData/Routes/api.php (nhom product-prices), ProductPriceController, Services/ProductPrice/
      {ProductPriceListService, ProductPriceUpdateService, ProductPriceWriter, ProductPriceApprovalSubmitter,
      ProductPriceHistoryService, ProductPriceSetWriter, ProductPriceNotifier}
  FE: pages/finance/product-prices/index.vue, components/product/price/{ProductPriceTable, ProductPriceHistoryModal,
      ProductRecipeModal}.vue, utils/productPriceModel.js, components/subsystem-menu/finance.js

Anh chup: Playwright MCP 1440x900, cong 3031 (worktree, DB hrm_erp_giacty), tai khoan E2E Assign (co san quyen 1657
tai Cty 1 — KHONG tao role tam). Du lieu THAT (28.371 hang Dang KD tai Cty 1, hang TEWI-AQUA). KHONG ghi DB:
  - 05/06/07/08: sua tren trinh duyet, khong bam Luu (06: Luu bi chan o FE, 0 request ghi).
  - 09-khoi-bi-khoa: MINH HOA — chan request Luu tren trinh duyet, tra cau "Hang hoa dang ngung kinh doanh..."
    (dung cau may chu) de thay trang thai khoi bi khoa; khong co hang Ngung KD that o Cty 1.
  - 11/12 nut + popup Gui duyet: MINH HOA — 8 cong ty dev deu TAT duyet gia, nen sua phan hoi danh sach tren trinh
    duyet (bat co "can gui duyet") roi bam Gui duyet, bam Huy (0 request ghi).
  - 13 co Khong duyet: du lieu that (loc deep-link ?status=2).
  - 15-lich-su-gia: anh THAT chup luc kiem G4 (10/10/2026, `.playwright-mcp/g4/history-1440.png`); DB dev hien khong
    con dong lich su gia nao (G4 da tra du lieu sau khi kiem).

Chay:  python3 .plans/gop-db/quan-ly-hang-hoa/srs-testcase/gen_srs_cap-nhat-gia-ban.py
"""
import os
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
HRM = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
sys.path.insert(0, os.path.join(HRM, '.claude', 'skills', 'srs-documenter', 'assets'))
from srs_docx_lib import SrsDoc  # noqa: E402

SHOTS = os.path.join(HERE, 'cap-nhat-gia-ban_shots')
OUT = os.path.join(HERE, 'SRS - Cập nhật giá bán.docx')


def shot(name):
    return os.path.join(SHOTS, name)


ACTOR = 'Nhân viên cập nhật giá bán'
MENU = 'Phân hệ Tài chính => Quản lý giá - CTKM => Giá bán => Cập nhật giá bán'
SCREEN = 'Cập nhật giá bán'

d = SrsDoc(out=OUT, menu=MENU, route='/finance/product-prices',
           full_url='http://hrm/finance/product-prices', img_prefix='cngb_')
d.set_menu_icons({k: shot(v) for k, v in {
    'Phân hệ Tài chính': 'icon_phanhe.png',
    'Quản lý giá - CTKM': 'icon_rail_quanlygia.png',
    'Giá bán': 'icon_nhom_giaban.png',
    'Cập nhật giá bán': 'icon_capnhatgiaban.png',
    'Tìm kiếm nâng cao': 'icon_timkiem.png',
    'Lưu': 'icon_luu.png',
    'Gửi duyệt': 'icon_guiduyet.png',
    'Lịch sử giá': 'icon_lichsu.png',
    'Xem công thức lắp ráp': 'icon_congthuc.png',
    'Thêm lý do sửa giá': 'icon_lydo.png',
    'Hiệu lực': 'icon_hieuluc.png',
}.items()})

MSG_NOPERM = 'Bạn không có quyền thực hiện chức năng này.'
LOCK_MSGS = [
    '– Hàng đã bị xoá → “Hàng hoá không tồn tại hoặc đã bị xoá.”',
    '– Công ty đang làm việc chưa dùng hàng → “Hàng hoá chưa dùng ở công ty đang làm việc.”',
    '– Đang nhập thông tin → “Hàng hoá đang nhập thông tin, chưa được nhập giá.”',
    '– Chờ tính giá bán → “Hàng hoá đang chờ tính giá, chưa được cập nhật giá.”',
    '– Đang tính giá → “Hàng hoá đang tính giá, chưa được cập nhật giá.”',
    '– Ngừng kinh doanh → “Hàng hoá đang ngừng kinh doanh, vui lòng mở khoá trước khi cập nhật.”',
    '– Trạng thái khác → “Hàng hoá chưa ở trạng thái đang kinh doanh, chưa được cập nhật giá.”',
    '– Giá của ĐVT đang có yêu cầu duyệt sinh từ Phiếu tính giá → “Giá đang chờ duyệt ở <mã phiếu tính giá>.”',
]

# ============================================================== TRANG DAU
d.title_block(SCREEN)
d.h2('Mục lục')
d.toc()

# ========================================================= PHAN 1
d.h1('Phần 1. Giới thiệu')
d.h2('1 Mục đích')
d.p('Tài liệu này đặc tả yêu cầu phần mềm cho màn hình Cập nhật giá bán (phân hệ Tài chính) thuộc luồng Chuyển đổi '
    'hàng hoá sang hệ thống mới, nhằm:')
d.bullets([
    'Là căn cứ nghiệm thu chức năng và phân quyền của màn Cập nhật giá bán.',
    'Làm rõ GIÁ BÁN THEO CÔNG TY: mỗi công ty có bộ giá riêng cho từng đơn vị tính (6 loại giá bán + giá vốn), chỉ '
    'thấy và chỉ sửa bộ giá của công ty đang làm việc.',
    'Làm rõ các phép tính tự động khi nhập giá (hệ số → giá, Bán lẻ lan sang các loại giá khác, giá Thương mại điện tử, '
    'giá công thức, giá hiệu lực) để nghiệp vụ và tester đối chiếu được từng con số.',
    'Làm rõ hai nhánh khi bấm lưu: LƯU THẲNG (công ty không bật duyệt giá) và GỬI DUYỆT (công ty bật duyệt giá), cùng '
    'cách hiển thị giá Chờ duyệt / Không duyệt.',
    'Làm rõ quan hệ với vòng đời hàng hoá: chỉ hàng Đang kinh doanh mới cập nhật giá được; hàng Đang nhập thông tin, '
    'Chờ tính giá bán, Đang tính giá, Ngừng kinh doanh bị chặn.',
])

d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('Công ty đang làm việc', 'Công ty người dùng đang chọn ở góc trên màn hình. Quyền, danh sách hàng, bộ giá, tồn kho, '
     'quy định duyệt giá và lịch sử đều xét theo công ty này.'),
    ('Khối giá', '1 hàng hoá × 1 đơn vị tính (ĐVT) đang chọn: giá vốn + 6 dòng loại giá + các dòng giá hiệu lực. '
     'Lưu theo từng khối.'),
    ('6 loại giá', 'Bán lẻ · Giá bán theo lô · Đại lý cấp 1 · Đại lý cấp 2 · Đại lý cấp 3 · Thương mại điện tử (TMĐT, '
     'tên đầy đủ “Giá bán thương mại điện tử ( online)”).'),
    ('Giá vốn', 'Giá vốn của ĐVT tại công ty đang làm việc — là cơ sở tính giá theo hệ số.'),
    ('Hệ số', 'Hệ số nhân trên giá vốn để ra giá bán của một loại giá.'),
    ('Giá hiện tại', 'Giá đang áp dụng (đã duyệt) của loại giá.'),
    ('Giá mới', 'Ô nhập giá. Khi đang có đề nghị chờ duyệt hoặc bị từ chối, ô này hiện giá đề nghị đó.'),
    ('Giá công thức', 'Giá vốn × Hệ số (TMĐT làm tròn nghìn) — số tham chiếu, không lưu.'),
    ('ĐMGG', 'Định mức giảm giá tối đa (%) của loại giá, 0 – 100.'),
    ('Giá hiệu lực', 'Giá đặt trước cho 1 ngày trong tương lai; đến ngày đó hệ thống tự áp thành giá hiện tại. '
     'Tối đa 1 dòng cho mỗi loại giá.'),
    ('Sửa tay (TMĐT)', 'Ô tick ở dòng TMĐT cho từng trường Hệ số / Giá / ĐMGG. Không tick: trường đó tự tính theo Bán lẻ.'),
    ('Duyệt giá', 'Quy định của công ty (bật duyệt giá + phạm vi hãng sản xuất). Bật: bấm lưu là GỬI DUYỆT, giá chưa áp '
     'cho tới khi người có quyền Duyệt giá bán hàng hoá duyệt.'),
    ('Chờ duyệt / Không duyệt', 'Cờ của từng ô giá: đang có đề nghị chờ duyệt / đề nghị đã bị từ chối.'),
    ('PTG', 'Phiếu tính giá — phiếu ra giá bán cho hàng mới trong luồng tính giá.'),
    ('Đang kinh doanh', 'Trạng thái của hàng TẠI một công ty; chỉ trạng thái này mới hiện ở màn và cập nhật giá được.'),
], widths=[1.8, 4.2])

# ========================================================= PHAN 2
d.h1('Phần 2. Phân quyền')
d.h2('1 Danh sách quyền')
d.p('Mọi quyền xét theo CÔNG TY ĐANG LÀM VIỆC — có quyền ở công ty khác không được tính. Super admin không được '
    'miễn: thiếu quyền là không vào được màn.')
d.p('Nhóm quyền thao tác:')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('Q1', 'Cập nhật giá bán hàng hoá',
     'Thấy mục menu Cập nhật giá bán; mở được màn; xem bộ giá + giá vốn + tồn kho của công ty; nhập và Lưu / Gửi duyệt '
     'giá; xem Lịch sử giá. Đây là quyền DUY NHẤT của màn.'),
    ('Q2', 'Xem giá vốn hàng hoá',
     'KHÔNG có tác dụng ở màn này: người có Q1 luôn thấy và nhập được giá vốn của công ty mình (chốt mockup 09/10/2026); '
     'không có Q1 thì có Q2 cũng không vào được màn. Ghi vào bảng để tránh hiểu nhầm.'),
    ('Q3', 'Duyệt giá bán hàng hoá',
     'Không có tác dụng ở màn này (là quyền của màn Duyệt giá bán). Người có Q3 tại công ty là người NHẬN thông báo '
     '“[GIA] Chờ duyệt” khi có người Gửi duyệt giá từ màn này.'),
], widths=[0.8, 2.0, 3.2])
d.p('Màn không phân quyền theo cấp dữ liệu (công ty / phòng ban / bộ phận). Phạm vi dữ liệu cố định: hàng ĐANG KINH '
    'DOANH tại công ty đang làm việc, bộ giá của chính công ty đó.')
d.p('Popup Công thức lắp ráp đọc thông tin chi tiết hàng hoá (mở cho mọi người dùng) nên không cần quyền riêng.')

d.h2('2 Ma trận phân quyền')
d.table(['Chức năng', 'Q1', 'Q2', 'Q3', 'Không có quyền nào'], [
    ('FR-01 Xem danh sách giá bán', '✅', '❌', '❌', '❌ (không thấy menu; mở thẳng màn không hiện gì, không tải dữ liệu)'),
    ('FR-02 Tìm kiếm và lọc', '✅', '❌', '❌', '❌'),
    ('FR-03 Cập nhật giá bán', '✅', '❌', '❌', '❌ (hệ thống từ chối khi gọi lưu bỏ qua giao diện)'),
    ('FR-04 Thiết lập giá hiệu lực', '✅', '❌', '❌', '❌'),
    ('FR-05 Gửi duyệt giá bán', '✅ (khi công ty bật duyệt giá)', '❌', '❌ (chỉ nhận thông báo)', '❌'),
    ('FR-06 Xem lịch sử giá', '✅', '❌', '❌ (xem ở màn Duyệt giá bán)', '❌'),
    ('FR-07 Xem công thức lắp ráp', '✅', '❌ (cần Q1 để mở màn)', '❌', '❌'),
], widths=[2.1, 1.0, 0.9, 1.0, 1.0])

# ========================================================= PHAN 3
d.h1('Phần 3. Đặc tả chi tiết theo từng chức năng')
d.h2('1 Sơ đồ UML tổng quan')
d.overview_figure2(
    [(ACTOR, [0, 1, 2, 3])],
    [('FR-01', 'Xem danh sách giá bán', 'view'),
     ('FR-03', 'Cập nhật giá bán', 'crud'),
     ('FR-04', 'Thiết lập giá hiệu lực', 'crud'),
     ('FR-05', 'Gửi duyệt giá bán', 'action')],
    [('FR-02', 'Tìm kiếm và lọc', 'view', 'extend', [0], None),
     ('FR-06', 'Xem lịch sử giá', 'view', 'extend', [0], None),
     ('FR-07', 'Xem công thức lắp ráp', 'view', 'extend', [0], None)],
    'Sơ đồ Use Case tổng quan màn Cập nhật giá bán')

d.h2('2 Đặc tả chi tiết từng chức năng')

LIST_RULE = ('- Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột. Chỉ bổ sung các quy tắc riêng của màn '
             'Cập nhật giá bán tại phần mô tả chi tiết.')

# ------------------------------------------------------------------ 2.1
d.h3('2.1 Xem danh sách giá bán')
d.p('2.1.1 Giới thiệu')
d.rule_ref(LIST_RULE, anchor='list')
d.intro_table(
    ten='Xem danh sách giá bán',
    mota='Hiển thị các hàng hoá ĐANG KINH DOANH tại công ty đang làm việc, mỗi hàng là 1 khối giá (hàng × ĐVT đang chọn) '
         'gồm giá vốn, 6 loại giá (giá hiện tại, hệ số, giá công thức, giá mới, ĐMGG), giá hiệu lực, tồn kho công ty, '
         'mã, model, hãng sản xuất. Bảng là bảng nhập liệu tại chỗ.',
    tacnhan=ACTOR + '; Người dùng đã đăng nhập',
    dieukien='Người dùng có quyền Cập nhật giá bán hàng hoá tại công ty đang làm việc.',
    chinh='1. Người dùng vào menu Tài chính → Quản lý giá - CTKM → Giá bán → Cập nhật giá bán.\n'
          '2. Hệ thống lấy các hàng Đang kinh doanh tại công ty đang làm việc (chưa bị xoá), mã hàng mới nhất lên trước, '
          '20 hàng / trang.\n'
          '3. Mỗi hàng hiện khối giá của ĐVT đầu tiên (ĐVT cơ bản), bộ giá đọc đúng công ty đang làm việc.\n'
          '4. Sau khi bảng hiện, hệ thống tải tiếp tồn kho của các hàng trong trang (cột Tồn kho hiện “…” trong lúc tải).',
    phu='• Không có hàng Đang kinh doanh → “Chưa có hàng hoá Đang kinh doanh tại <tên công ty>.”.\n'
        '• Đang lọc mà không có kết quả → “Không có dữ liệu phù hợp”.\n'
        '• Không có quyền tại công ty đang làm việc → không thấy menu; mở thẳng màn thì màn không hiển thị, không tải dữ liệu.\n'
        '• Mở từ thông báo “[GIA] Đã duyệt / Từ chối” → màn chỉ hiện đúng hàng trong thông báo; thông báo Từ chối bật sẵn lọc '
        'Trạng thái duyệt = Không duyệt.\n'
        '• Lỗi tải → thông báo “Lỗi khi tải dữ liệu”.')
d.p('2.1.2 Layout màn hình')
d.layout(menu=MENU, shot=shot('01-danh-sach.png'), shot_caption='Màn Cập nhật giá bán lúc mới vào (dữ liệu thật)')
d.layout(menu=MENU, shot=shot('03-khoi-gia.png'),
         shot_caption='Một khối giá đầy đủ: giá vốn, 6 loại giá, giá hiện tại, hệ số, giá công thức, giá mới')
d.layout(menu=MENU, shot=shot('04-cot-ben-phai.png'),
         shot_caption='Phần bên phải bảng: ĐMGG, Hiệu lực, Tồn kho, Mã hàng hoá, Model, Hãng sản xuất')
d.p('2.1.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề trang', 'Label', 'Hiển thị', '–', 'Cập nhật giá bán', 'Tiêu đề trên thanh đầu trang và tiêu đề khối bảng.'),
    ('Dòng đếm cạnh tiêu đề', 'Text', 'Read-only', '≥ 0', 'Theo dữ liệu', [
        '- Mẫu: “· N hàng hoá đang kinh doanh tại <tên công ty đang làm việc>”.',
        '- N = tổng số hàng khớp bộ lọc (không phải số dòng trên trang).',
        '- Không đọc được tên công ty thì ghi “công ty đang làm việc”.']),
    ('Bảng giá bán', 'Table/Grid', 'Enable', '14 cột', 'Theo dữ liệu', [
        '- Tiêu đề 1 dòng, không xuống dòng; tiêu đề dính trên khi cuộn dọc.',
        '- Bảng có vùng cuộn riêng (dọc + ngang), 2 cột Tên hàng hoá và ĐVT · Lưu dính trái khi cuộn ngang.',
        '- Mỗi hàng là 1 khối nhiều dòng: 6 dòng loại giá theo thứ tự Bán lẻ, Giá bán theo lô, Đại lý cấp 1, Đại lý cấp 2, '
        'Đại lý cấp 3, Thương mại điện tử; dưới mỗi loại có thêm dòng con “Giá hiệu lực” nếu đã đặt.',
        '- Không sắp xếp theo cột (không có tiêu đề bấm sắp xếp).']),
    ('Cột Tên hàng hoá', 'Text', 'Read-only', '–', 'Theo dữ liệu', [
        '- Dòng 1: tên hàng; dòng 2: mã hàng (chữ xám).',
        '- “Lý do không duyệt: <lý do>”: chỉ hiện khi đề nghị giá gần nhất của ĐVT bị từ chối.',
        '- Link “Thêm lý do sửa giá” (hoặc “Lý do sửa giá” khi đã có lý do): bấm → mở ô nhập lý do ngay dưới (mục 2.3).',
        '- Link “Xem công thức lắp ráp”: chỉ hiện với hàng có công thức lắp ráp. Bấm → mở popup Công thức lắp ráp (mục 2.7).',
        '- Khối bị khoá (mục 2.3): thay các link bằng biểu tượng ổ khoá + câu lý do.']),
    ('Cột ĐVT · Lưu – ô chọn ĐVT', 'Dropdown', 'Enable / Disable', 'Danh sách ĐVT của hàng', 'ĐVT đầu tiên (ĐVT cơ bản)', [
        '- Mỗi lựa chọn dạng “<tên ĐVT> (x<hệ số quy đổi>)”, vd “Bộ (x1)”.',
        '- Hàng chỉ có 1 ĐVT hoặc khối bị khoá → ô bị khoá.',
        '- Đổi ĐVT → khối hiện bộ giá của ĐVT mới; ĐVT cũ đang sửa dở → hỏi “Thông tin chưa lưu” (mục 2.3).',
        '- Icon ⓘ: “Lưu theo TỪNG ĐVT đang chọn (1 khối = hàng × ĐVT). Đổi ĐVT khi chưa lưu sẽ hỏi lại.”']),
    ('Cột ĐVT · Lưu – nút Lưu / Gửi duyệt', 'Button', 'Enable / Ẩn', '–', 'Hiển thị', [
        '- Công ty KHÔNG bật duyệt giá (hoặc hãng không thuộc phạm vi duyệt): nút “Lưu” (biểu tượng đĩa) → mục 2.3.',
        '- Công ty bật duyệt giá với hãng của hàng: nút “Gửi duyệt” (biểu tượng máy bay giấy) → mục 2.5.',
        '- Luôn bấm được (kể cả khi chưa sửa gì); đang lưu 1 khối thì mọi nút tạm khoá.',
        '- Ẩn khi khối bị khoá.']),
    ('Cột ĐVT · Lưu – nút Lịch sử giá', 'Icon Button', 'Enable', '–', 'Hiển thị',
     ['- Biểu tượng đồng hồ, tooltip “Lịch sử giá”.', '- Bấm → mở popup Lịch sử giá bán (mục 2.6).']),
    ('Cột ĐVT · Lưu – nhãn “● Chưa lưu”', 'Label', 'Enable / Ẩn', '–', 'Ẩn',
     '- Chữ cam, hiện khi khối đang có thay đổi chưa lưu (khác bản đã tải).'),
    ('Cột Giá vốn', 'Number', 'Enable / Disable', '0 – 999.999.999.999', 'Giá vốn của công ty', [
        '- Ô nhập số tiền, có dấu phẩy ngăn nghìn, không có số lẻ.',
        '- Hiện giá vốn của ĐVT TẠI CÔNG TY ĐANG LÀM VIỆC; có đề nghị giá vốn chờ duyệt / bị từ chối thì hiện giá đề nghị.',
        '- Kèm nhãn “Chờ duyệt” (cam) hoặc “Không duyệt” (đỏ) khi có cờ; dưới đó “Đang áp dụng: <giá vốn đang chạy>” nếu khác.',
        '- Hiện với mọi người có quyền Cập nhật giá bán hàng hoá (không xét quyền Xem giá vốn hàng hoá).',
        '- Sửa giá vốn KHÔNG tự tính lại giá bán, chỉ cột Giá công thức đổi theo.']),
    ('Cột Loại giá', 'Text', 'Read-only', 'Danh sách 6 giá trị', 'Theo thứ tự cố định', [
        '- Tên loại giá; rê chuột dòng TMĐT thấy tên đầy đủ “Giá bán thương mại điện tử ( online)”.',
        '- Nhãn cờ “Chờ duyệt” / “Không duyệt” của dòng (1 nhãn / dòng, theo cờ cao nhất của giá, hệ số, ĐMGG).',
        '- Link “+ Hiệu lực” (tooltip “Thêm giá hiệu lực (tối đa 1 / loại giá)”): chỉ hiện ở 5 loại giá trừ TMĐT, khi loại '
        'giá chưa có giá hiệu lực và khối không bị khoá. Bấm → thêm dòng giá hiệu lực (mục 2.4).',
        '- Dòng TMĐT có “Sửa tay:” + 3 ô tick Hệ số / Giá / ĐMGG (mục 2.3).']),
    ('Cột Giá hiện tại', 'Number', 'Read-only', '≥ 0', 'Theo dữ liệu', [
        '- Giá đang áp dụng của loại giá tại công ty đang làm việc (dấu phẩy ngăn nghìn).',
        '- Dòng giá hiệu lực: để trống.',
        '- Icon ⓘ: “Giá đang áp dụng (đã duyệt). Ô "Giá mới" có thể đang hiện giá chờ duyệt / giá bị từ chối.”']),
    ('Cột Hệ số', 'Number', 'Enable / Disable', '0 – < 100, tối đa 2 số lẻ', 'Theo dữ liệu', [
        '- Nhập hệ số → Giá mới tự tính = làm tròn trăm (hệ số × giá vốn) (BR-06).',
        '- Hệ số của Bán lẻ lan sang 4 loại Giá bán theo lô, Đại lý cấp 1–3 (BR-07).',
        '- Dòng TMĐT: bị khoá trừ khi tick Sửa tay Hệ số; khi khoá = hệ số Bán lẻ × 1,3 (BR-08).']),
    ('Cột Giá công thức', 'Number', 'Read-only', '≥ 0', 'Theo dữ liệu', [
        '- = Giá vốn × Hệ số của dòng; dòng TMĐT làm tròn nghìn; không lưu, chỉ để tham chiếu.',
        '- Icon ⓘ: “Giá vốn × Hệ số. Riêng Thương mại điện tử làm tròn nghìn.”']),
    ('Cột Giá mới', 'Number', 'Enable / Disable', '0 – 999.999.999.999', 'Theo dữ liệu', [
        '- Giá sẽ lưu cho loại giá. Có đề nghị chờ duyệt / bị từ chối → hiện giá đề nghị đó (khác Giá hiện tại).',
        '- Giá Bán lẻ lan sang 4 loại giá 2–5 (BR-07).',
        '- Dòng TMĐT: bị khoá trừ khi tick Sửa tay Giá; khi khoá = làm tròn (giá Bán lẻ × 1,3).']),
    ('Cột ĐMGG (%)', 'Number', 'Enable / Disable', '0 – 100, tối đa 2 số lẻ', 'Theo dữ liệu', [
        '- Bỏ trống được. Ngoài 0 – 100 → báo đỏ, không tự kẹp.',
        '- ĐMGG Bán lẻ lan sang 4 loại giá 2–5. Dòng TMĐT: khoá, = 0 trừ khi tick Sửa tay ĐMGG.',
        '- Icon ⓘ: “Định mức giảm giá tối đa (%), 0 – 100.”']),
    ('Cột Hiệu lực', 'Text', 'Read-only / Enable', 'dd/mm/yyyy', 'Đang áp dụng', [
        '- Dòng loại giá: chữ xanh “Đang áp dụng”.',
        '- Dòng giá hiệu lực: ô chọn ngày + nút ✕ đỏ “Xoá giá hiệu lực” (mục 2.4).']),
    ('Cột Tồn kho', 'Number', 'Read-only', '≥ 0', '“…” khi đang tải', [
        '- Tồn kho kế toán của CÔNG TY ĐANG LÀM VIỆC (cộng mọi kho kế toán của công ty), quy đổi theo ĐVT đang chọn '
        '(tồn ĐVT cơ bản ÷ hệ số quy đổi, tối đa 2 số lẻ).',
        '- Icon ⓘ: “Tồn kho kế toán của công ty đang làm (mọi kho kế toán của công ty), quy đổi theo ĐVT đang chọn.”']),
    ('Cột Mã hàng hoá', 'Text', 'Read-only', '–', 'Theo dữ liệu', [
        '- Mã hàng là link: bấm → mở màn Xem chi tiết hàng hoá ở TAB MỚI (màn giá giữ nguyên, không mất nháp).',
        '- “Công khoán: <số>” và “Ghi chú: <ghi chú hàng hoá>” chỉ đọc, hiện khi có.']),
    ('Cột Model', 'Text', 'Read-only', '–', 'Theo dữ liệu', 'Tên model của hàng.'),
    ('Cột Hãng sản xuất', 'Text', 'Read-only', '–', 'Theo dữ liệu', 'Tên hãng sản xuất của hàng.'),
    ('Chân bảng', 'Pagination', 'Enable', '10 / 20 / 50', '20 dòng / trang', [
        '- “Hiển thị a–b / N hàng hoá”: a, b là hàng đầu / cuối trang; N là tổng số hàng khớp bộ lọc.',
        '- Ô “Số dòng/trang” 10 / 20 / 50; đổi → về trang 1.',
        '- Đổi trang / số dòng khi còn khối chưa lưu → hỏi “Thông tin chưa lưu”.']),
    ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn', [
        '- Chưa lọc: “Chưa có hàng hoá Đang kinh doanh tại <tên công ty>.”',
        '- Đang lọc: “Không có dữ liệu phù hợp”.']),
    ('Đang tải', 'Loading', 'Hiển thị', '–', 'Ẩn', '“Đang tải…” trong bảng. Lỗi tải: thông báo “Lỗi khi tải dữ liệu”.'),
], required=False)
d.p('2.1.4 Danh sách event và xử lý event')
d.event_table([
    ('Mở màn hình', 'System',
     'Before:\n– Kiểm tra quyền Cập nhật giá bán hàng hoá tại công ty đang làm việc.\n'
     '– Không có quyền → màn không hiển thị và không tải dữ liệu; gọi thẳng chức năng thì hệ thống báo “' + MSG_NOPERM + '”.\n'
     'During:\n– Lấy hàng Đang kinh doanh tại công ty đang làm việc, chưa bị xoá; dựng bộ giá + giá vốn của CÔNG TY ĐÓ cho từng ĐVT.\n'
     '– Mở từ thông báo: chỉ lấy đúng hàng trong thông báo (thông báo Từ chối bật sẵn lọc Không duyệt).\n'
     'After:\n– Hiện trang 1 (20 hàng), mỗi hàng hiện ĐVT đầu tiên.\n– Tải tồn kho của các hàng trong trang.'),
    ('Đổi trang / số dòng mỗi trang', 'Click / Change',
     'Before:\n– Còn khối chưa lưu → hỏi “Thông tin chưa lưu”; chọn Ở lại → không đổi trang.\n'
     'After:\n– Tải lại dữ liệu; đổi số dòng thì về trang 1; cuộn bảng lên đầu.'),
    ('Bấm Mã hàng hoá', 'Click', 'After:\n– Mở màn Xem chi tiết hàng hoá ở tab mới.'),
    ('Đổi công ty đang làm việc', 'System',
     'After:\n– Danh sách, bộ giá, tồn kho tải lại theo công ty mới; không còn thấy giá của công ty cũ.'),
])

# ------------------------------------------------------------------ 2.2
d.h3('2.2 Tìm kiếm và lọc')
d.p('2.2.1 Giới thiệu')
d.rule_ref('- Kịch bản tìm kiếm, Bộ lọc, Dropdown. Chỉ bổ sung các quy tắc riêng của màn Cập nhật giá bán tại phần mô tả '
           'chi tiết.', anchor='search')
d.intro_table(
    ten='Tìm kiếm và lọc hàng hoá cần cập nhật giá',
    mota='Thu hẹp danh sách theo từ khoá, cây phân loại hàng hoá, hãng sản xuất, thương hiệu, trạng thái duyệt giá và '
         'tình trạng tồn kho của công ty.',
    tacnhan=ACTOR,
    dieukien='Đang ở màn Cập nhật giá bán.',
    chinh='1. Người dùng gõ từ khoá vào ô tìm nhanh rồi nhấn Enter hoặc bấm Tìm kiếm.\n'
          '2. Muốn lọc thêm: bấm Tìm kiếm nâng cao để mở các ô lọc, chọn giá trị — mỗi lần chọn là lọc ngay.\n'
          '3. Hệ thống tải lại danh sách từ trang 1 theo điều kiện đã chọn.',
    phu='• Bấm Làm mới → xoá toàn bộ điều kiện lọc, về trang 1.\n'
        '• Đổi cấp trên của cây phân loại → các cấp dưới bị xoá trắng.\n'
        '• Còn khối chưa lưu khi đổi bộ lọc / Tìm kiếm / Làm mới → hỏi “Thông tin chưa lưu”; Ở lại → ô lọc trả về giá trị cũ.\n'
        '• Không có kết quả → “Không có dữ liệu phù hợp”.')
d.p('2.2.2 Layout màn hình')
d.layout(menu=MENU + ' => Tìm kiếm nâng cao', shot=shot('02-loc-nang-cao.png'),
         shot_caption='Khối bộ lọc khi mở Tìm kiếm nâng cao')
d.layout(menu=MENU, shot=shot('14-khong-co-du-lieu.png'),
         shot_caption='Đang lọc không có kết quả: “Không có dữ liệu phù hợp”')
d.p('2.2.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề khối', 'Label', 'Hiển thị', '–', 'Không', 'Bộ lọc danh sách', 'Tiêu đề khối lọc.'),
    ('Ô tìm nhanh', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống', [
        '- Placeholder: “Tìm theo mã / tên / model hàng hoá”.',
        '- Tìm gần đúng trên Mã hàng, Tên hàng hoá, tên Model.',
        '- Chỉ chạy khi nhấn Enter hoặc bấm Tìm kiếm; có nút ✕ xoá nhanh.']),
    ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Chạy tìm theo từ khoá + các ô lọc, về trang 1.'),
    ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Xoá mọi điều kiện lọc (kể cả lọc mở từ thông báo), về trang 1.'),
    ('Nút Tìm kiếm nâng cao / Ẩn tìm kiếm nâng cao', 'Button', 'Enable', '–', '–', 'Đóng',
     ['- Mặc định khối ô lọc đang đóng.', '- Bấm để mở / đóng các ô lọc; bảng tự co giãn chiều cao theo.']),
    ('Nút Cài đặt bộ lọc', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Mở popup ẩn / hiện và đổi thứ tự ô lọc; cấu hình lưu theo người dùng.'),
    ('Tính chất', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống',
     ['- Cấp 1 của cây phân loại hàng hoá.', '- Đổi → xoá trắng Nhóm công nghệ, Nhóm sản phẩm, Loại sản phẩm.']),
    ('Nhóm công nghệ', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống',
     ['- Chỉ liệt kê nhóm thuộc Tính chất đã chọn (chưa chọn → liệt kê hết).', '- Đổi → xoá trắng 2 cấp dưới.']),
    ('Nhóm sản phẩm', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống',
     ['- Chỉ liệt kê nhóm thuộc Nhóm công nghệ đã chọn.', '- Đổi → xoá trắng Loại sản phẩm.']),
    ('Loại sản phẩm', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống',
     ['- Chỉ liệt kê loại thuộc Nhóm sản phẩm đã chọn.', '- Loại đã khoá có biểu tượng ổ khoá trước tên.']),
    ('Hãng sản xuất', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống',
     'Mọi hãng sản xuất (không giới hạn theo hãng của công ty).'),
    ('Thương hiệu', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống', 'Danh mục thương hiệu.'),
    ('Trạng thái duyệt', 'Dropdown', 'Enable', 'Danh sách 2 giá trị', 'Không', 'Trống (= tất cả)', [
        '- Mặc định: trống = không lọc.',
        '- Chờ duyệt: hàng có ít nhất 1 ô giá vốn / giá / hệ số / ĐMGG / giá hiệu lực tương lai đang chờ duyệt TẠI CÔNG TY MÌNH.',
        '- Không duyệt: tương tự, với ô có đề nghị bị từ chối.',
        '- Mở từ thông báo “[GIA] Từ chối” → bật sẵn Không duyệt.',
        '- Lưu ý: lọc này chạy chậm hơn các lọc khác (khoảng 2–3 giây).']),
    ('Tồn kho', 'Dropdown', 'Enable', 'Danh sách 2 giá trị', 'Không', 'Trống (= tất cả)', [
        '- Mặc định: trống = không lọc.',
        '- Còn tồn: có ít nhất 1 dòng tồn kế toán > 0 trong kho kế toán của công ty mình.',
        '- Hết tồn: không có dòng tồn > 0 nào.',
        '- Cùng định nghĩa với cột Tồn kho.']),
])
d.p('2.2.4 Danh sách event và xử lý event')
d.event_table([
    ('Nhấn Enter ở ô tìm nhanh / bấm Tìm kiếm', 'Keypress / Click',
     'Before:\n– Còn khối chưa lưu → hỏi “Thông tin chưa lưu”; Ở lại → dừng.\n'
     'After:\n– Bỏ lọc theo hàng của thông báo (nếu có), tải lại từ trang 1.'),
    ('Chọn giá trị ở 1 ô lọc', 'Change',
     'Before:\n– Còn khối chưa lưu → hỏi; Ở lại → ô lọc trả về giá trị cũ, không tải lại.\n'
     'After:\n– Lọc ngay, về trang 1; đổi cấp cây phân loại → xoá trắng các cấp dưới trong cùng 1 lần tải.'),
    ('Bấm Làm mới', 'Click', 'Before:\n– Còn khối chưa lưu → hỏi.\nAfter:\n– Xoá mọi ô lọc, tải lại trang 1.'),
    ('Bấm Tìm kiếm nâng cao', 'Click', 'After:\n– Mở / đóng khối ô lọc; bảng đo lại chiều cao vùng cuộn.'),
])

# ------------------------------------------------------------------ 2.3
d.h3('2.3 Cập nhật giá bán')
d.p('2.3.1 Biểu đồ Usecase')
d.uc_figure('FR-03', 'Cập nhật giá bán', 'crud', actor=ACTOR, caption='Biểu đồ Use Case — FR-03 Cập nhật giá bán')
d.p('2.3.2 Giới thiệu')
d.rule_ref('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX. Chỉ bổ sung các quy tắc riêng của màn Cập nhật giá bán '
           'tại phần mô tả chi tiết.', anchor='create')
d.intro_table(
    ten='Cập nhật giá bán (lưu thẳng)',
    mota='Nhập giá vốn, hệ số, giá, ĐMGG cho 6 loại giá của 1 khối (hàng × ĐVT) rồi bấm Lưu. Công ty KHÔNG bật duyệt giá '
         '(hoặc hãng của hàng không thuộc phạm vi duyệt) → giá mới áp dụng NGAY cho công ty đang làm việc.',
    tacnhan=ACTOR,
    dieukien='Có quyền Cập nhật giá bán hàng hoá tại công ty đang làm việc; hàng đang ở trạng thái Đang kinh doanh tại '
             'công ty đó; nút của khối là “Lưu”.',
    chinh='1. Người dùng chọn ĐVT cần sửa giá (nếu hàng có nhiều ĐVT).\n'
          '2. Nhập giá vốn / hệ số / giá mới / ĐMGG; hệ thống tự tính các ô liên quan theo BR-06 … BR-10; khối hiện “● Chưa lưu”.\n'
          '3. (Tuỳ chọn) bấm “Thêm lý do sửa giá” để nhập lý do; tick Sửa tay ở dòng TMĐT nếu muốn nhập tay TMĐT.\n'
          '4. Bấm Lưu của khối.\n'
          '5. Hệ thống kiểm tra đồng thời mọi ô; hợp lệ thì lưu bộ giá của công ty đang làm việc và ghi 1 dòng lịch sử.\n'
          '6. Thông báo “Đã cập nhật giá bán <mã hàng> (<ĐVT>)”; khối hiện lại giá vừa lưu, nhãn “Chưa lưu” mất.',
    phu='• Chưa sửa gì mà bấm Lưu → cảnh báo “Chưa có thay đổi để lưu”, không lưu.\n'
        '• Có ô sai → mọi ô sai cùng báo đỏ, thông báo “Có n ô chưa hợp lệ — xem chữ đỏ dưới từng ô”, con trỏ nhảy tới ô sai đầu tiên.\n'
        '• Hàng không còn ở trạng thái cập nhật được (bị khoá, đổi trạng thái, đang chờ duyệt từ PTG) → khối bị khoá, hiện lý do.\n'
        '• Đổi ĐVT / trang / bộ lọc khi chưa lưu → hỏi “Thông tin chưa lưu”; rời màn khi chưa lưu → hộp thoại cảnh báo chưa lưu.\n'
        '• Sau khi lưu hàng không còn Đang kinh doanh → danh sách tải lại.',
    dacbiet='Lưu từng khối, mỗi lần bấm 1 lần lưu (bấm liên tiếp 2 lần chỉ lưu 1 lần). Thao tác chỉ ghi bộ giá của công ty '
            'đang làm việc, không đụng giá của công ty khác.')
d.p('2.3.3 Layout màn hình')
d.layout(menu=MENU + ' => Lưu', shot=shot('05-sua-gia.png'),
         shot_caption='Khối đang sửa: hệ số Bán lẻ 1,6 lan sang 4 loại giá, TMĐT tự tính, nhãn “● Chưa lưu”')
d.layout(menu=MENU + ' => Thêm lý do sửa giá', shot=shot('08-ly-do-sua-gia.png'),
         shot_caption='Ô nhập Lý do sửa giá mở ngay dưới tên hàng')
d.layout(menu=MENU + ' => Lưu', shot=shot('06-loi-validate.png'),
         shot_caption='Bấm Lưu khi có ô sai: báo đồng thời mọi ô, không lưu')
d.layout(menu=MENU + ' => Lưu', shot=shot('07-chua-luu.png'),
         shot_caption='Hộp thoại “Thông tin chưa lưu” khi đổi bộ lọc lúc còn khối chưa lưu')
d.layout(menu=MENU + ' => Lưu', shot=shot('09-khoi-bi-khoa.png'),
         shot_caption='Khối bị khoá sau khi hệ thống từ chối lưu (minh hoạ: hàng đã Ngừng kinh doanh)')
d.p('2.3.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Ô chọn ĐVT', 'Dropdown', 'Enable / Disable', 'Danh sách ĐVT', 'Không', 'ĐVT đầu tiên', [
        '- Mỗi ĐVT có bộ giá + giá vốn riêng, không tự quy đổi từ ĐVT cơ bản.',
        '- Đổi khi ĐVT đang sửa dở → hỏi “Thông tin chưa lưu”.']),
    ('Giá vốn', 'Number', 'Enable / Disable', '0 – 999.999.999.999', 'Có', 'Giá vốn của công ty', [
        '- Bắt buộc; số nguyên, có dấu phẩy ngăn nghìn.',
        '- Sửa giá vốn KHÔNG đổi giá bán đã nhập; chỉ Giá công thức đổi theo (BR-10).']),
    ('Lý do sửa giá', 'Textbox', 'Enable / Ẩn', '0–2000 ký tự', 'Không', 'Ẩn (giữ lý do lần trước)', [
        '- Mở bằng link “Thêm lý do sửa giá” / “Lý do sửa giá”, bấm lại để đóng; đã có lý do thì hiện chữ xám dưới link.',
        '- Placeholder: “Lý do sửa giá”.',
        '- Lưu cùng khối; để trống thì xoá lý do cũ; lý do ghi kèm dòng lịch sử “Lý do sửa giá: …”.']),
    ('Hệ số (5 loại giá trừ TMĐT)', 'Number', 'Enable', '0 – < 100, tối đa 2 số lẻ', 'Có', 'Theo dữ liệu', [
        '- Bắt buộc. Gõ hệ số → Giá mới = làm tròn trăm (hệ số × giá vốn) (BR-06).',
        '- Hệ số Bán lẻ → ghi đè hệ số + giá của Giá bán theo lô, Đại lý cấp 1–3 (BR-07).']),
    ('Giá mới (5 loại giá trừ TMĐT)', 'Number', 'Enable', '0 – 999.999.999.999', 'Có', 'Theo dữ liệu', [
        '- Bắt buộc; số nguyên.',
        '- Sửa tay được sau khi hệ số đã tính; không tính ngược hệ số.',
        '- Giá Bán lẻ → ghi đè giá 4 loại 2–5, rồi TMĐT tính lại.']),
    ('ĐMGG (%) (5 loại giá trừ TMĐT)', 'Number', 'Enable', '0 – 100, tối đa 2 số lẻ', 'Không', 'Theo dữ liệu',
     ['- Bỏ trống được (lưu là 0).', '- ĐMGG Bán lẻ → ghi đè ĐMGG 4 loại 2–5.']),
    ('Dòng TMĐT – Hệ số / Giá / ĐMGG', 'Number', 'Disable / Enable', 'Như trên', 'Có (Hệ số, Giá)', 'Tự tính', [
        '- Không tick Sửa tay: Hệ số = hệ số Bán lẻ × 1,3 (2 số lẻ); Giá = làm tròn (giá Bán lẻ × 1,3); ĐMGG = 0 — ô xám, không sửa.',
        '- Hệ số 1,3 lấy theo cấu hình của công ty (hiện 1,3 ở cả 8 công ty); khi lưu máy chủ tự tính lại, không lấy số trên màn.']),
    ('Dòng TMĐT – ô tick Sửa tay', 'Checkbox', 'Enable / Disable', '3 ô: Hệ số / Giá / ĐMGG', 'Không', 'Theo dữ liệu', [
        '- Tick → mở ô tương ứng, giữ giá trị công thức đang có để sửa tiếp.',
        '- Bỏ tick → trường đó quay về công thức (ĐMGG về 0).',
        '- Trạng thái tick được lưu cùng khối.']),
    ('Nút Lưu', 'Button', 'Enable / Ẩn', '–', '–', 'Hiển thị', [
        '- Bấm → kiểm tra + lưu khối đang chọn.',
        '- Đang lưu → mọi nút Lưu tạm khoá, có vòng quay tải.']),
    ('Lỗi dưới ô', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', [
        '- Chữ đỏ ngay dưới ô sai + viền đỏ; sửa ô nào thì lỗi ô đó mất, lỗi ô khác giữ nguyên.',
        '- Thông báo chung: “Có n ô chưa hợp lệ — xem chữ đỏ dưới từng ô” (n = số ô sai).']),
    ('Hộp thoại Thông tin chưa lưu', 'Modal', 'Hiển thị', '–', '–', 'Ẩn', [
        '- Đổi trang / bộ lọc: “Có n khối giá đã sửa nhưng chưa lưu. <Thao tác> sẽ bỏ các thay đổi này.” + danh sách '
        '“<mã> – <tên> (<ĐVT>)”.',
        '- Đổi ĐVT: “Giá của ĐVT <ĐVT> đã sửa nhưng chưa lưu. Đổi ĐVT sẽ bỏ các thay đổi này.”',
        '- Nút “Bỏ thay đổi” (bỏ nháp, làm tiếp) / “Ở lại” (giữ nguyên giá trị đang nhập).']),
    ('Khối bị khoá', 'Label', 'Hiển thị', '–', '–', 'Ẩn', [
        '- Biểu tượng ổ khoá + câu lý do dưới tên hàng; mọi ô xám, ẩn nút Lưu, link lý do, “+ Hiệu lực”, nút xoá giá hiệu lực.',
        '- Nháp của hàng bị bỏ (không hỏi “chưa lưu” khi rời màn).',
        '- Tải lại danh sách thì khối được dựng lại theo trạng thái mới.']),
    ('Thông báo kết quả', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', [
        '- Thành công: “Đã cập nhật giá bán <mã hàng> (<ĐVT>)”.',
        '- Chưa sửa gì: “Chưa có thay đổi để lưu”.',
        '- Lỗi khác: “Lưu giá không thành công”.']),
])
d.p('2.3.5 Danh sách event và xử lý event')
d.event_table([
    ('Gõ Hệ số / Giá / ĐMGG / Giá vốn', 'Change',
     'After:\n– Áp phép tính BR-06 … BR-10 ngay trên khối; khối hiện “● Chưa lưu”.\n– Xoá lỗi của đúng ô vừa sửa.'),
    ('Tick / bỏ tick Sửa tay ở dòng TMĐT', 'Change',
     'After:\n– Tick: mở ô. Bỏ tick: trường quay về công thức theo Bán lẻ (ĐMGG về 0).'),
    ('Đổi ĐVT', 'Change',
     'Before:\n– ĐVT đang sửa dở → hỏi “Thông tin chưa lưu”; Ở lại → ô chọn trả về ĐVT cũ.\nAfter:\n– Hiện bộ giá của ĐVT mới.'),
    ('Bấm Lưu', 'Click',
     'Before:\n– Đang lưu khối khác → bỏ qua lần bấm.\n– Chưa có thay đổi → “Chưa có thay đổi để lưu”, dừng.\n'
     '– Tính lại TMĐT theo Bán lẻ (ô không tick Sửa tay).\n'
     '– Kiểm quyền Cập nhật giá bán hàng hoá tại công ty đang làm việc; không có → “' + MSG_NOPERM + '”.\n'
     'During:\n– Giá vốn trống → “Bắt buộc phải nhập”; > 12 chữ số → “Không được vượt quá 12 chữ số”; âm / không phải số → “Không hợp lệ”.\n'
     '– Hệ số trống → “Bắt buộc phải nhập”; ≥ 100 → “Không được vượt quá 2 chữ số trước dấu phẩy”.\n'
     '– Giá mới trống → “Bắt buộc phải nhập”; > 12 chữ số → “Không được vượt quá 12 chữ số”.\n'
     '– ĐMGG ngoài 0 – 100 → “Phải từ 0 đến 100”.\n'
     '– Lý do sửa giá > 2000 ký tự → “Không được vượt quá 2000 ký tự”.\n'
     '– ĐVT không thuộc hàng → “Đơn vị tính không thuộc hàng hoá này”; thiếu loại giá → “Phải gửi đủ 6 loại giá”.\n'
     '– Kiểm trạng thái hàng tại công ty:\n' + '\n'.join(LOCK_MSGS) + '\n'
     '– Có lỗi validate → báo đồng thời mọi ô, không thực hiện After. Bị chặn trạng thái → khoá khối, hiện lý do.\n'
     'After:\n– Ghi 6 loại giá + giá hiệu lực + giá vốn + lý do của ĐVT TẠI CÔNG TY ĐANG LÀM VIỆC; TMĐT máy chủ tự tính.\n'
     '– Xoá cờ Chờ duyệt / Không duyệt, xoá “Lý do không duyệt”, đóng yêu cầu duyệt cũ của ĐVT (nếu có).\n'
     '– Ghi 1 dòng lịch sử “Cập nhật giá” (chỉ ô thực sự đổi).\n'
     '– Hiển thị “Đã cập nhật giá bán <mã hàng> (<ĐVT>)”, khối hiện giá mới.'),
    ('Rời màn khi còn khối chưa lưu', 'System', 'After:\n– Hiện hộp thoại cảnh báo chưa lưu; đồng ý mới rời màn.'),
])

# ------------------------------------------------------------------ 2.4
d.h3('2.4 Thiết lập giá hiệu lực')
d.p('2.4.1 Biểu đồ Usecase')
d.uc_figure('FR-04', 'Thiết lập giá hiệu lực', 'crud', actor=ACTOR, caption='Biểu đồ Use Case — FR-04 Thiết lập giá hiệu lực')
d.p('2.4.2 Giới thiệu')
d.rule_ref('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX. Chỉ bổ sung các quy tắc riêng của màn Cập nhật giá bán '
           'tại phần mô tả chi tiết.', anchor='create')
d.intro_table(
    ten='Thiết lập giá hiệu lực',
    mota='Đặt trước giá cho 1 ngày trong tương lai của từng loại giá (Bán lẻ, Giá bán theo lô, Đại lý cấp 1–3). Đến ngày '
         'hiệu lực hệ thống tự áp thành giá hiện tại. Giá hiệu lực TMĐT tự sinh từ giá hiệu lực Bán lẻ.',
    tacnhan=ACTOR,
    dieukien='Như mục 2.3; loại giá chưa có giá hiệu lực tương lai.',
    chinh='1. Bấm “+ Hiệu lực” ở dòng loại giá.\n'
          '2. Hệ thống thêm dòng con “Giá hiệu lực” ngay dưới, chép sẵn hệ số / giá / ĐMGG của loại giá.\n'
          '3. Người dùng nhập hệ số (giá tự tính = hệ số × giá vốn, KHÔNG làm tròn) hoặc giá, ĐMGG và chọn ngày hiệu lực.\n'
          '4. Bấm Lưu (hoặc Gửi duyệt) của khối — giá hiệu lực lưu cùng khối.',
    phu='• Bấm ✕ “Xoá giá hiệu lực” → bỏ dòng; khi lưu, giá hiệu lực tương lai đã có của loại giá đó bị xoá.\n'
        '• Có giá hiệu lực Bán lẻ → dòng TMĐT có thêm dòng con “Giá hiệu lực” chỉ đọc = giá hiệu lực Bán lẻ × 1,3.\n'
        '• Ngày hiệu lực trống / không phải ngày tương lai → báo đỏ, không lưu.\n'
        '• Giá hiệu lực đã áp hoặc đã qua ngày không hiện ở màn và không bị đụng khi lưu.',
    dacbiet='Tối đa 1 giá hiệu lực tương lai cho mỗi loại giá của mỗi ĐVT tại mỗi công ty.')
d.p('2.4.3 Layout màn hình')
d.layout(menu=MENU + ' => Hiệu lực', shot=shot('05-sua-gia.png'),
         shot_caption='Dòng con “Giá hiệu lực” dưới Bán lẻ và dòng giá hiệu lực TMĐT chỉ đọc')
d.p('2.4.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Link + Hiệu lực', 'Button', 'Enable / Ẩn', '–', '–', 'Hiển thị', [
        '- Tooltip “Thêm giá hiệu lực (tối đa 1 / loại giá)”.',
        '- Ẩn khi loại giá đã có 1 giá hiệu lực, ở dòng TMĐT, hoặc khối bị khoá.']),
    ('Hệ số giá hiệu lực', 'Number', 'Enable', '0 – 99, tối đa 2 số lẻ', 'Có', 'Hệ số của loại giá', [
        '- Bắt buộc. > 99 → “Không được vượt quá 99”.',
        '- Gõ hệ số → giá hiệu lực = hệ số × giá vốn, làm tròn tới đồng (KHÔNG tròn trăm như giá hiện tại — BR-11).',
        '- Không lan sang loại giá khác.']),
    ('Giá công thức (dòng hiệu lực)', 'Number', 'Read-only', '≥ 0', '–', 'Tự tính', 'Giá vốn × hệ số giá hiệu lực.'),
    ('Giá hiệu lực', 'Number', 'Enable', '0 – 999.999.999.999', 'Có', 'Giá của loại giá', 'Bắt buộc; sửa tay được.'),
    ('ĐMGG giá hiệu lực', 'Number', 'Enable', '0 – 100', 'Không', 'ĐMGG của loại giá', 'Ngoài 0 – 100 → “Phải từ 0 đến 100”.'),
    ('Ngày hiệu lực', 'Datepicker', 'Enable', 'dd/mm/yyyy, > hôm nay', 'Có', 'Trống', [
        '- Placeholder “dd/mm/yyyy”; không chọn được hôm nay và ngày đã qua.',
        '- Trống → “Bắt buộc phải chọn”; sai định dạng → “Ngày không hợp lệ”; không phải ngày tương lai → “Phải chọn ngày tương lai”.']),
    ('Nút ✕ Xoá giá hiệu lực', 'Icon Button', 'Enable / Ẩn', '–', '–', 'Hiển thị',
     ['- Nút đỏ, tooltip “Xoá giá hiệu lực”.', '- Bỏ dòng + lỗi của dòng; lưu thì xoá giá hiệu lực tương lai cũ.']),
    ('Dòng giá hiệu lực TMĐT', 'Text', 'Read-only', '–', '–', 'Tự tính', [
        '- Hệ số = hệ số hiệu lực Bán lẻ × 1,3; Giá = giá hiệu lực Bán lẻ × 1,3; ĐMGG 0; cùng ngày với Bán lẻ.',
        '- Icon ⓘ: “Tự tính = giá hiệu lực Bán lẻ × 1.3 (máy chủ sinh khi lưu). Không sửa được.”']),
    ('Nhãn cờ của dòng hiệu lực', 'Badge', 'Hiển thị', '–', '–', 'Ẩn',
     '“Chờ duyệt” (cam) / “Không duyệt” (đỏ) khi giá hiệu lực đang có đề nghị chờ duyệt / bị từ chối.'),
])
d.p('2.4.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm + Hiệu lực', 'Click', 'After:\n– Thêm 1 dòng giá hiệu lực chép giá trị của loại giá, ngày trống; khối “● Chưa lưu”.'),
    ('Gõ hệ số giá hiệu lực', 'Change', 'After:\n– Giá hiệu lực = hệ số × giá vốn (làm tròn đồng).'),
    ('Bấm ✕ Xoá giá hiệu lực', 'Click', 'After:\n– Bỏ dòng và lỗi của dòng; hiện lại link “+ Hiệu lực”.'),
    ('Bấm Lưu / Gửi duyệt của khối', 'Click',
     'Before:\n– Như mục 2.3.\nDuring:\n– Hệ số trống → “Bắt buộc phải nhập”; > 99 → “Không được vượt quá 99”.\n'
     '– Giá trống → “Bắt buộc phải nhập”; > 12 chữ số → “Không được vượt quá 12 chữ số”.\n'
     '– ĐMGG ngoài 0 – 100 → “Phải từ 0 đến 100”.\n'
     '– Ngày trống → “Bắt buộc phải chọn”; sai → “Ngày không hợp lệ”; không phải tương lai → “Phải chọn ngày tương lai”.\n'
     '– Quá 1 giá hiệu lực / loại giá → “Chỉ được 1 giá hiệu lực”.\n'
     'After:\n– Lưu thẳng: sửa tại chỗ dòng đang có hoặc tạo dòng mới; xoá dòng tương lai không còn trên màn; giá hiệu lực TMĐT '
     'máy chủ tự sinh từ Bán lẻ.\n– Gửi duyệt: giá hiệu lực vào đề nghị chờ duyệt (mục 2.5).'),
    ('Đến ngày hiệu lực', 'System', 'After:\n– Tác vụ tự động hằng đêm áp giá hiệu lực thành giá hiện tại của loại giá đó.'),
])

# ------------------------------------------------------------------ 2.5
d.h3('2.5 Gửi duyệt giá bán')
d.p('2.5.1 Biểu đồ Usecase')
d.uc_figure('FR-05', 'Gửi duyệt giá bán', 'action', actor=ACTOR, caption='Biểu đồ Use Case — FR-05 Gửi duyệt giá bán')
d.p('2.5.2 Giới thiệu')
d.rule_ref('- Thông báo và Quy tắc ghi lịch sử. Chỉ bổ sung các quy tắc riêng của màn Cập nhật giá bán tại phần mô tả '
           'chi tiết.', anchor='notice')
d.intro_table(
    ten='Gửi duyệt giá bán',
    mota='Công ty đang làm việc bật duyệt giá (áp cho mọi hãng, hoặc hãng sản xuất của hàng nằm trong danh sách hãng phải '
         'duyệt) → nút của khối là “Gửi duyệt”: giá mới KHÔNG áp ngay mà thành đề nghị chờ người có quyền Duyệt giá bán '
         'hàng hoá của công ty duyệt ở màn Duyệt giá bán.',
    tacnhan=ACTOR,
    dieukien='Như mục 2.3; công ty đang làm việc bật duyệt giá với hãng sản xuất của hàng.',
    chinh='1. Người dùng sửa giá của khối như mục 2.3 / 2.4.\n'
          '2. Bấm “Gửi duyệt”; hệ thống kiểm tra các ô như mục 2.3.\n'
          '3. Hiện popup “Gửi duyệt giá bán” liệt kê các giá đổi (cũ → mới) và giá hiệu lực.\n'
          '4. Người dùng bấm “Gửi duyệt”.\n'
          '5. Hệ thống ghi đề nghị cho đúng các ô thực sự đổi (gắn cờ Chờ duyệt), giữ nguyên giá đang áp dụng, ghi lịch sử '
          '“Gửi duyệt giá”, gửi thông báo “[GIA] Chờ duyệt” cho người có quyền Duyệt giá bán hàng hoá tại công ty.\n'
          '6. Thông báo “Đã gửi yêu cầu duyệt giá bán <mã hàng> (<ĐVT>)”; ô đổi hiện nhãn “Chờ duyệt”.',
    phu='• Bấm Hủy / ✕ ở popup → không gửi, giữ nguyên giá đang nhập.\n'
        '• Đã có đề nghị đang chờ của cùng hàng × ĐVT × công ty → đề nghị mới GHI ĐÈ đề nghị cũ (không sinh 2 yêu cầu).\n'
        '• Gửi lại đúng giá đang áp dụng (không còn ô nào đổi) → đóng đề nghị cũ, không gửi thông báo; thông báo '
        '“Đã cập nhật giá bán …”.\n'
        '• Lý do sửa giá, ô tick Sửa tay TMĐT ghi thẳng, không cần duyệt; “Lý do không duyệt” cũ bị xoá.\n'
        '• Người duyệt Duyệt → giá áp dụng, người gửi nhận “[GIA] Đã duyệt”; Không duyệt → ô hiện “Không duyệt” + lý do, '
        'người gửi nhận “[GIA] Từ chối”.',
    dacbiet='Hiện 8 công ty trên môi trường thử đều TẮT duyệt giá; ảnh minh hoạ nút / popup Gửi duyệt được dựng bằng cách bật '
            'cờ trên trình duyệt, không đổi dữ liệu.')
d.p('2.5.3 Layout màn hình')
d.layout(menu=MENU + ' => Gửi duyệt', shot=shot('11-nut-gui-duyet.png'),
         shot_caption='Khối của công ty bật duyệt giá: nút “Gửi duyệt” (minh hoạ)')
d.layout(menu=MENU + ' => Gửi duyệt', shot=shot('12-xac-nhan-gui-duyet.png'),
         shot_caption='Popup “Gửi duyệt giá bán” liệt kê giá cũ → giá mới (minh hoạ)')
d.layout(menu=MENU, shot=shot('13-co-duyet-khong-duyet.png'),
         shot_caption='Đề nghị bị từ chối: nhãn “Không duyệt”, “Lý do không duyệt”, “Đang áp dụng: …” (dữ liệu thật)')
d.p('2.5.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút Gửi duyệt', 'Button', 'Enable / Ẩn', '–', '–', 'Hiển thị',
     ['- Thay chỗ nút Lưu khi công ty bật duyệt giá với hãng của hàng.', '- Bấm → kiểm tra các ô → mở popup Gửi duyệt giá bán.']),
    ('Popup Gửi duyệt giá bán – tiêu đề', 'Modal', 'Hiển thị', '–', '–', 'Ẩn', 'Tiêu đề “Gửi duyệt giá bán”.'),
    ('Popup – câu dẫn', 'Text', 'Read-only', '–', '–', 'Theo dữ liệu', [
        '- “Gửi đề nghị giá mới của <mã> – <tên> (<ĐVT>) cho người có quyền "Duyệt giá bán hàng hoá" tại <tên công ty>. '
        'Giá đang áp dụng giữ nguyên tới khi được duyệt.”']),
    ('Popup – danh sách giá đổi', 'Text', 'Read-only', '–', '–', 'Theo dữ liệu', [
        '- “Giá vốn: <cũ> → <mới>” khi giá vốn đổi.',
        '- “<Loại giá>: <giá đang áp dụng> → <giá mới>” cho mỗi loại giá có giá / hệ số / ĐMGG đổi.',
        '- “<Loại giá> — giá hiệu lực <yyyy-mm-dd>: <giá>” cho mỗi giá hiệu lực.',
        '- Khung cuộn khi dài.']),
    ('Popup – nút Gửi duyệt', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Xác nhận gửi.'),
    ('Popup – nút Hủy / ✕', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng popup, không gửi, giữ giá đang nhập.'),
    ('Nhãn Chờ duyệt / Không duyệt', 'Badge', 'Hiển thị', '–', '–', 'Ẩn', [
        '- Ở ô Giá vốn và ở dòng loại giá / giá hiệu lực có cờ.',
        '- Chờ duyệt: chữ cam; Không duyệt: chữ đỏ.']),
    ('Lý do không duyệt', 'Text', 'Read-only', '–', '–', 'Ẩn', '“Lý do không duyệt: <lý do>” dưới tên hàng khi bị từ chối.'),
    ('Đang áp dụng (dưới Giá vốn)', 'Text', 'Read-only', '–', '–', 'Ẩn',
     '“Đang áp dụng: <giá vốn đang chạy>” khi có cờ và giá vốn đề nghị khác giá đang chạy.'),
    ('Thông báo kết quả', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
     ['- “Đã gửi yêu cầu duyệt giá bán <mã hàng> (<ĐVT>)”.', '- Không còn gì để duyệt: “Đã cập nhật giá bán <mã hàng> (<ĐVT>)”.']),
])
d.p('2.5.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Gửi duyệt ở khối', 'Click',
     'Before:\n– Như nút Lưu ở mục 2.3 (chưa đổi, kiểm tra đồng thời các ô).\nAfter:\n– Mở popup Gửi duyệt giá bán.'),
    ('Bấm Gửi duyệt ở popup', 'Click',
     'Before:\n– Kiểm quyền Cập nhật giá bán hàng hoá; không có → “' + MSG_NOPERM + '”.\n'
     'During:\n– Validate + kiểm trạng thái như mục 2.3 (cùng câu thông báo).\n'
     'After:\n– Giữ nguyên giá đang áp dụng; ghi giá đề nghị + cờ Chờ duyệt cho ô đổi; ô không đổi xoá cờ cũ.\n'
     '– Tạo mới hoặc ghi đè yêu cầu duyệt của hàng × ĐVT × công ty; xoá “Lý do không duyệt”.\n'
     '– Ghi lịch sử “Gửi duyệt giá”; gửi “[GIA] Chờ duyệt” (kèm “Người đề nghị: <tên>”) tới người có quyền Duyệt giá bán hàng hoá của công ty.\n'
     '– Hiển thị “Đã gửi yêu cầu duyệt giá bán <mã hàng> (<ĐVT>)”.'),
    ('Bấm Hủy / ✕ ở popup', 'Click', 'After:\n– Đóng popup, không gửi, khối vẫn “● Chưa lưu”.'),
])

# ------------------------------------------------------------------ 2.6
d.h3('2.6 Xem lịch sử giá')
d.p('2.6.1 Giới thiệu')
d.rule_ref('- Quy tắc ghi lịch sử. Chỉ bổ sung các quy tắc riêng của màn Cập nhật giá bán tại phần mô tả chi tiết.',
           anchor='history')
d.intro_table(
    ten='Xem lịch sử giá bán',
    mota='Popup xem các lần thay đổi bộ giá của hàng TẠI CÔNG TY ĐANG LÀM VIỆC (mọi ĐVT): Cập nhật giá, Gửi duyệt giá, '
         'Duyệt giá, Không duyệt giá — ai làm, lúc nào, ô nào đổi từ giá trị nào sang giá trị nào.',
    tacnhan=ACTOR,
    dieukien='Có quyền Cập nhật giá bán hàng hoá tại công ty đang làm việc.',
    chinh='1. Bấm nút Lịch sử giá (biểu tượng đồng hồ) ở cột ĐVT · Lưu.\n'
          '2. Hệ thống mở popup “Lịch sử giá bán: <tên hàng>”, các lần thay đổi xếp mới → cũ.\n'
          '3. (Tuỳ chọn) bấm Bộ lọc để lọc theo loại hành động, người thực hiện, khoảng ngày.',
    phu='• Chưa có lần thay đổi nào → “Chưa có lịch sử thao tác nào.”.\n'
        '• Lọc không ra → “Không có lịch sử phù hợp bộ lọc.”.\n'
        '• Lịch sử của công ty khác KHÔNG hiện.')
d.p('2.6.2 Layout màn hình')
d.layout(menu=MENU + ' => Lịch sử giá', shot=shot('15-lich-su-gia.png'),
         shot_caption='Popup Lịch sử giá bán (ảnh chụp lúc kiểm thử 10/10/2026)')
d.p('2.6.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề popup', 'Label', 'Hiển thị', '–', 'Lịch sử giá bán: <tên hàng>', 'Chỉ tên hàng, không kèm mã.'),
    ('Nút Bộ lọc', 'Button', 'Enable', '–', 'Đóng', [
        '- Mở 4 ô lọc, chọn là lọc luôn (không có nút Tìm kiếm).',
        '- Loại hành động (“Chọn loại hành động”): Tạo mới / Thay đổi thông tin / Thay đổi trạng thái. Cập nhật giá thuộc '
        'Thay đổi thông tin; Gửi duyệt / Duyệt / Không duyệt thuộc Thay đổi trạng thái.',
        '- Người thực hiện (“Chọn người thực hiện”): nhân sự của công ty đang làm việc.',
        '- Từ ngày / Đến ngày.']),
    ('Mỗi lần thay đổi', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', [
        '- Thời điểm dd/mm/yyyy hh:mm.',
        '- Nhãn hành động: “Cập nhật giá” (xanh dương), “Gửi duyệt giá”, “Duyệt giá” (xanh lá), “Không duyệt giá” (đỏ).',
        '- “Người thực hiện: <tên> — <phòng ban>”.',
        '- Ghi chú: “Lý do sửa giá: <lý do>” (hoặc lý do không duyệt) nếu có.']),
    ('Chi tiết thay đổi', 'Text', 'Read-only', '–', 'Theo dữ liệu', [
        '- Mỗi dòng giá đặt tên “<Loại giá> (<ĐVT>)”, “Giá vốn (<ĐVT>)”, “<Loại giá> · giá hiệu lực (<ĐVT>)”.',
        '- Nhóm “Giá thêm mới” / “Giá sửa thông tin” / “Giá đã xóa”; ô đổi ghi “giá trị cũ → giá trị mới” cho Giá, Hệ số, '
        'ĐMGG (%), Ngày hiệu lực, Sửa tay (TMĐT).',
        '- Chỉ ô thực sự đổi mới được ghi; lưu lại đúng giá cũ không sinh dòng.']),
    ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn', '“Chưa có lịch sử thao tác nào.” / “Không có lịch sử phù hợp bộ lọc.”'),
    ('Nút Đóng / ✕', 'Button', 'Enable', '–', 'Hiển thị', 'Đóng popup, không ảnh hưởng nháp đang sửa trên bảng.'),
], required=False)
d.p('2.6.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Lịch sử giá', 'Click',
     'Before:\n– Kiểm quyền Cập nhật giá bán hàng hoá; không có → “' + MSG_NOPERM + '”.\n'
     'During:\n– Lấy lịch sử của hàng × công ty đang làm việc; công ty chưa dùng hàng → rỗng.\n'
     'After:\n– Hiện timeline mới → cũ.'),
    ('Chọn ô lọc trong popup', 'Change', 'After:\n– Lọc ngay danh sách lịch sử.'),
    ('Bấm Đóng', 'Click', 'After:\n– Đóng popup.'),
])

# ------------------------------------------------------------------ 2.7
d.h3('2.7 Xem công thức lắp ráp')
d.p('2.7.1 Giới thiệu')
d.rule_ref('- Màn Xem chi tiết và Phân quyền. Chỉ bổ sung các quy tắc riêng của màn Cập nhật giá bán tại phần mô tả chi tiết.',
           anchor='detail')
d.intro_table(
    ten='Xem công thức lắp ráp',
    mota='Popup chỉ đọc liệt kê các hàng thành phần của hàng lắp ráp, giúp người cập nhật giá đối chiếu giá vốn của hàng '
         'lắp ráp với các thành phần.',
    tacnhan=ACTOR,
    dieukien='Hàng có công thức lắp ráp (link “Xem công thức lắp ráp” hiện dưới tên hàng) và khối không bị khoá.',
    chinh='1. Bấm “Xem công thức lắp ráp” dưới tên hàng.\n'
          '2. Hệ thống mở popup “Công thức lắp ráp: <tên hàng>” và tải danh sách thành phần.',
    phu='• Không đọc được / không có thành phần → “Không có dữ liệu phù hợp”.\n• Đang tải → “Đang tải…”.')
d.p('2.7.2 Layout màn hình')
d.layout(menu=MENU + ' => Xem công thức lắp ráp', shot=shot('10-cong-thuc-lap-rap.png'),
         shot_caption='Popup Công thức lắp ráp của TEWI-AQUA (dữ liệu thật)')
d.p('2.7.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề popup', 'Label', 'Hiển thị', '–', 'Công thức lắp ráp: <tên hàng>', 'Tên hàng lắp ráp.'),
    ('Cột STT', 'Table/Grid', 'Read-only', 'Số nguyên', 'Theo dữ liệu', 'Đánh số từ 1.'),
    ('Cột Mã hàng hoá', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', 'Mã hàng thành phần.'),
    ('Cột Tên hàng hoá', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', 'Tên hàng thành phần.'),
    ('Cột ĐVT', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', 'Đơn vị tính của thành phần trong công thức.'),
    ('Cột Số lượng', 'Table/Grid', 'Read-only', '≥ 0', 'Theo dữ liệu', 'Số lượng thành phần, dấu phẩy ngăn nghìn.'),
    ('Trạng thái rỗng / đang tải', 'Label', 'Hiển thị', '–', 'Ẩn', '“Không có dữ liệu phù hợp” / “Đang tải…”.'),
    ('Nút Đóng / ✕', 'Button', 'Enable', '–', 'Hiển thị', 'Đóng popup.'),
], required=False)
d.p('2.7.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Xem công thức lắp ráp', 'Click',
     'During:\n– Đọc công thức lắp ráp từ thông tin chi tiết hàng hoá.\nAfter:\n– Hiện bảng thành phần; lỗi → bảng rỗng.'),
    ('Bấm Đóng', 'Click', 'After:\n– Đóng popup, xoá dữ liệu đã tải.'),
])

# ========================================================= PHAN 4
d.h1('Phần 4. Quy tắc nghiệp vụ')
d.rule_ref('chỉ ghi các quy tắc đặc thù của giá bán theo công ty; quy tắc dùng chung không nhắc lại.',
           anchor='list', head='Quy tắc áp dụng', lead='Ngoài SRS Các quy tắc chung ')
d.rule_table([
    ('BR-01', 'Phạm vi màn',
     ['– Chỉ hàng ĐANG KINH DOANH tại công ty đang làm việc, chưa bị xoá.',
      '– Hàng Đang nhập thông tin / Chờ tính giá bán / Đang tính giá / Ngừng kinh doanh, hàng công ty chưa dùng: không hiện.',
      '– Mã hàng mới nhất lên trước; 20 hàng / trang (tối đa 50).'], ['Xem danh sách']),
    ('BR-02', 'Quyền xét theo công ty đang làm việc',
     ['– Mọi thao tác (xem, lưu, gửi duyệt, lịch sử) cần quyền Cập nhật giá bán hàng hoá ĐƯỢC GÁN Ở công ty đang làm việc.',
      '– Không có quyền: ẩn menu, màn không hiển thị và không tải dữ liệu; gọi thẳng chức năng bị từ chối.',
      '– Super admin không được miễn.'], ['Mọi chức năng']),
    ('BR-03', 'GIÁ — Bộ giá theo công ty',
     ['– Mỗi công ty có bộ giá riêng cho từng ĐVT: 6 loại giá + giá vốn + giá hiệu lực + lý do sửa giá.',
      '– Màn chỉ đọc và chỉ ghi bộ giá của công ty đang làm việc; công ty lấy từ phiên làm việc, không nhận từ màn hình.',
      '– Lưu ở công ty A không đổi bất kỳ giá nào của công ty B.'], ['Mọi chức năng']),
    ('BR-04', 'GIÁ — Giá vốn hiển thị theo quyền của màn',
     ['– Người có quyền Cập nhật giá bán hàng hoá luôn thấy và nhập giá vốn công ty mình (cả trong lịch sử).',
      '– Quyền Xem giá vốn hàng hoá KHÔNG áp dụng ở màn này (khác màn Duyệt giá bán).'], ['Xem danh sách', 'Cập nhật giá', 'Lịch sử']),
    ('BR-05', 'GIÁ — Đủ 6 loại giá, giá ĐVT riêng',
     ['– Thứ tự: Bán lẻ, Giá bán theo lô, Đại lý cấp 1, 2, 3, TMĐT; thiếu loại nào thì hiện dòng giá 0 và lưu sẽ sinh đủ.',
      '– Giá của ĐVT quy đổi lưu riêng, không tự tính từ ĐVT cơ bản × hệ số quy đổi.'], ['Xem danh sách', 'Cập nhật giá']),
    ('BR-06', 'GIÁ — Hệ số → Giá (làm tròn trăm)',
     ['– Nhập hệ số của 1 loại giá → Giá mới = làm tròn tới trăm của (hệ số × giá vốn).',
      '– Vd giá vốn 195.989.760, hệ số 1,6 → 313.583.600; hệ số 1,7 → 333.182.600.'], ['Cập nhật giá']),
    ('BR-07', 'GIÁ — Bán lẻ lan sang 4 loại giá',
     ['– Sửa Hệ số, Giá hoặc ĐMGG của Bán lẻ → ghi đè đúng trường đó cho Giá bán theo lô, Đại lý cấp 1, 2, 3 (không lan sang TMĐT).',
      '– Sửa hệ số Bán lẻ → cả hệ số lẫn giá của 4 loại đều bị ghi đè; sửa riêng từng loại thì phải sửa SAU Bán lẻ.'], ['Cập nhật giá']),
    ('BR-08', 'GIÁ — Thương mại điện tử',
     ['– Không tick Sửa tay: Hệ số = hệ số Bán lẻ × 1,3 (2 số lẻ); Giá = làm tròn đồng (giá Bán lẻ × 1,3); ĐMGG = 0.',
      '– Tick Sửa tay từng trường → nhập tay trường đó; bỏ tick → về công thức.',
      '– Khi lưu máy chủ tự tính lại TMĐT theo hệ số cấu hình của công ty (hiện 1,3), không lấy số trên màn.',
      '– Vd giá Bán lẻ 313.583.600 → TMĐT 407.658.680, hệ số 2,08; giá Bán lẻ 120.000.000 → TMĐT 156.000.000.'], ['Cập nhật giá']),
    ('BR-09', 'GIÁ — Giá công thức',
     ['– Giá công thức = giá vốn × hệ số; TMĐT làm tròn nghìn (vd 195.989.760 × 2,08 → 407.659.000).',
      '– Chỉ để tham chiếu, không lưu.'], ['Xem danh sách', 'Cập nhật giá']),
    ('BR-10', 'GIÁ — Sửa giá vốn không tính lại giá',
     ['– Đổi giá vốn chỉ đổi cột Giá công thức; Giá mới giữ nguyên tới khi người dùng sửa hệ số / giá.'], ['Cập nhật giá']),
    ('BR-11', 'GIÁ — Giá hiệu lực',
     ['– Tối đa 1 giá hiệu lực tương lai / loại giá / ĐVT / công ty; ngày phải sau hôm nay.',
      '– Hệ số giá hiệu lực → giá = hệ số × giá vốn, làm tròn tới ĐỒNG (không tròn trăm như BR-06); vd hệ số 1,4 → 274.385.664.',
      '– Giá hiệu lực TMĐT không nhập được: máy chủ sinh = giá hiệu lực Bán lẻ × 1,3 cùng ngày.',
      '– Lưu: sửa tại chỗ dòng đang có; dòng tương lai bị bỏ trên màn sẽ bị xoá; dòng đã áp / quá hạn không bị đụng.',
      '– Đến ngày hiệu lực, tác vụ tự động hằng đêm áp giá hiệu lực thành giá hiện tại.'], ['Thiết lập giá hiệu lực']),
    ('BR-12', 'Kiểm tra dữ liệu báo đồng thời',
     ['– Bấm Lưu / Gửi duyệt: mọi ô sai của khối báo đỏ cùng lúc, con trỏ nhảy tới ô sai đầu tiên, không gửi lưu.',
      '– Câu chữ: “Bắt buộc phải nhập”, “Bắt buộc phải chọn”, “Không hợp lệ”, “Không được vượt quá 12 chữ số”, '
      '“Không được vượt quá 2 chữ số trước dấu phẩy”, “Không được vượt quá 99”, “Phải từ 0 đến 100”, “Ngày không hợp lệ”, '
      '“Phải chọn ngày tương lai”, “Chỉ được 1 giá hiệu lực”, “Không được vượt quá 2000 ký tự”.',
      '– ĐMGG ngoài 0 – 100 báo đỏ, không tự kẹp về 0 / 100.'], ['Cập nhật giá', 'Giá hiệu lực', 'Gửi duyệt']),
    ('BR-13', 'Lưu từng khối',
     ['– 1 lần lưu = 1 hàng × 1 ĐVT đang chọn; khối khác trên trang không bị lưu theo.',
      '– Chưa thay đổi → “Chưa có thay đổi để lưu”; bấm liên tiếp chỉ lưu 1 lần.'], ['Cập nhật giá', 'Gửi duyệt']),
    ('BR-14', 'Cảnh báo chưa lưu',
     ['– Đổi ĐVT, trang, số dòng, bộ lọc, Tìm kiếm, Làm mới khi còn khối chưa lưu → hỏi “Thông tin chưa lưu” (Bỏ thay đổi / Ở lại).',
      '– Rời màn khi chưa lưu → hộp thoại cảnh báo chưa lưu. Mở mã hàng ở tab mới không mất nháp.'], ['Cập nhật giá']),
    ('BR-15', 'Trạng thái hàng chặn cập nhật giá',
     ['– Chỉ hàng Đang kinh doanh tại công ty được lưu; kiểm lại ngay trong lúc lưu (vừa bị khoá giữa chừng cũng bị chặn).'] +
     LOCK_MSGS[:7] +
     ['– Bị chặn → khối bị khoá, hiện lý do, bỏ nháp; hàng mới chỉ có giá qua luồng Phiếu tính giá.'],
     ['Cập nhật giá', 'Giá hiệu lực', 'Gửi duyệt']),
    ('BR-16', 'Giá đang chờ duyệt từ Phiếu tính giá',
     ['– Hàng × ĐVT × công ty đang có yêu cầu duyệt sinh từ Phiếu tính giá → không lưu / gửi duyệt được: '
      '“Giá đang chờ duyệt ở <mã phiếu tính giá>.” (tránh làm treo phiếu).'], ['Cập nhật giá', 'Gửi duyệt']),
    ('BR-17', 'Nhánh Gửi duyệt',
     ['– Áp khi công ty đang làm việc bật duyệt giá và (áp mọi hãng hoặc hãng sản xuất của hàng thuộc danh sách hãng phải duyệt).',
      '– Quy định duyệt đọc của CÔNG TY BỘ GIÁ (công ty đang làm việc), không phải công ty tạo hàng.',
      '– Giá đang áp dụng giữ nguyên; chỉ ô thực sự đổi được gắn Chờ duyệt; tối đa 1 yêu cầu mở / hàng × ĐVT × công ty (gửi lại = ghi đè).',
      '– Không còn ô nào đổi → đóng yêu cầu cũ, không thông báo.',
      '– Thông báo “[GIA] Chờ duyệt” tới người có quyền Duyệt giá bán hàng hoá tại công ty.'], ['Gửi duyệt']),
    ('BR-18', 'Lưu thẳng xoá đề nghị cũ',
     ['– Nhánh lưu thẳng (kể cả khi công ty vừa tắt duyệt giá lúc còn yêu cầu chờ): áp giá mới, xoá cờ Chờ duyệt / Không duyệt, '
      'xoá “Lý do không duyệt”, đóng yêu cầu duyệt đang mở của hàng × ĐVT × công ty.'], ['Cập nhật giá']),
    ('BR-19', 'Hiển thị giá Chờ duyệt / Không duyệt',
     ['– Ô Giá vốn / Hệ số / Giá mới / ĐMGG / giá hiệu lực có cờ → hiện GIÁ ĐỀ NGHỊ; Giá hiện tại luôn là giá đang áp dụng.',
      '– Nhãn “Chờ duyệt” (cam) / “Không duyệt” (đỏ); có “Lý do không duyệt” khi bị từ chối.',
      '– Lưu ý: bấm Lưu (lưu thẳng) khi ô còn hiện giá bị từ chối sẽ áp chính giá đó; muốn giữ giá cũ phải nhập lại.'],
     ['Xem danh sách', 'Cập nhật giá']),
    ('BR-20', 'Lý do sửa giá',
     ['– Tối đa 2000 ký tự, lưu theo ĐVT × công ty; để trống khi lưu → xoá lý do cũ.',
      '– Ghi kèm dòng lịch sử “Lý do sửa giá: …”; nhánh gửi duyệt ghi thẳng, không cần duyệt.'], ['Cập nhật giá', 'Gửi duyệt']),
    ('BR-21', 'Lịch sử giá theo hàng × công ty',
     ['– Mỗi lần Lưu / Gửi duyệt / Duyệt / Không duyệt có thay đổi → 1 dòng; chỉ ghi ô thực sự đổi; không đổi gì → không ghi.',
      '– Chỉ xem được lịch sử của công ty đang làm việc; xem qua màn này cần quyền Cập nhật giá bán hàng hoá.'], ['Lịch sử']),
    ('BR-22', 'Tồn kho của công ty',
     ['– Tồn kế toán cộng mọi kho kế toán của CÔNG TY ĐANG LÀM VIỆC, tính theo ĐVT cơ bản rồi chia hệ số quy đổi của ĐVT đang chọn.',
      '– Lọc Còn tồn / Hết tồn cùng định nghĩa.'], ['Xem danh sách', 'Tìm kiếm và lọc']),
    ('BR-23', 'Thao tác đồng thời',
     ['– Hai người lưu cùng hàng × ĐVT × công ty: hệ thống xếp hàng, người sau lưu đè người trước (mỗi lần 1 dòng lịch sử).',
      '– Hàng đổi trạng thái giữa lúc lưu → bị chặn theo BR-15.'], ['Cập nhật giá', 'Gửi duyệt']),
    ('BR-24', 'Phạm vi KHÔNG ghi',
     ['– Màn không đổi đơn vị tính, hệ số quy đổi, công khoán, ghi chú hàng hoá, hệ số công nghệ hay trạng thái hàng.',
      '– Không ghi lịch sử hàng hoá (chỉ lịch sử giá).'], ['Cập nhật giá']),
])

# update_fields=False: may dang mo Microsoft Word cua user — buoc cap nhat muc luc tren macOS se `quit saving no`
# (dong Word, mat viec chua luu cua user). Muc luc cap nhat bang tay: chuot phai -> Update Field.
d.save(update_fields=os.environ.get('SRS_UPDATE_TOC') == '1')
print('OK ->', OUT)
