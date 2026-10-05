"""Sửa các testcase phân quyền CŨ trong tab 11.Meeting cho khớp phân quyền hiện tại.

Phân quyền hiện tại (đọc code worktrees/tpe-client + tpe-api, 24/09/2026):
- Không có quyền Tạo/Sửa/Xoá/In riêng cho meeting. Menu Meetings > Lịch Meeting ai cũng thấy; ai đăng nhập cũng tạo được.
- 4 quyền 'Xem danh sách meeting theo tổng công ty / công ty / phòng ban / bộ phận' chỉ mở rộng phạm vi XEM.
- Không có quyền nào: vẫn thấy meeting mình tạo / chủ trì / là thành viên nội bộ (bản Lưu nháp chỉ người tạo + chủ trì thấy).
- Sửa, Hoàn thành, Điểm danh: người tạo + người chủ trì. Hủy, Xoá: chỉ người tạo.
- Lỗi không có quyền trên màn hình luôn là câu chung 'Bạn không có quyền thực hiện chức năng này'.
Sinh old_tc_edits.json: [{row, id, col, text}] - col là chữ cột (E,G,H,I,J,O).
"""
import csv, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
CSV = sys.argv[1]
rows = list(csv.reader(open(CSV, encoding='utf-8')))
COL = {c: i for i, c in enumerate('ABCDEFGHIJKLMNOPQRST')}
NOTE = 'Cập nhật 24/09/2026: viết lại theo phân quyền hiện tại - cần test lại.'
DENY = "Bạn không có quyền thực hiện chức năng này"

E = {}  # row -> (id, {col: text})


def put(row, tcid, **cols):
    E[row] = (tcid, cols)


put(8, 'TC-ROLE-01.',
    E='Vào danh sách Meeting với quyền xem theo tổng công ty',
    G="Tài khoản có quyền 'Xem danh sách meeting theo tổng công ty'; đã đăng nhập.",
    H='1. Mở menu Meetings > Lịch Meeting.\n2. Quan sát màn hình, bộ lọc nâng cao và nút trên từng dòng.',
    I="Quyền: Xem danh sách meeting theo tổng công ty",
    J="- Mở được màn 'Danh sách meetings liên quan đến dự án tiền khả thi'.\n"
      "- Thấy meeting của mọi công ty (trừ bản Lưu nháp của người khác).\n"
      "- Có nút Tạo mới, Xuất Excel, Cấu hình cột.\n"
      "- Bộ lọc nâng cao có đủ ô Công ty, Phòng ban, Bộ phận.\n"
      "- Nút trên dòng: Xem, In biên bản, Lịch sử luôn có; Sửa chỉ khi mình là người tạo/chủ trì và meeting chưa Hoàn thành/Huỷ; "
      "Xoá chỉ khi mình là người tạo và meeting đang Lưu nháp.")
put(9, 'TC-ROLE-03',
    E='Không có quyền xem nào vẫn vào được và chỉ thấy meeting liên quan tới mình',
    G="Tài khoản E không được gán quyền nào trong 4 quyền 'Xem danh sách meeting theo ...'.\n"
      "E là thành viên MT-01 (Lên lịch hẹn), chủ trì MT-08 (Lưu nháp, người khác tạo), tự tạo MT-09.",
    H='1. Đăng nhập E.\n2. Mở menu Meetings > Lịch Meeting.\n3. Quan sát danh sách và bộ lọc nâng cao.',
    I='Tài khoản: E (không có quyền xem nào)',
    J="- Menu Meetings > Lịch Meeting vẫn hiển thị và vào được.\n"
      "- Danh sách chỉ có MT-01, MT-08, MT-09 (meeting mình là thành viên / chủ trì / tự tạo).\n"
      "- Không thấy meeting nào khác.\n"
      "- Bộ lọc nâng cao không có ô Công ty, Phòng ban, Bộ phận.")
put(10, 'TC-ROLE-04',
    E='Mở thẳng đường dẫn chi tiết meeting không liên quan tới mình',
    G='Tài khoản E không có quyền xem nào, không phải người tạo/chủ trì/thành viên của MT-10.',
    H='1. Đăng nhập E.\n2. Dán đường dẫn màn chi tiết MT-10 lên trình duyệt.',
    I='Đường dẫn chi tiết MT-10',
    J=f"- Hiện thông báo '{DENY}'.\n- Chuyển sang trang không tìm thấy (404).\n- Không lộ bất kỳ nội dung nào của MT-10.")
put(11, 'TC-ROLE-05',
    E='Bị đổi người chủ trì trong lúc đang mở màn Sửa',
    G='B là chủ trì (không phải người tạo) đang mở màn Sửa MT-01.\nCùng lúc đó A (người tạo) đổi chủ trì MT-01 sang B2 và lưu.',
    H='1. B sửa Nội dung cuộc họp.\n2. B bấm Lưu.\n3. B mở lại chi tiết MT-01.',
    I='Chủ trì mới: B2',
    J=f"- Hiện thông báo '{DENY}', dữ liệu B vừa sửa không được lưu.\n- Mở lại MT-01: B không còn nút Sửa.",
    O='Code hiện báo 2 lần cùng một câu. ' + NOTE)

# ---- Tạo mới: không có quyền tạo riêng
NO_CREATE_PERM = 'Tài khoản đã đăng nhập (mọi tài khoản đều tạo được meeting, không cần quyền riêng).'
for r, tid in [(39, 'TC-ROLE-30'), (40, 'TC-ROLE-31.'), (83, 'TC-ROLE-74'), (86, 'TC-ROLE-77'),
               (141, 'TC-ROLE-1.22'), (142, 'TC-ROLE-1.23'), (143, 'TC-ROLE-1.24')]:
    put(r, tid, G='__REPL__')
put(84, 'TC-ROLE-75',
    E='Tài khoản không có quyền nào vẫn tạo được meeting',
    G="Tài khoản E không có quyền nào trong nhóm meeting.",
    H='1. Đăng nhập E, bấm Tạo mới.\n2. Nhập đủ trường bắt buộc.\n3. Bấm Lưu nháp.',
    I='Tài khoản: E',
    J="- Lưu thành công, meeting ở trạng thái 'Lưu nháp'.\n- E là người tạo, có đủ nút Sửa / Xóa với meeting này.",
    O=NOTE)
put(87, 'TC-ROLE-78',
    E='Thành viên không lên lịch được meeting của người khác',
    G='D là thành viên (không phải người tạo/chủ trì) của MT-01 trạng thái Lên lịch hẹn.',
    H='1. Đăng nhập D, mở chi tiết MT-01.\n2. Dán đường dẫn màn Sửa MT-01.',
    I='Tài khoản: D',
    J="- Màn chi tiết không có nút Sửa nên không có Lưu và Lên lịch.\n- Mở đường dẫn Sửa thì tự chuyển về màn chi tiết.",
    O=NOTE)
put(89, 'TC-ROLE-80',
    E='Tài khoản không có quyền xem nào vẫn Lên lịch được meeting mới',
    G="Tài khoản E không có quyền nào trong nhóm meeting.",
    H='1. Đăng nhập E, bấm Tạo mới.\n2. Nhập đủ trường bắt buộc.\n3. Bấm Lưu và Lên lịch.',
    I='Tài khoản: E',
    J="- Lưu thành công, meeting chuyển 'Lên lịch hẹn'.",
    O=NOTE)
put(92, 'TC-ROLE-83',
    E='Người không phải người tạo/chủ trì không Hoàn thành được',
    G='MT-05 Đã chốt lịch, đã tới giờ họp. D là thành viên, E chỉ có quyền xem theo công ty.',
    H='1. Lần lượt đăng nhập D, E mở chi tiết MT-05.\n2. Dán đường dẫn màn Sửa MT-05.',
    I='Tài khoản: D, E',
    J="- Không có nút Hoàn thành.\n- Mở đường dẫn Sửa thì tự chuyển về màn chi tiết.",
    O=NOTE)
put(96, 'TC-ROLE-86',
    G='Tài khoản không phải người tạo, không phải chủ trì của meeting (vd thành viên D).',
    J='- Tự chuyển sang màn Chi tiết, không mở được màn Sửa.',
    O=NOTE)
put(97, 'TC-ROLE-87', G='Người tạo hoặc người chủ trì mở màn Sửa; meeting chưa Hoàn thành/Huỷ.')
for r, tid, btn in [(103, 'TC-ROLE-93', 'Lưu nháp'), (105, 'TC-ROLE-95', 'Lưu và Lên lịch'),
                    (107, 'TC-ROLE-97', 'Lưu và Chốt lịch'), (109, 'TC-ROLE-99', 'Hoàn thành')]:
    put(r, tid,
        E=f"Người không phải người tạo/chủ trì không bấm được '{btn}'",
        G='D là thành viên (không phải người tạo/chủ trì) của meeting.',
        H=f"1. Đăng nhập D, mở chi tiết meeting.\n2. Dán đường dẫn màn Sửa.\n"
          f"3. Dùng công cụ kiểm thử API gọi thẳng chức năng Sửa meeting.",
        I='Tài khoản: D',
        J=f"- Không có nút Sửa nên không có '{btn}'.\n- Đường dẫn Sửa tự chuyển về màn chi tiết.\n"
          f"- Gọi thẳng chức năng Sửa: hệ thống từ chối, báo '{DENY}', dữ liệu không đổi.",
        O=NOTE)
put(115, 'TC-ROLE-1.04', G='Meeting ở trạng thái Lưu nháp; tài khoản đăng nhập là người tạo meeting.')
put(116, 'TC-ROLE-1.05', G="Meeting ở trạng thái Lên lịch hẹn / Đã chốt lịch / Đã hoàn thành / Huỷ; tài khoản là người tạo.")
put(118, 'TC-ROLE-1.07',
    E='Người chủ trì / thành viên không xoá được meeting',
    G='MT-02 trạng thái Lưu nháp do A tạo, B là chủ trì.',
    H='1. Đăng nhập B, xem dòng MT-02 ở danh sách và màn chi tiết.\n2. Dùng công cụ kiểm thử API gọi thẳng chức năng Xoá MT-02.',
    I='Tài khoản: B',
    J=f"- Không có nút Xoá ở cả danh sách lẫn màn chi tiết.\n- Gọi thẳng chức năng Xoá: hệ thống từ chối, báo '{DENY}', MT-02 vẫn còn.",
    O=NOTE)
put(121, 'TC-ROLE-1.09',
    E='Mở chi tiết meeting ngoài phạm vi được xem',
    G='Tài khoản E không liên quan MT-10 và không có quyền xem theo phạm vi chứa MT-10.',
    J=f"- Hiện thông báo '{DENY}'.\n- Chuyển sang trang không tìm thấy (404), không hiển thị thông tin meeting.",
    O=NOTE)
for r, tid in [(125, 'TC-ROLE-51.'), (126, 'TC-ROLE-52')]:
    put(r, tid, G='Tài khoản bất kỳ (nút Xuất Excel không cần quyền riêng); có dữ liệu.',
        J='__APPEND__- File chỉ gồm meeting nằm trong phạm vi tài khoản đang xem được (giống danh sách trên màn hình).')
for r, tid in [(129, 'TC-ROLE-1.1.2'), (130, 'TC-ROLE-1.1.3'), (131, 'TC-ROLE-1.1.4')]:
    put(r, tid, G='__REPL_PRINT__', J='__DROPCHECK__')
put(132, 'TC-ROLE-1.1.5',
    E='In biên bản meeting ngoài phạm vi được xem',
    G='Tài khoản E không liên quan MT-10 và không có quyền xem theo phạm vi chứa MT-10.',
    H='1. Đăng nhập E, tìm MT-10 ở danh sách.\n2. Dán đường dẫn trang in biên bản của MT-10.',
    I='Tài khoản: E',
    J=f"- Không thấy MT-10 nên không có nút In.\n- Mở đường dẫn in: bị chặn, báo '{DENY}', không hiện nội dung biên bản.",
    O='Rà code thấy trang in chưa kiểm quyền xem - dễ Failed. ' + NOTE)
put(144, 'TC-ROLE-1.25', G="Người tạo hoặc người chủ trì mở màn Sửa meeting 'Đã chốt lịch', đã tới giờ họp.")
put(145, 'TC-ROLE-1.26', G="Người tạo mở chi tiết meeting 'Lên lịch hẹn' hoặc 'Đã chốt lịch', chưa tới giờ họp (chỉ người tạo được Hủy).")
put(146, 'TC-ROLE-1.27', G='Người tạo hoặc người chủ trì mở màn Sửa meeting chưa Hoàn thành/Huỷ.')
put(148, 'TC-ROLE-1.29', G='Tài khoản xem được meeting; meeting chưa Hoàn thành/Huỷ.')
put(188, 'TC-ROLE-1.33',
    E="Quyền 'Xem danh sách meeting theo tổng công ty' thấy meeting mọi nhóm tham gia",
    G="Hệ thống có 10 meeting của nhiều nhóm người tham gia khác nhau (không có bản Lưu nháp); tài khoản có quyền 'Xem danh sách meeting theo tổng công ty'.",
    O=NOTE)
put(190, 'TC-ROLE-1.35',
    J=f"- Hiện thông báo '{DENY}', chuyển sang trang không tìm thấy (404).\n- Không hiển thị bất kỳ nội dung nào của cuộc họp (tên, thời gian, biên bản).",
    O=NOTE)
put(200, 'TC-ROLE-1.45',
    J=f"- Tải lại chi tiết: báo '{DENY}' và chuyển sang trang không tìm thấy.\n- Meeting biến mất khỏi danh sách của NV B.\n"
      "- Lưu ý: nếu NV B có quyền xem theo phạm vi chứa meeting đó thì vẫn xem được.",
    O=NOTE)
put(201, 'TC-ROLE-1.46',
    J=f"- Bị chặn, báo '{DENY}', không tải được nội dung biên bản.",
    O='Rà code thấy trang in chưa kiểm quyền xem - dễ Failed. ' + NOTE)
for r, tid in [(217, 'TC_08.002'), (218, 'TC_08.003')]:
    put(r, tid, G='Tài khoản không phải người tạo/chủ trì/thành viên của meeting và không có quyền xem theo phạm vi chứa meeting đó.',
        J=f"- Không mở được màn Chi tiết Meeting.\n- Hiển thị thông báo '{DENY}' rồi chuyển sang trang không tìm thấy (404).\n"
          "- Không hiển thị bất kỳ thông tin nào của meeting.",
        O=NOTE)
put(226, 'TC_09.003',
    J='- Tự chuyển sang màn Xem chi tiết, không sửa được.\n- Không hiện nút Lưu, Hoàn thành, Hủy.',
    O=NOTE)
put(307, 'TC_1.8001.', G="Người tạo hoặc người chủ trì mở màn Sửa cuộc họp 'Đã chốt lịch'.")
put(309, 'TC_1.8003',
    E='Ai được điểm danh cuộc họp (không phụ thuộc quyền trong nhóm meeting)',
    G="MT-05 trạng thái 'Đã chốt lịch'. A: người tạo; B: người chủ trì; D: thành viên nội bộ; "
      "E: chỉ có quyền 'Xem danh sách meeting theo công ty'.\nA, B, D không được gán quyền nào trong nhóm meeting.",
    H="1. A và B lần lượt mở màn Sửa MT-05 > tab Điểm danh.\n2. D và E mở chi tiết MT-05 > tab Điểm danh.\n"
      "3. D dán đường dẫn màn Sửa MT-05.",
    I='Tài khoản: A, B, D, E',
    J="- A và B điểm danh được: chọn Có mặt / Vắng có lý do / Vắng không lý do, nhập Ghi chú, có nút 'Điểm danh nhanh: Tất cả có mặt'.\n"
      "- D và E chỉ xem kết quả điểm danh, không chọn được.\n"
      "- D chỉ tự xác nhận cho CHÍNH MÌNH bằng 'Có mặt' / 'Vắng có lý do' khi chưa tới giờ họp.\n"
      "- D mở đường dẫn Sửa thì tự chuyển về màn chi tiết.\n"
      "- Không có quyền nào trong nhóm meeting vẫn xem được meeting mình tạo / chủ trì / tham gia.",
    O=NOTE)
put(338, 'TC-ROLE-01.',
    E="Quyền xem theo tổng công ty chỉ mở rộng phạm vi XEM, không cho sửa thành phần tham gia",
    G="Tài khoản chỉ có quyền 'Xem danh sách meeting theo tổng công ty'; MT-11 do người khác tạo và chủ trì.",
    H='1. Mở Meetings > Lịch Meeting.\n2. Mở MT-11.\n3. Tìm nút Sửa / thêm người tham gia.',
    J="- Thấy meeting của mọi công ty.\n- Với MT-11: không có nút Sửa, không thêm/xoá được người tham gia (chỉ xem).\n"
      "- Với meeting mình tạo/chủ trì: màn Sửa có nút thêm (+) ở Thành phần - Phía Công ty, thêm/xoá được.",
    O=NOTE)
put(339, 'TC-ROLE-02',
    E="Quyền xem theo phòng ban: phạm vi xem theo phòng ban của người tạo meeting",
    G="Tài khoản chỉ có quyền 'Xem danh sách meeting theo phòng ban', quản lý phòng Kinh doanh 1.\n"
      "MT-12 do nhân viên phòng Kinh doanh 1 tạo; MT-13 do nhân viên phòng Kinh doanh 2 tạo.",
    H='1. Mở Meetings > Lịch Meeting.\n2. Quan sát danh sách.\n3. Mở MT-12, tìm nút Sửa.',
    J="- Thấy MT-12, không thấy MT-13 (trừ khi mình tạo/chủ trì/tham gia MT-13).\n"
      "- Phạm vi xét theo phòng ban của người tạo tại thời điểm tạo meeting.\n"
      "- MT-12 chỉ xem, không có nút Sửa (mình không phải người tạo/chủ trì).",
    O=NOTE)
put(340, 'TC-ROLE-03',
    E='Không có quyền nào trong nhóm meeting vẫn vào được menu, chỉ thấy meeting liên quan',
    G="Tài khoản không được gán quyền 'Xem danh sách meeting ...' nào; là chủ trì MT-01.",
    H='1. Mở Meetings > Lịch Meeting.\n2. Mở Sửa MT-01, thêm/xoá người tham gia.',
    J="- Menu vẫn hiện và vào được; chỉ thấy meeting mình tạo / chủ trì / tham gia.\n"
      "- Với MT-01 (mình chủ trì): thêm/xoá người tham gia bình thường.",
    O=NOTE)

# ---------------- dựng text cuối
out, bad = [], []
for r, (tid, cols) in sorted(E.items()):
    row = rows[r - 1]
    if row[COL['D']].strip() != tid.strip():
        bad.append((r, tid, row[COL['D']])); continue
    for c, v in cols.items():
        cur = row[COL[c]]
        if v == '__REPL__':
            v = NO_CREATE_PERM
        elif v == '__REPL_PRINT__':
            v = re.sub(r'user có quyền( Xem/In)?', 'tài khoản xem được meeting', cur, flags=re.I) or 'Tài khoản xem được meeting.'
            if v == cur: v = 'Tài khoản xem được meeting.'
        elif v == '__DROPCHECK__':
            v = re.sub(r'- *Kiểm tra quyền → *pass *\n?', '', cur)
        elif v.startswith('__APPEND__'):
            add = v[len('__APPEND__'):]
            v = cur.rstrip() + '\n' + add if add not in cur else cur
        if c == 'O' and cur.strip() and v not in cur:
            v = cur.rstrip() + '\n' + v
        if c == 'J' and r in (39, 40, 83, 86):
            pass
        if v != cur:
            out.append({'row': r, 'id': tid, 'col': c, 'text': v})
    # bỏ dòng 'Kiểm tra quyền → pass' ở expected của các case tạo mới
    if r in (39, 40, 83, 86):
        cur = row[COL['J']]
        nv = re.sub(r'- *Kiểm tra quyền → *pass *\n?', '', cur)
        if nv != cur: out.append({'row': r, 'id': tid, 'col': 'J', 'text': nv})
        if not any(o['row'] == r and o['col'] == 'O' for o in out):
            o = row[COL['O']]
            out.append({'row': r, 'id': tid, 'col': 'O', 'text': (o.rstrip() + '\n' if o.strip() else '') + NOTE})
print('lech ID:', bad)
print('so o can sua:', len(out), 'so dong:', len({o["row"] for o in out}))
json.dump(out, open(os.path.join(HERE, 'old_tc_edits.json'), 'w'), ensure_ascii=False, indent=1)
