#!/usr/bin/env python3
"""Video 2 — Đặt phòng họp khi tạo meeting (L = chủ trì namdangit, R = quản lý phòng thuydt). Dùng lại động cơ record.py."""
import datetime
import record as R
from record import tap, text, swipe, w, ocr, nz, tap_where, ensure_bell
from wheel import set_wheel

NAME = 'Họp kế hoạch quý IV'
KEY = 'ke hoach quy'
TOMORROW = (datetime.date.today() + datetime.timedelta(days=1)).day


def pick_card(rows):
    for x, y, bw, bh, t in sorted(rows, key=lambda r: r[1]):
        if KEY in nz(t) and any('len lich' in nz(t2) and abs(y2 - y) < 16 for _, y2, _, _, t2 in rows):
            return (round(x + bw / 2), round(y + bh / 2))
    return None


def pick_booking_noti(rows):
    """Thông báo 'Chờ duyệt' của phiếu đặt phòng (không phải yêu cầu dịch vụ) của cuộc họp mới."""
    rows = sorted(rows, key=lambda r: r[1])
    for x, y, bw, bh, t in rows:
        if 'cho duyet' not in nz(t):
            continue
        name = [r for r in rows if KEY in nz(r[4]) and 0 < r[1] - y < 40]
        if not name:
            continue
        ny = name[0][1]
        body = ' '.join(nz(r[4]) for r in rows if 0 < r[1] - ny < 45)
        if 'dich vu' in body:
            continue
        x2, y2, bw2, bh2, _ = name[0]
        return (round(x2 + bw2 / 2), round(y2 + bh2 / 2))
    return None


def tap_text(d, phrase, fallback):
    def pick(rows):
        for x, y, bw, bh, t in sorted(rows, key=lambda r: r[1]):
            if nz(phrase) in nz(t):
                return (round(x + bw / 2), round(y + bh / 2))
        return None
    tap_where(d, pick, fallback, tries=5)


def set_start():
    tap('L', 306, 373); w(1.6)
    set_wheel('L', 130, TOMORROW, 'date')
    set_wheel('L', 297, 9)
    w(0.6); tap('L', 375, 608)


ROOM_BLOCK = ('L', 20, 470, 362, 120)
S = [
    dict(ch='Mở đầu', say='Xin chào. Các bạn đang xem video hướng dẫn sử dụng Phần mềm quản trị ERP TPE.'),
    dict(ch='Mở đầu', say='Video này hướng dẫn đặt phòng họp ngay khi tạo cuộc họp trên ứng dụng di động, với cả phòng duyệt tự động và phòng cần người quản lý duyệt.'),
    dict(ch='Mở đầu', say='Bên trái là điện thoại của người chủ trì. Bên phải là điện thoại của người quản lý phòng họp.',
         mark=[('L', 0, 0, 402, 874), ('R', 0, 0, 402, 874)]),
    # ── Tạo cuộc họp
    dict(ch='Tạo cuộc họp', say='Ở phân hệ Meeting, người chủ trì bấm Tạo meeting, chọn họp Nội bộ.',
         act=lambda: (w(0.6), tap('L', 201, 787), w(2.2), tap('L', 296, 214))),
    dict(ch='Tạo cuộc họp', say='Chọn loại meeting và nhập tên cuộc họp.',
         act=lambda: (tap('L', 306, 255), w(2.0), tap('L', 120, 678), w(1.0), tap('L', 200, 343), w(0.8), text('L', NAME))),
    dict(ch='Tạo cuộc họp', say='Mở mục Thời gian, địa điểm và chủ trì. Ở ô Phòng họp, ứng dụng nhắc phải lưu cuộc họp trước rồi mới đăng ký phòng được.',
         act=lambda: (tap('L', 200, 628), w(1.2), swipe('L', 200, 650, 200, 250, 800)), mark=[('L', 14, 585, 374, 80)]),
    dict(ch='Tạo cuộc họp', say='Chọn ngày giờ họp, nằm trong giờ mở cửa của phòng. Giờ kết thúc tự lấy sau một tiếng.',
         act=set_start),
    dict(ch='Tạo cuộc họp', say='Bấm Tạo meeting. Cuộc họp được lưu ở trạng thái Đang tạo.',
         act=lambda: tap('L', 295, 805)),
    dict(ch='Tạo cuộc họp', say='Phòng họp chỉ đăng ký được khi cuộc họp đã lên lịch. Bấm Lên lịch.',
         act=lambda: (w(1.0), tap('L', 196, 805))),
    dict(ch='Tạo cuộc họp', say='Bấm Lên lịch để xác nhận.',
         act=lambda: (w(0.5), tap('L', 121, 542))),
    # ── Đăng ký phòng duyệt tự động
    dict(ch='Đăng ký phòng', say='Mở Danh sách meeting, gõ tên để tìm cuộc họp vừa tạo, rồi mở ra.',
         act=lambda: (w(1.0), tap('L', 270, 815), w(2.4), tap('L', 160, 139), w(0.8), text('L', 'quý IV'), w(3.0),
                      tap_where('L', pick_card, (200, 240)))),
    dict(ch='Đăng ký phòng', say='Vào Thông tin chung, mở mục Thời gian, địa điểm và chủ trì. Ô Phòng họp giờ đã có nút Đăng ký phòng.',
         act=lambda: (w(1.2), tap('L', 200, 420), w(2.4), tap('L', 200, 238)), mark=[('L', 20, 470, 362, 105)]),
    dict(ch='Đăng ký phòng', say='Bấm Đăng ký phòng. Ngày giờ lấy theo cuộc họp và được khoá lại, chỉ cần chọn phòng.',
         act=lambda: (tap('L', 117, 548), w(2.6)), mark=[('L', 12, 365, 380, 140)]),
    dict(ch='Đăng ký phòng', say='Bấm Chọn phòng. Danh sách hiện sức chứa, vị trí và tình trạng của từng phòng trong khung giờ họp.',
         act=lambda: (tap('L', 200, 320), w(2.4)), mark=[('L', 10, 640, 382, 200)]),
    dict(ch='Đăng ký phòng', say='Phòng họp tầng 3 duyệt tự động, đặt là có phòng ngay. Phòng VIP1 cần người quản lý phòng duyệt.',
         mark=[('L', 14, 650, 374, 90), ('L', 14, 745, 374, 85)]),
    dict(ch='Đăng ký phòng', say='Chọn Phòng họp tầng 3. Cần nước uống hay hoa quả thì bấm Thêm yêu cầu dịch vụ.',
         act=lambda: (tap('L', 200, 700), w(1.8), tap('L', 200, 565), w(2.2))),
    dict(ch='Đăng ký phòng', say='Chọn Nước uống, rồi nhập số lượng và ghi chú.',
         act=lambda: (tap('L', 100, 518), w(1.8), tap('L', 60, 642), w(0.6), text('L', '10'), w(0.5),
                      tap('L', 260, 642), w(0.6), text('L', 'Nước lọc'))),
    dict(ch='Đăng ký phòng', say='Bấm Gửi đặt phòng. Phòng duyệt tự động nên đăng ký xong là Đã duyệt ngay.',
         act=lambda: (w(0.6), tap('L', 295, 805), w(2.0)), mark=[ROOM_BLOCK]),
    dict(ch='Đăng ký phòng', say='Người quản lý phòng nhận thông báo có yêu cầu dịch vụ, để chuẩn bị trước buổi họp.',
         mark=[('R', 8, 50, 386, 110)]),
    # ── Phòng cần duyệt
    dict(ch='Phòng cần duyệt', say='Giả sử cần phòng lớn hơn. Bấm Đổi phòng.',
         act=lambda: (w(0.6), tap_text('L', 'Đổi phòng', (100, 580)), w(2.6))),
    dict(ch='Phòng cần duyệt', say='Chọn Phòng VIP1. Phòng này cần người quản lý duyệt.',
         act=lambda: (tap('L', 200, 302), w(2.4), tap_text('L', 'Phòng VIP1', (200, 769)), w(1.8))),
    dict(ch='Phòng cần duyệt', say='Bấm Gửi đặt phòng. Hệ thống báo phiếu sẽ ở trạng thái Chờ duyệt, cho tới khi người quản lý duyệt.',
         act=lambda: (w(0.6), tap('L', 295, 805)), mark=[('L', 28, 330, 346, 250)]),
    dict(ch='Phòng cần duyệt', say='Bấm Gửi đặt phòng để xác nhận. Phòng chuyển sang Chờ duyệt.',
         act=lambda: (w(0.5), tap('L', 120, 532), w(1.5)), mark=[ROOM_BLOCK]),
    # ── Quản lý duyệt
    dict(ch='Quản lý duyệt', say='Điện thoại người quản lý phòng nhận ngay thông báo Đặt phòng họp đang chờ duyệt.',
         mark=[('R', 8, 50, 386, 110)]),
    dict(ch='Quản lý duyệt', say='Người quản lý mở ứng dụng, rồi bấm vào biểu tượng chuông.',
         act=lambda: (w(0.6), tap('R', 339, 233), w(2.4), ensure_bell())),
    dict(ch='Quản lý duyệt', say='Bấm vào thông báo đặt phòng. Ứng dụng mở màn Duyệt phiếu đặt phòng.',
         act=lambda: (w(0.8), tap_where('R', pick_booking_noti, (200, 482)), w(2.5))),
    dict(ch='Quản lý duyệt', say='Phiếu chờ duyệt ghi rõ phòng, giờ họp và người đặt. Có hai nút: Từ chối, và Duyệt.',
         mark=[('R', 14, 205, 374, 180)]),
    dict(ch='Quản lý duyệt', say='Bấm Duyệt. Hệ thống hỏi lại trước khi duyệt.',
         act=lambda: (tap('R', 288, 360), w(1.2))),
    dict(ch='Quản lý duyệt', say='Bấm Duyệt để xác nhận. Người chủ trì nhận ngay thông báo Đặt phòng họp đã được duyệt.',
         act=lambda: (w(0.5), tap('R', 120, 542)), mark=[('L', 8, 50, 386, 110)]),
    # ── Kết quả
    dict(ch='Kết quả', say='Phía chủ trì, quay lại màn chi tiết cuộc họp và kéo xuống để tải lại. Phòng VIP1 đã được duyệt.',
         act=lambda: (w(2.5), tap('L', 36, 86), w(2.4), swipe('L', 200, 300, 200, 650, 700), w(2.0)),
         mark=[('L', 0, 248, 402, 76)]),
    dict(ch='Kết', say='Đó là cách đặt phòng họp khi tạo cuộc họp, với phòng duyệt tự động và phòng cần người quản lý duyệt.'),
    dict(ch='Kết', say='Cảm ơn các bạn đã xem video!'),
]

if __name__ == '__main__':
    R.S = S
    R.main()
