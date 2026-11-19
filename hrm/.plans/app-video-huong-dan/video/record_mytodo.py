#!/usr/bin/env python3
"""Quay video "Việc của tôi" + Nhắc việc cá nhân (kịch bản: kich-ban-viec-cua-toi.md).

Trước khi quay: tools/prep_mytodo.py (dữ liệu theo ngày quay), app ở màn chọn phân hệ, thông báo app đã BẬT.
Chạy:   python3 record_mytodo.py                 → quay thật (~15')
        python3 record_mytodo.py --try 34 63     → chạy thử bước 34..63, không quay
        python3 record_mytodo.py --tts-only      → chỉ tạo lời đọc
Dựng:   NAME=mytodo OUT=huong-dan-viec-cua-toi python3 build_app.py
"""
import os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vc import *   # noqa
import vc
from datetime import date, timedelta
TODAY = date.today()

HRM_API = '/Users/dnsnamdang/Documents/DNSMEDIA/websites/ERP-HRM/HRM/hrm-api'
PHP = '/opt/homebrew/opt/php@7.4/bin/php'
TOP = (0, 100, 402, 230)          # vùng thanh trên (tab, ô tìm)
BOTTOM = (0, 760, 402, 874)       # vùng nút đáy

MENU = (36, 86)
SORT = (318, 197)
FILTER = (365, 197)
FAB = (200, 790)
ADD_NEW = (67, 317)               # sheet Gắn liên hệ: icon Thêm mới (dải Gần đây)
PHONE_BOOK = (148, 317)           # icon Danh bạ máy


def to_root():
    """Lùi về màn gốc Việc của tôi (có tab "Công việc của tôi") — nút góc trái ở màn con là Quay lại, ở gốc là Menu."""
    for _ in range(4):
        if find('Công việc của tôi', area=TOP):
            return
        back(); w(1.3)


def menu(item):
    to_root(); tap(*MENU); w(1.0); tap_text(item, area=(0, 280, 280, 800)); w(0.4)


def back():
    tap(36, 86)


def create_todo():
    tap(*FAB); w(1.2); tap_text('Nhắc việc cá nhân'); wait_text('Tiêu đề')


def field(label, value, dy=36):
    """Bấm ô dưới nhãn `label` rồi gõ."""
    tap_text(label, dy=dy); w(0.5); text(value); w(0.3)


def artisan(cmd):
    subprocess.run([PHP, 'artisan', *cmd.split()], cwd=HRM_API, capture_output=True)


def push_latest(type_like):
    """Banner iOS = đúng dòng thông báo mới nhất trong DB (tools/push_payload.php)."""
    out = os.path.join(vc.WORK, 'push.apns')
    if os.path.exists(out):
        os.remove(out)
    env = dict(os.environ, EMP='13', TYPE_LIKE=type_like, OUT=out)
    code = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tools', 'push_payload.php')).read()
    subprocess.run([PHP, 'artisan', 'tinker', f'--execute={code}'], cwd=HRM_API, env=env, capture_output=True)
    if not os.path.exists(out):
        print(f'   ! không có thông báo {type_like} trong DB — không đẩy banner', flush=True)
        return
    subprocess.run(['xcrun', 'simctl', 'push', DEV, 'com.tanphat.app', out], capture_output=True)


DUE_AT = {}


def due_now_todo():
    """Nhắc việc có hạn = PHÚT KẾ TIẾP. Lệnh nhắc bỏ qua việc được tạo SAU mốc nhắc của nó (WorkReminderService:
    "phiếu lập sau mốc nhắc") ⇒ phải tạo trước giờ hạn, tới chương Thông báo mới chạy lệnh (wait_due)."""
    import datetime as _dt, json as _json, urllib.request as _u
    now = (_dt.datetime.now() + _dt.timedelta(minutes=2)).replace(second=0, microsecond=0)
    DUE_AT['t'] = now
    tok = subprocess.run([PHP, 'artisan', 'tinker', '--execute=echo auth("api")->login(\\App\\Models\\TpEmployee::find(13));'],
                         cwd=HRM_API, capture_output=True, text=True).stdout.strip().splitlines()[-1]
    body = {'list_id': 742, 'title': 'Xác nhận đơn hàng với Gara Thành Công', 'due_date': now.date().isoformat(),
            'due_time': now.strftime('%H:%M'), 'sub_items': []}
    req = _u.Request('http://127.0.0.1:8001/api/v1/assign/my-todo/todos', data=_json.dumps(body).encode(), method='POST',
                     headers={'Authorization': 'Bearer ' + tok, 'Accept': 'application/json', 'Content-Type': 'application/json'})
    _u.urlopen(req).read()


def wait_due():
    """Chờ tới giờ hạn của nhắc việc vừa tạo (+3s) — đoạn chờ ghi vào cuts để cắt khỏi video."""
    import datetime as _dt
    t = vc.now()
    while DUE_AT.get('t') and _dt.datetime.now() < DUE_AT['t'] + _dt.timedelta(seconds=3):
        w(0.5)
    if vc.now() - t > 0.5:
        vc.cuts.append([round(t + 0.1, 3), round(vc.now(), 3)])


CH = ['Mở đầu', 'Việc của tôi', 'Danh sách', 'Tìm · sắp xếp · lọc', 'Lịch làm việc', 'Tạo nhắc việc',
      'Báo lịch lãnh đạo', 'Gắn liên hệ', 'Dùng nhắc việc', 'Chi tiết nhắc việc', 'Danh bạ cá nhân',
      'Lịch lãnh đạo', 'Thông báo', 'Cài đặt nhắc việc', 'Kết']


def S_(ch, say, act=None, **kw):
    return dict(ch=CH[ch], say=say, act=act, **kw)


S = [
    # 1. Mở đầu
    S_(0, 'Xin chào. Các bạn đang xem video hướng dẫn sử dụng Phần mềm quản trị ERP TPE.'),
    S_(0, 'Video này giới thiệu màn Việc của tôi trên ứng dụng di động, và hướng dẫn chi tiết Nhắc việc cá nhân, Danh bạ cá nhân, cùng phần cài đặt nhắc việc.'),
    # 2. Việc của tôi là gì
    S_(1, 'Sau khi đăng nhập, bạn chọn phân hệ Công việc.', lambda: hl('CÔNG VIỆC', full_row=True, h=60)),
    S_(1, 'Màn đầu tiên là Việc của tôi. Đây là nơi gom mọi việc liên quan tới bạn vào một chỗ: nhiệm vụ, vấn đề, meeting, các loại phiếu, và nhắc việc cá nhân.',
       lambda: (tap_text('CÔNG VIỆC', exact=True), wait_text('Công việc của tôi'), w(0.6), hl('HÔM NAY', full_row=True, h=420))),
    S_(1, 'Màn có hai tab: Công việc của tôi, xem dạng danh sách; và Lịch làm việc, xem theo ngày.',
       lambda: hl(rect=(8, 116, 386, 42))),
    # 3. Danh sách
    S_(2, 'Việc được chia nhóm theo hạn: Hôm nay, Ngày mai, Tuần này, Tuần sau, Sau đó, Không hạn, và nhóm Quá hạn ở cuối. Số bên cạnh là số việc trong nhóm.',
       lambda: (tap_text('HÔM NAY'), w(0.8), hl('NGÀY MAI', full_row=True, h=230))),
    S_(2, 'Nhóm Tuần này tính cả việc của hôm nay và ngày mai, để bạn nhìn được cả tuần một lúc.',
       lambda: hl('TUẦN NÀY', full_row=True, h=34)),
    S_(2, 'Bấm vào tiêu đề nhóm để mở ra hoặc thu gọn. Mặc định chỉ mở nhóm Hôm nay.',
       lambda: (tap_text('QUÁ HẠN'), w(1.0))),
    S_(2, 'Mỗi thẻ cho biết loại việc, vai trò của bạn, trạng thái, tên việc và hạn. Việc quá hạn có chữ đỏ, ghi trễ bao nhiêu ngày.',
       lambda: hl('Được giao', area=(0, 400, 402, 800), full_row=True, h=100)),
    S_(2, 'Với meeting, thẻ ghi giờ họp và địa điểm. Nếu chưa xác nhận, bạn bấm Xác nhận tham gia ngay trên thẻ.',
       lambda: (tap_text('QUÁ HẠN'), w(0.8), tap_text('HÔM NAY'), w(1.0), hl('Họp giao ban', full_row=True, h=130))),
    S_(2, 'Mình bấm Xác nhận tham gia. Ứng dụng báo đã xác nhận, nhãn trên thẻ đổi luôn.',
       lambda: (tap_text('Xác nhận tham gia'), w(1.2))),
    S_(2, 'Bấm vào thẻ để mở chi tiết. Ví dụ đây là chi tiết một nhiệm vụ.',
       lambda: (tap_text('Lập báo giá cầu nâng'), wait_text('Người làm'))),
    S_(2, 'Bấm quay lại để về danh sách. Mỗi loại việc mở đúng màn chi tiết của nó, các loại này có video hướng dẫn riêng.',
       lambda: (back(), w(1.0))),
    # 4. Tìm, sắp xếp, lọc
    S_(3, 'Muốn tìm nhanh, gõ tên công việc vào ô tìm kiếm, danh sách lọc ngay khi gõ.',
       lambda: (type_in('Tìm theo tên công việc', 'báo giá'), w(1.0))),
    S_(3, 'Xoá chữ để hiện lại đầy đủ.', lambda: (clear_field(), w(0.8))),
    S_(3, 'Nút này để sắp xếp. Danh sách vẫn chia nhóm theo hạn, chỉ đổi thứ tự trong từng nhóm.',
       lambda: (tap(*SORT), w(1.0))),
    S_(3, 'Có năm cách: Hạn hoàn thành, Cập nhật gần nhất, Tạo gần nhất, Ưu tiên cao trước, và Tên A tới Z.',
       lambda: hl('Hạn hoàn thành', full_row=True, h=200)),
    S_(3, 'Ví dụ chọn Ưu tiên cao trước. Lựa chọn được ghi nhớ cho lần sau, và nút sáng màu để bạn biết đang sắp khác mặc định.',
       lambda: (tap_text('Ưu tiên cao trước'), w(1.0), hl(rect=(296, 177, 44, 40)))),
    S_(3, 'Mình chọn lại Hạn hoàn thành như mặc định.',
       lambda: (tap(*SORT), w(1.0), tap_text('Hạn hoàn thành'), w(0.8))),
    S_(3, 'Nút Bộ lọc có hai điều kiện: Loại việc và Trạng thái.',
       lambda: (tap(*FILTER), w(1.2))),
    S_(3, 'Loại việc chọn được nhiều loại cùng lúc. Ví dụ chỉ chọn Nhắc việc cá nhân.',
       lambda: (hl('Loại việc', full_row=True, h=180), tap_text('Nhắc việc cá nhân', area=(0, 300, 402, 520)))),
    S_(3, 'Trạng thái có bốn nhóm: Chưa làm, Đang làm, Hoàn thành, và Dừng hoặc Hủy. Để trống thì ứng dụng chỉ hiện việc chưa xong.',
       lambda: hl('Trạng thái', full_row=True, h=110)),
    S_(3, 'Mình chọn Chưa làm, Đang làm và Hoàn thành, rồi bấm Xem kết quả.',
       lambda: (tap_text('Chưa làm', area=(0, 540, 402, 640)), w(0.4), tap_text('Đang làm', area=(0, 540, 402, 640)), w(0.4),
                tap_text('Hoàn thành', area=(0, 540, 402, 640)), w(0.8), tap_text('Xem', area=BOTTOM), w(1.2))),
    S_(3, 'Điều kiện đang lọc hiện thành các nhãn phía trên. Chạm vào nhãn để sửa, bấm dấu x để bỏ.',
       lambda: hl(rect=(8, 220, 386, 44))),
    S_(3, 'Vì có chọn Hoàn thành, cuối danh sách có thêm nhóm Đã kết thúc trong 30 ngày gần nhất. Thẻ trong nhóm này có màu xám.',
       lambda: (tap_text('ĐÃ KẾT THÚC'), w(1.0), hl('ĐÃ KẾT THÚC', full_row=True, h=160))),
    S_(3, 'Muốn bỏ hết điều kiện, mở lại Bộ lọc, bấm Làm mới rồi Xem kết quả.',
       lambda: (tap(*FILTER), w(1.2), tap_text('Làm mới', area=BOTTOM), w(0.8), tap_text('Xem', area=BOTTOM), w(1.0))),
    S_(3, 'Kéo danh sách xuống để tải lại dữ liệu mới nhất.',
       lambda: (swipe(200, 300, 200, 650, 600), w(1.5))),
    # 5. Lịch làm việc
    S_(4, 'Tab Lịch làm việc xếp các việc theo ngày.',
       lambda: (tap_text('Lịch làm việc', area=TOP), wait_text('Hôm nay', area=(0, 150, 402, 260)))),
    S_(4, 'Dải tuần hiện thứ, ngày dương và ngày âm lịch. Chấm màu dưới mỗi ngày cho biết ngày đó có những loại việc nào.',
       lambda: hl(rect=(8, 218, 386, 66))),
    S_(4, 'Bấm vào một ngày, phía dưới hiện danh sách việc từ ngày đó tới hết tuần.',
       lambda: (tap_text('T4', area=(0, 200, 402, 260), dy=20), w(1.5))),
    S_(4, 'Bấm Tháng để xem cả tháng. Bạn cũng có thể vuốt lịch xuống để mở tháng, vuốt lên để thu về tuần.',
       lambda: (tap_text('Tháng', area=(250, 150, 402, 200)), w(1.5))),
    S_(4, 'Hai mũi tên để sang kỳ trước hoặc kỳ sau. Bấm Hôm nay để về ngày hiện tại.',
       lambda: (tap(164, 195), w(1.2), tap_text('Hôm nay', area=(0, 150, 402, 200)), w(1.2))),
    S_(4, 'Lịch có Bộ lọc riêng theo loại việc và trạng thái. Nút xoay tròn bên cạnh để bỏ lọc và tải lại.',
       lambda: (tap_text('Bộ lọc'), w(1.2))),
    S_(4, 'Bấm Tuần để thu lịch lại. Giờ mình đi vào phần chính: Nhắc việc cá nhân.',
       lambda: (tap(200, 150), w(0.8), tap_text('Tuần', area=(250, 150, 402, 200)), w(0.8), tap_text('Công việc của tôi', area=TOP), w(1.0))),
    # 6. Tạo nhắc việc — gọi điện cho khách, liên hệ NHẬP TAY
    S_(5, 'Bấm nút Tạo mới ở giữa thanh dưới.', lambda: (tap(*FAB), w(1.2))),
    S_(5, 'Từ đây tạo được mọi loại việc: Nhắc việc cá nhân, Nhiệm vụ, Meeting, các loại phiếu, và Vấn đề.',
       lambda: hl('Nhắc việc cá nhân', full_row=True, h=330)),
    S_(5, 'Nhắc việc cá nhân là việc riêng của bạn, có thể chia thành nhiều bước. Ví dụ mình cần nhắc gọi điện cho khách hàng.',
       lambda: (tap_text('Nhắc việc cá nhân'), wait_text('Tiêu đề'))),
    S_(5, 'Tiêu đề là ô bắt buộc. Chưa nhập mà bấm Lưu, ứng dụng báo đỏ ngay dưới ô.',
       lambda: (tap_btn('Lưu', area=BOTTOM), w(1.0), hl('Tiêu đề', full_row=True, h=80))),
    S_(5, 'Nhập tiêu đề: Gọi điện cho khách xác nhận lịch giao hàng.',
       lambda: (type_in('Nhập tiêu đề', 'Gọi điện cho khách xác nhận lịch giao hàng'), w(0.4))),
    S_(5, 'Việc này liên quan tới khách, nên bấm Gắn liên hệ.',
       lambda: (tap(200, 100), tap_text('Gắn liên hệ'), wait_text('Gần đây'))),
    S_(5, 'Sheet Gắn liên hệ hiện danh bạ cá nhân của bạn, xếp theo chữ cái, có thanh chữ cái bên phải để nhảy nhanh.',
       lambda: hl(rect=(8, 380, 386, 300))),
    S_(5, 'Dải Gần đây giữ những người bạn gắn gần nhất, kèm hai nút: Thêm mới để nhập tay, và Danh bạ máy để chọn từ điện thoại.',
       lambda: hl('Gần đây', full_row=True, h=120)),
    S_(5, 'Khách này chưa có trong điện thoại, mình bấm Thêm mới để nhập tay.',
       lambda: (tap(*ADD_NEW), wait_text('Nhập tên'))),
    S_(5, 'Nhập tên: Anh Minh.',
       lambda: (type_in('Nhập tên', 'Anh Minh'))),
    S_(5, 'Nhập số điện thoại. Tên và số điện thoại là bắt buộc, ứng dụng kiểm tra số có hợp lệ không.',
       lambda: (type_in('Nhập số điện thoại', '0987654321'))),
    S_(5, 'Địa chỉ và Ghi chú thì tuỳ chọn.',
       lambda: (type_in('Nhập địa chỉ', 'Khu công nghiệp Quang Minh, Hà Nội'),
                type_in('Nhập ghi chú', 'Công ty Hoà Phát, phụ trách mua hàng'), w(0.4))),
    S_(5, 'Lưu nhắc việc xong, người này tự vào danh bạ cá nhân, lần sau chỉ cần chọn lại. Nếu số đã có trong danh bạ, ứng dụng dùng lại người cũ, không tạo trùng.',
       lambda: hl('Lưu nhắc việc xong', padx=14)),
    S_(5, 'Bấm Gắn liên hệ. Thông tin khách đã vào form, có nút gọi nhanh. Chạm vào thẻ để đổi người, bấm dấu x để gỡ.',
       lambda: (tap_text('Gắn liên hệ', area=(0, 400, 260, 860)), w(1.2), hl('Anh Minh', full_row=True, h=56))),
    S_(5, 'Nhập mô tả: hỏi khách giờ nhận hàng và người ký nhận.',
       lambda: (type_in('Nhập mô tả', 'Hỏi khách giờ nhận hàng và người ký nhận'))),
    S_(5, 'Phần Các bước giúp chia việc thành từng bước. Gõ nội dung rồi nhấn Enter là thêm xong một bước.',
       lambda: (tap_text('Thêm bước'), w(0.4), text('Gọi xác nhận giờ giao'), keys('return'), w(0.4))),
    S_(5, 'Thêm tiếp các bước: Báo lại kho, Gửi tin nhắn xác nhận. Bấm thùng rác cạnh bước để xoá.',
       lambda: (text('Báo lại kho'), keys('return'), w(0.3), text('Gửi tin nhắn xác nhận'), keys('return'), w(0.4), tap(200, 100))),
    S_(5, 'Loại nhắc việc giúp phân nhóm. Có sẵn Việc cá nhân và Việc công ty.',
       lambda: (swipe(200, 600, 200, 380, 400), w(0.6), tap_text('Việc cá nhân', area=(0, 350, 402, 760)), w(1.2))),
    S_(5, 'Bạn tự thêm được loại mới, ví dụ Khách hàng. Bấm Thêm là loại mới được chọn luôn. Muốn sửa tên hoặc xoá loại thì làm trên web.',
       lambda: (tap_text('Thêm loại nhắc việc'), w(0.8), text('Khách hàng'), w(0.3),
                tap_text('Thêm', area=(280, 380, 402, 640)), w(1.5))),
    S_(5, 'Chọn ngày hạn trên lịch.',
       lambda: (tap_text('dd/mm/yyyy'), w(1.2), pick_date(TODAY + timedelta(days=1)))),
    S_(5, 'Chọn giờ hạn, ví dụ 9 giờ sáng. Có giờ hạn thì ứng dụng mới nhắc đúng giờ. Không chọn ngày hạn thì việc nằm ở nhóm Không hạn.',
       lambda: (tap_text('hh:mm'), w(1.2), set_wheel(178, 9), set_wheel(224, 0, modulo=60),
                tap_text('Chọn', area=(200, 780, 402, 840), fallback=(297, 808)), w(0.6))),
    S_(5, 'Bấm Lưu. Nhắc việc đã được tạo, nằm ở nhóm Ngày mai.',
       lambda: (tap_btn('Lưu', area=BOTTOM), w(1.5))),
    # 6a. Báo lịch làm việc lãnh đạo — nhắc việc riêng: đi công tác
    S_(6, 'Tiếp theo là Báo lịch làm việc lãnh đạo. Ví dụ bạn sắp đi công tác, tạo nhắc việc: Đi công tác TP Hồ Chí Minh gặp nhà cung cấp.',
       lambda: (create_todo(), type_in('Nhập tiêu đề', 'Đi công tác TP Hồ Chí Minh gặp nhà cung cấp'), tap(200, 100), w(0.4))),
    S_(6, 'Người được cấp quyền báo lịch sẽ thấy thêm phần Báo lịch làm việc lãnh đạo: báo cả công ty khi bạn đi vắng. Không có quyền thì phần này không hiện.',
       lambda: hl('Báo lịch làm việc lãnh đạo', full_row=True, h=60)),
    S_(6, 'Bật lên, Ngày hạn và Giờ hạn chuyển vào khung này, thêm Ngày bắt đầu và Giờ bắt đầu.',
       lambda: (tap(345, find('Báo lịch làm việc lãnh đạo')[1] + 8), w(1.2), swipe(200, 650, 200, 450, 400), w(0.6))),
    S_(6, 'Chọn đủ ngày bắt đầu và ngày hạn. Ngày hạn phải từ ngày bắt đầu trở đi, sai là báo đỏ.',
       lambda: (tap_text('dd/mm/yyyy'), w(1.2), pick_date_m(TODAY + timedelta(days=3)), w(0.4),
                tap_text('Ngày hạn', dy=37), w(1.2), pick_date(TODAY + timedelta(days=4)), w(0.6),
                swipe(200, 650, 200, 350, 400), w(0.6))),
    S_(6, 'Khung này cho xem trước thông báo cả công ty sẽ nhận: ông bà nào vắng mặt, từ ngày nào tới ngày nào.',
       lambda: hl('Cả công ty sẽ nhận thông báo', full_row=True, h=130)),
    S_(6, 'Bỏ chọn Gửi kèm tiêu đề nếu chỉ muốn báo thời gian vắng, không lộ nội dung việc. Mô tả, các bước và liên hệ không bao giờ gửi đi.',
       lambda: (tap_text('Gửi kèm tiêu đề', dx=-120), w(1.0), tap_text('Gửi kèm tiêu đề', dx=-120), w(0.6))),
    S_(6, 'Bấm Lưu, ứng dụng hỏi lại vì nhắc việc này sẽ thông báo cho toàn công ty.',
       lambda: (tap_btn('Lưu', area=BOTTOM), w(1.2), hl('Thông báo cho toàn Công ty', padx=20))),
    S_(6, 'Bấm Đồng ý. Nhắc việc được lưu, mọi nhân viên của công ty nhận thông báo, trừ chính bạn.',
       lambda: (tap_text('Đồng ý'), w(0.3))),
    S_(6, 'Sau khi đã báo, nếu bạn đổi ngày, tắt công tắc, xoá, hay hoàn thành sớm nhắc việc, cả công ty đều nhận thông báo cập nhật.',
       lambda: w(1.0)),
    # 6b. Danh bạ máy
    S_(7, 'Tạo thêm một nhắc việc: Gửi báo giá cho chị Kate.',
       lambda: (create_todo(), type_in('Nhập tiêu đề', 'Gửi báo giá cho chị Kate'), tap(200, 100))),
    S_(7, 'Người này đã có trong điện thoại, bấm Danh bạ máy.',
       lambda: (tap_text('Gắn liên hệ'), wait_text('Gần đây'), w(0.4), tap(*PHONE_BOOK), w(2.0))),
    S_(7, 'Danh bạ điện thoại mở ra, chọn đúng người. Tên và số được điền sẵn. Ứng dụng chỉ đọc đúng người bạn chọn, không đọc cả danh bạ.',
       lambda: (tap_text('Bell Kate'), w(1.5), hl('Kate Bell', full_row=True, h=56))),
    S_(7, 'Nếu người được chọn chưa có số, ứng dụng mở form Liên hệ mới để bạn nhập số.', lambda: w(0.5)),
    S_(7, 'Chọn hạn hôm nay rồi bấm Lưu.',
       lambda: (tap_text('dd/mm/yyyy'), w(1.2), pick_date(TODAY), tap_btn('Lưu', area=BOTTOM), w(1.5))),
    # 6c. Tìm liên hệ có sẵn + tra khách hàng công ty
    S_(7, 'Nhắc việc thứ ba: Hẹn gặp anh Toàn trao đổi thiết bị.',
       lambda: (create_todo(), type_in('Nhập tiêu đề', 'Hẹn gặp anh Toàn trao đổi thiết bị'), tap(200, 100))),
    S_(7, 'Muốn tìm người đã có, gõ tên vào ô tìm. Anh Minh vừa nhập tay ở trên đã có trong danh bạ.',
       lambda: (tap_text('Gắn liên hệ'), wait_text('Gần đây'), type_in('Tìm tên hoặc số', 'Minh'), w(1.2))),
    S_(7, 'Còn nếu gõ đủ số điện thoại, ứng dụng tra luôn trong danh mục khách hàng của công ty.',
       lambda: (clear_field(), w(0.3), text('0908396342'), wait_text('KHÁCH HÀNG CÔNG TY'))),
    S_(7, 'Số này khớp người liên hệ Bùi Thanh Toàn của Trường Cao đẳng Dầu khí, có nhãn KH công ty. Phải gõ đủ số mới tra được, không tìm khách theo tên.',
       lambda: hl('KHÁCH HÀNG CÔNG TY', full_row=True, h=90)),
    S_(7, 'Bên dưới còn hai lối khác: Chọn từ danh bạ điện thoại, hoặc Tạo liên hệ mới với đúng số vừa gõ.',
       lambda: hl('Tạo liên hệ mới', full_row=True, h=80)),
    S_(7, 'Chọn khách hàng. Thông tin được chép sang danh bạ của bạn.',
       lambda: (tap_text('Bùi Thanh Toàn'), w(1.5))),
    S_(7, 'Chọn hạn tuần sau rồi bấm Lưu.',
       lambda: (tap_text('dd/mm/yyyy'), w(1.2), pick_date(TODAY + timedelta(days=8)), tap_btn('Lưu', area=BOTTOM), w(1.5))),
    # 6d. Thoát khi chưa lưu
    S_(5, 'Nếu đang nhập dở mà bấm quay lại, ứng dụng hỏi lại để bạn không mất dữ liệu.',
       lambda: (create_todo(), type_in('Nhập tiêu đề', 'Mua quà sinh nhật khách'), tap(200, 100), w(0.3), back(), w(1.0))),
    S_(5, 'Bạn chọn Lưu và quay lại, Quay lại không lưu, hoặc Ở lại màn này.',
       lambda: hl('Lưu và quay lại', full_row=True, h=130)),
    S_(5, 'Ở đây mình bỏ, bấm Quay lại không lưu.',
       lambda: (tap_text('Quay lại, không lưu'), w(1.0))),
    # 7. Dùng nhắc việc ngay trên danh sách
    S_(8, 'Nhắc việc mới nằm ở nhóm Ngày mai và cả nhóm Tuần này. Thẻ có ô vuông để đánh dấu xong, tên khách kèm nút gọi, và số bước đã xong.',
       lambda: (tap_text('HÔM NAY'), w(0.6), tap_text('NGÀY MAI'), w(1.0), hl('Gọi điện cho khách', full_row=True, h=110))),
    S_(8, 'Bấm Xem bước để mở các bước ngay trên thẻ, bấm Thu gọn để đóng lại.',
       lambda: (tap_text('Xem bước'), w(1.0))),
    S_(8, 'Tick một bước, ứng dụng hỏi lại cho chắc, bấm Hoàn thành là xong bước đó.',
       lambda: (tap_row('Gọi xác nhận giờ giao', 42), w(1.2), tap_btn('Hoàn thành', area=(0, 380, 260, 720)), w(1.2))),
    S_(8, 'Bấm vào tên khách để xem thông tin người đó.',
       lambda: (tap_text('Anh Minh'), wait_text('Nhắn tin'))),
    S_(8, 'Quay lại danh sách.', lambda: (back(), w(1.0))),
    S_(8, 'Đây là cảnh trên điện thoại thật: tới giờ gọi khách, bấm nút xanh trên thẻ, điện thoại hỏi lại số rồi gọi luôn, không phải tìm lại số.',
       lambda: w(9.2), clip='goi-that-iphone.mp4'),
    S_(8, 'Gọi xong quay lại ứng dụng để đánh dấu các bước đã làm.', lambda: w(0.3)),
    # 8. Chi tiết nhắc việc
    S_(9, 'Bấm vào thẻ để mở chi tiết nhắc việc.',
       lambda: (tap_text('Gọi điện cho khách'), wait_text('LIÊN HỆ'))),
    S_(9, 'Đầu màn là tiêu đề, loại nhắc việc và hạn. Bên dưới là Liên hệ, Mô tả và các bước con.',
       lambda: hl(rect=(8, 120, 386, 90))),
    S_(9, 'Ở màn chi tiết cũng có nút Gọi ngay khối Liên hệ, bấm là gọi luôn như trên thẻ. Bấm vào tên liên hệ để mở thông tin người đó.',
       lambda: hl('LIÊN HỆ', full_row=True, h=70)),
    S_(9, 'Tick vòng tròn để hoàn thành bước.',
       lambda: (tap_row('Báo lại kho', 31), w(1.2), tap_btn('Hoàn thành', area=(0, 380, 260, 720), tries=3), w(1.0))),
    S_(9, 'Bấm vào tên bước để sửa nội dung rồi Lưu. Sheet này cũng có nút Xóa bước.',
       lambda: (tap_text('Gửi tin nhắn xác nhận'), w(1.2), clear_field(), text('Gửi tin nhắn xác nhận cho khách'), w(0.5),
                hl('Xóa bước', padx=16), w(1.0), tap_text('Lưu', area=(0, 470, 200, 540)), w(1.2))),
    S_(9, 'Bấm Thêm bước để thêm bước mới ngay tại đây.',
       lambda: (tap_text('Thêm bước'), w(1.0), type_in(None, 'Gọi lại nếu khách chưa nghe máy'), w(0.6), tap_btn('Lưu', area=(0, 380, 402, 720)), w(1.2))),
    S_(9, 'Nút Sửa mở lại form để đổi bất kỳ thông tin nào.',
       lambda: (tap_btn('Sửa', area=(0, 560, 200, 860)), wait_text('Tiêu đề'))),
    S_(9, 'Ví dụ đổi giờ hạn thành 10 giờ rồi bấm Lưu. Lưu xong ứng dụng về lại danh sách.',
       lambda: (swipe(200, 650, 200, 380, 400), w(0.8), tap_text('09:00'), w(1.2), set_wheel(178, 10), tap_text('Chọn', area=(200, 780, 402, 840), fallback=(297, 808)),
                w(0.6), tap_btn('Lưu', area=BOTTOM), w(1.8))),
    S_(9, 'Mở lại thẻ, làm xong việc thì bấm Đánh dấu hoàn thành. Còn bước chưa xong thì ứng dụng nhắc là các bước đó cũng sẽ được tick.',
       lambda: (tap_text('Gọi điện cho khách'), wait_text('LIÊN HỆ'), tap_text('Đánh dấu hoàn thành'), w(1.2),
                hl('Xác nhận hoàn thành', full_row=True, h=130))),
    S_(9, 'Xác nhận. Tiêu đề có gạch ngang. Tick hết từng bước con cũng tự hoàn thành cả nhắc việc.',
       lambda: (tap_btn('Hoàn thành', area=(0, 380, 260, 720)), w(1.5))),
    S_(9, 'Nút đổi thành Mở lại nếu bạn cần làm tiếp. Mở lại thì các bước cũng được bỏ tick.',
       lambda: (hl('Mở lại', padx=30), w(1.2), tap_text('Mở lại'), w(1.5))),
    S_(9, 'Muốn xoá nhắc việc không cần nữa, mở chi tiết và bấm Xóa.',
       lambda: (back(), w(1.2), tap_text('Mua văn phòng phẩm'), wait_text('BƯỚC CON'), tap_row('Sửa', 297, area=(0, 250, 200, 860)), w(1.2))),
    S_(9, 'Ứng dụng hỏi lại vì dữ liệu đã xoá không khôi phục được. Bấm Xóa để xác nhận.',
       lambda: (hl('không khôi phục', padx=20), w(1.5), tap(122, find('không khôi phục')[1] + 44), w(1.5))),
    # 9. Danh bạ cá nhân
    S_(10, 'Mọi liên hệ bạn gắn vào nhắc việc được gom ở Danh bạ cá nhân, trong menu bên trái.',
       lambda: (menu('Danh bạ cá nhân'), wait_text('người'))),
    S_(10, 'Liên hệ còn việc chờ có dòng Hẹn kèm ngày giờ và tên việc, quá hạn thì chữ đỏ. Nút xanh bên phải để gọi nhanh.',
       lambda: hl('Chị Lan', full_row=True, h=70)),
    S_(10, 'Ô tìm tìm theo tên hoặc số điện thoại.',
       lambda: (type_in('Tìm tên hoặc số', 'Minh'), w(1.5), clear_field(), w(0.3), tap(200, 88), w(0.6))),
    S_(10, 'Nút thêm người ở góc trên để thêm liên hệ thẳng vào danh bạ.',
       lambda: (tap(317, 86), wait_text('Liên hệ mới'))),
    S_(10, 'Bạn chọn từ danh bạ điện thoại, hoặc nhập tay như lúc nãy.',
       lambda: (tap_text('Chọn từ danh bạ điện thoại'), w(2.2), tap_text('Taylor David'), w(1.5))),
    S_(10, 'Bấm Lưu. David Taylor đã vào danh bạ cá nhân.',
       lambda: (tap_text('Lưu', area=(0, 450, 250, 860)), w(1.8))),
    S_(10, 'Nếu số đã có, ứng dụng báo: Số này đã có trong danh bạ, kèm tên người đó.',
       lambda: (tap(317, 86), wait_text('Liên hệ mới'), type_in('Nhập tên', 'Chị Kate'), w(0.3),
                type_in('Nhập số điện thoại', '5555648583'), w(1.2), tap_btn('Lưu', area=(0, 300, 250, 860)),
                w(0.5), hl('đã có trong danh bạ', padx=16))),
    S_(10, 'Bấm vào một người để xem chi tiết.',
       lambda: (w(1.5), tap_text('Anh Minh'), wait_text('Nhắn tin'))),
    S_(10, 'Ba nút: Gọi, Nhắn tin, và Tạo nhắc việc.', lambda: hl('Nhắn tin', full_row=True, h=56)),
    S_(10, 'Nhắn tin mở ứng dụng tin nhắn của điện thoại để nhắn cho người này.',
       lambda: (tap_text('Nhắn tin'), w(3.0))),
    S_(10, 'Bấm quay lại góc trên để về ứng dụng.',
       lambda: (tap(51, 40), w(1.5))),
    S_(10, 'Phần dưới là các nhắc việc với người này, chia Sắp tới và Đã xong, kèm loại nhắc việc và hạn còn bao nhiêu ngày.',
       lambda: hl('Nhắc việc với', full_row=True, h=150)),
    S_(10, 'Tạo nhắc việc từ đây sẽ điền sẵn người này vào form.',
       lambda: (tap_text('Tạo nhắc việc', area=(250, 300, 402, 460)), wait_text('Tiêu đề'), hl('Anh Minh', full_row=True, h=56))),
    S_(10, 'Mình không tạo, bấm Hủy để quay lại.',
       lambda: (tap_text('Hủy', area=(0, 780, 200, 840)), w(1.2))),
    S_(10, 'Menu ba chấm có Sửa liên hệ, Lưu vào danh bạ điện thoại, và Xoá liên hệ.',
       lambda: (tap(317, 86), w(1.2), hl('Sửa liên hệ', full_row=True, h=150))),
    S_(10, 'Sửa liên hệ để cập nhật thông tin, ví dụ thêm ghi chú rồi Lưu.',
       lambda: (tap_text('Sửa liên hệ'), w(1.3), tap_text('phụ trách mua hàng', area=(0, 420, 402, 860)), w(0.8), keys('cmd+right'),
                text(', hay nghe máy buổi sáng'), w(1.2), tap_btn('Lưu', area=(0, 420, 250, 860)), w(1.5))),
    S_(10, 'Lưu vào danh bạ điện thoại mở màn thêm liên hệ của máy, thông tin đã điền sẵn.',
       lambda: (tap(317, 86), w(1.2), tap_text('Lưu vào danh bạ điện thoại'), w(3.0))),
    S_(10, 'Ở đây mình đóng lại, không lưu vào máy.',
       lambda: (tap(37, 99), w(1.2), tap_text('Discard Changes'), w(1.2))),
    S_(10, 'Xoá liên hệ không cần nữa, ví dụ David Taylor.',
       lambda: (back(), w(1.2), tap_text('David Taylor'), wait_text('Nhắn tin'), tap(317, 86), w(1.2), tap_text('Xoá liên hệ'), w(1.2))),
    S_(10, 'Các nhắc việc đang gắn với người này vẫn giữ nguyên, chỉ bỏ phần liên hệ. Danh bạ trên điện thoại không bị ảnh hưởng.',
       lambda: (hl('khỏi danh bạ', full_row=True, h=120), w(1.0), tap_btn('Xoá liên hệ', area=(0, 380, 260, 760), fallback=(122, 560)), w(1.5))),
    # 10. Lịch làm việc lãnh đạo
    S_(11, 'Lịch vắng mà lãnh đạo báo từ nhắc việc hiện ở menu Lịch làm việc lãnh đạo. Mọi nhân viên đều xem được.',
       lambda: (due_now_todo(), menu('Lịch làm việc lãnh đạo'), wait_text('Bảng tuần'), w(1.0))),
    S_(11, 'Bảng tuần: mỗi ô chia buổi sáng và buổi chiều. Xanh là có mặt, vàng là vắng mặt, xám là ngoài ca hoặc nghỉ.',
       lambda: hl('D. Admin', full_row=True, h=50)),
    S_(11, 'Chạm vào ô vàng để xem thời gian và nội dung lịch vắng.',
       lambda: (tap(233, find('D. Admin')[1] + 8), w(1.5))),
    S_(11, 'Bấm Đóng để quay lại.', lambda: (tap(200, 150), w(1.0))),
    S_(11, 'Chế độ Theo ngày cho biết hôm đó bao nhiêu người vắng, bao nhiêu người có mặt.',
       lambda: (tap_text('Theo ngày'), w(1.8))),
    S_(11, 'Dòng thời gian chia Đang vắng, Sắp tới, và Đã qua trong 30 ngày, tìm được theo tên lãnh đạo.',
       lambda: (tap_text('Dòng thời gian'), w(1.8))),
    # 10b. Thông báo
    S_(12, 'Tới giờ nhắc, điện thoại hiện thông báo nhắc việc, kể cả khi đang dùng ứng dụng khác.',
       lambda: (wait_due(), artisan('assign:send-work-reminders'), home(), w(1.2), push_latest('work_reminder.personal'), w(2.0))),
    S_(12, 'Bấm vào thông báo là mở thẳng màn Việc của tôi.',
       lambda: (tap(200, 100), w(2.5))),
    S_(12, 'Mọi thông báo cũng lưu trong chuông ở góc trên, xem lại được bất cứ lúc nào.',
       lambda: (tap(374, 86), w(2.0))),
    S_(12, 'Mỗi sáng có việc, bạn nhận Bản tin sáng tóm tắt việc trong ngày.',
       lambda: (artisan('assign:send-work-digest'), home(), w(1.2), push_latest('work_reminder.digest'), w(2.0))),
    S_(12, 'Bấm vào bản tin cũng mở Việc của tôi, để bạn bắt đầu ngày làm việc.',
       lambda: (tap(200, 100), w(2.5))),
    # 11. Cài đặt nhắc việc
    S_(13, 'Cuối cùng, trong Cài đặt, nhóm Thông báo, có mục Nhắc việc.',
       lambda: (to_root(), tap(*MENU), w(1.0), tap_text('Cài đặt', area=(0, 680, 250, 780)), wait_text('THÔNG BÁO'), tap_text('Nhắc việc', exact=True), wait_text('NHẮC TRƯỚC HẠN'))),
    S_(13, 'Mỗi loại việc có công tắc nhắc trước hạn. Tắt thì việc chỉ hiện trong chuông thông báo, không báo về điện thoại.',
       lambda: hl('NHẮC TRƯỚC HẠN', full_row=True, h=420)),
    S_(13, 'Bấm vào loại để chọn nhắc trước bao lâu: đúng giờ hạn, 15 phút, 30 phút, 1 giờ, 2 giờ, 4 giờ, hoặc 1 ngày. Mặc định là đúng giờ hạn.',
       lambda: (tap_text('Nhắc việc cá nhân'), w(1.5))),
    S_(13, 'Thay đổi được lưu ngay, không cần bấm Lưu.', lambda: (tap(200, 150), w(1.0))),
    S_(13, 'Bản tin sáng gửi lúc 7 giờ 30 mỗi ngày có việc. Nhắc việc chỉ có ngày mà không có giờ thì không nhắc riêng, chỉ nằm trong bản tin sáng. Việc quá hạn luôn được báo.',
       lambda: hl('Bản tin sáng', full_row=True, h=130)),
    # Kết
    S_(14, 'Đó là các chức năng chính của màn Việc của tôi, Nhắc việc cá nhân và Danh bạ cá nhân.'),
    S_(14, 'Cảm ơn các bạn đã xem video!'),
]

if __name__ == '__main__':
    if '--try' in sys.argv:
        i = sys.argv.index('--try')
        run(S, 'mytodo', only=(int(sys.argv[i + 1]), int(sys.argv[i + 2])))
    else:
        run(S, 'mytodo')
